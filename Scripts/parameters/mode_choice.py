
### MODE CHOICE PARAMETERS ###

# Mode choice (generated 2.9.2024)
from typing import Any, Dict, Optional

mode_choice = {
    "hw": {
        "car": {
            "generation": {
                "car_density": (1.7898027723112746, 1.7898027723112746),
                "cbd": -0.037008413632491285,
                "helsinki_other": 0.03490177595970353,
                "espoo_vant_kau": 0.010947261419875204
            },
            "individual_dummy": {
                "car_users": (3.6091937349063166, 3.6091937349063166)
            },
            "log": {
                "logsum": 0.848444967824
            },
            "constant": (0.0, 0.04866918037693277),
            "attraction": {

            },
            "impedance": {

            }
        },
        "park_and_ride": {
            "generation": {
                "car_density": (1.7898027723112746, 1.7898027723112746)
            },
            "individual_dummy": {
                "car_users": (3.6091937349063166, 3.6091937349063166)
            },
            "constant": (-7.161631577312682, -7.161631577312682),
            "log": {
                "logsum": 0.848444967824
            },
            "attraction": {

            },
            "impedance": {

            }
        },
        "transit": {
            "constant": (3.8830650314912134, 3.8537541331889713),
            "log": {
                "logsum": 0.848444967824
            },
            "generation": {
                "cbd": 0.01565395640683194,
                "helsinki_other": 0.10277273111315371,
                "espoo_vant_kau": 0.004518509760761004
            },
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "bike": {
            "constant": (3.2167179590315493, 3.106974003364469),
            "log": {
                "logsum": 0.848444967824
            },
            "generation": {
                "cbd": -0.02089260731091727,
                "helsinki_other": 0.03636642628817646,
                "espoo_vant_kau": -0.03708688092318881
            },
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "walk": {
            "constant": (4.844449835047745, 4.9236995156619905),
            "log": {
                "logsum": 0.848444967824
            },
            "generation": {
                "cbd": -0.04319871497962407,
                "helsinki_other": 0.03453667897018747,
                "espoo_vant_kau": -0.02609202241344582
            },
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        }
    },
    "hc": {
        "car": {
            "generation": {
                "car_density": (2.343248935046031, 2.343248935046031),
                "cbd": -0.11628385085360328,
                "helsinki_other": 0.004864861004898668,
                "espoo_vant_kau": 0.02454837834992644
            },
            "log": {
                "logsum": 0.326164428873
            },
            "constant": (0.0, -0.024316482463758265),
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "transit": {
            "constant": (2.23179604883763, 2.2075220599898606),
            "log": {
                "logsum": 0.326164428873
            },
            "generation": {
                "cbd": -0.11004471008796977,
                "helsinki_other": 0.007876362087636417,
                "espoo_vant_kau": 0.02361602479340828
            },
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "bike": {
            "constant": (1.4820957990801067, 1.3632079059181381),
            "log": {
                "logsum": 0.326164428873
            },
            "generation": {
                "cbd": -0.1337538745278452,
                "helsinki_other": -0.019882013497229997,
                "espoo_vant_kau": 0.001094503013325565
            },
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "walk": {
            "constant": (2.6104495735108393, 2.6192330167065974),
            "log": {
                "logsum": 0.326164428873
            },
            "generation": {
                "cbd": -0.13281194694118229,
                "helsinki_other": -0.01118902271557439,
                "espoo_vant_kau": 0.012383238692490441
            },
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        }
    },
    "hu": {
        "car": {
            "generation": {
                "car_density": (5.236065716890001, 5.236065716890001),
                "cbd": 0.05344417309440747,
                "helsinki_other": 0.04019126525706993,
                "espoo_vant_kau": 0.10173612554855303
            },
            "log": {
                "logsum": 1.0
            },
            "constant": (0.0, -0.21943436500609237),
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "transit": {
            "constant": (3.55407315155, 3.273901169121045),
            "log": {
                "logsum": 1.0
            },
            "generation": {
                "cbd": 0.06123613527848611,
                "helsinki_other": 0.08452337057787536,
                "espoo_vant_kau": 0.0911353884682568
            },
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "bike": {
            "constant": (1.51681381373, 1.0536949091086338),
            "log": {
                "logsum": 1.0
            },
            "generation": {
                "cbd": -0.012794476332995287,
                "helsinki_other": -0.003197914905620915,
                "espoo_vant_kau": 0.08067138878721908
            },
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "walk": {
            "constant": (3.73925008614, 3.5091095644132047),
            "log": {
                "logsum": 1.0
            },
            "generation": {
                "cbd": -0.01593087763350792,
                "helsinki_other": 0.0,
                "espoo_vant_kau": 0.13654043098155427
            },
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        }
    },
    "hs": {
        "car": {
            "generation": {
                "car_density": (5.978400838845634, 5.978400838845634),
                "cbd": -0.11136462966235525,
                "helsinki_other": -0.1555274224828754,
                "espoo_vant_kau": -0.10817107756903314
            },
            "individual_dummy": {
                "car_users": (1.9069069532920093, 1.9069069532920093)
            },
            "log": {
                "logsum": 0.566271563066
            },
            "constant": (0.0, -0.31382109916287226),
            "attraction": {

            },
            "impedance": {

            }
        },
        "transit": {
            "constant": (3.846394306037391, 3.7112535932191384),
            "log": {
                "logsum": 0.566271563066
            },
            "generation": {
                "cbd": -0.10534153053669418,
                "helsinki_other": -0.06330930494258853,
                "espoo_vant_kau": -0.05543873475975054
            },
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "bike": {
            "constant": (2.2139830946764185, 2.4078708088676164),
            "log": {
                "logsum": 0.566271563066
            },
            "generation": {
                "cbd": -0.30024446634581825,
                "helsinki_other": -0.10584166976230419,
                "espoo_vant_kau": -0.2019781903690947
            },
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "walk": {
            "constant": (4.570099600398595, 4.417913201690682),
            "log": {
                "logsum": 0.566271563066
            },
            "generation": {
                "cbd": -0.07259048650400303,
                "helsinki_other": -0.11086296082665595,
                "espoo_vant_kau": -0.0746335469712121
            },
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        }
    },
    "ho": {
        "car": {
            "generation": {
                "car_density": (3.6822581920944355, 3.6822581920944355),
                "cbd": 0.00787007668775943,
                "helsinki_other": -0.07086567355695766,
                "espoo_vant_kau": -0.15032710078495565
            },
            "individual_dummy": {
                "car_users": (1.1587085900464564, 1.1587085900464564)
            },
            "log": {
                "logsum": 0.379991080528
            },
            "constant": (0.0, -0.07068006671719264),
            "attraction": {

            },
            "impedance": {

            }
        },
        "transit": {
            "constant": (1.6907671490795977, 1.6126983366170327),
            "log": {
                "logsum": 0.379991080528
            },
            "generation": {
                "cbd": 0.015387551491846809,
                "helsinki_other": -0.07268844604078,
                "espoo_vant_kau": -0.1641784361843387
            },
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "bike": {
            "constant": (0.8759342178056636, 0.6804250136598654),
            "log": {
                "logsum": 0.379991080528
            },
            "generation": {
                "cbd": -0.014659239564495257,
                "helsinki_other": -0.10632388880059432,
                "espoo_vant_kau": -0.18882439916902494
            },
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "walk": {
            "constant": (2.6828511778748703, 2.6190973605926207),
            "log": {
                "logsum": 0.379991080528
            },
            "generation": {
                "cbd": -0.0152844405609704,
                "helsinki_other": -0.0961873329959448,
                "espoo_vant_kau": -0.1810075956766916
            },
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        }
    },
    "hh": {
        "car": {
            "constant": -4.193566283037721,
            "generation": {

            },
            "individual_dummy": {

            },
            "log": {

            },
            "attraction": {

            },
            "impedance": {

            }
        },
        "transit": {
            "constant": -6.219339088071782,
            "log": {

            },
            "generation": {

            },
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "bike": {
            "constant": -3.557848140624303,
            "log": {

            },
            "generation": {

            },
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "walk": {
            "constant": -0.06238631413467127,
            "log": {

            },
            "generation": {

            },
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        }
    },
    "hoo": None,
    "wo": {
        "car": {
            "generation": {
                "car_density": (4.4900540445078025, 4.4900540445078025),
                "cbd": 0.06905329678479916,
                "helsinki_other": -0.2920627819825779,
                "espoo_vant_kau": 0.0569225212269937
            },
            "log": {
                "logsum": 1.11333581055
            },
            "constant": (0.0, 0.12090020571672967),
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "transit": {
            "constant": (2.580336404612475, 2.568561179626103),
            "log": {
                "logsum": 1.11333581055
            },
            "generation": {
                "cbd": 0.1005875215437466,
                "helsinki_other": -0.21616711735439376,
                "espoo_vant_kau": 0.05430207639257846
            },
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "bike": {
            "constant": (0.25675679866725687, -0.0037172776931688745),
            "log": {
                "logsum": 1.11333581055
            },
            "generation": {
                "cbd": 0.0752779460259763,
                "helsinki_other": 0.0,
                "espoo_vant_kau": 0.005486601802273943
            },
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "walk": {
            "constant": (4.502206471590505, 4.470502464113907),
            "log": {
                "logsum": 1.11333581055
            },
            "generation": {
                "cbd": 0.11582835969442296,
                "helsinki_other": -0.16134569277670274,
                "espoo_vant_kau": 0.05710843373943807
            },
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        }
    },
    "oo": {
        "car": {
            "generation": {
                "car_density": (4.4900540445078025, 4.4900540445078025),
                "cbd": 0.22347652021946596,
                "helsinki_other": -0.2244318166542487,
                "espoo_vant_kau": -0.4107621931244809
            },
            "log": {
                "logsum": 1.11333581055
            },
            "constant": (0.0, -0.17160645389541532),
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "transit": {
            "constant": (2.580336404612475, 2.468317103768018),
            "log": {
                "logsum": 1.11333581055
            },
            "generation": {
                "cbd": 0.2661954064810847,
                "helsinki_other": -0.17517190432496774,
                "espoo_vant_kau": -0.3750648475153083
            },
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "bike": {
            "constant": (0.25675679866725687, -0.1256947722703901),
            "log": {
                "logsum": 1.11333581055
            },
            "generation": {
                "cbd": 0.23660613769179764,
                "helsinki_other": -0.23763567971481775,
                "espoo_vant_kau": 0.0
            },
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "walk": {
            "constant": (4.502206471590505, 4.344647707407288),
            "log": {
                "logsum": 1.11333581055
            },
            "generation": {
                "cbd": 0.2835877604448049,
                "helsinki_other": -0.2187236622860091,
                "espoo_vant_kau": -0.36535902148657545
            },
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        }
    },
    "wh": {
        "car": {
            "constant": (0.23100097186810603, 0.208565625679477),
            "generation": {

            },
            "attraction": {

            },
            "impedance": {

            },
            "log": {
                "logsum": 0.830938747727
            },
            "individual_dummy": {

            }
        },
        "transit": {
            "constant": (2.6998874096268315, 2.3484376591912706),
            "generation": {

            },
            "attraction": {

            },
            "impedance": {

            },
            "log": {
                "logsum": 0.830938747727
            },
            "individual_dummy": {

            }
        },
        "bike": {
            "constant": (3.148907265438679, 3.6170161206362916),
            "generation": {

            },
            "attraction": {

            },
            "impedance": {

            },
            "log": {
                "logsum": 0.830938747727
            },
            "individual_dummy": {

            }
        },
        "walk": {
            "constant": (5.184886160179416, 5.072700877314392),
            "generation": {

            },
            "attraction": {

            },
            "impedance": {

            },
            "log": {
                "logsum": 0.830938747727
            },
            "individual_dummy": {

            }
        }
    },
    "hwp": {
        "car": {
            "constant": 0.024,
            "generation": {

            },
            "attraction": {

            },
            "impedance": {

            },
            "log": {
                "logsum": 1.0
            },
            "individual_dummy": {

            }
        },
        "transit": {
            "constant": -2.0319384929799997,
            "generation": {

            },
            "attraction": {

            },
            "impedance": {

            },
            "log": {
                "logsum": 1.0
            },
            "individual_dummy": {

            }
        }
    },
    "hop": {
        "car": {
            "constant": 0.075,
            "generation": {

            },
            "attraction": {

            },
            "impedance": {

            },
            "log": {
                "logsum": 1.0
            },
            "individual_dummy": {

            }
        },
        "transit": {
            "constant": -1.10107987269,
            "generation": {

            },
            "attraction": {

            },
            "impedance": {

            },
            "log": {
                "logsum": 1.0
            },
            "individual_dummy": {

            }
        }
    },
    "sop": {
        "car": {
            "constant": 0.0,
            "generation": {

            },
            "attraction": {
                "own_zone_area": -0.01478815,
                "parking_cost_work": -0.154340268
            },
            "impedance": {
                "time": -0.021262374,
                "cost": -0.154340268
            },
            "log": {

            },
            "individual_dummy": {

            }
        },
        "transit": {
            "constant": -2.060141017,
            "generation": {

            },
            "attraction": {
                "own_zone_area": -0.115937409151
            },
            "impedance": {
                "time": -0.007909217,
                "cost": -0.0051446756
            },
            "log": {

            },
            "individual_dummy": {

            }
        }
    },
    "oop": {
        "car": {
            "constant": 0.09656174479207501,
            "generation": {

            },
            "attraction": {

            },
            "impedance": {

            },
            "log": {
                "logsum": 0.715272183645
            },
            "individual_dummy": {

            }
        },
        "transit": {
            "constant": -2.2893821531891683,
            "generation": {

            },
            "attraction": {

            },
            "impedance": {

            },
            "log": {
                "logsum": 0.715272183645
            },
            "individual_dummy": {

            }
        }
    }
}