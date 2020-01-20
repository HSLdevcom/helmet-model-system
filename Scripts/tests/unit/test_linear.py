import numpy
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
        mtx = numpy.arange(24, dtype=numpy.float32)
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
        pur.bounds = slice(0, 4)
        pur.zone_numbers = (5, 6, 7, 2792)
        
        bounds = slice(0, zd.first_peripheral_zone)
        model = CarDensityModel(zd, bounds, parameters.car_density)
        prediction = model.predict()
        self._validate(prediction)
        
    
    def _validate(self, prediction):
        self.assertIs(type(prediction), numpy.ndarray)
        self.assertEquals(prediction.ndim, 2)
        self.assertEquals(prediction.shape[1], 4)
        self.assertNotEquals(prediction[0, 1], 0)
        assert numpy.isfinite(prediction).all()
