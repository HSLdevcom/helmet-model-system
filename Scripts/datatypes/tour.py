import numpy

class Tour:
    def __init__(self, purpose, orig):
        self._purpose = purpose
        self.orig = orig
        self.matrix = 1
        self.has_sec_dest = False

    @property 
    def purpose(self):
        if self.has_sec_dest and self.mode != "walk":
            return self._purpose.sec_dest_purpose
        else:
            return self._purpose
    
    @property
    def position(self):
        zone_numbers = self._purpose.zone_data.zone_numbers
        position = []
        position.append(zone_numbers.get_loc(self.orig))
        try:
            position.append(zone_numbers.get_loc(self.dest))
        except AttributeError:
            pass
        try:
            position.append(zone_numbers.get_loc(self.sec_dest))
        except AttributeError:
            pass
        return position

    def choose_mode(self):
        probs = []
        for mode in self._purpose.modes:
            probs.append(self._purpose.model.mode_prob[mode][self.position[0]])
        self.mode = numpy.random.choice(a=self._purpose.modes, p=probs)

    def choose_destination(self, impedance):
        zone_numbers = self._purpose.zone_data.zone_numbers
        probs = self._purpose.model.dest_prob[self.mode][:, self.position[0]]
        self.dest = numpy.random.choice(a=zone_numbers, p=probs)
        if self.has_sec_dest and self.mode != "walk":
            probs = self.purpose.calc_prob(self.mode, impedance[self.mode], self.position)
            self.sec_dest = numpy.random.choice(a=zone_numbers, p=probs)
        else:
            try:
                del self.sec_dest
            except AttributeError:
                pass