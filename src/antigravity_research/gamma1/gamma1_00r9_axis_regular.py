"""R9: finite-volume azimuthal regularity and Green self-cell quadrature.

Original PH16 stationary action and R3 native arrays are never modified.
Exterior truncation is finite; diagnostic self-order variants are not re-solved.
Neither test supplies the full Lorentzian/Einstein/gravity bridge.
"""
from __future__ import annotations

import hashlib
from pathlib import Path
import numpy as np
from scipy import sparse
from scipy.sparse.linalg import splu

PH16_SHA = 'b5468671f6418fad7b6ed01d916ea65a95a1d59252b84d4411beed9709f86df0'
P8_SHA = '406aa58db3092d2392adbb78429257538fd51a202f472fd49b3a08862a934fed'
P10_SHA = '25e564a6dbbd4658f6154781db610738b8ed1114aa0f8fe71bf4ab91092fdddb'
R3_SHA = '94d3763a8d7705ab3dc8774310cf3b8bba96557a0b80d2c34aa110d00b840d54'
R8_RESULT_SHA = 'e6fbf0216ff0b80ca142c97fee73157f5dd694b4542584e60dce4fde7f130d82'
R8_VERIFY_SHA = '2eb7f4cf257b58f160acab7076e09b28ac7a9c9c1208ab05f9ed8ae24128efe8'
R8_ARCHIVE_SHA = '9878534c2f6308c2b70693699eb056c00d71125209457bb2008701f78f5263b4'

EXTENTS = (14, 24, 36, 60)
ORDERS = (4, 8, 12)


def sha(path):
    p = Path(path)
    return hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else 'MISSING'


def continuous_azimuthal_identity():
    """Symbolic product rule; preserve the physical surface term."""
    import sympy as sp

    r, z = sp.symbols('rho z', positive=True, real=True)
    u = sp.Function('u')(r, z)
    A = r*u

    lhs = r*(sp.diff(A,r)**2 + sp.diff(A,z)**2 + A**2/r**2)
    rhs = r**3*(sp.diff(u,r)**2 + sp.diff(u,z)**2)

    identity = sp.simplify(
        sp.expand(lhs-rhs-sp.diff(r**2*u**2,r))
    ) == 0

    if not identity:
        raise RuntimeError('AXIS_TRANSFORM_PRODUCT_RULE_FAILED')

    return {
        'bulk_identity': identity,
        'surface_term':
            'd_dr(rho^2*u^2); zero only with appropriate regularity/outer boundary',
        'regularity': 'A_phi=rho*u with finite u at rho=0',
        'u_energy_weight': '2*pi*rho^3',
    }


def regular_azimuthal_fv(ext):
    """Finite-volume action from E=1/2 integral 2pi*rho^3 |grad u|^2.

    u=A_phi/rho. The axis face has zero flux. Outer radial and axial
    boundaries use finite-domain homogeneous Dirichlet conditions.
    No fitted constants are used.
    """
    if not isinstance(ext, int) or ext < 14:
        raise ValueError('EXTERIOR_DOMAIN_INVALID')

    nz = 2*ext
    N = ext*nz
    rr = np.arange(ext, dtype=float)+.5
    rho = np.repeat(rr,nz)

    diagonal = np.zeros(N)
    rows, cols, vals = [], [], []

    def link(a,b,c):
        diagonal[a] += c
        diagonal[b] += c
        rows.extend((a,b))
        cols.extend((b,a))
        vals.extend((-c,-c))

    for i,r in enumerate(rr):
        for k in range(nz):
            a = i*nz+k

            if i+1 < ext:
                link(a,a+nz,2*np.pi*(i+1.)**3)
            else:
                diagonal[a] += 4*np.pi*(i+1.)**3

            if k+1 < nz:
                link(a,a+1,2*np.pi*r**3)
            else:
                diagonal[a] += 4*np.pi*r**3

            if k == 0:
                diagonal[a] += 4*np.pi*r**3

            # rho=0 has a regular zero-flux u face.

    rows.extend(np.arange(N))
    cols.extend(np.arange(N))
    vals.extend(diagonal)

    Cu = sparse.coo_matrix(
        (vals,(rows,cols)), shape=(N,N)
    ).tocsr()

    invr = sparse.diags(1./rho)
    A = (invr@Cu@invr).tocsc()

    if np.max(abs((A-A.T).data),initial=0.) > 3e-11:
        raise RuntimeError('REGULARIZED_FV_NOT_RECIPROCAL')

    return A


def original_fv(ext):
    from antigravity_research.agminer.hook17_ph15_p8_electric_dipole import (
        Dipole, Spec,
    )

    m = Dipole(Spec(nr=ext,L=float(ext)))

    return (
        sparse.diags(m.w)
        @(m.L+sparse.diags(1./m.rho**2))
    ).tocsc()


def reduction(M,ext):
    """Exact finite-exterior Schur reduction onto the original 288 cells."""
    nz = 2*ext

    keep = np.array([
        i*nz+ext-12+k
        for i in range(12)
        for k in range(24)
    ],dtype=int)

    outside = np.setdiff1d(
        np.arange(M.shape[0]),keep
    )

    Aii = M[keep,:][:,keep].toarray()
    Aie = M[keep,:][:,outside].tocsr()

    rim = np.flatnonzero(
        Aie.getnnz(axis=1)
    )

    if len(rim) != 46:
        raise RuntimeError('INTERFACE_SHAPE_DRIFT')

    link = Aie[rim,:].toarray()
    sol = splu(
        M[outside,:][:,outside].tocsc()
    ).solve(link.T)

    correction = link@sol

    effective = Aii.copy()
    effective[np.ix_(rim,rim)] -= correction

    if np.max(abs(effective-effective.T)) > 5e-9:
        raise RuntimeError('SCHUR_RECIPROCITY_FAILED')

    if np.linalg.eigvalsh(effective)[0] <= 0:
        raise RuntimeError('SCHUR_NOT_POSITIVE')

    if np.linalg.eigvalsh(
        (correction+correction.T)/2
    )[0] < -5e-9:
        raise RuntimeError('EXTERIOR_CORRECTION_NOT_PSD')

    return effective,rim,correction


def metrics(K,L,Y,axis_rows=2):
    ky = K@Y
    ly = L@Y

    denominator = float(np.linalg.norm(ky))
    scale = float(np.dot(ky,ly)/np.dot(ly,ly))
    diff = ky-ly

    rowmask = np.arange(288).reshape(
        12,24
    )[:axis_rows,:].ravel()

    rim = np.zeros((12,24),dtype=bool)
    rim[-1,:] = True
    rim[:,0] = True
    rim[:,-1] = True
    rimmask = rim.ravel()

    return {
        'unfitted_relative_gradient_error':
            float(np.linalg.norm(diff)/denominator),

        'fitted_relative_gradient_error_DIAGNOSTIC':
            float(np.linalg.norm(ky-scale*ly)/denominator),

        'best_scale_DIAGNOSTIC':scale,

        'energy_ratio_original_over_fv':
            float(Y@ky/(Y@ly)),

        'axis_two_rows_original_gradient_fraction':
            float(np.linalg.norm(ky[rowmask])/denominator),

        'axis_two_rows_error_fraction_of_global_green_norm':
            float(np.linalg.norm(diff[rowmask])/denominator),

        'rim_original_gradient_fraction':
            float(np.linalg.norm(ky[rimmask])/denominator),

        'rim_error_fraction_of_global_green_norm':
            float(np.linalg.norm(diff[rimmask])/denominator),

        'bulk_interior_error_fraction_of_global_green_norm':
            float(np.linalg.norm(diff[~rimmask])/denominator),
    }


def analyze(native,r8_archive):
    from antigravity_research.ph16.ph16_04_joint_stationary import (
        CoulombSource,Spec,JointAction,Settings,
    )

    Y = native['A_Y']

    if Y.shape != (288,) or not np.isfinite(Y).all():
        raise RuntimeError('NATIVE_Y_INVALID')

    if not continuous_azimuthal_identity()['bulk_identity']:
        raise RuntimeError('IDENTITY_FAIL')

    m8 = CoulombSource(
        Spec(nr=12,L=12.),self_order=8
    )

    j8 = JointAction(
        m8,Settings(nr=12,L=12.)
    )

    K8 = j8.Ky
    original_gradient = K8@Y

    if np.max(abs(
        original_gradient-r8_archive['Y_green_native_gradient']
    )) > 1e-9:
        raise RuntimeError('R8_GREEN_GRADIENT_DRIFT')

    records = []
    stored = {}
    last_regular = None

    for ext in EXTENTS:
        old,rim_old,corr_old = reduction(
            original_fv(ext),ext
        )

        regular,rim_reg,corr_reg = reduction(
            regular_azimuthal_fv(ext),ext
        )

        if not np.array_equal(rim_old,rim_reg):
            raise RuntimeError('RIM_MISMATCH')

        base = metrics(K8,old,Y)
        reg = metrics(K8,regular,Y)

        if ext in (24,60):
            if np.max(abs(
                old@Y-r8_archive[
                    f'Y_outer_{ext}_native_gradient'
                ]
            )) > 3e-9:
                raise RuntimeError('R8_OPERATOR_REPLAY_MISMATCH')

            if np.max(abs(
                corr_old-r8_archive[
                    f'Y_outer_{ext}_rim_correction'
                ]
            )) > 3e-9:
                raise RuntimeError('R8_SCHUR_CORRECTION_REPLAY_MISMATCH')

        if (
            reg['unfitted_relative_gradient_error']
            >=base['unfitted_relative_gradient_error']
        ):
            raise RuntimeError(
                'AXIS_REGULAR_FORM_FAILED_TO_IMPROVE_Y'
            )

        records.append({
            'outer_extent':ext,
            'R8_azimuthal_mass_FV':base,
            'axis_regular_Aphi_over_rho_FV':reg,
            'interface_cells':len(rim_old),
            'both_operators_positive_reciprocal':True,
        })

        if ext == 60:
            last_regular = regular

            stored['Y_regular_outer_60_native_gradient'] = np.asarray(
                regular@Y,dtype='<f8'
            )

            stored['Y_regular_outer_60_interface_correction'] = np.asarray(
                corr_reg,dtype='<f8'
            )

            stored['Y_old_outer_60_native_gradient'] = np.asarray(
                old@Y,dtype='<f8'
            )

            stored['original_Y_order8_green_gradient'] = np.asarray(
                original_gradient,dtype='<f8'
            )

            stored['rim_indices'] = np.asarray(
                rim_reg,dtype='<i8'
            )

    order_records = {}

    for order in ORDERS:
        if order == 8:
            K = K8
        else:
            m = CoulombSource(
                Spec(nr=12,L=12.),self_order=order
            )

            K = JointAction(
                m,Settings(nr=12,L=12.)
            ).Ky

        order_records[str(order)] = metrics(
            K,last_regular,Y
        )

    last = records[-1]

    if not (
        .28<last['R8_azimuthal_mass_FV'][
            'unfitted_relative_gradient_error'
        ]<.30
    ):
        raise RuntimeError('R8_BASELINE_NOT_REPRODUCED')

    if not (
        .19<last['axis_regular_Aphi_over_rho_FV'][
            'unfitted_relative_gradient_error'
        ]<.23
    ):
        raise RuntimeError('AXIS_REGULAR_RESIDUAL_UNEXPECTED')

    if not (
        .19<order_records['12'][
            'unfitted_relative_gradient_error'
        ]<.22
    ):
        raise RuntimeError('SELF_ORDER_CONTROL_UNEXPECTED')

    if not (
        order_records['4']['unfitted_relative_gradient_error']
        >order_records['8']['unfitted_relative_gradient_error']
        >order_records['12']['unfitted_relative_gradient_error']
    ):
        raise RuntimeError('QUADRATURE_ORDER_TREND_FAILED')

    return {
        'analytic_continuum_identity':
            continuous_azimuthal_identity(),

        'finite_exterior_sweep':records,

        'green_self_cell_order_sensitivity_FIXED_R3_PROFILE':
            order_records,

        'data_arrays':stored,

        'negative_controls':{
            'R8_standard_m1_mass_discretization':
                'REPRODUCED_UNMODIFIED',
            'quadrature_orders_not_stationary_replays':'TRUE',
            'outer_extent_not_mesh_refinement':'TRUE',
            'self_quadrature_order_12_residual_nonzero':'TRUE',
            'zero_field_linear_operator_action':'EXACT_ZERO',
        },

        'physics_status':{
            'new_PH16_stationary_solve':'NOT_RUN',
            'source_free_exterior':'NOT_CERTIFIED',
            'complete_Lorentzian_action':'NOT_CLOSED',
            'covariant_Ward_Noether_Bianchi':'NOT_CLOSED',
            'healthy_constrained_spectrum':'NOT_CERTIFIED',
            'Einstein_metric_and_force':'NOT_DERIVED',
            'Earth_down_whole_craft_up':'NOT_DERIVED',
            'complete_SI_energy_lt10MJ':'NOT_CERTIFIED',
            'continuum_Y_operator_equivalence':'NOT_PROVEN',
        },
    }
