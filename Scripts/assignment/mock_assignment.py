import os
import numpy
import logging
import parameters as param
from abstract_assignment import AssignmentModel, ImpedanceSource 

class MockAssignmentModel(AssignmentModel, ImpedanceSource):
    def __init__(self, matrices):
        self.matrices = matrices
        self.logger = logging.getLogger()
        self.logger.info("Reading matrices from " + str(self.matrices.path))
    
    def assign(self, time_period, matrices, is_last_iteration=False, is_first_iteration=False):
        """Assign cars, bikes and transit for one time period.
        
        Parameters
        ----------
        time_period : str
            Time period (aht/pt/iht)
        matrices: dict
            Assignment class (car_work/transit/...): numpy 2-d matrix
        """
        self.time_period = time_period
        with self.matrices.open("demand", time_period, 'w') as mtx:
            for ass_class in matrices:
                mtx.set_data(matrices[ass_class], ass_class)
        self.logger.info("Saved demand matrices for " + str(time_period))
    
    def get_impedance(self):
        """Get travel impedance matrices for one time period from files.
        
        Return
        ------
        dict
            Type (time/cost/dist) : dict
                Assignment class (car_work/transit/...) : numpy 2-d matrix
        """
        mtxs = {}
        mtxs["time"] = self.get_matrices("time", self.time_period)
        mtxs["cost"] = self.get_matrices("cost", self.time_period)
        mtxs["dist"] = self.get_matrices("dist", self.time_period)
        return mtxs
    
    def get_matrices(self, mtx_type, time_period):
        """Get all matrices of specified type.
        
        Parameters
        ----------
        mtx_type : str
            Type (demand/time/transit/...)

        Return
        ------
        dict
            Subtype (car_work/truck/inv_time/...) : numpy 2-d matrix
                Matrix of the specified type
        """
        matrices = dict.fromkeys(param.emme_mtx[mtx_type].keys())
        with self.matrices.open(mtx_type, time_period) as mtx:
            for mode in matrices:
                matrices[mode] = mtx.get_data(mode)
        return matrices
    
    @property
    def zone_numbers(self):
        """Numpy array of all zone numbers.""" 
        with self.matrices.open("time", "aht") as mtx:
            zone_numbers = mtx.zone_numbers
        return zone_numbers
    
    @property
    def mapping(self):
        """dict: Dictionary of zone numbers and corresponding indices."""
        with self.matrices.open("time", "aht") as mtx:
            mapping = mtx.mapping
        return mapping

    @property
    def nr_zones(self):
        """int: Number of zones in assignment model."""
        return len(self.zone_numbers)

    def calc_transit_cost(self, fare, peripheral_cost, default_cost=None):
        pass
