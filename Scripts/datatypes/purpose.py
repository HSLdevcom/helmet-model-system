import parameters as param
import models.logit as logit
import models.generation as generation
from datatypes.demand import Demand
import datahandling.resultdata as result
import numpy
import pandas

class Purpose:
    def __init__(self, specification, zone_data):
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
        self.name = specification["name"]
        self.orig = specification["orig"]
        self.dest = specification["dest"]
        self.area = specification["area"]
        self.sources = []
        if self.area == "metropolitan":
            l = 0
            u = zone_data.first_peripheral_zone
        if self.area == "peripheral":
            l = zone_data.first_peripheral_zone
            u = zone_data.nr_zones
        if self.area == "all":
            l = 0
            u = zone_data.nr_zones
        if self.area == "external":
            l = zone_data.first_external_zone
            u = None
        self.bounds = slice(l, u)
        self.zone_data = zone_data
        self.generated_tours = {}
        self.attracted_tours = {}

    @property
    def zone_numbers(self):
        return self.zone_data.zone_numbers[self.bounds]

class TourPurpose(Purpose):
    def __init__(self, specification, zone_data, is_agent_model):
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
        """
        Purpose.__init__(self, specification, zone_data)
        if self.orig == "source":
            self.gen_model = generation.NonHomeGeneration(self)
        else:
            self.gen_model = generation.GenerationModel(self)
        if self.name == "sop":
            self.model = logit.OriginModel(zone_data, self, is_agent_model)
        elif self.name == "so":
            self.model = logit.DestModeModel(zone_data, self, is_agent_model)
        else:
            self.model = logit.ModeDestModel(zone_data, self, is_agent_model)
        self.modes = self.model.mode_choice_param.keys()
        self.sec_dest_purpose = None

    def init_sums(self):
        for mode in self.modes:
            self.generated_tours[mode] = numpy.zeros_like(self.zone_numbers)
            self.attracted_tours[mode] = numpy.zeros_like(self.zone_data.zone_numbers)

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

    def calc_demand(self):
        """Calculate purpose specific demand matrices.
              
        Return
        ------
        dict
            Mode (car/transit/bike) : dict
                Demand matrix for whole day : Demand
        """
        tours = self.gen_model.get_tours()
        demand = {}
        self.demsums = {}
        attracted_tours = 0
        for mode in self.model.mode_choice_param:
            mtx = (self.prob.pop(mode) * tours).T
            try:
                self.sec_dest_purpose.gen_model.add_tours(mtx, mode, self)
            except AttributeError:
                pass
            demand[mode] = Demand(self, mode, mtx)
            self.attracted_tours[mode] = mtx.sum(0)
            self.generated_tours[mode] = mtx.sum(1)
            attracted_tours += self.attracted_tours[mode]
            trip_lengths = self._count_trip_lengths(
                mtx, self.dist)
            result.print_data(
                trip_lengths, "trip_lengths.txt",
                trip_lengths.index, self.name + "_" + mode[0])
            aggregated_demand = self._aggregate(mtx)
            result.print_matrix(aggregated_demand,
                                "aggregated_demand", self.name + "_" + mode)
            own_zone = self.zone_data.get_data("own_zone", self.bounds)
            own_zone_demand = own_zone * mtx
            own_zone_aggregated = self._aggregate(own_zone_demand)
            result.print_data(
                numpy.diag(own_zone_aggregated), "own_zone_demand.txt",
                own_zone_aggregated.index, self.name + "_" + mode[0])
            self.demsums[mode] = self.generated_tours[mode].sum()
        result.print_data(
            attracted_tours, "attraction.txt",
            self.zone_data.zone_numbers, self.name)
        demand_all = sum(self.demsums.values())
        mode_shares = {mode: self.demsums[mode] / demand_all for mode in self.demsums}
        result.print_data(
            pandas.Series(mode_shares), "mode_share.txt",
            self.demsums.keys(), self.name)
        return demand
    
    def _aggregate(self, mtx):
        """Aggregate matrix to larger areas."""
        dest = self.zone_data.zone_numbers
        orig = self.zone_numbers
        mtx = pandas.DataFrame(mtx, orig, dest)
        areas = (
            "helsinki_cbd",
            "helsinki_other",
            "espoo_vant_kau",
            "surrounding",
            "peripheral",
        )
        aggr_mtx = pandas.DataFrame(0, areas, areas)
        tmp_mtx = pandas.DataFrame(0, areas, dest)
        for area in areas:
            l = param.areas[area][0]
            u = param.areas[area][1]
            tmp_mtx.loc[area] = mtx.loc[l:u].sum(0).values
        for area in areas:
            l = param.areas[area][0]
            u = param.areas[area][1]
            aggr_mtx.loc[:, area] = tmp_mtx.loc[:, l:u].sum(1).values
        return aggr_mtx

    def _count_trip_lengths(self, trips, dist):
        intervals = ("0-1", "1-3", "3-5", "5-10", "10-20", "20-30",
                     "30-40", "40-inf")
        trip_lengths = pandas.Series(index=intervals)
        for tl in trip_lengths.index:
            bounds = tl.split("-")
            l = float(bounds[0])
            u = float(bounds[1])
            trip_lengths[tl] = trips[(dist>=l) & (dist<u)].sum()
        return trip_lengths


class SecDestPurpose(Purpose):
    def __init__(self, specification, zone_data, is_agent_model):
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
        """
        Purpose.__init__(self, specification, zone_data)
        self.gen_model = generation.SecDestGeneration(self)
        self.model = logit.SecDestModel(zone_data, self, is_agent_model)
        self.modes = self.model.dest_choice_param.keys()

    def init_sums(self):
        for mode in self.model.dest_choice_param:
            self.generated_tours[mode] = 0
            self.attracted_tours[mode] = numpy.zeros_like(self.zone_data.zone_numbers, float)

    def generate_tours(self):
        """Generate the source tours without secondary destinations."""
        self.tours = {}
        self.init_sums()
        for mode in self.model.dest_choice_param:
            self.tours[mode] = self.gen_model.get_tours(mode)

    def distribute_tours(self, mode, impedance, origin):
        """Decide the secondary destinations for all tours (generated 
        earlier) starting from one specific zone.
        
        Parameters
        ----------
        mode : str
            Mode (car/transit/bike)
        impedance : dict
            Type (time/cost/dist) : numpy 2d matrix
        origin : int
            The zone index from which these tours origin

        Return
        ------
        Demand
            Matrix of destination -> secondary_destination pairs
            The origin zone for all of these tours
        """
        generation = self.tours[mode][origin, :]
        # All o-d pairs below threshold are neglected,
        # total demand is increased for other pairs.
        dests = generation > param.secondary_destination_threshold
        if not dests.any():
            # If no o-d pairs have demand above threshold,
            # the sole destination with largest demand is picked
            dests = generation.argmax()
            generation_sum = generation.sum()
            generation.fill(0)
            generation[dests] = generation_sum
        else:
            generation[dests] *= generation.sum() / generation[dests].sum()
            generation[~dests] = 0
        dest_imp = {}
        for mtx_type in impedance:
            try:
                dest_imp[mtx_type] = ( impedance[mtx_type][dests, :]
                                     + impedance[mtx_type][:, origin]
                                     - impedance[mtx_type][dests, origin][:, numpy.newaxis])
            except IndexError:
                dest_imp[mtx_type] = ( impedance[mtx_type][dests, :]
                                     + impedance[mtx_type][:, origin]
                                     - impedance[mtx_type][dests, origin])
        # TODO Make origin distinction between impedance matrix and lookup
        # In peripheral area these would not be the same
        prob = self.model.calc_prob(mode, dest_imp, origin, dests)
        demand = numpy.zeros_like(impedance["time"])
        demand[dests, :] = (prob * generation[dests]).T
        self.attracted_tours[mode][self.bounds] += demand.sum(0)
        return Demand(self, mode, demand, origin)

    def calc_prob(self, mode, impedance, position):
        """Calculate secondary destination probabilites for tours
        starting and ending in two specific zones.
        Method used in agent-based simulation.
        
        Parameters
        ----------
        mode : str
            Mode (car/transit/bike)
        impedance : dict
            Type (time/cost/dist) : numpy 2d matrix
        position : tuple
            int
                Origin zone
            int
                Destination zone

        Return
        ------
        numpy 1-d array
            Probability vector for chosing zones as secondary destination
        """
        orig = position[0]
        dest = position[1]
        dest_imp = {}
        for mtx_type in impedance:
            dest_imp[mtx_type] = ( impedance[mtx_type][dest, :]
                                 + impedance[mtx_type][:, orig]
                                 - impedance[mtx_type][dest, orig])
        return self.model.calc_prob(mode, dest_imp, orig, dest)
