import numpy
import os
import pandas

_path = ".."
_buffer = {}

def set_path(scenario):
    script_dir = os.path.dirname(os.path.realpath(__file__))
    project_dir = os.path.join(script_dir, "..", "..")
    data_dir = os.path.join(project_dir, "Results", scenario)
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    global _path 
    _path = data_dir

def print_data(data, filename, zone_numbers, colname, bounds=None):
    filepath = os.path.join(_path, filename)
    if filename not in _buffer:
        _buffer[filename] = pandas.DataFrame(index=zone_numbers)
    if bounds is None:
        _buffer[filename][colname] = data
    else:
        _buffer[filename][colname] = 0.0
        _buffer[filename][colname][bounds[0]:bounds[1]] = data
    _buffer[filename].to_csv(path_or_buf=filepath, sep='\t', float_format="%1.3f")
    # numpy.savetxt(filepath, data, fmt="%1.3f")