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
        base_mtx = self.base_demand.get_data(mode).clip(0.000001, None) 
        production = self.calibrate(base_mtx.sum(1), #[:len(production_base)], 
                                    production_base, 
                                    production_forecast)
        # # External demand is generated for the last centroids
        # external_base = production_calib[len(production):]
        # external_growth = 1.1
        # external_production = external_growth * external_base
        # production = numpy.append(production, external_production)
        zone_numbers = self.base_demand.get_zone_numbers()
        pd_mtx = pandas.DataFrame(base_mtx, zone_numbers, zone_numbers)
        ave1000 = pandas.DataFrame(1, zone_numbers, zone_numbers)
        for i in xrange(0, 30):
            l = i * 1000
            u = l + 999
            sum1000 = pd_mtx.loc[l:u].sum()
            scaling = 1 / max(sum1000.sum(), 1)
            ave1000.loc[l:u] = ave1000.loc[l:u] * sum1000 * scaling
        # If forecast>5*base, destination choice is replaced by area average
        cond = production_forecast < 5*production_base
        base_mtx = numpy.where(cond, base_mtx, ave1000*production)
        # The same check is done also for other axis
        cond1 = cond.values[:, numpy.newaxis]
        prod1 = production[:, numpy.newaxis]
        ave1000T = ave1000.values.T
        base_mtx = numpy.where(cond1, base_mtx, ave1000T*prod1)
        # TODO Add harbour traffic!
        demand = self.fratar(production, base_mtx)
        return demand

    def generate_trips(self, zone_data, mode):
        b = pandas.Series(parameters.trip_generation[mode])
        trucks = (b * zone_data).sum(1) + 0.001
        if mode == "truck":
            garbage = ( 0.000125 * zone_data["population"] 
                      + 0.000025 * zone_data["workplaces"])
            trucks += garbage
            garbage_destination = 2792
            trucks[garbage_destination] += garbage.sum()
        return trucks

    def fratar(self, prod, trips, max_iter = 10):
        """Perform fratar adjustment of matrix
        prod = Production target as array
        trips = Seed trip matrix
        max_iter (optional) = maximum iterations, default is 10
        Return fratared trip matrix
        """
        #Run 2D balancing
        for _ in xrange(0, max_iter):
            origfac = prod / trips.sum(1)
            trips = trips * origfac[:, numpy.newaxis]
            destfac = prod / trips.sum(0)
            trips = trips * destfac
        return trips

    def calibrate(self, b, n, s):
        """Calibrate a vector\n
        b = true value for base\n
        n = forecast for base\n
        s = forecast to calibrate\n
        """
        return numpy.where(s < 5*n, s * b/n, s + 5*(b - n))
