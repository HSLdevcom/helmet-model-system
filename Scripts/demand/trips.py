import numpy
import pandas
import parameters
from datatypes.purpose import Purpose, TourPurpose, SecDestPurpose
import models.logit as logit
from datatypes.person import Person
from datatypes.tour import Tour
import random


class DemandModel:
    def __init__(self, zone_data):
        """Container for private tour purposes and models.

        Parameters
        ----------
        zone_data : ZoneData
            Data used for all demand calculations
        """
        self.zone_data = zone_data
        self.tour_purposes = []
        self.purpose_dict = {}
        for purpose_spec in parameters.tour_purposes:
            if "sec_dest" in purpose_spec:
                purpose = SecDestPurpose(purpose_spec, zone_data)
            else:
                purpose = TourPurpose(purpose_spec, zone_data)
            self.tour_purposes.append(purpose)
            self.purpose_dict[purpose_spec["name"]] = purpose
        for purpose_spec in parameters.tour_purposes:
            if "source" in purpose_spec:
                purpose = self.purpose_dict[purpose_spec["name"]]
                for source in purpose_spec["source"]:
                    purpose.sources.append(self.purpose_dict[source])
                    if "sec_dest" in purpose_spec:
                        self.purpose_dict[source].sec_dest_purpose = purpose
        spec = {
            "name": "car_use",
            "orig": None,
            "dest": None,
            "area": "metropolitan",
        }
        cm = logit.CarUseModel(zone_data, Purpose(spec, zone_data))
        zone_data["car_users"] = cm.calc_prob()

    def create_population(self):
        """Create population for agent-based simulation."""
        self.population = []
        age_groups = (
            (7, 17),
            (18, 29),
            (30, 49),
            (50, 64),
            (65, 99),
        )
        zones = self.zone_data.zone_numbers[:self.zone_data.first_peripheral_zone]
        generation_model = logit.GenerationModel(self.zone_data)
        for idx, zone_pop in zones.iteritems():
            weights = [1]
            for age_group in age_groups:
                key = "share_age_" + str(age_group[0]) + "-" + str(age_group[1])
                share = self.zone_data[key][idx]
                weights.append(share)
                weights[0] -= share
            for _ in xrange(0, zone_pop):
                a = numpy.arange(-1, len(age_groups))
                group = numpy.random.choice(a=a, p=weights)
                if group != -1:
                    # Group -1 is under-7-year-olds and they have weights[0]
                    age_group = age_groups[group]
                    age = random.randint(age_group[0], age_group[1])
                    person = Person(idx, age, generation_model)
                    self.population.append(person)
        for person in self.population:
            for purpose in self.tour_purposes:
                if purpose.area == "metropolitan" and purpose.dest != "source" and not purpose.sources:
                    prob = purpose.gen_model.param["population"]
                    try:
                        sec_dest_prob = purpose.sec_dest_purpose.gen_model.param[purpose.name]
                        prob *= 1 + sec_dest_prob
                    except AttributeError:
                        sec_dest_prob = 0
                    if random.random() < prob:
                        tour = Tour(purpose, person.zone)
                        if random.random() < sec_dest_prob:
                            tour.has_sec_dest = True
                        person.tours.append(tour)