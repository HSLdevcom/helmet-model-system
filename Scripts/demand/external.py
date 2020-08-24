import pandas
import numpy
import parameters
from datatypes.demand import Demand
from datatypes.purpose import Purpose


class ExternalModel:
    """External traffic model.

    Parameters
    ----------
    base_demand : datahandling.matrixdata.MatrixData
        Base demand matrices
    zone_data : datahandling.zonedata.ZoneData
        Zone data for forecast year
    zone_numbers : numpy.ndarray
        Zone numbers from assignment model
    """

    def __init__(self, base_demand, zone_data, zone_numbers):
        self.base_demand = base_demand
        self.internal_zones = zone_data.zone_numbers
        self.all_zone_numbers = zone_numbers
        self.growth = zone_data.externalgrowth
        spec = {
            "name": "external",
            "orig": None,
            "dest": None,
            "area": "external",
        }
        self.purpose = Purpose(spec, zone_data)

    def calc_external(self, mode, internal_trips):
        """Calculate external traffic.

        Parameters
        ----------
        mode : str
            Travel mode (car/transit/truck/trailer_truck)
        internal_trips : numpy.ndarray
            Sums of all (intra-area) trips to and frome zones
        
        Return
        ------
        Demand
            Matrix of whole day trips from external to internal zones
        """
        base_mtx = self.base_demand.get_external(mode)
        mtx = pandas.DataFrame(0, self.all_zone_numbers, self.growth.index)
        internal_trips = pandas.Series(internal_trips, self.internal_zones)
        municipalities = parameters.municipality
        # Base matrix is aggregated to municipality level,
        # so we need to disaggregate it
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
            else:  # External-external trips
                mtx.loc[int(target)] = self.growth[mode] * base_vector.values
        return Demand(self.purpose, mode, mtx.values.T)
