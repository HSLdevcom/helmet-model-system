import logging
import sys
from config import Config

# Wrapper on top of standard Python logging interface so we can easily configure
# output of the logs in one single place. 
# Possible output targets: 
#   - stdout
#   - Log file
#   - EMME 
class Log:
    __instance = None
    
    def __init__(self):
        self.logger = logging.getLogger()

    @staticmethod
    def get_instance():
        if Log.__instance is None:
            Log.__instance = Log()
        return Log.__instance

    def initialize(self, config, emme_context=None):
        numeric_level = getattr(logging, config.get_value(Config.KEY_LOG_LEVEL), None)
        if not isinstance(numeric_level, int):
            print "Could not read log level from config, using level INFO"
            numeric_level = 20 # INFO = 20

        logging.basicConfig(filename='helmet.log',level=numeric_level, format='%(asctime)s [%(levelname)s] %(message)s')
        # Add output also to stdout
        self.logger.addHandler(logging.StreamHandler(sys.stdout))

    def info(self, msg):
        self.logger.info(msg)

    def warn(self, msg):
        self.logger.warn(msg)

    def error(self, msg):
        self.logger.error(msg)



