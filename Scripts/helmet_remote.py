import sys
import json
from utils.log import Log
from helmet_app import HelmetApplication
from utils.config import Config

print '{"level":"DEBUG", "msg":"starting helmet_app.."}'
print '{"level":"DEBUG", "msg":"python_version=' + str(sys.version_info[0]) + ', sys.path=' + str(sys.path) + '"}'

line = json.loads(sys.stdin.readline())
log_level = line['log_level']
emme_path = line['emme_path']
data_path = line['data_path']
iterations = line['iterations']

print '{"level":"DEBUG", "msg": "log_level ' + log_level + '"}'
print '{"level":"DEBUG", "msg": "emme_path ' + emme_path + '"}'
print '{"level":"DEBUG", "msg": "data_path ' + data_path + '"}'
print '{"level":"DEBUG", "msg": "iterations ' + str(iterations) + '"}'

config = Config()
config.set_value(Config.LOG_FORMAT, 'JSON')
config.set_value(Config.LOG_LEVEL, log_level)
config.set_value(Config.DATA_PATH, data_path)
config.set_value(Config.EMME_PROJECT_PATH, emme_path)
config.set_value(Config.ITERATION_COUNT, iterations)
config.set_value(Config.USE_EMME, True)

app = HelmetApplication(config)
app.run()
