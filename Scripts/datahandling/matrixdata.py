import os
import openmatrix as omx
import numpy
# TODO MON: Maybe move this to utils, and name more explicitly (e.g. read_csv_file or read_input_file)
from zonedata import read_file
from contextlib import contextmanager


class MatrixData:
    # TODO MON: Consider passing path as 2nd parameter, no change in practise but moving that logic to where it's init
    def __init__(self, scenario):
        script_dir = os.path.dirname(os.path.realpath(__file__))
        project_dir = os.path.join(script_dir, "..", "..")
        self.path = os.path.join(project_dir, "Matrices", scenario)
        # TODO MON: Ask is this necessary (essentially mkdir -p) for result files, or why this + open's internal check?
        if not os.path.exists(self.path):
            os.makedirs(self.path)
    
    @contextmanager
    def open(self, mtx_type, time_period, m='r'):
        # TODO MON: This construct doesn't actually prevent problems, but hides them (explain __enter__ __exit__)
        try:
            file_name = os.path.join(self.path, mtx_type+'_'+time_period+".omx")
            mtxfile = MatrixFile(omx.open_file(file_name, m))
            yield mtxfile
        finally:
            mtxfile.close()

    # TODO MON: Consider adding an explicit prefix "what mode". Mode of transportation? Or of transit?
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
