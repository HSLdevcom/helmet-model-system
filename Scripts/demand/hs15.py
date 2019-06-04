import numpy
import parameters

class DemandHS15:
    def __init__(self, zone_data):
        self.zone_data = zone_data
        self.dest_exps = {}
        self.mode_exps = {}
        nr_zones = len(zone_data.values["area"])
        di = numpy.diag_indices(nr_zones)
        self.zone_area = numpy.zeros((nr_zones, nr_zones))
        self.zone_area[di] = zone_data.values["area"]

    def get_zone_area(self, purpose):
        l, u = self.get_bounds(purpose)
        return self.zone_area[l:u, :]

    def calc_demand(self, purpose, impedance):
        trips = self.generate_trips(purpose)
        zone_area = self.get_zone_area(purpose)
        impedance["zone_area"] = {
            "car": zone_area,
            "transit": zone_area,
            "bike": zone_area,
        }
        if parameters.tour_purposes[purpose]["area"] == "peripheral":
            demand = self.calc_dest_mode(purpose, impedance, trips)
        else:
            demand = self.calc_mode_dest(purpose, impedance, trips)
        return demand

    def calc_mode_dest(self, purpose, impedance, trips):
        dest_expsums = {"logsum": {}}
        for mode in parameters.destination_choice[purpose]:
            expsum = self.calc_dest_util(purpose, mode, impedance)
            dest_expsums["logsum"][mode] = expsum
        mode_expsum = self.calc_mode_util(purpose, dest_expsums)
        demand = {}
        for mode in parameters.mode_choice[purpose]:
            mode_prob = self.mode_exps[mode] / mode_expsum
            dest_expsum = dest_expsums["logsum"][mode]
            dest_prob = self.dest_exps[mode].T / dest_expsum
            demand[mode] = (mode_prob * dest_prob * trips).T
        return demand

    def calc_dest_mode(self, purpose, impedance, trips):
        mode_expsum = self.calc_mode_util(purpose, impedance)
        logsum = {"log": {"logsum": mode_expsum}}
        dest_expsum = self.calc_dest_util(purpose, "logsum", logsum)
        demand = {}
        dest_prob = self.dest_exps["logsum"].T / dest_expsum
        for mode in parameters.mode_choice[purpose]:
            mode_prob = self.mode_exps[mode] / mode_expsum
            demand[mode] = (mode_prob * dest_prob * trips).T
        return demand

    def generate_trips(self, purpose):
        l, u = self.get_bounds(purpose)
        nr_zones = u - l
        b = parameters.trip_generation[purpose]
        trips = numpy.zeros(nr_zones)
        for i in b:
            trips += b[i] * self.zone_data.values[i][l:u]
        return trips

    def get_bounds(self, purpose):
        if parameters.tour_purposes[purpose]["area"] == "hs15":
            l = 0
            u_label = parameters.first_peripheral_zone
            u = self.zone_data.values["population"].index.get_loc(u_label)
        if parameters.tour_purposes[purpose]["area"] == "peripheral":
            l_label = parameters.first_peripheral_zone
            l = self.zone_data.values["population"].index.get_loc(l_label)
            u = len(self.zone_data.values["population"])
        return l, u

    def calc_mode_util(self, purpose, impedance):
        expsum = numpy.zeros_like(next(iter(impedance.values()))["car"])
        l, u = self.get_bounds(purpose)
        for mode in parameters.mode_choice[purpose]:
            utility = numpy.zeros_like(expsum)
            utility = utility.T
            b = parameters.mode_choice[purpose][mode]["generation"]
            for i in b:
                # TODO Check that this works for ympk also with several zones
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
        b = parameters.destination_choice[purpose][mode]["impedance"]
        for i in b:
            utility += b[i] * impedance[i][mode]
        self.dest_exps[mode] = numpy.exp(utility)
        nr_zones = len(self.zone_data.values["workplaces"])
        attraction = numpy.zeros(nr_zones)
        b = parameters.destination_choice[purpose][mode]["attraction"]
        for i in b:
            attraction += b[i] * self.zone_data.values[i]
        logs = {}
        logs["attraction"] = attraction
        if "log" in impedance:
            for i in impedance["log"]:
                logs[i] = impedance["log"][i]
        b = parameters.destination_choice[purpose][mode]["log"]
        for i in b:
            self.dest_exps[mode] *= numpy.power(logs[i], b[i])
        return numpy.sum(self.dest_exps[mode], 1)

    def _mul(self, parameter, variable):
        result = numpy.zeros(len(variable[0]))
        for i in parameter:
            result += parameter[i] * variable[i]
        return result