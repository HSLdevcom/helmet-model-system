
### MODE CHOICE PARAMETERS ###

# Mode choice (generated 2.9.2024)
from typing import Any, Dict, Optional
from parameters.assignment import inflation

mode_choice = {
    "hw": {
        "car": {
            "generation": {
                "car_density": (1.7921683550474736, 1.7921683550474736),
                "cbd": -0.438646,
                "helsinki_other": -0.139598,
                "espoo_vant_kau": -0.02144
            },
            "individual_dummy": {
                "car_users": (3.6090751065009843, 3.6090751065009843)
            },
            "log": {
                "logsum": 0.847425745398
            },
            "constant": (0.0, 0.094026),
            "attraction": {

            },
            "impedance": {

            }
        },
        "park_and_ride": {
            "generation": {
                "car_density": (1.7921683550474736, 1.7921683550474736),
                "cbd": 0.0,
                "helsinki_other": 0.713344,
                "espoo_vant_kau": 0.01634
            },
            "individual_dummy": {
                "car_users": (3.6090751065009843, 3.6090751065009843)
            },
            "constant": (-7.199376254626492, -6.610862254626492),
            "log": {
                "logsum": 0.847425745398
            },
            "attraction": {

            },
            "impedance": {

            }
        },
        "transit": {
            "constant": (3.8276876271995444, 3.5440586271995445),
            "log": {
                "logsum": 0.847425745398
            },
            "generation": {
                "cbd": 0.152967,
                "helsinki_other": 0.376262,
                "espoo_vant_kau": 0.034405
            },
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "bike": {
            "constant": (3.17588007404681, 3.9205260740468098),
            "log": {
                "logsum": 0.847425745398
            },
            "generation": {
                "cbd": -0.158448,
                "helsinki_other": 0.265807,
                "espoo_vant_kau": 0.011076
            },
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "walk": {
            "constant": (4.80073933289332, 5.1265413328933205),
            "log": {
                "logsum": 0.847425745398
            },
            "generation": {
                "cbd": 0.06007,
                "helsinki_other": -0.098367,
                "espoo_vant_kau": 0.309292
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
                "cbd": 0.314974,
                "helsinki_other": 0.139569,
                "espoo_vant_kau": -0.03956
            },
            "log": {
                "logsum": 0.326164428873
            },
            "constant": (0.0, 0.113179),
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "transit": {
            "constant": (2.23179604883763, 2.15717804883763),
            "log": {
                "logsum": 0.326164428873
            },
            "generation": {
                "cbd": -0.40563,
                "helsinki_other": -0.031242,
                "espoo_vant_kau": 0.15581
            },
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "bike": {
            "constant": (1.4820957990801067, 1.7727947990801067),
            "log": {
                "logsum": 0.326164428873
            },
            "generation": {
                "cbd": -1.78199,
                "helsinki_other": -0.276853,
                "espoo_vant_kau": 0.225941
            },
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "walk": {
            "constant": (2.6104495735108393, 2.2259845735108392),
            "log": {
                "logsum": 0.326164428873
            },
            "generation": {
                "cbd": 0.173547,
                "helsinki_other": 0.178262,
                "espoo_vant_kau": -0.116455
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
                "car_density": (5.22223737983, 5.22223737983),
                "cbd": 1.199549,
                "helsinki_other": -0.895205,
                "espoo_vant_kau": 0.658114
            },
            "log": {
                "logsum": 1.0
            },
            "constant": (0.0, -0.419355),
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "transit": {
            "constant": (3.42283129783, 3.14379729783),
            "log": {
                "logsum": 1.0
            },
            "generation": {
                "cbd": 0.005255,
                "helsinki_other": 0.447224,
                "espoo_vant_kau": 0.199835
            },
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "bike": {
            "constant": (1.43205591145, 1.96375391145),
            "log": {
                "logsum": 1.0
            },
            "generation": {
                "cbd": -1.259046,
                "helsinki_other": -0.272718,
                "espoo_vant_kau": 0.938277
            },
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "walk": {
            "constant": (3.65353450737, 2.15252650737),
            "log": {
                "logsum": 1.0
            },
            "generation": {
                "cbd": 0.38566,
                "helsinki_other": 0.0,
                "espoo_vant_kau": 0.718669
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
                "car_density": (5.907289797779808, 5.907289797779808),
                "cbd": -0.52381,
                "helsinki_other": 0.126528,
                "espoo_vant_kau": 0.030168
            },
            "individual_dummy": {
                "car_users": (1.9070931560304134, 1.9070931560304134)
            },
            "log": {
                "logsum": 0.573330213613
            },
            "constant": (0.0, -0.141276),
            "attraction": {

            },
            "impedance": {

            }
        },
        "transit": {
            "constant": (3.6878661531884274, 2.544663153188427),
            "log": {
                "logsum": 0.573330213613
            },
            "generation": {
                "cbd": -0.100078,
                "helsinki_other": -0.134304,
                "espoo_vant_kau": -0.242548
            },
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "bike": {
            "constant": (2.1441324758494504, 2.3943954758494503),
            "log": {
                "logsum": 0.573330213613
            },
            "generation": {
                "cbd": -0.591871,
                "helsinki_other": -0.187254,
                "espoo_vant_kau": -0.329228
            },
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "walk": {
            "constant": (4.507839950982731, 4.053192950982732),
            "log": {
                "logsum": 0.573330213613
            },
            "generation": {
                "cbd": -0.07066,
                "helsinki_other": -0.355869,
                "espoo_vant_kau": -0.022239
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
                "car_density": (3.662561532326187, 3.662561532326187),
                "cbd": -0.155577,
                "helsinki_other": -0.03931,
                "espoo_vant_kau": -0.087526
            },
            "individual_dummy": {
                "car_users": (1.1586558137394463, 1.1586558137394463)
            },
            "log": {
                "logsum": 0.381207914414
            },
            "constant": (0.0, -0.029363),
            "attraction": {

            },
            "impedance": {

            }
        },
        "transit": {
            "constant": (1.6351725273861322, 0.8689065273861322),
            "log": {
                "logsum": 0.381207914414
            },
            "generation": {
                "cbd": 0.293002,
                "helsinki_other": -0.173683,
                "espoo_vant_kau": -0.561474
            },
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "bike": {
            "constant": (0.843779672021141, 1.247050672021141),
            "log": {
                "logsum": 0.381207914414
            },
            "generation": {
                "cbd": -0.664021,
                "helsinki_other": 0.000548,
                "espoo_vant_kau": -0.174776
            },
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "walk": {
            "constant": (2.6527081396946057, 2.7191791396946057),
            "log": {
                "logsum": 0.381207914414
            },
            "generation": {
                "cbd": 0.088556,
                "helsinki_other": -0.034588,
                "espoo_vant_kau": -0.302973
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
                "car_density": (4.416300680023366, 4.416300680023366),
                "cbd": -0.285316,
                "helsinki_other": -0.956804,
                "espoo_vant_kau": 0.329168
            },
            "log": {
                "logsum": 1.12299531875
            },
            "constant": (0.0, 0.398299),
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "transit": {
            "constant": (2.3006034978506906, 2.1889504978506906),
            "log": {
                "logsum": 1.12299531875
            },
            "generation": {
                "cbd": -0.202912,
                "helsinki_other": -1.281818,
                "espoo_vant_kau": -1.982158
            },
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "bike": {
            "constant": (0.1281877124330426, 1.3258297124330427),
            "log": {
                "logsum": 1.12299531875
            },
            "generation": {
                "cbd": 0.296278,
                "helsinki_other": 0.0,
                "espoo_vant_kau": -0.414908
            },
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "walk": {
            "constant": (4.368536806736074, 4.006921806736074),
            "log": {
                "logsum": 1.12299531875
            },
            "generation": {
                "cbd": 0.453938,
                "helsinki_other": 0.219015,
                "espoo_vant_kau": 0.375856
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
                "car_density": (4.416300680023366, 4.416300680023366),
                "cbd": -0.446814,
                "helsinki_other": -0.867228,
                "espoo_vant_kau": -0.913714
            },
            "log": {
                "logsum": 1.12299531875
            },
            "constant": (0.0, -0.517369),
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "transit": {
            "constant": (2.3006034978506906, 3.0644314978506904),
            "log": {
                "logsum": 1.12299531875
            },
            "generation": {
                "cbd": -0.19662,
                "helsinki_other": 0.070267,
                "espoo_vant_kau": -0.571636
            },
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "bike": {
            "constant": (0.1281877124330426, 1.3912847124330425),
            "log": {
                "logsum": 1.12299531875
            },
            "generation": {
                "cbd": -0.19504,
                "helsinki_other": 0.383128,
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
            "constant": (4.368536806736074, 4.049314806736074),
            "log": {
                "logsum": 1.12299531875
            },
            "generation": {
                "cbd": 0.856315,
                "helsinki_other": -0.4442,
                "espoo_vant_kau": -0.403491
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
                "cost": -0.154340268/inflation
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
                "cost": -0.154340268/inflation
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