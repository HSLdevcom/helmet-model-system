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
        self.matrix = 1 # So far, one person per tour
        try:
            sec_dest_prob = purpose.sec_dest_purpose.gen_model.param[purpose.name]
        except AttributeError:
            sec_dest_prob = 0
        if random.random() < sec_dest_prob:
            self.has_sec_dest = True
        else:
            self.has_sec_dest = False
    
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
        if self.has_sec_dest and self.mode != "walk":
            probs = self.purpose.sec_dest_purpose.calc_prob(
                self.mode, impedance[self.mode], self.position)
            self.sec_dest = numpy.random.choice(a=zone_numbers, p=probs)
            self.purpose.sec_dest_purpose.attracted_tours[self.mode][self.position[2]] += 1
        else:
            self.sec_dest = None
    
    def choose_driver(self):
        # TODO Differentiate car users and others
        if random.random() > parameters.car_driver_share[self.purpose.name]:
            self.mode = "car_passenger"