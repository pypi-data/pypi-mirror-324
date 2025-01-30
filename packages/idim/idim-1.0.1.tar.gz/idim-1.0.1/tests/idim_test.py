import hashlib
import logging

import hypothesis
import hypothesis.extra.numpy as hen
import numpy as np
import pytest

from idim import (
    normalize_observable_diameter,
    calculate_feature_sequences,
    calculate_intrinsic_dimension,
    idim,
    idim_brute_force,
)
from idim.idim import (
    calculate_id_without_support_sequence_from_feature_sequences,
    calculate_id_with_support_sequence_from_feature_sequences,
)
from idim.support_sequence import support_sequence_factory

from .original_idim_exact import original_idim_exact
from .original_idim_approx import original_idim_approx

logger = logging.getLogger(__name__)


###########
# helpers #
###########


def hash_ndarray(array):
    byte_string = array.tobytes()
    shape_bytes = str(array.shape).encode("utf-8")
    dtype_bytes = str(array.dtype).encode("utf-8")
    combined_bytes = byte_string + shape_bytes + dtype_bytes
    return hashlib.md5(combined_bytes).hexdigest()


def assert_allclose(a, b):
    assert np.allclose(a, b)


def assert_bounds(lower, value, upper):
    if value == float("inf"):
        assert lower <= value and value == upper
    elif value == -float("inf"):
        assert lower == value and value <= upper
    else:
        assert (
            lower <= value <= upper
            or np.allclose(lower, value)
            or np.allclose(upper, value)
        )


def generate_cube_data(size):
    return np.eye(size)


def calculate_true_id_cube(size):
    data = generate_cube_data(size)
    result = (size, idim_brute_force(data, disable_tqdm=True), size**2)
    return result


############
# fixtures #
############


RECOMPUTE_FIXTURE_CASH = True


@pytest.fixture(
    scope="session",
    params=[False, True],
    # params=[None, False, 0, 1, 2, 3, 4, True],
)
def workers(request):
    return request.param


def cache_fixure(request, key, callback, *args, **kwargs):
    result = request.config.cache.get(key, None)
    if result is None or RECOMPUTE_FIXTURE_CASH:
        logger.debug(f"Preparing cache fixure {key=}, {callback=}, {args=}, {kwargs=}")
        result = callback(*args, **kwargs)
        assert result is not None
        logger.debug("Completed cache fixure preparation")
        request.config.cache.set(key, result)
    else:
        logger.debug(f"Using cached fixure    {key=}, {callback=}, {args=}, {kwargs=}")
    return result


@pytest.fixture(
    scope="session",
    params=list(range(2, 11)),
)
def true_ids_cube(request):
    size = request.param
    return cache_fixure(
        request,
        f"true_ids_cube_{size}",
        calculate_true_id_cube,
        size=size,
    )


def _cache_dim(request, base_key, callback, data, **kwargs):
    _hash = hash_ndarray(data)
    s = "-".join([f"{key}={value}" for key, value in sorted(kwargs.items())])
    key = f"{base_key}/data={_hash}"
    if s:
        key += f"-{s}"
    dim = cache_fixure(
        request,
        key,
        callback,
        data=data,
        **kwargs,
    )
    return dim


def cached_idim_brute_force(request, data, **kwargs):
    return _cache_dim(
        request,
        "hypothesis/idim_brute_force",
        idim_brute_force,
        data=data,
        **kwargs,
    )


def _oie(*args, **kwargs):
    return original_idim_exact(*args, **kwargs).tolist()


def cached_original_idim_exact(request, data, **kwargs):
    return _cache_dim(
        request,
        "hypothesis/original_idim_exact",
        _oie,
        data=data,
        **kwargs,
    )


def _oia(*args, **kwargs):
    return np.array(original_idim_approx(*args, **kwargs)).tolist()


def cached_original_idim_approx(request, data, **kwargs):
    return _cache_dim(
        request,
        "hypothesis/original_idim_approx",
        _oia,
        data=data,
        **kwargs,
    )


def _cid(*args, **kwargs):
    return calculate_intrinsic_dimension(*args, **kwargs).tolist()


def cached_cid(request, data, **kwargs):
    return _cache_dim(
        request,
        "hypothesis/cid",
        _cid,
        data=data,
        **kwargs,
    )


def cached_idim(request, data, **kwargs):
    return _cache_dim(
        request,
        "hypothesis/idim",
        idim,
        data,
        **kwargs,
    )


#################################
# helpers for hypothesis spaces #
#################################


_reasonable_numbers_config = dict(
    allow_nan=False,
    allow_infinity=False,
    allow_subnormal=False,
    min_value=-(10**10),
    max_value=10**10,
)


_small_shape_strategy = hypothesis.strategies.tuples(
    hypothesis.strategies.integers(min_value=2, max_value=10),
    hypothesis.strategies.integers(min_value=1, max_value=10),
)

_medium_shape_strategy = hypothesis.strategies.tuples(
    hypothesis.strategies.integers(min_value=2, max_value=100),
    hypothesis.strategies.integers(min_value=1, max_value=100),
)

_large_shape_strategy = hypothesis.strategies.tuples(
    hypothesis.strategies.integers(min_value=2, max_value=1000),
    hypothesis.strategies.integers(min_value=1, max_value=1000),
)


_small_data_config = dict(
    dtype=np.float64,
    shape=_small_shape_strategy,
    elements=_reasonable_numbers_config,
)

_medium_data_config = dict(
    dtype=np.float64,
    shape=_medium_shape_strategy,
    elements=_reasonable_numbers_config,
)

_large_data_config = dict(
    dtype=np.float64,
    shape=_large_shape_strategy,
    elements=_reasonable_numbers_config,
)


def _data_and_samples(draw, data_config):
    data = draw(hen.arrays(**data_config))
    samples = draw(hypothesis.strategies.integers(min_value=1, max_value=len(data) - 1))
    return data, samples


@hypothesis.strategies.composite
def small_data_and_samples(draw):
    return _data_and_samples(draw, _small_data_config)


@hypothesis.strategies.composite
def medium_data_and_samples(draw):
    return _data_and_samples(draw, _medium_data_config)


@hypothesis.strategies.composite
def large_data_and_samples(draw):
    return _data_and_samples(draw, _large_data_config)


####################
####################
## property tests ##
####################
####################


##########################
# brute_force_id correct #
##########################


@pytest.mark.property
def test_cube_manual(true_ids_cube):
    _, brute_force_id, manual_id = true_ids_cube
    assert_allclose(brute_force_id, manual_id)


#########################################
# original_idim_exact ~= brute_force_id #
#########################################


@pytest.mark.property
def test_cube_exact(true_ids_cube, workers):
    size, _, manual_id = true_ids_cube
    data = generate_cube_data(size)
    output = original_idim_exact(data, workers=workers, disable_tqdm=True)
    assert_allclose(output, manual_id)


@pytest.mark.property
@hypothesis.given(data=hen.arrays(**_small_data_config))
@hypothesis.settings(
    deadline=None,
    derandomize=True,
)
def test_hypothesis_original_idim_exact(request, data, workers):
    dim = cached_idim_brute_force(request, data, disable_tqdm=True)
    output = original_idim_exact(data, workers=workers, disable_tqdm=True)
    assert_allclose(output, dim)


##########################################
# original_idim_approx ~= brute_force_id #
##########################################


@pytest.mark.property
def test_cube_approx(true_ids_cube, workers):
    size, _, manual_id = true_ids_cube
    data = generate_cube_data(size)
    a, b = original_idim_approx(data, size // 2, workers=workers, disable_tqdm=True)
    assert_bounds(a, manual_id, b)


@pytest.mark.property
@hypothesis.given(das=small_data_and_samples())
@hypothesis.settings(
    deadline=None,
    derandomize=True,
)
def test_hypothesis_original_idim_approx(request, das, workers):
    data, samples = das
    dim = cached_idim_brute_force(
        request,
        data,
        disable_tqdm=True,
    )
    a, b = original_idim_approx(
        data,
        samples,
        workers=workers,
        disable_tqdm=True,
    )
    assert_bounds(a, dim, b)


#####################################
# original_approx -> original_exact #
#####################################


@pytest.mark.property
@hypothesis.given(das=medium_data_and_samples())
@hypothesis.settings(
    deadline=None,
    derandomize=True,
)
def test_hypothesis_original_exact_approx(request, das, workers):
    data, samples = das
    dim = cached_original_idim_exact(
        request,
        data,
        workers=workers,
        disable_tqdm=True,
    )
    _, _, dim_ = original_idim_approx(
        data,
        num_samples=samples,
        exact=True,
        workers=workers,
        disable_tqdm=True,
    )
    assert_allclose(dim, dim_)


####################################
# cid exact ~= original_idim_exact #
####################################


@pytest.mark.property
@hypothesis.given(data=hen.arrays(**_medium_data_config))
@hypothesis.settings(
    deadline=None,
    derandomize=True,
)
def test_hypothesis_cid_exact(request, data, workers):
    dim = cached_original_idim_exact(
        request,
        data,
        workers=workers,
        disable_tqdm=True,
    )
    output = calculate_intrinsic_dimension(
        data,
        workers=workers,
        disable_tqdm=True,
    )
    assert_allclose(output, dim)


######################################
# cid approx ~= original_idim_approx #
######################################


@pytest.mark.property
@hypothesis.given(das=medium_data_and_samples())
@hypothesis.settings(
    deadline=None,
    derandomize=True,
)
def test_hypothesis_cid_approx(request, das, workers):
    data, samples = das
    dim = cached_original_idim_approx(
        request,
        data,
        num_samples=samples,
        workers=workers,
        disable_tqdm=True,
    )
    output = calculate_intrinsic_dimension(
        data,
        support_sequence=samples,
        workers=workers,
        disable_tqdm=True,
    )
    assert_allclose(output[0], dim[0])
    assert_allclose(output[1], dim[1])


##################################################
# cid approx exact ~= original_idim_approx exact #
##################################################


@pytest.mark.property
@hypothesis.given(das=medium_data_and_samples())
@hypothesis.settings(
    deadline=None,
    derandomize=True,
)
def test_hypothesis_cid_original_approx_exact(request, das, workers):
    data, samples = das
    dim = cached_original_idim_approx(
        request,
        data,
        num_samples=samples,
        exact=True,
        workers=workers,
        disable_tqdm=True,
    )
    output = calculate_intrinsic_dimension(
        data,
        support_sequence=samples,
        exact=True,
        workers=workers,
        disable_tqdm=True,
    )
    assert_allclose(output[0], dim[2])


######################
# single == parallel #
######################


@pytest.mark.property
@hypothesis.given(data=hen.arrays(**_medium_data_config))
def test_hypothesis_feature_sequences_workers(data):
    fs = calculate_feature_sequences(
        data,
        workers=False,
        disable_tqdm=True,
    )
    fs_ = calculate_feature_sequences(
        data,
        workers=True,
        disable_tqdm=True,
    )
    assert_allclose(fs, fs_)


@pytest.mark.property
@hypothesis.given(data=hen.arrays(**_medium_data_config))
def test_hypothesis_cid_exact_workers(request, data):
    dim_s = calculate_intrinsic_dimension(
        data,
        workers=False,
        disable_tqdm=True,
    )
    dim_p = calculate_intrinsic_dimension(
        data,
        workers=True,
        disable_tqdm=True,
    )
    assert_allclose(dim_s, dim_p)


@pytest.mark.property
@hypothesis.given(das=medium_data_and_samples())
def test_hypothesis_cid_approx_workers(request, das):
    data, samples = das
    dim_s = calculate_intrinsic_dimension(
        data,
        support_sequence=samples,
        workers=False,
        disable_tqdm=True,
    )
    dim_p = calculate_intrinsic_dimension(
        data,
        support_sequence=samples,
        workers=True,
        disable_tqdm=True,
    )
    assert_allclose(dim_s, dim_p)


##############################
# lower < lower_more_samples #
# upper_more_samples < upper #
##############################


@hypothesis.strategies.composite
def medium_data_and_samples_and_more_samples(draw):
    data, samples = _data_and_samples(draw, _medium_data_config)
    hypothesis.assume(samples != len(data) - 1)
    more_samples = draw(
        hypothesis.strategies.integers(
            min_value=samples,
            max_value=len(data) - 1,
        )
    )
    return data, samples, more_samples


@pytest.mark.property
@hypothesis.given(dasams=medium_data_and_samples_and_more_samples())
@hypothesis.settings(
    deadline=None,
    derandomize=True,
)
def test_hypothesis_approximation_monotonicity(request, dasams, workers):
    data, samples, more_samples = dasams
    lower_a, upper_a, _ = cached_cid(
        request,
        data,
        support_sequence=samples,
        workers=workers,
        disable_tqdm=True,
    )
    lower_b, upper_b, _ = cached_cid(
        request,
        data,
        support_sequence=more_samples,
        workers=workers,
        disable_tqdm=True,
    )
    assert_bounds(lower_a, lower_b, lower_b)
    assert_bounds(upper_b, upper_b, upper_a)


###########################
# cid approx -> cid exact #
###########################


@pytest.mark.property
@hypothesis.given(das=medium_data_and_samples())
@hypothesis.settings(
    deadline=None,
    derandomize=True,
)
def test_hypothesis_cid_exact_approx(request, das, workers):
    data, samples = das
    (dim,) = calculate_intrinsic_dimension(
        data,
        workers=workers,
        disable_tqdm=True,
    )
    dim_, _, _ = calculate_intrinsic_dimension(
        data,
        support_sequence=samples,
        exact=True,
        workers=workers,
        disable_tqdm=True,
    )
    assert_allclose(dim, dim_)


#########################
# lower < exact < upper #
#########################


@pytest.mark.slow
@pytest.mark.property
@hypothesis.given(das=large_data_and_samples())
@hypothesis.settings(
    deadline=None,
    derandomize=True,
)
def test_hypothesis_cid(request, das, workers):
    data, samples = das
    lower, upper, _ = cached_cid(
        request,
        data,
        support_sequence=samples,
        workers=workers,
        disable_tqdm=True,
    )
    (dim,) = cached_cid(
        request,
        data,
        workers=workers,
        disable_tqdm=True,
    )
    assert_bounds(lower, dim, upper)


def samples_to_approximation(samples, len_data, epsilon=None):
    if epsilon is None:
        epsilon = 10 ** (-10)
    approximation_threshold = 0
    approximation_factor = samples / len_data
    if int(approximation_factor * len_data) != samples:
        approximation_factor = samples / (len_data - epsilon)
    assert int(approximation_factor * len_data) == samples
    return approximation_threshold, approximation_factor


@pytest.mark.slow
@pytest.mark.property
@hypothesis.given(das=large_data_and_samples())
@hypothesis.settings(
    deadline=None,
    derandomize=True,
)
def test_hypothesis_idim(request, das, workers):
    data, samples = das
    at, af = samples_to_approximation(samples, len(data))
    lower, upper = cached_original_idim_approx(
        request,
        data,
        num_samples=samples,
        workers=workers,
        disable_tqdm=True,
    )
    dim = (upper + lower) / 2
    dim_ = idim(
        data,
        at,
        af,
        workers=workers,
        disable_tqdm=True,
    )
    assert_allclose(dim_, dim)


###################
# more properties #
###################


@pytest.mark.property
@hypothesis.given(hen.arrays(**_medium_data_config))
def test_hypothesis_obs_diam_invariance(data):
    data_ = normalize_observable_diameter(data)
    assert_allclose(data_, normalize_observable_diameter(data_))


def _test_verify(callback, *args, **kwargs):
    dim = callback(*args, verify=False, **kwargs)
    dim_ = callback(*args, verify=True, **kwargs)
    assert_allclose(dim, dim_)


@pytest.mark.property
@hypothesis.given(hen.arrays(**_medium_data_config))
def test_hypothesis_ciwossffs_verify(data):
    _test_verify(
        calculate_id_without_support_sequence_from_feature_sequences,
        data,
        disable_tqdm=True,
    )


@pytest.mark.property
@hypothesis.given(medium_data_and_samples())
def test_hypothesis_ciwssffs_verify(das):
    data, samples = das
    support_sequence = support_sequence_factory(
        data,
        samples,
        "numpy",
        False,
    )
    _test_verify(
        calculate_id_with_support_sequence_from_feature_sequences,
        data,
        support_sequence=support_sequence,
        disable_tqdm=True,
    )


@pytest.mark.property
@hypothesis.given(hen.arrays(**_medium_data_config))
def test_hypothesis_cid_verify(data):
    _test_verify(
        calculate_intrinsic_dimension,
        data,
        disable_tqdm=True,
    )


@pytest.mark.property
@hypothesis.given(hen.arrays(**_medium_data_config))
@hypothesis.settings(
    deadline=None,
)
def test_hypothesis_cid_exact_serial_fs(data):
    dim = calculate_intrinsic_dimension(
        data,
        serial_feature_sequences=False,
        workers=True,
        disable_tqdm=True,
    )
    dim_ = calculate_intrinsic_dimension(
        data,
        serial_feature_sequences=True,
        workers=True,
        disable_tqdm=True,
    )
    assert_allclose(dim, dim_)


@pytest.mark.property
@hypothesis.given(medium_data_and_samples())
@hypothesis.settings(
    deadline=None,
)
def test_hypothesis_cid_approx_serial_fs(das):
    data, samples = das
    dim = calculate_intrinsic_dimension(
        data,
        support_sequence=samples,
        serial_feature_sequences=False,
        workers=True,
        disable_tqdm=True,
    )
    dim_ = calculate_intrinsic_dimension(
        data,
        support_sequence=samples,
        serial_feature_sequences=True,
        workers=True,
        disable_tqdm=True,
    )
    assert_allclose(dim, dim_)


@pytest.mark.property
@hypothesis.given(
    hen.array_shapes(min_dims=0, max_dims=0, max_side=100),
)
def test_hypothesis_idim_empty_shape_fail(shape):
    data = np.zeros(shape)
    with pytest.raises(TypeError):
        idim(data, disable_tqdm=True)


@pytest.mark.property
@hypothesis.given(
    hen.array_shapes(min_dims=1, max_dims=1, max_side=100),
)
def test_hypothesis_idim_one_dim_shape_fail(shape):
    data = np.zeros(shape)
    with pytest.raises(ValueError):
        idim(data, disable_tqdm=True)


@pytest.mark.property
@hypothesis.given(
    hen.array_shapes(min_dims=2, max_dims=2, max_side=100),
)
def test_hypothesis_idim_inf_dim_for_zero_data(shape):
    data = np.zeros(shape)
    output = idim(data, disable_tqdm=True)
    assert output == float("inf")


def _test_equal_idim(data_a, data_b, **kwargs):
    dim_a = idim(data_a, **kwargs)
    dim_b = idim(data_b, **kwargs)
    assert_allclose(dim_a, dim_b)


@pytest.mark.property
@hypothesis.given(
    hen.arrays(**_medium_data_config),
    hypothesis.strategies.floats(**_reasonable_numbers_config),
)
@hypothesis.settings(
    derandomize=True,
)
def test_hypothesis_idim_scale_invariance(data, x):
    hypothesis.assume(x != 0.0)
    _test_equal_idim(
        data,
        data * x,
        disable_tqdm=True,
    )


@pytest.mark.property
@hypothesis.given(
    hen.arrays(**_medium_data_config),
    hypothesis.strategies.floats(**_reasonable_numbers_config),
)
@hypothesis.settings(
    derandomize=True,
)
def test_hypothesis_idim_shift_invariance(data, x):
    hypothesis.assume(x != 0.0)
    _test_equal_idim(
        data,
        data + x,
        disable_tqdm=True,
    )


@hypothesis.strategies.composite
def data_and_permutation(draw):
    data = draw(hen.arrays(**_medium_data_config))
    row_perm = draw(hypothesis.strategies.permutations(range(data.shape[0])))
    col_perm = draw(hypothesis.strategies.permutations(range(data.shape[1])))
    return data, row_perm, col_perm


@pytest.mark.property
@hypothesis.given(data_and_permutation())
def test_hypothesis_idim_row_permutation(dup):
    data, row_perm, _ = dup
    _test_equal_idim(
        data,
        data[row_perm],
        disable_tqdm=True,
    )


@pytest.mark.property
@hypothesis.given(data_and_permutation())
def test_hypothesis_idim_col_permutation(dup):
    data, _, col_perm = dup
    _test_equal_idim(
        data,
        data[:, col_perm],
        disable_tqdm=True,
    )


# @pytest.mark.property
# @hypothesis.given(data_and_permutation())
# def test_hypothesis_idim_row_copy(dup):
#    data, row_perm, _ = dup
#    _data = np.concatenate((data, data[row_perm[0]][np.newaxis, :]))
#    _test_equal_idim(
#        data,
#        _data,
#        disable_tqdm=True,
#    )


@pytest.mark.property
@hypothesis.given(data_and_permutation())
def test_hypothesis_idim_col_copy(dup):
    data, _, col_perm = dup
    _data = np.column_stack((data, data[:, col_perm[0]][:, np.newaxis]))
    _test_equal_idim(
        data,
        _data,
        disable_tqdm=True,
    )
