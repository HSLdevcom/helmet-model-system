import numpy
import pandas
import unittest
import parameters
from datahandling.zonedata import BaseZoneData
from models.linear import CarDensityModel
from datahandling.resultdata import ResultsData
import os

TEST_DATA_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "test_data")


class LinearModelTest(unittest.TestCase):
    def test_linear_calc(self):
        resultdata = ResultsData(os.path.join(TEST_DATA_PATH, "Results", "test"))
        class Purpose:
            pass
        pur = Purpose()
        zi = numpy.array([5, 6, 7, 2792, 16001, 17000, 31000, 31501])
        zd = BaseZoneData(os.path.join(TEST_DATA_PATH, "Base_input_data", "2016_zonedata_test"), zi)
        zd["time_ratio"] = pandas.Series([0.9, 1.5, 1.3, 1.9, 2.0, 3.1, 0.0, 0.0],
            zi)
        zd["cost_ratio"] = pandas.Series([1.1, 0.9, 0.8, 1.2, 0.5, 0.4, 0.0, 0.0],
            zi)
        mtx = numpy.arange(24, dtype=numpy.float32)
        mtx.shape = (4, 6)
        mtx[numpy.diag_indices(4)] = 0
        pur.bounds = slice(0, 4)
        pur.zone_numbers = (5, 6, 7, 2792)
        bounds = slice(0, zd.nr_zones)
        model = CarDensityModel(zd, zd, bounds, resultdata)
        prediction = model.predict()
        zd["car_density"] = prediction
        self._validate(prediction)
        
    
    def _validate(self, prediction):
        self.assertIs(type(prediction), pandas.core.series.Series)
        self.assertEquals(prediction.ndim, 1)
        self.assertEquals(prediction.shape[0], 6)
        self.assertEquals(prediction.size, 6)
        self.assertNotEquals(prediction.iloc[0], 0)
        assert numpy.isfinite(prediction).all()
