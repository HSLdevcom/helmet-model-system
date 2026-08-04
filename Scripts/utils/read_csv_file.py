import os
import re
from typing import Optional
import pandas
import numpy

import utils.log as log


def read_csv_file(data_dir: str, 
                  file_end: str, 
                  zone_numbers: Optional[numpy.ndarray] = None, 
                  dtype: Optional[numpy.dtype] = None, 
                  squeeze: bool=False) -> pandas.DataFrame:
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
    header: Optional[str] = None if squeeze else "infer"
    if not squeeze:
        with open(path, encoding="utf-8") as f:
            for lineno, line in enumerate(f):
                if line.strip() and not line.lstrip().startswith("#"):
                    # Is first character of the line whitespace? 
                    has_unnamed_first_column = line[0].isspace()

                    # Works like sep=r"\s+": 
                    header_cleaned = re.split(r"\s+", line.strip())

                    if has_unnamed_first_column:
                        header_cleaned.insert(0, "zone")

                    break
            else:
                raise ValueError("File does not contain a header row")

        header = header_cleaned
        index_col = 0 if header and header[0] == "zone" else None
        data = pandas.read_csv(
            path,
            sep='\s+',
            skiprows=lineno + 1,   # ohita myös header-rivi
            names=header,
            header=None,
            comment="#",
            index_col=index_col,
            keep_default_na=False,
            na_values="",
        )
    else:
        data: pandas.DataFrame = pandas.read_csv(
            path, sep='\s+', keep_default_na=False,
            na_values="", comment='#', header=header)
    if squeeze:
        data = data.squeeze()
    log.info(str(data))
    if pandas.api.types.is_numeric_dtype(data.index) and data.index.hasnans:
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
        if not data.index.is_monotonic_increasing:
            data.sort_index(inplace=True)
            log.warn("File {} is not sorted in ascending order".format(path))
        map_path = os.path.join(data_dir, "zone_mapping.txt")
        if os.path.exists(map_path):
            log_path = map_path
            mapping = pandas.read_csv(map_path, sep='\s+').squeeze()
            if "total" in data.columns:
                # If file contains total and shares of total,
                # shares are aggregated as averages with total as weight
                data = data.groupby(mapping).agg(lambda ser: avg(ser, weights=data["total"]))
            elif "detach" in data.columns:
                funcs = dict.fromkeys(data.columns, "sum")
                funcs["detach"] = "mean"
                data = data.groupby(mapping).agg(funcs)
            else:
                data = data.groupby(mapping).sum()
            data.index = data.index.astype(int)
        else:
            log_path = path
        if data.index.size != zone_numbers.size or (data.index != zone_numbers).any():
            for i in data.index:
                if int(i) not in zone_numbers:
                    msg = "Zone number {} from file {} not found in network".format(
                        i, log_path)
                    log.error(msg)
                    raise IndexError(msg)
            for i in zone_numbers:
                if i not in data.index:
                    if log_path == map_path and i in mapping.array:
                        # If mapping is ok, then error must be in data file
                        log_path = path
                        i = mapping[mapping == i].index[0]
                    msg = "Zone number {} not found in file {}".format(i, log_path)
                    log.error(msg)
                    raise IndexError(msg)
            msg = "Zone numbers did not match for file {}".format(log_path)
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
