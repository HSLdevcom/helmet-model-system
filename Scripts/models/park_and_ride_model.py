from collections import defaultdict
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, NamedTuple, Tuple, TYPE_CHECKING
import numpy as np
if TYPE_CHECKING:
    from datatypes.purpose import Purpose

from parameters.assignment import assignment_classes
from parameters.impedance_transformation import impedance_share

from parameters.destination_choice import destination_choice
from datahandling.zonedata import ZoneData
from transform.impedance_transformer import ImpedanceTransformerBase, transit_cost_to_per_day
import multiprocessing as mp
from concurrent.futures import ThreadPoolExecutor

class ParkAndRidePseudoPurpose:
    """Pseudo-purpose class to be used in Demand class. Required to enable P5R specific matrix bounds.
    """
    def __init__(self, purpose: 'Purpose'):
        self.name = purpose.name
        self.zone_data = purpose.zone_data
        self.bounds = slice(0, len(self.zone_data.all_zone_numbers))

@dataclass
class ParkAndRideFacility:
    """Dataclass for park-and-ride facilities.
    """
    zone_offset: int
    zone_id: int
    capacity: float
    cost: float
    time: float
    used_capacity: float
    adjustments: int
    extra_utility: float = None

class ParkAndRideUtilities(NamedTuple):
    """Stored utilities for P&R model."""
    car_utility: np.ndarray
    transit_utility: np.ndarray
    facility_utility: np.ndarray

class ParkAndRideModel(ImpedanceTransformerBase):
    """A class for handling P&R model calculations."""
    _zone_data: ZoneData
    _purpose: 'Purpose'
    _facilities: List[ParkAndRideFacility]
    _park_and_ride_centroids: List[int]
    
    def __init__(self, zone_data: ZoneData, purpose: 'Purpose'):
        """Initialize the ParkAndRideModel.

        Args:
            zone_data (ZoneData): Zone data object.
            purpose (Purpose): Purpose object that is using the P&R model.
        """
        self._zone_data = zone_data
        self._purpose = purpose
        
        pnr_centroids = [(i, num) for i, num in enumerate(zone_data.all_zone_numbers) 
                         if num in zone_data['pnr_capacity'].index 
                         and (zone_data['pnr_capacity'].loc[num] > 0)]
        self._facilities = [ParkAndRideFacility(zone_offset = i,
                                                zone_id = num,
                                                capacity = zone_data['pnr_capacity'].loc[num],
                                                cost = zone_data['pnr_cost'].loc[num],
                                                time = 0.0,
                                                used_capacity = 0.0,
                                                adjustments=0)
                            for i, num in pnr_centroids]
        self._saved_utilities = None
        
    def set_impedance(self, impedance: Dict[str, Dict[str, Dict[str, np.ndarray]]]) -> Dict[str, Dict[str, np.ndarray]]:
        """Perform transformation from time period dependent matrices 
        to aggregate impedance matrices for specific travel purpose.

        Parameters
        ----------
        impedance: dict
            Time period (aht/pt/iht) : dict
                Type (time/cost/dist) : dict
                    Assignment class (car_work/transit/...) : numpy 2d matrix
        Return 
        ------
        dict 
            Mode (car/transit/bike/walk) : dict
                Type (time/cost/dist) : numpy 2-d matrix
        """
        
        # TODO: Refactor for readability and performance
        imp_share = impedance_share[self._purpose.name].get('park_and_ride', None)

        assignment_class = assignment_classes[self._purpose.name]
        car_mode = 'car_' + assignment_class
        transit_mode = 'transit_' + assignment_class
        
        types = ['cost', 'time']
        rows = self._purpose.bounds
        cols = (self._purpose.bounds if self._purpose.name == "hoo"
            else slice(0, self._purpose.zone_data.nr_zones))

        if len(self._facilities) == 0: #if there are no P+R facilities (mostly for testing)
            return

        pnr_param = destination_choice[self._purpose.name].get('park_and_ride', None)
        if pnr_param is None:
            return
        
        car_imp = pnr_param['utility']['car_impedance']
        transit_imp = pnr_param['utility']['transit_impedance']
        facility_offset = np.array([f.zone_offset for f in self._facilities])

        day_imp = {}
        for mode in [car_mode, transit_mode]:
            day_imp[mode] = defaultdict(float)
            for time_period in impedance:
                for mtx_type in types:
                    imp = impedance[time_period][mtx_type][mode]
                    day_imp[mode][mtx_type] += imp_share[time_period][0] * imp
                    day_imp[mode][mtx_type] += imp_share[time_period][1] * imp.T
        
        day_imp[transit_mode]['cost'] = transit_cost_to_per_day(day_imp[transit_mode]['cost'], self._purpose)
        
        car_cost     = np.stack([day_imp[car_mode]['cost'][:,f.zone_offset][rows,None] for f in self._facilities], axis=2)
        transit_cost = np.stack([day_imp[transit_mode]['cost'][f.zone_offset, :][None, cols] for f in self._facilities], axis=2)

        car_time     = np.stack([day_imp[car_mode]['time'][:,f.zone_offset][rows,None] for f in self._facilities], axis=2)
        transit_time = np.stack([day_imp[transit_mode]['time'][f.zone_offset, :][None, cols] for f in self._facilities], axis=2)

        self._calc_extra_utility(impedance)
        self._saved_utilities = ParkAndRideUtilities(
            car_utility = car_cost * car_imp['cost'] + car_time * car_imp['time'],
            transit_utility = transit_cost * transit_imp['cost'] + transit_time * transit_imp['time'],
            facility_utility = self._get_facility_utilities(),
        )
        
    def get_logsum(self) -> np.ndarray:
        """
        Calculate logsums for each od-pair.
        Returns:
            np.ndarray: A 2D array containing logsums for each od-pair. shape (nr_zones, nr_zones)
        """
        def _logsum_slice(s: slice) -> np.ndarray:
            return np.log(np.exp(self._calc_logit_slice(s, self._saved_utilities)).sum(axis=2))
        results = self._process_slices(_logsum_slice, self._purpose.zone_data.nr_zones)
        logsum = np.concatenate(results, axis=0)
        return logsum
    
    def distribute_demand(self, demand: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Distribute tour demand to facilities based on utilities.

        Parameters
        ----------
        demand : np.ndarray
            2d numpy array of shape (nr_zones, nr_zones)
        Return
        ------
        Tuple of car and transit demand matrices
        """
        
        def _demand_share_slice(s: slice) -> Any:
            exp_logits = np.exp(self._calc_logit_slice(s, self._saved_utilities))
            distribution = exp_logits / exp_logits.sum(axis=2, keepdims=True)
            distribution[np.isnan(distribution)] = 1.0 / distribution.shape[2]
            distributed_demand = distribution * demand[s,:, None]
            car_demand = distributed_demand.sum(axis=1)
            transit_demand = distributed_demand.sum(axis=0)
            facility_demand = distributed_demand.sum(axis=(0,1))
            return car_demand, transit_demand, facility_demand
        
        demand_mtxs = self._process_slices(_demand_share_slice, self._purpose.zone_data.nr_zones)
        cars_to_pnr = np.concatenate([r[0] for r in demand_mtxs], axis=0)
        transit_from_pnr = sum(r[1] for r in demand_mtxs).T
        facility_demand = sum(r[2] for r in demand_mtxs)
        
        facility_offsets = [f.zone_offset for f in self._facilities]
        nr_all_zones = len(self._zone_data.all_zone_numbers)
        car_demand = np.zeros((nr_all_zones, nr_all_zones), dtype=np.float32)
        car_demand[self._purpose.bounds, facility_offsets] = cars_to_pnr
        transit_demand = np.zeros_like(car_demand)
        transit_demand[facility_offsets, 0:transit_from_pnr.shape[1]] = transit_from_pnr
        
        for i, f in enumerate(self._facilities):
            f.used_capacity = facility_demand[i]
        
        return car_demand, transit_demand

    def apply_crowding_penalty(self) -> int:
        """
        Adjusts the time penalty for facilities based on their capacity usage.

        This method iterates over the facilities and applies a time penalty if the 
        facility is over capacity, or reduces the time penalty if the facility is 
        significantly under capacity.

        Returns:
            int: The number of facilities that had their time penalty modified.
        """
        modified = 0
        BASE_ADJUSTMENT = 3.0 # Base adjustment will be divided by the number of adjustments
        for f in self._facilities:
            if f.used_capacity > f.capacity:
                if f.adjustments%2 == 0:
                    f.adjustments += 1 # Use odd adjustments values to increase the time penalty
                # Increase the time penaltyif the facility is over capacity
                f.time += BASE_ADJUSTMENT/f.adjustments 
                modified += 1
                continue
            if f.used_capacity < 0.75*f.capacity and f.time > 0:
                if f.adjustments%2 != 0:
                    f.adjustments += 1 # Use even adjustments values to decrease the time penalty
                # reduce the time penalty if the facility is significantly under capacity
                f.time = max(0, f.time-BASE_ADJUSTMENT/f.adjustments)
                modified += 1
        self._saved_utilities = ParkAndRideUtilities(self._saved_utilities.car_utility,
                                                     self._saved_utilities.transit_utility,
                                                    self._get_facility_utilities())
        return modified
    
    def reset_crowding_penalty(self):
        """
        Reset the time penalty and adjustment step for all facilities.
        """
        for f in self._facilities:
            f.time = 0.0
            f.adjustments = 0
            f.used_capacity = 0.0
    
    def _get_facility_utilities(self) -> np.ndarray:
        """Calculates facility based utility for each facility.

        Returns:
            np.ndarray: Utitlity for each facility. shape (1, 1, nr_facilities)
        """
        pnr_param = destination_choice[self._purpose.name].get('park_and_ride', None)
        facility_cost_w = pnr_param['utility']['facility']['cost']
        facility_time_w = pnr_param['utility']['facility']['time']
        return np.array([f.cost * facility_cost_w + f.time * facility_time_w + f.extra_utility for f in self._facilities])[None, None, :]

    def _calc_extra_utility(self, impedance: Dict[str, Dict[str, Dict[str, np.ndarray]]]):
        """Calculate extra utility for each facility based on the number of shops within 1 km.
        Does nothing if there are no facilities or if the extra utility has already been calculated.

        Args:
            impedance (Dict[str, Dict[str, Dict[str, np.ndarray]]]): Impedance matrices
        """
        if len(self._facilities) == 0 or self._facilities[0].extra_utility is not None:
            return
        SHOP_SEARCH_RADIUS = 3.0 # Include shops within 1 km
        try:
            shop_weight = destination_choice[self._purpose.name]['park_and_ride']['utility']['facility']['shops']
        except KeyError:
            shop_weight = 0.0
                                     
        for facility in self._facilities:
            dist_mask = impedance['aht']['dist']['walk'][facility.zone_offset,0:self._zone_data.nr_zones] < SHOP_SEARCH_RADIUS
            facility.extra_utility = self._zone_data['shops'][dist_mask].sum() * shop_weight

    @staticmethod
    def _calc_logit_slice(s: slice, u: ParkAndRideUtilities) -> np.ndarray:
        """
        Calculate the utility slice for given car, transit, and facility utilities.
        Parameters:
        s (slice): Slice of origins that will be calculated.
        u (ParkAndRideUtilities): Car, transit, and facility utilities.
        Returns:
        np.ndarray: A 3D array where each slice along the third axis represents the combined utility 
                    for a specific facility offset. shape (slice, nr_zones, nr_facilities)
        """
        res = u.car_utility[s,:,:] + u.transit_utility + u.facility_utility
        res = np.clip(res,-50,None) #TODO: Hotfix, car utility sometimes not reasonable
        return res            

            


    def _calc_pnr_utilities(self, day_imp: Dict[str, Dict[str, Dict[str, np.ndarray]]]) -> ParkAndRideUtilities:
        """
        Calculate park-and-ride utilities for a given day impedance.
        Args:
            day_imp (Dict[str, Dict[str, Dict[str, np.ndarray]]]): A dictionary containing day impedance data for different modes.
        Returns:
            ParkAndRideUtilities: An object containing calculated utilities for car, transit, and facilities, 
                                  as well as facility offsets.
        Notes:
            - If the purpose does not have park-and-ride mode, None is returned.
            - The method calculates extra utility before computing the utilities for car, transit, and facilities.
        """

        pnr_param = destination_choice[self._purpose.name].get('park_and_ride', None)
        if not pnr_param: 
            return None # Skip purposes without park-and-ride mode

        self._calc_extra_utility(day_imp) 
        car_mode = 'car'
        transit_mode = 'transit'
        rows = self._purpose.bounds
        cols = slice(0, self._purpose.zone_data.nr_zones)

        car_imp = pnr_param['car_impedance']
        transit_imp = pnr_param['transit_impedance']
        facility_cost_w = pnr_param['facility']['cost']
        facility_time_w = pnr_param['facility']['time']
        facility_offset = np.array([f.zone_offset for f in self._facilities])
        return ParkAndRideUtilities(
            car_utility = sum(day_imp[car_mode][t][rows, facility_offset] * w for t, w in car_imp.items()),
            transit_utility = sum(day_imp[transit_mode][t][facility_offset, cols] * w for t, w in transit_imp.items()),
            facility_utility = sum(f.cost * facility_cost_w + f.time * facility_time_w + f.extra_utility for f in self._facilities),
        )


    def _process_slices(self, func: Callable[[slice], Any], max_range: int) -> List[Any]:
        """
        Calls given function for each number slices 0 to max_range.
        Args:
            func (Callable[[slice], Any]): Function to be called for each slice.
            max_range (int): Maximum range of slices.
        Returns:
            List[Any]: A list of results from the function calls.
        """
        
        # Enable or disable multithreading
        MULTITHREADING = False
        MIN_SLICE_SIZE = 5
        MAX_SLICE_SIZE = 10000
        if MULTITHREADING:
            slice_size = min(MAX_SLICE_SIZE, max(MIN_SLICE_SIZE, max_range//mp.cpu_count()))
            slices = [slice(i, i + slice_size) for i in range(0, max_range, slice_size)]
            with ThreadPoolExecutor() as executor:
                results = list(executor.map(func, slices))
        else:
            slice_size = min(MAX_SLICE_SIZE, max(MIN_SLICE_SIZE, max_range))
            slices = [slice(i, i + slice_size) for i in range(0, max_range, slice_size)]
            results = list(map(func, slices))
        return results
