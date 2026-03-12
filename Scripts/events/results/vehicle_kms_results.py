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


class VehicleKmsResults(ModelSystemEventListener):
    """
    A class to analyze kilometers driven by different road traffic modes.
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
            
    def on_daily_results_aggregated(self, assignment_model, day_network, network_aggregations):
        for ass_class in assignment_model.res_ass_classes:
            self.ms.resultdata.print_data(
                network_aggregations["vdf_kms"][ass_class], "vehicle_kms_vdfs.txt", ass_class)
            self.ms.resultdata.print_data(
                network_aggregations["area_kms"][ass_class], "vehicle_kms_areas.txt", ass_class)
        for vdf in network_aggregations["vdf_area_kms"]:
            self.ms.resultdata.print_data(
                network_aggregations["vdf_area_kms"][vdf], "vehicle_kms_vdfs_areas.txt", vdf)