import pandas

import parameters.tour_generation as param


class GenerationModel:
    """Container for tour vector.

    Regular tours are created in `model.logit.TourCombinationModel`
    and then added to the `tours` vector for each `TourPurpose`.
    Peripheral tours are calculated directly in `add_tours()`.

    Parameters
    ----------
    purpose : datatypes.purpose.TourPurpose
        Travel purpose (hw/hs/ho/...)
    resultdata : ResultData
        Writer object for result directory
    """

    def __init__(self, purpose, resultdata):
        self.resultdata = resultdata
        self.zone_data = purpose.zone_data
        self.purpose = purpose
        self.param = param.tour_generation[purpose.name]

    def init_tours(self):
        """Initialize `tours` vector to 0."""
        self.tours = pandas.Series(0, self.purpose.zone_numbers)

    def add_tours(self):
        """Generate and add (peripheral) tours to zone vector."""
        b = self.param
        for i in b:
            self.tours += b[i] * self.zone_data[i][self.purpose.bounds]

    def get_tours(self):
        """Get vector of tour numbers per zone.
        
        Return
        ------
        numpy.ndarray
            Vector of tour numbers per zone
        """
        self.resultdata.print_data(
            self.tours, "tours.txt", self.zone_data.zone_numbers,
            self.purpose.name)
        return self.tours.values


class NonHomeGeneration(GenerationModel):
    """For calculating numbers of non-home tours starting in each zone.

    Parameters
    ----------
    purpose : datatypes.purpose.TourPurpose
        Travel purpose (hw/hs/ho/...)
    resultdata : ResultData
        Writer object for result directory
    """

    def add_tours(self):
        pass
    
    def get_tours(self):
        """Generate vector of tour numbers from attracted source tours.

        Assumes that home-based tours have been assigned destinations.
        
        Return
        ------
        numpy.ndarray
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
    """For calculating numbers of secondary-destination tours.

    Calculation is for each mode and origin-destination pair separately.

    Parameters
    ----------
    purpose : datatypes.purpose.TourPurpose
        Travel purpose (hw/hs/ho/...)
    resultdata : ResultData
        Writer object for result directory
    """

    def init_tours(self):
        self.tours = dict.fromkeys(self.purpose.modes)
        for mode in self.tours:
            self.tours[mode] = 0
    
    def add_tours(self, demand, mode, purpose):
        """Generate matrix of tour numbers from attracted source tours."""
        if mode in self.purpose.modes:
            bounds = self.purpose.bounds
            metropolitan = next(iter(self.purpose.sources)).bounds
            b = self.param
            self.tours[mode] += b[purpose.name][mode] * demand[metropolitan, bounds]
    
    def get_tours(self, mode):
        """Get vector of tour numbers per od pair.
        
        Return
        ------
        numpy.ndarray
            Matrix of tour numbers per origin-destination pair
        """
        return self.tours[mode]
