"""Providing support sequences."""

import numpy as np

from .utils import move, verify_subset_size_argument, prepare_subset_size_argument


def support_sequence_size_for_approximation(
    len_data,
    approximation_threshold=1000,
    approximation_factor=0.05,
):
    if approximation_threshold is None:
        approximation_threshold = 1000
    if len_data <= approximation_threshold:
        return None
    if approximation_factor is None:
        approximation_factor = 0.05
    return max(approximation_threshold, int(len_data * approximation_factor))


def prepare_support_sequence(support_sequence, target="numpy"):
    """Make sure the support sequence is of specific type."""
    if target == "numpy":
        if isinstance(support_sequence, np.ndarray):
            return support_sequence

        return move("numpy", support_sequence)
    else:
        raise NotImplementedError(target)


def verify_support_sequence(number_of_data_points, support_sequence):
    """Parse a given support sequence and make sure it is correct."""
    if not isinstance(support_sequence, np.ndarray):
        raise TypeError("support sequence should be numpy ndarray")
    if support_sequence.dtype != np.int64:
        raise ValueError("matrix argument should be an int array")
    if len(support_sequence.shape) > 1:
        raise ValueError("support sequence should be one-dimensional")
    if len(support_sequence) < 1:
        raise ValueError("support sequence is too short")
    _, counts = np.unique(support_sequence, return_counts=True)
    if any(counts > 1):
        raise ValueError("support sequence should have no duplicated elements")

    min_ = min(support_sequence)
    max_ = max(support_sequence)
    if min_ < 2 or number_of_data_points < max_:
        raise ValueError(
            "support sequence should only have elements between 2 and "
            + f"number_of_data_points ({number_of_data_points})"
        )
    if min_ != 2:
        raise ValueError("smallest element of support sequence must be 2")
    if max_ != number_of_data_points:
        raise ValueError(
            "largest element of support sequence must be "
            + f"number_of_data_points ({number_of_data_points})"
        )


def _build_geometric_support_sequence(number_of_data_points, number_of_support_points):
    support_points = np.geomspace(number_of_data_points, 2, number_of_support_points)
    support_points = number_of_data_points + 2 - support_points
    support_points = np.floor(support_points)
    support_points = np.concatenate([[2], support_points, [number_of_data_points]])
    support_points = np.unique(support_points)
    support_points = support_points.astype(int)
    return support_points


def build_support_sequence(
    number_of_samples,
    number_of_support_points=None,
    mode="geometric",
    verify=False,
):
    """Construct a support sequence.

    Per default, a one-twentieth of the number of samples are used as
    number of support points.

    Parameters
    ----------
    number_of_samples : int
    number_of_support_points : optional[union[int, float]]
        When given as an int, build a support sequence of this size.
        When given as a float, it specifies the relative size of the
        support sequence that will be contructed.
    mode : str
        Choose type of support sequence.
        Available modes are ['geometric'].
    verify : bool
        Check the number_of_support_points arguments.

    Returns
    -------
    support_sequence : numpy.ndarray

    Raises
    ------
    NotImplementedError : invalid mode

    """
    if number_of_samples < 2:
        raise ValueError("can not build support sequence for less than two samples")
    if number_of_support_points is None:
        number_of_support_points = number_of_samples // 20
    else:
        if isinstance(number_of_support_points, (int, float)):
            if verify:
                verify_subset_size_argument(
                    number_of_support_points,
                    number_of_samples,
                )
            number_of_support_points = prepare_subset_size_argument(
                number_of_support_points,
                number_of_samples,
            )
        if number_of_support_points > number_of_samples:
            raise ValueError("there should be more samples than support points")
    if mode == "geometric":
        return _build_geometric_support_sequence(
            number_of_samples, number_of_support_points
        )
    raise NotImplementedError(mode)


def support_sequence_factory(
    data,
    support_sequence,
    target="numpy",
    verify=False,
):
    if isinstance(support_sequence, dict):
        number_of_data_points = support_sequence.pop(
            "number_of_data_points",
            len(data),
        )
        support_sequence = build_support_sequence(
            number_of_data_points,
            **support_sequence,
            verify=verify,
        )
    elif isinstance(support_sequence, int):
        support_sequence = build_support_sequence(
            len(data),
            support_sequence,
            verify=verify,
        )
    if verify:
        verify_support_sequence(len(data), support_sequence)
    support_sequence = prepare_support_sequence(
        support_sequence,
        target,
    )
    return support_sequence
