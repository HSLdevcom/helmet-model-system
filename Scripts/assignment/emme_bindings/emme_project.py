import os
import utils.log as log
import logging
import inro.emme.desktop.app as _app
import inro.modeller as _m


# Creates and initializes EMME-resources (INRO's own library, from EMME-software's Python site-packages)
class EmmeProject:
    def __init__(self, filepath):
        log.info("Starting Emme...")
        emme_desktop = _app.start_dedicated(
            project=filepath, 
            visible=False, 
            user_initials="HSL"
        )
        # Add logging to EMME
        sh = logging.StreamHandler(stream=self)
        logging.getLogger().addHandler(sh)

        self.modeller = _m.Modeller(emme_desktop)
        log.info("Emme started")
        self.path = os.path.dirname(self.modeller.emmebank.path)
        self.copy_scenario = self.modeller.tool(
            "inro.emme.data.scenario.copy_scenario")
        self.create_matrix = self.modeller.tool(
            "inro.emme.data.matrix.create_matrix")
        self.copy_matrix = self.modeller.tool(
            "inro.emme.data.matrix.copy_matrix")
        self.network_calc = self.modeller.tool(
            "inro.emme.network_calculation.network_calculator")
        self.process_functions = self.modeller.tool(
            "inro.emme.data.function.function_transaction")
        self.car_assignment = self.modeller.tool(
            "inro.emme.traffic_assignment.sola_traffic_assignment")
        self.bike_assignment = self.modeller.tool(
            "inro.emme.traffic_assignment.standard_traffic_assignment")
        self.pedestrian_assignment = self.modeller.tool(
            "inro.emme.transit_assignment.standard_transit_assignment")
        self.transit_assignment = self.modeller.tool(
            "inro.emme.transit_assignment.extended_transit_assignment")
        self.congested_assignment = self.modeller.tool(
            "inro.emme.transit_assignment.congested_transit_assignment")
        self.matrix_results = self.modeller.tool(
            "inro.emme.transit_assignment.extended.matrix_results")
        self.network_results = self.modeller.tool(
            "inro.emme.transit_assignment.extended.network_results")
        self.create_extra_attribute = self.modeller.tool(
            "inro.emme.data.extra_attribute.create_extra_attribute")
    
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
