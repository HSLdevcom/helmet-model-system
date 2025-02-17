### ASSIGNMENT PARAMETERS ###

from collections import namedtuple
from typing import Dict, List, Union

import numpy as np
import pandas as pd

from datahandling.zonedata import ZoneData
RoadClass = namedtuple(
    "RoadClass",
    (
        "type", "num_lanes", "volume_delay_func", "lane_capacity",
        "free_flow_speed", "bus_delay",
    ))
# Code derived from three-digit link type xyz, where yz is the road class code. See dictionary volume_delay_funcs below.
roadclasses = {
    21: RoadClass("motorway", "<3", 1, 2100, 113, 0.265),
    22: RoadClass("motorway", ">=3", 1, 1900, 113, 0.265),
    23: RoadClass("motorway", "<3", 1, 2000, 97, 0.309),
    24: RoadClass("motorway", ">=3", 1, 1800, 97, 0.309),
    25: RoadClass("motorway", "<3", 1, 2000, 81, 0.370),
    26: RoadClass("motorway", ">=3", 1, 1800, 81, 0.370),
    27: RoadClass("highway", "<3", 2, 1900, 97, 0.309),
    28: RoadClass("highway", ">=3", 2, 1800, 97, 0.309),
    29: RoadClass("highway", "<3", 2, 1850, 81, 0.370),
    30: RoadClass("highway", ">=3", 2, 1800, 81, 0.370),
    31: RoadClass("highway", "any", 2, 1600, 73, 0.411),
    32: RoadClass("highway", "any", 2, 1600, 63, 0.556),
    33: RoadClass("arterial", "any", 3, 1450, 61, 0.492),
    34: RoadClass("arterial", "any", 3, 1250, 54, 0.556),
    35: RoadClass("arterial", "any", 4, 1150, 48, 0.625),
    36: RoadClass("arterial", "any", 4, 1000, 44, 0.682),
    37: RoadClass("arterial", "any", 4, 1000, 41, 0.732),
    38: RoadClass("collector", "any", 5, 900, 41, 0.732),
    39: RoadClass("collector", "any", 5, 750, 36, 0.833),
    40: RoadClass("collector", "any", 5, 900, 36, 0.833),
    41: RoadClass("local", "any", 5, 600, 30, 1.000),
    42: RoadClass("local", "any", 5, 500, 12, 1.304),
    43: RoadClass("collector", "any", 5, 750, 30, 0.833),
}
connector_link_types = (84, 85, 86, 87, 88, 98, 99)
connector = RoadClass("connector", "any", 99, 0, 0, 0)
roadclasses.update({linktype: connector for linktype in connector_link_types})
custom_roadtypes = {
    91: "motorway",
    92: "highway",
    93: "arterial",
    94: "arterial",
    95: "local",
}
# Bike delay function ids, defaults to None. See dictionary volume_delay_funcs below.
bikepath_vdfs = (
    {  # 0 - Mixed traffic
        None: 78,
        "collector": 77,
        "arterial": 77,
        "highway": 76,
    },
    {  # 1 - Bike lane
        None: 75,
    },
    {  # 2 - Road-side bike path
        None: 74,
        "arterial": 73,
        "highway": 72,
    },
    {  # 3 - Separate bike path
        None: 71
    },
    {  # 4 - BAANA
        None: 70,
    }
)

# Transit delay function ids
transit_delay_funcs = {
    ("bus", "bgde"): {
        "no_buslane": 1,
        "buslane": 2,
    },
    ("lightrail", "tp"): {
        "aht": 3,
        "pt": 4,
        "iht": 5,
    },
    ("rail", "rjmw"): {
        "aht": 6,
        "pt": 6,
        "iht": 6,
    },
}
# Node numbers used in HSL official networks and their allowed modes
official_node_numbers = {
    "hcvkyasf": (1, 35500), #park and ride included
    "hcvkybgdewasf": (40000, 600000),
    "hmaf": (800000, 800500),
    "hrjasf": (801000, 801500),
    "htpaf": (802000, 806000),
    "hpaf": (810000, 816000),
}
vdf_temp = ("(put(60/ul2)*(1+{}*put((volau+volad)/{})/"
            + "(ul1-get(2))))*(get(2).le.put(ul1*{}))*length+(get(2).gt."
            + "get(3))*({}*get(1)*length+{}*(get(2)-get(3))*length)")
buslane = "((lanes-1).max.0.8)"
vdf_bikes = ("length * (60/((5.max.({} + (el1.lt.0) * (1.56 * el1) +"
             +" (el1.gt.0) * (1.3 * el1))).min.({}*1.3)))")
vdf_bikes_baana = ("length*(60/((5.max.({} + (el1.lt.0) * (1.56 * el1) +"
                   +" (el1.gt.0) * (1.3 * el1))).min.35))")
vdf_bikes_mixed_lane = "(length * (60/((5.max.({flat} + (el1.lt.0) * (1.56 * el1) + (el1.gt.0) * (1.3 * el1)) + (-5).max.{vol}.min.5).min.({flat}*1.5))))"

b_volume_mixed = "(-1.962 * ln(4*(el2+el3+el4+el5+el6+10)/1000) * 0.689)"
b_volume_lane = "(-1.962 * ln(4*(el2+el3+el4+el5+el6+10)/1000) * 0.807)"
volume_delay_funcs = {
    # Car functions
    "fd1": vdf_temp.format(0.02, "lanes", 0.975, 1.78, 0.0075),
    "fd2": vdf_temp.format(0.09, "lanes", 0.935, 2.29, 0.0085),
    "fd3": vdf_temp.format(0.10, "lanes", 0.915, 2.08, 0.0110),
    "fd4": vdf_temp.format(0.20, "lanes", 0.870, 2.34, 0.0140),
    "fd5": vdf_temp.format(0.30, "lanes", 0.810, 2.28, 0.0170),
    "fd6": vdf_temp.format(0.02, buslane, 0.975, 1.78, 0.0075),
    "fd7": vdf_temp.format(0.09, buslane, 0.935, 2.29, 0.0085),
    "fd8": vdf_temp.format(0.10, buslane, 0.915, 2.08, 0.0110),
    "fd9": vdf_temp.format(0.20, buslane, 0.870, 2.34, 0.0140),
    "fd10": vdf_temp.format(0.3, buslane, 0.810, 2.28, 0.0170),
    "fd99": "length * 1.3",
    # Bike functions
    "fd70": vdf_bikes_baana.format(19),
    "fd71": vdf_bikes.format(17, 17),
    "fd72": vdf_bikes.format(17, 17),
    "fd73": vdf_bikes.format(16, 16),
    "fd74": vdf_bikes.format(15, 15),
    "fd75": vdf_bikes_mixed_lane.format(flat=12, vol=b_volume_lane),
    "fd76": vdf_bikes_mixed_lane.format(flat=12, vol=b_volume_mixed),
    "fd77": vdf_bikes_mixed_lane.format(flat=10, vol=b_volume_mixed),
    "fd78": vdf_bikes_mixed_lane.format(flat=10, vol=b_volume_mixed),
    "fd98": vdf_bikes.format(12, 12),
    # Transit functions
    ## Bus, no bus lane
    "ft01": "us2*length+timau",
    ## Bus on bus lane
    "ft02": "us2*length",
    ## Tram aht
    "ft03": "(length / (int(ul1 / 10000))) * 60",
    ## Tram pt
    "ft04": "(length / ((int(ul1 / 100)) .mod. 100)) * 60",
    ## Tram iht
    "ft05": "(length / (ul1 .mod. 100)) * 60",
    ## Train functions
    "ft6": "us1",
    ## Escape function, speed 40 km/h
    "ft7": "length/(40/60)",
    ## Turn penalty function for bikes
    "fp1": "0",
}
# Code derived from three-digit link type xyz, where x is the bus lane code,
# 2 means that bus lane is active during aht and iht periods, etc.
bus_lane_link_codes = {
    "aht": (2, 3, 4, 6),
    "pt": (3, 6),
    "iht": (2, 3, 5, 6),
}
# Bus lane delay equivalent to 1.5 km per link
buslane_delay = 60 * 1.5
# Codes defining whether transit mode stops at node, stored in data2
stop_codes = {
    't': (1, 8),
    'p': (8,),
    'b': (2, 3, 4, 5, 11),
    'g': (3, 5, 11),
    'e': (4, 5, 7, 11),
    'd': (2, 3, 4, 5, 7, 11),
}
# Node labels for HSL members (new and old fare zones)
hsl_area = "ABCDE HEXL"
# Performance settings
performance_settings = {
    "number_of_processors": "max"
}
# Inversed value of time [min/eur]
vot_inv = {
    "work": 7.576, # 1 / ((7.92 eur/h) / (60 min/h)) = 7.576 min/eur
    "business": 2.439, # 1 / ((24.60 eur/h) / (60 min/h)) = 2.439 min/eur
    "leisure": 11.173, # 1 / ((5.37 eur/h) / (60 min/h)) = 11.173 min/eur
}
# Default distance unit cost [eur/km]
dist_unit_cost = 0.12
# Parking time function
def parking_time(zone_data: ZoneData) -> pd.Series:
    density: pd.Series = (zone_data['population'] + zone_data['workplaces']) / zone_data['zone_area']
    return 0.05993817*np.sqrt(density) + 5.24176150

# Default distance unit time for trucks and trailer trucks [min/km]
freight_dist_unit_time = 0.2
# Boarding penalties for different transit modes
boarding_penalty = {
    'b': 3, # Bus
    'g': 3, # Trunk bus
    'd': 5, # Long-distance bus
    'e': 5, # Express bus
    't': 0, # Tram
    'p': 0, # Light rail
    'm': 0, # Metro
    'w': 0, # Ferry
    'r': 2, # Commuter train
    'j': 2, # Long-distance train
}
# Boarding penalties for end assignment
last_boarding_penalty = {
    'b': 5, # Bus
    'g': 2, # Trunk bus
    'd': 5, # Long-distance bus
    'e': 5, # Express bus
    't': 0, # Tram
    'p': 0, # Light rail
    'm': 0, # Metro
    'w': 0, # Ferry
    'r': 2, # Commuter train
    'j': 2, # Long-distance train
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
    "max_iterations": 400,
    "relative_gap": 0.00001,
    "best_relative_gap": 0.001,
    "normalized_gap": 0.0005,
}
# Stopping criteria for traffic assignment in loop
stopping_criteria_coarse = {
    "max_iterations": 200,
    "relative_gap": 0.0001,
    "best_relative_gap": 0.01,
    "normalized_gap": 0.005,
}
# Congestion function for congested transit assignment
congestion_func = '''
def calc_segment_cost(transit_volume, line_capacity, segment):
    if transit_volume < segment.line.seated_capacity:
        return 0.0
    return 0.8 * (transit_volume - segment.line.seated_capacity) / transit_volume
'''
trass_func = {
    'type': 'CUSTOM',
    'assignment_period': 1,
    'orig_func': False,
    'congestion_attribute': 'us3',
    'python_function': congestion_func
}
always_congested = True

# Stopping criteria for congested transit assignment
trass_stop = {
    "max_iterations": 50,
    "normalized_gap": 0.01,
    "relative_gap": 0.001
}
# Specification for the transit assignment
transfer_penalty = {
    "transit_work": 3,
    "transit_leisure": 5,
    "transit": 5,
}
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
# Factors for 24-h expansion of volumes
# TODO: Trucks and vans
volume_factors = {
    "car": {
        "aht": 2.0622815050146266,
        "pt": 10.87756099936012,
        "iht": 2.636256734240595
    },
    "car_work": {
        "aht": 2.1511371941701443,
        "pt": 9.595261522147535,
        "iht": 2.6876828857537505
    },
    "car_leisure": {
        "aht": 1.822633510494245,
        "pt": 12.416216799069286,
        "iht": 2.567335795915922
    },
    "transit": {
        "aht": 1.718651340007729,
        "pt": 9.215218973897288,
        "iht": 2.466313449878458
    },
    "transit_work": {
        "aht": 1.7648082264481162,
        "pt": 9.458785710446705,
        "iht": 2.358668559084971
    },
    "transit_leisure": {
        "aht": 1.6101278413419995,
        "pt": 8.855898570776446,
        "iht": 2.7822971006521318
    },
    "bike": {
        "aht": 1.592424507799951,
        "pt": 9.778768584286764,
        "iht": 2.430075096866623
    },
    "bike_work": {
        "aht": 1.7792746478588168,
        "pt": 9.577998573953217,
        "iht": 2.0977940770728236
    },
    "bike_leisure": {
        "aht": 1.4153296994517823,
        "pt": 9.921895075001368,
        "iht": 3.003522618985676
    },
    "trailer_truck": {
        "aht": 3.3333333333333335,
        "pt": 10.0,
        "iht": 3.3333333333333335
    },
    "truck": {
        "aht": 3.3333333333333335,
        "pt": 10.0,
        "iht": 3.3333333333333335
    },
    "van": {
        "aht": 3.3333333333333335,
        "pt": 10.0,
        "iht": 3.3333333333333335
    },
    "bus": {
        "aht": 2.0120724346076457,
        "pt": 11.11111111111111,
        "iht": 2.0120724346076457
    }
}
volume_factors["aux_transit"] = volume_factors["transit"]
# Factor for converting weekday traffic into yearly day average
years_average_day_factor = 0.85
# Factor for converting day traffic into 7:00-22:00 traffic
share_7_22_of_day = 0.9
# Noise zone width as function of start noise
noise_zone_width = {
    (0, 55): lambda x: 5,
    (55, 65): lambda x: 10 + 31./10*x,
    (65, 68): lambda x: 41 + 16./3*x,
    (68, 71): lambda x: 57 + 21./3*x,
    (71, 74): lambda x: 78 + 31./3*x,
    (74, 77): lambda x: 109 + 44./3*x,
    (77, 80): lambda x: 153 + 66./3*x,
    (80, float("inf")): lambda x: 225,
}

### ASSIGNMENT REFERENCES ###
time_periods: List[str] = ["aht", "pt", "iht"]
transport_classes = (
    "car_work",
    "car_leisure",
    "transit_work",
    "transit_leisure",
    "bike_work",
    "bike_leisure",
    "trailer_truck",
    "truck",
    "van",
)
transit_classes = (
    "transit_work",
    "transit_leisure",
)
freight_classes = (
    "van",
    "truck",
    "trailer_truck",
)
assignment_classes = {
    "hw": "work",
    "hc": "work",
    "hu": "work",
    "hs": "leisure",
    "ho": "leisure",
    "hoo": "leisure",
    "wo": "leisure",
    "oo": "leisure",
    "wh": "work",
    "hwp": "work",
    "hop": "leisure",
    "sop": "leisure",
    "oop": "leisure",
    "external": "leisure",
}
main_mode = 'h'
bike_mode = 'f'
assignment_modes = {
    "car_work": 'c',
    "car_leisure": 'c',
    "trailer_truck": 'y',
    "truck": 'k',
    "van": 'v',
}
vot_classes = {
    "car_work": "work",
    "car_leisure": "leisure",
    "trailer_truck": "business",
    "truck": "business",
    "van": "business",
}
# Distance unit cost for freight [eur/km]
freight_dist_unit_cost = {
    "truck": freight_dist_unit_time / vot_inv[vot_classes["truck"]],
    "trailer_truck": freight_dist_unit_time / vot_inv[vot_classes["trailer_truck"]],
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
external_modes = [
    "car",
    "transit",
    "truck",
    "trailer_truck",
]
segment_results = {
    "transit_volumes": "vol",
    "total_boardings": "boa",
    "transfer_boardings": "trb",
}
# Hard-coded in Emme congested transit assignment
congestion_cost = "ccost"
uncongested_transit_time = "base_timtr"
emme_matrices = {
    "car_work": ("demand", "time", "dist", "cost", "gen_cost"),
    "car_leisure": ("demand", "time", "dist", "cost", "gen_cost"),
    "transit_work": ("demand", "time", "dist", "cost"),
    "transit_leisure": ("demand", "time", "dist", "cost"),
    "bike": ("demand", "time", "dist"),
    "walk": ("time", "dist"),
    "trailer_truck": ("demand", "time", "dist", "cost", "gen_cost"),
    "truck": ("demand", "time", "dist", "cost", "gen_cost"),
    "van": ("demand", "time", "dist", "cost", "gen_cost"),
}
transit_impedance_matrices = {
    "total": {
        "total_time": "total_travel_time",
        "tw_time": "actual_total_waiting_times",
        "fw_time": "actual_first_waiting_times",
    },
    "by_mode_subset": {
        "inv_time": "actual_in_vehicle_times",
        "aux_time": "actual_aux_transit_times",
        "board_time": "actual_total_boarding_times",
        "num_board": "avg_boardings",
        "board_cost": "actual_total_boarding_costs",
    },
}
background_traffic_attr = "ul3"
inactive_line_penalty_attr = "ut1"
boarding_penalty_attr = "ut3"
is_in_transit_zone_attr = "ui1"
railtypes = {
    2: "tram",
    3: "metro",
    4: "train",
    5: "tram",
    6: "tram",
}
roadtypes = {
    0: "walkway",
    1: "motorway",
    2: "multi-lane",
    3: "multi-lane",
    4: "single-lane",
    5: "single-lane",
    99: "connector",
}
station_ids = {
    "metro": 13,
    "train": 14,
}
