import numpy # type: ignore
import pandas
from shapely.geometry import Point, Polygon # type: ignore

import parameters.zone as param
import utils.log as log


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
    return slice(*param.__dict__[division_type][name])


def is_in(interval, zone_number):
    """Decide whether zone number is in zone number interval.

    If interval consists of several sub-intervals, we check recursively
    whether zone number is in any of these sub-intervals.

    Parameters
    ----------
    interval : tuple
        Either (start, end) tuple or tuple of (start, end) tuples
    zone_number : int
        Zone number

    Returns
    -------
    bool
        True if zone number is in interval
    """
    try:
        return interval[0] <= zone_number <= interval[1]
    except (TypeError, ValueError):
        for sub_interval in interval:
            if is_in(sub_interval, zone_number):
                return True
    return False

faulty_kela_code_nodes = set()

cbd = Polygon(param.helsinki_cbd)


def belongs_to_area(node):
    """Get name of area to which node belongs to.

    Parameters
    ----------
    node : inro.emme.network.node.Node
        Node in Emme network with municipality KELA code in `ui3`

    Returns
    -------
    str
        Name of area (helsinki_cbd/helsinki_other/espoo_vant_kau/...)
    """
    try:
        municipality = param.kela_codes[int(node.data3)]
    except KeyError:
        faulty_kela_code_nodes.add(node.id)
        first_zone_id = -1
    else:
        if municipality == "Helsinki" and not Point(node.x, node.y).within(cbd):
            first_zone_id = 1000
        else:
            try:
                first_zone_id = param.municipalities[municipality][0]
            except KeyError:
                first_zone_id = -1
    for area in param.area_aggregation:
        if is_in(param.areas[area], first_zone_id):
            return area


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
        try:
            # If zone grouping consists of several intervals
            return [slice(*i) for i in self._intervals[name]]
        except TypeError:
            # If zone grouping is one interval
            return slice(*self._intervals[name])

    def __iter__(self):
        return self.keys.__iter__()

    def __contains__(self, item):
        return item in self._intervals

    def _get_slice(self, name, index):
        try:
            # If zone grouping consists of several intervals
            bool_array = pandas.Series(False, index)
            for j in self[name]:
                bool_array.loc[j] = True
            return bool_array
        except TypeError:
            # If zone grouping is one interval
            return self[name]

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
        aggregation["all"] = numpy.average(array, weights=weights)
        for area in self:
            i = self._get_slice(area, array.index)
            w = weights.loc[i]
            if w.size == 0 or w.sum() == 0:
                aggregation[area] = 0
            else:
                aggregation[area] = numpy.average(array.loc[i], weights=w)
        return aggregation


class AreaAggregator(ZoneIntervals):
    def __init__(self, zone_numbers):
        ZoneIntervals.__init__(self, "areas")
        self.mapping = {}
        for zone_number in zone_numbers:
            for area in self:
                if is_in(self._intervals[area], zone_number):
                    self.mapping[zone_number] = area
                    break


class MatrixAggregator(AreaAggregator):
    def __init__(self, zone_numbers):
        AreaAggregator.__init__(self, zone_numbers)
        self.init_matrix()

    def init_matrix(self):
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
        self.matrix.at[self.mapping[orig], self.mapping[dest]] += 1

    def aggregate(self, matrix):
        """Aggregate (tour demand) matrix to larger areas.

        Parameters
        ----------
        matrix : pandas.DataFrame
            Disaggregated matrix with zone indices and columns
        """
        self.init_matrix()
        tmp_mtx = pandas.DataFrame(0, self.keys, matrix.columns)
        for area in self:
            i = self._get_slice(area, matrix.index)
            tmp_mtx.loc[area] = matrix.loc[i].sum(0).values
        for area in self:
            i = self._get_slice(area, matrix.columns)
            self.matrix.loc[:, area] = tmp_mtx.loc[:, i].sum(1).values
        return self.matrix


class ArrayAggregator(AreaAggregator):
    def __init__(self, zone_numbers):
        AreaAggregator.__init__(self, zone_numbers)
        self.init_array()

    def init_array(self):
        self.array = pandas.Series(0, self.keys)

    def add(self, zone):
        """Add individual tour to aggregated array.

        Parameters
        ----------
        zone : int
            Zone number
        """
        self.array.at[self.mapping[zone]] += 1

    def aggregate(self, array):
        """Aggregate (tour demand) array to larger areas.

        Parameters
        ----------
        array : pandas.Series
            Disaggregated array with zone indices
        """
        self.init_array()
        for area in self:
            i = self._get_slice(area, array.index)
            self.array.loc[area] = array.loc[i].sum()
        return self.array
