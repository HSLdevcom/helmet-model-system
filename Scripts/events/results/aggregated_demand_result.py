from pathlib import Path
from typing import Dict, List, Union, TYPE_CHECKING
import pandas as pd
import numpy as np

from events.model_system_event_listener import ModelSystemEventListener
from datatypes.purpose import TourPurpose
from datatypes.demand import Demand

if TYPE_CHECKING:
    from modelsystem import ModelSystem
    from assignment.abstract_assignment import AssignmentModel


class AggregatedDemandResults(ModelSystemEventListener):
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
        self.pnr_iteration = {}

    def on_iteration_started(self, iteration, previous_impedance):
        return super().on_iteration_started(iteration, previous_impedance)
    
    def on_purpose_demand_calculated(self, purpose: 'TourPurpose', demand: 'Demand', pnr_iteration: int = 0):
        if type(purpose) == TourPurpose:
            for mode in purpose.histograms:
                purpose.resultdata.print_matrix(
                    purpose.aggregates[mode].matrix, "aggregated_demand",
                    "{}_{}".format(purpose.name, mode), pnr_iteration)
    