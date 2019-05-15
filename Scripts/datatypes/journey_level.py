import parameters as param

class JourneyLevel:
    def __init__(self, boarded):
        waiting_time = {
            "headway_fraction": param.standard_headway_fraction,
            "effective_headways": "hdw",
            "spread_factor": 1,
            "perception_factor": param.waiting_time_perception_factor
        }
        if boarded:
            description = "Boarded at least once"
            dest_reachable = True
            boarding_penalty = {
                "penalty": param.transfer_penalty,
                "perception_factor": 1,
            }
        else:
            description = "Not boarded yet"
            dest_reachable = False
            boarding_penalty = None
            waiting_time["headway_fraction"] = param.first_headway_fraction
        # Definition of transition rules: all modes are allowed
        transitions = []
        for mode in param.transit_modes:
            transitions.append({
                "mode": mode,
                "next_journey_level": 1
            })
        self.spec = {
            "description": description,
            "destinations_reachable": dest_reachable,
            "transition_rules": transitions,
            "boarding_time": {
                "global": boarding_penalty,
                "at_nodes": None,
                "on_lines": {
                    "penalty": "ut3",
                    "perception_factor": 1
                },
                "on_segments": param.extra_waiting_time,
            },
            "boarding_cost": None,
            "waiting_time": waiting_time,
        }