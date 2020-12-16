import numpy
import random

import parameters.car as param
import parameters.zone as zone_param


class Tour(object):
    """Tour definition for agent-based simulation.
    
    Parameters
    ----------
    purpose : datatypes.purpose.TourPurpose
        Travel purpose (hw/hs/ho/...)
    origin : int or Tour
        Origin zone number or origin tour (if non-home tour)
    """
    # Expansion factor used on demand in departure time model
    matrix = numpy.array([[1 / zone_param.agent_demand_fraction]])

    def __init__(self, purpose, origin):
        self.purpose = purpose
        self.orig = origin
        try:
            self.sec_dest_prob = purpose.sec_dest_purpose.gen_model.param[purpose.name]
        except AttributeError:
            self.sec_dest_prob = 0

    @property
    def orig(self):
        return self.purpose.zone_data.zone_numbers[self.position[0]]

    @orig.setter
    def orig(self, origin):
        zone_data = self.purpose.zone_data
        try:
            self.position = (zone_data.zone_index(origin),)
        except IndexError:
            self._source = origin

    @property
    def dest(self):
        if len(self.position) > 1:
            return self.purpose.zone_data.zone_numbers[self.position[1]]
        else:
            return None

    @dest.setter
    def dest(self, destination):
        self.position = (
            self.position[0],
            self.purpose.zone_data.zone_index(destination)
        )

    @property
    def sec_dest(self):
        if len(self.position) > 2:
            return self.purpose.zone_data.zone_numbers[self.position[2]]
        else:
            return None

    @sec_dest.setter
    def sec_dest(self, destination):
        self.position = (
            self.position[0],
            self.position[1],
            self.purpose.zone_data.zone_index(destination)
        )

    @property
    def position(self):
        try:
            return self._position
        except AttributeError:
            self.orig = self._source.dest
            return self.position

    @position.setter
    def position(self, position):
        self._position = position

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

    def choose_destination(self, sec_dest_tours):
        """Choose primary destination for the tour.

        Assumes tour purpose model has already calculated probability matrices.

        Parameters
        ----------
        sec_dest_tours : dict
            Mode (car/transit/bike/walk) : dict
               Dictionary for inserting tours with secondary destination,
               key is `self.position`
        """
        dest_idx = numpy.searchsorted(
            self.purpose.model.cumul_dest_prob[self.mode][:, self.position[0]],
            random.random())
        self.dest = self.purpose.zone_data.zone_numbers[dest_idx]
        self.purpose.attracted_tours[self.mode][dest_idx] += 1
        purpose = self.purpose.sec_dest_purpose
        try:
            if (self.position[0] < purpose.bounds.stop
                    and self.position[1] < purpose.bounds.stop):
                is_in_area = True
            else:
                is_in_area = False
        except AttributeError:
            is_in_area = False
        if (self.mode != "walk" and is_in_area
                and random.random() < self.sec_dest_prob):
            try:
                sec_dest_tours[self.mode][self.position].append(self)
            except KeyError:
                sec_dest_tours[self.mode][self.position] = [self]

    def choose_secondary_destination(self, probs):
        """Choose secondary destination for the tour.

        Parameters
        ----------
        probs : numpy.ndarray
            1d array with probabilities for destinations
        """
        purpose = self.purpose.sec_dest_purpose
        self.sec_dest = numpy.random.choice(
            a=purpose.zone_numbers, p=probs)
        purpose.attracted_tours[self.mode][self.position[2]] += 1
    
    def choose_driver(self):
        """Choose if tour is as car driver or car passenger."""
        # TODO Differentiate car users and others
        if random.random() > param.car_driver_share[self.purpose.name]:
            self.mode = "car_passenger"
