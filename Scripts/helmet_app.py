from utils.config import Config
from utils.log import Log
from datahandling import resultdata
from assignment.emme_assignment import EmmeAssignmentModel
from assignment.mock_assignment import MockAssignmentModel
from modelsystem import ModelSystem
from datahandling.matrixdata import MatrixData
from emme.emme_context import EmmeContext


class HelmetApplication:
    # TODO MON: (after all else): refactor as def main(config): if .run() is always used in same manner (one-time)
    def __init__(self, config):
        self._config = config
        self.logger = Log.get_instance()
        # TODO MON: ternary operator would simplify this
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
        resultdata.set_path(name)
        if config.get_value(Config.USE_EMME):
            self.logger.info("Initializing Emme..")
            # TODO MON: redundant (one-time-use) variable
            emme_context = EmmeContext(self._config.get_value(Config.EMME_PROJECT_PATH))
            ass_model = EmmeAssignmentModel(emme_context, first_scenario_id=config.get_value(Config.FIRST_SCENARIO_ID))
        else:
            self.logger.info("Initializing MockAssignmentModel..")
            ass_model = MockAssignmentModel(MatrixData(config.get_value(Config.SCENARIO_NAME)))
        self.model = ModelSystem(self._config.get_value(Config.DATA_PATH), "2016", "base", ass_model, name)
        self._status["results"] = self.model.mode_share

    def run(self):
        self._status["state"] = "preparing"
        iterations = self._config.get_value(Config.ITERATION_COUNT)
        self.logger.info("Starting simulation with {} iterations..".format(iterations), extra=self._get_status())
        # TODO MON: decide if this is redundant or not?
        if not self._validate_input():
            self._status['state'] = 'aborted'
            self.logger.error("Failed to validate input, simulation aborted.", extra=self._get_status())
            return
        impedance = self.model.assign_base_demand(Config.USE_FIXED_TRANSIT_COST)
        self._status["state"] = "running"
        for i in range(1, iterations+1):
            self._status["current"] = i
            try:
                self.logger.info("Starting iteration {}".format(i), extra=self._get_status())
                # TODO MON: consider ternary operator to clarify it's the "same" operation with an extra argument
                if i == iterations:
                    impedance = self.model.run(impedance, is_last_iteration=True)
                else:
                    impedance = self.model.run(impedance)
                self._status["completed"] = self._status["completed"] + 1
            # TODO MON: consider moving away from catch-all, if main purpose is to increase verbosity of failures
            # TODO MON: though, in this case (main()) it may be necessary evil. Talk it, maybe multiple exceptions?
            except Exception as error:
                self._status["failed"] = self._status["failed"] + 1
                is_fatal = self.handle_error("Exception at iteration {}".format(i), error)
                if is_fatal:
                    self.logger.error("Fatal error occured, simulation aborted.", extra=self._get_status())
                    break
            if i == iterations:
                self._status['state'] = 'finished'
        self.logger.info("Simulation ended.", extra=self._get_status())

    def handle_error(self, msg, exception):
        # TODO MON: this is 100% redundant
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
        # TODO MON: This seems redundant, bringing unnecessary complexity vs. self.status (or in def main() glob status)
        return { "status": self._status }


# Main entry point for the application
if __name__ == "__main__":
    # TODO MON: argparser together with Config.read_from_file (as base default), explain use (now that GUI exist) vs CLI
    file_based_config = Config.read_from_file()
    Log.get_instance().initialize(file_based_config)
    app = HelmetApplication(file_based_config)
    app.run()
