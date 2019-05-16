import logging
import os
import numpy
from assignment.test_assignment import TestAssignmentModel
import assignment.departure_time as dt
from data_handling import ZoneData, MatrixData
from demand.freight import FreightModel

logging.basicConfig(format='%(asctime)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO)
logger = logging.getLogger()
zdata_base = ZoneData("2016")
zdata_forecast = ZoneData("2030")
mdata = MatrixData("base")
fm = FreightModel(zdata_base, zdata_forecast, mdata)
trucks = fm.calc_freight_traffic("truck")
trailer_trucks = fm.calc_freight_traffic("trailer_truck")
costs = MatrixData("2016")
ass_model = TestAssignmentModel(costs)
dtm = dt.DepartureTimeModel(ass_model)
# nr_zones = len(ass_model.get_zone_numbers())
car_matrix = numpy.arange(6).reshape(2, 3)
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
}

logger.info("Adding demand and assigning")

for purpose in demand:
    for mode in demand[purpose]:
        dtm.add_demand(purpose, mode, demand[purpose][mode])
dtm.add_demand("freight", "truck", trucks)
dtm.add_demand("freight", "trailer_truck", trailer_trucks)
dtm.assign()

logger.info("Done")
