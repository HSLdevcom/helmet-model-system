import assignment as ass
import logging
import numpy
import omx
import os
from parameters import emme_scenario, demand_share, assignment_class, emme_mtx

class DepartureTimeModel:
    def __init__(self, assignment_model):
        self.assignment = assignment_model
        self._init_demand()

    def _init_demand(self):
        self.demand = dict.fromkeys(emme_scenario.keys())
        nr_zones = len(self.assignment.get_mapping())
        for time_period in self.demand:
            ass_classes = dict.fromkeys(emme_mtx["demand"].keys())
            self.demand[time_period] = ass_classes
            for ass_class in ass_classes:
                zeros = numpy.zeros((nr_zones, nr_zones))
                self.demand[time_period][ass_class] = zeros

    def add_demand(self, purpose, mode, mtx, mtx_position=[0, 0]):
        r_0 = mtx_position[0]
        c_0 = mtx_position[1]
        r_n = r_0 + mtx.shape[0]
        c_n = c_0 + mtx.shape[1]
        if mode == "car":
            ass_class = assignment_class[purpose]
        else:
            ass_class = mode
        for time_period in emme_scenario:
            leave_share = demand_share[purpose][mode][time_period][0]
            return_share = demand_share[purpose][mode][time_period][1]
            large_mtx = self.demand[time_period][ass_class]
            large_mtx[r_0:r_n, c_0:c_n] += leave_share * mtx
            large_mtx[c_0:c_n, r_0:r_n] += return_share * mtx.T

    def assign(self):
        travel_cost = {}
        for tp in emme_scenario:
            travel_cost[tp] = self.assignment.assign(tp, self.demand[tp])
        self._init_demand()
        return travel_cost
