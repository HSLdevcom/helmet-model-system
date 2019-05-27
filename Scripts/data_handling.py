import os
import omx
import numpy
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
        return numpy.array(self.mtx_file[mode])

    def set_data(self, data, mode):
        self.mtx_file[mode] = data

    def get_zone_numbers(self):
        # zone_numbers = mtx_file.mapentries("zone_number")
        zone_numbers = self.mtx_file.mapping("zone_number").keys()
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
        population = popdata["total"]
        workplaces = workdata["total"]
        shops = ( workdata["share_shops"] 
                * workdata["total"])
        logistics = ( workdata["share_logistics"] 
                    * workdata["total"])
        industry = ( workdata["share_industry"] 
                   * workdata["total"])
        self.values = {
            "population": population,
            "workplaces": workplaces,
            "shops": shops,
            "logistics": logistics,
            "industry": industry,
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