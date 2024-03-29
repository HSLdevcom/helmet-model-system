# Share of demand that will be simulated in agent model
from typing import Any, Dict, List, Tuple, Union


agent_demand_fraction = 1.0

# Seed number for population attributes:
# int = fixed seed and same population for each run
# None = different population for each run
population_draw = 31

# Age groups in zone data
age_groups: List[Tuple[int, int]] = [ #changed to list for type checker
        (7, 17),
        (18, 29),
        (30, 49),
        (50, 64),
        (65, 99),
]

### DEMAND MODEL REFERENCES ###

tour_purposes: List[Dict[str, Any]] = [ #changed to list for type checker
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
        "name": "wo",
        "orig": "source",
        "dest": "other",
        "source": ("hw",),
        "area": "all",
    },
    {
        "name": "oo",
        "orig": "source",
        "dest": "other",
        "source": ("hc", "hu", "hs", "ho",),
        "area": "all",
    },
    {
        "name": "hoo",
        "orig": "home",
        "dest": "any",
        "sec_dest": "any",
        "source": ("hw", "hc", "hu", "hs", "ho", "wo", "oo",),
        "area": "metropolitan",
    },
    {  # Only for calculation of work-force accessibility, not assigned
        "name": "wh",
        "orig": "work",
        "dest": "source",
        "area": "metropolitan",
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
]
# Tour purpose zone intervals
# Some demand models have separate sub-region parameters,
# hence need sub-intervals defined.
purpose_areas: Dict[str, Union[Tuple[int,int],Tuple[int,int,int]]] = {
    "metropolitan": (0, 6000, 16000),
    "peripheral": (16000, 31000),
    "all": (0, 6000, 31000),
    "external": (31031, 34999),
}
areas = {
    "helsinki_cbd": (0, 999),
    "helsinki_other": (1000, 1999),
    "lauttasaari": (1000, 1014),
    "espoo_vant_kau": (2000, 5999),
    "surrounding": (6000, 15999),
    "surround_train": (
        (6000, 6999),
        (10000, 11999),
        (13000, 14999),
        (15500, 15999),
    ),
    "surround_other": (
        (7000, 9999),
        (12000, 12999),
        (15000, 15499),
    ),
    "peripheral": (16000, 30999),
    "external": (31031, 34999),
}
municipalities = {
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
    "Hanko": (17500, 17999),
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
kela_codes = {
    18: "Askola",
    49: "Espoo",
    61: "Forssa",
    78: "Hanko",
    82: "Hattula",
    86: "Hausjarvi",
    88: "Heinola",
    91: "Helsinki",
    92: "Vantaa",
    98: "Hollola",
    106: "Hyvinkaa",
    109: "Hameenlinna",
    142: "Iitti",
    149: "Inkoo",
    165: "Janakkala",
    169: "Jokioinen",
    186: "Jarvenpaa",
    224: "Karkkila",
    235: "Kauniainen",
    245: "Kerava",
    257: "Kirkkonummi",
    286: "Kouvola",
    316: "Karkola",
    398: "Lahti",
    407: "Lapinjarvi",
    444: "Lohja",
    433: "Loppi",
    434: "Loviisa",
    504: "Myrskyla",
    505: "Mantsala",
    543: "Nurmijarvi",
    560: "Orimattila",
    611: "Pornainen",
    638: "Porvoo",
    616: "Pukkila",
    624: "Pyhtaa",
    635: "Palkane",
    710: "Raasepori",
    694: "Riihimaki",
    734: "Salo",
    753: "Sipoo",
    755: "Siuntio",
    761: "Somero",
    834: "Tammela",
    858: "Tuusula",
    908: "Valkeakoski",
    927: "Vihti",
}
area_aggregation = (
    "helsinki_cbd",
    "helsinki_other",
    "espoo_vant_kau",
    "surround_train",
    "surround_other",
    "peripheral",
)
helsinki_cbd = (
    (25500485.22, 6670292.79),
    (25500113.55, 6673489.08),
    (25500206.01, 6674219.76),
    (25499290.41, 6674802.09),
    (25499887.56, 6676162.52),
    (25499179.77, 6677001.66),
    (25499324.67, 6677489.18),
    (25499116.86, 6677867.67),
    (25499197.08, 6678075.14),
    (25498885.23, 6678310.97),
    (25498883.07, 6678695.60),
    (25498027.56, 6679029.91),
    (25497200.97, 6678835.01),
    (25496572.08, 6678417.84),
    (25495643.82, 6678288.74),
    (25495718.82, 6678613.43),
    (25495215.72, 6678541.07),
    (25494930.06, 6677273.16),
    (25494137.91, 6677151.48),
    (25493932.98, 6676022.04),
    (25493452.62, 6675415.07),
    (25492719.18, 6673875.36),
    (25494293.55, 6672560.53),
    (25494289.62, 6669969.36),
    (25496587.35, 6669967.52),
    (25496587.89, 6670410.54),
    (25497356.88, 6670409.62),
    (25499970.42, 6667780.03),
    (25499637.69, 6668606.90),
    (25499538.96, 6669673.01),
    (25500485.22, 6670292.79),
)
savu_intervals = (-172.85, -169.77, -167.11, -161.52, -156.85, -152.07, 9999)
tour_length_intervals = (0, 1, 3, 5, 10, 20, 30, 40, float("inf"))
# Population in noise zones as share of total area population as
# function only of zone area, calculated by Ramboll Feb 2021
pop_share_per_noise_area = {
    "helsinki_cbd": 0.028816313,
    "helsinki_other": 0.005536503,
    "espoo_vant_kau": 0.002148004,
    "surround_train": 0.0019966,
    "surround_other": 0.001407824,
    "peripheral": 0,  # Not calculated
}
