import numpy
import pandas
import math
import parameters


class LogitModel:
    def __init__(self, zone_data, purpose, resultdata, is_agent_model):
        self.resultdata = resultdata
        self.purpose = purpose
        self.bounds = purpose.bounds
        self.zone_data = zone_data
        self.dest_exps = {}
        self.mode_exps = {}
        self.dest_choice_param = parameters.destination_choice[purpose.name]
        self.mode_choice_param = parameters.mode_choice[purpose.name]
        if is_agent_model:
            self.dtype = float
        else:
            self.dtype = None

    def _calc_mode_util(self, impedance):
        expsum = numpy.zeros_like(next(iter(impedance["car"].values())), self.dtype)
        for mode in self.mode_choice_param:
            b = self.mode_choice_param[mode]
            utility = numpy.zeros_like(expsum)
            utility += self._add_constant(utility, b["constant"])
            utility += self._add_zone_util(
                utility.T, b["generation"], generation=True).T
            utility += self._add_zone_util(utility, b["attraction"])
            utility += self._add_impedance(utility, impedance[mode], b["impedance"])
            exps = numpy.exp(utility)
            exps *= self._add_log_impedance(exps, impedance[mode], b["log"])
            self.mode_exps[mode] = exps
            expsum += exps
        return expsum
    
    def _calc_dest_util(self, mode, impedance):
        b = self.dest_choice_param[mode]
        utility = numpy.zeros_like(next(iter(impedance.values())), self.dtype)
        utility += self._add_zone_util(utility, b["attraction"])
        utility += self._add_impedance(utility, impedance, b["impedance"])
        self.dest_exps[mode] = numpy.exp(utility)
        size = numpy.zeros_like(utility)
        utility += self._add_zone_util(size, b["size"])
        impedance["size"] = size
        if "transform" in b:
            b_transf = b["transform"]
            transimp = numpy.zeros_like(utility)
            transimp += self._add_zone_util(transimp, b_transf["attraction"])
            transimp += self._add_impedance(transimp, impedance, b_transf["impedance"])
            impedance["transform"] = transimp
        self.dest_exps[mode] *= self._add_log_impedance(self.dest_exps[mode], impedance, b["log"])
        if mode != "logsum":
            threshold = parameters.distance_boundary[mode]
            self.dest_exps[mode][impedance["dist"] > threshold] = 0
        try:
            return self.dest_exps[mode].sum(1)
        except ValueError:
            return self.dest_exps[mode].sum()
    
    def _calc_sec_dest_util(self, mode, impedance, orig, dest):
        b = self.dest_choice_param[mode]
        utility = numpy.zeros_like(next(iter(impedance.values())), self.dtype)
        utility += self._add_sec_zone_util(utility, b["attraction"], orig, dest)
        utility += self._add_impedance(utility, impedance, b["impedance"])
        dest_exps = numpy.exp(utility)
        size = numpy.zeros_like(utility)
        size += self._add_sec_zone_util(size, b["size"])
        impedance["size"] = size
        dest_exps *= self._add_log_impedance(dest_exps, impedance, b["log"])
        if mode != "logsum":
            threshold = parameters.distance_boundary[mode]
            dest_exps[impedance["dist"] > threshold] = 0
        return dest_exps

    def _add_constant(self, shape, b):
        """Calculates constant term for utility function.
        
        Parameters
        ----------
        shape : ndarray
            An example numpy array which tells the function to what shape the
            result will be broadcasted to.
        b : float
            The value of the constant.
        
        Returns
        -------
        ndarray
            A numpy array of the same size and type as `shape` but filled with
            the constant value. The result is to be added to utility.
        """
        utility = numpy.zeros_like(shape)
        try: # If only one parameter
            utility += b
        except ValueError: # Separate params for cap region and surrounding
            k = self.zone_data.first_surrounding_zone
            if utility.ndim == 1: # 1-d array calculation
                utility[:k] += b[0]
                utility[k:] += b[1]
            else: # 2-d matrix calculation
                utility[:k, :] += b[0]
                utility[k:, :] += b[1]
        return utility
    
    def _add_impedance(self, shape, impedance, b):
        """Calculates simple linear impedance terms for utility function.
        
        Parameters
        ----------
        shape : ndarray
            An example numpy array which tells the function to what shape the
            result will be broadcasted to.
        impedance : dict
            A dictionary of time-averaged impedance matrices. Includes keys
            `time`, `cost`, and `dist` of which values are all ndarrays.
        b : float
            The parameters for different impedance matrices.
        
        Returns
        -------
        ndarray
            A numpy array of the same size and type as `shape` but filled with
            the impedance terms. The result is to be added to utility.
        """
        utility = numpy.zeros_like(shape)
        for i in b:
            try: # If only one parameter
                utility += b[i] * impedance[i]
            except ValueError: # Separate params for cap region and surrounding
                k = self.zone_data.first_surrounding_zone
                utility[:k, :] += b[i][0] * impedance[i][:k, :]
                utility[k:, :] += b[i][1] * impedance[i][k:, :]
        return utility

    def _add_log_impedance(self, shape, impedance, b):
        """Calculates log transformations of impedance for utility function.
        
        This is an optimized way of calculating log terms. Calculates
        impedance1^b1 * ... * impedanceN^bN in the following equation:
        e^(linear_terms + b1*log(impedance1) + ... + bN*log(impedanceN))
        = e^(linear_terms) * impedance1^b1 * ... * impedanceN^bN

        Parameters
        ----------
        shape : ndarray
            An example numpy array which tells the function to what shape the
            result will be broadcasted to.
        impedance : dict
            A dictionary of time-averaged impedance matrices. Includes keys
            `time`, `cost`, and `dist` of which values are all ndarrays.
        b : float
            The parameters for different impedance matrices.
        
        Returns
        -------
        ndarray
            A numpy array of the same size and type as `shape` but filled with
            the impedance terms. The result is to be multiplied with the
            exponents of utility.
        """
        exps = numpy.ones_like(shape)
        for i in b:
            try: # If only one parameter
                exps *= numpy.power(impedance[i] + 1, b[i])
            except ValueError: # Separate params for cap region and surrounding
                k = self.zone_data.first_surrounding_zone
                exps[:k, :] *= numpy.power(impedance[i][:k, :] + 1, b[i][0])
                exps[k:, :] *= numpy.power(impedance[i][k:, :] + 1, b[i][1])
        return exps
    
    def _add_zone_util(self, shape, b, generation=False):
        """Calculates simple linear zone terms for utility function.
        
        Parameters
        ----------
        shape : ndarray
            An example numpy array which tells the function to what shape the
            result will be broadcasted to.
        b : float
            The parameters for different zone data.
        generation : bool
            Whether the effect of the zone term is added only to the
            geographical area in which this model is used based on the
            `self.bounds` attribute of this class.
        
        Returns
        -------
        ndarray
            A numpy array of the same size and type as `shape` but filled with
            the zone terms. The result is to be added to utility.
        """
        utility = numpy.zeros_like(shape)
        zdata = self.zone_data
        for i in b:
            try: # If only one parameter
                utility += b[i] * zdata.get_data(i, self.bounds, generation)
            except ValueError: # Separate params for cap region and surrounding
                k = self.zone_data.first_surrounding_zone
                data_capital_region = zdata.get_data(
                    i, self.bounds, generation, zdata.CAPITAL_REGION)
                data_surrounding = zdata.get_data(
                    i, self.bounds, generation, zdata.SURROUNDING_AREA)
                if utility.ndim == 1: # 1-d array calculation
                    utility[:k] += b[i][0] * data_capital_region
                    utility[k:] += b[i][1] * data_surrounding
                else: # 2-d matrix calculation
                    utility[:k, :] += b[i][0] * data_capital_region
                    utility[k:, :] += b[i][1] * data_surrounding
        return utility
    
    def _add_sec_zone_util(self, shape, b, orig=None, dest=None):
        utility = numpy.zeros_like(shape)
        zdata = self.zone_data
        for i in b:
            data = zdata.get_data(i, self.bounds, generation=True)
            try: # If only one parameter
                utility += b[i] * data
            except ValueError: # Separate params for orig and dest
                u = self.zone_data.first_peripheral_zone
                utility += b[i][0] * data[orig, :u]
                utility += b[i][1] * data[dest, :u]
        return utility

    def _add_log_zone_util(self, shape, b, generation=False):
        """Calculates log transformations of zone data for utility function.
        
        This is an optimized way of calculating log terms. Calculates
        zonedata1^b1 * ... * zonedataN^bN in the following equation:
        e^(linear_terms + b1*log(zonedata1) + ... + bN*log(zonedataN))
        = e^(linear_terms) * zonedata1^b1 * ... * zonedataN^bN

        Parameters
        ----------
        shape : ndarray
            An example numpy array which tells the function to what shape the
            result will be broadcasted to.
        b : float
            The parameters for different zone data.
        generation : bool
            Whether the effect of the zone term is added only to the
            geographical area in which this model is used based on the
            `self.bounds` attribute of this class.
        
        Returns
        -------
        ndarray
            A numpy array of the same size and type as `shape` but filled with
            the zone terms. The result is to be multiplied with the
            exponents of utility.
        """
        exps = numpy.ones_like(shape)
        zdata = self.zone_data
        for i in b:
            exps *= numpy.power(
                zdata.get_data(i, self.bounds, generation) + 1, b[i])
        return exps


class ModeDestModel(LogitModel):
    def calc_prob(self, impedance):
        """Calculate matrix of choice probabilities.
        Insert individual dummy variables.
        
        Parameters
        ----------
        impedance : dict
            Mode (car/transit/bike/walk) : dict
                Type (time/cost/dist) : numpy 2-d matrix
                    Impedances
        
        Return
        ------
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
        """Calculate matrix of choice probabilities.
        
        Parameters
        ----------
        impedance : dict
            Mode (car/transit/bike/walk) : dict
                Type (time/cost/dist) : numpy 2-d matrix
                    Impedances
        
        Return
        ------
        dict
            Mode (car/transit/bike/walk) : numpy 2-d matrix
                Choice probabilities
        """
        mode_expsum = self._calc_utils(impedance)
        logsum = numpy.log(mode_expsum)
        self.resultdata.print_data(
            pandas.Series(logsum, self.purpose.zone_numbers),
            "accessibility.txt",
            self.zone_data.zone_numbers,
            self.purpose.name
        )
        return self._calc_prob(mode_expsum)
    
    def calc_individual_prob(self, mod_mode, dummy):
        """Calculate matrix of choice probabilities
        with individual dummy variable included.
        
        Parameters
        ----------
        mod_mode : str
            The mode for which the utility will be modified
        dummy : str
            The name of the individual dummy
        
        Return
        ------
        dict
            Mode (car/transit/bike/walk) : numpy 2-d matrix
                Choice probabilities
        """
        k = self.zone_data.first_surrounding_zone
        b = self.mode_choice_param[mod_mode]["individual_dummy"][dummy]
        try:
            self.mode_exps[mod_mode] *= numpy.exp(b)
        except ValueError:
            self.mode_exps[mod_mode][:k] *= numpy.exp(b[0])
            self.mode_exps[mod_mode][k:] *= numpy.exp(b[1])
        mode_expsum = numpy.zeros_like(self.mode_exps[mod_mode])
        for mode in self.mode_choice_param:
            mode_expsum += self.mode_exps[mode]
        return self._calc_prob(mode_expsum)
    
    def calc_individual_mode_prob(self, is_car_user, zone):
        """Calculate choice probabilities for individual agent
        with individual dummy variable included.
        
        Parameters
        ----------
        is_car_user : bool
            Whether the agent is car user or not
        zone : int
            Index of zone where the agent lives
        
        Return
        ------
        list
            Choice probabilities for purpose modes
        """
        mode_exps = {}
        mode_expsum = 0
        for mode in self.mode_choice_param:
            mode_exps[mode] = self.mode_exps[mode][zone]
            b = self.mode_choice_param[mode]["individual_dummy"]
            if is_car_user and "car_users" in b:
                try:
                    mode_exps[mode] *= math.exp(b["car_users"])
                except TypeError:
                    if zone < self.zone_data.first_surrounding_zone:
                        mode_exps[mode] *= math.exp(b["car_users"][0])
                    else:
                        mode_exps[mode] *= math.exp(b["car_users"][1])
            mode_expsum += mode_exps[mode]
        probs = []
        for mode in self.purpose.modes:
            probs.append(mode_exps[mode] / mode_expsum)
        return probs

    def _calc_utils(self, impedance):
        self.dest_expsums = {}
        for mode in self.dest_choice_param:
            expsum = self._calc_dest_util(mode, impedance[mode])
            self.dest_expsums[mode] = {}
            self.dest_expsums[mode]["logsum"] = expsum
            logsum = pandas.Series(numpy.log(expsum), self.purpose.zone_numbers)
            label = self.purpose.name + "_" + mode[0]
            self.zone_data._values[label] = logsum
            self.resultdata.print_data(
                logsum,
                "accessibility.txt",
                self.zone_data.zone_numbers,
                label
            )
        return self._calc_mode_util(self.dest_expsums)

    def _calc_prob(self, mode_expsum):
        prob = {}
        self.mode_prob = {}
        self.dest_prob = {}
        for mode in self.mode_choice_param:
            self.mode_prob[mode] = self.mode_exps[mode] / mode_expsum
            dest_expsum = self.dest_expsums[mode]["logsum"]
            self.dest_prob[mode] = self.dest_exps[mode].T / dest_expsum
            prob[mode] = self.mode_prob[mode] * self.dest_prob[mode]
        return prob


class DestModeModel(LogitModel):
    def calc_prob(self, impedance):
        """Calculate matrix of choice probabilities.
        
        Parameters
        ----------
        impedance : dict
            Mode (car/transit/bike/walk) : dict
                Type (time/cost/dist) : numpy 2-d matrix
                    Impedances
        
        Return
        ------
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
    def calc_prob(self, mode, impedance, origin=None, destination=None):
        """Calculate matrix of choice probabilities.
        
        Parameters
        ----------
        mode : str
            Mode (car/transit/bike)
        impedance : dict
            Type (time/cost/dist) : numpy 2d matrix
                Impedances
        origin: int
            Origin
        destination:
            Destination
        
        Return
        ------
        numpy 2-d matrix
                Choice probabilities
        """
        dest_exps = self._calc_sec_dest_util(mode, impedance, origin, destination)
        try:
            expsum = dest_exps.sum(1)
        except ValueError:
            expsum = dest_exps.sum()
        prob = dest_exps.T / expsum
        return prob


class OriginModel(DestModeModel):
    pass


class TourCombinationModel:
    def __init__(self, zone_data):
        self.zone_data = zone_data
        self.param = parameters.tour_combinations
        self.conditions = parameters.tour_conditions
        self.increases = parameters.tour_number_increase
    
    def calc_prob(self, age_group, is_car_user, zones):
        """Calculate choice probabilities for each tour combination.
        
        Parameters
        ----------
        age_group : str
            Age group (age_7-17/age_18-29/...)
        is_car_user : bool
            True if is car user
        zones : int or slice
            Zone number (for agent model) or zone data slice

        Return
        ------
        dict
            Tour combination (-/hw/hw-ho/...) : float or numpy 1-d array
                Choice probability
        """
        prob = {}
        nr_tours_exps = {}
        nr_tours_expsum = 0
        for nr_tours in self.param:
            combination_exps = {}
            combination_expsum = 0
            for tour_combination in self.param[nr_tours]:
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
            scale_param = parameters.tour_number_scale
            nr_tours_exps[nr_tours] *= numpy.power(combination_expsum, scale_param)
            nr_tours_expsum += nr_tours_exps[nr_tours]
        prob["-"] = 1
        for nr_tours in self.param:
            if nr_tours != 0:
                nr_tours_prob = nr_tours_exps[nr_tours] / nr_tours_expsum
                # Tour number probability is calibrated
                nr_tours_prob *= self.increases[nr_tours]
                prob["-"] -= nr_tours_prob
                for tour_combination in self.param[nr_tours]:
                    prob[tour_combination] *= nr_tours_prob
        return prob


class CarUseModel(LogitModel):
    def __init__(self, zone_data, bounds, resultdata):
        self.resultdata = resultdata
        self.zone_data = zone_data
        self.bounds = bounds
    
    def calc_basic_prob(self):
        b = parameters.car_usage
        utility = numpy.zeros(self.bounds.stop)
        utility += self._add_constant(utility, b["constant"])
        utility += self._add_zone_util(utility, b["generation"], True)
        self.exps = numpy.exp(utility)
        self.exps *= self._add_log_zone_util(self.exps, b["log"], True)
        prob = self.exps / (self.exps+1)
        return prob

    def calc_prob(self):
        prob = self.calc_basic_prob()
        no_dummy_share = 1
        dummy_prob = 0
        b = parameters.car_usage
        for i in b["individual_dummy"]:
            try:
                dummy_share = self.zone_data.get_data(
                    "share_"+i, self.bounds, generation=True)
            except TypeError:
                dummy_share = numpy.ones_like(prob)
                for j in i:
                    dummy_share *= self.zone_data.get_data("share_"+j, self.bounds, generation=True)
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
        if zone is None:
            exp = self.exps
        else:
            exp = self.exps[self.zone_data.zone_index(zone)]
        b = parameters.car_usage
        if age_group in b["individual_dummy"]:
            exp = numpy.exp(b["individual_dummy"][age_group]) * exp
        if (age_group, gender) in b["individual_dummy"]:
            exp = numpy.exp(b["individual_dummy"][(age_group, gender)]) * exp
        prob = exp / (exp+1)
        return prob

    def print_results(self, prob):
        """ Print results, mainly for calibration purposes"""
        population = self.zone_data["population"]
        population_7_99 = (population[:self.zone_data.first_peripheral_zone] * self.zone_data["share_age_7-99"])
        car_users = prob * population_7_99
                
        # Print car user share by zone
        self.resultdata.print_data(prob, "car_use.txt", self.zone_data.zone_numbers[self.bounds], "car_use")
        
        # print car use share by municipality
        prob_municipality = []
        for municipality in parameters.municipality:
            i = slice(parameters.municipality[municipality][0],
                      parameters.municipality[municipality][1])
            # comparison data has car user shares of population
            # over 6 years old (from HEHA)
            prob_municipality.append(car_users.loc[i].sum() / population_7_99.loc[i].sum())
        self.resultdata.print_data(prob_municipality, "car_use_per_municipality.txt", parameters.municipality.keys(), "car_use")
                          
        # print car use share by area (to get Helsinki CBD vs. Helsinki other)
        prob_area = []
        for area in parameters.areas:
            i = slice(parameters.areas[area][0],
                      parameters.areas[area][1])
            # comparison data has car user shares of population
            # over 6 years old (from HEHA)
            prob_area.append(car_users.loc[i].sum() / population_7_99.loc[i].sum())
        self.resultdata.print_data(prob_area, "car_use_per_area.txt", parameters.areas.keys(), "car_use")
