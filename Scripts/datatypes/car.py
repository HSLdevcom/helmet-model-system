import parameters as param
from path_analysis import PathAnalysis


class Car:
    def __init__(self, ass_class,
                 value_of_time_inv=None, link_costs="@rumsi"):
        od_travel_times = param.emme_mtx["gen_cost"][ass_class]["id"]
        if value_of_time_inv is None:
            value_of_time_inv = param.vot_inv[param.vot_class[ass_class]]
        self.spec = {
            "mode": param.assignment_mode[ass_class],
            "demand": param.emme_mtx["demand"][ass_class]["id"],
            "generalized_cost": {
                "link_costs": link_costs,
                "perception_factor": value_of_time_inv,
            },
            "results": {
                "link_volumes": param.link_volumes[ass_class],
                "od_travel_times": {
                    "shortest_paths": od_travel_times
                }
            },
            "path_analyses": []
        }
        self.add_analysis("length", param.emme_mtx["dist"][ass_class]["id"])
        self.add_analysis("@ruma", param.emme_mtx["cost"][ass_class]["id"])
    
    def add_analysis (self, link_component, od_values):
        analysis = PathAnalysis(link_component, od_values)
        self.spec["path_analyses"].append(analysis.spec)
