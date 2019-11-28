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
        tours = 0
        b = self.param
        for i in b:
            tours += b[i] * self.zone_data[i][self.purpose.bounds]
        return tours.values


class Tours(GenerationModel):
    def __init__(self, zone_data, purpose):
        self.zone_data = zone_data
        self.purpose = purpose
        self.tours = 0
    
    def generate_tours(self):
        return self.tours


class NonHomeGeneration(GenerationModel):
    def generate_tours(self):
        """Generate vector of tour numbers
        from attracted source tours.
        
        Return
        ------
        numpy 1-d array
            Vector of tour numbers per zone
        """
        tours = 0
        for source in self.purpose.sources:
            b = self.param[source.name]
            for mode in source.attracted_tours:
                tours += b * source.attracted_tours[mode]
        return tours


class SecDestGeneration(GenerationModel):
    def init_tours(self):
        self.tours = dict.fromkeys(self.purpose.modes)
        for mode in self.tours:
            self.tours[mode] = 0
    
    def add_tours(self, demand, mode, purpose):
        if mode in self.purpose.modes:
            bounds = self.purpose.bounds
            metropolitan = next(iter(self.purpose.sources)).bounds
            b = self.param
            self.tours[mode] += b[purpose.name] * demand[metropolitan, bounds]
    
    def generate_tours(self, mode):
        """Generate matrix of tour numbers
        from attracted source tours.
        
        Return
        ------
        numpy 2-d matrix
            Matrix of tour numbers per origin-destination pair
        """
        return self.tours[mode]