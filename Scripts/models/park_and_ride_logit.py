import numpy
import pandas
from datahandling.resultdata import ResultsData
from datahandling.zonedata import ZoneData
from datatypes.purpose import Purpose
from models.logit import LogitModel, SecDestModel


class ParkAndRideLogit(LogitModel):
    """Logit model for park and ride facility selection.

    Multinomial choice of parking facility for park and ride tours

    Parameters
    ----------
    zone_data : ZoneData
        Data used for all demand calculations
    purpose : TourPurpose
        Tour purpose (type of tour)
    resultdata : ResultData
        Writer object to result directory
    is_agent_model : bool (optional)
        Whether the model is used for agent-based simulation
    """
        
    def calc_utils(self,impedance, facility):
        
        b = self.dest_choice_param["park_and_ride"]
        utility = numpy.zeros_like(impedance.delta_time[facility])

        #self._add_sec_zone_util(utility, b["attraction"], orig, dest)
        zones_shops = self.zone_data.get_data("shops", self.bounds, generation=False)
        zones_shops_sum = (impedance.one_km_radius[facility] * zones_shops).sum() #broadcasting
        utility += numpy.full_like(impedance.delta_delta_impedance[facility], b["attraction"]["shops"] * zones_shops_sum) #utility of shopping 
        #self._add_impedance(utility, impedance, b["impedance"])
        utility += b["impedance"]["delta_time"] * impedance.delta_impedance[facility] #delta impedance of facility #TODO: Check this
        self.dest_exps[facility] = numpy.exp(utility)
        self.dest_expsum += self.dest_exps[facility] #defined in ParkAndRidePurpose
    

class ParkAndRidePurpose(Purpose):
    """Purpose for secondary destination of tour.

    Parameters
    ----------
    specification : dict
        "name" : str
            Tour purpose name (hoo)
        "orig" : str
            Origin of the tours (home)
        "dest" : str
            Destination of the tours (any)
        "area" : str
            Model area (metropolitan)
    zone_data : ZoneData
        Data used for all demand calculations
    resultdata : ResultData
        Writer object to result directory
    """

    def __init__(self, zone_data: ZoneData, resultdata: ResultsData):
        specification = {
            "name": "park_and_ride",
            "orig": "home",
            "dest": "work",
            "area": "metropolitan",
        }
        Purpose.__init__(self, specification, zone_data, resultdata)
        self.model = ParkAndRideLogit(zone_data, self, resultdata)
        self.modes = self.model.dest_choice_param.keys()

    def calc_park_and_ride_expsum(self, mode, impedance, zone_data: ZoneData):
        pnr_expsum = {}
        #source_zones = [j for j in range(zone_data.nr_zones_hs15)]
        #target_zones = [j for j in range(zone_data.nr_zones_hs15)]
        self.model.dest_expsum = 0
        self.pnr_centroids = [(i, num) for i, num in enumerate(zone_data.all_zone_numbers) 
                         if num in zone_data['pnr_capacity'].index and zone_data['pnr_capacity'].loc[num] > 0] #TODO: Check this?
        for facility in self.pnr_centroids:
            prob_single = self.calc_utils(mode, impedance, facility) #calc util?
            for pnr in self.pnr_centroids:
                pnr_expsum[pnr] += prob_single[:,pnr]
        return pnr_expsum

    def get_park_and_ride_routes(self, zone_data: ZoneData):
        """Decide the secondary destinations for all tours (generated 
        earlier) starting from one specific zone.
        
        Parameters
        ----------
        mode : str
            Mode (car/transit/bike)
        impedance : dict
            Type (time/cost/dist) : numpy 2d matrix
        orig : int
            The relative zone index from which these tours origin
        orig_offset : int (optional)
            Absolute zone index of orig is orig_offset + orig

        Returns
        -------
        Demand
            Matrix of destination -> secondary_destination pairs
            The origin zone for all of these tours
        """
        pnr_demand = {}

        for facility in self.pnr_centroids:
            pnr_demand[facility] = self.calc_prob(facility)
        return pnr_demand

    def calc_prob(self, facility):
        """Calculate secondary destination probabilites.
        
        For tours starting in specific zone and ending in some zones.
        
        Parameters
        ----------
        mode : str
            Mode (car/transit/bike)
        impedance : dict
            Type (time/cost/dist) : numpy 2d matrix
        orig : int
            Origin zone index
        dests : list or boolean array
            Destination zone indices

        Returns
        -------
        numpy.ndarray
            Probability matrix for chosing zones as secondary destination
        """
        pnr_demand = self.model.dest_exps[facility]/self.model.dest_expsum
        return pnr_demand