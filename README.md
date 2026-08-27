# Antigravity Research

> For detailed running research notes, intermediate conclusions, assumptions,
> and next-step planning, see [`NOTES.md`](NOTES.md).

> Project formatting, GitHub math, code-header, and documentation standards:
> [`FORMATTING_AND_CODE_STANDARDS.md`](FORMATTING_AND_CODE_STANDARDS.md).

> Active research priorities, decision gates, and execution strategy:
> [`RESEARCH_BUILDPLAN.md`](RESEARCH_BUILDPLAN.md).

Mathematical and computational research into gravitational repulsion,
gravitational defocusing, reduced gravitational attraction, relativistic
stress-energy, and related phenomena in general relativity and neighboring
theories.

The project begins with established physics, reproduces known solutions, and
then uses analytical and numerical methods to investigate the conditions under
which gravity can become locally repulsive.

The long-term question is:

> What physically consistent stress-energy configurations, spacetime
> geometries, or extensions of gravitational theory can produce measurable
> gravitational repulsion or reduced attraction?

---

## Research Philosophy

- Start with established physics.
- Reproduce known results before exploring new ideas.
- Separate coordinate effects from measurable physical effects.
- Prefer operational or invariant quantities such as geodesic deviation,
  proper acceleration, curvature, and relative free-fall acceleration.
- Verify important results independently.
- Record assumptions explicitly.
- Record negative results and no-go results.
- Distinguish exact GR solutions from weak-field or idealized models.
- Distinguish mathematical possibility from physical realizability.
- Treat AI-generated mathematics and code as unverified until checked.
- Do not classify anything as a discovery without independent validation.

---

## Current Research Status

The project has established that **local gravitational repulsion is permitted
within ordinary general relativity**.

Several known mechanisms have been reproduced computationally, including:

- cosmological-constant-driven geodesic defocusing;
- Schwarzschild-de Sitter / Kottler repulsive behavior;
- Reissner-Nordstrom gravitational repulsion;
- relativistic domain-wall gravitational repulsion.

The current results indicate that negative mass or negative energy is **not
intrinsically required for local gravitational repulsion**.

Instead, the recurring mechanism is:

> **Positive energy combined with sufficiently large relativistic negative
> pressure or tension can produce locally repulsive gravity.**

In a local rest frame, consider stress-energy of the approximate form

```math
T^\mu{}_\nu =
\operatorname{diag}
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
\epsilon + p_x + p_y + p_z
```

Ordinary matter generally satisfies

```math
|p_i| \ll \epsilon
```

and therefore behaves attractively.

Relativistic fields can instead have stresses comparable in magnitude to
their energy density. Sufficiently negative principal pressures can make the
local active gravitational contribution negative.

This makes the project increasingly a problem of **relativistic stress-energy
engineering** rather than a search for literal negative mass.

---

## Important Terminology

### Local gravitational repulsion

A nearby freely falling neutral object experiences acceleration away from a
source region.

This is known to occur in general relativity and has been reproduced in this
repository.

### Global gravitational repulsion

The asymptotic gravitational field of an isolated source points outward.

This has **not** been established for a conventional positive-mass isolated
system.

### Practical antigravity

A finite, controllable, stable apparatus produces useful gravitational
repulsion at physically realizable energy and material scales.

This has **not** been established.

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

This was an important change in direction.

The exact Reissner-Nordstrom exterior is

```math
f(r)
=
1
-
\frac{2GM}{c^2r}
+
\frac{GQ^2}
{4\pi\epsilon_0c^4r^2}
```

For neutral matter, the gravitational tendency changes sign at

```math
r_{\mathrm{rep}}
=
\frac{Q^2}
{4\pi\epsilon_0Mc^2}
```

The repository reproduced a region in which:

- ADM mass is positive;
- electromagnetic energy is positive;
- shell surface energy is nonnegative;
- shell NEC, WEC, and DEC can hold;
- neutral matter nevertheless experiences outward gravitational behavior.

This demonstrates that positive-energy local gravitational repulsion can
occur in an exact solution of ordinary Einstein-Maxwell theory.

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
\boxed{
\frac{1}{2}<q\le1
}
```

contains positive-energy, NEC/WEC/DEC-compatible repulsive stress-energy.

The most efficient member of this membrane class is

```math
q=1
```

corresponding to ideal relativistic domain-wall stress.

This gives the current classical design principle:

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
4.00615
```

with the repulsive region extending to approximately

```math
\frac{z}{R}
\approx
0.393320
```

For this particular disk-plus-rim architecture,

```math
M_{\mathrm{equiv}}
\approx
79.7531
\frac{ah^2}{G}
```

This is a model-specific result, not a universal lower bound.

For $1g$ at a one-meter stand-off, the required energy-equivalent mass is
approximately

```math
M_{\mathrm{equiv}}
\approx
1.17\times10^{13}\ \mathrm{kg}
```

This demonstrates a finite positive-energy **local** antigravity field in the
linearized model, but not a practical apparatus.

Files:

```text
src/antigravity_research/geometry/finite_tension_disk.py
tests/known_solutions/test_finite_tension_disk.py
simulations/005b_finite_supported_antigravity.py
```

---

## Research 006A — Static DEC Energy Lower-Bound Search

The current frontier is determining how much of the enormous energy cost is
fundamental and how much comes from inefficient source geometry.

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

The abstract optimum divided the energy equally between:

```text
repulsive region:
    p_x = p_y = p_z = -epsilon

support region:
    p_x = p_y = p_z = +epsilon
```

This suggests an optimistic scaling

```math
M_{\mathrm{equiv}}
\sim
\frac{ah^2}{G}
```

The important dependence is

```math
\boxed{
M,E\propto h^2
}
```

so reducing the source-target distance dramatically reduces the total energy
requirement.

### 1g at 1 meter

The abstract optimization gives approximately

```math
M_{\min}
\approx
1.47\times10^{11}\ \mathrm{kg}
```

### 1g at 1 micrometer

The abstract optimization gives approximately

```math
M_{\min}
\approx
1.47\times10^{-1}\ \mathrm{kg}
```

although the corresponding energy remains approximately

```math
E_{\min}
\approx
1.32\times10^{16}\ \mathrm{J}
```

### Important limitation

The coefficient $1$ is currently an **optimistic abstract bound inside the
model that was optimized**.

It has not yet been proven to be a universal theorem of general relativity.

The optimization currently imposes integrated stress balance rather than a
fully spatially resolved, locally conserved stress-energy tensor.

Files:

```text
src/antigravity_research/geometry/energy_bounds.py
tests/known_solutions/test_energy_bounds.py
simulations/006a_static_dec_lower_bound.py
```

---

# Current Research Frontier

The most important unresolved classical-GR question is now:

> **How close can a finite, locally conserved, DEC-respecting source get to
> the optimistic energy scaling below?**

```math
M_{\mathrm{equiv}}
=
\frac{ah^2}{G}
```

The explicit finite disk architecture currently requires

```math
M_{\mathrm{disk}}
\approx
79.753
\frac{ah^2}{G}
```

while the abstract optimization gives

```math
M_{\mathrm{abstract}}
\approx
1
\frac{ah^2}{G}
```

Equivalently, the currently unexplained architecture coefficient lies between

```math
1
\le
C_{\mathrm{physical}}
\le
79.753148
```

Understanding this gap is the highest-priority classical problem.

---

# Planned Research

## Research 006B — Geometry-Aware Stress-Energy Optimization

Build a spatially resolved axisymmetric optimization.

Candidate cell variables include:

```math
\epsilon,\quad
p_r,\quad
p_z,\quad
p_\phi
```

and, if needed, shear stresses.

Enforce pointwise energy conditions and discrete local conservation:

```math
\nabla_\mu T^{\mu\nu}=0
```

Compute the actual gravitational field using the spatial Green-function
kernel.

The objective is

```math
\min
\int
\epsilon\,dV
```

subject to a specified outward gravitational acceleration at a target point.

This should determine whether the coefficient can approach the abstract bound
of $1$ or whether geometry and local conservation impose a much larger
penalty.

---

## Research 006C — Independent Verification of the Finite Disk

Recalculate the 005B gravitational field using an independent numerical
integration of the complete stress-energy distribution.

The independent implementation should not reuse the analytic field
implementation from 005B.

Targets to reproduce include:

```math
\frac{z_{\mathrm{zero}}}{R}
\approx
0.393319893
```

and

```math
\frac{R}{h}
\approx
4.00614967
```

---

## Research 006D — Finite-Thickness Conserved Source

Replace idealized surface distributions with finite-thickness stress-energy.

Explicitly test

```math
\nabla_\mu T^{\mu\nu}=0
```

throughout the source and support structure.

Check NEC, WEC, and DEC locally.

This is necessary before treating the finite-wall architecture as a complete
physical stress-energy configuration.

---

## Research 007 — Quantum Energy-Condition Escape Routes

If classical positive-energy matter cannot approach useful energy scales, the
next established-physics branch will examine quantum violations of classical
energy conditions.

Candidate studies include:

- Casimir stress-energy;
- squeezed quantum states;
- quantum energy inequalities;
- negative-energy magnitude/duration bounds;
- complete apparatus gravitational accounting.

The purpose is not to assume quantum negative energy solves the problem, but
to determine quantitatively whether it can beat the classical static bounds.

---

## Research 008 — Modified Gravity

Modified gravitational theories will be investigated only after the
established-GR parameter space is better characterized.

Possible later candidates include:

- scalar-tensor gravity;
- $f(R)$ gravity;
- vector-tensor models;
- Horndeski-type theories;
- massive gravity;
- other well-defined extensions.

A modified theory producing repulsion is not by itself considered evidence
for a new physical effect unless the theory is independently motivated and
consistent with existing observations.

---

# Current Claims Ledger

## Known Results Reproduced

- Positive cosmological constant produces geodesic defocusing.
- Kottler spacetime contains an attraction/repulsion transition.
- Reissner-Nordstrom spacetime can produce local neutral-particle
  gravitational repulsion.
- Relativistic domain-wall stress can produce gravitational repulsion.

## Results Supported by Current Calculations

- Positive energy does not forbid local gravitational repulsion.
- Negative ADM mass is not required for local gravitational repulsion.
- Relativistically negative pressure/tension is a recurring mechanism for
  gravitational repulsion.
- A finite supported tension-disk model can possess a repulsive near field
  while retaining positive total mass and an attractive far field.
- The energy cost of the static positive-energy mechanisms studied so far
  scales approximately as $ah^2/G$ times an architecture-dependent
  coefficient.

## Model-Dependent Results Requiring Further Verification

Finite-disk optimum:

```math
\frac{R}{h}
\approx
4.00615
```

Finite-disk repulsive-zone height:

```math
\frac{z}{R}
\approx
0.393320
```

Finite-disk mass coefficient:

```math
C_{\mathrm{disk}}
\approx
79.753148
```

Abstract static DEC + integrated-stress optimum:

```math
C_{\mathrm{abstract}}
=
1
```

## Not Established

- A practical antigravity device.
- A known laboratory material capable of sustaining the required relativistic
  stress.
- A stable finite scalar-domain-wall apparatus.
- Global positive-mass antigravity.
- A universal proof that the Simulation 006A coefficient is the absolute
  lower bound in full general relativity.
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

> **Local antigravity in general relativity is primarily a relativistic
> stress-energy problem.**

The project is therefore focused on finding the lowest-energy, locally
conserved, physically realizable stress-energy configuration capable of
producing a measurable repulsive gravitational near field.

The immediate next objective is to determine whether spatial geometry and
local conservation allow a real finite source to approach the optimistic
Simulation 006A energy bound, or whether a much larger energy penalty is
unavoidable.
