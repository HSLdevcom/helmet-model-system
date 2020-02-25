#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import unittest
from datatypes.path_analysis import PathAnalysis


class PathAnalysisTest(unittest.TestCase):
    def test_constructor(self):
        # TODO improve, put actual values here
        analysis = PathAnalysis(None, None)
        self.assertTrue(analysis.spec["link_component"] is None)
