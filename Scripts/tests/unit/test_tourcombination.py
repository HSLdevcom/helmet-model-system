#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy
import pandas
import unittest
from datahandling.zonedata import ZoneData
from models.tour_combinations import TourCombinationModel
import os

TEST_DATA_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "test_data")
METROPOLITAN_ZONES = [102, 103, 244, 1063, 1531, 2703, 2741, 6272, 6291]
PERIPHERAL_ZONES = [19071]
EXTERNAL_ZONES = [31102, 31500]


class TourCombinationModelTest(unittest.TestCase):
    def test_generation(self):
        zi = numpy.array(METROPOLITAN_ZONES + PERIPHERAL_ZONES + EXTERNAL_ZONES)
        zd = ZoneData(
            os.path.join(TEST_DATA_PATH, "Base_input_data", "2018_zonedata"), zi)
        zd._values["hu_t"] = pandas.Series(0.0, METROPOLITAN_ZONES)
        zd._values["ho_w"] = pandas.Series(0.0, METROPOLITAN_ZONES)
        model = TourCombinationModel(zd)
        prob = model.calc_prob("age_50-64", False, 102)
        self.assertIs(type(prob[("hw",)]), numpy.float64)
        self.assertAlmostEquals(sum(prob.values()), 1)
        prob = model.calc_prob("age_7-17", True, slice(0, 9))
        self.assertIs(type(prob[()]), pandas.core.series.Series)
        self.assertEquals(prob[("hw", "ho")].values.ndim, 1)
        self.assertEquals(prob[("hw", "hs")].values.shape[0], 9)
