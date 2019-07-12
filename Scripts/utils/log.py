import os
import sys
import logging
import logging.handlers
from pythonjsonlogger import jsonlogger
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
        self.__logger = logging.getLogger()

    @staticmethod
    def get_instance():
        if Log.__instance is None:
            Log.__instance = Log()
        return Log.__instance

    def initialize(self, config, emme_context=None):
        # JSON logger for communicating with UI
        if config.get_value(Config.LOG_FORMAT) == 'JSON':
            jsonFormat = jsonlogger.JsonFormatter()
            streamHandler = logging.StreamHandler(sys.stderr)
            streamHandler.flush = sys.stderr.flush
            streamHandler.setFormatter(jsonFormat)
            streamHandler.setLevel(logging.DEBUG) # always debug to pass everything to UI
            self.__logger.addHandler(streamHandler)
        # Rotating file logger
        filename = os.path.join(sys.path[0], 'helmet.log')
        numeric_level = getattr(logging, config.get_value(Config.LOG_LEVEL), 20)
        fileFormat = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
        fileHandler = logging.handlers.TimedRotatingFileHandler(filename, when='midnight', backupCount=7)
        fileHandler.setFormatter(fileFormat)
        fileHandler.setLevel(numeric_level)
        self.__logger.addHandler(fileHandler)
        self.__logger.setLevel(logging.DEBUG) # this has to match the lowest for different levels to work?
        return Log.__instance

    def add_stream_handler(self, handler):
        self.__logger.addHandler(handler)

    def debug(self, msg, *args, **kwargs):
        self.__logger.debug(msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        self.__logger.info(msg, *args, **kwargs)
        
    def warn(self, msg, *args, **kwargs):
        self.__logger.warn(msg, *args, **kwargs)

    def error(self, msg, exception=None, *args, **kwargs):
        print_stacktrace = exception is not None
        self.__logger.error(msg, exc_info=print_stacktrace, *args, **kwargs)
