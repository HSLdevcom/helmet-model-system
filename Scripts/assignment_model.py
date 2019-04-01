from abc import ABCMeta, abstractmethod

class AssignmentModel:
    __metaclass__ = ABCMeta

    @abstractmethod
    def assign(self):
        pass

    @abstractmethod
    def get_mapping(self):
        pass

    @abstractmethod
    def get_matrices(self, mtx_type, time_period=None):
        pass

    @abstractmethod
    def get_zone_numbers(self):
        pass
