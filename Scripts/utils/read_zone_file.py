import os
from typing import Optional
import json
import utils.log as log 
import numpy # type: ignore

def read_zone_file(data_dir: str, 
                  file_end: str, 
                  dtype: Optional[numpy.dtype] = None):
    """Read (zone) data from space-separated file.
    
    Parameters
    ----------
    data_dir : str
        Directory where scenario input data files are found
    file_end : str
        Ending of the file in question (e.g., ".pop")
    dtype : data type (optional)
        Data type to cast data to

    Returns
    -------
    pandas DataFrame
    """

    def convert_lists_to_tuples(data):
        if isinstance(data, list):
            return tuple(convert_lists_to_tuples(item) for item in data)
        elif isinstance(data, dict):
            return {key: convert_lists_to_tuples(value) for key, value in data.items()}
        else:
            return data


    file_found = False
    for file_name in os.listdir(data_dir):
        if file_name.endswith(file_end):
            if file_found:
                msg = "Multiple {} files found in folder {}".format(
                    file_end, data_dir)
                log.error(msg)
                raise NameError(msg)
            else:
                msg = "Found zone file {}. Assuming HELMET5 zone intervals".format(file_name)
                log.debug(msg)
                path = os.path.join(data_dir, file_name)
                file_found = True
    if not file_found:
        msg = "No {} file found in folder {}, assuming HELMET4 zone intervals".format(file_end, data_dir)
        log.info(msg)
        return None
    with open(path, 'r') as f:
        file_content = f.read()
        data = json.loads(file_content)

    for key, value in data.items():
        if isinstance(value, list):
            data[key] = tuple(value)
        elif isinstance(value, dict):
            data[key] = convert_lists_to_tuples(value)

    data = convert_lists_to_tuples(data)

    return data
