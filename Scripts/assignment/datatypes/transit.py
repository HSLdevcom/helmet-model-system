import parameters.assignment as param
from assignment.datatypes.path_analysis import PathAnalysis
from assignment.datatypes.journey_level import JourneyLevel


class TransitSpecification:
    """
    Transit assignment specification.
    
    Two journey levels are added at a later stage.
    At the second level an extra boarding penalty is implemented,
    hence a transfer penalty. Waiting time length is also different. 
    Walk only trips are not allowed.

    Parameters
    ----------
    ass_class : str
        Assignment class (transit_work/transit_leisure)
    headway_attribute : str
        Line attribute where headway is stored
    demand_mtx_id : str
        Emme matrix id for demand matrix
    time_mtx_id : str
        Emme matrix id for time matrix
    dist_mtx_id : str
        Emme matrix id for distance matrix
    trip_part : dict
        key : str
            Impedance type (inv_time/aux_time/num_board/...)
        value : dict
            id : str
                Emme matrix id
            description : dict
                Matrix description
    count_zone_boardings : bool (optional)
        Whether assignment is performed only to count fare zone boardings
    """
    def __init__(self, ass_class, headway_attribute, demand_mtx_id,
                 time_mtx_id, dist_mtx_id, trip_part,
                 count_zone_boardings=False):
        no_penalty = dict.fromkeys(["at_nodes", "on_lines", "on_segments"])
        no_penalty["global"] = {
            "penalty": 0, 
            "perception_factor": 1,
        }
        self.transit_spec = {
            "type": "EXTENDED_TRANSIT_ASSIGNMENT",
            "modes": param.transit_assignment_modes,
            "demand": demand_mtx_id,
            "waiting_time": {
                "headway_fraction": param.standard_headway_fraction,
                "effective_headways": headway_attribute,
                "spread_factor": 1,
                "perception_factor": param.waiting_time_perception_factor
            },
            "boarding_time": {
                "global": None,
                "at_nodes": None,
                "on_lines": {
                    "penalty": "ut3",
                    "perception_factor": 1
                },
                "on_segments": param.extra_waiting_time,
            },
            # Boarding cost is defined for each journey level separately,
            # so here we just set the default to zero.
            "boarding_cost": no_penalty,
            "in_vehicle_time": {
                "perception_factor": 1
            },
            "aux_transit_time": param.aux_transit_time,
            "flow_distribution_at_origins": {
                "choices_at_origins": "OPTIMAL_STRATEGY",
            },
            "flow_distribution_at_regular_nodes_with_aux_transit_choices": {
                "choices_at_regular_nodes": "OPTIMAL_STRATEGY",
            },
            "flow_distribution_between_lines": {
                "consider_total_impedance": False
            },
            "journey_levels": None,
            "performance_settings": param.performance_settings,
        }

        self.ntw_results_spec = {
            "type": "EXTENDED_TRANSIT_NETWORK_RESULTS",
            "on_segments": {
                "transit_volumes": "@{}_vol".format(ass_class),
                "total_boardings": "@{}_boa".format(ass_class),
                "transfer_boardings": "@{}_trb".format(ass_class),
                }
            }
        if count_zone_boardings:
            jlevel1 = JourneyLevel(boarded=False, ass_class=ass_class, count_zone_boardings=True)
            jlevel2 = JourneyLevel(boarded=True, ass_class=ass_class, count_zone_boardings=True)
            mtx_results_spec = {
                "type": "EXTENDED_TRANSIT_MATRIX_RESULTS",
                "by_mode_subset": {
                    "modes": param.transit_modes,
                    "distance": dist_mtx_id,
                    "actual_total_boarding_costs": trip_part["board_cost"]["id"],
                },
            }
        else:
            jlevel1 = JourneyLevel(boarded=False, ass_class=ass_class)
            jlevel2 = JourneyLevel(boarded=True, ass_class=ass_class)
            mtx_results_spec = {
                "type": "EXTENDED_TRANSIT_MATRIX_RESULTS",
                "total_impedance": time_mtx_id,
                "total_travel_time": trip_part["total_time"]["id"],
                "actual_first_waiting_times": trip_part["fw_time"]["id"],
                "actual_total_waiting_times": trip_part["tw_time"]["id"],
                "by_mode_subset": {
                    "modes": param.transit_assignment_modes,
                    "distance": dist_mtx_id,
                    "avg_boardings": trip_part["num_board"]["id"],
                    "actual_total_boarding_times": trip_part["board_time"]["id"],
                    "actual_in_vehicle_times": trip_part["inv_time"]["id"],
                    "actual_aux_transit_times": trip_part["aux_time"]["id"],
                },
            }

        self.transit_spec["journey_levels"] = [jlevel1.spec, jlevel2.spec]
        self.transit_result_spec = mtx_results_spec

