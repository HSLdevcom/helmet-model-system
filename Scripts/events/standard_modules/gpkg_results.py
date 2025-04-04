from pathlib import Path
from typing import TYPE_CHECKING, Union
import pandas as pd
import numpy as np


from events.model_system_event_listener import ModelSystemEventListener

if TYPE_CHECKING:
    from modelsystem import ModelSystem
    from datatypes.purpose import TourPurpose
    from assignment.emme_assignment import AssignmentModel

class GpkgResult(ModelSystemEventListener):
    """
    A class to print zone and network data to results directory.
    """
    result_path: Path
    """ The path to the result file. """
    
    is_last_iteration: bool
    """ Flag to indicate if this is the last iteration. """
    
    model_system: 'ModelSystem'
    """ The model system instance. """

    zone_gpkg_path: Path
    """ The path to the zone data. """
    
    parking_time: pd.Series
    
    def __init__(self):
        super().__init__()
        self.is_last_iteration = False
    
    
    def on_model_system_initialized(self,
                                    model_system: 'ModelSystem',
                                    zone_data_path: str, 
                                    base_zone_data_path: str, 
                                    base_matrices_path: str,
                                    results_path: str, 
                                    assignment_model: 'AssignmentModel', 
                                    name: str) -> None:
        # Get result path when model system is initialized
        self.model_system = model_system
        self.result_path = Path(model_system.resultdata.path) / 'model_data.gpkg'
        self.zone_gpkg_path = Path(zone_data_path) / 'zones.gpkg'


    def on_iteration_started(self, iteration, previous_impedance):
        if iteration == 'last' or iteration is None:
            self.is_last_iteration = True
    
    def on_parking_time_calculated(self, purpose: 'TourPurpose', parking_time: np.ndarray):
        if not self.is_last_iteration:
            return
        # Create a DataFrame from parking_time using purpose.zone_data zone numbers as index
        self.parking_itme_df = pd.DataFrame(parking_time, index=purpose.zone_data.zone_numbers, columns=['parking_time'])
        self.parking_itme_df.index.name = 'zone_id'
        # Save the DataFrame to a CSV file
    
    def on_iteration_complete(self, iteration: Union[int, str], impedance, gap):
        if not self.is_last_iteration:
            return
        
        zone_data_df = self.model_system.zdata_forecast.get_zone_data()
        try:
            import geopandas as gpd
            zone_gdf = gpd.read_file(self.zone_gpkg_path, layer='polygons')
            # Join zone_gdf and zone_data_df using the index
            zone_gdf = zone_gdf.join(zone_data_df, how='left')
            # Join parking_time into zone_gdf
            zone_gdf = zone_gdf.join(self.parking_itme_df, how='left')
            # Write the updated GeoDataFrame to the result path
            zone_gdf.to_file(self.result_path, layer='zone_data', driver='GPKG')
        except ImportError:
            raise ImportError("geopandas is not installed. Please install it to use this feature to export GPKG data.")
        
    def on_daily_results_aggregated(self, assignment_model, day_network):
        if not self.is_last_iteration:
            return
        try:
            import geopandas as gpd
            from .geodata_helpers import (
                get_links,
                get_nodes,
                get_transit_lines,
                get_transit_segments
            )
        except ImportError:
            raise ImportError("geopandas is not installed. Please install it to use this feature to export GPKG data.")

        scenario = assignment_model.emme_scenario
        
        get_links(day_network, scenario).to_file(self.result_path, layer='links', driver='GPKG')
        get_nodes(day_network, scenario).to_file(self.result_path, layer='nodes', driver='GPKG')
        # Get the network and scenario from the assignment model
        gpd.GeoDataFrame(get_transit_lines(day_network, scenario), geom=None).to_file(self.result_path, layer='transit_lines', driver='GPKG')
        gpd.GeoDataFrame(get_transit_segments(day_network, scenario), geom=None).to_file(self.result_path, layer='transit_segments', driver='GPKG')
        # Get links and nodes from the network and scenario
