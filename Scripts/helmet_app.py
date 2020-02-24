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
    # yes
    def __init__(self, config):
        self._config = config
        self.logger = Log.get_instance()
        name = config.SCENARIO_NAME if config.SCENARIO_NAME is not None else Config.DefaultScenario
        # status to be reported in UI
        self._status = {
            "name": name,
            "state": "starting",
            "current": 0,
            "completed": 0,
            "failed": 0,
            "total": config.ITERATION_COUNT,
            "log": self.logger.get_filename()
        }
        self.logger.info("Initializing matrices and models..", extra=self._get_status())
        resultdata.set_path(name)
        if config.USE_EMME:
            self.logger.info("Initializing Emme..")
            ass_model = EmmeAssignmentModel(EmmeContext(self._config.EMME_PROJECT_PATH), first_scenario_id=config.FIRST_SCENARIO_ID)
        else:
            self.logger.info("Initializing MockAssignmentModel..")
            ass_model = MockAssignmentModel(MatrixData(config.SCENARIO_NAME))
        self.model = ModelSystem(self._config.DATA_PATH, "2016", "base", ass_model, name)
        self._status["results"] = self.model.mode_share

    def run(self):
        self._status["state"] = "preparing"
        iterations = self._config.ITERATION_COUNT
        self.logger.info("Starting simulation with {} iterations..".format(iterations), extra=self._get_status())
        impedance = self.model.assign_base_demand(Config.USE_FIXED_TRANSIT_COST)
        self._status["state"] = "running"
        for i in range(1, iterations+1):
            self._status["current"] = i
            try:
                self.logger.info("Starting iteration {}".format(i), extra=self._get_status())
                impedance = (self.model.run_iteration(impedance, is_last_iteration=True)
                             if i == iterations
                             else self.model.run_iteration(impedance))
                self._status["completed"] = self._status["completed"] + 1
            # TODO MON: consider moving away from catch-all, if main purpose is to increase verbosity of failures
            # TODO MON: though, in this case (main()) it may be necessary evil. Talk it, maybe multiple exceptions?
            # --
            except Exception as error:
                self._status["failed"] = self._status["failed"] + 1
                self.logger.error("Exception at iteration {}".format(i), error)
                self.logger.error("Fatal error occured, simulation aborted.", extra=self._get_status())
                break
            if i == iterations:
                self._status['state'] = 'finished'
        self.logger.info("Simulation ended.", extra=self._get_status())

    def _get_status(self):
        # TODO MON: This seems redundant, bringing unnecessary complexity vs. self.status (or in def main() glob status)
        # y
        return { "status": self._status }


# Main entry point for the application
if __name__ == "__main__":
    # TODO MON: argparser together with Config.read_from_file (as base default), explain use (now that GUI exist) vs CLI
    # yes
    file_based_config = Config.read_from_file()
    Log.get_instance().initialize(file_based_config)
    app = HelmetApplication(file_based_config)
    app.run()
