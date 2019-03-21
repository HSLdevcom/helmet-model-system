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
    
    def assign(self, scen_id, matrices):
        """Assign cars, bikes and transit for one time period."""
        self.logger.info("Assignment starts...")
        self.set_matrices(matrices)
        function_file = os.path.join(self.path,"d411_pituusriippuvaiset_HM30.in")
        self.process(function_file)
        self.calc_road_cost(scen_id)
        self.assign_cars(scen_id, param.stopping_criteria_coarse)
        self.assign_transit(scen_id)
        
    def set_matrix(self, id, mtx):
        self.emme_modeller.emmebank.matrix(id).set_numpy_data(mtx)
    
    def set_matrices(self, matrices):
        emmebank = self.emme_modeller.emmebank
        for mtx in matrices:
            id = param.emme_mtx["demand"][mtx]["id"]
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
            "expression": ( param.emme_mtx["time"]["car"]["id"]
                          + "-" + str(param.vot_inv)
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
                if cumulative_time > 0:
                    cumulative_speed = cumulative_length / cumulative_time * 60
                # Headway standard deviation for buses and trams
                if line.mode.id in param.headway_sd:
                    headway_sd = param.headway_sd[line.mode.id](
                        cumulative_time,
                        cumulative_speed)
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
        matrix_results(param.result_spec, scenario)
        self.logger.info("Transit assignment performed for scenario " + str(scen_id))