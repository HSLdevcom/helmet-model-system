#!/usr/bin/env python2
# -*- coding: utf-8 -*-


import unittest
import numpy
import pandas
import openmatrix as omx


class ImportTest(unittest.TestCase):
    def test_imports(self):
        self.assertIsNotNone(numpy.__version__)
        self.assertIsNotNone(pandas.__version__)
        self.assertIsNotNone(omx.__version__)