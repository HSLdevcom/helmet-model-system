
### MODE CHOICE PARAMETERS ###

# Mode choice (generated 2.9.2024)
from typing import Any, Dict, Optional

mode_choice = {
    "hw": {
        "car": {
            "generation": {
                "car_density": (1.4230680934983488, 1.4230680934983488),
                "cbd": -0.23762578854826522,
                "helsinki_other": -0.03717410809503896,
                "espoo_vant_kau": 0.09443037429772799
            },
            "individual_dummy": {
                "car_users": (3.6557459229208353, 3.6557459229208353)
            },
            "log": {
                "logsum": 0.905954533268
            },
            "constant": (0.0, 0.15431248349680393),
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
            "constant": (4.0312639497553455, 3.4800870713489838),
            "log": {
                "logsum": 0.905954533268
            },
            "generation": {
                "cbd": 0.1765494868289523,
                "helsinki_other": 0.31414038968548846,
                "espoo_vant_kau": -0.07865661750611767
            },
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "bike": {
            "constant": (3.3805264233409855, 4.188669389897422),
            "log": {
                "logsum": 0.905954533268
            },
            "generation": {
                "cbd": -0.10933873014076362,
                "helsinki_other": 0.2858268604360048,
                "espoo_vant_kau": 0.01333796732922721
            },
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "walk": {
            "constant": (5.1201889112403585, 5.320158226295109),
            "log": {
                "logsum": 0.905954533268
            },
            "generation": {
                "cbd": 0.05752875371700901,
                "helsinki_other": -0.15644478253684968,
                "espoo_vant_kau": 0.28986524407093567
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
                "cbd": 0.31269249912390185,
                "helsinki_other": 0.11931619559757425,
                "espoo_vant_kau": -0.09159378642099497
            },
            "log": {
                "logsum": 0.314055247569
            },
            "constant": (0.0, 0.09385963094082536),
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "transit": {
            "constant": (2.1452988663601404, 2.030030919412009),
            "log": {
                "logsum": 0.314055247569
            },
            "generation": {
                "cbd": -0.33023313327275566,
                "helsinki_other": -0.03648472802330442,
                "espoo_vant_kau": 0.12546884810980077
            },
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "bike": {
            "constant": (1.4739650599529817, 1.8348742343856679),
            "log": {
                "logsum": 0.314055247569
            },
            "generation": {
                "cbd": -1.7220505530862624,
                "helsinki_other": -0.27613723514231175,
                "espoo_vant_kau": 0.20104315669760736
            },
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "walk": {
            "constant": (2.533988138135327, 2.1017669435054263),
            "log": {
                "logsum": 0.314055247569
            },
            "generation": {
                "cbd": 0.2128438793496819,
                "helsinki_other": 0.15897870626340277,
                "espoo_vant_kau": -0.11984210493623784
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
                "cbd": 0.7983447650664127,
                "helsinki_other": -1.318402899739956,
                "espoo_vant_kau": 0.15120250187127207
            },
            "log": {
                "logsum": 1.0
            },
            "constant": (0.0, -0.6191149996959695),
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "transit": {
            "constant": (3.35026323444, 2.717968276474349),
            "log": {
                "logsum": 1.0
            },
            "generation": {
                "cbd": -0.1662306797969361,
                "helsinki_other": 0.12925972193996083,
                "espoo_vant_kau": -0.12191005999400362
            },
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "bike": {
            "constant": (1.36284433608, 2.070978220749706),
            "log": {
                "logsum": 1.0
            },
            "generation": {
                "cbd": -1.3777608968590074,
                "helsinki_other": -0.5035929996455595,
                "espoo_vant_kau": 0.7449244971951404
            },
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "walk": {
            "constant": (3.66513701501, 1.8648889883759934),
            "log": {
                "logsum": 1.0
            },
            "generation": {
                "cbd": 0.19368412246110667,
                "helsinki_other": 0.0,
                "espoo_vant_kau": 0.5530623177691827
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
                "cbd": -0.4968833633122285,
                "helsinki_other": 0.19357437590292104,
                "espoo_vant_kau": 0.008504811993208765
            },
            "individual_dummy": {
                "car_users": (1.8782949210154856, 1.8782949210154856)
            },
            "log": {
                "logsum": 0.528506854951
            },
            "constant": (0.0, 0.005717163678530885),
            "attraction": {

            },
            "impedance": {

            }
        },
        "transit": {
            "constant": (3.420460544152823, 2.289885108928535),
            "log": {
                "logsum": 0.528506854951
            },
            "generation": {
                "cbd": 0.02368936491904714,
                "helsinki_other": -0.12241908065838708,
                "espoo_vant_kau": -0.14357501829490107
            },
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "bike": {
            "constant": (1.9839467875824828, 2.3917971618194063),
            "log": {
                "logsum": 0.528506854951
            },
            "generation": {
                "cbd": -0.4547226414368938,
                "helsinki_other": -0.11704519178133155,
                "espoo_vant_kau": -0.243566027172882
            },
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "walk": {
            "constant": (4.275918726378757, 3.8291474264981513),
            "log": {
                "logsum": 0.528506854951
            },
            "generation": {
                "cbd": 0.05002108621487039,
                "helsinki_other": -0.3561795711238086,
                "espoo_vant_kau": 0.012763501089533369
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
                "cbd": -0.19814001918523882,
                "helsinki_other": -0.02756989868749099,
                "espoo_vant_kau": -0.04482694601043855
            },
            "individual_dummy": {
                "car_users": (1.160303767222481, 1.160303767222481)
            },
            "log": {
                "logsum": 0.376640331653
            },
            "constant": (0.0, -0.04205261977329772),
            "attraction": {

            },
            "impedance": {

            }
        },
        "transit": {
            "constant": (1.6832873308878444, 0.8546765882447533),
            "log": {
                "logsum": 0.376640331653
            },
            "generation": {
                "cbd": 0.38070383658434925,
                "helsinki_other": -0.048618394535027476,
                "espoo_vant_kau": -0.48962908485570245
            },
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "bike": {
            "constant": (0.7902164806081416, 1.3324363758659938),
            "log": {
                "logsum": 0.376640331653
            },
            "generation": {
                "cbd": -0.6474550856084003,
                "helsinki_other": 0.04720642919223314,
                "espoo_vant_kau": -0.06492315740702374
            },
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "walk": {
            "constant": (2.515488773357361, 2.6028221020861526),
            "log": {
                "logsum": 0.376640331653
            },
            "generation": {
                "cbd": 0.15543499402312108,
                "helsinki_other": -0.0885225742611363,
                "espoo_vant_kau": -0.20450002551570054
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
                #left empty on purpose
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
            "constant": (0.37344004706008, 1.070886367846882),
            "generation": {
                "car_density": (2.019845153892125, 2.203129466617543),
                "cbd": 0.12808747865285577,
                "helsinki_other": -0.28136169060556127,
                "espoo_vant_kau": 0.6929362530839216
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
            "constant": (0.9419571012680608, 0.9576244983466689),
            "generation": {
                "cbd": 1.3552256024601312,
                "helsinki_other": -0.6050702472281768,
                "espoo_vant_kau": -2.208318115568031
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
            "constant": (0.901232650926649, 0.3428809788705067),
            "generation": {
                "cbd": -0.0778919511393149,
                "helsinki_other": 0.0,
                "espoo_vant_kau": -1.5422181608452543
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
            "constant": (4.485001448888134, 3.5345561697686794),
            "generation": {
                "cbd": 0.23248072054807142,
                "helsinki_other": -0.25630366460008386,
                "espoo_vant_kau": -0.23330664158990963
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
                "cbd": -0.30811191490119344,
                "helsinki_other": -1.0121849092035655,
                "espoo_vant_kau": -1.153110585153804
            },
            "log": {
                "logsum": 1.04450466839
            },
            "constant": (0.0, -0.6094521983780463),
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "transit": {
            "constant": (2.4786042346020425, 3.443009109737264),
            "log": {
                "logsum": 1.04450466839
            },
            "generation": {
                "cbd": 0.25089976486686016,
                "helsinki_other": 0.08749663497430038,
                "espoo_vant_kau": -0.6797474137454669
            },
            "attraction": {

            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "bike": {
            "constant": (0.3386840000145957, 2.123032937391528),
            "log": {
                "logsum": 1.04450466839
            },
            "generation": {
                "cbd": 0.24239344795035705,
                "helsinki_other": 0.2861582977443439,
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
            "constant": (4.64565630822768, 4.5903655575666855),
            "log": {
                "logsum": 1.04450466839
            },
            "generation": {
                "cbd": 1.274129098856262,
                "helsinki_other": -0.6428067015010855,
                "espoo_vant_kau": -0.36735667529001925
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