from utils.config import Config
from utils.log import Log
import os
from assignment.abstract_assignment import AssignmentModel
from assignment.emme_assignment import EmmeAssignmentModel
from assignment.mock_assignment import MockAssignmentModel
import assignment.departure_time as dt
from datahandling.zonedata import ZoneData
from datahandling.matrixdata import MatrixData
from demand.freight import FreightModel
from demand.trips import DemandModel
from demand.external import ExternalModel
from transform.impedance_transformer import ImpedanceTransformer
from emme.emme_context import EmmeContext
import parameters
import numpy

class HelmetApplication():

    def __init__(self, config):
        self._config = config
        self.logger = Log.get_instance()
        
        if config.get_value(Config.SCENARIO_NAME) is not None:
            name = config.get_value(Config.SCENARIO_NAME)
        else:
            name = Config.DefaultScenario
        # status to be reported in UI
        self._status = {
            "name": name,
            "state": "starting",
            "current": 0,
            "completed": 0,
            "failed": 0,
            "total": config.get_value(Config.ITERATION_COUNT),
            "log": self.logger.get_filename()
        }
        
        self.logger.info("Initializing matrices and models..", extra=self._get_status())
        self.zdata_base = ZoneData("2016")
        self.zdata_forecast = ZoneData(self._config.get_value(Config.DATA_PATH))
        self.basematrices = MatrixData("base")

        self.dm = DemandModel(self.zdata_forecast)
        self.fm = FreightModel(self.zdata_base, self.zdata_forecast, self.basematrices)
        self.em = ExternalModel(self.basematrices, self.zdata_forecast)
      
        if config.get_value(Config.USE_EMME):
            self.logger.info("Initializing Emme..")
            self.emme_context = EmmeContext(self._config.get_value(Config.EMME_PROJECT_PATH))
            self.ass_model = EmmeAssignmentModel(self.emme_context)
        else:
            self.logger.info("Initializing MockAssignmentModel..")
            costs = MatrixData("2016")
            self.ass_model = MockAssignmentModel(costs)
        
        self.dtm = dt.DepartureTimeModel(self.ass_model.nr_zones)
        self.imptrans = ImpedanceTransformer()
        self.ass_classes = dict.fromkeys(parameters.emme_mtx["demand"].keys())
    

    def run(self):
        self._status["state"] = "preparing"
        iterations = self._config.get_value(Config.ITERATION_COUNT)

        self.logger.info("Starting simulation with {} iterations..".format(iterations), extra=self._get_status())

        if not self._validate_input():
            self._status['state'] = 'aborted'
            self.logger.error("Failed to validate input, simulation aborted.", extra=self._get_status())
            return
        
        self.mode_share = []
        self._status["results"] = self.mode_share

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
                self.ass_model.calc_transit_cost(self.zdata_forecast.transit_zone)
        
            impedance[tp] = self.ass_model.get_impedance()

        self._status["state"] = "running"
        for round in range(1, iterations+1):
            self._status["current"] = round
            try:
                self.logger.info("Starting iteration {}".format(round), extra=self._get_status())
                impedance = self.simulate(impedance)
                self._status["completed"] = self._status["completed"] + 1
            except Exception as error:
                self._status["failed"] = self._status["failed"] + 1
                is_fatal = self.handle_error("Exception at iteration {}".format(round), error)
                if is_fatal:
                    self.logger.error("Fatal error occured, simulation aborted.", extra=self._get_status())
                    break
            if round == iterations:
                self._status['state'] = 'finished'

        self.logger.info("Simulation ended.", extra=self._get_status())


    def handle_error(self, msg, exception):
        self.logger.error(msg, exception)
        fatal = True
        return fatal


    def simulate(self, impedance):
        
        self.dtm.add_demand(self.trucks)
        self.dtm.add_demand(self.trailer_trucks)
        
        for purpose in self.dm.tour_purposes:
            
            purpose_impedance = self.imptrans.transform(purpose, impedance)
            if purpose.name == "hoo":
                l, u = purpose.bounds
                nr_zones = u - l
                purpose.generate_tours()
                for mode in purpose.model.dest_choice_param:
                    for i in xrange(0, nr_zones):
                        demand = purpose.distribute_tours(mode, purpose_impedance[mode], i)
                        self.dtm.add_demand(demand)
            else:
                demand = purpose.calc_demand(purpose_impedance)
                if purpose.dest != "source":
                    for mode in demand:
                        self.dtm.add_demand(demand[mode])

        trip_sum = {}

        for mode in parameters.external_modes:

            if mode == "truck":
                int_demand = self.trucks.matrix.sum(0) + self.trucks.matrix.sum(1)
            elif mode == "trailer_truck":
                int_demand = self.trailer_trucks.matrix.sum(0) + self.trailer_trucks.matrix.sum(1)
            else:
                nr_zones = len(self.zdata_base.zone_numbers)
                int_demand = numpy.zeros(nr_zones)
            
                for purpose in self.dm.tour_purposes:
                    if purpose.dest != "source":
                        l, u = purpose.bounds
                        int_demand[l:u] += purpose.generated_tours[mode]
                        int_demand += purpose.attracted_tours[mode]
            
            ext_demand = self.em.calc_external(mode, int_demand)
            trip_sum[mode] = int_demand.sum()
            self.dtm.add_demand(ext_demand)
        
        sum_all = sum(trip_sum.values())
        mode_share = {}
        for mode in trip_sum:
            mode_share[mode] = trip_sum[mode] / sum_all
        self.mode_share.append(mode_share)

        impedance = {}
        
        for tp in parameters.emme_scenario:
            n = self.ass_model.mapping[parameters.first_external_zone]
            self.dtm.add_vans(tp, n)
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

    def _get_status(self):
        return { "status": self._status }


# Main entry point for the application
if __name__ == "__main__":
    config = Config.read_from_file()
    Log.get_instance().initialize(config)
    app = HelmetApplication(config)
    app.run()