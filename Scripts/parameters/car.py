### CAR DENSITY AND USAGE PARAMETERS ###

# Driver share of car tours
# Inverse of car occupancy
from typing import Any, Dict, Tuple, Union


car_driver_share = {
    "hw": 0.949308049508011,
    "hc": 0,
    "hu": 0.64455378516686,
    "hs": 0.794175881294076,
    "ho": 0.639435614706916,
    "hoo": 0.810204135531055,
    "wo": 0.661903340946716,
    "oo": 0.719526901929909,
    "hwp": 0.933275647078661,
    "hop": 0.648684175480966,
    "oop": 0.604623955305384,
}
car_usage: Dict[str,Any] = {
    "constant": -0.8551,
    "generation": {},
    "log": {
        "cars_per_1000": 0.6490,
        "population_density": -0.3684,
    },
    "individual_dummy": {
        "age_7-17": -9999,
        ("age_18-29", "male"): 0.0,
        ("age_30-49", "female"): 0.6795,
        ("age_30-49", "male"): 1.1779,
        ("age_50-64", "female"): 0.7980,
        ("age_50-64", "male"): 1.6197,
        ("age_65-99", "male"): 1.4483,
    },
}
car_density = {
    "constant": 0.0,
    "generation": {
        "share_detached_houses_new": 3.500e-01, # Originally estimated for percentages (0-100), here transformed
        "helsinki": 1.411e-01,
        "surrounding": 1.823e-01,
    },
    "log": {
        "time_ratio": 1.273e-01,
        "cost_ratio": 1.273e-01,
    },
}
