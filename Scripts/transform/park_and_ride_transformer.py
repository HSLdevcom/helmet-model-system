from collections import defaultdict
from typing import Dict, List, NamedTuple, Tuple
import numpy as np
from datatypes.purpose import Purpose
from parameters.zone import areas
import parameters.impedance_transformation as param
from parameters.assignment import assignment_classes
from datahandling.zonedata import ZoneData
from transform.impedance_transformer import ImpedanceTransformerBase, transit_cost_to_per_day
from parameters.assignment import vot_inv


class ParkAndRideFacility(NamedTuple):
    zone_offset: int
    zone_id: int
    capacity: float
    cost: float
    time: float
    used_capacity: float
    adjustments: int

class ParkAndRideTransformer(ImpedanceTransformerBase):
    _zone_data: ZoneData
    _facilities: List[ParkAndRideFacility]
    _park_and_ride_centroids: List[int]
    
    def __init__(self, zone_data: ZoneData):
        self._zone_data = zone_data
        pnr_centroids = [(i, num) for i, num in enumerate(zone_data.all_zone_numbers) 
                         if num in zone_data['pnr_capacity'].index and zone_data['pnr_capacity'].loc[num] > 0]
        self._facilities = [ParkAndRideFacility(i,
                                                num,
                                                zone_data['pnr_capacity'].loc[num],
                                                zone_data['pnr_cost'].loc[num],
                                                0.0,
                                                0.0,
                                                0)
                            for i, num in pnr_centroids]
        self.used_facility: np.ndarray = None

    def get_pnr_map(self) -> Dict[int,int]:
        """
        Get mapping pnr_zone_emme_number -> pnr_zone_order_index
        """
        return {f.zone_id: f.zone_offset for f in self._facilities}
    
    
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
        return modified
    
    def assign_demand(self, demand: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Assigns demand to car and transit facilities.
        Parameters:
        demand (np.ndarray): A 2D array representing the demand matrix.
        Returns:
        Tuple[np.ndarray, np.ndarray]: A tuple containing two 2D arrays:
            - car_demand: Car demand into facilities.
            - transit_demand: Transit demand from the facilities.
        """
        car_demand = np.zeros_like(demand)
        transit_demand = np.zeros_like(demand)
        
        for i, facility in enumerate(self._facilities):
            d = demand[self.used_facility == i]
            car_demand[:,facility.zone_offset] += d.sum(axis=1)
            transit_demand[facility.zone_offset,:] += d.sum(axis=0)
            facility.used_capacity = d.sum()
        
        return car_demand, transit_demand
            
    def transform(self,
                  purpose: Purpose,
                  impedance: Dict[str, Dict[str, Dict[str, np.ndarray]]]
                  ) -> Dict[str, Dict[str, np.ndarray]]:
        """Perform transformation from time period dependent matrices 
        to aggregate impedance matrices for specific travel purpose.

        Transform transit costs from (eur/month) to (eur/day).

        Parameters
        ----------
        purpose : TourPurpose
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
        
        impedance_share = param.impedance_share[purpose.name].get('park_and_ride', None)
        if not impedance_share: 
            return {} # Skip purposes without park-and-ride mode


        day_impedance = {}
        assignment_class = assignment_classes[purpose.name]
        car_mode = 'car_' + assignment_class
        transit_mode = 'transit_' + assignment_class
        inverse_value_of_time = vot_inv[assignment_class]
        
        types = ['cost', 'time']
        rows = purpose.bounds
        cols = (purpose.bounds if purpose.name == "hoo"
            else slice(0, purpose.zone_data.nr_zones))

        if len(self._facilities) == 0: #if there are no P+R facilities (mostly for testing)
            rows = sum([1 for _ in purpose.zone_numbers])
            cols = purpose.zone_data.nr_zones
            inf_mat = np.full((rows,cols), 999.)
            return {
                
                'park_and_ride': {
                    'cost': inf_mat,
                    'time': inf_mat,
                    'dist': inf_mat,
                    'gen_cost': inf_mat,
                    'used_facility': np.full((rows, cols), None)
                }
            }
        
        day_imp = {}
        for mode in [car_mode, transit_mode]:
            day_imp[mode] = defaultdict(float)
            for time_period in impedance:
                for mtx_type in types:
                    imp = impedance[time_period][mtx_type][mode]
                    day_imp[mode][mtx_type] += impedance_share[time_period][0] * imp
                    day_imp[mode][mtx_type] += impedance_share[time_period][1] * imp.T
        
        day_imp[transit_mode]['cost'] = transit_cost_to_per_day(day_imp[transit_mode]['cost'], purpose)
        
        cost = np.stack([day_imp[car_mode]['cost'][:,f.zone_offset][:,None] +
                         day_imp[transit_mode]['cost'][f.zone_offset, :][None,:]
                                    for f in self._facilities])
        cost = cost[:,rows,cols]
        time = np.stack([day_imp[car_mode]['time'][:,f.zone_offset][:,None] +
                         day_imp[transit_mode]['time'][f.zone_offset, :][None,:]
                                    for f in self._facilities])[:, rows, cols]
        time = time[:,rows,cols]
        cost += np.array([f.cost for f in self._facilities])[:,None,None]
        time += np.array([f.time for f in self._facilities])[:,None,None]
        
        generalized_cost = cost*inverse_value_of_time + time
        
        min_index = np.argmin(generalized_cost, axis=0)[None, :, :]#, keepdims=True)
        f_zones = np.array([f.zone_id for f in self._facilities])[:,None,None]
        self.used_facility = np.take_along_axis(f_zones, min_index, axis=0)[0]
        day_impedance = {
            'park_and_ride': {
                'cost': (np.take_along_axis(cost, min_index, axis=0)[0]),
                'time': np.take_along_axis(time, min_index, axis=0)[0],
                'gen_cost': np.take_along_axis(generalized_cost, min_index, axis=0)[0],
                'used_facility': self.used_facility
            }
        }
        return day_impedance
