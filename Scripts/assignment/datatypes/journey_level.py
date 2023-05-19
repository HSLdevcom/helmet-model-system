import parameters.assignment as param


NOT_BOARDED, PARKED, BOARDED, LEFT, FORBIDDEN = range(5)
DESCRIPTION = [
    "Not boarded yet",
    "Parked",
    "Boarded at least once",
    "Left transit system",
    "Forbidden",
]
DESTINATIONS_REACHABLE = [False, False, True, True, False]


class JourneyLevel:
    """
    Journey level specification for transit assignment.

    Parameters
    ----------
    level : int
        Journey level: 0 - not boarded yet, 1 - parked,
        2 - boarded at least once, 3 - left transit system,
        4 - forbidden (virtual level)
    headway_attribute : str
        Line attribute where headway is stored
    park_and_ride : str or False (optional)
        Extra attribute name for park-and-ride aux volume if
        this is park-and-ride assignment, else False
    count_zone_boardings : bool (optional)
        Whether assignment is performed only to count fare zone boardings
    """
    def __init__(self, level, headway_attribute, park_and_ride=False,
            count_zone_boardings=False):
        transitions = []
        if park_and_ride:
            if "first_mile" in park_and_ride:
                # Park-and-ride (car) mode allowed only on level 0.
                car = FORBIDDEN if level >= PARKED else NOT_BOARDED
                park = PARKED if level == NOT_BOARDED else FORBIDDEN
                walk = FORBIDDEN if level == NOT_BOARDED else level
                next = BOARDED if level in (PARKED, BOARDED) else FORBIDDEN
            elif "last_mile" in park_and_ride:
                # Transfer to park-and-ride (car) mode only allowed after first
                # boarding.
                walk = FORBIDDEN if level == LEFT else level
                next = BOARDED if level <= BOARDED else FORBIDDEN
                park = LEFT if level == BOARDED else FORBIDDEN
                car = LEFT if level == LEFT else FORBIDDEN
            transitions.append({
                "mode": param.drive_access_mode,
                "next_journey_level": car,
            })
            transitions.append({
                "mode": param.park_mode,
                "next_journey_level": park,
            })
        else:
            # Walk modes do not normally affect journey level transitions
            walk = level
            # Boarding transit modes allowed only on levels 0-2
            next = BOARDED if level <= BOARDED else FORBIDDEN
        transitions += [{
                "mode": mode,
                "next_journey_level": next,
            } for mode in param.transit_modes]
        transitions += [{
                "mode": mode,
                "next_journey_level": walk,
            } for mode in param.aux_modes]
        self.spec = {
            "description": DESCRIPTION[level],
            "destinations_reachable": DESTINATIONS_REACHABLE[level],
            "transition_rules": transitions,
            "boarding_time": None,
            "boarding_cost": {
                "global": {
                    "penalty": 0,
                    "perception_factor": 1,
                },
                "at_nodes": None,
                "on_lines": None,
                "on_segments": None,
            },
            "waiting_time": {
                "headway_fraction": param.standard_headway_fraction,
                "effective_headways": headway_attribute,
                "spread_factor": 1,
                "perception_factor": param.waiting_time_perception_factor,
            },
        }
        if level < BOARDED:
            (self.spec["waiting_time"]
                      ["headway_fraction"]) = param.first_headway_fraction
        elif level == BOARDED:
            (self.spec["boarding_cost"]
                      ["global"]["penalty"]) = param.transfer_penalty["transit"]
        if count_zone_boardings:
            self.spec["boarding_cost"]["global"] = None
            self.spec["boarding_cost"]["at_nodes"] = {
                "penalty": param.is_in_transit_zone_attr,
                "perception_factor": 0,
            }
        