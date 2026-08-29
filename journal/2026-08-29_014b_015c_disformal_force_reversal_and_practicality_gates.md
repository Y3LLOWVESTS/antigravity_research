# Research Journal — 2026-08-29

## Disformal Local Total-Force Reversal, Baryonic-Bridge Failure, Protected-Pair UV Preflight, and Finite-Payload Integration Gate

## Objective

The principal question of this research slice was:

> **Can the project-reproduced non-static disformal force reversal be promoted from a local grid-cell effect toward a physically meaningful finite-body antigravity-like force, and can the required coupling plausibly be connected to ordinary matter?**

This journal preserves the chain of work from Simulations 014B through 015C so that the branch can be reconstructed later if the renewed 006D established-GR route does not reach practical antigravity.

The branch was tested in progressively stronger stages:

```text
014B
NONSTATIC DISFORMAL REPULSION PREREQUISITE

014C
ANTIPARALLEL FIFTH-FORCE REPRODUCTION
+
WEAK-PERTURBATION SCALING THEOREM

014D
LOCAL TOTAL-FORCE REVERSAL

014E
ORDINARY-BARYON CONSTANT-B BRIDGE FEASIBILITY

015A
MINIMAL PROTECTED-PAIR RELATIVISTIC UV PREFLIGHT

015B
014D SOURCE/API AUDIT FOR FINITE-PAYLOAD EXTENSION

015C
FINITE LOCALIZED SOURCE + FINITE PASSIVE PAYLOAD
CENTER-OF-MASS FORCE GATE
```

The strongest positive result remains the 014D numerical demonstration of **local total-force reversal** in a controlled reduced non-static disformal model.

The strongest negative results added afterward are:

1. the minimal constant-$B$ bridge to ordinary Standard-Model matter fails by approximately $3.46\times10^{57}$ in coupling strength in the declared EFT comparison;
2. ordinary additive internal symmetry is insufficient to protect the minimal relativistic pair portal from one-body scalar counterterms;
3. the first finite-payload root-time search found **no safe finite-payload center-of-mass reversal** in the tested localized-source domain.

These conclusions do not constitute a universal no-go theorem against disformal or collective fifth-force antigravity.

They substantially narrow the remaining route.

---

## Starting State

### Established project anchor outside this branch

The strongest established project-derived gravitational result remains Simulation 006D.

Within static linearized general relativity, 006D constructed an explicit finite-radius, finite-thickness, nonsingular, positive-energy, locally conserved type-I stress-energy configuration satisfying NEC, WEC, and DEC whose near gravitational field points outward while its integrated far-field active mass remains positive.

Its best tested finite-thickness coefficient is

```math
C_{\mathrm{finite}}
=
23.591586299249
```

in

```math
M_{\mathrm{equiv}}
=
C\frac{ah^2}{G}
```

The independent thin conserved reference is

```math
C_{\mathrm{thin}}
=
23.426710175391
```

The 006D result remains an established-model mathematical construction, not a practical apparatus.

### Why the disformal branch was opened

Earlier static pure-disformal work had not produced a leading-order static fifth force, but that result did not exclude explicitly time-dependent backgrounds.

The 014 branch therefore investigated a distinct regime:

```text
NONSTATIC
PERTURBED
NONSYMMETRIC
NONLINEAR
```

rather than rerunning a rejected static mechanism.

### Regression baseline

The repository known-solution regression suite remained:

```text
94 passed
```

through the 015A, 015B, and repaired 015C gates.

### Preserved source integrity

The disposable 014-series source files were copied byte-for-byte into `simulations/`.

Their preserved SHA-256 values are:

```text
014B
8f6a3b0e5cb28546c456766d506460029b5f694a95ee76c526e0d842f945fb1b

014C
59132b42245d10187d1c26ff4ab75fa8c9cb36973bfc06420480013227dc93e1

014D
01220601e0ed71e84c79c94b36fec7d60b596572bc192b1ce168dec2db35d71c

014E
b363cfadff64f73db80bc5e8f5ab65cddd95842431c6a610a9338d6f218956e6
```

The byte comparisons all returned zero:

```text
014B_IDENTICAL=0
014C_IDENTICAL=0
014D_IDENTICAL=0
014E_IDENTICAL=0
```

Therefore the scientific source used for the 014B-014E results was successfully preserved.

---

# Work Performed

## 1. Simulation 014B — non-static disformal prerequisite

### Scientific question

Could the explicitly time-dependent disformal background enter a healthy regime associated with the sign-sensitive nonlinear behavior required for a repulsive fifth-force component?

The weak-field force-divergence structure motivating the test was

```math
\nabla\cdot\mathbf F_\phi
=
(1-\delta_d)\eta^2
\nabla\cdot\mathbf F_\Psi
```

with

```math
\eta^2
\propto
\frac{\xi^2}{g_\phi}
```

A healthy/invertible branch requires

```math
g_\phi>0
```

and consequently

```math
\eta^2\ge0
```

When $\eta^2>0$, the fifth-force divergence changes sign relative to Newtonian gravity when

```math
1-\delta_d<0
```

or equivalently

```math

\delta_d>1

```

At homogeneous background order, $\delta_d=0$, so spatial and nonlinear corrections are essential.

### Background equation

For the tested $\beta=0$ background, the dimensionless scalar equation was

```math
\ddot\chi
=
-\frac{2t}{t^2+D}\dot\chi
+
\frac{t^2}{t^2+D}e^{-\chi}
```

For this branch,

```math
\xi_0
\propto
\ddot\chi
```

so roots of

```math
\ddot\chi=0
```

locate the high-sensitivity $\xi_0=0$ windows.

### Numerical reproduction

The early-time analytical solution was reproduced with maximum relative error

```text
1.4488209440023864e-04
```

Four tested background families developed $\xi_0$ sign changes:

```text
FIDUCIAL    t ≈ 3.50612
VF          t ≈ 3.50612
STEEP       t ≈ 5.34931
FF_BASE     t ≈ 18.87736
```

All tested sign changes remained on the healthy branch

```math
g_\phi>0
```

with

```text
MIN_G_PHI_ACROSS_TESTED_BACKGROUNDS=
6.7568601471089274e-01
```

and

```text
ALL_TESTED_BETA0_MODELS_HAVE_XI0_SIGN_CHANGE=YES
```

Near the roots, the diagnostic sensitivity scale was approximately

```text
1/xi_proxy^2 ~ 1e5 to several e6
```

### 014B conclusion

014B established a necessary/high-value prerequisite window.

It did **not** establish an actual repulsive force.

```text
XI_ZERO_ALONE_PROVES_REPULSION=NO
```

Claim classification:

```text
PROJECT_DERIVED_REPRODUCTION_OF_PUBLISHED_DISFORMAL_REPULSION_PREREQUISITE
```

---

## 2. Simulation 014C — antiparallel fifth-force reproduction

### Force definitions

The reduced model used Newtonian peculiar acceleration

```math
\mathbf F_\Psi
=
-\frac{\nabla\Psi}{a^2}
```

and disformal fifth force

```math
\mathbf F_\phi
=
-\frac12
\frac{\xi}{g_\phi}
\nabla\phi
```

For the constant-$B$, $\beta=0$ branch,

```math
\xi
=
2B\ddot\phi
```

with the disformal metric factor

```math
g_\phi
=
1
+
B
\left[
-\dot\phi^2
+
\frac{|\nabla\phi|^2}{a^2}
\right]
```

The scalar field was evolved without imposing a quasistatic approximation.

### Positive numerical result

014C found regions satisfying

```math

\mathbf F_\phi\cdot\mathbf F_\Psi<0

```

This is an actual fifth-force component pointing partly or fully opposite Newtonian gravity.

At the $\xi_0$ root, the 2D refinement found approximately

```text
REPULSIVE_FRACTION ≈ 0.49
STRONGLY_ANTIPARALLEL_FRACTION ≈ 0.378
MIN_COS ≈ -1
```

The sign survived

```text
48x48
72x72
96x96
128x128
```

with high-grid RMS-ratio change

```text
0.00645
```

Independent 3D calculations found approximately

```text
REPULSIVE_FRACTION ≈ 0.57
STRONGLY_ANTIPARALLEL_FRACTION ≈ 0.57
MIN_COS ≈ -1
```

across

```text
24^3
32^3
40^3
```

with high-grid RMS-ratio change

```text
0.0213
```

The minimum metric factor over the refinement runs was

```text
MIN_GPHI_ALL_REFINEMENT_RUNS=
6.6736404459014953e-01
```

so this force-sign result did not depend on approaching $g_\phi=0$.

However, the largest repulsive fifth-force magnitude relative to Newtonian gravity at a meaningful tested point was only

```text
MAX_REPULSIVE_F5_OVER_FN_ANY_TESTED_MEANINGFUL_POINT=
3.0717239259386252e-02
```

Therefore

```text
TOTAL_FORCE_REVERSAL_FOUND=NO
```

in 014C.

---

## 3. 014C analytical result — weak-perturbation order theorem

This is an analytical project result and should be preserved separately from the numerical 014C force-sign observation.

Consider a regular perturbation expansion around a homogeneous background satisfying $\xi_0=0$.

Write

```math
\phi
=
\phi_0
+
\epsilon\phi_1
+
O(\epsilon^2)
```

and

```math
\Psi
=
\epsilon\Psi_1
+
O(\epsilon^2)
```

At the background root,

```math
\xi_0=0
```

so regular perturbation theory gives

```math
\xi
=
\epsilon\xi_1
+
O(\epsilon^2)
```

Assume the healthy background remains nondegenerate:

```math
g_\phi
=
g_0
+
O(\epsilon)
```

with

```math
g_0>0
```

Because $\phi_0$ is homogeneous,

```math
\nabla\phi_0=0
```

and therefore

```math
\nabla\phi
=
\epsilon\nabla\phi_1
+
O(\epsilon^2)
```

Expand the inverse disformal factor:

```math
\frac{1}{g_\phi}
=
\frac{1}{g_0}
+
O(\epsilon)
```

Substituting into

```math
\mathbf F_\phi
=
-\frac12
\frac{\xi}{g_\phi}
\nabla\phi
```

gives

```math
\mathbf F_\phi
=
-\frac12
\left[
\epsilon\xi_1+O(\epsilon^2)
\right]
\left[
\frac{1}{g_0}+O(\epsilon)
\right]
\left[
\epsilon\nabla\phi_1+O(\epsilon^2)
\right]
```

so

```math

\mathbf F_\phi
=
-\frac{\epsilon^2}{2g_0}
\xi_1\nabla\phi_1
+
O(\epsilon^3)

```

Hence

```math

\mathbf F_\phi
=
O(\epsilon^2)

```

Meanwhile,

```math
\mathbf F_\Psi
=
-\frac{\nabla\Psi}{a^2}
```

and

```math
\Psi
=
\epsilon\Psi_1
+
O(\epsilon^2)
```

imply

```math

\mathbf F_\Psi
=
O(\epsilon)

```

Therefore

```math

\frac{
|\mathbf F_\phi|
}{
|\mathbf F_\Psi|
}
=
O(\epsilon)

```

and thus

```math

\lim_{\epsilon\to0}
\frac{
|\mathbf F_\phi|
}{
|\mathbf F_\Psi|
}
=
0

```

within a regular weak-field expansion about the $\xi_0=0$ background.

This is **not** a universal no-go theorem against nonperturbative disformal enhancement.

It proves that the disformal mechanism cannot dominate Newtonian gravity in the strict regular $\epsilon\to0$ perturbative limit around this root.

### Numerical verification of the theorem

The amplitude scan measured

```text
ASYMPTOTIC_F_PHI_POWER=
1.9911392202550136

ASYMPTOTIC_F_PSI_POWER=
1.0000000000000002

ASYMPTOTIC_FORCE_RATIO_POWER=
9.9113922025501222e-01
```

in excellent agreement with the analytical powers

```math
2,\quad1,\quad1
```

for fifth force, Newtonian force, and their ratio respectively.

Claim classification:

```text
PROJECT_DERIVED_ANALYTIC_RESULT
PROVED_WITHIN_REGULAR_PERTURBATIVE_ASSUMPTIONS
```

---

## 4. Simulation 014D — local total-force reversal

014D strengthened the operational criterion from a repulsive correction to reversal of the total acceleration projection.

Define

```math
\mathbf F_{\mathrm{tot}}
=
\mathbf F_\Psi
+
\mathbf F_\phi
```

A repulsive fifth-force component requires only

```math
\mathbf F_\phi
\cdot
\mathbf F_\Psi
<
0
```

Actual local total-force reversal requires

```math

\mathbf F_{\mathrm{tot}}
\cdot
\mathbf F_\Psi
<
0

```

Substituting the total force gives

```math
\left(
\mathbf F_\Psi
+
\mathbf F_\phi
\right)
\cdot
\mathbf F_\Psi
<
0
```

or

```math
|\mathbf F_\Psi|^2
+
\mathbf F_\phi
\cdot
\mathbf F_\Psi
<
0
```

Therefore the exact projection condition is

```math

-\mathbf F_\phi
\cdot
\mathbf F_\Psi
>
|\mathbf F_\Psi|^2

```

For perfectly antiparallel forces this reduces to

```math

|\mathbf F_\phi|
>
|\mathbf F_\Psi|

```

This is the mathematical reason 014D is stronger than 014C.

### Coupling scan

The dimensionless disformal parameter $b_0$ was scanned through

```text
0.10
0.14
0.18
0.20
0.22
0.24
0.26
0.28
0.30
```

No local total reversal appeared through

```text
b0=0.22
```

The first coarse safe reversal occurred at

```text
b0=0.24
```

with

```text
ROOT_TOTAL_REVERSAL_FRAC=
0.0217293

ROOT_MAX_F5_OVER_FN=
1.63322

ROOT_MAX_OUTWARD_TOTAL_PROJ=
0.596925

ROOT_MIN_GPHI=
0.238378
```

At

```text
b0=0.28
```

the coarse signal became stronger:

```text
ROOT_TOTAL_REVERSAL_FRAC=
0.258488

ROOT_MAX_F5_OVER_FN=
3.70665

ROOT_MAX_OUTWARD_TOTAL_PROJ=
2.24505

ROOT_MIN_GPHI=
0.139278
```

### Validation

The principal validated point was

```text
b0=0.28
```

2D refinement:

```text
64x64
96x96
128x128
```

Independent 3D refinement:

```text
24^3
32^3
40^3
```

The preserved validation summary includes

```text
FIRST_COARSE_SAFE_REVERSAL_b0=
0.24

VALIDATED_REVERSAL_b0=
0.28

MIN_GPHI_VALIDATED_RUNS=
1.3850683595823443e-01

MIN_KINETIC_DENOMINATOR=
1.0762544665082980

MAX_ABS_PSI_VALIDATED_RUNS=
2.2492342554914720e-02

MAX_3D_ROOT_OUTWARD_TOTAL_PROJECTION_OVER_NEWTONIAN=
6.0665748860744895e-01

MAX_3D_ROOT_TOTAL_REVERSAL_FRACTION=
1.2972271769093562e-02

TIMESTEP_HALVING_OUTWARD_PROJECTION_REL_CHANGE=
1.0299289263913065e-04

2D_HIGH_GRID_MAX_OUTWARD_PROJECTION_REL_CHANGE=
3.1517358377771668e-03

3D_HIGH_GRID_MAX_OUTWARD_PROJECTION_REL_CHANGE=
4.6657528364683364e-02
```

The result survived timestep halving.

The minimum $g_\phi$ remained above the declared safety floor

```math
g_\phi\ge0.1
```

and the kinetic denominator remained positive.

### 014D result

```text
PROJECT_REPRODUCED_LOCAL_TOTAL_FORCE_REVERSAL=
YES_IN_CONTROLLED_REDUCED_DISFORMAL_MODEL

NONSYMMETRIC_2D_TOTAL_FORCE_REVERSAL=YES

NONSYMMETRIC_3D_TOTAL_FORCE_REVERSAL=YES

TOTAL_FORCE_REVERSAL_SURVIVES_GRID_REFINEMENT=YES

TOTAL_FORCE_REVERSAL_SURVIVES_TIMESTEP_HALVING=YES

LOCAL_TOTAL_ACCELERATION_PROJECTION_OPPOSITE_NEWTONIAN_GRAVITY=YES
```

Claim classification:

```text
PROJECT_DERIVED_REDUCED_DISFORMAL_LOCAL_TOTAL_FORCE_REVERSAL
```

This result is numerical, not a universal analytical theorem.

---

## 5. Simulation 014E — ordinary-baryon constant-disformal bridge

014E asked whether the coupling scale required by 014D could be connected directly to Standard-Model matter through the minimal constant disformal operator.

### Notation correction

The numerical parameter called `B0` in the reduced 014C/014D code corresponds to a dimensionless quantity $b_0$, related to the dimensionful disformal coefficient by

```math

b_0
=
H_0^2 M_{\mathrm{Pl}}^2 B_0

```

For the minimal constant operator,

```math
B_0
=
\frac{1}{M_D^4}
```

therefore

```math

b_0
=
\frac{
H_0^2 M_{\mathrm{Pl}}^2
}{
M_D^4
}

```

Solving for the suppression scale gives

```math

M_D
=
\sqrt{
H_0M_{\mathrm{Pl}}
}
\,
b_0^{-1/4}

```

### Physical scale of the 014D reversal

The first local reversal at $b_0=0.24$ corresponds to

```text
FIRST_REVERSAL_DISFORMAL_SCALE=
2.6799511607263058e-03 eV
```

The validated $b_0=0.28$ point corresponds to

```text
VALIDATED_REVERSAL_DISFORMAL_SCALE=
2.5786368350373110e-03 eV
```

Thus the minimal constant-disformal operating scale is of order a few meV.

### Constant-$B$ coupling-gap proof

For

```math
B=\frac{1}{M_D^4}
```

the ratio of two constant couplings is

```math
\frac{
B_{\mathrm{operating}}
}{
B_{\mathrm{constrained}}
}
=
\left(
\frac{
M_{D,\mathrm{constrained}}
}{
M_{D,\mathrm{operating}}
}
\right)^4
```

Using the project's declared constant-coupling comparison with the $650\,{\mathrm{GeV}}$ benchmark gives

```text
COLLIDER_ALLOWED_CONSTANT_B_b0_MAX=
6.9353012973239908e-59
```

and

```text
CONSTANT_B_COUPLING_GAP=
3.4605562139399018e57
```

The corresponding suppression-scale gap is

```text
DISFORMAL_SCALE_GAP=
2.4254173341869428e14
```

Therefore the minimal universal constant-$B$ bridge cannot simply use the operating coupling required by 014D while retaining the declared high-energy bound.

This is a feasibility rejection only within the stated constant-operator comparison.

### Environmental hierarchy required for an escape

An environment-dependent theory would need at least

```math
\frac{
B_{\mathrm{operating}}
}{
B_{\mathrm{constrained}}
}
\gtrsim
3.4605562139399018\times10^{57}
```

The logarithmic hierarchy is

```math
\Delta\ln B
=
\ln
\left(
\frac{
B_{\mathrm{operating}}
}{
B_{\mathrm{constrained}}
}
\right)
```

giving

```text
REQUIRED_ENVIRONMENTAL_DELTA_LN_B=
132.48877963228443
```

or

```math

\Delta\ln B
\gtrsim
132.49

```

This is the central hierarchy any environment-dependent rescue must explain.

### Canonical kinetic compensation failure

The matched canonical kinetic energy density required by the direct compensation estimate was

```text
MATCHED_CANONICAL_KINETIC_ENERGY_DENSITY=
1.3821555639528073e48 J/m^3
```

with equivalent mass density

```text
MATCHED_MASS_EQUIVALENT_DENSITY=
1.5378554657069117e31 kg/m^3
```

### Compactness proof

For an approximately uniform spherical region of energy density $\rho_E$, the mass inside radius $R$ is

```math
M
=
\frac{4\pi}{3}
R^3
\frac{\rho_E}{c^2}
```

The Schwarzschild compactness parameter is

```math
\mathcal C
=
\frac{2GM}{Rc^2}
```

Substitution gives

```math
\mathcal C
=
\frac{
8\pi G\rho_E R^2
}{
3c^4
}
```

Setting $\mathcal C=1$ gives the radius at which the weak/noncompact configuration ceases to be self-consistent:

```math

R_{\mathcal C=1}
=
\sqrt{
\frac{
3c^4
}{
8\pi G\rho_E
}
}

```

For the matched energy density above,

```text
COMPACTNESS_ONE_RADIUS=
3.2329633279144379e-03 m
```

or approximately

```math

R_{\mathcal C=1}
\approx
3.23\ {\mathrm{mm}}

```

Thus a direct canonical-energy compensation route reaches order-unity gravitational compactness at a millimeter scale.

### 014E result

```text
MINIMAL_CONSTANT_B_BARYONIC_BRIDGE=
REJECTED_IN_DECLARED_EFT_SCOPE

ENVIRONMENT_DEPENDENT_OR_UV_COMPLETE_ESCAPE=
LOGICALLY_OPEN

PRACTICAL_ANTIGRAVITY_DEVICE=
NO
```

---

## 6. Simulation 015A — minimal protected-pair portal UV preflight

After the direct universal baryonic bridge failed, the research reranked the earlier protected-composite scalar architecture.

The question was whether an ordinary exact additive internal symmetry could allow a baseline pair/dimer interaction and a scalar-modulated pair interaction while forbidding one-body scalar charges.

### Minimal relativistic portal

Consider fields $A$, $B$, and $D$ with interactions

```math
\mu D^\dagger AB
```

and

```math
y\phi D^\dagger AB
```

For an additive conserved charge, invariance of the baseline interaction requires

```math
-q_D+q_A+q_B=0
```

Invariance of the scalar-modulated interaction requires

```math
q_\phi-q_D+q_A+q_B=0
```

Subtracting the first condition from the second gives

```math

q_\phi=0

```

But the one-body operators

```math
\phi A^\dagger A
```

and

```math
\phi B^\dagger B
```

carry charge

```math
q_\phi-q_A+q_A=q_\phi
```

and

```math
q_\phi-q_B+q_B=q_\phi
```

respectively.

Because $q_\phi=0$, both one-body operators are invariant under the same additive symmetry.

Therefore

```math

\text{ordinary additive symmetry alone cannot forbid the one-body terms}

```

within this minimal portal while allowing both pair vertices.

This is an analytic no-go result for the stated minimal additive-symmetry structure.

### Independent finite-group enumeration

An independent exhaustive $Z_N$ enumeration was run for

```text
2 <= N <= 64
```

using eight worker processes.

Results:

```text
ZN_TOTAL_ASSIGNMENTS_WITH_BOTH_PAIR_VERTICES=
89439

ZN_PROTECTED_ASSIGNMENTS_FOUND=
0

ZN_ENUMERATION_CONFIRMS_ANALYTIC_NO_GO=
True
```

For the first tested groups,

```text
N=2  PAIR_ALLOWED=4   PROTECTED=0
N=3  PAIR_ALLOWED=9   PROTECTED=0
N=4  PAIR_ALLOWED=16  PROTECTED=0
N=5  PAIR_ALLOWED=25  PROTECTED=0
N=6  PAIR_ALLOWED=36  PROTECTED=0
N=7  PAIR_ALLOWED=49  PROTECTED=0
N=8  PAIR_ALLOWED=64  PROTECTED=0
N=9  PAIR_ALLOWED=81  PROTECTED=0
```

The finite enumeration is a computational cross-check; the additive-charge algebra above is the actual general argument for this minimal structure.

### One-loop counterterm power counting

The minimal scalar prototype admits a one-loop two-propagator graph built from one baseline mixing vertex and one scalar-modulated mixing vertex.

For scalar propagators in four dimensions,

```math
L=1
```

and

```math
I=2
```

so the superficial ultraviolet degree is

```math
\omega
=
4L-2I
```

giving

```math

\omega=0

```

Thus the graph is logarithmically divergent by power counting.

Because the local one-body operators are symmetry-allowed, the corresponding counterterms are not excluded by the additive symmetry.

The correct conclusion is:

```text
ONE_BODY_LOOP_DIVERGENCE=
LOGARITHMIC

PHI_A_DAGGER_A_COUNTERTERM_ALLOWED=
YES

PHI_B_DAGGER_B_COUNTERTERM_ALLOWED=
YES

MINIMAL_OFFDIAGONAL_DIMER_PORTAL_TECHNICALLY_NATURAL_ONE_BODY_ZERO=
NO_WITHOUT_ADDITIONAL_PROTECTION
```

### Important limitation on the 015A loop argument

015A also printed the heuristic comparison

```text
GENERIC_ONE_LOOP_FACTOR=
6.3325739776461110e-03

010E_ONE_BODY_LEAKAGE_ALLOWANCE=
5.7729614453248478e-07

GENERIC_LOOP_TO_LEAKAGE_ALLOWANCE_RATIO=
1.0969368213561269e04
```

This ratio must **not** be promoted into a proof that the actual radiatively generated one-body charge exceeds the allowed leakage by $1.1\times10^4$.

The real counterterm coefficient depends on the portal couplings, masses, representation content, renormalization conditions, and possible cancellations.

015A proves that simple additive symmetry does not protect the zero and that the counterterm is allowed/required in the minimal scalar prototype absent additional structure.

It does not determine the full UV coefficient.

### Thermal/EFT scale comparison recorded by 015A

The 014D operating scale corresponds to

```text
B0_0P24_MD_EQUIVALENT_TEMPERATURE_K=
31.099541810042

B0_0P28_MD_EQUIVALENT_TEMPERATURE_K=
29.923837881591
```

At $77\,{\mathrm{K}}$,

```text
kBT / MD(B0=0.24) ≈ 2.4759
```

and at $300\,{\mathrm{K}}$,

```text
kBT / MD(B0=0.24) ≈ 9.6464
```

A conservative condition

```math
\frac{k_BT}{M_D}<0.1
```

would correspond to only about

```text
3.11 K
```

for the first-reversal scale.

By comparison, the earlier 010E atomic EFT cutoff was

```text
657.7566013333334 eV
```

with

```text
010E_77K_KBT_OVER_ATOMIC_EFT_CUTOFF=
1.0087844954029408e-05
```

This comparison helped rerank direct low-scale baryonic disformal coupling below a protected collective architecture for practical research.

### 015A result

```text
MINIMAL_RELATIVISTIC_PAIR_PORTAL=
REJECTED_AS_SUFFICIENT_PROTECTION

ORDINARY_ADDITIVE_PARTICLE_NUMBER_PROTECTION_ALONE=
INSUFFICIENT

NEXT_REQUIRED_PROTECTION_CLASS=
NONTRIVIAL_PAIR_REPRESENTATION_OR_EMERGENT_SEQUESTERING_OR_CANCELLATION_STRUCTURE
```

Claim classification:

```text
PROJECT_DERIVED_MINIMAL_RELATIVISTIC_PAIR_PORTAL_UV_PREFLIGHT
```

---

## 7. Simulation 015B — 014D finite-payload implementation audit

015B was not a new physics calculation.

Its purpose was to inspect the exact preserved 014D implementation before modifying it.

The preserved source had

```text
TOTAL_LINES=2288
```

and exposed the required computational pipeline:

```text
HAS_DENSITY_PIPELINE=True
HAS_PSI_PIPELINE=True
HAS_PHI_PIPELINE=True
HAS_FORCE_PIPELINE=True
READY_TO_BUILD_FINITE_PAYLOAD_GATE=True
```

The extracted force implementation confirmed

```math
\mathbf F_\phi
=
-\frac12
\frac{\xi}{g_\phi}
\nabla\phi
```

and

```math
\mathbf F_\Psi
=
-\frac{\nabla\Psi}{a^2}
```

The audit also confirmed that 014D's density field was imposed rather than evolved through a complete matter/N-body system.

The 015A raw-docstring warning was repaired without changing its scientific content.

Regression result:

```text
94 passed
```

015B therefore established that a finite-payload extension could be constructed directly against the preserved 014D solver rather than reimplementing the model from prose.

---

## 8. Simulation 015C — finite localized source and finite passive payload

### Stronger operational target

014D established local grid-cell reversal.

015C asked whether the effect could survive integration over an entire finite passive payload.

Let $w(\mathbf x)$ be a positive compact-support payload weight.

The mass-weighted center-of-mass acceleration is

```math
\mathbf a_{\mathrm{CM}}
=
\frac{
\int
w(\mathbf x)
\left[
\mathbf F_\Psi(\mathbf x)
+
\mathbf F_\phi(\mathbf x)
\right]
dV
}{
\int
w(\mathbf x)dV
}
```

Define $\hat{\mathbf n}$ to point from the localized source toward the payload center.

Newtonian attraction requires

```math
\mathbf a_{\Psi,\mathrm{CM}}
\cdot
\hat{\mathbf n}
<
0
```

A finite-payload antigravity-like reversal would require

```math

\mathbf a_{\mathrm{CM}}
\cdot
\hat{\mathbf n}
>
0

```

### Payload self-force control

The payload was passive and was **not** inserted into the source density.

Therefore payload self-force was absent by construction in the test-body limit.

The localized positive source's residual Newtonian self-force was also measured numerically.

### Source families

Three finite localized asymmetric source families were tested:

```text
TRIPLET
ELONGATED
LOPSIDED_QUAD
```

The periodic peculiar-density field was mean-subtracted as required by the periodic Poisson solver.

The minimum density contrast was limited to

```text
delta_min=-0.8
```

so

```math
1+\delta\ge0.2
```

throughout the tested source fields.

### Payload scan

The 2D discovery gate used

```text
POINTS=64
CFL=0.1
```

with

```text
b0 =
0.24
0.28
0.30
0.32
```

Payload separations included

```text
dx =
0.20
0.24
0.28
0.32
```

transverse offsets included

```text
dy =
-0.06
0
+0.06
```

and compact-support payload radii included

```text
0.08
0.10
0.12
0.14
```

The root-time discovery search completed 12 source/coupling cases.

### Health criteria

A candidate required

```math
g_\phi\ge0.1
```

a positive kinetic denominator,

```math
K_{\mathrm{eff}}>0
```

and weak Newtonian potential,

```math
|\Psi|\le0.05
```

together with coherent Newtonian attraction across the finite payload.

### Initial software failure and repair

The first 015C execution failed before any physics was evaluated.

Python 3.13's `dataclasses` module could not resolve the dynamically executed 014D module because it had not been registered in `sys.modules`.

The failure was

```text
AttributeError:
'NoneType' object has no attribute '__dict__'
```

The repair registered the synthetic 014D module using `types.ModuleType` and `sys.modules`.

The patch was explicitly classified as

```text
SCIENTIFIC_LOGIC_CHANGED=NO

PATCH_CLASS=
PYTHON_DYNAMIC_MODULE_REGISTRATION_ONLY
```

After repair:

```text
PATCH_RC=0
COMPILE_RC=0
KNOWN_SOLUTION_RC=0
94 passed
015C_RC=0
```

Thus the scientific result below comes from the repaired execution, not from the failed first attempt.

---

## 9. 015C finite-payload result

### Overall discovery result

The repaired run returned

```text
DISCOVERY_COMPLETED_CASES=
12

DISCOVERY_SAFE_GLOBAL_REVERSAL_CASES=
0
```

Therefore

```text
015C_FINITE_PAYLOAD_DISCOVERY=
NO_SAFE_GLOBAL_REVERSAL_IN_TESTED_DOMAIN

GLOBAL_BODY_REPULSION=
NOT_ESTABLISHED

014D_LOCAL_REVERSAL_RESULT=
PRESERVED
```

### Strongest safe finite-payload case

The closest **safe** candidate to reversal was the elongated source at

```text
b0=0.30
```

with payload parameters

```text
OFFSET_X=+0.32
OFFSET_Y=-0.06
RADIUS=0.08
```

Its mass-weighted radial components were

```text
NEWTON_OUT=
-2.3728053747353969e-02

FIFTH_OUT=
+1.2409794690985517e-02

TOTAL_OUT=
-1.1318259056368454e-02
```

The finite payload therefore remained inward.

However, the fifth force canceled a substantial fraction of the Newtonian inward component.

The outward-to-Newtonian ratio is

```math
\frac{
F_{\phi,\mathrm{out}}
}{
|F_{\Psi,\mathrm{out}}|
}
=
\frac{
1.2409794690985517\times10^{-2}
}{
2.3728053747353969\times10^{-2}
}
```

giving approximately

```math

\frac{
F_{\phi,\mathrm{out}}
}{
|F_{\Psi,\mathrm{out}}|
}
\approx
0.523

```

So the strongest safe tested finite payload recovered about $52.3\%$ of the inward Newtonian radial acceleration at root time, but did not cross the reversal threshold.

The same case remained within the declared health margins:

```text
MIN_GPHI=
1.0691164045153490e-01

MIN_KIN=
1.2824192515041732e+00

MAX_ABS_PSI=
1.3865672029500176e-02

SOURCE_SELF_FORCE_RATIO=
3.4176487874780508e-03

SAFE=True

GLOBAL_REVERSAL=False
```

Importantly, the original pointwise local-reversal fraction in this same reduced-field run was

```text
ORIGINAL_LOCAL_REVERSAL_FRAC=
1.1040285568587456e-01
```

Therefore the calculation explicitly demonstrated the distinction

```text
LOCAL_REVERSED_CELLS=YES
FINITE_PAYLOAD_COM_REVERSAL=NO
```

for this tested case.

### Strongest numerical partial cancellation occurred outside the safety floor

The best failed discovery candidate was the elongated source at

```text
b0=0.32
```

with

```text
NEWTON_OUT=
-2.2339606567933542e-02

FIFTH_OUT=
+1.5468045899780243e-02

TOTAL_OUT=
-6.8715606681532997e-03
```

but

```text
MIN_GPHI=
7.2311913852263765e-02
```

which violates the acceptance floor

```math
g_\phi\ge0.1
```

It therefore cannot be promoted.

Even that unsafe point still did not reverse the finite payload.

### Source self-force residuals

Across the tested source families, the normalized Newtonian source self-force residual was approximately

```text
0.00189 to 0.00342
```

This is small compared with the coherent Newtonian field and does not explain the failed COM reversal.

---

# Result

The combined 014B-015C branch now supports the following hierarchy of statements.

## Positive results

```text
NONSTATIC_DISFORMAL_HIGH_SENSITIVITY_PREREQUISITE=
YES_IN_TESTED_BACKGROUNDS

ANTIPARALLEL_DISFORMAL_FIFTH_FORCE=
YES_IN_CONTROLLED_REDUCED_MODEL

WEAK_PERTURBATION_FORCE_ORDER_THEOREM=
PROVED_WITHIN_STATED_REGULAR_ASSUMPTIONS

LOCAL_TOTAL_FORCE_REVERSAL=
YES_IN_CONTROLLED_REDUCED_MODEL

LOCAL_TOTAL_FORCE_REVERSAL_2D_REFINEMENT=
PASS

LOCAL_TOTAL_FORCE_REVERSAL_3D_REFINEMENT=
PASS

LOCAL_TOTAL_FORCE_REVERSAL_TIMESTEP_HALVING=
PASS
```

## Negative or constraining results

```text
MINIMAL_CONSTANT_B_STANDARD_MODEL_BRIDGE=
REJECTED_IN_DECLARED_EFT_SCOPE

REQUIRED_CONSTANT_B_COUPLING_HIERARCHY=
3.4605562139399018e57

REQUIRED_ENVIRONMENTAL_DELTA_LN_B=
132.48877963228443

MINIMAL_ADDITIVE_SYMMETRY_PAIR_PORTAL_PROTECTION=
INSUFFICIENT

MINIMAL_SCALAR_PAIR_PORTAL_ONE_BODY_COUNTERTERM=
LOGARITHMICALLY_DIVERGENT_BY_POWER_COUNTING

FINITE_PASSIVE_PAYLOAD_COM_REVERSAL_AT_ROOT_TIME=
NOT_FOUND_IN_015C_TESTED_DOMAIN
```

## Practical status

```text
ORDINARY_BARYONIC_REALIZATION=
NOT_ESTABLISHED

GLOBAL_BODY_REPULSION=
NOT_ESTABLISHED

GLOBAL_CENTER_OF_MASS_LIFT=
NOT_ESTABLISHED

REACTIONLESS_PROPULSION=
NO_CLAIM

EXPERIMENTAL_REALIZATION=
NO

PRACTICAL_ANTIGRAVITY_DEVICE=
NO
```

---

# Verification

## Analytical

### 014B

The force-divergence sign criterion was reduced to

```math

\delta_d>1

```

for sign reversal when $\eta^2>0$ and $g_\phi>0$.

### 014C

The weak-perturbation theorem established

```math

\mathbf F_\phi=O(\epsilon^2)

```

```math

\mathbf F_\Psi=O(\epsilon)

```

and

```math

\frac{
|\mathbf F_\phi|
}{
|\mathbf F_\Psi|
}
=
O(\epsilon)

```

around a regular $\xi_0=0$ background.

### 014D

The local total-reversal condition was exactly reduced to

```math

-\mathbf F_\phi\cdot\mathbf F_\Psi
>
|\mathbf F_\Psi|^2

```

### 014E

The dimensionless/disformal-scale mapping was reconstructed as

```math

b_0
=
\frac{
H_0^2M_{\mathrm{Pl}}^2
}{
M_D^4
}

```

and therefore

```math

M_D
=
\sqrt{
H_0M_{\mathrm{Pl}}
}
b_0^{-1/4}

```

The constant-$B$ coupling hierarchy follows from

```math

\frac{
B_{\mathrm{operating}}
}{
B_{\mathrm{constrained}}
}
=
\left(
\frac{
M_{D,\mathrm{constrained}}
}{
M_{D,\mathrm{operating}}
}
\right)^4

```

The canonical-energy compactness radius follows from

```math

R_{\mathcal C=1}
=
\sqrt{
\frac{
3c^4
}{
8\pi G\rho_E
}
}

```

### 015A

The minimal additive-symmetry proof established

```math

q_\phi=0

```

whenever both

```math
\mu D^\dagger AB
```

and

```math
y\phi D^\dagger AB
```

are invariant under the same additive symmetry.

Therefore one-body operators proportional to $\phi A^\dagger A$ and $\phi B^\dagger B$ are not forbidden by that symmetry.

The scalar one-loop prototype has

```math

\omega=4L-2I=0

```

and is logarithmically divergent by superficial power counting.

### 015C

The physically relevant finite-payload observable was explicitly promoted from a pointwise criterion to

```math

\mathbf a_{\mathrm{CM}}
=
\frac{
\int
w(\mathbf x)
\left[
\mathbf F_\Psi+\mathbf F_\phi
\right]
dV
}{
\int
w(\mathbf x)dV
}

```

with outward reversal requiring

```math

\mathbf a_{\mathrm{CM}}\cdot\hat{\mathbf n}>0

```

No tested safe candidate satisfied this root-time finite-body criterion.

---

## Numerical

The repository regression baseline remained

```text
94 passed
```

The 014C result survived:

```text
2D:
48^2
72^2
96^2
128^2

3D:
24^3
32^3
40^3
```

The 014D result survived:

```text
2D:
64^2
96^2
128^2

3D:
24^3
32^3
40^3

TIMESTEP HALVING:
PASS
```

The 015A $Z_N$ enumeration found zero protected assignments through $N=64$.

The repaired 015C run completed all 12 root-time source/coupling discovery cases without finding a safe COM reversal.

---

## Dimensional

The 014E mapping explicitly distinguishes:

```text
b0
dimensionless reduced-model parameter
```

from

```text
B0
dimensionful constant-disformal coefficient
```

with

```math
B_0=M_D^{-4}
```

The compactness derivation uses energy density $\rho_E$ in ${\mathrm{J/m^3}}$ and converts to mass density through $\rho_E/c^2$ before inserting into the Schwarzschild compactness.

---

## Limiting cases

### Weak perturbations

014C proves that the fifth-force/Newtonian-force ratio vanishes in the regular $\epsilon\to0$ perturbative limit around the $\xi_0=0$ root.

### Disformal degeneracy

All promoted 014D results require a positive metric factor and use the explicit floor

```math
g_\phi\ge0.1
```

A reversal requiring $g_\phi$ below that floor is not accepted.

### Finite-payload limit

015C intentionally prevents the payload from becoming a source, so the test is a passive finite-body limit and not a closed-system propulsion model.

---

## Literature comparison

The 014B-014D branch was motivated by published non-static disformal-force behavior already recorded in the project notes.

This journal primarily preserves the project-derived analytical and numerical work.

The following remain necessary before stronger external claims:

1. independent reconstruction of the precise published-model normalization used by 014B-014D;
2. updated direct comparison of the 014E operator normalization against current collider and local-gravity bounds;
3. literature search for finite-body disformal force calculations using localized sources;
4. literature search for technically natural pair-specific or emergently sequestered scalar portals.

No new scientific-discovery claim should be made until those comparisons are complete.

---

# Falsification Attempt

The project deliberately attempted to destroy the promising disformal result at progressively stronger levels.

## 1. Could the effect require a singular/noninvertible disformal metric?

014B-014D tracked $g_\phi$.

The validated 014D calculations retained

```text
MIN_GPHI_VALIDATED_RUNS=
0.13850683595823443
```

above the declared floor of $0.1$.

This specific failure mode did not destroy 014D.

## 2. Could the force sign disappear under grid refinement?

No in the tested 014C/014D domains.

Both 2D and independent 3D refinements preserved the relevant local sign.

## 3. Could 014D be a time-step artifact?

Timestep halving changed the outward projection by only

```text
1.0299289263913065e-04
```

relative and preserved the reversal sign.

## 4. Could the local effect be too weak to overcome Newtonian gravity?

014C: yes.

014D: no locally.

014D found local cells where the full vector criterion reverses.

## 5. Could the operating coupling act directly on ordinary baryons through the minimal constant operator?

014E: not in the declared constant-$B$ EFT comparison.

The required coupling differs by approximately

```math
3.46\times10^{57}
```

from the stated constrained constant-coupling benchmark.

## 6. Could a simple additive symmetry protect a pair-only scalar portal?

015A: no for the minimal portal.

The same symmetry that permits both pair vertices forces $q_\phi=0$ and therefore permits the one-body density operators.

## 7. Could local reversed cells yield an outward force on an entire finite payload?

015C: not in the tested root-time localized-source domain.

This is the most important new falsification result after 014E.

The strongest safe finite-payload case canceled roughly $52.3\%$ of the inward Newtonian radial component but remained attractive overall.

---

# Claims Status

`CLAIMS.md` had not yet been synchronized with the live frontier when these calculations were performed.

This journal recommends the following durable claim records.

```text
CLAIM_ID=014B_DISFORMAL_XI0_PREREQUISITE
TYPE=PROJECT_DERIVED_REPRODUCTION
STATUS=SUPPORTED_IN_TESTED_BACKGROUNDS
```

```text
CLAIM_ID=014C_DISFORMAL_ANTIPARALLEL_FORCE
TYPE=PROJECT_DERIVED_NUMERICAL_RESULT
STATUS=SUPPORTED_WITHIN_TESTED_REDUCED_MODEL
```

```text
CLAIM_ID=014C_XI0_WEAK_PERTURBATION_SCALING
TYPE=PROJECT_DERIVED_ANALYTIC_RESULT
STATUS=PROVED_WITHIN_STATED_REGULAR_PERTURBATIVE_ASSUMPTIONS
```

```text
CLAIM_ID=014D_LOCAL_TOTAL_FORCE_REVERSAL
TYPE=PROJECT_DERIVED_NUMERICAL_RESULT
STATUS=SUPPORTED_WITH_GRID_AND_TIMESTEP_CONVERGENCE
```

```text
CLAIM_ID=014E_CONSTANT_B_BARYONIC_BRIDGE
TYPE=PROJECT_DERIVED_FEASIBILITY_BOUND
STATUS=REJECTED_IN_DECLARED_CONSTANT_OPERATOR_EFT_SCOPE
```

```text
CLAIM_ID=015A_MINIMAL_ADDITIVE_PAIR_PORTAL_PROTECTION
TYPE=PROJECT_DERIVED_ANALYTIC_AND_COMPUTATIONAL_UV_PREFLIGHT
STATUS=REJECTED_AS_SUFFICIENT_PROTECTION
```

```text
CLAIM_ID=015C_FINITE_PASSIVE_PAYLOAD_COM_REVERSAL
TYPE=PROJECT_DERIVED_NUMERICAL_NEGATIVE_RESULT
STATUS=NOT_FOUND_IN_TESTED_ROOT_TIME_LOCALIZED_SOURCE_DOMAIN
```

The following claims remain prohibited:

```text
GLOBAL_BODY_ANTIGRAVITY=ESTABLISHED
GLOBAL_CENTER_OF_MASS_LIFT=ESTABLISHED
ORDINARY_BARYONIC_DISFORMAL_ANTIGRAVITY=ESTABLISHED
REACTIONLESS_PROPULSION=ESTABLISHED
PRACTICAL_ANTIGRAVITY_DEVICE=ESTABLISHED
NEW_PHYSICS_DISCOVERY=ESTABLISHED
```

---

# Open Questions

## 1. Dynamic-time finite-payload gate

015C evaluated the finite-payload discovery criterion at the special root time.

014D is intrinsically time dependent.

Therefore the strongest immediate reopen condition is:

```math
\exists t:
\quad
\mathbf a_{\mathrm{CM}}(t)
\cdot
\hat{\mathbf n}
>
0
```

subject simultaneously to

```math
g_\phi(t,\mathbf x)\ge0.1
```

```math
K_{\mathrm{eff}}(t,\mathbf x)>0
```

and weak-field control.

A negative root-time result is therefore not yet a theorem against finite-payload reversal at other phases of the evolution.

## 2. Original-014D geometry finite-payload control

015C simultaneously changed both the density geometry and the observable.

A high-value control is:

```text
ORIGINAL VALIDATED 014D DENSITY
+
FINITE PASSIVE PAYLOAD INTEGRATION
```

This would distinguish:

```text
FINITE-BODY AVERAGING FAILURE
```

from

```text
LOCALIZATION/GEOMETRY FAILURE
```

## 3. Safe-coupling boundary

The finite-payload fifth-force cancellation grew strongly with $b_0$.

The $b_0=0.32$ cases approached the safety boundary but violated the $g_\phi\ge0.1$ floor.

The critical question is whether any physically controlled geometry/time choice produces

```math
a_{\mathrm{CM,out}}>0
```

**before** the metric-health boundary is crossed.

## 4. Environment-dependent or UV-complete disformal coupling

Any rescue of the direct baryonic branch must explain roughly

```math
\Delta\ln B
\gtrsim132.49
```

without:

- loss of EFT control;
- singular kinetic structure;
- unacceptable Standard-Model fifth forces;
- radiative instability;
- pathological propagation;
- removal of the 014D nonlinear reversal.

## 5. Structurally sequestered collective force

015A rules out ordinary additive symmetry as sufficient protection for the simplest relativistic pair portal.

Still logically open are:

- nontrivial pair representations;
- emergent/composite selection rules;
- partner/cancellation structures;
- derivative or topological couplings;
- nonperturbative protection;
- other structural sequestering mechanisms.

Each must be tested for actual one-body mixing and radiative stability rather than accepted by analogy.

## 6. 006D established-GR revisit

The immediate project plan is to revisit 006D before spending additional effort on this speculative branch.

The highest-value 006D revisit is not coefficient micro-optimization.

It is a microstandoff/realizability map exploiting

```math
M_{\mathrm{equiv}}
=
C\frac{ah^2}{G}
```

and hence

```math
M_{\mathrm{equiv}}\propto h^2
```

while tracking the opposing growth of local stress-energy density as the source is miniaturized.

If 006D fails to produce a physically nonempty microscopic window, the present journal defines the exact disformal/collective frontier from which to resume.

---

# AI Assistance

AI assistant used: ChatGPT by OpenAI

Substantial AI-assisted work in this research slice included:

- reconstruction of the non-static disformal prerequisite gate;
- derivation and checking of the 014C weak-perturbation force-order theorem;
- design of the 014D total-force reversal criterion;
- interpretation of the 014D convergence and health diagnostics;
- physical-scale reconstruction for 014E;
- derivation of the constant-$B$ coupling hierarchy;
- compactness estimate for the canonical kinetic compensation route;
- construction of the 015A additive-symmetry no-go preflight;
- design of the independent $Z_N$ enumeration;
- one-loop superficial-divergence analysis;
- 014D AST/API audit for 015B;
- construction of the 015C finite localized source / passive finite payload test;
- diagnosis and repair of the Python dynamic-module registration failure;
- interpretation of the repaired 015C negative finite-payload result;
- preparation of this durable journal record.

All AI-assisted results remain subject to independent human/scientific review.

No AI-generated result should be promoted to a new-physics discovery without independent verification and literature comparison.

---

# Next Action

## Immediate project priority

The project is temporarily returning to the stronger established-physics 006D construction.

The next 006D task should test whether microscopic stand-off and explicit field-realization constraints create any physically nonempty practical window.

Do **not** spend the next 006D run merely reducing

```math
C_{\mathrm{finite}}=23.591586299249
```

by a small percentage.

The important question is whether geometry miniaturization changes practical viability before stress-energy density, continuum validity, quantum-field constraints, curvature, or stability become fatal.

## Reopen condition for this journaled branch

If the 006D microstandoff/realizability branch does not reach a practical route, resume here.

The highest-value disformal continuation should be:

```text
DYNAMIC-TIME FINITE-PAYLOAD SEARCH
+
ORIGINAL-014D-GEOMETRY FINITE-PAYLOAD CONTROL
```

before inventing a more complicated UV theory.

That continuation should answer:

```math

\text{Does a safe finite-payload COM reversal exist anywhere in time
before the }g_\phi\text{ health boundary is crossed?}

```

If yes, freeze the source geometry, payload geometry, $b_0$, and normalized evaluation time and require 2D/3D refinement plus independent implementation.

If no, demote the direct disformal practical route and focus only on a structurally sequestered source-referenced collective force or return to established-GR realizability.

---

# Final Scientific State at Journal Close

```text
REGRESSION_BASELINE=
94_PASSED

014B_NONSTATIC_DISFORMAL_PREREQUISITE=
SUPPORTED

014C_ANTIPARALLEL_FIFTH_FORCE=
SUPPORTED_IN_CONTROLLED_REDUCED_MODEL

014C_WEAK_PERTURBATION_SCALING_THEOREM=
PROVED_WITHIN_STATED_ASSUMPTIONS

014D_LOCAL_TOTAL_FORCE_REVERSAL=
SUPPORTED_NUMERICALLY

014D_2D_REFINEMENT=
PASS

014D_3D_REFINEMENT=
PASS

014D_TIMESTEP_HALVING=
PASS

014E_MINIMAL_CONSTANT_B_BARYONIC_BRIDGE=
REJECTED_IN_DECLARED_SCOPE

014E_REQUIRED_COUPLING_HIERARCHY=
3.4605562139399018e57

014E_REQUIRED_DELTA_LN_B=
132.48877963228443

015A_SIMPLE_ADDITIVE_PAIR_PROTECTION=
INSUFFICIENT

015A_MINIMAL_SCALAR_ONE_BODY_COUNTERTERM=
LOGARITHMICALLY_DIVERGENT_BY_POWER_COUNTING

015B_014D_FINITE_PAYLOAD_API_AUDIT=
GREEN

015C_LOCALIZED_FINITE_SOURCE=
YES

015C_FINITE_PASSIVE_PAYLOAD=
YES

015C_ROOT_TIME_SAFE_COM_REVERSAL=
NOT_FOUND_IN_TESTED_DOMAIN

015C_STRONGEST_SAFE_OUTWARD_FIFTH_TO_NEWTONIAN_COMPONENT=
APPROX_0P523

014D_LOCAL_REVERSAL_RESULT=
PRESERVED

GLOBAL_BODY_REPULSION=
NOT_ESTABLISHED

GLOBAL_CENTER_OF_MASS_LIFT=
NOT_ESTABLISHED

ORDINARY_BARYONIC_REALIZATION=
NOT_ESTABLISHED

PRACTICAL_ANTIGRAVITY_DEVICE=
NO

NEW_PHYSICS_DISCOVERY=
NO
```
