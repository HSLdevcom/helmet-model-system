from dataclasses import asdict
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


class ParkAndRideFacilitiesResults(ModelSystemEventListener):
    """
    A class to analyze park and ride facilities.
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
    
    def on_iteration_complete(self, iteration: Union[str, int], impedance: Dict[str, Dict[str, np.ndarray]], gap: Dict[str, float]):
        if iteration=="last":
            self._save_pnr_facility_info()

    def _save_pnr_facility_info(self):
        pnr_data = []
        for facility in self.ms.dm.purpose_dict['hw'].park_and_ride_model._facilities:
            pnr_data.append({k: str(v) for k, v in asdict(facility).items()})

        pnr_results = pd.DataFrame(pnr_data)
        pnr_results['used_capacity'] = pnr_results['used_capacity'].astype(float).round().astype(int)
        pnr_results['shops'] = pnr_results['shops'].astype(float).round().astype(int)
        pnr_results.index = pnr_results['zone_id']
        pnr_results.index.name = None
        pnr_results = pnr_results[['cost','shops','capacity','used_capacity','time']]
        for col in pnr_results.columns:
            self.ms.resultdata.print_data(pnr_results[col], "pnr_facilities.txt", col)
            
