import threading
import multiprocessing
import os
import numpy
import pandas
import random
from collections import defaultdict

import utils.log as log
from utils.zone_interval import ArrayAggregator
import assignment.departure_time as dt
from datahandling.resultdata import ResultsData
from datahandling.zonedata import ZoneData, BaseZoneData
from datahandling.matrixdata import MatrixData
from demand.freight import FreightModel
from demand.trips import DemandModel
from demand.external import ExternalModel
from datatypes.purpose import SecDestPurpose
from datatypes.person import Person
from datatypes.tour import Tour
from transform.impedance_transformer import ImpedanceTransformer
from models.linear import CarDensityModel
import parameters.assignment as param
import parameters.zone as zone_param
import parameters.tour_generation as gen_param


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
        self.travel_modes = {}  # Dict instead of set, to preserve order

        # Input data
        self.zdata_base = BaseZoneData(
            base_zone_data_path, self.zone_numbers)
        self.basematrices = MatrixData(base_matrices_path)
        self.zdata_forecast = ZoneData(
            zone_data_path, self.zone_numbers)

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
            self.ass_model.nr_zones, self.ass_model.time_periods)
        self.imptrans = ImpedanceTransformer()
        bounds = slice(0, self.zdata_forecast.nr_zones)
        self.cdm = CarDensityModel(
            self.zdata_base, self.zdata_forecast, bounds, self.resultdata)
        self.mode_share = []
        self.convergence = pandas.DataFrame()
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
                purpose_impedance = self.imptrans.transform(
                    purpose, previous_iter_impedance)
                purpose.calc_prob(purpose_impedance)
                if is_last_iteration and purpose.name not in ("sop", "so"):
                    purpose.accessibility_model.calc_accessibility(
                        purpose_impedance)
        
        # Tour generation
        self.dm.generate_tours()
        
        # Assigning of tours to mode, destination and time period
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
                if purpose.name != "wh":
                    demand = purpose.calc_demand()
                if purpose.dest != "source":
                    for mode in demand:
                        self.dtm.add_demand(demand[mode])
                        self.travel_modes[mode] = True
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
        self.ass_model.prepare_network(self.zdata_forecast.car_dist_cost)

        # Calculate transit cost matrix, and save it to emmebank
        time_periods = self.ass_model.time_periods
        with self.basematrices.open(
                "demand", time_periods[0], self.ass_model.zone_numbers) as mtx:
            base_demand = {ass_class: mtx[ass_class]
                for ass_class in param.transport_classes}
        self.ass_model.init_assign(base_demand)
        if use_fixed_transit_cost:
            log.info("Using fixed transit cost matrix")
            with self.resultmatrices.open("cost", time_periods[0]) as aht_mtx:
                fixed_cost = aht_mtx["transit_work"]
        else:
            log.info("Calculating transit cost")
            fixed_cost = None
        self.ass_model.calc_transit_cost(
            self.zdata_forecast.transit_zone,
            self.basematrices.peripheral_transit_cost(self.zdata_base),
            fixed_cost)

        # Perform traffic assignment and get result impedance, 
        # for each time period
        demand = self.resultmatrices if is_end_assignment else self.basematrices
        for ap in self.ass_model.assignment_periods:
            tp = ap.name
            log.info("Assigning period {}...".format(tp))
            with demand.open("demand", tp, self.ass_model.zone_numbers) as mtx:
                for ass_class in param.transport_classes:
                    self.dtm.demand[tp][ass_class] = mtx[ass_class]
            impedance[tp] = ap.assign(
                self.dtm.demand[tp],
                iteration=("last" if is_end_assignment else 0))
            if tp == time_periods[0]:
                self._update_ratios(impedance[tp], tp)
            if is_end_assignment:
                self._save_to_omx(impedance[tp], tp)
        if is_end_assignment:
            self.ass_model.aggregate_results(self.resultdata)
            self._calculate_noise_areas()
            self.resultdata.flush()
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
                int_demand = pandas.Series(
                    self.trucks.matrix.sum(0) + self.trucks.matrix.sum(1),
                    self.zdata_base.zone_numbers)
            elif mode == "trailer_truck":
                int_demand = pandas.Series(
                    (self.trailer_trucks.matrix.sum(0)
                     + self.trailer_trucks.matrix.sum(1)),
                    self.zdata_base.zone_numbers)
            else:
                int_demand = self._sum_trips_per_zone(mode)
            ext_demand = self.em.calc_external(mode, int_demand)
            self.dtm.add_demand(ext_demand)

        # Calculate tour sums and mode shares
        tour_sum = {mode: self._sum_trips_per_zone(mode, include_dests=False)
            for mode in self.travel_modes}
        sum_all = sum(tour_sum.values())
        mode_shares = {}
        ar = ArrayAggregator(sum_all.index)
        for mode in tour_sum:
            self.resultdata.print_data(
                tour_sum[mode], "origins_demand.txt", mode)
            self.resultdata.print_data(
                ar.aggregate(tour_sum[mode]), "origins_demand_areas.txt", mode)
            self.resultdata.print_data(
                tour_sum[mode] / sum_all, "origins_shares.txt", mode)
            mode_shares[mode] = tour_sum[mode].sum() / sum_all.sum()
        self.mode_share.append(mode_shares)
        trip_sum = {mode: self._sum_trips_per_zone(mode)
            for mode in self.travel_modes}
        for mode in tour_sum:
            self.resultdata.print_data(
                ar.aggregate(trip_sum[mode]), "trips_areas.txt", mode)
        self.resultdata.print_line("\nAssigned demand", "result_summary")
        self.resultdata.print_line(
            "\t" + "\t".join(param.transport_classes), "result_summary")

        # Add vans and save demand matrices
        for ap in self.ass_model.assignment_periods:
            self.dtm.add_vans(ap.name, self.zdata_forecast.nr_zones)
            if iteration=="last":
                self._save_demand_to_omx(ap.name)

        # Calculate and return traffic impedance
        for ap in self.ass_model.assignment_periods:
            tp = ap.name
            log.info("Assigning period " + tp)
            impedance[tp] = ap.assign(self.dtm.demand[tp], iteration)
            if tp == "aht":
                self._update_ratios(impedance[tp], tp)
            if iteration=="last":
                impedance[tp]["time"]["transit_uncongested"] = previous_iter_impedance[tp]["time"]["transit_work"]
                self._save_to_omx(impedance[tp], tp)
        if iteration=="last":
            self.ass_model.aggregate_results(self.resultdata)
            self._calculate_noise_areas()
            self._calculate_accessibility_and_savu_zones()
            self.resultdata.print_line("\nMode shares", "result_summary")
            for mode in mode_shares:
                self.resultdata.print_line(
                    "{}\t{:1.2%}".format(mode, mode_shares[mode]),
                    "result_summary")

        # Reset time-period specific demand matrices (DTM),
        # and empty result buffer
        gap = self.dtm.init_demand()
        log.info("Demand model convergence in iteration {} is {:1.5f}".format(
            iteration, gap["rel_gap"]))
        self.convergence = self.convergence.append(gap, ignore_index=True)
        self.resultdata._df_buffer["demand_convergence.txt"] = self.convergence
        self.resultdata.flush()
        return impedance

    def _save_demand_to_omx(self, tp):
        zone_numbers = self.ass_model.zone_numbers
        demand_sum_string = tp
        with self.resultmatrices.open("demand", tp, zone_numbers, 'w') as mtx:
            for ass_class in param.transport_classes:
                demand = self.dtm.demand[tp][ass_class]
                mtx[ass_class] = demand
                demand_sum_string += "\t{:8.0f}".format(demand.sum())
        self.resultdata.print_line(demand_sum_string, "result_summary")
        log.info("Saved demand matrices for " + str(tp))

    def _save_to_omx(self, impedance, tp):
        zone_numbers = self.ass_model.zone_numbers
        for mtx_type in impedance:
            with self.resultmatrices.open(mtx_type, tp, zone_numbers, 'w') as mtx:
                for ass_class in impedance[mtx_type]:
                    mtx[ass_class] = impedance[mtx_type][ass_class]

    def _calculate_noise_areas(self):
        noise_areas = self.ass_model.calc_noise()
        self.resultdata.print_data(noise_areas, "noise_areas.txt", "area")
        ar = ArrayAggregator(self.zdata_forecast.zone_numbers)
        pop = ar.aggregate(self.zdata_forecast["population"])
        conversion = pandas.Series(zone_param.pop_share_per_noise_area)
        noise_pop = conversion * noise_areas * pop
        self.resultdata.print_data(noise_pop, "noise_areas.txt", "population")

    def _calculate_accessibility_and_savu_zones(self):
        logsum = 0
        sust_logsum = 0
        car_logsum = 0
        for purpose in self.dm.tour_purposes:
            if (purpose.area == "metropolitan" and purpose.orig == "home"
                    and purpose.dest != "source"
                    and not isinstance(purpose, SecDestPurpose)):
                zone_numbers = purpose.zone_numbers
                bounds = purpose.bounds
                weight = gen_param.tour_generation[purpose.name]["population"]
                logsum += weight * purpose.access
                sust_logsum += weight * purpose.sustainable_access
                car_logsum += weight * purpose.car_access
        pop = self.zdata_forecast["population"][bounds]
        self.resultdata.print_line(
            "\nTotal accessibility:\t{:1.2f}".format(
                numpy.average(logsum, weights=pop)),
            "result_summary")
        self.resultdata.print_data(logsum, "accessibility.txt", "all")
        avg_sust_logsum = numpy.average(sust_logsum, weights=pop)
        self.resultdata.print_line(
            "Sustainable accessibility:\t{:1.2f}".format(avg_sust_logsum),
            "result_summary")
        self.resultdata.print_data(
            sust_logsum, "sustainable_accessibility.txt", "all")
        self.resultdata.print_data(car_logsum, "car_accessibility.txt", "all")
        intervals = zone_param.savu_intervals
        savu = numpy.searchsorted(intervals, sust_logsum) + 1
        self.resultdata.print_data(
            pandas.Series(savu, zone_numbers), "savu.txt", "savu_zone")
        avg_savu = numpy.searchsorted(intervals, avg_sust_logsum) + 1
        avg_savu += ((avg_sust_logsum - intervals[avg_savu-2])
                     / (intervals[avg_savu-1] - intervals[avg_savu-2]))
        self.resultdata.print_line(
            "Average SAVU:\t{:1.4f}".format(avg_savu),
            "result_summary")

    def _sum_trips_per_zone(self, mode, include_dests=True):
        int_demand = pandas.Series(0, self.zdata_base.zone_numbers)
        for purpose in self.dm.tour_purposes:
            if mode in purpose.modes and purpose.dest != "source":
                bounds = (next(iter(purpose.sources)).bounds
                    if isinstance(purpose, SecDestPurpose)
                    else purpose.bounds)
                int_demand[bounds] += purpose.generated_tours[mode]
                if include_dests:
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
        for i in range(nr_threads):
            # Take a range of origins, for which this thread
            # will calculate secondary destinations
            origs = range(i, bounds.stop - bounds.start, nr_threads)
            # Results will be saved in a temp dtm, to avoid memory clashes
            dtm = dt.DepartureTimeModel(
                self.ass_model.nr_zones, self.ass_model.time_periods)
            demand.append(dtm)
            thread = threading.Thread(
                target=self._distribute_tours,
                args=(dtm, purpose, mode, impedance, origs))
            threads.append(thread)
            thread.start()
        for thread in threads:
            thread.join()
        for dtm in demand:
            for tp in dtm.demand:
                for ass_class in dtm.demand[tp]:
                    self.dtm.demand[tp][ass_class] += dtm.demand[tp][ass_class]
        purpose.print_data()

    def _distribute_tours(self, container, purpose, mode, impedance, origs):
        for orig in origs:
            demand = purpose.distribute_tours(mode, impedance[mode], orig)
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
        time_ratio = time_ratio.clip(0.01, None)
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
        random.seed(zone_param.population_draw)
        return DemandModel(self.zdata_forecast, self.resultdata, is_agent_model=True)

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
        random.seed(None)
        self.dm.car_use_model.calc_basic_prob()
        for purpose in self.dm.tour_purposes:
            if isinstance(purpose, SecDestPurpose):
                purpose.init_sums()
            else:
                purpose_impedance = self.imptrans.transform(
                    purpose, previous_iter_impedance)
                if (purpose.area == "peripheral" or purpose.dest == "source"
                        or purpose.name == "oop"):
                    purpose.calc_prob(purpose_impedance)
                    purpose.gen_model.init_tours()
                    purpose.gen_model.add_tours()
                    demand = purpose.calc_demand()
                    if purpose.dest != "source":
                        for mode in demand:
                            self.travel_modes[mode] = True
                            self.dtm.add_demand(demand[mode])
                else:
                    for mode in purpose.modes:
                        self.travel_modes[mode] = True
                    purpose.init_sums()
                    purpose.calc_basic_prob(purpose_impedance)
                if is_last_iteration and purpose.dest != "source":
                    purpose.accessibility_model.calc_accessibility(
                        purpose_impedance)
        tour_probs = self.dm.generate_tour_probs()
        log.info("Assigning mode and destination for {} agents ({} % of total population)".format(
            len(self.dm.population), int(zone_param.agent_demand_fraction*100)))
        purpose = self.dm.purpose_dict["hoo"]
        sec_dest_tours = {mode: [defaultdict(list) for _ in purpose.zone_numbers]
            for mode in purpose.modes}
        car_users = pandas.Series(
            0, self.zdata_forecast.zone_numbers[self.dm.car_use_model.bounds])
        for person in self.dm.population:
            person.decide_car_use()
            car_users[person.zone.number] += person.is_car_user
            person.add_tours(self.dm.purpose_dict, tour_probs)
            for tour in person.tours:
                tour.choose_mode(person.is_car_user)
                tour.choose_destination(sec_dest_tours)
        self.dm.car_use_model.print_results(
            car_users / self.dm.zone_population, self.dm.zone_population)
        log.info("Primary destinations assigned")
        purpose_impedance = self.imptrans.transform(
            purpose, previous_iter_impedance)
        nr_threads = param.performance_settings["number_of_processors"]
        if nr_threads == "max":
            nr_threads = multiprocessing.cpu_count()
        elif nr_threads <= 0:
            nr_threads = 1
        bounds = next(iter(purpose.sources)).bounds
        modes = purpose.modes if is_last_iteration else ["car"]
        for mode in modes:
            threads = []
            for i in range(nr_threads):
                origs = range(i, bounds.stop - bounds.start, nr_threads)
                thread = threading.Thread(
                    target=self._distribute_tours,
                    args=(
                        mode, origs, sec_dest_tours[mode],
                        purpose_impedance[mode]))
                threads.append(thread)
                thread.start()
            for thread in threads:
                thread.join()
        for purpose in self.dm.tour_purposes:
            purpose.print_data()
        for person in self.dm.population:
            for tour in person.tours:
                self.dtm.add_demand(tour)
        if is_last_iteration:
            random.seed(zone_param.population_draw)
            self.dm.predict_income()
            random.seed(None)
            fname0 = "agents"
            fname1 = "tours"
            # print person and tour attr to files
            self.resultdata.print_line("\t".join(Person.attr), fname0)
            self.resultdata.print_line("\t".join(Tour.attr), fname1)
            for person in self.dm.population:
                person.calc_income()
                self.resultdata.print_line(str(person), fname0)
                for tour in person.tours:
                    tour.calc_cost(previous_iter_impedance)
                    self.resultdata.print_line(str(tour), fname1)
            log.info("Results printed to files {} and {}".format(
                fname0, fname1))
        log.info("Demand calculation completed")

    def _distribute_tours(self, mode, origs, sec_dest_tours, impedance):
        sec_dest_purpose = self.dm.purpose_dict["hoo"]
        for orig in origs:
                dests = list(sec_dest_tours[orig])
                probs = sec_dest_purpose.calc_prob(
                    mode, impedance, orig, dests).cumsum(axis=0)
                for j, dest in enumerate(dests):
                    for tour in sec_dest_tours[orig][dest]:
                        tour.choose_secondary_destination(probs[:, j])
