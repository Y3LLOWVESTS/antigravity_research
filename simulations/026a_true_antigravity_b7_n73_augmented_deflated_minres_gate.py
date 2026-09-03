#!/usr/bin/env python3
"""026A — true-antigravity B7 N=73 augmented/deflated Newton-MINRES gate.

PURPOSE
-------
Close the remaining unrestricted N=73 Euler-Lagrange residual of the strongest
actual true-antigravity field stack: the false-core B=7, eta=0.4, m=8
Skyrmion. This is the long-planned successor to 023C2AQS2R5.

QUESTION / CHEAPEST DECISIVE TEST
---------------------------------
R3 showed ordinary full MINRES was slowed by smooth modes. R4 showed a small
residual-informed Galerkin space captured the smooth residual, but separate
coarse corrections regenerated a high-frequency complement. R5 showed that
neither the old L-BFGS inverse nor naive high-pass descent could relax that
complement independently. The cheapest distinct test is therefore the full
coupled damped Newton system

    (H + mu I) delta = -g

with the troublesome smooth space treated by augmentation/deflation.

BLOCK SOLVE
-----------
With orthonormal augmentation U, P = I-UU^T, A=H+mu I and Ac=U^T A U,
write delta=f+Uc, U^T f=0. Exact block elimination gives

    S f = P[b - A U Ac^{-1} U^T b]

    S = P[A - A U Ac^{-1} U^T A]P

    c = Ac^{-1} U^T(b-Af)

where b=-g. MINRES solves the symmetric Schur complement. Only the three
exact global pion-isorotation zero modes are projected out. Approximate
translations/rotations remain physical and may only enter U as augmentation.

OBSERVABLE / PROMOTION
----------------------
Unchanged strict stationarity:

    GRAD_RMS <= 1.5e-3
    GRAD_MAX <= 5.0e-2

If and only if that passes, preserve B=7/topology/smoothness, DEC, positive
total active mass, negative active region and trace gates, then run the
existing continuous finite-payload force certificate. Green requires a
certified outward N=73 sentinel.

FALSIFIER / STOP RULE
---------------------
Loss of B=7 or the physical-field gate rejects the candidate. If bounded
augmented MINRES cannot produce any admissible merit-reducing coupled Newton
step, stop solver tuning and move to a targeted low-Ritz-mode/discretization
obstruction diagnostic. Never weaken the physical or stationarity gates.

CLAIM LIMITS
------------
This run does not establish full Hessian/fission stability, N73/N81 continuum
force convergence, nonlinear Einstein-Skyrme consistency, escape from 1/G
scaling, an experiment, or a practical antigravity device.

INPUTS
------
simulations/023c2aqs2r5_two_level_vcycle_stationarity_closure.py
and its R4/R3/R2/R chain plus the latest N=73 checkpoint.

OUTPUTS
-------
results/data/026a_true_antigravity_n73_augmented_minres_checkpoint.npz
results/data/026a_true_antigravity_n73_augmented_minres_summary.json
results/data/026a_true_antigravity_strict_stationary_b7_n73.npz  (green only)

METHOD REFERENCE
----------------
Gaul, Gutknecht, Liesen & Nabben, SIAM J. Matrix Anal. Appl. 34 (2013),
framework for deflated and augmented Krylov methods including MINRES.

CLAIM CLASSIFICATION
--------------------
PROJECT_DERIVED_026A_TRUE_ANTIGRAVITY_N73_AUGMENTED_DEFLATED_MINRES_GATE
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path

import numpy as np
from scipy.sparse.linalg import LinearOperator


ROOT = Path(__file__).resolve().parents[1]
SIM = ROOT / "simulations"
DATA = ROOT / "results/data"

R5_SOURCE = (
    SIM
    / "023c2aqs2r5_two_level_vcycle_stationarity_closure.py"
)

EXPECTED_R5_SHA256 = (
    "5dfafa840ea10fa2e4aa3e1c0710d9bbd18110803d68cf93809ba2307f38d1df"
)

CHECKPOINT = (
    DATA
    / "026a_true_antigravity_n73_augmented_minres_checkpoint.npz"
)

SUMMARY = (
    DATA
    / "026a_true_antigravity_n73_augmented_minres_summary.json"
)

FINAL = (
    DATA
    / "026a_true_antigravity_strict_stationary_b7_n73.npz"
)


B = 7
ETA = 0.4
MASS = 8.0
N = 73

GRAD_RMS_TOL = 1.5e-3
GRAD_MAX_TOL = 5.0e-2
MAX_NEIGHBOR_ANGLE = 0.70

MAX_OUTER = max(
    1,
    int(
        os.environ.get(
            "AG_026A_MAX_OUTER",
            "3",
        )
    ),
)

MINRES_MAXITER = max(
    12,
    int(
        os.environ.get(
            "AG_026A_MINRES_MAXITER",
            "36",
        )
    ),
)

MINRES_RTOL = float(
    os.environ.get(
        "AG_026A_MINRES_RTOL",
        "0.025",
    )
)

MAX_AUGMENT_DIM = max(
    8,
    int(
        os.environ.get(
            "AG_026A_MAX_AUGMENT_DIM",
            "18",
        )
    ),
)

HVP_POINT_ANGLE = float(
    os.environ.get(
        "AG_026A_HVP_POINT_ANGLE",
        "2e-4",
    )
)

MAX_LINEAR_RELRES = float(
    os.environ.get(
        "AG_026A_MAX_LINEAR_RELRES",
        "0.35",
    )
)

DAMPING_FACTORS = tuple(
    float(x)
    for x in os.environ.get(
        "AG_026A_DAMPING_FACTORS",
        "0,0.10,1.0",
    ).split(",")
)


def sha256(path):
    """Return the SHA-256 hash of one upstream source file."""

    h = hashlib.sha256()

    with open(path, "rb") as f:
        for block in iter(
            lambda: f.read(1 << 20),
            b"",
        ):
            h.update(block)

    return h.hexdigest()


def load_module(name, path):
    """Load one audited simulation module directly from its repo path."""

    spec = importlib.util.spec_from_file_location(
        name,
        path,
    )

    if spec is None or spec.loader is None:
        raise RuntimeError(
            f"Cannot import {path}"
        )

    mod = importlib.util.module_from_spec(
        spec
    )

    spec.loader.exec_module(
        mod
    )

    return mod


def merit(rms, gmax):
    """Return normalized distance from the unchanged strict gate."""

    return max(
        rms / GRAD_RMS_TOL,
        gmax / GRAD_MAX_TOL,
    )


def json_default(x):
    """Serialize NumPy scalars/arrays without altering numerical values."""

    if isinstance(
        x,
        np.generic,
    ):
        return x.item()

    if isinstance(
        x,
        np.ndarray,
    ):
        return x.tolist()

    raise TypeError(
        type(x).__name__
    )


def project_q(
    c2a,
    x,
    Z,
    U,
):
    """Project exact isorotation zero modes and the augmentation space."""

    y = c2a.project_subspace(
        np.asarray(
            x,
            dtype=float,
        ),
        Z,
    )

    return (
        y
        - U @ (U.T @ y)
    )


def append_mgs(
    c2a,
    cols,
    v,
    Z,
):
    """Twice-reorthogonalized modified Gram-Schmidt insertion."""

    w = c2a.project_subspace(
        np.asarray(
            v,
            dtype=float,
        ).reshape(-1),
        Z,
    )

    for _ in range(2):
        for q in cols:
            w -= (
                q
                * float(
                    np.dot(
                        q,
                        w,
                    )
                )
            )

    n = float(
        np.linalg.norm(
            w
        )
    )

    if n <= 1e-13:
        return False

    cols.append(
        w / n
    )

    return True


def build_U(
    r4,
    r,
    c2a,
    cr3,
    state,
    g,
    history,
    basis,
    Z,
):
    """Construct the recycled smooth/problematic subspace.

    The main vectors are exactly the residual-informed family that succeeded
    in R4. Approximate spatial symmetry directions are allowed only as
    augmentation; they are never removed as zero modes.

    Recent positive-curvature secants are included only if room remains.
    """

    gvec = c2a.project_subspace(
        c2a.field_to_components(
            g,
            basis,
        ),
        Z,
    )

    gnorm = max(
        float(
            np.linalg.norm(
                gvec
            )
        ),
        1e-300,
    )

    gcomp = gvec.reshape(
        N - 2,
        N - 2,
        N - 2,
        3,
    )

    cols = []
    names = []

    for name, arr in r4.candidate_vectors(
        gcomp,
        state.axis,
    ):
        if len(cols) >= MAX_AUGMENT_DIM:
            break

        if append_mgs(
            c2a,
            cols,
            arr,
            Z,
        ):
            names.append(
                "R4_" + name
            )

    if len(cols) < MAX_AUGMENT_DIM:
        spatial = (
            c2a.spatial_symmetry_candidates(
                cr3,
                state.phi,
                state.axis,
                basis,
            )
        )

        if spatial.size:
            overlap = (
                np.abs(
                    spatial.T
                    @ gvec
                )
                / gnorm
            )

            for j in np.argsort(
                overlap
            )[::-1]:

                if (
                    len(cols)
                    >= MAX_AUGMENT_DIM
                ):
                    break

                if overlap[j] < 1e-5:
                    break

                if append_mgs(
                    c2a,
                    cols,
                    spatial[:, j],
                    Z,
                ):
                    names.append(
                        f"SPATIAL_{int(j)}"
                    )

    pairs = r.component_history(
        c2a,
        history,
        basis,
        Z,
    )

    for j, (
        s,
        _y,
        _rho,
    ) in enumerate(
        reversed(
            pairs[-4:]
        )
    ):
        if len(cols) >= MAX_AUGMENT_DIM:
            break

        if append_mgs(
            c2a,
            cols,
            s,
            Z,
        ):
            names.append(
                f"SECANT_{j}"
            )

    if not cols:
        raise RuntimeError(
            "No augmentation vectors survived"
        )

    U = np.column_stack(
        cols
    )

    gram = float(
        np.max(
            np.abs(
                U.T @ U
                - np.eye(
                    U.shape[1]
                )
            )
        )
    )

    if gram > 5e-10:
        raise RuntimeError(
            f"Augmentation Gram error {gram}"
        )

    capture = float(
        np.linalg.norm(
            U @ (
                U.T
                @ gvec
            )
        )
        / gnorm
    )

    print(
        f"026A_AUGMENT_DIM="
        f"{U.shape[1]}",
        flush=True,
    )

    print(
        "026A_AUGMENT_NAMES="
        + ",".join(
            names
        ),
        flush=True,
    )

    print(
        f"026A_AUGMENT_GRAM_MAXERR="
        f"{gram:.15e}",
        flush=True,
    )

    print(
        f"026A_AUGMENT_GRAD_CAPTURE="
        f"{capture:.15e}",
        flush=True,
    )

    return (
        U,
        gvec,
        pairs,
        capture,
        names,
    )


def save_checkpoint(
    state,
    history,
    E,
    rms,
    gmax,
    accepted,
):
    """Persist every accepted unrestricted 026A field."""

    DATA.mkdir(
        parents=True,
        exist_ok=True,
    )

    if history:
        s_hist = np.stack(
            [
                x[0]
                for x in history
            ]
        )

        y_hist = np.stack(
            [
                x[1]
                for x in history
            ]
        )

    else:
        s_hist = np.empty(
            (
                0,
                N,
                N,
                N,
                4,
            )
        )

        y_hist = np.empty(
            (
                0,
                N,
                N,
                N,
                4,
            )
        )

    np.savez(
        CHECKPOINT,
        phi=state.phi,
        axis=state.axis,
        dx=np.array(
            state.dx
        ),
        B=np.array(
            B
        ),
        eta=np.array(
            ETA
        ),
        mass=np.array(
            MASS
        ),
        accepted_total=np.array(
            state.accepted_total
        ),
        augmented_accepted_total=np.array(
            accepted
        ),
        energy=np.array(
            E
        ),
        grad_rms=np.array(
            rms
        ),
        grad_max=np.array(
            gmax
        ),
        source=np.array(
            "026A_TRUE_ANTIGRAVITY_AUGMENTED_MINRES"
        ),
        s_hist=s_hist,
        y_hist=y_hist,
    )

    print(
        "026A_CHECKPOINT="
        f"{CHECKPOINT.relative_to(ROOT)}",
        flush=True,
    )


def load_state(
    r5,
    qs2,
    cr3,
    cr4r,
):
    """Resume 026A or inherit the latest audited R5/R4 state."""

    if not CHECKPOINT.is_file():

        (
            state,
            hist,
            src,
            discarded,
            normerr,
            *_,
        ) = r5.load_state(
            None,
            qs2,
            cr3,
            cr4r,
        )

        return (
            state,
            hist,
            src,
            discarded,
            normerr,
            0,
        )

    with np.load(
        CHECKPOINT,
        allow_pickle=False,
    ) as d:

        phi = np.array(
            d["phi"]
        )

        axis = np.array(
            d["axis"]
        )

        dx = float(
            d["dx"]
        )

        if (
            int(
                d["B"]
            )
            != B
            or abs(
                float(
                    d["eta"]
                )
                - ETA
            )
            > 1e-14
            or abs(
                float(
                    d["mass"]
                )
                - MASS
            )
            > 1e-14
        ):
            raise RuntimeError(
                "026A metadata mismatch"
            )

        accepted = int(
            d["accepted_total"]
        )

        aug = int(
            d[
                "augmented_accepted_total"
            ]
        )

        s_hist = np.asarray(
            d["s_hist"]
        )

        y_hist = np.asarray(
            d["y_hist"]
        )

    if (
        phi.shape
        != (
            N,
            N,
            N,
            4,
        )
        or axis.shape
        != (
            N,
        )
    ):
        raise RuntimeError(
            "026A shape mismatch"
        )

    normerr = float(
        np.max(
            np.abs(
                np.linalg.norm(
                    phi,
                    axis=-1,
                )
                - 1.0
            )
        )
    )

    if normerr > 5e-10:
        raise RuntimeError(
            f"S3 norm error {normerr}"
        )

    hist, discarded = (
        qs2.history_from_arrays(
            cr3,
            s_hist,
            y_hist,
            dx,
        )
    )

    state = cr4r.State(
        phi=phi,
        axis=axis,
        dx=dx,
        accepted_total=accepted,
    )

    return (
        state,
        hist,
        CHECKPOINT,
        discarded,
        normerr,
        aug,
    )


def coupled_solve(
    r4,
    r5,
    r,
    qs2,
    c2a,
    cr2,
    cr3,
    state,
    history,
    E,
    g,
    rms,
    gmax,
    first_outer,
):
    """Solve the damped coupled coarse/fine Newton system."""

    phi = state.phi
    dx = state.dx

    basis = (
        c2a.tangent_basis_householder(
            phi
        )
    )

    Z = c2a.orthonormal_columns(
        c2a.isorotation_modes(
            phi,
            basis,
        )
    )

    ndof = (
        basis.shape[0]
        * 3
    )

    if (
        first_outer
        and not r.audit_hessian_operator(
            c2a,
            cr3,
            phi,
            state.axis,
            dx,
            basis,
            Z,
        )
    ):
        raise RuntimeError(
            "HVP audit failed"
        )

    (
        U,
        gvec,
        pairs,
        capture,
        names,
    ) = build_U(
        r4,
        r,
        c2a,
        cr3,
        state,
        g,
        history,
        basis,
        Z,
    )

    b = -gvec

    bnorm = max(
        float(
            np.linalg.norm(
                gvec
            )
        ),
        1e-300,
    )

    hvp, calls = c2a.make_hvp(
        cr3,
        phi,
        dx,
        basis,
        Z,
        HVP_POINT_ANGLE,
    )

    HU = np.column_stack(
        [
            hvp(
                U[:, j]
            )
            for j in range(
                U.shape[1]
            )
        ]
    )

    Hc0 = 0.5 * (
        U.T @ HU
        + HU.T @ U
    )

    evals = np.linalg.eigvalsh(
        Hc0
    )

    nz = np.abs(
        evals[
            np.abs(
                evals
            )
            > (
                1e-12
                * max(
                    float(
                        np.max(
                            np.abs(
                                evals
                            )
                        )
                    ),
                    1.0,
                )
            )
        ]
    )

    coarse_scale = (
        float(
            np.median(
                nz
            )
        )
        if nz.size
        else 1.0
    )

    pair_scale = (
        r.curvature_scale_from_pairs(
            pairs
        )
    )

    scale = max(
        coarse_scale,
        pair_scale,
        1e-8,
    )

    shift_floor = max(
        0.0,
        -float(
            evals[0]
        )
        + 0.02
        * scale,
    )

    PHU = np.column_stack(
        [
            project_q(
                c2a,
                HU[:, j],
                Z,
                U,
            )
            for j in range(
                U.shape[1]
            )
        ]
    )

    coupling = float(
        np.linalg.norm(
            PHU
        )
        / max(
            np.linalg.norm(
                HU
            ),
            1e-300,
        )
    )

    print(
        "026A_COARSE_EIGS="
        + ",".join(
            f"{x:.8e}"
            for x in evals
        ),
        flush=True,
    )

    print(
        "026A_COARSE_FINE_HESSIAN_COUPLING="
        f"{coupling:.15e}",
        flush=True,
    )

    print(
        "026A_SHIFT_FLOOR="
        f"{shift_floor:.15e}",
        flush=True,
    )

    M = None

    if pairs:

        rng = np.random.default_rng(
            20260902026
        )

        q = project_q(
            c2a,
            rng.normal(
                size=ndof
            ),
            Z,
            U,
        )

        q /= max(
            float(
                np.linalg.norm(
                    q
                )
            ),
            1e-300,
        )

        Bq = project_q(
            c2a,
            r.lbfgs_inverse_vector(
                q,
                pairs,
                Z,
                c2a,
            ),
            Z,
            U,
        )

        qBq = float(
            np.dot(
                q,
                Bq,
            )
        )

        print(
            "026A_PRECONDITIONER_QBQ="
            f"{qBq:.15e}",
            flush=True,
        )

        if (
            math.isfinite(
                qBq
            )
            and qBq > 1e-14
        ):

            def mvec(x):

                x = np.asarray(
                    x,
                    dtype=float,
                )

                xu = U @ (
                    U.T @ x
                )

                xq = project_q(
                    c2a,
                    x,
                    Z,
                    U,
                )

                yq = (
                    r.lbfgs_inverse_vector(
                        xq,
                        pairs,
                        Z,
                        c2a,
                    )
                )

                return (
                    project_q(
                        c2a,
                        yq,
                        Z,
                        U,
                    )
                    + xu
                )

            M = LinearOperator(
                (
                    ndof,
                    ndof,
                ),
                matvec=mvec,
                dtype=float,
            )

    print(
        "026A_PRECONDITIONER="
        + (
            "PROJECTED_LBFGS"
            if M is not None
            else "NONE"
        ),
        flush=True,
    )

    reports = []

    for trial, factor in enumerate(
        DAMPING_FACTORS
    ):

        mu = (
            shift_floor
            + max(
                0.0,
                factor,
            )
            * scale
        )

        AU = (
            HU
            + mu
            * U
        )

        Ac = 0.5 * (
            U.T @ AU
            + AU.T @ U
        )

        if (
            float(
                np.linalg.eigvalsh(
                    Ac
                )[0]
            )
            <= 0.0
        ):
            continue

        def solve_c(y):
            return np.linalg.solve(
                Ac,
                np.asarray(
                    y,
                    dtype=float,
                ),
            )

        def Avec(x):

            xp = (
                c2a.project_subspace(
                    np.asarray(
                        x,
                        dtype=float,
                    ),
                    Z,
                )
            )

            return (
                hvp(
                    xp
                )
                + mu
                * xp
            )

        rhs = project_q(
            c2a,
            b
            - AU
            @ solve_c(
                U.T @ b
            ),
            Z,
            U,
        )

        def Svec(x):

            x = np.asarray(
                x,
                dtype=float,
            )

            xu = (
                U
                @ (
                    U.T @ x
                )
            )

            xq = project_q(
                c2a,
                x,
                Z,
                U,
            )

            Ax = Avec(
                xq
            )

            result = (
                Ax
                - AU
                @ solve_c(
                    U.T @ Ax
                )
            )

            return (
                project_q(
                    c2a,
                    result,
                    Z,
                    U,
                )
                + xu
            )

        S = LinearOperator(
            (
                ndof,
                ndof,
            ),
            matvec=Svec,
            dtype=float,
        )

        if trial == 0:

            rng = np.random.default_rng(
                20260902027
            )

            u = project_q(
                c2a,
                rng.normal(
                    size=ndof
                ),
                Z,
                U,
            )

            w = project_q(
                c2a,
                rng.normal(
                    size=ndof
                ),
                Z,
                U,
            )

            u /= max(
                float(
                    np.linalg.norm(
                        u
                    )
                ),
                1e-300,
            )

            w /= max(
                float(
                    np.linalg.norm(
                        w
                    )
                ),
                1e-300,
            )

            Su = Svec(
                u
            )

            Sw = Svec(
                w
            )

            a = float(
                np.dot(
                    u,
                    Sw,
                )
            )

            z = float(
                np.dot(
                    Su,
                    w,
                )
            )

            asym = (
                abs(
                    a - z
                )
                / max(
                    abs(
                        a
                    ),
                    abs(
                        z
                    ),
                    1e-300,
                )
            )

            print(
                "026A_SCHUR_SELFADJ_RELASYM="
                f"{asym:.15e}",
                flush=True,
            )

            if asym > 8e-3:
                raise RuntimeError(
                    "Schur symmetry audit failed"
                )

        it = {
            "n": 0
        }

        def cb(_):
            it["n"] += 1

        f, info = r.minres_compat(
            S,
            rhs,
            M,
            MINRES_RTOL,
            MINRES_MAXITER,
            cb,
        )

        f = project_q(
            c2a,
            np.asarray(
                f
            ),
            Z,
            U,
        )

        Af = Avec(
            f
        )

        c = solve_c(
            U.T
            @ (
                b - Af
            )
        )

        delta = (
            c2a.project_subspace(
                f
                + U @ c,
                Z,
            )
        )

        lin = (
            Avec(
                delta
            )
            - b
        )

        rel = float(
            np.linalg.norm(
                lin
            )
            / bnorm
        )

        gd_comp = float(
            np.dot(
                gvec,
                delta,
            )
        )

        report = {
            "factor":
                factor,
            "mu":
                mu,
            "info":
                int(
                    info
                ),
            "iters":
                it["n"],
            "relres":
                rel,
            "gd_components":
                gd_comp,
        }

        reports.append(
            report
        )

        print(
            "026A_MINRES "
            f"FACTOR={factor:.6e} "
            f"MU={mu:.15e} "
            f"INFO={info} "
            f"ITERS={it['n']} "
            f"FULL_RELRES={rel:.15e} "
            f"G_DOT_DELTA_COMPONENTS={gd_comp:.15e}",
            flush=True,
        )

        if (
            math.isfinite(
                rel
            )
            and rel
            <= MAX_LINEAR_RELRES
        ):

            direction = (
                cr3.project_tangent(
                    phi,
                    c2a.components_to_field(
                        delta,
                        basis,
                        phi.shape,
                    ),
                )
            )

            pack = r5.full_candidate(
                r4,
                r,
                qs2,
                c2a,
                cr2,
                cr3,
                state,
                g,
                E,
                rms,
                gmax,
                direction,
                f"026A_DAMP_{factor:.6e}",
                False,
                r5.residual_metrics(
                    c2a,
                    state.phi,
                    g,
                ),
            )

            if pack is not None:

                pack[
                    "linear_selected"
                ] = report

                return (
                    pack,
                    {
                        "augment_dim":
                            U.shape[1],
                        "augment_names":
                            names,
                        "gradient_capture":
                            capture,
                        "coupling":
                            coupling,
                        "coarse_eigs":
                            evals,
                        "hvp_calls":
                            calls["count"],
                        "linear_trials":
                            reports,
                    },
                )

            print(
                "026A_DAMPING_NONLINEAR_ACCEPT="
                "NO_TRY_MORE_DAMPING",
                flush=True,
            )

    return (
        None,
        {
            "augment_dim":
                U.shape[1],
            "augment_names":
                names,
            "gradient_capture":
                capture,
            "coupling":
                coupling,
            "coarse_eigs":
                evals,
            "hvp_calls":
                calls["count"],
            "linear_trials":
                reports,
        },
    )


def main():
    """Execute bounded 026A true-antigravity closure."""

    print(
        "=== 026A TRUE ANTIGRAVITY "
        "N73 AUGMENTED/DEFLATED MINRES ===",
        flush=True,
    )

    if (
        not R5_SOURCE.is_file()
        or sha256(
            R5_SOURCE
        )
        != EXPECTED_R5_SHA256
    ):
        raise RuntimeError(
            "Fail-closed R5 source audit failed"
        )

    print(
        "026A_UPSTREAM_R5_AUDIT=PASS",
        flush=True,
    )

    r5 = load_module(
        "026a_r5",
        R5_SOURCE,
    )

    r4 = r5.load_module(
        "026a_r4",
        r5.R4_SOURCE,
    )

    r3 = r4.load_module(
        "026a_r3",
        r4.R3_SOURCE,
    )

    r2 = r3.load_module(
        "026a_r2",
        r3.R2_SOURCE,
    )

    r = r3.load_module(
        "026a_r",
        r2.R_SOURCE,
    )

    qs2 = r3.load_module(
        "026a_qs2",
        r.QS2_SOURCE,
    )

    c2a = r3.load_module(
        "026a_c2a",
        r.C2A_SOURCE,
    )

    c2ar = qs2.load_module(
        "026a_c2ar",
        qs2.C2AR_SOURCE,
    )

    c2aqs = qs2.load_module(
        "026a_c2aqs",
        qs2.C2AQS_SOURCE,
    )

    cr2 = c2ar.load_module(
        "026a_cr2",
        c2ar.CR2_SOURCE,
    )

    cr3 = c2ar.load_module(
        "026a_cr3",
        c2ar.CR3_SOURCE,
    )

    cr4r = c2ar.load_module(
        "026a_cr4r",
        c2ar.CR4R_SOURCE,
    )

    (
        state,
        history,
        source,
        discarded,
        normerr,
        aug_total,
    ) = load_state(
        r5,
        qs2,
        cr3,
        cr4r,
    )

    (
        E,
        _e2,
        _e4,
        _e0,
        g,
        rms,
        gmax,
        station,
    ) = r.strict_stationarity(
        cr3,
        state.phi,
        state.dx,
    )

    deg_ok, degrees = (
        cr3.geometric_guard(
            state.phi,
            cr2,
            True,
        )
    )

    if not deg_ok:
        raise RuntimeError(
            "Starting field lost B=7"
        )

    start_merit = merit(
        rms,
        gmax,
    )

    print(
        "026A_START_SOURCE="
        f"{source.relative_to(ROOT)}",
        flush=True,
    )

    print(
        f"026A_START_HISTORY={len(history)} "
        f"DISCARDED={discarded} "
        f"NORMERR={normerr:.15e}",
        flush=True,
    )

    print(
        f"026A_START_ENERGY={E:.15e} "
        f"GRAD_RMS={rms:.15e} "
        f"GRAD_MAX={gmax:.15e} "
        f"MERIT={start_merit:.15e}",
        flush=True,
    )

    print(
        "026A_START_TOPOLOGY4="
        f"{cr3.topology4(state.phi,state.dx):.15e} "
        "DEGREES="
        f"{','.join(str(x) for x in degrees)}",
        flush=True,
    )

    cr4r.residual_localization(
        cr3,
        state,
        g,
    )

    r5.print_metrics(
        "026A_START",
        r5.residual_metrics(
            c2a,
            state.phi,
            g,
        ),
    )

    outer_reports = []
    accepted = 0

    for outer in range(
        1,
        MAX_OUTER + 1,
    ):

        if station:
            break

        print(
            f"\n=== 026A OUTER {outer} ===",
            flush=True,
        )

        old_phi = state.phi.copy()
        old_g = g.copy()

        old_merit = merit(
            rms,
            gmax,
        )

        pack, diagnostics = coupled_solve(
            r4,
            r5,
            r,
            qs2,
            c2a,
            cr2,
            cr3,
            state,
            history,
            E,
            g,
            rms,
            gmax,
            outer == 1,
        )

        diagnostics[
            "outer"
        ] = outer

        if pack is None:

            diagnostics[
                "accepted"
            ] = False

            outer_reports.append(
                diagnostics
            )

            print(
                "026A_COUPLED_DIRECTION="
                "UNRESOLVED",
                flush=True,
            )

            break

        history = (
            r.transport_history_after_step(
                cr3,
                cr4r,
                old_phi,
                pack["cand"],
                pack["direction"],
                pack["alpha"],
                old_g,
                pack["g"],
                history,
            )
        )

        state.phi = pack[
            "cand"
        ]

        state.accepted_total += 1

        E = pack[
            "E"
        ]

        g = pack[
            "g"
        ]

        rms = pack[
            "rms"
        ]

        gmax = pack[
            "gmax"
        ]

        station = pack[
            "station"
        ]

        aug_total += 1
        accepted += 1

        new_merit = merit(
            rms,
            gmax,
        )

        t4 = cr3.topology4(
            state.phi,
            state.dx,
        )

        deg_ok, degrees = (
            cr3.geometric_guard(
                state.phi,
                cr2,
                True,
            )
        )

        angle = (
            cr3.max_neighbor_angle(
                state.phi
            )
        )

        if not deg_ok:
            raise RuntimeError(
                "Accepted step lost B=7"
            )

        diagnostics.update(
            {
                "accepted":
                    True,
                "alpha":
                    pack["alpha"],
                "end_merit":
                    new_merit,
                "topology4":
                    t4,
                "angle":
                    angle,
            }
        )

        outer_reports.append(
            diagnostics
        )

        print(
            "026A_STEP_ACCEPTED=YES "
            f"ALPHA={pack['alpha']:.15e} "
            "MERIT_REDUCTION="
            f"{old_merit/max(new_merit,1e-300):.15e} "
            f"GRAD_RMS={rms:.15e} "
            f"GRAD_MAX={gmax:.15e} "
            f"TOPOLOGY4={t4:.15e} "
            f"ANGLE={angle:.15e}",
            flush=True,
        )

        save_checkpoint(
            state,
            history,
            E,
            rms,
            gmax,
            aug_total,
        )

        if (
            old_merit
            / max(
                new_merit,
                1e-300,
            )
            < 1.002
            and not station
        ):

            print(
                "026A_STAGNATION_STOP=YES",
                flush=True,
            )

            break

    final_merit = merit(
        rms,
        gmax,
    )

    t4 = cr3.topology4(
        state.phi,
        state.dx,
    )

    deg_ok, degrees = (
        cr3.geometric_guard(
            state.phi,
            cr2,
            True,
        )
    )

    angle = (
        cr3.max_neighbor_angle(
            state.phi
        )
    )

    print(
        "\n=== 026A FINAL AUDIT ===",
        flush=True,
    )

    print(
        f"026A_ACCEPTED_THIS_RUN="
        f"{accepted}",
        flush=True,
    )

    print(
        f"026A_FINAL_ENERGY={E:.15e} "
        f"GRAD_RMS={rms:.15e} "
        f"GRAD_MAX={gmax:.15e} "
        f"MERIT={final_merit:.15e}",
        flush=True,
    )

    print(
        "026A_STRICT_N73_STATIONARITY="
        + (
            "PASS"
            if station
            else "FAIL"
        ),
        flush=True,
    )

    print(
        f"026A_FINAL_TOPOLOGY4={t4:.15e} "
        "DEGREES="
        f"{','.join(str(x) for x in degrees)} "
        f"ANGLE={angle:.15e}",
        flush=True,
    )

    cr4r.residual_localization(
        cr3,
        state,
        g,
    )

    r5.print_metrics(
        "026A_FINAL",
        r5.residual_metrics(
            c2a,
            state.phi,
            g,
        ),
    )

    physical_gate = False
    force = None

    if station:

        diag = (
            cr3.continuum_local_diagnostics(
                state.phi,
                state.axis,
                state.dx,
                cr2,
            )
        )

        physical_gate = bool(
            deg_ok
            and diag.active_total
            > 0.0
            and diag.min_active_fraction
            <= -1e-2
            and diag.min_dec_scaled_margin
            >= -1e-9
            and diag.max_active_trace_scaled
            <= 1e-10
            and angle
            <= MAX_NEIGHBOR_ANGLE
        )

        print(
            "026A_ACTIVE_TOTAL="
            f"{diag.active_total:.15e}",
            flush=True,
        )

        print(
            "026A_MIN_ACTIVE_FRACTION="
            f"{diag.min_active_fraction:.15e}",
            flush=True,
        )

        print(
            "026A_MIN_DEC_SCALED_MARGIN="
            f"{diag.min_dec_scaled_margin:.15e}",
            flush=True,
        )

        print(
            "026A_MAX_ACTIVE_TRACE_SCALED="
            f"{diag.max_active_trace_scaled:.15e}",
            flush=True,
        )

        print(
            "026A_PHYSICAL_FIELD_GATE="
            + (
                "PASS"
                if physical_gate
                else "FAIL"
            ),
            flush=True,
        )

        if physical_gate:

            DATA.mkdir(
                parents=True,
                exist_ok=True,
            )

            np.savez(
                FINAL,
                phi=state.phi,
                axis=state.axis,
                dx=np.array(
                    state.dx
                ),
                B=np.array(
                    B
                ),
                eta=np.array(
                    ETA
                ),
                mass=np.array(
                    MASS
                ),
                energy=np.array(
                    E
                ),
                grad_rms=np.array(
                    rms
                ),
                grad_max=np.array(
                    gmax
                ),
                topology4=np.array(
                    t4
                ),
                active_total=np.array(
                    diag.active_total
                ),
                min_active_fraction=np.array(
                    diag.min_active_fraction
                ),
                min_dec_scaled_margin=np.array(
                    diag.min_dec_scaled_margin
                ),
                max_active_trace_scaled=np.array(
                    diag.max_active_trace_scaled
                ),
                source=np.array(
                    "026A_TRUE_ANTIGRAVITY_STRICT_N73"
                ),
            )

            n65 = (
                qs2.load_n65_force_reference()
            )

            aqr = c2aqs.load_module(
                "026a_aqr",
                c2aqs.AQR_SOURCE,
            )

            aqr.validate_analytic_formulae()

            print(
                "026A_ANALYTIC_FORCE_KERNEL_AUDIT="
                "PASS",
                flush=True,
            )

            force = (
                qs2.continuous_force_gate(
                    c2aqs,
                    aqr,
                    cr3,
                    state.phi,
                    state.axis,
                    state.dx,
                    n65,
                )
            )

    if not station:

        if (
            accepted > 0
            and final_merit
            < start_merit
        ):

            decision = (
                "INCOMPLETE_N73_COUPLED_SOLVER_PROGRESS"
            )

            nxt = (
                "RERUN_026A_FROM_CHECKPOINT"
            )

        else:

            decision = (
                "N73_AUGMENTED_MINRES_STAGNATION"
            )

            nxt = (
                "026B_TARGETED_RITZ_LOW_MODE_DISCRETIZATION_GATE"
            )

        hess = (
            "DEFERRED_N73_STATIONARITY_UNRESOLVED"
        )

    elif not physical_gate:

        decision = (
            "RED_STRICT_N73_PHYSICAL_FIELD_GATE"
        )

        nxt = (
            "RERANK_TRUE_ANTIGRAVITY_FIELD_BRANCH"
        )

        hess = (
            "DEFERRED_BY_PHYSICAL_FALSIFIER"
        )

    elif (
        force is not None
        and force["certified"]
        and force["sign"]
        == "OUTWARD"
    ):

        decision = (
            "GREEN_STRICT_N73_CONTINUOUS_OUTWARD_SENTINEL"
        )

        nxt = (
            "026B_N81_STATIONARY_COMPANION_"
            "CONTINUOUS_FORCE_CONVERGENCE"
        )

        hess = (
            "DEFERRED_UNTIL_N73_N81_"
            "FORCE_CONVERGENCE"
        )

    elif (
        force is not None
        and force["certified"]
        and force["sign"]
        == "INWARD"
    ):

        decision = (
            "RED_STRICT_N73_CONTINUOUS_SENTINEL_INWARD"
        )

        nxt = (
            "026B_N81_CONFIRM_OR_"
            "PAYLOAD_VOLUME_RERANK"
        )

        hess = (
            "DEFERRED_BY_FORCE_FALSIFIER"
        )

    else:

        decision = (
            "INCOMPLETE_N73_CONTINUOUS_FORCE_SIGN"
        )

        nxt = (
            "026B_N81_ACTUAL_FIELD_RESOLUTION"
        )

        hess = (
            "DEFERRED_FORCE_CONTINUUM_UNRESOLVED"
        )

    summary = {
        "simulation":
            "026A",

        "branch":
            "TRUE_ANTIGRAVITY",

        "field": {
            "B":
                B,
            "eta":
                ETA,
            "m":
                MASS,
            "N":
                N,
        },

        "start_merit":
            start_merit,

        "outer_reports":
            outer_reports,

        "final": {
            "energy":
                E,
            "grad_rms":
                rms,
            "grad_max":
                gmax,
            "merit":
                final_merit,
            "stationary":
                station,
            "topology4":
                t4,
            "degrees":
                list(
                    degrees
                ),
            "max_neighbor_angle":
                angle,
            "physical_gate":
                physical_gate,
        },

        "force":
            force,

        "decision":
            decision,

        "next":
            nxt,

        "full_physical_hessian":
            hess,

        "claims": {
            "practical_antigravity_device":
                False,
            "new_physics_discovery":
                False,
            "heuristic_increase_authorized":
                False,
        },
    }

    DATA.mkdir(
        parents=True,
        exist_ok=True,
    )

    SUMMARY.write_text(
        json.dumps(
            summary,
            indent=2,
            sort_keys=True,
            default=json_default,
        )
        + "\n"
    )

    print(
        "\n=== 026A DECISION ===",
        flush=True,
    )

    print(
        f"026A_DECISION={decision}",
        flush=True,
    )

    print(
        f"FULL_PHYSICAL_HESSIAN={hess}",
        flush=True,
    )

    print(
        f"NEXT={nxt}",
        flush=True,
    )

    print(
        "NONLINEAR_EINSTEIN_SKYRME="
        "NOT_AUTHORIZED_UNTIL_FINE_FORCE_"
        "CONVERGENCE_AND_STABILITY",
        flush=True,
    )

    print(
        "PRACTICAL_ANTIGRAVITY_DEVICE=NO",
        flush=True,
    )

    print(
        "NEW_PHYSICS_DISCOVERY=NO",
        flush=True,
    )

    print(
        "CURRENT_KNOWLEDGE_HEURISTIC="
        "APPROXIMATELY_70_TO_71_PERCENT_"
        "NOT_A_PROBABILITY",
        flush=True,
    )

    print(
        f"OUT_SUMMARY={SUMMARY}",
        flush=True,
    )

    if CHECKPOINT.is_file():
        print(
            f"OUT_CHECKPOINT={CHECKPOINT}",
            flush=True,
        )

    if physical_gate:
        print(
            f"OUT_STRICT_FIELD={FINAL}",
            flush=True,
        )


if __name__ == "__main__":
    main()
