import os
import numpy
import logging
import parameters as param
from abstract_assignment import AssignmentModel, ImpedanceSource 

class TestAssignmentModel(AssignmentModel, ImpedanceSource):
    def __init__(self, matrices):
        self.matrices = matrices
        self.logger = logging.getLogger()
        self.logger.info("Reading Matrices from " + str(self.matrices.path))
    
    def assign(self, time_period, matrices):
        self.time_period = time_period
        self.matrices.open_file("demand", time_period, 'w')
        for ass_class in matrices:
            self.matrices.set_data(matrices[ass_class], ass_class)
        self.matrices.close()
    
    def get_impedance(self):
        """Get travel impedance matrices for one time period from files."""
        mtxs = {}
        mtxs["time"] = self.get_matrices("time", self.time_period)
        mtxs["cost"] = self.get_matrices("cost", self.time_period)
        mtxs["dist"] = self.get_matrices("dist", self.time_period)
        return mtxs
    
    def get_matrices(self, mtx_type, time_period):
        matrices = dict.fromkeys(param.emme_mtx[mtx_type].keys())
        self.matrices.open_file(mtx_type, time_period)
        for mode in matrices:
            matrices[mode] = self.matrices.get_data(mode)
        self.matrices.close()
        return matrices
    
    def get_zone_numbers(self):
        self.matrices.open_file("time", "aht")
        zone_numbers = self.matrices.get_zone_numbers()
        self.matrices.close()
        return zone_numbers
    
    def get_mapping(self):
        self.matrices.open_file("time", "aht")
        mapping = self.matrices.get_mapping()
        self.matrices.close()
        return mapping
