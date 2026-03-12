from pathlib import Path
from typing import Dict, List, Union, TYPE_CHECKING
import pandas as pd
import numpy as np
import openmatrix as omx

from events.model_system_event_listener import ModelSystemEventListener
import parameters.assignment as param

if TYPE_CHECKING:
    from modelsystem import ModelSystem
    from assignment.abstract_assignment import AssignmentModel


class MatrixPrinting(ModelSystemEventListener):
    """
    A class for matrix printing. Matrix and estimation folders contain matrices about demand and impedance.
    """
    
    result_path: Path
    """ The path to the result file. """
    
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
        # Get result path when model system is initialized
        self.result_path = Path(results_path, name)
        self.ms = model_system
        self.ass_model = assignment_model
    
    def on_purpose_demand_calculated(self, purpose, demand, pnr_iteration=0, estimation_mode = False):
        if purpose.name == "wh": return
        if estimation_mode:
            omx_file = omx.open_file(f"{purpose.resultdata.path}/estimation/demand_{purpose.name}.omx","w")
            omx_file.create_mapping("zone_number",purpose.zone_data.all_zone_numbers)
            for mode in purpose.modes:
                if mode != "park_and_ride":
                    omx_file[mode] = purpose.orig_purpose_demand
            omx_file.close()
        self.purpose = purpose
            
    def on_time_period_assigned(self, iteration, ap, impedance, tp, previous_iter_impedance):
        if iteration=="last" and param.always_congested:     
            self._save_to_omx(impedance, tp)
        elif iteration=="last":
            impedance["time"]["transit_uncongested"] = previous_iter_impedance[tp]["time"]["transit_work"]
            self._save_to_omx(impedance, tp)
    
    def on_demand_calculated(self, iteration, dtm):
        for tp in dtm.demand:
            zone_numbers = self.ass_model.zone_numbers
            demand_sum_string = tp
            with self.ms.resultmatrices.open("demand", tp, zone_numbers, 'w') as mtx:
                for ass_class in param.transport_classes:
                    demand = dtm.demand[tp][ass_class]
                    mtx[ass_class] = demand
                    demand_sum_string += "\t{:8.0f}".format(demand.sum())
        
        #Save park and ride utility matrix
        for purpose in self.ms.dm.tour_purposes:
            if hasattr(purpose, "pnr_utility"):
                # TODO: This is a temporary solution to print the park and ride utility
                omx_file = omx.open_file(self.result_path / 'park_and_ride_utility.omx', 'w')
                omx_file.create_mapping('zone_number', self.purpose.zone_data.zone_numbers)
                omx_file['park_and_ride_utility'] = purpose.pnr_utility
                omx_file.close()

    def _save_to_omx(self, impedance, tp):
        zone_numbers = self.ass_model.zone_numbers
        for mtx_type in impedance:
            with self.ms.resultmatrices.open(mtx_type, tp, zone_numbers, 'w') as mtx:
                for ass_class in impedance[mtx_type]:
                    mtx[ass_class] = impedance[mtx_type][ass_class]