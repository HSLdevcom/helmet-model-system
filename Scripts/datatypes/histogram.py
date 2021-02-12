import pandas
import numpy

from parameters.zone import tour_length_intervals as intervals


class TourLengthHistogram:
    _u = numpy.array(intervals[1:])

    def __init__(self):
        index = ["{}-{}".format(intervals[i], intervals[i + 1])
            for i in xrange(len(intervals) - 1)]
        self.histogram = pandas.Series(0, index)

    def add(self, dist):
        self.histogram.iloc[numpy.searchsorted(self._u, dist, "right")] += 1

    def count_tour_dists(self, tours, dists):
        self.histogram[:], _ = numpy.histogram(dists, intervals, weights=tours)
