#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import numpy
import pandas
import unittest
from utils.zone_interval import MatrixAggregator


class AreaFindTest(unittest.TestCase):
    def test_find_area(self):
        a = MatrixAggregator([101, 1006, 1007, 1009, 17601, 23000])
        orig = 1007
        self.assertEquals(a.mapping[orig], "helsinki_other")
        dest = 17601
        self.assertEquals(a.mapping[dest], "peripheral")
        a.add(orig, dest)
        self.assertEquals(a.matrix.at["helsinki_other", "peripheral"], 1)
