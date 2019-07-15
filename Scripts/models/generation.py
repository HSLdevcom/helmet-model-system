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
        b = self.param
        tours = numpy.zeros(nr_zones)
        for i in b:
            tours += b[i] * self.zone_data.values[i][l:u]
        return tours


class NonHomeGeneration(GenerationModel):
    def generate_tours(self):
        nr_zones = len(self.zone_data.zone_numbers)
        tours = numpy.zeros(nr_zones)
        for source in self.purpose.sources:
            b = self.param[source.name]
            for mode in source.attracted_tours:
                source_tours = source.attracted_tours[mode]
                tours += b * source_tours
        return tours