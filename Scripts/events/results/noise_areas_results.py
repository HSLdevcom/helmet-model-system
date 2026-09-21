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
        noise_areas, noise_areas_50_, noise_areas_55_, noise_areas_60_, noise_areas_65_, noise_areas_70_75 = self.ms.ass_model.calc_noise()
        # Since areas include each other, we need to subtract the smaller areas 
        # from the larger ones to get the population only within the specific noise range.
        noise_areas_50_54 = noise_areas_50_ - (noise_areas_55_ + noise_areas_60_ + noise_areas_65_ + noise_areas_70_75)
        noise_areas_55_59 = noise_areas_55_ - (noise_areas_60_ + noise_areas_65_ + noise_areas_70_75)
        noise_areas_60_64 = noise_areas_60_ - (noise_areas_65_ + noise_areas_70_75)
        noise_areas_65_69 = noise_areas_65_ - (noise_areas_70_75)
        self.ms.resultdata.print_data(noise_areas, "noise_areas.txt", "area_old")
        self.ms.resultdata.print_data(noise_areas_50_54, "noise_areas.txt", "area_50_54")
        self.ms.resultdata.print_data(noise_areas_55_59, "noise_areas.txt", "area_55_59")
        self.ms.resultdata.print_data(noise_areas_60_64, "noise_areas.txt", "area_60_64")
        self.ms.resultdata.print_data(noise_areas_65_69, "noise_areas.txt", "area_65_69")
        self.ms.resultdata.print_data(noise_areas_70_75, "noise_areas.txt", "area_70_75")
        ar = ArrayAggregator(self.ms.zdata_forecast.zone_numbers)
        pop = ar.aggregate(self.ms.zdata_forecast["population"])
        conversion = pd.Series(zone_param.pop_share_per_noise_area)
        noise_pop = conversion * noise_areas * pop
        noise_pop_50_54 = conversion * noise_areas_50_54 * pop
        noise_pop_55_59 = conversion * noise_areas_55_59 * pop
        noise_pop_60_64 = conversion * noise_areas_60_64 * pop
        noise_pop_65_69 = conversion * noise_areas_65_69 * pop
        noise_pop_70_75 = conversion * noise_areas_70_75 * pop
        noise_pop_total = noise_pop_50_54 + noise_pop_55_59 + noise_pop_60_64 + noise_pop_65_69 + noise_pop_70_75
        self.ms.resultdata.print_data(noise_pop, "noise_areas.txt", "population_old")
        self.ms.resultdata.print_data(noise_pop_50_54, "noise_areas.txt", "population_50_54")
        self.ms.resultdata.print_data(noise_pop_55_59, "noise_areas.txt", "population_55_59")
        self.ms.resultdata.print_data(noise_pop_60_64, "noise_areas.txt", "population_60_64")
        self.ms.resultdata.print_data(noise_pop_65_69, "noise_areas.txt", "population_65_69")
        self.ms.resultdata.print_data(noise_pop_70_75, "noise_areas.txt", "population_70_75")
        self.ms.resultdata.print_data(noise_pop_total, "noise_areas.txt", "population_total")