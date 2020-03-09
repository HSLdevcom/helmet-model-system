#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import numpy
import unittest
from datahandling.zonedata import ZoneData
from models.logit import ModeDestModel
from datahandling.resultdata import ResultsData
import os

TEST_DATA_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "test_data")


class LogitModelTest(unittest.TestCase):
    def test_logit_calc(self):
        resultdata = ResultsData(os.path.join(TEST_DATA_PATH, "Results", "test"))
        class Purpose:
            pass
        pur = Purpose()
        zi = numpy.array([5, 6, 7, 2792, 16001, 17000, 31000, 31501])
        zd = ZoneData(os.path.join(TEST_DATA_PATH, "Base_input_data", "2016_zonedata_test"), zi)
        mtx = numpy.arange(24, dtype=numpy.float32)
        mtx.shape = (4, 6)
        mtx[numpy.diag_indices(4)] = 0
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
        }
        pur.bounds = slice(0, 4)
        pur.zone_numbers = (5, 6, 7, 2792)
        for i in ("hw", "hc", "hu", "hs", "ho"):
            pur.name = i
            model = ModeDestModel(zd, pur, resultdata, is_agent_model=False)
            prob = model.calc_prob(impedance)
            for mode in ("car", "transit", "bike", "walk"):
                self._validate(prob[mode])
        for i in ("wo", "oo"):
            pur.name = i
            model = ModeDestModel(zd, pur, resultdata, is_agent_model=False)
            prob = model.calc_prob(impedance)
            for mode in ("car", "transit", "bike", "walk"):
                self._validate(prob[mode])
        pur.name = "oop"
        model = ModeDestModel(zd, pur, resultdata, is_agent_model=False)
        prob = model.calc_prob(impedance)
        for mode in ("car", "transit"):
            self._validate(prob[mode])
        for i in ("hwp", "hop"):
            pur.name = i
            model = ModeDestModel(zd, pur, resultdata, is_agent_model=False)
            prob = model.calc_prob(impedance)
            for mode in ("car", "transit"):
                self._validate(prob[mode])

    def _validate(self, prob):
        self.assertIs(type(prob), numpy.ndarray)
        self.assertEquals(prob.ndim, 2)
        self.assertEquals(prob.shape[1], 4)
        self.assertNotEquals(prob[0, 1], 0)
        assert numpy.isfinite(prob).all()