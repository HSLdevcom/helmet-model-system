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
    A class to analyze demand going to the very same zone as where it started.
    """
    
    def __init__(self):
        super().__init__()
    
    def on_model_system_initialized(self,
                                    model_system: 'ModelSystem',
                                    zone_data_path: Path, 
                                    base_zone_data_path: Path, 
                                    base_matrices_path: Path,
                                    results_path: Path, 
                                    assignment_model: 'AssignmentModel', 
                                    name: str) -> None:
        self.ms = model_system
    
    def on_purpose_demand_calculated(self, purpose: 'TourPurpose', demand: 'Demand', pnr_iteration=0, estimation_mode = False):
        if purpose.name == "wh": return
        if type(purpose) == TourPurpose:
            for mode in purpose.histograms:
                purpose.resultdata.print_data(
                    purpose.own_zone_aggregates[mode].array,
                    "own_zone_demand.txt", "{}_{}".format(purpose.name, mode[0]))
