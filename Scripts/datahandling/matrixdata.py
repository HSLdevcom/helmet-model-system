import os
import openmatrix as omx
import numpy
from zonedata import read_file
from contextlib import contextmanager


class MatrixData:
    def __init__(self, scenario):
        script_dir = os.path.dirname(os.path.realpath(__file__))
        project_dir = os.path.join(script_dir, "..", "..")
        self.path = os.path.join(project_dir, "Matrices", scenario)
        if not os.path.exists(self.path):
            os.makedirs(self.path)
    
    @contextmanager
    def open(self, mtx_type, time_period, m='r'):
        try:
            file_name = os.path.join(self.path, mtx_type+'_'+time_period+".omx")
            mtxfile = MatrixFile(omx.open_file(file_name, m))
            yield mtxfile
        finally:
            mtxfile.close()

    def get_external(self, mode):
        return read_file(self.path, "external_"+mode+".txt")


class MatrixFile(object):
    def __init__(self, omx_file):
        self._file = omx_file
    
    def close(self):
        self._file.close()
    
    def __getitem__(self, mode):
        return numpy.array(self._file[mode])

    def __setitem__(self, mode, data):
        self._file[mode] = data

    @property
    def zone_numbers(self):
        return self._file.mapentries("zone_number")

    @property
    def mapping(self):
        return self._file.mapping("zone_number")

    @mapping.setter
    def mapping(self, zone_numbers):
        self._file.create_mapping("zone_number", zone_numbers)