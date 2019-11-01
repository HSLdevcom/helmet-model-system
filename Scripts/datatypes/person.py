class Person:
    def __init__(self, zone, age, generation_model):
        self.zone = zone
        self.age = age
        self.tours = []
        self.generation_model = generation_model
    
    def add_tours(self):
        self.tours = self.generation_model.generate_tours(self.age, is_car_user=True)