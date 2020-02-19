import numpy
import random
import parameters


class Tour:
    def __init__(self, purpose, origin):
        """Tour definition for agent-based simulation.
        
        Parameters
        ----------
        purpose : Purpose
            Travel purpose (hw/hs/ho/...)
        origin : int
            Origin zone number
        """
        self.purpose = purpose
        self.orig = origin
        self.dest = None
        self.sec_dest = None
        self.matrix = 1  # So far, one person per tour
        try:
            self.sec_dest_prob = purpose.sec_dest_purpose.gen_model.param[purpose.name]
        except AttributeError:
            self.sec_dest_prob = 0
    
    @property
    def position(self):
        """tuple: (origin, destination, (secondary destination))
        Position where to insert the demand
        """
        zone_data = self.purpose.zone_data
        try:
            position = [zone_data.zone_index(self.orig)]
        except IndexError:
            position = [zone_data.zone_index(self.orig.dest)]
        if self.dest is not None:
            position.append(zone_data.zone_index(self.dest))
        if self.sec_dest is not None:
            position.append(zone_data.zone_index(self.sec_dest))
        return position

    def choose_mode(self, is_car_user):
        model = self.purpose.model
        probs = model.calc_individual_mode_prob(is_car_user, self.position[0])
        self.mode = numpy.random.choice(a=self.purpose.modes, p=probs)
        self.purpose.generated_tours[self.mode][self.position[0]] += 1

    def choose_destination(self, impedance):
        zone_numbers = self.purpose.zone_data.zone_numbers
        probs = self.purpose.model.dest_prob[self.mode][:, self.position[0]]
        self.dest = numpy.random.choice(a=zone_numbers, p=probs)
        self.purpose.attracted_tours[self.mode][self.position[1]] += 1
        sec_dest_purpose = self.purpose.sec_dest_purpose
        try:
            if self.position[1] < sec_dest_purpose.bounds.stop:
                is_in_area = True
            else:
                is_in_area = False
        except AttributeError:
            is_in_area = False
        if self.mode != "walk" and is_in_area and random.random() < self.sec_dest_prob:
            probs = sec_dest_purpose.calc_prob(
                self.mode, impedance[self.mode], self.position)
            self.sec_dest = numpy.random.choice(
                a=sec_dest_purpose.zone_numbers, p=probs)
            sec_dest_purpose.attracted_tours[self.mode][self.position[2]] += 1
        else:
            self.sec_dest = None
    
    def choose_driver(self):
        # TODO Differentiate car users and others
        if random.random() > parameters.car_driver_share[self.purpose.name]:
            self.mode = "car_passenger"
