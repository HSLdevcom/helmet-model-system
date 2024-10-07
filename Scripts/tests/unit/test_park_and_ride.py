#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy
import unittest
from assignment.departure_time import DepartureTimeModel
from datahandling.zonedata import ZoneData
from datatypes.purpose import Purpose
from transform.park_and_ride_transformer import ParkAndRideTransformer
import os

TEST_DATA_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "test_data")
METROPOLITAN_ZONES = [102, 103, 244, 1063, 1531, 2703, 2741, 6272, 6291]
PERIPHERAL_ZONES = [19071]
EXTERNAL_ZONES = [34102, 34500]
PR_ZONES = [35039]

class ParkAndRideTest(unittest.TestCase):
    def test_park_and_ride_demand(self):
        zi = numpy.array(METROPOLITAN_ZONES + PERIPHERAL_ZONES + EXTERNAL_ZONES)
        zi_w_liipy = numpy.array(METROPOLITAN_ZONES + PERIPHERAL_ZONES + EXTERNAL_ZONES + PR_ZONES) #zone indices with park and ride facilities
        
        zone_data = ZoneData(
            os.path.join(TEST_DATA_PATH, "Base_input_data", "2018_zonedata"), zi_w_liipy)
    
        dtm = DepartureTimeModel(len(zi_w_liipy)) #TODO: This will cause problems, make sure the zones include external and pnr zones
        mtx = numpy.arange(len(zi)*len(zi))
        mtx.shape = (len(zi), len(zi))
        class Demand:
            pass
        
        spec = {
        "name": "hw",
        "orig": "home",
        "dest": "work",
        "area": "metropolitan",
        }
        pur = Purpose(spec, zone_data)  

        demc = Demand()      
        demc.purpose = pur
        demc.is_car_passenger = False
    
        demc.purpose.name = "hw"
        demc.mode = "car"
        demc.dest = None
        demc.matrix = numpy.array([[0 for _ in range(len(zi_w_liipy))] for _ in range(len(zi_w_liipy))])
        demc.position = (0,0)
        dtm.add_demand(demc)

        demt = Demand()      
        demt.purpose = pur
        demt.is_car_passenger = False
        demt.purpose.name = "hw"
        demt.mode = "transit"
        demt.dest = None
        demt.matrix = numpy.array([[0 for _ in range(len(zi_w_liipy))] for _ in range(len(zi_w_liipy))])
        demt.position = (0,0)
        dtm.add_demand(demt)

        dem = Demand()      
        dem.purpose = pur
        dem.is_car_passenger = False
        dem.purpose.name = "hw"
        dem.mode = "park_and_ride"
        dem.dest = None
        dem.matrix = numpy.array([[1 for _ in range(len(zi_w_liipy))] for _ in range(len(zi_w_liipy))])
        dem.position = (0,0)

        impedance = {period: {impedance: {imp_type: numpy.array([[1 for _ in range(len(zi_w_liipy))] for _ in range(len(zi_w_liipy))]) for imp_type in ["car_work","transit_work"]} for impedance in ["cost","dist","time"]} for period in ["aht","pt","iht"]}
        park_and_ride_transformer = ParkAndRideTransformer(zone_data)
        park_and_ride_facility_map = park_and_ride_transformer.get_pnr_map()
        
        park_and_ride_impedance = park_and_ride_transformer.transform(dem.purpose,impedance)
        
        dtm.split_park_and_ride(dem, park_and_ride_impedance["park_and_ride"], park_and_ride_facility_map, zone_data)
        print(dtm.demand["pt"]["car_work"])
        self.assertIsNotNone(dtm.demand)
        #park and ride should be distributed to car and transit matrices
        self.assertIs(type(dtm.demand["iht"]["car_work"]), numpy.ndarray)
        self.assertEquals(dtm.demand["pt"]["car_work"].ndim, 2)
        self.assertGreater(numpy.sum(dtm.demand["pt"]["car_work"]), 0)
        self.assertEquals(dtm.demand["aht"]["transit_work"].shape[1], 13)
        #self.assertNotEquals(dtm.demand["iht"]["car"][12, 1], 12)
