from pathlib import Path
from typing import Dict, List, Union, TYPE_CHECKING
import pandas as pd
import numpy as np

from events.model_system_event_listener import ModelSystemEventListener
from utils.zone_interval import ZoneIntervals

if TYPE_CHECKING:
    from modelsystem import ModelSystem
    from datatypes.demand import Demand
    from datatypes.purpose import TourPurpose
    from assignment.abstract_assignment import AssignmentModel


class CarDensityResults(ModelSystemEventListener):
    """
    A class to analyze car density aka cars per people.
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

    def on_car_density_updated(self, iteration, prediction, model):
        """ Print results, mainly for calibration purposes"""
        # Print car density by zone
        self.ms.resultdata.print_data(prediction, "car_density.txt", "car_density")
        # In validation data, car density is calculated for the whole
        # population from ages 0 to 999.
        population = model.zone_data["population"][model.bounds]
        # print car density by municipality and area
        for area_type in ("municipalities", "areas"):
            aggregation = ZoneIntervals(area_type).averages(prediction, population)
            self.ms.resultdata.print_data(
                aggregation, "car_density_{}.txt".format(area_type),
                "car_density")