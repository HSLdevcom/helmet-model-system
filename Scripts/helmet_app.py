from utils.config import Config

class HelmetApplication():
    
    def __init__(self, config):
        self.__config = config
        print config.get_value(Config.KEY_ITERATION_COUNT)
        print config.get_value(Config.KEY_USE_EMME)
    
    def start_estimation(self):
        iterations = self.__config.get_value(Config.KEY_ITERATION_COUNT)
        print "Start estimation loop with {} iterations".format(self.__config.get_value(Config.KEY_ITERATION_COUNT))
        for round in range(1, iterations+1):
            try:
                print "Starting round {}".format(round)
            except Exception as error:
                is_fatal = self.handle_error(error)
                if is_fatal:
                    print "Fatal error occured, stopping estimation loop"
                    break    
        print "All done, thank you!"

    def handle_error(self, error):
        print "Error occured: {}".format(error.__traceback__)
        fatal = True
        return fatal


# Main entry point for the application
if __name__ == "__main__":
    print("Launching application")
    #TODO initialize logging
    config = Config.read_from_file()

    app = HelmetApplication(config)
    app.start_estimation()