import parameters as param
import models.logit as logit
import models.generation as generation

class TourPurpose:
    def __init__(self, spec, zone_data):
        self.name = spec["name"]
        self.orig = spec["orig"]
        self.dest = spec["dest"]
        self.area = spec["area"]
        self.sources = []
        self.generation_param = param.tour_generation[self.name]
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
        if self.orig == "source":
            self.generation = generation.NonHomeGeneration(zone_data, self)
        else:
            self.generation = generation.GenerationModel(zone_data, self)
        if self.name == "sop":
            self.model = logit.OriginModel(zone_data, self)
        elif self.name == "so":
            self.model = logit.DestModeModel(zone_data, self)
        else:
            self.model = logit.ModeDestModel(zone_data, self)

    def calc_demand(self, impedance):
        prob = self.model.calc_prob(impedance)
        tours = self.generation.generate_tours()
        demand = {}
        self.generated_tours = {}
        self.attracted_tours = {}
        for mode in self.model.mode_choice_param:
            demand[mode] = (prob[mode] * tours).T
            self.attracted_tours[mode] = demand[mode].sum(0)
            self.generated_tours[mode] = demand[mode].sum(1)
        return demand