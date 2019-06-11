class PathAnalysis:
    def __init__(self, link_component, od_values=None):
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
