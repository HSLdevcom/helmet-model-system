
from typing import Any, Dict
import numpy as np # type: ignore


### DESTINATION CHOICE PARAMETERS ###

# Destination choice (generated 2.9.2024)
destination_choice = {
    "hw": {
        "car": {
            "attraction": {
                "parking_cost_work": (-0.33192798198, -0.33192798198),
                "parking_time": (-0.018404991158664, -0.018404991158664)
            },
            "impedance": {
                "time": (-0.018404991158664, -0.018404991158664),
                "cost": (-0.139431751202, -0.139431751202)
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "workplaces": 1.0,
                "shops": 0.6104118022163425
            }
        },
        "transit": {
            "impedance": {
                "cost": (-0.139431751202, -0.139431751202),
                "time": -0.0172540258972
            },
            "attraction": {
                "parking_cost_work": (0.102222698132, 0.102222698132)
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "workplaces": 1.0,
                "shops": 0.6104118022163425
            }
        },
        "bike": {
            "impedance": {
                "time": -0.0311795779267
            },
            "log": {
                "time": -0.0431750153453,
                "size": 1.0
            },
            "size": {
                "workplaces": 1.0,
                "shops": 0.6104118022163425
            },
            "attraction": {

            }
        },
        "walk": {
            "impedance": {
                "time": -0.0448934708422
            },
            "log": {
                "time": -0.129787417057,
                "size": 1.0
            },
            "size": {
                "workplaces": 1.0,
                "shops": 0.6104118022163425
            },
            "attraction": {

            }
        },
        "park_and_ride": {
            "impedance": {
                "utility": 0.392738903034
            },
            "attraction": {
                "parking_cost_work": (0.744191638908, 0.744191638908)
            },
            "utility": {
                "facility": {
                    "shops": 1e-05,
                    "cost": -0.139431751202,
                    "time": -0.018404991158664
                },
                "car_impedance": {
                    "time": -0.018404991158664,
                    "cost": -0.139431751202
                },
                "transit_impedance": {
                    "time": -0.0172540258972,
                    "cost": -0.139431751202
                }
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "workplaces": 1.0,
                "shops": 0.6104118022163425
            }
        }
    },
    "hc": {
        "car": {
            "impedance": {
                "time": (-0.0458687875951, -0.0458687875951)
            },
            "log": {
                "transform": -1.9648309038,
                "size": 1.0
            },
            "transform": {
                "attraction": {
                    "parking_cost_errand": 1,
                },
                "impedance": {
                    "cost": 1
                }
            },
            "size": {
                "comprehensive_schools_own": 1.0,
                "comprehensive_schools_other": 0.12947776696627225,
                "secondary_schools": 0.20918368574140128
            },
            "attraction": {
                "parking_time": (-0.0458687875951, -0.0458687875951),
            }
        },
        "transit": {
            "log": {
                "transform": -1.9648309038,
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
                "time": -0.0243909853086
            },
            "size": {
                "comprehensive_schools_own": 1.0,
                "comprehensive_schools_other": 0.12947776696627225,
                "secondary_schools": 0.20918368574140128
            },
            "attraction": {

            }
        },
        "bike": {
            "impedance": {
                "time": -0.0932271247019
            },
            "log": {
                "time": 0.541608949236,
                "size": 1.0
            },
            "size": {
                "comprehensive_schools_own": 1.0,
                "comprehensive_schools_other": 0.12947776696627225,
                "secondary_schools": 0.20918368574140128
            },
            "attraction": {

            }
        },
        "walk": {
            "impedance": {
                "time": -0.115034502008
            },
            "log": {
                "time": 0.381378380471,
                "size": 1.0
            },
            "size": {
                "comprehensive_schools_own": 1.0,
                "comprehensive_schools_other": 0.12947776696627225,
                "secondary_schools": 0.20918368574140128
            },
            "attraction": {

            }
        }
    },
    "hu": {
        "car": {
            "attraction": {
                "parking_cost_work": (-1.70498207254, -1.70498207254),
                "parking_time": (-0.034699351229532, -0.034699351229532),
            },
            "impedance": {
                "time": (-0.034699351229532, -0.034699351229532),
                "cost": (-0.262873872951, -0.262873872951)
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "secondary_schools": 1.0,
                "tertiary_education": 2.7111609773727237
            }
        },
        "transit": {
            "impedance": {
                "cost": (-0.262873872951, -0.262873872951),
                "time": -0.0195578441319
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "secondary_schools": 1.0,
                "tertiary_education": 2.7111609773727237
            },
            "attraction": {

            }
        },
        "bike": {
            "impedance": {
                "time": -0.0704756738504
            },
            "log": {
                "time": 0.498948849065,
                "size": 1.0
            },
            "size": {
                "secondary_schools": 1.0,
                "tertiary_education": 2.7111609773727237
            },
            "attraction": {

            }
        },
        "walk": {
            "impedance": {
                "time": -0.0774083262075
            },
            "log": {
                "time": 0.175791824263,
                "size": 1.0
            },
            "size": {
                "secondary_schools": 1.0,
                "tertiary_education": 2.7111609773727237
            },
            "attraction": {

            }
        }
    },
    "hs": {
        "car": {
            "attraction": {
                "parking_cost_errand": (-0.113009972395, -0.113009972395),
                "parking_time": (-0.0447946929189585, -0.0447946929189585)
            },
            "impedance": {
                "time": (-0.0447946929189585, -0.0447946929189585),
                "cost": (-0.500499362223, -0.500499362223)
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "population": 1.0,
                "service_own": 54.7526271521749,
                "service_other": 20.652882290513375,
                "shops": 266.8841712681501
            }
        },
        "transit": {
            "impedance": {
                "cost": (-0.500499362223, -0.500499362223),
                "time": -0.0327173490115
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "population": 1.0,
                "service_own": 54.7526271521749,
                "service_other": 20.652882290513375,
                "shops": 266.8841712681501
            },
            "attraction": {

            }
        },
        "bike": {
            "impedance": {
                "time": -0.0822070283598
            },
            "log": {
                "time": 0.199726086195,
                "size": 1.0
            },
            "size": {
                "population": 1.0,
                "service_own": 54.7526271521749,
                "service_other": 20.652882290513375,
                "shops": 266.8841712681501
            },
            "attraction": {

            }
        },
        "walk": {
            "impedance": {
                "time": -0.0839536967896
            },
            "log": {
                "time": 0.141299370764,
                "size": 1.0
            },
            "size": {
                "population": 1.0,
                "service_own": 54.7526271521749,
                "service_other": 20.652882290513375,
                "shops": 266.8841712681501
            },
            "attraction": {

            }
        }
    },
    "ho": {
        "car": {
            "attraction": {
                "parking_cost_errand": (-0.189642588223, -0.189642588223),
                "parking_time": (-0.023104246599918495, -0.023104246599918495),
            },
            "impedance": {
                "time": (-0.023104246599918495, -0.023104246599918495),
                "cost": (-0.258148006703, -0.258148006703)
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "population": 0.06068045377170062,
                "service_own": 1.0,
                "service_other": 0.2368874941486913,
                "shops": 0.7546021596108856
            }
        },
        "transit": {
            "impedance": {
                "cost": (-0.258148006703, -0.258148006703),
                "time": -0.0220490845657
            },
            "attraction": {
                "cbd": 0.963929945593,
                "own_zone": -6.92853267286
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "population": 0.06068045377170062,
                "service_own": 1.0,
                "service_other": 0.2368874941486913,
                "shops": 0.7546021596108856
            }
        },
        "bike": {
            "impedance": {
                "time": -0.0826308468108
            },
            "log": {
                "time": 0.557793224002,
                "size": 1.0
            },
            "size": {
                "population": 0.06068045377170062,
                "service_own": 1.0,
                "service_other": 0.2368874941486913,
                "shops": 0.7546021596108856
            },
            "attraction": {

            }
        },
        "walk": {
            "impedance": {
                "time": -0.0588648410232
            },
            "log": {
                "time": 0.0483523498143,
                "size": 1.0
            },
            "size": {
                "population": 0.06068045377170062,
                "service_own": 1.0,
                "service_other": 0.2368874941486913,
                "shops": 0.7546021596108856
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
                "parking_cost_errand": -0.262354727472,
                "parking_time": -0.13295314811
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
                "dist": -0.515531341887 #muista muuttaa
            },
            "attraction": {

            }
        }
    },
    "wo": {
        "car": {
            "attraction": {
                "parking_cost_errand": (-0.0782036364099, -0.0782036364099),
                "parking_time": (-0.0311546660770915, -0.0311546660770915),
            },
            "impedance": {
                "time": (-0.0311546660770915, -0.0311546660770915),
                "cost": (-0.348096827677, -0.348096827677)
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "population": 1.0,
                "service": 33.31565823579392,
                "shops": 77.92169023915858
            }
        },
        "transit": {
            "impedance": {
                "cost": (-0.348096827677, -0.348096827677),
                "time": -0.0203526044799
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "population": 1.0,
                "service": 33.31565823579392,
                "shops": 77.92169023915858
            },
            "attraction": {

            }
        },
        "bike": {
            "impedance": {
                "time": -0.0798788305886
            },
            "log": {
                "time": 0.0913316444227,
                "size": 1.0
            },
            "size": {
                "population": 1.0,
                "service": 33.31565823579392,
                "shops": 77.92169023915858
            },
            "attraction": {

            }
        },
        "walk": {
            "impedance": {
                "time": -0.0797652907079
            },
            "log": {
                "time": -0.0435382727554,
                "size": 1.0
            },
            "size": {
                "population": 1.0,
                "service": 33.31565823579392,
                "shops": 77.92169023915858
            },
            "attraction": {

            }
        }
    },
    "oo": {
        "car": {
            "attraction": {
                "parking_cost_errand": (-0.0782036364099, -0.0782036364099),
                "parking_time": (-0.0311546660770915, -0.0311546660770915),
            },
            "impedance": {
                "time": (-0.0311546660770915, -0.0311546660770915),
                "cost": (-0.348096827677, -0.348096827677)
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "population": 1.0,
                "service": 33.31565823579392,
                "shops": 77.92169023915858
            }
        },
        "transit": {
            "impedance": {
                "cost": (-0.348096827677, -0.348096827677),
                "time": -0.0203526044799
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "population": 1.0,
                "service": 33.31565823579392,
                "shops": 77.92169023915858
            },
            "attraction": {

            }
        },
        "bike": {
            "impedance": {
                "time": -0.0798788305886
            },
            "log": {
                "time": 0.0913316444227,
                "size": 1.0
            },
            "size": {
                "population": 1.0,
                "service": 33.31565823579392,
                "shops": 77.92169023915858
            },
            "attraction": {

            }
        },
        "walk": {
            "impedance": {
                "time": -0.0797652907079
            },
            "log": {
                "time": -0.0435382727554,
                "size": 1.0
            },
            "size": {
                "population": 1.0,
                "service": 33.31565823579392,
                "shops": 77.92169023915858
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
