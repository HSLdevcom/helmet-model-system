#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import unittest
import numpy
import os

from utils.validate_network import validate
from assignment.emme_bindings.mock_project import MockProject
from assignment.emme_assignment import EmmeAssignmentModel
from datahandling.resultdata import ResultsData


class EmmeAssignmentTest(unittest.TestCase):
    def test_assignment(self):
        context = MockProject()
        scenario_dir = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            "..", "test_data", "Network")
        scenario_id = 19
        context.import_scenario(scenario_dir, scenario_id, "test")
        fares = {
            "fare": {
                'A': 59,
            },
            "exclusive": {},
            "dist_fare": 3.0,
            "start_fare": 35,
        }
        validate(
            context.modeller.emmebank.scenario(scenario_id).get_network(),
            fares)
        ass_model = EmmeAssignmentModel(
            context, scenario_id, save_matrices=True)
        ass_model.prepare_network()
        peripheral_cost = numpy.arange(10).reshape((1, 10))
        ass_model.calc_transit_cost(fares, peripheral_cost)
        nr_zones = ass_model.nr_zones
        car_matrix = numpy.arange(nr_zones**2).reshape(nr_zones, nr_zones)
        demand = {
            "car_work": car_matrix,
            "car_leisure": car_matrix,
            "transit_work": car_matrix,
            "transit_leisure": car_matrix,
            "bike": car_matrix,
            "trailer_truck": car_matrix,
            "truck": car_matrix,
            "van": car_matrix,
        }
        ass_model.init_assign(demand)
        resultdata = ResultsData(os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            "..", "test_data", "Results", "test"))
        ass_model.aggregate_results(resultdata)
        ass_model.calc_noise()
        resultdata.flush()
