#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import numpy
import unittest
from assignment.departure_time import DepartureTimeModel


class DepartureTimeTest(unittest.TestCase):
    def test_mtx_add(self):
        emme_scenarios = {"aht": 21, "pt": 22, "iht": 23}
        dtm = DepartureTimeModel(8, emme_scenarios)
        mtx = numpy.arange(9)
        mtx.shape = (3, 3)
        class Demand:
            pass
        class Purpose:
            pass
        dem = Demand()
        pur = Purpose()
        dem.purpose = pur

        dem.purpose.name = "hoo"
        dem.mode = "car"
        dem.matrix = mtx
        dem.orig = 1
        dem.dest = None
        dem.position = (1, 0, 0)
        dtm.add_demand(dem)

        dem.purpose.name = "hw"
        dem.mode = "bike"
        dem.dest = 2
        dem.matrix = numpy.array([[3]])
        dem.position = (1, 2)
        dtm.add_demand(dem)

        dem.purpose.name = "ho"
        dem.purpose.sec_dest_purpose = Purpose()
        dem.purpose.sec_dest_purpose.name = "hoo"
        dem.mode = "transit"
        dem.matrix = numpy.array([[3]])
        dem.position = (1, 2, 0)
        dtm.add_demand(dem)

        self.assertIsNotNone(dtm.demand)
        self.assertIs(type(dtm.demand["iht"]["car_leisure"]), numpy.ndarray)
        self.assertEquals(dtm.demand["pt"]["car_leisure"].ndim, 2)
        self.assertEquals(dtm.demand["aht"]["bike_work"].shape[1], 8)
        self.assertNotEquals(dtm.demand["iht"]["car_work"][0, 1], 0)
