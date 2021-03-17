import parameters.assignment as param
from assignment.datatypes.path_analysis import PathAnalysis


class Car:
    def __init__(self, ass_class, demand_mtx, result_mtx, 
                value_of_time_inv=None, link_costs="@total_cost"):
        od_travel_times = result_mtx["gen_cost"][ass_class]["id"]
        if value_of_time_inv is None:
            value_of_time_inv = param.vot_inv[param.vot_classes[ass_class]]
        self.spec = {
            "mode": param.assignment_modes[ass_class],
            "demand": demand_mtx[ass_class]["id"],
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
        self.add_analysis("length", result_mtx["dist"][ass_class]["id"])
        self.add_analysis("@toll_cost", result_mtx["cost"][ass_class]["id"])
    
    def add_analysis (self, link_component, od_values):
        analysis = PathAnalysis(link_component, od_values)
        self.spec["path_analyses"].append(analysis.spec)
