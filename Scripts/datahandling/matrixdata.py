import os
import omx
import numpy
from zonedata import read_file
from contextlib import contextmanager


class MatrixData:
    def __init__(self, scenario):
        script_dir = os.path.dirname(os.path.realpath(__file__))
        project_dir = os.path.join(script_dir, "..", "..")
        self.path = os.path.join(project_dir, "Matrices", scenario)
    
    @contextmanager
    def open(self, mtx_type, time_period, m='r'):
        try:
            file_name = os.path.join(self.path, mtx_type+'_'+time_period+".omx")
            mtxfile = MatrixFile(omx.openFile(file_name, m))
            yield mtxfile
        finally:
            mtxfile.close()

    def get_external(self, mode):
        return read_file(self.path, "external_"+mode+".txt")


class MatrixFile:
    def __init__(self, omx_file):
        self._file = omx_file
    
    def close(self):
        self._file.close()
    
    def get_data(self, mode):
        return numpy.array(self._file[mode])

    def set_data(self, data, mode):
        self._file[mode] = data

    def get_zone_numbers(self):
        # zone_numbers = mtx_file.mapentries("zone_number")
        zone_numbers = self._file.mapping("zone_number").keys()
        zone_numbers.sort()
        return zone_numbers

    def get_mapping(self):
        return self._file.mapping("zone_number")

    def set_mapping(self, zone_numbers):
        self._file.createMapping("zone_number", zone_numbers)