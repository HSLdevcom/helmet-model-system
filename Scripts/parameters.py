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
# Default distance unit cost [eur/km]
dist_unit_cost = 0.12
# Boarding penalties for different transit modes
boarding_penalty = {
    "b": 3, # Bus
    "g": 3, # Trunk bus
    "d": 5, # Long-distance bus
    "e": 5, # Express bus
    "t": 0, # Tram
    "p": 0, # Light rail
    "m": 0, # Metro
    "w": 0, # Ferry
    "r": 2, # Commuter train
    "j": 2, # Long-distance train
}
last_boarding_penalty = {
    "b": 3, # Bus
    "g": 3, # Trunk bus
    "d": 5, # Long-distance bus
    "e": 5, # Express bus
    "t": 0, # Tram
    "p": 0, # Light rail
    "m": 0, # Metro
    "w": 0, # Ferry
    "r": 2, # Commuter train
    "j": 2, # Long-distance train
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
    "max_iterations": 50,
    "normalized_gap": 0.01,
    "relative_gap": 0.001
}
# Specification for the transit assignment
transfer_penalty = {
    "transit_work": 5,
    "transit_leisure": 7,
    "transit": 5,
}
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
transit_classes = (
    "transit_work",
    "transit_leisure",
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
# Link attributes initialized 
# in helmet-model-system 
emme_attributes = {
    "@bus": "LINK",
    "@total_cost": "LINK",
    "@toll_cost": "LINK",
    "@wait_time_dev": "TRANSIT_SEGMENT",
    "@car_work": "LINK",
    "@car_leisure": "LINK",
    "@transit_work_vol": "TRANSIT_SEGMENT",
    "@transit_leisure_vol": "TRANSIT_SEGMENT",
    "@transit_work_boa": "TRANSIT_SEGMENT",
    "@transit_leisure_boa": "TRANSIT_SEGMENT",
    "@transit_work_trb": "TRANSIT_SEGMENT",
    "@transit_leisure_trb": "TRANSIT_SEGMENT",
    "@trailer_truck": "LINK",
    "@truck": "LINK",
    "@van": "LINK", 
    "@transit_vol": "TRANSIT_SEGMENT",
    "@transit_boa": "TRANSIT_SEGMENT",
    "@transit_trb": "TRANSIT_SEGMENT",
}
bike_attributes = {
    "@bike_aht": "LINK",
    "@bike_iht": "LINK",
    "@bike_pt": "LINK",
    "@bike_day": "LINK",
}
transit_assignment_modes = transit_modes + aux_modes
# Link attribute for volumes
link_volumes = {
    "car_work": "@car_work",
    "car_leisure": "@car_leisure",
    "trailer_truck": "@trailer_truck",
    "truck": "@truck",
    "van": "@van",
    "bus": "@bus"
    }
# Factors for 24-h expansion of volumes
# TODO: Trucks and vans
volume_factors = {
    "car": {
        "aht": 1. / 0.465,
        "pt": 1. / 0.094,
        "iht": 1. / 0.369,
    },
    "car_work": {
        "aht": 1. / 0.456,
        "pt": 1. / 0.102,
        "iht": 1. / 0.433,
    },
    "car_leisure": {
        "aht": 1. / 0.488,
        "pt": 1. / 0.089,
        "iht": 1. / 0.289,
    },
    "transit": {
        "aht": 1. / 0.478,
        "pt": 1. / 0.109,
        "iht": 1. / 0.405,
    },
    "transit_work": {
        "aht": 1. / 0.445,
        "pt": 1. / 0.103,
        "iht": 1. / 0.414,
    },
    "transit_leisure": {
        "aht": 1. / 0.571,
        "pt": 1. / 0.117,
        "iht": 1. / 0.373,
    },
    "bike": {
        "aht": 1. / 0.604,
        "pt": 1. / 0.105,
        "iht": 1. / 0.430,
    },
    "bike_work": {
        "aht": 1. / 0.542,
        "pt": 1. / 0.109,
        "iht": 1. / 0.500,
    },
    "bike_leisure": {
        "aht": 1. / 0.725,
        "pt": 1. / 0.103,
        "iht": 1. / 0.332,
    },
    "trailer_truck": {
        "aht": 1 / 0.3,
        "pt": 1 / 0.1,
        "iht": 1 / 0.3,
    },
    "truck": {
         "aht": 1 / 0.3,
        "pt": 1 / 0.1,
        "iht": 1 / 0.3,
    },
    "van": {
        "aht": 1 / 0.3,
        "pt": 1 / 0.1,
        "iht": 1 / 0.3,
    },
    "bus": {
        "aht": 1 / 0.497, 
        "pt": 1 / 0.090, 
        "iht": 1 / 0.497,
    },
}
# Emme matrix IDs
emme_demand_mtx = {
    "car_work": {
        "id": "mf1",
        "description": "car work demand",
    },
    "car_leisure": {
        "id": "mf2",
        "description": "car leisure demand",
    },
    "transit_work":  {
        "id":"mf3",
        "description": "transit demand",
    },
    "transit_leisure":  {
        "id":"mf4",
        "description": "transit demand",
    },
    "bike":  {
        "id":"mf5",
        "description": "bicyclist demand",
    },
    "trailer_truck": {
        "id": "mf7",
        "description": "trailer truck demand",
    },
    "truck":  {
        "id":"mf8",
        "description": "truck demand",
    },
    "van":  {
        "id":"mf9",
        "description": "van demand",
    },
}
emme_result_mtx = {
    "time": {
        "car_work": {
            "id": "mf11",
            "description": "car work travel time",
        },
        "car_leisure": {
            "id": "mf12",
            "description": "car leisure travel time",
        },
        "transit_work": {
            "id": "mf13",
            "description": "transit travel time",
        },
        "transit_leisure": {
            "id": "mf14",
            "description": "transit travel time",
        },
        "bike": {
            "id": "mf15",
            "description": "bike travel time",
        },
        "walk": {
            "id": "mf16",
            "description": "walk travel time",
        },
        "trailer_truck": {
            "id": "mf17",
            "description": "trailer truck time",
        },
        "truck":  {
            "id":"mf18",
            "description": "truck time",
        },
        "van":  {
            "id":"mf19",
            "description": "van time",
        },
    },
    "dist": {
        "car_work": {
            "id": "mf21",
            "description": "car work travel distance",
        },
        "car_leisure": {
            "id": "mf22",
            "description": "car leisure travel distance",
        },
        "transit_work": {
            "id": "mf23",
            "description": "transit in-vehicle distance",
        },
        "transit_leisure": {
            "id": "mf24",
            "description": "transit in-vehicle distance",
        },
        "bike": {
            "id": "mf25",
            "description": "bike travel distance",
        },
        "walk": {
            "id": "mf26",
            "description": "walk travel distance",
        },
        "trailer_truck": {
            "id": "mf27",
            "description": "trailer truck distance",
        },
        "truck":  {
            "id":"mf28",
            "description": "truck distance",
        },
        "van":  {
            "id":"mf29",
            "description": "van distance",
        },
    },
    "cost": {
        "car_work": {
            "id": "mf31",
            "description": "car work travel cost",
        },
        "car_leisure": {
            "id": "mf32",
            "description": "car leisure travel cost",
        },
        "transit_work": {
            "id": "mf33",
            "description": "transit travel cost",
        },
        "transit_leisure": {
            "id": "mf34",
            "description": "transit travel cost",
        },
        "trailer_truck": {
            "id": "mf37",
            "description": "trailer truck cost",
        },
        "truck":  {
            "id":"mf38",
            "description": "truck cost",
        },
        "van":  {
            "id":"mf39",
            "description": "van cost",
        },
    },
    "gen_cost": {
        "car_work": {
            "id": "mf41",
            "description": "car work travel generalized cost",
        },
        "car_leisure": {
            "id": "mf42",
            "description": "car leisure travel generalized cost",
        },
        "trailer_truck": {
            "id": "mf47",
            "description": "trailer truck travel generalized cost",
        },
        "truck":  {
            "id":"mf48",
            "description": "truck travel generalized cost",
        },
        "van":  {
            "id":"mf49",
            "description": "van travel generalized cost",
        },
    },
    "trip_part":{
        "transit_work_inv_time": {
            "id": "mf51",
            "description": "transit in-vehicle time",
        },
        "transit_work_aux_time": {
            "id": "mf52",
            "description": "transit auxilliary time",
        },
        "transit_work_tw_time": {
            "id": "mf53",
            "description": "transit total waiting time",
        },
        "transit_work_fw_time": {
            "id": "mf54",
            "description": "transit first waiting time",
        },
        "transit_work_board_time": {
            "id": "mf55",
            "description": "transit boarding time",
        },
        "transit_work_board_cost": {
            "id": "mf58",
            "description": "transit boarding cost",
        },
        "transit_work_num_board": {
            "id": "mf56",
            "description": "transit trip number of boardings",
        },
        "transit_leisure_inv_time": {
            "id": "mf57",
            "description": "transit in-vehicle time",
        },
        "transit_leisure_aux_time": {
            "id": "mf58",
            "description": "transit auxilliary time",
        },
        "transit_leisure_tw_time": {
            "id": "mf59",
            "description": "transit total waiting time",
        },
        "transit_leisure_fw_time": {
            "id": "mf60",
            "description": "transit first waiting time",
        },
        "transit_leisure_board_time": {
            "id": "mf61",
            "description": "transit boarding time",
        },
        "transit_leisure_board_cost": {
            "id": "mf62",
            "description": "transit boarding cost",
        },
        "transit_leisure_num_board": {
            "id": "mf63",
            "description": "transit trip number of boardings",
        },
        "bike_separate_dist": {
            "id": "mf64",
            "description": "separate bike way distance",
        },
        "bike_streetside_dist": {
            "id": "mf65",
            "description": "street-side bike way distance",
        },
        "bike_mixed_dist": {
            "id": "mf66",
            "description": "bike distance in mixed traffic",
        },
    }
}
background_traffic = "ul3"

### DEPARTURE TIME PARAMETERS ###

# Demand shares for different time periods
demand_share = {
    "hw": {
        "car": {
            "aht": (0.288820549293814, 0.00164983305999384),
            "pt": (0.0191570544576966, 0.0187771980766991),
            "iht": (0.00837994382924266, 0.200731740107779),
        },
        "transit": {
            "aht": (0.262479154675437, 0.00454557641637759),
            "pt": (0.0225536757473919, 0.0128179742542008),
            "iht": (0.00652782252709554, 0.195785332057699),
        },
        "bike": {
            "aht": (0.333051067436711, 0.00608107081976724),
            "pt": (0.0243488683605967, 0.0108569277701356),
            "iht": (0.00253869404962361, 0.305891580275386),
        },
        "walk": {
            "aht": (0.273980325226173, 0),
            "pt": (0.0435560236876547, 0.0189789041646973),
            "iht": (0.0103649240096114, 0.216436049124337),
        },
    },
    "hc": {
        "car": {
            "aht": (0.490351584394913, 0),
            "pt": (0.0254451935768562, 0.0703760687389817),
            "iht": (0, 0.0921431200622989),
        },
        "transit": {
            "aht": (0.540424167743717, 0),
            "pt": (0.0217636820804232, 0.091223241969132),
            "iht": (0, 0.15431375989959),
        },
        "bike": {
            "aht": (0.573544771072346, 0),
            "pt": (0.0341593458419707, 0.109149614323394),
            "iht": (0.00581859500994643, 0.106528611377131),
        },
        "walk": {
            "aht": (0.634870345538194, 0),
            "pt": (0.0306004089091672, 0.101786210936117),
            "iht": (0.00129395017965348, 0.0873941474226051),
        },
    },
    "hu": {
        "car": {
            "aht": (0.382660524070486, 0.0127971082664054),
            "pt": (0.0401662768013263, 0.0419553527613303),
            "iht": (0.0634572553797318, 0.174561156092557),
        },
        "transit": {
            "aht": (0.284476235025134, 0.00561152590349421),
            "pt": (0.0601280307807604, 0.0510887696999263),
            "iht": (0.0446532572748154, 0.126845096164362),
        },
        "bike": {
            "aht": (0.229360821622338, 0),
            "pt": (0.0853918424071615, 0.0977621699203758),
            "iht": (0, 0.139908006489409),
        },
        "walk": {
            "aht": (0.231109452978529, 0.0309167551561489),
            "pt": (0.070746711397507, 0.0467990916911236),
            "iht": (0.0684187871098807, 0.149939088659526),
        },
    },
    "hs": {
        "car": {
            "aht": (0.0405885794319654, 0.017477652057659),
            "pt": (0.0603970615836207, 0.0516421108026735),
            "iht": (0.0467016998318382, 0.0638692528598624),
        },
        "transit": {
            "aht": (0.0765341541405897, 0.00474012379675776),
            "pt": (0.0836406354990259, 0.0689212206158884),
            "iht": (0.0502459240576862, 0.0745312871363393),
        },
        "bike": {
            "aht": (0.0543007460241876, 0.00810299970756844),
            "pt": (0.0692597647600368, 0.0653942703626311),
            "iht": (0.103151738228992, 0.0943488182960698),
        },
        "walk": {
            "aht": (0.0541193511885965, 0.0352911509085712),
            "pt": (0.0722356526856759, 0.0662356604096378),
            "iht": (0.0779480165375336, 0.097691106660283),
        },
    },
    "ho": {
        "car": {
            "aht": (0.0383781860538185, 0.00726442614171374),
            "pt": (0.0360424142229208, 0.0275607040867388),
            "iht": (0.0806312062597426, 0.0540736359601802),
        },
        "transit": {
            "aht": (0.0269642764493981, 0.0119453710428538),
            "pt": (0.0503769382556892, 0.0333208756748491),
            "iht": (0.0561622637903115, 0.052159156048967),
        },
        "bike": {
            "aht": (0.0493482076538219, 0.00527814017610801),
            "pt": (0.0380796623932762, 0.0237108591394003),
            "iht": (0.103754797149548, 0.0365662237825043),
        },
        "walk": {
            "aht": (0.0503132293052518, 0.0126997362017003),
            "pt": (0.0423249887393872, 0.0148612529729895),
            "iht": (0.0743905515132885, 0.0235606061219946),
        },
    },
    "hoo": {
        "car": {
            "aht": (
                (0.0113538534294527, 0.0483356330299955),
                (0.000783876140666748, 0.0782437896466509),
            ),
            "pt": (
                (0.0415688948149155, 0.0275008865700513),
                (0.0249338403352452, 0.0218610155562793),
            ),
            "iht": (
                (0.126631086164843, 0.0254942149131846),
                (0.103874241247952, 0.0253360698120264),
            ),
        },
        "transit": {
            "aht": (
                (0.007848433131924, 0.0318369625680414),
                (0.00148575955291745, 0.0800841531842564),
            ),
            "pt": (
                (0.0392336062771297, 0.0251341675086098),
                (0.0191847672424449, 0.0215475457292278),
            ),
            "iht": (
                (0.191259463404029, 0.0367695909665859),
                (0.0872373132287834, 0.0165925719765324),
            ),
        },
        "bike": {
            "aht": (
                (0, 0.10752104373009),
                (0.00325263861271775, 0.0927918963956284),
            ),
            "pt": (
                (0.0409730943539997, 0.017507905833713),
                (0.0223568984557525, 0.0207634708992704),
            ),
            "iht": (
                (0.207855295206265, 0.0225336043406983),
                (0.145116003557633, 0.0142643853021503),
            ),
        },
        "walk": {
            "aht": (
                (0.00528306888246316, 0.0242399831328879),
                (0.00245894352109173, 0.0537383727550346),
            ),
            "pt": (
                (0.0563252625358924, 0.0206655527844586),
                (0.0292490758079734, 0.0210437085372139),
            ),
            "iht": (
                (0.0814142081203715, 0.0271941913428873),
                (0.172295888708894, 0.0396594463206377),
            ),
        },
    },
    "wo": {
        "car": {
            "aht": (0.0276329210085113, 0.0160545369209701),
            "pt": (0.117661361659664, 0.112453940581752),
            "iht": (0.0444924430264217, 0.0342827141128922),
        },
        "transit": {
            "aht": (0.0612632351804617, 0.262154110522183),
            "pt": (0.0433316351591352, 0.0504505017148806),
            "iht": (0.106235593058989, 0.0737024653715484),
        },
        "bike": {
            "aht": (0.086082711150622, 0),
            "pt": (0.123481019815671, 0.108973372738578),
            "iht": (0.0389737064352321, 0),
        },
        "walk": {
            "aht": (0.011792243269137, 0.00568311888204953),
            "pt": (0.142991903140661, 0.136629905882937),
            "iht": (0.0353877586419574, 0.00914593563528563),
        },
    },
    "oo": {
        "car": {
            "aht": (0.0196842157479813, 0.0479857415578179),
            "pt": (0.0586827967478624, 0.0422759234382751),
            "iht": (0.0681586448888759, 0.0736313747819507),
        },
        "transit": {
            "aht": (0.168710422485735, 0.0387468664988151),
            "pt": (0.0716348116654068, 0.0679842570835241),
            "iht": (0.0437554897467228, 0.108924099422715),
        },
        "bike": {
            "aht": (0.0259945209673068, 0.0164613914375604),
            "pt": (0.0692448058659033, 0.0449421010361262),
            "iht": (0.0131611231013582, 0.0411710936086695),
        },
        "walk": {
            "aht": (0.0453535537909917, 0.00282685203656034),
            "pt": (0.0873311164803913, 0.0374143719459607),
            "iht": (0.0547447028678427, 0.0134107502846961),
        },
    },
    "hwp": {
        "car": {
            "aht": (0.284828673072634, 0.00755712929837991),
            "pt": (0.023112752669798, 0.0328984808575901),
            "iht": (0.00803413387844214, 0.332443891285462),
        },
        "transit": {
            "aht": (0.149234181643916, 0),
            "pt": (0.0163476939401269, 0.0355138136169777),
            "iht": (0, 0.412582980634712),
        },
    },
    "hop": {
        "car": {
            "aht": (0.0910767007840877, 0.0133245756008547),
            "pt": (0.0733228496135912, 0.0632392268306549),
            "iht": (0.0725521634967265, 0.0897368257624752),
        },
        "transit": {
            "aht": (0.330576470748095, 0),
            "pt": (0.0391056752731289, 0.0919882820859918),
            "iht": (0.0311972821960398, 0.0991336256168802),
        },
    },
    "oop": {
        "car": {
            "aht": (0.0585795789311712, 0.041118431421166),
            "pt": (0.114889840412835, 0.116203520254407),
            "iht": (0.0397633661562958, 0.0277396603049591),
        },
        "transit": {
            "aht": (0.376361385885435, 0),
            "pt": (0.0869523179383367, 0.0347224022302181),
            "iht": (0.0112765910942976, 0.0136093560308682),
        },
    },
    "freight": {
        "trailer_truck": {
            "aht": (0.066, 0),
            "pt": (0.07, 0),
            "iht": (0.066, 0),
        },
        "truck": {
            "aht": (0.066, 0),
            "pt": (0.07, 0),
            "iht": (0.066, 0),
        },
        "van": {
            # As shares of car traffic
            # On top of this, the trucks sum is added
            "aht": (0.054, 0),
            "pt": (0.07, 0),
            "iht": (0.044, 0),
        },
    },
    "external": {
        # External matrices are untransposed (ext->int),
        # and describe trips, not tours
        "car": {
            "aht": (
                [
                    [0.042], [0.042], [0.049], [0.042], [0.055], [0.042],
                    [0.042], [0.058], [0.042], [0.042], [0.042], [0.042],
                    [0.042], [0.061], [0.030], [0.042], [0.042], [0.041],
                    [0.038], [0.040], [0.000], [0.000], [0.000], [0.043],
                    [0.000], [0.000], [0.000], [0.250],
                ], 
                [
                    0.028, 0.028, 0.024, 0.028, 0.018, 0.028,
                    0.028, 0.045, 0.028, 0.028, 0.028, 0.028,
                    0.028, 0.031, 0.039, 0.028, 0.028, 0.034,
                    0.028, 0.046, 0.000, 0.000, 0.000, 0.042,
                    0.000, 0.000, 0.083, 0.000,
                ],
            ),
            "pt": (0.05, 0.05),
            "iht": (
                [
                    [0.045], [0.045], [0.044], [0.045], [0.048], [0.045],
                    [0.045], [0.056], [0.045], [0.045], [0.045], [0.045],
                    [0.045], [0.051], [0.070], [0.045], [0.045], [0.039],
                    [0.056], [0.069], [0.000], [0.000], [0.000], [0.071],
                    [0.000], [0.000], [0.125], [0.000],
                ],
                [
                    0.055, 0.055, 0.069, 0.055, 0.066, 0.055,
                    0.055, 0.052, 0.055, 0.055, 0.055, 0.055,
                    0.055, 0.065, 0.049, 0.055, 0.055, 0.064,
                    0.076, 0.057, 0.000, 0.000, 0.000, 0.066,
                    0.188, 0.273, 0.083, 0.250,
                ],
            ),
        },
        "transit": {
            "aht": (0.101, 0.034),
            "pt": (0.05, 0.05),
            "iht": (0.064, 0.119),
        },
        "trailer_truck": {
            "aht": (0.033, 0.033),
            "pt": (0.035, 0.035),
            "iht": (0.033, 0.033),
        },
        "truck": {
            "aht": (0.033, 0.033),
            "pt": (0.035, 0.035),
            "iht": (0.033, 0.033),
        },
    },
}
backup_demand_share = {
    "aht": (0.042, 0.028),
    "pt": (0.05, 0.05),
    "iht": (0.045, 0.055),
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
        # Only un-transposed afternoon matrices are used.
        # However, the secondary destination choice is done "backwards",
        # from destination 1 to origin.
        "car": {
            "aht": (0, 0),
            "pt":  (0, 0),
            "iht": (1, 0),
        },
        "transit": {
            "aht": (0, 0),
            "pt":  (0, 0),
            "iht": (1, 0),
        },
        "bike": {
            "aht": (0, 0),
            "pt":  (0, 0),
            "iht": (1, 0),
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

# Destination choice (calibrated)
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
                "cbd": (numpy.exp(4.82525484469 - 3.0),
                        numpy.exp(5.46413339352 - 2.0)),
                "workplaces_own": (numpy.exp(0.326534462277 + 0.1),
                                   numpy.exp(0.914054873639 + 0.5)),
                "workplaces_other": 1,
            },
        },
        "transit": {
            "attraction": {
                "cbd": (0.483086068108, 0.483086068108),
                "helsinki_other": (0.2, 0.2),
            },
            "impedance": {
                "time": -0.111547282384e-1,
                "cost": ((-0.411197516348e-1) / 60.0, -0.976929479166e-1 / 44.0),
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
                "dist": -2.66058468415 + 0.1,
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
                "cbd": (0.704345842211 + 0.2, 0.704345842211 + 0.2),
                "helsinki_other": (0.5, 0.2),
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
                    "cost": (1.0 / 60.0, 1.0 / 44.0),
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
                "own_zone_area_sqrt": (-3.87680793384 + 0.1,
                                       -3.87680793384 - 1.5),
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
                "parking_cost_work": (-0.354136146210 - 0.5,
                                      -0.354136146210 - 0.5),
            },
            "impedance": {
                "time": -0.312118189213e-1 - 0.007,
                "cost": -0.216784178710 - 0.07,
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
                "cbd": (0.145833772041 + 0.015, 0.145833772041 + 0.04),
            },
            "impedance": {
                "time": (-0.136559859790e-1 - 0.005,
                         -0.136559859790e-1 - 0.005),
                "cost": (-0.216784178710 / 60.0, -0.216784178710 / 44.0),
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
            },
            "log": {
                "dist": (-1.71018514578, -1.71018514578),
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
                "dist": -3.32917729353 - 0.3,
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
                "time": (-0.960814824614e-1 - 0.01),
                "cost": -0.112450201944,
            },
            "log": {
                "size": 1.00000000000, # L_S_M
            },
            "size": {
                "population_other": 1,
                "population_own": numpy.exp(1.58732389618),
                "shops_other": numpy.exp(6.24804591506),
                "shops_own": (numpy.exp(6.19259580740 + 0.3), 
                              numpy.exp(7.10231579547 + 0.5)),
                "service_other": numpy.exp(3.77954709039),
                "service_own": (numpy.exp(4.53224477260),
                                numpy.exp(5.13038361124)),
                "cbd": (numpy.exp(9.04364663102 - 7.0),
                        numpy.exp(7.19898499824 + 3.7)),
            },
        },
        "transit": {
            "attraction": {
                "cbd": (0.135335656706 - 0.1, 2.62480475297 - 0.1),
                "helsinki_other": (0.1, 0.1),
            },
            "impedance": {
                "time": -0.299237931923e-1,
                "cost": -0.112450201944 / 30.0,
            },
            "log": {
                "size": 1.00000000000,
            },
            "size": {
                "population_other": 1,
                "population_own": numpy.exp(1.58732389618),
                "shops_other": numpy.exp(6.24804591506),
                "shops_own": (numpy.exp(6.19259580740), 
                              numpy.exp(7.10231579547 + 0.6)),
                "service_other": numpy.exp(3.77954709039),
                "service_own": (numpy.exp(4.53224477260), 
                                numpy.exp(5.13038361124)),
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
                "shops_own": (numpy.exp(6.19259580740 + 1.0),
                              numpy.exp(7.10231579547 + 1.5)),
                "service_other": numpy.exp(3.77954709039),
                "service_own": (numpy.exp(4.53224477260 + 1.0),
                                numpy.exp(5.13038361124 + 1.5)),
                "cbd": (numpy.exp(9.04364663102 - 5.0), 
                        numpy.exp(7.19898499824 - 6.0)),
            },
        },
        "walk": {
            "attraction": {
                "own_zone_area_sqrt": (-3.44256406401 - 0.4, 
                                       -4.67197096996 - 0.9),
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
                "shops_own": (numpy.exp(6.19259580740 + 0.3),
                              numpy.exp(7.10231579547 - 0.2)),
                "service_other": numpy.exp(3.77954709039),
                "service_own": (numpy.exp(4.53224477260), numpy.exp(5.13038361124)),
                "cbd": (numpy.exp(9.04364663102 - 6.0), 
                        numpy.exp(7.19898499824)),
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
                "population_own": (numpy.exp(1.205650309),
                                   numpy.exp(1.205650309 + 2.0)),
                "service_other": numpy.exp(2.384174142),
                "service_own": (numpy.exp(3.183207081),
                                numpy.exp(3.183207081 + 2.0)),
                "shops": numpy.exp(2.998477655),
                "cbd": (numpy.exp(7.813868577 - 6.0),
                        numpy.exp(4.709424332 - 6.0)),
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
                    "cost": 1.0 / 30.0,
                },
            },
        },
        "bike": {
            "attraction": {},
            "impedance": {},
            "log": {
                "dist": (-1.840032015 - 0.1, -1.657687972 - 0.1),
                "size": 1,
            },
            "size": {
                "population_other": 1,
                "population_own": (numpy.exp(1.205650309 + 2.0),
                                   numpy.exp(1.205650309 + 3.0)),
                "service_other": numpy.exp(2.384174142),
                "service_own": (numpy.exp(3.183207081 + 2.0),
                                numpy.exp(3.183207081 + 3.0)),
                "shops": numpy.exp(2.998477655),
                "cbd": (numpy.exp(7.813868577 - 4.0),
                        numpy.exp(4.709424332 - 4.0)),
            },
        },
        "walk": {
            "attraction": {
                "own_zone_area_sqrt": (-1.139032362 + 0.11,
                                       -1.012079317 + 0.15),
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
                "cost": -0.071273703 / 30.0,
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
                "parking_cost_errand": -.302597031681,
            },
            "impedance": {
                "time": -.0649586432326,
            },
            "log": {
                "cost": -.716918267916,
                "size": 1,
            },
            "size": {
                "population": 1,
                "workplaces": numpy.exp(.339167213937),
                "service": numpy.exp(1.54928000612),
                "shops_cbd": numpy.exp(3.48055138106),
                "shops_elsewhere": numpy.exp(3.30123960735),
                "own_zone": (numpy.exp(6.62440257143 - 4.0),
                             numpy.exp(6.62440257143 - 4.0)),
            },
        },
        "transit": {
            "attraction": {
                "cbd": .286734696885,
                "own_zone": -2.01312674021,
            },
            "impedance": {
                "time": -.0234309619841,
            },
            "log": {
                "transform": -.716918267916,
                "size": 1,
            },
            "size": {
                "population": 1,
                "workplaces": numpy.exp(.339167213937),
                "service": numpy.exp(1.54928000612),
                "shops_cbd": numpy.exp(3.48055138106),
                "shops_elsewhere": numpy.exp(3.30123960735),
                "own_zone": numpy.exp(6.62440257143),
            },
            "transform": {
                "attraction": {},
                "impedance": {
                    "cost": 1.0 / 30.0,
                },
            },
        },
        "bike": {
            "attraction": {},
            "impedance": {},
            "log": {
                "dist": (-2.04597614770, -1.84194439913),
                "size": 1,
            },
            "size": {
                "population": 1,
                "workplaces": numpy.exp(.339167213937),
                "service": numpy.exp(1.54928000612),
                "shops_cbd": numpy.exp(3.48055138106),
                "shops_elsewhere": numpy.exp(3.30123960735),
                "own_zone": numpy.exp(6.62440257143),
            },
        },
        "walk": {
            "attraction": {
                "own_zone_area_sqrt": (-.965499228388, -1.74017884580),
            },
            "impedance": {},
            "log": {
                "dist": -3.35260549718,
                "size": 1,
            },
            "size": {
                "population": 1,
                "workplaces": numpy.exp(.339167213937),
                "service": numpy.exp(1.54928000612),
                "shops_cbd": (numpy.exp(3.48055138106 + 3.0),
                              numpy.exp(3.48055138106)),
                "shops_elsewhere": numpy.exp(3.30123960735),
                "own_zone": numpy.exp(6.62440257143 - 7.0),
            },
        },
    },
    "oo": {
        "car": {
            "attraction": {
                "parking_cost_errand": -.302597031681,
            },
            "impedance": {
                "time": (-.0649586432326 - 0.02,
                         -.0649586432326 - 0.04),
            },
            "log": {
                "cost": -.716918267916,
                "size": 1,
            },
            "size": {
                "population": 1,
                "workplaces": numpy.exp(.339167213937),
                "service": numpy.exp(1.54928000612),
                "shops_cbd": numpy.exp(3.48055138106),
                "shops_elsewhere": numpy.exp(3.30123960735),
                "own_zone": numpy.exp(6.62440257143),
            },
        },
        "transit": {
            "attraction": {
                "cbd": (.286734696885 - 0.07,
                        .286734696885 + 1.7),
                "own_zone": -2.01312674021,
            },
            "impedance": {
                "time": -.0234309619841,
            },
            "log": {
                "transform": -.716918267916,
                "size": 1,
            },
            "size": {
                "population": 1,
                "workplaces": numpy.exp(.339167213937),
                "service": numpy.exp(1.54928000612),
                "shops_cbd": numpy.exp(3.48055138106),
                "shops_elsewhere": numpy.exp(3.30123960735),
                "own_zone": numpy.exp(6.62440257143),
            },
            "transform": {
                "attraction": {},
                "impedance": {
                    "cost": 1.0 / 30.0,
                },
            },
        },
        "bike": {
            "attraction": {},
            "impedance": {},
            "log": {
                "dist": (-2.04597614770, -1.84194439913),
                "size": 1,
            },
            "size": {
                "population": 1,
                "workplaces": numpy.exp(.339167213937),
                "service": numpy.exp(1.54928000612),
                "shops_cbd": numpy.exp(3.48055138106),
                "shops_elsewhere": numpy.exp(3.30123960735),
                "own_zone": numpy.exp(6.62440257143),
            },
        },
        "walk": {
            "attraction": {
                "own_zone_area_sqrt": (-.965499228388, -1.74017884580),
            },
            "impedance": {},
            "log": {
                "dist": -3.35260549718,
                "size": 1,
            },
            "size": {
                "population": 1,
                "workplaces": numpy.exp(.339167213937),
                "service": numpy.exp(1.54928000612),
                "shops_cbd": numpy.exp(3.48055138106 + 2.0),
                "shops_elsewhere": numpy.exp(3.30123960735),
                "own_zone": (numpy.exp(6.62440257143),
                             numpy.exp(6.62440257143 + 1.0)),
            },
        },
    },
    "hwp": {
        "car": {
            "attraction": {
                "parking_cost_work": -0.167648454911 + 0.06,
                "share_detached_houses": 0.579675740565,
                "own_zone_area": -0.194842606662e-1 - 0.004,
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
                "cbd": 0.490942327168 + 0.35,
                "own_zone_area": -0.112492660238,
            },
            "impedance": {
                "time": -0.808893404926e-2,
                "cost": (-0.167648454911 - 0.07) / 44.0,
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
                "own_zone_area": -0.138197654412e-1 + 0.0025,
            },
            "impedance": {
                "time": -0.288481815905e-1,
                "cost": -0.188691214282 - 0.015 ,
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
                "cost": (-0.188691214282 - 0.04) / 30.0,
            },
            "log": {
                "size": 1, # L_S_M
            },
            "size": {
                "workplaces": numpy.exp(1.07808303849),
                "service": numpy.exp(4.57535345257),
                "shops": numpy.exp(5.35085890989),
                "comprehensive_schools": numpy.exp(2.40450824304),
                "population_own": numpy.exp(3.28776000706 + 0.7),
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
                "cost": ((-0.227398812175 - 0.2) / 30.0,
                         (-0.227398812175 - 0.2) / 30.0),
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
# Mode choice (calibrated 06.05.2020)
mode_choice = {
    "hw": {
        "car": {
            "constant": (0.844179295926 * (0 + 0.254), 
                         0.844179295926 * (0 + 0.136)),
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
            "constant": (0.844179295926 * (3.15335645065 - 0.158), 
                         0.844179295926 * (3.09257722177 - 0.415)),
            "generation": {
                "cbd": 0.4,
                "helsinki_other": 0.1,
                "espoo_vant_kau": -0.2,
            },
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": 0.844179295926,
            },
            "individual_dummy": {},
        },
        "bike": {
            "constant": (0.844179295926 * (3.65997812160 + 0.023), 
                         0.844179295926 * (4.10083690370 + 0.193)),
            "generation": {},
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": 0.844179295926,
            },
            "individual_dummy": {},
        },
        "walk": {
            "constant": (0.844179295926 * (6.06426484277 - 0.156),
                         0.844179295926 * (6.31407702335 - 0.347)),
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
            "constant": (0.272803753976 * (0 + 0.531),
                         0.272803753976 * (0 - 0.852)),
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
            "constant": (0.272803753976 * (13.2817160786 + 0.211),
                         0.272803753976 * (13.2817160786 - 0.693)),
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
            "constant": (0.272803753976 * (11.3490028510 + 0.126),
                         0.272803753976 * (11.3490028510 + 2.076)),
            "generation": {},
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": 0.272803753976, # Dcoeff
            },
            "individual_dummy": {},
        },
        "walk": {
            "constant": (0.272803753976 * (17.7784859496 - 0.013),
                         0.272803753976 * (17.7784859496 - 1.260)),
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
            "constant": (0 - 0.342, 0 + 0.462),
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
            "constant": (3.10747422821 - 0.159, 3.10747422821 + 0.700),
            "generation": {
                "cbd": 0.5,
                "helsinki_other": 0.1,
                "espoo_vant_kau": -0.3,
            },
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": 1.00000000000,
            },
            "individual_dummy": {},
        },
        "bike": {
            "constant": (3.23689689401 - 0.172, 3.23689689401 + 1.278),
            "generation": {},
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": 1.00000000000,
            },
            "individual_dummy": {},
        }, 
        "walk": {
            "constant": (6.15888890793 + 0.130, 6.15888890793 + 0.865), 
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
            "constant": (0.539979474415 * (0 + 0.286), 
                         0.539979474415 * (0 + 0.087)),
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
            "constant": (0.539979474415 * (5.13091589060 - 0.134), 
                         0.539979474415 * (4.98462338486 - 0.476)),
            "generation": {
                "cbd": 0.1,
                "helsinki_other": 0.1,
                "espoo_vant_kau": -0.3,
            },
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": 0.539979474415,
            },
            "individual_dummy": {},
        },
        "bike": {
            "constant": (0.539979474415 * (3.98060152237 - 0.479), 
                         0.539979474415 * (7.26646802781 - 0.926)),
            "generation": {},
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": 0.539979474415,
            },
            "individual_dummy": {},
        }, 
        "walk": {
            "constant": (0.539979474415 * (10.8293044790 - 0.155),
                         0.539979474415 * (12.6937820419 + 0.230)),
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
            "constant": (0.151688898 * (0 + 0.311),
                         0.151688898 * (0 - 0.484)),
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
            "constant": (0.151688898 * (8.71611785 - 0.209), 
                         0.151688898 * (-9.326014274 + 0.711)),
            "generation": {
                "cbd": 0.4,
                "helsinki_other": 0.1,
                "espoo_vant_kau": -0.7,
            },
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": 0.151688898,
            },
            "individual_dummy": {},
        },
        "bike": {
            "constant": (0.151688898 * (5.077652282 - 1.265), 
                         0.151688898 * (-1.017242495 - 1.219)),
            "generation": {},
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": 0.151688898,
            },
            "individual_dummy": {},
        }, 
        "walk": {
            "constant": (0.151688898 * (20.72419038 - 0.037), 
                         0.151688898 * (12.53617415 + 0.749)),
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
    "wo": {
       "car": {
            "constant": (.798132431338 * (0 + 0.284),
                         .798132431338 * (0 + 0.535)),
            "generation": {
                "car_density": (.798132431338 * 1000 * .00221109216997, .798132431338 * 1000 * .00228561511302),
            },
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": .798132431338,
            },
            "individual_dummy": {},
        },
        "transit": {
            "constant": (.798132431338 * (1.00739274058 + 0.284),
                         .798132431338 * (1.00739274058 - 3.652)),
            "generation": {
                "cbd": 1.0,
                "helsinki_other": -0.5,
                "espoo_vant_kau": -1.0,
            },
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": .798132431338,
            },
            "individual_dummy": {},
        },
        "bike": {
            "constant": (.798132431338 * (-.869336973071 + 1.498),
                         .798132431338 * (-.517146785790 - 0.551)),
            "generation": {},
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": .798132431338,
            },
            "individual_dummy": {},
        }, 
        "walk": {
            "constant": (.798132431338 * (4.70332901113 - 0.240),
                         .798132431338 * (4.70332901113 - 0.491)),
            "generation": {},
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": .798132431338,
            },
            "individual_dummy": {},
        },
    },
    "oo": {
        "car": {
            "constant": (.798132431338 * (0 - 0.023),
                         .798132431338 * (0 + 0.380)),
            "generation": {
                "car_density": (.798132431338 * 1000 * .00221109216997, .798132431338 * 1000 * .00228561511302),
            },
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": .798132431338,
            },
            "individual_dummy": {},
        },
        "transit": {
            "constant": (.798132431338 * (1.00739274058 + 0.352),
                         .798132431338 * (1.00739274058 - 1.051)),
            "generation": {
                "cbd": 0.2,
                "helsinki_other": -0.4,
                "espoo_vant_kau": -0.4,
            },
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": .798132431338,
            },
            "individual_dummy": {},
        },
        "bike": {
            "constant": (.798132431338 * (-.869336973071 - 0.464),
                         .798132431338 * (-.517146785790 + 0.807)),
            "generation": {},
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": .798132431338,
            },
            "individual_dummy": {},
        }, 
        "walk": {
            "constant": (.798132431338 * (4.70332901113 - 0.033),
                         .798132431338 * (4.70332901113 + 0.082)),
            "generation": {},
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": .798132431338,
            },
            "individual_dummy": {},
        },
    },
    "hwp": {
        "car": {
            "constant": (0 - 0.022),
            "generation": {},
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": 1.00000000000, # Dcoeff
            },
            "individual_dummy": {},
        },
        "transit": {
            "constant": (-1.79569982464 + 0.332), # T_const
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
            "constant": (0 + 0.009),
            "generation": {},
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": 1.00000000000,
            },
            "individual_dummy": {},
        },
        "transit": {
            "constant": (-1.26883605707 - 0.101),
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
            "constant": (0.715272183645 * (0 + 0.120)),
            "generation": {},
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": 0.715272183645,
            },
            "individual_dummy": {},
        },
        "transit": {
            "constant": (0.715272183645 * (-3.44371464477 + 0.350)),
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
# Scale parameter used in upper level of tour pattern model
tour_number_scale = 0.622253957
# Calibration of tour numbers
tour_number_increase = {
    1: 1,
    2: 1.002732179,
    3: 1.05446538,
    4: 1.2455917 + 0.1043963,
}
# Tour combinations (calibrated)
tour_combinations = {
# utility function 1
    0: {
        () : {
            "constant":   0.000000000,
            "individual_dummy": {
                "age_50-64": -0.305509545 ,
                "age_65-99":  0.597976527
            },
            "zone": {},
        },
# utility function 2
    },
    1: {
        ("hw",) : {
            "constant":   0.000000000 + 0.0210,
            "individual_dummy": {
                "age_18-29":  2.306249018 + 0.1065,
                "age_30-49":  2.977241136 - 0.3498,
                "age_50-64":  2.018825449 - 0.1177,
                "age_65-99": -1.185980639 - 0.0771
            },
            "zone": {
                "share_detached_houses": -0.5910000
            },
        },
# utility function 3
        ("hc",) : {
            "constant":   3.308625072 + 0.0150,
            "individual_dummy": {
                "age_7-17":  0.000000000 - 0.0641
            },
            "zone": {
                "share_detached_houses": -0.5910000
            },
        },
# utility function 4
        ("hu",) : {
            "constant":   0.000000000 + 0.3000,
            "individual_dummy": {
                "age_18-29":  0.000000000 + 0.0653,
                "age_30-49": -1.586979829 - 0.0192,
                "age_50-64": -3.739206239 - 1.3644,
                "age_65-99": -3.636471246 - 0.5649
            },
            "zone": {
                "share_detached_houses": -0.5910000 ,
                "hu_t":  0.148402259
            },
        },
# utility function 5
        ("hs",) : {
            "constant":   0.000000000,
            "individual_dummy": {
                "age_7-17":   0.000000000 - 0.0600,
                "age_18-29":  0.632156675 + 0.2843,
                "age_30-49":  1.106558979 - 0.6505,
                "age_50-64":  0.636516485 - 0.0855,
                "age_65-99":  1.250192981 - 0.0811
            },
            "zone": {
                "share_detached_houses": -0.5910000
            },
        },
# utility function 6
        ("ho",) : {
            "constant":   0.811674639,
            "individual_dummy": {
                "age_7-17":   0.000000000 - 0.1096,
                "age_18-29":  0.000000000 + 0.0679,
                "age_30-49":  0.000000000 - 0.2390,
                "age_50-64":  0.000000000 - 0.1643,
                "age_65-99":  0.394182783 - 0.1262
            },
            "zone": {
                "share_detached_houses": -0.5910000
            },
        },
# utility function 7
    },
    2: {
        ("hw", "hw") : {
            "constant":  -6.702389265,
            "individual_dummy": {
                "age_18-29":  2.306249018 - 1.0022,
                "age_30-49":  2.977241136 + 0.3275,
                "age_50-64":  2.018825449 - 0.1879,
                "age_65-99": -1.185980639 ,
                "car_users":  0.647176487
            },
            "zone": {
                "ho_w":  0.249875934
            },
        },
# utility function 8
        ("hw", "hu") : {
            "constant":  -8.418852173 + 0.2000,
            "individual_dummy": {
                "age_18-29":  2.306249018 - 0.4439,
                "age_30-49": -1.586979829 +  2.977241136 + 0.4961,
                "age_50-64": -3.739206239 +  2.018825449 + 1.6450,
                "age_65-99": -3.636471246  -1.185980639 ,
                "car_users":  0.647176487
            },
            "zone": {
                "hu_t":  0.176002681 ,
                "ho_w":  0.249875934
            },
        },
# utility function 9
        ("hw", "hs") : {
            "constant":  -5.468303413,
            "individual_dummy": {
                "age_18-29":  0.632156675 +  2.306249018 - 0.1900,
                "age_30-49":  1.106558979 +  2.977241136 + 0.0878,
                "age_50-64":  0.636516485 +  2.018825449 - 0.1499,
                "age_65-99":  1.250192981  -1.185980639 - 0.6537,
                "car_users":  0.647176487
            },
            "zone": {
                "ho_w":  0.249875934
            },
        },
# utility function 10
        ("hw", "ho") : {
            "constant":  -3.969665707,
            "individual_dummy": {
                "age_18-29":  2.306249018 + 0.0229,
                "age_30-49":  2.977241136 + 0.0059,
                "age_50-64":  2.018825449 - 0.0759,
                "age_65-99":  0.394182783  -1.185980639 - 0.1253,
                "car_users":  0.647176487
            },
            "zone": {
                "ho_w":  0.249875934
            },
        },
# utility function 11
        ("hc", "hc") : {
            "constant":  -2.189925729,
            "individual_dummy": {},
            "zone": {
                "ho_w":  0.249875934
            },
        },
# utility function 12
        ("hc", "hs") : {
            "constant":  -0.932031836,
            "individual_dummy": {
                "age_7-17":   0.000000000 - 0.0317,
                "age_18-29":  0.632156675 ,
                "age_30-49":  1.106558979 ,
                "age_50-64":  0.636516485 ,
                "age_65-99":  1.250192981
            },
            "zone": {
                "ho_w":  0.249875934
            },
        },
# utility function 13
        ("hc", "ho") : {
            "constant":   1.040646615,
            "individual_dummy": {
                "age_7-17":   0.000000000 - 0.0322,
                "age_65-99":  0.394182783
            },
            "zone": {
                "ho_w":  0.249875934
            },
        },
# utility function 14
        ("hu", "hs") : {
            "constant":  -5.264912587 + 0.0736,
            "individual_dummy": {
                "age_18-29":  0.632156675 - 0.0197,
                "age_30-49":  1.106558979  -1.586979829 - 0.6757,
                "age_50-64":  0.636516485  -3.739206239 + 0.7197,
                "age_65-99":  1.250192981  -3.636471246 + 0.9990,
                "car_users":  0.647176487
            },
            "zone": {
                "hu_t":  0.176002681 ,
                "ho_w":  0.249875934
            },
        },
# utility function 15
        ("hu", "ho") : {
            "constant":  -4.133565561 + 0.0834,
            "individual_dummy": {
                "age_18-29":  0.000000000 + 0.2038,
                "age_30-49": -1.586979829 - 0.8545,
                "age_50-64": -3.739206239 + 0.2616,
                "age_65-99":  0.394182783  -3.636471246 - 0.3497,
                "car_users":  0.647176487
            },
            "zone": {
                "hu_t":  0.176002681 ,
                "ho_w":  0.249875934
            },
        },
# utility function 16
        ("hs", "hs") : {
            "constant":  -4.347727916,
            "individual_dummy": {
                "age_18-29":  0.632156675 - 0.2125,
                "age_30-49":  1.106558979 + 0.3402,
                "age_50-64":  0.636516485 - 0.1912,
                "age_65-99":  1.250192981 - 0.0980,
                "car_users":  0.647176487
            },
            "zone": {
                "ho_w":  0.249875934
            },
        },
# utility function 17
        ("hs", "ho") : {
            "constant":  -3.615413138,
            "individual_dummy": {
                "age_7-17":   0.000000000 + 0.1376,
                "age_18-29":  0.632156675 + 0.0695,
                "age_30-49":  1.106558979 - 0.2025,
                "age_50-64":  0.636516485 + 0.0648,
                "age_65-99":  1.250192981 +  0.394182783 - 0.0123,
                "car_users":  0.647176487
            },
            "zone": {
                "ho_w":  0.249875934
            },
        },
# utility function 18
        ("ho", "ho") : {
            "constant":  -2.954069138,
            "individual_dummy": {
                "age_7-17":   0.000000000 + 0.5035,
                "age_18-29":  0.000000000 - 0.1393,
                "age_30-49":  0.000000000 + 0.1371,
                "age_50-64":  0.000000000 - 0.2130,
                "age_65-99":  0.394182783 + 0.0096,
                "car_users":  0.647176487
            },
            "zone": {
                "ho_w":  0.249875934
            },
        },
# utility function 19
    },
    3: {
        ("hw", "hw", "ho") : {
            "constant":  -7.640316015,
            "individual_dummy": {
                "age_18-29":  2.306249018 ,
                "age_30-49":  2.977241136 - 0.4304,
                "age_50-64":  2.018825449 + 0.6609,
                "age_65-99":  0.394182783  -1.185980639 + 2.8800,
                "car_users":  1.492056593
            },
            "zone": {},
        },
# utility function 20
        ("hw", "hs", "hs") : {
            "constant":  -6.996908123,
            "individual_dummy": {
                "age_18-29":  0.632156675 +  2.306249018 - 0.7910,
                "age_30-49":  1.106558979 +  2.977241136 + 0.4528,
                "age_50-64":  0.636516485 +  2.018825449 - 0.2617,
                "age_65-99":  1.250192981  -1.185980639  - 0.2451,
                "car_users":  1.492056593
            },
            "zone": {},
        },
# utility function 21
        ("hw", "hs", "ho") : {
            "constant":  -6.280857590,
            "individual_dummy": {
                "age_18-29":  0.632156675 +  2.306249018 + 0.2580,
                "age_30-49":  1.106558979 +  2.977241136 + 0.1582,
                "age_50-64":  0.636516485 +  2.018825449 + 0.1107,
                "age_65-99":  1.250192981 +  0.394182783  -1.185980639 + 0.4486,
                "car_users":  1.492056593
            },
            "zone": {},
        },
# utility function 22
        ("hw", "ho", "ho") : {
            "constant":  -5.143814369,
            "individual_dummy": {
                "age_18-29":  2.306249018 - 0.2782,
                "age_30-49":  2.977241136 + 0.3222,
                "age_50-64":  2.018825449 + 0.0418,
                "age_65-99":  0.394182783  -1.185980639 + 0.7158,
                "car_users":  1.492056593
            },
            "zone": {},
        },
# utility function 23
        ("hc", "hs", "ho") : {
            "constant":  -1.110080901,
            "individual_dummy": {
                "age_7-17":   0.000000000 - 0.1097,
                "age_18-29":  0.632156675 ,
                "age_30-49":  1.106558979 ,
                "age_50-64":  0.636516485 ,
                "age_65-99":  1.250192981 +  0.394182783
            },
            "zone": {
                "ho_w":  0.025800000
            },
        },
# utility function 24
        ("hc", "ho", "ho") : {
            "constant":   0.000000000,
            "individual_dummy": {
                "age_7-17":   0.000000000 - 0.1805,
                "age_65-99":  0.394182783
            },
            "zone": {
                "ho_w":  0.025800000
            },
        },
# utility function 25
        ("hu", "hs", "ho") : {
            "constant": -11.751808160,
            "individual_dummy": {
                "age_18-29":  0.632156675 + 0.1437,
                "age_30-49":  1.106558979  -1.586979829 + 0.8652,
                "age_50-64":  0.636516485  -3.739206239 + 0.9321,
                "age_65-99":  1.250192981 +  0.394182783  -3.636471246 - 1.8292,
                "car_users":  1.492056593
            },
            "zone": {
                "hu_t":  0.829445548 ,
                "ho_w":  0.025800000
            },
        },
# utility function 26
        ("hu", "ho", "ho") : {
            "constant": -11.342729830,
            "individual_dummy": {
                "age_18-29": -0.000000000 + 0.1541,
                "age_30-49": -1.586979829 + 0.5275,
                "age_50-64": -3.739206239 - 0.7142,
                "age_65-99":  0.394182783  -3.636471246 ,
                "car_users":  1.492056593
            },
            "zone": {
                "hu_t":  0.829445548 ,
                "ho_w":  0.025800000
            },
        },
# utility function 27
        ("hs", "hs", "hs") : {
            "constant":  -5.575050535,
            "individual_dummy": {
                "age_18-29":  0.632156675 - 2.3203,
                "age_30-49":  1.106558979 + 0.9194,
                "age_50-64":  0.636516485 ,
                "age_65-99":  1.250192981 - 0.2474,
                "car_users":  1.492056593
            },
            "zone": {
                "ho_w":  0.025800000
            },
        },
# utility function 28
        ("hs", "hs", "ho") : {
            "constant":  -4.709369964,
            "individual_dummy": {
                "age_18-29":  0.632156675 - 0.7508,
                "age_30-49":  1.106558979 + 0.5842,
                "age_50-64":  0.636516485 ,
                "age_65-99":  1.250192981 +  0.394182783 + 0.1375,
                "car_users":  1.492056593
            },
            "zone": {
                "ho_w":  0.025800000
            },
        },
# utility function 29
        ("hs", "ho", "ho") : {
            "constant":  -4.115616267,
            "individual_dummy": {
                "age_18-29":  0.632156675 - 0.1442,
                "age_30-49":  1.106558979 ,
                "age_50-64":  0.636516485 + 0.3212,
                "age_65-99":  1.250192981 +  0.394182783 + 0.1907,
                "car_users":  1.492056593
            },
            "zone": {
                "ho_w":  0.025800000
            },
        },
# utility function 30
        ("ho", "ho", "ho") : {
            "constant":  -4.110394781,
            "individual_dummy": {
                "age_30-49":  0.000000000 - 0.1750,
                "age_50-64":  0.000000000 + 0.1126,
                "age_65-99":  0.394182783 + 0.3557,
                "car_users":  1.492056593
            },
            "zone": {
                "ho_w":  0.025800000
            },
        },
# utility function 31
    },
    4: {
        ("hw", "hs", "hs", "ho") : {
            "constant":  -8.782904966,
            "individual_dummy": {
                "age_18-29":  0.632156675 +  2.306249018 ,
                "age_30-49":  1.106558979 +  2.977241136 + 0.2190,
                "age_50-64":  0.636516485 +  2.018825449 + 0.7268,
                "age_65-99":  1.250192981 +  0.394182783  -1.185980639 ,
                "car_users":  1.544612164
            },
            "zone": {
                "share_detached_houses": -0.8050000
            },
        },
# utility function 32
        ("hw", "hs", "ho", "ho") : {
            "constant":  -7.819600775,
            "individual_dummy": {
                "age_18-29":  0.632156675 +  2.306249018 + 0.5615,
                "age_30-49":  1.106558979 +  2.977241136 + 0.2939,
                "age_50-64":  0.636516485 +  2.018825449 + 0.1404,
                "age_65-99":  1.250192981 +  0.394182783  -1.185980639 ,
                "car_users":  1.544612164
            },
            "zone": {
                "share_detached_houses": -0.8050000
            },
        },
# utility function 33
        ("hw", "ho", "ho", "ho") : {
            "constant":  -6.323991971,
            "individual_dummy": {
                "age_18-29":  2.306249018 + 0.3338,
                "age_30-49":  2.977241136 ,
                "age_50-64":  2.018825449 + 0.4624,
                "age_65-99":  0.394182783  -1.185980639 ,
                "car_users":  1.544612164
            },
            "zone": {
                "share_detached_houses": -0.8050000
            },
        },
# utility function 34
        ("hs", "hs", "hs", "hs") : {
            "constant":  -6.563838110,
            "individual_dummy": {
                "age_18-29":  0.632156675 ,
                "age_30-49":  1.106558979 + 1.11106,
                "age_50-64":  0.636516485 ,
                "age_65-99":  1.250192981 - 0.6711,
                "car_users":  1.544612164
            },
            "zone": {
                "share_detached_houses": -0.8050000
            },
        },
# utility function 35
        ("hs", "hs", "hs", "ho") : {
            "constant":  -6.280534875,
            "individual_dummy": {
                "age_18-29":  0.632156675 - 1.3263,
                "age_30-49":  1.106558979 + 0.9876,
                "age_50-64":  0.636516485 ,
                "age_65-99":  1.250192981 +  0.394182783 - 0.3030,
                "car_users":  1.544612164
            },
            "zone": {
                "share_detached_houses": -0.8050000
            },
        },
# utility function 36
        ("hs", "hs", "ho", "ho") : {
            "constant":  -5.728407971,
            "individual_dummy": {
                "age_18-29":  0.632156675 - 0.8239,
                "age_30-49":  1.106558979 + 0.4522,
                "age_50-64":  0.636516485 + 0.3281,
                "age_65-99":  1.250192981 +  0.394182783 - 0.0183,
                "car_users":  1.544612164
            },
            "zone": {
                "share_detached_houses": -0.8050000
            },
        },
# utility function 37
        ("hs", "ho", "ho", "ho") : {
            "constant":  -5.167664200,
            "individual_dummy": {
                "age_18-29":  0.632156675 - 0.8511,
                "age_30-49":  1.106558979 + 0.7283,
                "age_50-64":  0.636516485 - 0.0824,
                "age_65-99":  1.250192981 +  0.394182783 - 0.0263,
                "car_users":  1.544612164
            },
            "zone": {
                "share_detached_houses": -0.8050000
            },
        },
# utility function 38
        ("ho", "ho", "ho", "ho") : {
            "constant":  -4.892323651,
            "individual_dummy": {
                "age_18-29":  0.000000000 - 2.0113,
                "age_30-49":  0.000000000 + 0.2214,
                "age_50-64":  0.000000000 + 0.6946,
                "age_65-99":  0.394182783 - 0.0943,
                "car_users":  1.544612164
            },
            "zone": {
                "share_detached_houses": -0.8050000
            },
        },
    },
}

tour_conditions = {
    ("hw",): (False, "age_7-17"),
    ("hc",): (True, "age_7-17"),
    ("hu",): (False, "age_7-17"),
    ("hw", "hw"): (False, "age_7-17"),
    ("hw", "hu"): (False, "age_7-17"),
    ("hw", "hs"): (False, "age_7-17"),
    ("hw", "ho"): (False, "age_7-17"),
    ("hc", "hc"): (True, "age_7-17"),
    ("hc", "hs"): (True, "age_7-17"),
    ("hc", "ho"): (True, "age_7-17"),
    ("hu", "hs"): (False, "age_7-17"),
    ("hu", "ho"): (False, "age_7-17"),
    ("hw", "hw", "ho"): (False, "age_7-17"),
    ("hw", "hs", "hs"): (False, "age_7-17"),
    ("hw", "hs", "ho"): (False, "age_7-17"),
    ("hw", "ho", "ho"): (False, "age_7-17"),
    ("hc", "hs", "ho"): (True, "age_7-17"),
    ("hc", "ho", "ho"): (True, "age_7-17"),
    ("hu", "hs", "ho"): (False, "age_7-17"),
    ("hu", "ho", "ho"): (False, "age_7-17"),
    ("hs", "hs", "hs"): (False, "age_7-17"),
    ("hs", "hs", "ho"): (False, "age_7-17"),
    ("hs", "ho", "ho"): (False, "age_7-17"),
    ("ho", "ho", "ho"): (False, "age_7-17"),
    ("hw", "hs", "hs", "ho"): (False, "age_7-17"),
    ("hw", "hs", "ho", "ho"): (False, "age_7-17"),
    ("hw", "ho", "ho", "ho"): (False, "age_7-17"),
    ("hs", "hs", "hs", "hs"): (False, "age_7-17"),
    ("hs", "hs", "hs", "ho"): (False, "age_7-17"),
    ("hs", "hs", "ho", "ho"): (False, "age_7-17"),
    ("hs", "ho", "ho", "ho"): (False, "age_7-17"),
    ("ho", "ho", "ho", "ho"): (False, "age_7-17"),
}
tour_generation = {
    "hw": {
        "population": 0.421190694312828,
    },
    "hc": {
        "population": 0.11729635156358,
    },
    "hu": {
        "population": 0.0560714987587779,
    },
    "hs": {
        "population": 0.33693603147271,
    },
    "ho": {
        "population": 0.549510154252463,
    },
    "hoo": {
        "hw": {
            "car": 0.0803505590286341 / 0.421190694312828,
            "transit": 0.0631860320256202 / 0.421190694312828,
            "bike": 0.0168426955247172 / 0.421190694312828,
            "walk": 0.00882652405770048 / 0.421190694312828,
        },
        "hc": {
            "car": 0.00605142271605415 / 0.11729635156358,
            "transit": 0.00713210038247794 / 0.11729635156358,
            "bike": 0.0046272430085583 / 0.11729635156358,
            "walk": 0.00608329857890972 / 0.11729635156358,
        },
        "hu": {
            "car": 0.0034663682342903 / 0.0560714987587779,
            "transit": 0.0147227519917981 / 0.0560714987587779,
            "bike": 0.00109245930286708 / 0.0560714987587779,
            "walk": 0.00213086543691209 / 0.0560714987587779,
        },
        "hs": {
            "car": 0.0448579256071604 / 0.33693603147271,
            "transit": 0.0176773452875475 / 0.33693603147271,
            "bike": 0.00359034180559277 / 0.33693603147271,
            "walk": 0.0132361046691764 / 0.33693603147271,
        },
        "ho": {
            "car": 0.0392259245387762 / 0.549510154252463,
            "transit": 0.0196074421434222 / 0.549510154252463,
            "bike": 0.00566212353370659 / 0.549510154252463,
            "walk": 0.00990947303452182 / 0.549510154252463,
        },
        "wo": {
            "car": 0.00315162485929177 / 0.065007389777543,
            "transit": 0.00177006489416014 / 0.065007389777543,
            "bike": 0.000386671503740472 / 0.065007389777543,
            "walk": 0.000584040215529239 / 0.065007389777543,
        },
        "oo": {
            "car": 0.00305390275694459 / 0.0656146108075569,
            "transit": 0.00269475052921333 / 0.0656146108075569,
            "bike": 9.23278766544668e-5 / 0.0656146108075569,
            "walk": 0.00162839340586467 / 0.0656146108075569,
        },
    },
    "wo": {
        "hw": 0.065007389777543 / 0.421190694312828, # 0.1543419
    },
    "oo": {
        "hc": 0.009279938 / 0.11729635156358, # 0.079115314
        "hu": 0.006094387 / 0.0560714987587779, # 0.108689567
        "hs": 0.000323814 / 0.33693603147271, # 0.000961055
        "ho": 0.049916472 / 0.549510154252463, # 0.090838126
    },
    "hwp": {
        "population": (1-0.0619) * 0.229078193053959,
    },
    "hop": {
        "population": (1-0.0619) * 0.524683573054545,
    },
    "sop": {
        "population": (1-0.0619) * 0.0503171031715505,
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

# Driver share of car tours
# Inverse of car occupancy
car_driver_share = {
    "hw": 0.928309883,
    "hc": 0,
    "hu": 0.805783638,
    "hs": 0.803581362,
    "ho": 0.669375456,
    "hoo": 0.79867104,
    "wo": 0.809134377,
    "oo": 0.691710941,
    "hwp": 0.923397539,
    "hop": 0.699605826,
    "oop": 0.784781268,
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
        "age_7-17": -9999,
        ("age_18-29", "male"): 0.2969,
        ("age_30-49", "female"): 1.1019,
        ("age_30-49", "male"): 1.4157,
        ("age_50-64", "female"): 0.8173,
        ("age_50-64", "male"): 1.9978,
        ("age_65-99", "male"): 1.8737,
    },
}
car_density = {
    "constant": 0.0,
    "generation": {
        "share_detached_houses_new": 2.523e-01, # Originally estimated for percentages (0-100), here transformed
        "helsinki": 3.782e-02,
        "surrounding": 5.043e-02,
    },
    "log": {
        "time_ratio": 1.708e-01,
        "cost_ratio": 1.708e-01,
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
# O-D pairs with demand below threshold are neglected in sec dest calculation
secondary_destination_threshold = 0.1

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
        "name": "wo",
        "orig": "source",
        "dest": "other",
        "source": ("hw",),
        "area": "all",
    },
    {
        "name": "oo",
        "orig": "source",
        "dest": "other",
        "source": ("hc", "hu", "hs", "ho",),
        "area": "all",
    },
    {
        "name": "hoo",
        "orig": "home",
        "dest": "any",
        "sec_dest": "any",
        "source": ("hw", "hc", "hu", "hs", "ho", "wo", "oo",),
        "area": "metropolitan",
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
