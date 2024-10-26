import unittest
import numpy

import utils.log as log
from modelsystem import ModelSystem, AgentModelSystem
from assignment.mock_assignment import MockAssignmentModel
from datahandling.matrixdata import MatrixData
from datatypes.demand import Demand

from pathlib import Path

TEST_DATA_PATH = Path(__file__).resolve().parent.parent / "test_data"
TEST_RESULTS_PATH = TEST_DATA_PATH / 'Results'
TEST_MATRICES_PATH = TEST_RESULTS_PATH / "test" / "Matrices"
TEST_2030_ZONEDATA = TEST_DATA_PATH / "Scenario_input_data" / "2030_test"
TEST_2023_ZONEDATA = TEST_DATA_PATH / "Base_input_data" / "2023_zonedata"
TEST_BASE_MATRICES = TEST_DATA_PATH / "Base_input_data" / "base_matrices"

class Config():
    log_format = None
    log_level = "DEBUG"
    scenario_name = "TEST"
    results_path = TEST_RESULTS_PATH

class ModelTest(unittest.TestCase):
    
    def test_models(self):
        print("Testing assignment..")
        log.initialize(Config())
        ass_model = MockAssignmentModel(MatrixData(TEST_MATRICES_PATH))

        model = ModelSystem(
            TEST_2030_ZONEDATA, TEST_2023_ZONEDATA, TEST_BASE_MATRICES,
            TEST_RESULTS_PATH, ass_model, "test")
        impedance = model.assign_base_demand()
        for ap in ass_model.assignment_periods:
            tp = ap.name
            print("Validating impedance")
            self.assertEqual(3, len(impedance[tp]))
            self.assertIsNotNone(impedance[tp]["time"])
            self.assertIsNotNone(impedance[tp]["cost"])
            self.assertIsNotNone(impedance[tp]["dist"])
            
        print("Adding demand and assigning")
        impedance = model.run_iteration(impedance)

        self.assertEquals(len(ass_model.assignment_periods), len(impedance))
        self._validate_impedances(impedance["aht"])
        self._validate_impedances(impedance["pt"])
        self._validate_impedances(impedance["iht"])

        # Check that model result does not change
        self.assertAlmostEquals(model.mode_share[0]["car"], 0.22489513375983478)
        
        print("Model system test done")
    
    def test_agent_model(self):
        log.initialize(Config())
        ass_model = MockAssignmentModel(MatrixData(TEST_MATRICES_PATH))
        model = AgentModelSystem(
            TEST_2030_ZONEDATA, TEST_2023_ZONEDATA, TEST_BASE_MATRICES,
            TEST_RESULTS_PATH, ass_model, "test")
        impedance = model.assign_base_demand()
        impedance = model.run_iteration(impedance)
        impedance = model.run_iteration(impedance, "last")

    def _validate_impedances(self, impedances):
        self.assertIsNotNone(impedances)
        self.assertIs(type(impedances), dict)
        self.assertEquals(len(impedances), 3)
        self.assertIsNotNone(impedances["time"])
        self.assertIsNotNone(impedances["cost"])
        self.assertIsNotNone(impedances["dist"])
        self.assertIs(type(impedances["time"]), dict)
        self.assertEquals(len(impedances["time"]), 10)
        self.assertIsNotNone(impedances["time"]["transit_work"])
        self.assertIs(type(impedances["time"]["transit_work"]), numpy.ndarray)
        self.assertEquals(impedances["time"]["transit_work"].ndim, 2)
        self.assertEquals(len(impedances["time"]["transit_work"]), 12)

    def _validate_demand(self, demand):
        self.assertIsNotNone(demand)
        self.assertIsNotNone(demand)
        self.assertIsInstance(demand, Demand)
        self.assertIs(type(demand.matrix), numpy.ndarray)
        self.assertEquals(demand.matrix.ndim, 2)
        self.assertEquals(demand.matrix.shape[1], 6)
