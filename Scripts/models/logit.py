import numpy
import pandas
import parameters
import datahandling.resultdata as result


class LogitModel:
    def __init__(self, zone_data, purpose):
        self.purpose = purpose
        self.zone_data = zone_data
        self.dest_exps = {}
        self.mode_exps = {}
        self.dest_choice_param = parameters.destination_choice[purpose.name]
        self.mode_choice_param = parameters.mode_choice[purpose.name]

    def _calc_mode_util(self, impedance):
        # Impedances from omx are float32, here we use float64 to make
        # numpy random choice for agents work. Memory issue?
        expsum = numpy.zeros_like(next(iter(impedance["car"].values())), float)
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
        utility = numpy.zeros_like(next(iter(impedance.values())), float)
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
            threshold = parameters.distance_boundary[mode]
            self.dest_exps[mode][impedance["dist"] > threshold] = 0
        try:
            return self.dest_exps[mode].sum(1)
        except ValueError:
            return self.dest_exps[mode].sum()

    def _calc_origin_util(self, impedance):
        b = self.dest_choice_param
        utility = numpy.zeros_like(next(iter(impedance["car"].values())))
        for mode in b["impedance"]:
            self._add_impedance(utility, impedance[mode], b["impedance"][mode])
        self._add_zone_util(utility, b["attraction"])
        return utility

    def _add_constant(self, utility, b):
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
    
    def _add_impedance(self, utility, impedance, b):
        for i in b:
            try: # If only one parameter
                utility += b[i] * impedance[i]
            except ValueError: # Separate params for cap region and surrounding
                k = self.zone_data.first_surrounding_zone
                utility[:k, :] += b[i][0] * impedance[i][:k, :]
                utility[k:, :] += b[i][1] * impedance[i][k:, :]
        return utility

    def _add_log_impedance(self, exps, impedance, b):
        for i in b:
            try: # If only one parameter
                exps *= numpy.power(impedance[i] + 1, b[i])
            except ValueError: # Separate params for cap region and surrounding
                k = self.zone_data.first_surrounding_zone
                exps[:k, :] *= numpy.power(impedance[i][:k, :] + 1, b[i][0])
                exps[k:, :] *= numpy.power(impedance[i][k:, :] + 1, b[i][1])
        return exps
    
    def _add_zone_util(self, utility, b, generation=False):
        zdata = self.zone_data
        for i in b:
            try: # If only one parameter
                utility += b[i] * zdata.get_data(i, self.purpose, generation)
            except ValueError: # Separate params for cap region and surrounding
                k = self.zone_data.first_surrounding_zone
                data_capital_region = zdata.get_data(
                    i, self.purpose, generation, zdata.CAPITAL_REGION)
                data_surrounding = zdata.get_data(
                    i, self.purpose, generation, zdata.SURROUNDING_AREA)
                if utility.ndim == 1: # 1-d array calculation
                    utility[:k] += b[i][0] * data_capital_region
                    utility[k:] += b[i][1] * data_surrounding
                else: # 2-d matrix calculation
                    utility[:k, :] += b[i][0] * data_capital_region
                    utility[k:, :] += b[i][1] * data_surrounding
        return utility

    def _add_log_zone_util(self, exps, b, generation=False):
        zdata = self.zone_data
        for i in b:
            exps *= numpy.power(zdata.get_data(i, self.purpose, generation) + 1, b[i])
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
        
        Return
        ------
        dict
            Mode (car/transit/bike/walk) : dict
                Choice probabilities : numpy 2-d matrix
        """
        prob = self.calc_basic_prob(impedance)
        for mod_mode in self.mode_choice_param:
            for i in self.mode_choice_param[mod_mode]["individual_dummy"]:
                dummy_share = self.zone_data.get_data(
                    i, self.purpose, generation=True).values
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
        
        Return
        ------
        dict
            Mode (car/transit/bike/walk) : dict
                Choice probabilities : numpy 2-d matrix
        """
        mode_expsum = self._calc_utils(impedance)
        logsum = numpy.log(mode_expsum)
        result.print_data(
            pandas.Series(logsum, self.purpose.zone_numbers),
            "accessibility.txt", self.zone_data.zone_numbers,
            self.purpose.name)
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
            Mode (car/transit/bike/walk) : dict
                Choice probabilities : numpy 2-d matrix
        """
        k = self.zone_data.first_surrounding_zone
        b = self.mode_choice_param[mod_mode]["individual_dummy"][dummy]
        try:
            self.mode_exps[mod_mode] = b * self.mode_exps[mod_mode]
        except ValueError:
            self.mode_exps[mod_mode][:k] = b[0] * self.mode_exps[mod_mode][:k]
            self.mode_exps[mod_mode][k:] = b[1] * self.mode_exps[mod_mode][k:]
        mode_expsum = numpy.zeros_like(self.mode_exps[mod_mode])
        for mode in self.mode_choice_param:
            mode_expsum += self.mode_exps[mode]
        return self._calc_prob(mode_expsum)
    
    def _calc_utils(self, impedance):
        self.dest_expsums = {}
        for mode in self.dest_choice_param:
            expsum = self._calc_dest_util(mode, impedance[mode])
            self.dest_expsums[mode] = {}
            self.dest_expsums[mode]["logsum"] = expsum
            logsum = numpy.log(expsum)
            result.print_data(
                pandas.Series(logsum, self.purpose.zone_numbers),
                "accessibility.txt", self.zone_data.zone_numbers,
                self.purpose.name + "_" + mode[0])
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
        
        Return
        ------
        dict
            Mode (car/transit/bike/walk) : dict
                Choice probabilities : numpy 2-d matrix
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
    def calc_prob(self, mode, impedance):
        """Calculate matrix of choice probabilities.
        
        Parameters
        ----------
        mode : str
            Mode (car/transit/bike)
        impedance : dict
            Type (time/cost/dist) : numpy 2d matrix
        
        Return
        ------
        numpy 2-d matrix
                Choice probabilities
        """
        expsum = self._calc_dest_util(mode, impedance)
        prob = self.dest_exps[mode].T / expsum
        return prob


class OriginModel(LogitModel):
    def calc_prob(self, impedance):
        """Calculate matrix of choice probabilities.
        
        Parameters
        ----------
        impedance : dict
            Mode (car/transit/bike/walk) : dict
                Type (time/cost/dist) : numpy 2-d matrix
        
        Return
        ------
        dict
            Mode (transit) : dict
                Choice probabilities : numpy 2-d matrix
        """
        b = self.dest_choice_param
        utility = self._calc_origin_util(impedance)
        exps = numpy.exp(utility)
        # Here, size means kokotekija in Finnish
        size = numpy.ones_like(exps)
        size = self._add_zone_util(size, b["size"])
        exps *= numpy.power(size, b["log"]["size"])
        expsums = numpy.sum(exps, axis=0)
        prob = {}
        # Mode is needed here to get through tests even
        # though the origin model does not take modes into account.
        prob["all"] = (exps / expsums).T
        return prob


class CarUseModel(LogitModel):
    def __init__(self, zone_data, purpose):
        self.zone_data = zone_data
        self.purpose = purpose
    
    def calc_prob(self):
        b = parameters.car_usage
        utility = numpy.zeros(self.purpose.bounds[1])
        self._add_constant(utility, b["constant"])
        self._add_zone_util(utility, b["generation"], True)
        exps = numpy.exp(utility)
        self._add_log_zone_util(exps, b["log"], True)
        prob = exps / (exps+1)
        no_dummy_share = 1
        dummy_prob = 0
        for i in b["individual_dummy"]:
            dummy_share = self.zone_data.get_data(
                i, self.purpose, generation=True).values
            no_dummy_share -= dummy_share
            ind_exps = numpy.exp(b["individual_dummy"][i]) * exps
            ind_prob = ind_exps / (ind_exps+1)
            dummy_prob += dummy_share * ind_prob
        no_dummy_prob = no_dummy_share * prob
        prob = no_dummy_prob + dummy_prob
        return pandas.Series(prob, self.purpose.zone_numbers)
