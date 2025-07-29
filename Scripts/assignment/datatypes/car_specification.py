from __future__ import annotations
from typing import Any, Dict, List, Union
from assignment.datatypes.path_analysis import PathAnalysis3h
import parameters.assignment as param
from assignment.datatypes.car import Car
from collections.abc import Callable

class CarSpecification:
    """
    Car assignment specification.

    Parameters
    ----------
    extra : assignment_period.AssignmentPeriod.extra()
        Function for generating extra attribute name
        for specific assignment period
    emme_matrices : dict
        key : str
                Assignment class (car_work/transit_leisure/...)
        value : dict
            key : str
                Impedance type (time/cost/dist/...)
            value : str
                Emme matrix id
    """
    def __init__(self,
                 extra: Callable, 
                 emme_matrices: Dict[str, Union[str, Dict[str, str]]],
                 ap3h_emme_matrices: Dict[str, Dict[str,Any]]):
        self._modes = {}
        self._freight_modes = list(param.freight_dist_unit_cost)
        matrices = {"car_work":ap3h_emme_matrices["car_work"]["demand"],
                    "car_leisure":ap3h_emme_matrices["car_leisure"]["demand"],
                    "trailer_truck":ap3h_emme_matrices["trailer_truck"]["demand"],
                    "truck":ap3h_emme_matrices["truck"]["demand"],
                    "van":ap3h_emme_matrices["van"]["demand"]}
        for mode in param.assignment_modes:
            if mode in self._freight_modes:
                kwargs = {
                    "link_costs": "length",
                    "value_of_time_inv": param.freight_dist_unit_time,
                }
            else:
                kwargs = {"link_costs": extra("total_cost")}
            self._modes[mode] = Car(mode, extra, emme_matrices[mode], **kwargs)
            self._modes[mode].spec["path_analyses"].append(PathAnalysis3h(extra(mode),extra(mode)[:-1],matrices[mode]).spec)
        self._spec: Dict[str, Any] = {
            "type": "SOLA_TRAFFIC_ASSIGNMENT",
            "background_traffic": {
                "link_component": param.background_traffic_attr,
                "add_transit_vehicles": False,
            },
            "performance_settings": param.performance_settings,
            "stopping_criteria": None, # This is defined later
        }

    def spec(self, lightweight: bool = False) -> Dict[str, Any]:
        self._spec["classes"] = [self._modes[mode].spec for mode in self._modes
            if not lightweight or mode not in self._freight_modes]
        return self._spec
