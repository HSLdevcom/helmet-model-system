from pathlib import Path
from typing import Dict, List, Union, TYPE_CHECKING
import pandas as pd
import numpy as np

from events.model_system_event_listener import ModelSystemEventListener
from datatypes.purpose import TourPurpose

if TYPE_CHECKING:
    from modelsystem import ModelSystem
    from datatypes.demand import Demand
    from assignment.abstract_assignment import AssignmentModel


class ModeShareResults(ModelSystemEventListener):
    """
    A class to analyze mode shares.
    """

    def __init__(self):
        super().__init__()

    def on_purpose_demand_calculated(self, purpose: TourPurpose, demand: 'Demand', pnr_iteration=0, estimation_mode = False):
        if purpose.name == "wh": return
        if type(purpose) == TourPurpose:
            demsums = {mode: purpose.generated_tours[mode].sum()
                for mode in purpose.modes}
            demand_all = float(sum(demsums.values()))
            self.mode_shares = {mode: demsums[mode] / demand_all for mode in demsums}
            purpose.resultdata.print_data(
                pd.Series(self.mode_shares),
                "mode_share.txt", purpose.name)
    