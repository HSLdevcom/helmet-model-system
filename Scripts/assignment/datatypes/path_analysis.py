from typing import Optional, Union


class PathAnalysis:
    def __init__(self, link_component:str, od_values:Optional[Union[str,int]]=None):
        self.spec = {
            "link_component": link_component,
            "operator": "+",
            "selection_threshold": {
                "lower": None,
                "upper": None,
            },
            "path_to_od_composition": {
                "considered_paths": "ALL",
                "multiply_path_proportions_by": {
                    "analyzed_demand": False,
                    "path_value": True,
                }
            },
        }
        if od_values is not None:
            self.spec["results"] = {
                "od_values": od_values,
            }

class PathAnalysis3h:
    def __init__(self, link_component: str, link_vols_3h:str, demand_3h: str):
        self.spec = {
            "link_component": link_component,
            "operator": "+",
            "selection_threshold": {
                "lower": None,
                "upper": None,
            },
            "path_to_od_composition": {
                "considered_paths": "ALL",
                "multiply_path_proportions_by": {
                    "analyzed_demand": False,
                    "path_value": True,
                }
            },
            "analyzed_demand": demand_3h, 
            "results": {"selected_link_volumes": link_vols_3h, 
                        "selected_turn_volumes": None, "od_values": None}
        }
