from collections import defaultdict

from parameters.impedance_transformation import impedance_share, divided_classes
from parameters.assignment import assignment_classes


class ImpedanceTransformer:
    def __init__(self):
        self.iteration_counter = 0
        self.averaged_impedance = dict.fromkeys(
            ["aht", "pt", "iht"])
        for time_period in self.averaged_impedance:
            self.averaged_impedance[time_period] = dict.fromkeys(
                ["time", "cost", "dist"])
            for mtx_type in self.averaged_impedance[time_period]:
                self.averaged_impedance[time_period][mtx_type] = dict.fromkeys(
                    ["car_work", "car_leisure"])

    def average_car_impedance(self, impedance):
        """Perform averaging of car impedance matrices.
        Parameters
        ----------
        impedance: dict
            Time period (aht/pt/iht) : dict
                Type (time/cost/dist) : dict
                    Assignment class (car_work/transit/...) : numpy 2d matrix
        Return 
        ------
        dict
            Time period (aht/pt/iht) : dict
                Type (time/cost/dist) : dict
                    Assignment class (car_work/transit/...) : numpy 2d matrix
        """
        self.iteration_counter += 1
        n = self.iteration_counter
        for time_period in impedance:
            for mtx_type in impedance[time_period]:
                average_imp = self.averaged_impedance[time_period][mtx_type]
                for ass_class in average_imp:
                    imp = impedance[time_period][mtx_type][ass_class]
                    if n == 1:
                        average_imp[ass_class] = imp
                    else:
                        old_average = average_imp[ass_class]
                        # Method of successive averages
                        new_average = ((n-1)*old_average + imp) / n
                        average_imp[ass_class] = new_average
                        impedance[time_period][mtx_type][ass_class] = new_average
        return impedance

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
