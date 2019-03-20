# Inversed value of time [min/eur]
vot_inv = 6
# Distance cost [eur/km]
dist_cost = 0.12
# Stopping criteria for last traffic assignment
stopping_criteria_fine = {
    "max_iterations": 200,
    "relative_gap": 0.00001,
    "best_relative_gap": 0.001,
    "normalized_gap": 0.0005,
}
# Stopping criteria for traffic assignment in loop
stopping_criteria_coarse = {
    "max_iterations": 100,
    "relative_gap": 0.0001,
    "best_relative_gap": 0.01,
    "normalized_gap": 0.005,
}
# Emme matrix IDs for time periods
emme_scenario = {
    "aht": 21,
    "pt": 22,
    "iht": 23,
}
transit_modes = [
    'b',
    'd',
    'e',
    'g',
    'j',
    'm',
    'p',
    'r',
    't',
    'w',
]
aux_modes = [
    'a',
    's',
]
transit_assignment_modes = transit_modes + aux_modes
emme_mtx = {
    "demand": {
        "car": "mf1",
        "trailer_truck": "mf71",
        "truck": "mf72",
        "van": "mf73",
        "transit": "mf4",
    },
    "time": {
        "car": "mf380",
        "transit": "mf20"
    },
    "dist": {
        "car": "mf381",
    },
    "cost": {
        "car": "mf370",
    },
}
# pt_mtx_id = {
    # "car_demand": "mf2",
    # "car_time": "mf382",
    # "car_dist": "mf383",
    # "car_cost": "mf371",
    # "trailer_truck_demand": "mf74",
    # "truck_demand": "mf75",
    # "van_demand": "mf76",
# }
# iht_mtx_id = {
    # "car_demand": "mf3",
    # "car_time": "mf384",
    # "car_dist": "mf385",
    # "car_cost": "mf372",
    # "trailer_truck_demand": "mf77",
    # "truck_demand": "mf78",
    # "van_demand": "mf79",
# }
demand_share = {
    "car": {
        "aht": 0.1,
        "pt": 0.05,
        "iht": 0.1,
    },
    "trailer_truck": {
        "aht": 0.1,
        "pt": 0.05,
        "iht": 0.1,
    },
    "truck": {
        "aht": 0.1,
        "pt": 0.05,
        "iht": 0.1,
    },
    "van": {
        "aht": 0.1,
        "pt": 0.05,
        "iht": 0.1,
    },
    "transit": {
        "aht": 0.1,
        "pt": 0.05,
        "iht": 0.1,
    },
}
cars = {
    "mode": "c",
    "demand": emme_mtx["demand"]["car"],
    "generalized_cost": {
        "link_costs": "@rumsi",
        "perception_factor": vot_inv,
    },
    "results": {
        "link_volumes": None,
        "turn_volumes": None,
        "od_travel_times": {
            "shortest_paths": emme_mtx["time"]["car"]
        }
    },
    "path_analyses": [
        {
            "link_component": "length",
            "turn_component": None,
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
            "analyzed_demand": None,
            "results": {
                "selected_link_volumes": None,
                "selected_turn_volumes": None,
                "od_values": emme_mtx["dist"]["car"],
            },
        },
        {
            "link_component": "@ruma",
            "turn_component": None,
            "operator": "+",
            "selection_threshold": {
                "lower": None,
                "upper": None,
            },
            "path_to_od_composition": {
                "considered_paths": "ALL",
                "multiply_path_proportions_by": {
                    "analyzed_demand": False,
                    "path_value": True
                }
            },
            "analyzed_demand": None,
            "results": {
                "selected_link_volumes": None,
                "selected_turn_volumes": None,
                "od_values": emme_mtx["cost"]["car"],
            },
        },
    ]
}
trailer_trucks = {
    "mode": "y",
    "demand": emme_mtx["demand"]["trailer_truck"],
    "generalized_cost": {
        "link_costs": "length",
        "perception_factor": 0.2,
    },
    "results": {
        "link_volumes": "@yhd",
        "turn_volumes": None,
        "od_travel_times": {
            "shortest_paths": None
        }
    },
    "path_analyses": []
}
trucks = {
    "mode": "k",
    "demand": emme_mtx["demand"]["truck"],
    "generalized_cost": {
        "link_costs": "length",
        "perception_factor": 0.2,
    },
    "results": {
        "link_volumes": "@ka",
        "turn_volumes": None,
        "od_travel_times": {
            "shortest_paths": None
        }
    },
    "path_analyses": []
}
vans = {
    "mode": "v",
    "demand": emme_mtx["demand"]["van"],
    "generalized_cost": {
        "link_costs": "length",
        "perception_factor": 0.2,
    },
    "results": {
        "link_volumes": "@pa",
        "turn_volumes": None,
        "od_travel_times": {
            "shortest_paths": None
        }
    },
    "path_analyses": []
}
transitions = []
for mode in transit_modes:
    transitions.append({
        "mode": mode,
        "next_journey_level": 1
    })
# Specification of the transit assignment
trass_spec = {
    "type": "EXTENDED_TRANSIT_ASSIGNMENT",
    "modes": transit_assignment_modes,
    "demand": emme_mtx["demand"]["transit"],
    "waiting_time": {
        "headway_fraction": 0.5,
        "effective_headways": "hdw",
        "spread_factor": 1,
        "perception_factor": 1.5
    },
    # Boarding time is defined for each journey level separately,
    # so here we just set the default to zero.
    "boarding_time": {
        "global": {
            "penalty": 0,
            "perception_factor": 1,
        },
        "at_nodes": None,
        "on_lines": None,
        "on_segments": None,
    },
    "boarding_cost": {
        "global": {
            "penalty": 0,
            "perception_factor": 1,
        },
        "at_nodes": None,
        "on_lines": None,
        "on_segments": None,
    },
    "in_vehicle_time": {
        "perception_factor": 1
    },
    "in_vehicle_cost": None,
    "aux_transit_time": {
        "perception_factor": 1.75
    },
    "aux_transit_cost": None,
    "flow_distribution_at_origins": {
        "choices_at_origins": "OPTIMAL_STRATEGY",
        "fixed_proportions_on_connectors": None
    },
    "flow_distribution_at_regular_nodes_with_aux_transit_choices": {
        "choices_at_regular_nodes": "OPTIMAL_STRATEGY"
    },
    "flow_distribution_between_lines": {
        "consider_total_impedance": False
    },
    "connector_to_connector_path_prohibition": None,
    "od_results": {
        "total_impedance": None
    },
    # The two journey levels are identical, except that at the second
    # level an extra boarding penalty is implemented,
    # hence a transfer penalty. Walk only trips are not allowed.
    "journey_levels": [
        {
            "description": "Not boarded yet",
            "destinations_reachable": False,
            "transition_rules": transitions,
            "boarding_time": {
                "global": None,
                "at_nodes": None,
                "on_lines": {
                    "penalty": "ut3",
                    "perception_factor": 1
                },
                "on_segments": {
                    "penalty": "@wait_time_dev",
                    "perception_factor": 3.5
                },
            },
            "boarding_cost": None,
            "waiting_time": None
        },
        {
            "description": "Boarded at least once",
            "destinations_reachable": True,
            "transition_rules": transitions,
            "boarding_time": {
                "global": None,
                "at_nodes": None,
                "on_lines": {
                    "penalty": "ut3",
                    "perception_factor": 1
                },
                "on_segments": {
                    "penalty": "@wait_time_dev",
                    "perception_factor": 3.5
                }
            },
            "boarding_cost": {
                "global": {
                    "penalty": 5,
                    "perception_factor": 1,
                },
                "at_nodes": None,
                "on_lines": None,
                "on_segments": None,                    
            },
            "waiting_time": None
        }
    ],
    "performance_settings": {
        "number_of_processors": "max"
    },
}
result_spec = {
    "type": "EXTENDED_TRANSIT_MATRIX_RESULTS",
    "total_impedance": emme_mtx["time"]["transit"],
    "actual_first_waiting_times": None,
    "actual_total_waiting_times": None,
    "by_mode_subset": {
        "modes": transit_modes,
        "distance": None,
        "avg_boardings": None,
        "actual_total_boarding_times": None,
        "actual_in_vehicle_times": None,
        "actual_aux_transit_times": None,
    },
}