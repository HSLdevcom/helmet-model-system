import os
import numpy
import pandas

class MatrixData:
    def __init__(self):
        # Here we should actually set up a link to data files
        self.base_demand = numpy.arange(25).reshape(5, 5)
    
    def get_data(self, mode):
        return self.base_demand

    def get_zone_numbers(self):
        return [5, 6, 7, 2792, 16001]

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