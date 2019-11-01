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
        self.purpose = purpose
        self.orig = origin
        self.dest = None
        self.sec_dest = None
        self.matrix = 1 # So far, one person per tour
        self.has_sec_dest = False
    
    @property
    def position(self):
        """tuple: (origin, destination, (secondary destination))
        Position where to insert the demand
        """
        zone_numbers = self.purpose.zone_data.zone_numbers
        position = numpy.where(zone_numbers == self.orig)[0].tolist()
        if self.dest is not None:
            position.append(numpy.where(zone_numbers == self.dest)[0][0])
        if self.sec_dest is not None:
            position.append(numpy.where(zone_numbers == self.sec_dest)[0][0])
        return position

    def choose_mode(self):
        probs = []
        for mode in self.purpose.modes:
            probs.append(self.purpose.model.mode_prob[mode][self.position[0]])
        self.mode = numpy.random.choice(a=self.purpose.modes, p=probs)

    def choose_destination(self, impedance):
        zone_numbers = self.purpose.zone_data.zone_numbers
        probs = self.purpose.model.dest_prob[self.mode][:, self.position[0]]
        self.dest = numpy.random.choice(a=zone_numbers, p=probs)
        if self.has_sec_dest and self.mode != "walk":
            probs = self.purpose.sec_dest_purpose.calc_prob(
                self.mode, impedance[self.mode], self.position)
            self.sec_dest = numpy.random.choice(a=zone_numbers, p=probs)
            sec_dest = numpy.where(zone_numbers == self.sec_dest)[0][0]
            self.purpose.sec_dest_purpose.attracted_tours[self.mode][sec_dest] += 1
        else:
            self.sec_dest = None