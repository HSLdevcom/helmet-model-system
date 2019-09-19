import os
import numpy
import pandas
import parameters as param

class ZoneData:
    def __init__(self, scenario):
        script_dir = os.path.dirname(os.path.realpath(__file__))
        project_dir = os.path.join(script_dir, "..", "..")
        data_dir = os.path.join(project_dir, "Zone_data", scenario)
        popdata = read_file(data_dir, "population.txt")
        workdata = read_file(data_dir, "workplaces.txt")
        schooldata = read_file(data_dir, "schools.txt")
        landdata = read_file(data_dir, "land.txt")
        self.externalgrowth = read_file(data_dir, "external.txt")
        transit_zone = read_file(data_dir, "transit_cost.txt").to_dict()
        transit_zone["dist_fare"] = transit_zone["fare"].pop("dist")
        transit_zone["start_fare"] = transit_zone["fare"].pop("start")
        self.transit_zone = transit_zone
        car_cost = read_file(data_dir, "car_cost.txt", True)
        self.car_dist_cost = car_cost[0]
        truckdata = read_file(data_dir, "truck_zones.txt", True)
        self.trailers_prohibited = map(int, truckdata[0].split(','))
        self.garbage_destination = map(int, truckdata[1].split(','))
        val = {}
        pop = popdata["total"]
        val["population"] = pop
        val["share_age_7-17"] = popdata["sh_7-17"]
        val["share_age_18-29"] = popdata["sh_1829"]
        val["share_age_30-49"] = popdata["sh_3049"]
        val["share_age_50-64"] = popdata["sh_5064"]
        val["share_age_65-99"] = popdata["sh_65-"]
        self.zone_numbers = pop.index
        self.nr_zones = len(self.zone_numbers)
        val["population_density"] = pop / landdata["builtar"]
        val["car_users"] = popdata["caruse"]
        val["car_density"] = popdata["cardens"]
        wp = workdata["total"]
        val["workplaces"] = wp
        val["service"] = workdata["sh_serv"] * wp
        val["shops"] = workdata["sh_shop"] * wp
        val["logistics"] = workdata["sh_logi"] * wp
        val["industry"] = workdata["sh_indu"] * wp
        val["parking_cost_work"] = workdata["parcosw"]
        val["parking_cost_errand"] = workdata["parcose"]
        val["comprehensive_schools"] = schooldata["compreh"]
        val["secondary_schools"] = schooldata["secndry"]
        val["tertiary_education"] = schooldata["tertiary"]
        val["zone_area"] = landdata["builtar"]
        val["share_detached_houses"] = landdata["detach"]
        val["downtown"] = pandas.Series(0, self.zone_numbers)
        val["downtown"].loc[:param.areas["downtown"][1]] = 1
        val["shops_downtown"] = val["downtown"] * val["shops"]
        val["shops_elsewhere"] = (1-val["downtown"]) * val["shops"]
        # Create diagonal matrix with zone area
        di = numpy.diag_indices(self.nr_zones)
        val["own_zone_area"] = numpy.zeros((self.nr_zones, self.nr_zones))
        val["own_zone_area"][di] = val["zone_area"]
        val["own_zone_area_sqrt"] = numpy.sqrt(val["own_zone_area"])
        # Create matrix where value is 1 if origin and destination is in
        # same municipality
        idx = self.zone_numbers
        home_municipality = pandas.DataFrame(0, idx, idx)
        municipalities = param.municipality
        for municipality in municipalities:
            l = municipalities[municipality][0]
            u = municipalities[municipality][1]
            home_municipality.loc[l:u, l:u] = 1
        val["population_own"] = home_municipality.values * pop.values
        val["population_other"] = (1-home_municipality.values) * pop.values
        val["workplaces_own"] = home_municipality.values * wp.values
        val["workplaces_other"] = (1-home_municipality.values) * wp.values
        self.values = val

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
        data = {k: self.values[k] for k in freight_variables}
        return pandas.DataFrame(data)

    def get_data(self, key, purpose, generation=False, part=None):
        """Get data of correct shape for zones included in purpose.
        
        Parameters
        ----------
        key : str
            Key describing the data (e.g., "population")
        purpose : Purpose
            Purpose from which the zone bounds are taken
        generation : bool, optional
            If set to True, returns data only for zones in purpose,
            otherwise returns data for all zones
        part : int, optional
            0 if capital region, 1 if surrounding area
        
        Return
        ------
        pandas Series or numpy 2-d matrix
        """
        l, u = purpose.bounds
        k = self.zone_numbers.get_loc(param.first_surrounding_zone)
        if self.values[key].ndim == 1: # If not a compound (i.e., matrix)
            if generation:
                if part is None: # Return values for all purpose zones
                    return self.values[key][l:u]
                elif part == 0: # Return values for capital region
                    return self.values[key][l:k]
                else: # Return values for surrounding area
                    return self.values[key][k:u]
            else: # Return values for all zones
                return self.values[key]
        elif part is None: # Return matrix (purpose zones -> all zones)
            return self.values[key][l:u, :]
        elif part == 0: # Return matrix (capital region -> all zones)
            return self.values[key][:k, :]
        else: # Return matrix (surrounding area -> all zones)
            return self.values[key][k:u, :]

def read_file(data_dir, file_name, squeeze=False):
    path = os.path.join(data_dir, file_name)
    if squeeze:
        header = None
    else:
        header = "infer"
    return pandas.read_csv(filepath_or_buffer=path, 
                            delim_whitespace=True,
                            keep_default_na=False,
                            squeeze=squeeze,
                            comment='#',
                            header=header)