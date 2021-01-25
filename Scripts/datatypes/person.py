import numpy
import random

from datatypes.tour import Tour


class Person:
    """Container for person attributes.
    
    Parameters
    ----------
    zone : int
        Zone number, where person resides
    age_group : tuple
        int
            Age interval to which the person belongs
    generation_model : models.logit.TourCombinationModel
        Model used to create tours
    car_use_model : models.logit.CarUseModel
        Model used to decide if car user
    """

    FEMALE = 0
    MALE = 1
    
    def __init__(self, zone, age_group, generation_model, car_use_model):
        self.zone = zone
        self.age = random.randint(age_group[0], age_group[1])
        self.age_group = "age_" + str(age_group[0]) + "-" + str(age_group[1])
        self.sex = random.random() < 0.5
        self.tours = []
        self.generation_model = generation_model
        self._cm = car_use_model
        self._car_use_draw = random.random()
        self._tour_combination_draw = random.random()

    def decide_car_use(self):
        car_use_prob = self._cm.calc_individual_prob(
            self.age_group, self.gender, self.zone)
        self.is_car_user = self._car_use_draw < car_use_prob
    
    @property
    def gender(self):
        """Returns the person's gender.

        Returns
        -------
        str
            Gender (male/female)
        """
        if self.sex == Person.FEMALE:
            return "female"
        else:
            return "male"

    def add_tours(self, purposes, tour_probs):
        """Initilize tour list and add new tours.

        Parameters
        ----------
        purposes : dict
            key : str
                Tour purpose name (hw/ho/...)
            value : datatypes.purpose.TourPurpose
                The tour purpose object
        tour_probs : dict
            Age (age_7-17/...) : tuple
                Is car user (False/True) : numpy.array
                    Matrix with cumulative tour combination probabilities
                    for all zones
        """
        zone_idx = self.generation_model.zone_data.zone_index(self.zone)
        tour_comb_idx = numpy.searchsorted(
            tour_probs[self.age_group][self.is_car_user][zone_idx, :],
            self._tour_combination_draw)
        new_tours = list(self.generation_model.tour_combinations[tour_comb_idx])
        old_tours = self.tours
        self.tours = []
        for tour in old_tours:
            try:
                # Try to recycle old tour
                new_tours.remove(tour.purpose.name)
                self.tours.append(tour)
            except ValueError:
                # If name of old tour in not fould in list of new tours
                try:
                    # If old tour is not home-based, and its source tour
                    # was already recycled, it should be recycled as well
                    if tour._source is self.tours[-1]:
                        self.tours.append(tour)
                except (AttributeError, IndexError):
                    # Throw away old tour
                    pass
        # Tours that were not recycled, will be created
        for key in new_tours:
            tour = Tour(purposes[key], self.zone)
            self.tours.append(tour)
            if key == "hw":
                non_home_prob = purposes["wo"].gen_model.param[key]
                if random.random() < non_home_prob:
                    non_home_tour = Tour(purposes["wo"], tour)
                    self.tours.append(non_home_tour)
            else:
                non_home_prob = purposes["oo"].gen_model.param[key]
                if random.random() < non_home_prob:
                    non_home_tour = Tour(purposes["oo"], tour)
                    self.tours.append(non_home_tour)
