
### MODE CHOICE PARAMETERS ###

# Mode choice (generated 2.9.2024)
from typing import Any, Dict, Optional

mode_choice = {
    "hw": {
        "car": {
            "generation": {
                "car_density": (1.2250392848606655, 1.2250392848606655)
            },
            "individual_dummy": {
                "car_users": (4.00815837105, 4.00815837105)
            },
            "log": {
                "logsum": 0.9019259612739999
            }
        },
        "transit": {
            "constant": (4.069975274649584, 4.069975274649584),
            "log": {
                "logsum": 0.9019259612739999
            }
        },
        "bike": {
            "constant": (2.912968477866267, 2.912968477866267),
            "log": {
                "logsum": 0.9019259612739999
            }
        },
        "walk": {
            "constant": (4.782333281438626, 4.782333281438626),
            "log": {
                "logsum": 0.9019259612739999
            }
        }
    },
    "hc": {
        "car": {
            "generation": {
                "car_density": (4.324072248442647, 4.324072248442647)
            },
            "log": {
                "logsum": 0.253613771543
            }
        },
        "transit": {
            "constant": (2.830426833903452, 2.830426833903452),
            "log": {
                "logsum": 0.253613771543
            }
        },
        "bike": {
            "constant": (2.4845082618272936, 2.4845082618272936),
            "log": {
                "logsum": 0.253613771543
            }
        },
        "walk": {
            "constant": (3.162473568883928, 3.162473568883928),
            "log": {
                "logsum": 0.253613771543
            }
        }
    },
    "hu": {
        "car": {
            "generation": {
                "car_density": (4.28140287755, 4.28140287755)
            },
            "log": {
                "logsum": 1.0
            }
        },
        "transit": {
            "constant": (4.197980940369999, 4.197980940369999),
            "log": {
                "logsum": 1.0
            }
        },
        "bike": {
            "constant": (2.7288299967299996, 2.7288299967299996),
            "log": {
                "logsum": 1.0
            }
        },
        "walk": {
            "constant": (4.20886869795, 4.20886869795),
            "log": {
                "logsum": 1.0
            }
        }
    },
    "hs": {
        "car": {
            "generation": {
                "car_density": (6.063347609656314, 6.063347609656314)
            },
            "individual_dummy": {
                "car_users": (3.31407023257, 3.31407023257)
            },
            "log": {
                "logsum": 0.557198870792
            }
        },
        "transit": {
            "constant": (3.9577080672768545, 3.9577080672768545),
            "log": {
                "logsum": 0.557198870792
            }
        },
        "bike": {
            "constant": (2.3017199560405333, 2.3017199560405333),
            "log": {
                "logsum": 0.557198870792
            }
        },
        "walk": {
            "constant": (4.659707430419396, 4.659707430419396),
            "log": {
                "logsum": 0.557198870792
            }
        }
    },
    "ho": {
        "car": {
            "individual_dummy": {
                "car_users": (19.8846209005, 19.8846209005)
            },
            "log": {
                "logsum": 0.0331041833915
            }
        },
        "transit": {
            "constant": (1.3034795000580932, 1.3034795000580932),
            "log": {
                "logsum": 0.0331041833915
            }
        },
        "bike": {
            "constant": (0.8629432015400033, 0.8629432015400033),
            "log": {
                "logsum": 0.0331041833915
            }
        },
        "walk": {
            "constant": (3.054667882518675, 3.054667882518675),
            "log": {
                "logsum": 0.0331041833915
            }
        }
    },
    "hoo": None,
    "wo": {
        "car": {
            "constant": (0.37344004706008, 0.798587177559248),
            "generation": {
                "car_density": (2.019845153892125, 2.203129466617543)
            },
            "attraction": {

            },
            "impedance": {

            },
            "log": {
                "logsum": 0.718153936654
            },
            "individual_dummy": {

            }
        },
        "transit": {
            "constant": (0.9419571012680608, -1.5478825971113572),
            "generation": {
                "cbd": 0.9,
                "helsinki_other": -0.1,
                "espoo_vant_kau": -0.9
            },
            "attraction": {

            },
            "impedance": {

            },
            "log": {
                "logsum": 0.718153936654
            },
            "individual_dummy": {

            }
        },
        "bike": {
            "constant": (0.901232650926649, -0.15565490246074853),
            "generation": {

            },
            "attraction": {

            },
            "impedance": {

            },
            "log": {
                "logsum": 0.718153936654
            },
            "individual_dummy": {

            }
        },
        "walk": {
            "constant": (4.485001448888134, 3.845844445266074),
            "generation": {

            },
            "attraction": {

            },
            "impedance": {

            },
            "log": {
                "logsum": 0.718153936654
            },
            "individual_dummy": {

            }
        }
    },
    "oo": {
        "car": {
            "generation": {
                "car_density": (3.4865157659707626, 3.4865157659707626)
            },
            "log": {
                "logsum": 0.560117105619
            }
        },
        "transit": {
            "constant": (2.134266766251907, 2.134266766251907),
            "log": {
                "logsum": 0.560117105619
            }
        },
        "bike": {
            "constant": (-0.28735110033777433, -0.28735110033777433),
            "log": {
                "logsum": 0.560117105619
            }
        },
        "walk": {
            "constant": (4.023706009091386, 4.023706009091386),
            "log": {
                "logsum": 0.560117105619
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