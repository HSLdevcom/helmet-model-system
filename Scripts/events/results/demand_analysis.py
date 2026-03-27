from pathlib import Path
from typing import Dict, List, Union, TYPE_CHECKING
import pandas as pd
import numpy as np
from utils import log
from datatypes.purpose import TourPurpose

from events.model_system_event_listener import ModelSystemEventListener

if TYPE_CHECKING:
    from modelsystem import ModelSystem
    from datatypes.demand import Demand
    from assignment.abstract_assignment import AssignmentModel


class DemandAnalysis(ModelSystemEventListener):
    """
    A class to analyze demand in a model system by listening to specific events.
    """
    
    mode_demands: List[Dict[str, int]]
    """ A list of dictionaries to store mode demands for each iteration. """
    result_path: Path
    """ The path to the result file. """
    
    def __init__(self):
        super().__init__()
        self.mode_demands = []
    
    def on_model_system_initialized(self,
                                    model_system: 'ModelSystem',
                                    zone_data_path: Path, 
                                    base_zone_data_path: Path, 
                                    base_matrices_path: Path,
                                    results_path: Path, 
                                    assignment_model: 'AssignmentModel', 
                                    name: str) -> None:
        # Get result path when model system is initialized
        self.result_path = Path(results_path) / name / 'mode_analysis_results.csv'
    
    def on_iteration_started(self, iteration: Union[int, str], previous_impedance: Dict[str, Dict[str, np.ndarray]]):
        # Add new row for each iteration
        self.mode_demands.append({'iteration': iteration})
    
    def on_purpose_demand_calculated(self, purpose: TourPurpose, purpose_demand: 'Demand', pnr_iteration: int = 0, estimation_mode = False):
        if pnr_iteration > 0 or type(purpose)!=TourPurpose: return #sec_dest purposes skipped
        if purpose_demand is None: return #skip if purpose demand is not calculated (agent based model)
        # Sum mode demand for each purpose after it has been calculated
        current_results = self.mode_demands[-1]
        for m, d in purpose_demand.items():
            current_results[m] = d.matrix.sum() + current_results.get(m, 0)
    
    def on_iteration_complete(self, iteration: Union[str, int], impedance: Dict[str, Dict[str, np.ndarray]], gap: Dict[str, float]):
        # Print resuts after last iteration
        if iteration == 'last' or iteration is None:
            pd.DataFrame(self.mode_demands)\
                .to_csv(self.result_path, index=False)
