import os
import numpy
import pandas
import copy

import utils.log as log
import parameters.assignment as param
import parameters.zone as zone_param
from assignment.datatypes.car_specification import CarSpecification
from assignment.datatypes.transit import TransitSpecification
from assignment.datatypes.path_analysis import PathAnalysis
from assignment.abstract_assignment import Period


class AssignmentPeriod(Period):
    def __init__(self, name, emme_scenario, emme_context,
                 demand_mtx=param.emme_demand_mtx,
                 result_mtx=param.emme_result_mtx, save_matrices=False,
                 separate_emme_scenarios=False):
        self.name = name
        self.emme_scenario = emme_context.modeller.emmebank.scenario(
            emme_scenario)
        self.emme_project = emme_context
        self._separate_emme_scenarios = separate_emme_scenarios
        if save_matrices:
            self.demand_mtx = copy.deepcopy(demand_mtx)
            self.result_mtx = copy.deepcopy(result_mtx)
        else:
            # Refer to the same matrices for all time periods
            self.demand_mtx = demand_mtx
            self.result_mtx = result_mtx
        self.dist_unit_cost = param.dist_unit_cost

    def extra(self, attr):
        """Add prefix "@" and time-period suffix.

        Parameters
        ----------
        attr : str
            Attribute string to modify

        Returns
        -------
        str
            Modified string
        """
        return "@{}_{}".format(attr, self.name)

    def prepare(self, segment_results):
        """Prepare network for assignment.

        Calculate road toll cost, set boarding penalties,
        and add buses to background traffic.

        Parameters
        ----------
        segment_results : dict
            key : str
                Transit class (transit_work/transit_leisure)
            value : dict
                key : str
                    Segment result (transit_volumes/...)
                value : str
                    Extra attribute name (@transit_work_vol_aht/...)
        """
        self._segment_results = segment_results
        self._calc_road_cost()
        self._calc_boarding_penalties()
        self._calc_background_traffic()
        self._specify()

    def assign(self, matrices, iteration):
        """Assign cars, bikes and transit for one time period.

        Get travel impedance matrices for one time period from assignment.

        Parameters
        ----------
        matrices : dict
            Assignment class (car_work/transit/...) : numpy 2-d matrix
        iteration : int or str
            Iteration number (0, 1, 2, ...) or "init" or "last"

        Returns
        -------
        dict
            Type (time/cost/dist) : dict
                Assignment class (car_work/transit/...) : numpy 2-d matrix
        """
        self._set_emmebank_matrices(matrices, iteration=="last")
        if iteration=="init":
            self._assign_pedestrians()
            self._set_bike_vdfs()
            self._assign_bikes(self.result_mtx["dist"]["bike"]["id"], "all")
            self._set_car_and_transit_vdfs()
            if not self._separate_emme_scenarios:
                self._calc_background_traffic()
            self._assign_cars(param.stopping_criteria_coarse)
            self._calc_extra_wait_time()
            self._assign_transit()
        elif iteration==0:
            self._set_car_and_transit_vdfs()
            if not self._separate_emme_scenarios:
                self._calc_background_traffic()
            self._assign_cars(param.stopping_criteria_coarse)
            self._calc_extra_wait_time()
            self._assign_transit()
        elif iteration==1:
            if not self._separate_emme_scenarios:
                self._set_car_and_transit_vdfs()
                self._calc_background_traffic()
            self._assign_cars(param.stopping_criteria_coarse)
            self._calc_extra_wait_time()
            self._assign_transit()
            self._calc_background_traffic(include_trucks=True)
        elif isinstance(iteration, int) and iteration>1:
            if not self._separate_emme_scenarios:
                self._set_car_and_transit_vdfs()
                self._calc_background_traffic(include_trucks=True)
            self._assign_cars(
                param.stopping_criteria_coarse, lightweight=True)
            self._calc_extra_wait_time()
            self._assign_transit()
        elif iteration=="last":
            self._set_bike_vdfs()
            self._assign_bikes(self.result_mtx["dist"]["bike"]["id"], "all")
            self._set_car_and_transit_vdfs()
            self._calc_background_traffic()
            self._assign_cars(param.stopping_criteria_fine)
            self._calc_boarding_penalties(is_last_iteration=True)
            self._calc_extra_wait_time()
            self._assign_congested_transit()
        else:
            raise ValueError("Iteration number not valid")

        mtxs = {imp_type: self._get_matrices(imp_type, iteration=="last")
            for imp_type in ("time", "cost", "dist")}
        # fix the emme path analysis results
        # (dist and cost are zero if path not found but we want it to
        # be the default value 999999)
        for mtx_type in ("cost", "dist"):
            for mtx_class in mtxs[mtx_type]:
                path_not_found = mtxs["time"][mtx_class] > 999999
                mtxs[mtx_type][mtx_class][path_not_found] = 999999
        if iteration == "last":
            for mtx_class in ("trailer_truck", "truck"):
                # toll costs are not applied to freight, but the cost
                # matrix is automatically populated with default values
                # (999999) so we need to manually fill it with zeroes
                path_found = mtxs["time"][mtx_class] <= 999999
                mtxs["cost"][mtx_class][path_found] = 0
        # adjust impedance
        mtxs["time"]["bike"] = mtxs["time"]["bike"].clip(None, 9999.)
        if iteration != "last":
            for ass_cl in ("car_work", "car_leisure"):
                mtxs["cost"][ass_cl] += self.dist_unit_cost * mtxs["dist"][ass_cl]
        return mtxs

    def calc_transit_cost(self, fares, peripheral_cost, mapping):
        """Calculate transit zone cost matrix.
        
        Perform multiple transit assignments.
        For each assignment, check if a specific zone has been visited
        by the OD-pair flows. For all the zones that are visited, 
        check if there is a zone combination fare that includes them all.
        If not, distance fare is applied.

        Some fares can be exclusively for municipality citizens
        (i.e., tours starting in that municipality).
        
        Parameters
        ----------
        fares : assignment.datatypes.transit_fare.TransitFareZoneSpecification
            Transit fare zone specification
        peripheral_cost : numpy 2-d matrix
            Fixed cost matrix for peripheral zones
        mapping : dict
            Dictionary of zone numbers and corresponding indices
        """
        # Move transfer penalty to boarding penalties,
        # a side effect is that it then also affects first boarding
        self._calc_boarding_penalties(5)
        has_visited = {}
        network = self.emme_scenario.get_network()
        transit_zones = {node.label for node in network.nodes()}
        tc = "transit_work"
        spec = TransitSpecification(
            self._segment_results[tc], self.extra("hw"),
            self.demand_mtx[tc]["id"],
            self.result_mtx["time"][tc]["id"],
            self.result_mtx["dist"][tc]["id"],
            self.result_mtx["trip_part_"+tc],
            count_zone_boardings=True)
        is_in_transit_zone_attr = param.is_in_transit_zone_attr.replace(
            "ui", "data")
        for transit_zone in transit_zones:
            # Set tag to 1 for nodes in transit zone and 0 elsewhere
            for node in network.nodes():
                node[is_in_transit_zone_attr] = (node.label == transit_zone)
            self.emme_scenario.publish_network(network)
            # Transit assignment with zone tag as weightless boarding cost
            self.emme_project.transit_assignment(
                specification=spec.transit_spec, scenario=self.emme_scenario,
                save_strategies=True)
            self.emme_project.matrix_results(
                spec.transit_result_spec, self.emme_scenario)
            nr_visits = self._get_matrix(
                "trip_part_transit_work", "board_cost")
            # If the number of visits is less than 1, there seems to
            # be an easy way to avoid visiting this transit zone
            has_visited[transit_zone] = (nr_visits > 0.99)
        for centroid in network.centroids():
            # Add transit zone of destination to visited
            has_visited[centroid.label][:, mapping[centroid.number]] = True
        maxfare = 999
        cost = numpy.full_like(nr_visits, maxfare)
        mtx = next(iter(has_visited.values()))
        for zone_combination in fares.zone_fares:
            goes_outside = numpy.full_like(mtx, False)
            for transit_zone in has_visited:
                # Check if the OD-flow has been at a node that is
                # outside of this zone combination
                if transit_zone not in zone_combination:
                    goes_outside |= has_visited[transit_zone]
            is_inside = ~goes_outside
            if zone_combination in fares.exclusive:
                # Calculate fares exclusive for municipality citizens
                exclusion = pandas.DataFrame(
                    is_inside, self.emme_scenario.zone_numbers,
                    self.emme_scenario.zone_numbers)
                municipality = fares.exclusive[zone_combination]
                inclusion = zone_param.municipalities[municipality]
                exclusion.loc[:inclusion[0]-1] = False
                exclusion.loc[inclusion[1]+1:] = False
                is_inside = exclusion.values
            zone_fare = fares.zone_fares[zone_combination]
            # If OD-flow matches several combinations, pick cheapest
            cost[is_inside] = numpy.minimum(cost[is_inside], zone_fare)
        # Replace fare for peripheral zones with fixed matrix
        bounds = zone_param.areas["peripheral"]
        zn = pandas.Index(self.emme_scenario.zone_numbers)
        l, u = zn.slice_locs(bounds[0], bounds[1])
        cost[l:u, :u] = peripheral_cost
        cost[:u, l:u] = peripheral_cost.T
        # Calculate distance-based cost from inv-distance
        dist = self._get_matrix("dist", "transit_work")
        dist_cost = fares.start_fare + fares.dist_fare*dist
        cost[cost>=maxfare] = dist_cost[cost>=maxfare]
        # Reset boarding penalties
        self._calc_boarding_penalties()
        return cost

    def transit_results_links_nodes(self):
        """
        Calculate and sum transit results to link and nodes.
        """
        network = self.emme_scenario.get_network()
        segres = self._segment_results
        for tc in segres:
            for res in segres[tc]:
                nodeattr = self.extra(tc[:10]+"n_"+param.segment_results[res])
                for segment in network.transit_segments():
                    if res == "transit_volumes":
                        if segment.link is not None:
                            segment.link[self.extra(tc)] += segment[segres[tc][res]]
                    else:
                        segment.i_node[nodeattr] += segment[segres[tc][res]]
        self.emme_scenario.publish_network(network)

    def _set_car_and_transit_vdfs(self):
        log.info("Sets car and transit functions for scenario {}".format(
            self.emme_scenario.id))
        network = self.emme_scenario.get_network()
        transit_modesets = {modes[0]: {network.mode(m) for m in modes[1]}
            for modes in param.transit_delay_funcs}
        main_mode = network.mode(param.main_mode)
        car_mode = network.mode(param.assignment_modes["car_work"])
        for link in network.links():
            # Car volume delay function definition
            linktype = link.type % 100
            if linktype in param.roadclasses:
                # Car link with standard attributes
                roadclass = param.roadclasses[linktype]
                link.volume_delay_func = roadclass.volume_delay_func
                link.data1 = roadclass.lane_capacity
                link.data2 = roadclass.free_flow_speed
            elif linktype in param.custom_roadtypes:
                # Custom car link
                link.volume_delay_func = linktype - 90
                for linktype in param.roadclasses:
                    roadclass = param.roadclasses[linktype]
                    if (link.volume_delay_func == roadclass.volume_delay_func
                            and link.data2 > roadclass.free_flow_speed-1):
                        # Find the most appropriate road class
                        break
            else:
                # Link with no car traffic
                link.volume_delay_func = 0

            # Transit function definition
            for modeset in param.transit_delay_funcs:
                # Check that intersection is not empty,
                # hence that mode is active on link
                if transit_modesets[modeset[0]] & link.modes:
                    funcs = param.transit_delay_funcs[modeset]
                    if modeset[0] == "bus":
                        buslane_code = link.type // 100
                        if buslane_code in param.bus_lane_link_codes[self.name]:
                            # Bus lane
                            if (link.num_lanes == 3
                                    and roadclass.num_lanes == ">=3"):
                                roadclass = param.roadclasses[linktype - 1]
                                link.data1 = roadclass.lane_capacity
                            link.volume_delay_func += 5
                            func = funcs["buslane"]
                            try:
                                bus_delay = (param.buslane_delay
                                             / max(roadclass.free_flow_speed, 30))
                            except UnboundLocalError:
                                log.warn("Bus mode on link {}, type {}".format(
                                    link.id, link.type))
                        else:
                            # No bus lane
                            func = funcs["no_buslane"]
                            try:
                                bus_delay = roadclass.bus_delay
                            except UnboundLocalError:
                                log.warn("Bus mode on link {}, type {}".format(
                                    link.id, link.type))
                        for segment in link.segments():
                            segment.data2 = bus_delay
                    else:
                        func = funcs[self.name]
                    break
            for segment in link.segments():
                segment.transit_time_func = func
            if car_mode in link.modes:
                link.modes |= {main_mode}
            elif main_mode in link.modes:
                link.modes -= {main_mode}
        self.emme_scenario.publish_network(network)

    def _set_bike_vdfs(self):
        log.info("Sets bike functions for scenario {}".format(
            self.emme_scenario.id))
        network = self.emme_scenario.get_network()
        main_mode = network.mode(param.main_mode)
        bike_mode = network.mode(param.bike_mode)
        for link in network.links():
            linktype = link.type % 100
            if linktype in param.roadclasses:
                roadtype = param.roadclasses[linktype].type
            elif linktype in param.custom_roadtypes:
                roadtype = param.custom_roadtypes[linktype]
            else:
                roadtype = None
            if (roadtype == "motorway" and network.mode('f') in link.modes
                    and link["@pyoratieluokka"] == 0):
                # Force bikes on motorways onto separate bikepaths
                link["@pyoratieluokka"] = 3
            try:
                pathclass = param.bikepath_vdfs[int(link["@pyoratieluokka"])]
                if roadtype in pathclass:
                    link.volume_delay_func = pathclass[roadtype]
                else:
                    link.volume_delay_func = pathclass[None]
            except KeyError:
                link.volume_delay_func = 98
            if bike_mode in link.modes:
                link.modes |= {main_mode}
            elif main_mode in link.modes:
                link.modes -= {main_mode}
        self.emme_scenario.publish_network(network)

    def _set_emmebank_matrices(self, matrices, is_last_iteration):
        """Set matrices in emmebank.

        Bike matrices are added together, so that only one matrix is to be
        assigned. Similarly, transit matrices are added together if not last
        iteration. However, they are placed in the matrix "transit_work" to
        save space.

        Parameters
        ----------
        matrices : dict
            Assignment class (car_work/transit/...) : numpy 2-d matrix
        is_last_iteration : bool
            Whether this is the end (multiclass congested transit) assignment
        """
        tmp_mtx = {
            "bike": 0,
        }
        if not is_last_iteration:
            tmp_mtx["transit"] = 0
        for mtx in matrices:
            mode = mtx.split('_')[0]
            if mode in tmp_mtx:
                tmp_mtx[mode] += matrices[mtx]
                if mode == "transit":
                    self._set_matrix("transit_work", tmp_mtx[mode])
                else:
                    self._set_matrix(mode, tmp_mtx[mode])
            else:
                self._set_matrix(mtx, matrices[mtx])

    def _set_matrix(self, mtx_label, matrix, result_type=None):
        if numpy.isnan(matrix).any():
            msg = ("NAs in demand matrix {}. ".format(mtx_label)
                   + "Would cause infinite loop in Emme assignment.")
            log.error(msg)
            raise ValueError(msg)
        elif result_type is None:
            self.emme_project.modeller.emmebank.matrix(
                self.demand_mtx[mtx_label]["id"]).set_numpy_data(matrix)
        else:
            self.emme_project.modeller.emmebank.matrix(
                self.result_mtx[result_type][mtx_label]["id"]).set_numpy_data(matrix)

    def _get_matrices(self, mtx_type, is_last_iteration=False):
        """Get all matrices of specified type.

        Parameters
        ----------
        mtx_type : str
            Type (demand/time/transit/...)
        is_last_iteration : bool (optional)
            If this is the last iteration, all matrices are returned,
            otherwise freight impedance matrices are skipped

        Return
        ------
        dict
            Subtype (car_work/truck/inv_time/...) : numpy 2-d matrix
                Matrix of the specified type
        """
        last_iteration_classes = param.freight_classes + ("transit_leisure",)
        matrices = {}
        for subtype in self.result_mtx[mtx_type]:
            if is_last_iteration or subtype not in last_iteration_classes:
                if mtx_type == "time" and subtype in param.assignment_modes:
                    mtx = self._extract_timecost_from_gcost(subtype)
                elif mtx_type == "time" and subtype in param.transit_classes:
                    mtx = self._damp_travel_time(subtype)
                else:
                    mtx = self._get_matrix(mtx_type, subtype)
                matrices[subtype] = mtx
        if not is_last_iteration:
            matrices["transit_leisure"] = matrices["transit_work"]
        return matrices

    def _get_matrix(self, assignment_result_type, subtype):
        """Get matrix with type pair (e.g., demand, car_work).

        Parameters
        ----------
        assignment_result_type : str
            Type (demand/time/transit/...)
        subtype : str
            Subtype (car_work/truck/inv_time/...)

        Return
        ------
        numpy 2-d matrix
            Matrix of the specified type
        """
        emme_id = self.result_mtx[assignment_result_type][subtype]["id"]
        return (self.emme_project.modeller.emmebank.matrix(emme_id)
                .get_numpy_data())

    def _damp_travel_time(self, demand_type):
        """Reduce the impact from first waiting time on total travel time."""
        travel_time = self._get_matrix("time", demand_type)
        fw_time = self._get_matrix("trip_part_"+demand_type, "fw_time")
        wt_weight = param.waiting_time_perception_factor
        return travel_time + wt_weight*((5./3.*fw_time)**0.8 - fw_time)

    def _extract_timecost_from_gcost(self, ass_class):
        """Remove monetary cost from generalized cost.

        Traffic assignment produces a generalized cost matrix.
        To get travel time, monetary cost is removed from generalized cost.
        """
        vot_inv = param.vot_inv[param.vot_classes[ass_class]]
        gcost = self._get_matrix("gen_cost", ass_class)
        cost = self._get_matrix("cost", ass_class)
        dist = self._get_matrix("dist", ass_class)
        if ass_class in ("trailer_truck", "truck"):
            # toll costs are not applied to freight
            time = gcost - vot_inv*param.freight_dist_unit_cost[ass_class]*dist
        else:
            time = gcost - vot_inv*(cost + self.dist_unit_cost*dist)
        self._set_matrix(ass_class, time, "time")
        return time

    def _calc_background_traffic(self, include_trucks=False):
        """Calculate background traffic (buses)."""
        network = self.emme_scenario.get_network()
        # emme api has name "data3" for ul3
        background_traffic = param.background_traffic_attr.replace(
            "ul", "data")
        # calc @bus and data3
        heavy = (self.extra("truck"), self.extra("trailer_truck"))
        for link in network.links():
            if link.type > 100: # If car or bus link
                freq = 0
                for segment in link.segments():
                    segment_hdw = segment.line[self.extra("hw")]
                    if 0 < segment_hdw < 900:
                        freq += 60 / segment_hdw
                link[self.extra("bus")] = freq
                if link.type // 100 in param.bus_lane_link_codes[self.name]:
                    # Bus lane
                    link[background_traffic] = 0
                else:
                    link[background_traffic] = freq
                if include_trucks:
                    for ass_class in heavy:
                        link[background_traffic] += link[ass_class]
        self.emme_scenario.publish_network(network)

    def _calc_road_cost(self):
        """Calculate road charges and driving costs for one scenario."""
        log.info("Calculates road charges for time period {}...".format(self.name))
        network = self.emme_scenario.get_network()
        for link in network.links():
            toll_cost = link.length * link[self.extra("hinta")]
            dist_cost = self.dist_unit_cost * link.length
            link[self.extra("toll_cost")] = toll_cost
            link[self.extra("total_cost")] = toll_cost + dist_cost
        self.emme_scenario.publish_network(network)

    def _calc_boarding_penalties(self, extra_penalty=0, is_last_iteration=False):
        """Calculate boarding penalties for transit assignment."""
        # Definition of line specific boarding penalties
        network = self.emme_scenario.get_network()
        if is_last_iteration:
            penalty = param.last_boarding_penalty
        else:
            penalty = param.boarding_penalty
        missing_penalties = set()
        penalty_attr = param.boarding_penalty_attr.replace("ut", "data")
        for line in network.transit_lines():
            try:
                line[penalty_attr] = penalty[line.mode.id] + extra_penalty
            except KeyError:
                missing_penalties.add(line.mode.id)
        if missing_penalties:
            missing_penalties = ", ".join(missing_penalties)
            log.warn("No boarding penalty found for transit modes " + missing_penalties)
        self.emme_scenario.publish_network(network)

    def _specify(self):
        self._car_spec = CarSpecification(
            self.extra, self.demand_mtx, self.result_mtx)
        self._transit_specs = {tc: TransitSpecification(
                self._segment_results[tc], self.extra("hw"),
                self.demand_mtx[tc]["id"],
                self.result_mtx["time"][tc]["id"],
                self.result_mtx["dist"][tc]["id"],
                self.result_mtx["trip_part_"+tc])
            for tc in param.transit_classes}
        self.bike_spec = {
            "type": "STANDARD_TRAFFIC_ASSIGNMENT",
            "classes": [
                {
                    "mode": param.main_mode,
                    "demand": self.demand_mtx["bike"]["id"],
                    "results": {
                        "od_travel_times": {
                            "shortest_paths": self.result_mtx["time"]["bike"]["id"],
                        },
                        "link_volumes": None, # This is defined later
                    },
                    "analysis": {
                        "results": {
                            "od_values": None, # This is defined later
                        },
                    },
                }
            ],
            "path_analysis": PathAnalysis("ul3").spec,
            "stopping_criteria": {
                "max_iterations": 1,
                "best_relative_gap": 1,
                "relative_gap": 1,
                "normalized_gap": 1,
            },
            "performance_settings": param.performance_settings
        }
        self.walk_spec = {
            "type": "STANDARD_TRANSIT_ASSIGNMENT",
            "modes": param.aux_modes,
            "demand": self.demand_mtx["bike"]["id"],
            "waiting_time": {
                "headway_fraction": 0.01,
                "effective_headways": "hdw",
                "perception_factor": 0,
            },
            "boarding_time": {
                "penalty": 0,
                "perception_factor": 0,
            },
            "aux_transit_time": {
                "perception_factor": 1,
            },
            "od_results": {
                "transit_times": self.result_mtx["time"]["walk"]["id"],
            },
            "strategy_analysis": {
                "sub_path_combination_operator": "+",
                "sub_strategy_combination_operator": "average",
                "trip_components": {
                    "aux_transit": "length",
                },
                "selected_demand_and_transit_volumes": {
                    "sub_strategies_to_retain": "ALL",
                    "selection_threshold": {
                        "lower": None,
                        "upper": None,
                    },
                },
                "results": {
                    "od_values": self.result_mtx["dist"]["walk"]["id"],
                },
            },
        }

    def _assign_cars(self, stopping_criteria, lightweight=False):
        """Perform car_work traffic assignment for one scenario."""
        log.info("Car assignment started...")
        car_spec = self._car_spec.spec(lightweight)
        car_spec["stopping_criteria"] = stopping_criteria
        assign_report = self.emme_project.car_assignment(
            car_spec, self.emme_scenario)
        network = self.emme_scenario.get_network()
        time_attr = self.extra("car_time")
        for link in network.links():
            link[time_attr] = link.auto_time
        self.emme_scenario.publish_network(network)
        log.info("Car assignment performed for scenario {}".format(
            self.emme_scenario.id))
        log.info("Stopping criteria: {}, iteration {} / {}".format(
            assign_report["stopping_criterion"],
            assign_report["iterations"][-1]["number"],
            stopping_criteria["max_iterations"]
            ))
        if assign_report["stopping_criterion"] == "MAX_ITERATIONS":
            log.warn("Car assignment not fully converged.")
    
    def _assign_bikes(self, length_mat_id, length_for_links):
        """Perform bike traffic assignment for one scenario."""
        scen = self.emme_scenario
        spec = self.bike_spec
        spec["classes"][0]["results"]["link_volumes"] = self.extra("bike")
        spec["classes"][0]["analysis"]["results"]["od_values"] = length_mat_id
        # Reset ul3 to zero
        netw_spec = {
            "type": "NETWORK_CALCULATION",
            "selections": {
                "link": "all",
            },
            "expression": "0",
            "result": spec["path_analysis"]["link_component"],
            "aggregation": None,
        }
        self.emme_project.network_calc(netw_spec, scen)
        # Define for which links to calculate length and save in ul3
        netw_spec = {
            "type": "NETWORK_CALCULATION",
            "selections": {
                "link": length_for_links,
            },
            "expression": "length",
            "result": spec["path_analysis"]["link_component"],
            "aggregation": None,
        }
        self.emme_project.network_calc(netw_spec, scen)
        log.info("Bike assignment started...")
        self.emme_project.bike_assignment(
            specification=spec, scenario=scen)
        log.info("Bike assignment performed for scenario " + str(scen.id))

    def _assign_pedestrians(self):
        """Perform pedestrian assignment for one scenario."""
        log.info("Pedestrian assignment started...")
        self.emme_project.pedestrian_assignment(
            specification=self.walk_spec, scenario=self.emme_scenario)
        log.info("Pedestrian assignment performed for scenario " + str(self.emme_scenario.id)) 

    def _calc_extra_wait_time(self):
        """Calculate extra waiting time for one scenario."""
        network = self.emme_scenario.get_network()
        # Calculation of cumulative line segment travel time and speed
        log.info("Calculates cumulative travel times for scenario " + str(self.emme_scenario.id))
        for line in network.transit_lines():
            cumulative_length = 0
            cumulative_time = 0
            cumulative_speed = 0
            headway_sd = 0
            for segment in line.segments():
                cumulative_length += segment.link.length
                # Travel time for buses in mixed traffic
                if segment.transit_time_func == 1:
                    cumulative_time += (segment.data2 * segment.link.length
                                        # + segment.link["@timau"]
                                        + segment.link.auto_time
                                        + segment.dwell_time)
                # Travel time for buses on bus lanes
                if segment.transit_time_func == 2:
                    cumulative_time += (segment.data2 * segment.link.length
                                        + segment.dwell_time)
                # Travel time for trams AHT
                if segment.transit_time_func == 3:
                    speedstr = str(int(segment.link.data1))
                    # Digits 5-6 from end (1-2 from beg.) represent AHT
                    # speed. If AHT speed is less than 10, data1 will 
                    # have only 5 digits.
                    speed = int(speedstr[:-4])
                    cumulative_time += ((segment.link.length / speed) * 60
                                        + segment.dwell_time)
                # Travel time for trams PT
                if segment.transit_time_func == 4:
                    speedstr = str(int(segment.link.data1))
                    # Digits 3-4 from end represent PT speed.
                    speed = int(speedstr[-4:-2])
                    cumulative_time += ((segment.link.length / speed) * 60
                                        + segment.dwell_time)
                # Travel time for trams IHT
                if segment.transit_time_func == 5:
                    speedstr = str(int(segment.link.data1))
                    # Digits 1-2 from end represent IHT speed.
                    speed = int(speedstr[-2:])
                    cumulative_time += ((segment.link.length / speed) * 60
                                        + segment.dwell_time)
                if cumulative_time > 0:
                    cumulative_speed = (cumulative_length
                                        / cumulative_time
                                        * 60)
                # Headway standard deviation for buses and trams
                if line.mode.id in param.headway_sd_func:
                    b = param.headway_sd_func[line.mode.id]
                    headway_sd = (b["asc"]
                                  + b["ctime"]*cumulative_time
                                  + b["cspeed"]*cumulative_speed)
                # Estimated waiting time addition caused by headway deviation
                segment["@wait_time_dev"] = headway_sd**2 / (2.0*line.headway)
        self.emme_scenario.publish_network(network)

    def _assign_transit(self):
        """Perform transit assignment for one scenario."""
        log.info("Transit assignment started...")
        # Here we assign all transit in one class, multi-class assignment is
        # performed in last iteration (congested assignment)
        spec = self._transit_specs["transit_work"]
        self.emme_project.transit_assignment(
            specification=spec.transit_spec, scenario=self.emme_scenario,
            save_strategies=True)
        self.emme_project.matrix_results(spec.transit_result_spec, scenario=self.emme_scenario)
        log.info("Transit assignment performed for scenario {}".format(
            str(self.emme_scenario.id)))

    def _assign_congested_transit(self):
        """Perform congested transit assignment for one scenario."""
        log.info("Congested transit assignment started...")
        network = self.emme_scenario.get_network()
        headway_attr = self.extra("hw")
        penalty_attr = param.inactive_line_penalty_attr.replace("ut", "data")
        for line in network.transit_lines():
            line.headway = line[headway_attr]
            if line[headway_attr] > 900:
                line[penalty_attr] = 9999
            else:
                line[penalty_attr] = 0
        self.emme_scenario.publish_network(network)
        specs = self._transit_specs
        for transit_class in specs:
            spec = specs[transit_class].transit_spec
            (spec["journey_levels"][1]["boarding_cost"]["global"]
                 ["penalty"]) = param.transfer_penalty[transit_class]
            spec["in_vehicle_cost"] = {
                "penalty": param.inactive_line_penalty_attr,
                "perception_factor": 1,
            }
        assign_report = self.emme_project.congested_assignment(
            transit_assignment_spec=[specs[tc].transit_spec for tc in specs],
            class_names=list(specs),
            congestion_function=param.trass_func,
            stopping_criteria=param.trass_stop,
            log_worksheets=False, scenario=self.emme_scenario,
            save_strategies=True)
        # save results for both classes
        for tc in specs:
            self.emme_project.matrix_results(
                specs[tc].transit_result_spec, scenario=self.emme_scenario,
                class_name=tc)
            self.emme_project.network_results(
                specs[tc].ntw_results_spec, scenario=self.emme_scenario,
                class_name=tc)
        base_timtr = param.uncongested_transit_time
        time_attr = self.extra(base_timtr)
        volax_attr = self.extra("aux_transit")
        network = self.emme_scenario.get_network()
        for link in network.links():
            link[volax_attr] = link.aux_transit_volume
        for segment in network.transit_segments():
            segment[time_attr] = segment['@'+base_timtr]
        self.emme_scenario.publish_network(network)
        log.info("Congested transit assignment performed for scenario {}".format(
            str(self.emme_scenario.id)))
        log.info("Stopping criteria: {}, iteration {} / {}".format(
            assign_report["stopping_criteria"],
            assign_report["iterations"][-1]["number"],
            param.trass_stop["max_iterations"]
            ))
        if assign_report["stopping_criteria"] == "MAX_ITERATIONS":
            log.warn("Congested transit assignment not fully converged.")
