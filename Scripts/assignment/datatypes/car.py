from __future__ import annotations
import parameters.assignment as param
from assignment.datatypes.path_analysis import PathAnalysis
from collections.abc import Callable
from typing import Any, Dict, Optional, Union


class Car:
    def __init__(self, 
                 ass_class: str, 
                 extra: Callable, 
                 demand_mtx: Dict[str, Dict[str, Dict[str, Union[int, str]]]], 
                 result_mtx: Dict[str, Dict[str, Dict[str, Union[int, str]]]],
                 link_costs: str, 
                 value_of_time_inv: Optional[float]=None):
        od_travel_times = result_mtx["gen_cost"][ass_class]["id"]
        if value_of_time_inv is None:
            value_of_time_inv = param.vot_inv[param.vot_classes[ass_class]]
        self.spec: Dict[str, Any] = {
            "mode": param.assignment_modes[ass_class],
            "demand": demand_mtx[ass_class]["id"],
            "generalized_cost": {
                "link_costs": link_costs,
                "perception_factor": value_of_time_inv,
            },
            "results": {
                "link_volumes": extra(ass_class),
                "od_travel_times": {
                    "shortest_paths": od_travel_times
                }
            },
            "path_analyses": []
        }
        self.add_analysis("length", result_mtx["dist"][ass_class]["id"])
        if ass_class not in ("trailer_truck", "truck"):
            self.add_analysis(extra("toll_cost"), result_mtx["cost"][ass_class]["id"])
    
    def add_analysis (self, 
                      link_component: str, 
                      od_values: Union[int, str]):
        analysis = PathAnalysis(link_component, od_values)
        self.spec["path_analyses"].append(analysis.spec)
