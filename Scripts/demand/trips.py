import numpy
import pandas
import parameters

class DemandModel:
    def __init__(self, zone_data):
        self.zone_data = zone_data
        self.dest_exps = {}
        self.mode_exps = {}
        self.generated_tours = {}
        self.attracted_tours = {}

    def calc_demand(self, purpose, impedance):
        prob = self.calc_prob(purpose, impedance)
        nr_zones = len(self.zone_data.zone_numbers)
        if purpose.orig == "source":
            tours = numpy.zeros(nr_zones)
            for source in purpose.sources:
                b = parameters.tour_generation[purpose.name][source.name]
                for mode in source.attracted_tours:
                    source_tours = source.attracted_tours[mode]
                    tours += b * source_tours
        else:
            tours = self.generate_tours(purpose)
        demand = {}
        purpose.generated_tours = {}
        purpose.attracted_tours = {}
        for mode in parameters.mode_choice[purpose.name]:
            demand[mode] = (prob[mode] * tours).T
            purpose.attracted_tours[mode] = demand[mode].sum(0)
            purpose.generated_tours[mode] = demand[mode].sum(1)
        return demand

    def generate_tours(self, purpose):
        l, u = self.zone_data.get_bounds(purpose)
        nr_zones = u - l
        b = parameters.tour_generation[purpose.name]
        tours = numpy.zeros(nr_zones)
        for i in b:
            tours += b[i] * self.zone_data.values[i][l:u]
        return tours

    def calc_prob(self, purpose, impedance):
        if purpose.dest == "source":
            prob = self.calc_origin_prob(purpose, impedance)
        else:
            prob = self.calc_mode_dest_prob(purpose, impedance)
        return prob

    def calc_mode_dest_prob(self, purpose, impedance):
        dest_expsums = {}
        for mode in parameters.destination_choice[purpose.name]:
            expsum = self.calc_dest_util(purpose, mode, impedance[mode])
            dest_expsums[mode] = {}
            dest_expsums[mode]["logsum"] = expsum
        mode_expsum = self.calc_mode_util(purpose, dest_expsums)
        prob = {}
        for mode in parameters.mode_choice[purpose.name]:
            mode_prob = self.mode_exps[mode] / mode_expsum
            dest_expsum = dest_expsums[mode]["logsum"]
            dest_prob = self.dest_exps[mode].T / dest_expsum
            prob[mode] = mode_prob * dest_prob
        return prob

    def calc_dest_mode_prob(self, purpose, impedance):
        mode_expsum = self.calc_mode_util(purpose, impedance)
        logsum = {"logsum": mode_expsum}
        dest_expsum = self.calc_dest_util(purpose, "logsum", logsum)
        prob = {}
        dest_prob = self.dest_exps["logsum"].T / dest_expsum
        for mode in parameters.mode_choice[purpose.name]:
            mode_prob = (self.mode_exps[mode] / mode_expsum).T
            prob[mode] = mode_prob * dest_prob
        return prob

    def calc_mode_util(self, purpose, impedance):
        expsum = numpy.zeros_like(next(iter(impedance["car"].values())))
        for mode in parameters.mode_choice[purpose.name]:
            utility = numpy.zeros_like(expsum)
            b = parameters.mode_choice[purpose.name][mode]["constant"]
            self.add_constant(utility, b)
            b = parameters.mode_choice[purpose.name][mode]["generation"]
            utility = self.add_zone_util(purpose, utility.T, b, True).T
            b = parameters.mode_choice[purpose.name][mode]["attraction"]
            self.add_zone_util(purpose, utility, b, False)
            b = parameters.mode_choice[purpose.name][mode]["impedance"]
            self.add_impedance(utility, impedance[mode], b)
            self.mode_exps[mode] = numpy.exp(utility)
            b = parameters.mode_choice[purpose.name][mode]["log_impedance"]
            self.add_log_impedance(self.mode_exps[mode], impedance[mode], b)
            expsum += self.mode_exps[mode]
        return expsum
    
    def calc_dest_util(self, purpose, mode, impedance):
        utility = numpy.zeros_like(next(iter(impedance.values())))
        b = parameters.destination_choice[purpose.name][mode]["attraction"]
        self.add_zone_util(purpose, utility, b)
        b = parameters.destination_choice[purpose.name][mode]["impedance"]
        self.add_impedance(utility, impedance, b)
        self.dest_exps[mode] = numpy.exp(utility)
        size = numpy.zeros_like(utility)
        b = parameters.destination_choice[purpose.name][mode]["size"]
        self.add_zone_util(purpose, size, b)
        impedance["size"] = size
        b = parameters.destination_choice[purpose.name][mode]["log"]
        self.add_log_impedance(self.dest_exps[mode], impedance, b)
        if mode != "logsum":
            threshold = parameters.distance_boundary[mode]
            self.dest_exps[mode][impedance["dist"] > threshold] = 0
        return numpy.sum(self.dest_exps[mode], 1)

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
    
    def add_zone_util(self, purpose, utility, b, generation=False):
        zdata = self.zone_data
        k = zdata.zone_numbers.get_loc(parameters.first_surrounding_zone)
        for i in b:
            try:
                utility += b[i] * zdata.get_data(i, purpose, generation)
            except ValueError:
                data_capital_region = zdata.get_data(i, purpose, generation, 0)
                data_surrounding = zdata.get_data(i, purpose, generation, 1)
                if utility.ndim == 1:
                    utility[:k] += b[i][0] * data_capital_region
                    utility[k:] += b[i][1] * data_surrounding
                else:
                    utility[:k, :] += b[i][0] * data_capital_region
                    utility[k:, :] += b[i][1] * data_surrounding
        return utility

    def calc_origin_util(self, purpose, impedance):
        utility = numpy.zeros_like(next(iter(impedance["car"].values())))
        model = purpose.area
        modes = parameters.origin_choice[model]["impedance"]
        for mode in modes:
            b = parameters.origin_choice[model]["impedance"][mode]
            for i in b:
                utility += b[i] * impedance[mode][i]
        b = parameters.origin_choice[model]["attraction"]
        for i in b:
            utility += b[i] * self.zone_data.values[i]
        return utility

    def calc_origin_prob(self, purpose, impedance):
        utility = self.calc_origin_util(purpose, impedance)
        exps = numpy.exp(utility)
        # Here, size means kokotekija in Finnish
        size = numpy.ones_like(exps)
        b = parameters.origin_choice["logsum"]["attraction"]
        size = self.add_zone_util(purpose, size, b)
        size = numpy.power(size, parameters.origin_choice["logsum"]["log"]["attraction"])
        exps = size * exps
        expsums = numpy.sum(exps, axis=0)
        prob = {}
        # Mode is needed here to get through tests even
        # though the origin model does not take modes into account.
        prob["transit"] = (exps / expsums).T
        return prob
