#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import os
import logging
import numpy

import assignment.emme_assignment as ass
from datahandling.zonedata import ZoneData
from datahandling.matrixdata import MatrixData
from datahandling.resultdata import ResultsData
from assignment.emme_bindings.emme_project import EmmeProject
import inro.emme.desktop.app as _app
import inro.emme.database.emmebank as _eb


class EmmeAssignmentTest:
    """Create small EMME test network and test assignments.

    On first run, create new EMME project and database files.
    """
    def __init__(self):
        logging.basicConfig(format='%(asctime)s %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S',
                            level=logging.INFO)
        project_dir = os.path.join(
            os.path.dirname(os.path.realpath('__file__')),
            "tests", "test_data", "Results")
        project_name = "test_assignment"
        db_dir = os.path.join(project_dir, project_name, "Database")
        try:
            project_path = _app.create_project(project_dir, project_name)
            os.makedirs(db_dir)
        except FileExistsError:
            project_path = os.path.join(
                project_dir, project_name, project_name + ".emp")
        dim = {
            "scalar_matrices": 100,
            "origin_matrices": 100,
            "destination_matrices": 100,
            "full_matrices": 400,
            "scenarios": 5,
            "centroids": 20,
            "regular_nodes": 1000,
            "links": 2000,
            "turn_entries": 100,
            "transit_vehicles": 30,
            "transit_lines": 20,
            "transit_segments": 2000,
            "extra_attribute_values": 300000,
            "functions": 99,
            "operators": 5000,
            "sola_analyses": 240,
        }
        scenario_num = 19
        try:
            eb = _eb.create(os.path.join(db_dir, "emmebank"), dim)
            eb.create_scenario(scenario_num)
            emmebank_path = eb.path
            eb.dispose()
        except RuntimeError:
            emmebank_path = None
        emme_context = EmmeProject(project_path, emmebank_path)
        emme_context.import_scenario(
            os.path.join(project_dir, "..", "Network"), scenario_num, "test",
            overwrite=True)
        self.ass_model = ass.EmmeAssignmentModel(emme_context, scenario_num)
        self.ass_model.prepare_network()
    
    def test_assignment(self):
        nr_zones = self.ass_model.nr_zones
        car_matrix = numpy.full((nr_zones, nr_zones), 10.0)
        demand = {
            "car_work": car_matrix,
            "car_leisure": car_matrix,
            "transit_work": car_matrix,
            "transit_leisure": car_matrix,
            "car_first_mile": car_matrix,
            "car_last_mile": car_matrix,
            "bike": car_matrix,
            "trailer_truck": car_matrix,
            "truck": car_matrix,
            "van": car_matrix,
        }
        travel_cost = {}
        self.ass_model.init_assign(demand)
        self.test_transit_cost()
        for ap in self.ass_model.assignment_periods:
            travel_cost[ap.name] = ap.assign(demand, iteration="last")
            travel_cost[ap.name]["time"]["transit_uncongested"] = travel_cost[ap.name]["time"]["transit_work"]
        resultdata = ResultsData(os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            "tests", "test_data", "Results", "assignment"))
        self.ass_model.aggregate_results(resultdata)
        self.ass_model.calc_noise()
        resultdata.flush()
        costs_files = MatrixData(os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            "tests", "test_data", "Results", "assignment", "Matrices"))
        for time_period in travel_cost:
            for mtx_type in travel_cost[time_period]:
                zone_numbers = self.ass_model.zone_numbers
                with costs_files.open(mtx_type, time_period, zone_numbers, 'w') as mtx:
                    for ass_class in travel_cost[time_period][mtx_type]:
                        cost_data = travel_cost[time_period][mtx_type][ass_class]
                        mtx[ass_class] = cost_data

    def test_transit_cost(self):
        zdata = ZoneData(os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "tests", "test_data",
            "Scenario_input_data", "2030_test"), self.ass_model.zone_numbers)
        peripheral_cost = numpy.ones((1, 10))
        self.ass_model.calc_transit_cost(zdata.transit_zone, peripheral_cost)


em = EmmeAssignmentTest()
em.test_assignment()
