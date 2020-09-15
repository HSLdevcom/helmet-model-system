import parameters as param
from car import Car 

class CarSpecification:
    def __init__(self, demand_mtx, result_mtx):
        self.car_work = Car("car_work", demand_mtx, result_mtx)
        self.car_leisure = Car("car_leisure", demand_mtx, result_mtx)
        self.van = Car("van", demand_mtx, result_mtx)
        self.truck = Car(
            "truck", demand_mtx, result_mtx, 
            value_of_time_inv=0.2,link_costs="length")
        self.trailer_truck = Car(
            "trailer_truck", demand_mtx, result_mtx,
            value_of_time_inv=0.2, link_costs="length")
        self._spec = {
            "type": "SOLA_TRAFFIC_ASSIGNMENT",
            "background_traffic": {
                "link_component": param.background_traffic,
                "add_transit_vehicles": False,
            },
            "performance_settings": param.performance_settings,
            "stopping_criteria": None, # This is defined later
        }

    def spec (self, lightweight=False):
        if lightweight:
            self._spec["classes"] = [
                self.car_work.spec,
                self.car_leisure.spec,
                self.van.spec,
            ]
        else:
            self._spec["classes"] = [
                self.car_work.spec,
                self.car_leisure.spec,
                self.trailer_truck.spec,
                self.truck.spec,
                self.van.spec,
            ]
        return self._spec
