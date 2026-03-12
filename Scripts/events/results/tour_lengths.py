from pathlib import Path
from typing import Dict, List, Union, TYPE_CHECKING
import pandas as pd
import numpy as np

from events.model_system_event_listener import ModelSystemEventListener
from datatypes.demand import Demand
from datatypes.purpose import TourPurpose

if TYPE_CHECKING:
    from modelsystem import ModelSystem
    from assignment.abstract_assignment import AssignmentModel


class TourLengthsResults(ModelSystemEventListener):
    """
    A class to analyze tour lengths. Length based on car distance.
    """
    
    def __init__(self):
        super().__init__()
    
    def on_purpose_demand_calculated(self, purpose: 'TourPurpose', demand: 'Demand', pnr_iteration=0):
        if purpose.name == "wh": return
        if type(purpose) == TourPurpose:
            for mode in purpose.histograms:
                purpose.resultdata.print_data(
                    purpose.histograms[mode].histogram, "trip_lengths.txt",
                    "{}_{}".format(purpose.name, mode[0]))