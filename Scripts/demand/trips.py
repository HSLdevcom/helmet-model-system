import numpy
import pandas
import parameters
from datatypes.purpose import TourPurpose, SecDestPurpose
from datatypes.person import Person
import random

class DemandModel:
    def __init__(self, zone_data):
        self.zone_data = zone_data
        self.tour_purposes = []
        purpose_dict = {}
        for purpose_spec in parameters.tour_purposes:
            if "sec_dest" in purpose_spec:
                purpose = SecDestPurpose(purpose_spec, zone_data)
            else:
                purpose = TourPurpose(purpose_spec, zone_data)
            self.tour_purposes.append(purpose)
            purpose_dict[purpose_spec["name"]] = purpose
        for purpose_spec in parameters.tour_purposes:
            if "source" in purpose_spec:
                purpose = purpose_dict[purpose_spec["name"]]
                for source in purpose_spec["source"]:
                    purpose.sources.append(purpose_dict[source])

    def create_population(self):
        self.population = []
        age_groups = (
            (7, 17),
            (18, 29),
            (30, 49),
            (50, 64),
            (65, 99),
        )
        for idx, zone_pop in self.zone_data.values["population"].iteritems():
            weights = [1]
            for age_group in age_groups:
                key = "share_age_" + str(age_group[0]) + "-" + str(age_group[1])
                share = self.zone_data.values[key][idx]
                weights.append(share)
                weights[0] -= share
            for _ in xrange(0, zone_pop):
                a = numpy.arange(-1, len(age_groups))
                group = numpy.random.choice(a=a, p=weights)
                if group != -1:
                    age_group = age_groups[group]
                    age = random.randint(age_group[0], age_group[1])
                    person = Person(idx, age)
                    self.population.append(person)
