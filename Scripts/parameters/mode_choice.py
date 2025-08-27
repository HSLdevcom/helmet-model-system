
### MODE CHOICE PARAMETERS ###

# Mode choice (generated 2.9.2024)
from typing import Any, Dict, Optional

mode_choice = {
    "hw": {
        "car": {
            "generation": {
                "car_density": (1.8419087570969388, 1.8419087570969388),
                "cbd": -0.26320561673478776,
                "helsinki_other": -0.04745725770292141,
                "espoo_vant_kau": 0.050162952531424915
            },
            "individual_dummy": {
                "car_users": (3.6074856629935415, 3.6074856629935415)
            },
            "log": {
                "logsum": 0.846204700122
            },
            "constant": (0.0, 0.10106567342119509),
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
            "constant": (3.892045181119219, 3.5592707633871354),
            "log": {
                "logsum": 0.846204700122
            },
            "generation": {
                "cbd": 0.15582607064111087,
                "helsinki_other": 0.3327922786966788,
                "espoo_vant_kau": -0.02525975941771583
            },
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "bike": {
            "constant": (3.23168391795719, 3.7864762987609204),
            "log": {
                "logsum": 0.846204700122
            },
            "generation": {
                "cbd": -0.15546944549032612,
                "helsinki_other": 0.16813547984678887,
                "espoo_vant_kau": -0.09052896024381099
            },
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "walk": {
            "constant": (4.853946664677479, 5.111030619114686),
            "log": {
                "logsum": 0.846204700122
            },
            "generation": {
                "cbd": -0.0009261321509836801,
                "helsinki_other": -0.2440783214390405,
                "espoo_vant_kau": 0.1769539154617672
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
                "cbd": -0.07056909078533113,
                "helsinki_other": 0.06269082935045456,
                "espoo_vant_kau": 0.045853799430141035
            },
            "log": {
                "logsum": 0.326434720015
            },
            "constant": (0.0, -0.015230635464518204),
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "transit": {
            "constant": (2.2144687352693846, 2.1465349743326816),
            "log": {
                "logsum": 0.326434720015
            },
            "generation": {
                "cbd": -0.30896095068378987,
                "helsinki_other": 0.00997278509879072,
                "espoo_vant_kau": 0.08592154313387977
            },
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "bike": {
            "constant": (1.4728449856263395, 1.4186258253019228),
            "log": {
                "logsum": 0.326434720015
            },
            "generation": {
                "cbd": -0.7842872023439889,
                "helsinki_other": -0.12483315807950507,
                "espoo_vant_kau": 0.05995672051984568
            },
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "walk": {
            "constant": (2.602936355173292, 2.4434535942775697),
            "log": {
                "logsum": 0.326434720015
            },
            "generation": {
                "cbd": -0.1631696155935103,
                "helsinki_other": 0.03871701411758038,
                "espoo_vant_kau": -0.014629120443797074
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
                "cbd": 1.200282209470566,
                "helsinki_other": -1.0465162731240532,
                "espoo_vant_kau": 0.432677139893524
            },
            "log": {
                "logsum": 1.0
            },
            "constant": (0.0, -0.5750148939567843),
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "transit": {
            "constant": (3.55714351879, 3.0140379160935766),
            "log": {
                "logsum": 1.0
            },
            "generation": {
                "cbd": 0.07892087233145925,
                "helsinki_other": 0.3059533314879548,
                "espoo_vant_kau": 0.01929967823967832
            },
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "bike": {
            "constant": (1.54113758194, 1.8848724338549627),
            "log": {
                "logsum": 1.0
            },
            "generation": {
                "cbd": -1.2759177057671862,
                "helsinki_other": -0.48731938164215544,
                "espoo_vant_kau": 0.7182781356288768
            },
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "walk": {
            "constant": (3.76522269705, 2.0205581940507424),
            "log": {
                "logsum": 1.0
            },
            "generation": {
                "cbd": 0.3127039745252025,
                "helsinki_other": 0.0,
                "espoo_vant_kau": 0.5375755769457953
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
                "cbd": -0.3400377096450501,
                "helsinki_other": -0.061477977058528754,
                "espoo_vant_kau": -0.06196299809077822
            },
            "individual_dummy": {
                "car_users": (1.9063974550470684, 1.9063974550470684)
            },
            "log": {
                "logsum": 0.569238059006
            },
            "constant": (0.0, -0.35211282778518826),
            "attraction": {

            },
            "impedance": {

            }
        },
        "transit": {
            "constant": (3.869043873357799, 3.1490907619619883),
            "log": {
                "logsum": 0.569238059006
            },
            "generation": {
                "cbd": -0.0924345212197619,
                "helsinki_other": -0.1660927134765427,
                "espoo_vant_kau": -0.16871050611437502
            },
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "bike": {
            "constant": (2.2137488882854215, 2.6015243166678172),
            "log": {
                "logsum": 0.569238059006
            },
            "generation": {
                "cbd": -0.6004889326916365,
                "helsinki_other": -0.21168333952460838,
                "espoo_vant_kau": -0.4039563807381894
            },
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "walk": {
            "constant": (4.573762280685642, 4.184452862840539),
            "log": {
                "logsum": 0.569238059006
            },
            "generation": {
                "cbd": -0.0789701776887815,
                "helsinki_other": -0.3002819294648774,
                "espoo_vant_kau": -0.10709528587233898
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
                "cbd": 0.028756005133763612,
                "helsinki_other": -0.07844423048080472,
                "espoo_vant_kau": -0.18552149815830346
            },
            "individual_dummy": {
                "car_users": (1.1590086461971614, 1.1590086461971614)
            },
            "log": {
                "logsum": 0.381035783421
            },
            "constant": (0.0, -0.08804588215565742),
            "attraction": {

            },
            "impedance": {

            }
        },
        "transit": {
            "constant": (1.6960027379888027, 1.3631422926311711),
            "log": {
                "logsum": 0.381035783421
            },
            "generation": {
                "cbd": 0.14999031588087897,
                "helsinki_other": -0.19414915903432334,
                "espoo_vant_kau": -0.4225431589733957
            },
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "bike": {
            "constant": (0.8783664029630293, 0.8302870794101158),
            "log": {
                "logsum": 0.381035783421
            },
            "generation": {
                "cbd": -0.2898766586116877,
                "helsinki_other": -0.10627666726786003,
                "espoo_vant_kau": -0.3315958540488434
            },
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "walk": {
            "constant": (2.6849897070455824, 2.585221318830477),
            "log": {
                "logsum": 0.381035783421
            },
            "generation": {
                "cbd": 0.045682817587493076,
                "helsinki_other": -0.0839811420917966,
                "espoo_vant_kau": -0.34170764759204797
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
                "cbd": -0.015050043207786357,
                "helsinki_other": -0.9772936739938707,
                "espoo_vant_kau": 0.12928101227247307
            },
            "log": {
                "logsum": 1.12287350756
            },
            "constant": (0.0, 0.47903098292200397),
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "transit": {
            "constant": (2.6096070775164617, 1.8756245168746672),
            "log": {
                "logsum": 1.12287350756
            },
            "generation": {
                "cbd": -0.6782330355425633,
                "helsinki_other": -1.1405021266666038,
                "espoo_vant_kau": -1.0860849092965534
            },
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "bike": {
            "constant": (0.265257280721202, 1.3725701277184617),
            "log": {
                "logsum": 1.12287350756
            },
            "generation": {
                "cbd": 0.5767646214927595,
                "helsinki_other": 0.0,
                "espoo_vant_kau": -0.15245716465951342
            },
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "walk": {
            "constant": (4.5059026784451826, 4.246410697612761),
            "log": {
                "logsum": 1.12287350756
            },
            "generation": {
                "cbd": 0.6319703575788835,
                "helsinki_other": 0.23454647236178794,
                "espoo_vant_kau": 0.32091728179454876
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
                "cbd": -0.3789258066353438,
                "helsinki_other": -0.8445177997266899,
                "espoo_vant_kau": -0.919354871115452
            },
            "log": {
                "logsum": 1.12287350756
            },
            "constant": (0.0, -0.5492337258451867),
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "transit": {
            "constant": (2.6096070775164617, 3.344975976129036),
            "log": {
                "logsum": 1.12287350756
            },
            "generation": {
                "cbd": 0.12024515416584311,
                "helsinki_other": 0.1754041703399072,
                "espoo_vant_kau": -0.7857151305380119
            },
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "bike": {
            "constant": (0.265257280721202, 1.54374406365835),
            "log": {
                "logsum": 1.12287350756
            },
            "generation": {
                "cbd": -0.19055594384451682,
                "helsinki_other": 0.3262428606216861,
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
            "constant": (4.5059026784451826, 4.090666193076407),
            "log": {
                "logsum": 1.12287350756
            },
            "generation": {
                "cbd": 0.8820934834602043,
                "helsinki_other": -0.49388414942916636,
                "espoo_vant_kau": -0.45981333880529707
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