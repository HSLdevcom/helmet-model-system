from abc import ABCMeta, abstractmethod


class AssignmentModel:
    __metaclass__ = ABCMeta

    @abstractmethod
    def assign(self, time_period, matrices, is_last_iteration=False, is_first_iteration=False):
        """Assign cars, bikes and transit for one time period.
        
        Parameters
        ----------
        time_period : str
            Time period (aht/pt/iht)
        matrices: dict
            Assignment class (car_work/transit/...): numpy 2-d matrix
        is_last_iteration: bool
        is_first_iteration: bool
        """
        pass


class ImpedanceSource:
    __metaclass__ = ABCMeta

    MATRIX_TYPE_FREIGHT_KEY = "freight"

    @abstractmethod
    def mapping(self):
        """Dictionary of zone numbers and corresponding indices."""
        pass

    @abstractmethod
    def get_impedance(self, is_last_iteration=False):
        """Get travel impedance matrices for one time period.
        
        Return
        ------
        dict
            Type (time/cost/dist) : dict
                Assignment class (car_work/transit/...) : numpy 2-d matrix
        """
        pass

    @abstractmethod
    def get_emmebank_matrices(self, mtx_type, time_period=None):
        pass

    @abstractmethod
    def zone_numbers(self):
        pass
    
    @abstractmethod
    def calc_transit_cost(self, fares, peripheral_cost, default_cost=None):
        pass

    @abstractmethod
    def print_vehicle_kms(self, resultdatawriter):
        pass
