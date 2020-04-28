import os
import openmatrix as omx
import numpy
from utils.read_csv_file import read_csv_file
from contextlib import contextmanager


class MatrixData:
    def __init__(self, path):
        self.path = path
        if not os.path.exists(self.path):
            os.makedirs(self.path)
    
    @contextmanager
    def open(self, mtx_type, time_period, m='r'):
        file_name = os.path.join(self.path, mtx_type+'_'+time_period+".omx")
        mtxfile = MatrixFile(omx.open_file(file_name, m))
        yield mtxfile
        mtxfile.close()

    def list_matrices(self, mtx_type, time_period, m='r'):
        file_name = os.path.join(self.path, mtx_type+'_'+time_period+".omx")
        mtxfile = omx.open_file(file_name, m)
        names = mtxfile.list_matrices()
        mtxfile.close()
        return names

    def get_external(self, transport_mode):
        return read_csv_file(self.path, "external_"+transport_mode+".txt")


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
