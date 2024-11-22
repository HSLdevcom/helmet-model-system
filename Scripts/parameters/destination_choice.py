
from typing import Any, Dict
import numpy as np # type: ignore


### DESTINATION CHOICE PARAMETERS ###

# Destination choice (generated 2.9.2024)
destination_choice = {
    "hw": {
        "car": {
            "attraction": {
                "parking_cost_work": (-0.313674517231, -0.313674517231)
            },
            "impedance": {
                "time": (-0.019273809692544004, -0.019273809692544004),
                "cost": (-0.146013709792, -0.146013709792)
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "workplaces": 1.0,
                "zone_area": 112.72431420379814
            }
        },
        "transit": {
            "impedance": {
                "cost": (-0.146013709792, -0.146013709792),
                "time": -0.0174294749661
            },
            "attraction": {
                "parking_cost_work": (0.115186232819, 0.115186232819)
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "workplaces": 1.0,
                "zone_area": 112.72431420379814
            }
        },
        "bike": {
            "impedance": {
                "dist": -0.136332722306
            },
            "attraction": {
                "parking_cost_work": (-0.0892942135332, -0.0892942135332)
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "workplaces": 1.0,
                "zone_area": 112.72431420379814
            }
        },
        "walk": {
            "attraction": {
                "parking_cost_work": (-0.0115825697488, -0.0115825697488)
            },
            "impedance": {
                "dist": -0.594765428696
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "workplaces": 1.0,
                "zone_area": 112.72431420379814
            }
        },
        "park_and_ride": {
            "impedance": {
                "cost": -0.00770353464125
            },
            "attraction": {
                "parking_cost_work": (0.771663871487, 0.771663871487)
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "workplaces": 1.0,
                "zone_area": 112.72431420379814
            }
        }
    },
    "hc": {
        "car": {
            "impedance": {
                "time": (-0.133199078811, -0.133199078811)
            },
            "log": {
                "transform": -0.524105363129,
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
                "comprehensive_schools": 1.0,
                "secondary_schools": 0.3714895792335832,
                "zone_area": 0.010051835744633586
            },
            "attraction": {

            }
        },
        "transit": {
            "log": {
                "transform": -0.524105363129,
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
                "time": -0.0295809591255
            },
            "size": {
                "comprehensive_schools": 1.0,
                "secondary_schools": 0.3714895792335832,
                "zone_area": 0.010051835744633586
            },
            "attraction": {

            }
        },
        "bike": {
            "impedance": {
                "time": -0.0792213352194
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "comprehensive_schools": 1.0,
                "secondary_schools": 0.3714895792335832,
                "zone_area": 0.010051835744633586
            },
            "attraction": {

            }
        },
        "walk": {
            "impedance": {
                "dist": -1.31224668108
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "comprehensive_schools": 1.0,
                "secondary_schools": 0.3714895792335832,
                "zone_area": 0.010051835744633586
            },
            "attraction": {

            }
        }
    },
    "hu": {
        "car": {
            "attraction": {
                "parking_cost_work": (-0.0161348521922, -0.0161348521922)
            },
            "impedance": {
                "time": (-0.031794407186916, -0.031794407186916),
                "cost": (-0.240866721113, -0.240866721113)
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "secondary_schools": 1.0,
                "tertiary_education": 2.294997459829979,
                "zone_area": 732.7216528168823
            }
        },
        "transit": {
            "impedance": {
                "cost": (-0.240866721113, -0.240866721113),
                "time": -0.0197781048104
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "secondary_schools": 1.0,
                "tertiary_education": 2.294997459829979,
                "zone_area": 732.7216528168823
            },
            "attraction": {

            }
        },
        "bike": {
            "impedance": {
                "dist": -0.259597424497
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "secondary_schools": 1.0,
                "tertiary_education": 2.294997459829979,
                "zone_area": 732.7216528168823
            },
            "attraction": {

            }
        },
        "walk": {
            "impedance": {
                "dist": -0.727509037227
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "secondary_schools": 1.0,
                "tertiary_education": 2.294997459829979,
                "zone_area": 732.7216528168823
            },
            "attraction": {

            }
        }
    },
    "hs": {
        "car": {
            "attraction": {
                "parking_cost_errand": (-0.289716191347, -0.289716191347)
            },
            "impedance": {
                "time": (-0.047761288876862505, -0.047761288876862505),
                "cost": (-0.533645685775, -0.533645685775)
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "population": 1.0,
                "service": 5.175444887368656,
                "shops": 114.30948936377467,
                "zone_area": 0.010051835744633586
            }
        },
        "transit": {
            "impedance": {
                "cost": (-0.533645685775, -0.533645685775),
                "time": -0.0281617594632
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "population": 1.0,
                "service": 5.175444887368656,
                "shops": 114.30948936377467,
                "zone_area": 0.010051835744633586
            },
            "attraction": {

            }
        },
        "bike": {
            "impedance": {
                "time": -0.0754786139013
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "population": 1.0,
                "service": 5.175444887368656,
                "shops": 114.30948936377467,
                "zone_area": 0.010051835744633586
            },
            "attraction": {

            }
        },
        "walk": {
            "impedance": {
                "dist": -0.891538323184
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "population": 1.0,
                "service": 5.175444887368656,
                "shops": 114.30948936377467,
                "zone_area": 0.010051835744633586
            },
            "attraction": {

            }
        }
    },
    "ho": {
        "car": {
            "impedance": {
                "time": (-0.026922813990888, -0.026922813990888),
                "cost": (-0.300813564144, -0.300813564144)
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "population": 0.0004279153179266443,
                "service": 0.0007544368905376652,
                "shops": 0.008413253298912743,
                "zone_area": 1.0
            },
            "attraction": {

            }
        },
        "transit": {
            "impedance": {
                "cost": (-0.300813564144, -0.300813564144),
                "time": -0.0233518342265
            },
            "attraction": {
                "cbd": 1.380570068,
                "own_zone": -4.10690074909
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "population": 0.0004279153179266443,
                "service": 0.0007544368905376652,
                "shops": 0.008413253298912743,
                "zone_area": 1.0
            }
        },
        "bike": {
            "impedance": {
                "dist": -0.318658695058
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "population": 0.0004279153179266443,
                "service": 0.0007544368905376652,
                "shops": 0.008413253298912743,
                "zone_area": 1.0
            },
            "attraction": {

            }
        },
        "walk": {
            "impedance": {
                "dist": -0.671057122837
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "population": 0.0004279153179266443,
                "service": 0.0007544368905376652,
                "shops": 0.008413253298912743,
                "zone_area": 1.0
            },
            "attraction": {

            }
        }
    },
    "hoo": {
        "car": {
            "log": {
                "size": 1.0
            },
            "size": {
                "population": 1.0,
                "service": 4.483830444198899,
                "shops": 19.014887841870237
            },
            "impedance": {
                "time": -0.167802825326
            },
            "attraction": {
                "parking_cost_errand": -0.204598505332
            }
        },
        "transit": {
            "log": {
                "size": 1.0
            },
            "size": {
                "population": 1.0,
                "service": 4.483830444198899,
                "shops": 19.014887841870237
            },
            "impedance": {
                "time": -0.0464553991994
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
                "service": 4.483830444198899,
                "shops": 19.014887841870237
            },
            "impedance": {
                "dist": -0.847308504612
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
                "parking_cost_errand": (-0.172232765963, -0.172232765963)
            },
            "impedance": {
                "time": (-0.031039447989767, -0.031039447989767),
                "cost": (-0.346809474746, -0.346809474746)
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "population": 1.0,
                "service": 11.90905041786026,
                "shops": 89.12406192915552,
                "zone_area": 9163.194360880556
            }
        },
        "transit": {
            "impedance": {
                "cost": (-0.346809474746, -0.346809474746),
                "time": -0.018975584737
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "population": 1.0,
                "service": 11.90905041786026,
                "shops": 89.12406192915552,
                "zone_area": 9163.194360880556
            },
            "attraction": {

            }
        },
        "bike": {
            "impedance": {
                "dist": -0.423857096651
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "population": 1.0,
                "service": 11.90905041786026,
                "shops": 89.12406192915552,
                "zone_area": 9163.194360880556
            },
            "attraction": {

            }
        },
        "walk": {
            "impedance": {
                "dist": -1.02797125978
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "population": 1.0,
                "service": 11.90905041786026,
                "shops": 89.12406192915552,
                "zone_area": 9163.194360880556
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
