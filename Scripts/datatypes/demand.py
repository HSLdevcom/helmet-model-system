from __future__ import annotations
from typing import TYPE_CHECKING, Optional

import numpy # type: ignore
if TYPE_CHECKING:
    from datatypes.purpose import Purpose
import parameters.car as param


class Demand:
    # Only used for sister class Tour
    is_car_passenger = False

    def __init__(self, 
                 purpose: Purpose, 
                 mode: str, 
                 matrix: numpy.ndarray, 
                 origin: Optional[int]=None):
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
        if mode == "car" and purpose.name in param.car_driver_share:
            self.matrix = param.car_driver_share[purpose.name] * matrix
        else:
            self.matrix = matrix
        self.orig = origin
        self.dest = None # Destination will by default be whole model area

    @property
    def position(self):
        """tuple: (origin, destination, (secondary destination))
        Position where to insert the demand
        """
        start = self.purpose.bounds.start
        if self.orig is None:
            return (start, 0)
        else:
            return (self.orig, start, start)
