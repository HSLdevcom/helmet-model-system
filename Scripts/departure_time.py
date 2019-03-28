import assignment as ass
import logging
import numpy
import omx
import os
from parameters import emme_scenario, demand_share, assignment_class, emme_mtx

class DepartureTimeModel:
    def __init__(self, assignment_model):
        self.assignment_model = assignment_model
        self._init_demand()

    def _init_demand(self):
        self.demand = dict.fromkeys(emme_scenario.keys())
        nr_zones = len(self.assignment_model.get_mapping())
        for time_period in self.demand:
            self.demand[time_period] = dict.fromkeys(emme_mtx["demand"].keys())
            for ass_class in self.demand[time_period]:
                self.demand[time_period][ass_class] = numpy.zeros((nr_zones, nr_zones))

    def add_demand(self, purpose, mode, mtx):
        if mode == "car":
            ass_class = assignment_class[purpose]
        else:
            ass_class = mode
        for time_period in emme_scenario:
            share = demand_share[purpose][mode][time_period]
            self.demand[time_period][ass_class] += share * mtx

    def assign(self):
        travel_cost = {}
        for time_period in emme_scenario:
            travel_cost[time_period] = self.assignment_model.assign(time_period, self.demand[time_period])
        self._init_demand()
        return travel_cost
