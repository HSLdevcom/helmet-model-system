from abc import ABCMeta, abstractmethod

class AssignmentModel:
    __metaclass__ = ABCMeta

    @abstractmethod
    def assign(self):
        pass


class ImpedanceSource:
    __metaclass__ = ABCMeta

    MATRIX_TYPE_FREIGHT_KEY = "freight"

    @abstractmethod
    def get_mapping(self):
        pass

    @abstractmethod
    def get_impendance(self, time_period=None):
        pass

    @abstractmethod
    def get_matrices(self, mtx_type, time_period=None):
        pass

    @abstractmethod
    def get_zone_numbers(self):
        pass
