from collections import defaultdict
from pathlib import Path
from typing import Dict
import numpy # type: ignore
import openmatrix as omx

from Scripts.datatypes.purpose import Purpose
import parameters.impedance_transformation as param
from parameters.assignment import assignment_classes


class ImpedanceTransformer:
    def __init__(self, export_path: Path = None):
        self._export_path = export_path

    def transform(self, purpose, impedance):
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
        rows = purpose.bounds
        cols = (purpose.bounds if purpose.name == "hoo"
            else slice(0, purpose.zone_data.nr_zones))
        day_imp = {}
        impedance_share = param.impedance_share
        for mode in impedance_share[purpose.name]:
            day_imp[mode] = defaultdict(float)
            if mode in param.divided_classes:
                ass_class = "{}_{}".format(
                    mode, assignment_classes[purpose.name])
            else:
                ass_class = mode
            for time_period in impedance:
                for mtx_type in impedance[time_period]:
                    if ass_class in impedance[time_period][mtx_type]:
                        share = impedance_share[purpose.name][mode][time_period]
                        imp = impedance[time_period][mtx_type][ass_class]
                        day_imp[mode][mtx_type] += share[0] * imp[rows, cols]
                        day_imp[mode][mtx_type] += share[1] * imp[cols, rows].T
        # transit cost to eur per day
        trips_month = (param.transit_trips_per_month
            [purpose.area][assignment_classes[purpose.name]])
        trips_per_month = numpy.full_like(
            day_imp["transit"]["cost"], trips_month[0])
        for i in range(1, len(purpose.sub_bounds)):
            trips_per_month[purpose.sub_bounds[i], :] = trips_month[i]
        day_imp["transit"]["cost"] /= trips_per_month
        
        # Optionally export impedance data for estimation
        if self._export_path:
            self.export_day_impedance(purpose, day_imp)
        
        return day_imp

    def export_day_impedance(self, purpose: Purpose, day_imp: Dict[str, Dict[str, numpy.ndarray]]) -> None:
        """Export day impedance matrices to OMX files. Used for estimation process.

        Args:
            purpose (Purpose): Trip purpose
            day_imp (Dict[str, Dict[str, np.ndarray]]): Daily impedances in a dict 
                {mode: {impedance_type: array}}

        """
        with omx.open_file(self._export_path / (purpose.name + '.omx'), mode='w') as omx_file:
            for mode_name, mode_imp in day_imp.items():
                for type_name, type_imp in mode_imp.items():
                    omx_file[mode_name + '_' + type_name] = type_imp
