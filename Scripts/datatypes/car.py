import parameters as param
from path_analysis import PathAnalysis

class Car:
    def __init__(self, ass_class, value_of_time_inv, 
                 od_travel_times=None, link_costs="@rumsi"):
        self.spec = {
            "mode": param.assignment_mode[ass_class],
            "demand": param.emme_mtx["demand"][ass_class]["id"],
            "generalized_cost": {
                "link_costs": link_costs,
                "perception_factor": value_of_time_inv,
            },
            "results": {
                "link_volumes": param.link_volumes[ass_class],
                "turn_volumes": None,
                "od_travel_times": {
                    "shortest_paths": od_travel_times
                }
            },
            "path_analyses": []
        }
    
    def add_analysis (self, link_component, od_values):
        analysis = PathAnalysis(link_component, od_values)
        self.spec["path_analyses"].append(analysis.spec)

class PrivateCar (Car):
    def __init__(self, ass_class, value_of_time_inv):
        od_travel_times = param.emme_mtx["gen_cost"][ass_class]["id"]
        Car.__init__(self, ass_class, value_of_time_inv, od_travel_times)
        self.add_analysis("length", param.emme_mtx["dist"][ass_class]["id"])
        self.add_analysis("@ruma", param.emme_mtx["cost"][ass_class]["id"])
        
