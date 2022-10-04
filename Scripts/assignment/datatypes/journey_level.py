from argparse import ArgumentError
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
        Journey level (0-3)
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
        # Boarding transit modes allowed only on levels 0-2
        next = BOARDED if level <= BOARDED else FORBIDDEN
        transitions = [{
                "mode": mode,
                "next_journey_level": next,
            } for mode in param.transit_modes]
        if park_and_ride:
            if "first_mile" in park_and_ride:
                # Park-and-ride (car) mode allowed only on level 0.
                car = FORBIDDEN if level >= PARKED else NOT_BOARDED
                # If we want parking to be allowed only on specific links
                # (i.e., park-and-ride facilities), we should specify an
                # own mode for these links. For now, parking is allowed
                # on all links where walking to a stop is possible.
                walk = PARKED if level == NOT_BOARDED else level
            elif "last_mile" in park_and_ride:
                # Transfer to park-and-ride (car) mode only allowed after first
                # boarding. If we want parking to be allowed only on specific
                # links, we should specify an own mode for these links.
                # For now, parking is allowed on all links where walking
                # from a stop is possible.
                car = FORBIDDEN if level in (NOT_BOARDED, FORBIDDEN) else LEFT
                walk = FORBIDDEN if level == LEFT else level
            transitions.append({
                "mode": param.park_and_ride_mode,
                "next_journey_level": car,
            })
        else:
            # Walk modes do not normally affect journey level transitions
            walk = level
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
        