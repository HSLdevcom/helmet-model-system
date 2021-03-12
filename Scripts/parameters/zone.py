# Share of demand that will be simulated in agent model
agent_demand_fraction = 1.0

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
)
areas = {
    "helsinki_cbd": (0, 999),
    "helsinki_other": (1000, 1999),
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
    "external": (31031, None),
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
    78: "Hanko",
    82: "Hattula",
    86: "Hausjarvi",
    91: "Helsinki",
    98: "Hollola",
    106: "Hyvinkaa",
    109: "Hameenlinna",
    149: "Inkoo",
    165: "Janakkala",
    186: "Jarvenpaa",
    224: "Karkkila",
    235: "Kauniainen",
    245: "Kerava",
    257: "Kirkkonummi",
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
    710: "Raasepori",
    694: "Riihimaki",
    734: "Salo",
    753: "Sipoo",
    755: "Siuntio",
    761: "Somero",
    834: "Tammela",
    858: "Tuusula",
    92: "Vantaa",
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
savu_intervals = (-175.2, -171.3, -166.56, -130.1, -123.15, -118.13, 9999)
tour_length_intervals = (0, 1, 3, 5, 10, 20, 30, 40, float("inf"))
pop_share_per_noise_area = {
    "helsinki_cbd": 0.028816313,
    "helsinki_other": 0.005536503,
    "espoo_vant_kau": 0.002148004,
    "surround_train": 0.0019966,
    "surround_other": 0.001407824,
    "peripheral": 0,  # Not calculated
}
