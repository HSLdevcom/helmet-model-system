import os
import json


class Config:
    
    SCENARIO_NAME = 'SCENARIO_NAME'
    ITERATION_COUNT = 'ITERATION_COUNT'
    USE_EMME = 'USE_EMME'
    LOG_LEVEL = 'LOG_LEVEL'
    LOG_FORMAT = 'LOG_FORMAT'
    DATA_PATH = 'DATA_PATH'
    EMME_PROJECT_PATH = 'EMME_PROJECT_PATH'
    USE_FIXED_TRANSIT_COST = 'USE_FIXED_TRANSIT_COST'
    FIRST_SCENARIO_ID = 'FIRST_SCENARIO_ID'

    DefaultScenario = "helmet"

    def __init__(self):
        self.__config = {}

    @staticmethod
    def read_from_file(path="dev-config.json"):
        print 'reading configuration from file "{}"'.format(path)
        instance = Config()

        with open(path, 'r') as f:
            instance.__config = json.load(f)

        print 'read {} config variables'.format(len(instance.__config))
        return instance

    def get_value(self, key):
        # TODO MON: reverse maybe to "if config set -> that, else if os-environ set -> that, else None / raise KeyError or ValueError
        # TODO MON: would make sense because initially {}, from file or set_value -> we don't wanna override by env(?), default env, else is error
        from_env = os.environ.get(key, None)
        if from_env:
            return from_env
        else:
            return self.__config[key]

    # TODO MON: maybe use e.g. @property EMME_PROJECT_PATH(self): and @EMME_PROJECT_PATH.setter, and rename __set_value & __get_value
    def set_value(self, key, value):
        self.__config[key] = value
