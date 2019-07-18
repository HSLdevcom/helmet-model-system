class Demand:
    def __init__(self, purpose, mode, matrix, origin=None):
        self.purpose = purpose
        self.mode = mode
        self.matrix = matrix
        self.origin = origin

    @property
    def position(self):
        if self.origin is None:
            return (self.purpose.bounds[0], 0)
        else:
            return (self.origin, 0, 0)