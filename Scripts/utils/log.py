import os
import sys
import json
import logging
import logging.handlers
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
            jsonFormat = logging.Formatter('%(json)s')
            streamHandler = logging.StreamHandler(sys.stderr)
            streamHandler.flush = sys.stderr.flush
            streamHandler.setFormatter(jsonFormat)
            streamHandler.setLevel(logging.DEBUG) # always debug to pass everything to UI
            self.__logger.addHandler(streamHandler)
        # Rotating file logger
        file = config.get_value(Config.SCENARIO_NAME) + ".log"
        self._filename = os.path.join(sys.path[0], file)
        numeric_level = getattr(logging, config.get_value(Config.LOG_LEVEL), 20)
        fileFormat = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
        fileHandler = logging.handlers.TimedRotatingFileHandler(self._filename, when='midnight', backupCount=7)
        fileHandler.setFormatter(fileFormat)
        fileHandler.setLevel(numeric_level)
        self.__logger.addHandler(fileHandler)
        self.__logger.setLevel(logging.DEBUG) # this has to match the lowest for different levels to work?
        return Log.__instance

    def add_stream_handler(self, handler):
        self.__logger.addHandler(handler)

    def debug(self, msg, *args, **kwargs):
        json = self.json_entry(msg, "DEBUG", *args, **kwargs)
        self.__logger.debug(msg, *args, extra=json)

    def info(self, msg, *args, **kwargs):
        json = self.json_entry(msg, "INFO", *args, **kwargs)
        self.__logger.info(msg, *args, extra=json)
        
    def warn(self, msg, *args, **kwargs):
        json = self.json_entry(msg, "WARN", *args, **kwargs)
        self.__logger.warn(msg, *args, extra=json)

    def error(self, msg, exception=None, *args, **kwargs):
        print_stacktrace = exception is not None
        json = self.json_entry(msg, "ERROR", *args, **kwargs)
        self.__logger.error(msg, exc_info=print_stacktrace, *args, extra=json)

    def json_entry(self, msg, level, *args, **kwargs):
        entry = { "message": msg, "level": level }
        if (kwargs.get("extra") is not None):
            entry.update(kwargs.get("extra"))
        return { "json": json.dumps(entry) }

    def get_filename(self):
        return self._filename