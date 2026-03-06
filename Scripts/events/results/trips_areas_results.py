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


class TripsAreasResults(ModelSystemEventListener):
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
            
    def on_demand_calculated(self, iteration, dtm):
                # Calculate tour sums and mode shares
        tour_sum = {mode: self.ms._sum_trips_per_zone(mode, include_dests=False)
            for mode in self.ms.travel_modes}
        sum_all = sum(tour_sum.values())
        ar = ArrayAggregator(sum_all.index)
        trip_sum = {mode: self.ms._sum_trips_per_zone(mode)
            for mode in self.ms.travel_modes}
        for mode in tour_sum:
            self.ms.resultdata.print_data(
                ar.aggregate(trip_sum[mode]), "trips_areas.txt", mode)