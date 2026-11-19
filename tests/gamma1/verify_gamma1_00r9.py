"""Independent R9 verifier: separate incidence construction, no R9 import.

Recomputes exterior energy and Green-kernel sensitivity from original source.
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
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def independent_regular_matrix(ext):
    """Independent vectorized incidence-matrix FV reconstruction."""
    from antigravity_research.agminer.hook17_ph15_p8_electric_dipole import (
        Dipole,Spec,
    )

    m = Dipole(Spec(nr=ext,L=float(ext)))
    nz = 2*ext
    rr = np.arange(ext)+.5

    ri = np.repeat(np.arange(ext-1),nz)
    kz = np.tile(np.arange(nz),ext-1)
    ra = ri*nz+kz
    rb = ra+nz
    rc = 2*np.pi*(ri+1.)**3

    zi = np.repeat(np.arange(ext),nz-1)
    kj = np.tile(np.arange(nz-1),ext)
    za = zi*nz+kj
    zb = za+1
    zc = 2*np.pi*rr[zi]**3

    a = np.r_[ra,za]
    b = np.r_[rb,zb]
    c = np.r_[rc,zc]

    edge = np.arange(len(a))

    incidence = sparse.coo_matrix(
        (
            np.r_[np.ones(len(a)),-np.ones(len(a))],
            (np.r_[edge,edge],np.r_[a,b])
        ),
        shape=(len(a),m.cells)
    ).tocsr()

    boundary = np.zeros(m.cells)

    for i,r in enumerate(rr):
        boundary[i*nz] += 4*np.pi*r**3
        boundary[i*nz+nz-1] += 4*np.pi*r**3

    boundary[(ext-1)*nz:] += 4*np.pi*ext**3

    U = (
        incidence.T@sparse.diags(c)@incidence
        +sparse.diags(boundary)
    ).tocsc()

    invr = sparse.diags(1./m.rho)

    return (invr@U@invr).tocsc()


def independent_schur(ext,Y):
    M = independent_regular_matrix(ext)
    nz = 2*ext

    idx = np.array([
        i*nz+ext-12+k
        for i in range(12)
        for k in range(24)
    ])

    outside = np.setdiff1d(
        np.arange(M.shape[0]),idx
    )

    interior = M[idx,:][:,idx].toarray()
    link = M[idx,:][:,outside].tocsr()

    rim = np.where(
        link.getnnz(axis=1)>0
    )[0]

    assert len(rim)==46

    exterior_matrix = M[outside,:][:,outside]
    lu = splu(exterior_matrix.tocsc())

    exterior_solution = lu.solve(
        -link.T@Y
    )

    energy_full = (
        Y@interior@Y
        +2*Y@(link@exterior_solution)
        +exterior_solution@(exterior_matrix@exterior_solution)
    )/2

    link_rim = link[rim,:].toarray()
    correction = -link_rim@lu.solve(-link_rim.T)

    effective = interior.copy()
    effective[np.ix_(rim,rim)] -= correction

    energy_reduced = Y@effective@Y/2

    assert abs(energy_full-energy_reduced)<2e-8
    assert np.linalg.eigvalsh(effective)[0]>0

    return (
        effective,
        rim,
        correction,
        float(abs(energy_full-energy_reduced))
    )


def verify(path):
    from antigravity_research.ph16.ph16_04_joint_stationary import (
        CoulombSource,Spec,Settings,JointAction,
    )

    p = Path(path).resolve()

    assert p.parent==ROOT/'results/data'

    assert re.fullmatch(
        r'gamma1_00r9_\d{8}T\d{12}Z\.json',
        p.name
    )

    assert p.with_name(
        p.name+'.sha256'
    ).read_text().strip()==sha(p)+'  '+p.name

    d = json.loads(p.read_text())

    assert d['classification']==(
        'PASS_AXIS_REGULAR_Y_IMPROVEMENT_QUADRATURE_RESIDUAL_OPEN'
    )
    assert d['branch']=='GAMMA1-00R9'
    assert len(d['parents'])==7

    for ent in d['parents'].values():
        assert (
            sha(ROOT/ent['path'])
            ==ent['expected_sha256']
            ==ent['actual_sha256']
        )

    for rel,digest in d['producing_sources'].items():
        assert sha(ROOT/rel)==digest,rel

    result_archive = ROOT/d['archive']['path']

    assert sha(result_archive)==d['archive']['sha256']

    assert result_archive.with_name(
        result_archive.name+'.sha256'
    ).read_text().strip()==sha(result_archive)+'  '+result_archive.name

    with np.load(
        result_archive,
        allow_pickle=False
    ) as f:
        stored = {k:f[k].copy() for k in f.files}

    assert len(stored)==5
    assert set(stored)==set(d['archive']['keys'])

    with np.load(
        ROOT/d['parents']['R3_native']['path'],
        allow_pickle=False
    ) as f:
        Y = f['A_Y'].copy()

    with np.load(
        ROOT/d['parents']['R8_interface']['path'],
        allow_pickle=False
    ) as f:
        r8 = {k:f[k].copy() for k in f.files}

    fixed = JointAction(
        CoulombSource(
            Spec(nr=12,L=12),self_order=8
        ),
        Settings(nr=12,L=12)
    ).Ky@Y

    assert np.allclose(
        fixed,
        r8['Y_green_native_gradient'],
        atol=2e-9,
        rtol=1e-11
    )

    assert np.allclose(
        fixed,
        stored['original_Y_order8_green_gradient'],
        atol=2e-9,
        rtol=1e-11
    )

    comparison = d['science']['finite_exterior_sweep']
    values = {}

    for ext in (14,24,60):
        matrix,rim,corr,energy_error = independent_schur(
            ext,Y
        )

        assert np.array_equal(
            rim,stored['rim_indices']
        )

        drow = next(
            x for x in comparison
            if x['outer_extent']==ext
        )

        Ka = fixed
        Fa = matrix@Y

        scale = float(Ka@Fa/(Fa@Fa))
        raw = float(
            np.linalg.norm(Ka-Fa)/np.linalg.norm(Ka)
        )
        fit = float(
            np.linalg.norm(Ka-scale*Fa)/np.linalg.norm(Ka)
        )

        record = drow[
            'axis_regular_Aphi_over_rho_FV'
        ]

        assert np.isclose(
            raw,
            record['unfitted_relative_gradient_error'],
            rtol=1e-10
        )

        assert np.isclose(
            fit,
            record['fitted_relative_gradient_error_DIAGNOSTIC'],
            rtol=1e-10
        )

        assert np.isclose(
            scale,
            record['best_scale_DIAGNOSTIC'],
            rtol=1e-10
        )

        assert (
            raw<drow['R8_azimuthal_mass_FV'][
                'unfitted_relative_gradient_error'
            ]
        )

        if ext==60:
            assert np.allclose(
                Fa,
                stored['Y_regular_outer_60_native_gradient'],
                atol=2e-9,
                rtol=1e-10
            )

            assert np.allclose(
                corr,
                stored['Y_regular_outer_60_interface_correction'],
                atol=2e-9,
                rtol=1e-10
            )

            assert np.allclose(
                r8['Y_outer_60_native_gradient'],
                stored['Y_old_outer_60_native_gradient'],
                atol=2e-9,
                rtol=1e-10
            )

        values[str(ext)] = {
            'unfitted':raw,
            'fitted':fit,
            'full_energy_schur_abs':energy_error,
        }

    assert .19<values['60']['unfitted']<.23

    fractions = d['science'][
        'green_self_cell_order_sensitivity_FIXED_R3_PROFILE'
    ]

    largest,_,_,_ = independent_schur(60,Y)

    for order in (4,8,12):
        mf = CoulombSource(
            Spec(nr=12,L=12),
            self_order=order
        )

        K = JointAction(
            mf,Settings(nr=12,L=12)
        ).Ky

        actual = float(
            np.linalg.norm(K@Y-largest@Y)
            /np.linalg.norm(K@Y)
        )

        expected = fractions[str(order)][
            'unfitted_relative_gradient_error'
        ]

        assert np.isclose(
            actual,expected,
            rtol=1e-10,
            atol=1e-12
        )

    assert (
        fractions['4']['unfitted_relative_gradient_error']
        >fractions['8']['unfitted_relative_gradient_error']
        >fractions['12']['unfitted_relative_gradient_error']
        >.19
    )

    assert d['science'][
        'analytic_continuum_identity'
    ]['bulk_identity'] is True

    assert d['science']['physics_status'][
        'continuum_Y_operator_equivalence'
    ]=='NOT_PROVEN'

    assert d['Earth_down']=='NOT_DERIVED'
    assert d['whole_craft_up']=='NOT_DERIVED'
    assert d['complete_SI_energy_lt10MJ']=='NOT_CERTIFIED'
    assert d['qualified_physical_survivors']==[]
    assert d['GAMMA1_01_authorized'] is False
    assert d['006D_replaced'] is False

    print('GAMMA1_00R9_INDEPENDENT_VERIFICATION=PASS')
    print('ORIGINAL_R8_GREEN_COMPARATOR_REPRODUCED=PASS')
    print('DIRECT_EXTERIOR_ENERGY_MINIMIZATION=PASS')
    print('Y60_REGULAR_UNFITTED='+str(values['60']['unfitted']))
    print(
        'Y60_REGULAR_FITTED_DIAGNOSTIC='
        +str(values['60']['fitted'])
    )

    for order in (4,8,12):
        print(
            f'GREEN_ORDER{order}_UNFITTED='
            +str(fractions[str(order)][
                'unfitted_relative_gradient_error'
            ])
        )

    print('RESULT_SHA256='+sha(p))
    print('R9_ARCHIVE_SHA256='+sha(result_archive))


if __name__=='__main__':
    if len(sys.argv)!=2:
        raise SystemExit(
            'Usage: verify_gamma1_00r9.py exact-R9-result.json'
        )
    verify(sys.argv[1])
