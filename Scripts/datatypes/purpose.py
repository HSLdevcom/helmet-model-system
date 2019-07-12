import parameters as param

class TourPurpose:
    def __init__(self, spec, zone_data):
        self.name = spec["name"]
        self.orig = spec["orig"]
        self.dest = spec["dest"]
        self.area = spec["area"]
        self.sources = []
        self.generation_param = param.tour_generation[self.name]
        self.dest_choice_param = param.destination_choice[self.name]
        self.mode_choice_param = param.mode_choice[self.name]
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

def create_purposes(zone_data):
    tour_purposes = []
    purpose_dict = {}
    for purpose_spec in param.tour_purposes:
        purpose = TourPurpose(purpose_spec, zone_data)
        tour_purposes.append(purpose)
        purpose_dict[purpose_spec["name"]] = purpose
    for purpose_spec in param.tour_purposes:
        purpose = purpose_dict[purpose_spec["name"]]
        if "source" in purpose_spec:
            for source in purpose_spec["source"]:
                purpose.sources.append(purpose_dict[source])
    return tour_purposes