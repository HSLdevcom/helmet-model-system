#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import numpy
import pandas
import unittest
from datatypes.person import Person


class PersonTest(unittest.TestCase):
    def test_add_tours(self):
        class ZoneData:
                def zone_index(self, zonenumber):
                    try:
                        return zonenumber - 100
                    except TypeError:
                        raise KeyError()
        class GenMod:
            zone_data = ZoneData()
            tour_combinations = [("hw",), ("hw", "ho"), ("hw", "hw")]
            param = {
                "hw": 0.3,
                "ho": 0.7,
            }
        class Purpose:
            zone_data = ZoneData()
            gen_model = GenMod()
            def __init__(self, name):
                self.name = name
        class Zone:
            number = 101
            index = 0
        p = Person(Zone(), (18, 29), GenMod(), None, ZoneData())
        p.is_car_user = True
        purposes = {
            "hw": Purpose("hw"),
            "ho": Purpose("ho"),
            "wo": Purpose("wo"),
            "oo": Purpose("oo"),
        }
        data = numpy.array([
            [0.3, 0.6, 1.0],
            [0.3, 0.6, 1.0],
            [0.3, 0.6, 1.0],
            [0.3, 0.6, 1.0],
        ])
        probs = {"age_18-29": {True: data}}
        p.add_tours(purposes, probs)
        p.add_tours(purposes, probs)
