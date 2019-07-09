import sys
import json
from utils.log import Log
from helmet_app import HelmetApplication
from utils.config import Config

# read incoming message from the UI
line = json.loads(sys.stdin.readline())
log_level = line['log_level']
emme_path = line['emme_path']
data_path = line['data_path']
iterations = line['iterations']

# set configuration per incoming params
config = Config()
config.set_value(Config.LOG_FORMAT, 'JSON')
config.set_value(Config.LOG_LEVEL, log_level)
config.set_value(Config.DATA_PATH, data_path)
config.set_value(Config.EMME_PROJECT_PATH, emme_path)
config.set_value(Config.ITERATION_COUNT, iterations)
config.set_value(Config.USE_EMME, True)

log = Log.get_instance().initialize(config)
log.debug('{"level":"DEBUG", "msg":"starting helmet_app.."}')
log.debug('{"level":"DEBUG", "msg":"sys.version_info=' + str(sys.version_info[0]) + '"}')
log.debug('{"level":"DEBUG", "msg":"sys.path=' + str(sys.path) + '"}')
log.debug('{"level":"DEBUG", "msg":"log_level=' + log_level + '"}')
log.debug('{"level":"DEBUG", "msg":"emme_path=' + emme_path + '"}')
log.debug('{"level":"DEBUG", "msg":"data_path=' + data_path + '"}')
log.debug('{"level":"DEBUG", "msg":"iterations=' + str(iterations) + '"}')

app = HelmetApplication(config)
app.run()
