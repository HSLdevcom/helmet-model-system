import os
import logging
import inro.emme.desktop.app as _app
import inro.modeller as _m
import parameters as param

class AssignmentModel:
    def __init__(self, filepath):
        self.logger = logging.getLogger()
        self.logger.info("Starting Emme...")
        emme_desktop = _app.start_dedicated(
            project=filepath, 
            visible=False, 
            user_initials="HSL"
        )
        sh = logging.StreamHandler(stream=self)
        self.logger.addHandler(sh)
        self.emme_modeller = _m.Modeller(emme_desktop)
        self.logger.info("Emme started.")
        self.path = os.path.dirname(self.emme_modeller.emmebank.path)
        create_matrix = self.emme_modeller.tool(
            "inro.emme.data.matrix.create_matrix")
        for mtx_type in param.emme_mtx:
            mtx = param.emme_mtx[mtx_type]
            for ass_class in mtx:
                create_matrix(
                    matrix_id=mtx[ass_class]["id"],
                    matrix_name=mtx_type+"_"+ass_class,
                    matrix_description=mtx[ass_class]["description"],
                    default_value=0,
                    overwrite=True)
    
    def write(self, message):
        """Write to logbook."""
        # _m.logbook_write(message)
        try:
            self.cm.__exit__(None, None, None)
        except AttributeError:
            pass
        # Logbook_trace returns a content manager that can be used to create 
        # hierarchies. By entering the cm, everything that Emme itself writes
        # to the logbook will be nested underneath this logbook entry.
        self.cm = _m.logbook_trace(message)
        self.cm.__enter__()
        
    def flush(self):
        """Flush the logbook (i.e., do nothing)."""
        pass
    
    def assign(self, scen_id, time_period, matrices):
        """Assign cars, bikes and transit for one time period."""
        self.logger.info("Assignment starts...")
        self.set_matrices(matrices)
        function_file = os.path.join(self.path, param.func_car)
        process = self.emme_modeller.tool(
            "inro.emme.data.function.function_transaction")
        process(function_file)
        self.calc_road_cost(scen_id)
        self.assign_cars(scen_id, param.stopping_criteria_coarse)
        self.calc_boarding_penalties(scen_id)
        self.assign_transit(scen_id)
        function_file = os.path.join(self.path, param.func_bike)
        process(function_file)
        self.assign_bikes(param.bike_scenario, 
                          param.emme_mtx["time"]["bike"]["id"], 
                          "all", 
                          "@fvol_"+time_period)
        matrices = {}
        matrices["time"] = self.get_matrices("time")
        matrices["dist"] = self.get_matrices("dist")
        matrices["cost"] = self.get_matrices("cost")
        tt = matrices["time"]["transit"]
        fwt_id = param.emme_mtx["transit"]["fw_time"]["id"]
        fwt = self.emme_modeller.emmebank.matrix(fwt_id).get_numpy_data()
        wt_weight = param.trass_spec["waiting_time"]["perception_factor"]
        # Calculate transit travel time where first waiting time is damped
        dtt = tt + wt_weight*((5/3*fwt)**0.8 - fwt)
        matrices["time"]["transit"] = dtt
        return matrices
    
    def set_matrices(self, matrices):
        emmebank = self.emme_modeller.emmebank
        for mtx in matrices:
            id = param.emme_mtx["demand"][mtx]["id"]
            emmebank.matrix(id).set_numpy_data(matrices[mtx])
    
    def get_matrices(self, mtx_type):
        emmebank = self.emme_modeller.emmebank
        matrices = dict.fromkeys(param.emme_mtx[mtx_type].keys())
        for mtx in matrices:
            id = param.emme_mtx[mtx_type][mtx]["id"]
            matrices[mtx] = emmebank.matrix(id).get_numpy_data()
        return matrices
    
    def calc_road_cost(self, scen_id):
        """Calculate road charges and driving costs for one scenario."""
        self.logger.info("Calculates road charges for scenario "
                        + str(scen_id))
        emmebank = self.emme_modeller.emmebank
        scenario = emmebank.scenario(scen_id)
        netw_specs = []
        # Link cost [eur]
        netw_specs.append({
            "type": "NETWORK_CALCULATION",
            "selections": {
                "link": "all",
            },
            "expression": "@hinta*length",
            "result": "@ruma",
            "aggregation": None,
        })
        # Driving cost [eur]
        netw_specs.append({
            "type": "NETWORK_CALCULATION",
            "selections": {
                "link": "all",
            },
            "expression": str(param.dist_cost)+"*length",
            "result": "@rumpi",
            "aggregation": None,
        })
        # Total cost [eur]
        netw_specs.append({
            "type": "NETWORK_CALCULATION",
            "selections": {
                "link": "all",
            },
            "expression": "@ruma+@rumpi",
            "result": "@rumsi",
            "aggregation": None,
        })
        netcalc = self.emme_modeller.tool(
            "inro.emme.network_calculation.network_calculator")
        netcalc(netw_specs, scenario)
        
    def assign_cars(self, scen_id, stopping_criteria):
        """Perform car traffic assignment for one scenario."""
        emmebank = self.emme_modeller.emmebank
        scenario = emmebank.scenario(scen_id)
        car = Car(demand=param.emme_mtx["demand"]["car"]["id"],
                  ass_class="car",
                  value_of_time_inv=param.vot_inv["work"],
                  od_travel_times=param.emme_mtx["gen_cost"]["car"]["id"])
        car.add_analysis("length", param.emme_mtx["dist"]["car"]["id"])
        car.add_analysis("@ruma", param.emme_mtx["cost"]["car"]["id"])
        van = Car(demand=param.emme_mtx["demand"]["van"]["id"],
                  ass_class="van",
                  value_of_time_inv=param.vot_inv["business"])
        truck = Car(demand=param.emme_mtx["demand"]["truck"]["id"],
                    ass_class="truck",
                    value_of_time_inv=0.2,
                    link_costs="length")
        trailer_truck = Car(
            demand=param.emme_mtx["demand"]["trailer_truck"]["id"],
            ass_class="trailer_truck",
            value_of_time_inv=0.2,
            link_costs="length")
        spec = {
            "type": "SOLA_TRAFFIC_ASSIGNMENT",
            "classes": [
                car.spec,
                trailer_truck.spec,
                truck.spec,
                van.spec,
            ],
            "background_traffic": None,
            "performance_settings": param.performance_settings,
            "stopping_criteria": stopping_criteria,
        }
        self.logger.info("Car assignment started...")
        car_assignment = self.emme_modeller.tool(
            "inro.emme.traffic_assignment.sola_traffic_assignment")
        car_assignment(spec, scenario)
        self.logger.info("Car assignment performed for scenario " 
                        + str(scen_id))
        # Traffic assignment produces a generalized cost matrix.
        # To get travel time, monetary cost is removed from generalized cost.
        self.logger.info("Extracts time matrix from generalized cost")
        matrix_spec = {
            "type": "MATRIX_CALCULATION",
            "expression": ( param.emme_mtx["gen_cost"]["car"]["id"]
                          + "-" + str(param.vot_inv["work"])
                          + "*(" + param.emme_mtx["cost"]["car"]["id"]
                          + "+" + str(param.dist_cost)
                          + "*" + param.emme_mtx["dist"]["car"]["id"] + ")"),
            "result": param.emme_mtx["time"]["car"]["id"],
            "constraint": {
                "by_value": None,
                "by_zone": None,
            },
            "aggregation": {
                "origins": None,
                "destinations": None,
            },
        }
        matcalc = self.emme_modeller.tool(
            "inro.emme.matrix_calculation.matrix_calculator")
        matcalc(matrix_spec, scenario)
    
    def assign_bikes(self, scen_id, length_mat_id, length_for_links, link_vol):
        """Perform bike traffic assignment for one scenario."""
        emmebank = self.emme_modeller.emmebank
        scen = emmebank.scenario(scen_id)
        create_matrix = self.emme_modeller.tool(
            "inro.emme.data.matrix.create_matrix")
        netcalc = self.emme_modeller.tool(
            "inro.emme.network_calculation.network_calculator")
        spec = param.biass_spec
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
        netcalc(netw_spec, scen)
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
        netcalc(netw_spec, scen)
        self.logger.info("Bike assignment started")
        bike_assignment = self.emme_modeller.tool(
            "inro.emme.traffic_assignment.standard_traffic_assignment")
        bike_assignment(specification=spec,  
                        scenario=scen)
        stoch_bike_assignment = self.emme_modeller.tool(
            "inro.emme.traffic_assignment.stochastic_traffic_assignment")
        # stoch_bike_assignment(traffic_assignment_spec=spec, 
                        # dist_par=param.bike_dist, 
                        # replications=10, 
                        # scenario=scen)
        self.logger.info("Bike assignment performed for scenario "
                        + str(scen_id))
    
    def calc_boarding_penalties(self, scen_id):
        """Calculate boarding penalties for transit assignment."""
        emmebank = self.emme_modeller.emmebank
        scenario = emmebank.scenario(scen_id)
        network = scenario.get_network()
        # Calculation of cumulative line segment travel time and speed
        self.logger.info("Calculates cumulative travel times for scenario "
                         + str(scen_id))
        for line in network.transit_lines():
            cumulative_length = 0
            cumulative_time = 0
            cumulative_speed = 0
            headway_sd = 0
            for segment in line.segments():
                cumulative_length += segment.link.length
                # Travel time for buses in mixed traffic
                if segment.transit_time_func == 1:
                    cumulative_time += ( segment.data2 * segment.link.length
                                       # + segment.link["@timau"]
                                       + segment.link.auto_time
                                       + segment.dwell_time)
                # Travel time for buses on bus lanes
                if segment.transit_time_func == 2:
                    cumulative_time += ( segment.data2 * segment.link.length
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
                    cumulative_speed = ( cumulative_length 
                                       / cumulative_time 
                                       * 60)
                # Headway standard deviation for buses and trams
                if line.mode.id in param.headway_sd_func:
                    b = param.headway_sd_func[line.mode.id]
                    headway_sd = ( b["asc"] 
                                 + b["ctime"]*cumulative_time 
                                 + b["cspeed"]*cumulative_speed)
                # Estimated waiting time addition caused by headway deviation
                segment["@wait_time_dev"] = headway_sd**2 / (2*line.headway)
        scenario.publish_network(network)
        # Definition of line specific boarding penalties
        netw_specs = []
        # Bus
        for mode in param.boarding_penalty:
            netw_specs.append({
                "type": "NETWORK_CALCULATION",
                "selections": {
                    "transit_line": "mode=" + mode,
                },
                "expression": str(param.boarding_penalty[mode]),
                "result": "ut3",
                "aggregation": None,
            })
        netcalc = self.emme_modeller.tool(
            "inro.emme.network_calculation.network_calculator")
        netcalc(netw_specs, scenario)
        
    def assign_transit(self, scen_id):
        """Perform transit assignment for one scenario."""
        emmebank = self.emme_modeller.emmebank
        scenario = emmebank.scenario(scen_id)
        # Definition of transition rules: all modes are allowed
        transitions = []
        for mode in param.transit_modes:
            transitions.append({
                "mode": mode,
                "next_journey_level": 1
            })
        trass_spec = param.trass_spec
        trass_spec["journey_levels"][0]["transition_rules"] = transitions
        trass_spec["journey_levels"][1]["transition_rules"] = transitions
        self.logger.info("Transit assignment started")
        transit_assignment = self.emme_modeller.tool(
            "inro.emme.transit_assignment.extended_transit_assignment")
        congested_assignment = self.emme_modeller.tool(
            "inro.emme.transit_assignment.congested_transit_assignment")
        transit_assignment(trass_spec, scenario)
        # congested_assignment(transit_assignment_spec=trass_spec, 
                             # congestion_function=param.trass_func,
                             # stopping_criteria=param.trass_stop, 
                             # log_worksheets=False, 
                             # scenario=scenario)
        matrix_results = self.emme_modeller.tool(
            "inro.emme.transit_assignment.extended.matrix_results")
        # Transit assignment result specification
        mtx = param.emme_mtx
        result_spec = {
            "type": "EXTENDED_TRANSIT_MATRIX_RESULTS",
            "total_impedance": mtx["time"]["transit"]["id"],
            "actual_first_waiting_times": mtx["transit"]["fw_time"]["id"],
            "actual_total_waiting_times": mtx["transit"]["tw_time"]["id"],
            "by_mode_subset": {
                "modes": param.transit_modes,
                "distance": mtx["dist"]["transit"]["id"],
                "avg_boardings": mtx["transit"]["num_board"]["id"],
                "actual_total_boarding_times": mtx["transit"]["board_time"]["id"],
                "actual_in_vehicle_times": mtx["transit"]["inv_time"]["id"],
                "actual_aux_transit_times": mtx["transit"]["aux_time"]["id"],
            },
        }
        matrix_results(result_spec, scenario)
        self.logger.info("Transit assignment performed for scenario " 
                        + str(scen_id))
        
class Car:
    def __init__(self, demand, ass_class, value_of_time_inv, 
                 od_travel_times=None, link_costs="@rumsi"):
        self.spec = {
            "mode": param.mode[ass_class],
            "demand": demand,
            "generalized_cost": {
                "link_costs": "@rumsi",
                "perception_factor": value_of_time_inv,
            },
            "results": {
                "link_volumes": param.link_volumes[ass_class],
                "turn_volumes": None,
                "od_travel_times": {
                    "shortest_paths": od_travel_times
                }
            },
            "path_analyses": []
        }
    
    def add_analysis (self, link_component, od_values):
        analysis = PathAnalysis(link_component, od_values)
        self.spec["path_analyses"].append(analysis.spec)

class PathAnalysis:
    def __init__(self, link_component, od_values):
        self.spec = {
            "link_component": link_component,
            "turn_component": None,
            "operator": "+",
            "selection_threshold": {
                "lower": None,
                "upper": None,
            },
            "path_to_od_composition": {
                "considered_paths": "ALL",
                "multiply_path_proportions_by": {
                    "analyzed_demand": False,
                    "path_value": True,
                }
            },
            "analyzed_demand": None,
            "results": {
                "selected_link_volumes": None,
                "selected_turn_volumes": None,
                "od_values": od_values,
            },
        }