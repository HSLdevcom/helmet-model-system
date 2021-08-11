from collections import defaultdict
import numpy

from parameters.impedance_transformation import impedance_share, divided_classes, trips_month
from parameters.assignment import assignment_classes


class ImpedanceTransformer:
    def __init__(self):
        pass

    def transform(self, purpose, impedance):
        """Perform transformation from time period dependent matrices 
        to aggregate impedance matrices for specific travel purpose.

        Transform transit costs from (eur/month) to (eur/day).

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
        # transit cost to eur per day
        transit_class = "{}_{}".format("transit", assignment_classes[purpose.name])
        trips_per_month = numpy.full_like(
            day_imp["transit"]["cost"], trips_month[transit_class][0])
        trips_per_month[purpose.ubounds, :] = trips_month[transit_class][1]
        day_imp["transit"]["cost"] /= trips_per_month
        return day_imp
