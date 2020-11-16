import os
import openmatrix as omx
import numpy
import pandas
from contextlib import contextmanager

from utils.read_csv_file import read_csv_file
import parameters.assignment as param


class MatrixData:
    def __init__(self, path):
        self.path = path
        if not os.path.exists(self.path):
            os.makedirs(self.path)
    
    @contextmanager
    def open(self, mtx_type, time_period, zone_numbers=None, m='r'):
        file_name = os.path.join(self.path, mtx_type+'_'+time_period+".omx")
        mtxfile = MatrixFile(omx.open_file(file_name, m), zone_numbers)
        yield mtxfile
        mtxfile.close()

    def get_external(self, transport_mode):
        return read_csv_file(self.path, "external_"+transport_mode+".txt")


class MatrixFile(object):
    def __init__(self, omx_file, zone_numbers):
        self._file = omx_file
        self.missing_zones = []
        if zone_numbers is None:
            pass
        elif omx_file.mode == 'r':
            path = omx_file.filename
            mtx_numbers = self.zone_numbers
            if (numpy.diff(mtx_numbers) <= 0).any():
                raise IndexError("Zone numbers not in strictly ascending order in file {}".format(path))
            if mtx_numbers.size != zone_numbers.size or (mtx_numbers != zone_numbers).any():
                for i in mtx_numbers:
                    if i not in zone_numbers:
                        raise IndexError("Zone number {} from file {} not found in network".format(i, path))
                for i in zone_numbers:
                    if i not in mtx_numbers:
                        self.missing_zones.append(i)
                # TODO Print warning
                self.new_zone_numbers = zone_numbers
            ass_classes = self.matrix_list
            transport_classes = (("truck", "trailer_truck") 
                                 if "freight" in path
                                 else param.transport_classes)
            for ass_class in transport_classes:
                if ass_class not in ass_classes:
                    raise IndexError("File {} does not contain {} matrix.".format(
                        path, ass_class))
        else:
            self.mapping = zone_numbers
    
    def close(self):
        self._file.close()
    
    def __getitem__(self, mode):
        mtx = numpy.array(self._file[mode])
        nr_zones = self.zone_numbers.size
        if mtx.shape[0] != nr_zones or mtx.shape[1] != nr_zones:
            raise IndexError("Matrix {} in file {} dimensions {}x{}, should be {}x{}".format(
                mode, self._file.filename, mtx.shape[0], mtx.shape[1], nr_zones, nr_zones))
        if numpy.isnan(mtx).any():
            raise ValueError("Matrix {} in file {} contains NA values".format(
                mode, self._file.filename))
        if (mtx < 0).any():
            raise ValueError("Matrix {} in file {} contains negative values".format(
                mode, self._file.filename))
        if self.missing_zones:
            mtx = pandas.DataFrame(mtx, self.zone_numbers)
            mtx.reindex(
                index=self.new_zone_numbers, columns=self.new_zone_numbers,
                fill_value=0)
            mtx = mtx.values
        return mtx

    def __setitem__(self, mode, data):
        self._file[mode] = data

    @property
    def zone_numbers(self):
        return numpy.array(self._file.mapentries("zone_number"))

    @property
    def mapping(self):
        return self._file.mapping("zone_number")

    @mapping.setter
    def mapping(self, zone_numbers):
        self._file.create_mapping("zone_number", zone_numbers)

    @property
    def matrix_list(self):
        return self._file.list_matrices()
