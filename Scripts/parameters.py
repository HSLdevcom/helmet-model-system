# Performance settings
performance_settings = {
    "number_of_processors": "max"
}
# Volume-delay function files
func_car = "d411_pituusriippuvaiset_HM30.in"
func_bike = "d411_pituusriippuvaiset_pyora.in"
# Inversed value of time [min/eur]
vot_inv = {
    "work": 6,
    "business": 6,
    "leisure": 6,
}
# Distance cost [eur/km]
dist_cost = 0.12
# Boarding penalties for differnt transit modes
boarding_penalty = {
    "b": 3,  # Bus
    "g": 3,  # Trunk bus
    "de": 5, # Long-distance and express bus
    "tp": 0, # Tram and light rail
    "mw": 0, # Metro and ferry
    "rj": 2, # Train
}
# Headway standard deviation function parameters for different transit modes
headway_sd_func = {
    'b': {
        "asc": 2.164,
        "ctime": 0.078,
        "cspeed": -0.028,
    },
    'd':  {
        "asc": 2.164,
        "ctime": 0.078,
        "cspeed": -0.028,
    },
    'g':  {
        "asc": 2.127,
        "ctime": 0.034,
        "cspeed": -0.021,
    },
    't':  {
        "asc": 1.442,
        "ctime": 0.060,
        "cspeed": -0.039,
    },
    'p':  {
        "asc": 1.442,
        "ctime": 0.034,
        "cspeed": -0.039,
    },
}
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
# Congestion function for congested transit assignment
trass_func = {
    "type": "BPR",
    "weight": 1.23,
    "exponent": 3,
    "assignment_period": 1,
    "orig_func": False,
    "congestion_attribute": "us3",
}
# Stopping criteria for congested transit assignment
trass_stop = {
    "max_iterations": 10,
    "normalized_gap": 0.01,
    "relative_gap": 0.001
}
emme_scenario = {
    "aht": 21,
    "pt": 22,
    "iht": 23,
}
bike_scenario = 19
car_mode = 'c'
mode = {
    "car_work": 'c',
    "car_leisure": 'c',
    "trailer_truck": 'y',
    "truck": 'k',
    "van": 'v',
}
bike_mode = 'f'
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
# Emme matrix IDs
emme_mtx = {
    "demand": {
        "car_work": {
            "id": "mf1",
            "description": "car work demand",
        },
        "car_leisure": {
            "id": "mf2",
            "description": "car leisure demand",
        },
        "trailer_truck": {
            "id": "mf71",
            "description": "trailer truck demand",
        },
        "truck":  {
            "id":"mf72",
            "description": "truck demand",
        },
        "van":  {
            "id":"mf73",
            "description": "van demand",
        },
        "transit":  {
            "id":"mf4",
            "description": "transit demand",
        },
        "bike":  {
            "id":"mf7",
            "description": "bicyclist demand",
        },
    },
    "gen_cost": {
        "car_work": {
            "id": "mf371",
            "description": "car work travel generalized cost",
        },
        "car_leisure": {
            "id": "mf372",
            "description": "car leisure travel generalized cost",
        },
    },
    "time": {
        "car_work": {
            "id": "mf380",
            "description": "car work travel time",
        },
        "car_leisure": {
            "id": "mf382",
            "description": "car leisure travel time",
        },
        "transit": {
            "id": "mf20",
            "description": "transit travel time",
        },
        "bike": {
            "id": "mf386",
            "description": "bike travel time",
        },
    },
    "dist": {
        "car_work": {
            "id": "mf381",
            "description": "car work travel distance",
        },
        "car_leisure": {
            "id": "mf383",
            "description": "car leisure travel distance",
        },
        "transit": {
            "id": "mf27",
            "description": "transit in-vehicle distance",
        },
        "bike": {
            "id": "mf387",
            "description": "bike travel distance",
        },
    },
    "cost": {
        "car_work": {
            "id": "mf370",
            "description": "car work travel cost",
        },
        "car_leisure": {
            "id": "mf371",
            "description": "car leisure travel cost",
        },
    },
    "transit": {
        "inv_time": {
            "id": "mf21",
            "description": "transit in-vehicle time",
        },
        "aux_time": {
            "id": "mf22",
            "description": "transit auxilliary time",
        },
        "tw_time": {
            "id": "mf23",
            "description": "transit total waiting time",
        },
        "fw_time": {
            "id": "mf24",
            "description": "transit first waiting time",
        },
        "board_time": {
            "id": "mf25",
            "description": "transit boarding time",
        },
        "num_board": {
            "id": "mf26",
            "description": "transit trip number of boardings",
        },
    },
    "bike": {
        "separate_dist": {
            "id": "mf100",
            "description": "separate bike way distance",
        },
        "streetside_dist": {
            "id": "mf101",
            "description": "street-side bike way distance",
        },
        "mixed_dist": {
            "id": "mf102",
            "description": "bike distance in mixed traffic",
        },
    },
}
# Demand shares for different time periods
demand_share = {
    "car_work": {
        "aht": 0.1,
        "pt": 0.05,
        "iht": 0.1,
    },
    "car_leisure": {
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
link_volumes = {
    "car_work": None,
    "car_leisure": None,
    "trailer_truck": "@yhd",
    "truck": "@ka",
    "van": "@pa",
}
# Specification for the transit assignment
trass_spec = {
    "type": "EXTENDED_TRANSIT_ASSIGNMENT",
    "modes": transit_assignment_modes,
    "demand": emme_mtx["demand"]["transit"]["id"],
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
            "transition_rules": None,
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
            "transition_rules": None,
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
    "performance_settings": performance_settings,
}
# Bike assignment specification
biass_spec = {
    "type": "STANDARD_TRAFFIC_ASSIGNMENT",
    "classes": [ 
        {
            "mode": bike_mode,
            "demand": emme_mtx["demand"]["bike"]["id"],
            "generalized_cost": None,
            "results": {
                 "od_travel_times": {
                     "shortest_paths": emme_mtx["time"]["bike"]["id"],
                 },
                 "link_volumes": None,
                 "turn_volumes": None,
            },
            "analysis": {
                "analyzed_demand": None,
                "results": {
                    "od_values": None,
                    "selected_link_volumes": None,
                    "selected_turn_volumes": None,
                },
            },
        }
    ],
    "path_analysis": {
        "link_component": "ul3",
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
    },
    "background_traffic": None,
    "stopping_criteria": {
        "max_iterations": 1,
        "best_relative_gap": 1,
        "relative_gap": 1,
        "normalized_gap": 1,
    },
    "performance_settings": performance_settings
}  
# Stochastic bike assignment distribution
bike_dist = {
    "type": "UNIFORM", 
    "A": 0.5, 
    "B": 1.5,
}