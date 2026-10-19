from __future__ import annotations
from typing import Any, Dict, Union
import parameters.assignment as param
from assignment.datatypes.journey_level import JourneyLevel


class WalkSpecification:
    """
    Walk assignment specification.

    Two journey levels are added at a later stage.
    At the second level an extra boarding penalty is implemented,
    hence a transfer penalty. Waiting time length is also different. 
    Walk only trips are not allowed.

    Parameters
    ----------
    emme_matrices : dict
        key : str
            Impedance type (time/cost/dist/...)
        value : str
            Emme matrix id
    """
    def __init__(self, 
                 emme_matrices: Dict[str, Union[str, Dict[str, str]]]):
        self.walk_spec: Dict[str, Any] = {
            "type": "EXTENDED_TRANSIT_ASSIGNMENT",
            "modes": param.aux_modes,
            "demand": emme_matrices["demand"],
            "waiting_time": {
                "headway_fraction": 0.5,
                "effective_headways": "hdw",
                "spread_factor": 1,
                "perception_factor": 1
            },
            "boarding_time": {
                "global": {
                    "penalty": 0,
                    "perception_factor": 1
                },
                "at_nodes": None,
                "on_lines": None,
                "on_segments": None
            },
            "boarding_cost": {
                "global": {
                    "penalty": 0,
                    "perception_factor": 1
                },
                "at_nodes": None,
                "on_lines": None,
                "on_segments": None
            },
            "in_vehicle_time": {
                "perception_factor": 1
            },
            "in_vehicle_cost": None,
            "aux_transit_time": {
                "perception_factor": 1
            },
            "aux_transit_cost": None,
            "aux_transit_by_mode": None,
            "flow_distribution_at_origins": {
                "choices_at_origins": "OPTIMAL_STRATEGY",
                "fixed_proportions_on_connectors": None
            },
            "flow_distribution_at_regular_nodes_with_aux_transit_choices": {
                "choices_at_regular_nodes": "OPTIMAL_STRATEGY"
            },
            "flow_distribution_between_lines": {
                "consider_total_impedance": False
            },
            "connector_to_connector_path_prohibition": None,
            "circular_lines": {
                "stay": False
            },
            "od_results": {
                "total_impedance": emme_matrices["time"]
            },
            "results": {
                "aux_transit_volumes_by_mode": [
                    {
                        "mode": mode,
                        "volume": None
                    } for mode in param.aux_modes
                ]
            },
            "journey_levels": [],
            "performance_settings": param.performance_settings,
        }

        self.strategy_analysis_spec = {
            "type": "EXTENDED_TRANSIT_STRATEGY_ANALYSIS",
            "trip_components": {
                "boarding": None,
                "in_vehicle": None,
                "alighting": None,
                "aux_transit": "length",
            },
            "sub_path_combination_operator": "+",
            "sub_strategy_combination_operator": "average",
            "selected_demand_and_transit_volumes": {
                "sub_strategies_to_retain": "ALL",
                "selection_threshold": {
                    "lower": -999999,
                    "upper": 999999
                }
            },
            "analyzed_demand": None,
            "constraint": None,
            "results": {
                "strategy_values": emme_matrices["dist"],
                "selected_demand": None,
                "transit_volumes": None,
                "aux_transit_volumes": None,
                "total_boardings": None,
                "total_alightings": None
            }
        }

        #self.transit_result_spec["total_impedance"] = emme_matrices["time"]
