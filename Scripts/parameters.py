import numpy

### ASSIGNMENT PARAMETERS ###

# Performance settings
performance_settings = {
    "number_of_processors": "max"
}
# Inversed value of time [min/eur]
vot_inv = {
    "work": 6,
    "business": 6,
    "leisure": 6,
}
# Default distance cost [eur/km]
dist_cost = 0.12
# Default transit zone fare
transit_cost = {
    "AB": 59.7,
    "BC": 59.7,
    "DJ": 59.7, # It is also possible to travel to Jarvenpaa
    "ABC": 107.5,
    "CD": 98,
    "BCD": 115.8,
    "ABCD": 156.4,
    "DNJMP": 63, # Keski-Uudenmaan seutulippu
    "NA": 120, # Nurmijarvi - Helsinki
    "NB": 120,
    "NC": 120,
    "V": 85, # Vihti
    "VA": 149, # Vihti - Helsinki
    "VB": 149,
    "VC": 149,
    "J": 35, # Jarvenpaa
    "JA": 130, # Jarvenpaa - Helsinki
    "JB": 130,
    "JC": 87, # Jarvenpaa - Tikkurila
    "JD": 46, # Jarvenpaa - Kerava/Tuusula
    "MA": 168, # Mantsala/Hyvinkaa - Helsinki
    "MB": 168,
    "MC": 142, # Mantsala/Hyvinkaa - Tikkurila
    "MD": 121, # Mantsala/Hyvinkaa - Kerava
    "PA": 252, # Pornainen - Helsinki
    "PB": 252,
    "PC": 252,
}
# Tickets only sold to municipality citizens
exclusive_tickets = {
    "JD": "Jarvenpaa",
}
transit_start_cost = 57.5
transit_dist_cost = 5.34
# Boarding penalties for different transit modes
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
# Specification for the transit assignment
transfer_penalty = 5
extra_waiting_time = {
    "penalty": "@wait_time_dev",
    "perception_factor": 3.5
}
first_headway_fraction = 0.3
standard_headway_fraction = 0.5
waiting_time_perception_factor = 1.5
aux_transit_time = {
    "perception_factor": 1.75
}
# Stochastic bike assignment distribution
bike_dist = {
    "type": "UNIFORM", 
    "A": 0.5, 
    "B": 1.5,
}

### ASSIGNMENT REFERENCES ###

# Volume-delay function files
func_car = "d411_pituusriippuvaiset_HM30.in"
func_bike = "d411_pituusriippuvaiset_pyora.in"
# Emme scenarios used in assignment
emme_scenario = {
    "aht": 21,
    "pt": 22,
    "iht": 23,
}
bike_scenario = 19
assignment_class = {
    "hw": "car_work",
    "hc": "car_leisure",
    "hu": "car_leisure",
    "hs": "car_leisure",
    "ho": "car_leisure",
    "hoo": "car_work",
    "oo": "car_leisure",
    "hwp": "car_work",
    "hop": "car_leisure",
    "oop": "car_leisure",
    "external": "car_leisure",
}
car_mode = 'c'
assignment_mode = {
    "car_work": 'c',
    "car_leisure": 'c',
    "trailer_truck": 'y',
    "truck": 'k',
    "van": 'v',
}
vot_class = {
    "car_work": "work",
    "car_leisure": "leisure",
    "trailer_truck": "business",
    "truck": "business",
    "van": "business",
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
# Link attribute for volumes
link_volumes = {
    "car_work": None,
    "car_leisure": None,
    "trailer_truck": "@yhd",
    "truck": "@ka",
    "van": "@pa",
}
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
        "walk": {
            "id": "mf376",
            "description": "walk travel time",
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
        "walk": {
            "id": "mf377",
            "description": "walk travel distance",
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
        "transit": {
            "id": "mf31",
            "description": "transit travel cost",
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
        "board_cost": {
            "id": "mf28",
            "description": "transit boarding cost",
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
background_traffic = "ul3"

### DEPARTURE TIME PARAMETERS ###

# Demand shares for different time periods
demand_share = {
    "hw": {
        "car": {
            "aht": (0.1, 0.01),
            "pt": (0.01, 0.01),
            "iht": (0.01, 0.1),
        },
        "transit": {
            "aht": (0.1, 0.01),
            "pt": (0.01, 0.01),
            "iht": (0.01, 0.1),
        },
        "bike": {
            "aht": (0.1, 0.01),
            "pt": (0.01, 0.01),
            "iht": (0.01, 0.1),
        },
    },
    "hc": {
        "car": {
            "aht": (0.1, 0.01),
            "pt": (0.01, 0.01),
            "iht": (0.01, 0.1),
        },
        "transit": {
            "aht": (0.1, 0.01),
            "pt": (0.01, 0.01),
            "iht": (0.01, 0.1),
        },
        "bike": {
            "aht": (0.1, 0.01),
            "pt": (0.01, 0.01),
            "iht": (0.01, 0.1),
        },
    },
    "hu": {
        "car": {
            "aht": (0.1, 0.01),
            "pt": (0.01, 0.01),
            "iht": (0.01, 0.1),
        },
        "transit": {
            "aht": (0.1, 0.01),
            "pt": (0.01, 0.01),
            "iht": (0.01, 0.1),
        },
        "bike": {
            "aht": (0.1, 0.01),
            "pt": (0.01, 0.01),
            "iht": (0.01, 0.1),
        },
    },
    "hs": {
        "car": {
            "aht": (0.01, 0.01),
            "pt": (0.05, 0.05),
            "iht": (0.05, 0.05),
        },
        "transit": {
            "aht": (0.01, 0.01),
            "pt": (0.05, 0.05),
            "iht": (0.05, 0.05),
        },
        "bike": {
            "aht": (0.01, 0.01),
            "pt": (0.05, 0.05),
            "iht": (0.05, 0.05),
        },
    },
    "ho": {
        "car": {
            "aht": (0.01, 0.01),
            "pt": (0.05, 0.05),
            "iht": (0.05, 0.05),
        },
        "transit": {
            "aht": (0.01, 0.01),
            "pt": (0.05, 0.05),
            "iht": (0.05, 0.05),
        },
        "bike": {
            "aht": (0.01, 0.01),
            "pt": (0.05, 0.05),
            "iht": (0.05, 0.05),
        },
    },
    "hoo": {
        "car": {
            "aht": (
                (0.1, 0.01),
                (0.01, 0.01),
                (0.01, 0.01),
            ),
            "pt": (
                (0.01, 0.01),
                (0.1, 0.01),
                (0.01, 0.01),
            ),
            "iht": (
                (0.01, 0.01),
                (0.01, 0.01),
                (0.1, 0.01),
            ),
        },
        "transit": {
            "aht": (
                (0.1, 0.01),
                (0.01, 0.01),
                (0.01, 0.01),
            ),
            "pt": (
                (0.01, 0.01),
                (0.1, 0.01),
                (0.01, 0.01),
            ),
            "iht": (
                (0.01, 0.01),
                (0.01, 0.01),
                (0.1, 0.01),
            ),
        },
        "bike": {
            "aht": (
                (0.1, 0.01),
                (0.01, 0.01),
                (0.01, 0.01),
            ),
            "pt": (
                (0.01, 0.01),
                (0.1, 0.01),
                (0.01, 0.01),
            ),
            "iht": (
                (0.01, 0.01),
                (0.01, 0.01),
                (0.1, 0.01),
            ),
        },
    },
    "oo": {
        "car": {
            "aht": (0.01, 0.01),
            "pt": (0.05, 0.05),
            "iht": (0.05, 0.05),
        },
        "transit": {
            "aht": (0.01, 0.01),
            "pt": (0.05, 0.05),
            "iht": (0.05, 0.05),
        },
        "bike": {
            "aht": (0.01, 0.01),
            "pt": (0.05, 0.05),
            "iht": (0.05, 0.05),
        },
    },
    "hwp": {
        "car": {
            "aht": (0.01, 0.01),
            "pt": (0.05, 0.05),
            "iht": (0.05, 0.05),
        },
        "transit": {
            "aht": (0.01, 0.01),
            "pt": (0.05, 0.05),
            "iht": (0.05, 0.05),
        },
    },
    "hop": {
        "car": {
            "aht": (0.01, 0.01),
            "pt": (0.05, 0.05),
            "iht": (0.05, 0.05),
        },
        "transit": {
            "aht": (0.01, 0.01),
            "pt": (0.05, 0.05),
            "iht": (0.05, 0.05),
        },
    },
    "oop": {
        "car": {
            "aht": (0.01, 0.01),
            "pt": (0.05, 0.05),
            "iht": (0.05, 0.05),
        },
        "transit": {
            "aht": (0.01, 0.01),
            "pt": (0.05, 0.05),
            "iht": (0.05, 0.05),
        },
    },
    "freight": {
        "trailer_truck": {
            "aht": (0.1, 0),
            "pt": (0.1, 0),
            "iht": (0.1, 0),
        },
        "truck": {
            "aht": (0.1, 0),
            "pt": (0.1, 0),
            "iht": (0.1, 0),
        },
        "van": {
            "aht": (0.1, 0),
            "pt": (0.1, 0),
            "iht": (0.1, 0),
        },
    },
    "external": {
        "car": {
            "aht": (0.01, 0.01),
            "pt": (0.05, 0.05),
            "iht": (0.05, 0.05),
        },
        "transit": {
            "aht": (0.01, 0.01),
            "pt": (0.05, 0.05),
            "iht": (0.05, 0.05),
        },
        "trailer_truck": {
            "aht": (0.1, 0),
            "pt": (0.1, 0),
            "iht": (0.1, 0),
        },
        "truck": {
            "aht": (0.1, 0),
            "pt": (0.1, 0),
            "iht": (0.1, 0),
        },
    },
}
# This needs to be changed
impedance_share = {
    "hw": {
        "car": {
            "aht": (0.1, 0.01),
            "pt": (0.01, 0.01),
            "iht": (0.01, 0.1),
        },
        "transit": {
            "aht": (0.1, 0.01),
            "pt": (0.01, 0.01),
            "iht": (0.01, 0.1),
        },
        "bike": {
            "aht": (0, 0),
            "pt": (0.5, 0.5),
            "iht": (0, 0),
        },
        "walk": {
            "aht": (0, 0),
            "pt": (0.5, 0.5),
            "iht": (0, 0),
        },
    },
    "hc": {
        "car": {
            "aht": (0.1, 0.01),
            "pt": (0.01, 0.01),
            "iht": (0.01, 0.1),
        },
        "transit": {
            "aht": (0.1, 0.01),
            "pt": (0.01, 0.01),
            "iht": (0.01, 0.1),
        },
        "bike": {
            "aht": (0, 0),
            "pt": (0.5, 0.5),
            "iht": (0, 0),
        },
        "walk": {
            "aht": (0, 0),
            "pt": (0.5, 0.5),
            "iht": (0, 0),
        },
    },
    "hu": {
        "car": {
            "aht": (0.1, 0.01),
            "pt": (0.01, 0.01),
            "iht": (0.01, 0.1),
        },
        "transit": {
            "aht": (0.1, 0.01),
            "pt": (0.01, 0.01),
            "iht": (0.01, 0.1),
        },
        "bike": {
            "aht": (0, 0),
            "pt": (0.5, 0.5),
            "iht": (0, 0),
        },
        "walk": {
            "aht": (0, 0),
            "pt": (0.5, 0.5),
            "iht": (0, 0),
        },
    },
    "hs": {
        "car": {
            "aht": (0.01, 0.01),
            "pt": (0.05, 0.05),
            "iht": (0.05, 0.05),
        },
        "transit": {
            "aht": (0.01, 0.01),
            "pt": (0.05, 0.05),
            "iht": (0.05, 0.05),
        },
        "bike": {
            "aht": (0, 0),
            "pt": (0.5, 0.5),
            "iht": (0, 0),
        },
        "walk": {
            "aht": (0, 0),
            "pt": (0.5, 0.5),
            "iht": (0, 0),
        },
    },
    "ho": {
        "car": {
            "aht": (0.01, 0.01),
            "pt": (0.05, 0.05),
            "iht": (0.05, 0.05),
        },
        "transit": {
            "aht": (0.01, 0.01),
            "pt": (0.05, 0.05),
            "iht": (0.05, 0.05),
        },
        "bike": {
            "aht": (0, 0),
            "pt": (0.5, 0.5),
            "iht": (0, 0),
        },
        "walk": {
            "aht": (0, 0),
            "pt": (0.5, 0.5),
            "iht": (0, 0),
        },
    },
    "hoo": {
        "car": {
            "aht": (0, 0),
            "pt": (0, 0),
            "iht": (0, 1),
        },
        "transit": {
            "aht": (0, 0),
            "pt": (0, 0),
            "iht": (0, 1),
        },
        "bike": {
            "aht": (0, 0),
            "pt": (0, 0),
            "iht": (0, 1),
        },
    },
    "so": {
        "car": {
            "aht": (0.01, 0.01),
            "pt": (0.05, 0.05),
            "iht": (0.05, 0.05),
        },
        "transit": {
            "aht": (0.01, 0.01),
            "pt": (0.05, 0.05),
            "iht": (0.05, 0.05),
        },
        "bike": {
            "aht": (0, 0),
            "pt": (0.5, 0.5),
            "iht": (0, 0),
        },
        "walk": {
            "aht": (0, 0),
            "pt": (0.5, 0.5),
            "iht": (0, 0),
        },
    },
    "oo": {
        "car": {
            "aht": (0.01, 0.01),
            "pt": (0.05, 0.05),
            "iht": (0.05, 0.05),
        },
        "transit": {
            "aht": (0.01, 0.01),
            "pt": (0.05, 0.05),
            "iht": (0.05, 0.05),
        },
        "bike": {
            "aht": (0, 0),
            "pt": (0.5, 0.5),
            "iht": (0, 0),
        },
        "walk": {
            "aht": (0, 0),
            "pt": (0.5, 0.5),
            "iht": (0, 0),
        },
    },
    "hwp": {
        "car": {
            "aht": (0.01, 0.01),
            "pt": (0.05, 0.05),
            "iht": (0.05, 0.05),
        },
        "transit": {
            "aht": (0.01, 0.01),
            "pt": (0.05, 0.05),
            "iht": (0.05, 0.05),
        },
    },
    "hop": {
        "car": {
            "aht": (0.01, 0.01),
            "pt": (0.05, 0.05),
            "iht": (0.05, 0.05),
        },
        "transit": {
            "aht": (0.01, 0.01),
            "pt": (0.05, 0.05),
            "iht": (0.05, 0.05),
        },
    },
    "sop": {
        "car": {
            "aht": (0.01, 0.01),
            "pt": (0.05, 0.05),
            "iht": (0.05, 0.05),
        },
        "transit": {
            "aht": (0.01, 0.01),
            "pt": (0.05, 0.05),
            "iht": (0.05, 0.05),
        },
    },
    "oop": {
        "car": {
            "aht": (0.01, 0.01),
            "pt": (0.05, 0.05),
            "iht": (0.05, 0.05),
        },
        "transit": {
            "aht": (0.01, 0.01),
            "pt": (0.05, 0.05),
            "iht": (0.05, 0.05),
        },
    },
}

### DEMAND MODEL PARAMETERS ###

destination_choice = {
    "hw": {
        "car": {
            "attraction": {
                "parking_cost_work": -0.340,
            },
            "impedance": {
                "time": -0.246e-1,
                "cost": (-0.288e-1, -0.103),
            },
            "log": {
                "size": 1,
            },
            "size": {
                "downtown": (numpy.exp(4.62), numpy.exp(5.33)),
                "workplaces_own": (numpy.exp(0.341), numpy.exp(0.930)),
                "workplaces_other": 1,
            },
        },
        "transit": {
            "attraction": {
                "downtown": 0.512,
            },
            "impedance": {
                "time": -0.111e-1,
                "cost": (-0.288e-1, -0.103),
            },
            "log": {
                "size": 1,
            },
            "size": {
                "downtown": (4.62, 5.33),
                "workplaces_own": (0.341, 0.930),
                "workplaces_other": 1,
            },
        },
        "bike": {
            "attraction": {},
            "impedance": {},
            "log": {
                "dist": (-1.13, -1.36),
                "size": 1,
            },
            "size": {
                "downtown": (4.62, 5.33),
                "workplaces_own": (0.341, 0.930),
                "workplaces_other": 1,
            },
        },
        "walk": {
            "attraction": {
                "own_zone_area_sqrt": (-2.07, -2.16),
            },
            "impedance": {},
            "log": {
                "dist": -2.68,
                "size": 1,
            },
            "size": {
                "downtown": (4.62, 5.33),
                "workplaces_own": (0.341, 0.930),
                "workplaces_other": 1,
            },
        },
    },
    "hc": {
        "car": {
            "attraction": {
                "own_zone_area": -0.2,
            },
            "impedance": {
                "time": -0.3,
                "cost": -0.1,
            },
            "log": {
                "size": 0.2,
            },
            "size": {
                "workplaces": 0.3,
            },
        },
        "transit": {
            "attraction": {},
            "impedance": {
                "time": -0.3,
            },
            "log": {
                "size": 0.2,
            },
            "size": {
                "workplaces": 0.3,
            },
        },
        "bike": {
            "attraction": {},
            "impedance": {
                "time": -0.3,
            },
            "log": {
                "size": 0.2,
            },
            "size": {
                "workplaces": 0.3,
            },
        },
        "walk": {
            "attraction": {},
            "impedance": {
                "time": -0.3,
            },
            "log": {
                "size": 0.2,
            },
            "size": {
                "workplaces": 0.3,
            },
        },
    },
    "hu": {
        "car": {
            "attraction": {
                "own_zone_area": -0.2,
            },
            "impedance": {
                "time": -0.3,
                "cost": -0.1,
            },
            "log": {
                "size": 0.2,
            },
            "size": {
                "workplaces": 0.3,
            },
        },
        "transit": {
            "attraction": {},
            "impedance": {
                "time": -0.3,
            },
            "log": {
                "size": 0.2,
            },
            "size": {
                "workplaces": 0.3,
            },
        },
        "bike": {
            "attraction": {},
            "impedance": {
                "time": -0.3,
            },
            "log": {
                "size": 0.2,
            },
            "size": {
                "workplaces": 0.3,
            },
        },
        "walk": {
            "attraction": {},
            "impedance": {
                "time": -0.3,
            },
            "log": {
                "size": 0.2,
            },
            "size": {
                "workplaces": 0.3,
            },
        },
    },
    "hs": {
        "car": {
            "attraction": {},
            "impedance": {
                "time": -0.3,
                "cost": -0.1,
            },
            "log": {
                "size": 0.2,
            },
            "size": {
                "workplaces": 0.3,
            },
        },
        "transit": {
            "attraction": {},
            "impedance": {
                "time": -0.3,
            },
            "log": {
                "size": 0.2,
            },
            "size": {
                "workplaces": 0.3,
            },
        },
        "bike": {
            "attraction": {},
            "impedance": {
                "time": -0.3,
            },
            "log": {
                "size": 0.2,
            },
            "size": {
                "workplaces": 0.3,
            },
        },
        "walk": {
            "attraction": {},
            "impedance": {
                "time": -0.3,
            },
            "log": {
                "size": 0.2,
            },
            "size": {
                "workplaces": 0.3,
            },
        },
    },
    "ho": {
        "car": {
            "attraction": {},
            "impedance": {
                "time": -0.3,
                "cost": -0.1,
            },
            "log": {
                "size": 0.2,
            },
            "size": {
                "workplaces": 0.3,
            },
        },
        "transit": {
            "attraction": {},
            "impedance": {
                "time": -0.3,
            },
            "log": {
                "size": 0.2,
            },
            "size": {
                "workplaces": 0.3,
            },
        },
        "bike": {
            "attraction": {},
            "impedance": {
                "time": -0.3,
            },
            "log": {
                "size": 0.2,
            },
            "size": {
                "workplaces": 0.3,
            },
        },
        "walk": {
            "attraction": {},
            "impedance": {
                "time": -0.3,
            },
            "log": {
                "size": 0.2,
            },
            "size": {
                "workplaces": 0.3,
            },
        },
    },
    "hoo": {
        "car": {
            "attraction": {},
            "impedance": {
                "time": -0.3,
                "cost": -0.1,
            },
            "log": {
                "size": 0.2,
            },
            "size": {
                "workplaces": 0.3,
            },
        },
        "transit": {
            "attraction": {},
            "impedance": {
                "time": -0.3,
            },
            "log": {
                "size": 0.2,
            },
            "size": {
                "workplaces": 0.3,
            },
        },
        "bike": {
            "attraction": {},
            "impedance": {
                "time": -0.3,
            },
            "log": {
                "size": 0.2,
            },
            "size": {
                "workplaces": 0.3,
            },
        },
    },
    "so": {
        "logsum": {
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": 0.2,
                "size": 0.2,
            },
            "size": {
                "population": 1,
                "workplaces": 0.3,
                "downtown": (1, 1),
            },
        },
    },
    "oo": {
        "car": {
            "attraction": {},
            "impedance": {
                "time": -0.3,
                "cost": -0.1,
            },
            "log": {
                "size": 0.2,
            },
            "size": {
                "workplaces": 0.3,
            },
        },
        "transit": {
            "attraction": {},
            "impedance": {
                "time": -0.3,
            },
            "log": {
                "size": 0.2,
            },
            "size": {
                "workplaces": 0.3,
            },
        },
        "bike": {
            "attraction": {},
            "impedance": {
                "time": -0.3,
            },
            "log": {
                "size": 0.2,
            },
            "size": {
                "workplaces": 0.3,
            },
        },
        "walk": {
            "attraction": {},
            "impedance": {
                "time": -0.3,
            },
            "log": {
                "size": 0.2,
            },
            "size": {
                "workplaces": 0.3,
            },
        },
    },
    "hwp": {
        "car": {
            "attraction": {
                "parking_cost_work": -0.141,
                "share_detached_houses": 0.559e-2,
                "own_zone_area": -0.216e-1,
            },
            "impedance": {
                "time": -0.245e-1,
                "cost": -0.141,
            },
            "log": {
                "size": 0.909,
            },
            "size": {
                "workplaces": 1,
            },
        },
        "transit": {
            "attraction": {
                "downtown": 0.238,
                "own_zone_area": -0.853e-1,
            },
            "impedance": {
                "time": -0.714e-2,
                "cost": -0.141,
            },
            "log": {
                "size": 0.909,
            },
            "size": {
                "workplaces": 1,
            },
        },
    },
    "hop": {
        "car": {
            "attraction": {
                "car_density": 0.198e-2,
                "own_zone_area": -0.186e-1,
            },
            "impedance": {
                "time": -0.302e-1,
                "cost": -0.182,
            },
            "log": {
                "size": 1,
            },
            "size": {
                "workplaces": 1.16,
                "service": 110,
                "shops": 211,
                "comprehensive_schools": 14.1,
                "population_own": 28.8,
                "population_other": 1,
            },
        },
        "transit": {
            "attraction": {},
            "impedance": {
                "time": -0.611e-2,
                "cost": -0.182,
            },
            "log": {
                "size": 1,
            },
            "size": {
                "workplaces": 1.16,
                "service": 110,
                "shops": 211,
                "comprehensive_schools": 14.1,
                "population_own": 28.8,
                "population_other": 1,
            },
        },
    },
    "sop": {
        "attraction": {
            "parking_cost_errand": 0.94 * -0.609e-1,
            "population_density": -0.109e-3,
        },
        "impedance": {
            "car": {
                "cost": 0.94 * -0.609e-1,
                "time": 0.94 * -0.264e-1,
            },
            "transit": {
                "cost": 0.04 * -0.609e-1,
                "time": 0.04 * -0.264e-1,
            },
        },
        "log": {
            "size": 1,
        },
        "size": {
            "workplaces": numpy.exp(2.53759200723),
            "population_own": numpy.exp(1.17058855327),
            "population_other": 1,
        },
    },
    "oop": {
        "car": {
            "attraction": {
                "parking_cost_errand": -0.221,
            },
            "impedance": {
                "time": -0.407e-1,
                "cost": -0.221,
            },
            "log": {
                "size": 1,
            },
            "size": {
                "population": 1,
                "workplaces": 3.37,
                "shops_downtown": 43.3,
                "shops_elsewhere": 9.11,
            },
        },
        "transit": {
            "attraction": {
                "downtown": 2.79,
            },
            "impedance": {
                "time": -0.828e-2,
                "cost": -0.221,
            },
            "log": {
                "size": 1,
            },
            "size": {
                "population": 1,
                "workplaces": 3.37,
                "shops_downtown": 43.3,
                "shops_elsewhere": 9.11,
            },
        },
    },
}
mode_choice = {
    "hw": {
        "car": {
            "constant": 0,
            "generation": {
                "car_density": (0.290e-2, 0.472e-2),
            },
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": 0.792,
            },
            "individual_dummy": {
                "car_users": (numpy.exp(3.18), numpy.exp(3.09)),
            },
        },
        "transit": {
            "constant": (3.26, 3.46),
            "generation": {},
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": 0.792,
            },
            "individual_dummy": {},
        },
        "bike": {
            "constant": (3.79, 4.38),
            "generation": {},
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": 0.792,
            },
            "individual_dummy": {},
        }, 
        "walk": {
            "constant": (6.16, 6.58),
            "generation": {},
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": 0.792,
            },
            "individual_dummy": {},
        },
    },
    "hc": {
        "car": {
            "constant": 0,
            "generation": {
                "car_density": 0.3,
            },
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": 3,
            },
            "individual_dummy": {},
        },
        "transit": {
            "constant": 0,
            "generation": {},
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": 5,
            },
            "individual_dummy": {},
        },
        "bike": {
            "constant": 0,
            "generation": {},
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": 2,
            },
            "individual_dummy": {},
        },  
        "walk": {
            "constant": 0,
            "generation": {},
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": 2,
            },
            "individual_dummy": {},
        },
    },
    "hu": {
        "car": {
            "constant": 0,
            "generation": {
                "car_density": 0.3,
            },
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": 3,
            },
            "individual_dummy": {},
        },
        "transit": {
            "constant": 0,
            "generation": {},
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": 5,
            },
            "individual_dummy": {},
        },
        "bike": {
            "constant": 0,
            "generation": {},
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": 2,
            },
            "individual_dummy": {},
        },  
        "walk": {
            "constant": 0,
            "generation": {},
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": 2,
            },
            "individual_dummy": {},
        },
    },
    "hs": {
        "car": {
            "constant": 0,
            "generation": {},
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": 3,
            },
            "individual_dummy": {},
        },
        "transit": {
            "constant": 0,
            "generation": {},
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": 5,
            },
            "individual_dummy": {},
        },
        "bike": {
            "constant": 0,
            "generation": {},
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": 2,
            },
            "individual_dummy": {},
        },  
        "walk": {
            "constant": 0,
            "generation": {},
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": 2,
            },
            "individual_dummy": {},
        },
    },
    "ho": {
        "car": {
            "constant": 0,
            "generation": {},
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": 3,
            },
            "individual_dummy": {},
        },
        "transit": {
            "constant": 0,
            "generation": {},
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": 5,
            },
            "individual_dummy": {},
        },
        "bike": {
            "constant": 0,
            "generation": {},
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": 2,
            },
            "individual_dummy": {},
        },  
        "walk": {
            "constant": 0,
            "generation": {},
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": 2,
            },
            "individual_dummy": {},
        },
    },
    "hoo": None,
    "so": {
        "car": {
            "constant": 0,
            "generation": {},
            "attraction": {
                "parking_cost_errand": -1,
            },
            "impedance": {},
            "log": {
                "time": -1,
                "cost": -1,
            },
            "individual_dummy": {},
        },
        "transit": {
            "constant": 1,
            "generation": {},
            "attraction": {
                "downtown": 1,
            },
            "impedance": {
                "time": -1,
                "cost": -1,
            },
            "log": {},
            "individual_dummy": {},
        },
        "bike": {
            "constant": 1,
            "generation": {},
            "attraction": {},
            "impedance": {},
            "log": {
                "dist": -1,
            },
            "individual_dummy": {},
        },  
        "walk": {
            "constant": 1,
            "generation": {},
            "attraction": {
                "own_zone_area_sqrt": 1,
            },
            "impedance": {},
            "log": {
                "dist": -1,
            },
            "individual_dummy": {},
        },
    },
    "oo": {
        "car": {
            "constant": 0,
            "generation": {},
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": 3,
            },
            "individual_dummy": {},
        },
        "transit": {
            "constant": 0,
            "generation": {},
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": 5,
            },
            "individual_dummy": {},
        },
        "bike": {
            "constant": 0,
            "generation": {},
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": 2,
            },
            "individual_dummy": {},
        },  
        "walk": {
            "constant": 0,
            "generation": {},
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": 2,
            },
            "individual_dummy": {},
        },
    },
    "hwp": {
        "car": {
            "constant": 0,
            "generation": {},
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": 1,
            },
            "individual_dummy": {},
        },
        "transit": {
            "constant": -2.20,
            "generation": {},
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": 1,
            },
            "individual_dummy": {},
        },
    },
    "hop": {
        "car": {
            "constant": 0,
            "generation": {},
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": 1,
            },
            "individual_dummy": {},
        },
        "transit": {
            "constant": -1.14,
            "generation": {},
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": 1,
            },
            "individual_dummy": {},
        },
    },
    "sop": {
        "all": {
            "individual_dummy": {},
        },
    },
    "oop": {
        "car": {
            "constant": 0,
            "generation": {},
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": 0.786,
            },
            "individual_dummy": {},
        },
        "transit": {
            "constant": -3.24,
            "generation": {},
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": 0.786,
            },
            "individual_dummy": {},
        },
    },
}
tour_generation = {
    "hw": {
        "population": 0.5,
    },
    "hc": {
        "population": 0.5,
    },
    "hu": {
        "population": 0.5,
    },
    "hs": {
        "population": 0.5,
    },
    "ho": {
        "population": 0.5,
    },
    "hoo": {
        "hw": 0.5,
        "ho": 0.3,
    },
    "so": {
        "population": 0.5,
    },
    "oo": {
        "so": 0.5,
    },
    "hwp": {
        "population": 0.5,
    },
    "hop": {
        "population": 0.5,
    },
    "sop": {
        "population": 0.5,
    },
    "oop": {
        "sop": 0.5,
    },
    "truck": {
        "population": 0.01,
        "workplaces": 0.025,
        "logistics": 0.35,
        "industry": 0.035,
        "shops": 0.05,
    },
    "trailer_truck": {
        "population": None,
        "workplaces": 0.005,
        "logistics": 0.38,
        "industry": 0.038,
        "shops": 0.005,
    }
}
garbage_generation = {
    "population": 0.000125,
    "workplaces": 0.000025,
}
vector_calibration_threshold = 5
# Maximum possible distance to destination
distance_boundary = {
    "car": 9999,
    "transit": 9999,
    "bike": 60,
    "walk": 15,
}
### DEMAND MODEL REFERENCES ###

tour_purposes = (
    {
        "name": "hw",
        "orig": "home",
        "dest": "work",
        "area": "metropolitan",
    },
    {
        "name": "hc",
        "orig": "home",
        "dest": "comprehensive_school",
        "area": "metropolitan",
    },
    {
        "name": "hu",
        "orig": "home",
        "dest": "tertiary_education",
        "area": "metropolitan",
    },
    {
        "name": "hs",
        "orig": "home",
        "dest": "shopping",
        "area": "metropolitan",
    },
    {
        "name": "ho",
        "orig": "home",
        "dest": "other",
        "area": "metropolitan",
    },
    {
        "name": "hoo",
        "orig": "home",
        "dest": "any",
        "sec_dest": "any",
        "source": ("hw", "ho",),
        "area": "metropolitan",
    },
    {
        "name": "so",
        "orig": "home",
        "dest": "source",
        "area": "metropolitan",
    },
    {
        "name": "oo",
        "orig": "source",
        "dest": "other",
        "source": ("so",),
        "area": "all",
    },
    {
        "name": "hwp",
        "orig": "home",
        "dest": "work",
        "area": "peripheral",
    },
    {
        "name": "hop",
        "orig": "home",
        "dest": "other",
        "area": "peripheral",
    },
    {
        "name": "sop",
        "orig": "home",
        "dest": "source",
        "area": "peripheral",
    },
    {
        "name": "oop",
        "orig": "source",
        "dest": "other",
        "source": ("sop",),
        "area": "all",
    },
)

external_modes = [
    "car",
    "transit",
    "truck",
    "trailer_truck",
]
first_surrounding_zone = 2792
first_peripheral_zone = 16001
first_external_zone = 31001
garbage_destination = 2792
trailers_prohibited = [5, 6]
areas = {
    "downtown": (0, 999),
    "Helsinki_other": (1000, 1999),
    "capital_region_other": (2000, 5999),
    "surrounding": (6000, 15999),
    "peripheral": (16000, 30999),
}
municipality = {
    "Helsinki": (0, 1999),
    "Espoo": (2000, 3499),
    "Kauniainen": (3500, 3999),
    "Vantaa": (4000, 5999),
    "Kirkkonummi": (6000, 6999),
    "Vihti": (7000, 7999),
    "Nurmijarvi": (8000, 8999),
    "Tuusula": (9000, 9999),
    "Kerava": (10000, 10999),
    "Jarvenpaa": (11000, 11999),
    "Sipoo": (12000, 12999),
    "Mantsala": (13000, 13999),
    "Hyvinkaa": (14000, 14999),
    "Pornainen": (15000, 15499),
    "Siuntio": (15500, 15999),
    "Salo": (16000, 16499),
    "Somero": (16500, 16999),
    "Raasepori": (17000, 17499),
    "Hanko": (17500, 17499),
    "Inkoo": (18000, 18499),
    "Karkkila": (18500, 18999),
    "Lohja": (19000, 19999),
    "Hameenlinna": (20000, 20999),
    "Janakkala": (21000, 21499),
    "Hattula": (21500, 21999),
    "Loppi": (22000, 22499),
    "Tammela": (22500, 22999),
    "Riihimaki": (23000, 23999),
    "Hausjarvi": (24000, 24499),
    "Karkola": (24500, 24999),
    "Orimattila": (25000, 25499),
    "Hollola": (25500, 25999),
    "Lahti": (26000, 26999),
    "Porvoo": (27000, 27999),
    "Pukkila": (28000, 28499),
    "Askola": (28500, 28999),
    "Myrskyla": (29000, 29499),
    "Lapinjarvi": (29500, 29999),
    "Loviisa": (30000, 30999),
}
numpy_municipality = { # Avoid using
    "Helsinki": (100, 2001),
    "Espoo": (2001, 3500),
    "Kauniainen": (3500, 4001),
    "Vantaa": (4001, 6000),
    "Kirkkonummi": (6000, 7001),
    "Vihti": (7001, 8001),
    "Nurmijarvi": (8001, 9001),
    "Tuusula": (9001, 10001),
    "Kerava": (10001, 11001),
    "Jarvenpaa": (11001, 12000),
    "Sipoo": (12000, 13001),
    "Mantsala": (13001, 14001),
    "Hyvinkaa": (14001, 15000),
    "Pornainen": (15000, 15501),
    "Siuntio": (15501, 16000),
    "Salo": (16000, 16500),
    "Somero": (16500, 17000),
    "Raasepori": (17000, 17501),
    "Hanko": (17501, 18001),
    "Inkoo": (18001, 18501),
    "Karkkila": (18501, 19001),
    "Lohja": (19001, 20000),
    "Hameenlinna": (20000, 21000),
    "Janakkala": (21000, 21500),
    "Hattula": (21500, 22001),
    "Loppi": (22001, 22500),
    "Tammela": (22500, 23001),
    "Riihimaki": (23001, 24001),
    "Hausjarvi": (24001, 24500),
    "Karkola": (24500, 25000),
    "Orimattila": (25000, 25500),
    "Hollola": (25500, 26000),
    "Lahti": (26000, 27000),
    "Porvoo": (27000, 28000),
    "Pukkila": (28000, 28501),
    "Askola": (28501, 29000),
    "Myrskyla": (29000, 29501),
    "Lapinjarvi": (29501, 30000),
    "Loviisa": (30000, ),
}
