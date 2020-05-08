import os
import parameters as param
from datatypes.car import Car
from datatypes.journey_level import JourneyLevel
from datatypes.path_analysis import PathAnalysis

class BasicScenario():
    def __init__(self, emme_project, scenario_id, car_dist_cost=param.dist_unit_cost,
                demand_mtx=param.emme_demand_mtx, result_mtx=param.emme_result_mtx):
        """
        Class to hold methods for Emme-scenarios (car, transit).
        """
        self.emme_project = emme_project
        self.scenario_id = scenario_id
        self.dist_unit_cost = car_dist_cost
        self.demand_mtx=demand_mtx
        self.result_mtx=result_mtx

    def get_network(self):
        """Get network object from Emme."""
        scen = self.emme_project.modeller.emmebank.scenario(self.scenario_id)
        network = scen.get_network()
        return network

    def set_network(self, network):
        """Publish network object to Emme."""
        scen = self.emme_project.modeller.emmebank.scenario(self.scenario_id)
        scen.publish_network(network)

    @property
    def zone_numbers(self):
        """Return zone numbers in scenario.""" 
        emmebank = self.emme_project.modeller.emmebank
        scen = emmebank.scenario(self.scenario_id)
        return scen.zone_numbers
        
    def create_attributes(self, attributes):
        """Create attributes needed in assignment."""
        emmebank = self.emme_project.modeller.emmebank
        scen = emmebank.scenario(self.scenario_id)
        # defined in params
        for attr in attributes.keys():
            extr = self.emme_project.create_extra_attribute(
                extra_attribute_type = attributes[attr],
                extra_attribute_name = attr,
                extra_attribute_description = "HM40 extra attributes",
                extra_attribute_default_value = 0,
                overwrite = True,
                scenario = scen)
            self.emme_project.logger.debug(
                "Created attr {} for scen {}".format(extr.name, self.scenario_id))

    def _calc_background_traffic(self):
        """Calculate background traffic (buses)."""
        emmebank = self.emme_project.modeller.emmebank
        scen = emmebank.scenario(self.scenario_id)
        network = scen.get_network()
        # emme api has name "data3" for ul3
        param_name = param.background_traffic.replace("ul", "data")
        # calc @bus and data3
        extra_attr = "@bus"
        for link in network.links():
            segment_freq = 0
            for segment in link.segments():
                segment_hdw = segment.line.headway
                if 0 < segment_hdw < 900: 
                    segment_freq += 60 / segment_hdw
            link[extra_attr] = segment_freq
            if link.volume_delay_func in [1,2,3,4,5]:
                link[param_name] = segment_freq
        scen.publish_network(network)

    def _calc_road_cost(self):
        """Calculate road charges and driving costs for one scenario."""
        self.emme_project.logger.info("Calculates road charges for scenario " + str(self.scenario_id))
        emmebank = self.emme_project.modeller.emmebank
        scen = emmebank.scenario(self.scenario_id)
        network = scen.get_network()
        for link in network.links():
            toll_cost = link.length * link["@hinta"] # km * e/km = eur
            dist_cost = self.dist_unit_cost * link.length # (eur/km) * km = eur
            link['@toll_cost'] = toll_cost
            link["@total_cost"] = (toll_cost + dist_cost)
        scen.publish_network(network)

    def assign_transit_cost(self, transit_zone):
        """Check if trip has visited zone and calculate no visits 
        by performing multiple transit assignments.
        
        Parameters
        ----------
        zones_in_zonedata : set
            Set contains fare zones in input files. 
            Used to check that zones are specified in Emme-network.
        """
        # Move transfer penalty to boarding penalties,
        # a side effect is that it then also affects first boarding
        self._calc_boarding_penalties(5)
        emmebank = self.emme_project.modeller.emmebank
        scen = emmebank.scenario(self.scenario_id)
        network = scen.get_network()
        for node in network.nodes():
            node.data1 = (node.label == transit_zone)
        scen.publish_network(network)
        self._assign_transit(True)
        # Reset boarding penalties
        self._calc_boarding_penalties()

    def _specify(self):
        # Car assignment specification
        car_work = Car("car_work", self.demand_mtx, self.result_mtx)
        car_leisure = Car("car_leisure", self.demand_mtx, self.result_mtx)
        van = Car("van", self.demand_mtx, self.result_mtx)
        truck = Car(
            "truck", self.demand_mtx, self.result_mtx, 
            value_of_time_inv=0.2,link_costs="length")
        trailer_truck = Car(
            "trailer_truck", self.demand_mtx, self.result_mtx,
            value_of_time_inv=0.2, link_costs="length")
        self.car_spec = {
            "type": "SOLA_TRAFFIC_ASSIGNMENT",
            "classes": [
                car_work.spec,
                car_leisure.spec,
                trailer_truck.spec,
                truck.spec,
                van.spec,
            ],
            "background_traffic": {
                "link_component": param.background_traffic,
                "add_transit_vehicles": False,
            },
            "performance_settings": param.performance_settings,
            "stopping_criteria": None, # This is defined later
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
        # Transit assignment specification
        # Two journey levels are added at a later stage.
        # The two journey levels are identical, except that at the second
        # level an extra boarding penalty is implemented,
        # hence a transfer penalty. Waiting time length is also different. 
        # Walk only trips are not allowed.
        no_penalty = dict.fromkeys(["at_nodes", "on_lines", "on_segments"])
        no_penalty["global"] = {
            "penalty": 0, 
            "perception_factor": 1,
        }
        self.transit_spec = {
            "type": "EXTENDED_TRANSIT_ASSIGNMENT",
            "modes": param.transit_assignment_modes,
            "demand": self.demand_mtx["transit"]["id"],
            "waiting_time": {
                "headway_fraction": param.standard_headway_fraction,
                "effective_headways": "hdw",
                "spread_factor": 1,
                "perception_factor": param.waiting_time_perception_factor
            },
            "boarding_time": {
                "global": None,
                "at_nodes": None,
                "on_lines": {
                    "penalty": "ut3",
                    "perception_factor": 1
                },
                "on_segments": param.extra_waiting_time,
            },
            # Boarding cost is defined for each journey level separately,
            # so here we just set the default to zero.
            "boarding_cost": no_penalty,
            "in_vehicle_time": {
                "perception_factor": 1
            },
            "aux_transit_time": param.aux_transit_time,
            "flow_distribution_at_origins": {
                "choices_at_origins": "OPTIMAL_STRATEGY",
            },
            "flow_distribution_at_regular_nodes_with_aux_transit_choices": {
                "choices_at_regular_nodes": "OPTIMAL_STRATEGY",
            },
            "flow_distribution_between_lines": {
                "consider_total_impedance": False
            },
            "journey_levels": None,
            "performance_settings": param.performance_settings,
        }
        # Transit assignment result specification
        self.transit_result_spec = {
            "type": "EXTENDED_TRANSIT_MATRIX_RESULTS",
            "total_impedance": self.result_mtx["time"]["transit"]["id"],
            "actual_first_waiting_times": self.result_mtx["trip_components"]["transit_fw_time"]["id"],
            "actual_total_waiting_times": self.result_mtx["trip_components"]["transit_tw_time"]["id"],
            "by_mode_subset": {
                "modes": param.transit_modes,
                "distance": self.result_mtx["dist"]["transit"]["id"],
                "avg_boardings": self.result_mtx["trip_components"]["transit_num_board"]["id"],
                "actual_total_boarding_times": self.result_mtx["trip_components"]["transit_board_time"]["id"],
                "actual_in_vehicle_times": self.result_mtx["trip_components"]["transit_inv_time"]["id"],
                "actual_aux_transit_times": self.result_mtx["trip_components"]["transit_aux_time"]["id"],
            },
        }

    def _assign_cars(self, stopping_criteria):
        """Perform car_work traffic assignment for one scenario."""
        emmebank = self.emme_project.modeller.emmebank
        scen = emmebank.scenario(self.scenario_id)
        function_file = os.path.join(self.emme_project.path, param.func_car)  # TODO refactor paths out from here
        self.emme_project.process_functions(function_file)
        self.emme_project.logger.info("Car assignment started...")
        self.car_spec["stopping_criteria"] = stopping_criteria
        self.emme_project.car_assignment(self.car_spec, scen)
        self.emme_project.logger.info("Car assignment performed for scenario "
                                      + str(self.scenario_id))
    
    def _assign_pedestrians(self):
        """Perform pedestrian assignment for one scenario."""
        emmebank = self.emme_project.modeller.emmebank
        scen = emmebank.scenario(self.scenario_id)
        self.emme_project.logger.info("Pedestrian assignment started")
        self.emme_project.pedestrian_assignment(
            specification=self.walk_spec, scenario=scen)
        self.emme_project.logger.info("Pedestrian assignment performed for scenario "
                                      + str(self.scenario_id))

    def _calc_boarding_penalties(self, extra_penalty=0):
        """Calculate boarding penalties for transit assignment."""
        emmebank = self.emme_project.modeller.emmebank
        scen = emmebank.scenario(self.scenario_id)
        # Definition of line specific boarding penalties
        netw_specs = []
        # Bus
        for mode in param.boarding_penalty:
            netw_specs.append({
                "type": "NETWORK_CALCULATION",
                "selections": {
                    "transit_line": "mode=" + mode,
                },
                "expression": str(param.boarding_penalty[mode]) + "+" + str(extra_penalty),
                "result": "ut3",
                "aggregation": None,
            })
        self.emme_project.network_calc(netw_specs, scen)
        
    def _calc_extra_wait_time(self):
        """Calculate extra waiting time for one scenario."""
        emmebank = self.emme_project.modeller.emmebank
        scen = emmebank.scenario(self.scenario_id)
        network = scen.get_network()
        # Calculation of cumulative line segment travel time and speed
        self.emme_project.logger.info("Calculates cumulative travel times for scenario "
                                      + str(self.scenario_id))
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
        scen.publish_network(network)

    def _assign_transit(self, count_zone_boardings=False):
        """Perform transit assignment for one scenario."""
        if count_zone_boardings:
            jlevel1 = JourneyLevel(False, True)
            jlevel2 = JourneyLevel(True, True)
            bcost_spec = {
                "type": "EXTENDED_TRANSIT_MATRIX_RESULTS",
                "by_mode_subset": {
                    "modes": param.transit_modes,
                    "distance": self.result_mtx["dist"]["transit"]["id"],
                    "actual_total_boarding_costs": self.result_mtx["trip_components"]["transit_board_cost"]["id"],
                },
            }
        else:
            jlevel1 = JourneyLevel(boarded=False)
            jlevel2 = JourneyLevel(boarded=True)
        self.transit_spec["journey_levels"] = [jlevel1.spec, jlevel2.spec]
        # self.transit_spec["boarding_cost"] = bcost
        emmebank = self.emme_project.modeller.emmebank
        scen = emmebank.scenario(self.scenario_id)
        self.emme_project.logger.info("Transit assignment started")
        self.emme_project.transit_assignment(
            specification=self.transit_spec, 
            scenario=scen, save_strategies=True)
        if count_zone_boardings:
            self.emme_project.matrix_results(bcost_spec, scen)
        else:
            self.emme_project.matrix_results(self.transit_result_spec, scen)
        self.emme_project.logger.info("Transit assignment performed for scenario {}".format(str(self.scenario_id)))

    def _assign_congested_transit(self):
        """Perform congested transit assignment for one scenario."""
        emmebank = self.emme_project.modeller.emmebank
        scen = emmebank.scenario(self.scenario_id)
        self.emme_project.logger.info("Congested transit assignment started")
        self.emme_project.congested_assignment(
            transit_assignment_spec=self.transit_spec,
            congestion_function=param.trass_func,
            stopping_criteria=param.trass_stop,
            log_worksheets=False, scenario=scen,
            save_strategies=True)
        self.emme_project.matrix_results(self.transit_result_spec, scen)
        self.emme_project.logger.info("Transit assignment performed for scenario {}".format(str(self.scenario_id)))

class BikeScenario():
    def __init__(self, emme_project, scenario_id, demand_mtx=param.emme_demand_mtx, 
                result_mtx=param.emme_result_mtx):
        """
        Class to hold Emme-scenario (bike) specific methods.
        """
        self.demand_mtx=demand_mtx
        self.result_mtx=result_mtx
        self.emme_project = emme_project
        self.scenario_id = scenario_id
        self._has_assigned_walk = False

    def get_network(self):
        """Get network object from Emme."""
        tp_attr = {}
        scen = self.emme_project.modeller.emmebank.scenario(self.scenario_id)
        network = scen.get_network()
        return network

    def set_network(self, network):
        """Publish network object to Emme."""
        tp_attr = {}
        scen = self.emme_project.modeller.emmebank.scenario(self.scenario_id)
        scen.publish_network(network)
    
    def _specify(self):
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

    def create_attributes(self, attributes):
        """Create attributes needed in bike assignment."""
        emmebank = self.emme_project.modeller.emmebank
        scen = emmebank.scenario(self.scenario_id)
        # defined in params
        for attr in attributes.keys():
            extr = self.emme_project.create_extra_attribute(
                extra_attribute_type = attributes[attr],
                extra_attribute_name = attr,
                extra_attribute_description = "HM40 bike result attributes",
                extra_attribute_default_value = 0,
                overwrite = True,
                scenario = scen)
            self.emme_project.logger.debug(
                "Created attr {} for scen {}".format(extr.name, self.scenario_id))
    
    def _assign_bikes(self, length_for_links, link_vol):
        """Perform bike traffic assignment for one scenario."""
        emmebank = self.emme_project.modeller.emmebank
        scen = emmebank.scenario(self.scenario_id)
        function_file = os.path.join(self.emme_project.path, param.func_bike)  # TODO refactor paths out from here
        self.emme_project.process_functions(function_file)
        spec = self.bike_spec
        spec["classes"][0]["results"]["link_volumes"] = link_vol
        spec["classes"][0]["analysis"]["results"]["od_values"] = self.result_mtx["dist"]["bike"]["id"]
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
        self.emme_project.logger.info("Bike assignment started")
        self.emme_project.bike_assignment(specification=spec, scenario=scen)
        self.emme_project.logger.info("Bike assignment performed for scenario "
                                      + str(self.scenario_id))

class DayScenario():
    def __init__(self, emme_project, scenario_id):
        """
        Class to hold Emme-scenario (day) specific methods.
        """
        self.emme_project = emme_project
        self.scenario_id = scenario_id
    
    def get_network(self):
        """Get network object from Emme."""
        tp_attr = {}
        scen = self.emme_project.modeller.emmebank.scenario(self.scenario_id)
        network = scen.get_network()
        return network

    def set_network(self, network):
        """Publish network object to Emme."""
        tp_attr = {}
        scen = self.emme_project.modeller.emmebank.scenario(self.scenario_id)
        scen.publish_network(network)

    def create_attributes(self, attributes):
        """Create attributes needed to store 24h volumes from assignment."""
        emmebank = self.emme_project.modeller.emmebank
        scen = emmebank.scenario(self.scenario_id)
        # defined in params
        for attr in attributes.keys():
            extr = self.emme_project.create_extra_attribute(
                extra_attribute_type = attributes[attr],
                extra_attribute_name = attr,
                extra_attribute_description = "HM40 24h result attributes",
                extra_attribute_default_value = 0,
                overwrite = True,
                scenario = scen)
            self.emme_project.logger.debug(
                "Created attr {} for scen {}".format(extr.name, self.scenario_id))