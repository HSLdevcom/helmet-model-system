from pathlib import Path
import pandas as pd
import numpy as np
from events.model_system_event_listener import ModelSystemEventListener

from utils import log
from utils.validation import Validation, mean_error

class TripLengthAnalysis(ModelSystemEventListener):
    """
    A class to analyze trip lengths in a model system by listening to specific events.
    """
    data_path: Path
    result_path: Path
    validation: Validation
        
    def __init__(self):
        self.validation = None
        super().__init__()
    
    def on_simulation_started(self, forecastdata_path, result_path, args):
        self.result_path = result_path

    def on_validation_initialized(self, validation, validation_path):
        self.validation = validation
        self.data_path = validation_path / 'data'

    def on_simulation_complete(self):
        if self.validation is None:
            log.warn("Validation not initialized, skipping trip length analysis")
            return

        car_kms = pd.read_csv(self.data_path / 'suoritteet.csv', sep=';')
        car_kms_helmet4 = self.get_helmet_car_kms(self.data_path / 'vehicle_kms_areas.txt')
        car_kms_helmet5 = self.get_helmet_car_kms(self.result_path / 'vehicle_kms_areas.txt')

        validations = [{'name': 'Trip Lengths vs survey', 'data': car_kms_helmet5['total_car']},
                        {'name': 'Trip Lengths vs helmet4', 'data': car_kms_helmet4['total_car']}]
        for v in validations:
            group = self.validation.create_group(v['name'])
            for i, row in car_kms.iterrows():
                group.add_item(v['data'][i], row['kokonaissuorite'], alue=row['alue'])
            group.add_aggregation('mean_error', mean_error, group_by='alue')
        
    def get_helmet_car_kms(self, path: Path) -> pd.DataFrame:
        car_kms_helmet = pd.read_csv(path, sep='\t')
        car_kms_helmet = car_kms_helmet.filter(regex='car_*')
        car_kms_helmet['total_car'] = car_kms_helmet.sum(axis=1, numeric_only=True)
        head = car_kms_helmet.iloc[:3].sum()
        tail = car_kms_helmet.iloc[3:5].sum()
        
        whole = pd.concat([head, tail], axis=1, ignore_index=True).T
        return whole
