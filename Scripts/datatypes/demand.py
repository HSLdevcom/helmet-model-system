import parameters

class Demand:
    def __init__(self, purpose, mode, matrix, origin=None):
        """Demand matrix for whole day
        
        Parameters
        ----------
        purpose : Purpose
            Travel purpose (hw/hs/ho/...)
        mode: str
            Travel mode (car/transit/bike)
        matrix : numpy 2-d matrix
            Travel demand matrix
        origin : int, optional
            Origin if matrix is destination -> sec-destination
        """
        self.purpose = purpose
        self.mode = mode
        if mode == "car" and purpose.name in parameters.car_driver_share:
            self.matrix = parameters.car_driver_share[purpose.name] * matrix
        else:
            self.matrix = matrix
        self.origin = origin

    @property
    def position(self):
        """tuple: (origin, destination, (secondary destination))
        Position where to insert the demand
        """
        if self.origin is None:
            return (self.purpose.bounds.start, 0)
        else:
            return (self.origin, 0, 0)