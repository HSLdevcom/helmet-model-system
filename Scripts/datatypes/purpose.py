import parameters as param
import models.logit as logit
import models.generation as generation
import numpy
import pandas

class Purpose:
    def __init__(self, spec, zone_data):
        self.name = spec["name"]
        self.orig = spec["orig"]
        self.dest = spec["dest"]
        self.area = spec["area"]
        self.sources = []
        if self.area == "metropolitan":
            l = 0
            u = zone_data.zone_numbers.get_loc(param.first_peripheral_zone)
        if self.area == "peripheral":
            l = zone_data.zone_numbers.get_loc(param.first_peripheral_zone)
            u = zone_data.nr_zones
        if self.area == "all":
            l = 0
            u = zone_data.nr_zones
        self.bounds = (l, u)
        self.zone_data = zone_data
        self.generated_tours = {}
        self.attracted_tours = {}


class TourPurpose(Purpose):
    def __init__(self, spec, zone_data):
        Purpose.__init__(self, spec, zone_data)
        if self.orig == "source":
            self.gen_model = generation.NonHomeGeneration(zone_data, self)
        else:
            self.gen_model = generation.GenerationModel(zone_data, self)
        if self.name == "sop":
            self.model = logit.OriginModel(zone_data, self)
        elif self.name == "so":
            self.model = logit.DestModeModel(zone_data, self)
        else:
            self.model = logit.ModeDestModel(zone_data, self)

    def calc_demand(self, impedance):
        tours = self.gen_model.generate_tours()
        prob = self.model.calc_prob(impedance)
        car_share = self.zone_data.get_data("car_use_share", self, True)
        for mod_mode in self.model.mode_choice_param:
            if "car_users" in self.model.mode_choice_param[mod_mode]:
                car_prob = self.model.calc_car_users_prob(mod_mode)
                for mode in prob:
                    no_car = (1 - car_share) * prob[mode]
                    car = car_share * car_prob[mode]
                    prob[mode] = no_car + car
        self.demand = {}
        self.aggregated_demand = {}
        for mode in self.model.mode_choice_param:
            self.demand[mode] = (prob[mode] * tours).T
            self.attracted_tours[mode] = self.demand[mode].sum(0)
            self.generated_tours[mode] = self.demand[mode].sum(1)
            self.aggregated_demand[mode] = self.aggregate(self.demand[mode])
        return self.demand

    def aggregate(self, mtx):
        dest = self.zone_data.zone_numbers
        orig = self.zone_data.zone_numbers[self.bounds[0]:self.bounds[1]]
        mtx = pandas.DataFrame(mtx, orig, dest)
        idx = param.areas.keys()
        aggr_mtx = pandas.DataFrame(0, idx, idx)
        tmp_mtx = pandas.DataFrame(0, idx, dest)
        for area in param.areas:
            l = param.areas[area][0]
            u = param.areas[area][1]
            tmp_mtx.loc[area] = mtx.loc[l:u].sum(0).values
        for area in param.areas:
            l = param.areas[area][0]
            u = param.areas[area][1]
            aggr_mtx.loc[:, area] = tmp_mtx.loc[:, l:u].sum(1).values
        return aggr_mtx


class SecDestPurpose(Purpose):
    def __init__(self, spec, zone_data):
        Purpose.__init__(self, spec, zone_data)
        self.gen_model = generation.SecDestGeneration(zone_data, self)
        self.model = logit.SecDestModel(zone_data, self)

    def generate_tours(self):
        self.tours = {}
        for mode in self.model.dest_choice_param:
            self.tours[mode] = self.gen_model.generate_tours(mode)
            self.attracted_tours[mode] = self.tours[mode].sum(0)
            self.generated_tours[mode] = self.tours[mode].sum(1)

    def distribute_tours(self, mode, impedance, origin):
        dest_imp = {}
        for mtx_type in impedance:
            dest_imp[mtx_type] = ( impedance[mtx_type]
                                 + impedance[mtx_type][:, origin]
                                 - impedance[mtx_type][origin, :][:, numpy.newaxis])
        prob = self.model.calc_prob(mode, dest_imp)
        demand = (prob * self.tours[mode][origin, :]).T
        self.attracted_tours[mode] += demand.sum(0)
        return demand