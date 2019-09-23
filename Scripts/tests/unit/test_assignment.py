#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import unittest
import assignment.emme_assignment as ass
import numpy
import omx
import os
from parameters import emme_scenario, demand_share
from datahandling.matrixdata import MatrixData
from emme.emme_context import EmmeContext

class EmmeAssignmentTest(unittest.TestCase):
    def test_assignment(self):
        script_dir = os.path.dirname(os.path.realpath('__file__'))
        project_dir = os.path.join(script_dir, "..")
        for file_name in os.listdir(project_dir):
            if file_name.endswith(".emp"):
                empfile = os.path.join(project_dir, file_name)
        emme_context = EmmeContext(empfile)
        ass_model = ass.EmmeAssignmentModel(emme_context, 0.12)
        nr_zones = ass_model.nr_zones
        car_matrix = numpy.arange(nr_zones**2).reshape(nr_zones, nr_zones)
        demand = {
            "car_work": car_matrix,
            "car_leisure": car_matrix,
            "transit": car_matrix,
            "bike": car_matrix,
            "trailer_truck": car_matrix,
            "truck": car_matrix,
            "van": car_matrix,
        }
        travel_cost = {}
        for tp in emme_scenario:
            ass_model.assign(tp, demand)
            travel_cost[tp] = ass_model.get_impedance()
        costs_files = MatrixData("2016")
        for time_period in travel_cost:
            for mtx_type in travel_cost[time_period]:
                zone_numbers = ass_model.zone_numbers
                costs_files.open_file(mtx_type, time_period, 'w')
                costs_files.set_mapping(zone_numbers)
                for ass_class in travel_cost[time_period][mtx_type]:
                    cost_data = travel_cost[time_period][mtx_type][ass_class]
                    costs_files.set_data(cost_data, ass_class)
                costs_files.close()
