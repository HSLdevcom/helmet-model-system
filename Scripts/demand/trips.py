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
        bounds = (0, zone_data.first_peripheral_zone)
        self.cm = logit.CarUseModel(zone_data, bounds)
        zone_data["car_users"] = self.cm.calc_prob()
        self.age_groups = (
            (7, 17),
            (18, 29),
            (30, 49),
            (50, 64),
            (65, 99),
        )

    def create_population_segments(self):
        self.segments = {}
        first_peripheral_zone = self.zone_data.first_peripheral_zone
        pop = self.zone_data["population"][:first_peripheral_zone]
        for age_group in self.age_groups:
            age = "age_" + str(age_group[0]) + "-" + str(age_group[1])
            self.segments[age] = {}
            key = "share_" + age
            age_share = self.zone_data[key][:first_peripheral_zone]
            car_use_f = self.cm.calc_individual_prob(
                age, Person.FEMALE)
            car_use_m = self.cm.calc_individual_prob(
                age, Person.MALE)
            car_share = 0.5*car_use_f + 0.5*car_use_m
            self.segments[age]["car_users"] = car_share * age_share * pop
            self.segments[age]["no_car"] = (1-car_share) * age_share * pop

    def create_population(self):
        """Create population for agent-based simulation."""
        self.cm.calc_basic_prob()
        self.population = []
        zones = self.zone_data.zone_numbers[:self.zone_data.first_peripheral_zone]
        generation_model = logit.GenerationModel(self.zone_data)
        for idx in zones:
            weights = [1]
            for age_group in self.age_groups:
                key = "share_age_" + str(age_group[0]) + "-" + str(age_group[1])
                share = self.zone_data[key][idx]
                weights.append(share)
                weights[0] -= share
            for _ in xrange(0, self.zone_data["population"][idx]):
                a = numpy.arange(-1, len(self.age_groups))
                group = numpy.random.choice(a=a, p=weights)
                if group != -1:
                    # Group -1 is under-7-year-olds and they have weights[0]
                    age_group = self.age_groups[group]
                    person = Person(idx, age_group, generation_model, self.cm)
                    self.population.append(person)