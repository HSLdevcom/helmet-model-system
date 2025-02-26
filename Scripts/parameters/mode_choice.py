
### MODE CHOICE PARAMETERS ###

# Mode choice (generated 2.9.2024)
from typing import Any, Dict, Optional

mode_choice = {
    "hw": {
        "car": {
            "generation": {
                "car_density": (1.4230680934983488, 1.4230680934983488),
                "cbd": -0.19308168097281622,
                "helsinki_other": -0.07176067441819414,
                "espoo_vant_kau": 0.05985266409130238
            },
            "individual_dummy": {
                "car_users": (3.6557459229208353, 3.6557459229208353)
            },
            "log": {
                "logsum": 0.905954533268
            },
            "constant": (0.0, 0.09065193231904933),
            "attraction": {

            },
            "impedance": {

            }
        },
        "park_and_ride": {
            "generation": {
                "car_density": (1.4230680934983488, 1.4230680934983488)
            },
            "individual_dummy": {
                "car_users": (3.6557459229208353, 3.6557459229208353)
            },
            "constant": (-6.717136764977398, -6.717136764977398),
            "log": {
                "logsum": 0.905954533268
            },
            "attraction": {

            },
            "impedance": {

            }
        },
        "transit": {
            "constant": (4.0312639497553455, 3.5738355666012427),
            "log": {
                "logsum": 0.905954533268
            },
            "generation": {
                "cbd": 0.14410383865425938,
                "helsinki_other": 0.19809430807809542,
                "espoo_vant_kau": -0.0719787646613041
            },
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "bike": {
            "constant": (3.3805264233409855, 4.102419265393487),
            "log": {
                "logsum": 0.905954533268
            },
            "generation": {
                "cbd": -0.11536535617170107,
                "helsinki_other": 0.17430018197700148,
                "espoo_vant_kau": 0.004778508790505231
            },
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "walk": {
            "constant": (5.1201889112403585, 5.289042101189965),
            "log": {
                "logsum": 0.905954533268
            },
            "generation": {
                "cbd": 0.0343528406164293,
                "helsinki_other": -0.22502358269808992,
                "espoo_vant_kau": 0.2526579107014897
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
                "car_density": (2.306756600989689, 2.306756600989689),
                "cbd": 0.12499726890352293,
                "helsinki_other": 0.037967653939817166,
                "espoo_vant_kau": -0.031151281687749503
            },
            "log": {
                "logsum": 0.314055247569
            },
            "constant": (0.0, 0.03511862784403203),
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "transit": {
            "constant": (2.1452988663601404, 2.1159372665723444),
            "log": {
                "logsum": 0.314055247569
            },
            "generation": {
                "cbd": -0.07771419157801501,
                "helsinki_other": -0.011278592094695446,
                "espoo_vant_kau": 0.03736685111380318
            },
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "bike": {
            "constant": (1.4739650599529817, 1.593288327650331),
            "log": {
                "logsum": 0.314055247569
            },
            "generation": {
                "cbd": -0.514726343881985,
                "helsinki_other": -0.08641924268079437,
                "espoo_vant_kau": 0.06082032696704323
            },
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "walk": {
            "constant": (2.533988138135327, 2.4055926738691866),
            "log": {
                "logsum": 0.314055247569
            },
            "generation": {
                "cbd": 0.09210464857864308,
                "helsinki_other": 0.04980767164375952,
                "espoo_vant_kau": -0.03960028479082426
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
                "car_density": (4.72096933012, 4.72096933012),
                "cbd": 0.8536842362258463,
                "helsinki_other": -1.286813276971167,
                "espoo_vant_kau": 0.13357131231664005
            },
            "log": {
                "logsum": 1.0
            },
            "constant": (0.0, -0.3319235161649627),
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "transit": {
            "constant": (3.35026323444, 3.019295460683183),
            "log": {
                "logsum": 1.0
            },
            "generation": {
                "cbd": -0.10244822768032766,
                "helsinki_other": 0.13539904817617648,
                "espoo_vant_kau": -0.13524641338183632
            },
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "bike": {
            "constant": (1.36284433608, 2.3054016637574946),
            "log": {
                "logsum": 1.0
            },
            "generation": {
                "cbd": -1.3119882311950612,
                "helsinki_other": -0.49091932814071526,
                "espoo_vant_kau": 0.6873877782481544
            },
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "walk": {
            "constant": (3.66513701501, 2.170133873058522),
            "log": {
                "logsum": 1.0
            },
            "generation": {
                "cbd": 0.2462416269813527,
                "helsinki_other": 0.0,
                "espoo_vant_kau": 0.4323987863449281
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
                "car_density": (5.7091568661098675, 5.7091568661098675),
                "cbd": -0.22940849102140448,
                "helsinki_other": 0.10382233526566212,
                "espoo_vant_kau": 0.007160340104395777
            },
            "individual_dummy": {
                "car_users": (1.8782949210154856, 1.8782949210154856)
            },
            "log": {
                "logsum": 0.528506854951
            },
            "constant": (0.0, 0.021168891675513654),
            "attraction": {

            },
            "impedance": {

            }
        },
        "transit": {
            "constant": (3.420460544152823, 2.870195633133911),
            "log": {
                "logsum": 0.528506854951
            },
            "generation": {
                "cbd": 0.027115185386075803,
                "helsinki_other": -0.03957609646176889,
                "espoo_vant_kau": -0.0692778327092574
            },
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "bike": {
            "constant": (1.9839467875824828, 2.2445195799840794),
            "log": {
                "logsum": 0.528506854951
            },
            "generation": {
                "cbd": -0.22643764140610417,
                "helsinki_other": -0.03646942520305833,
                "espoo_vant_kau": -0.12237398457693693
            },
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "walk": {
            "constant": (4.275918726378757, 4.085800511455174),
            "log": {
                "logsum": 0.528506854951
            },
            "generation": {
                "cbd": 0.039285091966623144,
                "helsinki_other": -0.16175872666329752,
                "espoo_vant_kau": 0.01291129763548388
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
                "car_density": (3.776481043730373, 3.776481043730373),
                "cbd": -0.07464350853780057,
                "helsinki_other": -0.006191855766219894,
                "espoo_vant_kau": -0.002463190700597003
            },
            "individual_dummy": {
                "car_users": (1.160303767222481, 1.160303767222481)
            },
            "log": {
                "logsum": 0.376640331653
            },
            "constant": (0.0, -0.011649082184177982),
            "attraction": {

            },
            "impedance": {

            }
        },
        "transit": {
            "constant": (1.6832873308878444, 1.3765976658412402),
            "log": {
                "logsum": 0.376640331653
            },
            "generation": {
                "cbd": 0.13955871556013963,
                "helsinki_other": -0.01403758547528464,
                "espoo_vant_kau": -0.16634748195400076
            },
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "bike": {
            "constant": (0.7902164806081416, 0.9979524279901988),
            "log": {
                "logsum": 0.376640331653
            },
            "generation": {
                "cbd": -0.24774453878830102,
                "helsinki_other": 0.021969948083882227,
                "espoo_vant_kau": -0.006510088122157248
            },
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "walk": {
            "constant": (2.515488773357361, 2.5519510075572436),
            "log": {
                "logsum": 0.376640331653
            },
            "generation": {
                "cbd": 0.054453485383322224,
                "helsinki_other": -0.029138969680282963,
                "espoo_vant_kau": -0.05898402803248587
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
            "constant": (0.37344004706008, 0.959763526610097),
            "generation": {
                "car_density": (2.019845153892125, 2.203129466617543),
                "cbd": 0.12125042083153928,
                "helsinki_other": -0.13374391935653576,
                "espoo_vant_kau": 0.42303330671094325
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
            "constant": (0.9419571012680608, 0.22400959138875565),
            "generation": {
                "cbd": -0.29492089676187055,
                "helsinki_other": -0.22415361213131757,
                "espoo_vant_kau": -0.3460978011204781
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
            "constant": (0.901232650926649, 0.1851965085101428),
            "generation": {
                "cbd": -0.03669829259189516,
                "helsinki_other": 0.0,
                "espoo_vant_kau": -1.1539375035438024
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
            "constant": (4.485001448888134, 3.6187067748232598),
            "generation": {
                "cbd": 0.18107841752778273,
                "helsinki_other": -0.1176981039476024,
                "espoo_vant_kau": -0.20439469496580903
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
                "car_density": (5.270366986652963, 5.270366986652963),
                "cbd": -0.6812814852037595,
                "helsinki_other": -0.7706353612412983,
                "espoo_vant_kau": -0.7299926089105434
            },
            "log": {
                "logsum": 1.04450466839
            },
            "constant": (0.0, -0.48477595431623016),
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "transit": {
            "constant": (2.4786042346020425, 3.4975746044068354),
            "log": {
                "logsum": 1.04450466839
            },
            "generation": {
                "cbd": -0.14578685816731882,
                "helsinki_other": 0.3344253753971627,
                "espoo_vant_kau": -0.29274697917776893
            },
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "bike": {
            "constant": (0.3386840000145957, 2.222626640473643),
            "log": {
                "logsum": 1.04450466839
            },
            "generation": {
                "cbd": -0.2001437670288786,
                "helsinki_other": 0.5405861290401444,
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
            "constant": (4.64565630822768, 4.615761155488121),
            "log": {
                "logsum": 1.04450466839
            },
            "generation": {
                "cbd": 0.8416485384657438,
                "helsinki_other": -0.429467223007945,
                "espoo_vant_kau": -0.018621994398180533
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