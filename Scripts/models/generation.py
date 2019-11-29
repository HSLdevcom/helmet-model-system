import numpy
import pandas
import parameters
import datahandling.resultdata as result


class GenerationModel:
    def __init__(self, purpose):
        self.zone_data = purpose.zone_data
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
        result.print_data(
            tours, "tours.txt", self.zone_data.zone_numbers, self.purpose.name)
        return tours.values


class Tours(GenerationModel):
    def __init__(self, purpose):
        self.zone_data = purpose.zone_data
        self.purpose = purpose
        self.tours = 0
    
    def generate_tours(self):
        result.print_data(
            pandas.Series(self.tours, self.purpose.zone_numbers),
            "tours.txt", self.zone_data.zone_numbers, self.purpose.name)
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
        result.print_data(
            pandas.Series(tours, self.purpose.zone_numbers),
            "tours.txt", self.zone_data.zone_numbers, self.purpose.name)
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
        tours = 0
        bounds = self.purpose.bounds
        metropolitan = next(iter(self.purpose.sources)).bounds
        b = self.param
        for source in self.purpose.sources:
            tours += b[source.name] * source.demand[mode][metropolitan, bounds]
        return tours