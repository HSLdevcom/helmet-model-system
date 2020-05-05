import numpy
import random
import parameters


class Tour:
    """Tour definition for agent-based simulation.
    
    Parameters
    ----------
    purpose : datatypes.purpose.TourPurpose
        Travel purpose (hw/hs/ho/...)
    origin : int or Tour
        Origin zone number or origin tour (if non-home tour)
    """

    def __init__(self, purpose, origin):
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
        """Index position in matrix where to insert the demand.
        
        Returns
        -------
        tuple of ints
            (origin, destination, (secondary destination))
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
        """Choose tour travel mode.

        Assumes tour purpose model has already calculated probability matrices.
        
        Parameters
        ----------
        is_car_user : bool
            Whether the person is car user or not
        """
        model = self.purpose.model
        probs = model.calc_individual_mode_prob(is_car_user, self.position[0])
        self.mode = numpy.random.choice(a=self.purpose.modes, p=probs)
        self.purpose.generated_tours[self.mode][self.position[0]] += 1

    def choose_destination(self, impedance):
        """Choose primary and possibly secondary destinations for the tour.

        Assumes tour purpose model has already calculated probability matrices.

        Parameters
        ----------
        impedance : dict
            Mode (car/transit/bike/walk) : dict
                Type (time/cost/dist) : numpy.ndarray
                    2d matrix with purpose impedance
        """
        # Primary destination choice
        probs = self.purpose.model.dest_prob[self.mode][:, self.position[0]]
        self.dest = numpy.random.choice(
            a=self.purpose.zone_data.zone_numbers, p=probs)
        self.purpose.attracted_tours[self.mode][self.position[1]] += 1
        # Secondary destination choice
        sec_dest_purpose = self.purpose.sec_dest_purpose
        try:
            if (self.position[0] < sec_dest_purpose.bounds.stop
                    and self.position[1] < sec_dest_purpose.bounds.stop):
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
        """Choose if tour is as car driver or car passenger."""
        # TODO Differentiate car users and others
        if random.random() > parameters.car_driver_share[self.purpose.name]:
            self.mode = "car_passenger"
