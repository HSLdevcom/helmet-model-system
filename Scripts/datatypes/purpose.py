import parameters

class TourPurpose:
    def __init__(self, spec):
        self.name = spec["name"]
        self.orig = spec["orig"]
        self.dest = spec["dest"]
        self.area = spec["area"]
        self.sources = []
        self.generation_param = parameters.tour_generation[self.name]
        self.dest_choice_param = parameters.destination_choice[self.name]
        self.mode_choice_param = parameters.mode_choice[self.name]

def create_purposes():
    tour_purposes = []
    purpose_dict = {}
    for purpose_spec in parameters.tour_purposes:
        purpose = TourPurpose(purpose_spec)
        tour_purposes.append(purpose)
        purpose_dict[purpose_spec["name"]] = purpose
    for purpose_spec in parameters.tour_purposes:
        purpose = purpose_dict[purpose_spec["name"]]
        if "source" in purpose_spec:
            for source in purpose_spec["source"]:
                purpose.sources.append(purpose_dict[source])
    return tour_purposes