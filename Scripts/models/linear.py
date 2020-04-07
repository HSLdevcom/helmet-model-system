import numpy
import pandas
import math
import parameters


class LinearModel(object):
    def __init__(self, zone_data_base, zone_data_forecast, bounds, resultdata):
        """Initialize a linear model.

        Parameters
        ----------
        zone_data : ZoneData
            A ZoneData object defining the input data of zones.
        bounds : slice
            Defines the area on which the model is predicting to (usually the
            metropolitan area).
        """        
        self.zone_data = zone_data_forecast
        self.zone_data_base = zone_data_base
        self.bounds = bounds
        self.resultdata = resultdata

    def _add_constant(self, prediction, b):
        try: # If only one parameter
            prediction += b
        except ValueError: # Separate params for cap region and surrounding
            k = self.zone_data.first_surrounding_zone
            prediction[:k] += b[0]
            prediction[k:] += b[1]
        return prediction

    def _add_zone_terms(self, prediction, b, generation=False):
        zdata = self.zone_data
        for i in b:
            try: # If only one parameter
                prediction += b[i] * zdata.get_data(i, self.bounds, generation)
            except ValueError: # Separate params for cap region and surrounding
                k = self.zone_data.first_surrounding_zone
                data_capital_region = zdata.get_data(
                    i, self.bounds, generation, zdata.CAPITAL_REGION)
                data_surrounding = zdata.get_data(
                    i, self.bounds, generation, zdata.SURROUNDING_AREA)
                prediction[:k] += b[i][0] * data_capital_region
                prediction[k:] += b[i][1] * data_surrounding
        return prediction

    def _add_log_zone_terms(self, prediction, b, generation=False):
        zdata = self.zone_data
        for i in b:
            prediction += b[i] * numpy.log(zdata.get_data(i, self.bounds,
                generation))
        return prediction


class CarDensityModel(LinearModel):
    def predict(self):
        """Get car ownership prediction for zones.
        
        Return
        ------
        pandas Series
            Zone vector of cars per inhabitant
        """
        b = parameters.car_density
        prediction = numpy.zeros(self.bounds.stop)
        self._add_constant(prediction, b["constant"])
        self._add_zone_terms(prediction, b["generation"], True)
        self._add_log_zone_terms(prediction, b["log"], True)
        # Car density cannot be negative
        prediction = prediction.clip(0.0, None)
        base_pop = self.zone_data_base["population"]
        forecast_pop = self.zone_data["population"]
        # Car ownership model is applied only for population growth
        pop_growth = (forecast_pop - base_pop).clip(0, None)
        # Share of population that is growth
        # (set to zero if population is zero)
        pop_growth_share = numpy.divide(
            pop_growth, forecast_pop, out=numpy.zeros_like(pop_growth),
            where=forecast_pop!=0)
        base_car_density = self.zone_data_base["car_density"]
        prediction = (pop_growth_share * prediction
                      + (1-pop_growth_share) * base_car_density)
        self.print_results(prediction)
        return prediction

    def print_results(self, prediction):
        """ Print results, mainly for calibration purposes"""
        population = self.zone_data["population"]
        population_7_99 = ( population[:self.zone_data.first_peripheral_zone]
                          * self.zone_data["share_age_7-99"])
        car_density = prediction
                
        # Print car density by zone
        self.resultdata.print_data(
            prediction, "car_density.txt",
            self.zone_data.zone_numbers[self.bounds], "car_density")
        
        # print car density by municipality
        prediction_municipality = []
        for municipality in parameters.municipality:
            i = slice(parameters.municipality[municipality][0],
                      parameters.municipality[municipality][1])
            # comparison data has car user shares of population
            # over 6 years old (from HEHA)
            prediction_municipality.append( car_density.loc[i].sum() 
                                    / population_7_99.loc[i].sum())
        self.resultdata.print_data(
            prediction_municipality, "car_density_per_municipality.txt",
            parameters.municipality.keys(), "car_density")
                          
        # print car density by area (to get Helsinki CBD vs. Helsinki other)
        prediction_area = []
        for area in parameters.areas:
            i = slice(parameters.areas[area][0],
                      parameters.areas[area][1])
            # comparison data has car user shares of population
            # over 6 years old (from HEHA)
            prediction_area.append( car_density.loc[i].sum()
                            / population_7_99.loc[i].sum())
        self.resultdata.print_data(
            prediction_area, "car_density_per_area.txt",
            parameters.areas.keys(), "car_density")
