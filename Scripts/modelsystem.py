import threading
import multiprocessing
import os
import numpy
import pandas

from utils.log import Log
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
import parameters


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
        self.logger = Log.get_instance()
        self.ass_model = assignment_model
        self.emme_scenarios = self.ass_model.emme_scenarios

        # Input data
        self.zdata_base = BaseZoneData(
            base_zone_data_path, assignment_model.zone_numbers)
        self.basematrices = MatrixData(base_matrices_path)
        self.zdata_forecast = ZoneData(
            zone_data_path, assignment_model.zone_numbers)

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
            self.basematrices, self.zdata_forecast, self.ass_model.zone_numbers)
        self.dtm = dt.DepartureTimeModel(
            self.ass_model.nr_zones, self.emme_scenarios)
        self.imptrans = ImpedanceTransformer()
        bounds = slice(0, self.zdata_forecast.nr_zones)
        self.cdm = CarDensityModel(self.zdata_base, self.zdata_forecast, bounds, self.resultdata)
        # TODO: Should be better defined as parameter when we don't  
        # have different transit matrices as input data. 
        # Could use this list_matrices as input validation.
        self.ass_classes = self.basematrices.list_matrices("demand", "aht")
        self.mode_share = []
        self.trucks = self.fm.calc_freight_traffic("truck")
        self.trailer_trucks = self.fm.calc_freight_traffic("trailer_truck")

    def _init_demand_model(self):
        return DemandModel(self.zdata_forecast, self.resultdata, is_agent_model=False)

    def _add_internal_demand(self, previous_iter_impedance, is_last_iteration):
        """Produce mode-specific demand matrices and add them
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

    # possibly merge with init
    def assign_base_demand(self, use_fixed_transit_cost=False):
        """Assign base demand to network (before first iteration).

        Parameters
        ----------
        use_fixed_transit_cost : bool (optional)
            If transit cost is already calculated for this scenario and is
            found in Results folder, it can be reused to save time.
        
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
        with self.basematrices.open("demand", "aht") as mtx:
            base_demand = {ass_class: mtx[ass_class] for ass_class in self.ass_classes}
        self.ass_model.assign("aht", base_demand, is_first_iteration=True)
        with self.basematrices.open("cost", "peripheral") as peripheral_mtx:
            peripheral_cost = peripheral_mtx["transit"]
            if use_fixed_transit_cost:
                self.logger.info("Using fixed transit cost matrix")
                with self.basematrices.open("cost", "aht") as aht_mtx:
                    fixed_cost = aht_mtx["transit"]
            else:
                fixed_cost = None
            for transit_class in ["transit_work", "transit_leisure"]:
                self.logger.info("Calculating transit cost for class {}".format(transit_class))
                self.ass_model.calc_transit_cost(
                    transit_class, self.zdata_forecast.transit_zone, peripheral_cost, fixed_cost)

        # Perform traffic assignment and get result impedance, 
        # for each time period
        for tp in self.emme_scenarios:
            self.logger.info("Assigning period " + tp)
            with self.basematrices.open("demand", tp) as mtx:
                for ass_class in self.ass_classes:
                    self.dtm.demand[tp][ass_class] = mtx[ass_class]
            self.ass_model.assign(
                tp, self.dtm.demand[tp], is_first_iteration=True)
            impedance[tp] = self.ass_model.get_impedance()
            if tp == "aht":
                self._update_ratios(impedance, tp)
        self.dtm.init_demand()
        return impedance

    def run_iteration(self, previous_iter_impedance, is_last_iteration=False):
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
        is_last_iteration : bool (optional)
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

        self._add_internal_demand(previous_iter_impedance, is_last_iteration)

        # Calculate external demand
        trip_sum = {}
        for mode in parameters.external_modes:
            if mode == "truck":
                int_demand = self.trucks.matrix.sum(0) + self.trucks.matrix.sum(1)
            elif mode == "trailer_truck":
                int_demand = self.trailer_trucks.matrix.sum(0) + self.trailer_trucks.matrix.sum(1)
            else:
                int_demand = self._sum_trips_per_zone(mode)
                trip_sum[mode] = int_demand.sum()
            ext_demand = self.em.calc_external(mode, int_demand)
            self.dtm.add_demand(ext_demand)
        sum_all = sum(trip_sum.values())
        # ATM, these mode shares are for car and transit
        # for the whole model area
        mode_share = {}
        for mode in trip_sum:
            mode_share[mode] = trip_sum[mode] / sum_all
        self.mode_share.append(mode_share)

        # Calculate and return traffic impedance
        for tp in self.emme_scenarios:
            self.dtm.add_vans(tp, self.zdata_forecast.nr_zones)
            self.ass_model.assign(tp, self.dtm.demand[tp], is_last_iteration)
            impedance[tp] = self.ass_model.get_impedance(is_last_iteration)

            # Car Ownership -model specific block
            if tp == "aht":
                self._update_ratios(impedance, tp)
            
            if is_last_iteration:
                # Save to .omx files
                zone_numbers = self.ass_model.zone_numbers
                with self.resultmatrices.open("demand", tp, 'w') as mtx:
                    mtx.mapping = zone_numbers
                    for ass_class in self.dtm.demand[tp]:
                        mtx[ass_class] = self.dtm.demand[tp][ass_class]
                    self.logger.info("Saved demand matrices for " + str(tp))
                for mtx_type in impedance[tp]:
                    with self.resultmatrices.open(mtx_type, tp, 'w') as mtx:
                        mtx.mapping = zone_numbers
                        for ass_class in impedance[tp][mtx_type]:
                            cost_data = impedance[tp][mtx_type][ass_class]
                            mtx[ass_class] = cost_data

        if is_last_iteration:
            self.ass_model.print_vehicle_kms(self.resultdata)

        # Reset time-period specific demand matrices (DTM), and empty result buffer
        self.dtm.init_demand()
        self.resultdata.flush()
        return impedance

    def _sum_trips_per_zone(self, mode):
        int_demand = numpy.zeros(self.zdata_base.nr_zones)
        for purpose in self.dm.tour_purposes:
            if purpose.dest != "source":
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
        nr_threads = parameters.performance_settings["number_of_processors"]
        if nr_threads == "max":
            nr_threads = multiprocessing.cpu_count()
        elif nr_threads <= 0:
            nr_threads = 1
        bounds = next(iter(purpose.sources)).bounds
        split = (bounds.stop-bounds.start) // nr_threads
        for i in xrange(0, nr_threads):
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
            TIme period (usually aht in this function).
        """ 
        car_time = numpy.ma.average(
            impedance[tp]["time"]["car_work"], axis=1,
            weights=self.dtm.demand[tp]["car_work"])
        transit_time = numpy.ma.average(
            impedance[tp]["time"]["transit_work"], axis=1,
            weights=self.dtm.demand[tp]["transit_work"])
        time_ratio = transit_time / car_time
        self.resultdata.print_data(
            time_ratio, "impedance_ratio.txt",
            self.ass_model.zone_numbers, "time")
        self.zdata_forecast["time_ratio"] = pandas.Series(
            numpy.ma.getdata(time_ratio), self.ass_model.zone_numbers)
        car_cost = numpy.ma.average(
            impedance[tp]["cost"]["car_work"], axis=1,
            weights=self.dtm.demand[tp]["car_work"])
        transit_cost = numpy.ma.average(
            impedance[tp]["cost"]["transit_work"], axis=1,
            weights=self.dtm.demand[tp]["transit_work"])
        cost_ratio = transit_cost / 44. / car_cost
        cost_ratio = cost_ratio.clip(0.01, None)
        self.resultdata.print_data(
            cost_ratio, "impedance_ratio.txt",
            self.ass_model.zone_numbers, "cost")
        self.zdata_forecast["cost_ratio"] = pandas.Series(
            numpy.ma.getdata(cost_ratio), self.ass_model.zone_numbers)


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
        self.dm.create_population()
        for purpose in self.dm.tour_purposes:
            if isinstance(purpose, SecDestPurpose):
                purpose.init_sums()
            else:
                purpose_impedance = self.imptrans.transform(purpose, previous_iter_impedance)
                if purpose.area == "peripheral" or purpose.name == "oop":
                    purpose.calc_prob(purpose_impedance)
                    purpose.gen_model.init_tours()
                    purpose.gen_model.add_tours()
                    demand = purpose.calc_demand()
                    if purpose.dest != "source":
                        for mode in demand:
                            self.dtm.add_demand(demand[mode])
                else:
                    purpose.init_sums()
                    purpose.model.calc_basic_prob(purpose_impedance)
        purpose_impedance = self.imptrans.transform(self.dm.purpose_dict["hoo"], previous_iter_impedance)
        for person in self.dm.population:
            person.add_tours(self.dm.purpose_dict)
            for tour in person.tours:
                tour.choose_mode(person.is_car_user)
                tour.choose_destination(purpose_impedance)
                if tour.mode == "car":
                    tour.choose_driver()
                self.dtm.add_demand(tour)
