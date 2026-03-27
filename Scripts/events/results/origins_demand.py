from pathlib import Path
from typing import Dict, List, Union, TYPE_CHECKING
import pandas as pd
import numpy as np

from events.model_system_event_listener import ModelSystemEventListener
from utils.zone_interval import ArrayAggregator

if TYPE_CHECKING:
    from modelsystem import ModelSystem
    from datatypes.demand import Demand
    from datatypes.purpose import TourPurpose
    from assignment.abstract_assignment import AssignmentModel


class OriginsDemand(ModelSystemEventListener):
    """
    A class to analyze tour origins.
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
            
    def on_demand_calculated(self, iteration, dtm):
                # Calculate tour sums and mode shares
        tour_sum = {mode: self.ms._sum_trips_per_zone(mode, include_dests=False)
            for mode in self.ms.travel_modes}
        sum_all = sum(tour_sum.values())
        ar = ArrayAggregator(sum_all.index)
        mode_shares = {}
        for mode in tour_sum:
            self.ms.resultdata.print_data(
                tour_sum[mode], "origins_demand.txt", mode)
            self.ms.resultdata.print_data(
                ar.aggregate(tour_sum[mode]), "origins_demand_areas.txt", mode)
            self.ms.resultdata.print_data(
                tour_sum[mode] / sum_all, "origins_shares.txt", mode)
            mode_shares[mode] = tour_sum[mode].sum() / sum_all.sum()
        self.ms.mode_share.append(mode_shares) #Only for tests to go through