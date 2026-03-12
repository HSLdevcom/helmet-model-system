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


class GenerationResults(ModelSystemEventListener):
    """
    A class to analyze tour generation
    """
    
    def __init__(self):
        super().__init__()
    
    def on_model_system_initialized(self,
                                    model_system: 'ModelSystem',
                                    zone_data_path: str, 
                                    base_zone_data_path: str, 
                                    base_matrices_path: str,
                                    results_path: str, 
                                    assignment_model: 'AssignmentModel', 
                                    name: str) -> None:
        self.ms = model_system
    
    def on_purpose_demand_calculated(self, purpose: TourPurpose, demand: 'Demand', pnr_iteration: int = 0):
        if purpose.name == "wh": return
        if type(purpose) == TourPurpose:
            self.ms.resultdata.print_data(
                pd.Series(
                    sum(purpose.generated_tours.values()), purpose.zone_numbers),
                "generation.txt", purpose.name)   
    
