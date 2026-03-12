from pathlib import Path
from typing import Dict, List, Union, TYPE_CHECKING
import pandas as pd
import numpy as np

from events.model_system_event_listener import ModelSystemEventListener
import parameters.assignment as param

if TYPE_CHECKING:
    from modelsystem import ModelSystem
    from datatypes.demand import Demand
    from datatypes.purpose import TourPurpose
    from assignment.abstract_assignment import AssignmentModel


class TransitStationsResults(ModelSystemEventListener):
    """
    A class to count transit stations in network.
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
        self.ass_model = self.ms.ass_model
        # Aggregate and print numbers of stations
        stations = pd.Series(0, param.station_ids)
        for node in day_network.regular_nodes():
            for mode in param.station_ids:
                if (node.data2 == param.station_ids[mode]
                        and node[self.ass_model._extra("transit_won_boa")] > 0):
                    stations[mode] += 1
                    break
        self.ms.resultdata.print_data(stations, "transit_stations.txt", "number")