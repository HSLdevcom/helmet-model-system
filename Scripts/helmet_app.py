from utils.config import Config
from utils.log import Log
import os
from assignment.abstract_assignment import AssignmentModel
from assignment.emme_assignment import EmmeAssignmentModel
from assignment.mock_assignment import MockAssignmentModel
from data_handling import MatrixData

class HelmetApplication():

    def __init__(self, config):
        self.__config = config
        self.logger = Log.get_instance().initialize(config)
        self.logger.info("Initializing the application..")
        # TODO clean up the model initialization and initialize other relevant classes
        # We could also perhaps wrap these under some class..?
        if config.get_value(Config.USE_EMME):
            self.logger.info("Configuration set to use EMME, initializing")
            self.initialize_EMME()
            self.assignment_model = EmmeAssignmentModel(self.emme_context)
        else:
            self.logger.info("Configuration NOT using EMME")
            costs = MatrixData("2016")
            self.assignment_model = MockAssignmentModel(costs)

    
    def run(self):
        self.logger.info("Launching application..")
        if not self.validate_input():
            self.logger.error("Failed to validate input, aborting simulation")
            return

        iterations = self.__config.get_value(Config.ITERATION_COUNT)
        self.logger.info("Start simulation loop with {} iterations".format(self.__config.get_value(Config.ITERATION_COUNT)))
        for round in range(1, iterations+1):
            try:
                self.logger.info("Starting round {}".format(round))
                self.simulate()
            except Exception as error:
                is_fatal = self.handle_error("Exception at simulation round {}".format(round), error)
                if is_fatal:
                    self.logger.error("Fatal error occured, stopping simulation loop")
                    break

        self.logger.info("All done, thank you!")

    def handle_error(self, msg, exception):
        self.logger.error(msg, exception)
        fatal = True
        return fatal

    def simulate(self):
        #TODO Put the simulation logic for this round here
        pass

    def validate_input(self):
        # TODO read the scenario from parameters / config and read input data & validate it
        return True

    def initialize_EMME(self):
        #TODO figure out if we only need to do this once in the beginning or between simulations?
        from emme.emme_context import EmmeContext
        empfile = Config.get_value(Config.EMME_PATH)
        self.emme_context = EmmeContext(empfile)


# Main entry point for the application
if __name__ == "__main__":
    config = Config.read_from_file()
    app = HelmetApplication(config)
    app.run()