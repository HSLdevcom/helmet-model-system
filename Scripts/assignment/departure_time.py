import logging
import numpy
import parameters as param


class DepartureTimeModel:
    def __init__(self, nr_zones):
        """Container for time period and assignment class specific demand.
        
        Parameters
        ----------
        nr_zones : int
            Number of zones in assignment model
        """
        self.nr_zones = nr_zones
        self.demand = dict.fromkeys(param.emme_scenario)
        for time_period in self.demand:
            ass_classes = dict.fromkeys(param.transport_classes)
            self.demand[time_period] = ass_classes
            for ass_class in ass_classes:
                zeros = numpy.zeros((self.nr_zones, self.nr_zones))
                self.demand[time_period][ass_class] = zeros
        self.logger = logging.getLogger()

    def init_demand(self):
        """Initialize/reset demand for all time periods (each including transport_classes, each being set to zeros)."""
        self.demand = dict.fromkeys(param.emme_scenario)
        for time_period in self.demand:
            ass_classes = dict.fromkeys(param.transport_classes)
            self.demand[time_period] = ass_classes
            for ass_class in ass_classes:
                zeros = numpy.zeros((self.nr_zones, self.nr_zones))
                self.demand[time_period][ass_class] = zeros

    def add_demand(self, demand):
        """Add demand matrix for whole day.
        
        Parameters
        ----------
        demand : Demand or Tour
            Travel demand matrix or number of travellers
        """
        if demand.mode not in ("walk", "car_passenger"):
            if demand.mode in ("car", "transit", "bike"):
                ass_class = (demand.mode + '_' + param.assignment_class[demand.purpose.name])
            else:
                ass_class = demand.mode
            if len(demand.position) == 2:
                share = param.demand_share[demand.purpose.name][demand.mode]
                for time_period in param.emme_scenario:
                    self._add_2d_demand(
                        share[time_period], ass_class, time_period,
                        demand.matrix, demand.position)
                self.logger.debug("Added demand for {}, {}".format(demand.purpose.name, demand.mode))
            elif len(demand.position) == 3:
                for time_period in param.emme_scenario:
                    self._add_3d_demand(demand, ass_class, time_period)
                self.logger.debug("Added demand for {}, {}, {}".format(demand.purpose.name, demand.mode, demand.orig))
            else:
                raise IndexError("Tuple position has wrong dimensions.")

    def _add_2d_demand(self, demand_share, ass_class, time_period, mtx, mtx_pos):
        """Slice demand, include transpose and add for one time period."""
        r_0 = mtx_pos[0]
        c_0 = mtx_pos[1]
        try:  # Addition of matrix
            r_n = r_0 + mtx.shape[0]
            c_n = c_0 + mtx.shape[1]
        except AttributeError:  # Addition of agent
            r_n = r_0 + 1
            c_n = c_0 + 1
            mtx = numpy.asarray([mtx])
        large_mtx = self.demand[time_period][ass_class]
        try:
            large_mtx[r_0:r_n, c_0:c_n] += demand_share[0] * mtx
            large_mtx[c_0:c_n, r_0:r_n] += demand_share[1] * mtx.T
        except ValueError:
            share = param.backup_demand_share[time_period]
            large_mtx[r_0:r_n, c_0:c_n] += share[0] * mtx
            large_mtx[c_0:c_n, r_0:r_n] += share[1] * mtx.T
            self.logger.warn("{}x{} matrix not matching {} demand shares. Resorted to backup demand shares.".format(
                str(mtx.shape[0]),
                str(mtx.shape[0]),
                str(len(demand_share[0]))
            ))

    def _add_3d_demand(self, demand, ass_class, time_period):
        """Add three-way demand."""
        mtx = demand.matrix
        tp = time_period
        o = demand.position[0]
        d1 = demand.position[1]
        d2 = demand.position[2]
        try:  # Addition of matrix
            colsum = mtx.sum(0)[:, numpy.newaxis]
            share = param.demand_share[demand.purpose.name][demand.mode][tp]
            self._add_2d_demand(share[0], ass_class, tp, mtx, (d1, d2))
            self._add_2d_demand(share[1], ass_class, tp, colsum, (d2, o))
        except AttributeError:  # Addition of agent
            share = param.demand_share[demand.purpose.name][demand.mode][tp]
            self._add_2d_demand(share, ass_class, tp, mtx, (o, d1))
            sec_purpose_name = demand.purpose.sec_dest_purpose.name
            share = param.demand_share[sec_purpose_name][demand.mode][tp]
            self._add_2d_demand(share[0], ass_class, tp, mtx, (d1, d2))
            self._add_2d_demand(share[1], ass_class, tp, mtx, (d2, o))
    
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
        mtx = self.demand[time_period]
        car_demand = (mtx["car_work"][0:n, 0:n] + mtx["car_leisure"][0:n, 0:n])
        share = param.demand_share["freight"]["van"][time_period]
        self._add_2d_demand(share, "van", time_period, car_demand, (0, 0))
        mtx["van"][0:n, 0:n] += mtx["truck"][0:n, 0:n]
