### MODE CHOICE PARAMETERS ###

# Mode choice (calibrated 02.10.2020)
from typing import Any, Dict, Optional


mode_choice: Dict[str, Optional[Dict[str, Dict[str, Any]]]] = {
    "hw": {
        "car": {
            "constant": (0.830938747727 * (0 + 0.278), 
                         0.830938747727 * (0 + 0.251)),
            "generation": {
                "car_density": (0.830938747727 * 1000 * 0.00282859274412, 0.830938747727 * 1000 * 0.00453019737785),
            },
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": 0.830938747727,
            },
            "individual_dummy": {
                "car_users": (0.830938747727 * 3.03999716806, 0.830938747727 * 2.95110380739),
            },
        },
        "transit": {
            "constant": (0.830938747727 * (3.35620148087 - 0.107), 
                         0.830938747727 * (3.35324641782 - 0.527)),
            "generation": {
                "cbd": 0.40,
                "helsinki_other": -0.10,
                "espoo_vant_kau": -0.30,
            },
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": 0.830938747727,
            },
            "individual_dummy": {},
        },
        "bike": {
            "constant": (0.830938747727 * (3.80657808148 - 0.017), 
                         0.830938747727 * (4.31992749379 + 0.033)),
            "generation": {},
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": 0.830938747727,
            },
            "individual_dummy": {},
        },
        "walk": {
            "constant": (0.830938747727 * (6.19979345573 + 0.040),
                         0.830938747727 * (6.52578316385 - 0.421)),
            "generation": {},
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": 0.830938747727,
            },
            "individual_dummy": {},
        },
    },
    "hc": {
        "car": {
            "constant": (0.272803753976 * (0 + 0.684),
                         0.272803753976 * (0 - 0.697)),
            "generation": {
                "car_density": 0.272803753976 * 1000 * 0.201094997058e-01,
            },
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": 0.272803753976, # Dcoeff
            },
            "individual_dummy": {},
        },
        "transit": {
            "constant": (0.272803753976 * (13.2817160786 + 0.077),
                         0.272803753976 * (13.2817160786 - 0.734)),
            "generation": {
                "cbd": 0.3,
                "helsinki_other": 0.3,
                "espoo_vant_kau": -0.3,
            },
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": 0.272803753976, # Dcoeff
            },
            "individual_dummy": {},
        },
        "bike": {
            "constant": (0.272803753976 * (11.3490028510 + 0.163),
                         0.272803753976 * (11.3490028510 + 2.018)),
            "generation": {},
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": 0.272803753976, # Dcoeff
            },
            "individual_dummy": {},
        },
        "walk": {
            "constant": (0.272803753976 * (17.7784859496 + 0.033),
                         0.272803753976 * (17.7784859496 - 1.254)),
            "generation": {},
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": 0.272803753976, # Dcoeff
            },
            "individual_dummy": {},
        },
    },
    "hu": {
        "car": {
            "constant": (0 - 0.315, 0 + 0.675),
            "generation": {
                "car_density": 1000 * 0.504851816443e-2,
            },
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": 1.00000000000, # Dcoeff
            },
            "individual_dummy": {},
        },
        "transit": {
            "constant": (3.12509878421 + 0.053, 3.12509878421 + 0.468),
            "generation": {
                "cbd": 0.5,
                "helsinki_other": 0.1,
                "espoo_vant_kau": -0.7,
            },
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": 1.00000000000,
            },
            "individual_dummy": {},
        },
        "bike": {
            "constant": (3.24451960342 + 0.379, 3.24451960342 + 1.910),
            "generation": {},
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": 1.00000000000,
            },
            "individual_dummy": {},
        }, 
        "walk": {
            "constant": (6.16685830247 + 0.493, 6.16685830247 + 1.253), 
            "generation": {},
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": 1.00000000000,
            },
            "individual_dummy": {},
        },
    },
    "hs": {
        "car": {
            "constant": (0.522036062262 * (0 + 0.323), 
                         0.522036062262 * (0 + 0.189)),
            "generation": {
                "car_density": (0.522036062262 * 1000 * 0.00996637488914, 0.522036062262 * 1000 * 0.0166093327868),
            },
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": 0.522036062262, # Dcoeff
            },
            "individual_dummy": {
                "car_users": (0.522036062262 * 4.50826448347, 0.522036062262 * 3.60490124299),
            },
        },
        "transit": {
            "constant": (0.522036062262 * (6.72180796903 + 0.158), 
                         0.522036062262 * (6.67197643351 - 0.399)),
            "generation": {
                "espoo_vant_kau": -0.3,
            },
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": 0.522036062262,
            },
            "individual_dummy": {},
        },
        "bike": {
            "constant": (0.522036062262 * (4.3562332376 + 0.307), 
                         0.522036062262 * (7.8358175344 + 0.210)),
            "generation": {},
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": 0.522036062262,
            },
            "individual_dummy": {},
        }, 
        "walk": {
            "constant": (0.522036062262 * (11.3353754845 + 0.065),
                         0.522036062262 * (13.3431291443 + 0.068)),
            "generation": {},
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": 0.522036062262,
            },
            "individual_dummy": {},
        },
    },
    "ho": {
        "car": {
            "constant": (0.157371648547 * (0 - 0.280),
                         0.157371648547 * (0 - 0.130)),
            "generation": {
                "car_density": (0.157371648547 * 1000 * 0.0275157057103, 0.157371648547 * 1000 * 0.00903883238252),
            },
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": 0.157371648547,
            },
            "individual_dummy": {
                "car_users": (0.157371648547 * 4.43378318532, 0.157371648547 * 2.98838274317),
            },
        },
        "transit": {
            "constant": (0.157371648547 * (8.33856436370 - 0.380), 
                         0.157371648547 * (-9.21721208402 - 0.258)),
            "generation": {
                "cbd": 0.2,
                "espoo_vant_kau": -0.8,
            },
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": 0.157371648547,
            },
            "individual_dummy": {},
        },
        "bike": {
            "constant": (0.157371648547 * (5.65570738596 - 0.113), 
                         0.157371648547 * (-.549035575271 + 0.374)),
            "generation": {},
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": 0.157371648547,
            },
            "individual_dummy": {},
        }, 
        "walk": {
            "constant": (0.157371648547 * (20.8216972704 - 0.450), 
                         0.157371648547 * (12.5696379434 - 0.134)),
            "generation": {},
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": 0.157371648547,
            },
            "individual_dummy": {},
        },
    },
    "hoo": None,
    "wo": {
       "car": {
            "constant": (.718153936654 * (0 + 0.520),
                         .718153936654 * (0 + 1.112)),
            "generation": {
                "car_density": (.718153936654 * 1000 * .00281255180930, .718153936654 * 1000 * .00306776772245),
            },
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": .718153936654,
            },
            "individual_dummy": {},
        },
        "transit": {
            "constant": (.718153936654 * (1.47963675807 - 0.168),
                         .718153936654 * (1.47963675807 - 3.635)),
            "generation": {
                "cbd": 0.9,
                "helsinki_other": -0.1,
                "espoo_vant_kau": -0.9,
            },
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": .718153936654,
            },
            "individual_dummy": {},
        },
        "bike": {
            "constant": (.718153936654 * (-.346070374291 + 1.601),
                         .718153936654 * (.0632569112049 - 0.280)),
            "generation": {},
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": .718153936654,
            },
            "individual_dummy": {},
        }, 
        "walk": {
            "constant": (.718153936654 * (5.72318117910 + 0.522),
                         .718153936654 * (5.72318117910 - 0.368)),
            "generation": {},
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": .718153936654,
            },
            "individual_dummy": {},
        },
    },
    "oo": {
        "car": {
            "constant": (.718153936654 * (0 - 0.094),
                         .718153936654 * (0 + 0.030)),
            "generation": {
                "car_density": (.718153936654 * 1000 * .00281255180930, .718153936654 * 1000 * .00306776772245),
            },
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": .718153936654,
            },
            "individual_dummy": {},
        },
        "transit": {
            "constant": (.718153936654 * (1.47963675807 + 0.894),
                         .718153936654 * (1.47963675807 + 0.242)),
            "generation": {
                "cbd": 0.2,
                "helsinki_other": -0.4,
                "espoo_vant_kau": -0.4,
            },
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": .718153936654,
            },
            "individual_dummy": {},
        },
        "bike": {
            "constant": (.718153936654 * (-.346070374291 - 0.323),
                         .718153936654 * (.0632569112049 + 1.241)),
            "generation": {},
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": .718153936654,
            },
            "individual_dummy": {},
        }, 
        "walk": {
            "constant": (.718153936654 * (5.72318117910 + 0.464),
                         .718153936654 * (5.72318117910 + 0.867)),
            "generation": {},
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": .718153936654,
            },
            "individual_dummy": {},
        },
    },
    "wh": {
        "car": {
            "constant": (0.830938747727 * (0 + 0.278), 
                         0.830938747727 * (0 + 0.251)),
            "generation": {},
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": 0.830938747727,
            },
            "individual_dummy": {},
        },
        "transit": {
            "constant": (0.830938747727 * (3.35620148087 - 0.107), 
                         0.830938747727 * (3.35324641782 - 0.527)),
            "generation": {},
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": 0.830938747727,
            },
            "individual_dummy": {},
        },
        "bike": {
            "constant": (0.830938747727 * (3.80657808148 - 0.017), 
                         0.830938747727 * (4.31992749379 + 0.033)),
            "generation": {},
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": 0.830938747727,
            },
            "individual_dummy": {},
        },
        "walk": {
            "constant": (0.830938747727 * (6.19979345573 + 0.040),
                         0.830938747727 * (6.52578316385 - 0.421)),
            "generation": {},
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": 0.830938747727,
            },
            "individual_dummy": {},
        },
    },
    "hwp": {
        "car": {
            "constant": (0 + 0.024),
            "generation": {},
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": 1.00000000000, # Dcoeff
            },
            "individual_dummy": {},
        },
        "transit": {
            "constant": (-1.83293849298 - 0.199), # T_const
            "generation": {},
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": 1.00000000000, # Dcoeff
            },
            "individual_dummy": {},
        },
    },
    "hop": {
        "car": {
            "constant": (0 + 0.075),
            "generation": {},
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": 1.00000000000,
            },
            "individual_dummy": {},
        },
        "transit": {
            "constant": (-1.02607987269 - 0.075),
            "generation": {},
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": 1.00000000000,
            },
            "individual_dummy": {},
        },
    },
    "sop": {
        "car": {
            "constant": 0.0,
            "generation": {},
            "attraction": {
                "own_zone_area": -0.01478815,
                "parking_cost_work": -0.154340268,
            },
            "impedance": {
                "time": -0.021262374,
                "cost": -0.154340268,
            },
            "log": {},
            "individual_dummy": {},
        },
        "transit": {
            "constant": -2.060141017,
            "generation": {},
            "attraction": {
                "own_zone_area": -0.115937409151,
            },
            "impedance": {
                "time": -0.007909217,
                "cost": -0.154340268 / 30.0,
            },
            "log": {},
            "individual_dummy": {},
        },
    },
    "oop": {
        "car": {
            "constant": (0.715272183645 * (0 + 0.135)),
            "generation": {},
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": 0.715272183645,
            },
            "individual_dummy": {},
        },
        "transit": {
            "constant": (0.715272183645 * (-3.44371464477 + 0.243)),
            "generation": {},
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": 0.715272183645,
            },
            "individual_dummy": {},
        },
    },
}
