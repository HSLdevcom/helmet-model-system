import unittest

import logging
import os
import numpy
from assignment.mock_assignment import MockAssignmentModel
import assignment.departure_time as dt
from data_handling import ZoneData, MatrixData
from demand.freight import FreightModel
import demand.hs15 as hs15
from transform.impedance_transformer import ImpedanceTransformer
from parameters import emme_scenario, emme_mtx, tour_purposes, tour_modes

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
        imptrans = ImpedanceTransformer()
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
            impedance = ass_model.get_impedance()
-           travel_cost[tp] = impedance
            print("Validating impedance")
            self.assertEqual(3, len(impedance))
            self.assertIsNotNone(impedance["time"])
            self.assertIsNotNone(impedance["cost"])
            self.assertIsNotNone(impedance["dist"])
            
        print("Adding demand and assigning")

        for purpose in tour_purposes:
            for mode in tour_modes:
                demand = hs15.calc_demand(purpose, mode, impedance)
                dtm.add_demand(purpose, mode, demand)
        dtm.add_demand("freight", "truck", trucks)
        dtm.add_demand("freight", "trailer_truck", trailer_trucks)
        travel_cost = {}
        for tp in emme_scenario:
            dtm.add_vans(tp)
            ass_model.assign(tp, dtm.demand[tp])
            travel_cost[tp] = ass_model.get_impedance()
        dtm.init_demand()
        self.assertEquals(len(emme_scenario), len(demand_travel_costs))
        self._validate_demand_impedances(demand_travel_costs["aht"])
        self._validate_demand_impedances(demand_travel_costs["pt"])
        self._validate_demand_impedances(demand_travel_costs["iht"])
        
        print("Assignment test done")


    def _validate_demand_impedances(self, impedances):
        self.assertIsNotNone(impedances)
        assert type(impedances) is dict
        self.assertEquals(len(impedances), 3)
        self.assertIsNotNone(impedances["time"])
        self.assertIsNotNone(impedances["cost"])
        self.assertIsNotNone(impedances["dist"])
        