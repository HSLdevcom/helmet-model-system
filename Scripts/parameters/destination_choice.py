
from typing import Any, Dict
import numpy as np # type: ignore
from parameters.assignment import inflation

### DESTINATION CHOICE PARAMETERS ###

# Destination choice (generated 2.9.2024)
destination_choice = {
    "hw": {
        "car": {
            "attraction": {
                "parking_cost_work": (-0.278231553942, -0.278231553942),
                "parking_time": (-0.020975509369828237, -0.020975509369828237)
            },
            "impedance": {
                "time": (-0.020975509369828237, -0.020975509369828237),
                "cost": (-0.129124555969, -0.129124555969)
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "workplaces": 1.0,
                "shops": 0.5418333456894562
            }
        },
        "transit": {
            "impedance": {
                "cost": (-0.129124555969, -0.129124555969),
                "time": -0.0175690167046
            },
            "attraction": {
                "parking_cost_work": (0.100195339485, 0.100195339485)
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "workplaces": 1.0,
                "shops": 0.5418333456894562
            }
        },
        "bike": {
            "impedance": {
                "time": -0.0330477082888
            },
            "log": {
                "time": -0.0361888343987,
                "size": 1.0
            },
            "size": {
                "workplaces": 1.0,
                "shops": 0.5418333456894562
            },
            "attraction": {

            }
        },
        "walk": {
            "impedance": {
                "time": -0.0462815495025
            },
            "log": {
                "time": -0.141930373321,
                "size": 1.0
            },
            "size": {
                "workplaces": 1.0,
                "shops": 0.5418333456894562
            },
            "attraction": {

            }
        },
        "park_and_ride": {
            "impedance": {
                "utility": 0.38302005942
            },
            "attraction": {
                "parking_cost_work": (0.783131510546, 0.783131510546)
            },
            "utility": {
                "facility": {
                    "shops": 1e-05,
                    "cost": -0.129124555969,
                    "time": -0.020975509369828237
                },
                "car_impedance": {
                    "time": -0.020975509369828237,
                    "cost": -0.129124555969
                },
                "transit_impedance": {
                    "time": -0.0175690167046,
                    "cost": -0.129124555969
                }
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "workplaces": 1.0,
                "shops": 0.5418333456894562
            }
        }
    },
    "hc": {
        "car": {
            "impedance": {
                "time": (-0.0436891678367, -0.0436891678367)
            },
            "attraction": {
                "parking_time": (-0.0436891678367, -0.0436891678367)
            },
            "log": {
                "transform": -2.01788365016,
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
                "comprehensive_schools_other": 0.14011214402712113,
                "secondary_schools": 0.20993491000856285
            }
        },
        "transit": {
            "log": {
                "transform": -2.01788365016,
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
                "time": -0.0243580865251
            },
            "size": {
                "comprehensive_schools_own": 1.0,
                "comprehensive_schools_other": 0.14011214402712113,
                "secondary_schools": 0.20993491000856285
            },
            "attraction": {

            }
        },
        "bike": {
            "impedance": {
                "time": -0.104945457215
            },
            "log": {
                "time": 0.638009950042,
                "size": 1.0
            },
            "size": {
                "comprehensive_schools_own": 1.0,
                "comprehensive_schools_other": 0.14011214402712113,
                "secondary_schools": 0.20993491000856285
            },
            "attraction": {

            }
        },
        "walk": {
            "impedance": {
                "time": -0.120483800354
            },
            "log": {
                "time": 0.403438161412,
                "size": 1.0
            },
            "size": {
                "comprehensive_schools_own": 1.0,
                "comprehensive_schools_other": 0.14011214402712113,
                "secondary_schools": 0.20993491000856285
            },
            "attraction": {

            }
        }
    },
    "hu": {
        "car": {
            "attraction": {
                "parking_cost_work": (-1.68164418967, -1.68164418967),
                "parking_time": (-0.039357120832038454, -0.039357120832038454)
            },
            "impedance": {
                "time": (-0.039357120832038454, -0.039357120832038454),
                "cost": (-0.242281160474, -0.242281160474)
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "secondary_schools": 1.0,
                "tertiary_education": 2.6516052989545162
            }
        },
        "transit": {
            "impedance": {
                "cost": (-0.242281160474, -0.242281160474),
                "time": -0.0203906223539
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "secondary_schools": 1.0,
                "tertiary_education": 2.6516052989545162
            },
            "attraction": {

            }
        },
        "bike": {
            "impedance": {
                "time": -0.0716413456305
            },
            "log": {
                "time": 0.447914387278,
                "size": 1.0
            },
            "size": {
                "secondary_schools": 1.0,
                "tertiary_education": 2.6516052989545162
            },
            "attraction": {

            }
        },
        "walk": {
            "impedance": {
                "time": -0.0812456642316
            },
            "log": {
                "time": 0.188011252624,
                "size": 1.0
            },
            "size": {
                "secondary_schools": 1.0,
                "tertiary_education": 2.6516052989545162
            },
            "attraction": {

            }
        }
    },
    "hs": {
        "car": {
            "attraction": {
                "parking_cost_errand": (-0.0770066560025, -0.0770066560025),
                "parking_time": (-0.05137152460901073, -0.05137152460901073)
            },
            "impedance": {
                "time": (-0.05137152460901073, -0.05137152460901073),
                "cost": (-0.466738060319, -0.466738060319)
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "population": 1.0,
                "service_own": 49.95074692369058,
                "service_other": 19.647897964374852,
                "shops": 249.6273069036269
            }
        },
        "transit": {
            "impedance": {
                "cost": (-0.466738060319, -0.466738060319),
                "time": -0.0330789791993
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "population": 1.0,
                "service_own": 49.95074692369058,
                "service_other": 19.647897964374852,
                "shops": 249.6273069036269
            },
            "attraction": {

            }
        },
        "bike": {
            "impedance": {
                "time": -0.0864522492141
            },
            "log": {
                "time": 0.206355682608,
                "size": 1.0
            },
            "size": {
                "population": 1.0,
                "service_own": 49.95074692369058,
                "service_other": 19.647897964374852,
                "shops": 249.6273069036269
            },
            "attraction": {

            }
        },
        "walk": {
            "impedance": {
                "time": -0.0854683762686
            },
            "log": {
                "time": 0.14444795316,
                "size": 1.0
            },
            "size": {
                "population": 1.0,
                "service_own": 49.95074692369058,
                "service_other": 19.647897964374852,
                "shops": 249.6273069036269
            },
            "attraction": {

            }
        }
    },
    "ho": {
        "car": {
            "attraction": {
                "parking_cost_errand": (-0.165309184076, -0.165309184076),
                "parking_time": (-0.02601268115951978, -0.02601268115951978)
            },
            "impedance": {
                "time": (-0.02601268115951978, -0.02601268115951978),
                "cost": (-0.236339264612, -0.236339264612)
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "population": 0.06205347835935405,
                "service_own": 1.0,
                "service_other": 0.2545138901215862,
                "shops": 0.7484164086187722
            }
        },
        "transit": {
            "impedance": {
                "cost": (-0.236339264612, -0.236339264612),
                "time": -0.0206557959942
            },
            "attraction": {
                "cbd": 0.933456025763,
                "own_zone": -7.60448078069
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "population": 0.06205347835935405,
                "service_own": 1.0,
                "service_other": 0.2545138901215862,
                "shops": 0.7484164086187722
            }
        },
        "bike": {
            "impedance": {
                "time": -0.090511336822
            },
            "log": {
                "time": 0.604754882244,
                "size": 1.0
            },
            "size": {
                "population": 0.06205347835935405,
                "service_own": 1.0,
                "service_other": 0.2545138901215862,
                "shops": 0.7484164086187722
            },
            "attraction": {

            }
        },
        "walk": {
            "impedance": {
                "time": -0.0611169195239
            },
            "log": {
                "time": 0.0524902829028,
                "size": 1.0
            },
            "size": {
                "population": 0.06205347835935405,
                "service_own": 1.0,
                "service_other": 0.2545138901215862,
                "shops": 0.7484164086187722
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
                "service": 7.704376081743273,
                "shops": 19.64553176963933
            },
            "impedance": {
                "time": -0.158716055655
            },
            "attraction": {
                "parking_cost_errand": -0.073889435641
            }
        },
        "transit": {
            "log": {
                "size": 1.0
            },
            "size": {
                "population": 1.0,
                "service": 3.282631049223,
                "shops": 27.79741333933
            },
            "impedance": {
                "time": -0.0634374771047
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
                "service": 3.82060772393,
                "shops": 17.872812116
            },
            "impedance": {
                "time": -0.129277012255
            },
            "attraction": {

            }
        }
    },
    "wo": {
        "car": {
            "attraction": {
                "parking_cost_errand": (-0.0509793838484, -0.0509793838484),
                "parking_time": (-0.03559410675476322, -0.03559410675476322)
            },
            "impedance": {
                "time": (-0.03559410675476322, -0.03559410675476322),
                "cost": (-0.323391693588, -0.323391693588)
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "population": 1.0,
                "service": 33.08024026139248,
                "shops": 76.47502259018555
            }
        },
        "transit": {
            "impedance": {
                "cost": (-0.323391693588, -0.323391693588),
                "time": -0.0205685127175
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "population": 1.0,
                "service": 33.08024026139248,
                "shops": 76.47502259018555
            },
            "attraction": {

            }
        },
        "bike": {
            "impedance": {
                "time": -0.0843087483172
            },
            "log": {
                "time": 0.0532546396989,
                "size": 1.0
            },
            "size": {
                "population": 1.0,
                "service": 33.08024026139248,
                "shops": 76.47502259018555
            },
            "attraction": {

            }
        },
        "walk": {
            "impedance": {
                "time": -0.0822164156483
            },
            "log": {
                "time": -0.0421949188698,
                "size": 1.0
            },
            "size": {
                "population": 1.0,
                "service": 33.08024026139248,
                "shops": 76.47502259018555
            },
            "attraction": {

            }
        }
    },
    "oo": {
        "car": {
            "attraction": {
                "parking_cost_errand": (-0.0509793838484, -0.0509793838484),
                "parking_time": (-0.03559410675476322, -0.03559410675476322)
            },
            "impedance": {
                "time": (-0.03559410675476322, -0.03559410675476322),
                "cost": (-0.323391693588, -0.323391693588)
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "population": 1.0,
                "service": 33.08024026139248,
                "shops": 76.47502259018555
            }
        },
        "transit": {
            "impedance": {
                "cost": (-0.323391693588, -0.323391693588),
                "time": -0.0205685127175
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "population": 1.0,
                "service": 33.08024026139248,
                "shops": 76.47502259018555
            },
            "attraction": {

            }
        },
        "bike": {
            "impedance": {
                "time": -0.0843087483172
            },
            "log": {
                "time": 0.0532546396989,
                "size": 1.0
            },
            "size": {
                "population": 1.0,
                "service": 33.08024026139248,
                "shops": 76.47502259018555
            },
            "attraction": {

            }
        },
        "walk": {
            "impedance": {
                "time": -0.0822164156483
            },
            "log": {
                "time": -0.0421949188698,
                "size": 1.0
            },
            "size": {
                "population": 1.0,
                "service": 33.08024026139248,
                "shops": 76.47502259018555
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
