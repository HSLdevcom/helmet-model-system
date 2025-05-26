
from typing import Any, Dict
import numpy as np # type: ignore


### DESTINATION CHOICE PARAMETERS ###

# Destination choice (generated 2.9.2024)
destination_choice = {
    "hw": {
        "car": {
            "attraction": {
                "parking_cost_work": (-0.342801966916, -0.342801966916)
            },
            "impedance": {
                "time": (-0.018423150225612, -0.018423150225612),
                "cost": (-0.139569319891, -0.139569319891)
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "workplaces": 1.0,
                "shops": 0.6272936133911192
            }
        },
        "transit": {
            "impedance": {
                "cost": (-0.139569319891, -0.139569319891),
                "time": -0.0165513077356
            },
            "attraction": {
                "parking_cost_work": (0.101374043468, 0.101374043468)
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "workplaces": 1.0,
                "shops": 0.6272936133911192
            }
        },
        "bike": {
            "impedance": {
                "time": -0.032173039701
            },
            "log": {
                "time": -0.0307997853003,
                "size": 1.0
            },
            "size": {
                "workplaces": 1.0,
                "shops": 0.6272936133911192
            },
            "attraction": {

            }
        },
        "walk": {
            "impedance": {
                "time": -0.0444302985424
            },
            "log": {
                "time": -0.139324323742,
                "size": 1.0
            },
            "size": {
                "workplaces": 1.0,
                "shops": 0.6272936133911192
            },
            "attraction": {

            }
        },
        "park_and_ride": {
            "impedance": {
                "utility": 0.421733941529
            },
            "attraction": {
                "parking_cost_work": (0.717914956147, 0.717914956147)
            },
            "utility": {
                "facility": {
                    "shops": 1e-05,
                    "cost": -0.139569319891,
                    "time": -0.018423150225612
                },
                "car_impedance": {
                    "time": -0.018423150225612,
                    "cost": -0.139569319891
                },
                "transit_impedance": {
                    "time": -0.0165513077356,
                    "cost": -0.139569319891
                }
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "workplaces": 1.0,
                "shops": 0.6272936133911192
            }
        }
    },
    "hc": {
        "car": {
            "impedance": {
                "time": (-0.038866205867, -0.038866205867)
            },
            "log": {
                "transform": -1.98391717293,
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
                "comprehensive_schools_other": 0.13201422705816748,
                "secondary_schools": 0.21254782920548704
            },
            "attraction": {

            }
        },
        "transit": {
            "log": {
                "transform": -1.98391717293,
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
                "time": -0.0232623436293
            },
            "size": {
                "comprehensive_schools_own": 1.0,
                "comprehensive_schools_other": 0.13201422705816748,
                "secondary_schools": 0.21254782920548704
            },
            "attraction": {

            }
        },
        "bike": {
            "impedance": {
                "time": -0.100395150823
            },
            "log": {
                "time": 0.608074963508,
                "size": 1.0
            },
            "size": {
                "comprehensive_schools_own": 1.0,
                "comprehensive_schools_other": 0.13201422705816748,
                "secondary_schools": 0.21254782920548704
            },
            "attraction": {

            }
        },
        "walk": {
            "impedance": {
                "time": -0.114899693423
            },
            "log": {
                "time": 0.380588529472,
                "size": 1.0
            },
            "size": {
                "comprehensive_schools_own": 1.0,
                "comprehensive_schools_other": 0.13201422705816748,
                "secondary_schools": 0.21254782920548704
            },
            "attraction": {

            }
        }
    },
    "hu": {
        "car": {
            "attraction": {
                "parking_cost_work": (-1.42765645207, -1.42765645207)
            },
            "impedance": {
                "time": (-0.030841014066588002, -0.030841014066588002),
                "cost": (-0.233644045959, -0.233644045959)
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "secondary_schools": 1.0,
                "tertiary_education": 2.6736687422544825
            }
        },
        "transit": {
            "impedance": {
                "cost": (-0.233644045959, -0.233644045959),
                "time": -0.0188876272346
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "secondary_schools": 1.0,
                "tertiary_education": 2.6736687422544825
            },
            "attraction": {

            }
        },
        "bike": {
            "impedance": {
                "time": -0.070615606487
            },
            "log": {
                "time": 0.468789517309,
                "size": 1.0
            },
            "size": {
                "secondary_schools": 1.0,
                "tertiary_education": 2.6736687422544825
            },
            "attraction": {

            }
        },
        "walk": {
            "impedance": {
                "time": -0.0773388967016
            },
            "log": {
                "time": 0.171771530565,
                "size": 1.0
            },
            "size": {
                "secondary_schools": 1.0,
                "tertiary_education": 2.6736687422544825
            },
            "attraction": {

            }
        }
    },
    "hs": {
        "car": {
            "attraction": {
                "parking_cost_errand": (-0.215549007064, -0.215549007064)
            },
            "impedance": {
                "time": (-0.043105319120677, -0.043105319120677),
                "cost": (-0.481623677326, -0.481623677326)
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "population": 1.0,
                "service_own": 8.476983667496237,
                "service_other": 3.6848164284437015,
                "shops": 131.76425689582217
            }
        },
        "transit": {
            "impedance": {
                "cost": (-0.481623677326, -0.481623677326),
                "time": -0.031412409441
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "population": 1.0,
                "service_own": 8.476983667496237,
                "service_other": 3.6848164284437015,
                "shops": 131.76425689582217
            },
            "attraction": {

            }
        },
        "bike": {
            "impedance": {
                "time": -0.0846487231504
            },
            "log": {
                "time": 0.189334335073,
                "size": 1.0
            },
            "size": {
                "population": 1.0,
                "service_own": 8.476983667496237,
                "service_other": 3.6848164284437015,
                "shops": 131.76425689582217
            },
            "attraction": {

            }
        },
        "walk": {
            "impedance": {
                "time": -0.0861843771012
            },
            "log": {
                "time": 0.151580581494,
                "size": 1.0
            },
            "size": {
                "population": 1.0,
                "service_own": 8.476983667496237,
                "service_other": 3.6848164284437015,
                "shops": 131.76425689582217
            },
            "attraction": {

            }
        }
    },
    "ho": {
        "car": {
            "attraction": {
                "parking_cost_errand": (-0.241008933466, -0.241008933466)
            },
            "impedance": {
                "time": (-0.0237219908437375, -0.0237219908437375),
                "cost": (-0.265050177025, -0.265050177025)
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "population": 0.268340957927158,
                "service_own": 1.0,
                "service_other": 0.3094036540736867,
                "shops": 2.271315144501449
            }
        },
        "transit": {
            "impedance": {
                "cost": (-0.265050177025, -0.265050177025),
                "time": -0.0215683966038
            },
            "attraction": {
                "cbd": 0.775238355801,
                "own_zone": -7.92522524459
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "population": 0.268340957927158,
                "service_own": 1.0,
                "service_other": 0.3094036540736867,
                "shops": 2.271315144501449
            }
        },
        "bike": {
            "impedance": {
                "time": -0.0879887012872
            },
            "log": {
                "time": 0.599588470694,
                "size": 1.0
            },
            "size": {
                "population": 0.268340957927158,
                "service_own": 1.0,
                "service_other": 0.3094036540736867,
                "shops": 2.271315144501449
            },
            "attraction": {

            }
        },
        "walk": {
            "impedance": {
                "time": -0.0593521910839
            },
            "log": {
                "time": 0.0629334313695,
                "size": 1.0
            },
            "size": {
                "population": 0.268340957927158,
                "service_own": 1.0,
                "service_other": 0.3094036540736867,
                "shops": 2.271315144501449
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
                "service": 1.5616937845874477,
                "shops": 18.177881093790372
            },
            "impedance": {
                "time": -0.13295314811
            },
            "attraction": {
                "parking_cost_errand": -0.262354727472
            }
        },
        "transit": {
            "log": {
                "size": 1.0
            },
            "size": {
                "population": 1.0,
                "service": 1.5616937845874477,
                "shops": 18.177881093790372
            },
            "impedance": {
                "time": -0.0603680486607
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
                "service": 1.5616937845874477,
                "shops": 18.177881093790372
            },
            "impedance": {
                "dist": -0.515531341887
            },
            "attraction": {

            }
        }
    },
    "wo": {
        "car": {
            "attraction": {
                "parking_cost_errand": -0.291338216556
            },
            "impedance": {
                "time": -0.0371080433,
                "cost": -0.281121539905
            },
            "log": {
                "size": 1
            },
            "size": {
                "population": 1,
                "workplaces": 1.4931447755055838,
                "service": 4.899936388531657,
                "shops_cbd": 36.161227785768844,
                "shops_elsewhere": 29.03185180709253,
                "own_zone": (np.float64(1034.3523780364185), np.float64(1034.3523780364185))
            }
        },
        "transit": {
            "attraction": {
                "cbd": 0.350354942258,
                "own_zone": -1.87675547285
            },
            "impedance": {
                "time": -0.0190572340198,
                "cost": -0.281121539905
            },
            "log": {
                "size": 1
            },
            "size": {
                "population": 1,
                "workplaces": 1.4931447755055838,
                "service": 4.899936388531657,
                "shops_cbd": 36.161227785768844,
                "shops_elsewhere": 29.03185180709253,
                "own_zone": (np.float64(1034.3523780364185), np.float64(1034.3523780364185))
            }
        },
        "bike": {
            "attraction": {

            },
            "impedance": {

            },
            "log": {
                "dist": (-2.05206422461, -1.82198542728),
                "size": 1
            },
            "size": {
                "population": 1,
                "workplaces": 1.4931447755055838,
                "service": 4.899936388531657,
                "shops_cbd": 36.161227785768844,
                "shops_elsewhere": 29.03185180709253,
                "own_zone": (np.float64(1034.3523780364185), np.float64(1034.3523780364185))
            }
        },
        "walk": {
            "attraction": {
                "own_zone_area_sqrt": (-1.10044318679, -1.94548368752)
            },
            "impedance": {

            },
            "log": {
                "dist": -3.38855455974,
                "size": 1
            },
            "size": {
                "population": 1,
                "workplaces": 1.4931447755055838,
                "service": 4.899936388531657,
                "shops_cbd": 36.161227785768844,
                "shops_elsewhere": 29.03185180709253,
                "own_zone": (np.float64(1034.3523780364185), np.float64(1034.3523780364185))
            }
        }
    },
    "oo": {
        "car": {
            "attraction": {
                "parking_cost_errand": (-0.144317572278, -0.144317572278)
            },
            "impedance": {
                "time": (-0.029901260285165498, -0.029901260285165498),
                "cost": (-0.334092293689, -0.334092293689)
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "population": 1.0,
                "service": 6.034287177221872,
                "shops": 33.86903793259901
            }
        },
        "transit": {
            "impedance": {
                "cost": (-0.334092293689, -0.334092293689),
                "time": -0.0188573282936
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "population": 1.0,
                "service": 6.034287177221872,
                "shops": 33.86903793259901
            },
            "attraction": {

            }
        },
        "bike": {
            "impedance": {
                "time": -0.0847828015863
            },
            "log": {
                "time": 0.0651388569873,
                "size": 1.0
            },
            "size": {
                "population": 1.0,
                "service": 6.034287177221872,
                "shops": 33.86903793259901
            },
            "attraction": {

            }
        },
        "walk": {
            "impedance": {
                "time": -0.0766208960579
            },
            "log": {
                "time": -0.124099280361,
                "size": 1.0
            },
            "size": {
                "population": 1.0,
                "service": 6.034287177221872,
                "shops": 33.86903793259901
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
