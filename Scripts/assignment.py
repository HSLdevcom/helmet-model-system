import os
import logging
import inro.emme.desktop.app as _app
import inro.modeller as _m
import parameters

class AssignmentModel:
    def __init__(self, filepath):
        self.logger = logging.getLogger()
        self.logger.info("Starting Emme...")
        self.emme_desktop = _app.start_dedicated(
            project=filepath, 
            visible=False, 
            user_initials="HSL"
        )
        sh = logging.StreamHandler(stream=self)
        self.logger.addHandler(sh)
        self.emme_modeller = _m.Modeller(self.emme_desktop)
        self.logger.info("Emme started.")
        self.process = self.emme_modeller.tool(
            "inro.emme.data.function.function_transaction")
        self.path = os.path.dirname(self.emme_modeller.emmebank.path)
    
    def write(self, message):
        """Write to logbook."""
        # _m.logbook_write(message)
        try:
            self.cm.__exit__(None, None, None)
        except AttributeError:
            pass
        self.cm = _m.logbook_trace(message)
        self.cm.__enter__()
        
    def flush(self):
        """Flush the logbook (i.e., do nothing)."""
        pass
    
    def assign(self):
        """Assign cars, bikes and transit for all time periods."""
        self.logger.info("Assignment starts...")
        function_file = os.path.join(self.path,"d411_pituusriippuvaiset_HM30.in")
        self.process(function_file)
        self.calc_road_cost(21)
        self.calc_road_cost(22)
        self.calc_road_cost(23)
        
    def calc_road_cost (self, scen_id):
        """Calculate road charges and driving costs for one scenario."""
        self.logger.info("Calculates road charges for scenario " + str(scen_id) + "...")
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
            "expression": str(parameters.dist_cost)+"*length",
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