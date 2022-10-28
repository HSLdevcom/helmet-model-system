import numpy
import pandas

import parameters.zone as param
from utils.read_csv_file import read_csv_file
from utils.zone_interval import ZoneIntervals, zone_interval
import utils.log as log
from datatypes.zone import Zone
from assignment.datatypes.transit_fare import TransitFareZoneSpecification


class ZoneData:
    def __init__(self, data_dir, zone_numbers):
        self._values = {}
        self.share = ShareChecker(self)
        all_zone_numbers = numpy.array(zone_numbers)
        self.all_zone_numbers = all_zone_numbers
        surrounding = param.areas["surrounding"]
        peripheral = param.areas["peripheral"]
        external = param.areas["external"]
        self.zone_numbers = all_zone_numbers[:all_zone_numbers.searchsorted(
            peripheral[1], "right")]
        Zone.counter = 0
        self.zones = {number: Zone(number) for number in self.zone_numbers}
        self.first_not_helsinki_zone = self.zone_numbers.searchsorted(
            param.municipalities["Espoo"][0])
        self.first_surrounding_zone = self.zone_numbers.searchsorted(
            surrounding[0])
        first_peripheral = self.zone_numbers.searchsorted(peripheral[0])
        self.first_peripheral_zone = first_peripheral
        popdata = read_csv_file(data_dir, ".pop", self.zone_numbers, float)
        workdata = read_csv_file(data_dir, ".wrk", self.zone_numbers, float)
        schooldata = read_csv_file(data_dir, ".edu", self.zone_numbers, float)
        landdata = read_csv_file(data_dir, ".lnd", self.zone_numbers, float)
        parkdata = read_csv_file(data_dir, ".prk", self.zone_numbers, float)
        self.externalgrowth = read_csv_file(
            data_dir, ".ext",
            all_zone_numbers[all_zone_numbers.searchsorted(external[0]):],
            float)
        transit = read_csv_file(data_dir, ".tco")
        try:
            transit["fare"] = transit["fare"].astype(
                dtype=float, errors='raise')
        except ValueError:
            msg = "Zonedata file .tco has fare values not convertible to float"
            log.error(msg)
            raise ValueError(msg)
        self.transit_zone = TransitFareZoneSpecification(transit)
        try:
            cardata = read_csv_file(data_dir, ".car")
            self["parking_norm"] = cardata["prknorm"]
        except (NameError, KeyError):
            self._values["parking_norm"] = None
        car_cost = read_csv_file(data_dir, ".cco", squeeze=False)
        self.car_dist_cost = car_cost["dist_cost"][0]
        truckdata = read_csv_file(data_dir, ".trk", squeeze=True)
        self.trailers_prohibited = list(map(int, truckdata.loc[0, :]))
        self.garbage_destination = list(map(int, truckdata.loc[1, :].dropna()))
        pop = popdata["total"]
        self["population"] = pop
        self.share["share_age_7-17"] = popdata["sh_7-17"][:first_peripheral]
        self.share["share_age_18-29"] = popdata["sh_1829"][:first_peripheral]
        self.share["share_age_30-49"] = popdata["sh_3049"][:first_peripheral]
        self.share["share_age_50-64"] = popdata["sh_5064"][:first_peripheral]
        self.share["share_age_65-99"] = popdata["sh_65-"][:first_peripheral]
        self.share["share_age_7-99"] = (self["share_age_7-17"]      
                                        + self["share_age_18-29"]
                                        + self["share_age_30-49"]
                                        + self["share_age_50-64"]
                                        + self["share_age_65-99"])
        self.share["share_age_18-99"] = (self["share_age_7-99"]
                                         -self["share_age_7-17"])
        self.share["share_female"] = pandas.Series(0.5, self.zone_numbers)
        self.share["share_male"] = pandas.Series(0.5, self.zone_numbers)
        self.nr_zones = len(self.zone_numbers)
        self["population_density"] = pop / landdata["builtar"]
        wp = workdata["total"]
        self["workplaces"] = wp
        serv = workdata["sh_serv"] * wp
        self["service"] = serv
        shop = workdata["sh_shop"] * wp
        self["shops"] = shop
        self["logistics"] = workdata["sh_logi"] * wp
        self["industry"] = workdata["sh_indu"] * wp
        self["parking_cost_work"] = parkdata["parcosw"]
        self["parking_cost_errand"] = parkdata["parcose"]
        self["comprehensive_schools"] = schooldata["compreh"]
        self["secondary_schools"] = schooldata["secndry"]
        self["tertiary_education"] = schooldata["tertiary"]
        self["zone_area"] = landdata["builtar"]
        self.share["share_detached_houses"] = landdata["detach"]
        self["perc_detached_houses_sqrt"] = landdata["detach"] ** 0.5
        self["helsinki"] = self.dummy("municipalities", "Helsinki")
        self["cbd"] = self.dummy("areas", "helsinki_cbd")
        self["lauttasaari"] = self.dummy("areas", "lauttasaari")
        self["helsinki_other"] = self.dummy("areas", "helsinki_other")
        self["espoo_vant_kau"] = self.dummy("areas", "espoo_vant_kau")
        self["surrounding"] = self.dummy("areas", "surrounding")
        self["shops_cbd"] = self["cbd"] * self["shops"]
        self["shops_elsewhere"] = (1-self["cbd"]) * self["shops"]
        # Create diagonal matrix with zone area
        di = numpy.diag_indices(self.nr_zones)
        self["own_zone"] = numpy.zeros((self.nr_zones, self.nr_zones))
        self["own_zone"][di] = 1
        self["own_zone_area"] = self["own_zone"] * self["zone_area"].values
        self["own_zone_area_sqrt"] = numpy.sqrt(self["own_zone_area"])
        # Create matrix where value is 1 if origin and destination is in
        # same municipality
        home_municipality = pandas.DataFrame(
            0, self.zone_numbers, self.zone_numbers)
        intervals = ZoneIntervals("municipalities")
        for i in intervals:
            home_municipality.loc[intervals[i], intervals[i]] = 1
        self["population_own"] = home_municipality.values * pop.values
        self["population_other"] = (1-home_municipality.values) * pop.values
        self["workplaces_own"] = home_municipality.values * wp.values
        self["workplaces_other"] = (1-home_municipality.values) * wp.values
        self["service_own"] = home_municipality.values * serv.values
        self["service_other"] = (1-home_municipality.values) * serv.values
        self["shops_own"] = home_municipality.values * shop.values
        self["shops_other"] = (1-home_municipality.values) * shop.values

    def dummy(self, division_type, name, bounds=slice(None)):
        dummy = pandas.Series(0, self.zone_numbers[bounds])
        dummy.loc[zone_interval(division_type, name)] = 1
        return dummy

    def __getitem__(self, key):
        return self._values[key]

    def __setitem__(self, key, data):
        try:
            if not numpy.isfinite(data).all():
                for (i, val) in data.iteritems():
                    if not numpy.isfinite(val):
                        msg = "{} for zone {} is not a finite number".format(
                            key, i).capitalize()
                        log.error(msg)
                        raise ValueError(msg)
        except TypeError:
            for (i, val) in data.iteritems():
                try:
                    float(val)
                except ValueError:
                    msg = "{} for zone {} is not a number".format(
                        key, i).capitalize()
                    log.error(msg)
                    raise TypeError(msg)
            msg = "{} could not be read".format(key).capitalize()
            log.error(msg)
            raise TypeError(msg)
        if (data < 0).any():
            for (i, val) in data.iteritems():
                if val < 0:
                    msg = "{} ({}) for zone {} is negative".format(
                        key, val, i).capitalize()
                    log.error(msg)
                    raise ValueError(msg)
        self._values[key] = data

    def zone_index(self, zone_number):
        """Get index of given zone number.

        Parameters
        ----------
        zone_number : int
            The zone number to look up
        
        Returns
        -------
        int
            Index of zone number
        """
        return self.zones[zone_number].index

    def get_freight_data(self):
        """Get zone data for freight traffic calculation.
        
        Returns
        -------
        pandas DataFrame
            Zone data for freight traffic calculation
        """
        freight_variables = (
            "population",
            "workplaces",
            "shops",
            "logistics",
            "industry",
        )
        data = {k: self._values[k] for k in freight_variables}
        return pandas.DataFrame(data)

    def get_data(self, key, bounds, generation=False):
        """Get data of correct shape for zones included in purpose.
        
        Parameters
        ----------
        key : str
            Key describing the data (e.g., "population")
        bounds : tuple
            Two integers that describe the lower and upper bounds of purpose
        generation : bool, optional
            If set to True, returns data only for zones in purpose,
            otherwise returns data for all zones
        
        Returns
        -------
        pandas Series or numpy 2-d matrix
        """
        if self._values[key].ndim == 1: # If not a compound (i.e., matrix)
            if generation:  # Return values for purpose zones
                return self._values[key][bounds].values
            else:  # Return values for all zones
                return self._values[key].values
        else:  # Return matrix (purpose zones -> all zones)
            return self._values[key][bounds, :]


class BaseZoneData(ZoneData):
    def __init__(self, data_dir, zone_numbers):
        ZoneData.__init__(self, data_dir, zone_numbers)
        cardata = read_csv_file(data_dir, ".car", self.zone_numbers)
        self["car_density"] = cardata["cardens"]
        self["cars_per_1000"] = 1000 * self["car_density"]


class ShareChecker:
    def __init__(self, data):
        self.data = data

    def __setitem__(self, key, data):
        if (data > 1.005).any():
            for (i, val) in data.iteritems():
                if val > 1.005:
                    msg = "{} ({}) for zone {} is larger than one".format(
                        key, val, i).capitalize()
                    log.error(msg)
                    raise ValueError(msg)
        self.data[key] = data
