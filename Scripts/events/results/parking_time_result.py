from pathlib import Path
from typing import TYPE_CHECKING
import pandas as pd
import numpy as np

from events.model_system_event_listener import ModelSystemEventListener

if TYPE_CHECKING:
    from modelsystem import ModelSystem
    from datatypes.purpose import TourPurpose


class ParkingTimeResult(ModelSystemEventListener):
    """
    A class to print calculated parking time to results directory.
    """
    result_path: Path
    """ The path to the result file. """
    
    def __init__(self):
        super().__init__()
    
    def on_model_system_initialized(self, model_system: 'ModelSystem'):
        # Get result path when model system is initialized
        self.result_path = Path(model_system.resultdata.path) / 'parking_time.csv'

    def on_parking_time_calculated(self, purpose: 'TourPurpose', parking_time: np.ndarray):
        # Create a DataFrame from parking_time using purpose.zone_data zone numbers as index
        df = pd.DataFrame(parking_time, index=purpose.zone_data.zone_numbers, columns=['parking_time'])
        df.index.name = 'zone_id'
        # Save the DataFrame to a CSV file
        df.to_csv(self.result_path)
        # TODO: Only print results for last iteration and one Purpose