#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import os
import logging
import numpy

import assignment.emme_assignment as ass
from datahandling.zonedata import ZoneData
from datahandling.matrixdata import MatrixData
from assignment.emme_bindings.emme_project import EmmeProject


class EmmeAssignmentTest:
    def __init__(self):
        logging.basicConfig(format='%(asctime)s %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S',
                            level=logging.INFO)
        script_dir = os.path.dirname(os.path.realpath('__file__'))
        project_dir = os.path.join(script_dir, "..")
        for file_name in os.listdir(project_dir):
            if file_name.endswith(".emp"):
                empfile = os.path.join(project_dir, file_name)
        emme_context = EmmeProject(empfile)
        self.ass_model = ass.EmmeAssignmentModel(emme_context, 19)
        self.ass_model.prepare_network()
    
    def test_assignment(self):
        nr_zones = self.ass_model.nr_zones
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
        travel_cost = {}
        for tp in ("aht", "pt", "iht"):
            travel_cost[tp] = self.ass_model.assign(tp, demand, iteration="init")
        costs_files = MatrixData(os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            "..", "Matrices", "2016_test"))
        for time_period in travel_cost:
            for mtx_type in travel_cost[time_period]:
                zone_numbers = self.ass_model.zone_numbers
                with costs_files.open(mtx_type, time_period, zone_numbers, 'w') as mtx:
                    for ass_class in travel_cost[time_period][mtx_type]:
                        cost_data = travel_cost[time_period][mtx_type][ass_class]
                        mtx[ass_class] = cost_data

    def test_transit_cost(self):
        ZONE_INDEXES = numpy.array([5, 6, 7, 2792, 16001, 17000, 31000, 31501])
        zdata = ZoneData(os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "tests", "test_data",
            "Scenario_input_data", "2030_test"), ZONE_INDEXES)
        peripheral_cost = numpy.ones((2, 6))
        self.ass_model.calc_transit_cost(zdata.transit_zone, peripheral_cost)


em = EmmeAssignmentTest()
em.test_transit_cost()
em.test_assignment()
