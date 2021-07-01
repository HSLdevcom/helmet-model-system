import numpy

import parameters.tour_generation as param


def fratar(target_vect, trips, max_iter=10):
    """Perform fratar adjustment of matrix.

    Parameters
    ----------
    target_vect : numpy/pandas array
        Production/attraction target
    trips : pandas DataFrame
        Seed trip matrix
    max_iter (optional) : int
        Maximum iterations, default is 10
    
    Returns
    -------
    pandas DataFrame 
        Fratared trip matrix
    """
    # Run 2D balancing
    for _ in range(0, max_iter):
        colsum = trips.sum("columns")
        colsum[colsum == 0] = 1
        trips = trips.mul(target_vect/colsum, "index")
        rowsum = trips.sum("index")
        rowsum[rowsum == 0] = 1
        trips = trips.mul(target_vect/rowsum, "columns")
    return trips

def calibrate(calib_base, production_base, production_forecast):
    """Calibrate a forecast according to calibrated base matrix.
    
    Parameters
    ----------
    calib_base : numpy matrix
        Calibrated base matrix
    production_base : numpy matrix
        Uncalibrated base matrix
    production_forecast : numpy matrix
        Uncalibrated forecast

    Return
    ------
    numpy matrix
        Calibrated forecast
    """
    b = calib_base
    n = production_base
    s = production_forecast
    threshold = param.vector_calibration_threshold
    n[n == 0] = 0.000001
    return numpy.where(s < threshold*n, s * b/n, s + threshold*(b - n))
