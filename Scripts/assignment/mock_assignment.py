import logging

import parameters.assignment as param
from abstract_assignment import AssignmentModel


class MockAssignmentModel(AssignmentModel):
    def __init__(self, matrices):
        self.matrices = matrices
        self.logger = logging.getLogger()
        self.logger.info("Reading matrices from " + str(self.matrices.path))
        self.result_mtx=param.emme_result_mtx
        self.emme_scenarios = {"aht": 21, "pt": 22, "iht": 23}
    
    def assign(self, time_period, matrices, iteration=None):
        """Assign cars, bikes and transit for one time period.
        Get travel impedance matrices for one time period from assignment.
        
        Parameters
        ----------
        time_period : str
            Time period (aht/pt/iht)
        matrices: dict
            Assignment class (car_work/transit/...) : numpy 2-d matrix
        iteration: int or str
            Iteration number (0, 1, 2, ...) or "last"

        Returns
        -------
        dict
            Type (time/cost/dist) : dict
                Assignment class (car_work/transit_leisure/...) : numpy 2-d matrix
        """
        self.time_period = time_period
        with self.matrices.open("demand", time_period, self.zone_numbers, 'w') as mtx:
            for ass_class in matrices:
                mtx[ass_class] = matrices[ass_class]
        self.logger.info("Saved demand matrices for " + str(time_period))

        matrices = {mtx_type: self.get_emmebank_matrices(mtx_type, self.time_period)
            for mtx_type in ("time", "cost", "dist")}
        matrices["time"]["transit_work"] = matrices["time"]["transit_uncongested"]
        matrices["time"]["transit_leisure"] = matrices["time"]["transit_uncongested"]
        return matrices
    
    def get_emmebank_matrices(self, mtx_type, time_period=None):
        """Get all matrices of specified type.
        
        Parameters
        ----------
        mtx_type : str
            Type (demand/time/transit/...)
        time_period : str
            Matrices' time period.

        Return
        ------
        dict
            Subtype (car_work/truck/inv_time/...) : numpy 2-d matrix
                Matrix of the specified type
        """
        matrices = dict.fromkeys(self.matrices.list_matrices(mtx_type, time_period))
        with self.matrices.open(mtx_type, time_period) as mtx:
            for mode in matrices:
                matrices[mode] = mtx[mode]
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

    def aggregate_results(self, resultdata):
        pass

    def prepare_network(self):
        pass