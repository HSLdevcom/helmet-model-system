import numpy
import pandas
import math

from parameters.destination_choice import destination_choice, distance_boundary
from parameters.mode_choice import mode_choice
from parameters.car import car_usage
import parameters.tour_generation as generation_params
import parameters.zone as zone_params
from utils.zone_interval import ZoneIntervals


class LogitModel:
    """Generic logit model with mode/destination choice.

    Parameters
    ----------
    zone_data : ZoneData
        Data used for all demand calculations
    purpose : TourPurpose
        Tour purpose (type of tour)
    resultdata : ResultData
        Writer object to result directory
    is_agent_model : bool (optional)
        Whether the model is used for agent-based simulation
    """

    def __init__(self, zone_data, purpose, resultdata, is_agent_model):
        self.resultdata = resultdata
        self.purpose = purpose
        self.bounds = purpose.bounds
        self.sub_bounds = purpose.sub_bounds
        self.zone_data = zone_data
        self.dest_exps = {}
        self.mode_exps = {}
        self.dest_choice_param = destination_choice[purpose.name]
        self.mode_choice_param = mode_choice[purpose.name]
        if is_agent_model:
            self.dtype = float
        else:
            self.dtype = None

    def _calc_mode_util(self, impedance):
        expsum = numpy.zeros_like(
            next(iter(impedance["car"].values())), self.dtype)
        for mode in self.mode_choice_param:
            b = self.mode_choice_param[mode]
            utility = numpy.zeros_like(expsum)
            self._add_constant(utility, b["constant"])
            utility = self._add_zone_util(
                utility.T, b["generation"], generation=True).T
            self._add_zone_util(utility, b["attraction"])
            self._add_impedance(utility, impedance[mode], b["impedance"])
            exps = numpy.exp(utility)
            self._add_log_impedance(exps, impedance[mode], b["log"])
            self.mode_exps[mode] = exps
            expsum += exps
        return expsum
    
    def _calc_dest_util(self, mode, impedance):
        b = self.dest_choice_param[mode]
        utility = numpy.zeros_like(next(iter(impedance.values())), self.dtype)
        self._add_zone_util(utility, b["attraction"])
        self._add_impedance(utility, impedance, b["impedance"])
        self.dest_exps[mode] = numpy.exp(utility)
        size = numpy.zeros_like(utility)
        self._add_zone_util(size, b["size"])
        impedance["size"] = size
        if "transform" in b:
            b_transf = b["transform"]
            transimp = numpy.zeros_like(utility)
            self._add_zone_util(transimp, b_transf["attraction"])
            self._add_impedance(transimp, impedance, b_transf["impedance"])
            impedance["transform"] = transimp
        self._add_log_impedance(self.dest_exps[mode], impedance, b["log"])
        if mode != "logsum":
            threshold = distance_boundary[mode]
            self.dest_exps[mode][impedance["dist"] > threshold] = 0
        try:
            return self.dest_exps[mode].sum(1)
        except ValueError:
            return self.dest_exps[mode].sum()
    
    def _calc_sec_dest_util(self, mode, impedance, orig, dest):
        b = self.dest_choice_param[mode]
        utility = numpy.zeros_like(next(iter(impedance.values())), self.dtype)
        self._add_sec_zone_util(utility, b["attraction"], orig, dest)
        self._add_impedance(utility, impedance, b["impedance"])
        dest_exps = numpy.exp(utility)
        size = numpy.zeros_like(utility)
        self._add_sec_zone_util(size, b["size"])
        impedance["size"] = size
        self._add_log_impedance(dest_exps, impedance, b["log"])
        if mode != "logsum":
            threshold = distance_boundary[mode]
            dest_exps[impedance["dist"] > threshold] = 0
        return dest_exps

    def _add_constant(self, utility, b):
        """Add constant term to utility.

        If parameter b is a tuple of two terms, they will be added for
        capital region and surrounding region respectively.
        
        Parameters
        ----------
        utility : ndarray
            Numpy array to which the constant b will be added
        b : float or tuple
            The value of the constant
        """
        try: # If only one parameter
            utility += b
        except ValueError: # Separate sub-region parameters
            for i, bounds in enumerate(self.sub_bounds):
                if utility.ndim == 1: # 1-d array calculation
                    utility[bounds] += b[i]
                else: # 2-d matrix calculation
                    utility[bounds, :] += b[i]
    
    def _add_impedance(self, utility, impedance, b):
        """Adds simple linear impedances to utility.

        If parameter in b is tuple of two terms, they will be added for
        capital region and surrounding region respectively.
        
        Parameters
        ----------
        utility : ndarray
            Numpy array to which the impedances will be added
        impedance : dict
            A dictionary of time-averaged impedance matrices. Includes keys
            `time`, `cost`, and `dist` of which values are all ndarrays.
        b : dict
            The parameters for different impedance matrices.
        """
        for i in b:
            try: # If only one parameter
                utility += b[i] * impedance[i]
            except ValueError: # Separate sub-region parameters
                for j, bounds in enumerate(self.sub_bounds):
                    utility[bounds, :] += b[i][j] * impedance[i][bounds, :]
        return utility

    def _add_log_impedance(self, exps, impedance, b):
        """Adds log transformations of impedance to utility.
        
        This is an optimized way of calculating log terms. Calculates
        impedance1^b1 * ... * impedanceN^bN in the following equation:
        e^(linear_terms + b1*log(impedance1) + ... + bN*log(impedanceN))
        = e^(linear_terms) * impedance1^b1 * ... * impedanceN^bN

        If parameter in b is tuple of two terms, they will be multiplied for
        capital region and surrounding region respectively.

        Parameters
        ----------
        exps : ndarray
            Numpy array to which the impedances will be multiplied
        impedance : dict
            A dictionary of time-averaged impedance matrices. Includes keys
            `time`, `cost`, and `dist` of which values are all ndarrays.
        b : dict
            The parameters for different impedance matrices
        """
        for i in b:
            try: # If only one parameter
                exps *= numpy.power(impedance[i] + 1, b[i])
            except ValueError: # Separate sub-region parameters
                for j, bounds in enumerate(self.sub_bounds):
                    exps[bounds, :] *= numpy.power(
                        impedance[i][bounds, :] + 1, b[i][j])
        return exps
    
    def _add_zone_util(self, utility, b, generation=False):
        """Adds simple linear zone terms to utility.

        If parameter in b is tuple of two terms, they will be added for
        capital region and surrounding region respectively.
        
        Parameters
        ----------
        utility : ndarray
            Numpy array to which the impedances will be added
        b : dict
            The parameters for different zone data.
        generation : bool
            Whether the effect of the zone term is added only to the
            geographical area in which this model is used based on the
            `self.bounds` attribute of this class.
        """
        zdata = self.zone_data
        for i in b:
            try: # If only one parameter
                utility += b[i] * zdata.get_data(i, self.bounds, generation)
            except ValueError: # Separate sub-region parameters
                for j, bounds in enumerate(self.sub_bounds):
                    data = zdata.get_data(i, bounds, generation)
                    if utility.ndim == 1: # 1-d array calculation
                        utility[bounds] += b[i][j] * data
                    else: # 2-d matrix calculation
                        utility[bounds, :] += b[i][j] * data
        return utility
    
    def _add_sec_zone_util(self, utility, b, orig=None, dest=None):
        for i in b:
            data = self.zone_data.get_data(i, self.bounds, generation=True)
            try: # If only one parameter
                utility += b[i] * data
            except ValueError: # Separate params for orig and dest
                utility += b[i][0] * data[orig, self.bounds]
                utility += b[i][1] * data[dest, self.bounds]
        return utility

    def _add_log_zone_util(self, exps, b, generation=False):
        """Adds log transformations of zone data to utility.
        
        This is an optimized way of calculating log terms. Calculates
        zonedata1^b1 * ... * zonedataN^bN in the following equation:
        e^(linear_terms + b1*log(zonedata1) + ... + bN*log(zonedataN))
        = e^(linear_terms) * zonedata1^b1 * ... * zonedataN^bN

        If parameter in b is tuple of two terms, they will be multiplied for
        capital region and surrounding region respectively.

        Parameters
        ----------
        exps : ndarray
            Numpy array to which the impedances will be multiplied
        b : dict
            The parameters for different zone data.
        generation : bool
            Whether the effect of the zone term is added only to the
            geographical area in which this model is used based on the
            `self.bounds` attribute of this class.
        """
        zdata = self.zone_data
        for i in b:
            exps *= numpy.power(
                zdata.get_data(i, self.bounds, generation) + 1, b[i])
        return exps


class ModeDestModel(LogitModel):
    """Nested logit model with mode choice in upper level.

    Uses logsums from destination choice model as utility
    in mode choice model.

         choice
        /     \\
      m1        m2
     / \\      / \\
    d1   d2   d1   d2

    Parameters
    ----------
    zone_data : ZoneData
        Data used for all demand calculations
    purpose : TourPurpose
        Tour purpose (type of tour)
    resultdata : ResultData
        Writer object to result directory
    is_agent_model : bool (optional)
        Whether the model is used for agent-based simulation
    """

    def calc_prob(self, impedance):
        """Calculate matrix of choice probabilities.

        First calculates basic probabilities. Then inserts individual
        dummy variables by calling `calc_individual_prob()`.
        
        Parameters
        ----------
        impedance : dict
            Mode (car/transit/bike/walk) : dict
                Type (time/cost/dist) : numpy 2-d matrix
                    Impedances
        
        Returns
        -------
        dict
            Mode (car/transit/bike/walk) : numpy 2-d matrix
                Choice probabilities
        """
        prob = self.calc_basic_prob(impedance)
        for mod_mode in self.mode_choice_param:
            for i in self.mode_choice_param[mod_mode]["individual_dummy"]:
                dummy_share = self.zone_data.get_data(
                    i, self.bounds, generation=True)
                ind_prob = self.calc_individual_prob(mod_mode, i)
                for mode in prob:
                    no_dummy = (1 - dummy_share) * prob[mode]
                    dummy = dummy_share * ind_prob[mode]
                    prob[mode] = no_dummy + dummy
        return prob
    
    def calc_basic_prob(self, impedance):
        """Calculate matrix of mode and destination choice probabilities.

        Individual dummy variables are not included.
        
        Parameters
        ----------
        impedance : dict
            Mode (car/transit/bike/walk) : dict
                Type (time/cost/dist) : numpy 2-d matrix
                    Impedances
        
        Returns
        -------
        dict
            Mode (car/transit/bike/walk) : numpy 2-d matrix
                Choice probabilities
        """
        return self._calc_prob(self._calc_utils(impedance))
    
    def calc_individual_prob(self, mod_mode, dummy):
        """Calculate matrix of probabilities with individual dummies.
        
        Calculate matrix of mode and destination choice probabilities
        with individual dummy variable included.
        
        Parameters
        ----------
        mod_mode : str
            The mode for which the utility will be modified
        dummy : str
            The name of the individual dummy
        
        Returns
        -------
        dict
            Mode (car/transit/bike/walk) : numpy 2-d matrix
                Choice probabilities
        """
        b = self.mode_choice_param[mod_mode]["individual_dummy"][dummy]
        try:
            self.mode_exps[mod_mode] *= numpy.exp(b)
        except ValueError:
            for i, bounds in enumerate(self.sub_bounds):
                self.mode_exps[mod_mode][bounds] *= numpy.exp(b[i])
        mode_expsum = numpy.zeros_like(self.mode_exps[mod_mode])
        for mode in self.mode_choice_param:
            mode_expsum += self.mode_exps[mode]
        return self._calc_prob(mode_expsum)
    
    def calc_individual_mode_prob(self, is_car_user, zone):
        """Calculate individual choice probabilities with individual dummies.
        
        Calculate mode choice probabilities for individual
        agent with individual dummy variable "car_users" included.

        Additionally save and rescale logsum values for agent based accessibility 
        analysis.
        
        Parameters
        ----------
        is_car_user : bool
            Whether the agent is car user or not
        zone : int
            Index of zone where the agent lives
        
        Returns
        -------
        numpy.array
            Choice probabilities for purpose modes
        float
            Total accessibility for individual (eur)
        """
        mode_exps = {}
        mode_expsum = 0
        modes = self.purpose.modes
        for mode in modes:
            mode_exps[mode] = self.mode_exps[mode][zone]
            b = self.mode_choice_param[mode]["individual_dummy"]
            if is_car_user and "car_users" in b:
                try:
                    mode_exps[mode] *= math.exp(b["car_users"])
                except TypeError:
                    # Separate sub-region parameters
                    i = self.purpose.sub_intervals.searchsorted(
                        zone, side="right")
                    mode_exps[mode] *= math.exp(b["car_users"][i])
            mode_expsum += mode_exps[mode]
        probs = numpy.empty(len(modes))
        for i, mode in enumerate(modes):
            probs[i] = mode_exps[mode] / mode_expsum
        # utils to money
        logsum = numpy.log(mode_expsum)
        b = self._get_cost_util_coefficient()
        try:
            # Convert utility into euros
            money_utility = 1 / b
        except TypeError:
            # Separate sub-region parameters
            i = self.purpose.sub_intervals.searchsorted(zone, side="right")
            money_utility = 1 / b[i]
        money_utility /= self.mode_choice_param["car"]["log"]["logsum"]
        accessibility = -money_utility * logsum
        return probs, accessibility

    def _calc_utils(self, impedance):
        self.dest_expsums = {}
        for mode in self.dest_choice_param:
            expsum = self._calc_dest_util(mode, impedance[mode])
            self.dest_expsums[mode] = {}
            self.dest_expsums[mode]["logsum"] = expsum
            logsum = pandas.Series(numpy.log(expsum), self.purpose.zone_numbers)
            label = self.purpose.name + "_" + mode[0]
            self.zone_data._values[label] = logsum
            self.resultdata.print_data(logsum, "accessibility.txt", label)
        mode_expsum = self._calc_mode_util(self.dest_expsums)
        logsum = pandas.Series(
            numpy.log(mode_expsum), self.purpose.zone_numbers)
        self.zone_data._values[self.purpose.name] = logsum
        self.resultdata.print_data(
            logsum, "accessibility.txt", self.purpose.name)
        return mode_expsum

    def _calc_prob(self, mode_expsum):
        prob = {}
        self.mode_prob = {}
        self.cumul_dest_prob = {}
        for mode in self.mode_choice_param:
            self.mode_prob[mode] = self.mode_exps[mode] / mode_expsum
            dest_expsum = self.dest_expsums[mode]["logsum"]
            dest_prob = self.dest_exps[mode].T / dest_expsum
            prob[mode] = self.mode_prob[mode] * dest_prob
            self.cumul_dest_prob[mode] = dest_prob.cumsum(axis=0)
        return prob

    def _get_cost_util_coefficient(self):
        try:
            b = self.dest_choice_param["car"]["impedance"]["cost"]
        except KeyError:
            # School tours do not have a constant cost parameter
            # Use value of time conversion from CBA guidelines instead
            b = -0.46738697
        return b


class AccessibilityModel(ModeDestModel):
    def calc_accessibility(self, impedance):
        """Calculate logsum-based accessibility measures.

        Individual dummy variables are not included.

        Parameters
        ----------
        impedance : dict
            Mode (car/transit/bike/walk) : dict
                Type (time/cost/dist) : numpy 2-d matrix
                    Impedances
        """
        mode_expsum = self._calc_utils(impedance)

        # Calculate sustainable and car accessibility
        sustainable_sum = numpy.zeros_like(mode_expsum)
        for mode in self.mode_choice_param:
            if mode != "car":
                sustainable_sum += self.mode_exps[mode]
        logsum = pandas.Series(
            numpy.log(sustainable_sum), self.purpose.zone_numbers)
        self.resultdata.print_data(
            logsum, "sustainable_accessibility.txt", self.purpose.name)
        b = self._get_cost_util_coefficient()
        try:
            money_utility = 1 / b
        except TypeError:  # Separate params for cap region and surrounding
            money_utility = 1 / b[0]
        money_utility /= self.mode_choice_param["car"]["log"]["logsum"]
        self.purpose.access = money_utility * self.zone_data[self.purpose.name]
        self.purpose.sustainable_access = money_utility * logsum
        self.purpose.car_access = (money_utility
                                   * self.zone_data[self.purpose.name + "_c"])

        # Calculate workplace-based accessibility
        if self.purpose.name in ("hw", "wh"):
            # Transform into person equivalents
            param = self.mode_choice_param
            normalization = 1 / sum([param[mode]["constant"][0]
                for mode in param])
            workforce = ((normalization*mode_expsum)
                            **(1/param["car"]["log"]["logsum"]))
            workforce = pandas.Series(workforce, self.purpose.zone_numbers)
            self.resultdata.print_data(
                workforce, "workplace_accessibility.txt", self.purpose.name)
            workplaces = self.zone_data["workplaces"][self.bounds]
            aggregate = ZoneIntervals("areas").averages(workforce, workplaces)
            self.resultdata.print_data(
                aggregate, "workplace_accessibility_areas.txt",
                self.purpose.name)
            names = {
                "hw": "Workplace effective density",
                "wh": "Workforce accessibility",
            }
            self.resultdata.print_line(
                "{}:\t{:1.0f}".format(
                    names[self.purpose.name], aggregate["all"]),
                "result_summary")

    def _add_constant(self, utility, b):
        """Add constant term to utility.

        If parameter b is a tuple of two terms,
        capital region will be picked.

        Parameters
        ----------
        utility : ndarray
            Numpy array to which the constant b will be added
        b : float or tuple
            The value of the constant
        """
        try: # If only one parameter
            utility += b
        except ValueError: # Separate params for cap region and surrounding
            utility += b[0]

    def _add_impedance(self, utility, impedance, b):
        """Adds simple linear impedances to utility.

        If parameter in b is tuple of two terms,
        capital region will be picked.

        Parameters
        ----------
        utility : ndarray
            Numpy array to which the impedances will be added
        impedance : dict
            A dictionary of time-averaged impedance matrices. Includes keys
            `time`, `cost`, and `dist` of which values are all ndarrays.
        b : dict
            The parameters for different impedance matrices.
        """
        for i in b:
            try: # If only one parameter
                utility += b[i] * impedance[i]
            except ValueError: # Separate params for cap region and surrounding
                utility += b[i][0] * impedance[i]
        return utility

    def _add_log_impedance(self, exps, impedance, b):
        """Adds log transformations of impedance to utility.

        This is an optimized way of calculating log terms. Calculates
        impedance1^b1 * ... * impedanceN^bN in the following equation:
        e^(linear_terms + b1*log(impedance1) + ... + bN*log(impedanceN))
        = e^(linear_terms) * impedance1^b1 * ... * impedanceN^bN

        If parameter in b is tuple of two terms,
        capital region will be picked.

        Parameters
        ----------
        exps : ndarray
            Numpy array to which the impedances will be multiplied
        impedance : dict
            A dictionary of time-averaged impedance matrices. Includes keys
            `time`, `cost`, and `dist` of which values are all ndarrays.
        b : dict
            The parameters for different impedance matrices
        """
        for i in b:
            try: # If only one parameter
                exps *= numpy.power(impedance[i] + 1, b[i])
            except ValueError: # Separate params for cap region and surrounding
                exps *= numpy.power(impedance[i] + 1, b[i][0])
        return exps

    def _add_zone_util(self, utility, b, generation=False):
        """Adds simple linear zone terms to utility.

        If parameter in b is tuple of two terms,
        capital region will be picked.

        Parameters
        ----------
        utility : ndarray
            Numpy array to which the impedances will be added
        b : dict
            The parameters for different zone data.
        generation : bool
            Whether the effect of the zone term is added only to the
            geographical area in which this model is used based on the
            `self.bounds` attribute of this class.
        """
        zdata = self.zone_data
        for i in b:
            try: # If only one parameter
                # Remove area dummies from accessibility indicators
                if i not in zone_params.areas:
                    utility += b[i] * zdata.get_data(
                        i, self.bounds, generation)
            except ValueError: # Separate params for cap region and surrounding
                utility += b[i][0] * zdata.get_data(i, self.bounds, generation)
        return utility


class DestModeModel(LogitModel):
    """Nested logit model with destination choice in upper level.

    Used only in peripheral non-home source model.
    Uses logsums from mode choice model as utility
    in destination choice model.

         choice
        /     \\
      d1        d2
     / \\      / \\
    m1   m2   m1   m2

    Parameters
    ----------
    zone_data : ZoneData
        Data used for all demand calculations
    purpose : TourPurpose
        Tour purpose (type of tour)
    resultdata : ResultData
        Writer object to result directory
    is_agent_model : bool (optional)
        Whether the model is used for agent-based simulation
    """

    def calc_prob(self, impedance):
        """Calculate matrix of choice probabilities.
        
        Parameters
        ----------
        impedance : dict
            Mode (car/transit/bike/walk) : dict
                Type (time/cost/dist) : numpy 2-d matrix
                    Impedances
        
        Returns
        -------
        dict
            Mode (car/transit/bike/walk) : numpy 2-d matrix
                Choice probabilities
        """
        mode_expsum = self._calc_mode_util(impedance)
        logsum = {"logsum": mode_expsum}
        dest_expsum = self._calc_dest_util("logsum", logsum)
        prob = {}
        dest_prob = self.dest_exps["logsum"].T / dest_expsum
        for mode in self.mode_choice_param:
            mode_prob = (self.mode_exps[mode] / mode_expsum).T
            prob[mode] = mode_prob * dest_prob
        return prob


class SecDestModel(LogitModel):
    """Logit model for secondary destination choice.

    Attaches secondary destinations to tours with already calculated
    modes and destinations.

    Parameters
    ----------
    zone_data : ZoneData
        Data used for all demand calculations
    purpose : TourPurpose
        Tour purpose (type of tour)
    resultdata : ResultData
        Writer object to result directory
    is_agent_model : bool (optional)
        Whether the model is used for agent-based simulation
    """

    def calc_prob(self, mode, impedance, origin, destination=None):
        """Calculate matrix of choice probabilities.
        
        Parameters
        ----------
        mode : str
            Mode (car/transit/bike)
        impedance : dict
            Type (time/cost/dist) : numpy 2d matrix
                Impedances
        origin: int
            Origin zone index
        destination: int or ndarray (optional)
            Destination zone index or boolean array (if calculation for 
            all primary destinations is performed in parallel)
        
        Returns
        -------
        numpy 2-d matrix
                Choice probabilities
        """
        dest_exps = self._calc_sec_dest_util(mode, impedance, origin, destination)
        return dest_exps.T / dest_exps.sum(1)


class OriginModel(DestModeModel):
    pass


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
        self.param = generation_params.tour_combinations
        self.conditions = generation_params.tour_conditions
        self.increases = generation_params.tour_number_increase
        self.tour_combinations = []
        for nr_tours in self.param:
            self.tour_combinations += self.param[nr_tours].keys()
    
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
            value : float or numpy 1-d array
                Choice probability
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
                if tour_combination in self.conditions:
                    if self.conditions[tour_combination][0]:
                        # If this tour pattern is exclusively for one age group
                        if age_group == self.conditions[tour_combination][1]:
                            is_allowed = True
                        else:
                            is_allowed = False
                    else:
                        # If one age group is excluded from this tour pattern
                        if age_group == self.conditions[tour_combination][1]:
                            is_allowed = False
                        else:
                            is_allowed = True
                else:
                    is_allowed = True
                if is_allowed:
                    param = self.param[nr_tours][tour_combination]
                    util = 0
                    util += param["constant"]
                    for i in param["zone"]:
                        util += param["zone"][i] * self.zone_data[i][zones]
                    dummies = param["individual_dummy"]
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
            scale_param = generation_params.tour_number_scale
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


class CarUseModel(LogitModel):
    """Binary logit model for car use.

    Parameters
    ----------
    zone_data : ZoneData
        Data used for all demand calculations
    bounds : slice
        Zone bounds
    age_groups : tuple
        tuple
            int
                Age intervals
    resultdata : ResultData
        Writer object to result directory
    """

    def __init__(self, zone_data, bounds, age_groups, resultdata):
        self.resultdata = resultdata
        self.zone_data = zone_data
        self.bounds = bounds
        self.genders = ("female", "male")
        self.age_groups = age_groups
        self.param = car_usage
        for i in self.param["individual_dummy"]:
            self._check(i)
    
    def _check(self, dummy):
        try:
            age_interval = dummy.split('_')[1]
        except AttributeError:
            # If the dummy is for a compound segment (age + gender)
            age_interval = dummy[0].split('_')[1]
            if dummy[1] not in self.genders:
                raise AttributeError(
                    "Car use dummy name {} not valid".format(dummy[1]))
        if tuple(map(int, age_interval.split('-'))) not in self.age_groups:
            raise AttributeError(
                "Car use dummy name {} not valid".format(age_interval))
    
    def calc_basic_prob(self):
        """Calculate car user probabilities without individual dummies.

        Returns
        -------
        numpy.ndarray
                Choice probabilities
        """
        b = self.param
        utility = numpy.zeros(self.bounds.stop)
        self._add_constant(utility, b["constant"])
        self._add_zone_util(utility, b["generation"], True)
        self.exps = numpy.exp(utility)
        self._add_log_zone_util(self.exps, b["log"], True)
        prob = self.exps / (self.exps+1)
        return prob

    def calc_prob(self):
        """Calculate car user probabilities with individual dummies included.

        Returns
        -------
        pandas.Series
                Choice probabilities
        """
        prob = self.calc_basic_prob()
        no_dummy_share = 1
        dummy_prob = 0
        b = self.param
        for i in b["individual_dummy"]:
            try:
                dummy_share = self.zone_data.get_data(
                    "share_"+i, self.bounds, generation=True)
            except TypeError:
                # If the dummy is for a compound segment (age + gender)
                dummy_share = numpy.ones_like(prob)
                for j in i:
                    dummy_share *= self.zone_data.get_data(
                        "share_"+j, self.bounds, generation=True)
            no_dummy_share -= dummy_share
            ind_exps = numpy.exp(b["individual_dummy"][i]) * self.exps
            ind_prob = ind_exps / (ind_exps+1)
            dummy_prob += dummy_share * ind_prob
        no_dummy_prob = no_dummy_share * prob
        prob = no_dummy_prob + dummy_prob
        prob = pandas.Series(
            prob, self.zone_data.zone_numbers[self.bounds])
        self.print_results(prob)
        return prob
    
    def calc_individual_prob(self, age_group, gender, zone=None):
        """Calculate car user probability with individual dummies included.
        
        Uses results from previously run `calc_basic_prob()`.
        
        Parameters
        ----------
        age_group : str
            Agent/segment age group
        gender : str
            Agent/segment gender (female/male)
        zone : int (optional)
            Index of zone where the agent lives, if no zone index is given,
            calculation is done for all zones
        
        Returns
        -------
        numpy.ndarray
                Choice probabilities
        """
        self._check((age_group, gender))
        if zone is None:
            exp = self.exps
        else:
            exp = self.exps[self.zone_data.zone_index(zone)]
        b = self.param
        if age_group in b["individual_dummy"]:
            exp = numpy.exp(b["individual_dummy"][age_group]) * exp
        if (age_group, gender) in b["individual_dummy"]:
            exp = numpy.exp(b["individual_dummy"][(age_group, gender)]) * exp
        prob = exp / (exp+1)
        return prob

    def print_results(self, prob, population_7_99=None):
        """ Print results, mainly for calibration purposes"""
        # Print car user share by zone
        self.resultdata.print_data(prob, "car_use.txt", "car_use")
        if population_7_99 is None:
            # Comparison data has car user shares of population
            # over 6 years old (from HEHA)
            population_7_99 = (self.zone_data["population"][self.bounds]
                               * self.zone_data["share_age_7-99"])
        # print car use share by municipality and area
        for area_type in ("municipalities", "areas"):
            prob_area = ZoneIntervals(area_type).averages(prob, population_7_99)
            self.resultdata.print_data(
                prob_area, "car_use_{}.txt".format(area_type), "car_use")
