import numpy
import pandas
import parameters as param
from abstract_assignment import AssignmentModel, ImpedanceSource
from datatypes.emme_scenario import BasicScenario, BikeScenario, DayScenario


class EmmeAssignmentModel(AssignmentModel, ImpedanceSource):
    def __init__(self, emme_project, first_scenario_id, car_dist_cost=param.dist_unit_cost, fixed_transit_cost=False):
        """
        Emme-assignment methods for Helmet-scenario. This class is used as a part of Helmet-model-system run.
        Helmet-scenario has four Emme-scenarios. 
        First scenario is bike scenario, followed by day scenario, and three basic car and transit scenarios (morning, midday, evening).
        """
        self.emme_project = emme_project
        # create scenario instances and initialize attributes
        self.bike_scenario = BikeScenario(self.emme_project, first_scenario_id)
        self.bike_scenario.create_attributes(param.bike_attributes)
        self.bike_scenario._specify()
        self.day_scenario = DayScenario(self.emme_project, first_scenario_id+1)
        self.day_scenario.create_attributes(param.emme_attributes)
        self.emme_scenarios = {
            "aht": BasicScenario(self.emme_project, first_scenario_id+2),
            "pt": BasicScenario(self.emme_project, first_scenario_id+3),
            "iht": BasicScenario(self.emme_project, first_scenario_id+4)
        }
        for scen in self.emme_scenarios.values():
            scen.create_attributes(param.emme_attributes)
            scen._calc_road_cost()
            scen._calc_boarding_penalties()
            scen._calc_background_traffic()
            scen._specify()
        # initialize matrices
        self.demand_mtx=param.emme_demand_mtx
        self.result_mtx=param.emme_result_mtx
        for ass_class in self.demand_mtx:
            self.emme_project.create_matrix(
                matrix_id=self.demand_mtx[ass_class]["id"],
                matrix_name="demand_"+ass_class,
                matrix_description=self.demand_mtx[ass_class]["description"],
                default_value=0,
                overwrite=True)
        for mtx_type in self.result_mtx:
            mtx = self.result_mtx[mtx_type]
            for ass_class in mtx:
                self.emme_project.create_matrix(
                    matrix_id=mtx[ass_class]["id"],
                    matrix_name=mtx_type+"_"+ass_class,
                    matrix_description=mtx[ass_class]["description"],
                    default_value=999999,
                    overwrite=True)
        self._has_assigned_bike_and_walk = False
        self.dist_unit_cost = car_dist_cost

    def assign(self, time_period, matrices, is_last_iteration=False, is_first_iteration=False):
        """Assign cars, bikes and transit for one time period.
        
        Parameters
        ----------
        time_period : str
            Time period (aht/pt/iht)
        matrices: dict
            Assignment class (car_work/transit/...) : numpy 2-d matrix
        is_last_iteration: bool
        is_first_iteration: bool
        """
        scenario = self.emme_scenarios[time_period]
        self.emme_project.logger.info("Assignment starts...")
        self.set_emmebank_matrices(matrices)
        if not self._has_assigned_bike_and_walk:
            scenario._assign_pedestrians()
            self.bike_scenario._assign_bikes("all", "@bike_"+time_period)
            self._has_assigned_bike_and_walk = True
        if is_last_iteration:
            scenario._assign_cars(param.stopping_criteria_fine)
            scenario._calc_extra_wait_time()
            scenario._assign_congested_transit()
            self.bike_scenario._assign_bikes("all", "@bike_"+time_period)
            # calculate 24h volumes
            for result_attribute in param.link_volumes:
                self.auto_link_24h(result_attribute)
            self.transit_link_volume_24h() 
            self.transit_segment_boardings_24h()
            self.bike_link_24h() 
        else:
            scenario._assign_cars(param.stopping_criteria_coarse)
            scenario._calc_extra_wait_time()
            scenario._assign_transit()

    # TODO Could they be merged with (right after) .assign(). Currently both re-route via emmebank, which is ambiguous.
    # Then the ABC class as well as MockAssignment would have to be adjusted respectively.
    def get_impedance(self, is_last_iteration=False):
        """Get travel impedance matrices for one time period from assignment.
        
        Return
        ------
        dict
            Type (time/cost/dist) : dict
                Assignment class (car_work/transit/...) : numpy 2-d matrix
        """
        mtxs = {"time": self.get_emmebank_matrices("time"),
                "dist": self.get_emmebank_matrices("dist"),
                "cost": self.get_emmebank_matrices("cost")}
        # fix the emme path analysis results (dist and cost zero if path not found)
        for mtx_type in mtxs: 
            for mtx_class in mtxs[mtx_type]: 
                mtxs[mtx_type][mtx_class][ mtxs["time"][mtx_class] > 999999 ] = 999999
        # adjust impedance 
        mtxs["time"]["transit"] = self._damp(mtxs["time"]["transit"])
        mtxs["time"]["bike"] = mtxs["time"]["bike"].clip(None, 9999.)
        mtxs["time"]["car_work"] = self._extract_timecost_from_gcost("car_work")
        mtxs["time"]["car_leisure"] = self._extract_timecost_from_gcost("car_leisure")
        if not is_last_iteration:
            for ass_cl in ("car_work", "car_leisure"):
                mtxs["cost"][ass_cl] += self.dist_unit_cost * mtxs["dist"][ass_cl]
        return mtxs

    def set_emmebank_matrices(self, matrices):
        emmebank = self.emme_project.modeller.emmebank
        tmp_mtx = {
            "transit": 0,
            "bike": 0,
        }
        for mtx in matrices:
            mtx_label = mtx.split('_')[0]
            if mtx_label in tmp_mtx:
                idx = self.demand_mtx[mtx_label]["id"]
                tmp_mtx[mtx_label] += matrices[mtx]
                if numpy.isnan(tmp_mtx[mtx_label]).any():
                    msg = "NAs in Numpy-demand matrix. Would cause infinite loop in Emme-assignment."
                    self.emme_project.logger.error(msg)
                    raise ValueError(msg)
                else:
                    emmebank.matrix(idx).set_numpy_data(tmp_mtx[mtx_label])
            else:
                idx = self.demand_mtx[mtx]["id"]
                if numpy.isnan(matrices[mtx]).any():
                    msg = "NAs in Numpy-demand matrix. Would cause infinite loop in Emme-assignment."
                    self.emme_project.logger.error(msg)
                    raise ValueError(msg)
                else:
                    emmebank.matrix(idx).set_numpy_data(matrices[mtx])

    def get_emmebank_matrices(self, mtx_type, time_period=None):
        """Get all matrices of specified type.
        
        Parameters
        ----------
        mtx_type : str
            Type (demand/time/transit/...)
        time_period: str
            (Unused currently)

        Return
        ------
        dict
            Subtype (car_work/truck/inv_time/...) : numpy 2-d matrix
                Matrix of the specified type
        """
        # TODO Remove freight impedance matrices from selection,
        # if not last iteration
        matrices = dict.fromkeys(self.result_mtx[mtx_type].keys())
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

    @property
    def zone_numbers(self):
        """Numpy array of all zone numbers in aht scenario.""" 
        return self.emme_scenarios["aht"].zone_numbers

    @property
    def mapping(self):
        """dict: Dictionary of zone numbers and corresponding indices."""
        mapping = {}
        for idx, zone in enumerate(self.zone_numbers):
            mapping[zone] = idx
        return mapping

    @property
    def nr_zones(self):
        """int: Number of zones in assignment model."""
        return len(self.zone_numbers)

    def _damp(self, travel_time):
        """Reduce the impact from first waiting time on total travel time."""
        fwt = self.get_matrix("trip_components", "transit_fw_time")
        wt_weight = param.waiting_time_perception_factor
        # Calculate transit travel time where first waiting time is damped
        dtt = travel_time + wt_weight*((5./3.*fwt)**0.8 - fwt)
        return dtt

    def _extract_timecost_from_gcost(self, ass_class):
        """Remove monetary cost from generalized cost."""
        # Traffic assignment produces a generalized cost matrix.
        # To get travel time, monetary cost is removed from generalized cost.
        vot_inv = param.vot_inv[param.vot_class[ass_class]]
        gcost = self.get_matrix("gen_cost", ass_class)
        tcost = self.get_matrix("cost", ass_class)
        tdist = self.get_matrix("dist", ass_class)
        return gcost - vot_inv *(tcost + self.dist_unit_cost*tdist)
    
    def print_vehicle_kms(self, resultdata):
        vdfs = [1, 2, 3, 4, 5]
        transit_modes = {
            "bus": "bde",
            "trunk": "g",
            "metro": "m",
            "train": "rj",
            "tram": "tp",
            "other": ""
        }
        kms = dict.fromkeys(freight_classes + ["car"])
        for ass_class in kms:
            kms[ass_class] = dict.fromkeys(vdfs, 0)
        transit_dists = dict.fromkeys(transit_modes, 0)
        transit_times = dict.fromkeys(transit_modes, 0)
        for tp in self.emme_scenarios:
            scenario = self.emme_scenarios[tp]
            network = scenario.get_network()
            for link in network.links():
                if link.volume_delay_func <= 5:
                    vdf = link.volume_delay_func
                else:
                    # Links with bus lane
                    vdf = link.volume_delay_func - 5
                if vdf in vdfs:
                    car_vol = link.auto_volume
                    for ass_class in param.freight_classes:
                        kms[ass_class][vdf] += (param.volume_factors[ass_class][tp]
                                                * link[param.link_volumes[ass_class]]
                                                * link.length)
                        car_vol -= link[param.link_volumes[ass_class]]
                    kms["car"][vdf] += (param.volume_factors["car"][tp] * car_vol * link.length)
            for line in network.transit_lines():
                mode = "other"
                for modes in transit_modes:
                    if line.mode.id in transit_modes[modes]:
                        mode = modes
                for segment in line.segments():
                    transit_dists[mode] += (param.volume_factors["transit"][tp]
                                            * (60 / segment.line.headway)
                                            * segment.link.length)
                    transit_times[mode] += (param.volume_factors["transit"][tp]
                                            * (60 / segment.line.headway)
                                            * segment.transit_time)
        for ass_class in kms:
            resultdata.print_data(
                kms[ass_class].values(), "vehicle_kms.txt",
                kms[ass_class].keys(), ass_class)
        resultdata.print_data(
            transit_dists.values(), "transit_kms.txt",
            transit_dists.keys(), "dist")
        resultdata.print_data(
            transit_times.values(), "transit_kms.txt",
            transit_times.keys(), "time")

    def calc_transit_cost(self, fares, peripheral_cost, default_cost=None):
        """Calculate transit zone cost matrix by performing 
        multiple transit assignments.
        
        Parameters
        ----------
        fares : pandas Dataframe
            Zone fare vector and fare exclusiveness vector
        peripheral_cost : numpy 2-d matrix
            Fixed cost matrix for peripheral zones
        default_cost : numpy 2-d matrix
            (optional) Fixed cost matrix to use instead of calculated cost
        """
        emmebank = self.emme_project.modeller.emmebank
        scenario = self.emme_scenarios["aht"]
        network = scenario.get_network()
        idx = self.result_mtx["cost"]["transit"]["id"]
        if default_cost is not None:
            # Use fixed cost matrix
            emmebank.matrix(idx).set_numpy_data(default_cost)
            return

        # Move transfer penalty to boarding penalties,
        # a side effect is that it then also affects first boarding
        has_visited = {}
        mapping = self.mapping
        transit_zones = set()
        for node in network.nodes():
            transit_zones.add(node.label)
        # check that fare zones exist in network
        self.emme_project.logger.debug(
            "Network has fare zones {}".format(', '.join(transit_zones)))
        zones_in_zonedata = set(char for char in ''.join(fares["fare"].keys()))
        self.emme_project.logger.debug(
            "Zonedata has fare zones {}".format(', '.join(zones_in_zonedata)))
        if not zones_in_zonedata <= transit_zones:
            self.emme_project.logger.warn(
                "All zones in transit costs do not exist in Emme-network labels.")
        if not transit_zones <= zones_in_zonedata:
            self.emme_project.logger.warn(
                "All Emme-node labels do not have transit costs specified.")
        for transit_zone in transit_zones:
            # Transit assignment with zone tag as weightless boarding cost
            scenario.assign_transit_cost(transit_zone)
            nr_visits = self.get_matrix("trip_components", "transit_board_cost")
            # If the number of visits is less than 1, there seems to
            # be an easy way to avoid visiting this transit zone
            has_visited[transit_zone] = (nr_visits >= 1)
        network = scenario.get_network()
        for centroid in network.centroids():
            # Add transit zone of destination to visited
            has_visited[centroid.label][:, mapping[centroid.number]] = True
        maxprice = 999
        cost = numpy.full_like(nr_visits, maxprice)
        mtx = next(iter(has_visited.values()))
        for zone_combination in fares["fare"]:
            goes_outside = numpy.full_like(mtx, False)
            for transit_zone in has_visited:
                # Check if the OD-flow has been at a node that is
                # outside of this zone combination
                if transit_zone not in zone_combination:
                    goes_outside |= has_visited[transit_zone]
            is_inside = ~goes_outside
            if zone_combination in fares["exclusive"]:
                # Calculate fares exclusive for municipality citizens
                zn = self.zone_numbers
                exclusion = pandas.DataFrame(is_inside, zn, zn)
                municipality = fares["exclusive"][zone_combination]
                inclusion = param.municipality[municipality]
                exclusion.loc[:inclusion[0]-1] = False
                exclusion.loc[inclusion[1]+1:] = False
                is_inside = exclusion.values
            zone_price = fares["fare"][zone_combination]
            # If OD-flow matches several combinations, pick cheapest
            cost[is_inside] = numpy.minimum(cost[is_inside], zone_price)
        # Calculate distance-based cost from inv-distance
        dist = self.get_matrix("dist", "transit")
        dist_cost = fares["start_fare"] + fares["dist_fare"]*dist
        cost[cost==maxprice] = dist_cost[cost==maxprice]
        # Replace fare for peripheral zones with fixed matrix
        bounds = param.areas["peripheral"]
        zn = pandas.Index(self.zone_numbers)
        l, u = zn.slice_locs(bounds[0], bounds[1])
        cost[l:u, :u] = peripheral_cost
        cost[:u, l:u] = peripheral_cost.T
        emmebank.matrix(idx).set_numpy_data(cost)

    def auto_link_24h(self, attr):
        """ 
        Sums and expands link volumes from different scenarios to one result scenario.

         Parameters
        ----------
        attr : str
            Attribute name thatis usually part of Parameters: link_volumes.
        """
        extra_attr = param.link_volumes[attr]
        # get attr from different time periods to dictionary
        links_attr = {}
        for tp in self.emme_scenarios:
            tp_attr = {}
            scenario = self.emme_scenarios[tp]
            network = scenario.get_network()
            for link in network.links():
                tp_attr[link.id] = link[extra_attr]
            links_attr[tp] = tp_attr
        # create attr to save volume
        extra_attr_day = str(param.link_volumes[attr])
        network = self.day_scenario.get_network()
        # save link volumes to result network
        for link in network.links():
            day_attr = 0
            for tp in self.emme_scenarios:
                if link.id in links_attr[tp]:
                    day_attr += links_attr[tp][link.id] * param.volume_factors[attr][tp]
            link[extra_attr_day] = day_attr
        self.day_scenario.set_network(network)

    def transit_link_volume_24h(self):
        """ 
        Sums and expands segment volumes to links from different scenario.
        """
        attr = "transit"
        extra_attr = "@transit_volume"
        # get voltr from different time periods to dictionary
        links_attr = {}
        for tp in self.emme_scenarios:
            tp_attr = {}
            scenario = self.emme_scenarios[tp]
            network = scenario.get_network()
            for link in network.links():
                voltr_segment = 0
                for segment in link.segments():
                    voltr_segment += segment.transit_volume
                link[extra_attr] = voltr_segment
                tp_attr[link.id] = voltr_segment
            links_attr[tp] = tp_attr
            scenario.set_network(network)
        # save link volumes to result network
        network = self.day_scenario.get_network()
        for link in network.links():
            day_attr = 0
            for tp in self.emme_scenarios:
                if link.id in links_attr[tp]:
                    day_attr += links_attr[tp][link.id] * param.volume_factors[attr][tp]
            link[extra_attr] = day_attr
        self.day_scenario.set_network(network)

    def transit_segment_boardings_24h(self):
        """ 
        Sums and expands transit boardings to segments.
        """
        attr = "transit"
        extra_attr = "@transit_boardings"
        # get attr from different time periods to dictionary
        segments_attr = {}
        for tp in self.emme_scenarios:
            tp_attr = {}
            scenario = self.emme_scenarios[tp]
            network = scenario.get_network()
            for segment in network.transit_segments():
                tp_attr[segment.id] = segment.transit_boardings
            segments_attr[tp] = tp_attr
        # save link volumes to result network
        network = self.day_scenario.get_network()
        for segment in network.transit_segments():
            day_attr = 0
            for tp in self.emme_scenarios:
                if segment.id in segments_attr[tp]:
                    day_attr += segments_attr[tp][segment.id] * param.volume_factors[attr][tp]
            segment[extra_attr] = day_attr
        self.day_scenario.set_network(network)

    def bike_link_24h(self):
        """ 
        Sums and expands bike volumes from different scenarios to one result scenario.
        """
        attr = "bike"
        # get attr from different time periods to dictionary
        links_attr = {}
        for tp in param.emme_scenario:
            extra_attr = "@{}_{}".format(attr, tp)
            tp_attr = {}
            network = self.bike_scenario.get_network()
            for link in network.links():
                tp_attr[link.id] = link[extra_attr]
            links_attr[tp] = tp_attr
        # save link volumes to result network
        for link in network.links():
            day_attr = 0
            for tp in param.emme_scenario:
                if link.id in links_attr[tp]:
                    day_attr += links_attr[tp][link.id] * param.volume_factors[attr][tp]
            extra_attr = "@{}_{}".format(attr, "day")
            link[extra_attr] = day_attr
        self.bike_scenario.set_network(network)
