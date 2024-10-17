from typing import Any, Dict
import numpy # type: ignore


### DESTINATION CHOICE PARAMETERS ###

# Destination choice (calibrated 02.10.2020)
destination_choice: Dict[str, Dict[str, Dict[str, Any]]] = {
    "hw": {
        "car": {
            "attraction": {
                "parking_cost_work": -0.343374988523,
            },
            "impedance": {
                "time": (-0.0132535252, -0.0180517183),
                "cost": (-0.1004054942, -0.136755441374),
            },
            "log": {
                "size": 1.00000000000, # L_S_M
            },
            "size": {
                "cbd": (numpy.exp(4.6880073518),
                        numpy.exp(5.43822704609)),
                "workplaces_own": (numpy.exp(0.314367891487),
                                   numpy.exp(0.906947845409)),
                "workplaces_other": 1,
            },
        },
        "transit": {
            "attraction": {
                "cbd": (0.491418509053, 0.491418509053),
            },
            "impedance": {
                "time": -0.0101838292646,
                "cost": (-0.100405494227, -0.136755441374),
            },
            "log": {
                "size": 1.00000000000, # L_S_M
            },
            "size": {
                "cbd": (numpy.exp(4.6880073518), numpy.exp(5.43822704609)),
                "workplaces_own": (numpy.exp(0.314367891487), numpy.exp(0.906947845409)),
                "workplaces_other": 1,
            },
        },
        "bike": {
            "attraction": {},
            "impedance": {},
            "log": {
                "dist": (-1.11623384398, -1.3592708114),
                "size": 1.00000000000, # L_S_M
            },
            "size": {
                "cbd": (numpy.exp(4.6880073518), numpy.exp(5.43822704609)),
                "workplaces_own": (numpy.exp(0.314367891487), numpy.exp(0.906947845409)),
                "workplaces_other": 1,
            },
        },
        "walk": {
            "attraction": {
                "own_zone_area_sqrt": (-2.15046600566, -2.08475720417),
            },
            "impedance": {},
            "log": {
                "dist": -2.66277304293,
                "size": 1.00000000000, # L_S_M
            },
            "size": {
                "cbd": (numpy.exp(4.6880073518), numpy.exp(5.43822704609)),
                "workplaces_own": (numpy.exp(0.314367891487), numpy.exp(0.906947845409)),
                "workplaces_other": 1,
            },
        },
    },
    "hc": {
        "car": {
            "attraction": {},
            "impedance": {
                "time": -0.418311339830e-1,
            },
            "log": {
                "transform": -2.31917697254,
                "size": 1.00000000000,
            },
            "size": {
                "comprehensive_schools": 1,
            },
            "transform": {
                "attraction":{
                    "parking_cost_errand": 1,
                },
                "impedance": {
                    "cost": 1,
                },
            }
        },
        "transit": {
            "attraction": {
                "own_zone_area_sqrt": -1.40415965463,
                "cbd": (0.704345842211, 0.704345842211),
                "helsinki_other": (0.50, 0.20),
            },
            "impedance": {
                "time": -0.245629127645e-1,
            },
            "log": {
                "transform": -2.31917697254,
                "size": 1.00000000000,
            },
            "size": {
                "comprehensive_schools": 1,
            },
            "transform": {
                "attraction": {},
                "impedance": {
                    "cost": (1.0, 1.0),
                },
            },
        },
        "bike": {
            "attraction": {},
            "impedance": {},
            "log": {
                "dist": -2.04456095712,
                "size": 1.00000000000,
            },
            "size": {
                "comprehensive_schools": 1,
            },
        },
        "walk": {
            "attraction": {
                "own_zone_area_sqrt": (-3.87680793384 + 0.10,
                                       -3.87680793384 - 2.00),
            },
            "impedance": {},
            "log": {
                "dist": -4.89065780132,
                "size": 1.00000000000,
            },
            "size": {
                "comprehensive_schools": 1,
            },
        },
    },
    "hu": {
        "car": {
            "attraction": {
                "parking_cost_work": (-0.357366885936,
                                      -0.357366885936),
            },
            "impedance": {
                "time": -0.0297120650,
                "cost": -0.225091401758,
            },
            "log": {
                "size": 1.00000000000, # L_S_M
            },
            "size": {
                "secondary_schools": numpy.exp(-1.22536093464),
                "tertiary_education": 1,
            },
        },
        "transit": {
            "attraction": {
                "cbd": (0.145828916891, 0.145828916891),
            },
            "impedance": {
                "time": (-0.0135191971654, -0.0135191971654),
                "cost": (-0.225091401758, -0.225091401758),
            },
            "log": {
                "size": 1.00000000000,
            },
            "size": {
                "secondary_schools": numpy.exp(-1.22536093464),
                "tertiary_education": 1,
            },
        },
        "bike": {
            "attraction": {},
            "impedance": {
            },
            "log": {
                "dist": (-1.70901466021, -1.70901466021),
                "size": 1.00000000000,
            },
            "size": {
                "secondary_schools": numpy.exp(-1.22536093464),
                "tertiary_education": 1,
            },
        },
        "walk": {
            "attraction": {
                "own_zone_area_sqrt": -2.28428769533,
            },
            "impedance": {},
            "log": {
                "dist": -3.32824531424 + 0.00,
                "size": 1.00000000000,
            },
            "size": {
                "secondary_schools": numpy.exp(-1.22536093464),
                "tertiary_education": 1,
            },
        },
    },
    "hs": {
        "car": {
            "attraction": {
                "parking_cost_errand": -0.198005522852,
            },
            "impedance": {
                "time": -0.0427449023,
                "cost": -0.477596673469,
            },
            "log": {
                "size": 1.00000000000, # L_S_M
            },
            "size": {
                "population_other": 1,
                "population_own": numpy.exp(1.54407400279),
                "shops_other": numpy.exp(6.34839288971),
                "shops_own": (numpy.exp(5.90300326341), 
                              numpy.exp(6.98452705435)),
                "service_other": numpy.exp(3.80218657061),
                "service_own": (numpy.exp(4.399261887),
                                numpy.exp(5.06426205412)),
                "cbd": (numpy.exp(8.92119753904),
                        numpy.exp(7.17315876803)),
            },
        },
        "transit": {
            "attraction": {
                "cbd": (0.194157681759 + 0.00, 4.25838834127 + 0.00),
                "helsinki_other": (0.00, 0.00),
            },
            "impedance": {
                "time": -0.0268255591268,
                "cost": -0.477596673469,
            },
            "log": {
                "size": 1.00000000000,
            },
            "size": {
                "population_other": 1,
                "population_own": numpy.exp(1.54407400279),
                "shops_other": numpy.exp(6.34839288971),
                "shops_own": (numpy.exp(5.90300326341), 
                              numpy.exp(6.98452705435)),
                "service_other": numpy.exp(3.80218657061),
                "service_own": (numpy.exp(4.399261887),
                                numpy.exp(5.06426205412)),
                "cbd": (numpy.exp(8.92119753904),
                        numpy.exp(7.17315876803)),
            },
        },
        "bike": {
            "attraction": {},
            "impedance": {},
            "log": {
                "dist": (-1.95518149948, -1.67112409733),
                "size": 1.00000000000,
            },
            "size": {
                "population_other": 1,
                "population_own": numpy.exp(1.54407400279),
                "shops_other": numpy.exp(6.34839288971),
                "shops_own": (numpy.exp(5.90300326341), 
                              numpy.exp(6.98452705435)),
                "service_other": numpy.exp(3.80218657061),
                "service_own": (numpy.exp(4.399261887),
                                numpy.exp(5.06426205412)),
                "cbd": (numpy.exp(8.92119753904),
                        numpy.exp(7.17315876803)),
            },
        },
        "walk": {
            "attraction": {
                "own_zone_area_sqrt": (-3.46874228834 - 0.70, 
                                       -4.72081529262 - 1.20),
                "population_density": 0.0000215025563001,
            },
            "impedance": {},
            "log": {
                "dist": -4.00475528272,
                "size": 1.00000000000,
            },
            "size": {
                "population_other": 1,
                "population_own": numpy.exp(1.54407400279),
                "shops_other": numpy.exp(6.34839288971),
                "shops_own": (numpy.exp(5.90300326341), 
                              numpy.exp(6.98452705435)),
                "service_other": numpy.exp(3.80218657061),
                "service_own": (numpy.exp(4.399261887),
                                numpy.exp(5.06426205412)),
                "cbd": (numpy.exp(8.92119753904),
                        numpy.exp(7.17315876803)),
            },
        },
    },
    "ho": {
        "car": {
            "attraction": {
                "own_zone": 0.642829705544,
                "parking_cost_errand": -.271848312580,
            },
            "impedance": {
                "time": -0.0195496488,
                "cost": -.218431829623,
            },
            "log": {
                "size": 1,
            },
            "size": {
                "population_other": 1,
                "population_own": numpy.exp(1.36533858970),
                "service_other": numpy.exp(2.39351567744),
                "service_own": numpy.exp(3.35003762339),
                "shops": numpy.exp(3.10201560094),
                "cbd": (numpy.exp(7.82599214329),
                        numpy.exp(4.95459142492)),
            },
        },
        "transit": {
            "attraction": {
                "own_zone": -1.99877035216,
                "cbd": 0.637633920546,
            },
            "impedance": {
                "time": -0.0163548606161,
                "cost": -0.218431829623,
            },
            "log": {
                "size": 1,
            },
            "size": {
                "population_other": 1,
                "population_own": numpy.exp(1.36533858970),
                "service_other": numpy.exp(2.39351567744),
                "service_own": numpy.exp(3.35003762339),
                "shops": numpy.exp(3.10201560094),
                "cbd": (numpy.exp(7.82599214329),
                        numpy.exp(4.95459142492)),
            },
        },
        "bike": {
            "attraction": {},
            "impedance": {},
            "log": {
                "dist": (-1.83301197674, -1.64746747645),
                "size": 1,
            },
            "size": {
                "population_other": 1,
                "population_own": numpy.exp(1.36533858970),
                "service_other": numpy.exp(2.39351567744),
                "service_own": numpy.exp(3.35003762339),
                "shops": numpy.exp(3.10201560094),
                "cbd": (numpy.exp(7.82599214329),
                        numpy.exp(4.95459142492)),
            },
        },
        "walk": {
            "attraction": {
                "own_zone_area_sqrt": (-1.13782241032 + 0.00,
                                       -1.00451024484 + 0.00),
                "population_density": -0.423271371798E-04,
            },
            "impedance": {},
            "log": {
                "dist": -3.69672461344,
                "size": 1,
            },
            "size": {
                "population_other": 1,
                "population_own": numpy.exp(1.36533858970),
                "service_other": numpy.exp(2.39351567744),
                "service_own": numpy.exp(3.35003762339),
                "shops": numpy.exp(3.10201560094),
                "cbd": (numpy.exp(7.82599214329),
                        numpy.exp(4.95459142492)),
            },
        },
    },
    "hoo": {
        "car": {
            "attraction": {
                "own_zone": (1.511261249, 0.496255377),
                "parking_cost_errand": -0.110043052,
            },
            "impedance": {
                "time": -0.121821884,
                "cost": -0.071273703,
            },
            "log": {
                "size": 0.635546074,
            },
            "size": {
                "population": 1,
                "service": numpy.exp(3.359535766),
                "shops": numpy.exp(5.054869817),
                "cbd": numpy.exp(5.497881457),
            },
        },
        "transit": {
            "attraction": {
                "own_zone": (1.138959644, -0.582370838),
            },
            "impedance": {
                "time": -0.054854548,
                "cost": -0.071273703,
            },
            "log": {
                "size": 0.564060942,
            },
            "size": {
                "population": 1,
                "service": numpy.exp(3.171875158),
                "shops": numpy.exp(5.513706147),
            },
        },
        "bike": {
            "attraction": {
                "own_zone": (1.254997132, 0.698948786),
            },
            "impedance": {
                "dist": -0.575044482,
            },
            "log": {
                "size": 0.698342216,
            },
            "size": {
                "population": 1,
                "service": numpy.exp(1.455295457),
                "shops": numpy.exp(3.2502116),
            },
        },
    },
    "wo": {
        "car": {
            "attraction": {
                "parking_cost_errand": -.291338216556,
            },
            "impedance": {
                "time": -0.0371080433,
                "cost": -.281121539905,
            },
            "log": {
                "size": 1,
            },
            "size": {
                "population": 1,
                "workplaces": numpy.exp(.400884483384),
                "service": numpy.exp(1.58922222310),
                "shops_cbd": numpy.exp(3.58798748920),
                "shops_elsewhere": numpy.exp(3.36839356543),
                "own_zone": (numpy.exp(6.94153078815),
                             numpy.exp(6.94153078815)),
            },
        },
        "transit": {
            "attraction": {
                "cbd": .350354942258,
                "own_zone": -1.87675547285,
            },
            "impedance": {
                "time": -.0190572340198,
                "cost": -.281121539905,
            },
            "log": {
                "size": 1,
            },
            "size": {
                "population": 1,
                "workplaces": numpy.exp(.400884483384),
                "service": numpy.exp(1.58922222310),
                "shops_cbd": numpy.exp(3.58798748920),
                "shops_elsewhere": numpy.exp(3.36839356543),
                "own_zone": (numpy.exp(6.94153078815),
                             numpy.exp(6.94153078815)),
            },
        },
        "bike": {
            "attraction": {},
            "impedance": {},
            "log": {
                "dist": (-2.05206422461, -1.82198542728),
                "size": 1,
            },
           "size": {
                "population": 1,
                "workplaces": numpy.exp(.400884483384),
                "service": numpy.exp(1.58922222310),
                "shops_cbd": numpy.exp(3.58798748920),
                "shops_elsewhere": numpy.exp(3.36839356543),
                "own_zone": (numpy.exp(6.94153078815),
                             numpy.exp(6.94153078815)),
            },
        },
        "walk": {
            "attraction": {
                "own_zone_area_sqrt": (-1.10044318679, -1.94548368752),
            },
            "impedance": {},
            "log": {
                "dist": -3.38855455974,
                "size": 1,
            },
            "size": {
                "population": 1,
                "workplaces": numpy.exp(.400884483384),
                "service": numpy.exp(1.58922222310),
                "shops_cbd": numpy.exp(3.58798748920),
                "shops_elsewhere": numpy.exp(3.36839356543),
                "own_zone": (numpy.exp(6.94153078815),
                             numpy.exp(6.94153078815)),
            },
        },
    },
    "oo": {
        "car": {
            "attraction": {
                "parking_cost_errand": -.291338216556,
            },
            "impedance": {
                "time": -0.0371080433 + 0.00,
                "cost": -.281121539905 + 0.00,
            },
            "log": {
                "size": 1,
            },
            "size": {
                "population": 1,
                "workplaces": numpy.exp(.400884483384),
                "service": numpy.exp(1.58922222310),
                "shops_cbd": numpy.exp(3.58798748920),
                "shops_elsewhere": numpy.exp(3.36839356543),
                "own_zone": (numpy.exp(6.94153078815),
                             numpy.exp(6.94153078815)),
            },
        },
        "transit": {
            "attraction": {
                "cbd": .350354942258 + 0.00,
                "own_zone": -1.87675547285 + 0.00,
            },
            "impedance": {
                "time": -.0190572340198,
                "cost": -.281121539905,
            },
            "log": {
                "size": 1,
            },
            "size": {
                "population": 1,
                "workplaces": numpy.exp(.400884483384),
                "service": numpy.exp(1.58922222310),
                "shops_cbd": numpy.exp(3.58798748920),
                "shops_elsewhere": numpy.exp(3.36839356543),
                "own_zone": (numpy.exp(6.94153078815),
                             numpy.exp(6.94153078815)),
            },
        },
        "bike": {
            "attraction": {},
            "impedance": {},
            "log": {
                "dist": (-2.05206422461, -1.82198542728),
                "size": 1,
            },
           "size": {
                "population": 1,
                "workplaces": numpy.exp(.400884483384),
                "service": numpy.exp(1.58922222310),
                "shops_cbd": numpy.exp(3.58798748920),
                "shops_elsewhere": numpy.exp(3.36839356543),
                "own_zone": (numpy.exp(6.94153078815),
                             numpy.exp(6.94153078815)),
            },
        },
        "walk": {
            "attraction": {
                "own_zone_area_sqrt": (-1.10044318679, -1.94548368752),
            },
            "impedance": {},
            "log": {
                "dist": -3.38855455974,
                "size": 1,
            },
            "size": {
                "population": 1,
                "workplaces": numpy.exp(.400884483384),
                "service": numpy.exp(1.58922222310),
                "shops_cbd": numpy.exp(3.58798748920),
                "shops_elsewhere": numpy.exp(3.36839356543),
                "own_zone": (numpy.exp(6.94153078815),
                             numpy.exp(6.94153078815)),
            },
        },
    },
    "wh": {
        "car": {
            "attraction": {},
            "impedance": {
                "time": (-0.0132535252, -0.0180517183),
                "cost": (-0.1004054942, -0.136755441374),
            },
            "log": {
                "size": 1.00000000000, # L_S_M
            },
            "size": {
                "population_own": numpy.exp(0.314367891487),
                "population_other": 1,
            },
        },
        "transit": {
            "attraction": {},
            "impedance": {
                "time": -0.0101838292646,
                "cost": (-0.100405494227, -0.136755441374),
            },
            "log": {
                "size": 1.00000000000, # L_S_M
            },
            "size": {
                "population_own": numpy.exp(0.314367891487),
                "population_other": 1,
            },
        },
        "bike": {
            "attraction": {},
            "impedance": {},
            "log": {
                "dist": (-1.11623384398, -1.3592708114),
                "size": 1.00000000000, # L_S_M
            },
            "size": {
                "population_own": numpy.exp(0.314367891487),
                "population_other": 1,
            },
        },
        "walk": {
            "attraction": {
                "own_zone_area_sqrt": (-2.15046600566, -2.08475720417),
            },
            "impedance": {},
            "log": {
                "dist": -2.66277304293,
                "size": 1.00000000000, # L_S_M
            },
            "size": {
                "population_own": numpy.exp(0.314367891487),
                "population_other": 1,
            },
        },
    },
    "hwp": {
        "car": {
            "attraction": {
                "parking_cost_work": -0.157123873740,
                "share_detached_houses": 0.580974879625,
                "own_zone_area": -0.0205161484737 - 0.020,
            },
            "impedance": {
                "time": -0.0207403513,
                "cost": -0.157123873740,
            },
            "log": {
                "size": 0.906942834933, # LN_Size
            },
            "size": {
                "workplaces": 1,
            },
        },
        "transit": {
            "attraction": {
                "cbd": 0.460082225170,
                "own_zone_area": -0.113153242090,
            },
            "impedance": {
                "time": -0.824400763002E-02,
                "cost": (-0.157123873740),
            },
            "log": {
                "size": 0.906942834933, # LN_Size
            },
            "size": {
                "workplaces": 1,
            },
        },
    },
    "hop": {
        "car": {
            "attraction": {
                "car_density": 1000 * 0.190087895761E-02,
                "own_zone_area": -0.914703619822E-02,
            },
            "impedance": {
                "time": -0.0207498305,
                "cost": -.231841682005,
            },
            "log": {
                "size": 1, # L_S_M
            },
            "size": {
                "workplaces": numpy.exp(1.23033343181),
                "service": numpy.exp(4.63048603927),
                "shops": numpy.exp(5.40401631191),
                "comprehensive_schools": numpy.exp(2.38807154465),
                "population_own": numpy.exp(3.32704971816),
                "population_other": 1,
            },
        },
        "transit": {
            "attraction": {},
            "impedance": {
                "time": -0.503184346810E-02,
                "cost": (-0.231841682005 - 0.00),
            },
            "log": {
                "size": 1, # L_S_M
            },
            "size": {
                "workplaces": numpy.exp(1.23033343181),
                "service": numpy.exp(4.63048603927),
                "shops": numpy.exp(5.40401631191),
                "comprehensive_schools": numpy.exp(2.38807154465),
                "population_own": numpy.exp(3.32704971816),
                "population_other": 1,
            },
        },
    },
    "sop": {
        "logsum": {
            "attraction": {
                "own_zone": 0.491757816367,
            },
            "impedance": {},
            "log": {
                "logsum": 0.852698948873,
                "size": 0.824476718431,
            },
            "size": {
                "workplaces": numpy.exp(3.93387218470),
                "population_own": numpy.exp(3.04338951027),
                "population_other": 1.0,
            },
        },
    },
    "oop": {
        "car": {
            "attraction": {
                "parking_cost_errand": -0.227398812175,
            },
            "impedance": {
                "time": (-0.427365675012e-1,
                         -0.427365675012e-1 - 0.005),
                "cost": -0.227398812175,
            },
            "log": {
                "size": 1, # L_S_M
            },
            "size": {
                "population": 1,
                "workplaces": numpy.exp(1.26651176555),
                "shops_cbd": (numpy.exp(4.08944842667 - 3.0),
                              numpy.exp(4.08944842667 + 2.0)),
                "shops_elsewhere": numpy.exp(2.62226008068),
            },
        },
        "transit": {
            "attraction": {
                "cbd": (2.84600723332 - 1.0,
                        2.84600723332 + 2.0),
            },
            "impedance": {
                "time": -0.819579857062e-2,
                "cost": (-0.227398812175 - 0.2,
                         -0.227398812175 - 0.2),
            },
            "log": {
                "size": 1, # L_S_M
            },
            "size": {
                "population": 1,
                "workplaces": numpy.exp(1.26651176555),
                "shops_cbd": numpy.exp(4.08944842667),
                "shops_elsewhere": numpy.exp(2.62226008068),
            },
        },
    },
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
