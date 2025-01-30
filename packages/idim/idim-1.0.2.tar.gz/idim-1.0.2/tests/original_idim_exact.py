import functools
from multiprocessing import Pool

import numpy as np
from tqdm import tqdm


def obs_diam(X):
    return np.max(np.max(X, axis=0) - np.min(X, axis=0))


def create_lf(i, X):
    return np.sort(X[:, i])


def phi_fj(j, lf):
    return np.min(lf[j - 1 :] - lf[: 1 - j])


def phi_j(j, lfs):
    return np.max([phi_fj(j, lf) for lf in lfs])


def is_mult(workers, disable_print=False):
    if (
        workers is None
        or (isinstance(workers, bool) and not workers)
        or (isinstance(workers, int) and workers == 0)
    ):
        if not disable_print:
            print("no multiprocessing")
        return False
    if not disable_print:
        print("multiprocessing")
    return True


def original_idim_exact(data, workers=None, disable_tqdm=False):
    d = obs_diam(data)
    # print(f"{d=}")
    if d == 0.0:
        X = data
    else:
        X = data / d
    # print(f"{X=}")

    func = functools.partial(create_lf, X=X)
    if is_mult(workers, disable_print=disable_tqdm):
        with Pool(workers) as p:
            lfs = np.array(
                [
                    r
                    for r in tqdm(
                        p.imap(func, range(X.shape[1])),
                        total=X.shape[1],
                        disable=disable_tqdm,
                    )
                ]
            )
    else:
        lfs = np.array(
            [
                func(r)
                for r in tqdm(
                    range(X.shape[1]),
                    total=X.shape[1],
                    disable=disable_tqdm,
                )
            ]
        )
    # print(f"{lfs=}")

    func = functools.partial(phi_j, lfs=lfs)
    if is_mult(workers, disable_print=disable_tqdm):
        with Pool(workers) as p:
            phis = np.array(
                [
                    t
                    for t in tqdm(
                        p.imap(func, range(2, X.shape[0] + 1)),
                        total=X.shape[0] - 1,
                        disable=disable_tqdm,
                    )
                ]
            )
    else:
        phis = np.array(
            [
                func(t)
                for t in tqdm(
                    range(2, X.shape[0] + 1),
                    total=X.shape[0] - 1,
                    disable=disable_tqdm,
                )
            ]
        )
    # print(f"{phis=}")
    delta = np.sum(phis) / len(X)
    # print(f"{delta=}")
    if delta == 0.0:
        dim = np.array(float("inf"))
    else:
        dim = 1 / (delta**2)
    # print(f"{dim=}")
    return dim
