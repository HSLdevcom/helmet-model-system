#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import unittest
import numpy
import os

from assignment.emme_bindings.mock_project import MockProject
from assignment.emme_assignment import EmmeAssignmentModel
from datahandling.resultdata import ResultsData


class EmmeAssignmentTest(unittest.TestCase):
    def test_assignment(self):
        context = MockProject()
        for scenario in context.modeller.emmebank.scenarios():
            network = scenario.get_network()
            for idx in ('c', 'b'):
                network.create_mode(idx)
            network.create_transit_vehicle(0, 'b')
            for idx in (101, 4003, 16001, 16002):
                node = network.create_node(idx, is_centroid=True)
                node.label = 'A'
            for idx in range(1, 5):
                node = network.create_node(idx)
                node.label = 'A'
            for od in ((1, 2), (2, 3), (3, 4)):
                link = network.create_link(*od, modes=['c', 'b'])
                link.length = 3.5
            line = network.create_transit_line("1", 0, [1, 2])
            line.headway = 5
            line = network.create_transit_line("2", 0, [2, 3])
            line.headway = 10
        ass_model = EmmeAssignmentModel(context, 19)
        ass_model.prepare_network()
        fares = {
            "fare": {
                'A': 59,
            },
            "exclusive": {},
            "dist_fare": 3.0,
            "start_fare": 35,
        }
        peripheral_cost = numpy.arange(8).reshape((2, 4))
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
            "..", "test_data", "Results", "2016_test"))
        ass_model.aggregate_results(resultdata)
        ass_model.calc_noise()
        resultdata.flush()
