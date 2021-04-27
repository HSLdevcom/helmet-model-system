import unittest
import pandas
import os
import numpy

import utils.log as log
from datahandling.zonedata import ZoneData
from datahandling.matrixdata import MatrixData
import parameters.assignment as param


TEST_DATA_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "test_data")
ZONE_INDEXES = numpy.array([5, 6, 7, 2792, 16001, 17000, 31001, 31501])

# Integration tests for validating that we can read the matrices from OMX and CSV files correctly.
# Assumes that the matrix is fixed and the values don't change throughout the project.

class Config():
    LOG_FORMAT = None
    LOG_LEVEL = "DEBUG"
    SCENARIO_NAME = "TEST"

class MatrixDataTest(unittest.TestCase):
    
    def test_constructor(self):
        log.initialize(Config())
        m = MatrixData(os.path.join(TEST_DATA_PATH, "Base_input_data", "base_matrices"))
        # Verify that the base folder exists
        self.assertTrue(os.path.isdir(m.path))

    def test_matrix_operations(self):
        log.initialize(Config())
        m = MatrixData(os.path.join(TEST_DATA_PATH, "Base_input_data", "base_matrices"))
        # TODO now MockAssignmentModel writes the demand-matrices in it's tests, think about this.. 
        MATRIX_TYPES = ["demand"]
        for matrix_type in MATRIX_TYPES:
            print("validating matrix type", matrix_type)
            self._validate_matrix_operations(m, matrix_type)

    def _validate_matrix_operations(self, matrix_data, matrix_type):
        emme_scenarios = ["aht", "pt", "iht"]
        expanded_zones = numpy.insert(ZONE_INDEXES, 3, 8)
        for key in emme_scenarios:
            print("Opening matrix for time period", key)
            with matrix_data.open(matrix_type, key, expanded_zones) as mtx:
                for ass_class in param.transport_classes:
                    a = mtx[ass_class]


class ZoneDataTest(unittest.TestCase):
    FREIGHT_DATA_INDEXES = [5, 6, 7, 2792, 16001, 17000]

    def _get_freight_data_2016(self):
        zdata = ZoneData(os.path.join(TEST_DATA_PATH, "Base_input_data", "2016_zonedata"), ZONE_INDEXES)
        df = zdata.get_freight_data()
        self.assertIsNotNone(df)
        return df

    def test_csv_file_read(self):
        zdata2016 = ZoneData(os.path.join(TEST_DATA_PATH, "Base_input_data", "2016_zonedata"), ZONE_INDEXES)
        self.assertIsNotNone(zdata2016["population"])
        self.assertIsNotNone(zdata2016["workplaces"])

        zdata2030 = ZoneData(os.path.join(TEST_DATA_PATH, "Scenario_input_data", "2030_test"), ZONE_INDEXES)
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
        pandas.testing.assert_series_equal(industry, expected_industry)
