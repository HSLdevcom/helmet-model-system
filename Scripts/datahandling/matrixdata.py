import os
import openmatrix as omx
import numpy
from contextlib import contextmanager

from utils.read_csv_file import read_csv_file
import parameters.assignment as param


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
    
    def check(self, ass_numbers):
        path = self._file.filename
        # TODO Get these as numpy arrays from source
        mtx_numbers = numpy.array(self.zone_numbers)
        if not (numpy.diff(mtx_numbers) > 0).all():
            raise IndexError("Zone numbers not in strictly ascending order in file {}".format(path))
        if mtx_numbers.size != ass_numbers.size or (mtx_numbers != ass_numbers).any():
            for i in mtx_numbers:
                if int(i) not in ass_numbers:
                    raise IndexError("Zone number {} from file {} not found in network".format(i, path))
            for i in ass_numbers:
                if i not in mtx_numbers:
                    raise IndexError("Zone number {} not found in file {}".format(i, path))
            raise IndexError("Zone numbers did not match for file {}".format(path))
        ass_classes = self.matrix_list
        for ass_class in param.transport_classes:
            if ass_class not in ass_classes:
                raise IndexError("File {} does not contain {} matrix.".format(
                    path, ass_class))
            a = self[ass_class]
            if a.shape[0] != mtx_numbers.size or a.shape[1] != mtx_numbers.size:
                raise IndexError("Matrix {} in file {} has wrong dimensions".format(
                    ass_class, path))

    @property
    def zone_numbers(self):
        return self._file.mapentries("zone_number")

    @property
    def mapping(self):
        return self._file.mapping("zone_number")

    @mapping.setter
    def mapping(self, zone_numbers):
        self._file.create_mapping("zone_number", zone_numbers)

    @property
    def matrix_list(self):
        return self._file.list_matrices()
