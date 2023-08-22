from __future__ import annotations
from typing import TYPE_CHECKING, List, Optional, Tuple
import numpy # type: ignore
import pandas
if TYPE_CHECKING:
    from datahandling.resultdata import ResultsData
    from datahandling.zonedata import ZoneData

from models.logit import LogitModel
from parameters.car import car_usage
from utils.zone_interval import ZoneIntervals


class CarUseModel(LogitModel):
    """Binary logit model for car use.

    Parameters
    ----------
    zone_data : ZoneData
        Data used for all demand calculations
    bounds : slice
        Zone bounds
    age_groups : list
        tuple
            int
                Age intervals
    resultdata : ResultData
        Writer object to result directory
    """

    def __init__(self, 
                 zone_data: ZoneData, 
                 bounds: slice, 
                 age_groups: List[Tuple[int,int]], 
                 resultdata: ResultsData):
        self.resultdata = resultdata
        self.zone_data = zone_data
        self.bounds = bounds
        self.genders = ("female", "male")
        self.age_groups = age_groups
        self.param = car_usage
        for i in self.param["individual_dummy"]:
            self._check(i)

    def _check(self, dummy):
        try:
            age_interval = dummy.split('_')[1]
        except AttributeError:
            # If the dummy is for a compound segment (age + gender)
            age_interval = dummy[0].split('_')[1]
            if dummy[1] not in self.genders:
                raise AttributeError(
                    "Car use dummy name {} not valid".format(dummy[1]))
        if tuple(map(int, age_interval.split('-'))) not in self.age_groups:
            raise AttributeError(
                "Car use dummy name {} not valid".format(age_interval))

    def calc_basic_prob(self) -> numpy.ndarray:
        """Calculate car user probabilities without individual dummies.

        Returns
        -------
        numpy.ndarray
                Choice probabilities
        """
        b = self.param
        utility = numpy.zeros(self.bounds.stop)
        self._add_constant(utility, b["constant"])
        self._add_zone_util(utility, b["generation"], True)
        self.exps = numpy.exp(utility)
        self._add_log_zone_util(self.exps, b["log"], True)
        prob = self.exps / (self.exps+1)
        return prob

    def calc_prob(self) -> pandas.Series:
        """Calculate car user probabilities with individual dummies included.

        Returns
        -------
        pandas.Series
                Choice probabilities
        """
        prob = self.calc_basic_prob()
        no_dummy_share = 1
        dummy_prob = 0
        b = self.param # ???types
        for i in b["individual_dummy"]:
            try:
                dummy_share:numpy.ndarray = self.zone_data.get_data(
                    "share_"+i, self.bounds, generation=True)
            except TypeError:
                # If the dummy is for a compound segment (age + gender)
                dummy_share = numpy.ones_like(prob)
                for j in i:
                    dummy_share *= self.zone_data.get_data(
                        "share_"+j, self.bounds, generation=True)
            no_dummy_share -= dummy_share
            ind_exps = numpy.exp(b["individual_dummy"][i]) * self.exps
            ind_prob = ind_exps / (ind_exps+1)
            dummy_prob += dummy_share * ind_prob
        no_dummy_prob = no_dummy_share * prob
        prob = no_dummy_prob + dummy_prob
        prob = pandas.Series(
            prob, self.zone_data.zone_numbers[self.bounds])
        self.print_results(prob)
        return prob

    def calc_individual_prob(self, 
                             age_group: str, 
                             gender: str, 
                             zone: Optional[int] = None):
        """Calculate car user probability with individual dummies included.

        Uses results from previously run `calc_basic_prob()`.

        Parameters
        ----------
        age_group : str
            Agent/segment age group
        gender : str
            Agent/segment gender (female/male)
        zone : int (optional)
            Index of zone where the agent lives, if no zone index is given,
            calculation is done for all zones

        Returns
        -------
        numpy.ndarray
                Choice probabilities
        """
        self._check((age_group, gender))
        if zone is None:
            exp = self.exps
        else:
            exp = self.exps[self.zone_data.zone_index(zone)]
        b = self.param
        if age_group in b["individual_dummy"]:
            exp = numpy.exp(b["individual_dummy"][age_group]) * exp
        if (age_group, gender) in b["individual_dummy"]:
            exp = numpy.exp(b["individual_dummy"][(age_group, gender)]) * exp
        prob = exp / (exp+1)
        return prob

    def print_results(self, 
                      prob: pandas.Series, 
                      population_7_99: Optional[pandas.Series]=None):
        """ Print results, mainly for calibration purposes"""
        # Print car user share by zone
        self.resultdata.print_data(prob, "car_use.txt", "car_use")
        if population_7_99 is None:
            # Comparison data has car user shares of population
            # over 6 years old (from HEHA)
            population_7_99 = (self.zone_data["population"][self.bounds]
                               * self.zone_data["share_age_7-99"])
        # print car use share by municipality and area
        for area_type in ("municipalities", "areas"):
            prob_area = ZoneIntervals(area_type).averages(prob, population_7_99)
            self.resultdata.print_data(
                prob_area, "car_use_{}.txt".format(area_type), "car_use")
