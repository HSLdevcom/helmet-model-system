from pathlib import Path
from typing import Dict, List, Union, TYPE_CHECKING
import pandas as pd
import numpy as np

from events.model_system_event_listener import ModelSystemEventListener

if TYPE_CHECKING:
    from modelsystem import ModelSystem
    from datatypes.demand import Demand
    from datatypes.purpose import TourPurpose


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
    
    def on_model_system_initialized(self, model_system: 'ModelSystem'):
        # Get result path when model system is initialized
        self.result_path = Path(model_system.resultdata.path) / 'mode_analysis_results.csv'
    
    def on_iteration_started(self, iteration: Union[int, str], previous_impedance: Dict[str, Dict[str, np.ndarray]]):
        # Add new row for each iteration
        self.mode_demands.append({'iteration': iteration})
    
    def on_purpose_demand_calculated(self, purpose: 'TourPurpose', demand: 'Demand'):
        # Sum mode demand for each purpose after it has been calculated
        current_results = self.mode_demands[-1]
        for m, d in demand.items():
            current_results[m] = d.matrix.sum() + current_results.get(m, 0)
    
    def on_iteration_complete(self, iteration: Union[str, int], impedance: Dict[str, Dict[str, np.ndarray]], gap: Dict[str, float]):
        # Print resuts after last iteration
        if iteration == 'last' or iteration is None:
            pd.DataFrame(self.mode_demands)\
                .to_csv(self.result_path, index=False)
