
from typing import Any, Dict
import numpy as np # type: ignore
from parameters.assignment import inflation

### DESTINATION CHOICE PARAMETERS ###

# Destination choice (generated 2.9.2024)
destination_choice = {
    "hw": {
        "car": {
            "attraction": {
                "parking_cost_work": (-0.279250514208, -0.279250514208),
                "parking_time": (-0.020869875427159405, -0.020869875427159405)
            },
            "impedance": {
                "time": (-0.020869875427159405, -0.020869875427159405),
                "cost": (-0.128474276841, -0.128474276841)
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "workplaces": 1.0,
                "shops": 0.54216836285012
            }
        },
        "transit": {
            "impedance": {
                "cost": (-0.128474276841, -0.128474276841),
                "time": -0.0175541569732
            },
            "attraction": {
                "parking_cost_work": (0.100659754317, 0.100659754317)
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "workplaces": 1.0,
                "shops": 0.54216836285012
            }
        },
        "bike": {
            "impedance": {
                "time": -0.0330658150148
            },
            "log": {
                "time": -0.0363567705766,
                "size": 1.0
            },
            "size": {
                "workplaces": 1.0,
                "shops": 0.54216836285012
            },
            "attraction": {

            }
        },
        "walk": {
            "impedance": {
                "time": -0.0463112640724
            },
            "log": {
                "time": -0.141208888224,
                "size": 1.0
            },
            "size": {
                "workplaces": 1.0,
                "shops": 0.54216836285012
            },
            "attraction": {

            }
        },
        "park_and_ride": {
            "impedance": {
                "utility": 0.379676399593
            },
            "attraction": {
                "parking_cost_work": (0.780735949162, 0.780735949162)
            },
            "utility": {
                "facility": {
                    "shops": 1e-05,
                    "cost": -0.128474276841,
                    "time": -0.020869875427159405
                },
                "car_impedance": {
                    "time": -0.020869875427159405,
                    "cost": -0.128474276841
                },
                "transit_impedance": {
                    "time": -0.0175541569732,
                    "cost": -0.128474276841
                }
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "workplaces": 1.0,
                "shops": 0.54216836285012
            }
        }
    },
    "hc": {
        "car": {
            "impedance": {
                "time": (-0.0435995620816, -0.0435995620816)
            },
            "attraction": {
                "parking_time": (-0.0435995620816, -0.0435995620816)
            },
            "log": {
                "transform": -2.02366730541,
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
                "comprehensive_schools_other": 0.13956288370135,
                "secondary_schools": 0.20989720942020515
            }
        },
        "transit": {
            "log": {
                "transform": -2.02366730541,
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
                "time": -0.0243592473146
            },
            "size": {
                "comprehensive_schools_own": 1.0,
                "comprehensive_schools_other": 0.13956288370135,
                "secondary_schools": 0.20989720942020515
            },
            "attraction": {

            }
        },
        "bike": {
            "impedance": {
                "time": -0.104932435877
            },
            "log": {
                "time": 0.637916070431,
                "size": 1.0
            },
            "size": {
                "comprehensive_schools_own": 1.0,
                "comprehensive_schools_other": 0.13956288370135,
                "secondary_schools": 0.20989720942020515
            },
            "attraction": {

            }
        },
        "walk": {
            "impedance": {
                "time": -0.12046683154
            },
            "log": {
                "time": 0.403331073192,
                "size": 1.0
            },
            "size": {
                "comprehensive_schools_own": 1.0,
                "comprehensive_schools_other": 0.13956288370135,
                "secondary_schools": 0.20989720942020515
            },
            "attraction": {

            }
        }
    },
    "hu": {
        "car": {
            "attraction": {
                "parking_cost_work": (-1.68311842177, -1.68311842177),
                "parking_time": (-0.039189907887181775, -0.039189907887181775)
            },
            "impedance": {
                "time": (-0.039189907887181775, -0.039189907887181775),
                "cost": (-0.241251803004, -0.241251803004)
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "secondary_schools": 1.0,
                "tertiary_education": 2.6418680915034845
            }
        },
        "transit": {
            "impedance": {
                "cost": (-0.241251803004, -0.241251803004),
                "time": -0.0204660533412
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "secondary_schools": 1.0,
                "tertiary_education": 2.6418680915034845
            },
            "attraction": {

            }
        },
        "bike": {
            "impedance": {
                "time": -0.0716928099179
            },
            "log": {
                "time": 0.447846824973,
                "size": 1.0
            },
            "size": {
                "secondary_schools": 1.0,
                "tertiary_education": 2.6418680915034845
            },
            "attraction": {

            }
        },
        "walk": {
            "impedance": {
                "time": -0.0812885750562
            },
            "log": {
                "time": 0.18819545183,
                "size": 1.0
            },
            "size": {
                "secondary_schools": 1.0,
                "tertiary_education": 2.6418680915034845
            },
            "attraction": {

            }
        }
    },
    "hs": {
        "car": {
            "attraction": {
                "parking_cost_errand": (-0.0766197031693, -0.0766197031693),
                "parking_time": (-0.051485525066184805, -0.051485525066184805)
            },
            "impedance": {
                "time": (-0.051485525066184805, -0.051485525066184805),
                "cost": (-0.467773816074, -0.467773816074)
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "population": 1.0,
                "service_own": 49.93783764922847,
                "service_other": 19.67045387984566,
                "shops": 249.5465775211776
            }
        },
        "transit": {
            "impedance": {
                "cost": (-0.467773816074, -0.467773816074),
                "time": -0.0331152208169
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "population": 1.0,
                "service_own": 49.93783764922847,
                "service_other": 19.67045387984566,
                "shops": 249.5465775211776
            },
            "attraction": {

            }
        },
        "bike": {
            "impedance": {
                "time": -0.0864474476481
            },
            "log": {
                "time": 0.206371033551,
                "size": 1.0
            },
            "size": {
                "population": 1.0,
                "service_own": 49.93783764922847,
                "service_other": 19.67045387984566,
                "shops": 249.5465775211776
            },
            "attraction": {

            }
        },
        "walk": {
            "impedance": {
                "time": -0.0854677686498
            },
            "log": {
                "time": 0.144425950116,
                "size": 1.0
            },
            "size": {
                "population": 1.0,
                "service_own": 49.93783764922847,
                "service_other": 19.67045387984566,
                "shops": 249.5465775211776
            },
            "attraction": {

            }
        }
    },
    "ho": {
        "car": {
            "attraction": {
                "parking_cost_errand": (-0.165892738402, -0.165892738402),
                "parking_time": (-0.025898851759425193, -0.025898851759425193)
            },
            "impedance": {
                "time": (-0.025898851759425193, -0.025898851759425193),
                "cost": (-0.235305063003, -0.235305063003)
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "population": 0.06173204645048014,
                "service_own": 1.0,
                "service_other": 0.2518331006765743,
                "shops": 0.7441903771190829
            }
        },
        "transit": {
            "impedance": {
                "cost": (-0.235305063003, -0.235305063003),
                "time": -0.020810402716
            },
            "attraction": {
                "cbd": 0.928379835348,
                "own_zone": -7.57508538159
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "population": 0.06173204645048014,
                "service_own": 1.0,
                "service_other": 0.2518331006765743,
                "shops": 0.7441903771190829
            }
        },
        "bike": {
            "impedance": {
                "time": -0.0904898286091
            },
            "log": {
                "time": 0.604377851918,
                "size": 1.0
            },
            "size": {
                "population": 0.06173204645048014,
                "service_own": 1.0,
                "service_other": 0.2518331006765743,
                "shops": 0.7441903771190829
            },
            "attraction": {

            }
        },
        "walk": {
            "impedance": {
                "time": -0.0611110491419
            },
            "log": {
                "time": 0.0523216180048,
                "size": 1.0
            },
            "size": {
                "population": 0.06173204645048014,
                "service_own": 1.0,
                "service_other": 0.2518331006765743,
                "shops": 0.7441903771190829
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
                "service": 7.735811010118937,
                "shops": 19.35946758160272
            },
            "impedance": {
                "time": -0.160970765754
            },
            "attraction": {
                "parking_cost_errand": -0.0657355485324
            }
        },
        "transit": {
            "log": {
                "size": 1.0
            },
            "size": {
                "population": 1.0,
                "service": 7.735811010118937,
                "shops": 19.35946758160272
            },
            "impedance": {
                "time": -0.0633500467804
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
                "service": 7.735811010118937,
                "shops": 19.35946758160272
            },
            "impedance": {
                "time": -0.129281672822
            },
            "attraction": {

            }
        }
    },
    "wo": {
        "car": {
            "attraction": {
                "parking_cost_errand": (-0.0494444814145, -0.0494444814145),
                "parking_time": (-0.03589673226863408, -0.03589673226863408)
            },
            "impedance": {
                "time": (-0.03589673226863408, -0.03589673226863408),
                "cost": (-0.326141209909, -0.326141209909)
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "population": 1.0,
                "service": 33.013546357236024,
                "shops": 76.2361544274271
            }
        },
        "transit": {
            "impedance": {
                "cost": (-0.326141209909, -0.326141209909),
                "time": -0.0206912612378
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "population": 1.0,
                "service": 33.013546357236024,
                "shops": 76.2361544274271
            },
            "attraction": {

            }
        },
        "bike": {
            "impedance": {
                "time": -0.0842059470286
            },
            "log": {
                "time": 0.0513366551734,
                "size": 1.0
            },
            "size": {
                "population": 1.0,
                "service": 33.013546357236024,
                "shops": 76.2361544274271
            },
            "attraction": {

            }
        },
        "walk": {
            "impedance": {
                "time": -0.0822722174158
            },
            "log": {
                "time": -0.0409936973756,
                "size": 1.0
            },
            "size": {
                "population": 1.0,
                "service": 33.013546357236024,
                "shops": 76.2361544274271
            },
            "attraction": {

            }
        }
    },
    "oo": {
        "car": {
            "attraction": {
                "parking_cost_errand": (-0.0494444814145, -0.0494444814145),
                "parking_time": (-0.03589673226863408, -0.03589673226863408)
            },
            "impedance": {
                "time": (-0.03589673226863408, -0.03589673226863408),
                "cost": (-0.326141209909, -0.326141209909)
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "population": 1.0,
                "service": 33.013546357236024,
                "shops": 76.2361544274271
            }
        },
        "transit": {
            "impedance": {
                "cost": (-0.326141209909, -0.326141209909),
                "time": -0.0206912612378
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "population": 1.0,
                "service": 33.013546357236024,
                "shops": 76.2361544274271
            },
            "attraction": {

            }
        },
        "bike": {
            "impedance": {
                "time": -0.0842059470286
            },
            "log": {
                "time": 0.0513366551734,
                "size": 1.0
            },
            "size": {
                "population": 1.0,
                "service": 33.013546357236024,
                "shops": 76.2361544274271
            },
            "attraction": {

            }
        },
        "walk": {
            "impedance": {
                "time": -0.0822722174158
            },
            "log": {
                "time": -0.0409936973756,
                "size": 1.0
            },
            "size": {
                "population": 1.0,
                "service": 33.013546357236024,
                "shops": 76.2361544274271
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
                "parking_cost_work": -0.15712387374/inflation,
                "share_detached_houses": 0.580974879625,
                "own_zone_area": -0.0405161484737
            },
            "impedance": {
                "time": -0.0207403513,
                "cost": -0.15712387374/inflation
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
                "cost": -0.15712387374/inflation
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
                "cost": -0.231841682005/inflation
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
                "cost": -0.231841682005/inflation
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
                "parking_cost_errand": -0.227398812175/inflation
            },
            "impedance": {
                "time": (-0.0427365675012, -0.0477365675012),
                "cost": -0.227398812175/inflation
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
                "cost": (-0.427398812175/inflation, -0.427398812175/inflation)
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
