import unittest

import logging
import os
import numpy
from assignment.mock_assignment import MockAssignmentModel
import assignment.departure_time as dt
from data_handling import ZoneData, MatrixData
from demand.freight import FreightModel
from demand.trips import DemandModel
from transform.impedance_transformer import ImpedanceTransformer
from parameters import emme_scenario, emme_mtx, tour_purposes

class ModelTest(unittest.TestCase):
    
    def test_models(self):
        print("Testing assignment..")

        zdata_base = ZoneData("2016")
        zdata_forecast = ZoneData("2030")
        basematrices = MatrixData("base")
        dm = DemandModel(zdata_forecast)
        fm = FreightModel(zdata_base, zdata_forecast, basematrices)
        trucks = fm.calc_freight_traffic("truck")
        trailer_trucks = fm.calc_freight_traffic("trailer_truck")
        costs = MatrixData("2016")
        ass_model = MockAssignmentModel(costs)
        dtm = dt.DepartureTimeModel(ass_model)
        imptrans = ImpedanceTransformer(ass_model)
        ass_classes = dict.fromkeys(emme_mtx["demand"].keys())

        self.assertEqual(7, len(ass_classes))

        impedance = {}
        for tp in emme_scenario:
            base_demand = {}
            basematrices.open_file("demand", tp)
            for ass_class in ass_classes:
                base_demand[ass_class] = basematrices.get_data(ass_class)
            basematrices.close()
            ass_model.assign(tp, base_demand)
            impedance[tp] = ass_model.get_impedance()
            print("Validating impedance")
            self.assertEqual(3, len(impedance[tp]))
            self.assertIsNotNone(impedance[tp]["time"])
            self.assertIsNotNone(impedance[tp]["cost"])
            self.assertIsNotNone(impedance[tp]["dist"])
            
        print("Adding demand and assigning")

        for purpose in tour_purposes:
            purpose_impedance = imptrans.transform(purpose, impedance)
            demand = dm.calc_demand(purpose, purpose_impedance)
            if tour_purposes[purpose]["area"] == "peripheral":
                pos = ass_model.get_mapping()[16001]
                mtx_position = (pos, 0)
            else:
                mtx_position = (0, 0)
            for mode in demand:
                dtm.add_demand(purpose, mode, demand[mode], mtx_position)
        dtm.add_demand("freight", "truck", trucks)
        dtm.add_demand("freight", "trailer_truck", trailer_trucks)
        impedance = {}
        for tp in emme_scenario:
            dtm.add_vans(tp)
            ass_model.assign(tp, dtm.demand[tp])
            impedance[tp] = ass_model.get_impedance()
        dtm.init_demand()
        self.assertEquals(len(emme_scenario), len(impedance))
        self._validate_impedances(impedance["aht"])
        self._validate_impedances(impedance["pt"])
        self._validate_impedances(impedance["iht"])
        
        print("Assignment test done")


    def _validate_impedances(self, impedances):
        self.assertIsNotNone(impedances)
        assert type(impedances) is dict
        self.assertEquals(len(impedances), 3)
        self.assertIsNotNone(impedances["time"])
        self.assertIsNotNone(impedances["cost"])
        self.assertIsNotNone(impedances["dist"])
        