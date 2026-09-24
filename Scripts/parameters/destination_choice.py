
from typing import Any, Dict
import numpy as np # type: ignore
from parameters.assignment import inflation

### DESTINATION CHOICE PARAMETERS ###

# Destination choice (generated 2.9.2024)
destination_choice = {
    "hw": {
        "car": {
            "attraction": {
                "parking_cost_work": (-0.284852026741, -0.284852026741),
                "parking_time": (-0.021164645171639185, -0.021164645171639185)
            },
            "impedance": {
                "time": (-0.021164645171639185, -0.021164645171639185),
                "cost": (-0.130288869836, -0.130288869836)
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "workplaces": 1.0,
                "shops": 0.5548766826193385
            }
        },
        "transit": {
            "impedance": {
                "cost": (-0.130288869836, -0.130288869836),
                "time": -0.0176324850096
            },
            "attraction": {
                "parking_cost_work": (0.101400599232, 0.101400599232)
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "workplaces": 1.0,
                "shops": 0.5548766826193385
            }
        },
        "bike": {
            "impedance": {
                "time": -0.03438480715
            },
            "log": {
                "time": -0.0909501610082,
                "size": 1.0
            },
            "size": {
                "workplaces": 1.0,
                "shops": 0.5548766826193385
            },
            "attraction": {

            }
        },
        "walk": {
            "impedance": {
                "time": -0.044940097597
            },
            "log": {
                "time": -0.143513965467,
                "size": 1.0
            },
            "size": {
                "workplaces": 1.0,
                "shops": 0.5548766826193385
            },
            "attraction": {

            }
        },
        "park_and_ride": {
            "impedance": {
                "utility": 0.394120756734
            },
            "attraction": {
                "parking_cost_work": (0.778169160866, 0.778169160866)
            },
            "utility": {
                "facility": {
                    "shops": 1e-05,
                    "cost": -0.130288869836,
                    "time": -0.021164645171639185
                },
                "car_impedance": {
                    "time": -0.021164645171639185,
                    "cost": -0.130288869836
                },
                "transit_impedance": {
                    "time": -0.0176324850096,
                    "cost": -0.130288869836
                }
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "workplaces": 1.0,
                "shops": 0.5548766826193385
            }
        }
    },
    "hc": {
        "car": {
            "impedance": {
                "time": (-0.0457143923272, -0.0457143923272)
            },
            "attraction": {
                "parking_time": (-0.0457143923272, -0.0457143923272)
            },
            "log": {
                "transform": -1.99956530868,
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
                "comprehensive_schools_other": 0.14480881109908683,
                "secondary_schools": 0.22329503253819646
            }
        },
        "transit": {
            "log": {
                "transform": -1.99956530868,
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
                "time": -0.0244547072548
            },
            "size": {
                "comprehensive_schools_own": 1.0,
                "comprehensive_schools_other": 0.14480881109908683,
                "secondary_schools": 0.22329503253819646
            },
            "attraction": {

            }
        },
        "bike": {
            "impedance": {
                "time": -0.13868222231
            },
            "log": {
                "time": 0.629945786121,
                "size": 1.0
            },
            "size": {
                "comprehensive_schools_own": 1.0,
                "comprehensive_schools_other": 0.14480881109908683,
                "secondary_schools": 0.22329503253819646
            },
            "attraction": {

            }
        },
        "walk": {
            "impedance": {
                "time": -0.115995883348
            },
            "log": {
                "time": 0.39343674512,
                "size": 1.0
            },
            "size": {
                "comprehensive_schools_own": 1.0,
                "comprehensive_schools_other": 0.14480881109908683,
                "secondary_schools": 0.22329503253819646
            },
            "attraction": {

            }
        }
    },
    "hu": {
        "car": {
            "attraction": {
                "parking_cost_work": (-1.6859115896, -1.6859115896),
                "parking_time": (-0.03944236199890674, -0.03944236199890674)
            },
            "impedance": {
                "time": (-0.03944236199890674, -0.03944236199890674),
                "cost": (-0.242805902335, -0.242805902335)
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "secondary_schools": 1.0,
                "tertiary_education": 2.653799609577752
            }
        },
        "transit": {
            "impedance": {
                "cost": (-0.242805902335, -0.242805902335),
                "time": -0.0205523700063
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "secondary_schools": 1.0,
                "tertiary_education": 2.653799609577752
            },
            "attraction": {

            }
        },
        "bike": {
            "impedance": {
                "time": -0.0844734736891
            },
            "log": {
                "time": 0.452493795503,
                "size": 1.0
            },
            "size": {
                "secondary_schools": 1.0,
                "tertiary_education": 2.653799609577752
            },
            "attraction": {

            }
        },
        "walk": {
            "impedance": {
                "time": -0.0789571790404
            },
            "log": {
                "time": 0.190830622249,
                "size": 1.0
            },
            "size": {
                "secondary_schools": 1.0,
                "tertiary_education": 2.653799609577752
            },
            "attraction": {

            }
        }
    },
    "hs": {
        "car": {
            "attraction": {
                "parking_cost_errand": (-0.0808198585975, -0.0808198585975),
                "parking_time": (-0.051732987593925764, -0.051732987593925764)
            },
            "impedance": {
                "time": (-0.051732987593925764, -0.051732987593925764),
                "cost": (-0.470022146858, -0.470022146858)
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "population": 1.0,
                "service_own": 49.41714991215556,
                "service_other": 19.639072057133703,
                "shops": 249.7403903022187
            }
        },
        "transit": {
            "impedance": {
                "cost": (-0.470022146858, -0.470022146858),
                "time": -0.033275915084
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "population": 1.0,
                "service_own": 49.41714991215556,
                "service_other": 19.639072057133703,
                "shops": 249.7403903022187
            },
            "attraction": {

            }
        },
        "bike": {
            "impedance": {
                "time": -0.0936374441636
            },
            "log": {
                "time": 0.0249342964053,
                "size": 1.0
            },
            "size": {
                "population": 1.0,
                "service_own": 49.41714991215556,
                "service_other": 19.639072057133703,
                "shops": 249.7403903022187
            },
            "attraction": {

            }
        },
        "walk": {
            "impedance": {
                "time": -0.0831464376489
            },
            "log": {
                "time": 0.142633970132,
                "size": 1.0
            },
            "size": {
                "population": 1.0,
                "service_own": 49.41714991215556,
                "service_other": 19.639072057133703,
                "shops": 249.7403903022187
            },
            "attraction": {

            }
        }
    },
    "ho": {
        "car": {
            "attraction": {
                "parking_cost_errand": (-0.168081081197, -0.168081081197),
                "parking_time": (-0.02596790133952375, -0.02596790133952375)
            },
            "impedance": {
                "time": (-0.02596790133952375, -0.02596790133952375),
                "cost": (-0.23593241575, -0.23593241575)
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "population": 0.06103662920216613,
                "service_own": 1.0,
                "service_other": 0.2523642104269096,
                "shops": 0.7474147811140331
            }
        },
        "transit": {
            "impedance": {
                "cost": (-0.23593241575, -0.23593241575),
                "time": -0.0208631077196
            },
            "attraction": {
                "cbd": 0.926924806307,
                "own_zone": -7.34063679206
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "population": 0.06103662920216613,
                "service_own": 1.0,
                "service_other": 0.2523642104269096,
                "shops": 0.7474147811140331
            }
        },
        "bike": {
            "impedance": {
                "time": -0.105194148045
            },
            "log": {
                "time": 0.498610524766,
                "size": 1.0
            },
            "size": {
                "population": 0.06103662920216613,
                "service_own": 1.0,
                "service_other": 0.2523642104269096,
                "shops": 0.7474147811140331
            },
            "attraction": {

            }
        },
        "walk": {
            "impedance": {
                "time": -0.0597982971327
            },
            "log": {
                "time": 0.0532839952977,
                "size": 1.0
            },
            "size": {
                "population": 0.06103662920216613,
                "service_own": 1.0,
                "service_other": 0.2523642104269096,
                "shops": 0.7474147811140331
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
                "service": 7.717421705015447,
                "shops": 19.372109633994274
            },
            "impedance": {
                "time": -0.162259629378
            },
            "attraction": {
                "parking_cost_errand": -0.0676322938816
            }
        },
        "transit": {
            "log": {
                "size": 1.0
            },
            "size": {
                "population": 1.0,
                "service": 3.2858953853980735,
                "shops": 27.92631019283953
            },
            "impedance": {
                "time": -0.0637101956771
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
                "service": 4.402157168009162,
                "shops": 21.033353498229815
            },
            "impedance": {
                "time": -0.147846814095
            },
            "attraction": {

            }
        }
    },
    "wo": {
        "car": {
            "attraction": {
                "parking_cost_errand": (-0.0551686097543, -0.0551686097543),
                "parking_time": (-0.036030353590158236, -0.036030353590158236)
            },
            "impedance": {
                "time": (-0.036030353590158236, -0.036030353590158236),
                "cost": (-0.327355231819, -0.327355231819)
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "population": 1.0,
                "service": 33.370088015717435,
                "shops": 77.05218493658653
            }
        },
        "transit": {
            "impedance": {
                "cost": (-0.327355231819, -0.327355231819),
                "time": -0.0206734788846
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "population": 1.0,
                "service": 33.370088015717435,
                "shops": 77.05218493658653
            },
            "attraction": {

            }
        },
        "bike": {
            "impedance": {
                "time": -0.0859587546719
            },
            "log": {
                "time": -0.149075302012,
                "size": 1.0
            },
            "size": {
                "population": 1.0,
                "service": 33.370088015717435,
                "shops": 77.05218493658653
            },
            "attraction": {

            }
        },
        "walk": {
            "impedance": {
                "time": -0.0801543610471
            },
            "log": {
                "time": -0.0351928266517,
                "size": 1.0
            },
            "size": {
                "population": 1.0,
                "service": 33.370088015717435,
                "shops": 77.05218493658653
            },
            "attraction": {

            }
        }
    },
    "oo": {
        "car": {
            "attraction": {
                "parking_cost_errand": (-0.0551686097543, -0.0551686097543),
                "parking_time": (-0.036030353590158236, -0.036030353590158236)
            },
            "impedance": {
                "time": (-0.036030353590158236, -0.036030353590158236),
                "cost": (-0.327355231819, -0.327355231819)
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "population": 1.0,
                "service": 33.370088015717435,
                "shops": 77.05218493658653
            }
        },
        "transit": {
            "impedance": {
                "cost": (-0.327355231819, -0.327355231819),
                "time": -0.0206734788846
            },
            "log": {
                "size": 1.0
            },
            "size": {
                "population": 1.0,
                "service": 33.370088015717435,
                "shops": 77.05218493658653
            },
            "attraction": {

            }
        },
        "bike": {
            "impedance": {
                "time": -0.0859587546719
            },
            "log": {
                "time": -0.149075302012,
                "size": 1.0
            },
            "size": {
                "population": 1.0,
                "service": 33.370088015717435,
                "shops": 77.05218493658653
            },
            "attraction": {

            }
        },
        "walk": {
            "impedance": {
                "time": -0.0801543610471
            },
            "log": {
                "time": -0.0351928266517,
                "size": 1.0
            },
            "size": {
                "population": 1.0,
                "service": 33.370088015717435,
                "shops": 77.05218493658653
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
