from pathlib import Path
from typing import Dict, List, Union, TYPE_CHECKING
import pandas as pd
import numpy as np

from events.model_system_event_listener import ModelSystemEventListener
import parameters.assignment as param
import parameters.tour_generation as gen_param
from utils import log
from datatypes.demand import Demand
from datatypes.purpose import TourPurpose

if TYPE_CHECKING:
    from modelsystem import ModelSystem
    from assignment.abstract_assignment import AssignmentModel


class ResultSummary(ModelSystemEventListener):
    """
    A class to analyze demand in a model system by listening to specific events.
    """
    
    mode_demands: List[Dict[str, int]]
    """ A list of dictionaries to store mode demands for each iteration. """
    result_path: Path
    """ The path to the result file. """
    
    def __init__(self):
        super().__init__()
        self.mode_demands = []
    
    def on_model_system_initialized(self,
                                    model_system: 'ModelSystem',
                                    zone_data_path: str, 
                                    base_zone_data_path: str, 
                                    base_matrices_path: str,
                                    results_path: str, 
                                    assignment_model: 'AssignmentModel', 
                                    name: str) -> None:
        # Get result path when model system is initialized
        self.result_path = Path(results_path) / name / 'mode_analysis_results.csv'
        self.ms = model_system
    
    def on_purpose_demand_calculated(self, purpose: 'TourPurpose', demand: 'Demand', pnr_iteration=0):
        demsums = {mode: purpose.generated_tours[mode].sum()
            for mode in purpose.modes}
        demand_all = float(sum(demsums.values()))
        self.mode_shares = {mode: demsums[mode] / demand_all for mode in demsums}
        purpose.resultdata.print_data(
            pd.Series(self.mode_shares),
            "mode_share.txt", purpose.name)
            
    def on_demand_calculated(self, iteration: Union[str, int], dtm):
        self.ms.resultdata.print_line("\nAssigned demand", "result_summary")
        self.ms.resultdata.print_line(
            "\t" + "\t".join(param.transport_classes), "result_summary")
        
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

        if iteration=="last":
            self.ms.resultdata.print_line("\nMode shares", "result_summary")
            for mode in self.mode_shares:
                self.ms.resultdata.print_line(
                    "{}\t{:1.2%}".format(mode, self.mode_shares[mode]),
                    "result_summary")

    def on_daily_results_aggregated(self, assignment_model, day_network, network_aggregations):
        kms = network_aggregations["kms"]
        self.ms.resultdata.print_line("\nVehicle kilometres", "result_summary")
        for ass_class in assignment_model.res_ass_classes:
            self.ms.resultdata.print_line(
                "{}:\t{:1.0f}".format(ass_class, kms[ass_class]),
                "result_summary")