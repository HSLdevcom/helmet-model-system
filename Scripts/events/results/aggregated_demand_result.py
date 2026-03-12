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
    A class to print aggregated travel demand.
    """
    
    def __init__(self):
        super().__init__()

    def on_iteration_started(self, iteration, previous_impedance):
        return super().on_iteration_started(iteration, previous_impedance)
    
    def on_purpose_demand_calculated(self, purpose: 'TourPurpose', demand: 'Demand', pnr_iteration: int = 0, estimation_mode = False):
        if purpose.name == "wh": return
        if type(purpose) == TourPurpose:
            for mode in purpose.histograms:
                purpose.resultdata.print_matrix(
                    purpose.aggregates[mode].matrix, "aggregated_demand",
                    "{}_{}".format(purpose.name, mode), pnr_iteration)
    