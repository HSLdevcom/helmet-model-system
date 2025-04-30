from pathlib import Path
from typing import Dict, List, Union, TYPE_CHECKING
import pandas as pd
import numpy as np
import utils.log as log

from events.model_system_event_listener import ModelSystemEventListener

if TYPE_CHECKING:
    from modelsystem import ModelSystem
    from datatypes.demand import Demand
    from datatypes.purpose import TourPurpose
    from assignment.emme_bindings.mock_project import Scenario
    from assignment.assignment_period import AssignmentPeriod
    from assignment.emme_assignment import EmmeAssignmentModel
    from assignment.emme_bindings.mock_project import Network




class TransitResults(ModelSystemEventListener):
    """
    A class to print calculated transit results to results directory.
    """
    mode_demands: List[Dict[str, int]]
    """ A list of dictionaries to store mode demands for each iteration. """
    result_path: Path
    """ The path to the result file. """
    
    def __init__(self):
        super().__init__()
        self.transit_line_congestions = pd.DataFrame()
    
    def on_model_system_initialized(self, model_system: 'ModelSystem'):
        # Get result path when model system is initialized
        self.transit_result_path = Path(model_system.resultdata.path) / 'transit_congestion.csv'
        self.transit_line_congestions = pd.DataFrame(columns=['line_id', 'congestion_max_aht', 'congestion_max_pt', 'congestion_max_iht', 'congestion_avg_aht', 'congestion_avg_pt', 'congestion_avg_iht', 'total_capacity_aht', 'total_capacity_pt', 'total_capacity_iht', 'mode']).set_index('line_id')
    
    def on_assignment_complete(self,assignment_period: 'AssignmentPeriod',
                                    iteration: Union[int, str],
                                    demand: Dict[str, 'np.ndarray'],
                                    impedance: Dict[str, Dict[str, 'np.ndarray']],
                                    scenario: 'Scenario'):
        
        
        if iteration == 'last':
            # This will run three times, once for each assignment period (aht, pt, iht)
            ap_name = assignment_period.name # aht, pt, or iht
            network = scenario.get_network()
            transit_lines = network.transit_lines()
            for transit_line in transit_lines:
                line_id = transit_line.id
                mode = transit_line.mode
                vehicle_seated_capacity = transit_line.vehicle.seated_capacity
                vehicle_total_capacity = transit_line.vehicle.total_capacity
                line_total_hourly_capacity = (60 / transit_line[f'@hw_{ap_name}']) * vehicle_total_capacity if transit_line[f'@hw_{ap_name}'] < 999 else 0
                # This can be added to the dataframe as a new column if needed
                line_seated_hourly_capacity = (60 / transit_line[f'@hw_{ap_name}']) * vehicle_seated_capacity if transit_line[f'@hw_{ap_name}'] < 999 else 0
                segment_congestions = []
                for segment in transit_line.segments():
                    congestion = (segment[f'@transit_wor_vol_{ap_name}'] + segment[f'@transit_lei_vol_{ap_name}']) / line_total_hourly_capacity if line_total_hourly_capacity > 0 else 0
                    segment_congestions.append(congestion)
                max_congestion = max(segment_congestions)
                avg_congestion = np.mean(segment_congestions)

                # Prepare the data for the current assignment period
                transit_line_congestion = {
                    f'congestion_max_{ap_name}': max_congestion,
                    f'congestion_avg_{ap_name}': avg_congestion,
                    f'total_capacity_{ap_name}': line_total_hourly_capacity,
                    'mode': mode.id
                }

                # Update or insert the row for the current line_id
                if line_id in self.transit_line_congestions.index:
                    # Update existing row
                    for key, value in transit_line_congestion.items():
                        self.transit_line_congestions.at[line_id, key] = value
                else:
                    # Insert new row
                    transit_line_congestion['line_id'] = line_id
                    self.transit_line_congestions = pd.concat(
                        [self.transit_line_congestions, pd.DataFrame([transit_line_congestion]).set_index('line_id')], sort=False
                    )     

    def on_daily_results_aggregated(self, assignment_model: 'EmmeAssignmentModel', day_network: 'Network'):
        # This will run after all the data has been collected from each assignment period
        # congested_lines = self.transit_line_congestions[(self.transit_line_congestions['congestion_max_aht'] > 1)|(self.transit_line_congestions['congestion_max_iht'] > 1)]
        # If there are any congested lines, print an info log
        
        congested_lines = self.transit_line_congestions[(self.transit_line_congestions['congestion_max_aht'] > 1)|(self.transit_line_congestions['congestion_max_iht'] > 1)]
        if not congested_lines.empty:
            log.info(f"There are {len(congested_lines)} transit lines whose ridership exceeds capacity. Turn on debug logging to see details.")
            congested_lines.apply(
                lambda row: log.debug(f"Line {row.name} has a maximum congestion of {row['congestion_max_aht']:.2f} in AHT and {row['congestion_max_iht']:.2f} in IHT."), axis=1
            )

        self.transit_line_congestions = self.transit_line_congestions.sort_index()
        self.transit_line_congestions.to_csv(self.transit_result_path, sep=';', float_format='%.3f')
    
