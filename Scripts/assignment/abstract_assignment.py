from abc import ABCMeta, abstractmethod


class AssignmentModel:
    __metaclass__ = ABCMeta

    @abstractmethod
    def assign(self, time_period, matrices, iteration=None):
        """Assign cars, bikes and transit for one time period.
        Get travel impedance matrices for one time period from assignment.
        
        Parameters
        ----------
        time_period : str
            Time period (aht/pt/iht)
        matrices: dict
            Assignment class (car_work/transit/...) : numpy 2-d matrix
        iteration: int or str
            Iteration number (0, 1, 2, ...) or "last"

        Returns
        -------
        dict
            Type (time/cost/dist) : dict
                Assignment class (car_work/transit/...) : numpy 2-d matrix
        """
        pass

    @abstractmethod
    def mapping(self):
        """Dictionary of zone numbers and corresponding indices."""
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
    
    @abstractmethod
    def prepare_network(self):
        pass