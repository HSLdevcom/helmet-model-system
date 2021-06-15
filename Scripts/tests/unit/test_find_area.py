#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy
import pandas
import unittest
from utils.zone_interval import MatrixAggregator, belongs_to_area


class AreaFindTest(unittest.TestCase):
    def test_find_area(self):
        a = MatrixAggregator([101, 1006, 1007, 1009, 10001, 17601, 23000])
        orig = 1007
        self.assertEquals(a.mapping[orig], "helsinki_other")
        dest = 17601
        self.assertEquals(a.mapping[dest], "peripheral")
        a.add(orig, dest)
        self.assertEquals(a.matrix.at["helsinki_other", "peripheral"], 1)

    def test_belongs_to_area(self):
        class Node:
            id = "test"
            x = 25497000
            y = 6673000
        node = Node()
        node.data3 = 91
        area = belongs_to_area(node)
        self.assertEquals(area, "helsinki_cbd")
        node.data3 = 245
        area = belongs_to_area(node)
        self.assertEquals(area, "surround_train")
