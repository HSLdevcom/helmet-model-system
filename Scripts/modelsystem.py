import threading
import multiprocessing
import os
import numpy
import pandas
from collections import defaultdict

import utils.log as log
import assignment.departure_time as dt
from datahandling.resultdata import ResultsData
from datahandling.zonedata import ZoneData, BaseZoneData
from datahandling.matrixdata import MatrixData
from demand.freight import FreightModel
from demand.trips import DemandModel
from demand.external import ExternalModel
from datatypes.purpose import SecDestPurpose
from transform.impedance_transformer import ImpedanceTransformer
from models.linear import CarDensityModel
import parameters.assignment as param
import parameters.zone as zone_param


class ModelSystem:
    """Object keeping track of all sub-models and tasks in model system.
    
    Parameters
    ----------
    zone_data_path : str
        Directory path where input data for forecast year are found
    base_zone_data_path : str
        Directory path where input data for base year are found
    base_matrices_path : str
        Directory path where base demand matrices are found
    results_path : str
        Directory path where to store results
    assignment_model : assignment.abstract_assignment.AssignmentModel
        Assignment model wrapper used in model runs,
        can be EmmeAssignmentModel or MockAssignmentModel
    name : str
        Name of scenario, used for results subfolder
    """

    def __init__(self, zone_data_path, base_zone_data_path, base_matrices_path,
                 results_path, assignment_model, name):
        self.ass_model = assignment_model
        self.zone_numbers = self.ass_model.zone_numbers
        self.emme_scenarios = self.ass_model.emme_scenarios

        # Input data
        self.zdata_base = BaseZoneData(
            base_zone_data_path, self.zone_numbers)
        self.basematrices = MatrixData(base_matrices_path)
        self.zdata_forecast = ZoneData(
            zone_data_path, self.zone_numbers)

        # Set dist unit cost from zonedata
        self.ass_model.dist_unit_cost = self.zdata_forecast.car_dist_cost

        # Output data
        self.resultmatrices = MatrixData(
            os.path.join(results_path, name, "Matrices"))
        self.resultdata = ResultsData(os.path.join(results_path, name))

        self.dm = self._init_demand_model()
        self.fm = FreightModel(
            self.zdata_base, self.zdata_forecast, self.basematrices)
        self.em = ExternalModel(
            self.basematrices, self.zdata_forecast, self.zone_numbers)
        self.dtm = dt.DepartureTimeModel(
            self.ass_model.nr_zones, self.emme_scenarios)
        self.imptrans = ImpedanceTransformer()
        bounds = slice(0, self.zdata_forecast.nr_zones)
        self.cdm = CarDensityModel(
            self.zdata_base, self.zdata_forecast, bounds, self.resultdata)
        self.mode_share = []
        self.trucks = self.fm.calc_freight_traffic("truck")
        self.trailer_trucks = self.fm.calc_freight_traffic("trailer_truck")

    def _init_demand_model(self):
        return DemandModel(self.zdata_forecast, self.resultdata, is_agent_model=False)

    def _add_internal_demand(self, previous_iter_impedance, is_last_iteration):
        """Produce mode-specific demand matrices.

        Add them for each time-period to container in departure time model.

        Parameters
        ----------
        previous_iter_impedance : dict
            key : str
                Assignment class (car/transit/bike/walk)
            value : dict
                key : str
                    Impedance type (time/cost/dist)
                value : numpy.ndarray
                    Impedance (float 2-d matrix)
        is_last_iteration : bool (optional)
            If this is the last iteration, 
            secondary destinations are calculated for all modes
        """
        log.info("Demand calculation started...")

        # Mode and destination probability matrices are calculated first,
        # as logsums from probability calculation are used in tour generation.
        self.dm.create_population_segments()
        for purpose in self.dm.tour_purposes:
            if isinstance(purpose, SecDestPurpose):
                purpose.gen_model.init_tours()
            else:
                purpose.calc_prob(
                    self.imptrans.transform(purpose, previous_iter_impedance))
        
        # Tour generation
        self.dm.generate_tours()
        
        # Assigning of tours to mode, destination and time period
        self.travel_modes = set()
        for purpose in self.dm.tour_purposes:
            if isinstance(purpose, SecDestPurpose):
                purpose_impedance = self.imptrans.transform(
                    purpose, previous_iter_impedance)
                purpose.generate_tours()
                if is_last_iteration:
                    for mode in purpose.model.dest_choice_param:
                        self._distribute_sec_dests(
                            purpose, mode, purpose_impedance)
                else:
                    self._distribute_sec_dests(
                        purpose, "car", purpose_impedance)
            else:
                demand = purpose.calc_demand()
                if purpose.dest != "source":
                    for mode in demand:
                        self.dtm.add_demand(demand[mode])
                        self.travel_modes.add(mode)
        log.info("Demand calculation completed")

    # possibly merge with init
    def assign_base_demand(self, use_fixed_transit_cost=False, is_end_assignment=False):
        """Assign base demand to network (before first iteration).

        Parameters
        ----------
        use_fixed_transit_cost : bool (optional)
            If transit cost is already calculated for this scenario and is
            found in Results folder, it can be reused to save time
        is_end_assignment : bool (optional)
            If base demand is assigned without demand calculations

        Returns
        -------
        dict
            key : str
                Assignment class (car/transit/bike/walk)
            value : dict
                key : str
                    Impedance type (time/cost/dist)
                value : numpy.ndarray
                    Impedance (float 2-d matrix)
        """
        impedance = {}

        # create attributes and background variables to network
        self.ass_model.prepare_network()

        # Calculate transit cost matrix, and save it to emmebank
        with self.basematrices.open("demand", "aht", self.ass_model.zone_numbers) as mtx:
            base_demand = {ass_class: mtx[ass_class] for ass_class in param.transport_classes}
        self.ass_model.assign("aht", base_demand, iteration="init")
        with self.basematrices.open("cost", "peripheral") as peripheral_mtx:
            peripheral_cost = numpy.array(peripheral_mtx._file["transit"])
        if use_fixed_transit_cost:
            log.info("Using fixed transit cost matrix")
            with self.resultmatrices.open("cost", "aht") as aht_mtx:
                fixed_cost = aht_mtx["transit_work"]
        else:
            log.info("Calculating transit cost")
            fixed_cost = None
        self.ass_model.calc_transit_cost(
            self.zdata_forecast.transit_zone, peripheral_cost, fixed_cost)

        # Perform traffic assignment and get result impedance, 
        # for each time period
        demand = self.resultmatrices if is_end_assignment else self.basematrices
        for tp in self.emme_scenarios:
            log.info("Assigning period " + tp)
            with demand.open("demand", tp, self.ass_model.zone_numbers) as mtx:
                for ass_class in param.transport_classes:
                    self.dtm.demand[tp][ass_class] = mtx[ass_class]
            impedance[tp] = self.ass_model.assign(
                tp, self.dtm.demand[tp], 
                iteration=("last" if is_end_assignment else 0))
            if tp == "aht":
                self._update_ratios(impedance[tp], tp)
            if is_end_assignment:
                self._save_to_omx(impedance[tp], tp)
        if is_end_assignment:
            self.ass_model.aggregate_results(self.resultdata)
        self.dtm.init_demand()
        return impedance

    def run_iteration(self, previous_iter_impedance, iteration=None):
        """Calculate demand and assign to network.

        Parameters
        ----------
        previous_iter_impedance : dict
            key : str
                Assignment class (car/transit/bike/walk)
            value : dict
                key : str
                    Impedance type (time/cost/dist)
                value : numpy.ndarray
                    Impedance (float 2-d matrix)
        iteration : int or str (optional)
            Iteration number (0, 1, 2, ...) or "last"
            If this is the last iteration, 
            secondary destinations are calculated for all modes,
            congested assignment is performed,
            and matrix and assignment results are printed.
        Returns
        -------
        dict
            key : str
                Assignment class (car/transit/bike/walk)
            value : dict
                key : str
                    Impedance type (time/cost/dist)
                value : numpy.ndarray
                    Impedance (float 2-d matrix)
        """
        impedance = {}

        # Add truck and trailer truck demand, to time-period specific
        # matrices (DTM), used in traffic assignment
        self.dtm.add_demand(self.trucks)
        self.dtm.add_demand(self.trailer_trucks)

        # Update car density
        prediction = self.cdm.predict()
        self.zdata_forecast["car_density"] = prediction
        self.zdata_forecast["cars_per_1000"] = 1000 * prediction

        # Calculate internal demand
        self._add_internal_demand(previous_iter_impedance, iteration=="last")

        # Calculate external demand
        for mode in param.external_modes:
            if mode == "truck":
                int_demand = self.trucks.matrix.sum(0) + self.trucks.matrix.sum(1)
            elif mode == "trailer_truck":
                int_demand = self.trailer_trucks.matrix.sum(0) + self.trailer_trucks.matrix.sum(1)
            else:
                int_demand = self._sum_trips_per_zone(mode)
            ext_demand = self.em.calc_external(mode, int_demand)
            self.dtm.add_demand(ext_demand)

        # Calculate trips and mode shares
        trip_sum = {}
        for mode in self.travel_modes:
            trip_sum[mode] = self._sum_trips_per_zone(mode)
        sum_all = sum(trip_sum.values())
        mode_share = {}
        for mode in trip_sum:
            self.resultdata.print_data(
                pandas.Series(trip_sum[mode], self.zdata_base.zone_numbers),
                "origins_demand.txt", mode)
            self.resultdata.print_data(
                pandas.Series(trip_sum[mode] / sum_all, self.zdata_base.zone_numbers),
                "origins_shares.txt", mode)
            mode_share[mode] = trip_sum[mode].sum() / sum_all.sum()
        self.mode_share.append(mode_share)

        # Calculate and return traffic impedance
        for tp in self.emme_scenarios:
            log.info("Assigning period " + tp)
            self.dtm.add_vans(tp, self.zdata_forecast.nr_zones)
            impedance[tp] = self.ass_model.assign(
                tp, self.dtm.demand[tp], iteration)
            if tp == "aht":
                self._update_ratios(impedance[tp], tp)
            if iteration=="last":
                self._save_to_omx(impedance[tp], tp)
        if iteration=="last":
            self.ass_model.aggregate_results(self.resultdata)

        # Reset time-period specific demand matrices (DTM), and empty result buffer
        self.dtm.init_demand()
        self.resultdata.flush()
        return impedance

    def _save_to_omx(self, impedance, tp):
        zone_numbers = self.ass_model.zone_numbers
        with self.resultmatrices.open("demand", tp, zone_numbers, 'w') as mtx:
            for ass_class in self.dtm.demand[tp]:
                mtx[ass_class] = self.dtm.demand[tp][ass_class]
            log.info("Saved demand matrices for " + str(tp))
        for mtx_type in impedance:
            with self.resultmatrices.open(mtx_type, tp, zone_numbers, 'w') as mtx:
                for ass_class in impedance[mtx_type]:
                    mtx[ass_class] = impedance[mtx_type][ass_class]

    def _sum_trips_per_zone(self, mode):
        int_demand = numpy.zeros(self.zdata_base.nr_zones)
        for purpose in self.dm.tour_purposes:
            if mode in purpose.modes and purpose.dest != "source":
                if isinstance(purpose, SecDestPurpose):
                    bounds = next(iter(purpose.sources)).bounds
                else:
                    bounds = purpose.bounds
                int_demand[bounds] += purpose.generated_tours[mode]
                int_demand += purpose.attracted_tours[mode]
        return int_demand

    def _distribute_sec_dests(self, purpose, mode, impedance):
        threads = []
        demand = []
        nr_threads = param.performance_settings["number_of_processors"]
        if nr_threads == "max":
            nr_threads = multiprocessing.cpu_count()
        elif nr_threads <= 0:
            nr_threads = 1
        bounds = next(iter(purpose.sources)).bounds
        split = (bounds.stop-bounds.start) // nr_threads
        for i in xrange(nr_threads):
            # Take a chunk of destinations, for which this thread
            # will calculate secondary destinations
            start = bounds.start + i*split
            if i+1 < nr_threads:
                dests = xrange(start, start + split)
            else:
                dests = xrange(start, bounds.stop)
            # Results will be saved in a temp dtm, to avoid memory clashes
            dtm = dt.DepartureTimeModel(self.ass_model.nr_zones, self.emme_scenarios)
            demand.append(dtm)
            thread = threading.Thread(
                target=self._distribute_tours,
                args=(dtm, purpose, mode, impedance, dests))
            threads.append(thread)
            thread.start()
        for thread in threads:
            thread.join()
        for dtm in demand:
            for tp in dtm.demand:
                for ass_class in dtm.demand[tp]:
                    self.dtm.demand[tp][ass_class] += dtm.demand[tp][ass_class]
        purpose.print_data()

    def _distribute_tours(self, container, purpose, mode, impedance, dests):
        for i in dests:
            demand = purpose.distribute_tours(mode, impedance[mode], i)
            container.add_demand(demand)

    def _update_ratios(self, impedance, tp):
        """Calculate time and cost ratios.
        
        Parameters
        ----------
        impedance : dict
            Impedance matrices.
        tp : str
            Time period (usually aht in this function).
        """ 
        car_time = numpy.ma.average(
            impedance["time"]["car_work"], axis=1,
            weights=self.dtm.demand[tp]["car_work"])
        transit_time = numpy.ma.average(
            impedance["time"]["transit_work"], axis=1,
            weights=self.dtm.demand[tp]["transit_work"])
        time_ratio = transit_time / car_time
        self.resultdata.print_data(
            pandas.Series(time_ratio, self.zone_numbers),
            "impedance_ratio.txt", "time")
        self.zdata_forecast["time_ratio"] = pandas.Series(
            numpy.ma.getdata(time_ratio), self.zone_numbers)
        car_cost = numpy.ma.average(
            impedance["cost"]["car_work"], axis=1,
            weights=self.dtm.demand[tp]["car_work"])
        transit_cost = numpy.ma.average(
            impedance["cost"]["transit_work"], axis=1,
            weights=self.dtm.demand[tp]["transit_work"])
        cost_ratio = transit_cost / 44. / car_cost
        cost_ratio = cost_ratio.clip(0.01, None)
        self.resultdata.print_data(
            pandas.Series(cost_ratio, self.zone_numbers),
            "impedance_ratio.txt", "cost")
        self.zdata_forecast["cost_ratio"] = pandas.Series(
            numpy.ma.getdata(cost_ratio), self.zone_numbers)


class AgentModelSystem(ModelSystem):
    """Object keeping track of all sub-models and tasks in agent model system.

    Agents are added one-by-one to departure time model,
    where they are (so far) split in deterministic fractions.
    
    Parameters
    ----------
    zone_data_path : str
        Directory path where input data for forecast year are found
    base_zone_data_path : str
        Directory path where input data for base year are found
    base_matrices_path : str
        Directory path where base demand matrices are found
    results_path : str
        Directory path where to store results
    assignment_model : assignment.abstract_assignment.AssignmentModel
        Assignment model wrapper used in model runs,
        can be EmmeAssignmentModel or MockAssignmentModel
    name : str
        Name of scenario, used for results subfolder
    """

    def _init_demand_model(self):
        log.info("Creating synthetic population")
        nr_threads = param.performance_settings["number_of_processors"]
        if nr_threads == "max":
            nr_threads = multiprocessing.cpu_count()
        elif nr_threads <= 0:
            nr_threads = 1
        return DemandModel(
            self.zdata_forecast, self.resultdata, is_agent_model=True,
            nr_threads=nr_threads)

    def _add_internal_demand(self, previous_iter_impedance, is_last_iteration):
        """Produce tours and add fractions of them
        for each time-period to container in departure time model.

        Parameters
        ----------
        previous_iter_impedance : dict
            key : str
                Assignment class (car/transit/bike/walk)
            value : dict
                key : str
                    Impedance type (time/cost/dist)
                value : numpy.ndarray
                    Impedance (float 2-d matrix)
        is_last_iteration : bool (optional)
            If this is the last iteration, 
            secondary destinations are calculated for all modes
        """
        log.info("Demand calculation started...")
        self.dm.cm.calc_basic_prob()
        self.travel_modes = set()
        for purpose in self.dm.tour_purposes:
            if isinstance(purpose, SecDestPurpose):
                purpose.init_sums()
            else:
                purpose_impedance = self.imptrans.transform(
                    purpose, previous_iter_impedance)
                if purpose.area == "peripheral" or purpose.name == "oop":
                    purpose.calc_prob(purpose_impedance)
                    purpose.gen_model.init_tours()
                    purpose.gen_model.add_tours()
                    demand = purpose.calc_demand()
                    if purpose.dest != "source":
                        for mode in demand:
                            self.travel_modes.add(mode)
                            self.dtm.add_demand(demand[mode])
                else:
                    purpose.init_sums()
                    purpose.model.calc_basic_prob(purpose_impedance)
        tour_probs = self.dm.generate_tour_probs()
        purpose_impedance = self.imptrans.transform(
            self.dm.purpose_dict["hoo"], previous_iter_impedance)
        log.info("Assigning mode and destination for {} agents ({} % of total population)".format(
            self.dm.population_size, int(zone_param.agent_demand_fraction*100)))
        threads = []
        for persons in self.dm.population:
            thread = threading.Thread(
                target=self._distribute_tours,
                args=(persons, purpose_impedance, tour_probs))
            threads.append(thread)
            thread.start()
        for thread in threads:
            thread.join()
        for purpose in self.dm.tour_purposes:
            purpose.print_data()
        for persons in self.dm.population:
            for person in persons:
                for tour in person.tours:
                    self.dtm.add_demand(tour)
        log.info("Demand calculation completed")

    def _distribute_tours(self, persons, impedance, tour_probs):
        sec_dest_purpose = self.dm.purpose_dict["hoo"]
        sec_dest_tours = {mode: defaultdict(list)
            for mode in sec_dest_purpose.modes}
        for person in persons:
            person.decide_car_use()
            person.add_tours(self.dm.purpose_dict, tour_probs)
            for tour in person.tours:
                tour.choose_mode(person.is_car_user)
                tour.choose_destination(sec_dest_tours)
        for mode in sec_dest_tours:
            for od_pair in sec_dest_tours[mode]:
                probs = sec_dest_purpose.calc_prob(
                    mode, impedance[mode], od_pair).cumsum()
                for tour in sec_dest_tours[mode][od_pair]:
                    tour.choose_secondary_destination(probs)
