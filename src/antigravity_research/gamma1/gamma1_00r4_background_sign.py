"""GAMMA1-00R4: on-background portal-gradient sign, with falsifying controls.

This is a restricted canonical-lattice analysis of R3 replay arrays.
It neither solves Einstein gravity nor derives force on Earth or whole craft.
Coordinate radii are canonical grid values, not SI metres or stand-off.
"""
from __future__ import annotations

import hashlib
from pathlib import Path
import numpy as np

EXPECTED_PROFILE_SHA = (
    '94d3763a8d7705ab3dc8774310cf3b8bba96557a0b80d2c34aa110d00b840d54'
)
EXPECTED_R3_SHA = (
    '192fb12a39294dfea3035605375aab6cd5591d1fb51ddbce8924ca78aa041287'
)
EXPECTED_R3_VERIFY_SHA = (
    'a7014cfc54de6a4d0048239a897cb73b7f5db4e25d897e70c9a2c259e0f98a8c'
)
EXPECTED_PH16_SOURCE_SHA = (
    'b5468671f6418fad7b6ed01d916ea65a95a1d59252b84d4411beed9709f86df0'
)

KEYS = {
    'F_plus', 'F_minus', 'A_X', 'A_Y',
    'rho', 'z', 'weights',
    'E_X_r', 'E_X_z', 'B_Y_r', 'B_Y_z',
    'P', 'sigma', 'neutral_n', 'joint_gradient',
}


def sha(path):
    path = Path(path)
    return (
        hashlib.sha256(path.read_bytes()).hexdigest()
        if path.is_file()
        else 'MISSING'
    )


def grid_d1(n: int, h: float) -> np.ndarray:
    """Independent reconstruction of PH16 central/edge derivative."""
    if n < 5 or not (np.isfinite(h) and h > 0):
        raise ValueError('invalid grid')

    matrix = np.zeros((n, n), dtype=float)

    for i in range(1, n-1):
        matrix[i, i-1] = -0.5/h
        matrix[i, i+1] = +0.5/h

    matrix[0, 0] = -1/h
    matrix[0, 1] = +1/h
    matrix[-1, -2] = -1/h
    matrix[-1, -1] = +1/h

    return matrix


def checked_profile(
    file_path,
    expected_sha=EXPECTED_PROFILE_SHA
):
    path = Path(file_path)

    if sha(path) != expected_sha:
        raise ValueError(
            'R3 native array SHA mismatch or missing archive'
        )

    with np.load(path, allow_pickle=False) as archive:
        if set(archive.files) != KEYS:
            raise ValueError(
                'R3 native array keys changed'
            )

        arrays = {
            key: archive[key].copy()
            for key in KEYS
        }

    n = 288

    for key, array in arrays.items():
        expected_shape = (
            (4*n,)
            if key == 'joint_gradient'
            else (n,)
        )

        if (
            array.shape != expected_shape
            or not np.isfinite(array).all()
        ):
            raise ValueError(
                'Array shape or finiteness failed: '+key
            )

    if (
        np.any(arrays['weights'] <= 0)
        or np.any(arrays['neutral_n'] <= 0)
    ):
        raise ValueError(
            'Nonpositive neutral density or weights'
        )

    return arrays


def _counts(values, mask, threshold=0.):
    selected = values[mask]

    if not selected.size:
        return {
            'samples': 0,
            'outward': 0,
            'inward': 0,
            'zero': 0,
            'min': None,
            'max': None,
        }

    return {
        'samples': int(selected.size),
        'outward': int(np.count_nonzero(selected > threshold)),
        'inward': int(np.count_nonzero(selected < -threshold)),
        'zero': int(np.count_nonzero(abs(selected) <= threshold)),
        'min': float(np.min(selected)),
        'max': float(np.max(selected)),
    }


def inspect(arrays):
    """Signed portal-only local gradient of the native stationary profile."""
    nr, nz, h = 12, 24, 1.

    rho = arrays['rho']
    z = arrays['z']
    weights = arrays['weights']

    if not (
        np.allclose(
            rho.reshape(nr, nz),
            np.arange(.5, 12., 1.)[:, None]
        )
        and np.allclose(
            z.reshape(nr, nz),
            np.arange(-11.5, 12., 1.)[None, :]
        )
    ):
        raise ValueError(
            'Native coordinate indexing does not match 12/L12 grid'
        )

    D_r = np.kron(
        grid_d1(nr, h),
        np.eye(nz)
    )

    D_z = np.kron(
        np.eye(nr),
        grid_d1(nz, h)
    )

    AX = arrays['A_X']
    AY = arrays['A_Y']

    Er = -(D_r@AX)
    Ez = -(D_z@AX)

    Br = -(D_z@AY)
    Bz = (D_r@(rho*AY))/rho

    components = {
        'E_X_r': Er,
        'E_X_z': Ez,
        'B_Y_r': Br,
        'B_Y_z': Bz,
    }

    residuals = {
        key: float(np.max(abs(value-arrays[key])))
        for key, value in components.items()
    }

    if max(residuals.values()) > 2.e-12:
        raise AssertionError(
            'Independent native field stencil mismatch '
            +str(residuals)
        )

    P = Er*Br+Ez*Bz

    sigma = (
        .05*P
        -40.*P*P
    )

    if not np.allclose(
        P,
        arrays['P'],
        rtol=2.e-12,
        atol=2.e-14
    ):
        raise AssertionError(
            'P from native potentials mismatch'
        )

    if not np.allclose(
        sigma,
        arrays['sigma'],
        rtol=2.e-12,
        atol=2.e-14
    ):
        raise AssertionError(
            'sigma from native potentials mismatch'
        )

    # Neutral hydrostatic constraint:
    # The fixed inventory remains the PH16 n0=0.15.
    C = (
        .5*.15*np.sum(weights)
        +np.sum(weights*np.exp(3*sigma))
    )/np.sum(weights*np.exp(2*sigma))

    neutral_n = (
        C*np.exp(-sigma)-1.
    )/.5

    neutral_error = float(
        np.max(
            abs(neutral_n-arrays['neutral_n'])
        )
    )

    if neutral_error > 2.e-12:
        raise AssertionError(
            'Neutral hydrostatic formula mismatch'
        )

    # Restricted static portal term:
    # a_sigma / c^2 = -grad sigma.
    #
    # NOT the total Einstein+portal acceleration.
    # NOT SI acceleration without physical length normalization.

    ar = -(D_r@sigma)
    az = -(D_z@sigma)

    radius = np.hypot(rho, z)

    projected = (
        rho*ar+z*az
    )/radius

    mask_inner = radius < 6.
    mask_outer = radius >= 6.

    grid_indices = np.indices((nr, nz))

    interior = (
        (grid_indices[0] >= 1)
        &(grid_indices[0] < nr-1)
        &(grid_indices[1] >= 1)
        &(grid_indices[1] < nz-1)
    ).ravel()

    deep = (
        (grid_indices[0] >= 2)
        &(grid_indices[0] < nr-2)
        &(grid_indices[1] >= 2)
        &(grid_indices[1] < nz-2)
    ).ravel()

    # Fourth-order centered five-point stencil.
    # Only defined at least two cells from each box edge.

    sigma2 = sigma.reshape(nr, nz)

    ar4 = np.zeros_like(sigma2)
    az4 = np.zeros_like(sigma2)

    ar4[2:-2, :] = -(
        sigma2[:-4, :]
        -8*sigma2[1:-3, :]
        +8*sigma2[3:-1, :]
        -sigma2[4:, :]
    )/(12*h)

    az4[:, 2:-2] = -(
        sigma2[:, :-4]
        -8*sigma2[:, 1:-3]
        +8*sigma2[:, 3:-1]
        -sigma2[:, 4:]
    )/(12*h)

    projected4 = (
        rho*ar4.ravel()
        +z*az4.ravel()
    )/radius

    # Operator-off negative controls, not self-consistent
    # re-solved source-off PH16 states.

    null_coupling = np.zeros_like(P)

    null_carrier = (
        .05*np.zeros_like(P)
        -40*np.zeros_like(P)**2
    )

    for null in (
        null_coupling,
        null_carrier
    ):
        if (
            np.any(null != 0)
            or np.any(D_r@null != 0)
            or np.any(D_z@null != 0)
        ):
            raise AssertionError(
                'Negative-control portal failed to switch off'
            )

    outer_box = (
        (grid_indices[0] == nr-1)
        |(grid_indices[1] == 0)
        |(grid_indices[1] == nz-1)
    ).ravel()

    axis_inner = (
        grid_indices[0] == 0
    ).ravel()

    radial_bins = {}

    for lo, hi in [
        (0., 2.),
        (2., 4.),
        (4., 6.),
        (6., 8.),
        (8., 10.),
        (10., 12.),
        (12., float('inf')),
    ]:
        key = (
            f'{int(lo)}_to_{int(hi)}'
            if np.isfinite(hi)
            else '12_and_above'
        )

        radial_bins[key] = _counts(
            projected,
            (radius >= lo)&(radius < hi)
        )

    return {
        'scope':
            'CANONICAL_12x24_STATIONARY_PROFILE_PORTAL_ONLY_NO_EINSTEIN',

        'grid': {
            'nr': nr,
            'nz': nz,
            'N': nr*nz,
            'h_canonical': h,

            'center_definition':
                '(rho=0,z=0) model symmetry center, NOT craft COM',
        },

        'native_reconstruction_max_abs_error':
            residuals,

        'neutral_hydrostatic_max_abs_error':
            neutral_error,

        'neutral_mu_constant_canonical':
            float(C),

        'native_grad_L2':
            float(
                np.linalg.norm(
                    arrays['joint_gradient']
                )
            ),

        'signed_P_counts': {
            'positive':
                int((P > 0).sum()),

            'negative':
                int((P < 0).sum()),

            'zero':
                int((P == 0).sum()),
        },

        'sigma_range': {
            'min': float(sigma.min()),
            'max': float(sigma.max()),
        },

        'portal_radial_projected_a_over_c2': {
            'full_mesh':
                _counts(
                    projected,
                    np.ones(nr*nz, bool)
                ),

            'r_less_6':
                _counts(
                    projected,
                    mask_inner
                ),

            'r_at_least_6':
                _counts(
                    projected,
                    mask_outer
                ),

            'interior_r_at_least_6':
                _counts(
                    projected,
                    interior&mask_outer
                ),

            'deep_interior_fourth_order_r_at_least_6':
                _counts(
                    projected4,
                    deep&mask_outer
                ),

            'radial_bins':
                radial_bins,

            'outward_weight_fraction_full_grid':
                float(
                    np.sum(weights[projected > 0])
                    /np.sum(weights)
                ),
        },

        'boundary_diagnostics': {
            'outer_box_cell_count':
                int(outer_box.sum()),

            'outer_box_max_abs_sigma':
                float(
                    np.max(abs(sigma[outer_box]))
                ),

            'outer_box_max_source_amplitude':
                float(
                    max(
                        np.max(
                            abs(arrays['F_plus'][outer_box])
                        ),
                        np.max(
                            abs(arrays['F_minus'][outer_box])
                        )
                    )
                ),

            'inner_axis_cell_count':
                int(axis_inner.sum()),

            'inner_axis_max_abs_sigma':
                float(
                    np.max(abs(sigma[axis_inner]))
                ),

            'box_is_exterior_solved':
                False,

            'continuum_or_outer_boundary_convergence':
                'NOT_TESTED',
        },

        'negative_controls': {
            'alpha_beta_both_off_sigma_and_gradient':
                'ZERO_EXACT',

            'both_X_Y_fields_off_sigma_and_gradient':
                'ZERO_EXACT',

            'prescribed_source_off':
                'NOT_A_CONSERVED_RE_SOLVED_CONTROL',

            'Earth_off':
                'NO_EARTH_VARIABLE_IN_PH16',

            'stand_off':
                'COORDINATE_RADIUS_NOT_METERS',
        },

        'necessary_status': {
            'actual_canonical_background_portal_gradient_sign':
                'EVALUATED',

            'source_independent_outward_sign':
                'NOT_ESTABLISHED',

            'full_test_torus_outward_throughout':
                'NOT_TESTED',

            'physical_metric_Einstein_contribution':
                'NOT_SOLVED',

            'recoil_Earth_down_whole_craft_up':
                'NOT_DERIVED',

            'coupled_Lorentzian_mode_health':
                'NOT_CERTIFIED',

            'complete_energy_lt10MJ':
                'NOT_CERTIFIED',

            'true_exterior_convergence':
                'NOT_CERTIFIED',
        },
    }
