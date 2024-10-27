from typing import Optional, TypeVar, Union
import pandas as pd
import numpy as np
from pathlib import Path
import utils.log as log

T = TypeVar('T', bound=Union[pd.Series, pd.DataFrame])

def avg (data: pd.Series, weights: pd.Series) -> float:
    if data.name == weights.name:
        return data.sum()
    try:
        return np.average(data, weights=weights[data.index])
    except ZeroDivisionError:
        return 0

def _find_file_with_extension(data_dir: Path, file_extension: str) -> Path:
    files = list(data_dir.glob(f"*{file_extension}"))
    if not files:
        raise NameError(f"No {file_extension} file found in folder {data_dir}")
    if len(files) > 1:
        raise NameError(f"Multiple {file_extension} files found in folder {data_dir} ({files})")
    return files[0]

def _aggregate_and_validate_indices(data: T,
                                   file_path: Path,
                                   data_dir: Path,
                                   zone_numbers: Optional[np.ndarray]) -> T:
    def _raise_if_nan_in_index(data: T, path: Path) -> None:
        if pd.api.types.is_numeric_dtype(data.index) and data.index.hasnans:
            raise IndexError(f"Row with only spaces or tabs in file {path}")

        for i in data.index:
            try:
                if np.isnan(i):
                    raise IndexError(f"Row with only spaces or tabs in file {path}")
            except TypeError:
                pass

    def _raise_if_duplicates_in_index(data: T, path: Path) -> None:
        if data.index.has_duplicates:
            raise IndexError(f"Index in file {path} has duplicates")

    def _load_mapping(map_path: Path) -> pd.Series:
        return pd.read_csv(map_path, sep='\s+').squeeze()

    def _aggregate_data(data: T, mapping: pd.Series) -> T:
        if "total" in data.columns:
            return data.groupby(mapping).agg(lambda ser: avg(ser, weights=data["total"]))
        elif "detach" in data.columns:
            funcs = dict.fromkeys(data.columns, "sum")
            funcs["detach"] = "mean"
            return data.groupby(mapping).agg(funcs)
        else:
            return data.groupby(mapping).sum()

    def _raise_if_invalid_zone_numbers(data: T,
                              zone_numbers: np.ndarray,
                              file_path: Path,
                              mapping: Optional[pd.Series] = None) -> None:
        if data.index.size == zone_numbers.size and (data.index == zone_numbers).all():
            return
        missing_zones = [i for i in data.index if int(i) not in zone_numbers]
        if missing_zones:
            raise IndexError(f"Zone number(s) {missing_zones} from file {file_path} not found in network")
        extra_zones = [i for i in zone_numbers if i not in data.index]
        if extra_zones:
            if mapping is not None:
                extra_zones = [mapping[mapping == i].index[0] if i in mapping.array else i for i in extra_zones]
            raise IndexError(f"Zone number(s) {extra_zones} not found in file {file_path}")
        raise IndexError(f"Zone numbers did not match for file {file_path}")

    if not data.index.is_monotonic_increasing:
        data = data.sort_index()
        log.warn(f"File {file_path} is not sorted in ascending order")
        
    _raise_if_nan_in_index(data, file_path)
    _raise_if_duplicates_in_index(data, file_path)
    
    if zone_numbers is not None:
        map_path = data_dir / "zone_mapping.txt"
        mapping = None
        index_file = file_path
        if map_path.is_file():
            index_file = map_path
            mapping = _load_mapping(map_path)
            data = _aggregate_data(data, mapping)
            data.index = data.index.astype(int)
        _raise_if_invalid_zone_numbers(data, zone_numbers, index_file, mapping)
    return data

def _load_data_to_df(datafile: Path) -> pd.DataFrame:
    data: pd.DataFrame = pd.read_csv(
        datafile, sep='\s+', keep_default_na=False,
        na_values='', comment='#', header='infer')
    return data

def _load_data_to_series(datafile: Path) -> pd.Series:
    data: pd.DataFrame = pd.read_csv(
        datafile, sep='\s+', keep_default_na=False,
        na_values='', comment='#', header=None)
    data = data.squeeze()
    return data

def _set_dtype(data: T, file_end: str, dtype: Optional[np.dtype]) -> T:
    if dtype is not None:
        try:
            data = data.astype(dtype=dtype, errors='raise')
        except ValueError as e:
            raise ValueError(f"Zone data file {file_end} has values not convertible to floats.") from e
    return data

def _read_csv_file_common(data_dir: Path,
                            file_end: str, 
                            zone_numbers: Optional[np.ndarray], 
                            dtype: Optional[np.dtype], 
                            loader_func) -> T:
    try:
        path = _find_file_with_extension(data_dir, file_end)
        data = loader_func(path)
        data = _aggregate_and_validate_indices(data, path, data_dir, zone_numbers)
        data = _set_dtype(data, file_end, dtype)
        return data
    except (NameError, IndexError, ValueError) as e:
        log.error(str(e)) # Log the error message to keep old behavior and rereaise the exception
        raise

def read_csv_file(data_dir: Path,
                    file_end: str, 
                    zone_numbers: Optional[np.ndarray] = None, 
                    dtype: Optional[np.dtype] = None) -> pd.DataFrame:
    """Read (zone) DataFrame from space-separated file.
    
    Parameters
    ----------
    data_dir : Path
        Directory where scenario input data files are found
    file_end : str
        Ending of the file in question (e.g., ".pop")
    zone_numbers : ndarray (optional)
        Zone numbers to compare with for validation
    dtype : data type (optional)
        Data type to cast data to

    Returns
    -------
    pandas DataFrame
    """
    return _read_csv_file_common(data_dir, file_end, zone_numbers, dtype, _load_data_to_df)

def read_csv_file_series(data_dir: Path,
                            file_end: str, 
                            zone_numbers: Optional[np.ndarray] = None,
                            dtype: Optional[np.dtype] = None) -> pd.Series:
    """Read a single Series from space-separated file.
    
    Parameters
    ----------
    data_dir : Path
        Directory where scenario input data files are found
    file_end : str
        Ending of the file in question (e.g., ".pop")
    zone_numbers : ndarray (optional)
        Zone numbers to compare with for validation
    dtype : data type (optional)
        Data type to cast data to

    Returns
    -------
    pandas Series
    """
    return _read_csv_file_common(data_dir, file_end, zone_numbers, dtype, _load_data_to_series)