import unittest
from pathlib import Path

from helmet_validate_inputfiles import main
import utils.log as log

TEST_DATA_PATH = Path(__file__).resolve().parent.parent / "test_data"

class Args:
    log_format = None
    log_level = "DEBUG"
    baseline_data_path = TEST_DATA_PATH / "Base_input_data"
    emme_paths = [
        TEST_DATA_PATH / "Scenario_input_data" / "2030_test" / "2016.cco",
    ]
    first_scenario_ids = ["test"]
    forecast_data_paths = [
        TEST_DATA_PATH / "Scenario_input_data" / "2030_test",
    ]
    results_path = TEST_DATA_PATH / "Results"
    scenario_name = "test"
    do_not_use_emme = True

class ValidationTest(unittest.TestCase):

    def test_validation(self):
        print("Testing input file validation..")
        log.initialize(Args())
        main(Args())
