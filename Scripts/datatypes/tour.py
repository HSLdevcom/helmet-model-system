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
        self._is_car_passenger = (True
            if random.random() > param.car_driver_share[self.purpose.name]
            else False)
        self._mode_draw = random.random()
        self._dest_draw = random.random()
        self._sec_dest_gen_draw = random.random()
        self._sec_dest_draw = random.random()

    @property
    def mode(self):
            return self.purpose.modes[self._mode_idx]

    @property
    def is_car_passenger(self):
        return self.mode == "car" and self._is_car_passenger

    @property
    def orig(self):
        return self.purpose.zone_data.zone_numbers[self.position[0]]

    @orig.setter
    def orig(self, origin):
        try:
            self._position = (self.purpose.zone_data.zone_index(origin),)
        except KeyError:
            # If this is non-home tour, origin refers to home-based tour
            self._source = origin
            self._non_home_position = ()

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
        """Index position in matrix where to insert the demand.

        Returns
        -------
        tuple of ints
            (origin, destination, (secondary destination))
        """
        try:
            return self._position
        except AttributeError:
            return self._source.position[:1] + self._non_home_position

    @position.setter
    def position(self, position):
        try:
            _ = self._position[0]
            self._position = position
        except AttributeError:
            self._non_home_position = position[1:]

    def choose_mode(self, is_car_user):
        """Choose tour travel mode.

        Assumes tour purpose model has already calculated probability matrices.
        
        Parameters
        ----------
        is_car_user : bool
            Whether the person is car user or not
        """
        self._mode_idx = numpy.searchsorted(
            self.purpose.model.calc_individual_mode_prob(
                is_car_user, self.position[0]).cumsum(),
            self._mode_draw)
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
        orig_idx = self.position[0]
        orig_rel_idx = orig_idx - self.purpose.bounds.start
        dest_idx = numpy.searchsorted(
            self.purpose.model.cumul_dest_prob[self.mode][:, orig_rel_idx],
            self._dest_draw)
        self.position = (orig_idx, dest_idx)
        self.purpose.attracted_tours[self.mode][dest_idx] += 1
        self.purpose.histograms[self.mode].add(
            self.purpose.dist[orig_rel_idx, dest_idx])
        self.purpose.aggregates[self.mode].add(self.orig, self.dest)
        if orig_idx == dest_idx:
            self.purpose.own_zone_aggregates[self.mode].add(self.orig)
        bounds = self.purpose.sec_dest_purpose.bounds
        try:
            if (bounds.start <= orig_idx < bounds.stop
                    and bounds.start <= dest_idx < bounds.stop):
                is_in_area = True
            else:
                is_in_area = False
        except AttributeError:
            is_in_area = False
        if (self.mode != "walk" and is_in_area
                and self._sec_dest_gen_draw < self.sec_dest_prob[self.mode]):
            orig_rel_idx = orig_idx - bounds.start
            dest_idx =- bounds.start
            sec_dest_tours[self.mode][orig_rel_idx][dest_idx].append(self)

    def choose_secondary_destination(self, cumulative_probs):
        """Choose secondary destination for the tour.

        Parameters
        ----------
        cumulative_probs : numpy.ndarray
            1d array with cumulative probabilities for destinations
        """
        dest_idx = (self.purpose.sec_dest_purpose.bounds.start
                    + numpy.searchsorted(cumulative_probs, self._sec_dest_draw))
        self.position = (self.position[0], self.position[1], dest_idx)
        self.purpose.sec_dest_purpose.attracted_tours[self.mode][dest_idx] += 1
