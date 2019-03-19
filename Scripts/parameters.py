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
aht_mtx_id = {
    "car_demand": "mf1",
    "car_time": "mf380",
    "car_dist": "mf381",
    "car_cost": "mf370",
    "trailer_truck_demand": "mf71",
    "truck_demand": "mf72",
    "van_demand": "mf73",
}
pt_mtx_id = {
    "car_demand": "mf2",
    "car_time": "mf382",
    "car_dist": "mf383",
    "car_cost": "mf371",
    "trailer_truck_demand": "mf74",
    "truck_demand": "mf75",
    "van_demand": "mf76",
}
iht_mtx_id = {
    "car_demand": "mf3",
    "car_time": "mf384",
    "car_dist": "mf385",
    "car_cost": "mf372",
    "trailer_truck_demand": "mf77",
    "truck_demand": "mf78",
    "van_demand": "mf79",
}