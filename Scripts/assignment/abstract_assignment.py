from __future__ import annotations
from abc import ABCMeta, abstractmethod
from typing import Any, Dict, List, Union


class AssignmentModel:
    __metaclass__ = ABCMeta

    @property
    @abstractmethod
    def mapping(self) -> Dict[int,int]:
        """Dictionary of zone numbers and corresponding indices."""
        pass

    @property
    @abstractmethod
    def zone_numbers(self) -> List[int]:
        pass

    @property
    @abstractmethod
    def nr_zones(self) -> int:
        pass

    @abstractmethod
    def calc_transit_cost(self, fares, peripheral_cost, default_cost=None):
        pass

    @abstractmethod
    def aggregate_results(self, resultdatawriter):
        pass

    @abstractmethod
    def calc_noise(self):
        pass

    @abstractmethod
    def prepare_network(self, car_dist_unit_cost=None):
        pass

    @abstractmethod
    def init_assign(self, demand):
        pass

class Period:
    __metaclass__ = ABCMeta

    @abstractmethod
    def assign(self, matrices: Dict[Any, Any], iteration: Union[int, str]) -> Dict[Any, Any]:
        pass
