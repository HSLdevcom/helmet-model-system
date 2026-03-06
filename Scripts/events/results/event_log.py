from pathlib import Path
from typing import Dict, List, Union, TYPE_CHECKING, cast
import pandas as pd
import numpy as np
from datahandling.zonedata import ZoneData
from datatypes.purpose import SecDestPurpose
from demand.personal_internal import DemandModel
import utils.log as log
from parameters.tour_generation import tour_generation
from parameters.zone import savu_intervals

from events.model_system_event_listener import ModelSystemEventListener

if TYPE_CHECKING:
    from modelsystem import ModelSystem
    from datatypes.demand import Demand
    from datatypes.purpose import TourPurpose
    from assignment.emme_bindings.mock_project import Scenario
    from assignment.assignment_period import AssignmentPeriod
    from assignment.emme_assignment import EmmeAssignmentModel
    from assignment.emme_bindings.mock_project import Network
    from assignment.emme_assignment import AssignmentModel




class EventLog(ModelSystemEventListener):
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

    def on_validation_initialized(self, validation, validation_path):
        log.debug("EVENT: Validation")
    
    def on_simulation_started(self, forecastdata_path, result_path, args):
        log.debug("EVENT: Simulation started")
    
    def on_model_system_initialized(self, model_system, zone_data_path, base_zone_data_path, base_matrices_path, results_path, assignment_model, name):
        log.debug("EVENT: Model system initialized")
    
    def on_zone_data_loaded(self, base_data, forecast_data):
        log.debug("EVENT: Zone data loaded")
    
    def on_population_segments_created(self, dm):
        log.debug("EVENT: Population segments created")
    
    def on_parking_time_calculated(self, zone_data, parking_time):
        log.debug("EVENT: Parking time calculated")
    
    def on_demand_model_tours_generated(self, dm):
        log.debug("EVENT: Demand model tours generated")
    
    def on_purpose_demand_calculated(self, purpose, demand, pnr_iteration=0):
        log.debug("EVENT: Purpose demand calculated")
    
    def on_base_demand_assigned(self, impedance):
        log.debug("EVENT: Base demand assigned")
    
    def on_iteration_started(self, iteration, previous_impedance):
        log.debug("EVENT: Iteration started")
    
    def on_car_density_updated(self, iteration, prediction, cdm):
        log.debug("EVENT: Car density updated")
    
    def on_internal_demand_added(self, dtm):
        log.debug("EVENT: Internal demand added")
    
    def on_external_demand_calculated(self, demand):
        log.debug("EVENT: External demand calculated")
    
    def on_demand_calculated(self, iteration, dtm):
        log.debug("EVENT: On demand calculated")
    
    def on_time_period_assigned(self, iteration, ap, impedance, tp, previous_iter_impedance):
        log.debug("EVENT: On time period assigned")
    
    def on_iteration_complete(self, iteration, impedance, gap):
        log.debug("EVENT: On iteration complete")
    
    def on_assignment_period_initialized(self, assignment_period):
        log.debug("EVENT: On assignment period initialized")
    
    def on_assignment_started(self, assignment_period, iteration, demand):
        log.debug("EVENT: On assignment started")
    
    def on_assignment_complete(self, assignment_period, iteration, demand, impedance, scenario):
        log.debug("EVENT: On assignment complete")
    
    def on_car_and_transit_vdfs_set(self, assignment_period, network):
        log.debug("EVENT: On car and transit vdfs set")
    
    def on_bike_vdfs_set(self, assignment_period, network):
        log.debug("EVENT: On bike vdfs set")
    
    def on_background_traffic_calculated(self, assignment_period, network):
        log.debug("EVENT: On background traffic calculated")
    
    def on_road_cost_calculated(self, assignment_period, network):
        log.debug("EVENT: On road cost calculated")
    
    def on_boarding_penalties_calculated(self, assignment_period, network):
        log.debug("EVENT: On boarding penalties calculated")
    
    def on_pedestrian_assignment_complete(self, assignment_period, emme_scenario):
        log.debug("EVENT: On pedestrian assignment complete")
    
    def on_transit_wait_time_calculated(self, assignment_period, network):
        log.debug("EVENT: On transit wait time calculated")
    
    def on_daily_results_aggregated(self, assignment_model, day_network, network_aggregations):
        log.debug("EVENT: On daily results aggregated")
    
    def on_garbage_trips_generated(self, garbage_generated):
        log.debug("EVENT: On garbage trips generated")
    
    def on_simulation_complete(self):
        log.debug("EVENT: On simulation complete")
    