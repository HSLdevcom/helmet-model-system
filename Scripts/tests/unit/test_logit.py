#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import numpy
import unittest
import parameters
from datahandling.zonedata import ZoneData
from models.logit import ModeDestModel, DestModeModel
import datahandling.resultdata as result


class LogitModelTest(unittest.TestCase):
    def test_logit_calc(self):
        result.set_path("test")
        class Purpose:
            pass
        pur = Purpose()
        zi = numpy.array([5, 6, 7, 2792, 16001, 17000, 31000, 31501])
        zd = ZoneData("2016_test", zi)
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
        pur.bounds = (0, 4)
        pur.zone_numbers = (5, 6, 7, 2792)
        for i in ("hw", "hc", "hu", "hs", "ho"):
            pur.name = i
            model = ModeDestModel(zd, pur)
            prob = model.calc_prob(impedance)
            for mode in ("car", "transit", "bike", "walk"):
                self._validate(prob[mode])
        pur.name = "so"
        model = DestModeModel(zd, pur)
        prob = model.calc_prob(impedance)
        for mode in ("car", "transit", "bike", "walk"):
            self._validate(prob[mode])
        for i in ("wo", "oo"):
            pur.name = i
            model = ModeDestModel(zd, pur)
            prob = model.calc_prob(impedance)
            for mode in ("car", "transit", "bike", "walk"):
                self._validate(prob[mode])
        pur.name = "oop"
        model = ModeDestModel(zd, pur)
        prob = model.calc_prob(impedance)
        for mode in ("car", "transit"):
            self._validate(prob[mode])
        for i in ("hwp", "hop"):
            pur.name = i
            model = ModeDestModel(zd, pur)
            prob = model.calc_prob(impedance)
            for mode in ("car", "transit"):
                self._validate(prob[mode])
        
    
    def _validate(self, prob):
        self.assertIs(type(prob), numpy.ndarray)
        self.assertEquals(prob.ndim, 2)
        self.assertEquals(prob.shape[1], 4)
        self.assertNotEquals(prob[0, 1], 0)
        assert numpy.isfinite(prob).all()