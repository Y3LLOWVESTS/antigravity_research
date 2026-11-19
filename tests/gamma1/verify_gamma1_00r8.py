"""Independent R8 verifier: direct finite exterior minimization, no R8 import.

Reconstructs source FV matrices from original PH15-P8 and original PH16
inverse ring Green. Checks native fields, boundary support and archive SHA.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import sys

import numpy as np
from scipy import sparse
from scipy.sparse.linalg import splu

ROOT = Path(__file__).resolve().parents[2]


def sha(path):
    return hashlib.sha256(
        Path(path).read_bytes()
    ).hexdigest()


def direct_reduced(ext,mode):
    from antigravity_research.agminer.hook17_ph15_p8_electric_dipole import (
        Dipole,Spec,
    )

    model = Dipole(
        Spec(nr=ext,L=float(ext))
    )

    r = np.repeat(
        np.arange(.5,12.,1.),
        24
    )

    z = np.tile(
        np.arange(-11.5,12.,1.),
        12
    )

    target = np.stack(
        (r,z),
        axis=1
    )

    loc = {
        tuple(p):i
        for i,p in enumerate(
            zip(model.rho,model.z)
        )
    }

    inner = np.array(
        [loc[tuple(point)] for point in target],
        dtype=int
    )

    extids = np.setdiff1d(
        np.arange(model.cells),
        inner
    )

    W = sparse.diags(model.w)

    L = (
        model.L
        +(
            sparse.diags(1/model.rho**2)
            if mode == 'Y'
            else sparse.csr_matrix(model.L.shape)
        )
    )

    A = (W@L).tocsc()

    Aii = A[inner,:][:,inner].toarray()
    Aie = A[inner,:][:,extids].tocsc()

    rim = np.where(
        Aie.getnnz(axis=1)>0
    )[0]

    assert rim.size == 46

    link = Aie[rim,:].toarray()

    LU = splu(
        A[extids,:][:,extids]
    )

    minimizing_exterior = LU.solve(
        -link.T
    )

    correction = -link@minimizing_exterior

    reduced = Aii.copy()
    reduced[np.ix_(rim,rim)] -= correction

    assert np.linalg.norm(
        reduced-reduced.T,
        ord=np.inf
    ) < 2e-9

    boundary_trial = (
        np.sin(np.arange(288)*.171)
        +.01*np.arange(288)/288
    )

    outer = LU.solve(
        -(Aie.T@boundary_trial)
    )

    full_energy = (
        boundary_trial@Aii@boundary_trial
        +2*boundary_trial@(Aie@outer)
        +outer@(A[extids,:][:,extids]@outer)
    )/2

    reduced_energy = (
        boundary_trial@reduced@boundary_trial/2
    )

    error = float(
        abs(full_energy-reduced_energy)
    )

    assert error < 1e-8, (
        'exterior_minimized_energy',
        error
    )

    return reduced,rim,correction,error


def verify(path):
    from antigravity_research.ph16.ph16_04_joint_stationary import (
        CoulombSource,Spec,JointAction,Settings,
    )

    p = Path(path).resolve()

    assert p.parent == ROOT/'results/data'

    assert re.fullmatch(
        r'gamma1_00r8_\d{8}T\d{12}Z\.json',
        p.name
    )

    assert p.with_name(
        p.name+'.sha256'
    ).read_text().strip() == sha(p)+'  '+p.name

    result = json.loads(
        p.read_text()
    )

    assert result['classification'] == (
        'PASS_FINITE_EXTERIOR_SCHUR_X_IMPROVES_Y_RESIDUAL_OPEN'
    )

    assert result['qualified_physical_survivors'] == []
    assert len(result['parents']) == 6

    for ent in result['parents'].values():
        assert sha(ROOT/ent['path']) == ent['expected'] == ent['actual']

    for rel,h in result['producing_sources'].items():
        assert sha(ROOT/rel) == h,rel

    archive = ROOT/result['interface_archive']['path']

    assert sha(archive) == (
        result['interface_archive']['sha256']
    )

    assert archive.with_name(
        archive.name+'.sha256'
    ).read_text().strip() == sha(archive)+'  '+archive.name

    with np.load(
        archive,
        allow_pickle=False
    ) as f:
        saved = {
            k:f[k].copy()
            for k in f.files
        }

    assert set(saved) == set(
        result['interface_archive']['keys']
    )

    assert len(saved) == 11

    with np.load(
        ROOT/result['parents']['R3_native']['path'],
        allow_pickle=False
    ) as f:
        fields = {
            kind:f['A_'+kind].copy()
            for kind in ('X','Y')
        }

    m = CoulombSource(
        Spec(nr=12,L=12.),
        self_order=8
    )

    j = JointAction(
        m,
        Settings(nr=12,L=12.)
    )

    for kind,K in (
        ('X',j.Kx),
        ('Y',j.Ky)
    ):
        assert np.allclose(
            saved[kind+'_green_native_gradient'],
            K@fields[kind],
            atol=2e-11,
            rtol=1e-11
        )

    checked = {}

    series = result['science']['finite_exterior_schur_sweep']

    assert [
        q['outer_extent']
        for q in series
    ] == [14,18,24,30,36,48,60]

    for ext in (14,24,60):
        for kind,K in (
            ('X',j.Kx),
            ('Y',j.Ky)
        ):
            reduced,rim,correction,energy_err = direct_reduced(
                ext,
                kind
            )

            assert np.array_equal(
                rim,
                saved['rim_indices']
            )

            if ext in (24,60):
                assert np.allclose(
                    correction,
                    saved[f'{kind}_outer_{ext}_rim_correction'],
                    atol=2e-10,
                    rtol=1e-10
                )

                assert np.allclose(
                    reduced@fields[kind],
                    saved[f'{kind}_outer_{ext}_native_gradient'],
                    atol=2e-10,
                    rtol=1e-10
                )

            Kv = K@fields[kind]
            Lv = reduced@fields[kind]

            fitted = float(
                np.dot(Kv,Lv)/np.dot(Lv,Lv)
            )

            mismatch = float(
                np.linalg.norm(Kv-fitted*Lv)
                /np.linalg.norm(Kv)
            )

            raw = float(
                np.linalg.norm(Kv-Lv)
                /np.linalg.norm(Kv)
            )

            entry = next(
                q for q in series
                if q['outer_extent'] == ext
            )['carriers'][kind]

            assert np.isclose(
                mismatch,
                entry['native_gradient_relative_best_scaled_DIAGNOSTIC_ONLY'],
                rtol=1e-9,
                atol=1e-12
            )

            assert np.isclose(
                raw,
                entry['native_gradient_relative_unscaled'],
                rtol=1e-9,
                atol=1e-12
            )

            checked[f'{kind}_outer_{ext}'] = {
                'fit':mismatch,
                'unfitted':raw,
                'outer_energy_variation_error':energy_err,
            }

    assert checked['X_outer_60']['fit'] < .06
    assert checked['Y_outer_60']['fit'] > .15

    assert result['finite_DtN_is_infinite'] == 'NO'

    assert result['continuum_Maxwell_equivalence'] == (
        'NOT_CERTIFIED'
    )

    assert result['Einstein_metric'] == 'NOT_SOLVED'

    assert result['full_Lorentzian_mode_health'] == (
        'NOT_CERTIFIED'
    )

    assert result['whole_craft_up'] == 'NOT_DERIVED'

    assert result['SI_energy_lt10MJ'] == 'NOT_CERTIFIED'

    assert result['GAMMA1_01_authorized'] is False
    assert result['006D_replaced'] is False

    print('GAMMA1_00R8_INDEPENDENT_VERIFICATION=PASS')
    print('DIRECT_EXTERIOR_MINIMIZATION_AND_SCHUR=PASS')
    print('FINITE_OUTER_EXTENTS_VERIFIED=14,24,60')

    print(
        'X60_FITTED_NATIVE_GRADIENT_REL='
        +str(checked['X_outer_60']['fit'])
    )
    print(
        'X60_UNFITTED_NATIVE_GRADIENT_REL='
        +str(checked['X_outer_60']['unfitted'])
    )
    print(
        'Y60_FITTED_NATIVE_GRADIENT_REL='
        +str(checked['Y_outer_60']['fit'])
    )
    print(
        'Y60_UNFITTED_NATIVE_GRADIENT_REL='
        +str(checked['Y_outer_60']['unfitted'])
    )

    print('RESULT_SHA256='+sha(p))
    print('INTERFACE_ARCHIVE_SHA256='+sha(archive))

    return checked


if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise SystemExit(
            'Usage: verify_gamma1_00r8.py exact-result.json'
        )

    verify(sys.argv[1])
