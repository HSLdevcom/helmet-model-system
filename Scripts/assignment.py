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
        self.process = self.emme_modeller.tool(
            "inro.emme.data.function.function_transaction")
        self.path = os.path.dirname(self.emme_modeller.emmebank.path)
        create_matrix = self.emme_modeller.tool(
            "inro.emme.data.matrix.create_matrix")
        for mtx_type in param.emme_mtx:
            for ass_class in param.emme_mtx[mtx_type]:
                create_matrix(matrix_id=param.emme_mtx[mtx_type][ass_class],
                              matrix_name=mtx_type+ass_class,
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
    
    def assign(self, scen_id, matrices):
        """Assign cars, bikes and transit for one time period."""
        self.logger.info("Assignment starts...")
        self.set_matrices(matrices)
        function_file = os.path.join(self.path,"d411_pituusriippuvaiset_HM30.in")
        self.process(function_file)
        self.calc_road_cost(scen_id)
        self.assign_cars(scen_id, param.stopping_criteria_coarse)
        self.assign_transit(scen_id)

    # def create_matrix(self, id, name="", description=""):
        # emme_mtx = self.emme_modeller.emmebank.matrix(id)
        # if emme_mtx:
            # emme_mtx.initialize()
        # else:
            # emme_mtx = self.emme_modeller.emmebank.create_matrix(id)
        # emme_mtx.name = name
        # emme_mtx.description = description
        
    def set_matrix(self, id, mtx):
        self.emme_modeller.emmebank.matrix(id).set_numpy_data(mtx)
    
    def set_matrices(self, matrices):
        emmebank = self.emme_modeller.emmebank
        for mtx in matrices:
            id = param.emme_mtx["demand"][mtx]
            emmebank.matrix(id).set_numpy_data(matrices[mtx])
    
    def calc_road_cost(self, scen_id):
        """Calculate road charges and driving costs for one scenario."""
        self.logger.info("Calculates road charges for scenario " + str(scen_id))
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
        spec = {
            "type": "SOLA_TRAFFIC_ASSIGNMENT",
            "classes": [
                param.cars,
                param.trailer_trucks,
                param.trucks,
                param.vans,
            ],
            "background_traffic": None,
            "performance_settings": {
                "number_of_processors": "max"
            },
            "stopping_criteria": stopping_criteria,
        }
        self.logger.info("Car assignment started...")
        car_assignment = self.emme_modeller.tool(
            "inro.emme.traffic_assignment.sola_traffic_assignment")
        car_assignment(spec, scenario)
        self.logger.info("Car assignment performed for scenario " + str(scen_id))
        # Traffic assignment produces a generalized cost matrix.
        # To get travel time, monetary cost is removed from generalized cost.
        self.logger.info("Extracts time matrix from generalized cost")
        matrix_spec = {
            "type": "MATRIX_CALCULATION",
            "expression": param.emme_mtx["time"]["car"]
                          +"-"+str(param.vot_inv)+"*("+param.emme_mtx["cost"]["car"]
                          +"+"+str(param.dist_cost)+"*"+param.emme_mtx["dist"]["car"]+")",
            "result": param.emme_mtx["time"]["car"],
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
    
    def assign_bikes(self, scen_id):
        pass
        
    def assign_transit(self, scen_id):
        """Perform transit assignment for one scenario."""
        emmebank = self.emme_modeller.emmebank
        scenario = emmebank.scenario(scen_id)
        network = scenario.get_network()
        # Calculation of cumulative line segment travel time and speed
        self.logger.info("Calculates cumulative travel times for scenario "  + str(scen_id))
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
                    # Digits 5-6 from end (1-2 from beg.) represent AHT speed.
                    # If AHT speed is less than 10, data1 will have only 5 digits.
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
                if (cumulative_time > 0):
                    cumulative_speed = cumulative_length / cumulative_time * 60
                # Headway standard deviation for buses
                if (line.mode.id == 'b' or line.mode.id == 'd'):
                    headway_sd = ( 2.164 
                                 + 0.078 * cumulative_time 
                                 - 0.028 * cumulative_speed)
                # Headway standard deviation for trunk buses
                if (line.mode.id == 'g'):
                    headway_sd = ( 2.127 
                                 + 0.034 * cumulative_time 
                                 - 0.021 * cumulative_speed)
                # Headway standard deviation for trams
                if (line.mode.id == 't'):
                    headway_sd = ( 1.442 
                                 + 0.060 * cumulative_time 
                                 - 0.039 * cumulative_speed)
                # Headway standard deviation for light rail
                if (line.mode.id == 'p'):
                    headway_sd = ( 1.442 
                                 + 0.034 * cumulative_time 
                                 - 0.039 * cumulative_speed)
                # Estimated waiting time addition caused by headway deviation
                segment["@wait_time_dev"] = headway_sd**2 / (2*line.headway)
        scenario.publish_network(network)
        # Definition of line specific boarding penalties
        netw_specs = []
        # Bus
        netw_specs.append({
            "type": "NETWORK_CALCULATION",
            "selections": {
                "transit_line": "mode=b",
            },
            "expression": "3",
            "result": "ut3",
            "aggregation": None,
        })
        # Trunk bus
        netw_specs.append({
            "type": "NETWORK_CALCULATION",
            "selections": {
                "transit_line": "mode=g",
            },
            "expression": "3",
            "result": "ut3",
            "aggregation": None,
        })
        # Long-distance and express buses
        netw_specs.append({
            "type": "NETWORK_CALCULATION",
            "selections": {
                "transit_line": "mode=de",
            },
            "expression": "5",
            "result": "ut3",
            "aggregation": None,
        })
        # Train
        netw_specs.append({
            "type": "NETWORK_CALCULATION",
            "selections": {
                "transit_line": "mode=rj",
            },
            "expression": "2",
            "result": "ut3",
            "aggregation": None,
        })
        # Metro and ferry
        netw_specs.append({
            "type": "NETWORK_CALCULATION",
            "selections": {
                "transit_line": "mode=mw",
            },
            "expression": "0",
            "result": "ut3",
            "aggregation": None,
        })
        # Tram and light rail
        netw_specs.append({
            "type": "NETWORK_CALCULATION",
            "selections": {
                "transit_line": "mode=tp",
            },
            "expression": "0",
            "result": "ut3",
            "aggregation": None,
        })
        # netw_specs.append({
            # "type": "NETWORK_CALCULATION",
            # "selections": {
                # "link": "all",
                # "transit_line": "mode=bgde",
            # },
            # "expression": "0.1*index2",
            # "result": "us3",
            # "aggregation": None,
        # })
        netcalc = self.emme_modeller.tool(
            "inro.emme.network_calculation.network_calculator")
        netcalc(netw_specs, scenario)
        # Definition of transition rules: all modes are allowed
        transitions = []
        for mode in param.transit_modes:
            transitions.append({
                "mode": mode,
                "next_journey_level": 1
            })
        func = {
            "type": "BPR",
            "weight": 1.23,
            "exponent": 3,
            "assignment_period": 1,
            "orig_func": False,
            "congestion_attribute": "us3",
        }
        # func = {
            # "type": "CUSTOM",
            # "assignment_period": 1,
            # "orig_func": False,
            # "congestion_attribute": "us3",
            # "python_function": """def calc_segment_cost(transit_volume, capacity, segment):
                                    # return 0.53 * ((transit_volume / capacity) ** 2)"""
        # }
        stop = {
            "max_iterations": 10,
            "normalized_gap": 0.01,
            "relative_gap": 0.001
        }
        self.logger.info("Transit assignment started")
        transit_assignment = self.emme_modeller.tool(
            "inro.emme.transit_assignment.extended_transit_assignment")
        congested_assignment = self.emme_modeller.tool(
            "inro.emme.transit_assignment.congested_transit_assignment")
        transit_assignment(param.trass_spec, scenario)
        # congested_assignment(transit_assignment_spec=trass_spec, 
                             # congestion_function=func,
                             # stopping_criteria=stop, 
                             # log_worksheets=False, 
                             # scenario=scenario)
        
        # tottim_id = "mf" + result_mat_id + "0"
        # inveht_id = "mf" + result_mat_id + "1"
        # auxtim_id = "mf" + result_mat_id + "2"
        # twtime_id = "mf" + result_mat_id + "3"
        # fwtime_id = "mf" + result_mat_id + "4"
        # boatim_id = "mf" + result_mat_id + "5"
        # noboa_id = "mf" + result_mat_id + "6"
        # invlen_id = "mf" + result_mat_id + "7"
        # create_matrix = emme_modeller.tool(
            # "inro.emme.data.matrix.create_matrix")
        # create_matrix(matrix_id=tottim_id,
                      # matrix_name="tottim",
                      # matrix_description="total time s="+str(scen_id),
                      # default_value=0,
                      # overwrite=True)
        # create_matrix(matrix_id=inveht_id,
                      # matrix_name="inveht",
                      # matrix_description="in veh time s="+str(scen_id),
                      # default_value=0,
                      # overwrite=True)
        # create_matrix(matrix_id=auxtim_id,
                      # matrix_name="auxtim",
                      # matrix_description="aux time s="+str(scen_id),
                      # default_value=0,
                      # overwrite=True)
        # create_matrix(matrix_id=twtime_id,
                      # matrix_name="twtime",
                      # matrix_description="tot wait time s="+str(scen_id),
                      # default_value=0,
                      # overwrite=True)
        # create_matrix(matrix_id=fwtime_id,
                      # matrix_name="fwtime",
                      # matrix_description="first wait time s="+str(scen_id),
                      # default_value=0,
                      # overwrite=True)
        # create_matrix(matrix_id=boatim_id,
                      # matrix_name="boatim",
                      # matrix_description="board time s="+str(scen_id),
                      # default_value=0,
                      # overwrite=True)
        # create_matrix(matrix_id=noboa_id,
                      # matrix_name="noboa",
                      # matrix_description="no of board s="+str(scen_id),
                      # default_value=0,
                      # overwrite=True)
        # create_matrix(matrix_id=invlen_id,
                      # matrix_name="invlen",
                      # matrix_description="in veh lenght s="+str(scen_id),
                      # default_value=0,
                      # overwrite=True)
        # result_spec = {
            # "type": "EXTENDED_TRANSIT_MATRIX_RESULTS",
            # "total_impedance": tottim_id,
            # "actual_first_waiting_times": fwtime_id,
            # "actual_total_waiting_times": twtime_id,
            # "by_mode_subset": {
                # "modes": transit_modes,
                # "distance": invlen_id,
                # "avg_boardings": noboa_id,
                # "actual_total_boarding_times": boatim_id,
                # "actual_in_vehicle_times": inveht_id,
                # "actual_aux_transit_times": auxtim_id,
            # },
        # }
        matrix_results = self.emme_modeller.tool(
            "inro.emme.transit_assignment.extended.matrix_results")
        matrix_results(param.result_spec, scenario)
        self.logger.info("Transit assignment performed for scenario " + str(scen_id))