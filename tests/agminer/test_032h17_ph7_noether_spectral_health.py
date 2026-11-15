"""PH7 tests: coupled kinetic, spectral, and resolution controls."""

from dataclasses import replace
import math

import numpy as np
import pytest

from antigravity_research.agminer import (
    hook17_ph6_same_action_bridge as ph6
)
from antigravity_research.agminer import (
    hook17_ph7_noether_spectral_health as ph7
)


def test_exact_coupled_hessian():
    assert ph7.hessian_symbolic()[
        "local_joint_velocity_hessian"
    ] == "PASS_EXACT"


def test_frozen_K_is_not_sufficient():
    r = ph7.frozen_K_pass_joint_fail_example()

    assert r["frozen_K_positive"] > 0
    assert r["joint_S_negative"] < 0


def test_fourier_skew_adjoint_and_nyquist():
    rng = np.random.default_rng(17)
    a = rng.standard_normal(128)
    b = rng.standard_normal(128)
    D = ph7.spectral_D

    assert abs(
        np.dot(a, D(b, .13))
        + np.dot(D(a, .13), b)
    ) < 1e-11

    nyquist = (-1.)**np.arange(128)

    assert np.max(
        np.abs(D(nyquist, .13))
    ) < 1e-12


def test_fourier_analytic_sine_derivative():
    n = 128
    x = np.arange(n)*2*math.pi/n

    assert np.max(
        np.abs(
            ph7.spectral_D(
                np.sin(3*x), 2*math.pi/n
            ) - 3*np.cos(3*x)
        )
    ) < 1e-11


@pytest.mark.parametrize(
    "length,dx", [(7, .1), (8, -1.)]
)
def test_invalid_fourier_grid(length, dx):
    with pytest.raises(ValueError):
        ph7.spectral_D(
            np.ones(length), dx
        )


def excited_state():
    spec = ph6.Spec(n=96)
    y = ph6.initial(spec)
    n = spec.n

    x = (
        np.arange(n)*spec.length/n
        - spec.length/2
    )

    y[:n] = .02*np.sin(
        2*np.pi*x/spec.length
    )
    y[n:2*n] = .01*np.cos(
        4*np.pi*x/spec.length
    )
    y[2*n:3*n] = .013*np.sin(
        4*np.pi*x/spec.length
    )
    y[3*n:4*n] = .02*np.cos(
        2*np.pi*x/spec.length
    )
    y[4*n+1] = .021

    return spec, y


def test_global_schur_against_dense_hessian():
    spec, y = excited_state()
    d = ph6.state_data(y, spec)

    dx = spec.length/spec.n
    V = d["V"]
    h = d.get("h", d.get("lorentz_h"))

    rho = d["rho"]
    F = d["F"]
    sigma_prime = d["spr"]

    Fp = F*sigma_prime
    Fpp = F*(
        sigma_prime**2-2*spec.beta
    )

    ga, gb = d["ga"], d["gb"]
    n = spec.n

    H = np.eye(2*n+1)*dx

    for j in range(n):
        q = np.array([
            -gb[j], ga[j]
        ])

        block = dx*(
            np.eye(2)
            - rho[j]*h*Fpp[j]
            * np.outer(q, q)
        )

        indices = [j, n+j]

        H[np.ix_(indices, indices)] = block

        H[indices, 2*n] = (
            dx*rho[j]*V/h*Fp[j]*q
        )

        H[2*n, indices] = H[indices, 2*n]

    H[-1, -1] = dx*np.sum(
        rho*F/h**3
    )

    independent = float(
        H[-1, -1]
        - H[-1, :-1] @ np.linalg.solve(
            H[:-1, :-1],
            H[:-1, -1],
        )
    )

    result = ph7.health(spec, y)

    assert result["joint_positive"]
    assert result["S"] == pytest.approx(
        independent,
        rel=1e-11,
        abs=1e-12,
    )

    assert np.linalg.eigvalsh(H)[0] > 0


def test_joint_hessian_against_full_action_differences():
    spec, y = excited_state()
    d = ph6.state_data(y, spec)

    n = spec.n
    dx = spec.length/n

    tail = d.get("tail", d.get("t"))

    Z, pZ, qx, vx, X, Ux, qy, vy, Y, Uy = tail

    ua0 = d["ua"].copy()
    ub0 = d["ub"].copy()
    V0 = d["V"]

    idx = int(np.argmin(
        abs(
            np.arange(n)*dx
            - spec.length/2
            - (Z+.11)
        )
    ))

    def lag(uadd=0., vadd=0.):
        ua = ua0.copy()
        ua[idx] += uadd

        return ph6.action_lagrangian(
            d["a"], d["b"],
            ua, ub0,
            Z, V0+vadd,
            qx, vx, X, Ux,
            qy, vy, Y, Uy,
            spec,
        )

    hstep = 4e-4

    huu = (
        lag(hstep)
        + lag(-hstep)
        - 2*lag()
    )/hstep**2

    hvv = (
        lag(vadd=hstep)
        + lag(vadd=-hstep)
        - 2*lag()
    )/hstep**2

    huv = (
        lag(hstep, hstep)
        - lag(hstep, -hstep)
        - lag(-hstep, hstep)
        + lag(-hstep, -hstep)
    )/(4*hstep*hstep)

    rho = d["rho"][idx]
    F = d["F"][idx]
    s = d["spr"][idx]
    q = -d["gb"][idx]
    h = d.get("h", d.get("lorentz_h"))

    expected_uu = (
        dx*(1-rho*h*F*(s*s-2*spec.beta)*q*q)
    )
    expected_uv = (
        dx*rho*V0/h*F*s*q
    )
    expected_vv = (
        dx*np.sum(d["rho"]*d["F"]/h**3)
    )

    assert huu == pytest.approx(
        expected_uu, abs=1e-6
    )
    assert huv == pytest.approx(
        expected_uv, abs=1e-6
    )
    assert hvv == pytest.approx(
        expected_vv, abs=1e-6
    )


def test_spectral_neutral_impulse_convergence():
    medium = ph7.evolve_spectral(
        replace(ph6.Spec(), n=256)
    )
    fine = ph7.evolve_spectral(
        replace(ph6.Spec(), n=384)
    )

    assert fine[
        "neutral_signed_momentum_change"
    ] > 0

    assert abs(
        fine["neutral_signed_momentum_change"]
        - medium["neutral_signed_momentum_change"]
    ) < 2e-5

    assert (
        fine["max_momentum_drift"]
        < .2*medium["max_momentum_drift"]
    )

    assert fine["max_energy_drift"] < 1e-9
    assert fine["full_joint_hessian_pass_all_times"]


def test_no_portal_and_even_only_controls():
    no_portal = ph7.evolve_spectral(
        replace(
            ph6.Spec(), n=256,
            alpha=0., beta=0.
        )
    )

    even = ph7.evolve_spectral(
        replace(
            ph6.Spec(), n=256,
            alpha=0.
        )
    )

    assert abs(
        no_portal["neutral_signed_momentum_change"]
    ) < 1e-10

    assert abs(
        even["neutral_signed_momentum_change"]
    ) < 1e-8


def test_negative_even_original_grid_artifact():
    coarse = ph6.run_case(
        replace(
            ph6.Spec(), n=96,
            alpha=0.
        ),
        samples=41,
    )

    fine = ph6.run_case(
        replace(
            ph6.Spec(), n=256,
            alpha=0.
        ),
        samples=41,
    )

    assert abs(
        coarse["neutral_exact_momentum_change"]
    ) > 1e-6

    assert abs(
        fine["neutral_exact_momentum_change"]
    ) < 1e-8


def test_source_off_no_physical_promotion():
    result = ph7.evolve_spectral(
        replace(
            ph6.Spec(), n=128,
            q0_x=0., q0_y=0.
        ),
        samples=17,
    )

    assert result[
        "neutral_signed_momentum_change"
    ] == pytest.approx(0, abs=1e-12)

    assert result["earth_craft_lift"] == "NOT_DERIVED"
    assert result["closed_cycle"] is False


def test_ph6_derivative_restored_after_control():
    original = ph6.D

    ph7.evolve_spectral(
        replace(ph6.Spec(), n=128),
        samples=17,
    )

    assert ph6.D is original


def test_missing_history_blocks_promotion(tmp_path):
    result = ph7.run(tmp_path)

    assert result["gates"][
        "P0_PH6_PROVENANCE"
    ] == "UNRESOLVED"

    assert result["gates"][
        "P3_EARTH_DOWN_WHOLE_CRAFT_UP"
    ] == "NOT_DERIVED"

    assert result["gates"][
        "STRICT_COMPLETE_LT10MJ"
    ] == "NOT_CERTIFIED"

    assert result["gates"][
        "006D_REPLACED"
    ] == "NO"

    assert result["gates"][
        "P2_PH6_NEGATIVE_EVEN_SIGNAL"
    ] == "DEMOTED_GRID_ARTIFACT"


def test_history_mismatch_fails_closed(tmp_path):
    directory = (
        tmp_path
        / "src/antigravity_research/agminer"
    )
    directory.mkdir(parents=True)

    (
        directory/"hook17_ph6_same_action_bridge.py"
    ).write_text("not original PH6 source")

    assert ph7.provenance(tmp_path)[
        "ph6_module"
    ]["status"] == "HASH_MISMATCH"
