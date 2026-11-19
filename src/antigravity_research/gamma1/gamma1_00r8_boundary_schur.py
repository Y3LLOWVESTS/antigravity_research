"""R8: finite exterior, self-adjoint Schur reduction of P8 weighted FV Maxwell form.

No reconstructed Einstein metric, source solve, Lorentzian health, complete
energy or force. The finite outer Dirichlet condition is not infinity.
"""
from __future__ import annotations

import hashlib
from functools import lru_cache
from pathlib import Path

import numpy as np
from scipy import sparse
from scipy.sparse.linalg import splu

PH16_SHA = 'b5468671f6418fad7b6ed01d916ea65a95a1d59252b84d4411beed9709f86df0'
P8_SHA = '406aa58db3092d2392adbb78429257538fd51a202f472fd49b3a08862a934fed'
P10_SHA = '25e564a6dbbd4658f6154781db610738b8ed1114aa0f8fe71bf4ab91092fdddb'
R3_SHA = '94d3763a8d7705ab3dc8774310cf3b8bba96557a0b80d2c34aa110d00b840d54'
R7_SHA = '87037cbc138ad86bdb4a57e87b7d12228cd0054878b2bc79509b51f9f22cb1bc'
R7_VERIFY_SHA = 'febe1980b4a9208fb5b47b167ee9ff42d4cab4b4f1956130dd01917ad04c17c3'

EXTENTS = (14,18,24,30,36,48,60)
BASE_NR = 12
BASE_L = 12.


def sha(path):
    p = Path(path)
    return hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else 'MISSING'


def compare(K,L,v):
    """Record unfitted and fitted discrepancies; fitted values are diagnostics."""
    Kv = K@v
    Lv = L@v

    fit = float(np.sum(K*L)/np.sum(L*L))
    fit_field = float(np.dot(Kv,Lv)/np.dot(Lv,Lv))

    return {
      'matrix_relative_frobenius_best_scalar':
          float(np.linalg.norm(K-fit*L)/np.linalg.norm(K)),
      'matrix_best_scalar_DIAGNOSTIC_ONLY':fit,
      'native_gradient_relative_unscaled':
          float(np.linalg.norm(Kv-Lv)/np.linalg.norm(Kv)),
      'native_gradient_relative_best_scaled_DIAGNOSTIC_ONLY':
          float(np.linalg.norm(Kv-fit_field*Lv)/np.linalg.norm(Kv)),
      'native_gradient_best_scale_DIAGNOSTIC_ONLY':fit_field,
      'native_energy_K_over_schur':
          float(np.dot(v,Kv)/np.dot(v,Lv)),
    }


def extended_indices(ext):
    """Exact preservation of original rho/z cell centers in larger box."""
    if ext < 14 or int(ext) != ext:
        raise ValueError('Exterior needs at least two layers and integral nr')

    z0 = int(ext)-12

    ids = np.array(
        [
            r*(2*int(ext))+z0+z
            for r in range(12)
            for z in range(24)
        ],
        dtype=np.int64
    )
    return ids


@lru_cache(maxsize=9)
def exterior_schur(ext):
    """Eliminate exterior from local weighted FV action; no fitting.

    The exterior has zero Dirichlet data at outer box extent.
    Schur operator acts on the original 288 unknowns.
    """
    from antigravity_research.agminer.hook17_ph15_p8_electric_dipole import (
        Dipole, Spec,
    )

    m = Dipole(Spec(nr=ext,L=float(ext)))
    indices = extended_indices(ext)

    outside = np.setdiff1d(
        np.arange(m.cells),
        indices,
        assume_unique=True
    )

    if not (
        np.allclose(
            m.rho[indices],
            np.repeat(np.arange(.5,12.,1.),24)
        )
        and np.allclose(
            m.z[indices],
            np.tile(np.arange(-11.5,12.,1.),12)
        )
    ):
        raise AssertionError('Original cell centers not embedded exactly')

    W = sparse.diags(m.w)
    result = {}

    for name,term in [('X',False),('Y',True)]:
        additional = (
            sparse.diags(1./m.rho**2)
            if term
            else sparse.csr_matrix(m.L.shape)
        )

        operator = (
            W@(m.L+additional)
        ).tocsc()

        interior = operator[indices,:][:,indices].toarray()

        boundary_coupling = (
            operator[indices,:][:,outside]
        ).tocsr()

        rim = np.flatnonzero(
            boundary_coupling.getnnz(axis=1)
        )

        if rim.size != 46:
            raise RuntimeError('Invalid physical-box perimeter count')

        link = boundary_coupling[rim,:].toarray()

        exterior = operator[outside,:][:,outside].tocsc()

        free_solution = splu(exterior).solve(link.T)

        nonlocal_correction = link@free_solution

        reduced = interior.copy()
        reduced[np.ix_(rim,rim)] -= nonlocal_correction

        if np.max(abs(reduced-reduced.T)) > 4e-10:
            raise RuntimeError('Schur reciprocity broken')

        if min(np.linalg.eigvalsh(reduced)) <= 0:
            raise RuntimeError('Schur reduced action not positive')

        if min(np.linalg.eigvalsh(nonlocal_correction)) < -2e-9:
            raise RuntimeError('Exterior elimination not energy minimizing')

        result[name] = {
          'operator':reduced,
          'rim':rim,
          'correction':nonlocal_correction,
          'exterior_outer_unknowns':int(len(outside)),
          'exterior_size':int(m.cells),
        }

    if not np.array_equal(result['X']['rim'],result['Y']['rim']):
        raise AssertionError('Unmatched X/Y interface')

    return result


def analyze(native):
    from antigravity_research.ph16.ph16_04_joint_stationary import (
        CoulombSource, Spec, JointAction, Settings,
    )

    if (
        native['A_X'].shape != (288,)
        or native['A_Y'].shape != (288,)
    ):
        raise ValueError('Actual PH16 native profile required')

    m = CoulombSource(
        Spec(nr=12,L=12.),
        self_order=8
    )
    j = JointAction(
        m,
        Settings(nr=12,L=12.)
    )

    W = sparse.diags(m.w)

    base = {
      'X':(W@m.L).toarray(),
      'Y':(W@(m.L+sparse.diags(1/m.rho**2))).toarray(),
    }

    kernels = {
      'X':j.Kx,
      'Y':j.Ky,
    }

    fields = {
      'X':native['A_X'],
      'Y':native['A_Y'],
    }

    ref = {
        key:compare(kernels[key],base[key],fields[key])
        for key in ('X','Y')
    }

    series = []
    archive = {}
    rim_id = None

    for ext in EXTENTS:
        s = exterior_schur(ext)
        metrics = {}

        for key in ('X','Y'):
            red = s[key]['operator']
            rim = s[key]['rim']
            corr = s[key]['correction']

            off = np.setdiff1d(
                np.arange(288),
                rim,
                assume_unique=True
            )

            gap = base[key]-red

            offbound = float(
                max(
                    np.max(abs(gap[np.ix_(off,np.arange(288))])),
                    np.max(abs(gap[np.ix_(np.arange(288),off)]))
                )
            )

            if offbound > 1e-10:
                raise RuntimeError(
                    'EXTERIOR_EFFECT_NOT_CONFINED_TO_BOUNDARY_ROWS_'+key
                )

            if np.min(
                np.linalg.eigvalsh(
                    gap[np.ix_(rim,rim)]
                )
            ) <= -2e-9:
                raise RuntimeError(
                    'ORIGINAL_DIRICHLET_BOX_NOT_MORE_COSTLY_'+key
                )

            measurement = compare(
                kernels[key],
                red,
                fields[key]
            )

            measurement.update({
                'correction_only_on_box_rim':offbound<1e-10,
                'rim_cells':len(rim),
                'ext_cells':s[key]['exterior_size'],
                'ext_eliminated_cells':s[key]['exterior_outer_unknowns'],
                'boundary_energy_delta_negative_semidefinite':True,
                'schur_min_eigenvalue':float(
                    np.min(np.linalg.eigvalsh(red))
                ),
            })

            metrics[key] = measurement

            if ext in (24,60):
                archive[f'{key}_outer_{ext}_rim_correction'] = (
                    np.asarray(corr,dtype='<f8')
                )

                archive[f'{key}_outer_{ext}_native_gradient'] = (
                    np.asarray(red@fields[key],dtype='<f8')
                )

            if rim_id is None:
                rim_id = rim

        series.append({
          'outer_extent':ext,
          'boundary':'FINITE_OUTER_DIRICHLET_NOT_EXACT_INFINITY',
          'carriers':metrics,
        })

    archive['rim_indices'] = np.asarray(
        rim_id,
        dtype='<i8'
    )

    archive['X_green_native_gradient'] = np.asarray(
        j.Kx@fields['X'],
        dtype='<f8'
    )

    archive['Y_green_native_gradient'] = np.asarray(
        j.Ky@fields['Y'],
        dtype='<f8'
    )

    if not (
        ref['X']['native_gradient_relative_best_scaled_DIAGNOSTIC_ONLY'] > .95
        and ref['Y']['native_gradient_relative_best_scaled_DIAGNOSTIC_ONLY'] > .75
    ):
        raise RuntimeError('R7 native baseline drift')

    last = series[-1]['carriers']

    if not (
        last['X']['native_gradient_relative_best_scaled_DIAGNOSTIC_ONLY'] < .06
        and .15 < last['Y']['native_gradient_relative_best_scaled_DIAGNOSTIC_ONLY'] < .25
    ):
        raise RuntimeError(
            'DtN native improvement/plateau discrimination unexpected'
        )

    if not all(
        series[i+1]['carriers']['X'][
            'native_gradient_relative_best_scaled_DIAGNOSTIC_ONLY'
        ]
        <
        series[i]['carriers']['X'][
            'native_gradient_relative_best_scaled_DIAGNOSTIC_ONLY'
        ]
        for i in range(len(series)-1)
    ):
        raise RuntimeError('X exterior radius trend did not improve')

    return {
      'reference_local_dirichlet_native':ref,
      'finite_exterior_schur_sweep':series,
      'archive':archive,
      'negative_controls':{
        'boundary_coupling_removed':
            'RECOVERS_FIXED_BOX_DIRICHLET_BASELINE_ONLY_NOT_SCHUR',
        'finite_outer_dirichlet':
            'NOT_THE_INFINITE_EXTERIOR',
        'wrong_Y_without_rho_minus2':
            'REJECTED_BY_PRIOR_R7',
        'zero_field_exact_zero_action':
            'LINEAR_QUADRATIC_IDENTITY',
      },
      'scope':{
        'rank_of_added_boundary_interaction':
            'AT_MOST_46_OF_288; NO_CHANGE_TO_BULK_ROWS',
        'outer_sweep':
            'FIXED_H_1; CHANGES_OUTER_BOX_NOT_GRID_REFINEMENT',
        'physical_source_replay':'NOT_RUN',
        'asymptotic_infinite_DtN':'NOT_CERTIFIED',
        'full_operator_equivalence':'NOT_ESTABLISHED',
        'on_shell_convergence_across_meshes':'NOT_TESTED',
        'Einstein_metric':'NOT_SOLVED',
        'Lorentzian_modes':'NOT_CERTIFIED',
        'Earth_down_whole_craft_up':'NOT_DERIVED',
        'complete_energy_lt10MJ':'NOT_CERTIFIED',
      },
    }
