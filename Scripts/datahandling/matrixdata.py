import os
import omx
import numpy
from zonedata import read_file

class MatrixData:
    def __init__(self, scenario):
        script_dir = os.path.dirname(os.path.realpath(__file__))
        project_dir = os.path.join(script_dir, "..", "..")
        self.path = os.path.join(project_dir, "Matrices", scenario)
    
    def open_file(self, mtx_type, time_period, m='r'):
        file_name = os.path.join(self.path, mtx_type+'_'+time_period+".omx")
        self.mtx_file = omx.openFile(file_name, m)
    
    def close(self):
        self.mtx_file.close()
    
    def get_data(self, mode):
        return numpy.array(self.mtx_file[mode])

    def get_external(self, mode):
        return read_file(self.path, "external_"+mode+".csv")

    def set_data(self, data, mode):
        self.mtx_file[mode] = data

    def get_zone_numbers(self):
        # zone_numbers = mtx_file.mapentries("zone_number")
        zone_numbers = self.mtx_file.mapping("zone_number").keys()
        zone_numbers.sort()
        return zone_numbers

    def get_mapping(self):
        return self.mtx_file.mapping("zone_number")

    def set_mapping(self, zone_numbers):
        self.mtx_file.createMapping("zone_number", zone_numbers)