import numpy
import parameters

class LogitModel:
    def __init__(self, zone_data, purpose):
        self.purpose = purpose
        self.zone_data = zone_data
        self.dest_exps = {}
        self.mode_exps = {}
        self.dest_choice_param = parameters.destination_choice[purpose.name]
        self.mode_choice_param = parameters.mode_choice[purpose.name]

    def calc_mode_util(self, impedance):
        expsum = numpy.zeros_like(next(iter(impedance["car"].values())))
        for mode in self.mode_choice_param:
            b = self.mode_choice_param[mode]
            utility = numpy.zeros_like(expsum)
            self.add_constant(utility, b["constant"])
            utility = self.add_zone_util(utility=utility.T, 
                                         b=b["generation"], 
                                         generation=True).T
            self.add_zone_util(utility, b["attraction"], False)
            self.add_impedance(utility, impedance[mode], b["impedance"])
            exps = numpy.exp(utility)
            self.add_log_impedance(exps, impedance[mode], b["log"])
            self.mode_exps[mode] = exps
            expsum += exps
        return expsum
    
    def calc_dest_util(self, mode, impedance):
        b = self.dest_choice_param[mode]
        utility = numpy.zeros_like(next(iter(impedance.values())))
        self.add_zone_util(utility, b["attraction"])
        self.add_impedance(utility, impedance, b["impedance"])
        self.dest_exps[mode] = numpy.exp(utility)
        size = numpy.zeros_like(utility)
        self.add_zone_util(size, b["size"])
        impedance["size"] = size
        self.add_log_impedance(self.dest_exps[mode], impedance, b["log"])
        if mode != "logsum":
            threshold = parameters.distance_boundary[mode]
            self.dest_exps[mode][impedance["dist"] > threshold] = 0
        return numpy.sum(self.dest_exps[mode], 1)

    def calc_origin_util(self, impedance):
        b = self.dest_choice_param
        utility = numpy.zeros_like(next(iter(impedance["car"].values())))
        for mode in b["impedance"]:
            self.add_impedance(utility, impedance[mode], b["impedance"][mode])
        self.add_zone_util(utility, b["attraction"])
        return utility

    def add_constant(self, utility, b):
        k_label = parameters.first_surrounding_zone
        k = self.zone_data.zone_numbers.get_loc(k_label)
        try:
            utility += b
        except ValueError:
            if utility.ndim == 1:
                utility[:k] += b[0]
                utility[k:] += b[1]
            else:
                utility[:k, :] += b[0]
                utility[k:, :] += b[1]
    
    def add_impedance(self, utility, impedance, b):
        k_label = parameters.first_surrounding_zone
        k = self.zone_data.zone_numbers.get_loc(k_label)
        for i in b:
            try:
                utility += b[i] * impedance[i]
            except ValueError:
                utility[:k, :] += b[i][0] * impedance[i][:k, :]
                utility[k:, :] += b[i][1] * impedance[i][k:, :]
        return utility

    def add_log_impedance(self, exps, impedance, b):
        k_label = parameters.first_surrounding_zone
        k = self.zone_data.zone_numbers.get_loc(k_label)
        for i in b:
            try:
                exps *= numpy.power(impedance[i] + 1, b[i])
            except ValueError:
                exps[:k, :] *= numpy.power(impedance[i][:k, :] + 1, b[i][0])
                exps[k:, :] *= numpy.power(impedance[i][k:, :] + 1, b[i][1])
        return exps
    
    def add_zone_util(self, utility, b, generation=False):
        zdata = self.zone_data
        k = zdata.zone_numbers.get_loc(parameters.first_surrounding_zone)
        for i in b:
            try:
                utility += b[i] * zdata.get_data(i, self.purpose, generation)
            except ValueError:
                data_capital_region = zdata.get_data(i, self.purpose, generation, 0)
                data_surrounding = zdata.get_data(i, self.purpose, generation, 1)
                if utility.ndim == 1:
                    utility[:k] += b[i][0] * data_capital_region
                    utility[k:] += b[i][1] * data_surrounding
                else:
                    utility[:k, :] += b[i][0] * data_capital_region
                    utility[k:, :] += b[i][1] * data_surrounding
        return utility


class ModeDestModel(LogitModel):
    def calc_prob(self, impedance):
        dest_expsums = {}
        for mode in self.dest_choice_param:
            expsum = self.calc_dest_util(mode, impedance[mode])
            dest_expsums[mode] = {}
            dest_expsums[mode]["logsum"] = expsum
        mode_expsum = self.calc_mode_util(dest_expsums)
        prob = {}
        for mode in self.mode_choice_param:
            mode_prob = self.mode_exps[mode] / mode_expsum
            dest_expsum = dest_expsums[mode]["logsum"]
            dest_prob = self.dest_exps[mode].T / dest_expsum
            prob[mode] = mode_prob * dest_prob
        return prob


class DestModeModel(LogitModel):
    def calc_prob(self, impedance):
        mode_expsum = self.calc_mode_util(impedance)
        logsum = {"logsum": mode_expsum}
        dest_expsum = self.calc_dest_util("logsum", logsum)
        prob = {}
        dest_prob = self.dest_exps["logsum"].T / dest_expsum
        for mode in self.mode_choice_param:
            mode_prob = (self.mode_exps[mode] / mode_expsum).T
            prob[mode] = mode_prob * dest_prob
        return prob

class SecDestModel(LogitModel):
    def calc_prob(self, mode, impedance):
        expsum = self.calc_dest_util(mode, impedance)
        prob = self.dest_exps[mode].T / expsum
        return prob

class OriginModel(LogitModel):
    def calc_prob(self, impedance):
        b = self.dest_choice_param
        utility = self.calc_origin_util(impedance)
        exps = numpy.exp(utility)
        # Here, size means kokotekija in Finnish
        size = numpy.ones_like(exps)
        size = self.add_zone_util(size, b["size"])
        exps *= numpy.power(size, b["log"]["size"])
        expsums = numpy.sum(exps, axis=0)
        prob = {}
        # Mode is needed here to get through tests even
        # though the origin model does not take modes into account.
        prob["transit"] = (exps / expsums).T
        return prob