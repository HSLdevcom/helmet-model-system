import unittest

import logging
import os
import numpy
import modelsystem
import datahandling.resultdata as result
from assignment.mock_assignment import MockAssignmentModel
from datahandling.matrixdata import MatrixData
from demand.freight import FreightModel
from datatypes.demand import Demand
import parameters

class ModelTest(unittest.TestCase):
    
    def test_models(self):
        print("Testing assignment..")
        result.set_path("test")
        ass_model = MockAssignmentModel(MatrixData("2016_test"))
        model = modelsystem.ModelSystem("2030_test", "2016_test", "base_test", ass_model, "test")
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
        impedance = model.run(impedance)
        # for mode in demand:
        #     self._validate_demand(demand[mode])
        self.assertEquals(len(parameters.emme_scenario), len(impedance))
        self._validate_impedances(impedance["aht"])
        self._validate_impedances(impedance["pt"])
        self._validate_impedances(impedance["iht"])
        
        print("Assignment test done")
    
    def test_agent_model(self):
        result.set_path("test")
        ass_model = MockAssignmentModel(MatrixData("2016_test"))
        model = modelsystem.ModelSystem("2030_test", "2016_test", "base_test", ass_model, "test", is_agent_model=True)
        impedance = model.assign_base_demand()
        impedance = model.run(impedance)

    def _validate_impedances(self, impedances):
        self.assertIsNotNone(impedances)
        self.assertIs(type(impedances), dict)
        self.assertEquals(len(impedances), 3)
        self.assertIsNotNone(impedances["time"])
        self.assertIsNotNone(impedances["cost"])
        self.assertIsNotNone(impedances["dist"])
        self.assertIs(type(impedances["time"]), dict)
        self.assertEquals(len(impedances["time"]), 5)
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
        