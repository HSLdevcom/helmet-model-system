from config import Config

class HelmetApplication():

    def __init__(self, config):
        print config.get_value('ITERATION_COUNT')


# Main entry point for the application
if __name__ == "__main__":
    print("Launching application")
    config = Config.read_from_file()

    HelmetApplication(config)