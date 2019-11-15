import numpy
import random
from datatypes.tour import Tour

class Person:
    FEMALE = 0
    MALE = 1
    
    def __init__(self, zone, age_group, generation_model, car_use_model):
        self.zone = zone
        self.age = random.randint(age_group[0], age_group[1])
        self.age_group = "age_" + str(age_group[0]) + "-" + str(age_group[1])
        self.sex = random.random() < 0.5
        self.tours = []
        self.generation_model = generation_model
        car_use_prob = car_use_model.calc_individual_prob(
            self.age_group, self.gender, zone)
        self.is_car_user = random.random() < car_use_prob
    
    @property
    def gender(self):
        if self.sex == Person.FEMALE:
            return "female"
        else:
            return "male"

    def add_tours(self, purposes):
        self.tours = []
        prob = self.generation_model.calc_prob(self.age_group, self.is_car_user, self.zone)
        pattern = numpy.random.choice(a=prob.keys(), p=prob.values())
        tour_list = pattern.split('-')
        if tour_list[0] == "":
            tour_list = []
        for key in tour_list:
            tour = Tour(purposes[key], self.zone)
            self.tours.append(tour)