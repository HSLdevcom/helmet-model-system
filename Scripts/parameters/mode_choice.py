
### MODE CHOICE PARAMETERS ###

# Mode choice (generated 2.9.2024)
from typing import Any, Dict, Optional

mode_choice = {
    "hw": {
        "car": {
            "generation": {
                "car_density": (1.7992112165554988, 1.7992112165554988),
                "cbd": -0.04454410757544899,
                "helsinki_other": 0.03458656632315518,
                "espoo_vant_kau": 0.0345777102064256
            },
            "individual_dummy": {
                "car_users": (3.646422477940345, 3.646422477940345)
            },
            "log": {
                "logsum": 0.850744694097
            },
            "constant": (0.0, 0.06366055117775461),
            "attraction": {

            },
            "impedance": {

            }
        },
        "park_and_ride": {
            "generation": {
                "car_density": (1.7992112165554988, 1.7992112165554988)
            },
            "individual_dummy": {
                "car_users": (3.646422477940345, 3.646422477940345)
            },
            "constant": (-6.658342532339443, -6.658342532339443),
            "log": {
                "logsum": 0.850744694097
            },
            "attraction": {

            },
            "impedance": {

            }
        },
        "transit": {
            "constant": (4.077884776393074, 3.9841362811408154),
            "log": {
                "logsum": 0.850744694097
            },
            "generation": {
                "cbd": 0.03244564817469291,
                "helsinki_other": 0.11604608160739305,
                "espoo_vant_kau": -0.006677852844813573
            },
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "bike": {
            "constant": (3.4294816968772457, 3.51573182138118),
            "log": {
                "logsum": 0.850744694097
            },
            "generation": {
                "cbd": 0.006026626030937461,
                "helsinki_other": 0.11152667845900331,
                "espoo_vant_kau": 0.00855945853872198
            },
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "walk": {
            "constant": (5.031385411986816, 5.06250153709196),
            "log": {
                "logsum": 0.850744694097
            },
            "generation": {
                "cbd": 0.023175913100579714,
                "helsinki_other": 0.06857880016124022,
                "espoo_vant_kau": 0.037207333369446
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
                "car_density": (2.3728285844709576, 2.3728285844709576),
                "cbd": 0.18769523022037893,
                "helsinki_other": 0.0813485416577571,
                "espoo_vant_kau": -0.060442504733245465
            },
            "log": {
                "logsum": 0.310646022511
            },
            "constant": (0.0, 0.05874100309679332),
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "transit": {
            "constant": (2.171001689025219, 2.085095341864884),
            "log": {
                "logsum": 0.310646022511
            },
            "generation": {
                "cbd": -0.25251894169474065,
                "helsinki_other": -0.025206135928608975,
                "espoo_vant_kau": 0.08810199699599759
            },
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "bike": {
            "constant": (1.5237298257762777, 1.7653157325116147),
            "log": {
                "logsum": 0.310646022511
            },
            "generation": {
                "cbd": -1.2073242092042773,
                "helsinki_other": -0.18971799246151738,
                "espoo_vant_kau": 0.14022282973056413
            },
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "walk": {
            "constant": (2.5646124292051713, 2.260786698841411),
            "log": {
                "logsum": 0.310646022511
            },
            "generation": {
                "cbd": 0.12073923077103883,
                "helsinki_other": 0.10917103461964324,
                "espoo_vant_kau": -0.08024182014541359
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
                "car_density": (5.29371519179, 5.29371519179),
                "cbd": -0.05533947115943365,
                "helsinki_other": -0.031589622768788836,
                "espoo_vant_kau": 0.01763118955463202
            },
            "log": {
                "logsum": 1.0
            },
            "constant": (0.0, -0.2871914835310068),
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "transit": {
            "constant": (3.48333340168, 3.182006217471166),
            "log": {
                "logsum": 1.0
            },
            "generation": {
                "cbd": -0.06378245211660843,
                "helsinki_other": -0.006139326236215666,
                "espoo_vant_kau": 0.013336353387832713
            },
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "bike": {
            "constant": (1.39665637305, 1.1622329300422112),
            "log": {
                "logsum": 1.0
            },
            "generation": {
                "cbd": -0.06577266566394603,
                "helsinki_other": -0.012673671504844195,
                "espoo_vant_kau": 0.05753671894698601
            },
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "walk": {
            "constant": (3.75171051766, 3.446465632977471),
            "log": {
                "logsum": 1.0
            },
            "generation": {
                "cbd": -0.05255750452024605,
                "helsinki_other": 0.0,
                "espoo_vant_kau": 0.12066353142425455
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
                "car_density": (6.071025790431748, 6.071025790431748),
                "cbd": -0.267474872290824,
                "helsinki_other": 0.0897520406372589,
                "espoo_vant_kau": 0.0013444718888129873
            },
            "individual_dummy": {
                "car_users": (1.8985961615452254, 1.8985961615452254)
            },
            "log": {
                "logsum": 0.535232484914
            },
            "constant": (0.0, -0.015451727996982769),
            "attraction": {

            },
            "impedance": {

            }
        },
        "transit": {
            "constant": (3.7568562043102767, 3.176545680104901),
            "log": {
                "logsum": 0.535232484914
            },
            "generation": {
                "cbd": -0.0034258204670286605,
                "helsinki_other": -0.08284298419661819,
                "espoo_vant_kau": -0.07429718558564367
            },
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "bike": {
            "constant": (2.2296137223426755, 2.3768913041780024),
            "log": {
                "logsum": 0.535232484914
            },
            "generation": {
                "cbd": -0.22828500003078964,
                "helsinki_other": -0.08057576657827321,
                "espoo_vant_kau": -0.12119204259594506
            },
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "walk": {
            "constant": (4.531834735523872, 4.275181650566849),
            "log": {
                "logsum": 0.535232484914
            },
            "generation": {
                "cbd": 0.010735994248247244,
                "helsinki_other": -0.1944208444605111,
                "espoo_vant_kau": -0.00014779654595051036
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
                "car_density": (3.6068417317245296, 3.6068417317245296),
                "cbd": -0.12349651064743825,
                "helsinki_other": -0.021378042921271097,
                "espoo_vant_kau": -0.04236375530984155
            },
            "individual_dummy": {
                "car_users": (1.1572269881276056, 1.1572269881276056)
            },
            "log": {
                "logsum": 0.428894328079
            },
            "constant": (0.0, -0.030403537589119737),
            "attraction": {

            },
            "impedance": {

            }
        },
        "transit": {
            "constant": (1.759406400807731, 1.2374853232112442),
            "log": {
                "logsum": 0.428894328079
            },
            "generation": {
                "cbd": 0.24114512102420965,
                "helsinki_other": -0.03458080905974284,
                "espoo_vant_kau": -0.32328160290170166
            },
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "bike": {
            "constant": (0.896739856981925, 1.23122380485772),
            "log": {
                "logsum": 0.428894328079
            },
            "generation": {
                "cbd": -0.39971054682009927,
                "helsinki_other": 0.025236481108350917,
                "espoo_vant_kau": -0.05841306928486649
            },
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "walk": {
            "constant": (2.717657933957617, 2.768529028486526),
            "log": {
                "logsum": 0.428894328079
            },
            "generation": {
                "cbd": 0.10098150863979886,
                "helsinki_other": -0.05938360458085334,
                "espoo_vant_kau": -0.14551599748321467
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
                "car_density": (4.506185988148862, 4.506185988148862),
                "cbd": 0.006837057821316501,
                "helsinki_other": -0.14761777124902553,
                "espoo_vant_kau": 0.2699029463729783
            },
            "log": {
                "logsum": 1.09590339572
            },
            "constant": (0.0, 0.1111228412367851),
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "transit": {
            "constant": (2.5456093738755805, 3.2792242808334935),
            "log": {
                "logsum": 1.09590339572
            },
            "generation": {
                "cbd": 0.7501464992220017,
                "helsinki_other": -0.2809166350968592,
                "espoo_vant_kau": -0.9622203144475527
            },
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "bike": {
            "constant": (0.11729576479924024, 0.2749802351596042),
            "log": {
                "logsum": 1.09590339572
            },
            "generation": {
                "cbd": -0.041193658547419736,
                "helsinki_other": 0.0,
                "espoo_vant_kau": -0.3882806573014519
            },
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "walk": {
            "constant": (4.492152222396459, 4.408001617341879),
            "log": {
                "logsum": 1.09590339572
            },
            "generation": {
                "cbd": 0.051402303020288705,
                "helsinki_other": -0.13860556065248147,
                "espoo_vant_kau": -0.028911946624100588
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
                "car_density": (4.506185988148862, 4.506185988148862),
                "cbd": 0.3731695703025661,
                "helsinki_other": -0.2415495479622672,
                "espoo_vant_kau": -0.42311797624326053
            },
            "log": {
                "logsum": 1.09590339572
            },
            "constant": (0.0, -0.12467624406181614),
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "transit": {
            "constant": (2.5456093738755805, 2.4910438792060092),
            "log": {
                "logsum": 1.09590339572
            },
            "generation": {
                "cbd": 0.396686623034179,
                "helsinki_other": -0.24692874042286234,
                "espoo_vant_kau": -0.38700043456769795
            },
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "bike": {
            "constant": (0.11729576479924024, 0.01770206171712546),
            "log": {
                "logsum": 1.09590339572
            },
            "generation": {
                "cbd": 0.44253721497923565,
                "helsinki_other": -0.25442783129580043,
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
            "constant": (4.492152222396459, 4.466756624475024),
            "log": {
                "logsum": 1.09590339572
            },
            "generation": {
                "cbd": 0.4324805603905181,
                "helsinki_other": -0.21333947849314056,
                "espoo_vant_kau": -0.34873468089183873
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