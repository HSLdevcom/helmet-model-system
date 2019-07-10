import os
import omx
import numpy as np
import pandas
import parameters as param

class MatrixData:
    def __init__(self, scenario):
        script_dir = os.path.dirname(os.path.realpath('__file__'))
        project_dir = os.path.join(script_dir, "..")
        self.path = os.path.join(project_dir, "Matrices", scenario)
    
    def open_file(self, mtx_type, time_period, m='r'):
        file_name = os.path.join(self.path, mtx_type+'_'+time_period+".omx")
        self.mtx_file = omx.openFile(file_name, m)
    
    def close(self):
        self.mtx_file.close()
    
    def get_data(self, mode):
        return np.array(self.mtx_file[mode])

    def get_external(self, mode):
        path = os.path.join(self.path, "external_"+mode+".csv")
        extdata = pandas.read_csv(filepath_or_buffer=path, 
                                  delim_whitespace=True)
        return extdata

    def set_data(self, data, mode):
        self.mtx_file[mode] = data

    def get_zone_numbers(self):
        # zone_numbers = mtx_file.mapentries("zone_number")
        zone_numbers = self.mtx_file.mapping("zone_number").keys()
        zone_numbers.sort()
        return zone_numbers

    def get_mapping(self):
        mapping = self.mtx_file.mapping("zone_number")
        return mapping

    def set_mapping(self, zone_numbers):
        self.mtx_file.createMapping("zone_number", zone_numbers)

class ZoneData:
    def __init__(self, scenario):
        script_dir = os.path.dirname(os.path.realpath('__file__'))
        project_dir = os.path.join(script_dir, "..")
        data_dir = os.path.join(project_dir, "Zone_data", scenario)
        path = os.path.join(data_dir, "population.csv")
        popdata = pandas.read_csv(filepath_or_buffer=path, 
                                  delim_whitespace=True)
        path = os.path.join(data_dir, "workplaces.csv")
        workdata = pandas.read_csv(filepath_or_buffer=path, 
                                   delim_whitespace=True)
        path = os.path.join(data_dir, "schools.csv")
        schooldata = pandas.read_csv(filepath_or_buffer=path, 
                                     delim_whitespace=True)
        path = os.path.join(data_dir, "area.csv")
        areadata = pandas.read_csv(filepath_or_buffer=path, 
                                   delim_whitespace=True)
        path = os.path.join(data_dir, "external.csv")
        self.externalgrowth = pandas.read_csv(filepath_or_buffer=path, 
                                              delim_whitespace=True)
        population = popdata["total"]
        self.zone_numbers = population.index
        population_density = ( popdata["total"]
                             / areadata["area"])
        car_density = popdata["car_density"]
        workplaces = workdata["total"]
        service = ( workdata["share_service"] 
                  * workdata["total"])
        shops = ( workdata["share_shops"] 
                * workdata["total"])
        logistics = ( workdata["share_logistics"] 
                    * workdata["total"])
        industry = ( workdata["share_industry"] 
                   * workdata["total"])
        parking_cost = workdata["parking_cost"]
        comprehensive_schools = schooldata["comprehensive"]
        zone_area = areadata["area"]
        share_detached_houses = areadata["share_detached_houses"]
        downtown = pandas.Series(0, self.zone_numbers)
        downtown.loc[:999] = 1
        capital_region = pandas.Series(0, self.zone_numbers)
        capital_region.loc[:5999] = 1
        shops_downtown = downtown * shops
        shops_elsewhere = (1-downtown) * shops
        # Create diagonal matrix with zone area
        nr_zones = len(zone_area)
        di = np.diag_indices(nr_zones)
        own_zone_area = np.zeros((nr_zones, nr_zones))
        own_zone_area[di] = zone_area
        own_zone_area_sqrt = np.sqrt(own_zone_area)
        # Create matrix where value is 1 if origin and destination is in
        # same municipality
        idx = self.zone_numbers
        home_municipality = pandas.DataFrame(0, idx, idx)
        municipalities = param.municipality
        for municipality in municipalities:
            l = municipalities[municipality][0]
            u = municipalities[municipality][1]
            home_municipality.loc[l:u, l:u] = 1
        population_own = home_municipality.values * population.values
        population_other = (1-home_municipality.values) * population.values
        workplaces_own = home_municipality.values * workplaces.values
        workplaces_other = (1-home_municipality.values) * workplaces.values
        self.values = {
            "population": population,
            "population_own": population_own,
            "population_other": population_other,
            "population_density": population_density,
            "car_density": car_density,
            "workplaces": workplaces,
            "workplaces_own": workplaces_own,
            "workplaces_other": workplaces_other,
            "service": service,
            "shops": shops,
            "shops_downtown": shops_downtown,
            "shops_elsewhere": shops_elsewhere,
            "logistics": logistics,
            "industry": industry,
            "parking_cost": parking_cost,
            "comprehensive_schools": comprehensive_schools,
            "zone_area": zone_area,
            "own_zone_area": own_zone_area,
            "own_zone_area_sqrt": own_zone_area_sqrt,
            "downtown": downtown,
            "share_detached_houses": share_detached_houses,
        }

    def get_freight_data(self):
        freight_variables = (
            "population",
            "workplaces",
            "shops",
            "logistics",
            "industry",
        )
        data = {k: self.values[k] for k in freight_variables}
        return pandas.DataFrame(data)

    def get_data(self, data_type, purpose, generation=False, part=None):
        l, u = self.get_bounds(purpose)
        k = self.zone_numbers.get_loc(param.first_surrounding_zone)
        if self.values[data_type].ndim == 1:
            if generation:
                if part is None:
                    return self.values[data_type][l:u]
                elif part == 0:
                    return self.values[data_type][l:k]
                else:
                    return self.values[data_type][k:u]
            else:
                return self.values[data_type]
        if part is None:
            return self.values[data_type][l:u, :]
        elif part == 0:
            return self.values[data_type][:k, :]
        else:
            return self.values[data_type][k:u, :]

    def get_bounds(self, purpose):
        if purpose.area == "metropolitan":
            l = 0
            u_label = param.first_peripheral_zone
            u = self.zone_numbers.get_loc(u_label)
        if purpose.area == "peripheral":
            l_label = param.first_peripheral_zone
            l = self.zone_numbers.get_loc(l_label)
            u = len(self.zone_numbers)
        if purpose.area == "all":
            l = 0
            u = len(self.zone_numbers)
        return l, u