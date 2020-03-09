import pandas
import parameters


class GenerationModel:
    def __init__(self, purpose, resultdata):
        self.resultdata = resultdata
        self.zone_data = purpose.zone_data
        self.purpose = purpose
        self.param = parameters.tour_generation[purpose.name]

    def init_tours(self):
        self.tours = pandas.Series(0, self.purpose.zone_numbers)

    def add_tours(self):
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
        for i in b:
            self.tours += b[i] * self.zone_data[i][self.purpose.bounds]

    def get_tours(self):
        """Get vector of tour numbers
        from zone data.
        
        Return
        ------
        numpy 1-d array
            Vector of tour numbers per zone
        """
        self.resultdata.print_data(self.tours, "tours.txt", self.zone_data.zone_numbers, self.purpose.name)
        return self.tours.values


class NonHomeGeneration(GenerationModel):
    def add_tours(self):
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
        self.resultdata.print_data(
            pandas.Series(tours, self.purpose.zone_numbers),
            "tours.txt",
            self.zone_data.zone_numbers,
            self.purpose.name
        )
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
            self.tours[mode] += b[purpose.name][mode] * demand[metropolitan, bounds]
    
    def get_tours(self, mode):
        """Generate matrix of tour numbers
        from attracted source tours.
        
        Return
        ------
        numpy 2-d matrix
            Matrix of tour numbers per origin-destination pair
        """
        return self.tours[mode]
