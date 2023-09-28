from __future__ import annotations
import parameters.assignment as param
from assignment.datatypes.path_analysis import PathAnalysis
from collections.abc import Callable
from typing import Any, Dict, Optional, Union


class Car:
    """Car assignment class definition.

    Parameters
    ----------
    ass_class : str
        Assignment class (car_work/car_leisure/van/truck/trailer_truck)
    extra : assignment_period.AssignmentPeriod.extra()
        Function for generating extra attribute name
        for specific assignment period
    emme_matrices : dict
        key : str
            Impedance type (time/cost/dist/...)
        value : str
            Emme matrix id
    link_costs : str
        Link attribute where link cost is found
    value_of_time_inv : float (optional)
        Inversed value of time [min/eur], default is param.vot_inv
    """
    def __init__(self,
                 ass_class: str,
                 extra: Callable,
                 emme_matrices: Dict[str, Union[str, Dict[str, str]]],
                 link_costs: str,
                 value_of_time_inv: Optional[float]=None):
        if value_of_time_inv is None:
            value_of_time_inv = param.vot_inv[param.vot_classes[ass_class]]
        self.spec: Dict[str, Any] = {
            "mode": param.assignment_modes[ass_class],
            "demand": emme_matrices["demand"],
            "generalized_cost": {
                "link_costs": link_costs,
                "perception_factor": value_of_time_inv,
            },
            "results": {
                "link_volumes": extra(ass_class),
                "od_travel_times": {
                    "shortest_paths": emme_matrices["gen_cost"]
                }
            },
            "path_analyses": []
        }
        self.add_analysis("length", emme_matrices["dist"])
        if ass_class not in ("trailer_truck", "truck"):
            self.add_analysis(extra("toll_cost"), emme_matrices["cost"])
    
    def add_analysis (self, 
                      link_component: str, 
                      od_values: Union[int, str]):
        analysis = PathAnalysis(link_component, od_values)
        self.spec["path_analyses"].append(analysis.spec)
