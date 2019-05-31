import numpy
import parameters

class DemandHS15:
    def __init__(self, zone_data):
        self.zone_data = zone_data
        self.dest_exps = {}
        self.mode_exps = {}

    def calc_demand(self, purpose, impedance):
        trips = self.generate_trips(purpose)
        dest_expsums = {}
        for mode in parameters.destination_choice[purpose]:
            expsum = self.calc_dest_util(purpose, mode, impedance)
            dest_expsums[mode] = {"logsum": expsum}
        mode_expsum = self.calc_mode_util(purpose, dest_expsums)
        demand = {}
        for mode in parameters.destination_choice[purpose]:
            mode_probability = self.mode_exps[mode] / mode_expsum
            dest_expsum = dest_expsums[mode]["logsum"][:, numpy.newaxis]
            destination_probability = self.dest_exps[mode] / dest_expsum
            demand[mode] = ( mode_probability[:, numpy.newaxis] 
                           * destination_probability 
                           * trips[:, numpy.newaxis])
        return demand

    def generate_trips(self, purpose):
        if parameters.tour_purposes[purpose]["area"] == "hs15":
            l = 0
            u_label = parameters.first_peripheral_zone
            u = self.zone_data.values["population"].index.get_loc(u_label)
        if parameters.tour_purposes[purpose]["area"] == "peripheral":
            l_label = parameters.first_peripheral_zone
            l = self.zone_data.values["population"].index.get_loc(l_label)
            u = len(self.zone_data.values["population"])
        nr_zones = u - l
        b = parameters.trip_generation[purpose]
        trips = numpy.zeros(nr_zones)
        for i in b:
            trips += b[i] * self.zone_data.values[i][l:u]
        return trips

    def calc_mode_util(self, purpose, impedance):
        expsum = numpy.zeros_like(next(iter(impedance["car"].values())))
        for mode in parameters.mode_choice[purpose]:
            utility = numpy.zeros_like(next(iter(impedance[mode].values())))
            # TODO maybe add some utility
            self.mode_exps[mode] = numpy.exp(utility)
            b = parameters.mode_choice[purpose][mode]
            for i in b:
                self.mode_exps[mode] *= numpy.power(impedance[mode][i], b[i])
            expsum += self.mode_exps[mode]
        return expsum
    
    def calc_dest_util(self, purpose, mode, impedance):
        b = parameters.destination_choice[purpose][mode]["impedance"]
        utility = numpy.zeros_like(impedance["time"][mode])
        for i in b:
            utility += b[i] * impedance[i][mode]
        self.dest_exps[mode] = numpy.exp(utility)
        nr_zones = len(self.zone_data.values["workplaces"])
        attraction = numpy.zeros(nr_zones)
        b = parameters.destination_choice[purpose][mode]["attraction"]
        for i in b:
            attraction += b[i] * self.zone_data.values[i]
        self.dest_exps[mode] *= attraction
        return numpy.sum(self.dest_exps[mode], 1)

    def _mul(self, parameter, variable):
        result = numpy.zeros(len(variable[0]))
        for i in parameter:
            result += parameter[i] * variable[i]
        return result