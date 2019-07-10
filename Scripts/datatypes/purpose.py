import parameters

class TourPurpose:
    def __init__(self, purpose_name):
        self.name = purpose_name
        self.orig = parameters.tour_purposes[purpose_name]["orig"]
        self.dest = parameters.tour_purposes[purpose_name]["dest"]
        self.area = parameters.tour_purposes[purpose_name]["area"]
        self.sources = []
