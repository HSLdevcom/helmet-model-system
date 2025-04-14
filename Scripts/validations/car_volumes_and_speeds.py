from pathlib import Path
from typing import TYPE_CHECKING, Callable, Tuple

from events.model_system_event_listener import ModelSystemEventListener
from utils import log
from utils.validation import Validation, ValidationGroup, mae, mean, scatter_plot
import pandas as pd

if TYPE_CHECKING:
    from assignment.emme_bindings.mock_project import Network, Link



class VolumesAndSpeedsValidation(ModelSystemEventListener):
    """
    A class to analyze trip lengths in a model system by listening to specific events.
    """
    data_path: Path
    result_path: Path
    validation: Validation
    active: bool
        
    def __init__(self):
        self.validation = None
        self.active = False
        super().__init__()
    
    def on_simulation_started(self, forecastdata_path, result_path, args):
        self.result_path = result_path

    def on_validation_initialized(self, validation, validation_path):
        self.validation = validation
        self.data_path = validation_path / 'data'
    
    def on_iteration_started(self, iteration, previous_impedance):
        if iteration == 'last':
            # Active validation results on last iteration
            self.active = True
    
    def is_disabled(self) -> bool:
        if not self.active:
            return True
        if self.validation is None:
            log.warn("Validation not initialized, skipping volume and speed analysis")
            return True
        if not self.data_path.is_dir():
            log.warn(f"Validation data directory not found at {self.data_path}, skipping volume and speed analysis")
            return True
        return False
    
    def create_vol_group(self, name: str) -> ValidationGroup:
        vol_group = self.validation.create_group(name)
        vol_group.add_visualization('Volumes vs survey', scatter_plot(x='expected', y='prediction'))
        vol_group.add_visualization('Volumes vs Helmet4', scatter_plot(x='helmet4', y='prediction'))
        vol_group.add_aggregation('mean absolute error', mae, group_by='kuntaryhma')
        vol_group.add_aggregation('mean relative error', mean('relative_error'), group_by='kuntaryhma')
        return vol_group
    
    def create_speed_group(self, name: str) -> ValidationGroup:
        speed_group = self.validation.create_group(name)
        speed_group.add_visualization('Speed vs survey', scatter_plot(x='expected', y='prediction'))
        speed_group.add_aggregation('mean relative error', mean('relative_error'), group_by='kuntaryhma')
        return speed_group
    
    def on_assignment_complete(self, assignment_period, iteration, demand, impedance, scenario):
        if self.is_disabled():
            return
        suffix = assignment_period.name
        if suffix not in ['aht', 'iht']:
            return
        df = self._get_data()
        network = scenario.get_network()
        vol_group = self.create_vol_group(f'{suffix.capitalize()} Volumes')
        _add_to_validation_group(vol_group,
                                 network,
                                 df,
                                 lambda x: _sum_volumes(x, suffix),
                                 f'{suffix}_laskenta',
                                 f'{suffix}_helmet4')
        speed_group = self.create_speed_group(f'{suffix.capitalize()} Speeds')
        speed_tag = f'{suffix}_keskinopeus'
        _add_to_validation_group(speed_group,
                                 network,
                                 df,
                                 lambda x: x.length / (x.auto_time/60),
                                 speed_tag,
                                 helmet4=None,
                                 row_filter=lambda x: x[speed_tag] > 0)
        speed_group.add_visualization('Speeds vs survey', scatter_plot(x='expected', y='prediction'))
    
    def on_daily_results_aggregated(self, assignment_model, day_network):
        if self.is_disabled():
            return

        df = self._get_data()
        vol_group = self.create_vol_group('VRK Volumes')
        _add_to_validation_group(vol_group,
                                 day_network,
                                 df,
                                 lambda x: _sum_volumes(x, 'vrk'),
                                 'vrk_laskenta',
                                 'vrk_helmet4')

    def _get_data(self) -> pd.DataFrame:
        file_path = self.data_path / 'Helmet_laskenta_yhdistetty.xlsx'
        return pd.read_excel(file_path)\
            .set_index(['inode', 'jnode'])


def _add_to_validation_group(group: ValidationGroup,
                            network: 'Network',
                            df: pd.DataFrame,
                            prediction_func: Callable[['Link'], float],
                            expected: str,
                            helmet4: str,
                            row_filter: Callable[[pd.Series], bool] = None):
        for i, row in df.iterrows():
            link = _get_link(network, i)
            if link is None:
                continue
            if row_filter is not None and not row_filter(row):
                continue
            group.add_item(id=f'{i[0]}-{i[1]}',
                             prediction=prediction_func(link),
                             expected=row[expected],
                             helmet4=row[helmet4] if helmet4 is not None else None,
                             kunta=row['kunta'],
                             kuntaryhma=row['kuntaryhma'])

def _sum_volumes(link, suffix: str) -> float:
    attributes = ['@car_work', '@car_leisure', '@van']
    return sum(link[f'{attr}_{suffix}'] for attr in attributes)

def _get_link(network: 'Network', id: Tuple[int, int]) -> 'Link':
    link = network.link(id[0], id[1])
    if link is None:
        log.warn(f'Link {id[0]}-{id[1]} in validation data not found in the network')
    return link
