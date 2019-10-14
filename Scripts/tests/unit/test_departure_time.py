#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import numpy
import unittest
import parameters
from assignment.departure_time import DepartureTimeModel


class DepartureTimeTest(unittest.TestCase):
    def test_mtx_add(self):
        dtm = DepartureTimeModel(8)
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
        dem.position = (1, 0, 0)
        dtm.add_demand(dem)

        dem.purpose.name = "hw"
        dem.mode = "bike"
        dem.matrix = 3
        dem.position = (1, 2)
        dtm.add_demand(dem)

        dem.purpose.name = "hoo"
        dem.mode = "transit"
        dem.matrix = 3
        dem.position = (1, 2, 0)
        dtm.add_demand(dem)

        self.assertIsNotNone(dtm.demand)
        self.assertIs(type(dtm.demand["iht"]["car_leisure"]), numpy.ndarray)
        self.assertEquals(dtm.demand["pt"]["car_work"].ndim, 2)
        self.assertEquals(dtm.demand["aht"]["bike"].shape[1], 8)
        self.assertNotEquals(dtm.demand["iht"]["car_leisure"][0, 1], 0)