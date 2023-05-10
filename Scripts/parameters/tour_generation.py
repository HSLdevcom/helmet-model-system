### TOUR GENERATION PARAMETERS ####

# Scale parameter used in upper level of tour pattern model
tour_number_scale = 0.622253957
# Calibration of tour numbers
tour_number_increase = {
    1: 1,
    2: 1.002732179,
    3: 1.05446538,
    4: 1.2455917 + 0.1043963,
}
MUULITAR_CONSTANT_ZERO = 0.0
MUULITAR_CONSTANT_HW = -0.3
MUULITAR_CONSTANT_HO = 0.38
MUULITAR_CONSTANT_HU = -0.08
# Tour combinations (calibrated)
tour_combinations = {
# utility function 1
    0: {
        () : {
            "constant":   0.000000000 + MUULITAR_CONSTANT_ZERO,
            "individual_dummy": {
                "age_50-64": -0.305509545 ,
                "age_65-99":  0.597976527
            },
            "zone": {},
        },
# utility function 2
    },
    1: {
        ("hw",) : {
            "constant":   0.000000000 + 0.0210 + MUULITAR_CONSTANT_HW,
            "individual_dummy": {
                "age_18-29":  2.306249018 + 0.1065,
                "age_30-49":  2.977241136 - 0.3498,
                "age_50-64":  2.018825449 - 0.1177,
                "age_65-99": -1.185980639 - 0.0771
            },
            "zone": {
                "share_detached_houses": -0.5910000
            },
        },
# utility function 3
        ("hc",) : {
            "constant":   3.308625072 + 0.0150,
            "individual_dummy": {
                "age_7-17":  0.000000000 - 0.0641
            },
            "zone": {
                "share_detached_houses": -0.5910000
            },
        },
# utility function 4
        ("hu",) : {
            "constant":   0.000000000 + 0.3000 + MUULITAR_CONSTANT_HU,
            "individual_dummy": {
                "age_18-29":  0.000000000 + 0.0653,
                "age_30-49": -1.586979829 - 0.0192,
                "age_50-64": -3.739206239 - 1.3644,
                "age_65-99": -3.636471246 - 0.5649
            },
            "zone": {
                "share_detached_houses": -0.5910000 ,
                "hu_t":  0.148402259
            },
        },
# utility function 5
        ("hs",) : {
            "constant":   0.000000000,
            "individual_dummy": {
                "age_7-17":   0.000000000 - 0.0600,
                "age_18-29":  0.632156675 + 0.2843,
                "age_30-49":  1.106558979 - 0.6505,
                "age_50-64":  0.636516485 - 0.0855,
                "age_65-99":  1.250192981 - 0.0811
            },
            "zone": {
                "share_detached_houses": -0.5910000
            },
        },
# utility function 6
        ("ho",) : {
            "constant":   0.811674639 + MUULITAR_CONSTANT_HO,
            "individual_dummy": {
                "age_7-17":   0.000000000 - 0.1096,
                "age_18-29":  0.000000000 + 0.0679,
                "age_30-49":  0.000000000 - 0.2390,
                "age_50-64":  0.000000000 - 0.1643,
                "age_65-99":  0.394182783 - 0.1262
            },
            "zone": {
                "share_detached_houses": -0.5910000
            },
        },
# utility function 7
    },
    2: {
        ("hw", "hw") : {
            "constant":  -6.702389265 + MUULITAR_CONSTANT_HW,
            "individual_dummy": {
                "age_18-29":  2.306249018 - 1.0022,
                "age_30-49":  2.977241136 + 0.3275,
                "age_50-64":  2.018825449 - 0.1879,
                "age_65-99": -1.185980639 ,
                "car_users":  0.647176487
            },
            "zone": {
                "ho_w":  0.249875934
            },
        },
# utility function 8
        ("hw", "hu") : {
            "constant":  -8.418852173 + 0.2000 + MUULITAR_CONSTANT_HW,
            "individual_dummy": {
                "age_18-29":  2.306249018 - 0.4439,
                "age_30-49": -1.586979829 +  2.977241136 + 0.4961,
                "age_50-64": -3.739206239 +  2.018825449 + 1.6450,
                "age_65-99": -3.636471246  -1.185980639 ,
                "car_users":  0.647176487
            },
            "zone": {
                "hu_t":  0.176002681 ,
                "ho_w":  0.249875934
            },
        },
# utility function 9
        ("hw", "hs") : {
            "constant":  -5.468303413 + MUULITAR_CONSTANT_HW,
            "individual_dummy": {
                "age_18-29":  0.632156675 +  2.306249018 - 0.1900,
                "age_30-49":  1.106558979 +  2.977241136 + 0.0878,
                "age_50-64":  0.636516485 +  2.018825449 - 0.1499,
                "age_65-99":  1.250192981  -1.185980639 - 0.6537,
                "car_users":  0.647176487
            },
            "zone": {
                "ho_w":  0.249875934
            },
        },
# utility function 10
        ("hw", "ho") : {
            "constant":  -3.969665707 + MUULITAR_CONSTANT_HW,
            "individual_dummy": {
                "age_18-29":  2.306249018 + 0.0229,
                "age_30-49":  2.977241136 + 0.0059,
                "age_50-64":  2.018825449 - 0.0759,
                "age_65-99":  0.394182783  -1.185980639 - 0.1253,
                "car_users":  0.647176487
            },
            "zone": {
                "ho_w":  0.249875934
            },
        },
# utility function 11
        ("hc", "hc") : {
            "constant":  -2.189925729,
            "individual_dummy": {},
            "zone": {
                "ho_w":  0.249875934
            },
        },
# utility function 12
        ("hc", "hs") : {
            "constant":  -0.932031836,
            "individual_dummy": {
                "age_7-17":   0.000000000 - 0.0317,
                "age_18-29":  0.632156675 ,
                "age_30-49":  1.106558979 ,
                "age_50-64":  0.636516485 ,
                "age_65-99":  1.250192981
            },
            "zone": {
                "ho_w":  0.249875934
            },
        },
# utility function 13
        ("hc", "ho") : {
            "constant":   1.040646615,
            "individual_dummy": {
                "age_7-17":   0.000000000 - 0.0322,
                "age_65-99":  0.394182783
            },
            "zone": {
                "ho_w":  0.249875934
            },
        },
# utility function 14
        ("hu", "hs") : {
            "constant":  -5.264912587 + 0.0736 + MUULITAR_CONSTANT_HU,
            "individual_dummy": {
                "age_18-29":  0.632156675 - 0.0197,
                "age_30-49":  1.106558979  -1.586979829 - 0.6757,
                "age_50-64":  0.636516485  -3.739206239 + 0.7197,
                "age_65-99":  1.250192981  -3.636471246 + 0.9990,
                "car_users":  0.647176487
            },
            "zone": {
                "hu_t":  0.176002681 ,
                "ho_w":  0.249875934
            },
        },
# utility function 15
        ("hu", "ho") : {
            "constant":  -4.133565561 + 0.0834 + MUULITAR_CONSTANT_HU,
            "individual_dummy": {
                "age_18-29":  0.000000000 + 0.2038,
                "age_30-49": -1.586979829 - 0.8545,
                "age_50-64": -3.739206239 + 0.2616,
                "age_65-99":  0.394182783  -3.636471246 - 0.3497,
                "car_users":  0.647176487
            },
            "zone": {
                "hu_t":  0.176002681 ,
                "ho_w":  0.249875934
            },
        },
# utility function 16
        ("hs", "hs") : {
            "constant":  -4.347727916,
            "individual_dummy": {
                "age_18-29":  0.632156675 - 0.2125,
                "age_30-49":  1.106558979 + 0.3402,
                "age_50-64":  0.636516485 - 0.1912,
                "age_65-99":  1.250192981 - 0.0980,
                "car_users":  0.647176487
            },
            "zone": {
                "ho_w":  0.249875934
            },
        },
# utility function 17
        ("hs", "ho") : {
            "constant":  -3.615413138 + MUULITAR_CONSTANT_HO,
            "individual_dummy": {
                "age_7-17":   0.000000000 + 0.1376,
                "age_18-29":  0.632156675 + 0.0695,
                "age_30-49":  1.106558979 - 0.2025,
                "age_50-64":  0.636516485 + 0.0648,
                "age_65-99":  1.250192981 +  0.394182783 - 0.0123,
                "car_users":  0.647176487
            },
            "zone": {
                "ho_w":  0.249875934
            },
        },
# utility function 18
        ("ho", "ho") : {
            "constant":  -2.954069138 + MUULITAR_CONSTANT_HO,
            "individual_dummy": {
                "age_7-17":   0.000000000 + 0.5035,
                "age_18-29":  0.000000000 - 0.1393,
                "age_30-49":  0.000000000 + 0.1371,
                "age_50-64":  0.000000000 - 0.2130,
                "age_65-99":  0.394182783 + 0.0096,
                "car_users":  0.647176487
            },
            "zone": {
                "ho_w":  0.249875934
            },
        },
# utility function 19
    },
    3: {
        ("hw", "hw", "ho") : {
            "constant":  -7.640316015 + MUULITAR_CONSTANT_HW,
            "individual_dummy": {
                "age_18-29":  2.306249018 ,
                "age_30-49":  2.977241136 - 0.4304,
                "age_50-64":  2.018825449 + 0.6609,
                "age_65-99":  0.394182783  -1.185980639 + 2.8800,
                "car_users":  1.492056593
            },
            "zone": {},
        },
# utility function 20
        ("hw", "hs", "hs") : {
            "constant":  -6.996908123 + MUULITAR_CONSTANT_HW,
            "individual_dummy": {
                "age_18-29":  0.632156675 +  2.306249018 - 0.7910,
                "age_30-49":  1.106558979 +  2.977241136 + 0.4528,
                "age_50-64":  0.636516485 +  2.018825449 - 0.2617,
                "age_65-99":  1.250192981  -1.185980639  - 0.2451,
                "car_users":  1.492056593
            },
            "zone": {},
        },
# utility function 21
        ("hw", "hs", "ho") : {
            "constant":  -6.280857590 + MUULITAR_CONSTANT_HW,
            "individual_dummy": {
                "age_18-29":  0.632156675 +  2.306249018 + 0.2580,
                "age_30-49":  1.106558979 +  2.977241136 + 0.1582,
                "age_50-64":  0.636516485 +  2.018825449 + 0.1107,
                "age_65-99":  1.250192981 +  0.394182783  -1.185980639 + 0.4486,
                "car_users":  1.492056593
            },
            "zone": {},
        },
# utility function 22
        ("hw", "ho", "ho") : {
            "constant":  -5.143814369 + MUULITAR_CONSTANT_HW,
            "individual_dummy": {
                "age_18-29":  2.306249018 - 0.2782,
                "age_30-49":  2.977241136 + 0.3222,
                "age_50-64":  2.018825449 + 0.0418,
                "age_65-99":  0.394182783  -1.185980639 + 0.7158,
                "car_users":  1.492056593
            },
            "zone": {},
        },
# utility function 23
        ("hc", "hs", "ho") : {
            "constant":  -1.110080901,
            "individual_dummy": {
                "age_7-17":   0.000000000 - 0.1097,
                "age_18-29":  0.632156675 ,
                "age_30-49":  1.106558979 ,
                "age_50-64":  0.636516485 ,
                "age_65-99":  1.250192981 +  0.394182783
            },
            "zone": {
                "ho_w":  0.025800000
            },
        },
# utility function 24
        ("hc", "ho", "ho") : {
            "constant":   0.000000000,
            "individual_dummy": {
                "age_7-17":   0.000000000 - 0.1805,
                "age_65-99":  0.394182783
            },
            "zone": {
                "ho_w":  0.025800000
            },
        },
# utility function 25
        ("hu", "hs", "ho") : {
            "constant": -11.751808160 + MUULITAR_CONSTANT_HU,
            "individual_dummy": {
                "age_18-29":  0.632156675 + 0.1437,
                "age_30-49":  1.106558979  -1.586979829 + 0.8652,
                "age_50-64":  0.636516485  -3.739206239 + 0.9321,
                "age_65-99":  1.250192981 +  0.394182783  -3.636471246 - 1.8292,
                "car_users":  1.492056593
            },
            "zone": {
                "hu_t":  0.829445548 ,
                "ho_w":  0.025800000
            },
        },
# utility function 26
        ("hu", "ho", "ho") : {
            "constant": -11.342729830 + MUULITAR_CONSTANT_HU,
            "individual_dummy": {
                "age_18-29": -0.000000000 + 0.1541,
                "age_30-49": -1.586979829 + 0.5275,
                "age_50-64": -3.739206239 - 0.7142,
                "age_65-99":  0.394182783  -3.636471246 ,
                "car_users":  1.492056593
            },
            "zone": {
                "hu_t":  0.829445548 ,
                "ho_w":  0.025800000
            },
        },
# utility function 27
        ("hs", "hs", "hs") : {
            "constant":  -5.575050535,
            "individual_dummy": {
                "age_18-29":  0.632156675 - 2.3203,
                "age_30-49":  1.106558979 + 0.9194,
                "age_50-64":  0.636516485 ,
                "age_65-99":  1.250192981 - 0.2474,
                "car_users":  1.492056593
            },
            "zone": {
                "ho_w":  0.025800000
            },
        },
# utility function 28
        ("hs", "hs", "ho") : {
            "constant":  -4.709369964 + MUULITAR_CONSTANT_HO,
            "individual_dummy": {
                "age_18-29":  0.632156675 - 0.7508,
                "age_30-49":  1.106558979 + 0.5842,
                "age_50-64":  0.636516485 ,
                "age_65-99":  1.250192981 +  0.394182783 + 0.1375,
                "car_users":  1.492056593
            },
            "zone": {
                "ho_w":  0.025800000
            },
        },
# utility function 29
        ("hs", "ho", "ho") : {
            "constant":  -4.115616267 + MUULITAR_CONSTANT_HO,
            "individual_dummy": {
                "age_18-29":  0.632156675 - 0.1442,
                "age_30-49":  1.106558979 ,
                "age_50-64":  0.636516485 + 0.3212,
                "age_65-99":  1.250192981 +  0.394182783 + 0.1907,
                "car_users":  1.492056593
            },
            "zone": {
                "ho_w":  0.025800000
            },
        },
# utility function 30
        ("ho", "ho", "ho") : {
            "constant":  -4.110394781 + MUULITAR_CONSTANT_HO,
            "individual_dummy": {
                "age_30-49":  0.000000000 - 0.1750,
                "age_50-64":  0.000000000 + 0.1126,
                "age_65-99":  0.394182783 + 0.3557,
                "car_users":  1.492056593
            },
            "zone": {
                "ho_w":  0.025800000
            },
        },
# utility function 31
    },
    4: {
        ("hw", "hs", "hs", "ho") : {
            "constant":  -8.782904966 + MUULITAR_CONSTANT_HW,
            "individual_dummy": {
                "age_18-29":  0.632156675 +  2.306249018 ,
                "age_30-49":  1.106558979 +  2.977241136 + 0.2190,
                "age_50-64":  0.636516485 +  2.018825449 + 0.7268,
                "age_65-99":  1.250192981 +  0.394182783  -1.185980639 ,
                "car_users":  1.544612164
            },
            "zone": {
                "share_detached_houses": -0.8050000
            },
        },
# utility function 32
        ("hw", "hs", "ho", "ho") : {
            "constant":  -7.819600775 + MUULITAR_CONSTANT_HW,
            "individual_dummy": {
                "age_18-29":  0.632156675 +  2.306249018 + 0.5615,
                "age_30-49":  1.106558979 +  2.977241136 + 0.2939,
                "age_50-64":  0.636516485 +  2.018825449 + 0.1404,
                "age_65-99":  1.250192981 +  0.394182783  -1.185980639 ,
                "car_users":  1.544612164
            },
            "zone": {
                "share_detached_houses": -0.8050000
            },
        },
# utility function 33
        ("hw", "ho", "ho", "ho") : {
            "constant":  -6.323991971 + MUULITAR_CONSTANT_HW,
            "individual_dummy": {
                "age_18-29":  2.306249018 + 0.3338,
                "age_30-49":  2.977241136 ,
                "age_50-64":  2.018825449 + 0.4624,
                "age_65-99":  0.394182783  -1.185980639 ,
                "car_users":  1.544612164
            },
            "zone": {
                "share_detached_houses": -0.8050000
            },
        },
# utility function 34
        ("hs", "hs", "hs", "hs") : {
            "constant":  -6.563838110,
            "individual_dummy": {
                "age_18-29":  0.632156675 ,
                "age_30-49":  1.106558979 + 1.11106,
                "age_50-64":  0.636516485 ,
                "age_65-99":  1.250192981 - 0.6711,
                "car_users":  1.544612164
            },
            "zone": {
                "share_detached_houses": -0.8050000
            },
        },
# utility function 35
        ("hs", "hs", "hs", "ho") : {
            "constant":  -6.280534875 + MUULITAR_CONSTANT_HO,
            "individual_dummy": {
                "age_18-29":  0.632156675 - 1.3263,
                "age_30-49":  1.106558979 + 0.9876,
                "age_50-64":  0.636516485 ,
                "age_65-99":  1.250192981 +  0.394182783 - 0.3030,
                "car_users":  1.544612164
            },
            "zone": {
                "share_detached_houses": -0.8050000
            },
        },
# utility function 36
        ("hs", "hs", "ho", "ho") : {
            "constant":  -5.728407971 + MUULITAR_CONSTANT_HO,
            "individual_dummy": {
                "age_18-29":  0.632156675 - 0.8239,
                "age_30-49":  1.106558979 + 0.4522,
                "age_50-64":  0.636516485 + 0.3281,
                "age_65-99":  1.250192981 +  0.394182783 - 0.0183,
                "car_users":  1.544612164
            },
            "zone": {
                "share_detached_houses": -0.8050000
            },
        },
# utility function 37
        ("hs", "ho", "ho", "ho") : {
            "constant":  -5.167664200 + MUULITAR_CONSTANT_HO,
            "individual_dummy": {
                "age_18-29":  0.632156675 - 0.8511,
                "age_30-49":  1.106558979 + 0.7283,
                "age_50-64":  0.636516485 - 0.0824,
                "age_65-99":  1.250192981 +  0.394182783 - 0.0263,
                "car_users":  1.544612164
            },
            "zone": {
                "share_detached_houses": -0.8050000
            },
        },
# utility function 38
        ("ho", "ho", "ho", "ho") : {
            "constant":  -4.892323651 + MUULITAR_CONSTANT_HO,
            "individual_dummy": {
                "age_18-29":  0.000000000 - 2.0113,
                "age_30-49":  0.000000000 + 0.2214,
                "age_50-64":  0.000000000 + 0.6946,
                "age_65-99":  0.394182783 - 0.0943,
                "car_users":  1.544612164
            },
            "zone": {
                "share_detached_houses": -0.8050000
            },
        },
    },
}

tour_conditions = {
    ("hw",): (False, "age_7-17"),
    ("hc",): (True, "age_7-17"),
    ("hu",): (False, "age_7-17"),
    ("hw", "hw"): (False, "age_7-17"),
    ("hw", "hu"): (False, "age_7-17"),
    ("hw", "hs"): (False, "age_7-17"),
    ("hw", "ho"): (False, "age_7-17"),
    ("hc", "hc"): (True, "age_7-17"),
    ("hc", "hs"): (True, "age_7-17"),
    ("hc", "ho"): (True, "age_7-17"),
    ("hu", "hs"): (False, "age_7-17"),
    ("hu", "ho"): (False, "age_7-17"),
    ("hw", "hw", "ho"): (False, "age_7-17"),
    ("hw", "hs", "hs"): (False, "age_7-17"),
    ("hw", "hs", "ho"): (False, "age_7-17"),
    ("hw", "ho", "ho"): (False, "age_7-17"),
    ("hc", "hs", "ho"): (True, "age_7-17"),
    ("hc", "ho", "ho"): (True, "age_7-17"),
    ("hu", "hs", "ho"): (False, "age_7-17"),
    ("hu", "ho", "ho"): (False, "age_7-17"),
    ("hs", "hs", "hs"): (False, "age_7-17"),
    ("hs", "hs", "ho"): (False, "age_7-17"),
    ("hs", "ho", "ho"): (False, "age_7-17"),
    ("ho", "ho", "ho"): (False, "age_7-17"),
    ("hw", "hs", "hs", "ho"): (False, "age_7-17"),
    ("hw", "hs", "ho", "ho"): (False, "age_7-17"),
    ("hw", "ho", "ho", "ho"): (False, "age_7-17"),
    ("hs", "hs", "hs", "hs"): (False, "age_7-17"),
    ("hs", "hs", "hs", "ho"): (False, "age_7-17"),
    ("hs", "hs", "ho", "ho"): (False, "age_7-17"),
    ("hs", "ho", "ho", "ho"): (False, "age_7-17"),
    ("ho", "ho", "ho", "ho"): (False, "age_7-17"),
}
tour_generation = {
    "hw": {
        "population": 0.421190694312828,
    },
    "hc": {
        "population": 0.11729635156358,
    },
    "hu": {
        "population": 0.0560714987587779,
    },
    "hs": {
        "population": 0.33693603147271,
    },
    "ho": {
        "population": 0.549510154252463,
    },
    "hoo": {
        "hw": {
            "car": 0.0803505590286341 / 0.421190694312828,
            "transit": 0.0631860320256202 / 0.421190694312828,
            "bike": 0.0168426955247172 / 0.421190694312828,
            "walk": 0.00882652405770048 / 0.421190694312828,
        },
        "hc": {
            "car": 0.00605142271605415 / 0.11729635156358,
            "transit": 0.00713210038247794 / 0.11729635156358,
            "bike": 0.0046272430085583 / 0.11729635156358,
            "walk": 0.00608329857890972 / 0.11729635156358,
        },
        "hu": {
            "car": 0.0034663682342903 / 0.0560714987587779,
            "transit": 0.0147227519917981 / 0.0560714987587779,
            "bike": 0.00109245930286708 / 0.0560714987587779,
            "walk": 0.00213086543691209 / 0.0560714987587779,
        },
        "hs": {
            "car": 0.0448579256071604 / 0.33693603147271,
            "transit": 0.0176773452875475 / 0.33693603147271,
            "bike": 0.00359034180559277 / 0.33693603147271,
            "walk": 0.0132361046691764 / 0.33693603147271,
        },
        "ho": {
            "car": 0.0392259245387762 / 0.549510154252463,
            "transit": 0.0196074421434222 / 0.549510154252463,
            "bike": 0.00566212353370659 / 0.549510154252463,
            "walk": 0.00990947303452182 / 0.549510154252463,
        },
        "wo": {
            "car": 0.00315162485929177 / 0.065007389777543,
            "transit": 0.00177006489416014 / 0.065007389777543,
            "bike": 0.000386671503740472 / 0.065007389777543,
            "walk": 0.000584040215529239 / 0.065007389777543,
        },
        "oo": {
            "car": 0.00305390275694459 / 0.0656146108075569,
            "transit": 0.00269475052921333 / 0.0656146108075569,
            "bike": 9.23278766544668e-5 / 0.0656146108075569,
            "walk": 0.00162839340586467 / 0.0656146108075569,
        },
    },
    "wo": {
        "hw": 0.065007389777543 / 0.421190694312828, # 0.1543419
    },
    "oo": {
        "hc": 0.009279938 / 0.11729635156358, # 0.079115314
        "hu": 0.006094387 / 0.0560714987587779, # 0.108689567
        "hs": 0.000323814 / 0.33693603147271, # 0.000961055
        "ho": 0.049916472 / 0.549510154252463, # 0.090838126
    },
    "wh": {
        "workplaces": 1,
    },
    "hwp": {
        "population": (1-0.0619) * 0.229078193053959,
    },
    "hop": {
        "population": (1-0.0619) * 0.524683573054545,
    },
    "sop": {
        "population": (1-0.0619) * 0.0503171031715505,
    },
    "oop": {
        # Every sop trip continues with oop trip
        "sop": 1,
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
