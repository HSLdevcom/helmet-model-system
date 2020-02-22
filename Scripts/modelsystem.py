from utils.log import Log
import assignment.departure_time as dt
from datahandling import resultdata
from datahandling.zonedata import ZoneData
from datahandling.matrixdata import MatrixData
from demand.freight import FreightModel
from demand.trips import DemandModel
from demand.external import ExternalModel
from datatypes.purpose import SecDestPurpose
from transform.impedance_transformer import ImpedanceTransformer
import parameters
import numpy
import threading
import multiprocessing


class ModelSystem:
    def __init__(self, zone_data_path, base_zone_data_path, base_matrices, ass_model, name, is_agent_model=False):
        self.logger = Log.get_instance()
        self.ass_model = ass_model
        self.zdata_base = ZoneData(base_zone_data_path, ass_model.zone_numbers)
        self.zdata_forecast = ZoneData(zone_data_path, ass_model.zone_numbers)
        self.basematrices = MatrixData(base_matrices)
        self.resultmatrices = MatrixData(name)
        self.is_agent_model = is_agent_model
        if is_agent_model:
            self.dm = DemandModel(self.zdata_forecast, is_agent_model)
            self.dm.create_population()
        else:
            self.dm = DemandModel(self.zdata_forecast)
            self.dm.create_population_segments()
        self.fm = FreightModel(self.zdata_base,
                               self.zdata_forecast,
                               self.basematrices)
        self.em = ExternalModel(self.basematrices,
                                self.zdata_forecast,
                                self.ass_model.zone_numbers)
        self.dtm = dt.DepartureTimeModel(self.ass_model.nr_zones)
        self.imptrans = ImpedanceTransformer()
        self.ass_classes = dict.fromkeys(parameters.emme_mtx["demand"].keys())
        self.mode_share = []

    def assign_base_demand(self, use_fixed_transit_cost=False):
        # TODO MON: Is this used as a "reset" or are these always calculated on init? Could be either None or this in constructor.
        self.trucks = self.fm.calc_freight_traffic("truck")
        self.trailer_trucks = self.fm.calc_freight_traffic("trailer_truck")
        impedance = {}
        # TODO MON: what is the purpose of this logical block? (1) (calc_transit_cost saves the data in emmebank, and isn't part of abstract ass)
        with self.basematrices.open("cost", "peripheral") as mtx:
            peripheral_cost = mtx["transit"]
            if use_fixed_transit_cost:
                self.logger.info("Using fixed transit cost matrix")
                # TODO MON: re-using mtx is ambiguous
                with self.basematrices.open("cost", "aht") as mtx:
                    fixed_cost = mtx["transit"]
            else:
                self.logger.info("Calculating transit cost")
                fixed_cost = None
            self.ass_model.calc_transit_cost(
                self.zdata_forecast.transit_zone, peripheral_cost,
                fixed_cost)
        # TODO MON: what is the purpose of this logical block? (2)
        for tp in parameters.emme_scenario:
            self.logger.info("Assigning period " + tp)
            # TODO MON: This could be written inside with-statement using dict comprehension, no need to init it outside
            base_demand = {}
            with self.basematrices.open("demand", tp) as mtx:
                for ass_class in self.ass_classes:
                    base_demand[ass_class] = mtx[ass_class]
            self.ass_model.assign(tp, base_demand)
            impedance[tp] = self.ass_model.get_impedance()
        return impedance

    # TODO MON: If generally speaking of iterations, would "run_iteration" make more sense? An iteration of "what"?
    def run(self, impedance, is_last_iteration=False):
        # TODO MON: what is the purpose of this logical block? "add demand required by(?) truck and trailer truck traffic to DTM"?
        # TODO MON: e.g. how does Departure Time Model affect the whole traffic assignment? It's used later in weights, but can it be briefly summed?
        self.dtm.add_demand(self.trucks)
        self.dtm.add_demand(self.trailer_trucks)
        # TODO MON: What is agent model, briefly? How does it affect a single iteration, briefly?
        if self.is_agent_model:
            for purpose in self.dm.tour_purposes:
                if isinstance(purpose, SecDestPurpose):
                    purpose.init_sums()
                else:
                    purpose_impedance = self.imptrans.transform(purpose, impedance)
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
            purpose_impedance = self.imptrans.transform(self.dm.purpose_dict["hoo"], impedance)
            for person in self.dm.population:
                person.add_tours(self.dm.purpose_dict)
                for tour in person.tours:
                    tour.choose_mode(person.is_car_user)
                    tour.choose_destination(purpose_impedance)
                    if tour.mode == "car":
                        tour.choose_driver()
                    self.dtm.add_demand(tour)
        # TODO MON: If not an agent model, what is the alternative (briefly)? How does it affect a single iteration, briefly?
        else:
            for purpose in self.dm.tour_purposes:
                if isinstance(purpose, SecDestPurpose):
                    purpose.gen_model.init_tours()
                else:
                    purpose_impedance = self.imptrans.transform(purpose, impedance)
                    purpose.calc_prob(purpose_impedance)
            self.dm.generate_tours()
            for purpose in self.dm.tour_purposes:
                if isinstance(purpose, SecDestPurpose):
                    purpose_impedance = self.imptrans.transform(purpose, impedance)
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
        # TODO MON: Was the previous block "(internal?) demand calculation and application" where as this block is "what"?
        trip_sum = {}
        for mode in parameters.external_modes:
            if mode == "truck":
                int_demand = self.trucks.matrix.sum(0) + self.trucks.matrix.sum(1)
            elif mode == "trailer_truck":
                int_demand = self.trailer_trucks.matrix.sum(0) + self.trailer_trucks.matrix.sum(1)
            else:
                nr_zones = len(self.zdata_base.zone_numbers)
                int_demand = numpy.zeros(nr_zones)
                for purpose in self.dm.tour_purposes:
                    if purpose.dest != "source":
                        if isinstance(purpose, SecDestPurpose):
                            bounds = next(iter(purpose.sources)).bounds
                        else:
                            bounds = purpose.bounds
                        int_demand[bounds] += purpose.generated_tours[mode]
                        int_demand += purpose.attracted_tours[mode]
            ext_demand = self.em.calc_external(mode, int_demand)
            trip_sum[mode] = int_demand.sum()
            self.dtm.add_demand(ext_demand)
        sum_all = sum(trip_sum.values())
        mode_share = {}
        for mode in trip_sum:
            mode_share[mode] = trip_sum[mode] / sum_all
        self.mode_share.append(mode_share)
        # TODO MON: Prev. impedance could be renamed previous_iter_impedance, so it doesn't collide with this. And this be very top (good practise).
        impedance = {}
        for tp in parameters.emme_scenario:
            self.dtm.add_vans(tp, self.zdata_forecast.nr_zones)
            self.ass_model.assign(tp, self.dtm.demand[tp], is_last_iteration)
            impedance[tp] = self.ass_model.get_impedance(is_last_iteration)
            if tp == "aht":
                # TODO MON: Visually, one operation per one line, if not very long, is preferable. If split to multi-line, then also 1-arg-per-line.
                # TODO MON: Makes it more readable since usually first thing to check is the beginning of oper, not arguments passed.
                car_time = numpy.ma.average(
                    impedance[tp]["time"]["car_work"], axis=1,
                    weights=self.dtm.demand[tp]["car_work"])
                transit_time = numpy.ma.average(
                    impedance[tp]["time"]["transit"], axis=1,
                    weights=self.dtm.demand[tp]["transit_work"])
                time_ratio = transit_time / car_time
                resultdata.print_data(
                    time_ratio, "impedance_ratio.txt",
                    self.ass_model.zone_numbers, "time")
                # TODO MON: What is the purpose of previous and next logical blocks? It's quite apparent they're separate. They're also aht specific.
                car_cost = numpy.ma.average(
                    impedance[tp]["cost"]["car_work"], axis=1,
                    weights=self.dtm.demand[tp]["car_work"])
                transit_cost = numpy.ma.average(
                    impedance[tp]["cost"]["transit"], axis=1,
                    weights=self.dtm.demand[tp]["transit_work"])
                cost_ratio = transit_cost / 44. / car_cost
                resultdata.print_data(
                    cost_ratio, "impedance_ratio.txt",
                    self.ass_model.zone_numbers, "cost")
            # TODO MON: time periods could be iterated again, to separate last-iteration specific operations to same block (instead of here and there)
            if is_last_iteration:
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
            self.ass_model.print_vehicle_kms()
        # TODO MON: If these essentially "reset" some things, could those be explicitly mentioned (e.g. what does resetting DTM affect)? Empty result?
        self.dtm.init_demand()
        resultdata.flush()
        return impedance

    def _distribute_sec_dests(self, purpose, mode, impedance):
        threads = []
        demand = []
        # TODO MON: This'd be extremely important to be an input argument, since parameters.py is tracked in version control.
        nr_threads = parameters.performance_settings["number_of_processors"]
        # TODO MON: what if nr_threads is higher than cpu_count but not explicitly "max"
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
            dtm = dt.DepartureTimeModel(self.ass_model.nr_zones)
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
