from utils.config import Config
from utils.log import Log
import os
import datahandling.resultdata as result
from assignment.abstract_assignment import AssignmentModel
from assignment.emme_assignment import EmmeAssignmentModel
from assignment.mock_assignment import MockAssignmentModel
import modelsystem
from datahandling.matrixdata import MatrixData
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
        result.set_path(name)
        if config.get_value(Config.USE_EMME):
            self.logger.info("Initializing Emme..")
            emme_context = EmmeContext(self._config.get_value(Config.EMME_PROJECT_PATH))
            ass_model = EmmeAssignmentModel(emme_context)
        else:
            self.logger.info("Initializing MockAssignmentModel..")
            ass_model = MockAssignmentModel(MatrixData("2016"))
        self.model = modelsystem.ModelSystem(self._config.get_value(Config.DATA_PATH), ass_model)
        self._status["results"] = self.model.mode_share

    def run(self):
        self._status["state"] = "preparing"
        iterations = self._config.get_value(Config.ITERATION_COUNT)
        self.logger.info("Starting simulation with {} iterations..".format(iterations), extra=self._get_status())
        if not self._validate_input():
            self._status['state'] = 'aborted'
            self.logger.error("Failed to validate input, simulation aborted.", extra=self._get_status())
            return
        impedance = self.model.assign_base_demand(Config.USE_FIXED_TRANSIT_COST)
        self._status["state"] = "running"
        for round in range(1, iterations+1):
            self._status["current"] = round
            try:
                self.logger.info("Starting iteration {}".format(round), extra=self._get_status())
                impedance = self.model.run(impedance)
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