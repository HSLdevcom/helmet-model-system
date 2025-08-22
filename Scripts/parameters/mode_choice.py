
### MODE CHOICE PARAMETERS ###

# Mode choice (generated 2.9.2024)
from typing import Any, Dict, Optional

mode_choice = {
    "hw": {
        "car": {
            "generation": {
                "car_density": (1.8419087570969388, 1.8419087570969388),
                "cbd": -0.2261972031022965,
                "helsinki_other": -0.08235903366262494,
                "espoo_vant_kau": 0.03921569111154971
            },
            "individual_dummy": {
                "car_users": (3.6074856629935415, 3.6074856629935415)
            },
            "log": {
                "logsum": 0.846204700122
            },
            "constant": (0.0, 0.05239649304426232),
            "attraction": {

            },
            "impedance": {

            }
        },
        "park_and_ride": {
            "generation": {
                "car_density": (1.8419087570969388, 1.8419087570969388)
            },
            "individual_dummy": {
                "car_users": (3.6074856629935415, 3.6074856629935415)
            },
            "constant": (-7.153435502280538, -7.153435502280538),
            "log": {
                "logsum": 0.846204700122
            },
            "attraction": {

            },
            "impedance": {

            }
        },
        "transit": {
            "constant": (3.892045181119219, 3.5885816616893775),
            "log": {
                "logsum": 0.846204700122
            },
            "generation": {
                "cbd": 0.14017211423427892,
                "helsinki_other": 0.2300195475835251,
                "espoo_vant_kau": -0.029778269178476834
            },
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "bike": {
            "constant": (3.23168391795719, 3.896220254428001),
            "log": {
                "logsum": 0.846204700122
            },
            "generation": {
                "cbd": -0.13457683817940885,
                "helsinki_other": 0.1317690535586124,
                "espoo_vant_kau": -0.053442079320622185
            },
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "walk": {
            "constant": (4.853946664677479, 5.03178093850044),
            "log": {
                "logsum": 0.846204700122
            },
            "generation": {
                "cbd": 0.04227258282864039,
                "helsinki_other": -0.278615000409228,
                "espoo_vant_kau": 0.20304593787521302
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
                "car_density": (2.3339063101142106, 2.3339063101142106),
                "cbd": 0.04571476006827215,
                "helsinki_other": 0.05782596834555589,
                "espoo_vant_kau": 0.02130542108021459
            },
            "log": {
                "logsum": 0.326434720015
            },
            "constant": (0.0, 0.00908584699924006),
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "transit": {
            "constant": (2.2144687352693846, 2.170808963180451),
            "log": {
                "logsum": 0.326434720015
            },
            "generation": {
                "cbd": -0.19891624059582008,
                "helsinki_other": 0.0020964230111543028,
                "espoo_vant_kau": 0.062305518340471495
            },
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "bike": {
            "constant": (1.4728449856263395, 1.5375137184638914),
            "log": {
                "logsum": 0.326434720015
            },
            "generation": {
                "cbd": -0.6505333278161437,
                "helsinki_other": -0.10495114458227507,
                "espoo_vant_kau": 0.05886221750652011
            },
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "walk": {
            "constant": (2.602936355173292, 2.4346701510818116),
            "log": {
                "logsum": 0.326434720015
            },
            "generation": {
                "cbd": -0.030357668652327995,
                "helsinki_other": 0.04990603683315477,
                "espoo_vant_kau": -0.027012359136287516
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
                "car_density": (5.378769456130001, 5.378769456130001),
                "cbd": 1.1468380363761586,
                "helsinki_other": -1.086707538381123,
                "espoo_vant_kau": 0.330941014344971
            },
            "log": {
                "logsum": 1.0
            },
            "constant": (0.0, -0.35558052895069187),
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "transit": {
            "constant": (3.55714351879, 3.2942098985225314),
            "log": {
                "logsum": 1.0
            },
            "generation": {
                "cbd": 0.017684737052973142,
                "helsinki_other": 0.2214299609100794,
                "espoo_vant_kau": -0.07183571022857849
            },
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "bike": {
            "constant": (1.54113758194, 2.347991338476329),
            "log": {
                "logsum": 1.0
            },
            "generation": {
                "cbd": -1.263123229434191,
                "helsinki_other": -0.4841214667365345,
                "espoo_vant_kau": 0.6376067468416576
            },
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "walk": {
            "constant": (3.76522269705, 2.250698715777538),
            "log": {
                "logsum": 1.0
            },
            "generation": {
                "cbd": 0.3286348521587104,
                "helsinki_other": 0.0,
                "espoo_vant_kau": 0.40103514596424106
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
                "car_density": (5.974546881661984, 5.974546881661984),
                "cbd": -0.22867307998269487,
                "helsinki_other": 0.09404944542434665,
                "espoo_vant_kau": 0.04620807947825493
            },
            "individual_dummy": {
                "car_users": (1.9063974550470684, 1.9063974550470684)
            },
            "log": {
                "logsum": 0.569238059006
            },
            "constant": (0.0, -0.038291728622315974),
            "attraction": {

            },
            "impedance": {

            }
        },
        "transit": {
            "constant": (3.869043873357799, 3.284231474780241),
            "log": {
                "logsum": 0.569238059006
            },
            "generation": {
                "cbd": 0.012907009316932283,
                "helsinki_other": -0.10278340853395418,
                "espoo_vant_kau": -0.11327177135462448
            },
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "bike": {
            "constant": (2.2137488882854215, 2.4076366024766194),
            "log": {
                "logsum": 0.569238059006
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
            "constant": (4.573762280685642, 4.336639261548451),
            "log": {
                "logsum": 0.569238059006
            },
            "generation": {
                "cbd": -0.006379691184778472,
                "helsinki_other": -0.1894189686382215,
                "espoo_vant_kau": -0.03246173890112687
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
                "car_density": (3.6815961714770133, 3.6815961714770133),
                "cbd": 0.020885928446004183,
                "helsinki_other": -0.007578556923847055,
                "espoo_vant_kau": -0.035194397373347806
            },
            "individual_dummy": {
                "car_users": (1.1590086461971614, 1.1590086461971614)
            },
            "log": {
                "logsum": 0.381035783421
            },
            "constant": (0.0, -0.01736581543846478),
            "attraction": {

            },
            "impedance": {

            }
        },
        "transit": {
            "constant": (1.6960027379888027, 1.4412111050937362),
            "log": {
                "logsum": 0.381035783421
            },
            "generation": {
                "cbd": 0.13460276438903215,
                "helsinki_other": -0.12146071299354336,
                "espoo_vant_kau": -0.25836472278905703
            },
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "bike": {
            "constant": (0.8783664029630293, 1.025796283555914),
            "log": {
                "logsum": 0.381035783421
            },
            "generation": {
                "cbd": -0.27521741904719244,
                "helsinki_other": 4.7221532734289565e-05,
                "espoo_vant_kau": -0.1427714548798185
            },
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "walk": {
            "constant": (2.6849897070455824, 2.6489751361127265),
            "log": {
                "logsum": 0.381035783421
            },
            "generation": {
                "cbd": 0.060967258148463474,
                "helsinki_other": 0.012206190904148194,
                "espoo_vant_kau": -0.16070005191535633
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
                "car_density": (4.459252566023384, 4.459252566023384),
                "cbd": -0.08410333999258551,
                "helsinki_other": -0.6852308920112927,
                "espoo_vant_kau": 0.07235849104547938
            },
            "log": {
                "logsum": 1.12287350756
            },
            "constant": (0.0, 0.3581307772052743),
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "transit": {
            "constant": (2.6096070775164617, 1.887399741861039),
            "log": {
                "logsum": 1.12287350756
            },
            "generation": {
                "cbd": -0.7788205570863099,
                "helsinki_other": -0.92433500931221,
                "espoo_vant_kau": -1.140386985689132
            },
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "bike": {
            "constant": (0.265257280721202, 1.6330442040788875),
            "log": {
                "logsum": 1.12287350756
            },
            "generation": {
                "cbd": 0.5014866754667833,
                "helsinki_other": 0.0,
                "espoo_vant_kau": -0.15794376646178737
            },
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "walk": {
            "constant": (4.5059026784451826, 4.278114705089359),
            "log": {
                "logsum": 1.12287350756
            },
            "generation": {
                "cbd": 0.5161419978844606,
                "helsinki_other": 0.3958921651384907,
                "espoo_vant_kau": 0.2638088480551107
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
                "car_density": (4.459252566023384, 4.459252566023384),
                "cbd": -0.6024023268548098,
                "helsinki_other": -0.6200859830724412,
                "espoo_vant_kau": -0.5085926779909711
            },
            "log": {
                "logsum": 1.12287350756
            },
            "constant": (0.0, -0.37762727194977136),
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "transit": {
            "constant": (2.6096070775164617, 3.4569952769734926),
            "log": {
                "logsum": 1.12287350756
            },
            "generation": {
                "cbd": -0.14595025231524159,
                "helsinki_other": 0.35057607466487495,
                "espoo_vant_kau": -0.4106502830227037
            },
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "bike": {
            "constant": (0.265257280721202, 1.926195634595997),
            "log": {
                "logsum": 1.12287350756
            },
            "generation": {
                "cbd": -0.42716208153631446,
                "helsinki_other": 0.5638785403365039,
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
            "constant": (4.5059026784451826, 4.248224957259624),
            "log": {
                "logsum": 1.12287350756
            },
            "generation": {
                "cbd": 0.5985057230153994,
                "helsinki_other": -0.2751604871431573,
                "espoo_vant_kau": -0.09445431731872163
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