import assignment.emme_assignment as ass
import assignment.departure_time as dt
import logging
import numpy
import omx
import os
from parameters import emme_scenario, demand_share
from emme.emme_context import EmmeContext

logging.basicConfig(format='%(asctime)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO)
script_dir = os.path.dirname(os.path.realpath('__file__'))
project_dir = os.path.join(script_dir, "..")
for file_name in os.listdir(project_dir):
    if file_name.endswith(".emp"):
        empfile = os.path.join(project_dir, file_name)
emme_context = EmmeContext(empfile)
ass_model = ass.EmmeAssignmentModel(emme_context)
dtm = dt.DepartureTimeModel(ass_model)
nr_zones = len(ass_model.get_zone_numbers())
car_matrix = numpy.arange(nr_zones**2).reshape(nr_zones, nr_zones)
demand = {
    "hw": {
        "car": car_matrix,
        "transit": car_matrix,
        "bike": car_matrix,
    },
    "hs": {
        "car": car_matrix,
    },
    "ho": {
        "car": car_matrix,
    },
    "freight": {
        "trailer_truck": car_matrix,
        "truck": car_matrix,
        "van": car_matrix,
    },
}
for purpose in demand:
    for mode in demand[purpose]:
        dtm.add_demand(purpose, mode, demand[purpose][mode])
travel_cost = dtm.assign()
for time_period in travel_cost:
    for mtx_type in travel_cost[time_period]:
        filename = os.path.join(project_dir, "Matrices", mtx_type+'_'+time_period+".omx")
        costs_file = omx.openFile(filename, 'w')
        costs_file.createMapping("zone_number", ass_model.get_zone_numbers())
        for ass_class in travel_cost[time_period][mtx_type]:
            costs_file[ass_class] = travel_cost[time_period][mtx_type][ass_class]
        costs_file.close()
