import pandas

import parameters.tour_generation as param
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from datatypes.purpose import Purpose, TourPurpose
    from datahandling.zonedata import ZoneData
    from datahandling.resultdata import ResultsData


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

    def __init__(self, purpose: Purpose, resultdata: ResultsData):
        self.resultdata = resultdata
        self.zone_data = purpose.zone_data
        self.purpose = purpose
        self.param: dict[str,float] | dict[str, dict[str, float]] = param.tour_generation[purpose.name]

    def init_tours(self):
        """Initialize `tours` vector to 0."""
        self.tours = pandas.Series(0.0, self.purpose.zone_numbers)

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
    
    def add_tours(self, demand, mode: str, purpose: TourPurpose):
        """Generate matrix of tour numbers from attracted source tours."""
        if mode in self.purpose.modes:
            bounds = self.purpose.bounds
            metropolitan = next(iter(self.purpose.sources)).bounds
            b = self.param
            self.tours[mode] += b[purpose.name][mode] * demand[metropolitan, bounds]
    
    def get_tours(self, mode: str):
        """Get vector of tour numbers per od pair.
        
        Return
        ------
        numpy.ndarray
            Matrix of tour numbers per origin-destination pair
        """
        return self.tours[mode]
