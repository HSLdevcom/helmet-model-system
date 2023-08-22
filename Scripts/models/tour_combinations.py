import numpy # type: ignore

import parameters.tour_generation as param


class TourCombinationModel:
    """Nested logit model for tour combination choice.

    Number of tours per day is the upper level of the model and each
    number-of-tour nest can have different combinations of tours
    (e.g., a two-tour combination can be hw-ho, hw-hs or ho-ho, etc.).
    Base for tour generation.

    Parameters
    ----------
    zone_data : ZoneData
        Data used for all demand calculations
    """

    def __init__(self, zone_data):
        self.zone_data = zone_data
        self.param = param.tour_combinations
        self.conditions = param.tour_conditions
        self.increases = param.tour_number_increase
        self.tour_combinations = [combination for nr_tours in self.param
            for combination in self.param[nr_tours]]

    def calc_prob(self, age_group, is_car_user, zones):
        """Calculate choice probabilities for each tour combination.

        Calculation is done for one specific population group
        (age + is car user or not) and probabilities are returned for every
        possible tour combination.

        Parameters
        ----------
        age_group : str
            Age group (age_7-17/age_18-29/...)
        is_car_user : bool
            True if is car user
        zones : int or slice
            Zone number (for agent model) or zone data slice

        Returns
        -------
        dict
            key : tuple of str
                Tour combination (-/hw/hw-ho/...)
            value : pandas.Series
                Choice probabilities per zone
        """
        prob = {}
        nr_tours_exps = {}
        nr_tours_expsum = 0
        for nr_tours in self.param:
            # Upper level of nested logit model
            combination_exps = {}
            combination_expsum = 0
            for tour_combination in self.param[nr_tours]:
                # Lower level of nested logit model
                try:
                    cond = self.conditions[tour_combination]
                except KeyError:
                    is_allowed = True
                else:
                    # If this tour pattern is exclusively for this age group
                    # or if this age group is excluded from this tour pattern
                    is_allowed = (age_group == cond[1] if cond[0]
                        else age_group != cond[1])
                if is_allowed:
                    b = self.param[nr_tours][tour_combination]
                    util = b["constant"]
                    for i in b["zone"]:
                        util += b["zone"][i] * self.zone_data[i][zones]
                    dummies = b["individual_dummy"]
                    if age_group in dummies:
                        util += dummies[age_group]
                    if is_car_user and "car_users" in dummies:
                        util += dummies["car_users"]
                    combination_exps[tour_combination] = numpy.exp(util)
                else:
                    combination_exps[tour_combination] = 0
                combination_expsum += combination_exps[tour_combination]
            for tour_combination in self.param[nr_tours]:
                try:
                    prob[tour_combination] = ( combination_exps[tour_combination]
                                             / combination_expsum)
                except ZeroDivisionError:
                    # Specifically, no 4-tour patterns are allowed for
                    # 7-17-year-olds, so sum will be zero in this case
                    prob[tour_combination] = 0
            util = 0
            nr_tours_exps[nr_tours] = numpy.exp(util)
            scale_param = param.tour_number_scale
            nr_tours_exps[nr_tours] *= numpy.power(combination_expsum, scale_param)
            nr_tours_expsum += nr_tours_exps[nr_tours]
        # Probability of no tours at all (empty tuple) is deduced from
        # other combinations (after calibration)
        prob[()] = 1
        for nr_tours in self.param:
            if nr_tours != 0:
                nr_tours_prob = nr_tours_exps[nr_tours] / nr_tours_expsum
                # Tour number probability is calibrated
                nr_tours_prob *= self.increases[nr_tours]
                prob[()] -= nr_tours_prob
                for tour_combination in self.param[nr_tours]:
                    # Upper and lower level probabilities are combined
                    prob[tour_combination] *= nr_tours_prob
        return prob
