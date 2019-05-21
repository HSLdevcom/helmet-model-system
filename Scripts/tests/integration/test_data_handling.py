import unittest

from data_handling import ZoneData
import pandas

# Integration test for validating that we can read the matrices from OMX and CSV files correctly.
# Assumes that the matrix is fixed and the values don't change throughout the project.
class ZoneDataTest(unittest.TestCase):
    FREIGHT_DATA_INDEXES = [5, 6, 7, 2792, 16001]

    def _get_freight_data_2016(self):
        zdata = ZoneData("2016")
        df = zdata.get_freight_data()
        self.assertIsNotNone(df)
        #print(df)
        return df

    def test_csv_file_read(self):
        zdata2016 = ZoneData("2016")
        self.assertIsNotNone(zdata2016.population)
        self.assertIsNotNone(zdata2016.workplaces)

        zdata2030 = ZoneData("2030")
        self.assertIsNotNone(zdata2030.population)
        self.assertIsNotNone(zdata2030.workplaces)

        self.assertEquals(len(zdata2016.population), len(zdata2030.population))
        self.assertEquals(len(zdata2016.workplaces), len(zdata2030.workplaces))
        #Assert that data content is a bit different so we know we're not reading the same file all over again
        self.assertFalse(zdata2016.population.equals(zdata2030.population))
        self.assertFalse(zdata2016.workplaces.equals(zdata2030.workplaces))


    def test_all_cols_have_values_2016(self):
        df = self._get_freight_data_2016()
        row = df.loc[7, :] # Let's pick some row and validate it
        self.assertAlmostEquals(row['industry'], 0.0)
        self.assertAlmostEquals(row['logistics'], 0.4)
        self.assertEquals(row['population'], 10)
        self.assertAlmostEquals(row['shops'], 0.8)
        self.assertEquals(row['workplaces'], 4)

    def test_industry_series_and_indexes_2016(self):
        df = self._get_freight_data_2016()
        industry = df["industry"] # Let's pick a column and validate it
        expected_industry = pandas.Series([0.7, 0.0, 0.0, 0.9, 0.0], index = self.FREIGHT_DATA_INDEXES)
        pandas.util.testing.assert_series_equal(industry, expected_industry)
        
