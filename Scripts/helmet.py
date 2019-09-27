import sys
import json
from utils.log import Log
from helmet_app import HelmetApplication
from utils.config import Config

config = Config.read_from_file(path="dev-config.json")
log = Log.get_instance().initialize(config)
log.info('Running helmet_app.py via Helmet command line app..')
log.debug('sys.version_info=' + str(sys.version_info[0]))
log.debug('sys.path=' + str(sys.path))
app = HelmetApplication(config)
app.run()
