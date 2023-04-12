import unittest
import pandas
import os
import numpy

import utils.log as log
from datahandling.zonedata import ZoneData
from datahandling.matrixdata import MatrixData
import parameters.assignment as param


TEST_DATA_PATH = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), "..", "test_data")
INTERNAL_ZONES = [102, 103, 244, 1063, 1531, 2703, 2741, 6272, 6291, 19071]
EXTERNAL_ZONES = [31102, 31500]
ZONE_INDEXES = numpy.array(INTERNAL_ZONES + EXTERNAL_ZONES)

# Integration tests for validating that we can read the matrices from OMX
#  and CSV files correctly. Assumes that the matrix is fixed and the
# values don't change throughout the project.

class Config():
    log_format = None
    log_level = "DEBUG"
    scenario_name = "TEST"
    results_path = os.path.join(TEST_DATA_PATH, "Results")

class MatrixDataTest(unittest.TestCase):
    
    def test_constructor(self):
        log.initialize(Config())
        m = MatrixData(
            os.path.join(TEST_DATA_PATH, "Base_input_data", "base_matrices"))
        # Verify that the base folder exists
        self.assertTrue(os.path.isdir(m.path))

    def test_matrix_operations(self):
        log.initialize(Config())
        m = MatrixData(
            os.path.join(TEST_DATA_PATH, "Base_input_data", "base_matrices"))
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

    def _get_freight_data_2016(self):
        zdata = ZoneData(
            os.path.join(TEST_DATA_PATH, "Base_input_data", "2018_zonedata"),
            ZONE_INDEXES)
        df = zdata.get_freight_data()
        self.assertIsNotNone(df)
        return df

    def test_csv_file_read(self):
        zdata2016 = ZoneData(
            os.path.join(TEST_DATA_PATH, "Base_input_data", "2018_zonedata"),
            ZONE_INDEXES)
        self.assertIsNotNone(zdata2016["population"])
        self.assertIsNotNone(zdata2016["workplaces"])

        zdata2030 = ZoneData(
            os.path.join(TEST_DATA_PATH, "Scenario_input_data", "2030_test"),
            ZONE_INDEXES)
        self.assertIsNotNone(zdata2030["population"])
        self.assertIsNotNone(zdata2030["workplaces"])

        self.assertEquals(
            len(zdata2016["population"]), len(zdata2030["population"]))
        self.assertEquals(
            len(zdata2016["workplaces"]), len(zdata2030["workplaces"]))
        # Assert that data content is a bit different so we know we're
        # not reading the same file all over again
        self.assertFalse(
            zdata2016["population"].equals(zdata2030["population"]))
        self.assertFalse(
            zdata2016["workplaces"].equals(zdata2030["workplaces"]))

    def test_all_cols_have_values_2016(self):
        df = self._get_freight_data_2016()
        row = df.loc[244, :]  # Let's pick some row and validate it
        expected_row = pandas.Series(
            [1142, 229, 3.8014, 1.8091, 2.1984],
            index=["population", "workplaces", "shops", "logistics", "industry"],
            dtype=numpy.float32, name=244)
        pandas.testing.assert_series_equal(row, expected_row)

    def test_industry_series_and_indexes_2016(self):
        df = self._get_freight_data_2016()
        industry = df["industry"] # Let's pick a column and validate it
        expected_industry = pandas.Series(
            [3.3971, 579.7232, 2.1984, 467.7852, 29.4101, 2.1424, 7.392, 0, 0, 0],
            index=INTERNAL_ZONES, dtype=numpy.float32, name="industry")
        pandas.testing.assert_series_equal(industry, expected_industry)
