import parameters.assignment as param
from assignment.datatypes.car import Car

class CarSpecification:
    """
    Car assignment specification.

    Parameters
    ----------
    demand_mtx : dict
        key : str
            Assignment class (transit_work/transit_leisure)
        value : dict
            id : str
                Emme matrix id
            description : dict
                Matrix description
    result_mtx : dict
        key : str
            Impedance type (time/cost/dist)
        value : dict
            key : str
                Assignment class (transit_work/transit_leisure)
            value : dict
                id : str
                    Emme matrix id
                description : dict
                    Matrix description
    """
    def __init__(self, extra, demand_mtx, result_mtx):
        self.car_work = Car(
            "car_work", extra, demand_mtx, result_mtx,
            link_costs=extra("total_cost"))
        self.car_leisure = Car(
            "car_leisure", extra, demand_mtx, result_mtx,
            link_costs=extra("total_cost"))
        self.van = Car(
            "van", extra, demand_mtx, result_mtx,
            link_costs=extra("total_cost"))
        self.truck = Car(
            "truck", extra, demand_mtx, result_mtx,
            value_of_time_inv=param.freight_dist_unit_time,
            link_costs="length")
        self.trailer_truck = Car(
            "trailer_truck", extra, demand_mtx, result_mtx,
            value_of_time_inv=param.freight_dist_unit_time,
            link_costs="length")
        self._spec = {
            "type": "SOLA_TRAFFIC_ASSIGNMENT",
            "background_traffic": {
                "link_component": param.background_traffic_attr,
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
