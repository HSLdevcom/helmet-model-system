from decimal import DivisionByZero
from itertools import groupby
import os
import pandas
import numpy

import utils.log as log


def read_csv_file(data_dir, file_end, zone_numbers=None, dtype=None, squeeze=False):
    """Read (zone) data from space-separated file.
    
    Parameters
    ----------
    data_dir : str
        Directory where scenario input data files are found
    file_end : str
        Ending of the file in question (e.g., ".pop")
    zone_numbers : ndarray (optional)
        Zone numbers to compare with for validation
    dtype : data type (optional)
        Data type to cast data to
    squeeze : bool (optional)
        If the parsed data only contains one column and no header

    Returns
    -------
    pandas DataFrame
    """
    file_found = False
    for file_name in os.listdir(data_dir):
        if file_name.endswith(file_end):
            if file_found:
                msg = "Multiple {} files found in folder {}".format(
                    file_end, data_dir)
                log.error(msg)
                raise NameError(msg)
            else:
                path = os.path.join(data_dir, file_name)
                file_found = True
    if not file_found:
        msg = "No {} file found in folder {}".format(file_end, data_dir)
        # This error should not be logged, as it is sometimes excepted
        raise NameError(msg)
    header = None if squeeze else "infer"
    data = pandas.read_csv(
        path, delim_whitespace=True, squeeze=squeeze, keep_default_na=False,
        na_values="", comment='#', header=header)
    if data.index.is_numeric() and data.index.hasnans:
        msg = "Row with only spaces or tabs in file {}".format(path)
        log.error(msg)
        raise IndexError(msg)
    else:
        for i in data.index:
            try:
                if numpy.isnan(i):
                    msg = "Row with only spaces or tabs in file {}".format(path)
                    log.error(msg)
                    raise IndexError(msg)
            except TypeError:
                # Text indices are ok and should not raise an exception
                pass
    if data.index.has_duplicates:
        raise IndexError("Index in file {} has duplicates".format(path))
    if zone_numbers is not None:
        map_path = os.path.join(data_dir, "zone_mapping.txt")
        if os.path.exists(map_path):
            mapping = pandas.read_csv(map_path, delim_whitespace=True).squeeze()
            if "total" in data.columns:
                # If file contains total and shares of total,
                # shares are aggregated as averages with total as weight
                data = data.groupby(mapping).agg(avg, weights=data["total"])
            elif "detach" in data.columns:
                funcs = dict.fromkeys(data.columns, "sum")
                funcs["detach"] = "mean"
                data = data.groupby(mapping).agg(funcs)
            else:
                data = data.groupby(mapping).sum()
            data.index = data.index.astype(int)
        if not data.index.is_monotonic:
            data.sort_index(inplace=True)
            log.warn("File {} is not sorted in ascending order".format(path))
        if data.index.size != zone_numbers.size or (data.index != zone_numbers).any():
            for i in data.index:
                if int(i) not in zone_numbers:
                    msg = "Zone number {} from file {} not found in network".format(
                        i, path)
                    log.error(msg)
                    raise IndexError(msg)
            for i in zone_numbers:
                if i not in data.index:
                    msg = "Zone number {} not found in file {}".format(i, path)
                    log.error(msg)
                    raise IndexError(msg)
            msg = "Zone numbers did not match for file {}".format(path)
            log.error(msg)
            raise IndexError(msg)
    if dtype is not None:
        try:
            data = data.astype(dtype=dtype, errors='raise')
        except ValueError:
            msg = "Zone data file {} has values not convertible to floats.".format(
                file_end)
            log.error(msg)
            raise ValueError(msg)
    return data

def avg (data, weights):
    if data.name == weights.name:
        return sum(data)
    try:
        return numpy.average(data, weights=weights[data.index])
    except ZeroDivisionError:
        return 0
