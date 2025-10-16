
### MODE CHOICE PARAMETERS ###

# Mode choice (generated 2.9.2024)
from typing import Any, Dict, Optional
from parameters.assignment import inflation

mode_choice = {
    "hw": {
        "car": {
            "generation": {
                "car_density": (1.7982204256248782, 1.7982204256248782),
                "cbd": -0.5686410095478218,
                "helsinki_other": -0.13562834728133313,
                "espoo_vant_kau": -0.027600855630398227
            },
            "individual_dummy": {
                "car_users": (3.6090816689609784, 3.6090816689609784)
            },
            "log": {
                "logsum": 0.845599347812
            },
            "constant": (0.0, 0.16722762461943327),
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
            "constant": (3.8327935897334235, 3.585180484302631),
            "log": {
                "logsum": 0.845599347812
            },
            "generation": {
                "cbd": 0.10117819121345614,
                "helsinki_other": 0.48575529407353774,
                "espoo_vant_kau": 0.05714665820622189
            },
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "bike": {
            "constant": (3.1813994873480613, 4.035304380321256),
            "log": {
                "logsum": 0.845599347812
            },
            "generation": {
                "cbd": -0.20956496106611253,
                "helsinki_other": 0.3621616833962815,
                "espoo_vant_kau": 0.03617047904915257
            },
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "walk": {
            "constant": (4.800296081933036, 5.229553351275655),
            "log": {
                "logsum": 0.845599347812
            },
            "generation": {
                "cbd": 0.009559036798823438,
                "helsinki_other": -0.004462767064854267,
                "espoo_vant_kau": 0.33614807730599455
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
                "cbd": 0.12801557528557905,
                "helsinki_other": 0.11776295183234971,
                "espoo_vant_kau": -0.02947416298900807
            },
            "log": {
                "logsum": 0.326683960214
            },
            "constant": (0.0, 0.09840244930633735),
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "transit": {
            "constant": (2.2368033146541735, 2.140392092121819),
            "log": {
                "logsum": 0.326683960214
            },
            "generation": {
                "cbd": -0.5862989440222353,
                "helsinki_other": -0.04854777597795913,
                "espoo_vant_kau": 0.16233504059410153
            },
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "bike": {
            "constant": (1.4822776210309465, 1.7489534249395235),
            "log": {
                "logsum": 0.326683960214
            },
            "generation": {
                "cbd": -1.96304268572077,
                "helsinki_other": -0.2985773310933363,
                "espoo_vant_kau": 0.23198945072301913
            },
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "walk": {
            "constant": (2.6115557978687023, 2.181182687912487),
            "log": {
                "logsum": 0.326683960214
            },
            "generation": {
                "cbd": -0.0022483036518538,
                "helsinki_other": 0.16139213305674616,
                "espoo_vant_kau": -0.11588973384503816
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
                "cbd": 1.179801550431891,
                "helsinki_other": -0.7144842528657014,
                "espoo_vant_kau": 0.9517080163700662
            },
            "log": {
                "logsum": 1.0
            },
            "constant": (0.0, -0.4581172524543915),
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "transit": {
            "constant": (3.44996052654, 3.1148554815858853),
            "log": {
                "logsum": 1.0
            },
            "generation": {
                "cbd": -0.0270391087211973,
                "helsinki_other": 0.669104265624288,
                "espoo_vant_kau": 0.4790913510142052
            },
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "bike": {
            "constant": (1.45658742061, 2.0418331724078773),
            "log": {
                "logsum": 1.0
            },
            "generation": {
                "cbd": -1.2928816311554585,
                "helsinki_other": -0.07395648697802717,
                "espoo_vant_kau": 1.2471975313217076
            },
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "walk": {
            "constant": (3.67789978445, 2.1489278398778136),
            "log": {
                "logsum": 1.0
            },
            "generation": {
                "cbd": 0.36246902879324744,
                "helsinki_other": 0.0,
                "espoo_vant_kau": 1.054711523697197
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
                "cbd": -0.7033016774812533,
                "helsinki_other": 0.16497199419230862,
                "espoo_vant_kau": 0.09228577895322013
            },
            "individual_dummy": {
                "car_users": (1.906808496794927, 1.906808496794927)
            },
            "log": {
                "logsum": 0.572582948265
            },
            "constant": (0.0, -0.08607658306774423),
            "attraction": {

            },
            "impedance": {

            }
        },
        "transit": {
            "constant": (3.694384648559692, 2.4814797610012693),
            "log": {
                "logsum": 0.572582948265
            },
            "generation": {
                "cbd": -0.23264604276862727,
                "helsinki_other": -0.19444164454917567,
                "espoo_vant_kau": -0.22939720689245827
            },
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "bike": {
            "constant": (2.1460007302056847, 2.3084975497571754),
            "log": {
                "logsum": 0.572582948265
            },
            "generation": {
                "cbd": -0.7247764004726589,
                "helsinki_other": -0.2502846455744382,
                "espoo_vant_kau": -0.31224979125273006
            },
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "walk": {
            "constant": (4.5086994955464865, 3.9599136922629325),
            "log": {
                "logsum": 0.572582948265
            },
            "generation": {
                "cbd": -0.20451323869187565,
                "helsinki_other": -0.42186748539439295,
                "espoo_vant_kau": -0.0072378699556842445
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
                "cbd": -0.2171617684361389,
                "helsinki_other": -0.05957905774084832,
                "espoo_vant_kau": -0.16114147486134292
            },
            "individual_dummy": {
                "car_users": (1.15887653311202, 1.15887653311202)
            },
            "log": {
                "logsum": 0.38212862884
            },
            "constant": (0.0, -0.06952543833898858),
            "attraction": {

            },
            "impedance": {

            }
        },
        "transit": {
            "constant": (1.6440119247766711, 0.8190847596610806),
            "log": {
                "logsum": 0.38212862884
            },
            "generation": {
                "cbd": 0.24901196120405947,
                "helsinki_other": -0.19378697689230706,
                "espoo_vant_kau": -0.668574602251678
            },
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "bike": {
            "constant": (0.8477288973572704, 1.2087659262946184),
            "log": {
                "logsum": 0.38212862884
            },
            "generation": {
                "cbd": -0.7088159719245121,
                "helsinki_other": -0.0228604526370652,
                "espoo_vant_kau": -0.2812974398562073
            },
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "walk": {
            "constant": (2.6581585079469625, 2.6817414789035325),
            "log": {
                "logsum": 0.38212862884
            },
            "generation": {
                "cbd": 0.042472567199793955,
                "helsinki_other": -0.05784663170384664,
                "espoo_vant_kau": -0.4112300670670975
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
                "cbd": -0.3331929550248979,
                "helsinki_other": -1.3285762465716218,
                "espoo_vant_kau": 0.35772979434636476
            },
            "log": {
                "logsum": 1.12642919422
            },
            "constant": (0.0, 0.5073067068078587),
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "transit": {
            "constant": (2.319574742677783, 2.3035446563571003),
            "log": {
                "logsum": 1.12642919422
            },
            "generation": {
                "cbd": -0.15140102016139284,
                "helsinki_other": -1.5254717198878969,
                "espoo_vant_kau": -1.9849822154231642
            },
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "bike": {
            "constant": (0.12501650571514702, 1.3813107604211723),
            "log": {
                "logsum": 1.12642919422
            },
            "generation": {
                "cbd": 0.37107914470661785,
                "helsinki_other": 0.0,
                "espoo_vant_kau": -0.37698023313727813
            },
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "walk": {
            "constant": (4.363510999568777, 4.0295270276367665),
            "log": {
                "logsum": 1.12642919422
            },
            "generation": {
                "cbd": 0.5494534127733218,
                "helsinki_other": 0.07457612227914201,
                "espoo_vant_kau": 0.435706441435163
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
                "cbd": -0.4073098665720221,
                "helsinki_other": -1.1782226660488404,
                "espoo_vant_kau": -1.2984829583191413
            },
            "log": {
                "logsum": 1.12642919422
            },
            "constant": (0.0, -0.6828879798118497),
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "transit": {
            "constant": (2.319574742677783, 3.0665764865071585),
            "log": {
                "logsum": 1.12642919422
            },
            "generation": {
                "cbd": -0.04490953535738523,
                "helsinki_other": -0.12296364850850267,
                "espoo_vant_kau": -0.8491938563558319
            },
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "bike": {
            "constant": (0.12501650571514702, 1.3562938708842542),
            "log": {
                "logsum": 1.12642919422
            },
            "generation": {
                "cbd": 0.007523773054635308,
                "helsinki_other": 0.18600497683878914,
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
            "constant": (4.363510999568777, 4.002199635282803),
            "log": {
                "logsum": 1.12642919422
            },
            "generation": {
                "cbd": 1.1007739295187826,
                "helsinki_other": -0.6336960072481885,
                "espoo_vant_kau": -0.638199330273551
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