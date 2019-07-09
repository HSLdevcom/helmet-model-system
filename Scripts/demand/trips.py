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
        if parameters.tour_purposes[purpose]["type"] == "other-other":
            tours = numpy.zeros(nr_zones)
            for source in parameters.tour_purposes[purpose]["source"]:
                b = parameters.tour_generation[purpose][source]
                for mode in self.attracted_tours[source]:
                    source_tours = self.attracted_tours[source][mode]
                    tours += b * source_tours
        else:
            tours = self.generate_tours(purpose)
        demand = {}
        self.generated_tours[purpose] = {}
        self.attracted_tours[purpose] = {}
        for mode in parameters.mode_choice[purpose]:
            demand[mode] = (prob[mode] * tours).T
            self.attracted_tours[purpose][mode] = demand[mode].sum(0)
            self.generated_tours[purpose][mode] = demand[mode].sum(1)
        return demand

    def generate_tours(self, purpose):
        l, u = self.get_bounds(purpose)
        nr_zones = u - l
        b = parameters.tour_generation[purpose]
        tours = numpy.zeros(nr_zones)
        for i in b:
            tours += b[i] * self.zone_data.values[i][l:u]
        return tours

    def calc_prob(self, purpose, impedance):
        if parameters.tour_purposes[purpose]["type"] == "source-other-peripheral":
            prob = self.calc_origin_prob(purpose, impedance)
        else:
            prob = self.calc_mode_dest_prob(purpose, impedance)
        return prob

    def get_compound(self, data_type, purpose, part=None):
        l, u = self.get_bounds(purpose)
        k = self.zone_data.zone_numbers.get_loc(2792)
        if self.zone_data.values[data_type].ndim == 1:
            return self.zone_data.values[data_type]
        if part is None:
            return self.zone_data.values[data_type][l:u, :]
        elif part == 0:
            return self.zone_data.values[data_type][l:u, :][:k, :]
        else:
            return self.zone_data.values[data_type][l:u, :][k:, :]
    
    def get_sum(self, mode):
        nr_zones = len(self.zone_data.zone_numbers)
        trips = numpy.zeros(nr_zones)
        for purpose in self.generated_tours:
            if purpose != "sop":
                l, u = self.get_bounds(purpose)
                trips[l:u] += self.generated_tours[purpose][mode]
                trips += self.attracted_tours[purpose][mode]
        return trips

    def calc_mode_dest_prob(self, purpose, impedance):
        dest_expsums = {}
        for mode in parameters.destination_choice[purpose]:
            expsum = self.calc_dest_util(purpose, mode, impedance[mode])
            dest_expsums[mode] = {}
            dest_expsums[mode]["logsum"] = expsum
        mode_expsum = self.calc_mode_util(purpose, dest_expsums)
        prob = {}
        for mode in parameters.mode_choice[purpose]:
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
        for mode in parameters.mode_choice[purpose]:
            mode_prob = (self.mode_exps[mode] / mode_expsum).T
            prob[mode] = mode_prob * dest_prob
        return prob

    def get_bounds(self, purpose):
        if parameters.tour_purposes[purpose]["area"] == "metropolitan":
            l = 0
            u_label = parameters.first_peripheral_zone
            u = self.zone_data.zone_numbers.get_loc(u_label)
        if parameters.tour_purposes[purpose]["area"] == "peripheral":
            l_label = parameters.first_peripheral_zone
            l = self.zone_data.zone_numbers.get_loc(l_label)
            u = len(self.zone_data.zone_numbers)
        if parameters.tour_purposes[purpose]["area"] == "all":
            l = 0
            u = len(self.zone_data.zone_numbers)
        return l, u

    def calc_mode_util(self, purpose, impedance):
        expsum = numpy.zeros_like(next(iter(impedance["car"].values())))
        for mode in parameters.mode_choice[purpose]:
            utility = numpy.zeros_like(expsum)
            utility += parameters.mode_choice[purpose][mode]["constant"]
            b = parameters.mode_choice[purpose][mode]["generation"]
            utility = self.add_zone_util(purpose, utility.T, b, True).T
            b = parameters.mode_choice[purpose][mode]["attraction"]
            utility = self.add_zone_util(purpose, utility, b, False)
            b = parameters.mode_choice[purpose][mode]["impedance"]
            utility = self.add_impedance(utility, impedance, b)
            self.mode_exps[mode] = numpy.exp(utility)
            b = parameters.mode_choice[purpose][mode]["log_impedance"]
            for i in b:
                self.mode_exps[mode] *= numpy.power(impedance[mode][i], b[i])
            expsum += self.mode_exps[mode]
        return expsum
    
    def calc_dest_util(self, purpose, mode, impedance):
        utility = numpy.zeros_like(next(iter(impedance.values())))
        b = parameters.destination_choice[purpose][mode]["attraction"]
        utility = self.add_zone_util(purpose, utility, b)
        b = parameters.destination_choice[purpose][mode]["impedance"]
        utility = self.add_impedance(utility, impedance, b)
        self.dest_exps[mode] = numpy.exp(utility)
        size = numpy.ones_like(utility)
        b = parameters.destination_choice[purpose][mode]["size"]
        size = self.add_zone_util(purpose, size, b)
        impedance["size"] = size
        b = parameters.destination_choice[purpose][mode]["log"]
        for i in b:
            self.dest_exps[mode] *= numpy.power(impedance[i], b[i])
        return numpy.sum(self.dest_exps[mode], 1)

    def add_impedance(self, utility, impedance, b):
        k = self.zone_data.zone_numbers.get_loc(2792)
        for i in b:
            try:
                utility += b[i] * impedance[i]
            except ValueError:
                utility[:k, :] += b[i][0] * impedance[i][:k, :]
                utility[k:, :] += b[i][1] * impedance[i][k:, :]
        return utility
    
    def add_zone_util(self, purpose, utility, b, generation=False):
        k = self.zone_data.zone_numbers.get_loc(2792)
        for i in b:
            try:
                utility += b[i] * self.zone_data.get_data(i, purpose, generation)
            except ValueError:
                utility[:k, :] += b[i][0] * self.zone_data.get_data(i, purpose, generation, 0)
                utility[k:, :] += b[i][1] * self.zone_data.get_data(i, purpose, generation, 1)
        return utility

    def calc_origin_util(self, purpose, impedance):
        utility = numpy.zeros_like(next(iter(impedance["car"].values())))
        if purpose == "oop":
            # TODO ???
            return utility + 1
        model = parameters.tour_purposes[purpose]["area"]
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
