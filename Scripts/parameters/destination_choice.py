
from typing import Any, Dict
import numpy as np # type: ignore
from parameters.assignment import inflation

### DESTINATION CHOICE PARAMETERS ###

# Destination choice (generated 2.9.2024)
destination_choice = {
    "hw": {
        "car": {
            "attraction": {
                "parking_cost_work": (-0.285023839582, -0.285023839582),
                "parking_time": (-0.02115590561523804, -0.02115590561523804)
            },
            "impedance": {
                "time": (-0.02115590561523804, -0.02115590561523804),
                "cost": (-0.13023506941, -0.13023506941)
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "workplaces": 1.0,
                "shops": 0.5534880822318661
            }
        },
        "transit": {
            "impedance": {
                "cost": (-0.13023506941, -0.13023506941),
                "time": -0.0175895053671
            },
            "attraction": {
                "parking_cost_work": (0.102034422069, 0.102034422069)
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "workplaces": 1.0,
                "shops": 0.5534880822318661
            }
        },
        "bike": {
            "impedance": {
                "time": -0.0343718987488
            },
            "log": {
                "time": -0.091425785374,
                "size": 1.0
            },
            "size": {
                "workplaces": 1.0,
                "shops": 0.5534880822318661
            },
            "attraction": {

            }
        },
        "walk": {
            "impedance": {
                "time": -0.0449391361826
            },
            "log": {
                "time": -0.143557319072,
                "size": 1.0
            },
            "size": {
                "workplaces": 1.0,
                "shops": 0.5534880822318661
            },
            "attraction": {

            }
        },
        "park_and_ride": {
            "impedance": {
                "utility": 0.38801488403
            },
            "attraction": {
                "parking_cost_work": (0.779594981691, 0.779594981691)
            },
            "utility": {
                "facility": {
                    "shops": 1e-05,
                    "cost": -0.13023506941,
                    "time": -0.02115590561523804
                },
                "car_impedance": {
                    "time": -0.02115590561523804,
                    "cost": -0.13023506941
                },
                "transit_impedance": {
                    "time": -0.0175895053671,
                    "cost": -0.13023506941
                }
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "workplaces": 1.0,
                "shops": 0.5534880822318661
            }
        }
    },
    "hc": {
        "car": {
            "impedance": {
                "time": (-0.0460166680561, -0.0460166680561)
            },
            "attraction": {
                "parking_time": (-0.0460166680561, -0.0460166680561)
            },
            "log": {
                "transform": -1.99145523095,
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
                "comprehensive_schools_other": 0.14491950292166725,
                "secondary_schools": 0.22376970548462705
            }
        },
        "transit": {
            "log": {
                "transform": -1.99145523095,
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
                "time": -0.0244079189784
            },
            "size": {
                "comprehensive_schools_own": 1.0,
                "comprehensive_schools_other": 0.14491950292166725,
                "secondary_schools": 0.22376970548462705
            },
            "attraction": {

            }
        },
        "bike": {
            "impedance": {
                "time": -0.138376410409
            },
            "log": {
                "time": 0.628177986692,
                "size": 1.0
            },
            "size": {
                "comprehensive_schools_own": 1.0,
                "comprehensive_schools_other": 0.14491950292166725,
                "secondary_schools": 0.22376970548462705
            },
            "attraction": {

            }
        },
        "walk": {
            "impedance": {
                "time": -0.115989177993
            },
            "log": {
                "time": 0.393377145085,
                "size": 1.0
            },
            "size": {
                "comprehensive_schools_own": 1.0,
                "comprehensive_schools_other": 0.14491950292166725,
                "secondary_schools": 0.22376970548462705
            },
            "attraction": {

            }
        }
    },
    "hu": {
        "car": {
            "attraction": {
                "parking_cost_work": (-1.68637278785, -1.68637278785),
                "parking_time": (-0.039416559116654835, -0.039416559116654835)
            },
            "impedance": {
                "time": (-0.039416559116654835, -0.039416559116654835),
                "cost": (-0.242647060628, -0.242647060628)
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "secondary_schools": 1.0,
                "tertiary_education": 2.654845521142443
            }
        },
        "transit": {
            "impedance": {
                "cost": (-0.242647060628, -0.242647060628),
                "time": -0.020503666466
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "secondary_schools": 1.0,
                "tertiary_education": 2.654845521142443
            },
            "attraction": {

            }
        },
        "bike": {
            "impedance": {
                "time": -0.0845718067303
            },
            "log": {
                "time": 0.453924772672,
                "size": 1.0
            },
            "size": {
                "secondary_schools": 1.0,
                "tertiary_education": 2.654845521142443
            },
            "attraction": {

            }
        },
        "walk": {
            "impedance": {
                "time": -0.0789812894366
            },
            "log": {
                "time": 0.191132499065,
                "size": 1.0
            },
            "size": {
                "secondary_schools": 1.0,
                "tertiary_education": 2.654845521142443
            },
            "attraction": {

            }
        }
    },
    "hs": {
        "car": {
            "attraction": {
                "parking_cost_errand": (-0.0811436158097, -0.0811436158097),
                "parking_time": (-0.05170409054471081, -0.05170409054471081)
            },
            "impedance": {
                "time": (-0.05170409054471081, -0.05170409054471081),
                "cost": (-0.469759601551, -0.469759601551)
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "population": 1.0,
                "service_own": 49.43027733279195,
                "service_other": 19.658490451507053,
                "shops": 249.82391367136293
            }
        },
        "transit": {
            "impedance": {
                "cost": (-0.469759601551, -0.469759601551),
                "time": -0.0332336840796
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "population": 1.0,
                "service_own": 49.43027733279195,
                "service_other": 19.658490451507053,
                "shops": 249.82391367136293
            },
            "attraction": {

            }
        },
        "bike": {
            "impedance": {
                "time": -0.0936194384101
            },
            "log": {
                "time": 0.0256104267537,
                "size": 1.0
            },
            "size": {
                "population": 1.0,
                "service_own": 49.43027733279195,
                "service_other": 19.658490451507053,
                "shops": 249.82391367136293
            },
            "attraction": {

            }
        },
        "walk": {
            "impedance": {
                "time": -0.0831454459767
            },
            "log": {
                "time": 0.142616881777,
                "size": 1.0
            },
            "size": {
                "population": 1.0,
                "service_own": 49.43027733279195,
                "service_other": 19.658490451507053,
                "shops": 249.82391367136293
            },
            "attraction": {

            }
        }
    },
    "ho": {
        "car": {
            "attraction": {
                "parking_cost_errand": (-0.168233007816, -0.168233007816),
                "parking_time": (-0.025962573469626243, -0.025962573469626243)
            },
            "impedance": {
                "time": (-0.025962573469626243, -0.025962573469626243),
                "cost": (-0.235884009173, -0.235884009173)
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "population": 0.06106240578485677,
                "service_own": 1.0,
                "service_other": 0.2526280565026863,
                "shops": 0.7476902015082432
            }
        },
        "transit": {
            "impedance": {
                "cost": (-0.235884009173, -0.235884009173),
                "time": -0.0208544790981
            },
            "attraction": {
                "cbd": 0.9271060748,
                "own_zone": -7.33711383503
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "population": 0.06106240578485677,
                "service_own": 1.0,
                "service_other": 0.2526280565026863,
                "shops": 0.7476902015082432
            }
        },
        "bike": {
            "impedance": {
                "time": -0.105171849179
            },
            "log": {
                "time": 0.498755919283,
                "size": 1.0
            },
            "size": {
                "population": 0.06106240578485677,
                "service_own": 1.0,
                "service_other": 0.2526280565026863,
                "shops": 0.7476902015082432
            },
            "attraction": {

            }
        },
        "walk": {
            "impedance": {
                "time": -0.0597987279909
            },
            "log": {
                "time": 0.0532971756078,
                "size": 1.0
            },
            "size": {
                "population": 0.06106240578485677,
                "service_own": 1.0,
                "service_other": 0.2526280565026863,
                "shops": 0.7476902015082432
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
                "service": 7.723525025862965,
                "shops": 19.378827844819217
            },
            "impedance": {
                "time": -0.162180028912
            },
            "attraction": {
                "parking_cost_errand": -0.0686102614231
            }
        },
        "transit": {
            "log": {
                "size": 1.0
            },
            "size": {
                "population": 1.0,
                "service": 3.287116843152361,
                "shops": 27.946066573648146
            },
            "impedance": {
                "time": -0.06362512335
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
                "service": 4.421274451713132,
                "shops": 21.045811318433785
            },
            "impedance": {
                "time": -0.147692214145
            },
            "attraction": {

            }
        }
    },
    "wo": {
        "car": {
            "attraction": {
                "parking_cost_errand": (-0.0556175386504, -0.0556175386504),
                "parking_time": (-0.03601082165986907, -0.03601082165986907)
            },
            "impedance": {
                "time": (-0.03601082165986907, -0.03601082165986907),
                "cost": (-0.327177773678, -0.327177773678)
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "population": 1.0,
                "service": 33.37778946855477,
                "shops": 77.06906579010413
            }
        },
        "transit": {
            "impedance": {
                "cost": (-0.327177773678, -0.327177773678),
                "time": -0.0206635299669
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "population": 1.0,
                "service": 33.37778946855477,
                "shops": 77.06906579010413
            },
            "attraction": {

            }
        },
        "bike": {
            "impedance": {
                "time": -0.085984487806
            },
            "log": {
                "time": -0.148717366459,
                "size": 1.0
            },
            "size": {
                "population": 1.0,
                "service": 33.37778946855477,
                "shops": 77.06906579010413
            },
            "attraction": {

            }
        },
        "walk": {
            "impedance": {
                "time": -0.0801623290472
            },
            "log": {
                "time": -0.0350855573743,
                "size": 1.0
            },
            "size": {
                "population": 1.0,
                "service": 33.37778946855477,
                "shops": 77.06906579010413
            },
            "attraction": {

            }
        }
    },
    "oo": {
        "car": {
            "attraction": {
                "parking_cost_errand": (-0.0556175386504, -0.0556175386504),
                "parking_time": (-0.03601082165986907, -0.03601082165986907)
            },
            "impedance": {
                "time": (-0.03601082165986907, -0.03601082165986907),
                "cost": (-0.327177773678, -0.327177773678)
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "population": 1.0,
                "service": 33.37778946855477,
                "shops": 77.06906579010413
            }
        },
        "transit": {
            "impedance": {
                "cost": (-0.327177773678, -0.327177773678),
                "time": -0.0206635299669
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "population": 1.0,
                "service": 33.37778946855477,
                "shops": 77.06906579010413
            },
            "attraction": {

            }
        },
        "bike": {
            "impedance": {
                "time": -0.085984487806
            },
            "log": {
                "time": -0.148717366459,
                "size": 1.0
            },
            "size": {
                "population": 1.0,
                "service": 33.37778946855477,
                "shops": 77.06906579010413
            },
            "attraction": {

            }
        },
        "walk": {
            "impedance": {
                "time": -0.0801623290472
            },
            "log": {
                "time": -0.0350855573743,
                "size": 1.0
            },
            "size": {
                "population": 1.0,
                "service": 33.37778946855477,
                "shops": 77.06906579010413
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
