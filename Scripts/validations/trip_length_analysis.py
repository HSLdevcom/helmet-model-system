from pathlib import Path
import pandas as pd
from events.model_system_event_listener import ModelSystemEventListener

from utils import log
from utils.validation import Validation, bar_plot, mae

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
        
        length_distribution = pd.read_csv(self.data_path / 'pituusjakauma.csv', sep=';')
        length_distribution_helmet4 = self.get_helmet_length_distribution(self.data_path / 'trip_lengths_helmet4.txt')
        length_distribution_helmet5 = self.get_helmet_length_distribution(self.result_path / 'trip_lengths.txt')

        group = self.validation.create_group('Trip length distribution (trip_lengths.txt)')
        for i, row in length_distribution.iterrows():
            group.add_item(id=row['pituusjakauma'],
                           prediction=length_distribution_helmet5['length_percentages'][i],
                           expected=row['osuus'],
                           helmet4=length_distribution_helmet4['length_percentages'][i])
        group.add_aggregation('mean absolute error', mae)
        group.add_visualization('Trip lengths', bar_plot(y=['prediction', 'expected', 'helmet4']))

            
    def get_helmet_length_distribution(self, path):
        length_distribution_helmet = pd.read_csv(path, sep='\t')
        length_distribution_helmet = length_distribution_helmet.filter(regex='.*_c')
        length_distribution_helmet['total_c'] = length_distribution_helmet.sum(axis=1, numeric_only=True)
        total_total_c = length_distribution_helmet['total_c'].sum()
        length_distribution_helmet['length_percentages'] = (length_distribution_helmet['total_c']/total_total_c)*100
        tail = length_distribution_helmet.iloc[4:].sum()
        head = length_distribution_helmet.iloc[:4]
        whole = pd.concat([head.T, tail], axis=1, ignore_index=True).T
        return whole
