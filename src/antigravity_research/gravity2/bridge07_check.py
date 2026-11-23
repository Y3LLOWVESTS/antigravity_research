"""Independent verification of GRAVITY2-07 numerical fields.

Reconstructs the Euler residual, Bianchi identity and discrete-action
finite differences. PASS is NOT source, gravity, exterior or lift closure.
"""
from __future__ import annotations

import json
import numpy as np

from .engine import (
    ROOT,
    atomic_json,
    atomic_text,
    digest,
)
from . import bridge07 as run


def D(v, h, axis):
    n = v.shape[axis]

    left = np.take(
        v,
        (np.arange(n)-1) % n,
        axis=axis,
    )

    right = np.take(
        v,
        (np.arange(n)+1) % n,
        axis=axis,
    )

    return (right-left)/(2*h)


def independent_audit(a, f, b, h):
    ax, az = D(a, h, 0), D(a, h, 1)
    bx, bz = D(b, h, 0), D(b, h, 1)

    P = ax*bz-az*bx
    alpha, beta = .08, .005

    sigma = alpha*P-beta*P*P

    K = (
        (1.25-.4*a)**2*f*f
        -D(f, h, 0)**2
        -D(f, h, 1)**2
    )

    V = .4*f*f+.1*f**4

    Pi = (
        np.exp(2*sigma)*K
        -4*np.exp(4*sigma)*V
    )*(alpha-2*beta*P)

    forcing = (
        D(Pi*az, h, 0)
        -D(Pi*ax, h, 1)
    )

    lap = (
        D(D(b, h, 0), h, 0)
        +D(D(b, h, 1), h, 1)
    )

    residual = -lap-forcing

    bianchi = (
        D(-D(b, h, 1), h, 0)
        +D(D(b, h, 0), h, 1)
    )

    energy_density = .5*np.mean(
        bx*bx+bz*bz
    )

    action = np.sum(
        -.5*(bx*bx+bz*bz)
        +.5*np.exp(2*sigma)*K
        -np.exp(4*sigma)*V
    )*h*h

    return (
        residual,
        bianchi,
        float(energy_density),
        float(action),
        forcing,
    )


def independent_action(a, f, b, h):
    return independent_audit(
        a, f, b, h
    )[3]


def finite_difference_action(a, f, b, h):
    # Test off shell, avoiding a vacuous zero=zero check.
    n = len(a)

    x = np.arange(n)*2*np.pi/n
    X, Z = np.meshgrid(x, x, indexing="ij")

    off = (
        b
        +.035*np.cos(2*X+Z)*np.sin(Z)
    )

    residual, _, _, _, _ = independent_audit(
        a, f, off, h
    )

    perturb = np.zeros_like(b)
    perturb[3, 4] = 1

    epsilon = 1e-4

    numeric = (
        independent_action(
            a, f, off+epsilon*perturb, h
        )
        -independent_action(
            a, f, off-epsilon*perturb, h
        )
    )/(2*epsilon)

    predicted = -h*h*float(
        np.sum(residual*perturb)
    )

    return (
        abs(numeric-predicted),
        abs(predicted),
    )


def verify(folder):
    checks = {}

    def gate(label, ok):
        checks[label] = bool(ok)

        if not ok:
            raise AssertionError(label)

    try:
        manifest = json.loads(
            (folder/"manifest.json").read_text()
        )

        science = json.loads(
            (folder/"science.json").read_text()
        )

        recorded = dict(
            line.split("  ", 1)[::-1]
            for line in (
                folder/"hashes.sha256"
            ).read_text().splitlines()
        )

        for name in (
            "manifest.json",
            "science.json",
            "fields.npz",
        ):
            gate(
                "SHA " + name,
                recorded[name] == digest(folder/name),
            )

        gate(
            "archive science SHA",
            science["field_archive_sha256"]
            == digest(folder/"fields.npz"),
        )

        gate(
            "run linkage",
            manifest["run_id"]
            == science["run_id"]
            == folder.name,
        )

        gate(
            "producer source hashes",
            manifest["producer_sha256"]
            == run.sources(),
        )

        gate(
            "L1 bounded",
            manifest["level"] == "L1"
            and manifest["workers"] == 1
            and 0 < manifest["time_ceiling_s"] <= 60,
        )

        gate(
            "soft watchdog",
            science["resource"]["watchdog"]
            == "SOFT_PSUTIL_PROCESS",
        )

        gate(
            "parent hashes",
            science["parents"] == run.parents()
            and science["parents"]["all_match"],
        )

        gate(
            "source not reclassified",
            science["source_still_prescribed"] is True
            and science["real_finite_source"]
                == "NOT_ESTABLISHED"
            and science["source_support_Earth"]
                == "NOT_DERIVED",
        )

        gate(
            "no gravitational promotion",
            science["Einstein_gravity"]
                == "NOT_SOLVED"
            and science["whole_craft_lift"]
                == "NOT_DERIVED"
            and science["complete_energy_SI"]
                == "NOT_CERTIFIED"
            and science["qualified_survivors"] == 0
            and not science["006D_replaced"],
        )

        gate(
            "no solver-level promotion",
            science["L2_authorized"] is False
            and science["full_repository_regression"]
                == "NOT_RUN",
        )

        gate(
            "no previous-source modification",
            manifest["previous_source_modification"]
                == "NONE"
            and manifest["AGMINER"]
                == "READ_ONLY_PINNED_HASHES_NOT_EXECUTED",
        )

        gate(
            "execution completed",
            science["execution_status"]
                == "COMPLETED",
        )

        e = science["evidence"]

        gate(
            "scoped decision",
            e["decision"]
            == "2D_HODGE_VALID_NONLINEAR_Y_RESPONSE; "
               "FROZEN_SOURCE_AND_X_NOT_PHYSICALIZED",
        )

        gate(
            "four resolutions",
            tuple(
                row["n"] for row in e["rows"]
            ) == (9, 15, 23, 31),
        )

        gate(
            "not an exterior",
            e["geometry"]
            == "2D_PERIODIC_FLAT_XZ_PATCH_NOT_FINITE_EXTERIOR",
        )

        with np.load(
            folder/"fields.npz",
            allow_pickle=False,
        ) as archive:

            gate(
                "exact archive fields",
                set(archive.files)
                == {
                    f"{kind}_{n}"
                    for kind in ("a", "b", "f")
                    for n in (9, 15, 23, 31)
                },
            )

            energies = []

            for row in e["rows"]:
                n = row["n"]
                h = 2*np.pi/n

                a, f, b = (
                    np.asarray(
                        archive[f"{name}_{n}"],
                        dtype=float,
                    )
                    for name in ("a", "f", "b")
                )

                gate(
                    f"shape and finite n={n}",
                    all(
                        array.shape == (n, n)
                        and np.isfinite(array).all()
                        for array in (a, f, b)
                    ),
                )

                (
                    residual,
                    bianchi,
                    energy,
                    action,
                    forcing,
                ) = independent_audit(a, f, b, h)

                relative = float(
                    np.linalg.norm(residual)
                    /max(
                        float(np.linalg.norm(forcing)),
                        1.0,
                    )
                )

                gate(
                    f"Euler residual n={n}",
                    relative < 1e-10
                    and abs(
                        relative
                        -row["equation_residual_relative"]
                    ) < 1e-12,
                )

                gate(
                    f"Bianchi n={n}",
                    np.max(abs(bianchi)) < 1e-12
                    and abs(
                        np.max(abs(bianchi))
                        -row["bianchi_max_abs"]
                    ) < 1e-12,
                )

                gate(
                    f"magnetic energy diagnostic n={n}",
                    abs(
                        energy
                        -row[
                            "magnetic_gradient_energy_density_canonical"
                        ]
                    ) < 1e-12,
                )

                gate(
                    f"action diagnostic n={n}",
                    abs(
                        action
                        -row["off_shell_action_canonical"]
                    ) < 1e-9,
                )

                gate(
                    f"nonzero Y n={n}",
                    np.max(abs(b)) > 1e-5
                    and abs(
                        np.max(abs(b))
                        -row["y_field_max_abs"]
                    ) < 1e-10,
                )

                gate(
                    f"constant zero mode n={n}",
                    abs(np.mean(b)) < 1e-12,
                )

                energies.append(energy)

                if n == 15:
                    error, signal = finite_difference_action(
                        a, f, b, h
                    )

                    gate(
                        "same discrete action finite difference",
                        error < 1e-7
                        and signal > 1e-5,
                    )

                    wrong = (
                        -D(D(b, h, 0), h, 0)
                        -D(D(b, h, 1), h, 1)
                        +forcing
                    )

                    gate(
                        "wrong portal sign rejected",
                        np.linalg.norm(wrong) > 1e-3,
                    )

                    Pi_const = np.full_like(a, .37)

                    null = (
                        D(
                            Pi_const*D(a, h, 1),
                            h, 0,
                        )
                        -D(
                            Pi_const*D(a, h, 0),
                            h, 1,
                        )
                    )

                    gate(
                        "constant Pi topological null",
                        np.max(abs(null)) < 1e-12,
                    )

        gate(
            "resolution sensitivity only",
            0
            < abs(energies[-1]-energies[-2])
                /energies[-1]
            < .03,
        )

        gate(
            "portal-off zero Y",
            e["controls"][
                "no_portal_zero_Y_max"
            ] == 0,
        )

        gate(
            "collinear and constant Pi controls",
            e["controls"][
                "collinear_1D_zero_source_max"
            ] < 1e-12
            and e["controls"][
                "constant_Pi_topological_source_max"
            ] < 1e-12,
        )

        gate(
            "historical R3B failure preserved",
            e["parent_history"][
                "R3B_loaded_min_m_s2"
            ] == -129.67185782242464
            and e["parent_history"][
                "R3B_prescribed_capacity_J"
            ] == 1.5429162116460216
            and e["parent_history"][
                "R3B_history_recomputed"
            ] is False,
        )

        status = (
            "PASS_SCOPED_2D_NUMERICAL_Y_ONLY_NO_SOURCE"
        )

        report = {
            "program": "GRAVITY2-07-INDEPENDENT",
            "run_id": folder.name,
            "status": status,
            "checks": checks,
            "science_sha256":
                digest(folder/"science.json"),
            "source": "NOT_ESTABLISHED",
            "whole_craft_lift": "NOT_DERIVED",
        }

    except Exception as exc:
        report = {
            "program": "GRAVITY2-07-INDEPENDENT",
            "run_id": folder.name,
            "status": "HOLD",
            "checks": checks,
            "error": repr(exc),
            "whole_craft_lift": "NOT_DERIVED",
        }

    destination = folder/"verification.json"

    if destination.exists():
        if json.loads(destination.read_text()) != report:
            print(
                "GRAVITY2_07_REVERIFY_DIFFERS_NO_OVERWRITE"
            )
            return 3

    else:
        atomic_json(destination, report)

        atomic_text(
            folder/"verification.sha256",
            digest(destination)
            + "  verification.json\n",
        )

    print(
        "GRAVITY2_07_VERIFY=" + report["status"]
    )

    print(
        "CHECKS="
        + str(sum(checks.values()))
        + "/"
        + str(len(checks))
    )

    if "error" in report:
        print("ERROR=" + report["error"])

    print(
        "VERIFICATION_SHA256="
        + digest(destination)
    )

    return (
        0 if report["status"]
        == "PASS_SCOPED_2D_NUMERICAL_Y_ONLY_NO_SOURCE"
        else 3
    )
