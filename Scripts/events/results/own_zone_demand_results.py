from pathlib import Path
from typing import Dict, List, Union, TYPE_CHECKING
import pandas as pd
import numpy as np

from events.model_system_event_listener import ModelSystemEventListener
from datatypes.demand import Demand
from datatypes.purpose import TourPurpose

if TYPE_CHECKING:
    from modelsystem import ModelSystem
    from assignment.abstract_assignment import AssignmentModel


class OwnZoneDemandResults(ModelSystemEventListener):
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
                                    zone_data_path: str, 
                                    base_zone_data_path: str, 
                                    base_matrices_path: str,
                                    results_path: str, 
                                    assignment_model: 'AssignmentModel', 
                                    name: str) -> None:
        # Get result path when model system is initialized
        self.result_path = Path(results_path) / name / 'mode_analysis_results.csv'
        self.ms = model_system
    
    def on_purpose_demand_calculated(self, purpose: 'TourPurpose', demand: 'Demand', pnr_iteration=0):
        if type(purpose) == TourPurpose:
            for mode in purpose.histograms:
                purpose.resultdata.print_data(
                    purpose.own_zone_aggregates[mode].array,
                    "own_zone_demand.txt", "{}_{}".format(purpose.name, mode[0]))
