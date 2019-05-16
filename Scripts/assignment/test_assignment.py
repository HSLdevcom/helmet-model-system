import os
import omx
import numpy
import logging
import parameters as param
from abstract_assignment import AssignmentModel, ImpedanceSource 

class TestAssignmentModel(AssignmentModel, ImpedanceSource):
    def __init__(self, cost_matrixes):
        self.costs = cost_matrixes
        self.logger = logging.getLogger()
        self.logger.info("Reading Matrices from " + str(self.costs.path))
    
    def assign(self, time_period, matrices):
        self.time_period = time_period
    
    def get_impedance(self):
        """Get travel impedance matrices for one time period from files."""
        mtxs = {}
        mtxs["time"] = self.get_matrices("time", self.time_period)
        mtxs["cost"] = self.get_matrices("cost", self.time_period)
        mtxs["dist"] = self.get_matrices("dist", self.time_period)
        return mtxs
    
    def get_matrices(self, mtx_type, time_period):
        matrices = dict.fromkeys(param.emme_mtx[mtx_type].keys())
        for mode in matrices:
            matrices[mode] = self.costs.get_data(mtx_type, mode, time_period)
        return matrices
    
    def get_zone_numbers(self):
        return self.costs.get_zone_numbers("time", "aht")
    
    def get_mapping(self):
        return self.costs.get_mapping("time", "aht")
