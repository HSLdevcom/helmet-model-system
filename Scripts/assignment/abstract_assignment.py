from abc import ABCMeta, abstractmethod


class AssignmentModel:
    __metaclass__ = ABCMeta

    @abstractmethod
    def mapping(self):
        """Dictionary of zone numbers and corresponding indices."""
        pass

    @abstractmethod
    def zone_numbers(self):
        pass
    
    @abstractmethod
    def calc_transit_cost(self, fares, peripheral_cost, default_cost=None):
        pass

    @abstractmethod
    def aggregate_results(self, resultdatawriter):
        pass
    
    @abstractmethod
    def prepare_network(self):
        pass