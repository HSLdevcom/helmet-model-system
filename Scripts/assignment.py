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
        pass