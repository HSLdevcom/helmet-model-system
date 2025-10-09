from __future__ import annotations
from typing import TYPE_CHECKING
import numpy # type: ignore
import pandas
if TYPE_CHECKING:
    from datahandling.matrixdata import MatrixData
    from datahandling.zonedata import ZoneData

import parameters.tour_generation as param
from utils.freight import fratar, calibrate
from datatypes.demand import Demand
from datatypes.purpose import Purpose
from events.event_handler import EventHandler


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

    def __init__(self, 
                 zone_data_base: ZoneData, 
                 zone_data_forecast: ZoneData, 
                 base_demand: MatrixData,
                 event_handler: EventHandler = None):
        self.zdata_b = zone_data_base
        self.zdata_f = zone_data_forecast
        self.base_demand = base_demand
        self.event_handler = event_handler
        spec = {
            "name": "freight",
            "orig": None,
            "dest": None,
            "area": "all",
        }
        self.purpose = Purpose(spec, zone_data_base)

    def calc_freight_traffic(self, mode: str) -> Demand:
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
        production_base: numpy.ndarray = self._generate_trips(zone_data_base, mode)
        production_forecast: numpy.ndarray = self._generate_trips(zone_data_forecast, mode)
        zone_numbers = self.zdata_b.zone_numbers
        with self.base_demand.open("freight", "vrk", list(zone_numbers)) as mtx:
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
            sum1000 = mtx.loc[l:u].sum().to_numpy()
            scaling = 1 / max(sum1000.sum(), 1)
            # ave1 and ave2 are scaled down so the vector sum is 1
            ave1 = sum1000 * scaling
            ave2 = ave1[:, numpy.newaxis]
            cond1 = cond.loc[l:u].to_numpy()
            cond2 = cond1[:, numpy.newaxis]
            prod1 = prod.loc[l:u].to_numpy()
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
            demand = self._generate_garbage_trips(demand, zone_data_forecast)
        # Remove trailer truck traffic to/from (inner-city) prohibited zones
        if mode == "trailer_truck":
            demand[self.zdata_f.trailers_prohibited] = 0
            demand.loc[self.zdata_f.trailers_prohibited] = 0
        return Demand(self.purpose, mode, demand.values)
    
    def _generate_garbage_trips(self, demand: numpy.ndarray, zone_data_forecast) -> numpy.ndarray:
        g = param.garbage_generation
        # Calculate yearly garbage generation per zone (kg/year) separately
        yearly_garbage_population = g["population"] * zone_data_forecast["population"]
        yearly_garbage_services = g["service"] * zone_data_forecast["service"]
        yearly_garbage_shops= g["shops"] * zone_data_forecast["shops"]
        yearly_garbage_industry = g["industry"] * zone_data_forecast["industry"]
        yearly_garbage = yearly_garbage_population + yearly_garbage_services + yearly_garbage_shops + yearly_garbage_industry
        # Convert to daily truckloads (8000 kg/truck, 365 days/year)
        daily_truckloads = yearly_garbage / 365 / 8000

        # Use actual zone numbers from demand DataFrame index
        zone_numbers = demand.index

        # Build garbage matrix
        garbage_zones = self.zdata_f.garbage_destination
        garbage_matrix = pandas.DataFrame(0.0, index=zone_numbers, columns=zone_numbers)

        # Add garbage trips to/from garbage zones
        garbage_matrix.loc[:, garbage_zones] = daily_truckloads.loc[zone_numbers].values[:, None] / len(garbage_zones)
        garbage_matrix.loc[garbage_zones, :] += daily_truckloads.loc[zone_numbers].values[None, :] / len(garbage_zones)

        demand += garbage_matrix

        garbage_array = pandas.DataFrame({
            "population_garbage": yearly_garbage_population.loc[zone_numbers],
            "services_garbage": yearly_garbage_services.loc[zone_numbers],
            "shops_garbage": yearly_garbage_shops.loc[zone_numbers],
            "industry_garbage": yearly_garbage_industry.loc[zone_numbers],
            "total_garbage": yearly_garbage.loc[zone_numbers]
        }, index=zone_numbers)
        if self.event_handler is not None:
            self.event_handler.on_garbage_trips_generated(garbage_array)

        return demand

    def _generate_trips(self, 
                        zone_data: pandas.DataFrame, 
                        mode: str) -> numpy.ndarray:
        b = pandas.Series(param.tour_generation[mode])
        return (b * zone_data).sum(1) + 0.001
