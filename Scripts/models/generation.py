import numpy
import pandas
import parameters
import datahandling.resultdata as result


class GenerationModel:
    def __init__(self, purpose):
        self.zone_data = purpose.zone_data
        self.purpose = purpose
        self.param = parameters.tour_generation[purpose.name]

    def init_tours(self):
        self.tours = pandas.Series(0, self.purpose.zone_numbers)

    def add_tours(self, segment=None, age=None, is_car_user=None):
        """Add generated tours to vector.
        
        Parameters
        ----------
        segment : numpy 1-d array, optional
            Population segment for which tours are added
        age : string, optional
            Age group of population segment
        is_car_user : string, optional
            Whether population segment consists of car users or not
        """
        b = self.param
        try:
            for i in b:
                self.tours += b[i] * self.zone_data[i][self.purpose.bounds]
        except KeyError:
            self.tours += b[age][is_car_user] * segment

    def get_tours(self):
        """Get vector of tour numbers
        from zone data.
        
        Return
        ------
        numpy 1-d array
            Vector of tour numbers per zone
        """
        result.print_data(
            self.tours, "tours.txt", self.zone_data.zone_numbers, self.purpose.name)
        return self.tours.values


class NonHomeGeneration(GenerationModel):
    def add_tours(self, segment, age, is_car_user):
        pass
    
    def get_tours(self):
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
    def get_tours(self, mode):
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