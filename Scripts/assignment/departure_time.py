from __future__ import annotations
from typing import Any, Callable, Dict, List, Optional, Tuple, Union, cast
import numpy # type: ignore
from datatypes.demand import Demand
from datatypes.tour import Tour

from transform.park_and_ride_transformer import ParkAndRideTransformer
import utils.log as log
import parameters.departure_time as param
from parameters.assignment import transport_classes, assignment_classes


class DepartureTimeModel:
    """Container for time period and assignment class specific demand.

    Parameters
    ----------
    nr_zones : int
        Number of zones in assignment model
    time_periods : list of str (optional)
        Time period names, default is aht, pt, iht
    """
    def __init__(self, 
                 nr_zones: int, 
                 time_periods: List[str]=list(param.backup_demand_share)):
        self.nr_zones = nr_zones
        self.time_periods = time_periods
        self.demand: Optional[Union[int,Dict[str,Dict[str,numpy.ndarray]]]] = None
        self.old_car_demand: Union[int,numpy.ndarray] = 0
        self.init_demand()

    def init_demand(self) -> Dict[str,float]:
        """Initialize/reset demand for all time periods.

        Includes all transport classes, each being set to zero.
        The function also calculates two demand convergence indicators,
        comparing car work demand matrix from previous round to current one.

        Returns
        -------
        dict
            rel_gap : float
                Mean relative gap for car work demand ((new-old)/old)
            max_gap : float
                Maximum gap for OD pair in car work demand matrix
        """
        # Calculate gaps
        try:
            self.demand = cast(Dict[str,Dict[str,numpy.ndarray]], self.demand) #type checker hint
            car_demand = self.demand[self.time_periods[0]]["car_work"]
        except TypeError:
            car_demand = 0
        max_gap = numpy.abs(car_demand - self.old_car_demand).max()
        try:
            self.old_car_demand = cast(numpy.ndarray, self.old_car_demand) #type checker hint
            old_sum = self.old_car_demand.sum()
            relative_gap = abs((car_demand.sum()-old_sum) / old_sum)
        except AttributeError:
            relative_gap = 0
        self.old_car_demand = car_demand

        # Init demand
        n = self.nr_zones
        self.demand = {tp: {tc: numpy.zeros((n, n), numpy.float32)
                for tc in transport_classes}
            for tp in self.time_periods}

        return {"rel_gap": relative_gap, "max_gap": max_gap}

    def split_park_and_ride(self, demand: Union[Demand, Tour], park_and_ride_impedance:Dict[str, numpy.ndarray]):
        position2 = cast(Tuple[int,int], demand.position) #type checker hint
        share: Dict[str, Any] = param.demand_share[demand.purpose.name][demand.mode]
        used_facility = park_and_ride_impedance["used_facility"]

        car_matrix = numpy.zeros_like(demand.matrix)
        transit_matrix = numpy.zeros_like(demand.matrix)

        #move car journeys to park and ride facilities
        for i in range(demand.matrix.shape[0]): #TODO: handle the zone spaces correctly
            for j in range(demand.matrix.shape[1]):
                target_cell = used_facility[i, j]
                car_matrix[i, target_cell] += demand.matrix[i, j] #for cars Park and ride is target only
                transit_matrix[target_cell, j] += demand.matrix[i,j] #for transit Park and ride is source only


        for time_period in self.time_periods:
            self._add_2d_demand(
                share[time_period], "car_work", time_period,
                car_matrix, position2)
            self._add_2d_demand(
                share[time_period], "transit_work", time_period,
                transit_matrix, position2)

    def add_demand(self, demand: Union[Demand, Tour]):
        """Add demand matrix for whole day.
        
        Parameters
        ----------
        demand : Demand or Tour
            Travel demand matrix or number of travellers
        """
        demand.purpose.name = cast(str,demand.purpose.name) #type checker hint

        if demand.mode != "walk" and demand.mode != "park_and_ride" and not demand.is_car_passenger:
            if demand.mode in param.divided_classes:
                ass_class = "{}_{}".format(
                    demand.mode, assignment_classes[demand.purpose.name])
            else:
                ass_class = demand.mode
            if len(demand.position) == 2:
                position2 = cast(Tuple[int,int], demand.position) #type checker hint
                share: Dict[str, Any] = param.demand_share[demand.purpose.name][demand.mode]
                for time_period in self.time_periods:
                    self._add_2d_demand(
                        share[time_period], ass_class, time_period,
                        demand.matrix, position2)
            elif len(demand.position) == 3:
                for time_period in self.time_periods:
                    self._add_3d_demand(demand, ass_class, time_period)
            else:
                raise IndexError("Tuple position has wrong dimensions.")

    def _add_2d_demand(self, 
                       demand_share: Any, 
                       ass_class: str, 
                       time_period: str, 
                       mtx: numpy.ndarray, 
                       mtx_pos: Tuple[int, int]):
        """Slice demand, include transpose and add for one time period. ???types"""
        r_0 = mtx_pos[0]
        c_0 = mtx_pos[1]
        r_n = r_0 + mtx.shape[0]
        c_n = c_0 + mtx.shape[1]
        self.demand = cast(Dict[str, Dict[str, Any]], self.demand) #type checker help
        large_mtx = self.demand[time_period][ass_class]
        try:
            large_mtx[r_0:r_n, c_0:c_n] += demand_share[0] * mtx
            large_mtx[c_0:c_n, r_0:r_n] += demand_share[1] * mtx.T
        except ValueError:
            share = param.backup_demand_share[time_period]
            large_mtx[r_0:r_n, c_0:c_n] += share[0] * mtx
            large_mtx[c_0:c_n, r_0:r_n] += share[1] * mtx.T
            log.warn("{} {} matrix not matching {} demand shares. Resorted to backup demand shares.".format(
                mtx.shape, ass_class, len(demand_share[0])))

    def _add_3d_demand(self, 
                       demand: Union[Demand, Tour], 
                       ass_class: str, 
                       time_period: str):
        """Add three-way demand."""
        demand_position = cast(Tuple[int,int,int],demand.position) #type checker hint
        demand.purpose.name = cast(str,demand.purpose.name) #type checker hint
        mtx = demand.matrix
        tp = time_period
        o = demand_position[0]
        d1 = demand_position[1]
        d2 = demand_position[2]
        share = param.demand_share[demand.purpose.name][demand.mode][tp]
        if demand.dest is not None:
            # For agent simulation
            self._add_2d_demand(share, ass_class, tp, mtx, (o, d1))
            sec_purpose_name = demand.purpose.sec_dest_purpose.name
            share = param.demand_share[sec_purpose_name][demand.mode][tp]
        colsum = mtx.sum(0)[:, numpy.newaxis]
        self._add_2d_demand(share[0], ass_class, tp, mtx, (d1, d2))
        self._add_2d_demand(share[1], ass_class, tp, colsum, (d2, o))
    
    def add_vans(self, time_period: str, nr_zones: int):
        """Add vans as a share of private car trips for one time period.
        
        Parameters
        ----------
        time_period : str
            Time period (aht/pt/iht)
        nr_zones : int
            Number of zones in model area (metropolitan + peripheral)
        """
        demand = cast(Dict[str, Dict[str, numpy.ndarray]],self.demand)
        n = nr_zones
        mtx = demand[time_period]
        car_demand = (mtx["car_work"][0:n, 0:n] + mtx["car_leisure"][0:n, 0:n])
        share = param.demand_share["freight"]["van"][time_period]
        self._add_2d_demand(share, "van", time_period, car_demand, (0, 0))
        mtx["van"][0:n, 0:n] += mtx["truck"][0:n, 0:n]
