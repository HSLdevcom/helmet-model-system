from pathlib import Path
from typing import Dict, List, Union, TYPE_CHECKING
import pandas as pd
import numpy as np

from events.model_system_event_listener import ModelSystemEventListener
from utils.zone_interval import ArrayAggregator
import parameters.zone as zone_param

if TYPE_CHECKING:
    from modelsystem import ModelSystem
    from datatypes.demand import Demand
    from datatypes.purpose import TourPurpose
    from assignment.abstract_assignment import AssignmentModel


class NoiseAreasResults(ModelSystemEventListener):
    """
    A class to analyze noise impacts.
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
    
    def on_iteration_complete(self, iteration: Union[str, int], impedance: Dict[str, Dict[str, np.ndarray]], gap: Dict[str, float]):
        if iteration=="last":
            self._calculate_noise_areas()

    def _calculate_noise_areas(self):
        noise_areas_55, noise_areas_80, noise_areas = self.ms.ass_model.calc_noise()
        self.ms.resultdata.print_data(noise_areas, "noise_areas.txt", "area")
        self.ms.resultdata.print_data(noise_areas_55, "noise_areas.txt", "new_area>=55")
        self.ms.resultdata.print_data(noise_areas_80, "noise_areas.txt", "new_area>=80")
        ar = ArrayAggregator(self.ms.zdata_forecast.zone_numbers)
        pop = ar.aggregate(self.ms.zdata_forecast["population"])
        conversion = pd.Series(zone_param.pop_share_per_noise_area)
        noise_pop = conversion * noise_areas * pop
        noise_pop_55 = conversion * noise_areas_55 * pop
        noise_pop_80 = conversion * noise_areas_80 * pop
        self.ms.resultdata.print_data(noise_pop, "noise_areas.txt", "population")
        self.ms.resultdata.print_data(noise_pop_55, "noise_areas.txt", "population>=55")
        self.ms.resultdata.print_data(noise_pop_80, "noise_areas.txt", "population>=80")