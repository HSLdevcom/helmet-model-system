import pandas
import numpy
import parameters

class ExternalModel:
    def __init__(self, base_demand, zone_data):
        self.base_demand = base_demand
        self.zone_numbers = zone_data.zone_numbers
        self.growth = zone_data.externalgrowth

    def calc_external(self, mode, internal_trips):
        base_mtx = self.base_demand.get_external(mode)
        mtx = pandas.DataFrame(0, self.zone_numbers, self.growth[mode].index)
        internal_trips = pandas.Series(internal_trips, self.zone_numbers)
        municipalities = parameters.municipality
        for municipality, base_vector in base_mtx.iterrows():
            l = municipalities[municipality][0]
            u = municipalities[municipality][1]
            zone_weights = internal_trips.loc[l:u]
            zone_weights = zone_weights / zone_weights.sum()
            mtx.loc[l:u] = ( self.growth[mode].values
                           * zone_weights[:, numpy.newaxis]
                           * base_vector.values)
        return mtx.values.T