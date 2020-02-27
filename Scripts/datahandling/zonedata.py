import numpy
import pandas
import parameters as param
from utils.read_csv_file import read_csv_file


class ZoneData:
    CAPITAL_REGION = 0
    SURROUNDING_AREA = 1
    
    def __init__(self, data_dir, zone_numbers):
        self._values = {}
        zone_numbers = numpy.array(zone_numbers)
        surrounding = param.areas["surrounding"]
        peripheral = param.areas["peripheral"]
        external = param.areas["external"]
        first_extra = numpy.where(zone_numbers > peripheral[1])[0][0]
        idx = zone_numbers[:first_extra]
        self.zone_numbers = idx
        first_surrounding = numpy.where(idx >= surrounding[0])[0][0]
        self.first_surrounding_zone = first_surrounding
        first_peripheral = numpy.where(idx >= peripheral[0])[0][0]
        self.first_peripheral_zone = first_peripheral
        first_external = numpy.where(zone_numbers >= external[0])[0][0]
        self.first_external_zone = first_external
        external_zones = zone_numbers[first_external:]
        popdata = read_csv_file(data_dir, ".pop", self.zone_numbers)
        workdata = read_csv_file(data_dir, ".wrk", self.zone_numbers)
        schooldata = read_csv_file(data_dir, ".edu", self.zone_numbers)
        landdata = read_csv_file(data_dir, ".lnd", self.zone_numbers)
        cardata = read_csv_file(data_dir, ".car", self.zone_numbers)
        parkdata = read_csv_file(data_dir, ".prk", self.zone_numbers)
        self.externalgrowth = read_csv_file(data_dir, ".ext", external_zones)
        transit_zone = {}
        transit = read_csv_file(data_dir, ".tco")
        transit_zone["fare"] = transit["fare"].to_dict()
        transit_zone["exclusive"] = transit["exclusive"].dropna().to_dict()
        transit_zone["dist_fare"] = transit_zone["fare"].pop("dist")
        transit_zone["start_fare"] = transit_zone["fare"].pop("start")
        self.transit_zone = transit_zone
        car_cost = read_csv_file(data_dir, ".cco", squeeze=True)
        self.car_dist_cost = car_cost[0]
        truckdata = read_csv_file(data_dir, ".trk", squeeze=True)
        self.trailers_prohibited = map(int, truckdata.loc[0, :])
        self.garbage_destination = map(int, truckdata.loc[1, :].dropna())
        pop = popdata["total"]
        self["population"] = pop
        self["share_age_7-17"] = popdata["sh_7-17"][:first_peripheral]
        self["share_age_18-29"] = popdata["sh_1829"][:first_peripheral]
        self["share_age_30-49"] = popdata["sh_3049"][:first_peripheral]
        self["share_age_50-64"] = popdata["sh_5064"][:first_peripheral]
        self["share_age_65-99"] = popdata["sh_65-"][:first_peripheral]
        self["share_age_7-99"] = ( self["share_age_7-17"]        
            + self["share_age_18-29"] + self["share_age_30-49"]
            + self["share_age_50-64"] + self["share_age_65-99"])
        self["share_age_18-99"] = ( self["share_age_7-99"]
                                   -self["share_age_7-17"])
        self["share_female"] = pandas.Series(0.5, zone_numbers)
        self["share_male"] = pandas.Series(0.5, zone_numbers)
        self.nr_zones = len(self.zone_numbers)
        self["population_density"] = pop / landdata["builtar"]
        self["car_users"] = cardata["caruse"]
        self["car_density"] = cardata["cardens"]
        self["cars_per_1000"] = 1000 * self["car_density"]
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
        self["share_detached_houses"] = landdata["detach"]
        self["cbd"] = pandas.Series(0, self.zone_numbers)
        self["cbd"].loc[:param.areas["helsinki_cbd"][1]] = 1
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
        home_municipality = pandas.DataFrame(0, idx, idx)
        municipalities = param.municipality
        for municipality in municipalities:
            l = municipalities[municipality][0]
            u = municipalities[municipality][1]
            home_municipality.loc[l:u, l:u] = 1
        self["population_own"] = home_municipality.values * pop.values
        self["population_other"] = (1-home_municipality.values) * pop.values
        self["workplaces_own"] = home_municipality.values * wp.values
        self["workplaces_other"] = (1-home_municipality.values) * wp.values
        self["service_own"] = home_municipality.values * serv.values
        self["service_other"] = (1-home_municipality.values) * serv.values
        self["shops_own"] = home_municipality.values * shop.values
        self["shops_other"] = (1-home_municipality.values) * shop.values

    def __getitem__(self, key):
        return self._values[key]

    def __setitem__(self, key, data):
        try:
            if not numpy.isfinite(data).all():
                for (i, val) in data.iteritems():
                    if not numpy.isfinite(val):
                        raise ValueError("{} for zone {} is not a finite number".format(key, i).capitalize())
        except TypeError:
            for (i, val) in data.iteritems():
                try:
                    float(val)
                except ValueError:
                    raise TypeError("{} for zone {} is not a number".format(key, i).capitalize())
            raise TypeError("{} could not be read".format(key).capitalize())
        if (data < 0).any():
            for (i, val) in data.iteritems():
                if val < 0:
                    raise ValueError("{} ({}) for zone {} is negative".format(key, val, i).capitalize())
        self._values[key] = data

    def zone_index(self, zone_number):
        match = numpy.where(self.zone_numbers == zone_number)
        if len(match) == 1 and len(match[0]) == 1:
            return match[0][0]
        else:
            raise IndexError("Found several matching zone numbers {}".format(zone_number))

    def get_freight_data(self):
        """Get zone data for freight traffic calculation.
        
        Return
        ------
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

    def get_data(self, key, bounds, generation=False, part=None):
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
        part : int, optional
            0 if capital region, 1 if surrounding area
        
        Return
        ------
        pandas Series or numpy 2-d matrix
        """
        l = bounds.start
        u = bounds.stop
        if part is not None:  # Return values for partial area only
            if part == self.CAPITAL_REGION:
                u = self.first_surrounding_zone
            else:
                l = self.first_surrounding_zone
        if self._values[key].ndim == 1: # If not a compound (i.e., matrix)
            if generation:  # Return values for purpose zones
                return self._values[key][l:u].values
            else:  # Return values for all zones
                return self._values[key].values
        else:  # Return matrix (purpose zones -> all zones)
            return self._values[key][l:u, :]
