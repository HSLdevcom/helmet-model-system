import unittest
import os


from helmet_validate_inputfiles import main
import utils.log as log


TEST_DATA_PATH = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), "..", "test_data")


class Args:
    log_format = None
    log_level = "DEBUG"
    baseline_data_path = os.path.join(TEST_DATA_PATH, "Base_input_data")
    emme_paths = [
        os.path.join(
            TEST_DATA_PATH, "Scenario_input_data", "2030_test", "2016.cco"),
    ]
    first_scenario_ids = ["test"]
    forecast_data_paths = [
        os.path.join(TEST_DATA_PATH, "Scenario_input_data", "2030_test"),
    ]
    results_path = os.path.join(TEST_DATA_PATH, "Results")
    scenario_name = "test"
    do_not_use_emme = True


class ValdidationTest(unittest.TestCase):

    def test_validation(self):
        print("Testing input file validation..")
        log.initialize(Args())
        main(Args())
