import numpy

### ASSIGNMENT PARAMETERS ###

# Performance settings
performance_settings = {
    "number_of_processors": "max"
}
# Inversed value of time [min/eur]
vot_inv = {
    "work": 6,
    "business": 6,
    "leisure": 6,
}
# Default distance cost [eur/km]
dist_cost = 0.12
# Boarding penalties for different transit modes
boarding_penalty = {
    "b": 3,  # Bus
    "g": 3,  # Trunk bus
    "de": 5, # Long-distance and express bus
    "tp": 0, # Tram and light rail
    "mw": 0, # Metro and ferry
    "rj": 2, # Train
}
# Headway standard deviation function parameters for different transit modes
headway_sd_func = {
    'b': {
        "asc": 2.164,
        "ctime": 0.078,
        "cspeed": -0.028,
    },
    'd':  {
        "asc": 2.164,
        "ctime": 0.078,
        "cspeed": -0.028,
    },
    'g':  {
        "asc": 2.127,
        "ctime": 0.034,
        "cspeed": -0.021,
    },
    't':  {
        "asc": 1.442,
        "ctime": 0.060,
        "cspeed": -0.039,
    },
    'p':  {
        "asc": 1.442,
        "ctime": 0.034,
        "cspeed": -0.039,
    },
}
# Stopping criteria for last traffic assignment
stopping_criteria_fine = {
    "max_iterations": 200,
    "relative_gap": 0.00001,
    "best_relative_gap": 0.001,
    "normalized_gap": 0.0005,
}
# Stopping criteria for traffic assignment in loop
stopping_criteria_coarse = {
    "max_iterations": 100,
    "relative_gap": 0.0001,
    "best_relative_gap": 0.01,
    "normalized_gap": 0.005,
}
# Congestion function for congested transit assignment
trass_func = {
    "type": "BPR",
    "weight": 1.23,
    "exponent": 3,
    "assignment_period": 1,
    "orig_func": False,
    "congestion_attribute": "us3",
}
# Stopping criteria for congested transit assignment
trass_stop = {
    "max_iterations": 10,
    "normalized_gap": 0.01,
    "relative_gap": 0.001
}
# Specification for the transit assignment
transfer_penalty = 5
extra_waiting_time = {
    "penalty": "@wait_time_dev",
    "perception_factor": 3.5
}
first_headway_fraction = 0.3
standard_headway_fraction = 0.5
waiting_time_perception_factor = 1.5
aux_transit_time = {
    "perception_factor": 1.75
}
# Stochastic bike assignment distribution
bike_dist = {
    "type": "UNIFORM", 
    "A": 0.5, 
    "B": 1.5,
}

### ASSIGNMENT REFERENCES ###

# Volume-delay function files
func_car = "d411_pituusriippuvaiset_HM30.in"
func_bike = "d411_pituusriippuvaiset_pyora.in"
# Emme scenarios used in assignment
emme_scenario = {
    "aht": 21,
    "pt": 22,
    "iht": 23,
}
bike_scenario = 19
transport_classes = (
    "car_work",
    "car_leisure",
    "transit_work",
    "transit_leisure",
    "bike_work",
    "bike_leisure",
    "trailer_truck",
    "truck",
    "van",
)
assignment_class = {
    "hw": "work",
    "hc": "leisure",
    "hu": "leisure",
    "hs": "leisure",
    "ho": "leisure",
    "hoo": "work",
    "wo": "work",
    "oo": "leisure",
    "hwp": "work",
    "hop": "leisure",
    "oop": "leisure",
    "external": "leisure",
}
car_mode = 'c'
assignment_mode = {
    "car_work": 'c',
    "car_leisure": 'c',
    "trailer_truck": 'y',
    "truck": 'k',
    "van": 'v',
}
vot_class = {
    "car_work": "work",
    "car_leisure": "leisure",
    "trailer_truck": "business",
    "truck": "business",
    "van": "business",
}
bike_mode = 'f'
transit_modes = [
    'b',
    'd',
    'e',
    'g',
    'j',
    'm',
    'p',
    'r',
    't',
    'w',
]
aux_modes = [
    'a',
    's',
]
transit_assignment_modes = transit_modes + aux_modes
# Link attribute for volumes
link_volumes = {
    "car_work": None,
    "car_leisure": None,
    "trailer_truck": "@yhd",
    "truck": "@ka",
    "van": "@pa",
}
# Emme matrix IDs
emme_mtx = {
    "demand": {
        "car_work": {
            "id": "mf1",
            "description": "car work demand",
        },
        "car_leisure": {
            "id": "mf2",
            "description": "car leisure demand",
        },
        "trailer_truck": {
            "id": "mf71",
            "description": "trailer truck demand",
        },
        "truck":  {
            "id":"mf72",
            "description": "truck demand",
        },
        "van":  {
            "id":"mf73",
            "description": "van demand",
        },
        "transit":  {
            "id":"mf4",
            "description": "transit demand",
        },
        "bike":  {
            "id":"mf7",
            "description": "bicyclist demand",
        },
    },
    "gen_cost": {
        "car_work": {
            "id": "mf372",
            "description": "car work travel generalized cost",
        },
        "car_leisure": {
            "id": "mf373",
            "description": "car leisure travel generalized cost",
        },
    },
    "time": {
        "car_work": {
            "id": "mf380",
            "description": "car work travel time",
        },
        "car_leisure": {
            "id": "mf382",
            "description": "car leisure travel time",
        },
        "transit": {
            "id": "mf20",
            "description": "transit travel time",
        },
        "bike": {
            "id": "mf386",
            "description": "bike travel time",
        },
        "walk": {
            "id": "mf376",
            "description": "walk travel time",
        },
    },
    "dist": {
        "car_work": {
            "id": "mf381",
            "description": "car work travel distance",
        },
        "car_leisure": {
            "id": "mf383",
            "description": "car leisure travel distance",
        },
        "transit": {
            "id": "mf27",
            "description": "transit in-vehicle distance",
        },
        "bike": {
            "id": "mf387",
            "description": "bike travel distance",
        },
        "walk": {
            "id": "mf377",
            "description": "walk travel distance",
        },
    },
    "cost": {
        "car_work": {
            "id": "mf370",
            "description": "car work travel cost",
        },
        "car_leisure": {
            "id": "mf371",
            "description": "car leisure travel cost",
        },
        "transit": {
            "id": "mf31",
            "description": "transit travel cost",
        },
    },
    "transit": {
        "inv_time": {
            "id": "mf21",
            "description": "transit in-vehicle time",
        },
        "aux_time": {
            "id": "mf22",
            "description": "transit auxilliary time",
        },
        "tw_time": {
            "id": "mf23",
            "description": "transit total waiting time",
        },
        "fw_time": {
            "id": "mf24",
            "description": "transit first waiting time",
        },
        "board_time": {
            "id": "mf25",
            "description": "transit boarding time",
        },
        "board_cost": {
            "id": "mf28",
            "description": "transit boarding cost",
        },
        "num_board": {
            "id": "mf26",
            "description": "transit trip number of boardings",
        },
    },
    "bike": {
        "separate_dist": {
            "id": "mf100",
            "description": "separate bike way distance",
        },
        "streetside_dist": {
            "id": "mf101",
            "description": "street-side bike way distance",
        },
        "mixed_dist": {
            "id": "mf102",
            "description": "bike distance in mixed traffic",
        },
    },
}
background_traffic = "ul3"

### DEPARTURE TIME PARAMETERS ###

# Demand shares for different time periods
demand_share = {
    "hw": {
        "car": {
            "aht": (0.182755037123829, 0.000367115427580429),
            "pt": (0.022343644659004, 0.00157136493073783),
            "iht": (0.113305596333855, 0.0243291362182353),
        },
        "transit": {
            "aht": (0.168711059732239, 0),
            "pt": (0.0218751689568907, 0.000473279937135581),
            "iht": (0.113363569361422, 0.0144615446952855),
        },
        "bike": {
            "aht": (0.203057934841124, 0.00119076332075889),
            "pt": (0.0190461620914818, 0.00215718968881016),
            "iht": (0.170453565625586, 0.0153043584935159),
        },
        "walk": {
            "aht": (0.164142085189847, 0),
            "pt": (0.0372688843249433, 0.000195898762704092),
            "iht": (0.127145781212114, 0.00873107280125695),
        },
    },
    "hc": {
        "car": {
            "aht": (0.310417241278776, 0),
            "pt": (0.0572333556244746, 0.00342632785679063),
            "iht": (0.0320934306414137, 0.0148051165083341),
        },
        "transit": {
            "aht": (0.304893450525294, 0),
            "pt": (0.0613753972913634, 0.0023689265080948),
            "iht": (0.0736235228063451, 0.0134363415142118),
        },
        "bike": {
            "aht": (0.31262218616239, 0),
            "pt": (0.0754389786386322, 0.00267447070864475),
            "iht": (0.0575717735967143, 0.00366534518007794),
        },
        "walk": {
            "aht": (0.34118435176724, 0),
            "pt": (0.0699011924883841, 0.00124442549804012),
            "iht": (0.0476616860474796, 0),
        },
    },
    "hu": {
        "car": {
            "aht": (0.241027549652423, 0),
            "pt": (0.0459160119569292, 0.00413631610153875),
            "iht": (0.0767840509578923, 0.0173565959443348),
        },
        "transit": {
            "aht": (0.180134784106046, 0.00355330562864804),
            "pt": (0.0683930092744635, 0.00203120152748125),
            "iht": (0.100698226598881, 0.00789720271203847),
        },
        "bike": {
            "aht": (0.128957938321136, 0),
            "pt": (0.100717066079754, 0.00226113071051614),
            "iht": (0.078663164632373, 0),
        },
        "walk": {
            "aht": (0.156778787310747, 0),
            "pt": (0.0675815357412708, 0.00274993450704592),
            "iht": (0.130650606313711, 0),
        },
    },
    "hs": {
        "car": {
            "aht": (0.033245077555297, 0.000553511226067097),
            "pt": (0.0600279492079586, 0.0051866482911981),
            "iht": (0.0636372912263753, 0.00875071329333986),
        },
        "transit": {
            "aht": (0.0508927659494044, 0),
            "pt": (0.0859562814465929, 0.00957572490415399),
            "iht": (0.0622201237254957, 0.0159135437309192),
        },
        "bike": {
            "aht": (0.0342125271956583, 0),
            "pt": (0.0695202242938326, 0.00430314615642964),
            "iht": (0.103653706468167, 0.00462494062324966),
        },
        "walk": {
            "aht": (0.0463947697528905, 0.00103484852199231),
            "pt": (0.0715624838553775, 0.00189243886717988),
            "iht": (0.0888871375956203, 0.00428420550179696),
        },
    },
    "ho": {
        "car": {
            "aht": (0.024223584974353, 0.00183131511440919),
            "pt": (0.0336054113721059, 0.00270217080116225),
            "iht": (0.0696996272520316, 0.00719608569439149),
        },
        "transit": {
            "aht": (0.0192721911985514, 0.00419079217033318),
            "pt": (0.0453281511620232, 0.00514263289366042),
            "iht": (0.0531348279008259, 0.0121842853779324),
        },
        "bike": {
            "aht": (0.0320627698645252, 0),
            "pt": (0.0337017642218225, 0.00256599575875046),
            "iht": (0.0823609994083213, 0),
        },
        "walk": {
            "aht": (0.0471234369258131, 9.82547435950078e-5),
            "pt": (0.0423219848161192, 0.000533180817628955),
            "iht": (0.0724539373753259, 0.000950310898064908),
        },
    },
    "hoo": {
        "car": {
            "aht": (
                (0.00550037493956103, 0.0234162001700969),
                (0.000391905374911285, 0.0391186312800236),
            ),
            "pt": (
                (0.0201380534569954, 0.0133228060627617),
                (0.0124658801787879, 0.0109295959566237),
            ),
            "iht": (
                (0.0565009340812867, 0.0120147737621355),
                (0.0570183519842412, 0.0133201445543908),
            ),
        },
        "transit": {
            "aht": (
                (0.00382607878503005, 0.0155203879569167),
                (0.000736548266748814, 0.0397008009176757),
            ),
            "pt": (
                (0.019126221261485, 0.0122528030076379),
                (0.00951062844095834, 0.0106819487906973),
            ),
            "iht": (
                (0.0932381996592227, 0.0179250239591453),
                (0.0432468980113997, 0.00822557735282413),
            ),
        },
        "bike": {
            "aht": (
                (0, 0.0523112729277413),
                (0.00163405028001402, 0.0466164988927611),
            ),
            "pt": (
                (0.0199342812075618, 0.00851796828497718),
                (0.011231587806597, 0.010431086719673),
            ),
            "iht": (
                (0.101126018682501, 0.0109630774201843),
                (0.0729029180557304, 0.00716609669025943),
            ),
        },
        "walk": {
            "aht": (
                (0.00255136094336464, 0.0117062539991403),
                (0.00124294167977029, 0.0271635613942893),
            ),
            "pt": (
                (0.0272012495305256, 0.0099800486081729),
                (0.0147847622788628, 0.0106371302201477),
            ),
            "iht": (
                (0.0393174943303846, 0.0131329345163259),
                (0.0870917690839306, 0.0200469748108112),
            ),
        },
    },
    "wo": {
        "car": {
            "aht": (0.0149736650092181, 0.00869959631334979),
            "pt": (0.118537564467046, 0.00615679731239296),
            "iht": (0.0268293676484866, 0.0146327231238902),
        },
        "transit": {
            "aht": (0.0344112634112872, 0.147250698154569),
            "pt": (0.0426055865519115, 0.0100713869337193),
            "iht": (0.0355359725501345, 0.0655343660979877),
        },
        "bike": {
            "aht": (0.051360825273135, 0),
            "pt": (0.136200889229658, 0.00249187823048058),
            "iht": (0, 0.0232534698281509),
        },
        "walk": {
            "aht": (0.00695066700184841, 0.0022355088512395),
            "pt": (0.142956216767179, 0.00403101518983796),
            "iht": (0.0159929448887833, 0.00741683303050483),
        },
    },
    "oo": {
        "car": {
            "aht": (0.0123772155360135, 0.0265503034680466),
            "pt": (0.0476229814284928, 0.0104540834189332),
            "iht": (0.0724435968884137, 0.00416164627166021),
        },
        "transit": {
            "aht": (0.101341164670841, 0.0156026096077042),
            "pt": (0.0696207090086308, 0.00908262766695663),
            "iht": (0.0775970225401135, 0.00846853582212564),
        },
        "bike": {
            "aht": (0.0150684277360474, 0.00954229114757055),
            "pt": (0.0536101210823421, 0.0125814104800212),
            "iht": (0.0314951401591126, 0),
        },
        "walk": {
            "aht": (0.0333944312059417, 0.00208144914727809),
            "pt": (0.0900902068501387, 0.00176157285169458),
            "iht": (0.0490699347001694, 0.00111384146213679),
        },
    },
    "hwp": {
        "car": {
            "aht": (0.144753500812815, 0.00143940037269233),
            "pt": (0.0276354028917735, 0.000370213871920647),
            "iht": (0.132827490967523, 0.000385951788972209),
        },
        "transit": {
            "aht": (0.0746170908219579, 0),
            "pt": (0.0259307537785523, 0),
            "iht": (0.206291490317356, 0),
        },
    },
    "hop": {
        "car": {
            "aht": (0.0522419012319373, 0.000128437095882837),
            "pt": (0.0676510066763338, 0.000852007786488304),
            "iht": (0.0804041291969594, 0.00176130727770113),
        },
        "transit": {
            "aht": (0.165288235374047, 0),
            "pt": (0.0637946809570873, 0.00175229772247291),
            "iht": (0.056490691451754, 0.00867476245470596),
        },
    },
    "oop": {
        "car": {
            "aht": (0.0397584328389859, 0.0109075025884319),
            "pt": (0.113050311517589, 0.00438995883377368),
            "iht": (0.024128578417531, 0.00481021897699741),
        },
        "transit": {
            "aht": (0.188180692942718, 0),
            "pt": (0.0608373600842774, 0),
            "iht": (0.00680467801543412, 0.00563829554714879),
        },
    },
    "freight": {
        "trailer_truck": {
            "aht": (0.1, 0),
            "pt": (0.1, 0),
            "iht": (0.1, 0),
        },
        "truck": {
            "aht": (0.1, 0),
            "pt": (0.1, 0),
            "iht": (0.1, 0),
        },
        "van": {
            "aht": (0.1, 0),
            "pt": (0.1, 0),
            "iht": (0.1, 0),
        },
    },
    "external": {
        "car": {
            # This is a way of implementing road-specific parameters,
            # but it will work only with a fixed number of external zones,
            # so no testing is possible.
            # "aht": ([[0.01], [0.01]], [[0.01], [0.01]]),
            "aht": (0.01, 0.01),
            "pt": (0.05, 0.05),
            "iht": (0.05, 0.05),
        },
        "transit": {
            "aht": (0.01, 0.01),
            "pt": (0.05, 0.05),
            "iht": (0.05, 0.05),
        },
        "trailer_truck": {
            "aht": (0.1, 0),
            "pt": (0.1, 0),
            "iht": (0.1, 0),
        },
        "truck": {
            "aht": (0.1, 0),
            "pt": (0.1, 0),
            "iht": (0.1, 0),
        },
    },
}

impedance_share = {
    "hw": {
        "car": {
            "aht": (0.746026, 0.015065),
            "pt":  (0.234217, 0.329877),
            "iht": (0.019757, 0.655057),
        },
        "transit": {
            "aht": (0.746026, 0.015065),
            "pt":  (0.234217, 0.329877),
            "iht": (0.019757, 0.655057),
        },
        "bike": {
            "aht": (0, 0),
            "pt":  (1, 1),
            "iht": (0, 0),
        },
        "walk": {
            "aht": (0, 0),
            "pt":  (1, 1),
            "iht": (0, 0),
        },
    },
    "hc": {
        "car": {
            "aht": (0.811476, 0.000687),
            "pt":  (0.178970, 0.719189),
            "iht": (0.009555, 0.280124),
        },
        "transit": {
            "aht": (0.811476, 0.000687),
            "pt":  (0.178970, 0.719189),
            "iht": (0.009555, 0.280124),
        },
        "bike": {
            "aht": (0, 0),
            "pt":  (1, 1),
            "iht": (0, 0),
        },
        "walk": {
            "aht": (0, 0),
            "pt":  (1, 1),
            "iht": (0, 0),
        },
    },
    "hu": {
        "car": {
            "aht": (0.485475, 0.010482),
            "pt":  (0.430205, 0.609424),
            "iht": (0.084320, 0.380094),
        },
        "transit": {
            "aht": (0.485475, 0.010482),
            "pt":  (0.430205, 0.609424),
            "iht": (0.084320, 0.380094),
        },
        "bike": {
            "aht": (0, 0),
            "pt":  (1, 1),
            "iht": (0, 0),
        },
        "walk": {
            "aht": (0, 0),
            "pt":  (1, 1),
            "iht": (0, 0),
        },
    },
    "hs": {
        "car": {
            "aht": (0.096467, 0.042198),
            "pt":  (0.642764, 0.712821),
            "iht": (0.260769, 0.244981),
        },
        "transit": {
            "aht": (0.096467, 0.042198),
            "pt":  (0.642764, 0.712821),
            "iht": (0.260769, 0.244981),
        },
        "bike": {
            "aht": (0, 0),
            "pt":  (1, 1),
            "iht": (0, 0),
        },
        "walk": {
            "aht": (0, 0),
            "pt":  (1, 1),
            "iht": (0, 0),
        },
    },
    "ho": {
        "car": {
            "aht": (0.129790, 0.034834),
            "pt":  (0.573629, 0.778648),
            "iht": (0.296581, 0.186519),
        },
        "transit": {
            "aht": (0.129790, 0.034834),
            "pt":  (0.573629, 0.778648),
            "iht": (0.296581, 0.186519),
        },
        "bike": {
            "aht": (0, 0),
            "pt":  (1, 1),
            "iht": (0, 0),
        },
        "walk": {
            "aht": (0, 0),
            "pt":  (1, 1),
            "iht": (0, 0),
        },
    },
    "hoo": {
        "car": {
            "aht": (0, 0),
            "pt":  (0, 0),
            "iht": (0, 1),
        },
        "transit": {
            "aht": (0, 0),
            "pt":  (0, 0),
            "iht": (0, 1),
        },
        "bike": {
            "aht": (0, 0),
            "pt":  (0, 0),
            "iht": (0, 1),
        },
    },
    "so": {
        "car": {
            "aht": (0.462121, 0.024173),
            "pt":  (0.390587, 0.536630),
            "iht": (0.147292, 0.439198),
        },
        "transit": {
            "aht": (0.462121, 0.024173),
            "pt":  (0.390587, 0.536630),
            "iht": (0.147292, 0.439198),
        },
        "bike": {
            "aht": (0, 0),
            "pt":  (1, 1),
            "iht": (0, 0),
        },
        "walk": {
            "aht": (0, 0),
            "pt":  (1, 1),
            "iht": (0, 0),
        },
    },
    "wo": {
        "car": {
            "aht": (0.060857, 0.131316),
            "pt":  (0.781535, 0.785023),
            "iht": (0.157608, 0.083661),
        },
        "transit": {
            "aht": (0.060857, 0.131316),
            "pt":  (0.781535, 0.785023),
            "iht": (0.157608, 0.083661),
        },
        "bike": {
            "aht": (0, 0),
            "pt":  (1, 1),
            "iht": (0, 0),
        },
        "walk": {
            "aht": (0, 0),
            "pt":  (1, 1),
            "iht": (0, 0),
        },
    },
    "oo": {
        "car": {
            "aht": (0.129495, 0.055808),
            "pt":  (0.668475, 0.666841),
            "iht": (0.202030, 0.277352),
        },
        "transit": {
            "aht": (0.129495, 0.055808),
            "pt":  (0.668475, 0.666841),
            "iht": (0.202030, 0.277352),
        },
        "bike": {
            "aht": (0, 0),
            "pt":  (1, 1),
            "iht": (0, 0),
        },
        "walk": {
            "aht": (0, 0),
            "pt":  (1, 1),
            "iht": (0, 0),
        },
    },
    "hwp": {
        "car": {
            "aht": (0.679006, 0.031175),
            "pt":  (0.296493, 0.356524),
            "iht": (0.024502, 0.612301),
        },
        "transit": {
            "aht": (0.679006, 0.031175),
            "pt":  (0.296493, 0.356524),
            "iht": (0.024502, 0.612301),
        },
    },
    "hop": {
        "car": {
            "aht": (0.223073, 0.032569),
            "pt":  (0.532323, 0.708387),
            "iht": (0.244604, 0.259044),
        },
        "transit": {
            "aht": (0.223073, 0.032569),
            "pt":  (0.532323, 0.708387),
            "iht": (0.244604, 0.259044),
        },
    },
    "sop": {
        "car": {
            "aht": (0.538281, 0.031605),
            "pt":  (0.369282, 0.465128),
            "iht": (0.092437, 0.503267),
        },
        "transit": {
            "aht": (0.538281, 0.031605),
            "pt":  (0.369282, 0.465128),
            "iht": (0.092437, 0.503267),
        },
    },
    "oop": {
        "car": {
            "aht": (0.183770, 0.071658),
            "pt":  (0.714281, 0.754509),
            "iht": (0.101948, 0.173833),
        },
        "transit": {
            "aht": (0.183770, 0.071658),
            "pt":  (0.714281, 0.754509),
            "iht": (0.101948, 0.173833),
        },
    },
}

### DEMAND MODEL PARAMETERS ###

destination_choice = {
    "hw": {
        "car": {
            "attraction": {
                "parking_cost_work": -0.306967355090,
            },
            "impedance": {
                "time": -0.240311421071e-1,
                "cost": (-0.411197516348e-1, -0.976929479166e-1),
            },
            "log": {
                "size": 1.00000000000, # L_S_M
            },
            "size": {
                "cbd": (numpy.exp(4.82525484469), numpy.exp(5.46413339352)),
                "workplaces_own": (numpy.exp(0.326534462277), numpy.exp(0.914054873639)),
                "workplaces_other": 1,
            },
        },
        "transit": {
            "attraction": {
                "cbd": 0.483086068108,
            },
            "impedance": {
                "time": -0.111547282384e-1,
                "cost": ((-0.411197516348e-1) / 60, -0.976929479166e-1 / 44),
            },
            "log": {
                "size": 1.00000000000, # L_S_M
            },
            "size": {
                "cbd": (numpy.exp(4.82525484469), numpy.exp(5.46413339352)),
                "workplaces_own": (numpy.exp(0.326534462277), numpy.exp(0.914054873639)),
                "workplaces_other": 1,
            },
        },
        "bike": {
            "attraction": {},
            "impedance": {},
            "log": {
                "dist": (-1.11485765438, -1.35996965070),
                "size": 1.00000000000, # L_S_M
            },
            "size": {
                "cbd": (numpy.exp(4.82525484469), numpy.exp(5.46413339352)),
                "workplaces_own": (numpy.exp(0.326534462277), numpy.exp(0.914054873639)),
                "workplaces_other": 1,
            },
        },
        "walk": {
            "attraction": {
                "own_zone_area_sqrt": (-2.14509122337, -2.07210556201),
            },
            "impedance": {},
            "log": {
                "dist": -2.66058468415,
                "size": 1.00000000000, # L_S_M
            },
            "size": {
                "cbd": (numpy.exp(4.82525484469), numpy.exp(5.46413339352)),
                "workplaces_own": (numpy.exp(0.326534462277), numpy.exp(0.914054873639)),
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
                "cbd": 0.704345842211,
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
                    "cost": (1/60, 1/44),
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
                "own_zone_area_sqrt": -3.87680793384,
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
                "parking_cost_work": -0.354136146210,
            },
            "impedance": {
                "time": -0.312118189213e-1,
                "cost": -0.216784178710,
            },
            "log": {
                "size": 1.00000000000, # L_S_M
            },
            "size": {
                "secondary_schools": numpy.exp(-1.22533543313),
                "tertiary_education": 1,
            },
        },
        "transit": {
            "attraction": {
                "cbd": 0.145833772041,
            },
            "impedance": {
                "time": -0.136559859790e-1,
                "cost": (-0.216784178710 / 60, -0.216784178710 / 44)
            },
            "log": {
                "size": 1.00000000000,
            },
            "size": {
                "secondary_schools": numpy.exp(-1.22533543313),
                "tertiary_education": 1,
            },
        },
        "bike": {
            "attraction": {},
            "impedance": {
                "dist": -1.71018514578,
            },
            "log": {
                "size": 1.00000000000,
            },
            "size": {
                "secondary_schools": numpy.exp(-1.22533543313),
                "tertiary_education": 1,
            },
        },
        "walk": {
            "attraction": {
                "own_zone_area_sqrt": -2.28325100532,
            },
            "impedance": {},
            "log": {
                "dist": -3.32917729353,
                "size": 1.00000000000,
            },
            "size": {
                "secondary_schools": numpy.exp(-1.22533543313),
                "tertiary_education": 1,
            },
        },
    },
    "hs": {
        "car": {
            "attraction": {
                "parking_cost_errand": -0.131053326543,
            },
            "impedance": {
                "time": -0.960814824614e-1,
                "cost": -0.112450201944,
            },
            "log": {
                "size": 1.00000000000, # L_S_M
            },
            "size": {
                "population_other": 1,
                "population_own": numpy.exp(1.58732389618),
                "shops_other": numpy.exp(6.24804591506),
                "shops_own": (numpy.exp(6.19259580740), numpy.exp(7.10231579547)),
                "service_other": numpy.exp(3.77954709039),
                "service_own": (numpy.exp(4.53224477260), numpy.exp(5.13038361124)),
                "cbd": (numpy.exp(9.04364663102), numpy.exp(7.19898499824)),
            },
        },
        "transit": {
            "attraction": {
                "cbd": (0.135335656706, 2.62480475297),
            },
            "impedance": {
                "time": -0.299237931923e-1,
                "cost": -0.112450201944 / 30,
            },
            "log": {
                "size": 1.00000000000,
            },
            "size": {
                "population_other": 1,
                "population_own": numpy.exp(1.58732389618),
                "shops_other": numpy.exp(6.24804591506),
                "shops_own": (numpy.exp(6.19259580740), numpy.exp(7.10231579547)),
                "service_other": numpy.exp(3.77954709039),
                "service_own": (numpy.exp(4.53224477260), numpy.exp(5.13038361124)),
                "cbd": (numpy.exp(9.04364663102), numpy.exp(7.19898499824)),
            },
        },
        "bike": {
            "attraction": {},
            "impedance": {},
            "log": {
                "dist": (-1.93990622922, -1.65381682081),
                "size": 1.00000000000,
            },
            "size": {
                "population_other": 1,
                "population_own": numpy.exp(1.58732389618),
                "shops_other": numpy.exp(6.24804591506),
                "shops_own": (numpy.exp(6.19259580740), numpy.exp(7.10231579547)),
                "service_other": numpy.exp(3.77954709039),
                "service_own": (numpy.exp(4.53224477260), numpy.exp(5.13038361124)),
                "cbd": (numpy.exp(9.04364663102), numpy.exp(7.19898499824)),
            },
        },
        "walk": {
            "attraction": {
                "own_zone_area_sqrt": (-3.44256406401, -4.67197096996),
                "population_density": 0.212083748622e-4,
            },
            "impedance": {},
            "log": {
                "dist": -3.98943568695,
                "size": 1.00000000000,
            },
            "size": {
                "population_other": 1,
                "population_own": numpy.exp(1.58732389618),
                "shops_other": numpy.exp(6.24804591506),
                "shops_own": (numpy.exp(6.19259580740), numpy.exp(7.10231579547)),
                "service_other": numpy.exp(3.77954709039),
                "service_own": (numpy.exp(4.53224477260), numpy.exp(5.13038361124)),
                "cbd": (numpy.exp(9.04364663102), numpy.exp(7.19898499824)),
            },
        },
    },
    "ho": {
        "car": {
            "attraction": {
                "own_zone": -0.146221054,
                "parking_cost_errand": -0.24573436,
            },
            "impedance": {
                "time": -0.034134566,
            },
            "log": {
                "cost": -0.922540003,
                "size": 1,
            },
            "size": {
                "population_other": 1,
                "population_own": numpy.exp(1.205650309),
                "service_other": numpy.exp(2.384174142),
                "service_own": numpy.exp(3.183207081),
                "shops": numpy.exp(2.998477655),
                "cbd": (numpy.exp(7.813868577), numpy.exp(4.709424332)),
            },
        },
        "transit": {
            "attraction": {
                "own_zone": -2.139067338,
                "cbd": 0.569673156,
            },
            "impedance": {
                "time": -0.018376845,
            },
            "log": {
                "transform": -0.922540003,
                "size": 1,
            },
            "size": {
                "population_other": 1,
                "population_own": numpy.exp(1.205650309),
                "service_other": numpy.exp(2.384174142),
                "service_own": numpy.exp(3.183207081),
                "shops": numpy.exp(2.998477655),
                "cbd": (numpy.exp(7.813868577), numpy.exp(4.709424332)),
            },
            "transform": {
                "attraction": {},
                "impedance": {
                    "cost": 1/30,
                },
            },
        },
        "bike": {
            "attraction": {},
            "impedance": {},
            "log": {
                "dist": (-1.840032015, -1.657687972),
                "size": 1,
            },
            "size": {
                "population_other": 1,
                "population_own": numpy.exp(1.205650309),
                "service_other": numpy.exp(2.384174142),
                "service_own": numpy.exp(3.183207081),
                "shops": numpy.exp(2.998477655),
                "cbd": (numpy.exp(7.813868577), numpy.exp(4.709424332)),
            },
        },
        "walk": {
            "attraction": {
                "own_zone_area_sqrt": (-1.139032362, -1.012079317),
                "population_density": -4.18771E-05,
            },
            "impedance": {},
            "log": {
                "dist": -3.701172838,
                "size": 1,
            },
            "size": {
                "population_other": 1,
                "population_own": numpy.exp(1.205650309),
                "service_other": numpy.exp(2.384174142),
                "service_own": numpy.exp(3.183207081),
                "shops": numpy.exp(2.998477655),
                "cbd": (numpy.exp(7.813868577), numpy.exp(4.709424332)),
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
                "cost": -0.071273703 / 30,
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
    "so": {
        "logsum": {
            "attraction": {
                "own_zone": 0.578607605,
            },
            "impedance": {},
            "log": {
                "logsum": 1.011586109,
                "size": 0.814168308,
            },
            "size": {
                "population": 1,
                "workplaces": 2.572258993,
                "cbd": (1, 5.674738917), # Fix
            },
        },
    },
    "wo": {
        "car": {
            "attraction": {
                "parking_cost_errand": -0.306197294,
            },
            "impedance": {
                "time": -0.064566099,
            },
            "log": {
                "cost": -0.722944564,
                "size": 1,
            },
            "size": {
                "population": 1,
                "workplaces": numpy.exp(0.407701749),
                "service": numpy.exp(1.500860632),
                "shops_cbd": numpy.exp(3.473356486),
                "shops_elsewhere": numpy.exp(3.32217248),
                "own_zone": numpy.exp(6.64854455),
            },
        },
        "transit": {
            "attraction": {
                "cbd": 0.287337989,
                "own_zone": -2.001694496,
            },
            "impedance": {
                "time": -0.023467029,
            },
            "log": {
                "transform": -0.722944564,
                "size": 1,
            },
            "size": {
                "population": 1,
                "workplaces": numpy.exp(0.407701749),
                "service": numpy.exp(1.500860632),
                "shops_cbd": numpy.exp(3.473356486),
                "shops_elsewhere": numpy.exp(3.32217248),
                "own_zone": numpy.exp(6.64854455),
            },
            "transform": {
                "attraction": {},
                "impedance": {
                    "cost": 1/30,
                },
            },
        },
        "bike": {
            "attraction": {},
            "impedance": {},
            "log": {
                "dist": (-2.050036721, -1.837765569),
                "size": 1,
            },
            "size": {
                "population": 1,
                "workplaces": numpy.exp(0.407701749),
                "service": numpy.exp(1.500860632),
                "shops_cbd": numpy.exp(3.473356486),
                "shops_elsewhere": numpy.exp(3.32217248),
                "own_zone": numpy.exp(6.64854455),
            },
        },
        "walk": {
            "attraction": {
                "own_zone_area_sqrt": (-0.959191593, -1.704599482),
            },
            "impedance": {},
            "log": {
                "dist": -3.346606131,
                "size": 1,
            },
            "size": {
                "population": 1,
                "workplaces": numpy.exp(0.407701749),
                "service": numpy.exp(1.500860632),
                "shops_cbd": numpy.exp(3.473356486),
                "shops_elsewhere": numpy.exp(3.32217248),
                "own_zone": numpy.exp(6.64854455),
            },
        },
    },
    "oo": {
        "car": {
            "attraction": {
                "parking_cost_errand": -0.306197294,
            },
            "impedance": {
                "time": -0.064566099,
            },
            "log": {
                "cost": -0.722944564,
                "size": 1,
            },
            "size": {
                "population": 1,
                "workplaces": numpy.exp(0.407701749),
                "service": numpy.exp(1.500860632),
                "shops_cbd": numpy.exp(3.473356486),
                "shops_elsewhere": numpy.exp(3.32217248),
                "own_zone": numpy.exp(6.64854455),
            },
        },
        "transit": {
            "attraction": {
                "cbd": 0.287337989,
                "own_zone": -2.001694496,
            },
            "impedance": {
                "time": -0.023467029,
            },
            "log": {
                "transform": -0.722944564,
                "size": 1,
            },
            "size": {
                "population": 1,
                "workplaces": numpy.exp(0.407701749),
                "service": numpy.exp(1.500860632),
                "shops_cbd": numpy.exp(3.473356486),
                "shops_elsewhere": numpy.exp(3.32217248),
                "own_zone": numpy.exp(6.64854455),
            },
            "transform": {
                "attraction": {},
                "impedance": {
                    "cost": 1/30,
                },
            },
        },
        "bike": {
            "attraction": {},
            "impedance": {},
            "log": {
                "dist": (-2.050036721, -1.837765569),
                "size": 1,
            },
            "size": {
                "population": 1,
                "workplaces": numpy.exp(0.407701749),
                "service": numpy.exp(1.500860632),
                "shops_cbd": numpy.exp(3.473356486),
                "shops_elsewhere": numpy.exp(3.32217248),
                "own_zone": numpy.exp(6.64854455),
            },
        },
        "walk": {
            "attraction": {
                "own_zone_area_sqrt": (-0.959191593, -1.704599482),
            },
            "impedance": {},
            "log": {
                "dist": -3.346606131,
                "size": 1,
            },
            "size": {
                "population": 1,
                "workplaces": numpy.exp(0.407701749),
                "service": numpy.exp(1.500860632),
                "shops_cbd": numpy.exp(3.473356486),
                "shops_elsewhere": numpy.exp(3.32217248),
                "own_zone": numpy.exp(6.64854455),
            },
        },
    },
    "hwp": {
        "car": {
            "attraction": {
                "parking_cost_work": -0.167648454911,
                "share_detached_houses": 0.579675740565e-2,
                "own_zone_area": -0.194842606662e-1,
            },
            "impedance": {
                "time": -0.188031062001e-1,
                "cost": -0.167648454911,
            },
            "log": {
                "size": 0.906272269187, # LN_Size
            },
            "size": {
                "workplaces": 1,
            },
        },
        "transit": {
            "attraction": {
                "cbd": 0.490942327168,
                "own_zone_area": -0.112492660238,
            },
            "impedance": {
                "time": -0.808893404926e-2,
                "cost": -0.167648454911 / 44,
            },
            "log": {
                "size": 0.906272269187, # LN_Size
            },
            "size": {
                "workplaces": 1,
            },
        },
    },
    "hop": {
        "car": {
            "attraction": {
                "car_density": 1000 * 0.187305245180e-2,
                "own_zone_area": -0.138197654412e-1,
            },
            "impedance": {
                "time": -0.288481815905e-1,
                "cost": -0.188691214282,
            },
            "log": {
                "size": 1, # L_S_M
            },
            "size": {
                "workplaces": numpy.exp(1.07808303849),
                "service": numpy.exp(4.57535345257),
                "shops": numpy.exp(5.35085890989),
                "comprehensive_schools": numpy.exp(2.40450824304),
                "population_own": numpy.exp(3.28776000706),
                "population_other": 1,
            },
        },
        "transit": {
            "attraction": {},
            "impedance": {
                "time": -0.552308836126e-2,
                "cost": -0.188691214282 / 30,
            },
            "log": {
                "size": 1, # L_S_M
            },
            "size": {
                "workplaces": numpy.exp(1.07808303849),
                "service": numpy.exp(4.57535345257),
                "shops": numpy.exp(5.35085890989),
                "comprehensive_schools": numpy.exp(2.40450824304),
                "population_own": numpy.exp(3.28776000706),
                "population_other": 1,
            },
        },
    },
    "sop": {
        "attraction": {
            "parking_cost_errand": 0.94 * -0.609e-1,
            "population_density": -0.109e-3,
        },
        "impedance": {
            "car": {
                "cost": 0.94 * -0.609e-1,
                "time": 0.94 * -0.264e-1,
            },
            "transit": {
                "cost": 0.04 * (-0.609e-1) / 30,
                "time": 0.04 * -0.264e-1,
            },
        },
        "log": {
            "size": 1,
        },
        "size": {
            "workplaces": numpy.exp(2.53759200723),
            "population_own": numpy.exp(1.17058855327),
            "population_other": 1,
        },
    },
    "oop": {
        "car": {
            "attraction": {
                "parking_cost_errand": -0.227398812175,
            },
            "impedance": {
                "time": -0.427365675012e-1,
                "cost": -0.227398812175,
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
        "transit": {
            "attraction": {
                "cbd": 2.84600723332,
            },
            "impedance": {
                "time": -0.819579857062e-2,
                "cost": -0.227398812175 / 30,
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
mode_choice = {
    "hw": {
        "car": {
            "constant": 0,
            "generation": {
                "car_density": (0.844179295926 * 1000 * 0.286886466040e-2, 0.844179295926 * 1000 * 0.412205399149e-2),
            },
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": 0.844179295926,
            },
            "individual_dummy": {
                "car_users": (0.844179295926 * 2.99432056907, 0.844179295926 * 2.90130969119),
            },
        },
        "transit": {
            "constant": (0.844179295926 * 3.15335645065, 0.844179295926 * 3.09257722177),
            "generation": {},
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": 0.844179295926,
            },
            "individual_dummy": {},
        },
        "bike": {
            "constant": (0.844179295926 * 3.65997812160, 0.844179295926 * 4.10083690370),
            "generation": {},
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": 0.844179295926,
            },
            "individual_dummy": {},
        }, 
        "walk": {
            "constant": (0.844179295926 * 6.06426484277, 0.844179295926 * 6.31407702335),
            "generation": {},
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": 0.844179295926,
            },
            "individual_dummy": {},
        },
    },
    "hc": {
        "car": {
            "constant": 0,
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
            "constant": 0.272803753976 * 13.2817160786,
            "generation": {},
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": 0.272803753976, # Dcoeff
            },
            "individual_dummy": {},
        },
        "bike": {
            "constant": 0.272803753976 * 11.3490028510,
            "generation": {},
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": 0.272803753976, # Dcoeff
            },
            "individual_dummy": {},
        },  
        "walk": {
            "constant": 0.272803753976 * 17.7784859496,
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
            "constant": 0,
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
            "constant": 3.10747422821,
            "generation": {},
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": 1.00000000000,
            },
            "individual_dummy": {},
        },
        "bike": {
            "constant": 3.23689689401,
            "generation": {},
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": 1.00000000000,
            },
            "individual_dummy": {},
        },  
        "walk": {
            "constant": 6.15888890793,
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
            "constant": 0,
            "generation": {
                "car_density": (0.539979474415 * 1000 * 0.952522128478e-2, 0.539979474415 * 1000 * 0.156268961848e-1),
            },
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": 0.539979474415, # Dcoeff
            },
            "individual_dummy": {
                "car_users": (0.539979474415 * 4.35523030487, 0.539979474415 * 3.46844128674),
            },
        },
        "transit": {
            "constant": (0.539979474415 * 5.13091589060, 0.539979474415 * 4.98462338486),
            "generation": {},
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": 0.539979474415,
            },
            "individual_dummy": {},
        },
        "bike": {
            "constant": (0.539979474415 * 3.98060152237, 0.539979474415 * 7.26646802781),
            "generation": {},
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": 0.539979474415,
            },
            "individual_dummy": {},
        },  
        "walk": {
            "constant": (0.539979474415 * 10.8293044790, 0.539979474415 * 12.6937820419),
            "generation": {},
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": 0.539979474415,
            },
            "individual_dummy": {},
        },
    },
    "ho": {
        "car": {
            "constant": 0,
            "generation": {
                "car_density": (0.151688898 * 1000 * 0.029028726, 0.151688898 * 1000 * 0.010179897),
            },
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": 0.151688898,
            },
            "individual_dummy": {
                "car_users": (0.151688898 * 4.597793819, 0.151688898 * 3.107665106),
            },
        },
        "transit": {
            "constant": (0.151688898 * 8.71611785, 0.151688898 * -9.326014274),
            "generation": {},
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": 0.151688898,
            },
            "individual_dummy": {},
        },
        "bike": {
            "constant": (0.151688898 * 5.077652282, 0.151688898 * -1.017242495),
            "generation": {},
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": 0.151688898,
            },
            "individual_dummy": {},
        },  
        "walk": {
            "constant": (0.151688898 * 20.72419038, 0.151688898 * 12.53617415),
            "generation": {},
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": 0.151688898,
            },
            "individual_dummy": {},
        },
    },
    "hoo": None,
    "so": {
        "car": {
            "constant": 0,
            "generation": {},
            "attraction": {
                "parking_cost_work": -0.35058138,
            },
            "impedance": {
                "time": -0.021901628,
                "cost": -0.10378753,
            },
            "log": {},
            "individual_dummy": {},
        },
        "transit": {
            "constant": 0.437744247,
            "generation": {},
            "attraction": {
                "cbd": 0.502605142,
            },
            "impedance": {
                "time": -0.015704891,
                "cost": -0.10378753 / 30,
            },
            "log": {},
            "individual_dummy": {},
        },
        "bike": {
            "constant": 0.911203717,
            "generation": {},
            "attraction": {},
            "impedance": {},
            "log": {
                "dist": -1.292779721,
            },
            "individual_dummy": {},
        },  
        "walk": {
            "constant": 3.309720696,
            "generation": {},
            "attraction": {
                "own_zone_area_sqrt": -2.154849688,
            },
            "impedance": {},
            "log": {
                "dist": -2.70272318,
            },
            "individual_dummy": {},
        },
    },
    "wo": {
        "car": {
            "constant": 0,
            "generation": {
                "car_density": (0.799256902 * 1000 * 0.002492582, 0.799256902 * 1000 * 0.001638454),
            },
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": 0.799256902,
            },
            "individual_dummy": {},
        },
        "transit": {
            "constant": 0.799256902 * 2.739088214,
            "generation": {},
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": 0.799256902,
            },
            "individual_dummy": {},
        },
        "bike": {
            "constant": (0.799256902 * 0.854636531, 0.799256902 * 1.245322555),
            "generation": {},
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": 0.799256902,
            },
            "individual_dummy": {},
        },  
        "walk": {
            "constant": 0.799256902 * 6.416635051,
            "generation": {},
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": 0.799256902,
            },
            "individual_dummy": {},
        },
    },
    "oo": {
        "car": {
            "constant": 0,
            "generation": {
                "car_density": (0.799256902 * 1000 * 0.002492582, 0.799256902 * 1000 * 0.001638454),
            },
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": 0.799256902,
            },
            "individual_dummy": {},
        },
        "transit": {
            "constant": 0.799256902 * 2.739088214,
            "generation": {},
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": 0.799256902,
            },
            "individual_dummy": {},
        },
        "bike": {
            "constant": (0.799256902 * 0.854636531, 0.799256902 * 1.245322555),
            "generation": {},
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": 0.799256902,
            },
            "individual_dummy": {},
        },  
        "walk": {
            "constant": 0.799256902 * 6.416635051,
            "generation": {},
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": 0.799256902,
            },
            "individual_dummy": {},
        },
    },
    "hwp": {
        "car": {
            "constant": 0,
            "generation": {},
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": 1.00000000000, # Dcoeff
            },
            "individual_dummy": {},
        },
        "transit": {
            "constant": -1.79569982464, # T_const
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
            "constant": 0,
            "generation": {},
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": 1.00000000000,
            },
            "individual_dummy": {},
        },
        "transit": {
            "constant": -1.26883605707,
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
        "all": {
            "individual_dummy": {},
        },
    },
    "oop": {
        "car": {
            "constant": 0,
            "generation": {},
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": 0.715272183645,
            },
            "individual_dummy": {},
        },
        "transit": {
            "constant": 0.715272183645 * -3.44371464477,
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
tour_patterns = {
    0: {},
    1: {
        "hw": {
            "individual_dummy": {
                "share_age_18-29": 3.5,
            },
        },
    },
    2: {
        "hw-ho": {
            "individual_dummy": {
                "share_age_18-29": 3.5,
            },
        },
    },
}
tour_generation = {
    "hw": {
        "population": 0.428264806,
    },
    "hc": {
        "population": 0.118155143,
    },
    "hu": {
        "population": 0.057333814,
    },
    "hs": {
        "population": 0.339996241,
    },
    "ho": {
        "population": 0.558925061,
    },
    "hoo": {
        "hw": 0.172863550 / 0.428264806,
        "hc": 0.024415337 / 0.118155143,
        "hu": 0.022225799 / 0.057333814,
        "hs": 0.081158959 / 0.339996241,
        "ho": 0.078710513 / 0.558925061,
        "wo": 0.006012753 / 0.065687335,
        "oo": 0.007727243 / 0.067638093,
    },
    "so": {
        "population": 0.133325428,
    },
    "wo": {
        # Some so trips continue with wo trips
        "so": 0.065687335 / 0.133325428,
    },
    "oo": {
        # Some so trips continue with oo trips
        "so": 0.067638093 / 0.133325428,
    },
    "hwp": {
        "population": 0.237579403,
    },
    "hop": {
        "population": 0.561035077,
    },
    "sop": {
        "population": 0.050959288,
    },
    "oop": {
        # Every sop trip continues with oop trip
        "sop": 1,
    },
    "truck": {
        "population": 0.01,
        "workplaces": 0.025,
        "logistics": 0.35,
        "industry": 0.035,
        "shops": 0.05,
    },
    "trailer_truck": {
        "population": None,
        "workplaces": 0.005,
        "logistics": 0.38,
        "industry": 0.038,
        "shops": 0.005,
    }
}
garbage_generation = {
    "population": 0.000125,
    "workplaces": 0.000025,
}
car_usage = {
    "constant": -11.2296,
    "generation": {},
    "log": {
        "cars_per_1000": 2.0804,
        "population_density": -0.1471,
    },
    "individual_dummy": {
        "share_age_7-17": -9999,
        "share_age_18-29_m": 0.2969,
        "share_age_30-49_f": 1.1019,
        "share_age_30-49_m": 1.4157,
        "share_age_50-64_f": 0.8173,
        "share_age_50-64_m": 1.9978,
        "share_age_65-99_m": 1.8737,
    },
}
vector_calibration_threshold = 5
# Maximum possible distance to destination
distance_boundary = {
    "car": 9999,
    "transit": 9999,
    "bike": 60,
    "walk": 15,
}
### DEMAND MODEL REFERENCES ###

tour_purposes = (
    {
        "name": "hw",
        "orig": "home",
        "dest": "work",
        "area": "metropolitan",
    },
    {
        "name": "hc",
        "orig": "home",
        "dest": "comprehensive_school",
        "area": "metropolitan",
    },
    {
        "name": "hu",
        "orig": "home",
        "dest": "tertiary_education",
        "area": "metropolitan",
    },
    {
        "name": "hs",
        "orig": "home",
        "dest": "shopping",
        "area": "metropolitan",
    },
    {
        "name": "ho",
        "orig": "home",
        "dest": "other",
        "area": "metropolitan",
    },
    {
        "name": "hoo",
        "orig": "home",
        "dest": "any",
        "sec_dest": "any",
        "source": ("hw", "ho",),
        "area": "all",
    },
    {
        "name": "so",
        "orig": "home",
        "dest": "source",
        "area": "metropolitan",
    },
    {
        "name": "wo",
        "orig": "source",
        "dest": "other",
        "source": ("so",),
        "area": "all",
    },
    {
        "name": "oo",
        "orig": "source",
        "dest": "other",
        "source": ("so",),
        "area": "all",
    },
    {
        "name": "hwp",
        "orig": "home",
        "dest": "work",
        "area": "peripheral",
    },
    {
        "name": "hop",
        "orig": "home",
        "dest": "other",
        "area": "peripheral",
    },
    {
        "name": "sop",
        "orig": "home",
        "dest": "source",
        "area": "peripheral",
    },
    {
        "name": "oop",
        "orig": "source",
        "dest": "other",
        "source": ("sop",),
        "area": "all",
    },
)

external_modes = [
    "car",
    "transit",
    "truck",
    "trailer_truck",
]
areas = {
    "helsinki_cbd": (0, 999),
    "helsinki_other": (1000, 1999),
    "espoo_vant_kau": (2000, 5999),
    "surrounding": (6000, 15999),
    "peripheral": (16000, 30999),
    "external": (31031, None),
}
municipality = {
    "Helsinki": (0, 1999),
    "Espoo": (2000, 3499),
    "Kauniainen": (3500, 3999),
    "Vantaa": (4000, 5999),
    "Kirkkonummi": (6000, 6999),
    "Vihti": (7000, 7999),
    "Nurmijarvi": (8000, 8999),
    "Tuusula": (9000, 9999),
    "Kerava": (10000, 10999),
    "Jarvenpaa": (11000, 11999),
    "Sipoo": (12000, 12999),
    "Mantsala": (13000, 13999),
    "Hyvinkaa": (14000, 14999),
    "Pornainen": (15000, 15499),
    "Siuntio": (15500, 15999),
    "Salo": (16000, 16499),
    "Somero": (16500, 16999),
    "Raasepori": (17000, 17499),
    "Hanko": (17500, 17499),
    "Inkoo": (18000, 18499),
    "Karkkila": (18500, 18999),
    "Lohja": (19000, 19999),
    "Hameenlinna": (20000, 20999),
    "Janakkala": (21000, 21499),
    "Hattula": (21500, 21999),
    "Loppi": (22000, 22499),
    "Tammela": (22500, 22999),
    "Riihimaki": (23000, 23999),
    "Hausjarvi": (24000, 24499),
    "Karkola": (24500, 24999),
    "Orimattila": (25000, 25499),
    "Hollola": (25500, 25999),
    "Lahti": (26000, 26999),
    "Porvoo": (27000, 27999),
    "Pukkila": (28000, 28499),
    "Askola": (28500, 28999),
    "Myrskyla": (29000, 29499),
    "Lapinjarvi": (29500, 29999),
    "Loviisa": (30000, 30999),
}
