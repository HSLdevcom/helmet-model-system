
### MODE CHOICE PARAMETERS ###

# Mode choice (generated 2.9.2024)
from typing import Any, Dict, Optional

mode_choice = {
    "hw": {
        "car": {
            "generation": {
                "car_density": (1.7898027723112746, 1.7898027723112746),
                "cbd": -0.4386459967421909,
                "helsinki_other": -0.13959766920168454,
                "espoo_vant_kau": -0.021439721010634266
            },
            "individual_dummy": {
                "car_users": (3.6091937349063166, 3.6091937349063166)
            },
            "log": {
                "logsum": 0.848444967824
            },
            "constant": (0.0, 0.09402604957965541),
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
            "constant": (3.8830650314912134, 3.599435834526354),
            "log": {
                "logsum": 0.848444967824
            },
            "generation": {
                "cbd": 0.15296709802997616,
                "helsinki_other": 0.3762622031220961,
                "espoo_vant_kau": 0.034405207415259806
            },
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "bike": {
            "constant": (3.2167179590315493, 3.96136363474956),
            "log": {
                "logsum": 0.848444967824
            },
            "generation": {
                "cbd": -0.15844768684649382,
                "helsinki_other": 0.26580689268647584,
                "espoo_vant_kau": 0.011075956560613512
            },
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "walk": {
            "constant": (4.844449835047745, 5.170252287125295),
            "log": {
                "logsum": 0.848444967824
            },
            "generation": {
                "cbd": 0.06007034153469227,
                "helsinki_other": -0.09836652729884046,
                "espoo_vant_kau": 0.3092923514318446
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
                "cbd": 0.31497376275167005,
                "helsinki_other": 0.1395690723965754,
                "espoo_vant_kau": -0.03956034657879054
            },
            "log": {
                "logsum": 0.326164428873
            },
            "constant": (0.0, 0.11317918833514666),
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "transit": {
            "constant": (2.23179604883763, 2.1571782905545973),
            "log": {
                "logsum": 0.326164428873
            },
            "generation": {
                "cbd": -0.4056300947123598,
                "helsinki_other": -0.031241520140850867,
                "espoo_vant_kau": 0.15581011907082043
            },
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "bike": {
            "constant": (1.4820957990801067, 1.772794601084558),
            "log": {
                "logsum": 0.326164428873
            },
            "generation": {
                "cbd": -1.7819904175324892,
                "helsinki_other": -0.27685271740647194,
                "espoo_vant_kau": 0.22594147487018337
            },
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "walk": {
            "constant": (2.6104495735108393, 2.2259842504704976),
            "log": {
                "logsum": 0.326164428873
            },
            "generation": {
                "cbd": 0.17354690494677164,
                "helsinki_other": 0.17826239463968738,
                "espoo_vant_kau": -0.11645544110442216
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
                "cbd": 1.1995489308170169,
                "helsinki_other": -0.8952053774452255,
                "espoo_vant_kau": 0.6581140025810681
            },
            "log": {
                "logsum": 1.0
            },
            "constant": (0.0, -0.41935540654059456),
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "transit": {
            "constant": (3.55407315155, 3.275039212114848),
            "log": {
                "logsum": 1.0
            },
            "generation": {
                "cbd": 0.005254656610773463,
                "helsinki_other": 0.44722395156769096,
                "espoo_vant_kau": 0.19983531341423522
            },
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "bike": {
            "constant": (1.51681381373, 2.0485115150028563),
            "log": {
                "logsum": 1.0
            },
            "generation": {
                "cbd": -1.2590463091492547,
                "helsinki_other": -0.27271762787139603,
                "espoo_vant_kau": 0.9382769386409968
            },
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "walk": {
            "constant": (3.73925008614, 2.238242488113706),
            "log": {
                "logsum": 1.0
            },
            "generation": {
                "cbd": 0.38565955345035613,
                "helsinki_other": 0.0,
                "espoo_vant_kau": 0.7186689952239105
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
                "cbd": -0.523810330597562,
                "helsinki_other": 0.12652773825211852,
                "espoo_vant_kau": 0.030168139893990878
            },
            "individual_dummy": {
                "car_users": (1.9069069532920093, 1.9069069532920093)
            },
            "log": {
                "logsum": 0.566271563066
            },
            "constant": (0.0, -0.14127587811583422),
            "attraction": {

            },
            "impedance": {

            }
        },
        "transit": {
            "constant": (3.846394306037391, 2.703191045607851),
            "log": {
                "logsum": 0.566271563066
            },
            "generation": {
                "cbd": -0.10007755770116088,
                "helsinki_other": -0.13430363594518174,
                "espoo_vant_kau": -0.24254795376217952
            },
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "bike": {
            "constant": (2.2139830946764185, 2.464245665188701),
            "log": {
                "logsum": 0.566271563066
            },
            "generation": {
                "cbd": -0.5918713758782193,
                "helsinki_other": -0.18725375689645685,
                "espoo_vant_kau": -0.3292275855437514
            },
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "walk": {
            "constant": (4.570099600398595, 4.115452327559344),
            "log": {
                "logsum": 0.566271563066
            },
            "generation": {
                "cbd": -0.07066028078932787,
                "helsinki_other": -0.35586921384799447,
                "espoo_vant_kau": -0.022238679305560276
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
                "cbd": -0.15557690916492897,
                "helsinki_other": -0.03931018932833578,
                "espoo_vant_kau": -0.08752562380024684
            },
            "individual_dummy": {
                "car_users": (1.1587085900464564, 1.1587085900464564)
            },
            "log": {
                "logsum": 0.379991080528
            },
            "constant": (0.0, -0.029362887561128904),
            "attraction": {

            },
            "impedance": {

            }
        },
        "transit": {
            "constant": (1.6907671490795977, 0.9245015400578723),
            "log": {
                "logsum": 0.379991080528
            },
            "generation": {
                "cbd": 0.29300189138793853,
                "helsinki_other": -0.1736834847738427,
                "espoo_vant_kau": -0.561473615846195
            },
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "bike": {
            "constant": (0.8759342178056636, 1.2792047856301973),
            "log": {
                "logsum": 0.379991080528
            },
            "generation": {
                "cbd": -0.6640210713377779,
                "helsinki_other": 0.0005479261583558465,
                "espoo_vant_kau": -0.17477620977032118
            },
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "walk": {
            "constant": (2.6828511778748703, 2.74932252580096),
            "log": {
                "logsum": 0.379991080528
            },
            "generation": {
                "cbd": 0.0885560773110958,
                "helsinki_other": -0.034588327045015854,
                "espoo_vant_kau": -0.30297267817046075
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
                "cbd": -0.285316026054737,
                "helsinki_other": -0.9568039074438299,
                "espoo_vant_kau": 0.329167896365602
            },
            "log": {
                "logsum": 1.11333581055
            },
            "constant": (0.0, 0.3982985356153526),
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "transit": {
            "constant": (2.580336404612475, 2.468683629314808),
            "log": {
                "logsum": 1.11333581055
            },
            "generation": {
                "cbd": -0.20291247566643217,
                "helsinki_other": -1.2818176323878343,
                "espoo_vant_kau": -1.9821582803666093
            },
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "bike": {
            "constant": (0.25675679866725687, 1.4543991960252027),
            "log": {
                "logsum": 1.11333581055
            },
            "generation": {
                "cbd": 0.29627761710549494,
                "helsinki_other": 0.0,
                "espoo_vant_kau": -0.41490783208972076
            },
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "walk": {
            "constant": (4.502206471590505, 4.140591735205532),
            "log": {
                "logsum": 1.11333581055
            },
            "generation": {
                "cbd": 0.4539380459122802,
                "helsinki_other": 0.2190151254854164,
                "espoo_vant_kau": 0.375855951368308
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
                "cbd": -0.44681424705730566,
                "helsinki_other": -0.8672278954828966,
                "espoo_vant_kau": -0.9137136532363077
            },
            "log": {
                "logsum": 1.11333581055
            },
            "constant": (0.0, -0.5173689952632802),
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "transit": {
            "constant": (2.580336404612475, 3.3441648412947083),
            "log": {
                "logsum": 1.11333581055
            },
            "generation": {
                "cbd": -0.1966199366568429,
                "helsinki_other": 0.07026712880761923,
                "espoo_vant_kau": -0.5716362251302245
            },
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "bike": {
            "constant": (0.25675679866725687, 1.5198541263663068),
            "log": {
                "logsum": 1.11333581055
            },
            "generation": {
                "cbd": -0.1950398886735504,
                "helsinki_other": 0.38312754852139935,
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
            "constant": (4.502206471590505, 4.182984589518133),
            "log": {
                "logsum": 1.11333581055
            },
            "generation": {
                "cbd": 0.8563147197444894,
                "helsinki_other": -0.44419988236651825,
                "espoo_vant_kau": -0.4034908102663649
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