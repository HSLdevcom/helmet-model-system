
from typing import Any, Dict
import numpy as np # type: ignore


### DESTINATION CHOICE PARAMETERS ###

# Destination choice (generated 2.9.2024)
destination_choice = {
    "hw": {
        "car": {
            "attraction": {
                "parking_cost_work": (-0.273695999725, -0.273695999725)
            },
            "impedance": {
                "time": (-0.018480763956864, -0.018480763956864),
                "cost": (-0.140005787552, -0.140005787552)
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "workplaces": 1.0,
                "area": 85.15485292715536
            }
        },
        "transit": {
            "impedance": {
                "cost": (-0.140005787552, -0.140005787552),
                "time": (-0.016972928457, -0.016972928457)
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "workplaces": 1.0,
                "area": 85.15485292715536
            }
        },
        "bike": {
            "impedance": {
                "dist": -0.142870222143
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "workplaces": 1.0,
                "area": 85.15485292715536
            }
        },
        "walk": {
            "impedance": {
                "dist": -0.601229291092
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "workplaces": 1.0,
                "area": 85.15485292715536
            }
        }
    },
    "hc": {
        "car": {
            "impedance": {
                "time": (-0.0651224641997, -0.0651224641997)
            },
            "log": {
                "transform": -1.7803163780000002,
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
                "secondary_schools": 0.5184168941205347,
                "area": 84.44188603996112
            }
        },
        "transit": {
            "log": {
                "transform": -1.7803163780000002,
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
                "time": (-0.025324773613900002, -0.025324773613900002)
            },
            "size": {
                "comprehensive_schools": 1.0,
                "secondary_schools": 0.5184168941205347,
                "area": 84.44188603996112
            }
        },
        "bike": {
            "impedance": {
                "dist": -0.41162182123
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "comprehensive_schools": 1.0,
                "secondary_schools": 0.5184168941205347,
                "area": 84.44188603996112
            }
        },
        "walk": {
            "impedance": {
                "dist": -0.907668871567
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "comprehensive_schools": 1.0,
                "secondary_schools": 0.5184168941205347,
                "area": 84.44188603996112
            }
        }
    },
    "hu": {
        "car": {
            "attraction": {
                "parking_cost_work": (0.0141377297019, 0.0141377297019)
            },
            "impedance": {
                "time": (-0.029113927908516003, -0.029113927908516003),
                "cost": (-0.220560059913, -0.220560059913)
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "secondary_schools": 1.0,
                "tertiary_education": 2.309725037812683,
                "area": 772.5951659479507
            }
        },
        "transit": {
            "impedance": {
                "cost": (-0.220560059913, -0.220560059913),
                "time": (-0.0195111793724, -0.0195111793724)
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "secondary_schools": 1.0,
                "tertiary_education": 2.309725037812683,
                "area": 772.5951659479507
            }
        },
        "bike": {
            "impedance": {
                "dist": -0.268548936417
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "secondary_schools": 1.0,
                "tertiary_education": 2.309725037812683,
                "area": 772.5951659479507
            }
        },
        "walk": {
            "impedance": {
                "dist": -0.716215569049
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "secondary_schools": 1.0,
                "tertiary_education": 2.309725037812683,
                "area": 772.5951659479507
            }
        }
    },
    "hs": {
        "car": {
            "attraction": {
                "parking_cost_errand": (-0.26545384075100004, -0.26545384075100004)
            },
            "impedance": {
                "time": (-0.0459163563410375, -0.0459163563410375),
                "cost": (-0.5130319144250001, -0.5130319144250001)
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "population": 1.0,
                "service": 8.050306985676482,
                "shops": 178.9029456047575,
                "area": 1466.6244395531417
            }
        },
        "transit": {
            "impedance": {
                "cost": (-0.5130319144250001, -0.5130319144250001),
                "time": (-0.0321923140734, -0.0321923140734)
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "population": 1.0,
                "service": 8.050306985676482,
                "shops": 178.9029456047575,
                "area": 1466.6244395531417
            }
        },
        "bike": {
            "impedance": {
                "dist": -0.376205806825
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "population": 1.0,
                "service": 8.050306985676482,
                "shops": 178.9029456047575,
                "area": 1466.6244395531417
            }
        },
        "walk": {
            "impedance": {
                "dist": -0.8951182013429999
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "population": 1.0,
                "service": 8.050306985676482,
                "shops": 178.9029456047575,
                "area": 1466.6244395531417
            }
        }
    },
    "ho": {
        "car": {
            "impedance": {
                "time": (0.000895, 0.000895),
                "cost": (0.01, 0.01)
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "population": 1.0,
                "service": 20.085536923187668,
                "shops": 7.38905609893065,
                "area": 1.0
            }
        },
        "transit": {
            "impedance": {
                "cost": (0.01, 0.01),
                "time": (-0.024812532636, -0.024812532636)
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "population": 1.0,
                "service": 20.085536923187668,
                "shops": 7.38905609893065,
                "area": 1.0
            }
        },
        "bike": {
            "impedance": {
                "dist": -0.390121359793
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "population": 1.0,
                "service": 20.085536923187668,
                "shops": 7.38905609893065,
                "area": 1.0
            }
        },
        "walk": {
            "impedance": {
                "dist": -1.32830205317
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "population": 1.0,
                "service": 20.085536923187668,
                "shops": 7.38905609893065,
                "area": 1.0
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
                "parking_cost_errand": (-0.204598505332, -0.204598505332)
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
                "time": -0.046455399199400005
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
                "own_zone": (1034.3523780364185, 1034.3523780364185)
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
                "own_zone": (1034.3523780364185, 1034.3523780364185)
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
                "own_zone": (1034.3523780364185, 1034.3523780364185)
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
                "own_zone": (1034.3523780364185, 1034.3523780364185)
            }
        }
    },
    "oo": {
        "car": {
            "attraction": {
                "parking_cost_errand": (-0.12024635638699999, -0.12024635638699999)
            },
            "impedance": {
                "time": (-0.029298148659566002, -0.029298148659566002),
                "cost": (-0.32735361630800003, -0.32735361630800003)
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "population": 1.0,
                "service": 6.630673698198112,
                "shops": 56.02846477957964,
                "area": 8143.054966843178
            }
        },
        "transit": {
            "impedance": {
                "cost": (-0.32735361630800003, -0.32735361630800003),
                "time": (-0.0231941928793, -0.0231941928793)
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "population": 1.0,
                "service": 6.630673698198112,
                "shops": 56.02846477957964,
                "area": 8143.054966843178
            }
        },
        "bike": {
            "impedance": {
                "dist": -0.490089834913
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "population": 1.0,
                "service": 6.630673698198112,
                "shops": 56.02846477957964,
                "area": 8143.054966843178
            }
        },
        "walk": {
            "impedance": {
                "dist": -1.27537248881
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "population": 1.0,
                "service": 6.630673698198112,
                "shops": 56.02846477957964,
                "area": 8143.054966843178
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
                "shops_cbd": (2.9726339946617237, 441.17800200345823),
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
}
# O-D pairs with demand below threshold are neglected in sec dest calculation
secondary_destination_threshold = 0.1
