import numpy
import parameters

class GenerationModel:
    def __init__(self, zone_data, purpose):
        self.zone_data = zone_data
        self.purpose = purpose
        self.param = parameters.tour_generation[purpose.name]

    def generate_tours(self):
        l, u = self.purpose.bounds
        nr_zones = u - l
        tours = numpy.zeros(nr_zones)
        b = self.param
        for i in b:
            tours += b[i] * self.zone_data.values[i][l:u]
        return tours


class NonHomeGeneration(GenerationModel):
    def generate_tours(self):
        tours = numpy.zeros(self.zone_data.nr_zones)
        for source in self.purpose.sources:
            b = self.param[source.name]
            for mode in source.attracted_tours:
                tours += b * source.attracted_tours[mode]
        return tours


class SecDestGeneration(GenerationModel):
    def generate_tours(self, mode):
        l, u = self.purpose.bounds
        nr_zones = u - l
        tours = numpy.zeros((nr_zones, self.zone_data.nr_zones))
        b = self.param
        for source in self.purpose.sources:
            tours += b[source.name] * source.demand[mode]
        return tours