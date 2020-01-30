import numpy
import pandas
import unittest
import parameters
from datahandling.zonedata import ZoneData
from models.linear import CarDensityModel
import datahandling.resultdata as result


class LinearModelTest(unittest.TestCase):
    def test_linear_calc(self):
        result.set_path("test")
        class Purpose:
            pass
        pur = Purpose()
        zi = numpy.array([5, 6, 7, 2792, 16001, 17000, 31000, 31501])
        zd = ZoneData("2016_test", zi)
        zd["time_ratio"] = pandas.Series([0.9, 1.5, 1.3, 1.9, 2.0, 3.1, 0.0, 0.0],
            zi)
        zd["cost_ratio"] = pandas.Series([1.1, 0.9, 0.8, 1.2, 0.5, 0.4, 0.0, 0.0],
            zi)
        mtx = numpy.arange(24, dtype=numpy.float32)
        mtx.shape = (4, 6)
        mtx[numpy.diag_indices(4)] = 0
        pur.bounds = slice(0, 4)
        pur.zone_numbers = (5, 6, 7, 2792)
        bounds = slice(0, zd.first_peripheral_zone)
        model = CarDensityModel(zd, bounds, parameters.car_density)
        prediction = model.predict()
        zd["car_density"][:zd.first_peripheral_zone] = prediction
        self._validate(prediction)
        
    
    def _validate(self, prediction):
        self.assertIs(type(prediction), pandas.core.series.Series)
        self.assertEquals(prediction.ndim, 1)
        self.assertEquals(prediction.shape[0], 4)
        self.assertEquals(prediction.size, 4)
        self.assertNotEquals(prediction.iloc[0], 0)
        assert numpy.isfinite(prediction).all()
