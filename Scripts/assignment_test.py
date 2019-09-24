import assignment.emme_assignment as ass
import assignment.departure_time as dt
import logging
import numpy
import pythonlibs.omx
import os
from parameters import emme_scenario, demand_share
from datahandling.zonedata import ZoneData
from datahandling.matrixdata import MatrixData
from datatypes.demand import Demand
from datatypes.purpose import Purpose
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
nr_zones = ass_model.nr_zones
dtm = dt.DepartureTimeModel(nr_zones)
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
    spec = {
        "name": purpose,
        "orig": None,
        "dest": None,
        "area": "all",
    }
    purp = Purpose(spec, zdata_forecast)
    for mode in demand[purpose]:
        dem = Demand(purp, mode, demand[purpose][mode])
        dtm.add_demand(dem)
travel_cost = {}
for tp in emme_scenario:
    ass_model.assign(tp, dtm.demand[tp])
    travel_cost[tp] = ass_model.get_impedance()
costs_files = MatrixData("2016")
for time_period in travel_cost:
    for mtx_type in travel_cost[time_period]:
        zone_numbers = ass_model.zone_numbers
        costs_files.open_file(mtx_type, time_period, 'w')
        costs_files.set_mapping(zone_numbers)
        for ass_class in travel_cost[time_period][mtx_type]:
            cost_data = travel_cost[time_period][mtx_type][ass_class]
            costs_files.set_data(cost_data, ass_class)
        costs_files.close()
