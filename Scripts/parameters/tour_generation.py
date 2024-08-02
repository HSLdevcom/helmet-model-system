
### TOUR GENERATION PARAMETERS ####

# Scale parameter used in upper level of tour pattern model
#tour_number_scale = 0.622253957 #2018
tour_number_scale = 0.671569412046 #2024
# Calibration of tour numbers
tour_number_increase = {
    1: 1,
    2: 1.002732179,
    3: 1.05446538,
    4: 1.2455917 + 0.1043963,
}
# Tour combinations 2024 (calibrated)
tour_combinations = {
    0: {
        (): {
            "constant": 0.0,
            "individual_dummy": {
                "age_50-64": -0.219468849303,
                "age_65-99": 0.126061945454
            },
            "zone": {

            }
        }
    },
    1: {
        ("hw",): {
            "constant": 0,
            "individual_dummy": {
                "age_18-29": 1.48000908915,
                "age_30-49": 1.8797429117,
                "age_50-64": 1.44353710396,
                "age_65-99": -1.59680564297
            },
            "zone": {
                "share_detached_houses": -0.401227681496
            }
        },
        ("hc",): {
            "constant": 3.45389775551,
            "individual_dummy": {
                "age_7-17": 0
            },
            "zone": {
                "share_detached_houses": -0.401227681496
            }
        },
        ("hu",): {
            "constant": 0,
            "individual_dummy": {
                "age_18-29": 0,
                "age_30-49": -2.15205230059,
                "age_50-64": -3.62380885808,
                "age_65-99": -4.26302735239
            },
            "zone": {
                "share_detached_houses": -0.401227681496,
                "hu_t": 0.0754795814242
            }
        },
        ("hs",): {
            "constant": 0,
            "individual_dummy": {
                "age_7-17": 0,
                "age_18-29": 0.0966718013031,
                "age_30-49": 0.690854372304,
                "age_50-64": -0.0639518986382,
                "age_65-99": 0.467782547031
            },
            "zone": {
                "share_detached_houses": -0.401227681496
            }
        },
        ("ho",): {
            "constant": 0.467991377055,
            "individual_dummy": {
                "age_7-17": 0,
                "age_18-29": 0,
                "age_30-49": 0,
                "age_50-64": 0,
                "age_65-99": 0.209048267514
            },
            "zone": {
                "share_detached_houses": -0.401227681496
            }
        }
    },
    2: {
        ("hw", "hw"): {
            "constant": -5.77062931075,
            "individual_dummy": {
                "age_18-29": 1.48000908915,
                "age_30-49": 1.8797429117,
                "age_50-64": 1.44353710396,
                "age_65-99": -1.59680564297,
                "car_users": -0.271590141734
            },
            "zone": {
                "ho_w": 0.164973343238
            }
        },
        ("hw", "hu"): {
            "constant": -7.10710355438,
            "individual_dummy": {
                "age_18-29": 1.48000908915,
                "age_30-49": -0.2723093888899999,
                "age_50-64": -2.1802717541199996,
                "age_65-99": -5.85983299536,
                "car_users": -0.271590141734
            },
            "zone": {
                "hu_t": 0.197031975021,
                "ho_w": 0.164973343238
            }
        },
        ("hw", "hs"): {
            "constant": -3.9600434707,
            "individual_dummy": {
                "age_18-29": 1.5766808904531,
                "age_30-49": 2.570597284004,
                "age_50-64": 1.3795852053218,
                "age_65-99": -1.129023095939,
                "car_users": -0.271590141734
            },
            "zone": {
                "ho_w": 0.164973343238
            }
        },
        ("hw", "ho"): {
            "constant": -2.9391852913,
            "individual_dummy": {
                "age_18-29": 1.48000908915,
                "age_30-49": 1.8797429117,
                "age_50-64": 1.44353710396,
                "age_65-99": -1.387757375456,
                "car_users": -0.271590141734
            },
            "zone": {
                "ho_w": 0.164973343238
            }
        },
        ("hc", "hc"): {
            "constant": -1.59596665213,
            "individual_dummy": {

            },
            "zone": {
                "ho_w": 0.164973343238
            }
        },
        ("hc", "hs"): {
            "constant": -0.387809421555,
            "individual_dummy": {
                "age_7-17": 0,
                "age_18-29": 0.0966718013031,
                "age_30-49": 0.690854372304,
                "age_50-64": -0.0639518986382,
                "age_65-99": 0.467782547031
            },
            "zone": {
                "ho_w": 0.164973343238
            }
        },
        ("hc", "ho"): {
            "constant": 1.83604857913,
            "individual_dummy": {
                "age_7-17": 0,
                "age_65-99": 0.209048267514
            },
            "zone": {
                "ho_w": 0.164973343238
            }
        },
        ("hu", "hs"): {
            "constant": -4.6664837601,
            "individual_dummy": {
                "age_18-29": 0.0966718013031,
                "age_30-49": -1.461197928286,
                "age_50-64": -3.6877607567182,
                "age_65-99": -3.795244805359,
                "car_users": -0.271590141734
            },
            "zone": {
                "hu_t": 0.197031975021,
                "ho_w": 0.164973343238
            }
        },
        ("hu", "ho"): {
            "constant": -4.01110604041,
            "individual_dummy": {
                "age_18-29": 0,
                "age_30-49": -2.15205230059,
                "age_50-64": -3.62380885808,
                "age_65-99": -4.053979084876,
                "car_users": -0.271590141734
            },
            "zone": {
                "hu_t": 0.197031975021,
                "ho_w": 0.164973343238
            }
        },
        ("hs", "hs"): {
            "constant": -3.12841230127,
            "individual_dummy": {
                "age_18-29": 0.0966718013031,
                "age_30-49": 0.690854372304,
                "age_50-64": -0.0639518986382,
                "age_65-99": 0.467782547031,
                "car_users": -0.271590141734
            },
            "zone": {
                "ho_w": 0.164973343238
            }
        },
        ("hs", "ho"): {
            "constant": -2.37347845681,
            "individual_dummy": {
                "age_7-17": 0,
                "age_18-29": 0.0966718013031,
                "age_30-49": 0.690854372304,
                "age_50-64": -0.0639518986382,
                "age_65-99": 0.6768308145449999,
                "car_users": -0.271590141734
            },
            "zone": {
                "ho_w": 0.164973343238
            }
        },
        ("ho", "ho"): {
            "constant": -2.38213267521,
            "individual_dummy": {
                "age_7-17": 0,
                "age_18-29": 0,
                "age_30-49": 0,
                "age_50-64": 0,
                "age_65-99": 0.209048267514,
                "car_users": -0.271590141734
            },
            "zone": {
                "ho_w": 0.164973343238
            }
        }
    },
    3: {
        ("hw", "hw", "ho"): {
            "constant": -5.43611772875,
            "individual_dummy": {
                "age_18-29": 1.48000908915,
                "age_30-49": 1.8797429117,
                "age_50-64": 1.44353710396,
                "age_65-99": -1.387757375456,
                "car_users": -23.4898042934
            },
            "zone": {

            }
        },
        ("hw", "hs", "hs"): {
            "constant": -5.21759447377,
            "individual_dummy": {
                "age_18-29": 1.5766808904531,
                "age_30-49": 2.570597284004,
                "age_50-64": 1.3795852053218,
                "age_65-99": -1.129023095939,
                "car_users": -23.4898042934
            },
            "zone": {

            }
        },
        ("hw", "hs", "ho"): {
            "constant": -4.30215385706,
            "individual_dummy": {
                "age_18-29": 1.5766808904531,
                "age_30-49": 2.570597284004,
                "age_50-64": 1.3795852053218,
                "age_65-99": -0.919974828425,
                "car_users": -23.4898042934
            },
            "zone": {

            }
        },
        ("hw", "ho", "ho"): {
            "constant": -3.59297683406,
            "individual_dummy": {
                "age_18-29": 1.48000908915,
                "age_30-49": 1.8797429117,
                "age_50-64": 1.44353710396,
                "age_65-99": -1.387757375456,
                "car_users": -23.4898042934
            },
            "zone": {

            }
        },
        ("hc", "hs", "ho"): {
            "constant": -1.34856140687,
            "individual_dummy": {
                "age_7-17": 0,
                "age_18-29": 0.0966718013031,
                "age_30-49": 0.690854372304,
                "age_50-64": -0.0639518986382,
                "age_65-99": 0.6768308145449999
            },
            "zone": {
                "ho_w": -0.048406807307
            }
        },
        ("hc", "ho", "ho"): {
            "constant": 0,
            "individual_dummy": {
                "age_7-17": 0,
                "age_65-99": 0.209048267514
            },
            "zone": {
                "ho_w": -0.048406807307
            }
        },
        ("hu", "hs", "ho"): {
            "constant": -14.0727751499,
            "individual_dummy": {
                "age_18-29": 0.0966718013031,
                "age_30-49": -1.461197928286,
                "age_50-64": -3.6877607567182,
                "age_65-99": -3.586196537845,
                "car_users": -23.4898042934
            },
            "zone": {
                "hu_t": 1.06571914257,
                "ho_w": -0.048406807307
            }
        },
        ("hu", "ho", "ho"): {
            "constant": -12.4878824712,
            "individual_dummy": {
                "age_18-29": 0,
                "age_30-49": -2.15205230059,
                "age_50-64": -3.62380885808,
                "age_65-99": -4.053979084876,
                "car_users": -23.4898042934
            },
            "zone": {
                "hu_t": 1.06571914257,
                "ho_w": -0.048406807307
            }
        },
        ("hs", "hs", "hs"): {
            "constant": -3.91906444474,
            "individual_dummy": {
                "age_18-29": 0.0966718013031,
                "age_30-49": 0.690854372304,
                "age_50-64": -0.0639518986382,
                "age_65-99": 0.467782547031,
                "car_users": -23.4898042934
            },
            "zone": {
                "ho_w": -0.048406807307
            }
        },
        ("hs", "hs", "ho"): {
            "constant": -2.80062151034,
            "individual_dummy": {
                "age_18-29": 0.0966718013031,
                "age_30-49": 0.690854372304,
                "age_50-64": -0.0639518986382,
                "age_65-99": 0.6768308145449999,
                "car_users": -23.4898042934
            },
            "zone": {
                "ho_w": -0.048406807307
            }
        },
        ("hs", "ho", "ho"): {
            "constant": -2.21042449832,
            "individual_dummy": {
                "age_18-29": 0.0966718013031,
                "age_30-49": 0.690854372304,
                "age_50-64": -0.0639518986382,
                "age_65-99": 0.6768308145449999,
                "car_users": -23.4898042934
            },
            "zone": {
                "ho_w": -0.048406807307
            }
        },
        ("ho", "ho", "ho"): {
            "constant": -2.35994153342,
            "individual_dummy": {
                "age_30-49": 0,
                "age_50-64": 0,
                "age_65-99": 0.209048267514,
                "car_users": -23.4898042934
            },
            "zone": {
                "ho_w": -0.048406807307
            }
        }
    },
    4: {
        ("hw", "hs", "hs", "ho"): {
            "constant": -7.4202093218,
            "individual_dummy": {
                "age_18-29": 1.5766808904531,
                "age_30-49": 2.570597284004,
                "age_50-64": 1.3795852053218,
                "age_65-99": -0.919974828425,
                "car_users": -22.3120504425
            },
            "zone": {
                "share_detached_houses": 0.521683236366
            }
        },
        ("hw", "hs", "ho", "ho"): {
            "constant": -6.66991760726,
            "individual_dummy": {
                "age_18-29": 1.5766808904531,
                "age_30-49": 2.570597284004,
                "age_50-64": 1.3795852053218,
                "age_65-99": -0.919974828425,
                "car_users": -22.3120504425
            },
            "zone": {
                "share_detached_houses": 0.521683236366
            }
        },
        ("hw", "ho", "ho", "ho"): {
            "constant": -5.50152062388,
            "individual_dummy": {
                "age_18-29": 1.48000908915,
                "age_30-49": 1.8797429117,
                "age_50-64": 1.44353710396,
                "age_65-99": -1.387757375456,
                "car_users": -22.3120504425
            },
            "zone": {
                "share_detached_houses": 0.521683236366
            }
        },
        ("hs", "hs", "hs", "hs"): {
            "constant": -7.17443262087,
            "individual_dummy": {
                "age_18-29": 0.0966718013031,
                "age_30-49": 0.690854372304,
                "age_50-64": -0.0639518986382,
                "age_65-99": 0.467782547031,
                "car_users": -22.3120504425
            },
            "zone": {
                "share_detached_houses": 0.521683236366
            }
        },
        ("hs", "hs", "hs", "ho"): {
            "constant": -4.92378407588,
            "individual_dummy": {
                "age_18-29": 0.0966718013031,
                "age_30-49": 0.690854372304,
                "age_50-64": -0.0639518986382,
                "age_65-99": 0.6768308145449999,
                "car_users": -22.3120504425
            },
            "zone": {
                "share_detached_houses": 0.521683236366
            }
        },
        ("hs", "hs", "ho", "ho"): {
            "constant": -4.44757184886,
            "individual_dummy": {
                "age_18-29": 0.0966718013031,
                "age_30-49": 0.690854372304,
                "age_50-64": -0.0639518986382,
                "age_65-99": 0.6768308145449999,
                "car_users": -22.3120504425
            },
            "zone": {
                "share_detached_houses": 0.521683236366
            }
        },
        ("hs", "ho", "ho", "ho"): {
            "constant": -4.3421395638,
            "individual_dummy": {
                "age_18-29": 0.0966718013031,
                "age_30-49": 0.690854372304,
                "age_50-64": -0.0639518986382,
                "age_65-99": 0.6768308145449999,
                "car_users": -22.3120504425
            },
            "zone": {
                "share_detached_houses": 0.521683236366
            }
        },
        ("ho", "ho", "ho", "ho"): {
            "constant": -4.05509456402,
            "individual_dummy": {
                "age_18-29": 0,
                "age_30-49": 0,
                "age_50-64": 0,
                "age_65-99": 0.209048267514,
                "car_users": -22.3120504425
            },
            "zone": {
                "share_detached_houses": 0.521683236366
            }
        }
    }
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
