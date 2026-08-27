# Antigravity Research

> For detailed running research notes, intermediate conclusions, assumptions,
> and next-step planning, see [`NOTES.md`](NOTES.md).
>
> Project formatting, GitHub math, code-header, and documentation standards:
> [`FORMATTING_AND_CODE_STANDARDS.md`](FORMATTING_AND_CODE_STANDARDS.md).
>
> Active research priorities, decision gates, and execution strategy:
> [`RESEARCH_BUILDPLAN.md`](RESEARCH_BUILDPLAN.md).

Mathematical and computational research into gravitational repulsion,
gravitational defocusing, reduced gravitational attraction, relativistic
stress-energy, quantum stress-energy, and related phenomena in general
relativity and neighboring theories.

The project begins with established physics, reproduces known solutions, and
then uses analytical and numerical methods to investigate the conditions under
which gravity can become locally repulsive.

The long-term question is:

> What physically consistent stress-energy configurations, spacetime
> geometries, quantum effects, or well-motivated extensions of gravitational
> theory can produce measurable gravitational repulsion or reduced attraction?

---

## Research Philosophy

- Start with established physics.
- Reproduce known results before exploring new ideas.
- Separate coordinate effects from measurable physical effects.
- Prefer operational or invariant quantities such as geodesic deviation,
  proper acceleration, curvature, and relative free-fall acceleration.
- Verify important results independently.
- Record assumptions explicitly.
- Test dimensional consistency and limiting cases.
- Record negative results and no-go results.
- Distinguish exact GR solutions from weak-field or idealized models.
- Distinguish mathematical possibility from physical realizability.
- Distinguish local repulsion from global repulsion.
- Distinguish a theoretical stress-energy construction from a practical device.
- Treat AI-generated mathematics and code as unverified until checked.
- Do not classify anything as a discovery without independent validation and
  literature comparison.

---

## Current Research Status

The project has established that **local gravitational repulsion is permitted
within established general relativity** and has reproduced several known
mechanisms computationally, including:

- cosmological-constant-driven geodesic defocusing;
- Schwarzschild-de Sitter / Kottler repulsive behavior;
- Reissner-Nordstrom gravitational repulsion;
- relativistic domain-wall gravitational repulsion.

The project has also constructed a stronger finite-source result within
**static linearized general relativity**:

> **A finite-radius, finite-thickness, nonsingular, positive-energy, locally
> conserved stress-energy configuration satisfying NEC, WEC, and DEC can
> produce a locally outward gravitational field while retaining positive
> far-field mass.**

This result is project-derived and belongs specifically to the linearized-GR
model used in Simulations 006B-006D. It is not yet an exact nonlinear GR
solution and does not establish a realizable material or practical device.

The recurring classical mechanism is:

> **Positive energy combined with sufficiently large relativistic negative
> pressure or tension can produce locally repulsive gravity.**

In a local rest frame, consider stress-energy of the approximate form

```math
T^\mu{}_{\nu}
=
\mathrm{diag}
\left(
\epsilon,
 p_x,
 p_y,
 p_z
\right)
```

In the static weak-field limit, the active gravitational source contains the
combination

```math
\epsilon+p_x+p_y+p_z
```

Ordinary matter generally satisfies

```math
|p_i|\ll\epsilon
```

and therefore behaves attractively.

Relativistic fields can instead have stresses comparable in magnitude to
their energy density. Sufficiently negative principal pressures can make the
local active gravitational contribution negative.

The current best classical static architecture is characterized using

```math
M_{\mathrm{equiv}}
=
C\frac{a h^2}{G}
```

with the best verified thin conserved architecture at

```math
C_{\mathrm{thin}}
=
23.426710175391
```

and the best tested finite-thickness regularization at

```math
C_{\mathrm{finite}}
=
23.591586299249
```

The finite-thickness value is approximately $0.704\%$ above the thin limit.

The classical static branch has therefore reached its current decision gate:
local repulsion, finite support, positive energy, pointwise classical energy
conditions, and local conservation have been demonstrated within the
linearized model, but no known material realization, dynamical stability,
energetic plausibility, experimental accessibility, or practical device has
been established.

The active research frontier is now the **established-quantum-physics gate**,
beginning with a complete Casimir apparatus benchmark and then quantum energy
inequality bounds.

---

## Important Terminology

### Local gravitational repulsion

A nearby freely falling neutral object experiences acceleration away from a
source region.

This is known to occur in general relativity and has been reproduced in this
repository.

```text
PROJECT_STATUS=YES
```

### Global gravitational repulsion

The asymptotic gravitational field of an isolated source points outward.

This has **not** been established for a conventional positive-mass isolated
system in this project.

```text
PROJECT_STATUS=NO
```

The finite 005B/006D architectures retain an attractive positive-mass far
field.

### Practical antigravity

A finite, controllable, stable apparatus produces useful gravitational
repulsion at physically realizable energy and material scales.

This has **not** been established.

```text
PROJECT_STATUS=NO
```

---

# Research Program

## Research 001A — Schwarzschild-de Sitter Baseline

The first calculation reproduced the weak-field Kottler acceleration:

```math
a(r)
=
-\frac{GM}{r^2}
+
\frac{\Lambda c^2 r}{3}
```

The static radius is

```math
r_{\mathrm{static}}
=
\left(
\frac{3GM}{\Lambda c^2}
\right)^{1/3}
```

The observed positive cosmological constant therefore produces genuine
outward gravitational behavior at sufficiently large distances.

However, the observed value of $\Lambda$ is far too small to be useful at
laboratory scales.

Files:

```text
src/antigravity_research/geometry/kottler.py
tests/known_solutions/test_kottler.py
simulations/001_kottler_weak_field.py
```

---

## Research 001B — Geodesic Deviation

Because coordinate acceleration can be misleading in general relativity, the
Kottler result was checked using free-fall tidal eigenvalues.

For Schwarzschild-de Sitter spacetime:

```math
\lambda_r
=
\frac{2GM}{r^3}
+
\frac{\Lambda c^2}{3}
```

and

```math
\lambda_t
=
-\frac{GM}{r^3}
+
\frac{\Lambda c^2}{3}
```

The calculation reproduced the region in which all spatial directions
experience geodesic stretching.

This confirms that the cosmological repulsive effect is physical rather than
merely a coordinate artifact.

Files:

```text
src/antigravity_research/geometry/kottler_tidal.py
tests/known_solutions/test_kottler_tidal.py
simulations/001b_kottler_tidal_eigenvalues.py
```

---

## Research 002 — Stress-Energy Required for Defocusing

For an ideal homogeneous and isotropic perfect fluid:

```math
\frac{\ddot{\xi}}{\xi}
=
-\frac{4\pi G}{3c^2}
\left(
\epsilon+3p
\right)
+
\frac{\Lambda c^2}{3}
```

For an equation of state

```math
p=w\epsilon
```

positive-energy defocusing becomes possible when

```math
w<-\frac{1}{3}
```

A particularly important case is

```math
w=-1
```

for which

```math
p=-\epsilon
```

This produces repulsive geodesic behavior with positive energy while
satisfying NEC, WEC, and DEC and violating the strong energy condition.

This established an important project result:

> **Negative energy is not required for the sign of local gravitational
> repulsion.**

Files:

```text
src/antigravity_research/geometry/perfect_fluid_defocusing.py
tests/known_solutions/test_perfect_fluid_defocusing.py
simulations/002_required_stress_energy.py
```

---

## Research 003A — Finite Vacuum-Energy Localization

The project next investigated whether a finite $w=-1$ region could simply be
localized inside ordinary vacuum.

For pure vacuum-like stress,

```math
p=-\epsilon
```

stress-energy conservation gives a vanishing pressure gradient.

The calculation therefore found that a pure $w=-1$ region cannot smoothly
taper from finite energy density to vacuum while retaining the same equation
of state.

A de Sitter interior and Schwarzschild exterior can match their metric value
at the boundary while failing to match the required derivative structure.

A boundary stress layer is therefore required.

Files:

```text
src/antigravity_research/geometry/vacuum_energy_core.py
tests/known_solutions/test_vacuum_energy_core.py
simulations/003a_finite_vacuum_energy_core.py
```

---

## Research 003B — Israel Thin-Shell Search

The boundary was then modeled using the Israel junction conditions.

The search varied the exterior Schwarzschild ADM mass and calculated the
required shell surface energy and pressure.

A repulsive Schwarzschild exterior requires negative ADM mass.

Within the tested de Sitter-core construction, obtaining such an exterior
required negative shell surface energy and violation of WEC and DEC.

A small negative-mass interval could retain NEC, but the ordinary positive
energy conditions did not survive.

This branch is therefore currently considered a mathematical exotic-matter
route rather than a promising practical mechanism.

Files:

```text
src/antigravity_research/geometry/israel_shell.py
tests/known_solutions/test_israel_shell.py
simulations/003b_israel_shell_mass_search.py
```

---

## Research 004A — Einstein-Maxwell / Reissner-Nordstrom Repulsion

The exact Reissner-Nordstrom exterior is

```math
f(r)
=
1
-
\frac{2GM}{c^2r}
+
\frac{GQ^2}{4\pi\epsilon_0c^4r^2}
```

For neutral matter, the gravitational tendency changes sign at

```math
r_{\mathrm{rep}}
=
\frac{Q^2}{4\pi\epsilon_0Mc^2}
```

The repository reproduced a region in which:

- ADM mass is positive;
- electromagnetic energy is positive;
- shell surface energy is nonnegative;
- shell NEC, WEC, and DEC can hold;
- neutral matter nevertheless experiences outward gravitational behavior.

This demonstrates that positive-energy local gravitational repulsion can occur
in an exact solution of ordinary Einstein-Maxwell theory.

The physical problem is the required electrical field strength. Useful
macroscopic acceleration requires enormous charge and fields that rapidly
approach or exceed fundamental quantum-electrodynamic limits.

The Einstein-Maxwell solution is therefore retained as an important
proof-of-principle rather than the leading engineering candidate.

Files:

```text
src/antigravity_research/geometry/reissner_nordstrom.py
tests/known_solutions/test_reissner_nordstrom.py
simulations/004a_einstein_maxwell_repulsion.py
```

---

## Research 005A — Relativistic Tension and Domain Walls

The Einstein-Maxwell result suggested a more general principle:

> **The important ingredient is not electric charge itself, but relativistic
> stress.**

For an ideal membrane with surface energy density $U$ and tangential tension

```math
\tau=qU
```

the planar gravitational field becomes repulsive when

```math
q>\frac{1}{2}
```

The dominant energy condition permits

```math
q\le1
```

Therefore the interval

```math
q\in\left(\frac{1}{2},1\right]
```

contains positive-energy, NEC/WEC/DEC-compatible repulsive stress-energy.

The most efficient member of this membrane class is

```math
q=1
```

corresponding to ideal relativistic domain-wall stress.

This gives the classical design principle:

> **Maximize relativistic tangential tension per unit positive energy.**

Files:

```text
src/antigravity_research/geometry/relativistic_wall.py
tests/known_solutions/test_relativistic_wall.py
simulations/005a_relativistic_tension_wall.py
```

---

## Research 005B — Finite Supported Relativistic-Tension Source

An infinite domain wall is not a device.

The next model therefore used:

```text
finite circular relativistic-tension membrane
+
minimum-energy DEC-compatible compressive support rim
```

The result was:

```text
FINITE_LOCAL_GRAVITATIONAL_REPULSION=YES
FINITE_SOURCE_TOTAL_ENERGY_POSITIVE=YES
COMPONENT_NEC_WEC_DEC_COMPATIBLE=YES
VON_LAUE_STRESS_BALANCE=YES
TOTAL_ACTIVE_MASS_POSITIVE=YES
LOCAL_FIELD_DIRECTION_NEAR_WALL=REPULSIVE
FAR_FIELD_DIRECTION=ATTRACTIVE
```

The optimal member of this architecture was again

```math
q=1
```

The optimized geometry was approximately

```math
\frac{R}{h}
\approx
4.00614967
```

with the repulsive region extending to approximately

```math
\frac{z_{\mathrm{zero}}}{R}
\approx
0.393319893
```

For this particular disk-plus-rim architecture,

```math
M_{\mathrm{equiv}}
\approx
79.753148\frac{a h^2}{G}
```

This is a model-specific result, not a universal lower bound.

For $1g$ at a one-meter stand-off, the required energy-equivalent mass is
approximately

```math
M_{\mathrm{equiv}}
\approx
1.17\times10^{13}\ \mathrm{kg}
```

This demonstrates a finite positive-energy **local** antigravity-like field in
the linearized model, but not a practical apparatus.

Simulation 006C later independently reproduced the field, zero crossing,
optimum geometry, and coefficient to high numerical precision.

Files:

```text
src/antigravity_research/geometry/finite_tension_disk.py
tests/known_solutions/test_finite_tension_disk.py
simulations/005b_finite_supported_antigravity.py
```

---

## Research 006A — Static DEC Energy Lower-Bound Search

Simulation 006A asked how much of the enormous 005B energy cost might be
fundamental and how much might come from inefficient source geometry.

For type-I matter satisfying the dominant energy condition:

```math
|p_i|\le\epsilon
```

Therefore the static active source satisfies

```math
\epsilon+p_x+p_y+p_z
\ge
-2\epsilon
```

The maximally negative local source permitted by this condition is

```math
p_x=p_y=p_z=-\epsilon
```

A linear-program optimization was then performed using:

- positive energy;
- type-I DEC;
- negative active gravitational source;
- integrated static stress balance.

The optimizer returned:

```text
GENERAL_MIN_ENERGY_COEFFICIENT=1.000000
DOMAIN_WALL_MIN_ENERGY_COEFFICIENT=2.000000
005B_DISK_MASS_COEFFICIENT=79.753148
```

This suggested the optimistic scaling

```math
M_{\mathrm{equiv}}
\sim
\frac{a h^2}{G}
```

with the important dependence

```math
M,E\propto h^2
```

The coefficient $C=1$ is an optimistic abstract result inside the model that
was optimized. It is **not** established as a universal lower bound in general
relativity because 006A imposed integrated stress balance rather than a fully
spatially resolved, locally conserved source.

Files:

```text
src/antigravity_research/geometry/energy_bounds.py
tests/known_solutions/test_energy_bounds.py
simulations/006a_static_dec_lower_bound.py
```

---

## Research 006B — Geometry-Aware Conserved DEC Optimization

**Status: complete at the classical decision level.**

Simulation 006B replaced the abstract 006A stress accounting with explicit
axisymmetric spatial geometry, actual gravitational kernels, pointwise
positive energy, pointwise DEC, and local stress conservation.

For a static axisymmetric thin source without shear, local radial conservation
requires

```math
\frac{dp_r}{dr}
+
\frac{p_r-p_\phi}{r}
=
0
```

or equivalently

```math
\frac{d(rp_r)}{dr}
=
p_\phi
```

An efficient piecewise conserved architecture was found and independently
checked with a discretized radial linear program.

The optimized dimensionless radii are

```math
\alpha
=
\frac{a}{h}
=
1.437500564637
```

and

```math
\beta
=
\frac{R}{h}
=
4.701437405300
```

with coefficient

```math
C_{\mathrm{006B,thin}}
=
23.426710175391
```

This improves the 005B disk/rim value by approximately

```math
\frac{79.753148116012}{23.426710175391}
\approx
3.40437
```

A separate radial LP converged toward the same closed-form value:

```text
N=50   C=23.279848767693
N=100  C=23.390094671093
N=200  C=23.417573464368
N=400  C=23.424535334824
N=800  C=23.426231369342
```

A more general staggered finite-volume $r$-$z$ optimizer was then built with
exact cell force balance and exact type-I DEC imposed through second-order-cone
constraints on stress eigenvalues.

Finite-grid $r$-$z$ results initially appeared much more expensive, but radial
and especially vertical refinement showed that a substantial part of the gap
was discretization error. Combined continuum diagnostics bracketed the thin
coefficient:

```text
DEPTH8_CONTINUUM_BRACKET=22.949343418307,24.570375590694
DEPTH_AND_GRID_EXTRAPOLATED_BRACKET=22.554042171855,24.175074344242
THIN_REFERENCE_C=23.426710175391
```

The correct conclusion is therefore:

```text
FULL_RZ_CONTINUUM_EVIDENCE=CONSISTENT_WITH_THIN_REFERENCE
VERIFIED_FULL_RZ_IMPROVEMENT_BELOW_THIN=NO
VERIFIED_FINITE_2D_PENALTY_ABOVE_THIN=NO
C_1_TO_5_ROUTE_FOUND=NO
GLOBAL_FULL_RZ_OPTIMUM=NOT_ESTABLISHED
```

Simulation 006B falsified the idea that 005B was near-optimal within the
restricted locally conserved thin class, but it did **not** establish
$C=23.426710175391$ as a universal lower bound of GR.

Files:

```text
src/antigravity_research/geometry/axisymmetric_thin_stress.py
tests/known_solutions/test_axisymmetric_thin_stress.py
simulations/006b_geometry_aware_dec_optimizer.py
simulations/006b_full_rz_decision.py
```

Primary generated outputs:

```text
results/data/006b_geometry_aware_dec_optimizer.csv
results/figures/006b_geometry_aware_dec_convergence.png
results/logs/006b_geometry_aware_dec_optimizer.log
results/data/006b_full_rz_decision.csv
results/logs/006b_full_rz_decision.log
```

---

## Research 006C — Independent Verification of the Finite Disk

**Status: complete and green.**

Simulation 006C independently reconstructed the 005B gravitational field by
numerically integrating the complete membrane-plus-support stress-energy
through the linearized gravitational Green function.

The primary independent calculation does not reuse the 005B analytic field
formula.

Field-grid comparison:

```text
COMPARISON_POINT_COUNT=30
MAX_ABSOLUTE_FIELD_ERROR=2.220446049250e-16
MAX_RELATIVE_FIELD_ERROR=1.419475206905e-15
FIELD_GRID_MATCH=PASS
```

Independent repulsive zero:

```math
\frac{z_{\mathrm{zero}}}{R}
=
0.393319893190334
```

Reference value:

```math
\frac{z_{\mathrm{zero}}}{R}
=
0.393319893190329
```

Independent optimized geometry:

```math
\frac{R}{h}
=
4.006149730747969
```

Independent coefficient:

```math
C_{\mathrm{005B}}
=
79.753148116012255
```

Reference coefficient:

```math
C_{\mathrm{005B,reference}}
=
79.753148116011999
```

Final classification:

```text
FIELD_GRID_VERIFIED=YES
REPULSIVE_ZERO_VERIFIED=YES
005B_OPTIMUM_VERIFIED=YES
SIMULATION_006C=GREEN
CLAIM_CLASSIFICATION=INDEPENDENT_NUMERICAL_VERIFICATION
```

This materially upgrades confidence in the 005B result and removes reuse of a
single analytic field implementation as a central validation weakness.

Files:

```text
simulations/006c_independent_finite_disk_field.py
results/data/006c_independent_finite_disk_field.csv
results/logs/006c_independent_finite_disk_field.log
```

---

## Research 006D — Finite-Thickness Locally Conserved Source

**Status: complete and green at the linearized-GR model level.**

Simulation 006D replaced the ideal zero-thickness source and singular support
ring with a finite-thickness source and finite radial support collar.

Define

```math
q(r)=r p_r(r)
```

and impose

```math
p_\phi(r)
=
\frac{dq}{dr}
```

with

```math
p_z=0
```

and

```math
T_{rz}=0
```

Then the static cylindrical radial conservation equation

```math
\frac{dp_r}{dr}
+
\frac{p_r-p_\phi}{r}
=
0
```

is satisfied by construction.

The in-plane source is multiplied by a smooth, compact, nonnegative vertical
profile of finite thickness. The energy density is chosen as

```math
\epsilon
=
\max\left(
|p_r|,
|p_\phi|
\right)
```

which enforces the static type-I dominant energy condition pointwise for the
constructed stress tensor.

Independent numerical checks gave:

```text
MAX_CONTROL_VOLUME_CONSERVATION_RESIDUAL=3.103073353827e-14
MAX_DEC_VIOLATION=0.000000000000e+00
MIN_NEC_MARGIN=0.000000000000e+00
MAX_INTEGRATED_STRESS_TRACE=2.922107000813e-13
LOCAL_CONSERVATION=PASS
NEC=PASS
WEC=PASS
DEC=PASS
LAUE_STRESS_BALANCE=PASS
```

Finite-thickness convergence was:

```text
scale=0.40000  C=38.037638025730
scale=0.20000  C=29.559369544823
scale=0.10000  C=26.258214373557
scale=0.05000  C=24.789414887263
scale=0.02500  C=24.095429926871
scale=0.01250  C=23.757986246352
scale=0.00625  C=23.591586299249
```

against the independently established thin reference

```math
C_{\mathrm{thin}}
=
23.426710175391
```

The finest tested finite source differs from the thin value by approximately
$0.704\%$ and approaches it monotonically as the regularization scale is
reduced.

Final classification:

```text
FINITE_SPATIAL_SUPPORT=YES
FINITE_THICKNESS=YES
SINGULAR_OUTER_RING=NO
FINITE_RADIAL_SUPPORT_COLLAR=YES
POINTWISE_POSITIVE_ENERGY=YES
POINTWISE_NEC_WEC_DEC=YES
LOCAL_CONSERVATION_LINEARIZED_ORDER=YES
OUTWARD_GRAVITATIONAL_FIELD=YES
POSITIVE_FAR_FIELD_ACTIVE_MASS=YES
FINITE_THICKNESS_STRESS_ENERGY_CONFIGURATION=YES
C_FINITE_BEST_TESTED=23.591586299249
C_THIN_LIMIT=23.426710175391
SIMULATION_006D=GREEN
CLAIM_CLASSIFICATION=CONSTRUCTIVE_LINEARIZED_GR_STRESS_ENERGY_RESULT
```

The following remain explicitly unestablished:

```text
EXACT_NONLINEAR_GR_CONSERVATION=NOT_ESTABLISHED
DYNAMIC_STABILITY=NOT_ESTABLISHED
KNOWN_MATERIAL_REALIZATION=NO
PRACTICAL_ANTIGRAVITY_DEVICE=NO
```

Files:

```text
simulations/006d_finite_thickness_conserved_source.py
results/data/006d_finite_thickness_conserved_source.csv
results/logs/006d_finite_thickness_conserved_source.log
```

---

# Classical-GR Decision Gate

Simulations 006B, 006C, and 006D have now answered the principal classical
static questions that motivated this phase.

Current status:

```text
LOCAL_GRAVITATIONAL_REPULSION_IN_LINEARIZED_GR=YES
POSITIVE_ENERGY_SOURCE=YES
FINITE_RADIUS_SOURCE=YES
FINITE_THICKNESS_SOURCE=YES
LOCAL_CONSERVATION_LINEARIZED_ORDER=YES
NEC=PASS
WEC=PASS
DEC=PASS
POSITIVE_FAR_FIELD_MASS=YES

BEST_VERIFIED_THIN_COEFFICIENT=23.426710175391
BEST_TESTED_FINITE_THICKNESS_COEFFICIENT=23.591586299249

EXACT_NONLINEAR_GR_SOLUTION=NOT_ESTABLISHED
DYNAMIC_STABILITY=NOT_ESTABLISHED
KNOWN_MATERIAL_REALIZATION=NO
ENERGETIC_PLAUSIBILITY=NO
EXPERIMENTAL_ACCESSIBILITY=NO
PRACTICAL_ANTIGRAVITY_DEVICE=NO
```

The best mature classical results remain in the approximate regime
$C\sim20$-$25$, not $C\sim1$-$5$.

At human scales, the underlying scaling remains severe. Even the abstract
coefficient $C=1$ would require

```math
M
\sim
\frac{a h^2}{G}
```

which for $a=1g$ and $h=1\ \mathrm{m}$ is approximately

```math
M
\approx
1.47\times10^{11}\ \mathrm{kg}
```

The classical static branch is therefore preserved as a strong theoretical
reference result, but further order-unity coefficient tuning is deprioritized
unless a specific physically motivated matter or field model makes it
worthwhile.

---

# Current Research Frontier

The highest-priority question is no longer whether a finite, positive-energy,
locally conserved linearized-GR stress-energy distribution can produce local
repulsion. Simulation 006D answers that question constructively within its
stated approximation.

The new frontier is:

> **Can any physically motivated matter, quantum field, or dynamical mechanism
> realize or outperform the required stress-energy while avoiding the severe
> $a h^2/G$ energy scale?**

The active next branch is established quantum field theory.

---

# Planned Research

## Research 007A — Complete Casimir Benchmark

**Next active experiment.**

Do not count only the negative vacuum-energy region. The complete model must
include:

- Casimir-region stress-energy;
- conducting plates;
- supports required for static equilibrium;
- total apparatus energy;
- total apparatus stress-energy;
- local gravitational field;
- far-field mass.

Primary outputs should include:

```text
vacuum energy density
principal stresses
active gravitational density
plate/support energy
total apparatus mass
local gravitational acceleration
far-field mass
dependence on plate separation
energy-condition behavior of the complete apparatus
```

A useful initial separation scan is:

```text
1 mm
100 micrometers
10 micrometers
1 micrometer
100 nm
10 nm
1 nm
```

The purpose is to determine quantitatively whether complete-apparatus quantum
stress-energy can materially outperform the classical static branch.

---

## Research 007B — Quantum Energy Inequality Bound

After 007A, quantify the negative-energy magnitude/duration restrictions from
established quantum field theory.

For spatial scale $h$ and sampling duration $\tau$, the target output is a
bound or benchmark of the form

```math
a_{\max}(h,\tau)
```

The purpose is to determine whether allowed quantum negative energy can ever
produce useful gravitational acceleration at experimentally accessible
scales.

If the answer is decisively negative, close or strongly deprioritize the
quantum-vacuum branch rather than adding unnecessary model complexity.

---

## Research 007C — Dynamic Sources

Only pursue this branch after the cheaper 007A/007B gates unless a new
analytical argument changes the priority.

Candidate systems include:

- scalar-field pulses;
- moving domain walls;
- oscillating anisotropic stresses;
- transient field configurations;
- retarded gravitational response.

The decisive question is:

> Can dynamics improve the **parametric scaling** of useful gravitational
> repulsion rather than merely change an order-unity coefficient?

If dynamics only changes $C$ by a factor of order unity while preserving the
same basic energy scaling, deprioritize the branch.

---

## Research 008 — Modified Gravity

Modified gravitational theories remain deferred until the established-GR and
established-QFT parameter spaces have been quantitatively constrained.

Possible later candidates include:

- scalar-tensor gravity;
- $f(R)$ gravity;
- vector-tensor models;
- Horndeski-type theories;
- massive gravity;
- other well-defined and observationally constrained extensions.

A modified theory producing repulsion is not by itself considered evidence for
a new physical effect. Any candidate must be independently motivated and
filtered by theoretical consistency, stability, solar-system constraints,
gravity-wave constraints, cosmology, and other relevant observations.

---

# Current Claims Ledger

## Known Results Reproduced

- Positive cosmological constant produces geodesic defocusing.
- Kottler spacetime contains an attraction/repulsion transition.
- Reissner-Nordstrom spacetime can produce local neutral-particle
  gravitational repulsion.
- Relativistic domain-wall stress can produce gravitational repulsion.

## Project-Derived Results Supported by Current Calculations

- Positive energy does not forbid local gravitational repulsion.
- Negative ADM mass is not required for local gravitational repulsion.
- Relativistically negative pressure/tension is a recurring mechanism for
  gravitational repulsion.
- The 005B finite supported tension disk has a repulsive near field, positive
  total energy, positive far-field mass, and independently verified coefficient
  $C_{005B}\approx79.753148116012$ within its linearized model.
- The 006B locally conserved thin radial architecture reduces the coefficient
  to $C_{\mathrm{thin}}=23.426710175391$ within its restricted optimization
  class.
- Full $r$-$z$ continuum diagnostics are consistent with the 006B thin
  reference; no verified lower full-2D coefficient has been established.
- Simulation 006D constructs a finite-radius, finite-thickness, nonsingular,
  positive-energy, locally conserved linearized-GR stress-energy distribution
  satisfying NEC/WEC/DEC and producing a local outward gravitational field.
- The best tested finite-thickness coefficient is
  $C_{\mathrm{finite}}=23.591586299249$.
- The static positive-energy mechanisms studied so far retain the basic energy
  scaling $M\sim C a h^2/G$.

## Not Established

- A universal proof that $C=23.426710175391$ or $C=1$ is the absolute lower
  bound in full general relativity.
- A self-consistent exact nonlinear-GR realization of the 006D source.
- Dynamical stability of the finite stress-energy architecture.
- A known laboratory material or field configuration capable of sustaining
  the required relativistic stress.
- Energetically plausible human-scale antigravity.
- Experimentally accessible antigravity from the project-derived source.
- Global positive-mass antigravity.
- A practical antigravity device.
- Novel physics.

---

# Running the Research

Activate the repository environment from the project root:

```bash
ROOT="$(pwd)"
PY="$ROOT/.venv/bin/python"
export PYTHONPATH="$ROOT/src"
```

Run the complete known-solution test suite:

```bash
"$PY" -m pytest -q tests/known_solutions
```

The current observed regression baseline after 006D is:

```text
72 passed
```

Run the existing simulations:

```bash
"$PY" simulations/001_kottler_weak_field.py
"$PY" simulations/001b_kottler_tidal_eigenvalues.py
"$PY" simulations/002_required_stress_energy.py
"$PY" simulations/003a_finite_vacuum_energy_core.py
"$PY" simulations/003b_israel_shell_mass_search.py
"$PY" simulations/004a_einstein_maxwell_repulsion.py
"$PY" simulations/005a_relativistic_tension_wall.py
"$PY" simulations/005b_finite_supported_antigravity.py
"$PY" simulations/006a_static_dec_lower_bound.py
"$PY" simulations/006b_geometry_aware_dec_optimizer.py
"$PY" simulations/006b_full_rz_decision.py
"$PY" simulations/006c_independent_finite_disk_field.py
"$PY" simulations/006d_finite_thickness_conserved_source.py
```

Simulation output should be preserved in `results/logs/` whenever possible.

Generated numerical data is stored under:

```text
results/data/
```

Generated figures are stored under:

```text
results/figures/
```

---

# Scientific Classification

Results in this repository should use categories such as:

```text
KNOWN_RESULT
REPRODUCED
NUMERICAL_OBSERVATION
NUMERICAL_OPTIMIZATION_RESULT
INDEPENDENT_NUMERICAL_VERIFICATION
CONSTRUCTIVE_LINEARIZED_GR_STRESS_ENERGY_RESULT
CONJECTURE
NOVEL_CANDIDATE
REJECTED
```

A result should not be promoted to `NOVEL_CANDIDATE` merely because it has not
yet been found in the project's literature search.

Independent mathematical verification and literature review are required.

---

## AI-Assisted Research

Antigravity Research is a human-directed research project by **Stevan White**
that uses **ChatGPT by OpenAI** as an AI research and development assistant.

ChatGPT assists with:

- mathematical derivations;
- Python development;
- simulation design;
- debugging;
- numerical analysis;
- literature-search assistance;
- documentation;
- hypothesis generation;
- falsification efforts.

AI-generated material is not assumed to be correct.

Important results are subject to analytical, numerical, dimensional,
literature, and other independent verification.

Use of ChatGPT does not imply endorsement or sponsorship by OpenAI.

See [`AI_ASSISTANCE.md`](AI_ASSISTANCE.md) for the complete disclosure.

---

## Licensing

Antigravity Research uses separate licenses for software and research
materials.

- **Software:** MIT OR Apache-2.0, at the user's option.
- **Original research materials, generated data, and original figures:**
  CC0 1.0 Universal.

See [`LICENSE.md`](LICENSE.md) for the complete licensing policy and the
`LICENSES/` directory for the full license texts.

Third-party materials retain their original copyright and licensing terms.

---

## Current Project Direction

The current working interpretation is:

> **Local gravitational repulsion in established GR is possible in theory,
> but the practical problem is dominated by stress-energy realizability,
> stability, and energy scale.**

The static classical branch has progressed from a finite disk coefficient of
$C\approx79.753148$ to a locally conserved optimized thin architecture with
$C\approx23.426710$, followed by a finite-thickness regularization with
$C\approx23.591586$.

That is a substantial theoretical improvement, but it does not solve the
underlying engineering problem because the basic scaling remains

```math
M_{\mathrm{equiv}}
\sim
C\frac{a h^2}{G}
```

The immediate next objective is therefore **Simulation 007A: a complete
Casimir apparatus benchmark**, followed by **Simulation 007B: quantum energy
inequality bounds**. The goal is to determine quickly whether established
quantum physics offers a route that materially outperforms the classical
static stress-energy scaling before considering more speculative extensions of
gravity.
