import utils.log as log
import parameters.assignment as param
from abstract_assignment import AssignmentModel, Period


class MockAssignmentModel(AssignmentModel):
    def __init__(self, matrices):
        self.matrices = matrices
        log.info("Reading matrices from " + str(self.matrices.path))
        self.result_mtx=param.emme_result_mtx
        emme_scenarios = {"aht": 21, "pt": 22, "iht": 23}
        self.assignment_periods = [MockPeriod(tp, matrices) for tp in emme_scenarios]
    
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

    def init_assign(self, demand):
        pass


class MockPeriod(Period):
    def __init__(self, name, matrices):
        self.name = name
        self.matrices = matrices

    @property
    def zone_numbers(self):
        """Numpy array of all zone numbers.""" 
        with self.matrices.open("time", self.name) as mtx:
            zone_numbers = mtx.zone_numbers
        return zone_numbers

    def assign(self, matrices, iteration=None):
        """Assign cars, bikes and transit for one time period.
        Get travel impedance matrices for one time period from assignment.
        
        Parameters
        ----------
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
        with self.matrices.open("demand", self.name, self.zone_numbers, 'w') as mtx:
            for ass_class in matrices:
                mtx[ass_class] = matrices[ass_class]
        log.info("Saved demand matrices for " + str(self.name))
        mtxs = {mtx_type: self._get_matrices(mtx_type)
            for mtx_type in ("time", "cost", "dist")}
        for ass_cl in ("transit_work", "transit_leisure"):
            mtxs["time"][ass_cl] = mtxs["time"]["transit_uncongested"]
        if iteration != "last":
            for ass_cl in ("car_work", "car_leisure"):
                mtxs["cost"][ass_cl] += (param.dist_unit_cost
                                         * mtxs["dist"][ass_cl])
        return mtxs
    
    def _get_matrices(self, mtx_type):
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
        with self.matrices.open(mtx_type, self.name) as mtx:
            matrices = {mode: mtx[mode] for mode in mtx.matrix_list}
        return matrices
