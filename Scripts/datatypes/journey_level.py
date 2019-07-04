import parameters as param

class JourneyLevel:
    def __init__(self, boarded, count_zone_boardings=False):
        # Definition of transition rules: all modes are allowed
        transitions = []
        for mode in param.transit_modes:
            transitions.append({
                "mode": mode,
                "next_journey_level": 1
            })
        self.spec = {
            "transition_rules": transitions,
            "boarding_time": None,
            "boarding_cost": dict.fromkeys(["global", 
                                            "at_nodes", 
                                            "on_lines", 
                                            "on_segments"]),
            "waiting_time": {
                "headway_fraction": param.standard_headway_fraction,
                "effective_headways": "hdw",
                "spread_factor": 1,
                "perception_factor": param.waiting_time_perception_factor,
            },
        }
        if boarded:
            self.spec["description"] = "Boarded at least once"
            self.spec["destinations_reachable"] = True
            self.spec["boarding_cost"]["global"] = {
                "penalty": param.transfer_penalty,
                "perception_factor": 1,
            }
        else:
            self.spec["description"] = "Not boarded yet"
            self.spec["destinations_reachable"] = False
            hdw_frac = param.first_headway_fraction
            self.spec["waiting_time"]["headway_fraction"] = hdw_frac
            self.spec["boarding_cost"]["global"] = {
                "penalty": 0,
                "perception_factor": 1,
            }
        if count_zone_boardings:
            self.spec["boarding_cost"]["global"] = None
            self.spec["boarding_cost"]["at_nodes"] = {
                "penalty": "ui1", 
                "perception_factor": 0,
            }
        