import numpy
import pandas

from parameters.destination_choice import secondary_destination_threshold
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

    def __init__(self, specification, zone_data, resultdata=None):
        self.name = specification["name"]
        self.orig = specification["orig"]
        self.dest = specification["dest"]
        self.area = specification["area"]
        self.sources = []
        if self.area == "metropolitan":
            l = 0
            m = zone_data.first_surrounding_zone
            u = zone_data.first_peripheral_zone
        if self.area == "peripheral":
            l = zone_data.first_peripheral_zone
            m = None
            u = zone_data.nr_zones
        if self.area == "all":
            l = 0
            m = zone_data.first_surrounding_zone
            u = zone_data.nr_zones
        if self.area == "external":
            l = zone_data.first_external_zone
            m = None
            u = None
        self.bounds = slice(l, u)
        self.lbounds = slice(l, m)
        self.ubounds = slice(m, u)
        self.zone_data = zone_data
        self.resultdata = resultdata
        self.model = None
        self.modes = []
        self.generated_tours = {}
        self.attracted_tours = {}

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
    is_agent_model : bool (optional)
        Whether the model is used for agent-based simulation
    """

    def __init__(self, specification, zone_data, resultdata, is_agent_model):
        Purpose.__init__(self, specification, zone_data, resultdata)
        if self.orig == "source":
            self.gen_model = generation.NonHomeGeneration(self, resultdata)
        else:
            self.gen_model = generation.GenerationModel(self, resultdata)
        if self.name == "sop":
            self.model = logit.OriginModel(
                zone_data, self, resultdata, is_agent_model)
        elif self.name == "so":
            self.model = logit.DestModeModel(
                zone_data, self, resultdata, is_agent_model)
        else:
            self.model = logit.ModeDestModel(
                zone_data, self, resultdata, is_agent_model)
            self.access_model = logit.AccessibilityModel(
                zone_data, self, resultdata, is_agent_model)
        self.modes = self.model.mode_choice_param.keys()
        self.histograms = {mode: TourLengthHistogram() for mode in self.modes}
        self.aggregates = {mode: MatrixAggregator(zone_data.zone_numbers)
            for mode in self.modes}
        self.own_zone_aggregates = {mode: ArrayAggregator(zone_data.zone_numbers)
            for mode in self.modes}
        self.sec_dest_purpose = None

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
        self.model.calc_basic_prob(impedance)
        self.dist = impedance["car"]["dist"]

    def calc_demand(self):
        """Calculate purpose specific demand matrices.
              
        Returns
        -------
        dict
            Mode (car/transit/bike) : dict
                Demand matrix for whole day : Demand
        """
        tours = self.gen_model.get_tours()
        demand = {}
        for mode in self.modes:
            mtx = (self.prob.pop(mode) * tours).T
            try:
                self.sec_dest_purpose.gen_model.add_tours(mtx, mode, self)
            except AttributeError:
                pass
            demand[mode] = Demand(self, mode, mtx)
            self.attracted_tours[mode] = mtx.sum(0)
            self.generated_tours[mode] = mtx.sum(1)
            self.histograms[mode].count_tour_dists(mtx, self.dist)
            self.aggregates[mode].aggregate(pandas.DataFrame(
                mtx, self.zone_numbers, self.zone_data.zone_numbers))
            self.own_zone_aggregates[mode].aggregate(pandas.Series(
                numpy.diag(mtx), self.zone_numbers))
        self.print_data()
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
    is_agent_model : bool (optional)
        Whether the model is used for agent-based simulation
    """

    def __init__(self, specification, zone_data, resultdata, is_agent_model):
        Purpose.__init__(self, specification, zone_data, resultdata)
        self.gen_model = generation.SecDestGeneration(self, resultdata)
        self.model = logit.SecDestModel(
            zone_data, self, resultdata, is_agent_model)
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
