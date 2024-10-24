#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy
import pandas
import unittest
from datahandling.zonedata import BaseZoneData
from models.logit import ModeDestModel
from datahandling.resultdata import ResultsData
import os

TEST_DATA_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "test_data")
METROPOLITAN_ZONES = [102, 103, 244, 1063, 1531, 2703, 2741, 6272, 6291]
PERIPHERAL_ZONES = [19071]
EXTERNAL_ZONES = [34102, 34500]


class LogitModelTest(unittest.TestCase):
    def test_logit_calc(self):
        resultdata = ResultsData(os.path.join(TEST_DATA_PATH, "Results", "test"))
        class Purpose:
            pass
        pur = Purpose()
        zi = numpy.array(METROPOLITAN_ZONES + PERIPHERAL_ZONES + EXTERNAL_ZONES)
        zd = BaseZoneData(os.path.join(TEST_DATA_PATH, "Base_input_data", "2023_zonedata"), zi)
        zd["car_users"] = pandas.Series(0.5, zd.zone_numbers)
        mtx = numpy.arange(90, dtype=numpy.float32)
        mtx.shape = (9, 10)
        mtx[numpy.diag_indices(9)] = 0
        impedance = {
            "car": {
                "time": mtx,
                "cost": mtx,
                "dist": mtx,
            },
            "transit": {
                "time": mtx,
                "cost": mtx,
                "dist": mtx,
            },
            "bike": {
                "dist": mtx,
            },
            "walk": {
                "dist": mtx,
            },
            "park_and_ride": {
                "time": mtx,
                "cost": mtx,
                "dist": mtx,
            }
        }
        pur.bounds = slice(0, 9)
        pur.sub_bounds = [slice(0, 7), slice(7, 9)]
        pur.zone_numbers = METROPOLITAN_ZONES
        for i in ("hw", "hc", "hu", "hs", "ho"):
            pur.name = i
            model = ModeDestModel(zd, pur, resultdata)
            prob = model.calc_prob(impedance)
            for mode in ("car", "transit", "bike", "walk"):
                self._validate(prob[mode])
        for i in ("wo", "oo"):
            pur.name = i
            model = ModeDestModel(zd, pur, resultdata)
            prob = model.calc_prob(impedance)
            for mode in ("car", "transit", "bike", "walk"):
                self._validate(prob[mode])
        pur.name = "oop"
        model = ModeDestModel(zd, pur, resultdata)
        prob = model.calc_prob(impedance)
        for mode in ("car", "transit"):
            self._validate(prob[mode])
        for i in ("hwp", "hop"):
            pur.name = i
            model = ModeDestModel(zd, pur, resultdata)
            prob = model.calc_prob(impedance)
            for mode in ("car", "transit"):
                self._validate(prob[mode])

    def _validate(self, prob):
        self.assertIs(type(prob), numpy.ndarray)
        self.assertEquals(prob.ndim, 2)
        self.assertEquals(prob.shape[1], 9)
        self.assertNotEquals(prob[0, 1], 0)
        assert numpy.isfinite(prob).all()