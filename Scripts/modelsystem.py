from utils.log import Log
import datahandling.resultdata as result
import assignment.departure_time as dt
from datahandling.zonedata import ZoneData
from datahandling.matrixdata import MatrixData
from demand.freight import FreightModel
from demand.trips import DemandModel
from demand.external import ExternalModel
from datatypes.purpose import SecDestPurpose
from transform.impedance_transformer import ImpedanceTransformer
import parameters
import numpy


class ModelSystem:
    def __init__(self, zone_data_path, ass_model):
        self.logger = Log.get_instance()
        self.ass_model = ass_model
        self.zdata_base = ZoneData("2016")
        self.zdata_forecast = ZoneData(zone_data_path)
        self.basematrices = MatrixData("base")
        self.dm = DemandModel(self.zdata_forecast)
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
        self.trucks = self.fm.calc_freight_traffic("truck")
        self.trailer_trucks = self.fm.calc_freight_traffic("trailer_truck")
        impedance = {}
        for tp in parameters.emme_scenario:
            self.logger.info("Assigning period " + tp)
            base_demand = {}
            self.basematrices.open_file("demand", tp)
            for ass_class in self.ass_classes:
                base_demand[ass_class] = self.basematrices.get_data(ass_class)
            self.basematrices.close()
            self.ass_model.assign(tp, base_demand, is_first_iteration=True)
            if tp == "aht":
                self.basematrices.open_file("cost", "peripheral")
                peripheral_cost = self.basematrices.get_data("transit")
                self.basematrices.close()
                if use_fixed_transit_cost:
                    self.logger.info("Using fixed transit cost matrix")
                    self.basematrices.open_file("cost", tp)
                    fixed_cost = self.basematrices.get_data("transit")
                    self.basematrices.close()
                else:
                    self.logger.info("Calculating transit cost")
                    fixed_cost = None
                self.ass_model.calc_transit_cost(self.zdata_forecast.transit_zone,
                                                 peripheral_cost,
                                                 fixed_cost)
            impedance[tp] = self.ass_model.get_impedance()
        return impedance

    def run(self, impedance, is_last_iteration=False):
        self.dtm.add_demand(self.trucks)
        self.dtm.add_demand(self.trailer_trucks)
        for purpose in self.dm.tour_purposes:
            purpose_impedance = self.imptrans.transform(purpose, impedance)
            if isinstance(purpose, SecDestPurpose):
                l, u = next(iter(purpose.sources)).bounds
                purpose.generate_tours()
                if is_last_iteration:
                    for mode in purpose.model.dest_choice_param:
                        for i in xrange(0, u - l):
                            demand = purpose.distribute_tours(mode, purpose_impedance[mode], i)
                            self.dtm.add_demand(demand)
                else:
                    for i in xrange(0, u - l):
                        demand = purpose.distribute_tours("car", purpose_impedance["car"], i)
                        self.dtm.add_demand(demand)
            else:
                demand = purpose.calc_demand(purpose_impedance)
                if purpose.dest != "source":
                    for mode in demand:
                        self.dtm.add_demand(demand[mode])
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
                            l, u = next(iter(purpose.sources)).bounds
                        else:
                            l, u = purpose.bounds
                        int_demand[l:u] += purpose.generated_tours[mode]
                        int_demand += purpose.attracted_tours[mode]
            ext_demand = self.em.calc_external(mode, int_demand)
            trip_sum[mode] = int_demand.sum()
            self.dtm.add_demand(ext_demand)
        sum_all = sum(trip_sum.values())
        mode_share = {}
        for mode in trip_sum:
            mode_share[mode] = trip_sum[mode] / sum_all
        self.mode_share.append(mode_share)
        impedance = {}
        for tp in parameters.emme_scenario:
            self.dtm.add_vans(tp, self.zdata_forecast.nr_zones)
            self.ass_model.assign(tp, self.dtm.demand[tp], is_last_iteration)
            impedance[tp] = self.ass_model.get_impedance()
            if tp == "aht":
                car_time = numpy.ma.average(impedance[tp]["time"]["car_work"],
                                            axis=1,
                                            weights=self.dtm.demand[tp]["car_work"])
                transit_time = numpy.ma.average(impedance[tp]["time"]["transit"],
                                                axis=1,
                                                weights=self.dtm.demand[tp]["transit"])
                time_ratio = transit_time / car_time
                result.print_data(time_ratio,
                                  "impedance_ratio.txt",
                                  self.ass_model.zone_numbers,
                                  "time")
                car_cost = numpy.ma.average(impedance[tp]["cost"]["car_work"],
                                            axis=1,
                                            weights=self.dtm.demand[tp]["car_work"])
                transit_cost = numpy.ma.average(impedance[tp]["cost"]["transit"],
                                                axis=1,
                                                weights=self.dtm.demand[tp]["transit"])
                cost_ratio = transit_cost / 44 / car_cost
                result.print_data(cost_ratio,
                                  "impedance_ratio.txt",
                                  self.ass_model.zone_numbers,
                                  "cost")
        self.dtm.init_demand()
        return impedance