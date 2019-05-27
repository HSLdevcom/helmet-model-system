import numpy

class DemandHS15:
    def __init__(self, zone_data):
        self.zone_data = zone_data

    def calc_demand(self, purpose, impedance):
        mtx = numpy.arange(6).reshape(2, 3)
        demand = {
            "car": mtx,
            "transit": mtx,
            "bike": mtx,
        }
        return demand
