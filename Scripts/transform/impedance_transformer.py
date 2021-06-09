from collections import defaultdict
import numpy

from parameters.impedance_transformation import impedance_share, divided_classes
from parameters.assignment import assignment_classes


class ImpedanceTransformer:
    def __init__(self):
        pass

    def transform(self, purpose, impedance):
        """Perform transformation from time period dependent matrices 
        to aggregate impedance matrices for specific travel purpose.

        Parameters
        ----------
        purpose : TourPurpose
        impedance: dict
            Time period (aht/pt/iht) : dict
                Type (time/cost/dist) : dict
                    Assignment class (car_work/transit/...) : numpy 2d matrix
        Return 
        ------
        dict 
            Mode (car/transit/bike/walk) : dict
                Type (time/cost/dist) : numpy 2-d matrix
        """
        rows = purpose.bounds
        cols = (purpose.bounds if purpose.name == "hoo"
            else slice(0, purpose.zone_data.nr_zones))
        day_imp = {}
        for mode in impedance_share[purpose.name]:
            day_imp[mode] = defaultdict(float)
            if mode in divided_classes:
                ass_class = "{}_{}".format(
                    mode, assignment_classes[purpose.name])
            else:
                ass_class = mode
            for time_period in impedance:
                for mtx_type in impedance[time_period]:
                    if ass_class in impedance[time_period][mtx_type]:
                        share = impedance_share[purpose.name][mode][time_period]
                        imp = impedance[time_period][mtx_type][ass_class]
                        day_imp[mode][mtx_type] += share[0] * imp[rows, cols]
                        day_imp[mode][mtx_type] += share[1] * imp[cols, rows].T
        return day_imp

    def transform_transit_cost(self, zone_data, impedance):
        """Convert transit costs.

        From [eur/month] to [eur/day].
        """
        for time_period in impedance:
            imp = impedance[time_period]
            trips_per_month = numpy.full_like(imp["cost"]["transit_work"], 60.0)
            trips_per_month[zone_data.first_surrounding_zone:, :] = 44.0
            trips_per_month = 0.5 * (trips_per_month+trips_per_month.T)
            imp["cost"]["transit_work"] /= trips_per_month
            trips_per_month = numpy.full_like(imp["cost"]["transit_leisure"], 30.0)
            imp["cost"]["transit_leisure"] /= trips_per_month
        return(impedance)
