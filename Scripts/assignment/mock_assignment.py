from __future__ import annotations
from typing import TYPE_CHECKING, Dict, List, Optional, Tuple, Union
import numpy # type: ignore
import numpy.typing as npt
import pandas
if TYPE_CHECKING:
    from datahandling.matrixdata import MatrixData
    from datatypes.literals import TimePeriod, ImpedanceType


import utils.log as log
import parameters.assignment as param
import parameters.zone as zone_param
from assignment.abstract_assignment import AssignmentModel, Period
from assignment.emme_bindings.mock_project import MockProject


class MockAssignmentModel(AssignmentModel):
    def __init__(self, 
                 emme_context: MockProject, 
                 first_scenario_id: int, 
                 matrices: MatrixData, 
                 time_periods: List[TimePeriod]=param.time_periods):
        self.matrices = matrices
        log.info("Reading matrices from " + str(self.matrices.path))
        self.mock_project = emme_context
        self.mod_scenario = self.mock_project.modeller.emmebank.scenario(first_scenario_id)
        self.time_periods = time_periods
        self.assignment_periods = [MockPeriod(tp, first_scenario_id, self.mock_project, matrices)
                                   for tp in time_periods]

    @property
    def zone_numbers(self) -> list:
        """Numpy array of all zone numbers.""" 
        return self.mod_scenario.zone_numbers

    @property
    def mapping(self):
        """dict: Dictionary of zone numbers and corresponding indices."""
        with self.matrices.open("time", "aht") as mtx:
            mapping = mtx.mapping
        return mapping

    @property
    def nr_zones(self) -> int:
        """int: Number of zones in assignment model."""
        return len(self.zone_numbers)
    
    def calc_transit_cost(self, fare, peripheral_cost, default_cost=None):
        pass

    def aggregate_results(self, resultdata):
        pass

    def calc_noise(self):
        return pandas.Series(0.0, zone_param.area_aggregation)

    def prepare_network(self, car_dist_unit_cost: Optional[float]=None):
        pass

    def init_assign(self, demand):
        pass


class MockPeriod(Period):
    def __init__(self, name: TimePeriod, scen_id: int, mock_project: MockProject, matrices: MatrixData):
        self.name: TimePeriod = name
        self.matrices = matrices
        self.scenario = mock_project.modeller.emmebank.scenario(scen_id)

    @property
    def zone_numbers(self):
        """Numpy array of all zone numbers.""" 
        return self.scenario.zone_numbers

    def assign(self, 
               matrices: Dict[str, npt.NDArray], 
               iteration: int | str) -> dict[ImpedanceType, dict[str, npt.NDArray]]:
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
        mtxs : dict[ImpedanceType, dict[str, npt.NDArray]]
        mtxs = {mtx_type: self._get_matrices(mtx_type)
            for mtx_type in ("time", "cost", "dist")}
        for ass_cl in ("transit_work", "transit_leisure"):
            mtxs["time"][ass_cl] = mtxs["time"][f"{ass_cl}_uncongested"]
        if iteration != "last":
            for ass_cl in ("car_work", "car_leisure"):
                mtxs["cost"][ass_cl] += (param.dist_unit_cost
                                         * mtxs["dist"][ass_cl])
        return mtxs
    
    def _get_matrices(self, mtx_type: str) -> Dict[str, npt.NDArray]:
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
        with self.matrices.open(mtx_type, self.name, self.zone_numbers) as mtx:
            matrices = {mode: mtx[mode] for mode in mtx.matrix_list}
        return matrices
