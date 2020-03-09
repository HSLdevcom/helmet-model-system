import unittest
from datahandling.zonedata import ZoneData
from datahandling.matrixdata import MatrixData
import pandas
import os
import parameters as params
import numpy

TEST_DATA_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "test_data")

# Integration tests for validating that we can read the matrices from OMX and CSV files correctly.
# Assumes that the matrix is fixed and the values don't change throughout the project.


class MatrixDataTest(unittest.TestCase):
    
    def test_constructor(self):
        m = MatrixData(os.path.join(TEST_DATA_PATH, "Results", "test", "Matrices"))
        # Verify that the base folder exists
        self.assertTrue(os.path.isdir(m.path))
        self.assertTrue(m.path.endswith("Matrices"))

    def test_matrix_operations(self):
        m = MatrixData(os.path.join(TEST_DATA_PATH, "Results", "test", "Matrices"))
        # TODO add matrices for gen_cost, transit, bike? 
        # TODO now MockAssignmentModel writes the demand-matrices in it's tests, think about this.. 
        MATRIX_TYPES = ["time", "dist", "cost"]
        for matrix_type in MATRIX_TYPES:
            print("validating matrix type", matrix_type)
            self._validate_matrix_operations(m, matrix_type)

    def _validate_matrix_operations(self, matrix_data, matrix_type):
        for key in params.emme_scenario.keys():
            print("Opening matrix for time period", key)
            with matrix_data.open(matrix_type, time_period=key) as mtx:
                self.assertIsNotNone(mtx._file)
                # Validate that has some zone numbers and mapping
                self.assertTrue(len(mtx.zone_numbers) > 0)
                self.assertEquals(len(mtx.zone_numbers), len(mtx.mapping))
                modes_for_this_type = params.emme_mtx[matrix_type].keys()
                for mode in modes_for_this_type:
                    # Validata that there is some data for each mode
                    print("validating data for matrix mode", mode)
                    data = mtx[mode]
                    assert type(data) is numpy.ndarray
                    self.assertTrue(len(data) > 0)
                    assert (data >= 0).all()


class ZoneDataTest(unittest.TestCase):
    FREIGHT_DATA_INDEXES = [5, 6, 7, 2792, 16001, 17000]
    ZONE_INDEXES = numpy.array([5, 6, 7, 2792, 16001, 17000, 31000, 31501])

    def _get_freight_data_2016(self):
        zdata = ZoneData(os.path.join(TEST_DATA_PATH, "Base_input_data", "2016_zonedata_test"), self.ZONE_INDEXES)
        df = zdata.get_freight_data()
        self.assertIsNotNone(df)
        return df

    def test_csv_file_read(self):
        zdata2016 = ZoneData(os.path.join(TEST_DATA_PATH, "Base_input_data", "2016_zonedata_test"), self.ZONE_INDEXES)
        self.assertIsNotNone(zdata2016["population"])
        self.assertIsNotNone(zdata2016["workplaces"])

        zdata2030 = ZoneData(os.path.join(TEST_DATA_PATH, "Scenario_input_data", "2030_test"), self.ZONE_INDEXES)
        self.assertIsNotNone(zdata2030["population"])
        self.assertIsNotNone(zdata2030["workplaces"])

        self.assertEquals(len(zdata2016["population"]), len(zdata2030["population"]))
        self.assertEquals(len(zdata2016["workplaces"]), len(zdata2030["workplaces"]))
        # Assert that data content is a bit different so we know we're not reading the same file all over again
        self.assertFalse(zdata2016["population"].equals(zdata2030["population"]))
        self.assertFalse(zdata2016["workplaces"].equals(zdata2030["workplaces"]))

    def test_all_cols_have_values_2016(self):
        df = self._get_freight_data_2016()
        row = df.loc[7, :]  # Let's pick some row and validate it
        self.assertAlmostEquals(row['industry'], 0.0)
        self.assertAlmostEquals(row['logistics'], 0.4)
        self.assertEquals(row['population'], 10)
        self.assertAlmostEquals(row['shops'], 0.8)
        self.assertEquals(row['workplaces'], 4)

    def test_industry_series_and_indexes_2016(self):
        df = self._get_freight_data_2016()
        industry = df["industry"] # Let's pick a column and validate it
        expected_industry = pandas.Series([0.7, 0.0, 0.0, 0.9, 0.0, 0.0], index=self.FREIGHT_DATA_INDEXES, name="industry")
        pandas.util.testing.assert_series_equal(industry, expected_industry)
