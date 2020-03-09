import unittest
import numpy
from modelsystem import ModelSystem, AgentModelSystem
from assignment.mock_assignment import MockAssignmentModel
from datahandling.matrixdata import MatrixData
from datatypes.demand import Demand
import parameters
import os

TEST_DATA_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "test_data")


class ModelTest(unittest.TestCase):
    
    def test_models(self):
        print("Testing assignment..")
        ass_model = MockAssignmentModel(MatrixData(os.path.join(TEST_DATA_PATH, "Results", "test", "Matrices")))
        zone_data_path = os.path.join(TEST_DATA_PATH, "Scenario_input_data", "2030_test")
        base_zone_data_path = os.path.join(TEST_DATA_PATH, "Base_input_data", "2016_zonedata_test")
        base_matrices_path = os.path.join(TEST_DATA_PATH, "Base_input_data", "base_matrices_test")
        results_path = os.path.join(TEST_DATA_PATH, "Results")
        model = ModelSystem(zone_data_path, base_zone_data_path, base_matrices_path, results_path, ass_model, "test")
        # model.dm.create_population()
        # self.assertEqual(7, len(ass_classes))
        impedance = model.assign_base_demand()
        for tp in parameters.emme_scenario:
            print("Validating impedance")
            self.assertEqual(3, len(impedance[tp]))
            self.assertIsNotNone(impedance[tp]["time"])
            self.assertIsNotNone(impedance[tp]["cost"])
            self.assertIsNotNone(impedance[tp]["dist"])
            
        print("Adding demand and assigning")
        impedance = model.run_iteration(impedance)
        # for mode in demand:
        #     self._validate_demand(demand[mode])
        self.assertEquals(len(parameters.emme_scenario), len(impedance))
        self._validate_impedances(impedance["aht"])
        self._validate_impedances(impedance["pt"])
        self._validate_impedances(impedance["iht"])
        
        print("Assignment test done")
    
    def test_agent_model(self):
        ass_model = MockAssignmentModel(MatrixData(os.path.join(TEST_DATA_PATH, "Results", "test", "Matrices")))
        zone_data_path = os.path.join(TEST_DATA_PATH, "Scenario_input_data", "2030_test")
        base_zone_data_path = os.path.join(TEST_DATA_PATH, "Base_input_data", "2016_zonedata_test")
        base_matrices_path = os.path.join(TEST_DATA_PATH, "Base_input_data", "base_matrices_test")
        results_path = os.path.join(TEST_DATA_PATH, "Results")
        model = AgentModelSystem(zone_data_path, base_zone_data_path, base_matrices_path, results_path, ass_model, "test")
        impedance = model.assign_base_demand()
        impedance = model.run_iteration(impedance)

    def _validate_impedances(self, impedances):
        self.assertIsNotNone(impedances)
        self.assertIs(type(impedances), dict)
        self.assertEquals(len(impedances), 3)
        self.assertIsNotNone(impedances["time"])
        self.assertIsNotNone(impedances["cost"])
        self.assertIsNotNone(impedances["dist"])
        self.assertIs(type(impedances["time"]), dict)
        self.assertEquals(len(impedances["time"]), 8)
        self.assertIsNotNone(impedances["time"]["transit"])
        self.assertIs(type(impedances["time"]["transit"]), numpy.ndarray)
        self.assertEquals(impedances["time"]["transit"].ndim, 2)
        self.assertEquals(len(impedances["time"]["transit"]), 8)

    def _validate_demand(self, demand):
        self.assertIsNotNone(demand)
        self.assertIsNotNone(demand)
        self.assertIsInstance(demand, Demand)
        self.assertIs(type(demand.matrix), numpy.ndarray)
        self.assertEquals(demand.matrix.ndim, 2)
        self.assertEquals(demand.matrix.shape[1], 6)
