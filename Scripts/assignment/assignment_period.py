import os
import numpy
import copy

import utils.log as log
import parameters.assignment as param
from datatypes.car_specification import CarSpecification
from datatypes.path_analysis import PathAnalysis


class AssignmentPeriod:
    def __init__(self, emme_scenario, emme_context,
                 demand_mtx=param.emme_demand_mtx,
                 result_mtx=param.emme_result_mtx,
                 save_matrices=False):
        self.emme_scenario_id = emme_scenario
        self.emme_scenario = emme_context.modeller.emmebank.scenario(
            emme_scenario)
        self.emme_project = emme_context
        self.save_matrices = save_matrices
        if save_matrices:
            self.demand_mtx = copy.deepcopy(demand_mtx)
            self.result_mtx = copy.deepcopy(result_mtx)
        else:
            # Refer to the same matrices for all time periods
            self.demand_mtx = demand_mtx
            self.result_mtx = result_mtx
        self.dist_unit_cost = param.dist_unit_cost

    def prepare(self):
        """Create attributes needed in assignment."""
        for attr in param.emme_attributes.keys():
            extr = self.emme_project.create_extra_attribute(
                extra_attribute_type=param.emme_attributes[attr],
                extra_attribute_name=attr,
                extra_attribute_description="HM40 results attr",
                extra_attribute_default_value=0,
                overwrite=True,
                scenario=self.emme_scenario)
            log.debug("Created attr {} for scen {}".format(
                extr.name, self.emme_scenario))
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
        log.info("Assignment starts...")
        self.set_emmebank_matrices(matrices, iteration=="last")
        if iteration=="init":
            self._assign_pedestrians()
            self._assign_bikes(
                self.bike_scenario,
                self.result_mtx["dist"]["bike"]["id"],
                "all")
            self._assign_cars(param.stopping_criteria_coarse)
            self._calc_extra_wait_time()
            self._assign_transit()
        elif iteration==0:
            self._assign_cars(param.stopping_criteria_coarse)
            self._calc_extra_wait_time()
            self._assign_transit()
        elif iteration==1:
            self._assign_cars(param.stopping_criteria_coarse)
            self._calc_extra_wait_time()
            self._assign_transit()
            self._calc_background_traffic(include_trucks=True)
        elif isinstance(iteration, int) and iteration>1:
            self._assign_cars(
                param.stopping_criteria_coarse, lightweight=True)
            self._calc_extra_wait_time()
            self._assign_transit()
        elif iteration=="last":
            self._calc_background_traffic()
            self._assign_cars(param.stopping_criteria_fine)
            self._calc_boarding_penalties(is_last_iteration=True)
            self._calc_extra_wait_time()
            self._assign_congested_transit(param.transit_classes)
            self._assign_bikes(
                self.bike_scenario,
                self.result_mtx["dist"]["bike"]["id"],
                "all")
        else:
            raise ValueError("Iteration number not valid")

        impedance_types = ("time", "dist", "cost")
        mtxs = {imp_type: self.get_emmebank_matrices(imp_type, iteration=="last")
            for imp_type in impedance_types}
        # fix the emme path analysis results (dist and cost zero if path not found)
        for mtx_type in mtxs:
            for mtx_class in mtxs[mtx_type]:
                mtxs[mtx_type][mtx_class][ mtxs["time"][mtx_class] > 999999 ] = 999999
        # adjust impedance
        mtxs["time"]["bike"] = mtxs["time"]["bike"].clip(None, 9999.)
        mtxs["time"]["car_work"] = self._extract_timecost_from_gcost(
            "car_work")
        mtxs["time"]["car_leisure"] = self._extract_timecost_from_gcost(
            "car_leisure")
        mtxs["time"]["transit_work"] = self._damp(
            mtxs["time"]["transit_work"], "transit_work_fw_time")
        if iteration=="last":
            mtxs["time"]["transit_leisure"] = self._damp(
                mtxs["time"]["transit_leisure"], "transit_leisure_fw_time")
        else:
            for mtx_type in mtxs:
                mtxs[mtx_type]["transit_leisure"] = mtxs[mtx_type]["transit_work"]
            for ass_cl in ("car_work", "car_leisure"):
                mtxs["cost"][ass_cl] += self.dist_unit_cost * mtxs["dist"][ass_cl]
        return mtxs

    def set_emmebank_matrices(self, matrices, is_last_iteration):
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

    def _set_matrix(self, mtx_label, matrix):
        if numpy.isnan(matrix).any():
            msg = "NAs in demand matrix {}. Would cause infinite loop in Emme assignment.".format(
                mtx_label)
            log.error(msg)
            raise ValueError(msg)
        else:
            self.emme_project.modeller.emmebank.matrix(
                self.demand_mtx[mtx_label]["id"]).set_numpy_data(matrix)

    def get_emmebank_matrices(self, mtx_type, is_last_iteration=False):
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
        matrices = dict.fromkeys(self.result_mtx[mtx_type].keys())
        if not is_last_iteration:
            for key in ("van", "truck", "trailer_truck"):
                del matrices[key]
        for subtype in matrices:
            matrices[subtype] = self.get_matrix(mtx_type, subtype)
        return matrices

    def get_matrix(self, assignment_result_type, subtype):
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
        return self.emme_project.modeller.emmebank.matrix(emme_id).get_numpy_data()

    def _damp(self, travel_time, fw_mtx_name):
        """Reduce the impact from first waiting time on total travel time."""
        fwt = self.get_matrix("trip_part", fw_mtx_name)
        wt_weight = param.waiting_time_perception_factor
        # Calculate transit travel time where first waiting time is damped
        dtt = travel_time + wt_weight*((5./3.*fwt)**0.8 - fwt)
        return dtt

    def _extract_timecost_from_gcost(self, ass_class):
        """Remove monetary cost from generalized cost."""
        # Traffic assignment produces a generalized cost matrix.
        # To get travel time, monetary cost is removed from generalized cost.
        vot_inv = param.vot_inv[param.vot_classes[ass_class]]
        gcost = self.get_matrix("gen_cost", ass_class)
        tcost = self.get_matrix("cost", ass_class)
        tdist = self.get_matrix("dist", ass_class)
        return gcost - vot_inv *(tcost + self.dist_unit_cost*tdist)

    def _calc_background_traffic(self, include_trucks=False):
        """Calculate background traffic (buses)."""
        network = self.emme_scenario.get_network()
        # emme api has name "data3" for ul3
        background_traffic = param.background_traffic.replace("ul", "data")
        # calc @bus and data3
        for link in network.links():
            segment_freq = 0
            for segment in link.segments():
                segment_hdw = segment.line.headway
                if 0 < segment_hdw < 900:
                    segment_freq += 60 / segment_hdw
            link["@bus"] = segment_freq
            if link.volume_delay_func in [1,2,3,4,5]:
                # If no bus lane
                link[background_traffic] = segment_freq
            else:
                link[background_traffic] = 0
            if include_trucks:
                for ass_class in ("@truck", "@trailer_truck"):
                    link[background_traffic] += link[ass_class]
        self.emme_scenario.publish_network(network)

    def _calc_road_cost(self):
        """Calculate road charges and driving costs for one scenario."""
        log.info("Calculates road charges for scenario {}".format(self.emme_scenario_id))
        network = self.emme_scenario.get_network()
        for link in network.links():
            toll_cost = link.length * link["@hinta"] # km * e/km = eur
            dist_cost = self.dist_unit_cost * link.length # (eur/km) * km = eur
            link['@toll_cost'] = toll_cost
            link["@total_cost"] = (toll_cost + dist_cost)
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
        for line in network.transit_lines():
            try:
                line.data3 = penalty[line.mode.id] + extra_penalty
            except KeyError:
                missing_penalties.add(line.mode.id)
        if missing_penalties:
            missing_penalties = ", ".join(missing_penalties)
            log.warn("No boarding penalty found for transit modes " + missing_penalties)
        self.emme_scenario.publish_network(network)

    def _specify(self):
        self._car_spec = CarSpecification(self.demand_mtx, self.result_mtx)
        # Bike assignment specification
        self.bike_spec = {
            "type": "STANDARD_TRAFFIC_ASSIGNMENT",
            "classes": [
                {
                    "mode": param.bike_mode,
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
        # Pedestrian assignment specification
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
        function_file = os.path.join(self.emme_project.path, param.func_car)  # TODO refactor paths out from here
        self.emme_project.process_functions(function_file)
        log.info("Car assignment started...")
        car_spec = self._car_spec.spec(lightweight)
        car_spec["stopping_criteria"] = stopping_criteria
        self.emme_project.car_assignment(car_spec, self.emme_scenario)
        log.info("Car assignment performed for scenario " + str(self.emme_scenario_id))

    def _assign_bikes(self, length_mat_id, length_for_links, link_vol):
        """Perform bike traffic assignment for one scenario."""
        function_file = os.path.join(self.emme_project.path, param.func_bike)  # TODO refactor paths out from here
        self.emme_project.process_functions(function_file)
        spec = self.bike_spec
        spec["classes"][0]["results"]["link_volumes"] = link_vol
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
        self.emme_project.network_calc(netw_spec, self.emme_scenario)
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
        self.emme_project.network_calc(netw_spec, self.emme_scenario)
        log.info("Bike assignment started...")
        self.emme_project.bike_assignment(
            specification=spec, scenario=self.emme_scenario)
        if self.save_matrices:
            for tp in self.emme_scenarios:
                if self.emme_scenarios[tp] != self.emme_scenario_id:
                    self._copy_matrix(
                        spec["classes"][0]["results"]["od_travel_times"]["shortest_paths"],
                        "time", "bike",tp)
                    self._copy_matrix(
                        length_mat_id, "dist", "bike", tp)
        log.info("Bike assignment performed for scenario " + str(self.emme_scenario_id))

    def _assign_pedestrians(self):
        """Perform pedestrian assignment for one scenario."""
        log.info("Pedestrian assignment started...")
        self.emme_project.pedestrian_assignment(
            specification=self.walk_spec, scenario=self.emme_scenario)
        if self.save_matrices:
            for tp in self.emme_scenarios:
                if self.emme_scenarios[tp] != self.emme_scenario_id:
                    self._copy_matrix(
                        self.walk_spec["od_results"]["transit_times"],
                        "time", "walk", tp)
                    self._copy_matrix(
                        self.walk_spec["strategy_analysis"]["results"]["od_values"],
                        "dist", "walk", tp)
        log.info("Pedestrian assignment performed for scenario " + str(self.emme_scenario_id)) 
