import functools
from multiprocessing import Pool

import numpy as np
from tqdm import tqdm


def obs_diam(X):
    return np.max(np.max(X, axis=0) - np.min(X, axis=0))


def create_lf(i, X):
    return np.sort(X[:, i])


def phi_fj(lf, j):
    return np.min(lf[j - 1 :] - lf[: 1 - j])


def phi_j(j, lfs):
    return np.array([phi_fj(lf, j) for lf in lfs])


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


def original_idim_approx(
    data, num_samples, exact=False, workers=None, disable_tqdm=False
):
    d = obs_diam(data)
    if d == 0.0:
        X = data
    else:
        X = data / d
    n = len(X)
    samples = list(n + 2 - np.geomspace(n, 2, num_samples))
    samples = [int(x) for x in samples]
    samples = sorted(list(set(samples)))
    if samples[0] != 2:
        samples = [2] + samples
    if samples[-1] != n:
        samples.append(n)
    # print(f"{len(samples)=}")

    _create_lf = functools.partial(create_lf, X=X)

    if is_mult(workers, disable_print=disable_tqdm):
        with Pool(workers) as p:
            lfs = np.array(
                [
                    lf
                    for lf in tqdm(
                        p.imap(_create_lf, range(X.shape[1])),
                        total=X.shape[1],
                        disable=disable_tqdm,
                    )
                ]
            )
    else:
        lfs = np.array(
            [
                _create_lf(r)
                for r in tqdm(
                    range(X.shape[1]),
                    total=X.shape[1],
                    disable=disable_tqdm,
                )
            ]
        )

    # print("lfs", lfs)

    _phi_j = functools.partial(phi_j, lfs=lfs)

    max_phi = 0  # phi_j for the last support phi_j
    phi_js = []  # store al phi_js
    phi_sets = []  # store for each j which features have to be considered

    if is_mult(workers, disable_print=disable_tqdm):
        with Pool(workers) as p:
            for phi_lfs in tqdm(
                p.imap(_phi_j, samples),
                total=len(samples),
                disable=disable_tqdm,
            ):
                phi_sets.append(np.where(phi_lfs > max_phi)[0])
                max_phi = np.max(phi_lfs)
                phi_js.append(max_phi)
    else:
        for t in tqdm(
            samples,
            total=len(samples),
            disable=disable_tqdm,
        ):
            phi_lfs = _phi_j(t)
            phi_sets.append(np.where(phi_lfs > max_phi)[0])
            max_phi = np.max(phi_lfs)
            phi_js.append(max_phi)

    phi_sets = phi_sets[1:]

    phi_js = np.array(phi_js)
    # print("phi_js", phi_js)

    # print("Compute Error")
    S = np.array(samples)
    gaps = S[1:] - S[:-1]
    # print("gaps", gaps)
    min_Delta = (np.sum(phi_js[:-1] * gaps) + phi_js[-1]) * (1 / n)
    max_Delta = (np.sum(phi_js[1:] * gaps) + phi_js[0]) * (1 / n)
    if min_Delta == 0.0:
        max_Dim = np.array(float("inf"))
    else:
        max_Dim = 1 / (min_Delta**2)
    if max_Delta == 0.0:
        min_Dim = np.array(float("inf"))
    else:
        min_Dim = 1 / (max_Delta**2)

    # print("Compute Costs")
    # pre_costs = np.sum([len(lfs) * cost(n, s) for s in samples])
    # phi_sets = phi_sets[1:]
    # full_gap_costs = np.array([gap_costs(n, x, y) for x, y in zip(S, S[1:])])
    # full_gap_costs = np.array([len(s) for s in phi_sets]) * full_gap_costs
    # full_gap_costs = np.sum(full_gap_costs)
    # costs_full_computation = len(lfs) * ((n**2/2) - (n/2))
    # skipped_costs = 1 - ((pre_costs + full_gap_costs) / costs_full_computation)
    # print("Skipped costs:", skipped_costs)

    if exact:
        Dim = original_approx_to_exact(
            lfs,
            n,
            samples,
            phi_sets,
            phi_js,
            workers,
            disable_tqdm,
        )
        return min_Dim, max_Dim, Dim

    return min_Dim, max_Dim


def phi_t(t, lfs):
    i, j, current_lfs, default = t
    gap = range(i + 1, j)
    values = np.array([[phi_fj(lfs[i], j) for i in current_lfs] for j in gap])
    # print(i, j, current_lfs, default, values)
    if len(values):
        return np.max(values, axis=1, initial=default)
    return []


def original_approx_to_exact(
    lfs, n, samples, phi_indices, phi_js, workers, disable_tqdm
):
    max_phis = []

    _phi_t = functools.partial(phi_t, lfs=lfs)
    if is_mult(workers, disable_print=disable_tqdm):
        with Pool(workers) as p:
            for d_list in tqdm(
                p.imap(_phi_t, zip(samples, samples[1:], phi_indices, phi_js)),
                total=len(phi_indices),
                disable=disable_tqdm,
            ):
                max_phis.extend(d_list)
    else:
        for t in tqdm(
            zip(samples, samples[1:], phi_indices, phi_js),
            total=len(phi_indices),
            disable=disable_tqdm,
        ):
            d_list = _phi_t(t)
            max_phis.extend(d_list)

    # print(f"{max_phis=}")
    # print(f"{len(max_phis)=}")
    # print(f"{phi_js=}")
    # print(f"{len(phi_js)=}")
    all_phi_js = np.concatenate([phi_js, max_phis])
    Delta = np.sum(all_phi_js)
    Delta /= n
    if Delta == 0.0:
        Dim = np.array(float("inf"))
    else:
        Dim = 1.0 / (Delta**2)
    return Dim
