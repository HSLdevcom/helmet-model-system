import numpy
import pandas

import parameters.tour_generation as param
from utils.freight import fratar, calibrate
from datatypes.demand import Demand
from datatypes.purpose import Purpose


class FreightModel:
    """Freight traffic model.

    Parameters
    ----------
    zone_data_base : datahandling.zonedata.ZoneData
        Zone data for base year
    zone_data_forecast : datahandling.zonedata.ZoneData
        Zone data for forecast year
    base_demand : datahandling.matrixdata.MatrixData
        Base demand matrices
    """

    def __init__(self, zone_data_base, zone_data_forecast, base_demand):
        self.zdata_b = zone_data_base
        self.zdata_f = zone_data_forecast
        self.base_demand = base_demand
        spec = {
            "name": "freight",
            "orig": None,
            "dest": None,
            "area": "all",
        }
        self.purpose = Purpose(spec, zone_data_base)

    def calc_freight_traffic(self, mode):
        """Calculate freight traffic matrix.

        Parameters
        ----------
        mode : str
            Freight mode (truck/trailer_truck)

        Return
        ------
        datatypes.demand.Demand
            Freight mode demand matrix for whole day
        """
        zone_data_base = self.zdata_b.get_freight_data()
        zone_data_forecast = self.zdata_f.get_freight_data()
        production_base = self._generate_trips(zone_data_base, mode)
        production_forecast = self._generate_trips(zone_data_forecast, mode)
        zone_numbers = self.zdata_b.zone_numbers
        with self.base_demand.open("freight", "vrk", zone_numbers) as mtx:
            # Remove zero values
            base_mtx = mtx[mode].clip(0.000001, None)
        production = calibrate(
            base_mtx.sum(1), production_base, production_forecast)
        mtx = pandas.DataFrame(base_mtx, zone_numbers, zone_numbers)
        prod = pandas.Series(production, zone_numbers)

        # If forecast>5*base, destination choice is replaced by area average
        # For simplicity, areas are zone numbers in the same thousand
        threshold = param.vector_calibration_threshold
        cond = production_forecast < threshold*production_base
        last1000 = zone_numbers[-1] // 1000
        for i in range(0, last1000):
            l = i * 1000
            u = l + 999
            # sum1000 is a vector with the same length as one side of mtx,
            # where production for the whole thousand is summed
            sum1000 = mtx.loc[l:u].sum().values
            scaling = 1 / max(sum1000.sum(), 1)
            # ave1 and ave2 are scaled down so the vector sum is 1
            ave1 = sum1000 * scaling
            ave2 = ave1[:, numpy.newaxis]
            cond1 = cond.loc[l:u]
            cond2 = cond1[:, numpy.newaxis]
            prod1 = prod.loc[l:u].values
            prod2 = prod1[:, numpy.newaxis]
            # Where condition is not met, mtx rows and cols are replaced by
            # destination choice vector ave1/ave2 multiplied by production
            # factor for that zone
            mtx.loc[l:u] = numpy.where(cond2, mtx.loc[l:u], ave1*prod2)
            mtx.loc[:, l:u] = numpy.where(cond1, mtx.loc[:, l:u], ave2*prod1)

        # Matrix balancing
        demand = fratar(production, mtx)
        # Add garbage transport to/from garbage zone
        if mode == "truck":
            b = param.garbage_generation
            garbage = ( b["population"] * zone_data_forecast["population"] 
                      + b["workplaces"] * zone_data_forecast["workplaces"])
            demand[self.zdata_f.garbage_destination] += garbage
            demand.loc[self.zdata_f.garbage_destination] += garbage
        # Remove trailer truck traffic to/from (inner-city) prohibited zones
        if mode == "trailer_truck":
            demand[self.zdata_f.trailers_prohibited] = 0
            demand.loc[self.zdata_f.trailers_prohibited] = 0
        return Demand(self.purpose, mode, demand.values)

    def _generate_trips(self, zone_data, mode):
        b = pandas.Series(param.tour_generation[mode])
        return (b * zone_data).sum(1) + 0.001
