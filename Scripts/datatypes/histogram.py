import pandas
import numpy


class TourLengthHistogram:
    def __init__(self):
        intervals = ("0-1", "1-3", "3-5", "5-10", "10-20", "20-30",
                     "30-40", "40-inf")
        self.histogram = pandas.Series(0, index=intervals)
        self._l = numpy.array([float(i.split("-")[0]) for i in intervals])
        self._u = numpy.array([float(i.split("-")[1]) for i in intervals])

    def add(self, dist):
        self.histogram.iloc[numpy.searchsorted(self._u, dist)] += 1

    def count_tour_dists(self, tours, dists):
        for i in xrange(self.histogram.size):
            interval = (dists>=self._l[i]) & (dists<self._u[i])
            self.histogram.iloc[i] = tours[interval].sum()
