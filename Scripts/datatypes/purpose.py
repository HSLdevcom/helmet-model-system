from __future__ import annotations
from pathlib import Path
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Union, cast
import numpy # type: ignore
import pandas
from datahandling.resultdata import ResultsData
import openmatrix as omx
from datahandling.zonedata import ZoneData

from models.park_and_ride_model import ParkAndRideModel, ParkAndRidePseudoPurpose
import parameters.zone as param
from parameters.destination_choice import secondary_destination_threshold, destination_choice
import models.logit as logit
import models.generation as generation
from datatypes.demand import Demand
from utils.zone_interval import MatrixAggregator, ArrayAggregator
from datatypes.histogram import TourLengthHistogram


class Purpose:
    """Generic container class without methods.
    
    Sets the purpose zone bounds.

    Parameters
    ----------
    specification : dict
        "name" : str
            Tour purpose name
        "orig" : str
            Origin of the tours
        "dest" : str
            Destination of the tours
        "area" : str
            Model area
    zone_data : ZoneData
        Data used for all demand calculations
    """

    def __init__(self, 
                 specification: Dict[str,Optional[str]], 
                 zone_data: ZoneData, 
                 resultdata: Optional[ResultsData]=None):
        self.name = specification["name"]
        self.orig = specification["orig"]
        self.dest = specification["dest"]
        self.area = specification["area"]
        self.name = cast(str, self.name) #type checker help
        self.area = cast(str, self.area) #type checker help
        self.sources: List[Any] = []
        zone_numbers = zone_data.all_zone_numbers
        zone_intervals = param.purpose_areas[self.area]
        self.bounds = slice(*zone_numbers.searchsorted(
            [zone_intervals[0], zone_intervals[-1]]))
        sub_intervals = zone_numbers[self.bounds].searchsorted(zone_intervals)
        self.sub_bounds = [slice(sub_intervals[i-1], sub_intervals[i])
            for i in range(1, len(sub_intervals))]
        self.sub_intervals = sub_intervals[1:]
        self.zone_data = zone_data
        self.resultdata = resultdata
        self.model = None
        self.modes: List[str] = []
        self.generated_tours: Dict[str, numpy.array] = {}
        self.attracted_tours: Dict[str, numpy.array] = {}
        self.park_and_ride_model: ParkAndRideModel = None

    @property
    def zone_numbers(self):
        return self.zone_data.zone_numbers[self.bounds]

    def print_data(self):
        self.resultdata.print_data(
            pandas.Series(
                sum(self.generated_tours.values()), self.zone_numbers),
            "generation.txt", self.name)
        self.resultdata.print_data(
            pandas.Series(
                sum(self.attracted_tours.values()),
                self.zone_data.zone_numbers),
            "attraction.txt", self.name)
        demsums = {mode: self.generated_tours[mode].sum()
            for mode in self.modes}
        demand_all = float(sum(demsums.values()))
        mode_shares = {mode: demsums[mode] / demand_all for mode in demsums}
        self.resultdata.print_data(
            pandas.Series(mode_shares),
            "mode_share.txt", self.name)


class TourPurpose(Purpose):
    """Standard two-way tour purpose.

    Parameters
    ----------
    specification : dict
        "name" : str
            Tour purpose name (hw/oo/hop/sop/...)
        "orig" : str
            Origin of the tours (home/source)
        "dest" : str
            Destination of the tours (work/other/source/...)
        "area" : str
            Model area (metropolitan/peripheral)
    zone_data : ZoneData
        Data used for all demand calculations
    resultdata : ResultData
        Writer object for result directory
    """

    def __init__(self, specification, zone_data, resultdata):
        Purpose.__init__(self, specification, zone_data, resultdata)
        if self.orig == "source":
            self.gen_model = generation.NonHomeGeneration(self, resultdata)
        else:
            self.gen_model = generation.GenerationModel(self, resultdata)
        if self.name == "sop":
            self.model: Union[logit.OriginModel, logit.DestModeModel, logit.ModeDestModel] = logit.OriginModel(zone_data, self, resultdata)
        elif self.name == "so":
            self.model = logit.DestModeModel(zone_data, self, resultdata)
        else:
            self.model = logit.ModeDestModel(zone_data, self, resultdata)
            self.accessibility_model = logit.AccessibilityModel(
                zone_data, self, resultdata)
        self.modes = list(self.model.mode_choice_param)
        self.histograms = {mode: TourLengthHistogram() for mode in self.modes}
        self.aggregates = {mode: MatrixAggregator(zone_data.zone_numbers)
            for mode in self.modes}
        self.own_zone_aggregates = {mode: ArrayAggregator(zone_data.zone_numbers)
            for mode in self.modes}
        self.sec_dest_purpose = None
        self.park_and_ride_model = None
        if "park_and_ride" in destination_choice[self.name]:
            self.park_and_ride_model = ParkAndRideModel(
                zone_data, self)
        else:
            self.park_and_ride_model = None

    def print_data(self):
        Purpose.print_data(self)
        for mode in self.histograms:
            self.resultdata.print_data(
                self.histograms[mode].histogram, "trip_lengths.txt",
                "{}_{}".format(self.name, mode[0]))
            self.resultdata.print_matrix(
                self.aggregates[mode].matrix, "aggregated_demand",
                "{}_{}".format(self.name, mode))
            self.resultdata.print_data(
                self.own_zone_aggregates[mode].array,
                "own_zone_demand.txt", "{}_{}".format(self.name, mode[0]))

    def init_sums(self):
        for mode in self.modes:
            self.generated_tours[mode] = numpy.zeros_like(self.zone_numbers)
            self.attracted_tours[mode] = numpy.zeros_like(self.zone_data.zone_numbers)
            self.histograms[mode].__init__()
            self.aggregates[mode].init_matrix()
            self.own_zone_aggregates[mode].init_array()

    def calc_prob(self, impedance):
        """Calculate mode and destination probabilities.
        
        Parameters
        ----------
        impedance : dict
            Mode (car/transit/bike/walk) : dict
                Type (time/cost/dist) : numpy 2d matrix
        """
        def print_pnr_utility(pnr_utility: numpy.ndarray, result_path: Path):
            # TODO: This is a temporary solution to print the park and ride utility
            omx_file = omx.open_file(result_path / 'park_and_ride_utility.omx', 'w')
            omx_file.create_mapping('zone_number', self.zone_data.zone_numbers)
            omx_file['park_and_ride_utility'] = pnr_utility
            omx_file.close()
        if self.park_and_ride_model is not None:
            pnr_utility = self.park_and_ride_model.get_logsum()
            impedance['park_and_ride'] = {'utility': pnr_utility,
                                          'dist': impedance['car']['dist']}
            print_pnr_utility(pnr_utility, Path(self.resultdata.path))
        self.prob = self.model.calc_prob(impedance)
        self.dist = impedance["car"]["dist"]

    def calc_basic_prob(self, impedance):
        """Calculate mode and destination probabilities.

        Individual dummy variables are not included.

        Parameters
        ----------
        impedance : dict
            Mode (car/transit/bike/walk) : dict
                Type (time/cost/dist) : numpy 2d matrix
        """
        if self.park_and_ride_model is not None:
            pnr_utility = self.park_and_ride_model.get_logsum()
            impedance['park_and_ride'] = {'utility': pnr_utility,
                                          'dist': impedance['car']['dist']}
        self.model.calc_basic_prob(impedance)
        self.dist = impedance["car"]["dist"]

    def calc_demand(self, estimation_mode=False):
        """Calculate purpose specific demand matrices.
              
        Returns
        -------
        dict
            Mode (car/transit/bike) : dict
                Demand matrix for whole day : Demand
        """
        tours = self.gen_model.get_tours()
        demand = {}
        if estimation_mode:
            omx_file = omx.open_file(f"{self.resultdata.path}/estimation/demand_{self.name}.omx","w")
            omx_file.create_mapping("zone_number",self.zone_data.all_zone_numbers)
        for mode in self.modes:
            mtx = (self.prob.pop(mode) * tours).T
            try:
                self.sec_dest_purpose.gen_model.add_tours(mtx, mode, self)
            except AttributeError:
                pass
            if mode == "park_and_ride":
                car_demand, transit_demand = self.park_and_ride_model.distribute_demand(mtx)
                pnr_purpose = ParkAndRidePseudoPurpose(self)
                demand["pnr_car"] = Demand(pnr_purpose, "car", car_demand)
                demand["pnr_transit"] = Demand(pnr_purpose, "transit", transit_demand)
                # if True: 
                #     omx_file["pnr_car"] = car_demand
                #     omx_file["pnr_transit"] = transit_demand
            else:
                demand[mode] = Demand(self, mode, mtx)
                if estimation_mode:
                    omx_file[mode] = mtx
            self.attracted_tours[mode] = mtx.sum(0)
            self.generated_tours[mode] = mtx.sum(1)
            self.histograms[mode].count_tour_dists(mtx, self.dist)
            self.aggregates[mode].aggregate(pandas.DataFrame(
                mtx, self.zone_numbers, self.zone_data.zone_numbers))
            self.own_zone_aggregates[mode].aggregate(pandas.Series(
                numpy.diag(mtx), self.zone_numbers))
        self.print_data()
        if estimation_mode:
            omx_file.close()
        return demand


class SecDestPurpose(Purpose):
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

    def __init__(self, specification, zone_data, resultdata):
        Purpose.__init__(self, specification, zone_data, resultdata)
        self.gen_model = generation.SecDestGeneration(self, resultdata)
        self.model = logit.SecDestModel(zone_data, self, resultdata)
        self.modes = self.model.dest_choice_param.keys()

    def init_sums(self):
        for mode in self.model.dest_choice_param:
            self.generated_tours[mode] = numpy.zeros_like(self.zone_numbers)
            self.attracted_tours[mode] = numpy.zeros_like(
                self.zone_data.zone_numbers, float)

    def generate_tours(self):
        """Generate the source tours without secondary destinations."""
        self.tours = {}
        self.init_sums()
        for mode in self.model.dest_choice_param:
            self.tours[mode] = self.gen_model.get_tours(mode)

    def distribute_tours(self, mode, impedance, orig, orig_offset=0):
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
        generation = self.tours[mode][orig, :]
        # All o-d pairs below threshold are neglected,
        # total demand is increased for other pairs.
        dests = generation > secondary_destination_threshold
        if not dests.any():
            # If no o-d pairs have demand above threshold,
            # the sole destination with largest demand is picked
            dests = [generation.argmax()]
            generation.fill(0)
            generation[dests] = generation.sum()
        else:
            generation[dests] *= generation.sum() / generation[dests].sum()
            generation[~dests] = 0
        prob = self.calc_prob(mode, impedance, orig, dests)
        demand = numpy.zeros_like(impedance["time"])
        demand[dests, :] = (prob * generation[dests]).T
        self.attracted_tours[mode][self.bounds] += demand.sum(0)
        return Demand(self, mode, demand, orig_offset + orig)

    def calc_prob(self, mode, impedance, orig, dests):
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
        dest_imp = {}
        for mtx_type in impedance:
            dest_imp[mtx_type] = (impedance[mtx_type][dests, :]
                                  + impedance[mtx_type][:, orig]
                                  - impedance[mtx_type][dests, orig][:, numpy.newaxis])
        return self.model.calc_prob(mode, dest_imp, orig, dests)

    def print_data(self):
        self.resultdata.print_data(
            pandas.Series(
                sum(self.attracted_tours.values()),
                self.zone_data.zone_numbers),
            "attraction.txt", self.name)
