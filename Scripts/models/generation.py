import numpy
import parameters

class GenerationModel:
    def __init__(self, zone_data, purpose):
        self.zone_data = zone_data
        self.purpose = purpose
        self.param = parameters.tour_generation[purpose.name]

    def generate_tours(self):
        """Generate vector of tour numbers
        from zone data.
        
        Return
        ------
        numpy 1-d array
            Vector of tour numbers per zone
        """
        l, u = self.purpose.bounds
        nr_zones = u - l
        tours = numpy.zeros(nr_zones)
        b = self.param
        for i in b:
            tours += b[i] * self.zone_data[i][l:u]
        return tours


class NonHomeGeneration(GenerationModel):
    def generate_tours(self):
        """Generate vector of tour numbers
        from attracted source tours.
        
        Return
        ------
        numpy 1-d array
            Vector of tour numbers per zone
        """
        tours = numpy.zeros(self.zone_data.nr_zones)
        for source in self.purpose.sources:
            b = self.param[source.name]
            for mode in source.attracted_tours:
                tours += b * source.attracted_tours[mode]
        return tours


class SecDestGeneration(GenerationModel):
    def generate_tours(self, mode):
        """Generate matrix of tour numbers
        from attracted source tours.
        
        Return
        ------
        numpy 2-d matrix
            Matrix of tour numbers per origin-destination pair
        """
        tours = numpy.zeros_like(next(iter(self.purpose.sources)).demand[mode])
        b = self.param
        for source in self.purpose.sources:
            tours += b[source.name] * source.demand[mode]
        return tours