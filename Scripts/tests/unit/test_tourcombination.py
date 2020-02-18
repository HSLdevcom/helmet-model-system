#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import numpy
import pandas
import unittest
import parameters
from datahandling.zonedata import ZoneData
from models.logit import TourCombinationModel
import datahandling.resultdata as result


class TourCombinationModelTest(unittest.TestCase):
    def test_generation(self):
        zi = numpy.array([5, 6, 7, 2792, 16001, 17000, 31000, 31501])
        zd = ZoneData("2016_test", zi)
        zd._values["hu_t"] = pandas.Series([0, 0, 0, 0], [5, 6, 7, 2792])
        zd._values["ho_w"] = pandas.Series([0, 0, 0, 0], [5, 6, 7, 2792])
        model = TourCombinationModel(zd)
        prob = model.calc_prob("age_50-64", False, 6)
        self.assertIs(type(prob["hw"]), numpy.float64)
        self.assertAlmostEquals(sum(prob.values()), 1)
        prob = model.calc_prob("age_7-17", True, slice(0, 4))
        self.assertIs(type(prob["-"]), pandas.core.series.Series)
        self.assertEquals(prob["hw-ho"].values.ndim, 1)
        self.assertEquals(prob["hw-hs"].values.shape[0], 4)
        