import numpy
import parameters

class DemandHS15:
    def __init__(self, zone_data):
        self.zone_data = zone_data
        self.dest_exps = {}
        self.mode_exps = {}
        self.dest_expsum = {}

    def calc_demand(self, purpose, impedance):
        trips = self.generate_trips(purpose)
        expsum = self.calc_mode_util(purpose, impedance)
        demand = {}
        for mode in parameters.tour_modes:
            mode_probability = self.mode_exps[mode] / expsum
            destination_probability = self.dest_exps[mode] / self.dest_expsum[mode]
            demand[mode] = mode_probability * destination_probability * trips
        return demand

    def generate_trips(self, purpose):
        nr_zones = len(self.zone_data.values["population"])
        b = parameters.trip_generation[purpose]
        trips = numpy.zeros(nr_zones)
        for i in b:
            trips += b[i] * self.zone_data.values[i]
        return trips

    def calc_mode_util(self, purpose, impedance):
        nr_zones = len(impedance["time"]["car"])
        b = parameters.mode_choice
        expsum = numpy.zeros(nr_zones)
        for mode in parameters.tour_modes:
            self.calc_destination_util(purpose, mode, impedance)
            self.mode_exps[mode] = b[mode] * self.dest_expsum[mode]
            expsum += self.mode_exps[mode]
        return expsum
    
    def calc_destination_util(self, purpose, mode, impedance):
        nr_zones = len(impedance["time"][mode])
        b = parameters.destination_choice[purpose][mode]["impedance"]
        utility = numpy.zeros((nr_zones, nr_zones))
        for i in b:
            utility += b[i] * impedance[i][mode]
        self.dest_exps[mode] = numpy.exp(utility)
        attraction = numpy.zeros(nr_zones)
        b = parameters.destination_choice[purpose][mode]["attraction"]
        for i in b:
            attraction += b[i] * self.zone_data.values[i]
        # TODO Check that this is the right direction
        self.dest_exps[mode] *= attraction
        self.dest_expsum[mode] = numpy.sum(self.dest_exps[mode], 1)

    def _mul(self, parameter, variable):
        result = numpy.zeros(len(variable[0]))
        for i in parameter:
            result += parameter[i] * variable[i]
        return result