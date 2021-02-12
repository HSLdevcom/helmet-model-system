#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import numpy
import pandas
import unittest
from utils.zone_interval import Aggregator


class AreaFindTest(unittest.TestCase):
    def test_find_area(self):
        a = Aggregator(None, None)
        orig = 1007
        self.assertEquals(a.find_area(orig), "helsinki_other")
        dest = 17601
        self.assertEquals(a.find_area(dest), "peripheral")
        a.add(orig, dest)
        self.assertEquals(a.matrix.at["helsinki_other", "peripheral"], 1)
