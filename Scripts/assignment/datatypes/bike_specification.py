from typing import Any, Dict, Union
from assignment.datatypes.path_analysis import PathAnalysis
import parameters.assignment as param

class BikeSpecification:
    """
    Class to hold bike assignment specification parameters.

    Parameters
    ----------
    emme_matrices : dict
        key : str
            Impedance type (time/cost/dist/...)
        value : str
            Emme matrix id
    """
    def __init__(self, 
                 emme_matrices: Dict[str, str]):
        self.bike_spec: Dict[str, Any] = {
            "type": "STANDARD_TRAFFIC_ASSIGNMENT",
            "classes": [
                {
                    "mode": param.bike_mode,
                    "demand": emme_matrices["demand"],
                    "results": {
                        "od_travel_times": {
                            "shortest_paths": emme_matrices["time"],
                        },
                        "link_volumes": None, # This is defined later
                    },
                    "analysis": {
                        "results": {
                            "od_values": None, # This is defined later
                        },
                    },
                }
            ],
            "path_analysis": PathAnalysis("ul3").spec,
            "stopping_criteria": {
                "max_iterations": 1,
                "best_relative_gap": 1,
                "relative_gap": 1,
                "normalized_gap": 1,
            },
            "performance_settings": param.performance_settings
        }