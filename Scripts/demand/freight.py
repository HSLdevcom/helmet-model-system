import numpy
import pandas
import parameters

class FreightModel:
    def __init__(self, zone_data_base, zone_data_forecast, base_demand):
        self.zdata_b = zone_data_base
        self.zdata_f = zone_data_forecast
        self.base_demand = base_demand

    def calc_freight_traffic(self, mode):
        zone_data_base = self.zdata_b.get_freight_data()
        zone_data_forecast = self.zdata_f.get_freight_data()
        production_base = self.generate_trips(zone_data_base, mode)
        production_forecast = self.generate_trips(zone_data_forecast, mode)
        # Remove zero values
        base_mtx = self.base_demand.get_data("freight", mode, "vrk").clip(0.000001, None)
        production = self.calibrate(base_mtx.sum(1), #[:len(production_base)], 
                                    production_base, 
                                    production_forecast)
        zone_numbers = self.base_demand.get_zone_numbers("freight", "vrk")
        mtx = pandas.DataFrame(base_mtx, zone_numbers, zone_numbers)
        prod = pandas.Series(production, zone_numbers)
        # If forecast>5*base, destination choice is replaced by area average
        threshold = parameters.vector_calibration_threshold
        cond = production_forecast < threshold*production_base
        last1000 = zone_numbers[-1] // 1000
        for i in xrange(0, last1000):
            l = i * 1000
            u = l + 999
            sum1000 = mtx.loc[l:u].sum().values
            scaling = 1 / max(sum1000.sum(), 1)
            ave1 = sum1000 * scaling
            ave2 = ave1[:, numpy.newaxis]
            cond1 = cond.loc[l:u]
            cond2 = cond1[:, numpy.newaxis]
            prod1 = prod.loc[l:u].values
            prod2 = prod1[:, numpy.newaxis]
            mtx.loc[l:u] = numpy.where(cond2, mtx.loc[l:u], ave1*prod2)
            mtx.loc[:, l:u] = numpy.where(cond1, mtx.loc[:, l:u], ave2*prod1)
        # TODO Add external and harbour traffic!
        demand = self.fratar(production, mtx)
        if mode == "truck":
            b = parameters.garbage_generation
            garbage = ( b["population"] * zone_data_forecast["population"] 
                      + b["workplaces"] * zone_data_forecast["workplaces"])
            demand[parameters.garbage_destination] += garbage
            demand.loc[parameters.garbage_destination] += garbage
        if mode == "trailer_truck":
            demand[parameters.trailers_prohibited] = 0
            demand.loc[parameters.trailers_prohibited] = 0
        return demand.values

    def generate_trips(self, zone_data, mode):
        b = pandas.Series(parameters.trip_generation[mode])
        return (b * zone_data).sum(1) + 0.001

    def fratar(self, prod, trips, max_iter = 10):
        """Perform fratar adjustment of matrix\n
        prod = Production target as array\n
        trips = Seed trip matrix\n
        max_iter (optional) = maximum iterations, default is 10\n
        Return fratared trip matrix
        """
        #Run 2D balancing
        for _ in xrange(0, max_iter):
            colsum = trips.sum("columns")
            colsum[colsum == 0] = 1
            trips = trips.mul(prod/colsum, "index")
            rowsum = trips.sum("index")
            rowsum[rowsum == 0] = 1
            trips = trips.mul(prod/rowsum, "columns")
        return trips

    def calibrate(self, calib_base, production_base, production_forecast):
        """Calibrate a forecast according to calibrated base matrix"""
        b = calib_base
        n = production_base
        s = production_forecast
        threshold = parameters.vector_calibration_threshold
        n[n==0] = 0.000001
        return numpy.where(s < threshold*n, s * b/n, s + threshold*(b - n))
