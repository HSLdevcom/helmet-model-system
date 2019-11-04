import numpy
from datatypes.tour import Tour

class Person:
    def __init__(self, zone, age, age_group, generation_model):
        self.zone = zone
        self.age = age
        self.age_group = age_group
        self.tours = []
        self.generation_model = generation_model
    
    def add_tours(self, purposes):
        self.tours = []
        prob = self.generation_model.calc_prob(self.zone, self.age_group, is_car_user=True)
        pattern = numpy.random.choice(a=prob.keys(), p=prob.values())
        tour_list = pattern.split('-')
        if tour_list[0] == "":
            tour_list = []
        for key in tour_list:
            tour = Tour(purposes[key], self.zone)
            self.tours.append(tour)