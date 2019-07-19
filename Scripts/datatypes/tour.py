import numpy

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
        zone_numbers = self._purpose.zone_data.zone_numbers
        position = [zone_numbers.get_loc(self.orig)]
        if self.dest is not None:
            position.append(zone_numbers.get_loc(self.dest))
        if self.sec_dest is not None:
            position.append(zone_numbers.get_loc(self.sec_dest))
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
            self.sec_dest = None