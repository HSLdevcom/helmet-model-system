import assignment.emme_assignment as ass
import assignment.departure_time as dt
import logging
import numpy
import pythonlibs.omx
import os
from parameters import emme_scenario, demand_share
from data_handling import MatrixData, ZoneData
from emme.emme_context import EmmeContext

logging.basicConfig(format='%(asctime)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO)
script_dir = os.path.dirname(os.path.realpath('__file__'))
project_dir = os.path.join(script_dir, "..")
for file_name in os.listdir(project_dir):
    if file_name.endswith(".emp"):
        empfile = os.path.join(project_dir, file_name)
zdata_forecast = ZoneData("2030")
emme_context = EmmeContext(empfile)
ass_model = ass.EmmeAssignmentModel(emme_context, zdata_forecast.car_dist_cost)
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
# filename = os.path.join(project_dir, "Matrices", "freight_vrk"+".omx")
# freight_file = omx.openFile(filename, 'w')
# freight_file.createMapping("zone_number", [5, 6, 7, 2792, 16001])
# for mode in demand["freight"]:
#     freight_file[mode] = demand["freight"][mode][:5,:5]
travel_cost = dtm.assign()
ass_model.calc_transit_cost(zdata_forecast.transit_zone)
costs_files = MatrixData("2016")
for time_period in travel_cost:
    for mtx_type in travel_cost[time_period]:
        zone_numbers = ass_model.get_zone_numbers()
        costs_files.open_file(mtx_type, time_period, 'w')
        costs_files.set_mapping(zone_numbers)
        for ass_class in travel_cost[time_period][mtx_type]:
            cost_data = travel_cost[time_period][mtx_type][ass_class]
            costs_files.set_data(cost_data, ass_class)
        costs_files.close()
