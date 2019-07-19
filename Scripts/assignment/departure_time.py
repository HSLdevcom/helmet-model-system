import logging
import numpy
import os
from parameters import emme_scenario, demand_share, assignment_class, emme_mtx, first_external_zone

class DepartureTimeModel:
    def __init__(self, nr_zones):
        """Container for time period and assignment class specific demand.
        
        Parameters
        ----------
        nr_zones : int
            Number of zones in assignment model
        """
        self.nr_zones = nr_zones
        self.init_demand()
        self.logger = logging.getLogger()

    def init_demand(self):
        """Initialize demand for all time periods."""
        self.demand = dict.fromkeys(emme_scenario.keys())
        zeros = numpy.zeros((self.nr_zones, self.nr_zones))
        for time_period in self.demand:
            ass_classes = dict.fromkeys(emme_mtx["demand"].keys())
            self.demand[time_period] = ass_classes
            for ass_class in ass_classes:
                self.demand[time_period][ass_class] = zeros

    def add_demand(self, demand):
        """Add demand matrix for whole day.
        
        Parameters
        ----------
        demand : Demand or Tour
            Travel demand matrix or number of travellers
        """
        if demand.mode != "walk":
            if demand.mode == "car":
                ass_class = assignment_class[demand.purpose.name]
            else:
                ass_class = demand.mode
            if len(demand.position) == 2:
                for tp in emme_scenario:
                    share = demand_share[demand.purpose.name][demand.mode][tp]
                    self._add_2d_demand(share, ass_class, tp, demand.matrix, demand.position)
            elif len(demand.position) == 3:
                for tp in emme_scenario:
                    share = demand_share[demand.purpose.name][demand.mode][tp]
                    self._add_3d_demand(share, ass_class, tp, demand.matrix, demand.position)
            else:
                raise IndexError("Tuple mtx_pos has wrong dimensions.")
            self.logger.debug("Added demand for " + demand.purpose.name + ", " + demand.mode)

    def _add_2d_demand(self, demand_share, ass_class, time_period, mtx, mtx_pos):
        """Slice demand, include transpose and add for one time period."""
        r_0 = mtx_pos[0]
        c_0 = mtx_pos[1]
        try:
            r_n = r_0 + mtx.shape[0]
            c_n = c_0 + mtx.shape[1]
        except AttributeError:
            r_n = r_0 + 1
            c_n = c_0 + 1
            mtx = numpy.asarray([mtx])
        large_mtx = self.demand[time_period][ass_class]
        large_mtx[r_0:r_n, c_0:c_n] += demand_share[0] * mtx
        large_mtx[c_0:c_n, r_0:r_n] += demand_share[1] * mtx.T

    def _add_3d_demand(self, share, ass_class, time_period, mtx, mtx_pos):
        """Add three-way demand."""
        o = mtx_pos[0]
        d1 = mtx_pos[1]
        d2 = mtx_pos[2]
        try:
            rowsum = mtx.sum(1)[numpy.newaxis, :]
            colsum = mtx.sum(0)[:, numpy.newaxis]
        except AttributeError:
            rowsum = mtx
            colsum = mtx
        self._add_2d_demand(share[0], ass_class, time_period, rowsum, (o, d1))
        self._add_2d_demand(share[1], ass_class, time_period, mtx, (d1, d2))
        self._add_2d_demand(share[2], ass_class, time_period, colsum, (d2, o))
    
    def add_vans(self, time_period, nr_zones):
        """Add vans as a share of private car trips for one time period.
        
        Parameters
        ----------
        time_period : str
            Time period (aht/pt/iht)
        nr_zones : int
            Number of zones in model area (metropolitan + peripheral)
        """
        n = nr_zones
        car_demand = ( self.demand[time_period]["car_work"][0:n, 0:n]
                     + self.demand[time_period]["car_leisure"][0:n, 0:n])
        share = demand_share["freight"]["van"][time_period]
        self._add_2d_demand(share, "van", time_period, car_demand, (0, 0))
