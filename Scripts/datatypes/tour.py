from __future__ import annotations
from typing import TYPE_CHECKING, Dict, List, Optional, Tuple, Union, cast
import numpy # type: ignore
import random
if TYPE_CHECKING:
    from datatypes.purpose import TourPurpose
    from datatypes.zone import Zone
from models.logit import ModeDestModel

import parameters.car as param
import parameters.zone as zone_param
from parameters.assignment import assignment_classes, vot_inv
from parameters.impedance_transformation import divided_classes, transit_trips_per_month


class Tour:
    """Tour definition for agent-based simulation.
    
    Parameters
    ----------
    purpose : datatypes.purpose.TourPurpose
        Travel purpose (hw/hs/ho/...)
    origin : Zone or Tour
        Origin zone number or origin tour (if non-home tour)
    person_id: 
        id of Person
    """
    # Expansion factor used on demand in departure time model
    matrix = numpy.array([[1 / zone_param.agent_demand_fraction]])
    attr = ["person_id", "purpose_name", "mode", 
            "total_access", "sustainable_access",
            "cost", "gen_cost"]

    def __init__(self, 
                 purpose: TourPurpose, 
                 origin: Union[Zone,'Tour'], 
                 person_id: int):
        self.person_id = person_id
        self.purpose = purpose
        self.purpose_name = purpose.name
        self.purpose.name = cast(str, self.purpose.name) #type checker help
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
    def is_car_passenger(self) -> bool:
        return self.mode == "car" and self._is_car_passenger

    @property
    def orig(self):
        return self.purpose.zone_data.zone_numbers[self.position[0]]

    @orig.setter
    def orig(self, origin):
        try:
            self._position = (origin.index,)
        except AttributeError:
            # If this is non-home tour, origin refers to home-based tour
            self._source = origin
            self._non_home_position = ()

    @property
    def dest(self) -> Optional[int]:
        if len(self.position) > 1:
            return self.purpose.zone_data.zone_numbers[self.position[1]]
        else:
            return None

    @dest.setter
    def dest(self, destination):
        self.position = (
            self.position[0],
            destination.index
        )

    @property
    def sec_dest(self) -> Optional[int]:
        if len(self.position) > 2:
            self.position = cast(Tuple[int,int,int], self.position) #help for the type checker
            return self.purpose.zone_data.zone_numbers[self.position[2]]
        else:
            return None

    @sec_dest.setter
    def sec_dest(self, destination):
        self.position = (
            self.position[0],
            self.position[1],
            destination.index
        )

    @property
    def position(self) -> Union[Tuple[int,int], Tuple[int,int,int]]:
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
        if hasattr(self, "_position"):
            self._position = position
        else:
            self._non_home_position = position[1:]

    def choose_mode(self, is_car_user: bool):
        """Choose tour travel mode.

        Assumes tour purpose model has already calculated probability matrices.
        
        Parameters
        ----------
        is_car_user : bool
            Whether the person is car user or not
        """
        self.purpose.model = cast(ModeDestModel, self.purpose.model) #type checker help
        probs, accessibility = self.purpose.model.calc_individual_mode_prob(
                is_car_user, self.position[0])
        self._mode_idx = numpy.searchsorted(probs.cumsum(), self._mode_draw)
        self.purpose.generated_tours[self.mode][self.position[0]] += 1
        self.total_access = accessibility

    @property
    def sustainable_access(self):
        return -self.purpose.sustainable_access[self.orig]

    def choose_destination(self, sec_dest_tours: Dict[str, Dict[int, Dict[int, List['Tour']]]]):
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
        self.purpose.model = cast(ModeDestModel, self.purpose.model) #type checker help
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

    def choose_secondary_destination(self, cumulative_probs: numpy.ndarray):
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
    
    def calc_cost(self, impedance: Dict[str,Dict[str,Dict[str,numpy.ndarray]]]):
        """Construct cost and time components from tour dest choice.

        Parameters
        ----------
        impedance: dict
            Time period (aht/pt/iht) : dict
                Type (time/cost/dist) : dict
                    Assignment class (car_work/transit/...) : numpy 2d matrix
        """
        time = self._get_cost(impedance, "time")
        self.cost = self._get_cost(impedance, "cost")
        self.purpose_name = cast(str, self.purpose_name) #type checker help
        vot = 1 / vot_inv[assignment_classes[self.purpose_name]]
        self.gen_cost = self.cost + time * vot

    def _get_cost(self, 
                  impedance: Dict[str,Dict[str,Dict[str,numpy.ndarray]]], 
                  mtx_type: str) -> Union[int,float]:
        """Get cost and time components from tour dest choice."""
        self.purpose.name = cast(str, self.purpose.name) #type checker help
        demand_type = assignment_classes[self.purpose.name]
        ass_class = ("{}_{}".format(self.mode, demand_type)
            if self.mode in divided_classes else self.mode)
        cost: float = 0.0
        try:
            if demand_type == "work":
                departure_imp = impedance["aht"][mtx_type][ass_class]
                sec_dest_imp = impedance["iht"][mtx_type][ass_class]
                return_imp = impedance["iht"][mtx_type][ass_class]
            else:
                departure_imp = impedance["pt"][mtx_type][ass_class]
                sec_dest_imp = impedance["pt"][mtx_type][ass_class]
                return_imp = impedance["pt"][mtx_type][ass_class]
            # first leg of tour
            cost += departure_imp[self.position[0], self.position[1]]
            # check if tour has secondary destination and add accordingly
            if len(self.position) > 2:
                self.position = cast(Tuple[int,int,int], self.position) #type checker help
                cost += sec_dest_imp[self.position[1], self.position[2]]
                cost += return_imp[self.position[2], self.position[0]]
            else: 
                cost += return_imp[self.position[1], self.position[0]]
        except KeyError:
            # bike and walk modes do not have cost matrices specified
            # KeyErrors are produced when trying to access matrix
            pass
        # scale transit costs from month to day
        self.purpose.area = cast(str, self.purpose.area) #type checker help
        if self.mode == "transit" and mtx_type == "cost":
            i = self.purpose.sub_intervals.searchsorted(
                self.position[0], side="right")
            cost /= transit_trips_per_month[self.purpose.area][demand_type][i]
        return cost

    def __str__(self) -> str:
        """ Return tour attributes as string.

        Returns
        ----------
        str
            Tour object attributes.
        """
        tourdata = [str(getattr(self, attr)) for attr in Tour.attr]
        return "\t".join(tourdata)
