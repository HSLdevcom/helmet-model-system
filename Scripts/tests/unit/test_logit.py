#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import numpy
import unittest
import parameters
from datahandling.zonedata import ZoneData
from models.logit import ModeDestModel
import datahandling.resultdata as result


class LogitModelTest(unittest.TestCase):
    def test_logit_calc(self):
        result.set_path("test")
        class Purpose:
            pass
        pur = Purpose()
        pur.bounds = (0, 4)
        zd = ZoneData("2016_test")
        mtx = numpy.arange(24)
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
        for i in ("hw", "hc", "hu", "hs", "ho", "wo", "oo"):
            pur.name = i
            model = ModeDestModel(zd, pur)
            prob = model.calc_prob(impedance)
            for mode in ("car", "transit", "bike", "walk"):
                self.assertIs(type(prob[mode]), numpy.ndarray)
                self.assertEquals(prob[mode].ndim, 2)
                self.assertEquals(prob[mode].shape[1], 4)
                self.assertNotEquals(prob[mode][0, 1], 0)
                assert numpy.isfinite(prob[mode]).all()
        for i in ("hwp", "hop", "oop"):
            pur.name = i
            model = ModeDestModel(zd, pur)
            prob = model.calc_prob(impedance)
            for mode in ("car", "transit"):
                self.assertIs(type(prob[mode]), numpy.ndarray)
                self.assertEquals(prob[mode].ndim, 2)
                self.assertEquals(prob[mode].shape[1], 4)
                self.assertNotEquals(prob[mode][0, 1], 0)
                assert numpy.isfinite(prob[mode]).all()