
from typing import Any, Dict
import numpy as np # type: ignore


### DESTINATION CHOICE PARAMETERS ###

# Destination choice (generated 2.9.2024)
destination_choice = {
    "hw": {
        "car": {
            "attraction": {
                "parking_cost_work": (-0.288745496979, -0.288745496979),
                "parking_time": (-0.018625929329436, -0.018625929329436)
            },
            "impedance": {
                "time": (-0.018625929329436, -0.018625929329436),
                "cost": (-0.141105525223, -0.141105525223)
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "workplaces": 1.0,
                "shops": 0.5613996161385892
            }
        },
        "transit": {
            "impedance": {
                "cost": (-0.141105525223, -0.141105525223),
                "time": -0.0175649864963
            },
            "attraction": {
                "parking_cost_work": (0.101881603013, 0.101881603013)
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "workplaces": 1.0,
                "shops": 0.5613996161385892
            }
        },
        "bike": {
            "impedance": {
                "time": -0.0330373117222
            },
            "log": {
                "time": -0.0367379619167,
                "size": 1.0
            },
            "size": {
                "workplaces": 1.0,
                "shops": 0.5613996161385892
            },
            "attraction": {

            }
        },
        "walk": {
            "impedance": {
                "time": -0.0463234989897
            },
            "log": {
                "time": -0.142311912472,
                "size": 1.0
            },
            "size": {
                "workplaces": 1.0,
                "shops": 0.5613996161385892
            },
            "attraction": {

            }
        },
        "park_and_ride": {
            "impedance": {
                "utility": 0.38565740109
            },
            "attraction": {
                "parking_cost_work": (0.78277663967, 0.78277663967)
            },
            "utility": {
                "facility": {
                    "shops": 1e-05,
                    "cost": -0.141105525223,
                    "time": -0.018625929329436
                },
                "car_impedance": {
                    "time": -0.018625929329436,
                    "cost": -0.141105525223
                },
                "transit_impedance": {
                    "time": -0.0175649864963,
                    "cost": -0.141105525223
                }
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "workplaces": 1.0,
                "shops": 0.5613996161385892
            }
        }
    },
    "hc": {
        "car": {
            "impedance": {
                "time": (-0.0450795617507, -0.0450795617507)
            },
            "attraction": {
                "parking_time": (-0.0450795617507, -0.0450795617507)
            },
            "log": {
                "transform": -1.98883835433,
                "size": 1.0
            },
            "transform": {
                "attraction": {
                    "parking_cost_errand": 1
                },
                "impedance": {
                    "cost": 1
                }
            },
            "size": {
                "comprehensive_schools_own": 1.0,
                "comprehensive_schools_other": 0.14017697173958366,
                "secondary_schools": 0.20853612337767546
            }
        },
        "transit": {
            "log": {
                "transform": -1.98883835433,
                "size": 1.0
            },
            "transform": {
                "attraction": {

                },
                "impedance": {
                    "cost": (1.0, 1.0)
                }
            },
            "impedance": {
                "time": -0.0245839893632
            },
            "size": {
                "comprehensive_schools_own": 1.0,
                "comprehensive_schools_other": 0.14017697173958366,
                "secondary_schools": 0.20853612337767546
            },
            "attraction": {

            }
        },
        "bike": {
            "impedance": {
                "time": -0.104870095028
            },
            "log": {
                "time": 0.637875354427,
                "size": 1.0
            },
            "size": {
                "comprehensive_schools_own": 1.0,
                "comprehensive_schools_other": 0.14017697173958366,
                "secondary_schools": 0.20853612337767546
            },
            "attraction": {

            }
        },
        "walk": {
            "impedance": {
                "time": -0.1203910345
            },
            "log": {
                "time": 0.402158460638,
                "size": 1.0
            },
            "size": {
                "comprehensive_schools_own": 1.0,
                "comprehensive_schools_other": 0.14017697173958366,
                "secondary_schools": 0.20853612337767546
            },
            "attraction": {

            }
        }
    },
    "hu": {
        "car": {
            "attraction": {
                "parking_cost_work": (-1.69910850394, -1.69910850394),
                "parking_time": (-0.035019399564996, -0.035019399564996)
            },
            "impedance": {
                "time": (-0.035019399564996, -0.035019399564996),
                "cost": (-0.265298481553, -0.265298481553)
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "secondary_schools": 1.0,
                "tertiary_education": 2.6507508111673426
            }
        },
        "transit": {
            "impedance": {
                "cost": (-0.265298481553, -0.265298481553),
                "time": -0.019996601922
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "secondary_schools": 1.0,
                "tertiary_education": 2.6507508111673426
            },
            "attraction": {

            }
        },
        "bike": {
            "impedance": {
                "time": -0.0714345999019
            },
            "log": {
                "time": 0.448561178711,
                "size": 1.0
            },
            "size": {
                "secondary_schools": 1.0,
                "tertiary_education": 2.6507508111673426
            },
            "attraction": {

            }
        },
        "walk": {
            "impedance": {
                "time": -0.0809842733795
            },
            "log": {
                "time": 0.186178880894,
                "size": 1.0
            },
            "size": {
                "secondary_schools": 1.0,
                "tertiary_education": 2.6507508111673426
            },
            "attraction": {

            }
        }
    },
    "hs": {
        "car": {
            "attraction": {
                "parking_cost_errand": (-0.102343407187, -0.102343407187),
                "parking_time": (-0.04533294350854449, -0.04533294350854449)
            },
            "impedance": {
                "time": (-0.04533294350854449, -0.04533294350854449),
                "cost": (-0.506513335291, -0.506513335291)
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "population": 1.0,
                "service_own": 49.18460243360923,
                "service_other": 19.407485783473906,
                "shops": 249.6694818591807
            }
        },
        "transit": {
            "impedance": {
                "cost": (-0.506513335291, -0.506513335291),
                "time": -0.0335454061032
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "population": 1.0,
                "service_own": 49.18460243360923,
                "service_other": 19.407485783473906,
                "shops": 249.6694818591807
            },
            "attraction": {

            }
        },
        "bike": {
            "impedance": {
                "time": -0.0864428137486
            },
            "log": {
                "time": 0.206026853467,
                "size": 1.0
            },
            "size": {
                "population": 1.0,
                "service_own": 49.18460243360923,
                "service_other": 19.407485783473906,
                "shops": 249.6694818591807
            },
            "attraction": {

            }
        },
        "walk": {
            "impedance": {
                "time": -0.085447273384
            },
            "log": {
                "time": 0.143220147859,
                "size": 1.0
            },
            "size": {
                "population": 1.0,
                "service_own": 49.18460243360923,
                "service_other": 19.407485783473906,
                "shops": 249.6694818591807
            },
            "attraction": {

            }
        }
    },
    "ho": {
        "car": {
            "attraction": {
                "parking_cost_errand": (-0.176567704266, -0.176567704266),
                "parking_time": (-0.0226284516970615, -0.0226284516970615)
            },
            "impedance": {
                "time": (-0.0226284516970615, -0.0226284516970615),
                "cost": (-0.252831862537, -0.252831862537)
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "population": 0.061936408758314535,
                "service_own": 1.0,
                "service_other": 0.2509289530439359,
                "shops": 0.7525520585121053
            }
        },
        "transit": {
            "impedance": {
                "cost": (-0.252831862537, -0.252831862537),
                "time": -0.020713707603
            },
            "attraction": {
                "cbd": 0.941393220072,
                "own_zone": -7.61339101141
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "population": 0.061936408758314535,
                "service_own": 1.0,
                "service_other": 0.2509289530439359,
                "shops": 0.7525520585121053
            }
        },
        "bike": {
            "impedance": {
                "time": -0.0905026960757
            },
            "log": {
                "time": 0.602663373539,
                "size": 1.0
            },
            "size": {
                "population": 0.061936408758314535,
                "service_own": 1.0,
                "service_other": 0.2509289530439359,
                "shops": 0.7525520585121053
            },
            "attraction": {

            }
        },
        "walk": {
            "impedance": {
                "time": -0.0611676349482
            },
            "log": {
                "time": 0.0527078868191,
                "size": 1.0
            },
            "size": {
                "population": 0.061936408758314535,
                "service_own": 1.0,
                "service_other": 0.2509289530439359,
                "shops": 0.7525520585121053
            },
            "attraction": {

            }
        }
    },
    "hh": {
        "car": {
            "attraction": {
            },
            "impedance": {
            },
            "log": {
            },
            "size": {
            }
        },
        "transit": {
            "impedance": {
            },
            "attraction": {
            },
            "log": {
            },
            "size": {
            }
        },
        "bike": {
            "impedance": {
            },
            "log": {
            },
            "size": {
            },
            "attraction": {
            },
        },
        "walk": {
            "impedance": {
            },
            "log": {
            },
            "size": {
            },
            "attraction": {
            },
        }
    },
    "hoo": {
        "car": {
            "log": {
                "size": 1.0
            },
            "size": {
                "population": 1.0,
                "service": 5.65054846698699,
                "shops": 20.999177846492255
            },
            "impedance": {
                "time": -0.154094521902
            },
            "attraction": {
                "parking_cost_errand": -0.352258723591,
                "parking_time": -0.154094521902
            }
        },
        "transit": {
            "log": {
                "size": 1.0
            },
            "size": {
                "population": 1.0,
                "service": 5.65054846698699,
                "shops": 20.999177846492255
            },
            "impedance": {
                "time": -0.0640084587647
            },
            "attraction": {

            }
        },
        "bike": {
            "log": {
                "size": 1.0
            },
            "size": {
                "population": 1.0,
                "service": 5.65054846698699,
                "shops": 20.999177846492255
            },
            "impedance": {
                "time": -0.12934693149
            },
            "attraction": {

            }
        }
    },
    "wo": {
        "car": {
            "attraction": {
                "parking_cost_errand": (-0.0718097046785, -0.0718097046785),
                "parking_time": (-0.0314413700185545, -0.0314413700185545)
            },
            "impedance": {
                "time": (-0.0314413700185545, -0.0314413700185545),
                "cost": (-0.351300223671, -0.351300223671)
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "population": 1.0,
                "service": 32.90788773696218,
                "shops": 76.68476989989074
            }
        },
        "transit": {
            "impedance": {
                "cost": (-0.351300223671, -0.351300223671),
                "time": -0.0208592688918
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "population": 1.0,
                "service": 32.90788773696218,
                "shops": 76.68476989989074
            },
            "attraction": {

            }
        },
        "bike": {
            "impedance": {
                "time": -0.0842740311278
            },
            "log": {
                "time": 0.0535929303143,
                "size": 1.0
            },
            "size": {
                "population": 1.0,
                "service": 32.90788773696218,
                "shops": 76.68476989989074
            },
            "attraction": {

            }
        },
        "walk": {
            "impedance": {
                "time": -0.0822325190087
            },
            "log": {
                "time": -0.0416670319077,
                "size": 1.0
            },
            "size": {
                "population": 1.0,
                "service": 32.90788773696218,
                "shops": 76.68476989989074
            },
            "attraction": {

            }
        }
    },
    "oo": {
        "car": {
            "attraction": {
                "parking_cost_errand": (-0.0718097046785, -0.0718097046785),
                "parking_time": (-0.0314413700185545, -0.0314413700185545)
            },
            "impedance": {
                "time": (-0.0314413700185545, -0.0314413700185545),
                "cost": (-0.351300223671, -0.351300223671)
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "population": 1.0,
                "service": 32.90788773696218,
                "shops": 76.68476989989074
            }
        },
        "transit": {
            "impedance": {
                "cost": (-0.351300223671, -0.351300223671),
                "time": -0.0208592688918
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "population": 1.0,
                "service": 32.90788773696218,
                "shops": 76.68476989989074
            },
            "attraction": {

            }
        },
        "bike": {
            "impedance": {
                "time": -0.0842740311278
            },
            "log": {
                "time": 0.0535929303143,
                "size": 1.0
            },
            "size": {
                "population": 1.0,
                "service": 32.90788773696218,
                "shops": 76.68476989989074
            },
            "attraction": {

            }
        },
        "walk": {
            "impedance": {
                "time": -0.0822325190087
            },
            "log": {
                "time": -0.0416670319077,
                "size": 1.0
            },
            "size": {
                "population": 1.0,
                "service": 32.90788773696218,
                "shops": 76.68476989989074
            },
            "attraction": {

            }
        }
    },
    "wh": {
        "car": {
            "attraction": {

            },
            "impedance": {
                "time": (-0.0132535252, -0.0180517183),
                "cost": (-0.1004054942, -0.136755441374)
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "population_own": 1.3693934320750605,
                "population_other": 1
            }
        },
        "transit": {
            "attraction": {

            },
            "impedance": {
                "time": -0.0101838292646,
                "cost": (-0.100405494227, -0.136755441374)
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "population_own": 1.3693934320750605,
                "population_other": 1
            }
        },
        "bike": {
            "attraction": {

            },
            "impedance": {

            },
            "log": {
                "dist": (-1.11623384398, -1.3592708114),
                "size": 1.0
            },
            "size": {
                "population_own": 1.3693934320750605,
                "population_other": 1
            }
        },
        "walk": {
            "attraction": {
                "own_zone_area_sqrt": (-2.15046600566, -2.08475720417)
            },
            "impedance": {

            },
            "log": {
                "dist": -2.66277304293,
                "size": 1.0
            },
            "size": {
                "population_own": 1.3693934320750605,
                "population_other": 1
            }
        }
    },
    "hwp": {
        "car": {
            "attraction": {
                "parking_cost_work": -0.15712387374,
                "share_detached_houses": 0.580974879625,
                "own_zone_area": -0.0405161484737
            },
            "impedance": {
                "time": -0.0207403513,
                "cost": -0.15712387374
            },
            "log": {
                "size": 0.906942834933
            },
            "size": {
                "workplaces": 1
            }
        },
        "transit": {
            "attraction": {
                "cbd": 0.46008222517,
                "own_zone_area": -0.11315324209
            },
            "impedance": {
                "time": -0.00824400763002,
                "cost": -0.15712387374
            },
            "log": {
                "size": 0.906942834933
            },
            "size": {
                "workplaces": 1
            }
        }
    },
    "hop": {
        "car": {
            "attraction": {
                "car_density": 1.9008789576099998,
                "own_zone_area": -0.00914703619822
            },
            "impedance": {
                "time": -0.0207498305,
                "cost": -0.231841682005
            },
            "log": {
                "size": 1
            },
            "size": {
                "workplaces": 3.4223704732481517,
                "service": 102.563902082003,
                "shops": 222.29744155065126,
                "comprehensive_schools": 10.892468037536473,
                "population_own": 27.85603719152218,
                "population_other": 1
            }
        },
        "transit": {
            "attraction": {

            },
            "impedance": {
                "time": -0.0050318434681,
                "cost": -0.231841682005
            },
            "log": {
                "size": 1
            },
            "size": {
                "workplaces": 3.4223704732481517,
                "service": 102.563902082003,
                "shops": 222.29744155065126,
                "comprehensive_schools": 10.892468037536473,
                "population_own": 27.85603719152218,
                "population_other": 1
            }
        }
    },
    "sop": {
        "logsum": {
            "attraction": {
                "own_zone": 0.491757816367
            },
            "impedance": {

            },
            "log": {
                "logsum": 0.852698948873,
                "size": 0.824476718431
            },
            "size": {
                "workplaces": 51.10448102721859,
                "population_own": 20.97622199539852,
                "population_other": 1.0
            }
        }
    },
    "oop": {
        "car": {
            "attraction": {
                "parking_cost_errand": -0.227398812175
            },
            "impedance": {
                "time": (-0.0427365675012, -0.0477365675012),
                "cost": -0.227398812175
            },
            "log": {
                "size": 1
            },
            "size": {
                "population": 1,
                "workplaces": 3.548453112443126,
                "shops_cbd": (np.float64(2.9726339946617237), np.float64(441.17800200345823)),
                "shops_elsewhere": 13.766802535817257
            }
        },
        "transit": {
            "attraction": {
                "cbd": (1.84600723332, 4.84600723332)
            },
            "impedance": {
                "time": -0.00819579857062,
                "cost": (-0.427398812175, -0.427398812175)
            },
            "log": {
                "size": 1
            },
            "size": {
                "population": 1,
                "workplaces": 3.548453112443126,
                "shops_cbd": 59.7069498589009,
                "shops_elsewhere": 13.766802535817257
            }
        }
    }
}
# Maximum possible distance to destination
distance_boundary = {
    "car": 9999,
    "transit": 9999,
    "bike": 60,
    "walk": 15,
    "park_and_ride": 9999,
}
# O-D pairs with demand below threshold are neglected in sec dest calculation
secondary_destination_threshold = 0.1
