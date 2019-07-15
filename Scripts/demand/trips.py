import numpy
import pandas
import parameters
from datatypes.purpose import TourPurpose

class DemandModel:
    def __init__(self, zone_data):
        self.tour_purposes = []
        purpose_dict = {}
        for purpose_spec in parameters.tour_purposes:
            purpose = TourPurpose(purpose_spec, zone_data)
            self.tour_purposes.append(purpose)
            purpose_dict[purpose_spec["name"]] = purpose
        for purpose_spec in parameters.tour_purposes:
            if "source" in purpose_spec:
                purpose = purpose_dict[purpose_spec["name"]]
                for source in purpose_spec["source"]:
                    purpose.sources.append(purpose_dict[source])
