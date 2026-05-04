from pathlib import Path
from typing import Dict, List, Union, TYPE_CHECKING
import pandas as pd
import numpy as np

from events.model_system_event_listener import ModelSystemEventListener

if TYPE_CHECKING:
    from modelsystem import ModelSystem
    from datatypes.demand import Demand
    from datatypes.purpose import TourPurpose
    from assignment.abstract_assignment import AssignmentModel


class TourCombinationsResults(ModelSystemEventListener):
    """
    A class to analyze generated tour combinations.
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
    
    def on_demand_model_tours_generated(self, dm):
        self.ms.resultdata.print_matrix(
            dm.tour_generation_model.result, "tour_combinations", "tour_combinations")