import unittest
import numpy

import utils.log as log
from modelsystem import ModelSystem, AgentModelSystem
from assignment.mock_assignment import MockAssignmentModel
from datahandling.matrixdata import MatrixData
from datatypes.demand import Demand
import parameters
import os

TEST_DATA_PATH = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), "..", "test_data")

class Config():
    LOG_FORMAT = None
    LOG_LEVEL = "DEBUG"
    SCENARIO_NAME = "TEST"
    RESULTS_PATH = os.path.join(TEST_DATA_PATH, "Results")

class ModelTest(unittest.TestCase):
    
    def test_models(self):
        print("Testing assignment..")
        log.initialize(Config())
        results_path = os.path.join(TEST_DATA_PATH, "Results")
        ass_model = MockAssignmentModel(
            MatrixData(os.path.join(results_path, "test", "Matrices")))
        zone_data_path = os.path.join(
            TEST_DATA_PATH, "Scenario_input_data", "2030_test")
        base_zone_data_path = os.path.join(
            TEST_DATA_PATH, "Base_input_data", "2016_zonedata")
        base_matrices_path = os.path.join(
            TEST_DATA_PATH, "Base_input_data", "base_matrices")
        model = ModelSystem(
            zone_data_path, base_zone_data_path, base_matrices_path,
            results_path, ass_model, "test")
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
        self.assertAlmostEquals(model.mode_share[0]["car"], 0.44038986782290057)
        
        print("Model system test done")
    
    def test_agent_model(self):
        log.initialize(Config())
        results_path = os.path.join(TEST_DATA_PATH, "Results")
        ass_model = MockAssignmentModel(MatrixData(
            os.path.join(results_path, "test", "Matrices")))
        zone_data_path = os.path.join(
            TEST_DATA_PATH, "Scenario_input_data", "2030_test")
        base_zone_data_path = os.path.join(
            TEST_DATA_PATH, "Base_input_data", "2016_zonedata")
        base_matrices_path = os.path.join(
            TEST_DATA_PATH, "Base_input_data", "base_matrices")
        model = AgentModelSystem(
            zone_data_path, base_zone_data_path, base_matrices_path,
            results_path, ass_model, "test")
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
        self.assertEquals(len(impedances["time"]["transit_work"]), 8)

    def _validate_demand(self, demand):
        self.assertIsNotNone(demand)
        self.assertIsNotNone(demand)
        self.assertIsInstance(demand, Demand)
        self.assertIs(type(demand.matrix), numpy.ndarray)
        self.assertEquals(demand.matrix.ndim, 2)
        self.assertEquals(demand.matrix.shape[1], 6)
