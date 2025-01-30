"""Calculation of the Geometric Intrinsic Dimension."""

import functools
import itertools
import logging
import math
import multiprocessing

import numpy
import tqdm

from .support_sequence import (
    verify_support_sequence,
    support_sequence_factory,
    support_sequence_size_for_approximation,
)
from .utils import (
    parallel_or_not,
    verify_matrix_argument,
    log_func_call,
)

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

numpy.seterr(divide="raise")


@log_func_call
def calculate_observable_diameter(data):
    """Calculate the observable diameter of the data.

    Parameters
    ----------
    data : numpy.ndarray
        This should be a two-dimensional array with
        the dimensions [number_of_samples x number_of_features].

    Returns
    -------
    observable_diameter : numpy.array
    """
    return numpy.amax(numpy.amax(data, axis=0) - numpy.amin(data, axis=0))


@log_func_call
def normalize_observable_diameter(data):
    """Divide the data by its observable diameter.

    Parameters
    ----------
    data : numpy.ndarray
        This should be a two-dimensional array with
        the dimensions [number_of_samples x number_of_features].

    Returns
    -------
    normalized_data : numpy.array
        This array will have the same shape as the provided data argument.
    """
    observable_diameter = calculate_observable_diameter(data)
    logger.debug(f"{observable_diameter=}")
    if observable_diameter == 0.0:
        return data
    return data / observable_diameter


def _determine_chunk_size(number_of_items, workers=1):
    chunk_size = number_of_items / workers
    chunk_size = numpy.ceil(chunk_size).astype(int)
    return chunk_size


@log_func_call
def _transform_delta_into_id(delta):
    logger.debug(f"{delta=}")
    try:
        _id = 1 / (delta**2)
        return _id
    except (ZeroDivisionError, FloatingPointError):
        logger.debug("infinite id")
        return float("inf")


def _calculate_feature_sequences(data, *args, **kwargs):
    if data.ndim != 2:
        raise ValueError("expected two dimensional data")
    return numpy.sort(data, axis=0)


def _sort_single_column(data, i):
    # coverage ignored because of partial call in multiprocessing
    return numpy.sort(data[:, i])  # pragma: no cover


def _calculate_feature_sequences_parallel(data, workers, disable_tqdm):
    chunk_size = _determine_chunk_size(data.shape[1], workers)
    _sort_data = functools.partial(_sort_single_column, data)
    with multiprocessing.Pool(workers) as pool:
        result = tqdm.tqdm(
            pool.imap(_sort_data, range(data.shape[1]), chunksize=chunk_size),
            total=data.shape[1],
            disable=disable_tqdm,
        )
        columns = list(result)
        data = numpy.stack(columns, axis=1)  # pylint: disable=E1101
    return data


def calculate_feature_sequences(
    data,
    workers=None,
    unit_obs_diam=True,
    verify=False,
    disable_tqdm=False,
):
    """Sort the data separately per feature columns in ascending order.

    Implementation of Calculation from [StubbemannIntrinsicDF, Lemma 3.5].

    Parameters
    ----------
    data : numpy.ndarray
        This should be a two-dimensional array with
        the dimensions [number_of_samples x number_of_features].
    workers : optional[union[bool, int]]
        Controls the use of multiprocessing for parallel execution.
        - None, False, 0, or 1: Uses single-threaded execution.
        - True: Automatically uses multiprocessing.cpu_count() for maximum parallelism.
        - int > 1: Specifies the exact number of parallel threads to use.
    unit_obs_diam : optional[bool]
        Divide the data by its observable diameter.
    verify : optional[bool]
        Check the data argument before doing anything.
    disable_tqdm : optional[bool]
        Whether to disable the entire progressbar wrapper.
        If set to None, disable on non-TTY.

    Returns
    -------
    feature_sequences : numpy.ndarray
        This array will have the same shape as the provided data argument.
    """
    if verify:
        verify_matrix_argument(data)
    if unit_obs_diam:
        data = normalize_observable_diameter(data)
    feature_sequences = parallel_or_not(
        _calculate_feature_sequences,
        _calculate_feature_sequences_parallel,
        workers=workers,
        data=data,
        disable_tqdm=disable_tqdm,
    )
    return feature_sequences


def _determine_single_offset_gaps(feature_sequences, offset):
    _offset = offset - 1
    gaps = feature_sequences[_offset:] - feature_sequences[:-_offset]
    return gaps


def _determine_single_offset_phis(feature_sequences, offset):
    gaps = _determine_single_offset_gaps(feature_sequences, offset)
    phis = numpy.amin(gaps, axis=0)  # pylint: disable=E1101
    return phis


def _determine_single_offset_max_phi(feature_sequences, offset):
    phis = _determine_single_offset_phis(feature_sequences, offset)
    max_phi = numpy.amax(phis, axis=0)  # pylint: disable=E1101
    return max_phi


def _calculate_max_phis_without_support_sequence(feature_sequences, disable_tqdm):
    max_phis = []
    for offset in tqdm.tqdm(range(2, len(feature_sequences) + 1), disable=disable_tqdm):
        max_phi = _determine_single_offset_max_phi(feature_sequences, offset)
        max_phis.append(max_phi)
    return max_phis


def _calculate_max_phis_without_support_sequence_parallel(
    feature_sequences,
    workers,
    disable_tqdm,
):
    offsets = range(2, len(feature_sequences) + 1)
    workers = min(workers, len(offsets))
    _partial = functools.partial(
        _determine_single_offset_max_phi,
        feature_sequences,
    )
    chunk_size = _determine_chunk_size(len(feature_sequences), workers)
    with multiprocessing.Pool(workers) as pool:
        result = tqdm.tqdm(
            pool.imap_unordered(
                _partial,
                offsets,
                chunksize=chunk_size,
            ),
            total=len(offsets),
            disable=disable_tqdm,
        )
        max_phis = list(result)
    return max_phis


@log_func_call
def calculate_id_without_support_sequence_from_feature_sequences(
    feature_sequences,
    workers=None,
    verify=False,
    disable_tqdm=False,
):
    """Calculate id from feature sequences without using a support sequence.

    Parameters
    ----------
    feature_sequences : numpy.ndarray
        This should be a two-dimensional array with
        the dimensions [number_of_samples x number_of_features].
    workers : optional[union[bool, int]]
        Controls the use of multiprocessing for parallel execution.
        - None, False, 0, or 1: Uses single-threaded execution.
        - True: Automatically uses multiprocessing.cpu_count() for maximum parallelism.
        - int > 1: Specifies the exact number of parallel threads to use.
    verify : optional[bool]
        Check the feature sequence argument before doing anything.
    disable_tqdm : optional[bool]
        Whether to disable the entire progressbar wrapper.
        If set to None, disable on non-TTY.

    Returns
    -------
    _id : numpy.ndarray
        The intrinsic dimension of the data.
    """
    if verify:
        verify_matrix_argument(feature_sequences)
    max_phis = parallel_or_not(
        _calculate_max_phis_without_support_sequence,
        _calculate_max_phis_without_support_sequence_parallel,
        workers=workers,
        feature_sequences=feature_sequences,
        disable_tqdm=disable_tqdm,
    )
    delta = sum(max_phis)
    delta /= len(feature_sequences)
    _id = numpy.array([_transform_delta_into_id(delta)])
    return _id


def _calculate_delta_bounds(feature_sequences, support_sequence, max_phis):
    # we can make support sequence jumps one bigger than actual defined
    #  and skip adding delta to bounds
    #  because max_phi=0 for k=0
    #  see remark at the end of proof of theorem 3.2
    support_sequence_jumps = support_sequence[1:] - support_sequence[:-1]
    delta_min = sum(support_sequence_jumps * max_phis[:-1]) + max_phis[-1]
    delta_max = sum(support_sequence_jumps * max_phis[1:]) + max_phis[0]
    delta_min /= len(feature_sequences)
    delta_max /= len(feature_sequences)
    # delta = sum(max_phis)
    # delta /= len(feature_sequences)
    return delta_min, delta_max


def _determine_remaining_phis(feature_sequences, interval):
    last_support, next_support, used_phi_indices, default = interval
    missing_supports = range(last_support + 1, next_support)
    values = numpy.array(
        [
            [
                _determine_single_offset_phis(feature_sequences[:, i], missing_support)
                for i in used_phi_indices
            ]
            for missing_support in missing_supports
        ]
    )
    if len(values):
        return numpy.max(values, axis=1, initial=default)
    return []


def _collect_remaining_phis(
    feature_sequences,
    support_sequence,
    phi_indices,
    max_phis,
    disable_tqdm,
):
    remaining_phis = []
    for interval in tqdm.tqdm(
        zip(support_sequence, support_sequence[1:], phi_indices, max_phis),
        total=len(phi_indices),
        disable=disable_tqdm,
    ):
        new_phis = _determine_remaining_phis(feature_sequences, interval)
        remaining_phis.extend(new_phis)
    return remaining_phis


def _collect_remaining_phis_parallel(
    feature_sequences,
    support_sequence,
    phi_indices,
    max_phis,
    workers,
    disable_tqdm,
):
    remaining_phis = []
    _partial = functools.partial(
        _determine_remaining_phis,
        feature_sequences,
    )
    chunk_size = _determine_chunk_size(len(feature_sequences), workers)
    with multiprocessing.Pool(workers) as pool:
        for new_phis in tqdm.tqdm(
            pool.imap(
                _partial,
                zip(support_sequence, support_sequence[1:], phi_indices, max_phis),
                chunksize=chunk_size,
            ),
            total=len(phi_indices),
            disable=disable_tqdm,
        ):
            remaining_phis.extend(new_phis)
    return remaining_phis


def _calculate_delta_with_support_sequence_exact(
    feature_sequences,
    support_sequence,
    phi_indices,
    max_phis,
    workers,
    disable_tqdm,
):
    remaining_phis = parallel_or_not(
        _collect_remaining_phis,
        _collect_remaining_phis_parallel,
        feature_sequences,
        support_sequence,
        phi_indices,
        max_phis,
        workers=workers,
        disable_tqdm=disable_tqdm,
    )
    all_phi_js = numpy.concatenate([remaining_phis, max_phis])
    delta = sum(all_phi_js) / len(feature_sequences)
    return delta


def _calculate_delta_bounds_and_error(
    feature_sequences,
    support_sequence,
    phi_indices,
    max_phis,
    exact,
    workers,
    disable_tqdm,
):
    if isinstance(max_phis, list):
        max_phis = numpy.array(max_phis)
    delta_min, delta_max = _calculate_delta_bounds(
        feature_sequences,
        support_sequence,
        max_phis,
    )
    if exact:
        delta_min = _calculate_delta_with_support_sequence_exact(
            feature_sequences,
            support_sequence,
            phi_indices,
            max_phis,
            workers=workers,
            disable_tqdm=disable_tqdm,
        )
        delta_max = delta_min
        error = None
    else:
        if delta_min == 0.0:
            error = numpy.array(float("inf"))
        else:
            error = (delta_max - delta_min) / delta_min
    return delta_min, delta_max, error


def _calculate_deltas_with_support_sequence(
    feature_sequences,
    support_sequence,
    exact,
    disable_tqdm,
):
    phi_indices = []
    max_phi = 0
    max_phis = []
    for support in tqdm.tqdm(support_sequence, disable=disable_tqdm):
        phis = _determine_single_offset_phis(feature_sequences, support)
        phi_indices.append(numpy.where(phis > max_phi)[0])
        max_phi = numpy.amax(phis)
        max_phis.append(max_phi)

    phi_indices = phi_indices[1:]

    return _calculate_delta_bounds_and_error(
        feature_sequences,
        support_sequence,
        phi_indices,
        max_phis,
        exact,
        workers=None,
        disable_tqdm=disable_tqdm,
    )


def _calculate_deltas_with_support_sequence_parallel(
    feature_sequences,
    support_sequence,
    exact,
    workers,
    disable_tqdm,
):
    workers = min(workers, len(support_sequence))
    chunk_size = _determine_chunk_size(len(support_sequence), workers)
    _partial = functools.partial(
        _determine_single_offset_phis,
        feature_sequences,
    )
    phi_indices = []
    max_phi = 0
    max_phis = []
    with multiprocessing.Pool(workers) as pool:
        result = tqdm.tqdm(
            pool.imap(
                _partial,
                support_sequence,
                chunksize=chunk_size,
            ),
            total=len(support_sequence),
            disable=disable_tqdm,
        )
        for phis in result:
            phi_indices.append(numpy.where(phis > max_phi)[0])
            max_phi = numpy.amax(phis)
            max_phis.append(max_phi)

    phi_indices = phi_indices[1:]

    return _calculate_delta_bounds_and_error(
        feature_sequences,
        support_sequence,
        phi_indices,
        max_phis,
        exact,
        workers=workers,
        disable_tqdm=disable_tqdm,
    )


@log_func_call
def calculate_id_with_support_sequence_from_feature_sequences(
    feature_sequences,
    support_sequence,
    workers=None,
    exact=False,
    verify=False,
    disable_tqdm=False,
):
    """Calculate id from feature sequences using a support sequence.

    Parameters
    ----------
    feature_sequences : numpy.ndarray
        This should be a two-dimensional array with
        the dimensions [number_of_samples x number_of_features].
    support_sequence : numpy.ndarray
        This should be a one dimensional array with monotonic increasing
        sequence from 2 to number_of_samples.
    workers : optional[union[bool, int]]
        Controls the use of multiprocessing for parallel execution.
        - None, False, 0, or 1: Uses single-threaded execution.
        - True: Automatically uses multiprocessing.cpu_count() for maximum parallelism.
        - int > 1: Specifies the exact number of parallel threads to use.
    exact : optional[bool]
        Use this flag for calculating exact value.
    verify : optional[bool]
        Check the feature and support sequence arguments before doing anything.
    disable_tqdm : optional[bool]
        Whether to disable the entire progressbar wrapper.
        If set to None, disable on non-TTY.

    Returns
    -------
    _ids : numpy.ndarray
        The lower and upper bounds of the intrinsic dimension of the data and
        the relative delta error.
    """
    if verify:
        verify_matrix_argument(feature_sequences)
        verify_support_sequence(len(feature_sequences), support_sequence)
    delta_min, delta_max, error = parallel_or_not(
        _calculate_deltas_with_support_sequence,
        _calculate_deltas_with_support_sequence_parallel,
        feature_sequences,
        support_sequence,
        exact,
        workers=workers,
        disable_tqdm=disable_tqdm,
    )
    return numpy.array(
        [
            _transform_delta_into_id(delta_max),
            _transform_delta_into_id(delta_min),
            error,
        ]
    )


#####################
# wrapper functions #
#####################


@log_func_call
def calculate_intrinsic_dimension_without_support_sequence(
    data,
    workers=None,
    serial_feature_sequences=True,
    unit_obs_diam=True,
    verify=False,
    disable_tqdm=False,
):
    """Calculate the intrinsic dimension without using a support sequence.

    Implementation of [StubbemannIntrinsicDF, Algorithm 1].

    Parameters
    ----------
    data : numpy.ndarray
        This should be a two-dimensional array with
        the dimensions [number_of_samples x number_of_features].
    workers : optional[union[bool, int]]
        Controls the use of multiprocessing for parallel execution.
        - None, False, 0, or 1: Uses single-threaded execution.
        - True: Automatically uses multiprocessing.cpu_count() for maximum parallelism.
        - int > 1: Specifies the exact number of parallel threads to use.
    serial_feature_sequences : optional[bool]
        Do not use multiprocessing for calculation of feature sequences.
        Faster up to very large data dimension.
        Setting this to False only has an effect when using workers.
    unit_obs_diam : optional[bool]
        Divide the data by its observable diameter.
    verify : optional[bool]
        Check the data argument before doing anything.
    disable_tqdm : optional[bool]
        Whether to disable the entire progressbar wrapper.
        If set to None, disable on non-TTY.

    Returns
    -------
    _id : numpy.ndarray
        The intrinsic dimension of the data.
    """
    if serial_feature_sequences:
        _workers = False
    else:
        _workers = workers
    feature_sequences = calculate_feature_sequences(
        data,
        _workers,
        unit_obs_diam,
        verify,
        disable_tqdm,
    )
    _id = calculate_id_without_support_sequence_from_feature_sequences(
        feature_sequences,
        workers,
        verify=False,
        disable_tqdm=disable_tqdm,
    )
    return _id


@log_func_call
def calculate_intrinsic_dimension_with_support_sequence(
    data,
    support_sequence,
    workers=None,
    serial_feature_sequences=True,
    exact=False,
    unit_obs_diam=True,
    verify=False,
    disable_tqdm=False,
):
    """Calculate the intrinsic dimension by using a support sequence.

    Implementation of [StubbemannIntrinsicDF, Algorithm 2].

    Parameters
    ----------
    data : numpy.ndarray
        This should be a two-dimensional array with
        the dimensions [number_of_samples x number_of_features].
    support_sequence : union[dict, int, float, iterable]
        For *support_sequence='a dict'* a new support sequence with
        these key-word-arguments is constructed.
        See 'build_support_sequence' for details.
        For *support_sequence='an int'* a new support sequence of this
        length is constructed, using the default arguments
        of 'build_support_sequence'.
        For *support_sequence='a float'* a new support sequence of this
        relative length is constructed, using the default arguments
        of 'build_support_sequence'.
        For *support_sequence='an iterable'* that support sequence is used.
    workers : optional[union[bool, int]]
        Controls the use of multiprocessing for parallel execution.
        - None, False, 0, or 1: Uses single-threaded execution.
        - True: Automatically uses multiprocessing.cpu_count() for maximum parallelism.
        - int > 1: Specifies the exact number of parallel threads to use.
    serial_feature_sequences : optional[bool]
        Do not use multiprocessing for calculation of feature sequences.
        Faster up to very large data dimension.
        Setting this to False only has an effect when using workers.
    exact : optional[bool]
        Use this flag for calculating exact value.
    unit_obs_diam : optional[bool]
        Divide the data by its observable diameter.
    verify : optional[bool]
        Check the data argument before doing anything.
        This is also applied to support sequence argument, if this is provided.
    disable_tqdm : optional[bool]
        Whether to disable the entire progressbar wrapper.
        If set to None, disable on non-TTY.

    Returns
    -------
    _id : numpy.ndarray
        The lower and upper bounds of the intrinsic dimension of the data and
        the relative delta error.
    """
    if serial_feature_sequences:
        _workers = False
    else:
        _workers = workers
    feature_sequences = calculate_feature_sequences(
        data,
        _workers,
        unit_obs_diam,
        verify,
        disable_tqdm,
    )
    support_sequence = support_sequence_factory(
        data,
        support_sequence,
        "numpy",
        verify,
    )
    _id = calculate_id_with_support_sequence_from_feature_sequences(
        feature_sequences,
        support_sequence,
        workers,
        exact,
        verify=False,
        disable_tqdm=disable_tqdm,
    )
    return _id


@log_func_call
def calculate_intrinsic_dimension(
    data,
    support_sequence=None,
    workers=None,
    serial_feature_sequences=True,
    exact=False,
    unit_obs_diam=True,
    verify=False,
    disable_tqdm=False,
):
    """Calculate the intrinsic dimension.

    Parameters
    ----------
    data : numpy.ndarray
        This should be a two-dimensional array with
        the dimensions [number_of_samples x number_of_features].
    support_sequence : union[dict, int, float, iterable]
        For *support_sequence='a dict'* a new support sequence with
        these key-word-arguments is constructed.
        See 'build_support_sequence' for details.
        For *support_sequence='an int'* a new support sequence of this
        length is constructed, using the default arguments
        of 'build_support_sequence'.
        For *support_sequence='a float'* a new support sequence of this
        relative length is constructed, using the default arguments
        of 'build_support_sequence'.
        For *support_sequence='an iterable'* that support sequence is used.
    workers : optional[union[bool, int]]
        Controls the use of multiprocessing for parallel execution.
        - None, False, 0, or 1: Uses single-threaded execution.
        - True: Automatically uses multiprocessing.cpu_count() for maximum parallelism.
        - int > 1: Specifies the exact number of parallel threads to use.
    serial_feature_sequences : optional[bool]
        Do not use multiprocessing for calculation of feature sequences.
        Faster up to very large data dimension.
        Setting this to False only has an effect when using workers.
    exact : optional[bool]
        Use this flag for calculating exact value when using support sequences.
    unit_obs_diam : optional[bool]
      Divide the data by its observable diameter.
    verify : optional[bool]
        Check the data argument before doing anything.
        This is also applied to support sequence argument, if this is provided.
    disable_tqdm : optional[bool]
        Whether to disable the entire progressbar wrapper.
        If set to None, disable on non-TTY.

    Returns
    -------
    intrinsic_dimension : numpy.ndarray
        Either only the intrinsic dimension of the data or lower and upper
        bounds of the intrinsic dimension and the relative delta error.
    """
    if support_sequence is None:
        return calculate_intrinsic_dimension_without_support_sequence(
            data,
            workers,
            serial_feature_sequences,
            unit_obs_diam,
            verify,
            disable_tqdm,
        )
    return calculate_intrinsic_dimension_with_support_sequence(
        data,
        support_sequence,
        workers,
        serial_feature_sequences,
        exact,
        unit_obs_diam,
        verify,
        disable_tqdm,
    )


@log_func_call
def idim(
    data,
    approximation_threshold=None,
    approximation_factor=None,
    workers=None,
    serial_feature_sequences=True,
    unit_obs_diam=True,
    verify=False,
    disable_tqdm=False,
):
    """Calculate the (estimated) intrinsic dimension.

    Adaptive switch between exact and approximated calculation.

    See original publications for mathematical details.

    Parameters:
    -----------
    data : numpy.ndarray
        This should be a two-dimensional array with
        the dimensions [number_of_samples x number_of_features].
    approximation_threshold : optional[int]
        The threshold number of data points above which approximation is used.
    approximation_factor : optional[float]
        The factor used to determine the size of the support sequence when approximating.
    workers : optional[union[bool, int]]
        Controls the use of multiprocessing for parallel execution.
        - None, False, 0, or 1: Uses single-threaded execution.
        - True: Automatically uses multiprocessing.cpu_count() for maximum parallelism.
        - int > 1: Specifies the exact number of parallel threads to use.
    serial_feature_sequences : optional[bool]
        Do not use multiprocessing for calculation of feature sequences.
        Faster up to very large data dimension.
        Setting this to False only has an effect when using workers.
    unit_obs_diam : optional[bool]
        Divide the data by its observable diameter.
    verify : optional[bool]
        Check the data argument before doing anything.
        This is also applied to the constructed support sequence.
    disable_tqdm : optional[bool]
        Whether to disable the entire progressbar wrapper.
        If set to None, disable on non-TTY.

    Returns:
    --------
    intrinsic_dimension : float
        The (estimated) intrinsic dimension of the data.

    Notes:
    ------
    - If the data size is below or equal to the approximation_threshold,
      the function calculates the exact intrinsic dimension.
    - For larger datasets, it uses the approximation method based on a support
      sequence.
    - The support sequence size is determined by taking the maximum of either
      the specified approximation threshold or the product of the approximation
      factor and total number of samples.
    - The function relies on `calculate_intrinsic_dimension` function
      for the core computation. When approximating, the returned value
      is the average of the calculated upper and lower bounds.
    """
    support_sequence = support_sequence_size_for_approximation(
        len(data), approximation_threshold, approximation_factor
    )
    gid = calculate_intrinsic_dimension(
        data,
        support_sequence,
        workers=workers,
        serial_feature_sequences=serial_feature_sequences,
        unit_obs_diam=unit_obs_diam,
        verify=verify,
        disable_tqdm=disable_tqdm,
    )
    if support_sequence is None:
        return gid[0]
    return (gid[0] + gid[1]) / 2


@log_func_call
def idim_brute_force(data, unit_diam=True, disable_tqdm=False):
    """
    Calculate the intrinsic dimension of the given data.

    Implementation of Calculation from [StubbemannIntrinsicDF2022, Theorem 3.2].

    Beware runtime and space explosion. Useful for testing purposes.

    Parameters:
    -----------
    data : numpy.ndarray
        This should be a two-dimensional array with
        the dimensions [number_of_samples x number_of_features].
    unit_obs_diam : optional[bool]
        Divide the data by its observable diameter.
    disable_tqdm : optional[bool]
        Whether to disable the entire progressbar wrapper.
        If set to None, disable on non-TTY.

    Returns:
    --------
    intrinsic_dimension : float
        The intrinsic dimension of the data.
    """
    if unit_diam:
        data = normalize_observable_diameter(data)
    delta = 0.0
    for k in tqdm.tqdm(
        range(2, len(data) + 1),
        desc="k",
        total=len(data) - 1,
        disable=disable_tqdm,
    ):
        worst = numpy.full_like(data[0], numpy.inf)
        for subset in tqdm.tqdm(
            itertools.combinations(range(len(data)), k),
            desc="s",
            leave=False,
            total=math.comb(len(data), k),
            disable=disable_tqdm,
        ):
            data_subset = data[list(subset)]
            best = numpy.full_like(data_subset[0], -numpy.inf)
            for i, j in itertools.combinations(range(len(data_subset)), 2):
                r = abs(data_subset[i] - data_subset[j])
                best = numpy.maximum(best, r)
            worst = numpy.minimum(worst, best)
        delta += numpy.max(worst)
    delta /= len(data)
    dim = _transform_delta_into_id(delta)
    return dim
