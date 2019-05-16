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
    
    def get_data(self, mtx_type, mode, time_period):
        file_name = os.path.join(self.path, mtx_type+'_'+time_period+".omx")
        mtx_file = omx.openFile(file_name)
        mtx = numpy.array(mtx_file[mode])
        mtx_file.close()
        return mtx

    def get_zone_numbers(self, mtx_type, time_period):
        file_name = os.path.join(self.path, mtx_type+'_'+time_period+".omx")
        mtx_file = omx.openFile(file_name)
        # zone_numbers = mtx_file.mapentries("zone_number")
        zone_numbers = mtx_file.mapping("zone_number").keys()
        mtx_file.close()
        return zone_numbers

    def get_mapping(self, mtx_type, time_period):
        file_name = os.path.join(self.path, mtx_type+'_'+time_period+".omx")
        mtx_file = omx.openFile(file_name)
        mapping = mtx_file.mapping("zone_number")
        mtx_file.close()
        return mapping

class ZoneData:
    def __init__(self, scenario):
        script_dir = os.path.dirname(os.path.realpath('__file__'))
        project_dir = os.path.join(script_dir, "..")
        data_dir = os.path.join(project_dir, "Zone_data", scenario)
        path = os.path.join(data_dir, "population.csv")
        self.population = pandas.read_csv(filepath_or_buffer=path, 
                                          delim_whitespace=True)
        path = os.path.join(data_dir, "workplaces.csv")
        self.workplaces = pandas.read_csv(filepath_or_buffer=path, 
                                          delim_whitespace=True)

    def get_freight_data(self):
        data = {}
        data["population"] = self.population["total"]
        data["workplaces"] = self.workplaces["total"]
        data["shops"] = ( self.workplaces["share_shops"] 
                        * self.workplaces["total"])
        data["logistics"] = ( self.workplaces["share_logistics"] 
                        * self.workplaces["total"])
        data["industry"] = ( self.workplaces["share_industry"] 
                        * self.workplaces["total"])
        return pandas.DataFrame(data)