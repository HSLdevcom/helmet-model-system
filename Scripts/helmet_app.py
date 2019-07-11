from utils.config import Config
from utils.log import Log
import os
from assignment.abstract_assignment import AssignmentModel
from assignment.emme_assignment import EmmeAssignmentModel
from assignment.mock_assignment import MockAssignmentModel
import assignment.departure_time as dt
from data_handling import ZoneData, MatrixData
from demand.freight import FreightModel
from demand.trips import DemandModel
from demand.external import ExternalModel
from transform.impedance_transformer import ImpedanceTransformer
from datatypes.purpose import create_purposes
from emme.emme_context import EmmeContext
import parameters
import numpy

class HelmetApplication():

    def __init__(self, config):
        self._config = config
        self.logger = Log.get_instance()
        self.logger.info("Initializing the application..")

        self.zdata_base = ZoneData("2016")
        self.zdata_forecast = ZoneData(self._config.get_value(Config.DATA_PATH))
        self.basematrices = MatrixData("base")

        self.dm = DemandModel(self.zdata_forecast)
        self.fm = FreightModel(self.zdata_base, self.zdata_forecast, self.basematrices)
        self.em = ExternalModel(self.basematrices, self.zdata_forecast)

        if config.get_value(Config.USE_EMME):
            self.logger.info("Initializing EMME..")
            self.emme_context = EmmeContext(self._config.get_value(Config.EMME_PROJECT_PATH))
            self.ass_model = EmmeAssignmentModel(self.emme_context)
        else:
            self.logger.info("Initializing MockAssignmentModel..")
            costs = MatrixData("2016")
            self.ass_model = MockAssignmentModel(costs)
        
        self.dtm = dt.DepartureTimeModel(self.ass_model)
        self.imptrans = ImpedanceTransformer(self.ass_model)
        self.ass_classes = dict.fromkeys(parameters.emme_mtx["demand"].keys())
        self.tour_purposes = create_purposes()
    
    def run(self):
        iterations = self._config.get_value(Config.ITERATION_COUNT)
        self.logger.info("Running simulation with {} iterations".format(self._config.get_value(Config.ITERATION_COUNT)))

        if not self._validate_input():
            self.logger.error("Failed to validate input, simulation aborted.")
            return
        
        self.trucks = self.fm.calc_freight_traffic("truck")
        self.trailer_trucks = self.fm.calc_freight_traffic("trailer_truck")
        impedance = {}
        
        for tp in parameters.emme_scenario:
            base_demand = {}
            self.basematrices.open_file("demand", tp)
        
            for ass_class in self.ass_classes:
                base_demand[ass_class] = self.basematrices.get_data(ass_class)
        
            self.basematrices.close()
            self.ass_model.assign(tp, base_demand)
        
            if tp == "aht":
                self.ass_model.calc_transit_cost()
        
            impedance[tp] = self.ass_model.get_impedance()

        for round in range(1, iterations+1):
            try:
                self.logger.info("Starting iteration {}".format(round))
                impedance = self.simulate(impedance)
            except Exception as error:
                is_fatal = self.handle_error("Exception at iteration {}".format(round), error)
                if is_fatal:
                    self.logger.error("Fatal error occured, simulation aborted.")
                    break

        self.logger.info("All done, thank you!")

    def handle_error(self, msg, exception):
        self.logger.error(msg, exception)
        fatal = True
        return fatal

    def simulate(self, impedance):
        
        self.dtm.add_demand("freight", "truck", self.trucks)
        self.dtm.add_demand("freight", "trailer_truck", self.trailer_trucks)
        
        for purpose in self.tour_purposes:
            
            purpose_impedance = self.imptrans.transform(purpose, impedance)
            demand = self.dm.calc_demand(purpose, purpose_impedance)
            self._validate_demand(demand)
            
            if purpose.area == "peripheral":
                pos = self.ass_model.get_mapping()[16001]
                mtx_position = (pos, 0)
            else:
                mtx_position = (0, 0)

            if purpose.dest != "source":
                for mode in demand:
                    self.dtm.add_demand(purpose.name, mode, demand[mode], mtx_position)
        
        pos = self.ass_model.get_mapping()[31001]
        
        for mode in parameters.external_modes:

            if mode == "truck":
                int_demand = self.trucks.sum(0) + self.trucks.sum(1)
            elif mode == "trailer_truck":
                int_demand = self.trailer_trucks.sum(0) + self.trailer_trucks.sum(1)
            else:
                nr_zones = len(self.zdata_base.zone_numbers)
                int_demand = numpy.zeros(nr_zones)
            
                for purpose in self.tour_purposes:
                    if purpose.dest != "source":
                        l, u = self.zdata_base.get_bounds(purpose)
                        int_demand[l:u] += purpose.generated_tours[mode]
                        int_demand += purpose.attracted_tours[mode]
            
            ext_demand = self.em.calc_external(mode, int_demand)
            self.dtm.add_demand("external", mode, ext_demand, (pos, 0))

        impedance = {}
        
        for tp in parameters.emme_scenario:
            self.dtm.add_vans(tp)
            self.ass_model.assign(tp, self.dtm.demand[tp])
            impedance[tp] = self.ass_model.get_impedance()
        
        self.dtm.init_demand()
        return impedance

    def _validate_input(self):
        # TODO read the scenario from parameters / config and read input data & validate it
        return True

    def _validate_demand(self, demand):
        # TODO read the scenario from parameters / config and read input data & validate it
        return True

    def initialize_EMME(self):
        from emme.emme_context import EmmeContext
        empfile = self._config.get_value(Config.EMME_PROJECT_PATH)
        self.emme_context = EmmeContext(empfile)


# Main entry point for the application
if __name__ == "__main__":
    config = Config.read_from_file()
    Log.get_instance().initialize(config)
    app = HelmetApplication(config)
    app.run()