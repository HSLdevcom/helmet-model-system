### CAR DENSITY AND USAGE PARAMETERS ###

# Driver share of car tours
# Inverse of car occupancy
from typing import Any, Dict, Tuple, Union


car_driver_share = {
    "hw": 0.928309883,
    "hc": 0,
    "hu": 0.805783638,
    "hs": 0.803581362,
    "ho": 0.669375456,
    "hoo": 0.79867104,
    "wo": 0.809134377,
    "oo": 0.691710941,
    "hwp": 0.923397539,
    "hop": 0.699605826,
    "oop": 0.784781268,
}
car_usage: Dict[str,Any] = {
    "constant": -1.0477,
    "generation": {},
    "log": {
        "cars_per_1000": 0.6475,
        "population_density": -0.3436,
    },
    "individual_dummy": {
        "age_7-17": -9999,
        ("age_18-29", "male"): -0.0890,
        ("age_30-49", "female"): 0.6808,
        ("age_30-49", "male"): 1.1759,
        ("age_50-64", "female"): 0.8005,
        ("age_50-64", "male"): 1.6203,
        ("age_65-99", "male"): 1.4475,
    },
}
car_density = {
    "constant": 0.0,
    "generation": {
        "share_detached_houses_new": 4.241e-01, # Originally estimated for percentages (0-100), here transformed
        "helsinki": 1.248e-01,
        "surrounding": 1.733e-01,
    },
    "log": {
        "time_ratio": 1.284e-01,
        "cost_ratio": 1.284e-01,
    },
}
