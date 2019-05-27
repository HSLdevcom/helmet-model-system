import numpy
import parameters

class DemandHS15:
    def __init__(self, zone_data):
        self.zone_data = zone_data
        self.probability = {}

    def calc_demand(self, purpose, impedance):
        logsum = {}
        for mode in parameters.tour_modes:
            logsum[mode] = self.calc_destination_util(purpose, mode, impedance)
        mtx = numpy.arange(6).reshape(2, 3)
        demand = {
            "car": mtx,
            "transit": mtx,
            "bike": mtx,
        }
        return demand

    def calc_destination_util(self, purpose, mode, impedance):
        nr_zones = len(impedance["time"][mode])
        b = parameters.destination_choice[purpose][mode]["impedance"]
        utility = numpy.zeros((nr_zones, nr_zones))
        for i in b:
            utility += b[i] * impedance[i][mode]
        exps = numpy.exp(utility)
        attraction = numpy.zeros(nr_zones)
        b = parameters.destination_choice[purpose][mode]["attraction"]
        for i in b:
            attraction += b[i] * self.zone_data.values[i]
        # TODO Check that this is the right direction
        exps *= attraction
        logsum = numpy.sum(exps)
        self.probability[mode] = exps / logsum
        return logsum
