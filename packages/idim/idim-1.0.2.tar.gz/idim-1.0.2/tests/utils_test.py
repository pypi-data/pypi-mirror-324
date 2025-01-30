import pytest
import numpy as np

from idim.utils import (
    move,
    verify_matrix_argument,
    verify_subset_size_argument,
    prepare_subset_size_argument,
)


def test_move_to_list():
    # Test converting various types to list
    assert move("list", (1, 2, 3)) == [1, 2, 3]
    assert move("list", "abc") == ["a", "b", "c"]
    assert move("list", {1, 2, 3}) == [1, 2, 3]
    assert move("list", {"a": 1, "b": 2}) == ["a", "b"]


def test_move_to_numpy():
    # Test converting to numpy array
    assert np.array_equal(move("numpy", [1, 2, 3]), np.array([1, 2, 3]))
    assert np.array_equal(move("numpy", (1, 2, 3)), np.array([1, 2, 3]))
    assert np.array_equal(move("numpy", [[1, 2], [3, 4]]), np.array([[1, 2], [3, 4]]))


def test_move_to_numpy_with_args():
    # Test numpy conversion with additional arguments
    result = move("numpy", [1, 2, 3], dtype=float)
    assert np.array_equal(result, np.array([1.0, 2.0, 3.0]))
    assert result.dtype == float


def test_move_to_numpy_with_kwargs():
    # Test numpy conversion with keyword arguments
    result = move("numpy", [1, 2, 3], dtype=float, order="F")
    assert np.array_equal(result, np.array([1.0, 2.0, 3.0]))
    assert result.dtype == float
    assert result.flags["F_CONTIGUOUS"]


def test_move_invalid_mode():
    # Test raising NotImplementedError for invalid mode
    with pytest.raises(NotImplementedError):
        move("invalid_mode", [1, 2, 3])


def test_move_empty_input():
    # Test with empty inputs
    assert move("list", []) == []
    assert np.array_equal(move("numpy", []), np.array([]))


def test_move_none_input():
    # Test with None input
    with pytest.raises(TypeError):
        move("list", None)
    with pytest.raises(TypeError):
        move("numpy", None)


def test_valid_matrix():
    # Test with a valid matrix
    valid_matrix = np.array([[1.0, 2.0], [3.0, 4.0]], dtype=np.float64)
    verify_matrix_argument(valid_matrix)  # Should not raise any exception


def test_non_numpy_array():
    # Test with a non-numpy array
    with pytest.raises(TypeError, match="matrix argument should be numpy array"):
        verify_matrix_argument([[1.0, 2.0], [3.0, 4.0]])


def test_non_float_array():
    # Test with a non-float numpy array
    with pytest.raises(ValueError, match="matrix argument should be float array"):
        verify_matrix_argument(np.array([[1, 2], [3, 4]], dtype=int))


def test_empty_matrix():
    # Test with an empty matrix
    with pytest.raises(ValueError, match="matrix argument has no elements"):
        verify_matrix_argument(np.array([], dtype=np.float64))


def test_1d_array():
    # Test with a 1D array
    with pytest.raises(ValueError, match="matrix argument has no features"):
        verify_matrix_argument(np.array([1.0, 2.0, 3.0], dtype=np.float64))


def test_matrix_with_no_features():
    # Test with a matrix that has rows but no columns
    with pytest.raises(ValueError, match="matrix argument has no features"):
        verify_matrix_argument(np.array([[]], dtype=np.float64))


def test_matrix_with_one_feature():
    # Test with a matrix that has one feature (should be valid)
    valid_matrix = np.array([[1.0], [2.0]], dtype=np.float64)
    verify_matrix_argument(valid_matrix)  # Should not raise any exception


def test_matrix_with_one_sample():
    # Test with a matrix that has one sample (should be valid)
    valid_matrix = np.array([[1.0, 2.0]], dtype=np.float64)
    verify_matrix_argument(valid_matrix)  # Should not raise any exception


def test_3d_array():
    # Test with a 3D array
    with pytest.raises(ValueError, match="matrix argument has too many dimensions"):
        verify_matrix_argument(np.array([[[1.0]]], dtype=np.float64))


def test_verify_valid_float_subset_size():
    verify_subset_size_argument(0.5, 100)  # Should not raise any exception


def test_verify_invalid_float_subset_size():
    with pytest.raises(
        ValueError, match="float subset size should be between 0.0 and 1.0"
    ):
        verify_subset_size_argument(1.5, 100)


def test_verify_valid_int_subset_size():
    verify_subset_size_argument(50, 100)  # Should not raise any exception


def test_verify_invalid_int_subset_size():
    with pytest.raises(ValueError, match="int subset size should be between 0 and 100"):
        verify_subset_size_argument(150, 100)


def test_verify_invalid_type_subset_size():
    with pytest.raises(NotImplementedError, match="subset_size type <class 'str'>"):
        verify_subset_size_argument("50", 100)


def test_verify_edge_cases():
    verify_subset_size_argument(0.0, 100)  # Should not raise any exception
    verify_subset_size_argument(1.0, 100)  # Should not raise any exception
    verify_subset_size_argument(0, 100)  # Should not raise any exception
    verify_subset_size_argument(100, 100)  # Should not raise any exception


def test_prepare_float_subset_size():
    assert prepare_subset_size_argument(0.5, 100) == 50


def test_prepare_float_subset_size_rounding():
    assert prepare_subset_size_argument(0.33, 100) == 33
    assert prepare_subset_size_argument(0.66, 100) == 66


def test_prepare_int_subset_size():
    assert prepare_subset_size_argument(50, 100) == 50


def test_prepare_invalid_type_subset_size():
    with pytest.raises(NotImplementedError, match="subset_size type <class 'str'>"):
        prepare_subset_size_argument("50", 100)


def test_prepare_edge_cases():
    assert prepare_subset_size_argument(0.0, 100) == 0
    assert prepare_subset_size_argument(1.0, 100) == 100
    assert prepare_subset_size_argument(0, 100) == 0
    assert prepare_subset_size_argument(100, 100) == 100


def test_prepare_float_rounding_up():
    assert prepare_subset_size_argument(0.01, 100) == 1  # Should round up to 1
    assert prepare_subset_size_argument(0.99, 100) == 99  # Should round up to 99
