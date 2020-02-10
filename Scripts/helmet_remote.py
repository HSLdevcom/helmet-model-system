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
scenario = line['scenario']
use_fixed_transit_cost = line['use_fixed_transit_cost']
first_scenario_id = line['first_scenario_id']

# set configuration per incoming params
config = Config()
config.set_value(Config.LOG_FORMAT, 'JSON')
config.set_value(Config.LOG_LEVEL, log_level)
config.set_value(Config.DATA_PATH, data_path)
config.set_value(Config.EMME_PROJECT_PATH, emme_path)
config.set_value(Config.ITERATION_COUNT, iterations)
config.set_value(Config.USE_EMME, True)
config.set_value(Config.USE_FIXED_TRANSIT_COST, use_fixed_transit_cost)
config.set_value(Config.FIRST_SCENARIO_ID, first_scenario_id)
config.set_value(Config.SCENARIO_NAME, scenario)

log = Log.get_instance().initialize(config)
log.info('Running helmet_app.py via Helmet UI..')
log.debug('sys.version_info=' + str(sys.version_info[0]))
log.debug('sys.path=' + str(sys.path))
log.debug('log_level=' + log_level)
log.debug('emme_path=' + emme_path)
log.debug('data_path=' + data_path)
log.debug('iterations=' + str(iterations))
log.debug('use_fixed_transit_cost=' + str(use_fixed_transit_cost))
log.debug('first_scenario_id=' + str(first_scenario_id))
log.debug('scenario_name=' + scenario)

app = HelmetApplication(config)
app.run()
