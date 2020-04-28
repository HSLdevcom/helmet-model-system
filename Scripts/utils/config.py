import os
import json


class Config:

    DefaultScenario = "helmet"

    def __init__(self):
        self.__config = {}

    @staticmethod
    def read_from_file(path=os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "dev-config.json")):
        instance = Config()
        with open(path, 'r') as f:
            instance.__config = json.load(f)
        return instance

    def __get_value(self, key):
        # Lookup from explicitly set values
        if key in self.__config:
            return self.__config[key]
        # As backup, try lookup from environment variables
        elif os.environ.get(key, None) is not None:
            return os.environ[key]
        # Else raise KeyError since the config was instantiated without setting the key
        else:
            raise KeyError("Tried to lookup Config.{} which isn't set and doesn't exist in environment variables".format(key))

    def __set_value(self, key, value):
        self.__config[key] = value

    @property
    def SCENARIO_NAME(self): return self.__get_value("SCENARIO_NAME")

    @SCENARIO_NAME.setter
    def SCENARIO_NAME(self, value): self.__set_value("SCENARIO_NAME", value)

    @property
    def ITERATION_COUNT(self): return self.__get_value("ITERATION_COUNT")

    @ITERATION_COUNT.setter
    def ITERATION_COUNT(self, value): self.__set_value("ITERATION_COUNT", value)

    @property
    def USE_EMME(self): return self.__get_value("USE_EMME")

    @USE_EMME.setter
    def USE_EMME(self, value): self.__set_value("USE_EMME", value)

    @property
    def LOG_LEVEL(self): return self.__get_value("LOG_LEVEL")

    @LOG_LEVEL.setter
    def LOG_LEVEL(self, value): self.__set_value("LOG_LEVEL", value)

    @property
    def LOG_FORMAT(self): return self.__get_value("LOG_FORMAT")

    @LOG_FORMAT.setter
    def LOG_FORMAT(self, value): self.__set_value("LOG_FORMAT", value)

    @property
    def BASELINE_DATA_PATH(self): return self.__get_value("BASELINE_DATA_PATH")

    @BASELINE_DATA_PATH.setter
    def BASELINE_DATA_PATH(self, value): self.__set_value("BASELINE_DATA_PATH", value)

    @property
    def FORECAST_DATA_PATH(self): return self.__get_value("FORECAST_DATA_PATH")

    @FORECAST_DATA_PATH.setter
    def FORECAST_DATA_PATH(self, value): self.__set_value("FORECAST_DATA_PATH", value)

    @property
    def RESULTS_PATH(self): return self.__get_value("RESULTS_PATH")

    @RESULTS_PATH.setter
    def RESULTS_PATH(self, value): self.__set_value("RESULTS_PATH", value)

    @property
    def EMME_PROJECT_PATH(self): return self.__get_value("EMME_PROJECT_PATH")

    @EMME_PROJECT_PATH.setter
    def EMME_PROJECT_PATH(self, value): self.__set_value("EMME_PROJECT_PATH", value)

    @property
    def USE_FIXED_TRANSIT_COST(self): return self.__get_value("USE_FIXED_TRANSIT_COST")

    @USE_FIXED_TRANSIT_COST.setter
    def USE_FIXED_TRANSIT_COST(self, value): self.__set_value("USE_FIXED_TRANSIT_COST", value)

    @property
    def FIRST_SCENARIO_ID(self): return self.__get_value("FIRST_SCENARIO_ID")

    @FIRST_SCENARIO_ID.setter
    def FIRST_SCENARIO_ID(self, value): self.__set_value("FIRST_SCENARIO_ID", value)
