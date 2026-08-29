# Antigravity Research — Research Buildplan

This document is the active scientific execution plan for **Antigravity Research**.

Its purpose is to keep the project focused on the analytical derivations, simulations, falsification tests, literature checks, and independent verification steps that provide the greatest increase in scientific knowledge per unit research time.

This is a living document.

Update it when:

* a major simulation or analytical gate is completed;
* a major candidate branch is falsified;
* a new physical constraint changes priorities;
* a substantially better mechanism is identified;
* the active scientific frontier changes;
* a previously speculative mechanism becomes sufficiently concrete to require a stronger verification standard.

Do not rewrite this document after every minor implementation change.

Chronological detail belongs in `NOTES.md`.

This file should remain focused on:

```text
CURRENT_FRONTIER
ACTIVE_SCIENTIFIC_QUESTION
ACTIVE_TASK
DECISION_GATES
PRIORITIES
STOP_RULES
CLAIM_PROMOTION_REQUIREMENTS
NEXT
```

---

# 1. Purpose

The central project question is:

> **What physically consistent mechanism offers the most plausible path toward controllable, measurable local gravitational repulsion or an operationally equivalent antigravity-like force on neutral matter?**

The project is not merely attempting to find equations containing a repulsive sign.

The research program should progressively narrow the space of possibilities toward mechanisms that survive increasingly demanding physical requirements.

A candidate is scientifically stronger when it moves from:

```text
MATHEMATICAL_SIGN
```

toward:

```text
OPERATIONAL_REPULSION
THEORETICAL_CONSISTENCY
FINITE_LOCALIZATION
CONSERVATION
STABILITY
MICROPHYSICAL_REALIZATION
EMPIRICAL_VIABILITY
MATERIAL_REALIZATION
EXPERIMENTAL_ACCESSIBILITY
PRACTICAL_CONTROL
```

These levels must never be conflated.

---

# 2. Two Distinct Mechanism Classes

The project now contains two fundamentally different kinds of antigravity-like mechanisms.

## 2.1 Metric/gravitational mechanisms

These produce repulsion through spacetime geometry or stress-energy in a gravitational theory.

Examples include:

* Kottler / Schwarzschild-de Sitter;
* Reissner-Nordström gravitational repulsion;
* relativistic pressure/tension;
* the project-derived 006D linearized-GR source;
* quantum stress-energy;
* modified-gravity mechanisms.

For these mechanisms, the relevant observable should ultimately be metric or curvature based.

Examples include:

* relative free-fall acceleration;
* geodesic deviation;
* proper acceleration;
* invariant curvature effects.

## 2.2 Additional-force mechanisms

These produce an antigravity-like acceleration through a force beyond ordinary GR.

The current 010E scalar branch belongs to this category.

It is not correct to call such a mechanism ordinary general-relativistic antigravity.

The appropriate description is:

> **A hypothetical ground-referenced repulsive fifth force on neutral matter capable of producing antigravity-like acceleration.**

Momentum conservation must remain explicit.

The Earth or other source mass is the external momentum reservoir.

This is not reactionless propulsion.

---

# 3. Operational Definition of the Target

A useful candidate must produce a measurable outward acceleration of neutral matter relative to an external gravitational source or reference mass.

Coordinate acceleration by itself is insufficient.

The target should be represented by a measurable quantity such as:

```math
a_{\mathrm{out}}
```

with a clearly defined sign convention.

For the principal benchmark used in the late 010E work:

```math
a_{\mathrm{target}}
\sim
g
```

with:

```math
g
=
9.80665\ {\rm m\,s^{-2}}
```

The project should not assume that a mechanism must produce an outward asymptotic field.

A finite positive-total-mass GR source may have:

```math
\text{repulsive near field}
```

while retaining:

```math
\text{attractive far field}
```

That remains acceptable.

---

# 4. Unified Success Ladder

All candidate mechanisms should be classified using the following ladder.

## Level 0 — Mathematical sign

A formula contains a repulsive contribution.

No physical claim follows yet.

## Level 1 — Operational repulsion

A measurable or invariant physical quantity points outward or produces reduced attraction.

For GR mechanisms this may involve:

* geodesic deviation;
* relative free fall;
* proper acceleration;
* curvature.

For fifth-force mechanisms this may involve:

* force on neutral matter;
* relative acceleration;
* composition-dependent acceleration;
* source-referenced acceleration.

## Level 2 — Governing-theory consistency

The result satisfies the equations of the theory being claimed.

Examples:

* Einstein equations;
* Einstein-Maxwell equations;
* a specified scalar EFT;
* a specified relativistic QFT.

## Level 3 — Source / charge consistency

The complete source is characterized.

For gravitational branches this includes:

* energy density;
* pressure;
* tension;
* stress-energy type;
* energy conditions.

For fifth-force branches this includes:

* source charge;
* test-body charge;
* mediator properties;
* microscopic operators;
* charge signs;
* conservation laws.

## Level 4 — Finite localization

The effect arises from a finite source or finite physical body rather than an infinite idealization.

## Level 5 — Conservation

The complete system satisfies the relevant conservation equations.

For stress-energy:

```math
\nabla_\mu T^{\mu\nu}=0
```

For force models:

* energy conservation;
* momentum conservation;
* charge conservation;
* consistent source/test backreaction.

## Level 6 — Stability and naturalness

The mechanism survives the relevant:

* mechanical stability;
* dynamical stability;
* field stability;
* finite-size instability;
* discharge;
* collapse;
* radiative stability;
* ultralight-mass naturalness;
* thermal stability;
* quantum instability.

## Level 7 — Microscopic physical realization

A known or theoretically controlled microscopic field/material mechanism generates the required source or charge.

A phenomenological EFT coefficient alone is not sufficient.

## Level 8 — Empirical viability

The complete mechanism survives relevant existing constraints.

Examples:

* inverse-square-law tests;
* equivalence-principle tests;
* atomic spectroscopy;
* electron magnetic moment;
* stellar cooling;
* supernova constraints;
* cosmology;
* gravitational-wave bounds.

## Level 9 — Material/control realization

A real or convincingly modeled material/system can enter and leave the required state with plausible control requirements.

## Level 10 — Experimental accessibility

A measurable experiment can be defined with realistic sensitivity and systematic control.

## Level 11 — Practical antigravity

A controllable apparatus produces useful macroscopic repulsion.

The project is not currently at Level 11.

---

# 5. Scientific Priority Rule

When selecting the next research task, prioritize the calculation that maximizes:

```text
INFORMATION_GAIN
+
FALSIFICATION_POWER
+
INDEPENDENT_VERIFICATION_VALUE
+
ABILITY_TO_CLOSE_AN_ENTIRE_BRANCH
```

Prefer a task that could prove the current leading mechanism impossible over a task that merely improves one of its parameters by a small amount.

Specifically, prioritize tasks that:

1. falsify an important candidate;
2. close a fundamental uncertainty;
3. independently reconstruct a central result;
4. establish a theorem or strong bound;
5. expose an unavoidable conflict with experiment;
6. identify a genuine symmetry or conservation mechanism;
7. reduce required energy or stress by orders of magnitude;
8. convert a phenomenological coefficient into a microscopic derivation;
9. determine whether an entire branch should continue.

Avoid increasing model complexity before the simpler model's failure mode has been understood.

---

# 6. Evidence Hierarchy

Evidence should generally be weighted in the following order.

## Strongest

* exact analytical theorem;
* exact known GR/QFT solution;
* independent analytical derivations agreeing;
* independent numerical implementations agreeing;
* microscopic matching calculation;
* comparison with peer-reviewed experimental data;
* experimentally established effect.

## Strong

* converged numerical solution;
* explicit conservation proof;
* multiple independent checks;
* dimensional and limiting-case verification;
* Feynman-Hellmann reconstruction;
* independent EFT representation;
* numerical optimization with independent reconstruction.

## Intermediate

* one self-consistent EFT model;
* one internally tested numerical model;
* linearized approximation;
* idealized thin-wall or finite-size model;
* phenomenological coupling satisfying known preflight constraints.

## Weak

* analogy;
* one unverified numerical result;
* coordinate acceleration;
* arbitrary state-dependent coupling;
* parameter coincidence;
* unexplained symmetry;
* speculative material label;
* tunable coefficient without microscopic origin.

Research priority should be especially high when a promising intermediate result can cheaply be either promoted or destroyed.

---

# 7. Regression Integrity Gate

Before extending any major scientific branch:

```text
GOAL:
Verify the complete known-solution regression suite.

CURRENT_EXPECTED_BASELINE:
94 PASSED

FAIL:
Investigate the regression before generating new scientific claims.
```

Recommended first commands:

```bash
git status --short

ROOT="$(pwd)"
PY="$ROOT/.venv/bin/python"

PYTHONPATH="$ROOT/src" \
"$PY" -m pytest -q tests/known_solutions
```

The late 010E-Y run ended with:

```text
94 passed
```

This is the current expected baseline unless permanent tests are deliberately added.

---

# 8. Strongest Established Project Result — 006D

The strongest established project-derived result remains the finite linearized-GR construction completed in 006D.

The source is:

```text
FINITE_RADIUS=YES
FINITE_THICKNESS=YES
NONSINGULAR=YES
POSITIVE_ENERGY=YES
LOCAL_CONSERVATION_LINEARIZED_ORDER=YES
NEC=PASS
WEC=PASS
DEC=PASS
LOCAL_OUTWARD_FIELD=YES
POSITIVE_FAR_FIELD_ACTIVE_MASS=YES
```

The best tested finite-thickness coefficient is:

```math
C_{\mathrm{finite}}
=
23.591586299249
```

in:

```math
M_{\mathrm{equiv}}
=
C\frac{ah^2}{G}
```

The thin conserved architecture gives:

```math
C_{\mathrm{thin}}
=
23.426710175391
```

The finite realization is therefore only about:

```math
0.704\%
```

above the thin result.

The central headline remains:

> **We have a mathematical construction for antigravity-like gravitational repulsion.**

Correct limitations:

```text
EXACT_NONLINEAR_GR_REALIZATION=NOT_ESTABLISHED
DYNAMIC_STABILITY=NOT_ESTABLISHED
KNOWN_MATERIAL_REALIZATION=NO
ENERGETIC_PRACTICALITY=NO
PRACTICAL_ANTIGRAVITY_DEVICE=NO
NEW_PHYSICS_DISCOVERY=NO
```

---

# 9. Classical-GR Branch Status

The original buildplan treated 006B, 006C, and 006D as future work.

That phase is complete at the stated linearized-model level.

The remaining major classical obstacle is the scaling:

```math
M
\sim
C\frac{ah^2}{G}
```

A general static one-sided conserved-DEC argument produced the optimistic scaling bound:

```math
M
\ge
\frac{ah^2}{G}
```

For:

```math
a=g
```

and:

```math
h=1\ {\rm m}
```

this already implies:

```math
M_{\min}
\approx
1.47\times10^{11}\ {\rm kg}
```

The explicit 006D coefficient raises this to approximately:

```math
3.47\times10^{12}\ {\rm kg}
```

for the same benchmark.

Therefore:

```text
CLASSICAL_STATIC_GR_SIGN_PROBLEM=SOLVED_IN_MODEL
CLASSICAL_STATIC_GR_ENERGY_SCALE=SEVERE
CLASSICAL_STATIC_COEFFICIENT_OPTIMIZATION=DEPRIORITIZED
```

Do not return to small improvements in $C$ unless a new theorem or physical matter realization changes the scaling itself.

---

# 10. Quantum Stress-Energy Branch Status

Casimir / quantum-negative-energy mechanisms have already been subjected to:

* complete-apparatus reasoning;
* quantum-energy-inequality preflights;
* macroscopic scaling analysis.

The project found no practical macroscopic escape in the tested established-QFT route.

Therefore:

```text
FREE_FIELD_QUANTUM_NEGATIVE_ENERGY=
REFERENCE_AND_CONSTRAINT_BRANCH

PRACTICAL_MACROSCOPIC_ESCAPE=
NOT_FOUND
```

Do not restart generic Casimir optimization unless a genuinely new quantum state or theorem changes the relevant scaling.

---

# 11. Fifth-Force Program Status

After the classical and quantum routes remained impractical, the project investigated source-referenced additional-force mechanisms.

Important previous outcomes include:

```text
ORDINARY_UNSCREENED_VECTOR=
CONSTRAINT_LIMITED

SIMPLE_GOLD_NULL_ELECTROWEAK_VECTOR=
REJECTED_AT_PREFLIGHT_LEVEL

HEALTHY_UNIVERSAL_SCALAR_TENSOR=
ATTRACTIVE_OR_SCREENED_TOWARD_GR

REACTIONLESS_INTERNAL_SELF_THRUST=
REJECTED_BY_CENTER_OF_ENERGY_CONSERVATION
```

The leading surviving fifth-force direction became a material-state-dependent opposite-sign scalar response.

The current branch is not ordinary GR.

It is:

> **A hypothetical ultralight scalar fifth force whose effective charge becomes large and opposite in sign to the terrestrial source only in a protected material bound state.**

---

# 12. Current Scalar Working Benchmark

The current phenomenological benchmark uses:

```math
\lambda
=
5000\ {\rm m}
```

and:

```math
\alpha_Y
=
2.0\times10^{-4}
```

The corresponding mediator mass is:

```math
m_\phi
=
\frac{\hbar c}{\lambda}
```

giving:

```math
m_\phi
=
3.946539608\times10^{-11}\ {\rm eV}
```

The working terrestrial source coupling is:

```math
\alpha_{\mathrm{source}}
=
\sqrt{
\frac{\alpha_Y}{2}
}
=
10^{-2}
```

The thick-source half-space benchmark requires approximately:

```math
\alpha_{\mathrm{activated}}
=
-1.558991777087370\times10^5
```

to generate an order-$1g$ upward force in the chosen geometry.

The required extra microscopic coupling per nucleon is approximately:

```math
g_N
=
6.011882433614129\times10^{-14}
```

The selected benchmark is a working phenomenological point.

It is not yet an experimentally confirmed allowed point.

---

# 13. Current Experimental-Bound Status

The project has used the historical intermediate-range Yukawa ceiling:

```math
\alpha_Y
\lesssim
2\times10^{-3}
```

as a conservative numerical anchor.

The working point:

```math
\alpha_Y
=
2\times10^{-4}
```

is a factor of ten below that historical ceiling.

However:

```text
CURRENT_EXACT_2026_5KM_YUKAWA_MARGIN=
NOT_NUMERICALLY_RECONSTRUCTED
```

The modern graphical boundary should not be replaced by an invented precise number.

This empirical uncertainty becomes decisive only if the microscopic theory survives the current UV gate.

---

# 14. Current Leading Low-Energy Material Architecture

The late 010E work systematically simplified the material branch.

The present leading low-energy chain is:

```text
EARTH / GROUND SOURCE
        |
        v
ULTRALIGHT SCALAR phi
        |
        v
MATERIAL-SPECIFIC TWO-BODY OPERATOR
        |
        v
FIXED BOUND DINUCLEAR IDENTITY
        |
        v
COOPERATIVE HIGH-SPIN INTERNAL STATE
        |
        v
SPIN-LATTICE RESPONSE
        |
        v
MACROSCOPIC PAYLOAD
```

The previous pre-existing compact hidden phase is no longer required in the minimal finite-payload low-energy architecture.

Therefore:

```text
PREEXISTING_COMPACT_HIDDEN_PHASE_REQUIRED=NO
PREEXISTING_10KEV_HIDDEN_CONDENSATE_REQUIRED=NO
HIDDEN_PHASE_COSMOLOGICAL_VACUUM_REQUIRED=NO
```

---

# 15. Current Selector Structure

The protected low-energy selector is factorized:

```math
Q_N
=
B_{\mathrm{material}}
\prod_{i=1}^N
P_{\mathrm{HS},i}
```

where:

* $B_{\mathrm{material}}$ identifies the fixed bound material species;
* $P_{\mathrm{HS},i}$ projects each site onto the relevant high-spin state.

This permits:

```math
[
B_{\mathrm{material}},
H_{\mathrm{control}}
]
=
0
```

while:

```math
[
Q_N,
H_{\mathrm{control}}
]
\ne
0
```

Thus exact material identity does not have to be the degree of freedom that is switched.

This resolves the apparent conflict between strong material selectivity and control.

---

# 16. Cooperative Cluster Window

Off-state leakage decreases rapidly with cooperative cluster size.

For an $N$-site all-high-spin state with scalar energy penalty $E_s$:

```math
W_N
=
5^N
\exp
\left(
-\frac{N E_s}{k_BT}
\right)
```

and:

```math
p_{\mathrm{all-HS}}
\lesssim
\frac{W_N}{1+W_N}
```

This creates a minimum cluster size from leakage.

However the maximum equilibrium scalar susceptibility scales as:

```math
|\Delta m_\phi^2|
\propto
N
\frac{
n_{\mathrm{site}}g_{\mathrm{site}}^2
}{
4k_BT
}
```

so finite-size scalar stability produces a maximum cluster size.

The condition:

```math
N_{\min}
\le
N
\le
N_{\max}
```

defines the selector window.

The selected one-ton benchmark produced a nonempty window.

At $300,{\rm K}$:

```text
N_MIN=11
N_MAX=21
```

At $77,{\rm K}$:

```text
N_MIN=2
N_MAX=5
```

The lowest-complexity survivor is therefore dinuclear.

---

# 17. Dinuclear Low-Energy Benchmark

For the selected $N=2$ architecture:

```text
DINUCLEAR_STABILITY_T_MIN_K=
28.13102372293623

DINUCLEAR_LEAKAGE_T_MAX_K=
101.8315502857560
```

At $77,{\rm K}$:

```text
DINUCLEAR_ALL_HS_LEAKAGE=
1.989338055378181e-9

DINUCLEAR_LEAKAGE_MARGIN=
290.1950942786034

DINUCLEAR_MU_R=
0.9556137730170507

DINUCLEAR_STABILITY_MARGIN=
1.643839124818559
```

The selected low-energy control scale is:

```text
CONTROL_SITE_EV=
0.07919352471801402

CONTROL_DIMER_EV=
0.1583870494360280

CONTROL_1000KG_FREE_ENERGY_SCALE_J=
1.063556252028522e8
```

These values are free-energy scales of the effective model.

They are not demonstrated device energy consumption.

---

# 18. Finite-Size Scalar Stability

The finite-size correction is central and must be retained.

For an interior effective scalar mass:

```math
m_{\mathrm{in}}^2
=
-\mu^2
```

inside a sphere of radius $R$, with ordinary exterior mass $m_\phi$, the first static zero mode satisfies:

```math
\mu\cot(\mu R)
=
-m_\phi
```

Define:

```math
x
=
\mu R
```

Then:

```math
x\cot x
=
-m_\phi R
```

For the one-ton benchmark:

```text
FINITE_SPHERE_X_CRITICAL=
1.570875308300910
```

A finite body is not automatically unstable merely because the local infinite-medium value of $m_{\mathrm{eff}}^2$ becomes negative.

This correction invalidated several overly strong infinite-medium stability arguments.

Every future material-susceptibility calculation must distinguish:

```text
LOCAL_NEGATIVE_MASS2
```

from:

```text
ACTUAL_FINITE_BODY_ZERO_MODE_INSTABILITY
```

---

# 19. Local Composite Matching Result — 010E-Y

The strongest current speculative result is the local nonrelativistic composite construction.

Introduce constituent fields:

```text
A
B
```

and an emergent bound-state field:

```text
D
```

with number assignments:

```math
N_A=1
```

```math
N_B=1
```

```math
N_D=2
```

and:

```math
N
=
N_A+N_B+2N_D
```

The conversion interaction is:

```math
H_{\mathrm{mix}}
=
h
\left(
D^\dagger AB
+
A^\dagger B^\dagger D
\right)
```

The scalar couples only to the bound-state field:

```math
H_\phi
=
g_D\phi D^\dagger D
```

The model obeys:

```math
[H,N]=0
```

Therefore the isolated one-particle sectors cannot access the $D$ state.

The explicit result is:

```text
ISOLATED_A_EXTRA_SCALAR_CHARGE=0
ISOLATED_B_EXTRA_SCALAR_CHARGE=0
BOUND_DIMER_EXTRA_SCALAR_CHARGE=NONZERO
```

This demonstrates that locality and Feynman-Hellmann do not alone force a low-energy composite scalar charge onto isolated constituents.

The statement applies only to the strict NR composite EFT.

---

# 20. Feynman-Hellmann Check

The two-state Hamiltonian is:

```math
H_2(\phi)
=
\begin{pmatrix}
0 & h \\
h & \Delta_D + g_D\phi
\end{pmatrix}
```

For a dressed bound state:

```math
\frac{dE_{\mathrm{bound}}}{d\phi}
=
g_D Z_D
```

The selected Y benchmark gives:

```text
TARGET_DINUCLEAR_COUPLING=
8.638353631211470e-12

BARE_DIMER_SCALAR_COUPLING=
8.904546001587151e-12

DIMER_FRACTION_EARTH_PHI=
0.9701060143517443
```

The Feynman-Hellmann derivative and independent finite difference agree to relative error:

```text
3.079119804066939e-10
```

Therefore:

```text
FEYNMAN_HELLMANN=PASS
```

within the low-energy model.

---

# 21. Independent Two-Body Contact Representation

The same bound-state response can be represented as:

```math
\mathcal H_{\phi,2}
=
C_\phi
\phi
A^\dagger B^\dagger BA
```

This operator vanishes exactly in the isolated one-body sectors.

For a representative pair radius:

```math
a
=
3\ {\rm \AA}
```

the required coefficient is:

```math
C_\phi
=
9.536416387852626\times10^{-20}\ {\rm eV^{-3}}
```

The corresponding atomic EFT cutoff is:

```math
\Lambda_{\mathrm{EFT}}
\sim
\frac{\hbar c}{a}
=
657.7566013333334\ {\rm eV}
```

and:

```math
C_\phi
\Lambda_{\mathrm{EFT}}^3
=
2.713818830692468\times10^{-11}
```

Thus the required pair operator is perturbatively small at the atomic EFT cutoff.

This provides an independent low-energy representation of the dimer result.

---

# 22. Current Dominant Theoretical Obstruction

The low-energy EFT survives.

The ultraviolet problem does not.

Treating the approximately $134,{\rm GeV}$ dimer as a fundamental relativistic particle gives scalar-mass corrections of order:

```text
RELATIVISTIC_FERMION_DIMER_LOOP_TO_TARGET_MASS2=
1.155053548350539e19

RELATIVISTIC_SCALAR_DIMER_LOOP_TO_TARGET_MASS2=
2.310107096701078e19
```

Therefore:

```text
FUNDAMENTAL_RELATIVISTIC_DIMER=REJECTED
```

Generic relativistic one-loop operator mixing is:

```math
\frac{1}{16\pi^2}
=
6.332573977646111\times10^{-3}
```

while the conservative allowed target-equivalent leakage is:

```math
f_{\mathrm{leak}}
=
5.772961445324848\times10^{-7}
```

Thus generic one-loop mixing is larger by:

```math
\frac{
6.3326\times10^{-3}
}{
5.77296\times10^{-7}
}
\approx
1.10\times10^4
```

Therefore:

```text
GENERIC_UNPROTECTED_RELATIVISTIC_UV_MATCH=REJECTED
```

A real microscopic completion requires a non-generic protection mechanism.

---

# 23. Current Scientific Frontier

The single active scientific question is now:

> **Can a local relativistic microscopic theory matched to Standard Model constituents and a technically natural ultralight scalar generate the required protected two-body material Wilson coefficient while keeping all induced one-body ordinary-matter scalar charge below the leakage limit and preserving the ultralight mediator mass?**

This is the decisive bridge between:

```text
LOW_ENERGY_COMPOSITE_EFT
```

and:

```text
PHYSICAL_REALIZABILITY
```

The current branch should receive no additional phenomenological material fields, selector functions, hidden condensates, or optimization layers until this question is answered.

---

# 24. Active Phase

```text
ACTIVE_PHASE=
010E_Z_PROTECTED_RELATIVISTIC_TWO_BODY_MATCH_OR_NO_GO
```

The exact label may be changed when a permanent implementation is created.

The scientific content is more important than the numbering.

Active objective:

```text
DERIVE_OR_RULE_OUT_A_PROTECTED_RELATIVISTIC_ORIGIN_FOR_C_PHI
```

Required low-energy target:

```math
\mathcal H_{\phi,2}
=
C_\phi
\phi
A^\dagger B^\dagger BA
```

with representative:

```math
C_\phi
\approx
9.54\times10^{-20}\ {\rm eV^{-3}}
```

while maintaining ordinary one-body leakage below:

```math
f_{\mathrm{leak}}
\approx
5.77\times10^{-7}
```

of the activated target-equivalent response.

---

# 25. Active Gate A — Symmetry and Operator-Basis No-Go

This is the highest-value immediate calculation.

## Scientific question

Does any local relativistic symmetry structure allow the required composite/two-body scalar operator while forbidding or parametrically suppressing all dangerous one-body operators?

## First action

Construct the smallest complete operator basis rather than proposing one desired interaction in isolation.

For a candidate microscopic theory:

```math
\mathcal L
=
\mathcal L_{\mathrm{SM}}
+
\mathcal L_\phi
+
\sum_i
c_i\mathcal O_i
```

classify all operators capable of producing:

```math
\phi
A^\dagger B^\dagger BA
```

after NR matching.

For each proposed symmetry, explicitly determine whether it also permits lower-dimension terms such as:

```math
\phi\bar\psi\psi
```

or effective one-body operators after:

* electroweak symmetry breaking;
* confinement;
* atomic matching;
* integrating out heavy mediators.

## Required checks

```text
LORENTZ_INVARIANCE
SM_GAUGE_INVARIANCE
LOCALITY
EXACT_OR_TECHNICALLY_NATURAL_SYMMETRY
OPERATOR_DIMENSIONS
TREE_LEVEL_ONE_BODY_TERMS
LOOP_GENERATED_ONE_BODY_TERMS
RENORMALIZATION_GROUP_MIXING
WARD_IDENTITIES_IF_APPLICABLE
BOUND_STATE_MATCHING
```

## Pass condition

A well-defined symmetry or structural theorem forbids the dangerous one-body operators to sufficiently high order while allowing the required pair operator.

## Fail condition

The same symmetry that permits the pair response also allows a one-body scalar coupling at an experimentally fatal level.

If so:

```text
CLOSE_CURRENT_DIRECT_MATERIAL_BRANCH
```

unless a fundamentally different exact symmetry is identified immediately.

---

# 26. Active Gate B — Operator-Mixing Calculation

A tree-level zero is not sufficient.

For every candidate operator basis, calculate RG/operator mixing into one-body scalar operators.

The generic loop scale:

```math
\frac{1}{16\pi^2}
\approx
6.33\times10^{-3}
```

is already approximately:

```math
1.10\times10^4
```

times larger than the conservative leakage allowance.

Therefore the mechanism requires at least roughly four additional orders of magnitude of protection beyond a generic one-loop factor.

The central output should be:

```text
INDUCED_ONE_BODY_CHARGE / TARGET_DIMER_CHARGE
```

for:

* electrons;
* nucleons;
* quarks/gluons;
* electromagnetic binding;
* generic atoms;
* generic molecules.

Required:

```math
\frac{
g_{\mathrm{ordinary}}
}{
g_{\mathrm{target}}
}
<
f_{\mathrm{leak}}
```

with:

```math
f_{\mathrm{leak}}
=
5.772961445324848\times10^{-7}
```

under the present conservative benchmark.

---

# 27. Active Gate C — Ultralight Scalar Naturalness

The selected force range requires:

```math
m_\phi
=
3.946539608\times10^{-11}\ {\rm eV}
```

so:

```math
m_\phi^2
\approx
1.56\times10^{-21}\ {\rm eV^2}
```

For every candidate microscopic completion calculate threshold and loop corrections:

```math
\delta m_\phi^2
```

The default naturalness requirement, absent a demonstrated protective symmetry, is:

```math
|\delta m_\phi^2|
\lesssim
m_\phi^2
```

Do not accept:

```text
BARE_MASS_RETUNED_AGAINST_LARGE_LOOP
```

as a physical solution.

Possible protection mechanisms may be investigated only if they are explicit and technically controlled.

Examples of concepts worth testing include:

* exact shift symmetry;
* pseudo-Nambu-Goldstone structure;
* conserved currents;
* spurion suppression;
* collective symmetry breaking;
* nonrenormalization structures.

These are candidate tools, not assumed solutions.

---

# 28. Active Gate D — Independent Microscopic Matching

If a candidate survives A-C, derive the low-energy coefficient independently by at least two methods.

Preferred combinations include:

```text
RELATIVISTIC_SCATTERING_AMPLITUDE_MATCH
+
BOUND_STATE_FEYNMAN_HELLMANN
```

or:

```text
INTEGRATE_OUT_HEAVY_FIELD
+
SCHRIEFFER_WOLFF / SECOND_ORDER_REDUCTION
```

or:

```text
AUXILIARY_DIMER_MATCH
+
DIRECT_TWO_BODY_CONTACT_MATCH
```

The derivations must agree on:

* dimensions;
* sign;
* UV-scale dependence;
* wavefunction-overlap dependence;
* zero-binding limit;
* zero-mixing limit;
* decoupling limit.

A self-test that evaluates the same formula twice does not count.

---

# 29. Active Gate E — Exact Experimental Boundary

Only after a microscopic theory survives the previous gates should the project spend substantial time closing the exact current $5,{\rm km}$ bound.

Working point:

```text
lambda=5000 m
alpha_Y=2.0e-4
```

Required work:

1. obtain numerical exclusion data if available;
2. otherwise independently digitize the modern exclusion curve;
3. retain graphical/digitization uncertainty;
4. determine the actual modern margin;
5. compare against composition-dependent constraints produced by the microscopic theory.

Required output:

```text
WORKING_POINT_ALLOWED=YES/NO
NUMERICAL_MARGIN=<value>
UNCERTAINTY=<value>
```

If excluded:

```text
BRANCH_STOP
```

unless a physically justified change of the benchmark leaves useful acceleration.

Do not optimize around an excluded point using arbitrary retuning.

---

# 30. Active Gate F — Stellar and Cosmological Completion

Only after the actual microscopic portal is specified should the project perform full stellar and cosmological analysis.

Required topics may include:

* stellar production;
* red-giant cooling;
* horizontal-branch stars;
* supernova production/trapping;
* early-Universe thermalization;
* BBN;
* CMB;
* dark radiation;
* scalar background evolution;
* induced matter couplings.

Do not infer stellar or cosmological safety from the NR dimer EFT alone.

The high-energy operator determines these constraints.

---

# 31. Current Branch Stop Rules

Immediately close or strongly demote the protected material-scalar branch if any of the following is established:

```text
ONE_BODY_OPERATOR_INDUCED_ABOVE_LEAKAGE_LIMIT
```

```text
REQUIRED_PROTECTION_IS_FINE_TUNED_CANCELLATION
```

```text
ULTRALIGHT_SCALAR_MASS_DESTABILIZED_WITHOUT_TECHNICAL_PROTECTION
```

```text
RELATIVISTIC_LOCALITY_OR_GAUGE_INVARIANCE_FORBIDS_REQUIRED_MATCH
```

```text
BOUND_STATE_SPECIFIC_RESPONSE_REQUIRES_FORBIDDEN_CONSTITUENT_CHARGE
```

```text
CURRENT_EXACT_FIFTH_FORCE_BOUND_EXCLUDES_USEFUL_PARAMETER_REGION
```

```text
STELLAR_OR_COSMOLOGICAL_CONSTRAINTS_ELIMINATE_USEFUL_PARAMETER_REGION
```

```text
MICROSCOPIC_MATCH_REQUIRES_NONPERTURBATIVE_OR_UNCONTROLLED_COUPLING
```

When a stop rule fires:

1. record the negative result in `NOTES.md`;
2. preserve any useful theorem or test;
3. do not add arbitrary compensating fields;
4. do not protect sunk effort;
5. globally rerank the project.

---

# 32. Branch Promotion Conditions

The current dinuclear EFT may move from:

```text
PARAMETRIC_LOW_ENERGY_SURVIVOR
```

to:

```text
MICROSCOPIC_THEORETICAL_CANDIDATE
```

only if it passes:

```text
RELATIVISTIC_OPERATOR_BASIS
GAUGE_INVARIANCE
SYMMETRY_PROTECTION
RG_OPERATOR_MIXING
ONE_BODY_LEAKAGE
ULTRALIGHT_MASS_NATURALNESS
INDEPENDENT_MATCHING
EXACT_EXPERIMENTAL_BOUND
STELLAR_CONSTRAINTS
COSMOLOGICAL_CONSTRAINTS
```

Even after these pass:

```text
KNOWN_REAL_MATERIAL=NO
```

until an actual material-specific microscopic calculation demonstrates the operator.

---

# 33. Material Realization Gate

Do not scan materials before the microscopic interaction itself survives.

Once the UV theory is credible, material candidates may be ranked by:

* existence of the required bound pair state;
* spin-state projector purity;
* cooperative switching;
* mixing with ordinary configurations;
* actual bound-state wavefunctions;
* binding energy;
* pair density;
* thermal occupation;
* finite-size susceptibility;
* control free energy.

The target low-energy values currently include:

```text
TARGET_DINUCLEAR_COUPLING=
8.638353631211470e-12

CONTROL_SITE_EV=
0.07919352471801402

CONTROL_DIMER_EV=
0.1583870494360280
```

These values should be treated as benchmark targets, not predictions for any known material.

---

# 34. Current Pathway Ranking

This ranking reflects expected information gain, not scientific certainty.

## Priority 1 — Protected relativistic two-body scalar matching

Status:

```text
ACTIVE
```

Reason:

* current lowest-complexity low-energy survivor exists;
* low-energy consistency gates are unusually advanced;
* one UV calculation could either promote or kill the branch;
* current uncertainty is fundamental rather than parametric.

Primary question:

```text
CAN_C_PHI_EXIST_WITHOUT_ONE_BODY_LEAKAGE_OR_M_PHI_NATURALNESS_FAILURE
```

---

## Priority 2 — Classical positive-energy GR construction

Status:

```text
ESTABLISHED_REFERENCE
DEPRIORITIZED_FOR_PRACTICALITY
```

Reason:

* strongest established project result;
* well-verified local repulsion;
* severe $ah^2/G$ energy scaling;
* no known material realization;
* additional coefficient optimization presently has low expected value.

---

## Priority 3 — Established quantum stress-energy

Status:

```text
CONSTRAINED_REFERENCE_BRANCH
```

Reason:

* established QFT permits local negative energy;
* complete-apparatus and QEI effects remain severe;
* no practical macroscopic escape found in tested scope.

---

## Priority 4 — Exact Einstein-Maxwell repulsion

Status:

```text
REFERENCE_SOLUTION
```

Reason:

* exact established-theory local repulsion;
* physically real Maxwell energy;
* required electric fields/charge are catastrophically large for practical use.

---

## Priority 5 — Other fifth-force vector mechanisms

Status:

```text
STRONGLY_DISFAVORED_IN_TESTED_MINIMAL_FORMS
```

Reason:

* simple phenomenological vectors can repel;
* electroweak matching, axial sectors, stellar constraints, and longitudinal-mode consistency strongly damage minimal useful realizations.

Reopen only with a genuinely new theoretically motivated protection mechanism.

---

## Priority 6 — Modified gravity

Status:

```text
DEFERRED
```

Reason:

* enormous model space;
* easy to obtain desired signs by assumption;
* low information value compared with the sharp current UV-matching gate.

Do not jump to modified gravity merely because the current branch becomes difficult.

---

# 35. Closed or Strongly Disfavored Routes

Do not casually restart the following.

```text
LIGHT_POINTLIKE_HIDDEN_CARRIER_PER_ATOMIC_CELL
= REJECTED_BY_LOCALIZATION_NATURALNESS
```

```text
MATERIAL_CREATED_10KEV_HIDDEN_CONDENSATE
= REJECTED_AS_PRACTICAL_ROUTE
```

```text
DIRECT_UNPROTECTED_ELECTRON_MASS_PORTAL
= REJECTED_BY_RADIATIVE_NATURALNESS
```

```text
SIMPLE_FUNDAMENTAL_ELECTRON_CURRENT_MEDIATOR
= REJECTED_BY_ELECTRON_G_MINUS_2_PREFLIGHT
```

```text
LINEAR_CONTINUOUS_STRUCTURAL_SELECTOR
= REJECTED_BY_SCALAR_POLARIZATION
```

```text
SIMPLE_EVEN_STRUCTURAL_MONOMIAL_SELECTOR
= REJECTED_BY_ZERO_POINT_AND_THERMAL_LEAKAGE
```

```text
NORMAL_ORDERED_QUADRATIC_SELECTOR
= REJECTED_BY_FINITE_TEMPERATURE_LEAKAGE
```

```text
UNIVERSAL_HIGH_SPIN_PORTAL
= REJECTED_BY_ORDINARY_MATTER_LEAKAGE
```

```text
ACCIDENTALLY_TUNED_POLYNOMIAL_PROJECTOR
= REJECTED_AS_UNPROTECTED_FINE_TUNING
```

```text
FUNDAMENTAL_RELATIVISTIC_DIMER
= REJECTED_BY_ULTRALIGHT_SCALAR_NATURALNESS
```

```text
GENERIC_UNPROTECTED_RELATIVISTIC_MATCHING
= REJECTED_BY_OPERATOR_LEAKAGE
```

A rejected branch should only be reopened if a new physical principle directly changes the calculation that killed it.

---

# 36. Anti-Drift Rules

Do not:

* optimize an already-invalid mechanism;
* add new hidden particles before resolving UV matching;
* change the material solely to avoid a theoretical contradiction;
* call an unexplained coefficient a physical mechanism;
* assume a tree-level zero remains zero under loops;
* confuse NR particle-number protection with a relativistic UV symmetry;
* ignore antiparticle/high-energy sectors when claiming a UV theory;
* retune the ultralight scalar bare mass against enormous corrections;
* use generic loop suppression as sufficient material selectivity;
* use a fifth-force model and describe it as ordinary GR antigravity;
* confuse ground-referenced force with reactionless propulsion;
* reopen Casimir or modified-gravity branches simply because the active UV problem is difficult;
* move to hardware design before the microscopic force survives;
* interpret control free-energy scales as demonstrated electrical power requirements.

---

# 37. Independent Verification Rule

Every central quantitative result should eventually have at least two genuinely independent verification paths.

Examples:

```text
ANALYTIC_DERIVATION
vs
NUMERICAL_INTEGRATION
```

```text
RELATIVISTIC_MATCHING
vs
BOUND_STATE_FEYNMAN_HELLMANN
```

```text
AUXILIARY_DIMER_EFT
vs
DIRECT_TWO_BODY_CONTACT_OPERATOR
```

```text
PROJECT_CALCULATION
vs
PUBLISHED_EXPERIMENTAL_BOUND
```

A regression test that calls the same production function is not independent scientific verification.

---

# 38. Mandatory Limiting Cases for the Current UV Problem

Every proposed microscopic completion should explicitly test the following.

## Scalar-decoupling limit

```math
C_\phi\to0
```

All new force effects must vanish.

## No-binding limit

As:

```math
E_{\mathrm{bind}}\to0
```

the claimed bound-state-specific charge must behave consistently.

## Zero-mixing limit

```math
t\to0
```

The dressed response must approach the unmixed limit.

## Infinite-detuning limit

```math
\Delta\to\infty
```

Target-state contamination of ordinary states must vanish.

## Heavy-mediator limit

A heavy UV mediator should decouple with the correct power of its mass.

## Symmetry-restoration limit

Turning off the symmetry-breaking spurion responsible for the pair operator should restore the claimed protection.

## Infinite-volume versus finite-volume limit

The finite-body stability result must not be mistaken for an infinite-medium theorem.

---

# 39. Required Outputs for the Next Major Gate

The next protected-matching gate should explicitly print or preserve:

```text
SCIENTIFIC_QUESTION
MICROSCOPIC_FIELD_CONTENT
GAUGE_GROUP
EXACT_SYMMETRIES
SPURIONS
DESIRED_OPERATOR
LOWEST_DIMENSION_DANGEROUS_ONE_BODY_OPERATORS
TREE_LEVEL_MATCH
ONE_LOOP_MIXING
RG_RUNNING
ULTRALIGHT_MASS_CORRECTION
NR_MATCHED_C_PHI
ONE_BODY_LEAKAGE_RATIO
LIMITING_CASES
INDEPENDENT_RECONSTRUCTION
LITERATURE_COMPARISON
STOP_RULE_TRIGGERED
CLAIM_CLASSIFICATION
NEXT
```

Do not produce only a final `GREEN` label.

The physical reason for the decision must remain auditable.

---

# 40. Research-Session Efficiency Protocol

## Step 1 — Orient

Read:

```text
RESEARCH_BUILDPLAN.md
NOTES.md
FORMATTING_AND_CODE_STANDARDS.md
```

and inspect the latest codebundle if implementation state matters.

## Step 2 — Reconfirm regression baseline

Expected:

```text
94 PASSED
```

## Step 3 — State one scientific question

Current example:

> Can an exact relativistic symmetry allow the required pair scalar response while forbidding one-body scalar charge?

## Step 4 — Perform the cheapest decisive analytical check

Before coding a large model, test:

* operator dimensions;
* gauge charges;
* symmetry selection rules;
* loop mixing;
* dimensional analysis.

## Step 5 — Only then implement a numerical gate

Do not start with a large simulation if algebra already kills the model.

## Step 6 — Attempt falsification

Try to generate the forbidden one-body term.

Try to destabilize $m_\phi$.

Try to violate the leakage bound.

## Step 7 — Independently reconstruct central numbers

Do not test an implementation only against itself.

## Step 8 — Interpret

Record:

```text
WHAT_CHANGED
WHAT_WAS_LEARNED
WHAT_WAS_FALSIFIED
WHAT_REMAINS_UNRESOLVED
CLAIM_CLASSIFICATION
NEXT
```

## Step 9 — Preserve

Durable results belong in:

```text
NOTES.md
results/logs/
results/data/
tests/
```

as appropriate.

---

# 41. Default Time Allocation

For a focused research session, prefer approximately:

```text
5-10 minutes:
Orient, inspect baseline, define question.

20-30 minutes:
Analytical symmetry/operator attack.

20-30 minutes:
Focused numerical or symbolic check if needed.

10-15 minutes:
Independent reconstruction and falsification.

5-10 minutes:
Interpret, document, set NEXT.
```

Do not force a predetermined schedule if the branch fails earlier.

An early clean no-go is a successful research session.

---

# 42. Quantities to Track for Classical GR Branches

When comparing metric/stress-energy architectures, retain:

```math
C
```

in:

```math
M
=
C\frac{ah^2}{G}
```

and track:

* total energy;
* energy density;
* principal pressures;
* stress-to-energy ratios;
* compactness;
* source-target distance;
* local conservation residual;
* NEC/WEC/DEC margins;
* repulsive-zone extent;
* convergence;
* stability.

---

# 43. Quantities to Track for Fifth-Force Branches

For current scalar mechanisms track:

```text
lambda
m_phi
alpha_Y
alpha_source
alpha_test
g_nucleon
g_site
g_bound_state
C_phi
atomic_EFT_cutoff
C_phi * cutoff^3
ordinary_matter_leakage_fraction
delta_m_phi^2 / m_phi^2
thermal_susceptibility
finite_size_mu_R
zero_mode_threshold
control_free_energy
binding_energy
mixing
detuning
```

The current decisive quantities are:

```text
MAX_LEAKAGE=
5.772961445324848e-7

TARGET_DINUCLEAR_COUPLING=
8.638353631211470e-12

C_PHI_3A=
9.536416387852626e-20 eV^-3

M_PHI=
3.946539608e-11 eV
```

---

# 44. Claim Promotion Gates

A result may move upward in project status only after the relevant checks.

For the current dinuclear branch, promotion requires:

```text
DIMENSIONAL_CHECK
LIMITING_CASE_CHECK
GAUGE_INVARIANCE_CHECK
SYMMETRY_CHECK
LOOP_OPERATOR_MIXING_CHECK
ULTRALIGHT_NATURALNESS_CHECK
INDEPENDENT_NR_MATCH
EXACT_EXPERIMENTAL_BOUND
STELLAR_CHECK
COSMOLOGY_CHECK
LITERATURE_COMPARISON
ASSUMPTION_AUDIT
```

Passing project calculations alone does not constitute discovery.

---

# 45. Current Project Checkpoint

Strongest established result:

```text
006D_FINITE_POSITIVE_ENERGY_LINEARIZED_GR_REPULSION=
ESTABLISHED_IN_STATED_SCOPE
```

Current leading speculative mechanism:

```text
PROTECTED_DINUCLEAR_BOUND_STATE_SCALAR_RESPONSE=
PARAMETRIC_LOW_ENERGY_SURVIVOR
```

Current low-energy checks:

```text
FINITE_SIZE_STABILITY=
PASS_IN_SELECTED_MODEL

THERMAL_SELECTOR_WINDOW=
PASS_IN_SELECTED_MODEL

EXACT_SELECTOR_LOGIC=
PASS

FEYNMAN_HELLMANN=
PASS

INDEPENDENT_TWO_BODY_REPRESENTATION=
PASS

ATOMIC_EFT_PERTURBATIVITY=
PASS
```

Current fundamental failures:

```text
FUNDAMENTAL_RELATIVISTIC_DIMER=
REJECTED

GENERIC_UNPROTECTED_RELATIVISTIC_MATCH=
REJECTED
```

Current unresolved frontier:

```text
PROTECTED_RELATIVISTIC_UV_MATCH=
NOT_ESTABLISHED

ONE_BODY_OPERATOR_LEAKAGE=
NOT_CLOSED

ULTRALIGHT_MASS_NATURALNESS=
NOT_CLOSED_FOR_ANY_ACTUAL_COMPLETION

EXACT_CURRENT_5KM_BOUND=
NOT_CLOSED

REAL_MATERIAL_WITH_PORTAL=
NO

PRACTICAL_ANTIGRAVITY=
NO

NOVELTY=
NOT_ESTABLISHED
```

---

# 46. Current Decision Tree

```text
START
  |
  v
CAN AN EXACT / TECHNICALLY NATURAL RELATIVISTIC STRUCTURE
GENERATE THE REQUIRED TWO-BODY SCALAR OPERATOR?
  |
  +-- NO --> CLOSE CURRENT MATERIAL-SCALAR BRANCH
  |
  +-- YES
        |
        v
DO LOOPS / RG GENERATE ONE-BODY CHARGE ABOVE 5.77e-7?
        |
        +-- YES --> CLOSE BRANCH
        |
        +-- NO
              |
              v
IS m_phi ~ 3.95e-11 eV TECHNICALLY NATURAL?
              |
              +-- NO --> CLOSE BRANCH
              |
              +-- YES
                    |
                    v
DO TWO INDEPENDENT MATCHES REPRODUCE C_phi?
                    |
                    +-- NO --> INVESTIGATE / DO NOT PROMOTE
                    |
                    +-- YES
                          |
                          v
IS THE 5-km FORCE POINT EXPERIMENTALLY ALLOWED?
                          |
                          +-- NO --> CLOSE / RERANK
                          |
                          +-- YES
                                |
                                v
DO STELLAR + COSMOLOGICAL CONSTRAINTS PASS?
                                |
                                +-- NO --> CLOSE / RERANK
                                |
                                +-- YES
                                      |
                                      v
PROMOTE TO MICROSCOPIC THEORETICAL CANDIDATE
THEN BEGIN REAL-MATERIAL MATCHING
```

This decision tree should prevent the project from drifting into additional speculative detail before the central physics is resolved.

---

# 47. Planned Execution Order

```text
0. REGRESSION BASELINE
   Confirm 94 tests or understand any change.

1. PROTECTED RELATIVISTIC OPERATOR / SYMMETRY GATE
   Construct complete operator basis.
   Search for exact protection or prove a no-go.

2. ONE-BODY OPERATOR MIXING GATE
   Calculate tree-level and loop/RG leakage.

3. ULTRALIGHT SCALAR NATURALNESS GATE
   Compute actual threshold corrections.

4. INDEPENDENT MICROSCOPIC MATCH
   Reconstruct C_phi by two methods.

5. EXACT 5-KM EXPERIMENTAL BOUND CLOSURE
   Obtain numerical curve data or independently digitize.

6. MODEL-SPECIFIC STELLAR / COSMOLOGY GATE
   Only after the microscopic operator exists.

7. FIFTH-FORCE BRANCH DECISION
   Survive -> microscopic candidate.
   Fail -> close/demote and globally rerank.

8. REAL MATERIAL MATCH
   Only after theoretical microscopic survival.

9. EXPERIMENTAL ACCESSIBILITY
   Only after a real material mechanism exists.

10. PRACTICAL ENGINEERING
    Far downstream.
```

---

# 48. Global Reranking Rule if Current Branch Dies

If the protected relativistic matching fails, do not immediately invent another variant of the same material scalar interaction.

Perform a global rerank among:

```text
CLASSICAL_GR_MATERIAL_REALIZATION
NEW_ESTABLISHED_QFT_STRESS_ENERGY_IDEA
OTHER_HEALTHY_FIFTH_FORCE_CLASSES
HIGHLY_CONSTRAINED_MODIFIED_GRAVITY
NEGATIVE_RESULT / PROJECT_STOP
```

The reranking should explicitly compare:

* theory confidence;
* remaining feasibility gap;
* number of required speculative assumptions;
* current experimental constraints;
* information gain of the next calculation.

Stopping a branch is scientifically preferable to indefinite model proliferation.

---

# 49. What Would Count as the Next Major Breakthrough

## Positive theoretical breakthrough

A local relativistic theory is found in which:

1. the required two-body material scalar operator is generated;
2. dangerous one-body operators are symmetry forbidden or parametrically below bounds;
3. $m_\phi\sim4\times10^{-11},{\rm eV}$ remains technically natural;
4. independent matching reproduces the low-energy coefficient;
5. current terrestrial constraints permit the useful force point.

This would justify classification as:

```text
MICROSCOPIC_THEORETICAL_CANDIDATE
```

It would still not establish a material or device.

## Negative theoretical breakthrough

A theorem or robust calculation shows that every local relativistic completion capable of producing the necessary pair response must:

* generate forbidden one-body charge; or
* destabilize the ultralight mediator; or
* violate current experimental bounds.

That would justify:

```text
CURRENT_MATERIAL_SCALAR_BRANCH=CLOSED
```

A rigorous negative result is a successful outcome.

---

# 50. Documentation Discipline

Use repository files for distinct purposes.

```text
README.md
    Public-facing project overview and conservative headline.

RESEARCH_BUILDPLAN.md
    Active frontier, priorities, decision gates, stop rules, NEXT.

ROADMAP.md
    Broad long-term research map.

RESEARCH_QUESTIONS.md
    Question inventory.

ASSUMPTIONS.md
    Shared assumptions.

CLAIMS.md
    Formal claim classifications.

NOTES.md
    Detailed chronological scientific history.

FORMATTING_AND_CODE_STANDARDS.md
    Markdown, mathematics, documentation, and source-code rules.
```

Do not duplicate the exhaustive O-Y chronology inside this buildplan.

The notes preserve history.

The buildplan controls execution.

---

# 51. Immediate Next Action

```text
ACTIVE_FRONTIER=
PROTECTED_RELATIVISTIC_TWO_BODY_MATCH_OR_BRANCH_CLOSE

ACTIVE_TASK=
RELATIVISTIC_OPERATOR_BASIS_AND_ONE_BODY_MIXING_NO_GO_GATE

PRIMARY_QUESTION=
CAN_THE_REQUIRED_TWO_BODY_BOUND_STATE_SCALAR_RESPONSE_EXIST_IN_A_TECHNICALLY_NATURAL_LOCAL_RELATIVISTIC_THEORY_WITHOUT_FORBIDDEN_ONE_BODY_CHARGE

REGRESSION_BASELINE=
94_PASSED

LOW_ENERGY_TARGET_OPERATOR=
C_PHI_PHI_A_DAGGER_B_DAGGER_B_A

TARGET_DINUCLEAR_COUPLING=
8.638353631211470e-12

REPRESENTATIVE_C_PHI_EV_MINUS3=
9.536416387852626e-20

MAX_ORDINARY_MATTER_LEAKAGE_FRACTION=
5.772961445324848e-7

MEDIATOR_MASS_EV=
3.946539608e-11

KNOWN_REAL_MATERIAL_WITH_PORTAL=
NO

PRACTICAL_ANTIGRAVITY=
NO

NOVELTY=
NOT_ESTABLISHED

NEXT=
RELATIVISTIC_PROTECTED_TWO_BODY_OPERATOR_MIXING_GATE
```

The first next-session calculation should be the cheapest symmetry/operator-mixing attack capable of killing the branch.

Do not begin with another material model.

Do not begin with another hidden field.

Do not begin with device engineering.

First determine whether the required low-energy interaction can exist inside a technically natural local relativistic theory at all.
