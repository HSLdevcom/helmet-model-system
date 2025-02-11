from abc import ABC
from typing import TYPE_CHECKING, Dict, Union
from sys import gettrace
from utils import log
from pathlib import Path
import importlib.util

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

class ModelSystemEventListener(ABC):
   
    def __init__(self):
        pass

    def on_zone_data_loaded(self, base_data: 'ZoneData', forecast_data: 'ZoneData') -> None:
        """
        Event handler that is called when zone data is loaded.

        Args:
            base_data (ZoneData): The loaded base zone data.
            forecast_data (ZoneData): The loaded forecast zone data.
        """
        pass

    def on_model_system_initialized(self, model_system: 'ModelSystem') -> None:
        """
        Event handler that is called when the model system is initialized.

        Args:
            model_system (ModelSystem): The model system.
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
 
    def on_transit_wait_time_calculated(self, assignment_period: 'AssignmentPeriod' ,network: 'Network') -> None:
        """
        Event handler for when the extra transit wait time has been calculated.
        Args:
            assignment_period (AssignmentPeriod): The period during which the assignment is being calculated.
            network (inro.emme.network.Network): The network object representing the transit network.
        """
        pass
    
    def on_background_traffic_calculated(self, assignment_period: 'AssignmentPeriod' ,network: 'Network') -> None:
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
    
    def on_parking_time_calculated(self, purpose: 'TourPurpose', parking_time: 'np.ndarray') -> None:
        """
        Event handler for when parking time has been calculated.
        Args:
            purpose (Purpose): The purpose for which parking time has been calculated.
            parking_time ('np.ndarray'): The parking time data.
        """
        pass


class EventHandler(ModelSystemEventListener):
    """Event handler that calls all equivalent methods in all other ModelSystemEventListener classes."""
    def __init__(self):
        """Initialize the EventHandler.

        Args:
            model_system (ModelSystem): ModelSystem instance.
        """
        super().__init__()
        self.listeners = []
        self._create_methods()

    def register_listener(self, listener: ModelSystemEventListener):
        self.listeners.append(listener)

    def load_listeners(self, listener_path: Path):
        """Load all listeners from a given path.

        Args:
            listener_path (str): The path to the listeners.
        """
        for file_path in listener_path.glob("*.py"):
            if file_path.name != "__init__.py":
                module_name = file_path.stem
                spec = importlib.util.spec_from_file_location(module_name, file_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                for attr_name in dir(module):
                    attr = getattr(module, attr_name)
                    if isinstance(attr, type) and issubclass(attr, ModelSystemEventListener) and attr is not ModelSystemEventListener:
                        self.register_listener(attr())
                        log.info(f"Loaded listener {attr.__name__} from {file_path}")


    def _create_methods(self):
        """Create methods that call all equivalent methods in all other ModelSystemEventListener classes.
        Methods area automatically created for all methods that start with "on_" in all ModelSystemEventListener classes.
        """
        for method_name in dir(ModelSystemEventListener):
            if method_name.startswith("on_") and callable(getattr(ModelSystemEventListener, method_name)):
                setattr(self, method_name, self._create_method(method_name))
                
    def _create_method(self, method_name):
        """Create a method that calls all equivalent methods in all other ModelSystemEventListener classes.

        Args:
            method_name (str): name of the method to create.
        """
        def method(*args, **kwargs):
            for listener in self.listeners:
                try:
                    getattr(listener, method_name)(*args, **kwargs)
                except Exception as e:
                    if gettrace() is not None:
                        # Re-raise exception if debugger is attached
                        raise e
                    log.error(f"Error in {listener.__class__.__name__}.{method_name}: {e}")
        return method