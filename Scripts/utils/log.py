import os
import sys
import json
import logging
from pathlib import Path
import logging.handlers


# Wrapper on top of standard Python logging interface so we can easily configure
# output of the logs in one single place. 
# Possible output targets: 
#   - stdout
#   - Log file
#   - EMME 

filename = None

def initialize(args):
    # JSON logger for communicating with UI
    logger = logging.getLogger()
    numeric_level = getattr(logging, args.log_level, 20)
    if args.log_format == 'JSON':
        jsonFormat = logging.Formatter('%(json)s')
        streamHandler = logging.StreamHandler(sys.stderr)
        streamHandler.flush = sys.stderr.flush
        streamHandler.setFormatter(jsonFormat)
        streamHandler.setLevel(logging.DEBUG) # always debug to pass everything to UI
        logger.addHandler(streamHandler)
    else:
        logging.basicConfig(
            level=numeric_level, stream=sys.stdout, 
            format='%(asctime)s [%(levelname)s] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',)
    # Rotating file logger
    file = args.scenario_name + ".log"
    result_dir = Path(args.results_path) / args.scenario_name
    result_dir.mkdir(parents=True, exist_ok=True)
    global filename
    filename = result_dir / file
    fileFormat = logging.Formatter(
        '%(asctime)s [%(levelname)s] %(message)s', '%Y-%m-%d %H:%M:%S')
    fileHandler = logging.handlers.TimedRotatingFileHandler(
        filename, when='H', interval=10, backupCount=7)
    fileHandler.setFormatter(fileFormat)
    fileHandler.setLevel(numeric_level)
    logger.addHandler(fileHandler)
    logger.setLevel(logging.DEBUG) # this has to match the lowest for different levels to work?

def debug(msg, *args, **kwargs):
    json = json_entry(msg, "DEBUG", *args, **kwargs)
    logging.getLogger().debug(msg, *args, extra=json)

def info(msg, *args, **kwargs):
    json = json_entry(msg, "INFO", *args, **kwargs)
    logging.getLogger().info(msg, *args, extra=json)
    
def warn(msg, *args, **kwargs):
    json = json_entry(msg, "WARN", *args, **kwargs)
    logging.getLogger().warn(msg, *args, extra=json)

def error(msg, exception=None, *args, **kwargs):
    print_stacktrace = exception is not None
    json = json_entry(msg, "ERROR", *args, **kwargs)
    logging.getLogger().error(msg, exc_info=print_stacktrace, *args, extra=json)

def json_entry(msg, level, *args, **kwargs):
    entry = { "message": msg, "level": level }
    if (kwargs.get("extra") is not None):
        entry.update(kwargs.get("extra"))
    return { "json": json.dumps(entry) }
