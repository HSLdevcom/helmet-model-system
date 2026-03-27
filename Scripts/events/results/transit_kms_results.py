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


class TransitKmsResults(ModelSystemEventListener):
    """
    A class to analyze kilometers driven by transit modes.
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

    def on_daily_results_aggregated(self, assignment_model, day_network, network_aggregations):
        self.ass_model = self.ms.ass_model
        # Aggregate and print transit vehicle kms
        transit_modes = [veh.description for veh in day_network.transit_vehicles()]
        dists = pd.Series(0.0, transit_modes)
        times = pd.Series(0.0, transit_modes)
        for ap in self.ass_model.assignment_periods:
            network = ap.emme_scenario.get_network()
            volume_factor = param.volume_factors["bus"][ap.name]
            for line in network.transit_lines():
                mode = line.vehicle.description
                headway = line[ap.extra("hw")]
                if 0 < headway < 900:
                    departures = volume_factor * 60/headway
                    for segment in line.segments():
                        dists[mode] += departures * segment.link.length
                        times[mode] += (departures
                                        * segment[ap.extra("base_timtr")])
        self.ms.resultdata.print_data(dists, "transit_kms.txt", "dist")
        self.ms.resultdata.print_data(times, "transit_kms.txt", "time")