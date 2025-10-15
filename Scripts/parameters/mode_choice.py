
### MODE CHOICE PARAMETERS ###

# Mode choice (generated 2.9.2024)
from typing import Any, Dict, Optional
from parameters.assignment import inflation

mode_choice = {
    "hw": {
        "car": {
            "generation": {
                "car_density": (1.7982204256248782, 1.7982204256248782),
                "cbd": -0.438646,
                "helsinki_other": -0.139598,
                "espoo_vant_kau": -0.02144
            },
            "individual_dummy": {
                "car_users": (3.6090816689609784, 3.6090816689609784)
            },
            "log": {
                "logsum": 0.845599347812
            },
            "constant": (0.0, 0.094026),
            "attraction": {

            },
            "impedance": {

            }
        },
        "park_and_ride": {
            "generation": {
                "car_density": (1.7982204256248782, 1.7982204256248782),
                "cbd": 0.0,
                "helsinki_other": 0.713344,
                "espoo_vant_kau": 0.01634
            },
            "individual_dummy": {
                "car_users": (3.6090816689609784, 3.6090816689609784)
            },
            "constant": (-7.157609305607602, -6.569095305607602),
            "log": {
                "logsum": 0.845599347812
            },
            "attraction": {

            },
            "impedance": {

            }
        },
        "transit": {
            "constant": (3.8327935897334235, 3.5491645897334236),
            "log": {
                "logsum": 0.845599347812
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
            "constant": (3.1813994873480613, 3.9260454873480612),
            "log": {
                "logsum": 0.845599347812
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
            "constant": (4.800296081933036, 5.126098081933036),
            "log": {
                "logsum": 0.845599347812
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
                "car_density": (2.3449742167608645, 2.3449742167608645),
                "cbd": 0.314974,
                "helsinki_other": 0.139569,
                "espoo_vant_kau": -0.03956
            },
            "log": {
                "logsum": 0.326683960214
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
            "constant": (2.2368033146541735, 2.1621853146541734),
            "log": {
                "logsum": 0.326683960214
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
            "constant": (1.4822776210309465, 1.7729766210309466),
            "log": {
                "logsum": 0.326683960214
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
            "constant": (2.6115557978687023, 2.2270907978687022),
            "log": {
                "logsum": 0.326683960214
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
                "car_density": (5.24406266057, 5.24406266057),
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
            "constant": (3.44996052654, 3.1709265265399997),
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
            "constant": (1.45658742061, 1.98828542061),
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
            "constant": (3.67789978445, 2.1768917844500004),
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
                "car_density": (5.916765673297294, 5.916765673297294),
                "cbd": -0.52381,
                "helsinki_other": 0.126528,
                "espoo_vant_kau": 0.030168
            },
            "individual_dummy": {
                "car_users": (1.906808496794927, 1.906808496794927)
            },
            "log": {
                "logsum": 0.572582948265
            },
            "constant": (0.0, -0.141276),
            "attraction": {

            },
            "impedance": {

            }
        },
        "transit": {
            "constant": (3.694384648559692, 2.551181648559692),
            "log": {
                "logsum": 0.572582948265
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
            "constant": (2.1460007302056847, 2.3962637302056846),
            "log": {
                "logsum": 0.572582948265
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
            "constant": (4.5086994955464865, 4.054052495546486),
            "log": {
                "logsum": 0.572582948265
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
                "car_density": (3.661184203155298, 3.661184203155298),
                "cbd": -0.155577,
                "helsinki_other": -0.03931,
                "espoo_vant_kau": -0.087526
            },
            "individual_dummy": {
                "car_users": (1.15887653311202, 1.15887653311202)
            },
            "log": {
                "logsum": 0.38212862884
            },
            "constant": (0.0, -0.029363),
            "attraction": {

            },
            "impedance": {

            }
        },
        "transit": {
            "constant": (1.6440119247766711, 0.8777459247766711),
            "log": {
                "logsum": 0.38212862884
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
            "constant": (0.8477288973572704, 1.2509998973572705),
            "log": {
                "logsum": 0.38212862884
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
            "constant": (2.6581585079469625, 2.7246295079469625),
            "log": {
                "logsum": 0.38212862884
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
                "car_density": (4.429863965743461, 4.429863965743461),
                "cbd": -0.285316,
                "helsinki_other": -0.956804,
                "espoo_vant_kau": 0.329168
            },
            "log": {
                "logsum": 1.12642919422
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
            "constant": (2.319574742677783, 2.207921742677783),
            "log": {
                "logsum": 1.12642919422
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
            "constant": (0.12501650571514702, 1.3226585057151472),
            "log": {
                "logsum": 1.12642919422
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
            "constant": (4.363510999568777, 4.001895999568777),
            "log": {
                "logsum": 1.12642919422
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
                "car_density": (4.429863965743461, 4.429863965743461),
                "cbd": -0.446814,
                "helsinki_other": -0.867228,
                "espoo_vant_kau": -0.913714
            },
            "log": {
                "logsum": 1.12642919422
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
            "constant": (2.319574742677783, 3.083402742677783),
            "log": {
                "logsum": 1.12642919422
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
            "constant": (0.12501650571514702, 1.388113505715147),
            "log": {
                "logsum": 1.12642919422
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
            "constant": (4.363510999568777, 4.044288999568777),
            "log": {
                "logsum": 1.12642919422
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