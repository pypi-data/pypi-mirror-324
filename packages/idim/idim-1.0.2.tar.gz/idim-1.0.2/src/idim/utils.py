"""Utility functions."""

import functools
import logging
import math
import multiprocessing

import numpy as np

SINGLE_WORKER = (None, False, 0, 1)

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


def parallel_or_not(function_a, function_b, *args, workers=None, **kwargs):
    """Run a single or multiprocessing version of the same functionality.

    Parameters
    ----------
    function_a : callable
        Single processing function to run.
    function_b : callable
        Multiprocessing function to run.
    args : iterable
        Arguments for either function to use.
    workers : optional[union[bool, int]]
        Controls the use of multiprocessing for parallel execution.
        - None, False, 0, or 1: Uses single-threaded execution.
        - True: Automatically uses multiprocessing.cpu_count() for maximum parallelism.
        - int > 1: Specifies the exact number of parallel threads to use.
    kwargs : dict
        Key-Word-Arguments for either function to use.

    Returns
    -------
    return : any
        Return whatever the functions return.
    """
    if isinstance(workers, bool) and workers:
        workers = multiprocessing.cpu_count()
    if workers in SINGLE_WORKER:
        return function_a(*args, **kwargs)
    return function_b(*args, workers=workers, **kwargs)


def move(mode: str, element, *args, **kwargs):
    """Move data to different type."""
    if element is None:
        raise TypeError(f"{element=}")
    if mode == "list":
        return list(element)
    if mode == "numpy":
        return np.array(element, *args, **kwargs)
    raise NotImplementedError(mode)


def verify_matrix_argument(matrix):
    """Make sure the matrix value is as expected."""
    if not isinstance(matrix, np.ndarray):
        raise TypeError("matrix argument should be numpy array")
    if matrix.dtype != np.float64:
        raise ValueError("matrix argument should be float array")
    if len(matrix) == 0:
        raise ValueError("matrix argument has no elements")
    if len(matrix.shape) == 1:
        raise ValueError("matrix argument has no features")
    if len(matrix[0]) == 0:
        raise ValueError("matrix argument has no features")
    if len(matrix.shape) > 2:
        raise ValueError("matrix argument has too many dimensions")


def verify_subset_size_argument(subset_size, total_size):
    """Check bounds on given subset size."""
    if isinstance(subset_size, float):
        if not (0.0 <= subset_size <= 1.0):
            raise ValueError("float subset size should be between 0.0 and 1.0")
    elif isinstance(subset_size, int):
        if not (0 <= subset_size <= total_size):
            raise ValueError(f"int subset size should be between 0 and {total_size}")
    else:
        raise NotImplementedError(f"subset_size type {type(subset_size)}")


def prepare_subset_size_argument(subset_size, total_size):
    """Transform a subset size given as float or int into int."""
    if isinstance(subset_size, float):
        return int(math.ceil(total_size * subset_size))
    elif isinstance(subset_size, int):
        return subset_size
    raise NotImplementedError(f"subset_size type {type(subset_size)}")


def log_func_call(func):
    """A decorator that logs the call of the decorated function to the debug
    log.
    """
    logger.debug(f"applying log_func_call on func {func=}")

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger = logging.getLogger(func.__module__)
        logger.debug(f"Call  {func.__name__}")
        result = func(*args, **kwargs)
        logger.debug(f"Done  {func.__name__}")
        return result
        # try:
        #    result = func(*args, **kwargs)
        #    logger.debug(f"Done  {func.__name__}")
        #    return result
        # except Exception as e:
        #    logger.exception(f"Error {func.__name__}: {str(e)}")
        #    raise e

    return wrapper
