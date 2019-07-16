import pandas
import numpy
import parameters

class ExternalModel:
    def __init__(self, base_demand, zone_data):
        self.base_demand = base_demand
        self.zone_numbers = zone_data.zone_numbers
        self.growth = zone_data.externalgrowth

    def calc_external(self, mode, internal_trips):
        """Calculate external traffic.

        Parameters
        ----------
        mode : str
            Travel mode (car/transit/truck/trailer_truck)
        internal_trips : numpy array
            Sums of all (intra-area) trips to and frome zones
        
        Return
        ------
        numpy 2-d matrix
            Matrix of whole day trips from external to internal zones
        """
        base_mtx = self.base_demand.get_external(mode)
        indices = numpy.append(self.zone_numbers, self.growth[mode].index)
        mtx = pandas.DataFrame(0, indices, self.growth[mode].index)
        internal_trips = pandas.Series(internal_trips, self.zone_numbers)
        municipalities = parameters.municipality
        # Base matrix is aggregated to municipality level
        for target, base_vector in base_mtx.iterrows():
            if target in municipalities:
                l = municipalities[target][0]
                u = municipalities[target][1]
                zone_trips = internal_trips.loc[l:u]
                zone_weights = zone_trips / zone_trips.sum()
                # Disaggregate base matrix to zone level and 
                # multiply by growth factors
                mtx.loc[l:u] = ( self.growth[mode].values
                            * zone_weights[:, numpy.newaxis]
                            * base_vector.values)
            else: # External-external trips
                mtx.loc[int(target)] = self.growth[mode] * base_vector.values
        return mtx.values.T