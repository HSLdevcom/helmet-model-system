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
            self.insert_compounds(purpose, impedance)
            prob = self.calc_mode_dest_prob(purpose, impedance)
        return prob

    def insert_compounds(self, purpose, impedance):
        compounds = (
            "own_zone_area", 
            "own_zone_area_sq_capital",
            "own_zone_area_sq_surround",
        )
        for compound in compounds:
            self.insert_compound(purpose, impedance, compound)
    
    def insert_compound(self, purpose, impedance, compound_type):
        choices = (parameters.mode_choice, parameters.destination_choice)
        for choice in choices:
            for mode in choice[purpose]:
                if compound_type in choice[purpose][mode]["impedance"]:
                    if compound_type not in impedance:
                        impedance[compound_type] = {}
                        zone_area = self.get_compound(compound_type, purpose)
                    impedance[compound_type][mode] = zone_area

    def get_compound(self, compound_type, purpose):
        l, u = self.get_bounds(purpose)
        return self.zone_data.values[compound_type][l:u, :]
    
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
        dest_expsums = {"logsum": {}}
        for mode in parameters.destination_choice[purpose]:
            expsum = self.calc_dest_util(purpose, mode, impedance)
            dest_expsums["logsum"][mode] = expsum
        mode_expsum = self.calc_mode_util(purpose, dest_expsums)
        prob = {}
        for mode in parameters.mode_choice[purpose]:
            mode_prob = self.mode_exps[mode] / mode_expsum
            dest_expsum = dest_expsums["logsum"][mode]
            dest_prob = self.dest_exps[mode].T / dest_expsum
            prob[mode] = mode_prob * dest_prob
        return prob

    def calc_dest_mode_prob(self, purpose, impedance):
        mode_expsum = self.calc_mode_util(purpose, impedance)
        logsum = {"log": {"logsum": mode_expsum}}
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
            u = self.zone_data.values["population"].index.get_loc(u_label)
        if parameters.tour_purposes[purpose]["area"] == "peripheral":
            l_label = parameters.first_peripheral_zone
            l = self.zone_data.values["population"].index.get_loc(l_label)
            u = len(self.zone_data.values["population"])
        if parameters.tour_purposes[purpose]["area"] == "all":
            l = 0
            u = len(self.zone_data.values["population"])
        return l, u

    def calc_mode_util(self, purpose, impedance):
        expsum = numpy.zeros_like(next(iter(impedance.values()))["car"])
        l, u = self.get_bounds(purpose)
        for mode in parameters.mode_choice[purpose]:
            utility = numpy.zeros_like(expsum)
            utility += parameters.mode_choice[purpose][mode]["constant"]
            utility = utility.T
            b = parameters.mode_choice[purpose][mode]["generation"]
            for i in b:
                utility += b[i] * self.zone_data.values[i][l:u]
            utility = utility.T
            b = parameters.mode_choice[purpose][mode]["attraction"]
            for i in b:
                utility += b[i] * self.zone_data.values[i].values
            b = parameters.mode_choice[purpose][mode]["impedance"]
            for i in b:
                utility += b[i] * impedance[i][mode]
            self.mode_exps[mode] = numpy.exp(utility)
            b = parameters.mode_choice[purpose][mode]["log_impedance"]
            for i in b:
                self.mode_exps[mode] *= numpy.power(impedance[i][mode], b[i])
            expsum += self.mode_exps[mode]
        return expsum
    
    def calc_dest_util(self, purpose, mode, impedance):
        type_mtxs = next(iter(impedance.values()))
        mode_mtxs = next(iter(type_mtxs.values()))
        utility = numpy.zeros_like(mode_mtxs)
        b = parameters.destination_choice[purpose][mode]["attraction"]
        for i in b:
            utility += b[i] * self.zone_data.values[i]
        b = parameters.destination_choice[purpose][mode]["impedance"]
        for i in b:
            utility += b[i] * impedance[i][mode]
        self.dest_exps[mode] = numpy.exp(utility)
        nr_zones = len(self.zone_data.zone_numbers)
        size = numpy.ones(nr_zones)
        b = parameters.destination_choice[purpose][mode]["size"]
        for i in b:
            size += b[i] * self.zone_data.values[i]
        b = parameters.destination_choice[purpose][mode]["compound"]
        for i in b:
            size = size + b[i] * self.get_compound(i, purpose)
        logs = {}
        logs["size"] = size
        if "log" in impedance:
            for i in impedance["log"]:
                logs[i] = impedance["log"][i]
        b = parameters.destination_choice[purpose][mode]["log"]
        for i in b:
            self.dest_exps[mode] *= numpy.power(logs[i], b[i])
        return numpy.sum(self.dest_exps[mode], 1)

    def calc_origin_util(self, purpose, impedance):
        utility = numpy.zeros_like(next(iter(impedance.values()))["car"])
        if purpose == "oop":
            # TODO ???
            return utility + 1
        model = parameters.tour_purposes[purpose]["area"]
        modes = parameters.origin_choice[model]["impedance"]
        for mode in modes:
            b = parameters.origin_choice[model]["impedance"][mode]
            for i in b:
                utility += b[i] * impedance[i][mode]
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
        for i in b:
            size += b[i] * self.zone_data.values[i]
        b = parameters.origin_choice["logsum"]["compound"]
        for i in b:
            size += b[i] * self.get_compound(i, purpose)
        size = numpy.power(size, parameters.origin_choice["logsum"]["log"]["attraction"])
        exps = size * exps
        expsums = numpy.sum(exps, axis=0)
        prob = {}
        # Mode is needed here to get through tests even
        # though the origin model does not take modes into account.
        prob["transit"] = (exps / expsums).T
        return prob
