from pathlib import Path
import threading
import multiprocessing
import os
from typing import Any, Dict, List, Union, cast
import numpy
import numpy.typing as npt
import pandas
import random
from collections import defaultdict
from assignment.abstract_assignment import AssignmentModel
from assignment.emme_assignment import EmmeAssignmentModel
from assignment.mock_assignment import MockAssignmentModel
from dataclasses import asdict

import utils.log as log
from utils.zone_interval import ArrayAggregator
import assignment.departure_time as dt
from datahandling.resultdata import ResultsData
from datahandling.zonedata import ZoneData, BaseZoneData
from datahandling.matrixdata import MatrixData
from demand.freight_internal import FreightModel
from demand.personal_internal import DemandModel
from demand.all_external import ExternalModel
from datatypes.purpose import SecDestPurpose
from datatypes.person import Person
from datatypes.tour import Tour
from datatypes.literals import TimePeriod
from transform.impedance_transformer import ImpedanceTransformer
from models.linear import CarDensityModel
from events.event_handler import EventHandler
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

    def __init__(self, 
                 zone_data_path: str, 
                 base_zone_data_path: str, 
                 base_matrices_path: str,
                 results_path: str, 
                 assignment_model: AssignmentModel, 
                 name: str,
                 event_handler: EventHandler,
                 estimation_data_path: Path | None = None):
        self.event_handler = event_handler

        self.event_handler.on_model_system_initialized(self,
                                                zone_data_path, 
                                                base_zone_data_path, 
                                                base_matrices_path,
                                                results_path, 
                                                assignment_model, 
                                                name)

        self.ass_model = cast(Union[MockAssignmentModel,EmmeAssignmentModel], assignment_model) #type checker hint
        self.zone_numbers: list = self.ass_model.zone_numbers
        self.travel_modes: Dict[str, bool] = {}  # Dict instead of set, to preserve order

        # Input data
        self.zdata_base = BaseZoneData(
            base_zone_data_path, self.zone_numbers, event_handler)
        self.basematrices = MatrixData(base_matrices_path)
        self.zdata_forecast = ZoneData(
            zone_data_path, self.zone_numbers, event_handler)

        if estimation_data_path:
            self.zdata_base.export_data(estimation_data_path / 'zonedata_base.csv')
            self.zdata_forecast.export_data(estimation_data_path / 'zonedata_forecast.csv')
        self.event_handler.on_zone_data_loaded(self.zdata_base, self.zdata_forecast)
        
        # Output data
        self.resultmatrices = MatrixData(
            os.path.join(results_path, name, "Matrices"))
        self.resultdata = ResultsData(os.path.join(results_path, name))

        self.dm = self._init_demand_model()
        self.fm = FreightModel(
            self.zdata_base, self.zdata_forecast, self.basematrices, self.event_handler)
        self.em = ExternalModel(
            self.basematrices, self.zdata_forecast, self.zone_numbers)
        self.dtm = dt.DepartureTimeModel(
            self.ass_model.nr_zones, self.ass_model.time_periods)

        #init Impedance transformers
        self.imptrans = ImpedanceTransformer(self.event_handler,
                                             extra_transformers=[],
                                             export_path=estimation_data_path)
        
        bounds = slice(0, self.zdata_forecast.nr_zones)
        self.cdm = CarDensityModel(
            self.zdata_base, self.zdata_forecast, bounds, self.resultdata)
        self.mode_share: List[Dict[str,Any]] = []
        self.convergence = []
        self.trucks = self.fm.calc_freight_traffic("truck")
        self.trailer_trucks = self.fm.calc_freight_traffic("trailer_truck")

    def _init_demand_model(self):
        return DemandModel(self.zdata_forecast, self.resultdata, is_agent_model=False)

    def _add_internal_demand(self, previous_iter_impedance: Dict[TimePeriod, Dict[str, Dict[str, npt.NDArray]]], is_last_iteration, estimation_mode=False):
        """Produce mode-specific demand matrices.

        Add them for each time-period to container in departure time model.

        Parameters
        ----------
        previous_iter_impedance : dict
            key : str
                TimePeriod
            value : dict
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
        saved_pnr_impedance = {}
        self.event_handler.on_population_segments_created(self.dm)
        for purpose in self.dm.tour_purposes:
            if isinstance(purpose, SecDestPurpose):
                purpose.gen_model.init_tours()
            else:
                purpose_impedance = self.imptrans.transform(
                    purpose, previous_iter_impedance)
                if purpose.park_and_ride_model is not None:
                    saved_pnr_impedance[purpose.name] = purpose_impedance
                    purpose.park_and_ride_model.set_impedance(previous_iter_impedance)
                purpose.calc_prob(purpose_impedance)
                if is_last_iteration and purpose.name not in ("sop", "hh"):
                    self.event_handler.on_calc_accessibility(purpose_impedance, purpose.accessibility_model)
        
        # Tour generation
        self.dm.generate_tours()
        self.event_handler.on_demand_model_tours_generated(self.dm)
        
        # Assigning of tours to mode, destination and time period
        for purpose in self.dm.tour_purposes:
            pnr_it = 0 #park and ride iteration
            if isinstance(purpose, SecDestPurpose): #hoo
                purpose_impedance = self.imptrans.transform(
                    purpose, previous_iter_impedance)
                purpose.generate_tours()
                if param.always_congested or is_last_iteration:
                    for mode in purpose.model.dest_choice_param:
                        self._distribute_sec_dests(
                            purpose, mode, purpose_impedance)
                else:
                    self._distribute_sec_dests(
                        purpose, "car", purpose_impedance)
            else: #hw-hh, hwp-oop
                if purpose.name != "wh":
                    demand = purpose.calc_demand(estimation_mode)
                    if purpose.park_and_ride_model is not None:
                        # Apply penalty for overcrowded park and ride facilities.
                        MAX_PNR_ITERATIONS = 5 # Maximum number of iterations. Set to 0 for no penalty
                        for pnr_it in range(MAX_PNR_ITERATIONS):
                            self.event_handler.on_purpose_demand_calculated(purpose, demand, pnr_iteration = pnr_it, estimation_mode=estimation_mode)
                            modified = purpose.park_and_ride_model.apply_crowding_penalty()
                            purpose.calc_prob(saved_pnr_impedance[purpose.name])
                            demand = purpose.calc_demand(estimation_mode=estimation_mode, add_sec_dest=False, pnr_iteration=pnr_it+1)
                            log.debug(f"Park and ride crowding penalty iteration {pnr_it+1} modified {modified} facilities.")
                            if modified < 1:                                
                                break
                        pnr_it += 1
                        log.debug("Park and ride demand calculation completed.")
                if purpose.dest != "source":
                    for mode in demand:
                        self.dtm.add_demand(demand[mode])
                        self.travel_modes[mode] = True
            self.event_handler.on_purpose_demand_calculated(purpose, demand, pnr_iteration = pnr_it, estimation_mode=estimation_mode)

    # possibly merge with init
    def assign_base_demand(self, 
                           use_fixed_transit_cost: bool = False, 
                           is_end_assignment: bool = False) -> Dict[TimePeriod, Dict[str, Dict[str, npt.NDArray]]]:
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
                Time period (aht, pt, iht)
            value : dict
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
            log.info("Assigning base demand for period {}...".format(tp))
            with demand.open("demand", tp, self.ass_model.zone_numbers) as mtx:
                for ass_class in param.transport_classes:
                    self.dtm.demand[tp][ass_class] = mtx[ass_class]
            impedance[tp] = ap.assign(
                self.dtm.demand[tp],
                iteration=("last" if is_end_assignment else 0))
            if tp == time_periods[0]:
                time_ratios, cost_ratios = self._update_ratios(impedance[tp], tp)
                self.event_handler.on_ratios_updated(time_ratios, cost_ratios)
            if is_end_assignment:
                self._save_to_omx(impedance[tp], tp)
        if is_end_assignment:
            self.ass_model.aggregate_results(self.resultdata)
            self._calculate_noise_areas()
            self.resultdata.flush()
        self.dtm.init_demand_and_get_gaps()
        self.event_handler.on_base_demand_assigned(impedance)
        return impedance

    def run_iteration(self,
                      previous_iter_impedance: Dict[TimePeriod, Dict[str, Dict[str, npt.NDArray]]],
                      iteration: Union[int, str],
                      estimation_mode=False):
        """Calculate demand and assign to network.

        Parameters
        ----------
        previous_iter_impedance : dict
            key : TimePeriod
            value : dict
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
        self.event_handler.on_iteration_started(iteration, previous_iter_impedance)
        impedance = {}

        # Add truck and trailer truck demand, to time-period specific
        # matrices (DTM), used in traffic assignment
        self.dtm.add_demand(self.trucks)
        self.dtm.add_demand(self.trailer_trucks)

        # Update car density
        prediction = self.cdm.predict()
        self.zdata_forecast["car_density"] = prediction
        self.zdata_forecast["cars_per_1000"] = 1000 * prediction
        self.event_handler.on_car_density_updated(iteration, prediction, self.cdm)

        # Calculate internal demand
        self._add_internal_demand(previous_iter_impedance, iteration=="last", estimation_mode)
        self.event_handler.on_internal_demand_added(self.dtm)

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
            self.event_handler.on_external_demand_calculated({mode: ext_demand})
            self.dtm.add_demand(ext_demand)
        
        # Add vans and save demand matrices
        for ap in self.ass_model.assignment_periods:
            self.dtm.add_vans(ap.name, self.zdata_forecast.nr_zones)
        log.info("Demand matrices saved")
        self.event_handler.on_demand_calculated(iteration, self.dtm)

        # Calculate and return traffic impedance
        for ap in self.ass_model.assignment_periods:
            tp = ap.name
            log.info("Assigning period " + tp)
            impedance[tp] = ap.assign(self.dtm.demand[tp], iteration)
            self.event_handler.on_time_period_assigned(iteration, ap, impedance[tp], tp, previous_iter_impedance)
            if tp == "aht":
                time_ratios, cost_ratios = self._update_ratios(impedance[tp], tp)
                self.event_handler.on_ratios_updated(time_ratios, cost_ratios)

        if iteration=="last":
            self.ass_model.aggregate_results(self.resultdata)

        # Reset time-period specific demand matrices (DTM),
        # and empty result buffer
        gap = self.dtm.init_demand_and_get_gaps() 
        self.convergence.append(gap)      
        self.event_handler.on_iteration_complete(iteration, impedance, gap)
        self.resultdata.flush()
        return impedance

    def _sum_trips_per_zone(self, mode, include_dests=True):
        int_demand = pandas.Series(0.0, self.zdata_base.zone_numbers)
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
        elif int(nr_threads) <= 0:
            nr_threads = 1
        else:
            nr_threads = int(nr_threads)
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

    def _distribute_tours(self, container, purpose, mode, impedance, origs):
        for orig in origs:
            demand = purpose.distribute_tours(mode, impedance[mode], orig)
            container.add_demand(demand)

    def _update_ratios(self, impedance, tp: TimePeriod):
        """Calculate time and cost ratios.
        
        Parameters
        ----------
        impedance : dict
            Impedance matrices.
        tp : str
            Time period ["aht", "pt", "iht"] (usually aht in this function).
        """ 
        car_time = numpy.ma.average(
            impedance["time"]["car_work"], axis=1,
            weights=self.dtm.demand[tp]["car_work"])
        transit_time = numpy.ma.average(
            impedance["time"]["transit_work"], axis=1,
            weights=self.dtm.demand[tp]["transit_work"])
        time_ratio = transit_time / car_time
        time_ratio = time_ratio.clip(0.01, None)

        self.zdata_forecast["time_ratio"] = pandas.Series(
            numpy.ma.getdata(time_ratio), self.zone_numbers)
        car_cost = numpy.ma.average(
            impedance["cost"]["car_work"], axis=1,
            weights=self.dtm.demand[tp]["car_work"])
        dist_cost = self.zdata_forecast.car_dist_cost
        car_cost += dist_cost * numpy.ma.average(
            impedance["dist"]["car_work"], axis=1,
            weights=self.dtm.demand[tp]["car_work"])
        transit_cost = numpy.ma.average(
            impedance["cost"]["transit_work"], axis=1,
            weights=self.dtm.demand[tp]["transit_work"])
        cost_ratio = transit_cost / 44. / car_cost
        cost_ratio = cost_ratio.clip(0.01, None)
        self.zdata_forecast["cost_ratio"] = pandas.Series(
            numpy.ma.getdata(cost_ratio), self.zone_numbers)
        
        return time_ratio, cost_ratio



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

    def _add_internal_demand(self, previous_iter_impedance, is_last_iteration, estimation_mode=False):
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
        saved_pnr_impedance = {}
        for purpose in self.dm.tour_purposes:
            if isinstance(purpose, SecDestPurpose):
                purpose.init_sums()
            else:
                purpose_impedance = self.imptrans.transform(
                    purpose, previous_iter_impedance)
                if purpose.park_and_ride_model is not None:
                    saved_pnr_impedance[purpose.name] = purpose_impedance
                    purpose.park_and_ride_model.set_impedance(previous_iter_impedance)

                if (purpose.area == "peripheral" or purpose.dest == "source"
                        or purpose.name in ["oop","hh"]):
                    purpose.calc_prob(purpose_impedance)
                    purpose.gen_model.init_tours()
                    purpose.gen_model.add_tours()
                    demand = purpose.calc_demand(estimation_mode)
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
                    self.event_handler.on_calc_accessibility(purpose_impedance, purpose.accessibility_model)
        tour_probs = self.dm.generate_tour_probs()
        log.info("Assigning mode and destination for {} agents ({} % of total population)".format(
            len(self.dm.population), int(zone_param.agent_demand_fraction*100)))
        purpose = self.dm.purpose_dict["hoo"]
        sec_dest_tours = {mode: [defaultdict(list) for _ in purpose.zone_numbers]
            for mode in purpose.modes}
        for person in self.dm.population:
            person.decide_car_use()
            person.add_tours(self.dm.purpose_dict, tour_probs)
            for tour in person.tours:
                tour.choose_mode(person.is_car_user)
                tour.choose_destination(sec_dest_tours)
        self.event_handler.on_population_segments_created(self.dm)
        log.info("Primary destinations assigned")
        purpose_impedance = self.imptrans.transform(
            purpose, previous_iter_impedance)
        nr_threads = param.performance_settings["number_of_processors"]
        if nr_threads == "max":
            nr_threads = multiprocessing.cpu_count()
        elif int(nr_threads) <= 0:
            nr_threads = 1
        else:
            nr_threads = int(nr_threads)
        bounds = next(iter(purpose.sources)).bounds
        modes = purpose.modes if param.always_congested or is_last_iteration else ["car"]
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
            #None for demand, because agent-based models work differently
            self.event_handler.on_purpose_demand_calculated(purpose, None, estimation_mode=estimation_mode) 
            #Park and ride
            if purpose.park_and_ride_model is not None:
                # Apply penalty for overcrowded park and ride facilities.
                MAX_PNR_ITERATIONS = 5 # Maximum number of iterations. Set to 0 for no penalty
                for i in range(MAX_PNR_ITERATIONS):
                    modified = purpose.park_and_ride_model.apply_crowding_penalty()
                    purpose.calc_basic_prob(saved_pnr_impedance[purpose.name])
                    demand = purpose.calc_pnr_demand(self.dm.population,estimation_mode=estimation_mode, log=log)
                    log.debug(f"Park and ride crowding penalty iteration {i+1} modified {modified} facilities.")
                    if modified < 1:                                
                        break
                log.debug("Park and ride demand calculation completed.")
        #Add park and ride to time periods
        self.dtm.add_demand(demand["pnr_car"])
        self.dtm.add_demand(demand["pnr_transit"])
        #Add all tours to time periods
        for person in self.dm.population:
            for tour in person.tours:
                self.dtm.add_demand(tour)
        if is_last_iteration:
            self.event_handler.on_agent_model_results_calculated(previous_iter_impedance)
        log.info("Demand calculation completed")

    def _distribute_tours(self, mode, origs, sec_dest_tours, impedance):
        sec_dest_purpose = self.dm.purpose_dict["hoo"]
        for orig in origs:
            dests = list(sec_dest_tours[orig])
            if type(sec_dest_purpose) == SecDestPurpose:
                probs = sec_dest_purpose.calc_prob(
                    mode, impedance, orig, dests).cumsum(axis=0)
                for j, dest in enumerate(dests):
                    for tour in sec_dest_tours[orig][dest]:
                        tour.choose_secondary_destination(probs[:, j])
