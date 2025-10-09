from abc import ABC
from typing import TYPE_CHECKING, Dict, Union
from pathlib import Path

if TYPE_CHECKING:
    import pandas as pd
    import numpy as np
    from datahandling.zonedata import ZoneData
    from modelsystem import ModelSystem
    from datatypes.purpose import TourPurpose
    from datatypes.demand import Demand
    from assignment.departure_time import DepartureTimeModel
    from assignment.abstract_assignment import Period
    from assignment.emme_bindings.mock_project import Network
    from assignment.emme_bindings.mock_project import Scenario
    from assignment.assignment_period import AssignmentPeriod
    from demand.trips import DemandModel
    from argparse import Namespace
    from utils.validation import Validation
    from assignment.emme_assignment import EmmeAssignmentModel, AssignmentModel

class ModelSystemEventListener(ABC):
   
    def __init__(self):
        pass
    
    def on_simulation_started(self, forecastdata_path: Path, result_path: Path, args: 'Namespace') -> None:
        """
        Event handler for when a simulation starts.
        Args:
            forecastdata (Path): The path to the forecast data file.
            result_path (Path): The path where the simulation results will be stored.
            args (Namespace): Additional arguments for the simulation.
        """
        pass
    
    def on_simulation_complete(self) -> None:
        """
        Event handler that is called when simulation is complete.
        """
        pass

    def on_validation_initialized(self, validation: 'Validation', validation_path: Path) -> None:
        """
        Event handler that is called when validation is initialized.

        Args:
            validation (Validation): The validation object.
            validation_path (Path): The path to the validation data.
        """

    def on_zone_data_loaded(self, base_data: 'ZoneData', forecast_data: 'ZoneData') -> None:
        """
        Event handler that is called when zone data is loaded.

        Args:
            base_data (ZoneData): The loaded base zone data.
            forecast_data (ZoneData): The loaded forecast zone data.
        """
        pass

    def on_model_system_initialized(self,
                                    model_system: 'ModelSystem',
                                    zone_data_path: str, 
                                    base_zone_data_path: str, 
                                    base_matrices_path: str,
                                    results_path: str, 
                                    assignment_model: 'AssignmentModel', 
                                    name: str) -> None:
        """
        Event handler that is called at the beginning of model system initialization.

        Args:
            model_system (ModelSystem): The model system.
            zone_data_path (str): The path to the zone data.
            base_zone_data_path (str): The path to the base zone data.
            base_matrices_path (str): The path to the base matrices.
            results_path (str): The path to the results.
            assignment_model (AssignmentModel): The assignment model.
            name (str): The name of the model system.
        """
        pass
    
    def on_iteration_started(self, iteration: Union[int, str], previous_impedance: Dict[str, Dict[str, 'np.ndarray']]) -> None:
        """
        Event handler that is called when an iteration is started.

        Args:
            iteration (int | str): The iteration number.
        """
        pass

    def on_car_density_updated(self, iteration: Union[int, str], prediction: 'pd.Series' ) -> None:
        """
        Event handler that is called when car density is updated.

        Args:
            iteration (int | str): The iteration number.
            prediction (pandas.Series): The updated car density prediction.
        """
        pass
    
    def on_base_demand_assigned(self, impedance: Dict[str, Dict[str, 'np.ndarray']]) -> None:
        """
        Event handler that is called when base demand has been assigned.

        Args:
            impedance (dict): The impedance matrices.
        """
        pass

    def on_population_segments_created(self, dm: 'DemandModel') -> None:
        """
        Event handler that is called when population segments have been created.

        Args:
            dm (DemandModel): The demand model.
        """
        pass
    
    def on_demand_model_tours_generated(self, dm: 'DemandModel') -> None:
        """
        Event handler that is called when demand model tours have been generated.

        Args:
            dm (DemandModel): The demand model.
        """
        pass
    
    def on_purpose_demand_calculated(self, purpose: 'TourPurpose', demand: Dict[str, 'Demand']) -> None:
        """
        Event handler that is called when purpose demand has been calculated.

        Args:
            dm (DemandModel): The demand model.
        """
        pass

    def on_internal_demand_added(self, dtm: 'DepartureTimeModel') -> None:
        """
        Event handler that is called when internal demand has been calculated.

        Args:
            dtm (DepartureTimeModel): The departure time model.
        """
        pass

    def on_external_demand_calculated(self, demand: Dict[str, 'Demand']) -> None:
        """
        Event handler that is called when external demand has been calculated.

        Args:
            dtm (DepartureTimeModel): The departure time model.
        """
        pass
    
    def on_demand_calculated(self, iteration: Union[int, str], dtm: 'DepartureTimeModel') -> None:
        """
        Event handler that is called when all demands has been added to the DTM.

        Args:
            iteration (int | str): The iteration number.
            dtm (DepartureTimeModel): The departure time model.
        """
        pass
    
    def on_time_period_assigned(self, iteration: Union[int, str], ap: 'Period', impedance: Dict[str, Dict[str, 'np.ndarray']]) -> None:
        """
        Event handler that is called when time period has been assigned.

        Args:
            iteration (int | str): The iteration number.
            ap (Period): The assignment period.
            impedance (dict): The impedance matrices.
        """
        pass

    def on_iteration_complete(self, iteration: Union[int, str], impedance: Dict[str, Dict[str, 'np.ndarray']], gap: Dict[str, float]) -> None:
        """
        Event handler that is called when an iteration is complete.

        Args:
            iteration (int | str): The iteration number.
        """
        pass

    def on_assignment_period_initialized(self, assignment_period: 'AssignmentPeriod'):
        """
        Event handler for when an EMME assignment period is initialized.
        Args:
            assignment_period (AssignmentPeriod): The assignment period that has been initialized.
        """
        pass

    def on_pedestrian_assignment_complete(self, assignment_period: 'AssignmentPeriod', emme_scenario: 'Scenario') -> None:
        """
        Event handler for when an EMME pedestrian assignment is complete.
        Args:
            assignment_period (AssignmentPeriod): The assignment period that has been initialized.
            emme_scenario (inro.emme.scenario.Scenario): The EMME scenario.
        """
        pass
 
    def on_transit_wait_time_calculated(self, assignment_period: 'AssignmentPeriod', network: 'Network') -> None:
        """
        Event handler for when the extra transit wait time has been calculated.
        Args:
            assignment_period (AssignmentPeriod): The period during which the assignment is being calculated.
            network (inro.emme.network.Network): The network object representing the transit network.
        """
        pass
    
    def on_background_traffic_calculated(self, assignment_period: 'AssignmentPeriod', network: 'Network') -> None:
        """
        Event handler for when background traffic has been calculated.
        Args:
            assignment_period (AssignmentPeriod): The period for which the traffic assignment is calculated.
            network (Network): The network on which the traffic is calculated.
        """        
        pass
    
    def on_assignment_started(self,
                              assignment_period: 'AssignmentPeriod',
                              iteration: Union[int, str],
                              demand: Dict[str, 'np.ndarray']) -> None:
        """
        Event handler for when Emme assignment is started.
        Args:
            assignment_period (AssignmentPeriod): The period during which the assignment was performed.
            iteration (Union[int, str]): The iteration number or identifier.
            demand (Dict[str, 'np.ndarray']): The demand data, represented as a dictionary where keys are strings and values are numpy arrays.
        """
        pass
    
    def on_assignment_complete(self,
                                    assignment_period: 'AssignmentPeriod',
                                    iteration: Union[int, str],
                                    demand: Dict[str, 'np.ndarray'],
                                    impedance: Dict[str, Dict[str, 'np.ndarray']],
                                    scenario: 'Scenario') -> None:
        """
        Event handler for when Emme assignment is complete.
        Args:
            assignment_period (AssignmentPeriod): The period during which the assignment was performed.
            iteration (Union[int, str]): The iteration number or identifier.
            demand (Dict[str, 'np.ndarray']): The demand data, represented as a dictionary where keys are strings and values are numpy arrays.
            impedance (Dict[str, Dict[str, 'np.ndarray']]): The impedance data, represented as a nested dictionary where the outer keys are strings, 
                                                        the inner keys are also strings, and the values are numpy arrays.
            scenario (Scenario): The scenario for which the assignment was performed.
        """
        pass

    def on_car_and_transit_vdfs_set(self, assignment_period: 'AssignmentPeriod', network: 'Network') -> None:
        """
        Event handler for when car and transit VDFs have been set.
        Args:
            assignment_period (AssignmentPeriod): The period during which the assignment is being calculated.
            network (inro.emme.network.Network): The network object representing the transit network.
        """
        pass
    
    def on_bike_vdfs_set(self, assignment_period: 'AssignmentPeriod', network: 'Network') -> None:
        """
        Event handler for when bike VDFs have been set.
        Args:
            assignment_period (AssignmentPeriod): The period during which the assignment is being calculated.
            network (inro.emme.network.Network): The network object representing the transit network.
        """
        pass
    
    def on_road_cost_calculated(self, assignment_period: 'AssignmentPeriod', network: 'Network') -> None:
        """
        Event handler for when road costs have been calculated.
        Args:
            assignment_period (AssignmentPeriod): The period during which the assignment is being calculated.
            network (inro.emme.network.Network): The network object representing the transit network.
        """
        pass
    
    def on_boarding_penalties_calculated(self, assignment_period: 'AssignmentPeriod', network: 'Network') -> None:
        """
        Event handler for when boarding penalties have been calculated.
        Args:
            assignment_period (AssignmentPeriod): The period during which the assignment is being calculated.
            network (inro.emme.network.Network): The network object representing the transit network.
        """
        pass
    
    def on_parking_time_calculated(self, zone_data: 'ZoneData', parking_time: 'np.ndarray') -> None:
        """
        Event handler for when parking time has been calculated.
        Args:
            purpose (Purpose): The purpose for which parking time has been calculated.
            parking_time ('np.ndarray'): The parking time data.
        """
        pass

    def on_garbage_trips_generated(self, garbage_generated) -> None:
        """
        Event handler for when garbage trips have been generated.
        Args:
            zone_data (ZoneData): The zone data.
            garbage_generated (np.ndarray): The generated garbage trips data.
        """
        pass
    
    def on_daily_results_aggregated(self, assignment_model: 'EmmeAssignmentModel', day_network: 'Network') -> None:
        """
        Event handler for when daily results have been aggregated.
        Args:
            assignment_model (EmmeAssignmentModel): The assignment model.
            day_network (Network): The Emme network for the daily results.
        """
        pass


