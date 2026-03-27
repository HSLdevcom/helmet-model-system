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
from utils.zone_interval import ZoneIntervals

if TYPE_CHECKING:
    from modelsystem import ModelSystem
    from datatypes.demand import Demand
    from datatypes.purpose import TourPurpose
    from assignment.emme_bindings.mock_project import Scenario
    from assignment.assignment_period import AssignmentPeriod
    from assignment.emme_assignment import EmmeAssignmentModel
    from assignment.emme_bindings.mock_project import Network
    from assignment.emme_assignment import AssignmentModel




class AccessibilityResults(ModelSystemEventListener):
    """
    A class to print accessibility results.
    """
    
    def __init__(self):
        super().__init__()
    
    def on_model_system_initialized(self,
                                    model_system: 'ModelSystem',
                                    zone_data_path: Path, 
                                    base_zone_data_path: Path, 
                                    base_matrices_path: Path,
                                    results_path: Path, 
                                    assignment_model: 'AssignmentModel', 
                                    name: str):
        self.ms = model_system

    def on_population_segments_created(self,
                                    dm: 'DemandModel'):
        self.dm = dm
        acc_columns = ["zone_id"]
        for tp in dm.tour_purposes:
            tp
            for mode in tp.modes:
                acc_columns.append(f"{tp}_{mode[:1]}")
        self.accessibilities = pd.DataFrame(columns=acc_columns).set_index("zone_id")
        self.zdata = self.ms.zdata_base

        #self.transit_line_congestions = pd.DataFrame(columns=['line_id', 'congestion_max_aht', 'congestion_max_pt', 'congestion_max_iht', 'congestion_avg_aht', 'congestion_avg_pt', 'congestion_avg_iht', 'total_capacity_aht', 'total_capacity_pt', 'total_capacity_iht', 'mode']).set_index('line_id')

    def on_calc_accessibility(self, impedance, model):
        """Calculate logsum-based accessibility measures.

        Individual dummy variables are not included.

        Parameters
        ----------
        impedance : dict
            Mode (car/transit/bike/walk) : dict
                Type (time/cost/dist) : numpy 2-d matrix
                    Impedances
        """
        mode_expsum = model._calc_utils(impedance)

        # Calculate sustainable and car accessibility
        sustainable_sum = np.zeros_like(mode_expsum)
        for mode in model.mode_choice_param:
            if mode != "car":
                sustainable_sum += model.mode_exps[mode]
        logsum = pd.Series(
            np.log(sustainable_sum), model.purpose.zone_numbers)
        self.ms.resultdata.print_data(
            logsum, "sustainable_accessibility.txt", model.purpose.name)
        #Note: Shared results are problematic, but for now we save them through this function
        model.purpose.access = (model.money_utility
                               * model.zone_data[model.purpose.name])
        model.purpose.sustainable_access = model.money_utility * logsum
        model.purpose.car_access = (model.money_utility
                                   * model.zone_data[model.purpose.name + "_c"])

        #Calculate workplace-based accessibility
        if model.purpose.name in ("hw", "wh"):
            # Transform into person equivalents
            param = model.mode_choice_param
            normalization = 1 / sum([param[mode]["constant"][0]
                for mode in param])
            workforce = ((normalization*mode_expsum)
                            **(1/param["car"]["log"]["logsum"]))
            workforce = pd.Series(workforce, model.purpose.zone_numbers)
            self.ms.resultdata.print_data(
                workforce, "workplace_accessibility.txt", model.purpose.name)
            workplaces = model.zone_data["workplaces"][model.bounds]
            aggregate = ZoneIntervals("areas").averages(workforce, workplaces)
            self.ms.resultdata.print_data(
                aggregate, "workplace_accessibility_areas.txt",
                model.purpose.name)
    
    def on_purpose_demand_calculated(self, purpose, demand, pnr_iteration=0, estimation_mode=False):
        """
        Print logsums for each mode
        """
        for mode in purpose.modes:
            if purpose.name+"_"+mode[0] not in purpose.model.zone_data._values: return #some tours do not contain accessibility values
            self.ms.resultdata.print_data(purpose.model.zone_data._values[purpose.name+"_"+mode[0]], "accessibility.txt", purpose.name+"_"+mode[0])
        self.ms.resultdata.print_data(purpose.model.zone_data._values[purpose.name], "accessibility.txt", purpose.name)
    
    def on_iteration_complete(self, iteration, impedance, gap):
        if iteration == "last":
            logsum = 0
            sust_logsum = 0
            car_logsum = 0
            for purpose in self.dm.tour_purposes:
                if (purpose.area == "metropolitan" and purpose.orig == "home"
                        and purpose.dest != "source" and purpose.dest != "home"
                        and not isinstance(purpose, SecDestPurpose)):
                    zone_numbers = purpose.zone_numbers
                    weight = tour_generation[purpose.name]["population"]
                    logsum += weight * purpose.access
                    sust_logsum += weight * purpose.sustainable_access
                    car_logsum += weight * purpose.car_access

            self.ms.resultdata.print_data(logsum, "accessibility.txt", "all")
            self.ms.resultdata.print_data(
                sust_logsum, "sustainable_accessibility.txt", "all")
            self.ms.resultdata.print_data(car_logsum, "car_accessibility.txt", "all")
            intervals = savu_intervals
            savu = np.searchsorted(intervals, sust_logsum) + 1
            self.ms.resultdata.print_data(
                pd.Series(savu, zone_numbers), "savu.txt", "savu_zone")
