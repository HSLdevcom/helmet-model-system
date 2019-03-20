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
emme_mtx = {
    "demand": {
        "car": "mf1",
        "trailer_truck": "mf71",
        "truck": "mf72",
        "van": "mf73",
    },
    "time": {
        "car": "mf380",
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