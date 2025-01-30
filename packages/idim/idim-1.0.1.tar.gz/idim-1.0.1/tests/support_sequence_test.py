import pytest
import numpy as np


from idim.support_sequence import (
    support_sequence_size_for_approximation,
    prepare_support_sequence,
    verify_support_sequence,
    _build_geometric_support_sequence,
    build_support_sequence,
    support_sequence_factory,
)


# Tests for support_sequence_size_for_approximation
def test_support_sequence_size_for_approximation():
    assert support_sequence_size_for_approximation(1000, None) is None
    assert support_sequence_size_for_approximation(3) is None
    assert support_sequence_size_for_approximation(2000) == 1000
    assert (
        support_sequence_size_for_approximation(2000, approximation_threshold=500)
        == 500
    )
    assert (
        support_sequence_size_for_approximation(10000, approximation_factor=0.1) == 1000
    )
    assert (
        support_sequence_size_for_approximation(100000, approximation_factor=None)
        == 5000
    )


# Tests for prepare_support_sequence
def test_prepare_support_sequence():
    assert np.array_equal(prepare_support_sequence([1, 2, 3]), np.array([1, 2, 3]))
    assert np.array_equal(
        prepare_support_sequence(np.array([1, 2, 3])), np.array([1, 2, 3])
    )
    with pytest.raises(NotImplementedError):
        prepare_support_sequence([1, 2, 3], target="invalid")


# Tests for verify_support_sequence
def test_verify_support_sequence():
    valid_sequence = np.array([2, 3, 4, 5], dtype=np.int64)
    verify_support_sequence(5, valid_sequence)  # Should not raise any exception

    with pytest.raises(TypeError):
        verify_support_sequence(5, [2, 3, 4, 5])  # Not a numpy array

    with pytest.raises(ValueError):
        verify_support_sequence(5, np.array([2, 3, 4, 5], dtype=float))  # Not int64

    with pytest.raises(ValueError):
        verify_support_sequence(
            5, np.array([[2, 3], [4, 5]], dtype=np.int64)
        )  # Not one-dimensional

    with pytest.raises(ValueError):
        verify_support_sequence(5, np.array([], dtype=np.int64))  # Empty array

    with pytest.raises(ValueError):
        verify_support_sequence(5, np.array([2, 3, 3, 4], dtype=np.int64))  # Duplicates

    with pytest.raises(ValueError):
        verify_support_sequence(5, np.array([1, 2, 3, 4], dtype=np.int64))  # Min < 2

    with pytest.raises(ValueError):
        verify_support_sequence(
            5, np.array([2, 3, 4, 6], dtype=np.int64)
        )  # Max > number_of_data_points

    with pytest.raises(ValueError):
        verify_support_sequence(
            5, np.array([3, 4, 5], dtype=np.int64)
        )  # Smallest element not 2

    with pytest.raises(ValueError):
        verify_support_sequence(
            5, np.array([2, 3, 4], dtype=np.int64)
        )  # Largest element not number_of_data_points


# Tests for _build_geometric_support_sequence
def test_build_geometric_support_sequence():
    result = _build_geometric_support_sequence(10, 5)
    assert isinstance(result, np.ndarray)
    assert result.dtype == np.int64
    assert np.array_equal(result, np.array([2, 5, 7, 9, 10]))


# Tests for build_support_sequence
def test_build_support_sequence():
    with pytest.raises(ValueError):
        build_support_sequence(1)  # Less than two samples

    result = build_support_sequence(100)
    assert isinstance(result, np.ndarray)
    assert result.dtype == np.int64
    assert len(result) == 5  # 100 // 20

    result = build_support_sequence(100, 10)
    assert len(result) == 10

    result = build_support_sequence(100, 0.1)
    assert len(result) == 10

    with pytest.raises(ValueError):
        build_support_sequence(100, 101)  # More support points than samples

    with pytest.raises(NotImplementedError):
        build_support_sequence(100, mode="invalid")


# Tests for support_sequence_factory
def test_support_sequence_factory():
    data = list(range(100))

    result = support_sequence_factory(data, 10)
    assert isinstance(result, np.ndarray)
    assert result.dtype == np.int64
    assert len(result) == 10

    result = support_sequence_factory(
        data, {"number_of_support_points": 10}, verify=True
    )
    assert isinstance(result, np.ndarray)
    assert result.dtype == np.int64
    assert len(result) == 10

    result = support_sequence_factory(data, np.array([2, 3, 4, 5], dtype=np.int64))
    assert np.array_equal(result, np.array([2, 3, 4, 5]))

    with pytest.raises(ValueError):
        support_sequence_factory(data, 1000, verify=True)  # This will fail verification
