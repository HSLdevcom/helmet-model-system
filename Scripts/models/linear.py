import numpy # type: ignore
import pandas
import math

import parameters.car
import parameters.income
from utils.zone_interval import ZoneIntervals
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from datatypes.purpose import Purpose, TourPurpose
    from datahandling.zonedata import ZoneData
    from datahandling.resultdata import ResultsData



class LinearModel(object):
    """Initialize a linear model.

    Parameters
    ----------
    zone_data : datahandling.ZoneData
        Object defining the input data of zones
    bounds : slice
        Defines the area on which the model is predicting to (usually the
        metropolitan area)
    resultdata : datahandling.ResultData
        Writer object for result directory
    """
    def __init__(self, zone_data: ZoneData, bounds: slice, resultdata: ResultsData):
        self.zone_data = zone_data
        self.bounds = bounds
        self.resultdata = resultdata

    def _add_zone_terms(self, prediction: pandas.Series, b: dict, generation=False):
        zdata = self.zone_data
        for i in b:
            prediction += b[i] * zdata.get_data(i, self.bounds, generation)
        return prediction

    def _add_log_zone_terms(self, prediction: pandas.Series, b: dict, generation=False):
        zdata = self.zone_data
        for i in b:
            prediction += b[i] * numpy.log(zdata.get_data(
                i, self.bounds, generation))
        return prediction


class CarDensityModel(LinearModel):
    """Initialize a car density model.

    Population growth and share of new dwellings that are detached houses
    are calculated once, to be used later in predictions.

    Parameters
    ----------
    zone_data_base : datahandling.ZoneData
        Zone input data for base year
    zone_data_forecast : datahandling.ZoneData
        Zone input data for forecast year
    bounds : slice
        Defines the area on which the model is predicting to (usually the
        metropolitan area)
    resultdata : datahandling.ResultData
        Writer object for result directory
    """
    def __init__(self, zone_data_base: ZoneData, zone_data_forecast: ZoneData, bounds: slice, resultdata: ResultsData):
        LinearModel.__init__(self, zone_data_forecast, bounds, resultdata)
        self.zone_data_base = zone_data_base
        base_pop = self.zone_data_base["population"][bounds]
        forecast_pop = self.zone_data["population"][bounds]
        # Car ownership model is applied only for population growth
        pop_growth = (forecast_pop - base_pop).clip(0, None)
        # Share of population that is growth
        # (set to zero if population is zero)
        self.pop_growth_share = numpy.divide(
            pop_growth, forecast_pop, out=numpy.zeros_like(pop_growth),
            where=forecast_pop!=0)
        # Share of new dwellings that are detached houses is calculated
        # from difference in shares in base and forecast data
        forecast_sh_detached = self.zone_data["share_detached_houses"][bounds]
        base_sh_detached = self.zone_data_base["share_detached_houses"][bounds]
        detached_houses_diff = (forecast_sh_detached*forecast_pop 
                                - base_sh_detached*base_pop)
        share_detached_new = numpy.divide(
            detached_houses_diff, pop_growth,
            out=numpy.array(forecast_sh_detached), where=pop_growth!=0)
        self.zone_data._values["share_detached_houses_new"] = pandas.Series(
            share_detached_new, self.zone_data.zone_numbers[self.bounds])
    
    def predict(self):
        """Get car ownership prediction for zones.
        
        Return
        ------
        pandas.Series
            Zone vector of cars per inhabitant
        """
        b = parameters.car.car_density
        prediction = pandas.Series(
            b["constant"], self.zone_data.zone_numbers[self.bounds])
        prediction = self._add_zone_terms(prediction, b["generation"], True)
        prediction = self._add_log_zone_terms(prediction, b["log"], True)
        # Car density cannot be negative
        prediction = prediction.clip(0.0, None)
        try:
            # Take parking norms as given and replace model results
            # for these zones
            parking_norm = self.zone_data["parking_norm"]
            prediction[parking_norm.index] = parking_norm
        except AttributeError:
            # If no parking norms are given
            pass
        base_car_density = (self.zone_data_base["car_density"][self.bounds]
                            .clip(upper=1.0))
        prediction = (self.pop_growth_share * prediction
                      + (1-self.pop_growth_share) * base_car_density)
        return prediction


class IncomeModel(LinearModel):
    """Initialize income model.

    Parameters
    ----------
    zone_data : datahandling.ZoneData
        Zone input data for forecast year
    bounds : slice
        Defines the area on which the model is predicting to (usually the
        metropolitan area)
    resultdata : datahandling.ResultData
        Writer object for result directory
    age_groups : tuple
        tuple
            int
                Age intervals for validation
    is_helsinki : bool (optional)
        If model is for the municipality of Helsinki
    """
    def __init__(self, zone_data: ZoneData, bounds: slice, resultdata: ResultsData, age_groups: tuple[int, int],
                 is_helsinki=False):
        LinearModel.__init__(self, zone_data, bounds, resultdata)
        self.param = (parameters.income.log_income_helsinki if is_helsinki
            else parameters.income.log_income)
        for age_group in self.param["age_dummies"]:
            age_interval = age_group.split('_')[1]
            if tuple(map(int, age_interval.split('-'))) not in age_groups:
                raise AttributeError("Income dummy {} not valid.".format(
                    age_group))

    def predict(self):
        prediction = pandas.Series(
            self.param["constant"], self.zone_data.zone_numbers[self.bounds])
        prediction = self._add_zone_terms(prediction, self.param["zone"], True)
        for municipality in self.param["municipality_dummies"]:
            dummy = self.zone_data.dummy(
                "municipalities", municipality, self.bounds)
            prediction += self.param["municipality_dummies"][municipality] * dummy
        self.log_income = prediction
