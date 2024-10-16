from __future__ import annotations
from typing import Any, Dict, Union
import parameters.assignment as param
from assignment.datatypes.journey_level import JourneyLevel


class TransitSpecification:
    """
    Transit assignment specification.
    
    Two journey levels are added at a later stage.
    At the second level an extra boarding penalty is implemented,
    hence a transfer penalty. Waiting time length is also different. 
    Walk only trips are not allowed.

    Parameters
    ----------
    segment_results : dict
        key : str
            Segment result (transit_volumes/...)
        value : str
            Extra attribute name (@transit_work_vol_aht/...)
    headway_attribute : str
        Line attribute where headway is stored
    emme_matrices : dict
        key : str
            Impedance type (time/cost/dist/...)
        value : str
            Emme matrix id
    count_zone_boardings : bool (optional)
        Whether assignment is performed only to count fare zone boardings
    """
    def __init__(self, 
                 segment_results: Dict[str,str], 
                 headway_attribute: str,
                 emme_matrices: Dict[str, Union[str, Dict[str, str]]], 
                 count_zone_boardings: bool = False):
        no_penalty = dict.fromkeys(["at_nodes", "on_lines", "on_segments"])
        no_penalty["global"] = {
            "penalty": 0, 
            "perception_factor": 1,
        }
        self.transit_spec: Dict[str, Any] = {
            "type": "EXTENDED_TRANSIT_ASSIGNMENT",
            "modes": param.transit_assignment_modes,
            "demand": emme_matrices["demand"],
            "waiting_time": {
                "headway_fraction": param.standard_headway_fraction,
                "effective_headways": headway_attribute,
                "spread_factor": 1,
                "perception_factor": param.waiting_time_perception_factor
            },
            "boarding_time": {
                "global": None,
                "at_nodes": None,
                "on_lines": {
                    "penalty": param.boarding_penalty_attr,
                    "perception_factor": 1
                },
                "on_segments": param.extra_waiting_time,
            },
            # Boarding cost is defined for each journey level separately,
            # so here we just set the default to zero.
            "boarding_cost": no_penalty,
            "in_vehicle_time": {
                "perception_factor": param.in_vehicle_time_perception_attr
            },
            "aux_transit_time": param.aux_transit_time,
            "flow_distribution_at_origins": {
                "choices_at_origins": "OPTIMAL_STRATEGY",
            },
            "flow_distribution_at_regular_nodes_with_aux_transit_choices": {
                "choices_at_regular_nodes": "OPTIMAL_STRATEGY",
            },
            "flow_distribution_between_lines": {
                "consider_total_impedance": False
            },
            "journey_levels": None,
            "performance_settings": param.performance_settings,
        }
        self.ntw_results_spec = {
            "type": "EXTENDED_TRANSIT_NETWORK_RESULTS",
            "on_segments": segment_results,
            }
        subset = "by_mode_subset"
        self.transit_result_spec = {
            "type": "EXTENDED_TRANSIT_MATRIX_RESULTS",
            subset: {
                "modes": param.transit_modes,
                "distance": emme_matrices["dist"],
            },
        }
        if count_zone_boardings:
            jlevel1 = JourneyLevel(
                headway_attribute, boarded=False, count_zone_boardings=True)
            jlevel2 = JourneyLevel(
                headway_attribute, boarded=True, count_zone_boardings=True)
            bcost = "actual_total_boarding_costs"
            self.transit_result_spec[subset][bcost] = emme_matrices[bcost]
        else:
            jlevel1 = JourneyLevel(headway_attribute, boarded=False)
            jlevel2 = JourneyLevel(headway_attribute, boarded=True)
            self.transit_result_spec["total_impedance"] = emme_matrices["time"]
            (self.transit_result_spec[subset]
                                     ["modes"]) = param.transit_assignment_modes
            for trip_part, matrix_id in emme_matrices["total"].items():
                self.transit_result_spec[trip_part] = matrix_id
            for trip_part, matrix_id in emme_matrices[subset].items():
                self.transit_result_spec[subset][trip_part] = matrix_id
        self.transit_spec["journey_levels"] = [jlevel1.spec, jlevel2.spec]
