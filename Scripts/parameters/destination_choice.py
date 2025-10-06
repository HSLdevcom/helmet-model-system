
from typing import Any, Dict
import numpy as np # type: ignore
from parameters.assignment import inflation

### DESTINATION CHOICE PARAMETERS ###

# Destination choice (generated 2.9.2024)
destination_choice = {
    "hw": {
        "car": {
            "attraction": {
                "parking_cost_work": (-0.288752653394, -0.288752653394),
                "parking_time": (-0.018629675025852, -0.018629675025852)
            },
            "impedance": {
                "time": (-0.018629675025852, -0.018629675025852),
                "cost": (-0.141133901711, -0.141133901711)
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "workplaces": 1.0,
                "shops": 0.5582370648273897
            }
        },
        "transit": {
            "impedance": {
                "cost": (-0.141133901711, -0.141133901711),
                "time": -0.0174288204949
            },
            "attraction": {
                "parking_cost_work": (0.101201118297, 0.101201118297)
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "workplaces": 1.0,
                "shops": 0.5582370648273897
            }
        },
        "bike": {
            "impedance": {
                "time": -0.0330298672578
            },
            "log": {
                "time": -0.0358459651185,
                "size": 1.0
            },
            "size": {
                "workplaces": 1.0,
                "shops": 0.5582370648273897
            },
            "attraction": {

            }
        },
        "walk": {
            "impedance": {
                "time": -0.0462548328277
            },
            "log": {
                "time": -0.142199656954,
                "size": 1.0
            },
            "size": {
                "workplaces": 1.0,
                "shops": 0.5582370648273897
            },
            "attraction": {

            }
        },
        "park_and_ride": {
            "impedance": {
                "utility": 0.387528886482
            },
            "attraction": {
                "parking_cost_work": (0.782424889817, 0.782424889817)
            },
            "utility": {
                "facility": {
                    "shops": 1e-05,
                    "cost": -0.141133901711,
                    "time": -0.018629675025852
                },
                "car_impedance": {
                    "time": -0.018629675025852,
                    "cost": -0.141133901711
                },
                "transit_impedance": {
                    "time": -0.0174288204949,
                    "cost": -0.141133901711
                }
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "workplaces": 1.0,
                "shops": 0.5582370648273897
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
                "parking_cost_work": (-1.69427537431, -1.69427537431),
                "parking_time": (-0.035047152924696, -0.035047152924696)
            },
            "impedance": {
                "time": (-0.035047152924696, -0.035047152924696),
                "cost": (-0.265508734278, -0.265508734278)
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "secondary_schools": 1.0,
                "tertiary_education": 2.652495668858298
            }
        },
        "transit": {
            "impedance": {
                "cost": (-0.265508734278, -0.265508734278),
                "time": -0.0202012441483
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "secondary_schools": 1.0,
                "tertiary_education": 2.652495668858298
            },
            "attraction": {

            }
        },
        "bike": {
            "impedance": {
                "time": -0.0715871345112
            },
            "log": {
                "time": 0.448669496214,
                "size": 1.0
            },
            "size": {
                "secondary_schools": 1.0,
                "tertiary_education": 2.652495668858298
            },
            "attraction": {

            }
        },
        "walk": {
            "impedance": {
                "time": -0.0811752940354
            },
            "log": {
                "time": 0.187849858687,
                "size": 1.0
            },
            "size": {
                "secondary_schools": 1.0,
                "tertiary_education": 2.652495668858298
            },
            "attraction": {

            }
        }
    },
    "hs": {
        "car": {
            "attraction": {
                "parking_cost_errand": (-0.096801882885, -0.096801882885),
                "parking_time": (-0.045295238672258, -0.045295238672258)
            },
            "impedance": {
                "time": (-0.045295238672258, -0.045295238672258),
                "cost": (-0.506092052204, -0.506092052204)
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "population": 1.0,
                "service_own": 49.433105793421106,
                "service_other": 19.42602949160159,
                "shops": 249.84196405371978
            }
        },
        "transit": {
            "impedance": {
                "cost": (-0.506092052204, -0.506092052204),
                "time": -0.0329692070175
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "population": 1.0,
                "service_own": 49.433105793421106,
                "service_other": 19.42602949160159,
                "shops": 249.84196405371978
            },
            "attraction": {

            }
        },
        "bike": {
            "impedance": {
                "time": -0.0865044403503
            },
            "log": {
                "time": 0.207075305599,
                "size": 1.0
            },
            "size": {
                "population": 1.0,
                "service_own": 49.433105793421106,
                "service_other": 19.42602949160159,
                "shops": 249.84196405371978
            },
            "attraction": {

            }
        },
        "walk": {
            "impedance": {
                "time": -0.0855099742944
            },
            "log": {
                "time": 0.144427276387,
                "size": 1.0
            },
            "size": {
                "population": 1.0,
                "service_own": 49.433105793421106,
                "service_other": 19.42602949160159,
                "shops": 249.84196405371978
            },
            "attraction": {

            }
        }
    },
    "ho": {
        "car": {
            "attraction": {
                "parking_cost_errand": (-0.175762277122, -0.175762277122),
                "parking_time": (-0.0226187764885855, -0.0226187764885855)
            },
            "impedance": {
                "time": (-0.0226187764885855, -0.0226187764885855),
                "cost": (-0.252723759649, -0.252723759649)
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "population": 0.06178629404761088,
                "service_own": 1.0,
                "service_other": 0.25013674926456225,
                "shops": 0.7507158498647125
            }
        },
        "transit": {
            "impedance": {
                "cost": (-0.252723759649, -0.252723759649),
                "time": -0.0204911367486
            },
            "attraction": {
                "cbd": 0.940008968658,
                "own_zone": -7.6270948289
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "population": 0.06178629404761088,
                "service_own": 1.0,
                "service_other": 0.25013674926456225,
                "shops": 0.7507158498647125
            }
        },
        "bike": {
            "impedance": {
                "time": -0.0904982419314
            },
            "log": {
                "time": 0.604743982149,
                "size": 1.0
            },
            "size": {
                "population": 0.06178629404761088,
                "service_own": 1.0,
                "service_other": 0.25013674926456225,
                "shops": 0.7507158498647125
            },
            "attraction": {

            }
        },
        "walk": {
            "impedance": {
                "time": -0.0611096438303
            },
            "log": {
                "time": 0.0522535919018,
                "size": 1.0
            },
            "size": {
                "population": 0.06178629404761088,
                "service_own": 1.0,
                "service_other": 0.25013674926456225,
                "shops": 0.7507158498647125
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
                "service": 5.670055505151,
                "shops": 20.96384501204548
            },
            "impedance": {
                "time": -0.15513256375
            },
            "attraction": {
                "parking_cost_errand": -0.345084858291,
                "parking_time": -.15513256375
            }
        },
        "transit": {
            "log": {
                "size": 1.0
            },
            "size": {
                "population": 1.0,
                "service": 5.670055505151,
                "shops": 20.96384501204548
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
                "service": 5.670055505151,
                "shops": 20.96384501204548
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
                "parking_cost_errand": (-0.0682403475763, -0.0682403475763),
                "parking_time": (-0.0315001970160305, -0.0315001970160305)
            },
            "impedance": {
                "time": (-0.0315001970160305, -0.0315001970160305),
                "cost": (-0.351957508559, -0.351957508559)
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "population": 1.0,
                "service": 33.08583955728218,
                "shops": 77.0417847786292
            }
        },
        "transit": {
            "impedance": {
                "cost": (-0.351957508559, -0.351957508559),
                "time": -0.0203649024264
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "population": 1.0,
                "service": 33.08583955728218,
                "shops": 77.0417847786292
            },
            "attraction": {

            }
        },
        "bike": {
            "impedance": {
                "time": -0.0847534716462
            },
            "log": {
                "time": 0.061519136933,
                "size": 1.0
            },
            "size": {
                "population": 1.0,
                "service": 33.08583955728218,
                "shops": 77.0417847786292
            },
            "attraction": {

            }
        },
        "walk": {
            "impedance": {
                "time": -0.0822055863127
            },
            "log": {
                "time": -0.0429673272687,
                "size": 1.0
            },
            "size": {
                "population": 1.0,
                "service": 33.08583955728218,
                "shops": 77.0417847786292
            },
            "attraction": {

            }
        }
    },
    "oo": {
        "car": {
            "attraction": {
                "parking_cost_errand": (-0.0682403475763, -0.0682403475763),
                "parking_time": (-0.0315001970160305, -0.0315001970160305)
            },
            "impedance": {
                "time": (-0.0315001970160305, -0.0315001970160305),
                "cost": (-0.351957508559, -0.351957508559)
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "population": 1.0,
                "service": 33.08583955728218,
                "shops": 77.0417847786292
            }
        },
        "transit": {
            "impedance": {
                "cost": (-0.351957508559, -0.351957508559),
                "time": -0.0203649024264
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "population": 1.0,
                "service": 33.08583955728218,
                "shops": 77.0417847786292
            },
            "attraction": {

            }
        },
        "bike": {
            "impedance": {
                "time": -0.0847534716462
            },
            "log": {
                "time": 0.061519136933,
                "size": 1.0
            },
            "size": {
                "population": 1.0,
                "service": 33.08583955728218,
                "shops": 77.0417847786292
            },
            "attraction": {

            }
        },
        "walk": {
            "impedance": {
                "time": -0.0822055863127
            },
            "log": {
                "time": -0.0429673272687,
                "size": 1.0
            },
            "size": {
                "population": 1.0,
                "service": 33.08583955728218,
                "shops": 77.0417847786292
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
