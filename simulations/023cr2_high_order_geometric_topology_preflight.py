#!/usr/bin/env python3
"""023CR2 — high-order checkerboard-free geometric-topology preflight.

023CR2 V2 PARSER REPAIR
-----------------------
The only scientific-code change from the initial 023CR2 preflight is a strict
single-line numeric-log parser repair: values are terminated by CR/LF rather
than the erroneous raw-regex character class that excluded literal backslash
and ``n``. No physical thresholds, equations, grids, topology algorithms, or
promotion criteria are changed.

PURPOSE
-------
Resolve the remaining Cartesian representation question exposed by 023CR
before spending more computation on unrestricted relaxation or a Hessian.

023C failed because a centered-difference lattice admitted a checkerboard
null mode and did not faithfully represent the initial B=7 field.  023CR
replaced that action with a nearest-neighbor link action, proved the
checkerboard diagnosis, and recovered clean convergence toward the exact B=7
continuum state.  At N=113 it obtained

    B_4 ~= 6.995398,

with only ~6.6e-4 relative topology error, but the second-order link action
still underestimated total energy by ~1.20 percent and E4 by ~1.65 percent.

This run asks the cheapest next question:

    Can a higher-order checkerboard-free Cartesian representation achieve
    sub-percent continuum fidelity and an independent integer |B|=7
    geometric degree witness at moderate resolution?

If yes, the numerical representation problem is repaired well enough to
justify a separate topology-guarded unrestricted relaxation gate.  This run
does NOT itself perform that relaxation and therefore cannot promote physical
stability.

CONTINUUM MODEL
---------------
The static SU(2) Skyrme field is represented by

    phi = (sigma, pi_1, pi_2, pi_3),
    phi . phi = 1,

with

    E = integral (e2 + e4 + V) d^3x,

    e2 = sum_i |d_i phi|^2,

    e4 = sum_(i<j) [
        |d_i phi|^2 |d_j phi|^2
        - (d_i phi . d_j phi)^2
    ],

    V = m^2 (1-sigma)(1+eta sigma).

The selected candidate remains

    B = 7,
    eta = 0.4,
    m = 8.

HIGH-ORDER CHECKERBOARD-FREE DERIVATIVE
---------------------------------------
Use the fourth-order one-sided derivative

    D_+ f_i =
      (-25 f_i + 48 f_{i+1} - 36 f_{i+2}
       +16 f_{i+3} - 3 f_{i+4}) / (12 dx),

and average the forward- and backward-oriented energies.

For a Fourier mode z = exp(i theta), the forward symbol is

    P(z) = (-25 + 48z - 36z^2 + 16z^3 - 3z^4)/12.

Its only unit-circle zero is z=1.  In particular the checkerboard/Nyquist
mode z=-1 has |P(-1)|=32/3, so it cannot hide at zero derivative energy.

GEOMETRIC DEGREE WITNESS
------------------------
Each Cartesian cube is decomposed into six consistently oriented spatial
tetrahedra.  For a generic regular target q on S^3, a field tetrahedron
contains a preimage when its normalized affine interpolation satisfies

    sum_a lambda_a phi_a = c q,
    sum_a lambda_a = 1,
    lambda_a >= 0,
    c > 0.

The signed preimage count is an integer degree witness.  Three generic targets
must independently return the same sign and |degree|=7.  This is independent
of the derivative-integral topology estimator.

CHEAPEST DECISIVE EXPERIMENT
----------------------------
1. Audit the exact 023CR source and log.
2. Fit the observed 023CR convergence order from N=81,97,113.
3. Verify analytically/numerically that the fourth-order one-sided symbol has
   no nonphysical unit-circle zero.
4. Reconstruct the exact rational-map B=7 field on a moderate resolution
   ladder.
5. Require sub-percent total-energy fidelity, <=1.5 percent E4 error,
   fourth-order topology error <=1 percent, smooth nearest-neighbor angles,
   and exact geometric degree |B|=7 for three regular targets.
6. Require two adjacent passing resolutions with stable energy/topology.

PROMOTION CONDITION
-------------------
023CR2 is GREEN_NUMERICAL_REPRESENTATION_REPAIR only if:

    UPSTREAM_023CR_AUDIT=PASS
    OBSERVED_LINK_ACTION_CONVERGENCE=PASS
    HIGH_ORDER_SYMBOL_NO_SPURIOUS_UNIT_CIRCLE_ZERO=PASS
    INITIAL_HIGH_ORDER_RESOLUTION_PAIR=FOUND
    INITIAL_HIGH_ORDER_ENERGY_RECONSTRUCTION=PASS
    INITIAL_DERIVATIVE_TOPOLOGY_RECONSTRUCTION=PASS
    INITIAL_GEOMETRIC_B7_DEGREE=PASS

A green result does not increase the project heuristic.  It authorizes the
next physical/numerical gate:

    023CR3_GEOMETRIC_DEGREE_GUARDED_UNRESTRICTED_RELAXATION

Only after a converged unrestricted relaxation should the project rebuild the
full tangent Hessian and dense finite-payload orientation test.

STOP RULE
---------
If this high-order/geometric representation still cannot reproduce the exact
B=7 state at moderate resolution, do not brute-force relaxation.  Move to an
adaptive/spectral Cartesian representation.

CLAIM CLASSIFICATION
--------------------
PROJECT_DERIVED_023CR2_HIGH_ORDER_GEOMETRIC_TOPOLOGY_PREFLIGHT
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import importlib.util
import math
from pathlib import Path
import re
import sys

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
A23_SOURCE = ROOT / "simulations/023a_topological_false_core_multiskyrmion_gr_repulsion_gate.py"
B23_SOURCE = ROOT / "simulations/023b_exact_rational_map_full3d_tmunu_gravity_promotion_gate.py"
C23_SOURCE = ROOT / "simulations/023c_unrestricted_cartesian_3d_relaxation_and_full_physical_hessian.py"
CR23_SOURCE = ROOT / "simulations/023cr_checkerboard_free_link_lattice_topology_repair.py"
CR23_LOG = ROOT / "results/logs/023cr_checkerboard_free_link_lattice_topology_repair.log"

EXPECTED_023A_SHA256 = "0087a5d2b4f93667308cabf4c3c498200ed29381e9493acf21714df7d8e11c9b"
EXPECTED_023B_SHA256 = "6bf99785e67cfe1b2dfcb460bc3145a24115e25949e112f8480a89c880a2803c"
EXPECTED_023C_SHA256 = "9fd323a2f845c0373f7926af11f09c563138386b18c8fa3c091acb114318a675"
EXPECTED_023CR_SHA256 = "925c61407aa21a97198be98fe930155e338bb02cf8e0ea8bbf062cbf9c24d327"

B = 7
ETA = 0.40
MASS = 8.0
GRID_LEVELS = (53, 57, 65, 73, 81, 89, 97)

MAX_TOTAL_ENERGY_RELERR = 1.0e-2
MAX_E2_RELERR = 1.0e-2
MAX_E4_RELERR = 1.5e-2
MAX_E0_RELERR = 2.0e-4
MAX_TOPOLOGY4_RELERR = 1.0e-2
MAX_NEIGHBOR_ANGLE = 0.70
MAX_PAIR_ENERGY_RELCHANGE = 8.0e-3
MAX_PAIR_E4_RELCHANGE = 1.0e-2
MAX_PAIR_TOPOLOGY_ABSCHANGE = 8.0e-3

GEOMETRIC_TARGETS = (
    (0.20, 0.30, 0.40, 0.84),
    (-0.20, 0.50, -0.40, 0.74),
    (0.30, -0.60, 0.20, 0.71),
)

FORWARD_COEFF = np.array([-25.0, 48.0, -36.0, 16.0, -3.0]) / 12.0
BACKWARD_COEFF = np.array([25.0, -48.0, 36.0, -16.0, 3.0]) / 12.0

TETRA_OFFSETS = np.array(
    [
        [[0,0,0],[1,0,0],[1,1,0],[1,1,1]],
        [[0,0,0],[1,1,0],[0,1,0],[1,1,1]],
        [[0,0,0],[0,1,0],[0,1,1],[1,1,1]],
        [[0,0,0],[0,1,1],[0,0,1],[1,1,1]],
        [[0,0,0],[0,0,1],[1,0,1],[1,1,1]],
        [[0,0,0],[1,0,1],[1,0,0],[1,1,1]],
    ],
    dtype=int,
)


@dataclass
class Audit:
    n: int
    dx: float
    energy: float
    e2: float
    e4: float
    e0: float
    energy_relerr: float
    e2_relerr: float
    e4_relerr: float
    e0_relerr: float
    topology4: float
    topology4_relerr: float
    geometric_degrees: tuple[int, ...]
    max_neighbor_angle: float
    passed: bool


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require_file(path: Path) -> None:
    if not path.exists():
        raise RuntimeError(f"Missing required file: {path}")


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    try:
        spec.loader.exec_module(module)
    except Exception:
        sys.modules.pop(name, None)
        raise
    return module


def relative_error(a: float, b: float) -> float:
    return abs(a-b) / max(abs(a), abs(b), 1.0e-300)


def metric_terms(qx, qy, qz):
    gxx = np.sum(qx*qx, axis=-1)
    gyy = np.sum(qy*qy, axis=-1)
    gzz = np.sum(qz*qz, axis=-1)
    gxy = np.sum(qx*qy, axis=-1)
    gxz = np.sum(qx*qz, axis=-1)
    gyz = np.sum(qy*qz, axis=-1)
    e2 = gxx + gyy + gzz
    e4 = (
        gxx*gyy - gxy*gxy
        + gxx*gzz - gxz*gxz
        + gyy*gzz - gyz*gyz
    )
    return e2, e4


def oriented_high_order_energy(phi: np.ndarray, dx: float, forward: bool):
    n = phi.shape[0]
    coeff = FORWARD_COEFF if forward else BACKWARD_COEFF
    if forward:
        qx = sum(coeff[s]*phi[s:n-4+s, :-4, :-4] for s in range(5)) / dx
        qy = sum(coeff[s]*phi[:-4, s:n-4+s, :-4] for s in range(5)) / dx
        qz = sum(coeff[s]*phi[:-4, :-4, s:n-4+s] for s in range(5)) / dx
    else:
        qx = sum(coeff[s]*phi[4-s:n-s, 4:, 4:] for s in range(5)) / dx
        qy = sum(coeff[s]*phi[4:, 4-s:n-s, 4:] for s in range(5)) / dx
        qz = sum(coeff[s]*phi[4:, 4:, 4-s:n-s] for s in range(5)) / dx
    e2, e4 = metric_terms(qx, qy, qz)
    return float(np.sum(e2)*dx**3), float(np.sum(e4)*dx**3)


def high_order_energy(phi: np.ndarray, dx: float):
    E2f, E4f = oriented_high_order_energy(phi, dx, True)
    E2b, E4b = oriented_high_order_energy(phi, dx, False)
    E2 = 0.5*(E2f+E2b)
    E4 = 0.5*(E4f+E4b)
    sigma = phi[2:-2, 2:-2, 2:-2, 0]
    V = MASS*MASS*(1.0-sigma)*(1.0+ETA*sigma)
    E0 = float(np.sum(V)*dx**3)
    return E2+E4+E0, E2, E4, E0


def central4_derivatives(phi: np.ndarray, dx: float):
    c = 1.0/(12.0*dx)
    qx = (-phi[4:,2:-2,2:-2] + 8*phi[3:-1,2:-2,2:-2]
          -8*phi[1:-3,2:-2,2:-2] + phi[:-4,2:-2,2:-2])*c
    qy = (-phi[2:-2,4:,2:-2] + 8*phi[2:-2,3:-1,2:-2]
          -8*phi[2:-2,1:-3,2:-2] + phi[2:-2,:-4,2:-2])*c
    qz = (-phi[2:-2,2:-2,4:] + 8*phi[2:-2,2:-2,3:-1]
          -8*phi[2:-2,2:-2,1:-3] + phi[2:-2,2:-2,:-4])*c
    return qx, qy, qz


def topology4(phi: np.ndarray, dx: float) -> float:
    qx, qy, qz = central4_derivatives(phi, dx)
    center = phi[2:-2,2:-2,2:-2]
    mat = np.stack([center,qx,qy,qz], axis=-1)
    det = np.linalg.det(mat)
    return -float(np.sum(det)*dx**3/(2.0*math.pi**2))


def max_neighbor_angle(phi: np.ndarray) -> float:
    out = []
    for a,b in ((phi[1:],phi[:-1]),(phi[:,1:],phi[:,:-1]),(phi[:,:,1:],phi[:,:,:-1])):
        dot = np.sum(a*b,axis=-1)
        out.append(float(np.max(np.arccos(np.clip(dot,-1.0,1.0)))))
    return max(out)


def geometric_degree_single(phi: np.ndarray, target, candidate_radius: float = 1.15) -> int:
    q = np.asarray(target,dtype=float)
    q /= np.linalg.norm(q)
    dots = np.tensordot(phi,q,axes=([-1],[0]))
    candidate_nodes = np.argwhere(dots > math.cos(candidate_radius))
    n = phi.shape[0]
    cubes: set[tuple[int,int,int]] = set()
    for i,j,k in candidate_nodes:
        for di in (-1,0):
            for dj in (-1,0):
                for dk in (-1,0):
                    ci,cj,ck = int(i+di),int(j+dj),int(k+dk)
                    if 0 <= ci < n-1 and 0 <= cj < n-1 and 0 <= ck < n-1:
                        cubes.add((ci,cj,ck))

    rhs = np.array([0.0,0.0,0.0,0.0,1.0])
    degree = 0
    tol = 2.0e-9
    for cube in cubes:
        base = np.asarray(cube,dtype=int)
        for offsets in TETRA_OFFSETS:
            inds = base + offsets
            vs = np.array([phi[tuple(ind)] for ind in inds])
            M = np.zeros((5,5))
            M[:4,:4] = vs.T
            M[:4,4] = -q
            M[4,:4] = 1.0
            try:
                sol = np.linalg.solve(M,rhs)
            except np.linalg.LinAlgError:
                continue
            lam = sol[:4]
            scale = sol[4]
            if scale <= tol or np.min(lam) < -tol or np.max(lam) > 1.0+tol:
                continue
            A = np.stack([vs[1]-vs[0],vs[2]-vs[0],vs[3]-vs[0]],axis=1)
            det = float(np.linalg.det(np.column_stack([q,A])))
            if abs(det) > 1.0e-14:
                degree += 1 if det > 0 else -1
    return degree


def geometric_degrees(phi: np.ndarray) -> tuple[int,...]:
    out = []
    for target in GEOMETRIC_TARGETS:
        degree = geometric_degree_single(phi,target,1.15)
        if abs(degree) != B:
            degree = geometric_degree_single(phi,target,1.55)
        out.append(int(degree))
    return tuple(out)


def high_order_symbol_diagnostic():
    theta = np.linspace(1.0e-4,math.pi,50000)
    z = np.exp(1j*theta)
    symbol = (-25 + 48*z - 36*z**2 + 16*z**3 - 3*z**4)/12.0
    ratio = np.abs(symbol)/theta
    min_ratio = float(np.min(ratio))
    nyquist = float(abs((-25-48-36-16-3)/12.0))
    return min_ratio,nyquist,(min_ratio > 0.90 and nyquist > 8.0)


def parse_float(log_text: str, key: str) -> float:
    match = re.search(rf"^{re.escape(key)}=([^\r\n]+)$", log_text, re.MULTILINE)
    if match is None:
        raise RuntimeError(f"Missing {key} in 023CR log")
    return float(match.group(1).strip())


def observed_convergence(log_text: str):
    dx = np.array([parse_float(log_text,f"N{n}_DX") for n in (81,97,113)])
    e = np.array([parse_float(log_text,f"N{n}_ENERGY_RELERR") for n in (81,97,113)])
    t = np.array([parse_float(log_text,f"N{n}_TOPOLOGY4_RELERR") for n in (81,97,113)])
    pE = float(np.polyfit(np.log(dx),np.log(e),1)[0])
    pT = float(np.polyfit(np.log(dx),np.log(t),1)[0])
    return pE,pT,(1.6 <= pE <= 2.4 and 3.0 <= pT <= 5.0)


def audit(phi,dx,n,continuum):
    E,E2,E4,E0 = high_order_energy(phi,dx)
    CE,CE2,CE4,CE0 = continuum
    t4 = topology4(phi,dx)
    trel = abs(abs(t4)/B - 1.0)
    degrees = geometric_degrees(phi)
    angle = max_neighbor_angle(phi)
    passed = (
        relative_error(E,CE) <= MAX_TOTAL_ENERGY_RELERR
        and relative_error(E2,CE2) <= MAX_E2_RELERR
        and relative_error(E4,CE4) <= MAX_E4_RELERR
        and relative_error(E0,CE0) <= MAX_E0_RELERR
        and trel <= MAX_TOPOLOGY4_RELERR
        and all(abs(d)==B for d in degrees)
        and len(set(np.sign(d) for d in degrees)) == 1
        and angle <= MAX_NEIGHBOR_ANGLE
    )
    return Audit(n,dx,E,E2,E4,E0,
                 relative_error(E,CE),relative_error(E2,CE2),
                 relative_error(E4,CE4),relative_error(E0,CE0),
                 t4,trel,degrees,angle,passed)


def print_audit(a: Audit):
    p=f"N{a.n}"
    print(f"{p}_DX={a.dx:.15e}")
    print(f"{p}_HIGH_ORDER_ENERGY={a.energy:.15e}")
    print(f"{p}_HIGH_ORDER_E2={a.e2:.15e}")
    print(f"{p}_HIGH_ORDER_E4={a.e4:.15e}")
    print(f"{p}_HIGH_ORDER_E0={a.e0:.15e}")
    print(f"{p}_ENERGY_RELERR={a.energy_relerr:.15e}")
    print(f"{p}_E2_RELERR={a.e2_relerr:.15e}")
    print(f"{p}_E4_RELERR={a.e4_relerr:.15e}")
    print(f"{p}_E0_RELERR={a.e0_relerr:.15e}")
    print(f"{p}_TOPOLOGY4={a.topology4:.15e}")
    print(f"{p}_TOPOLOGY4_RELERR={a.topology4_relerr:.15e}")
    print(f"{p}_GEOMETRIC_DEGREES="+",".join(str(x) for x in a.geometric_degrees))
    print(f"{p}_MAX_NEIGHBOR_ANGLE={a.max_neighbor_angle:.15e}")
    print(f"{p}_INITIAL_HIGH_ORDER_RECONSTRUCTION="+("PASS" if a.passed else "FAIL"))


def main():
    print("=== 023CR2 — HIGH-ORDER GEOMETRIC-TOPOLOGY PREFLIGHT ===")

    print("\n=== A — UPSTREAM 023CR AUDIT ===")
    for p in (A23_SOURCE,B23_SOURCE,C23_SOURCE,CR23_SOURCE,CR23_LOG):
        require_file(p)
    hashes = {
        "023A":sha256(A23_SOURCE),
        "023B":sha256(B23_SOURCE),
        "023C":sha256(C23_SOURCE),
        "023CR":sha256(CR23_SOURCE),
    }
    expected = {
        "023A":EXPECTED_023A_SHA256,
        "023B":EXPECTED_023B_SHA256,
        "023C":EXPECTED_023C_SHA256,
        "023CR":EXPECTED_023CR_SHA256,
    }
    for k,v in hashes.items():
        print(f"{k}_SOURCE_SHA256={v}")
    log_text = CR23_LOG.read_text(errors="replace")
    markers = (
        "CHECKERBOARD_NULL_MODE_DIAGNOSIS=PASS",
        "N113_TOPOLOGY_CENTRAL4=6.995398007429317e+00",
        "023CR_CHECKERBOARD_FREE_LINK_LATTICE_TOPOLOGY_REPAIR=INCOMPLETE_NUMERICAL_GATE",
    )
    audit_ok = all(hashes[k]==expected[k] for k in expected) and all(x in log_text for x in markers)
    print("UPSTREAM_023CR_AUDIT="+("PASS" if audit_ok else "FAIL"))
    if not audit_ok:
        raise RuntimeError("023CR audit failed")

    print("\n=== B — OBSERVED 023CR CONVERGENCE ===")
    pE,pT,conv_ok = observed_convergence(log_text)
    print(f"OBSERVED_LINK_ENERGY_CONVERGENCE_ORDER={pE:.15e}")
    print(f"OBSERVED_TOPOLOGY4_CONVERGENCE_ORDER={pT:.15e}")
    print("OBSERVED_LINK_ACTION_CONVERGENCE="+("PASS" if conv_ok else "FAIL"))

    print("\n=== C — HIGH-ORDER SYMBOL AUDIT ===")
    min_ratio,nyquist,symbol_ok = high_order_symbol_diagnostic()
    print(f"HIGH_ORDER_SYMBOL_MIN_ABS_OVER_THETA={min_ratio:.15e}")
    print(f"HIGH_ORDER_NYQUIST_SYMBOL_ABS={nyquist:.15e}")
    print("HIGH_ORDER_SYMBOL_NO_SPURIOUS_UNIT_CIRCLE_ZERO="+("PASS" if symbol_ok else "FAIL"))

    a23 = load_module("a23_for_023cr2",A23_SOURCE)
    b23 = load_module("b23_for_023cr2",B23_SOURCE)
    c23 = load_module("c23_for_023cr2",C23_SOURCE)
    cr23 = load_module("cr23_for_023cr2",CR23_SOURCE)

    print("\n=== D — CONTINUUM B7 RECONSTRUCTION ===")
    degree,I_direct = b23.angular_integrals_b7(b23.B7_B0)
    profile = b23.solve_profile_with_custom_I(a23,B,ETA,MASS,I_direct)
    sector_profiles,sector_energies = b23.solve_exact_sector(a23,ETA,MASS)
    selected = b23.candidate_from_sector(a23,sector_profiles,sector_energies,B)
    continuum = (
        4*math.pi*float(profile.E),
        4*math.pi*float(profile.E2),
        4*math.pi*float(profile.E4),
        4*math.pi*float(profile.E0),
    )
    half_domain,r_tail,boundary_F = cr23.choose_compact_half_domain(
        profile,selected.payload.payload_center,selected.payload.payload_radius
    )
    print(f"DIRECT_MAP_DEGREE={degree:.15e}")
    print(f"DIRECT_MAP_I={I_direct:.15e}")
    print(f"CONTINUUM_ENERGY={continuum[0]:.15e}")
    print(f"CONTINUUM_E2={continuum[1]:.15e}")
    print(f"CONTINUUM_E4={continuum[2]:.15e}")
    print(f"CONTINUUM_E0={continuum[3]:.15e}")
    print(f"HALF_DOMAIN={half_domain:.15e}")
    print(f"R_TAIL={r_tail:.15e}")
    print(f"PROFILE_F_AT_FACE={boundary_F:.15e}")

    print("\n=== E — HIGH-ORDER + GEOMETRIC-DEGREE RESOLUTION SCAN ===")
    audits=[]
    selected_pair=None
    for n in GRID_LEVELS:
        phi,axis,dx = c23.sample_rational_map_field(profile,b23.B7_B0,n,half_domain)
        a = audit(phi,dx,n,continuum)
        audits.append(a)
        print_audit(a)
        if len(audits)>=2:
            lo,hi=audits[-2],audits[-1]
            dE=relative_error(lo.energy,hi.energy)
            dE4=relative_error(lo.e4,hi.e4)
            dT=abs(abs(lo.topology4)-abs(hi.topology4))/B
            pair_ok=(lo.passed and hi.passed and dE<=MAX_PAIR_ENERGY_RELCHANGE
                     and dE4<=MAX_PAIR_E4_RELCHANGE and dT<=MAX_PAIR_TOPOLOGY_ABSCHANGE)
            print(f"PAIR_N{lo.n}_N{hi.n}_ENERGY_RELCHANGE={dE:.15e}")
            print(f"PAIR_N{lo.n}_N{hi.n}_E4_RELCHANGE={dE4:.15e}")
            print(f"PAIR_N{lo.n}_N{hi.n}_TOPOLOGY_ABSCHANGE={dT:.15e}")
            print(f"PAIR_N{lo.n}_N{hi.n}_CONVERGENCE="+("PASS" if pair_ok else "FAIL"))
            if pair_ok:
                selected_pair=(lo,hi)
                break

    pair_found=selected_pair is not None
    energy_ok=pair_found and selected_pair[0].passed and selected_pair[1].passed
    topology_ok=pair_found and all(x.topology4_relerr<=MAX_TOPOLOGY4_RELERR for x in selected_pair)
    geometric_ok=pair_found and all(all(abs(d)==B for d in x.geometric_degrees) for x in selected_pair)

    print("\n=== F — 023CR2 DECISION ===")
    if pair_found:
        lo,hi=selected_pair
        print(f"INITIAL_HIGH_ORDER_RESOLUTION_PAIR=N{lo.n}_N{hi.n}")
    else:
        print("INITIAL_HIGH_ORDER_RESOLUTION_PAIR=NOT_FOUND")
    print("INITIAL_HIGH_ORDER_ENERGY_RECONSTRUCTION="+("PASS" if energy_ok else "FAIL_OR_UNRESOLVED"))
    print("INITIAL_DERIVATIVE_TOPOLOGY_RECONSTRUCTION="+("PASS" if topology_ok else "FAIL_OR_UNRESOLVED"))
    print("INITIAL_GEOMETRIC_B7_DEGREE="+("PASS" if geometric_ok else "FAIL_OR_UNRESOLVED"))

    green=audit_ok and conv_ok and symbol_ok and pair_found and energy_ok and topology_ok and geometric_ok
    if green:
        print("023CR2_HIGH_ORDER_GEOMETRIC_TOPOLOGY_PREFLIGHT=GREEN_NUMERICAL_REPRESENTATION_REPAIR")
        print("CARTESIAN_B7_REPRESENTATION=PROMOTION_GRADE_FOR_RELAXATION")
        print("HEURISTIC_PROMOTION_FROM_023CR2=NO_NUMERICAL_REPAIR_ONLY")
        print("CURRENT_KNOWLEDGE_HEURISTIC=APPROXIMATELY_70_TO_71_PERCENT_FROM_023BR")
        print("NEXT=023CR3_GEOMETRIC_DEGREE_GUARDED_UNRESTRICTED_RELAXATION")
    else:
        print("023CR2_HIGH_ORDER_GEOMETRIC_TOPOLOGY_PREFLIGHT=INCOMPLETE_NUMERICAL_GATE")
        print("CARTESIAN_B7_REPRESENTATION=NOT_YET_PROMOTED")
        print("HEURISTIC_PROMOTION_FROM_023CR2=NO")
        print("CURRENT_KNOWLEDGE_HEURISTIC=APPROXIMATELY_70_TO_71_PERCENT_FROM_023BR")
        print("NEXT=ADAPTIVE_OR_SPECTRAL_CARTESIAN_REPRESENTATION")
    print("UNRESTRICTED_CARTESIAN_3D_STABILITY=NOT_YET_RESOLVED")
    print("NONLINEAR_EINSTEIN_SKYRME=NOT_ESTABLISHED")
    print("PRACTICAL_ANTIGRAVITY_DEVICE=NO")
    print("NEW_PHYSICS_DISCOVERY=NO")
    print("CLAIM_CLASSIFICATION=PROJECT_DERIVED_023CR2_HIGH_ORDER_GEOMETRIC_TOPOLOGY_PREFLIGHT")


if __name__=="__main__":
    main()
