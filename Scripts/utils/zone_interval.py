import numpy
import pandas

import parameters.zone as param


class ZoneIntervals:
    """Get interval slices for given zone division type.

    Parameters
    ----------
    division_type : str
        Type of zone division (municipalities/areas)
    """

    def __init__(self, division_type):
        self._intervals = param.__dict__[division_type]
        if division_type == "areas":
            self.keys = param.area_aggregation
        else:
            self.keys = self._intervals.keys()

    def __getitem__(self, name):
        return slice(
            self._intervals[name][0],
            self._intervals[name][1])

    def __iter__(self):
        return self.keys.__iter__()

    def __contains__(self, item):
        return self._intervals.has_key(item)

    def averages(self, array, weights):
        """Get weighted area averages.

        Parameters
        ----------
        array : pandas.Series
            Array to average over areas
        weights : pandas.Series
            Array of weights

        Returns
        -------
        pandas.Series
            Aggregated array
        """
        aggregation = pandas.Series(index=self.keys)
        for area in self:
            i = self[area]
            w = weights.loc[i]
            if w.size == 0 or w.sum() == 0:
                aggregation[area] = 0
            else:
                aggregation[area] = numpy.average(array.loc[i], weights=w)
        return aggregation


def zone_interval(division_type, name):
    """Get interval for given zone division type.

    Parameters
    ----------
    division_type : str
        Type of zone division (municipalities/areas)
    name : str
        Name of the municipality or area

    Returns
    -------
    slice
        (first zone number, last zone number)
    """
    return slice(
        param.__dict__[division_type][name][0],
        param.__dict__[division_type][name][1])


class AreaAggregator(ZoneIntervals):
    def __init__(self):
        ZoneIntervals.__init__(self, "areas")
        self.borders = numpy.array([self._intervals[area][1] for area in self])

    def find_index(self, zone):
        # We could also have an area mapping dict
        return numpy.searchsorted(self.borders, zone)

    def find_area(self, zone):
        return self.keys[self.find_index(zone)]


class MatrixAggregator(AreaAggregator):
    def __init__(self):
        AreaAggregator.__init__(self)
        self.matrix = pandas.DataFrame(0, self.keys, self.keys)

    def add(self, orig, dest):
        """Add individual tour to aggregated matrix.

        Parameters
        ----------
        orig : int
            Tour origin zone number
        dest : int
            Tour destination zone number
        """
        self.matrix.iat[self.find_index(orig), self.find_index(dest)] += 1

    def aggregate(self, matrix):
        """Aggregate (tour demand) matrix to larger areas.

        Parameters
        ----------
        matrix : pandas.DataFrame
            Disaggregated matrix with zone indices and columns
        """
        tmp_mtx = pandas.DataFrame(0, self.keys, matrix.columns)
        for area in self:
            tmp_mtx.loc[area] = matrix.loc[self[area]].sum(0).values
        for area in self:
            self.matrix.loc[:, area] = tmp_mtx.loc[:, self[area]].sum(1).values


class ArrayAggregator(AreaAggregator):
    def __init__(self):
        AreaAggregator.__init__(self)
        self.array = pandas.Series(0, self.keys)

    def add(self, zone):
        """Add individual tour to aggregated array.

        Parameters
        ----------
        zone : int
            Zone number
        """
        self.array.iat[self.find_index(zone)] += 1

    def aggregate(self, array):
        """Aggregate (tour demand) array to larger areas.

        Parameters
        ----------
        array : pandas.Series
            Disaggregated array with zone indices
        """
        for area in self:
            self.array.loc[area] = array.loc[self[area]].sum()
