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
        dtm.add_demand("hoo", "car", mtx, (1, 0, 0))
        dtm.add_demand("hw", "bike", 3, (1, 2))
        dtm.add_demand("hoo", "transit", 3, (1, 2, 0))
