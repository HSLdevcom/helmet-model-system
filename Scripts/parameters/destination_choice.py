
from typing import Any, Dict
import numpy as np # type: ignore


### DESTINATION CHOICE PARAMETERS ###

# Destination choice (generated 2.9.2024)
destination_choice = {
    "hw": {
        "car": {
            "attraction": {
                "parking_cost_work": (-0.342515069907, -0.342515069907)
            },
            "impedance": {
                "time": (-0.018463012860336, -0.018463012860336),
                "cost": (-0.139871309548, -0.139871309548)
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "workplaces": 1.0,
                "shops": 0.6272981122453887
            }
        },
        "transit": {
            "impedance": {
                "cost": (-0.139871309548, -0.139871309548),
                "time": -0.0165872750829
            },
            "attraction": {
                "parking_cost_work": (0.101880829735, 0.101880829735)
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "workplaces": 1.0,
                "shops": 0.6272981122453887
            }
        },
        "bike": {
            "impedance": {
                "time": -0.0322129518382
            },
            "log": {
                "time": -0.0296380230616,
                "size": 1.0
            },
            "size": {
                "workplaces": 1.0,
                "shops": 0.6272981122453887
            },
            "attraction": {

            }
        },
        "walk": {
            "impedance": {
                "time": -0.0453525121887
            },
            "log": {
                "time": -0.144203513552,
                "size": 1.0
            },
            "size": {
                "workplaces": 1.0,
                "shops": 0.6272981122453887
            },
            "attraction": {

            }
        },
        "park_and_ride": {
            "impedance": {
                "utility": 0.162806259982
            },
            "attraction": {
                "parking_cost_work": (0.750052854068, 0.750052854068)
            },
            "utility": {
                "facility": {
                    "shops": 1e-05,
                    "cost": -0.139871309548,
                    "time": -0.018463012860336
                },
                "car_impedance": {
                    "time": -0.018463012860336,
                    "cost": -0.139871309548
                },
                "transit_impedance": {
                    "time": -0.0165872750829,
                    "cost": -0.139871309548
                }
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "workplaces": 1.0,
                "shops": 0.6272981122453887
            }
        }
    },
    "hc": {
        "car": {
            "impedance": {
                "time": (-0.0354638078517, -0.0354638078517)
            },
            "log": {
                "transform": -2.09144887123,
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
                "comprehensive_schools_other": 0.1333390853310356,
                "secondary_schools": 0.5050821783216296
            },
            "attraction": {

            }
        },
        "transit": {
            "log": {
                "transform": -2.09144887123,
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
                "time": -0.0225341436648
            },
            "size": {
                "comprehensive_schools_own": 1.0,
                "comprehensive_schools_other": 0.1333390853310356,
                "secondary_schools": 0.5050821783216296
            },
            "attraction": {

            }
        },
        "bike": {
            "impedance": {
                "time": -0.0989728207693
            },
            "log": {
                "time": 0.566792062632,
                "size": 1.0
            },
            "size": {
                "comprehensive_schools_own": 1.0,
                "comprehensive_schools_other": 0.1333390853310356,
                "secondary_schools": 0.5050821783216296
            },
            "attraction": {
                "cbd": -1.0
            }
        },
        "walk": {
            "impedance": {
                "time": -0.121823411404
            },
            "log": {
                "time": 0.323242691676,
                "size": 1.0
            },
            "size": {
                "comprehensive_schools_own": 1.0,
                "comprehensive_schools_other": 0.1333390853310356,
                "secondary_schools": 0.5050821783216296
            },
            "attraction": {

            }
        }
    },
    "hu": {
        "car": {
            "attraction": {
                "parking_cost_work": (-1.22065217547, -1.22065217547)
            },
            "impedance": {
                "time": (-0.033734239934868, -0.033734239934868),
                "cost": (-0.255562423749, -0.255562423749)
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "secondary_schools": 1.0,
                "tertiary_education": 1.8687634921828995
            }
        },
        "transit": {
            "impedance": {
                "cost": (-0.255562423749, -0.255562423749),
                "time": -0.0210012747331
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "secondary_schools": 1.0,
                "tertiary_education": 1.8687634921828995
            },
            "attraction": {

            }
        },
        "bike": {
            "impedance": {
                "time": -0.0895283563094
            },
            "log": {
                "time": 1.38459887003,
                "size": 1.0
            },
            "size": {
                "secondary_schools": 1.0,
                "tertiary_education": 1.8687634921828995
            },
            "attraction": {

            }
        },
        "walk": {
            "impedance": {
                "time": -0.125303041384
            },
            "log": {
                "time": 0.629022905602,
                "size": 1.0
            },
            "size": {
                "secondary_schools": 1.0,
                "tertiary_education": 1.8687634921828995
            },
            "attraction": {

            }
        }
    },
    "hs": {
        "car": {
            "attraction": {
                "parking_cost_errand": (-0.216893455253, -0.216893455253)
            },
            "impedance": {
                "time": (-0.0436816541396775, -0.0436816541396775),
                "cost": (-0.488063174745, -0.488063174745)
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "population": 1.0,
                "service_own": 3.6719688394365027,
                "service_other": 8.469208553137102,
                "shops": 131.71316047456068
            }
        },
        "transit": {
            "impedance": {
                "cost": (-0.488063174745, -0.488063174745),
                "time": -0.0314514200469
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "population": 1.0,
                "service_own": 3.6719688394365027,
                "service_other": 8.469208553137102,
                "shops": 131.71316047456068
            },
            "attraction": {

            }
        },
        "bike": {
            "impedance": {
                "time": -0.0847216033539
            },
            "log": {
                "time": 0.190532678912,
                "size": 1.0
            },
            "size": {
                "population": 1.0,
                "service_own": 3.6719688394365027,
                "service_other": 8.469208553137102,
                "shops": 131.71316047456068
            },
            "attraction": {

            }
        },
        "walk": {
            "impedance": {
                "time": -0.0881879206739
            },
            "log": {
                "time": 0.151299874148,
                "size": 1.0
            },
            "size": {
                "population": 1.0,
                "service_own": 3.6719688394365027,
                "service_other": 8.469208553137102,
                "shops": 131.71316047456068
            },
            "attraction": {

            }
        }
    },
    "ho": {
        "car": {
            "attraction": {
                "parking_cost_errand": (-0.242043274399, -0.242043274399)
            },
            "impedance": {
                "time": (-0.041855820669452, -0.041855820669452),
                "cost": (-0.46766280077600003, -0.46766280077600003)
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "population": 0.2685443681333689,
                "service_own": 1.0,
                "service_other": 0.30698758271050564,
                "shops": 2.272130355918152
            }
        },
        "transit": {
            "impedance": {
                "cost": (-0.267662800776, -0.267662800776),
                "time": -0.0215584748662
            },
            "attraction": {
                "cbd": 0.780330855558,
                "own_zone": -7.89782713084
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "population": 0.2685443681333689,
                "service_own": 1.0,
                "service_other": 0.30698758271050564,
                "shops": 2.272130355918152
            }
        },
        "bike": {
            "impedance": {
                "time": -0.0879826791601
            },
            "log": {
                "time": 0.599625961983,
                "size": 1.0
            },
            "size": {
                "population": 0.2685443681333689,
                "service_own": 1.0,
                "service_other": 0.30698758271050564,
                "shops": 2.272130355918152
            },
            "attraction": {

            }
        },
        "walk": {
            "impedance": {
                "time": -0.0604420957549
            },
            "log": {
                "time": 0.0602321247351,
                "size": 1.0
            },
            "size": {
                "population": 0.2685443681333689,
                "service_own": 1.0,
                "service_other": 0.30698758271050564,
                "shops": 2.272130355918152
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
                "parking_cost_errand": (-0.143364715541, -0.143364715541)
            },
            "impedance": {
                "time": (-0.030217135667246497, -0.030217135667246497),
                "cost": (-0.337621627567, -0.337621627567)
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "population": 1.0,
                "service": 5.99638688387262,
                "shops": 33.847956331783536
            }
        },
        "transit": {
            "impedance": {
                "cost": (-0.337621627567, -0.337621627567),
                "time": -0.0188789753296
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "population": 1.0,
                "service": 5.99638688387262,
                "shops": 33.847956331783536
            },
            "attraction": {

            }
        },
        "bike": {
            "impedance": {
                "time": -0.0857607900308
            },
            "log": {
                "time": 0.0799687416129,
                "size": 1.0
            },
            "size": {
                "population": 1.0,
                "service": 5.99638688387262,
                "shops": 33.847956331783536
            },
            "attraction": {

            }
        },
        "walk": {
            "impedance": {
                "time": -0.0782333623268
            },
            "log": {
                "time": -0.133569594496,
                "size": 1.0
            },
            "size": {
                "population": 1.0,
                "service": 5.99638688387262,
                "shops": 33.847956331783536
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
