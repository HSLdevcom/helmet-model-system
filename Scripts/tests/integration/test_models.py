import unittest

import logging
import os
import numpy
from assignment.mock_assignment import MockAssignmentModel
import assignment.departure_time as dt
from data_handling import ZoneData, MatrixData
from demand.freight import FreightModel
from parameters import emme_scenario, emme_mtx

class ModelTest(unittest.TestCase):
    
    def test_models(self):
        print("Testing assignment..")

        zdata_base = ZoneData("2016")
        zdata_forecast = ZoneData("2030")
        basematrices = MatrixData("base")
        fm = FreightModel(zdata_base, zdata_forecast, basematrices)
        trucks = fm.calc_freight_traffic("truck")
        trailer_trucks = fm.calc_freight_traffic("trailer_truck")
        costs = MatrixData("2016")
        ass_model = MockAssignmentModel(costs)
        dtm = dt.DepartureTimeModel(ass_model)
        ass_classes = dict.fromkeys(emme_mtx["demand"].keys())

        self.assertEqual(7, len(ass_classes))

        travel_cost = {}
        for tp in emme_scenario:
            base_demand = {}
            basematrices.open_file("demand", tp)
            for ass_class in ass_classes:
                base_demand[ass_class] = basematrices.get_data(ass_class)
            basematrices.close()
            ass_model.assign(tp, base_demand)
            
            impendance = ass_model.get_impedance()
            travel_cost[tp] = impendance
            print("Validating impedance")
            self.assertEqual(3, len(impendance))
            self.assertIsNotNone(impendance["time"])
            self.assertIsNotNone(impendance["cost"])
            self.assertIsNotNone(impendance["dist"])
            

        nr_zones = len(ass_model.get_zone_numbers())
        car_matrix = numpy.arange(6).reshape(2, 3)
        demand = {
            "hw": {
                "car": car_matrix,
                "transit": car_matrix,
                "bike": car_matrix,
            },
            "hs": {
                "car": car_matrix,
            },
            "ho": {
                "car": car_matrix,
            },
        }

        print("Adding demand and assigning")

        for purpose in demand:
            for mode in demand[purpose]:
                dtm.add_demand(purpose, mode, demand[purpose][mode])
        dtm.add_demand("freight", "truck", trucks)
        dtm.add_demand("freight", "trailer_truck", trailer_trucks)
        dtm.assign()

        print("Assignment test done")
