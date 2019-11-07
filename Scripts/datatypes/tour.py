import numpy
import random


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
        self._purpose = purpose
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
    def purpose(self):
        if self.has_sec_dest and self.mode != "walk":
            return self._purpose.sec_dest_purpose
        else:
            return self._purpose
    
    @property
    def position(self):
        """tuple: (origin, destination, (secondary destination))
        Position where to insert the demand
        """
        zone_data = self._purpose.zone_data
        position = [zone_data.zone_index(self.orig)]
        if self.dest is not None:
            position.append(zone_data.zone_index(self.dest))
        if self.sec_dest is not None:
            position.append(zone_data.zone_index(self.sec_dest))
        return position

    def choose_mode(self, is_car_user):
        model = self._purpose.model
        probs = model.calc_individual_mode_prob(is_car_user, self.orig)
        self.mode = numpy.random.choice(a=self._purpose.modes, p=probs)
        self.purpose.generated_tours[self.mode][self.position[0]] += 1

    def choose_destination(self, impedance):
        zone_numbers = self._purpose.zone_data.zone_numbers
        probs = self._purpose.model.dest_prob[self.mode][:, self.position[0]]
        self.dest = numpy.random.choice(a=zone_numbers, p=probs)
        self.purpose.attracted_tours[self.mode][self.position[1]] += 1
        if self.has_sec_dest and self.mode != "walk":
            probs = self.purpose.calc_prob(self.mode, impedance[self.mode], self.position)
            self.sec_dest = numpy.random.choice(a=zone_numbers, p=probs)
            self.purpose.attracted_tours[self.mode][self.position[2]] += 1
        else:
            self.sec_dest = None