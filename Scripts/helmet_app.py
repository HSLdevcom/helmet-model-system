from utils.config import Config
from utils.log import Log

class HelmetApplication():

    def __init__(self, config):
        self.__config = config
        self.logger = Log.get_instance()
        self.logger.info("Configuration set to use EMME: {}".format(config.get_value(Config.KEY_USE_EMME)))
        
    
    def start_estimation(self):
        iterations = self.__config.get_value(Config.KEY_ITERATION_COUNT)
        self.logger.info("Start estimation loop with {} iterations".format(self.__config.get_value(Config.KEY_ITERATION_COUNT)))
        for round in range(1, iterations+1):
            try:
                self.logger.info("Starting round {}".format(round))
            except Exception as error:
                is_fatal = self.handle_error(error)
                if is_fatal:
                    self.logger.error("Fatal error occured, stopping estimation loop")
                    break    
        self.logger.info("All done, thank you!")

    def handle_error(self, error):
        self.logger.error("Error occured: {}".format(error.__traceback__))
        fatal = True
        return fatal


# Main entry point for the application
if __name__ == "__main__":
    print "Initializing the application.."
    
    config = Config.read_from_file()
    Log.get_instance().initialize(config)
    
    Log.get_instance().info("Launching application")
    
    app = HelmetApplication(config)
    app.start_estimation()