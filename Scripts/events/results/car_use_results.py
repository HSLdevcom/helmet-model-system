from pathlib import Path
from typing import Dict, List, Optional, Union, TYPE_CHECKING
import pandas as pd
import numpy as np

from events.model_system_event_listener import ModelSystemEventListener
from utils import log
from utils.zone_interval import ZoneIntervals

if TYPE_CHECKING:
    from modelsystem import ModelSystem
    from datatypes.demand import Demand
    from datatypes.purpose import TourPurpose
    from assignment.abstract_assignment import AssignmentModel


class CarUseResults(ModelSystemEventListener):
    """
    A class to analyze access to car (HAP model).
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

    def on_population_segments_created(self, dm):
        """ Print results, mainly for calibration purposes"""
        if "car_users" not in dm.zone_data._values: #agent model
            car_users = pd.Series(
            0, dm.zone_data.zone_numbers[dm.car_use_model.bounds])
            for person in dm.population:
                car_users[person.zone.number] += person.is_car_user
            prob = car_users / dm.zone_population
        else: #agg model
            prob = dm.zone_data["car_users"]
        # Print car user share by zone
        self.ms.resultdata.print_data(prob, "car_use.txt", "car_use")
        if not hasattr(dm, "zone_population"):
            # Comparison data has car user shares of population
            # over 6 years old (from HEHA)
            population_7_99 = (dm.zone_data["population"][dm.bounds]
                               * dm.zone_data["share_age_7-99"])
        else:
            population_7_99 = dm.zone_population

        # print car use share by municipality and area
        for area_type in ("municipalities", "areas"):
            prob_area = ZoneIntervals(area_type).averages(prob, population_7_99)
            self.ms.resultdata.print_data(
                prob_area, "car_use_{}.txt".format(area_type), "car_use")