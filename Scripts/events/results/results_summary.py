from pathlib import Path
from typing import Dict, List, Union, TYPE_CHECKING
import pandas as pd
import numpy as np

from events.model_system_event_listener import ModelSystemEventListener
import parameters.assignment as param
import parameters.tour_generation as gen_param
from utils import log
from datatypes.demand import Demand
from datatypes.purpose import SecDestPurpose, TourPurpose
from parameters.zone import savu_intervals
from utils.zone_interval import ArrayAggregator, ZoneIntervals

if TYPE_CHECKING:
    from modelsystem import ModelSystem
    from assignment.abstract_assignment import AssignmentModel


class ResultSummary(ModelSystemEventListener):
    """
    A class to print result summary.
    """
    
    
    def __init__(self):
        super().__init__()
    
    def on_model_system_initialized(self,
                                    model_system: 'ModelSystem',
                                    zone_data_path: str, 
                                    base_zone_data_path: str, 
                                    base_matrices_path: str,
                                    results_path: str, 
                                    assignment_model: 'AssignmentModel', 
                                    name: str) -> None:
        self.ms = model_system
    
    def on_population_segments_created(self, dm: 'DemandModel'):
        self.zdata = self.ms.zdata_forecast
    
    def on_calc_accessibility(self, impedance, model):

        #Calculate workplace-based accessibility
        if model.purpose.name in ("hw", "wh"):
            mode_expsum = model._calc_utils(impedance)
            # Transform into person equivalents
            param = model.mode_choice_param
            normalization = 1 / sum([param[mode]["constant"][0]
                for mode in param])
            workforce = ((normalization*mode_expsum)
                            **(1/param["car"]["log"]["logsum"]))
            workforce = pd.Series(workforce, model.purpose.zone_numbers)
            workplaces = self.zdata["workplaces"][model.purpose.bounds]
            aggregate = ZoneIntervals("areas").averages(workforce, workplaces)
            names = {
                "hw": "Workplace effective density",
                "wh": "Workforce accessibility",
            }
            self.ms.resultdata.print_line(
                "{}:\t{:1.0f}".format(
                    names[model.purpose.name], aggregate["all"]),
                "result_summary")
            
    def on_demand_calculated(self, iteration: Union[str, int], dtm):
        self.ms.resultdata.print_line("\nAssigned demand", "result_summary")
        self.ms.resultdata.print_line(
            "\t" + "\t".join(param.transport_classes), "result_summary")
        
        for tp in dtm.demand:
            demand_sum_string = tp
            for ass_class in param.transport_classes:
                demand = dtm.demand[tp][ass_class]
                demand_sum_string += "\t{:8.0f}".format(demand.sum())
            self.ms.resultdata.print_line(demand_sum_string, "result_summary")
        
        #Modes for HS15 region
        hs15_modes_total = {mode: 0 for mode in self.ms.dm.purpose_dict["hw"].modes}
        for pur in self.ms.dm.purpose_dict:
            purpose = self.ms.dm.purpose_dict[pur]
            if purpose.name in ["hw","hc","hu","hs","ho","hh","wo","oo"]: 
                for mode in purpose.modes:
                    demsum = purpose.generated_tours[mode].sum()
                    if purpose.name == "hh":
                        hs15_modes_total[mode] += 0.5*demsum
                    else:
                        hs15_modes_total[mode] += demsum
        hs15_modes_shares = {m: hs15_modes_total[m]/sum(hs15_modes_total.values()) for m in hs15_modes_total}
        hs15_modes = [m for m in hs15_modes_total]
        self.ms.resultdata.print_line("\nHS15 mode shares (tour-based)", "result_summary")
        for m in hs15_modes:
            self.ms.resultdata.print_line(
                "{}\t{:1.2%}".format(m, hs15_modes_shares[m]),
                "result_summary")
            
        #Modes for HS15 region (including secondary destination)
        hs15_modes_total = {mode: 0 for mode in self.ms.dm.purpose_dict["hw"].modes}
        tour_generation = gen_param.tour_generation
        for pur in self.ms.dm.purpose_dict:
            purpose = self.ms.dm.purpose_dict[pur]
            if purpose.name in ["hw","hc","hu","hs","ho","hh","wo","oo"]: 
                for mode in purpose.modes:
                    demsum = purpose.generated_tours[mode].sum()
                    if purpose.name == "hh":
                        hs15_modes_total[mode] += demsum #one trip only
                    elif mode=="park_and_ride":
                        #2 trips split by mode
                        hs15_modes_total["transit"] += 0.5 * demsum * 2
                        hs15_modes_total["car"] += 0.5 * demsum * 2
                    else:
                        hs15_modes_total[mode] += demsum * (2+tour_generation["hoo"][purpose.name][mode]) #sec_dest included
        hs15_modes_shares = {m: hs15_modes_total[m]/sum(hs15_modes_total.values()) for m in hs15_modes_total}
        hs15_modes = [m for m in hs15_modes_total]
        self.ms.resultdata.print_line("\nHS15 mode shares (trip-based with secondary destinations)", "result_summary")
        for m in hs15_modes:
            self.ms.resultdata.print_line(
                "{}\t{:1.2%}".format(m, hs15_modes_shares[m]),
                "result_summary")

    def on_daily_results_aggregated(self, assignment_model, day_network, network_aggregations):
        kms = network_aggregations["kms"]
        self.ms.resultdata.print_line("\nVehicle kilometres", "result_summary")
        for ass_class in assignment_model.res_ass_classes:
            self.ms.resultdata.print_line(
                "{}:\t{:1.0f}".format(ass_class, kms[ass_class]),
                "result_summary")

        #Accessibility measures 
        logsum = 0
        sust_logsum = 0
        car_logsum = 0
        for purpose in self.ms.dm.tour_purposes:
            if (purpose.area == "metropolitan" and purpose.orig == "home"
                    and purpose.dest != "source" and purpose.dest != "home"
                    and not isinstance(purpose, SecDestPurpose)):
                bounds = purpose.bounds
                weight = gen_param.tour_generation[purpose.name]["population"]
                logsum += weight * purpose.access
                sust_logsum += weight * purpose.sustainable_access
                log.info(f"WEIGHT \n{weight} \nACC \n{purpose.sustainable_access}")
                car_logsum += weight * purpose.car_access
        pop = self.zdata["population"][bounds]

        self.ms.resultdata.print_line(
            "\nTotal accessibility:\t{:1.2f}".format(
                np.average(logsum, weights=pop)),
            "result_summary")
        avg_sust_logsum = np.average(sust_logsum, weights=pop)
        self.ms.resultdata.print_line(
            "Sustainable accessibility:\t{:1.2f}".format(avg_sust_logsum),
            "result_summary")
        intervals = savu_intervals
        avg_savu = np.searchsorted(intervals, avg_sust_logsum) + 1
        avg_savu += ((avg_sust_logsum - intervals[avg_savu-2])
                    / (intervals[avg_savu-1] - intervals[avg_savu-2]))
        self.ms.resultdata.print_line(
            "Average SAVU:\t{:1.4f}".format(avg_savu),
            "result_summary")
        
        # Calculate tour sums and mode shares
        tour_sum = {mode: self.ms._sum_trips_per_zone(mode, include_dests=False)
            for mode in self.ms.travel_modes}
        sum_all = sum(tour_sum.values())
        mode_shares = {}
        for mode in tour_sum:
            mode_shares[mode] = tour_sum[mode].sum() / sum_all.sum()

        self.ms.resultdata.print_line("\nMode shares", "result_summary")
        for mode in mode_shares:
            self.ms.resultdata.print_line(
                "{}\t{:1.2%}".format(mode, mode_shares[mode]),
                "result_summary")