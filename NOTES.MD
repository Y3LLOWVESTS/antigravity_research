GitHub rendering note: This file intentionally contains the complete monolithic research history for AI/session handoff. Because it contains roughly 39,000 lines and more than one thousand mathematical display blocks, GitHub may show Unable to render expression for otherwise valid mathematics. For reliable rendered equations, use the corresponding files under notes/chronology/. The raw mathematical source remains intact.

### BEGIN NOTE - AUGUST 27 2026 - 01:00 CST

# ANTIGRAVITY_RESEARCH — Comprehensive Carry-Forward Notes

This is the right place to stop adding patches and consolidate what we actually know.

The project has advanced far enough that the problem is now much more sharply defined than when we started. We have **not discovered a new law of physics or a practical antigravity device**, but we have established something important and useful:

```math
\text{General relativity absolutely permits local gravitational repulsion.}
```

More specifically, we have reproduced several known GR mechanisms and constructed a finite linearized-GR model in which **positive energy, positive total mass, and classical energy conditions coexist with a locally repulsive gravitational field**. What has emerged as the dominant obstacle is no longer the **sign** of gravity. It is the **stress-energy cost and physical realizability** of the source.

Simulation 006A then sharpened that further: within its stated assumptions, the optimistic static energy cost scales as

```math
M_{\mathrm{equiv}}\sim\frac{a h^2}{G}
```

where $a$ is the desired repulsive acceleration and $h$ is the source-to-target scale. Your optimizer independently reproduced the coefficient 1.0 exactly, while the explicit finite disk/rim architecture costs 79.753 times more. 

That gap—**1 versus 79.753**—is now one of the most important open mathematical questions in the project.

---

# 1. Current scientific conclusion

The simplest useful description of everything we have learned is:

```math
\text{gravity responds to stress-energy, not merely mass density}
```

and therefore sufficiently large **negative pressure/tension** can make the local active gravitational source negative even when the actual energy density remains positive.

For type-I matter in its local rest frame,

```math
T^\mu{}_\nu
\sim
{\mathrm{diag}}(\epsilon,p_x,p_y,p_z)
```

and in static weak-field GR the relevant active combination is schematically

```math
S=\epsilon+p_x+p_y+p_z
```

Ordinary matter has relatively tiny stresses compared with its rest energy:

```math
|p_i|\ll\epsilon
```

Hence it attracts.

Relativistic fields can instead have

```math
|p_i|\sim\epsilon
```

and sufficiently negative principal pressures can make

```math
S<0
```

That is the recurring mechanism behind essentially every successful branch we found:

```math
\text{vacuum energy},
\quad
\text{domain walls},
\quad
\text{anisotropic Maxwell stress},
\quad
\text{relativistic tension}
```

This is not speculative. Exact GR domain-wall solutions are known to repel, and the planar-wall attraction/repulsion transition occurs at tension/surface-energy ratio $1/2$. ([APS Journals][1]) Reissner–Nordström spacetime likewise has a known repulsive region for neutral test particles. ([arXiv][2])

So a useful project-level statement is now:

> **Antigravity-like local gravitational repulsion does not inherently require negative mass or negative energy. Relativistic stress/tension can produce it within ordinary general relativity.**

That statement is supported.

What is **not** established is a practical apparatus capable of generating such stresses economically or stably.

---

# 2. Current repository / environment checkpoint

The development environment is healthy:

```text
Python 3.13.15
NumPy 2.5.2
SciPy 1.18.1
SymPy 1.14.0
Matplotlib 3.11.1
mpmath 1.3.0
pytest 9.1.1
```

The repo now has a real research structure with theory, simulations, reusable geometry modules, known-solution tests, figures, CSV results, and persistent run logs.

Licensing was also cleaned up:

```text
Software:
MIT OR Apache-2.0
Original research:
CC0-1.0
Human project lead / affirmer:
Stevan White
AI assistance:
ChatGPT by OpenAI disclosed in AI_ASSISTANCE.md
```

The last Git commit/push you showed was:

```text
447d35b  updated licenses :)
```

That commit already contained Simulations 001–002 and the licensing changes. Everything from 003A onward was created later in this session, so unless you committed again afterward, those newer simulations are probably still uncommitted. That is worth checking at the beginning of the next session with:

```bash
git status --short
```

Do not assume that 003–006 are safely on GitHub until checked.

---

# 3. Test-suite checkpoint

Before 006A, the entire known-solutions suite had reached:

```text
61 passed
```

Simulation 006A then added six more tests, which individually passed:

```text
6 passed
```

So the expected total current regression count is approximately:

```math
67\text{ tests}
```

assuming everything is still present and no test discovery issue exists.

The first verification command next session should therefore be:

```bash
ROOT="$(pwd)"
PY="$ROOT/.venv/bin/python"
PYTHONPATH="$ROOT/src" \
"$PY" -m pytest -q tests/known_solutions
```

Expected:

```text
67 passed
```

If it differs, inspect the discrepancy before doing new physics.

---

# 4. Simulation 001A — Kottler / Schwarzschild–de Sitter baseline

Files:

```text
src/antigravity_research/geometry/kottler.py
tests/known_solutions/test_kottler.py
simulations/001_kottler_weak_field.py
results/data/001_kottler_weak_field.csv
results/figures/001_kottler_weak_field.png
```

We began with known GR:

```math
a(r)=
-\frac{GM}{r^2}
+
\frac{\Lambda c^2r}{3}
```

The radius where attraction and cosmological repulsion balance is

```math
r_s=
\left(
\frac{3GM}{\Lambda c^2}
\right)^{1/3}
```

For a $10^{12}M_\odot$ mass and observed cosmological parameters, we reproduced:

```math
r_s\simeq1.1139\ {\mathrm{Mpc}}
```

Below that scale, gravity was inward.

Above it, the cosmological-$\Lambda$ contribution won.

### Conclusion

Cosmological repulsion is real GR physics.

But observed $\Lambda$ is fantastically too weak for laboratory antigravity.

Classification:

```text
KNOWN_RESULT=YES
REPRODUCED=YES
NOVEL_ANTIGRAVITY_CLAIM=NO
```

---

# 5. Simulation 001B — invariant geodesic-deviation check

Files:

```text
src/antigravity_research/geometry/kottler_tidal.py
tests/known_solutions/test_kottler_tidal.py
simulations/001b_kottler_tidal_eigenvalues.py
results/data/001b_kottler_tidal_eigenvalues.csv
results/figures/001b_kottler_tidal_eigenvalues.png
```

This was important because coordinate acceleration alone can be misleading in GR.

We therefore examined the local free-fall tidal eigenvalues:

```math
\lambda_r=
\frac{2GM}{r^3}
+\frac{\Lambda c^2}{3}
```

```math
\lambda_t=
-\frac{GM}{r^3}
+\frac{\Lambda c^2}{3}
```

We reproduced:

```math
\lambda_r+2\lambda_t=\Lambda c^2
```

At sufficiently large radius all three spatial modes become stretching modes.

The transverse transition occurred numerically essentially where expected:

```text
ANALYTICAL_THRESHOLD ≈ 1.1139216 Mpc
NUMERICAL_THRESHOLD  ≈ 1.1138830 Mpc
```

### Conclusion

The cosmological repulsion is not merely a coordinate artifact. Neighboring free-falling particles genuinely separate.

This established our preferred operational definition:

> **Repulsion should ultimately be diagnosed through invariant or observer-operational quantities such as geodesic deviation, relative free-fall acceleration, or proper acceleration—not arbitrary coordinate acceleration.**

---

# 6. Simulation 002 — required stress-energy

Files:

```text
src/antigravity_research/geometry/perfect_fluid_defocusing.py
tests/known_solutions/test_perfect_fluid_defocusing.py
simulations/002_required_stress_energy.py
results/data/002_required_stress_energy.csv
results/figures/002_required_energy_density_1m.png
```

For an ideal isotropic fluid we used

```math
\frac{\ddot\xi}{\xi}
=
-\frac{4\pi G}{3c^2}
(\epsilon+3p)
+
\frac{\Lambda c^2}{3}
```

For

```math
p=w\epsilon
```

the active combination is

```math
\epsilon(1+3w)
```

Positive-energy defocusing becomes possible when

```math
w<-\frac13
```

The especially interesting $w=-1$ case preserved classical NEC/WEC/DEC while violating SEC.

For $1g$ of relative acceleration across one meter:

```math
\epsilon
\simeq
1.5763\times10^{27}\ {\mathrm{J/m^3}}
```

with

```math
p=-\epsilon
```

### Conclusion

Negative energy is **not necessary** for the sign of gravitational repulsion.

Sufficiently negative pressure works.

But this was a local homogeneous/isotropic benchmark, not a localized object.

---

# 7. Simulation 003A — localization obstruction for vacuum energy

Files:

```text
src/antigravity_research/geometry/vacuum_energy_core.py
tests/known_solutions/test_vacuum_energy_core.py
simulations/003a_finite_vacuum_energy_core.py
```

We attempted to make a finite $w=-1$ region.

The TOV equation gave

```math
\frac{dp}{dr}=0
```

for pure

```math
p=-\epsilon
```

Therefore a pure vacuum-energy region cannot simply taper continuously to zero at a finite radius while retaining that same EOS.

The proposed de Sitter interior and Schwarzschild exterior had:

```math
f_{\mathrm{in}}(R)=f_{\mathrm{out}}(R)
```

but

```math
f'_{\mathrm{in}}(R)\ne f'_{\mathrm{out}}(R)
```

Specifically we found the derivative ratio:

```math
\frac{f'_{\mathrm{in}}}{f'_{\mathrm{out}}}=-2
```

Therefore boundary stress is needed.

Even more importantly, the positive-volume-energy core produced a **positive Schwarzschild exterior mass**, hence:

```text
INTERIOR_DEFOCUSING=YES
EXTERIOR_FIELD=INWARD
```

### Conclusion

Internal repulsion does not automatically imply external antigravity.

---

# 8. Simulation 003B — exact Israel shell search

Files:

```text
src/antigravity_research/geometry/israel_shell.py
tests/known_solutions/test_israel_shell.py
simulations/003b_israel_shell_mass_search.py
results/data/003b_israel_shell_mass_search.csv
results/figures/003b_israel_shell_conditions_1g.png
```

Here we calculated the thin-shell stress properly rather than relying on a derivative mismatch.

The central question was:

> Can the de Sitter core be surrounded by a shell that yields a repulsive Schwarzschild exterior?

For an asymptotically flat Schwarzschild exterior, outward weak-field behavior requires

```math
M_{\mathrm{ADM}}<0
```

The exact shell search showed:

```text
OUTWARD_CASE_WITH_NONNEGATIVE_SHELL_SURFACE_ENERGY=NO
OUTWARD_CASE_WITH_WEC=NO
OUTWARD_CASE_WITH_DEC=NO
OUTWARD_CASE_WITH_NEC=YES
NEGATIVE_SHELL_ENERGY_REQUIRED_FOR_OUTWARD_EXTERIOR=YES
```

The NEC survived approximately over the narrow region

```math
-\frac12M_v\lesssim M_{\mathrm{ADM}}<0
```

but WEC/DEC did not.

The mass relation closed to roughly

```math
5\times10^{-16}
```

fractional error.

### Conclusion

Negative Schwarzschild mass provides repulsion mathematically, but it buys that result using exotic negative shell energy.

This also fits the broader positive-mass theorem: for asymptotically flat initial data satisfying the dominant energy condition,

```math
E\ge |P|
```

so negative ADM energy is unavailable under those assumptions. ([arXiv][3])

This route should remain low priority.

---

# 9. Simulation 004A — Reissner–Nordström breakthrough

Files:

```text
src/antigravity_research/geometry/reissner_nordstrom.py
tests/known_solutions/test_reissner_nordstrom.py
simulations/004a_einstein_maxwell_repulsion.py
results/data/004a_einstein_maxwell_repulsion.csv
results/figures/004a_rn_neutral_gravity_1g_z1p2.png
```

This changed the project.

We tested an exact Einstein–Maxwell system:

```text
Minkowski interior
charged shell
Reissner–Nordström exterior
```

and recovered the known RN sign-change radius

```math
r_{\mathrm{rep}}
=
\frac{Q^2}
{4\pi\epsilon_0Mc^2}
```

Define

```math
z=\frac{r_{\mathrm{rep}}}{R}
```

Then

```math
z>1
```

puts part of the repulsive region **outside the physical source**.

Our search found:

```text
DEC_REPULSIVE_Z_MIN ≈ 1.001
DEC_REPULSIVE_Z_MAX ≈ 1.33317
```

and, decisively:

```text
POSITIVE_ADM_MASS=YES
MAXWELL_FIELD_ENERGY_POSITIVE=YES
EXTERNAL_NEUTRAL_GRAVITATIONAL_REPULSION=YES
REPULSION_WITH_NONNEGATIVE_SHELL_ENERGY=YES
REPULSION_WITH_SHELL_WEC=YES
REPULSION_WITH_SHELL_DEC=YES
NEGATIVE_ADM_MASS_REQUIRED=NO
NEGATIVE_ENERGY_REQUIRED=NO_FOR_THIS_EXACT_MODEL
```

This is consistent with known RN repulsive behavior for neutral test particles. ([arXiv][2])

### The physics insight

The electromagnetic field has anisotropic stresses:

```math
p_r=-\epsilon,
\qquad
p_t=+\epsilon
```

It therefore taught us that **anisotropic relativistic stress can reverse local gravity without negative energy**.

### Physical failure mode

For the $1g$, $1\,{\mathrm{m}}$ benchmark:

```math
E_{\mathrm{surface}}
\simeq
2.67\times10^{19}\ {\mathrm{V/m}}
```

around twenty Schwinger fields.

Even making the solution sub-Schwinger pushed the scale to roughly:

```text
radius ≈ 407 m
mass ≈ 1.22×10^17 kg
charge ≈ 2.44×10^13 C
```

So the gravitational equations work.

Electrical engineering does not.

RN remains extremely valuable as a **proof of principle**, not presently as the best implementation route.

---

# 10. Simulation 005A — relativistic-tension/domain-wall principle

Files:

```text
src/antigravity_research/geometry/relativistic_wall.py
tests/known_solutions/test_relativistic_wall.py
simulations/005a_relativistic_tension_wall.py
results/data/005a_relativistic_tension_wall.csv
results/figures/005a_tension_efficiency.png
```

This generalized the RN lesson.

For a membrane having surface energy $U$ and tension

```math
\tau=qU
```

the planar gravitational sign changes at:

```math
q=\frac12
```

Repulsion:

```math
q>\frac12
```

DEC:

```math
q\le1
```

Therefore the entire interval

```math
\frac12<q\le1
```

supports positive-energy repulsive gravity while satisfying NEC/WEC/DEC.

This matches established GR wall results: sufficiently high tension makes walls repulsive, with the transition at $\tau/\sigma=1/2$. ([APS Journals][4])

The most efficient member of this membrane class is

```math
q=1
```

the ideal domain-wall stress tensor.

### One-g benchmark

We obtained:

```math
U_{\min}
\simeq
2.1017\times10^{27}\ {\mathrm{J/m^2}}
```

Equivalent surface mass:

```math
2.3385\times10^{10}\ {\mathrm{kg/m^2}}
```

The toy $\phi^4$ mapping produced

```math
v\simeq81.5\ {\mathrm{GeV}}
```

for $\lambda=1$.

Important caveat:

**That does not mean electroweak physics provides a usable antigravity wall.**

It only means that a toy scalar potential with the required integrated wall tension can be parameterized with a VEV on that scale.

Exact scalar-domain-wall GR solutions are known and are repulsive. ([APS Journals][5])

---

# 11. Simulation 005B — finite supported wall

Files:

```text
src/antigravity_research/geometry/finite_tension_disk.py
tests/known_solutions/test_finite_tension_disk.py
simulations/005b_finite_supported_antigravity.py
results/data/005b_finite_supported_antigravity.csv
results/figures/005b_finite_supported_field.png
```

This was our first attempt to turn the infinite wall into a finite static source.

Architecture:

```text
relativistic-tension disk
+
minimum-energy DEC-compatible compressive rim
```

The support rim was included specifically because one cannot simply ignore the stresses required to hold a finite tension-bearing object together.

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

This is the key physical picture.

A finite positive-energy system can have:

```math
\text{repulsive near field}
```

while still having:

```math
\text{ordinary attractive far field}
```

There is no contradiction with positive total mass.

The optimal disk geometry in this model was

```math
q=1
```

```math
\frac{R}{h}
\simeq4.00615
```

with repulsion extending to

```math
\frac{z}{R}
\simeq0.393320
```

The architecture's mass law was:

```math
M_{\mathrm{disk}}
\simeq
79.753148
\frac{ah^2}{G}.
```

At $1g$ one meter away:

```math
M\simeq1.172\times10^{13}\ {\mathrm{kg}}
```

```math
E\simeq1.053\times10^{30}\ {\mathrm{J}}
```

At $10^{-6}g$, one centimeter away:

```math
M\simeq1.172\times10^3\ {\mathrm{kg}}
```

### Important qualification

005B is **linearized GR plus an idealized membrane/rim stress model**.

It is not yet:

* an exact Einstein solution;
* a realistic material;
* a demonstrated dynamically stable configuration;
* a proof that all local conservation laws can be satisfied by an actual finite-thickness field theory.

So classify it as:

```text
NUMERICAL_MODEL_RESULT
```

not:

```text
PRACTICAL_DEVICE
```

The Laue theorem itself has precise hypotheses involving stationary/localized stress-energy and spacetime symmetries, so we should preserve those assumptions explicitly rather than treating integrated stress cancellation as a universally applicable identity. ([arXiv][6])

---

# 12. Simulation 006A — abstract static DEC energy bound

Files:

```text
src/antigravity_research/geometry/energy_bounds.py
tests/known_solutions/test_energy_bounds.py
simulations/006a_static_dec_lower_bound.py
results/data/006a_static_dec_energy_bound.csv
results/figures/006a_static_dec_mass_bound.png
```

This is the current frontier.

The optimizer was given independent integrated stress variables and asked:

> What is the smallest positive energy capable of producing a normalized negative active gravitational source while satisfying DEC and static Laue balance?

It returned exactly:

```text
GENERAL_MIN_ENERGY_COEFFICIENT=1.000000
E_REP=0.500000
E_SUPPORT=0.500000
P_REP_X=-0.500000
P_REP_Y=-0.500000
P_REP_Z=-0.500000
P_SUPPORT_X=+0.500000
P_SUPPORT_Y=+0.500000
P_SUPPORT_Z=+0.500000
```

The domain-wall-restricted LP returned:

```text
DOMAIN_WALL_MIN_ENERGY_COEFFICIENT=2.000000
```

And:

```text
005B_ARCHITECTURE_COEFFICIENT=79.753148
```

So:

```math
1
<
79.753
```

by an enormous margin. 

The general solution tells us that the abstract optimum wants:

### Repulsive region

```math
p_x=p_y=p_z=-\epsilon
```

That is maximally negative pressure while saturating DEC.

### Supporting region

```math
p_x=p_y=p_z=+\epsilon
```

That is maximally positive stress.

Both carry positive energy.

The optimizer splits the energy equally.

---

# 13. Extremely important caveat about 006A

Do **not** promote

```math
M\ge\frac{ah^2}{G}
```

to a universal theorem yet.

006A proves the optimum **of the LP we formulated**.

That LP uses:

* linearized gravity;
* type-I stress-energy;
* DEC;
* integrated Laue balance;
* an optimistic $1/h^2$ gravitational kernel;
* no explicit spatial support geometry;
* no discrete local equation

```math
  \partial_jT^{ij}=0
```
* no exact Einstein constraint equations;
* no stability conditions;
* no finite-thickness field realization.

Therefore coefficient 1 should currently be labeled:

```text
OPTIMISTIC_ABSTRACT_STATIC_DEC_BOUND
```

not:

```text
PROVEN_UNIVERSAL_GR_BOUND
```

That distinction is critical.

The **pointwise** part is much stronger:

DEC gives

```math
|p_i|\le\epsilon
```

and therefore

```math
\epsilon+p_x+p_y+p_z
\ge
-2\epsilon
```

That really does identify

```math
p_x=p_y=p_z=-\epsilon
```

as the maximally negative active source within this type-I DEC framework.

But converting that local statement into the global coefficient exactly equal to 1 requires additional geometric assumptions.

---

# 14. Current fundamental scale estimates

006A produced an especially useful matrix.

For a static DEC source, the optimistic abstract bound is:

```math
M_{\mathrm{static}}
\approx
\frac{ah^2}{G}.
```

### $1g$

At $h=1\,{\mathrm{m}}$:

```math
M_{\min}
=
1.4693\times10^{11}\ {\mathrm{kg}}
```

```math
E_{\min}
=
1.3206\times10^{28}\ {\mathrm{J}}
```

At $h=1\,{\mathrm{cm}}$:

```math
M_{\min}
=
1.4693\times10^7\ {\mathrm{kg}}
```

At $h=1\,{\mathrm{mm}}$:

```math
M_{\min}
=
1.4693\times10^5\ {\mathrm{kg}}
```

At $h=1\,\mu{\mathrm{m}}$:

```math
M_{\min}
=
0.1469\ {\mathrm{kg}}
```

but still:

```math
E_{\min}
=
1.3206\times10^{16}\ {\mathrm{J}}
```

At $h=1\,{\mathrm{nm}}$:

```math
M_{\min}
=
1.4693\times10^{-7}\ {\mathrm{kg}}
```

with

```math
E_{\min}
\sim1.32\times10^{10}\ {\mathrm{J}}
```

The extremely important scaling is:

```math
M,E\propto h^2
```

This means microscopic stand-off helps enormously.

It does **not** make the corresponding energy density automatically feasible.

---

# 15. What has actually been discovered by this project

I would classify our results like this.

## KNOWN_RESULT — independently reproduced

### Cosmological-$\Lambda$ defocusing

Confirmed.

### Kottler static-radius behavior

Confirmed.

### Domain-wall gravitational repulsion

Confirmed and consistent with known exact GR results. ([APS Journals][1])

### Tension threshold near

```math
\tau/U=1/2
```

Confirmed and consistent with established planar-wall calculations. ([APS Journals][4])

### Reissner–Nordström repulsive region

Confirmed and consistent with known neutral-test-particle analyses. ([arXiv][2])

---

# 16. Project-derived results that are interesting but not yet independently established

### Finite disk/rim architecture

We obtained:

```math
R/h\simeq4.00615
```

```math
z_{\mathrm{zero}}/R\simeq0.393320
```

```math
M\simeq79.753\,ah^2/G
```

This appears internally consistent in our linearized model.

It needs independent analytical derivation and ideally an independent implementation.

### Abstract static DEC+Laue LP optimum

We obtained:

```math
C_{\mathrm{optimum}}=1
```

This is extremely interesting.

It is **not yet a universal theorem**.

The LP needs to be upgraded to include spatial geometry and local conservation.

---

# 17. Routes that now look comparatively weak

## Negative ADM mass

Mathematically repulsive.

Requires negative shell energy/WEC failure in our exact shell construction.

Positive-mass results additionally make this unattractive under conventional asymptotically flat DEC assumptions. ([arXiv][3])

Low priority.

## Pure cosmological constant

Correct sign.

Hopeless magnitude at observed $\Lambda$.

Low priority.

## Ordinary electrostatic RN device

Excellent mathematical proof of principle.

Engineering requires absurd net charge/field strength.

Keep as reference solution, not primary practical route.

## Ordinary mechanical tension

Far too small because ordinary matter has roughly

```math
\tau/U\ll1
```

Antigravity wants relativistic stresses:

```math
\tau/U\sim1
```

Low priority unless an exotic condensed-matter effective stress can mimic relativistic field stress gravitationally—which would require extremely careful treatment because effective pressure is not automatically the same as fundamental stress-energy.

---

# 18. Highest-priority next simulation: 006B

This should be the **geometry-aware stress-energy optimizer**.

This is, in my assessment, more important than immediately jumping to modified gravity or random exotic fields.

The unresolved question is:

```math
1
\le C_{\mathrm{real}}
\le79.753
```

where

```math
M=C_{\mathrm{real}}\frac{ah^2}{G}
```

We need to determine how close an actual spatially conserved source can get to 1.

### Simulation 006B should discretize space

Use axisymmetry initially.

Each cell should contain variables like:

```math
\epsilon,
p_r,
p_z,
p_\phi
```

and potentially shear stresses.

Impose pointwise:

```math
\epsilon\ge0
```

and DEC constraints such as

```math
|p_i|\le\epsilon
```

Then impose discrete local conservation:

```math
\partial_jT^{ij}=0
```

Not merely integrated Laue balance.

The target acceleration should be computed using the actual spatial Green-function kernel.

Objective:

```math
\min \int \epsilon\,dV
```

Constraint:

```math
a_z(\text{target})\ge a_{\mathrm{requested}}
```

Then optimize source geometry.

### What 006B would tell us

If it reaches:

```math
C\sim1-5
```

then our disk was extremely inefficient and there may be a much better classical architecture.

If it bottoms out around:

```math
C\sim10-100
```

then finite geometry/local stress conservation imposes a major penalty.

If it reproduces approximately:

```math
C\sim79.753
```

then our simple disk/rim architecture may already be surprisingly close to optimal.

This is probably the single most valuable next classical-GR computation.

---

# 19. Simulation 006C — independent verification of 005B

Before relying heavily on 79.753, independently reproduce the finite-disk field.

Do not reuse `finite_tension_disk.py`.

Write an independent numerical integration directly over the stress-energy:

```math
T_{\mu\nu}(\mathbf{x})
```

Numerically integrate the linearized Einstein Green function.

Compare the resulting axial acceleration against:

```text
dimensionless_axis_factor()
```

for many $q,z/R$.

Specifically reproduce:

```math
z_{\mathrm{zero}}/R
=
0.393319893190
```

for $q=1$,

and

```math
R/h
=
4.006149670781
```

at the optimum.

This is important because 005B currently uses an analytical formula and tests that mostly call the same implementation.

Independent numerical integration would substantially increase confidence.

---

# 20. Simulation 006D — exact conservation / finite-thickness support

The current disk and rim are ideal distributions.

Replace them with finite thickness.

Check:

```math
\nabla_\mu T^{\mu\nu}=0
```

throughout the entire source.

Specifically inspect the disk/rim boundary because this is where hidden forces or singular support stresses are most likely.

Then verify NEC/WEC/DEC locally rather than only in idealized components.

This is a prerequisite before calling 005B a physically self-consistent matter configuration.

---

# 21. Quantum negative energy: next major escape route

If 006B shows that ordinary DEC matter cannot reduce the coefficient enough, the next established-physics escape is quantum stress-energy.

Quantum fields can violate classical pointwise energy conditions.

However they obey quantum energy inequalities, which constrain negative energy averaged over time/space. Fewster's reviews describe these QEIs as surviving remnants of classical energy conditions. ([arXiv][7]) Ford/Pfenning/Roman similarly describe restrictions relating negative-energy magnitude and duration. ([arXiv][8])

This means quantum negative energy is worth investigating, but not assuming to be a magic loophole.

---

# 22. Proposed Simulation 007A — Casimir gravitational benchmark

This should be our first quantum calculation.

Use the parallel-plate Casimir stress tensor.

Calculate:

* negative vacuum energy density;
* principal pressures;
* active gravitational combination;
* predicted local gravitational acceleration;
* dependence on plate spacing $d$;
* apparatus support stresses;
* total apparatus mass;
* gravitational field including plates/support.

Scan:

```text
1 mm
100 μm
10 μm
1 μm
100 nm
10 nm
1 nm
```

The fundamental Casimir scaling is roughly:

```math
|\rho_C|\propto\frac{\hbar c}{d^4}
```

The corresponding gravitational scale is therefore roughly:

```math
a_{\mathrm{Casimir}}
\sim
\frac{G\hbar}{c\,d^3}
```

up to order-one/geometric factors.

That scaling is useful because it immediately tells us that quantum-vacuum gravity becomes appreciable only at extremely small length scales.

Casimir vacuum energy itself does gravitate consistently with the equivalence principle once the complete apparatus is treated properly. ([APS Journals][9])

That complete-apparatus point is crucial—we must not count the negative vacuum region while ignoring the plates holding it there.

---

# 23. Proposed Simulation 007B — quantum-energy-inequality benchmark

Instead of choosing a particular apparatus, impose a representative QEI bound.

Ask:

> Given a sampling duration $\tau$ and spatial scale $h$, what maximum negative stress-energy is quantum field theory plausibly allowed to sustain?

Then convert that into maximum gravitational acceleration.

Make the result a map:

```math
a_{\max}(h,\tau)
```

If QEI-limited negative energy remains hopelessly weak until near nuclear or Planck scales, we can deprioritize the whole quantum-vacuum branch.

This is much more informative than casually discussing Casimir plates.

---

# 24. Dynamic sources are another escape route—but probably only an O(1) improvement

006A assumes static stress balance.

A time-dependent source need not satisfy the same instantaneous Laue conditions.

Therefore a dynamic pulse could in principle avoid the factor-of-two support-energy penalty that changed:

```math
\frac{ah^2}{2G}
```

into:

```math
\frac{ah^2}{G}
```

But it does **not** automatically evade the pointwise DEC inequality

```math
S\ge-2\epsilon
```

Therefore I do not currently expect dynamics alone to reduce the energy requirement by dozens of orders of magnitude.

It may reduce coefficients.

It probably does not solve the basic energy scale.

Still, a future Simulation 007C should investigate:

* scalar-field pulses;
* oscillating domain walls;
* moving anisotropic stress;
* retarded gravitational fields;
* transient negative active source;
* gravitational-wave stress contributions.

---

# 25. Modified gravity should come later

Modified gravity gives us enormous freedom:

* scalar-tensor gravity;
* $f(R)$;
* Horndeski-type theories;
* vector-tensor models;
* massive gravity;
* emergent/effective gravity.

But we should not jump there yet.

Why?

Because if we allow ourselves to change Einstein's equations before we have mapped the strongest possible result in Einstein gravity, almost any desired behavior can be engineered into a model.

It becomes difficult to distinguish:

```text
REAL_PHYSICAL_INSIGHT
```

from:

```text
ASSUMED_THEORY_PRODUCES_DESIRED_RESULT
```

I would only move modified gravity ahead of classical/quantum GR once we can state a sharp no-go theorem under established physics.

---

# 26. Important conceptual distinction going forward

We should use three separate terms.

### Local gravitational repulsion

A nearby freely falling neutral object accelerates away from some source region.

We have this.

### Global gravitational repulsion

The asymptotic field of the entire isolated source points outward.

We do **not** have this with positive total ADM mass.

### Practical antigravity

A finite controllable device produces useful local repulsive acceleration with realizable energy/material requirements.

We definitely do **not** have this.

That terminology will prevent us from accidentally turning a valid local-GR result into an unjustified device claim.

---

# 27. Claims ledger

I would record the current claims as:

```text
KNOWN_RESULT:
Cosmological Lambda produces geodesic defocusing.
KNOWN_RESULT_REPRODUCED:
Kottler static-radius transition.
KNOWN_RESULT_REPRODUCED:
Reissner-Nordstrom geometry can produce local neutral-particle
gravitational repulsion.
KNOWN_RESULT_REPRODUCED:
Relativistic domain-wall tension can produce gravitational repulsion.
REPRODUCED:
Positive energy does not forbid local gravitational repulsion.
REPRODUCED:
Negative ADM mass is not required for local gravitational repulsion.
NUMERICAL_MODEL_RESULT:
Finite DEC-supported tension disk has a local repulsive region.
NUMERICAL_MODEL_RESULT:
005B optimum R/h ≈ 4.00614967.
NUMERICAL_MODEL_RESULT:
005B coefficient ≈ 79.753148.
NUMERICAL_OPTIMIZATION_RESULT:
Abstract static DEC+Laue LP coefficient = 1.
CONJECTURE / UNPROVEN:
Coefficient 1 is a universal attainable lower bound for finite static
DEC matter in GR.
NOT_ESTABLISHED:
Finite material capable of realizing required relativistic stress.
NOT_ESTABLISHED:
Stable laboratory domain-wall source.
NOT_ESTABLISHED:
Global positive-mass antigravity.
NOT_ESTABLISHED:
Practical antigravity device.
NOVEL_PHYSICS_CLAIM:
NO.
```

That is the scientifically defensible state.

---

# 28. How to rerun every current simulation

From repo root:

```bash
ROOT="$(pwd)"
PY="$ROOT/.venv/bin/python"
export PYTHONPATH="$ROOT/src"
```

Full verification:

```bash
"$PY" -m pytest -q tests/known_solutions
```

Then the simulations individually:

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

To preserve all output:

```bash
mkdir -p results/logs
for SIM in \
  simulations/001_kottler_weak_field.py \
  simulations/001b_kottler_tidal_eigenvalues.py \
  simulations/002_required_stress_energy.py \
  simulations/003a_finite_vacuum_energy_core.py \
  simulations/003b_israel_shell_mass_search.py \
  simulations/004a_einstein_maxwell_repulsion.py \
  simulations/005a_relativistic_tension_wall.py \
  simulations/005b_finite_supported_antigravity.py \
  simulations/006a_static_dec_lower_bound.py
do
    NAME="$(basename "$SIM" .py)"
    echo
    echo "===== $NAME ====="
    "$PY" "$SIM" 2>&1 |
      tee "results/logs/${NAME}_rerun.log"
done
```

That will let us reproduce the entire research chain without losing Terminal output.

---

# 29. Recommended order for the next research session

I would **not** continue randomly.

The highest-value path is:

```text
FIRST:
Run full ~67-test regression.
SECOND:
006B geometry-aware DEC optimizer with local conservation.
THIRD:
006C independently integrate the 005B stress-energy gravitational field.
FOURTH:
006D finite-thickness/local-conservation realization.
FIFTH:
007A Casimir negative-energy gravitational benchmark.
SIXTH:
007B quantum-energy-inequality bound.
SEVENTH:
007C dynamic/nonstatic stress sources.
ONLY THEN:
008 modified-gravity escape routes.
```

The single most important immediate question is therefore:

```math
\text{How close can an actual finite, locally conserved DEC source get to }
M=\frac{ah^2}{G}\text{?}
```

If we can reduce the explicit coefficient from

```math
79.753
```

toward

```math
1
```

that is a substantial improvement in the classical positive-energy antigravity architecture.

If local conservation forces it to remain large, then the classical route has effectively given us its answer, and we move into quantum negative energy.

---

# 30. Overall state of the project

The project began with the vague question:

> Can antigravity exist?

We now have a much more precise answer.

### Mathematically

**Yes—local gravitational repulsion exists in ordinary general relativity.**

We reproduced multiple independent examples.

### Positive energy?

**Yes.**

RN and domain-wall mechanisms establish that negative energy is not intrinsically required for local repulsion.

### Negative mass?

**No—not for local repulsion.**

Our positive-mass RN and tension models demonstrate this.

### Classical energy conditions?

**They can be satisfied locally.**

We found NEC/WEC/DEC-compatible repulsive configurations.

### Finite source?

**We have a finite linearized model with a repulsive near field.**

005B.

### Attractive far field?

**Yes.**

Finite positive-total-mass configurations return to attraction far away.

That is consistent with the positive-mass structure of GR rather than being a bug. ([arXiv][3])

### Practical?

**Not remotely yet.**

The required relativistic stress-energy densities are enormous.

### Best current physical interpretation

The project has converged on:

```math
\text{Antigravity in GR is fundamentally a stress-engineering problem.}
```

The source should not be thought of as “negative mass.”

The more useful target is:

```math
\text{positive energy with relativistically negative principal pressure/tension}
```

placed near the target while compensating positive stresses are arranged so that the complete isolated system remains physically consistent.

And 006A has now made the next research objective extraordinarily clear:

```math
\text{Find the minimum-energy spatial realization of that stress tensor.}
```

That is where I would resume. It gives us a focused mathematical optimization problem instead of another broad search for mysterious antigravity physics.

[1]: https://journals.aps.org/prd/abstract/10.1103/PhysRevD.30.712 "Gravitationally repulsive domain wall | Phys. Rev. D"
[2]: https://arxiv.org/abs/1012.5411 "Circular motion of neutral test particles in Reissner-Nordström spacetime"
[3]: https://arxiv.org/abs/1110.2087 "The spacetime positive mass theorem in dimensions less than eight"
[4]: https://journals.aps.org/prd/abstract/10.1103/PhysRevD.30.2452 "Repulsive and attractive planar walls in general relativity | Phys. Rev. D"
[5]: https://journals.aps.org/prd/abstract/10.1103/PhysRevD.39.3571 "General-relativistic domain walls | Phys. Rev. D"
[6]: https://arxiv.org/abs/1808.09320 "[1808.09320] Laue's Theorem Revisited: Energy-Momentum Tensors, Symmetries, and the Habitat of Globally Conserved Quantities"
[7]: https://arxiv.org/abs/math-ph/0501073 "Energy Inequalities in Quantum Field Theory"
[8]: https://arxiv.org/abs/gr-qc/9711030 "Quantum Inequalities and Singular Energy Densities"
[9]: https://journals.aps.org/prd/abstract/10.1103/PhysRevD.76.025008 "Relativistic mechanics of Casimir apparatuses in a weak gravitational field | Phys. Rev. D"

### END NOTE - AUGUST 27 2026 - 01:00 CST



### BEGIN NOTE - AUGUST 27 2026 - 03:30 CST

# ANTIGRAVITY_RESEARCH — Comprehensive Carry-Forward Notes

## Session ending August 27, 2026 — Simulations 006B, 006C, and 006D

These notes supersede the scientific frontier described in the currently attached `NOTES.md` and `RESEARCH_BUILDPLAN.md` for the classical positive-energy branch. At the beginning of this session, the buildplan identified Simulation 006B as the highest-value classical experiment, followed by independent verification in 006C and finite-thickness/local-conservation work in 006D. All three of those gates have now been materially completed at the **linearized-GR model level**.

The central outcome is:

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

The appropriate scientific interpretation is therefore:

> **The project has constructed a theoretical existence example of local antigravity-like gravitational repulsion within linearized general relativity using a finite, positive-energy, locally conserved stress-energy distribution satisfying NEC/WEC/DEC. It has not demonstrated a realizable material, a stable apparatus, an exact nonlinear GR solution, or practical antigravity.**

The buildplan explicitly requires those accomplishments to remain separate; its success ladder places finite source and local conservation well below stability, physical realization, energetic plausibility, experimental accessibility, and a practical device.

---

# 1. Scientific state entering this session

Before this session, the project had already established or reproduced several important results:

- cosmological-$\Lambda$ defocusing;
- Kottler static-radius behavior and invariant tidal/geodesic-deviation confirmation;
- positive-energy defocusing for sufficiently negative pressure;
- the localization obstruction for a finite pure $w=-1$ region;
- the Israel-shell result showing that globally repulsive Schwarzschild exterior mass requires negative ADM mass and exotic shell energy in the studied construction;
- Reissner–Nordström local repulsion as an exact Einstein-Maxwell proof of principle, but with extreme electric-field/charge requirements;
- relativistic tension/domain-wall repulsion;
- the finite 005B supported tension disk with $C_{005B}\approx79.753148$;
- the abstract 006A static DEC/Laue result $C_{\mathrm{abstract}}=1$, which was explicitly **not** a universal physical lower bound because spatial geometry and local conservation were missing.

The previous notes therefore identified the unresolved classical problem as roughly

```math
1 \le C_{\mathrm{physical}} \le 79.753148
```

and called 006B the single most important next classical-GR calculation.

---

# 2. Regression baseline before new work

The first action in this session was to reconstruct and run the existing known-solution suite from the provided codebundle.

Result:

```text
BASELINE_TESTS=67
BASELINE_RESULT=67 PASSED
```

This cleared the buildplan's Phase A regression-integrity gate before extending the physics.

The original codebundle contained nine established scientific test files and reflected the repository before 006B was added.

After the new 006B regression tests were added, the suite increased to:

```text
CURRENT_EXPECTED_KNOWN_SOLUTION_TESTS=72
```

Every subsequent major simulation run in this session ended with:

```text
72 passed
```

The final observed regression result after 006D was:

```text
........................................................................ [100%]
72 passed in 0.92s
REGRESSION_RC=0
```

So the scientific regression baseline is currently green.

---

# 3. Simulation 006B — geometry-aware conserved DEC optimization

## 3.1 Original question

006A had shown that, abstractly, DEC permits a very optimistic mass scaling

```math
M \sim \frac{a h^2}{G}
```

with coefficient $C=1$, but the explicit finite 005B disk/rim architecture required

```math
C \approx 79.753148
```

The buildplan asked whether an explicit spatial geometry with pointwise positive energy, pointwise DEC, actual gravitational kernels, and **local** conservation would remain near $79.75$ or approach $1$.

The buildplan's research-decision ranges were:

```text
C ~ 1–5:
    exceptionally promising classical architecture

C ~ 10–100:
    geometry/local conservation impose a substantial penalty

C ~ 79.753:
    original disk/rim may already be near-efficient
```

Those were research-management ranges, not fundamental bounds.

---

# 4. 006B first slice — conserved thin radial optimizer

Rather than immediately paying the complexity cost of a complete 2D $r$-$z$ optimizer, we first attacked the cheapest nontrivial geometry-aware problem: an axisymmetric thin source with arbitrary radial stress structure.

The essential local conservation equation is

```math
\frac{d p_r}{d r}
+
\frac{p_r-p_\phi}{r}
=
0
```

or equivalently

```math
\frac{d(r p_r)}{d r}
=
p_\phi
```

The active weak-field source is

```math
S
=
U+p_r+p_\phi
```

The actual axial spatial kernel was used rather than the optimistic $1/h^2$ bound from 006A. The new source module documents this formulation explicitly.

## 4.1 Efficient conserved architecture discovered

A substantially better architecture than 005B was found.

### Inner region

For

```math
0 \le r \le a
```

use

```math
U=U_0
```

```math
p_r=-U_0
```

```math
p_\phi=-U_0
```

This region has negative active density and provides the local repulsive field.

### Stress-transfer annulus

For

```math
a < r < R
```

use

```math
U
=
U_0\frac{a^2}{r^2}
```

```math
p_r=-U
```

```math
p_\phi=+U
```

This transports the radial tension toward the outside while saturating DEC.

### Outer support

The thin limiting architecture has the minimum-energy support line

```math
\lambda
=
\frac{U_0 a^2}{R}
```

with positive hoop compression of equal magnitude.

This construction obeys local conservation distributionally in the ideal thin-source model and saturates the relevant DEC inequalities.

---

# 5. Closed-form 006B thin optimum

The dimensionless geometry variables were

```math
\alpha=\frac{a}{h}
```

and

```math
\beta=\frac{R}{h}
```

Optimization gave:

```text
INNER_RADIUS_OVER_H=1.437500564637
OUTER_RADIUS_OVER_H=4.701437405300
CLOSED_FORM_COEFFICIENT=23.426710175391
```

Compared with 005B:

```text
005B_COEFFICIENT=79.753148116012
006B_THIN_COEFFICIENT=23.426710175391
IMPROVEMENT_OVER_005B=3.404368241162x
```

Equivalently, the energy-equivalent coefficient fell by approximately 70.6%.

This directly falsified the hypothesis that the simple 005B disk-plus-single-rim architecture might already be near-optimal within the locally conserved axisymmetric thin DEC class.

The newly added 006B source and tests encode the expected optimum near

```text
alpha = 1.43750056
beta  = 4.70143745
C     = 23.426710175391
```

and explicitly classify it as a restricted architecture result rather than a universal GR lower bound.

---

# 6. Independent radial LP verification of 006B

We did not rely only on the closed-form derivation.

A separate discretized radial linear program used:

```text
U_i
q_i = r p_r
```

with conservation reconstructed through

```math
p_\phi
=
\frac{d(r p_r)}{d r}
```

It enforced cellwise:

```math
U \ge 0
```

```math
|p_r| \le U
```

```math
|p_\phi| \le U
```

and minimized total energy using the actual gravitational kernel.

Convergence was:

```text
N=50
C=23.279848767693
relative error=-6.268972749406e-03

N=100
C=23.390094671093
relative error=-1.562981059804e-03

N=200
C=23.417573464368
relative error=-3.900125521157e-04

N=400
C=23.424535334824
relative error=-9.283593602616e-05

N=800
C=23.426231369342
relative error=-2.043846726030e-05
```

The LP converges toward the independent closed-form value:

```text
C=23.426710175391
```

This is strong evidence that the identified piecewise conserved solution is the thin radial optimum or extremely close to it within that restricted class.

Simulation summary:

```text
REGRESSION_BASELINE_RECONSTRUCTED=YES
INDEPENDENT_LP_CONVERGENCE=PASS
POINTWISE_POSITIVE_ENERGY=YES
POINTWISE_DEC=YES
LOCAL_RADIAL_CONSERVATION=YES
ACTUAL_SPATIAL_GRAVITATIONAL_KERNEL=YES
TARGET_OUTWARD_ACCELERATION_NORMALIZED=YES
TOTAL_ENERGY_MINIMIZED=YES_WITHIN_THIN_RADIAL_SUBCLASS
```

Claim:

```text
NUMERICAL_OPTIMIZATION_RESULT
```

Not:

```text
FULL_2D_GLOBAL_GR_OPTIMUM
```

---

# 7. New 006B regression tests

A new regression file was added:

```text
tests/known_solutions/test_axisymmetric_thin_stress.py
```

Five focused tests passed:

```text
5 passed
```

They protect:

- the radial kernel primitive;
- integrated stress-trace cancellation;
- local conservation in the smooth regions;
- pointwise DEC;
- independent reconstruction of the 005B optimum;
- the improved 006B conserved-annular optimum.

The full suite consequently rose from 67 to:

```text
72 passed
```

and remained there through the rest of the session.

---

# 8. 006B full $r$-$z$ exact-DEC solver prerequisite

The next question was whether genuine 2D geometry and $r$-$z$ shear could improve on $C=23.4267$.

Allowing shear gives the spatial stress block

```math
\begin{pmatrix}
p_r & T_{rz} \\
T_{rz} & p_z
\end{pmatrix}
```

Diagonal inequalities alone are not sufficient for DEC once $T_{rz}\neq0$.

Exact type-I DEC requires the principal-stress eigenvalues to obey

```math
|\lambda_i| \le \epsilon
```

For the $r$-$z$ block this can be expressed as a second-order-cone constraint.

Therefore CVXPY was added.

## 8.1 Dependency change

Installed:

```text
cvxpy==1.9.2
```

Observed available solvers:

```text
CLARABEL
SCS
SCIPY
HIGHS
OSQP
```

`pyproject.toml` was modified to record:

```text
cvxpy==1.9.2
```

The environment installed transitive solver packages including Clarabel, SCS, OSQP, HiGHS, and related dependencies.

---

# 9. Exact DEC conic self-test

Before trusting the optimizer, an independent numerical equivalence test compared direct stress eigenvalues against the conic DEC constraint.

Test stress eigenvalues:

```text
-0.937056879750
-0.600000000000
+0.487056879750
```

Direct required energy density:

```text
DIRECT_DEC_MIN_EPSILON=0.937056879750
```

Conic optimizer result:

```text
CONIC_DEC_MIN_EPSILON=0.937056878751
```

Difference:

```text
ABSOLUTE_ERROR=9.996471428408e-10
RELATIVE_ERROR=1.066794518500e-09
```

Result:

```text
EXACT_DEC_SOC_EQUIVALENCE=PASS
POINTWISE_SHEAR_DEC_SOLVER_GATE=GREEN
```

This removed a potentially serious formulation error before the full 2D calculation.

---

# 10. Full $r$-$z$ staggered finite-volume optimizer

A second 006B simulation was added:

```text
simulations/006b_full_rz_decision.py
```

The formulation used:

```text
STRESS_GRID=STAGGERED_FINITE_VOLUME
LOCAL_CONSERVATION=EXACT_CELL_FORCE_BALANCE
DEC=EXACT_EIGENVALUE_SOC
KERNEL=EXACT_ANNULAR_CELL_INTEGRAL
```

Variables included:

```text
epsilon
p_phi
p_r on radial faces
p_z on vertical faces
T_rz on vertices
```

Staggering was deliberately used to reduce the risk of checkerboard/odd-even stress modes that can occur with naive collocated centered discretizations.

The solver also independently reconstructed:

- exact DEC eigenvalue violations;
- cell conservation residuals;
- integrated Laue balances;
- achieved acceleration.

---

# 11. Initial full $r$-$z$ finite-grid results

The first five cases gave:

```text
6x4, RMAX=5, depth=1
C=326.856547069958

8x6, RMAX=5, depth=1
C=80.635416635818

10x8, RMAX=5, depth=1
C=51.238386636844

8x6, RMAX=7, depth=2
C=76.194048456460

10x8, RMAX=7, depth=2
C=53.002083298871
```

All had:

```text
ACCELERATION≈1
DEC residuals tiny
conservation residuals tiny
integrated stress trace≈0
```

The best initial value was:

```text
51.238386636844
```

but it was immediately recognized as **not converged** because the compact refinement sequence fell extremely rapidly:

```text
326.86 -> 80.64 -> 51.24
```

Therefore we explicitly did **not** promote $51.24$ to a physical coefficient.

---

# 12. Important analytical observation about the full 2D problem

The full 2D optimization placed no lower limit on thickness and no upper limit on energy density.

Therefore the known thin solution can be approached as a distributional limiting sequence by concentrating energy/stress into a thinner layer.

Consequently, within the assumptions of this unrestricted continuum problem, there is no reason for the continuum full $r$-$z$ infimum to be forced *above* the known admissible thin value.

This was an important reason not to misinterpret coarse finite-volume values such as $51.24$ as physical lower bounds.

---

# 13. Thin-limit recovery using the independent full $r$-$z$ code

We deliberately forced the full $r$-$z$ solver into a thin slab and increased radial resolution.

Results:

```text
12x2
depth=0.125
C=48.782287947292

16x2
depth=0.125
C=37.700669553189

20x2
depth=0.125
C=32.954754666944
```

A simple $1/N_r^2$ extrapolation produced:

```text
THIN_EXTRAPOLATED_C=23.902968107527
```

or:

```text
THIN_EXTRAPOLATED_RATIO=1.020329697536
```

This is only about 2.03% above the independently derived exact thin coefficient:

```text
23.426710175391
```

This was a major validation of the full 2D formulation.

---

# 14. Matched-resolution depth experiment

Holding the grid scales fixed at

```text
dr=0.3125
dz=0.125
```

while increasing available depth gave:

```text
depth=0.5
C=39.446944669376

depth=1.0
C=34.637229670751

depth=2.0
C=30.331762534312
```

The nested-domain test behaved correctly:

```text
NESTED_DOMAIN_MONOTONICITY=PASS
```

Energy improvements were:

```text
0.5 -> 1.0:
12.1928708%

1.0 -> 2.0:
12.4301717%
```

This showed that genuine 2D stress routing had some value at finite resolution.

---

# 15. Extended depth-asymptote test

Further matched-resolution depth tests gave:

```text
depth=4
C=28.253514148213

depth=8
C=27.523479508905
```

The improvement from $4h$ to $8h$ fell to only:

```text
2.5838719937%
```

Therefore the depth benefit was clearly beginning to saturate.

This also produced an important engineering interpretation:

> Increasing source depth is an increase in source size, not free improvement. Even if deeper stress routing lowers total energy at fixed target stand-off, it may make the apparatus less compact.

No depth-only route toward $C\sim1$-$5$ appeared.

---

# 16. Radial convergence at depth $8h$

At fixed:

```text
depth=8
dz=0.125
RMAX=5
```

radial refinement gave:

```text
NR=16
C=27.523479508905

NR=20
C=27.162622405315

NR=24
C=27.020680149787
```

Simple extrapolations gave:

```text
1/NR^2 fit:
C_inf=26.598356460580

1/NR fit:
C_inf=25.976148873579
```

So at fixed $dz=0.125$, the apparent continuum limit remained above the thin result.

But this was not the end of the convergence analysis.

---

# 17. Vertical-refinement result — critical 006B observation

The decisive additional test held:

```text
NR=16
depth=8
RMAX=5
```

fixed while halving vertical spacing from:

```text
dz=0.125
```

to:

```text
dz=0.0625.
```

The coefficient fell from:

```text
27.523479508905
```

to:

```text
25.994503758080.
```

This showed that a substantial portion of the apparent $26$-$27$ plateau was a **vertical-discretization artifact**.

The new case also remained numerically excellent:

```text
ACCELERATION=1.000000000014
MAX_DEC_VIOLATION=1.048e-09
MAX_CONSERVATION_RESIDUAL=1.350e-12
STRESS_TRACE_INTEGRAL=-1.891e-15
```

---

# 18. 2D continuum diagnostic

Using the available radial and vertical refinement points, four simple first-/second-order discretization models produced:

```text
radial order 1, vertical order 1:
C=22.949343418307

radial order 1, vertical order 2:
C=23.958278570064

radial order 2, vertical order 1:
C=23.556385155751

radial order 2, vertical order 2:
C=24.570375590694
```

Thus the depth-88 continuum diagnostic bracket was:

```text
22.949343418307
to
24.570375590694
```

The independent thin coefficient

```text
23.426710175391
```

lies inside this bracket.

After applying the diagnostic residual depth correction, the combined depth/grid bracket was:

```text
22.554042171855
to
24.175074344242
```

Again:

```text
23.426710175391
```

lies inside it.

Final 006B 2D interpretation:

```text
FULL_RZ_CONTINUUM_EVIDENCE=CONSISTENT_WITH_THIN_REFERENCE
VERIFIED_FULL_RZ_IMPROVEMENT_BELOW_THIN=NO
VERIFIED_FINITE_2D_PENALTY_ABOVE_THIN=NO
C_1_TO_5_ROUTE_FOUND=NO
GLOBAL_FULL_RZ_OPTIMUM=NOT_ESTABLISHED
```

The extrapolation itself remains diagnostic rather than proof.

---

# 19. Final 006B decision

The strong result of 006B is not a universal theorem that $C=23.4267$.

The defensible result is:

> Within the most mature static, axisymmetric, positive-energy, DEC-constrained, locally conserved linearized-GR architectures studied so far, the energy coefficient is of order $20$-$25$, with a rigorously characterized restricted thin architecture at $C=23.426710175391$. No evidence was found for a dramatic collapse to $C\sim1$-$5$.

This places the classical problem firmly in the buildplan's

```text
C ~ 10–100
```

decision regime, meaning spatial geometry and conservation impose a substantial penalty relative to the abstract 006A coefficient $C=1$.

---

# 20. Physical scaling of the best 006B architecture

Using

```math
M
=
C\frac{a h^2}{G}
```

with

```text
C≈23.4267
a=1g
```

gives approximately:

```text
h=1 m:
M≈3.44e12 kg

h=1 cm:
M≈3.44e8 kg

h=1 mm:
M≈3.44e6 kg

h=1 micrometer:
M≈3.44 kg
```

For $h=1\ \mathrm{m}$, the energy equivalent is roughly:

```text
E≈3.09e29 J
```

Even the abstract $C=1$ result would still require roughly:

```text
1.47e11 kg
```

of mass-energy equivalent for $1g$ at $1\ \mathrm{m}$.

This is why reducing $C$ from $79.75$ to $23.43$ is scientifically important but does not solve the practical energy problem.

---

# 21. Simulation 006C — independent 005B Green-function verification

The buildplan explicitly required the 005B gravitational field to be reconstructed without reusing its analytic production formula before treating $79.753148$ as highly reliable.

A new simulation was created:

```text
simulations/006c_independent_finite_disk_field.py
```

Its primary computation directly numerically integrates the linearized gravitational Green function over:

- the membrane active stress-energy;
- the complete support rim contribution.

Only after the independent values are obtained is the production 005B field implementation imported for comparison.

---

# 22. 006C initial numerical failure and repair

The first 006C run already produced an extremely strong field comparison:

```text
COMPARISON_POINT_COUNT=30
MAX_ABSOLUTE_FIELD_ERROR=2.220446049250e-16
MAX_RELATIVE_FIELD_ERROR=1.419475206905e-15
FIELD_GRID_MATCH=PASS
```

However, the root finder then failed.

Cause:

- the independent membrane radial integral was evaluated at $y=z/R=10^{-6}$;
- the original adaptive radial quadrature became sharply localized near $r=0$;
- SciPy emitted an integration warning;
- the inaccurate endpoint value prevented `brentq` from seeing the correct sign-changing bracket.

This was a numerical-conditioning problem, not a physics disagreement.

A separate shell-harness problem was also discovered:

```text
python ... | tee ...
```

without `set -o pipefail` caused the shell to report the success code from `tee` instead of the crashed Python process.

That workflow bug was corrected.

---

# 23. 006C stable Green-function coordinate transform

The numerical integration was repaired using the variable transformation

```math
r
=
y\tan\theta
```

The problematic radial kernel

```math
\int_0^1
\frac{y r}{(r^2+y^2)^{3/2}}
\,dr
```

becomes the regular numerical integral

```math
\int_0^{\arctan(1/y)}
\sin\theta
\,d\theta
```

The transformed integral was **still evaluated numerically**.

The code did not substitute the known analytic 005B field formula.

The root finder was also changed to scan the independently computed field and discover its own sign-changing interval rather than assuming the known root.

---

# 24. Final 006C results

The repaired implementation produced:

```text
FIELD GRID:
30 comparison points

MAX_ABSOLUTE_FIELD_ERROR=
2.220446049250e-16

MAX_RELATIVE_FIELD_ERROR=
1.419475206905e-15

FIELD_GRID_MATCH=PASS
```

Independent repulsive zero:

```text
NUMERIC_Z_ZERO_OVER_R=
0.393319893190334

REFERENCE_Z_ZERO_OVER_R=
0.393319893190329

ABSOLUTE_ERROR=
4.773959005888e-15

REPULSIVE_ZERO_MATCH=PASS
```

Independent optimized geometry:

```text
OPTIMAL_H_OVER_R=
0.249616231845956

OPTIMAL_R_OVER_H=
4.006149730747969

REFERENCE_R_OVER_H=
4.006149670781000

ABSOLUTE_ERROR=
5.996696916810e-08
```

Independent coefficient:

```text
NUMERIC_005B_COEFFICIENT=
79.753148116012255

REFERENCE_005B_COEFFICIENT=
79.753148116011999

ABSOLUTE_ERROR=
2.557953848736e-13
```

Final:

```text
FIELD_GRID_VERIFIED=YES
REPULSIVE_ZERO_VERIFIED=YES
005B_OPTIMUM_VERIFIED=YES
SIMULATION_006C=GREEN
CLAIM_CLASSIFICATION=INDEPENDENT_NUMERICAL_VERIFICATION
```

This materially upgrades confidence in Simulation 005B.

---

# 25. Simulation 006D — finite-thickness conserved source

The buildplan's Phase D required replacing ideal membranes/rims with finite-thickness stress-energy and explicitly evaluating local conservation and energy conditions throughout the source.

A new simulation was created:

```text
simulations/006d_finite_thickness_conserved_source.py
```

This produced the strongest project-derived classical result so far.

---

# 26. Central 006D analytical construction

Define

```math
q(r)
=
r p_r(r)
```

Then impose

```math
p_\phi(r)
=
\frac{d q}{d r}
```

With

```math
p_z=0
```

and

```math
T_{rz}=0
```

the static cylindrical radial conservation equation becomes identically

```math
\frac{d p_r}{d r}
+
\frac{p_r-p_\phi}{r}
=
0
```

Equivalently:

```math
\frac{1}{r}
\left[
\frac{d(r p_r)}{d r}
-
p_\phi
\right]
=
0
```

The vertical conservation equation is also identically satisfied because:

```text
p_z=0
T_rz=0.
```

---

# 27. Finite vertical thickness

The complete in-plane energy/stress distribution was multiplied by a smooth, compact, nonnegative finite-thickness vertical profile.

The tested slab occupies:

```math
-t \le z \le 0
```

with target surface stand-off $h=1$.

A normalized compact polynomial bump of the form

```math
30x^2(1-x)^2
```

was used across the slab.

Because all components carrying a $z$ index are zero, multiplying the in-plane conserved source by this static $z$ profile does not generate a new vertical stress divergence in the linearized flat-background conservation equations.

This converts the zero-thickness source into a genuine nonzero-thickness distribution.

---

# 28. Finite radial support collar

The singular thin support line of 006B was removed.

A smooth cubic `smoothstep` transition was used to bring $q(r)$ continuously to zero over a finite outer radial collar.

At the outer boundary:

```text
q=0
dq/dr=0
```

so there is no remaining hidden line force.

The inner transition was also smoothed.

Therefore 006D has:

```text
SINGULAR_OUTER_RING=NO
FINITE_RADIAL_SUPPORT_COLLAR=YES
```

This falsifies the idea that the repulsive architecture intrinsically requires an ideal singular rim.

---

# 29. Pointwise energy conditions in 006D

Energy density was chosen as

```math
\epsilon
=
\max\left(
|p_r|,
|p_\phi|
\right)
```

With $p_z=0$, this enforces the static type-I DEC by construction.

The numerical checks found:

```text
MAX_DEC_VIOLATION=
0.000000000000e+00

MIN_NEC_MARGIN=
0.000000000000e+00
```

Therefore:

```text
NEC=PASS
WEC=PASS
DEC=PASS
POINTWISE_POSITIVE_ENERGY=YES
```

The zero NEC margin means parts of the optimized source **saturate** the energy condition; it does not mean the check was absent.

---

# 30. Local-conservation verification in 006D

Although the source is analytically constructed to satisfy radial conservation, an independent control-volume reconstruction was also performed.

Result:

```text
MAX_CONTROL_VOLUME_CONSERVATION_RESIDUAL=
3.103073353827e-14
```

Integrated stress balance:

```text
MAX_INTEGRATED_STRESS_TRACE=
2.922107000813e-13
```

Therefore:

```text
LOCAL_CONSERVATION=PASS
LAUE_STRESS_BALANCE=PASS
```

This is local conservation at the **linearized/static background order**.

It is not yet an exact nonlinear demonstration of:

```math
\nabla_\mu T^{\mu\nu}=0
```

in the self-consistent full metric.

The simulation correctly prints:

```text
EXACT_NONLINEAR_GR_CONSERVATION=NOT_ESTABLISHED
```

---

# 31. 006D finite-thickness convergence

The finite thickness and outer support-collar scale were reduced systematically.

Results:

```text
scale=0.40000
thickness/h=0.40000
C=38.037638025730

scale=0.20000
thickness/h=0.20000
C=29.559369544823

scale=0.10000
thickness/h=0.10000
C=26.258214373557

scale=0.05000
thickness/h=0.05000
C=24.789414887263

scale=0.02500
thickness/h=0.02500
C=24.095429926871

scale=0.01250
thickness/h=0.01250
C=23.757986246352

scale=0.00625
thickness/h=0.00625
C=23.591586299249
```

The independently established thin limit is:

```text
23.426710175391
```

The finest finite source differs by only:

```text
0.7037954651904%
```

Result:

```text
MONOTONIC_APPROACH_TO_THIN=YES
THIN_LIMIT_RECOVERY=PASS
```

---

# 32. Final 006D result

Final terminal classification:

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

C_FINITE_BEST_TESTED=
23.591586299249

C_THIN_LIMIT=
23.426710175391

SIMULATION_006D=GREEN

CLAIM_CLASSIFICATION=
CONSTRUCTIVE_LINEARIZED_GR_STRESS_ENERGY_RESULT
```

The simulation correctly retains:

```text
EXACT_NONLINEAR_GR_CONSERVATION=NOT_ESTABLISHED
DYNAMIC_STABILITY=NOT_ESTABLISHED
KNOWN_MATERIAL_REALIZATION=NO
PRACTICAL_ANTIGRAVITY_DEVICE=NO
```

---

# 33. What 006D actually establishes

The strongest defensible project statement is now:

> **There exists, within static linearized general relativity, an explicit finite-radius, finite-thickness, nonsingular, positive-energy, locally conserved stress-energy distribution satisfying NEC/WEC/DEC that produces a locally outward gravitational field while retaining positive total/far-field gravitational mass.**

This is stronger than merely showing a negative active-density cell or an infinite domain wall.

It addresses:

- finite source;
- positive energy;
- classical energy conditions;
- support completion;
- local conservation;
- finite thickness;
- removal of the singular rim;
- local gravitational repulsion;
- positive far-field mass.

It remains a **stress-energy construction**, not a known material or device.

---

# 34. Current success-ladder position

Using the buildplan's success ladder, the project has now effectively reached approximately **Level 5 within the stated linearized-GR approximation**:

```text
LEVEL 0 — Mathematical sign:
YES

LEVEL 1 — Physical gravitational observable:
YES
Local outward acceleration of a neutral test body in the weak-field model.

LEVEL 2 — Established-theory consistency:
YES WITHIN LINEARIZED GR
NOT YET A SELF-CONSISTENT EXACT NONLINEAR SOLUTION

LEVEL 3 — Acceptable stress-energy characterized:
YES
Positive energy and NEC/WEC/DEC.

LEVEL 4 — Finite source:
YES

LEVEL 5 — Local conservation:
YES AT LINEARIZED/STATIC ORDER

LEVEL 6 — Stability:
NO

LEVEL 7 — Physical realization:
NO

LEVEL 8 — Energetic plausibility:
NO

LEVEL 9 — Experimental accessibility:
NO

LEVEL 10 — Practical antigravity:
NO
```

The formal ladder itself warns not to describe progress as reaching levels whose requirements have not been satisfied.

---

# 35. What was falsified or weakened in this session

Several hypotheses were materially weakened or falsified.

### Hypothesis: 005B might already be near-optimal

Falsified within the thin radial DEC/conservation subclass.

```text
79.753 -> 23.427
```

is a 3.404× improvement.

### Hypothesis: finite geometry/local conservation might permit $C\sim1$-$5$

Not supported.

All mature results remain approximately:

```text
C ~ 20–25
```

rather than:

```text
C ~ 1–5.
```

### Hypothesis: the coarse full $r$-$z$ $C=51.24$ represented a physical finite-thickness penalty

Falsified.

The value collapsed substantially under spatial refinement, particularly vertical refinement.

### Hypothesis: genuine 2D shear clearly beats the thin architecture

Not established.

Continuum diagnostics bracket the thin value rather than showing a stable coefficient below it.

### Hypothesis: finite thickness necessarily destroys the local repulsive source

Falsified within linearized GR.

006D gives an explicit finite-thickness sequence retaining the effect.

### Hypothesis: a singular support ring is required

Falsified.

A finite smooth radial support collar works.

### Hypothesis: positive energy plus DEC prevents local gravitational repulsion

Falsified within the stated linearized model.

006D has:

```text
epsilon >= 0
NEC/WEC/DEC pass
outward local field
```

simultaneously.

### Hypothesis: these results imply practical antigravity

Not supported.

Energetics, stability, material realization, and experiment remain unresolved.

---

# 36. Important terminology going forward

The older project notes already made this distinction, and it is now more important than ever.

### Local gravitational repulsion

A neutral test object in the relevant near-field region accelerates away from the source.

```text
PROJECT_STATUS=YES
```

### Global gravitational repulsion

The entire isolated positive-total-mass source has an outward asymptotic gravitational field.

```text
PROJECT_STATUS=NO
```

The 006D far field remains attractive.

### Practical antigravity

A controllable physical apparatus generates useful gravitational repulsion with realizable material, energy, stability, and experimental requirements.

```text
PROJECT_STATUS=NO
```

Avoid using “antigravity proved” without explicitly attaching the word **local**, **theoretical**, and **within linearized GR**.

---

# 37. Current claim ledger

Recommended claim classifications:

```text
KNOWN_RESULT_REPRODUCED:
Cosmological-Lambda gravitational defocusing.

KNOWN_RESULT_REPRODUCED:
Kottler static-radius and tidal behavior.

KNOWN_RESULT_REPRODUCED:
Positive-energy relativistic tension/domain-wall repulsion.

KNOWN_RESULT_REPRODUCED:
Reissner-Nordstrom local repulsive region.

PROJECT_DERIVED_INDEPENDENTLY_VERIFIED_RESULT:
005B finite supported tension disk:
R/h ≈ 4.0061497
z_zero/R ≈ 0.393319893
C ≈ 79.753148116012.

PROJECT_DERIVED_NUMERICAL_OPTIMIZATION_RESULT:
006B thin locally conserved DEC architecture:
C = 23.426710175391.

PROJECT_DERIVED_NUMERICAL_OBSERVATION:
Full-rz optimizer continuum diagnostics are consistent with the thin
C≈23.43 result.
No stable 2D improvement below it has been demonstrated.

PROJECT_DERIVED_CONSTRUCTIVE_LINEARIZED_GR_STRESS_ENERGY_RESULT:
006D finite-radius, finite-thickness, locally conserved,
positive-energy NEC/WEC/DEC source with local outward gravity.

NOT_ESTABLISHED:
Exact nonlinear-GR realization.

NOT_ESTABLISHED:
Dynamical stability.

NOT_ESTABLISHED:
Known material/field realization.

NOT_ESTABLISHED:
Energetically practical antigravity.

NOT_ESTABLISHED:
Laboratory antigravity.

NOT_ESTABLISHED:
Practical antigravity device.
```

---

# 38. New and modified source files from this session

The following substantive files were added during this session:

```text
src/antigravity_research/geometry/axisymmetric_thin_stress.py

tests/known_solutions/test_axisymmetric_thin_stress.py

simulations/006b_geometry_aware_dec_optimizer.py

simulations/006b_full_rz_decision.py

simulations/006c_independent_finite_disk_field.py

simulations/006d_finite_thickness_conserved_source.py
```

Modified:

```text
pyproject.toml
```

to add:

```text
cvxpy==1.9.2
```

The 006B patch source itself documented the restricted thin architecture, assumptions, local conservation, DEC, validation plan, and explicit prohibition against promoting its coefficient to a universal GR bound.

---

# 39. New generated scientific outputs

Known generated files include:

```text
results/data/006b_geometry_aware_dec_optimizer.csv
results/figures/006b_geometry_aware_dec_convergence.png
results/logs/006b_geometry_aware_dec_optimizer.log

results/data/006b_full_rz_decision.csv
results/logs/006b_full_rz_decision.log

results/data/006b_depth_asymptote.csv

results/data/006c_independent_finite_disk_field.csv
results/logs/006c_independent_finite_disk_field.log

results/data/006d_finite_thickness_conserved_source.csv
results/logs/006d_finite_thickness_conserved_source.log
```

Some later 006B radial/vertical convergence experiments were run as inline terminal programs and **were not necessarily persisted into dedicated CSV/log files**.

Their important numbers must therefore be copied into `NOTES.md` or a consolidated result artifact before relying on the terminal history as the sole record.

---

# 40. Repository state / Git warning

The original codebundle already showed a dirty/untracked working tree before this session.

The last explicit `git status --short` shown during this session, before 006C/006D were added, included:

```text
M pyproject.toml

?? results/data/006b_full_rz_decision.csv
?? results/data/006b_geometry_aware_dec_optimizer.csv
?? results/figures/006b_geometry_aware_dec_convergence.png
?? results/logs/006b_full_rz_decision.log
?? results/logs/006b_geometry_aware_dec_optimizer.log

?? simulations/006b_full_rz_decision.py
?? simulations/006b_geometry_aware_dec_optimizer.py

?? src/antigravity_research/geometry/axisymmetric_thin_stress.py
?? tests/known_solutions/test_axisymmetric_thin_stress.py
```

006C and 006D were created afterward and are therefore also likely untracked unless separately saved/committed outside the shown terminal output.

**Do not assume this session is committed or pushed.**

First repository action next session:

```text
git status --short
```

Then inspect and preserve the complete scientific slice.

---

# 41. Regression protection still needed

Current full suite:

```text
72 passed
```

However, 006C and 006D are currently protected mainly by their simulation self-checks rather than dedicated known-solution regression files.

Before large refactors, add focused tests for at least:

### 006C

Protect:

```text
z_zero/R ≈ 0.393319893190334
R/h ≈ 4.00614973
C_005B ≈ 79.753148116012
```

and at least several direct Green-function field points.

### 006D

Protect:

- $q=r p_r$ conservation identity;
- $p_\phi=dq/dr$;
- outer collar termination;
- DEC;
- NEC/WEC;
- integrated stress balance;
- monotonic finite-thickness convergence;
- one or two benchmark coefficients;
- finest tested $C\approx23.5915863$.

The next expected regression count should rise above 72 once these are added.

---

# 42. Documentation that must be updated

The currently attached `RESEARCH_BUILDPLAN.md` is now scientifically stale because it still lists 006B/006C/006D as the active future path.

It should be updated to state:

```text
PHASE_A_REGRESSION=COMPLETE

PHASE_B_006B=COMPLETE_AT_DECISION_LEVEL
C_THIN=23.426710175391
FULL_RZ_EVIDENCE=CONSISTENT_WITH_THIN
C_1_TO_5_ROUTE_FOUND=NO

PHASE_C_006C=COMPLETE
005B_FIELD_INDEPENDENTLY_VERIFIED=YES

PHASE_D_006D=COMPLETE_AT_LINEARIZED_MODEL_LEVEL
FINITE_THICKNESS=YES
LOCAL_CONSERVATION=YES
NEC_WEC_DEC=YES
C_FINITE_BEST_TESTED=23.591586299249

CLASSICAL_DECISION_GATE=REACHED
```

Also update:

```text
NOTES.md
README.md
CLAIMS.md
ASSUMPTIONS.md
```

where appropriate.

Do not overwrite the historical 006A/005B discussion; append the new result and explicitly explain which earlier uncertainties were resolved.

---

# 43. Classical-GR decision gate

The buildplan states that after 006B, 006C, and 006D the project must make an explicit decision rather than indefinitely preserving the branch.

Its continuation criteria include:

- local conservation works;
- repulsive near field survives;
- coefficient falls substantially;
- plausible field-theory source exists;
- more optimization has clear expected value.

Our status is mixed:

```text
LOCAL_CONSERVATION=YES
REPULSIVE_FIELD_SURVIVES=YES
COEFFICIENT_REDUCED_SUBSTANTIALLY_FROM_005B=YES

PLAUSIBLE_FIELD_THEORY_REALIZATION=NO
ENERGY_REQUIREMENT_REMAINS_ENORMOUS=YES
MORE_STATIC_GEOMETRY_OPTIMIZATION_HIGH_VALUE=NO
```

Recommended decision:

```text
CLASSICAL_POSITIVE_ENERGY_STATIC_BRANCH=
PRESERVE_AS_STRONG_REFERENCE_RESULT

FURTHER_C_COEFFICIENT_TUNING=
DEPRIORITIZE

CLASSICAL_STABILITY_OR_REALIZABILITY_WORK=
ONLY_IF_A_SPECIFIC_PLAUSIBLE_MATTER_FIELD_MODEL_IS_IDENTIFIED

NEXT_PRIMARY_BRANCH=
QUANTUM_STRESS_ENERGY
```

This follows the buildplan stop rule rather than protecting sunk effort.

---

# 44. Why we should not spend the next session chasing $23.43\rightarrow20$

Even an order-unity coefficient cannot fix the fundamental scale

```math
M
\sim
\frac{a h^2}{G}
```

At $1g$ and $1\ \mathrm{m}$, even the abstract $C=1$ result still corresponds to approximately:

```text
1.47e11 kg
```

of mass-energy equivalent.

Therefore a modest coefficient improvement:

```text
23.4 -> 20
```

cannot alter the engineering conclusion.

A genuinely game-changing pathway must instead:

- change the scaling;
- exploit a fundamentally different source;
- find a large coherent/dynamical effect;
- use quantum stress-energy in a way not eliminated by complete-apparatus costs/QEIs;
- or eventually motivate an observationally viable modification of gravity.

---

# 45. Preliminary quantum reconnaissance performed this session

No 007-series repository simulation was completed.

However, the literature/analytical reconnaissance at the end of the session identified the correct next targets.

Brown and Maclay explicitly calculated the electromagnetic vacuum stress-energy tensor between perfectly conducting parallel plates, providing the foundational stress tensor needed for a proper Casimir calculation. ([APS Journals](https://journals.aps.org/pr/abstract/10.1103/PhysRev.184.1272 "Vacuum Stress between Conducting Plates: An Image Solution | Phys. Rev."))

Costa and Matsas showed that a complete Casimir apparatus held in equilibrium has nonnegative total mass when the additional supporting matter satisfies the DEC. This reinforces the project's rule that one must not count the negative vacuum region while ignoring the plates/support system. ([APS Journals](https://journals.aps.org/prd/abstract/10.1103/PhysRevD.105.085016 "Can quantum mechanics breed negative masses? | Phys. Rev. D"))

Ford and Roman established quantum-inequality constraints limiting the magnitude and duration of negative energy density in four-dimensional Minkowski spacetime for free quantum fields. ([DOI](https://doi.org/10.1103/PhysRevD.51.4277 "Averaged energy conditions and quantum inequalities | Phys. Rev. D"))

These support exactly the quantum sequence already specified in the buildplan.

---

# 46. Preliminary Casimir scale estimate — NOT YET SIMULATION 007A

For ideal parallel plates with separation $d$, the standard zero-temperature Casimir scale is

```math
K
=
\frac{\pi^2\hbar c}{720d^4}
```

For the ideal electromagnetic region, the active gravitational source is negative.

A simple infinite-plane linearized estimate gives the outward acceleration scale

```math
a_{\mathrm{Casimir}}
\sim
\frac{\pi^3G\hbar}{180c\,d^3}
```

Setting this optimistic ideal expression equal to $1g$ gives approximately:

```text
d ≈ 7.44e-19 m
```

which is vastly below ordinary nuclear dimensions.

This was **only an analytical reconnaissance estimate**.

It has not yet been promoted to a repository result and does not include the complete apparatus.

The complete-apparatus requirement is precisely why Simulation 007A must come next.

---

# 47. Highest-value next action — Simulation 007A

The buildplan already specifies the first quantum experiment:

## Simulation 007A — Complete Casimir Benchmark

It should model:

```text
negative Casimir-region stress-energy
plates
supports
total apparatus energy
total apparatus stress-energy
complete gravitational response
```

The crucial rule is:

> **Never calculate the gravitational benefit of the negative vacuum region without including the matter and stresses required to produce and hold the configuration.**

Primary outputs should include:

```text
vacuum energy density
principal stresses
active gravitational density
plate/support energy
total apparatus mass
local gravitational acceleration
far-field mass
dependence on separation d
energy-condition behavior of complete apparatus
```

Recommended spacing scan remains:

```text
1 mm
100 micrometers
10 micrometers
1 micrometer
100 nm
10 nm
1 nm
```

with smaller scales added only as a theoretical asymptotic benchmark.

---

# 48. Simulation 007B — quantum energy inequality bound

After 007A, implement the buildplan's QEI benchmark.

Question:

> Given spatial scale $h$ and sampling duration $\tau$, what negative stress-energy can established QFT sustain, and what is the corresponding maximum gravitational acceleration?

Target output:

```math
a_{\max}(h,\tau)
```

If the QEI result shows that useful negative-energy gravity requires nuclear, subnuclear, or still smaller scales, the quantum-vacuum branch can be deprioritized rapidly.

The buildplan explicitly identifies this as the second quantum gate.

---

# 49. Simulation 007C — dynamic sources

Only after 007A/007B, unless a cheaper analytic no-go check changes priority.

Candidate systems:

```text
scalar-field pulses
moving domain walls
oscillating anisotropic stresses
transient field configurations
retarded gravitational response
```

The project already has an important constraint:

Time dependence may relax static Laue/support relations, but it does **not** automatically evade pointwise stress-energy constraints.

The earlier notes therefore expected dynamics to perhaps improve order-unity coefficients rather than eliminate dozens of orders of magnitude of energy cost.

The key question for 007C should be:

> Can dynamics improve the **parametric scaling**, rather than merely modify $C$ by a factor of order unity?

If not, close it rapidly.

---

# 50. Modified gravity remains deferred

Do not jump to modified gravity yet.

The buildplan explicitly places modified gravity after established GR and QFT have been quantitatively constrained.

Later candidates may include:

```text
scalar-tensor
f(R)
Horndeski-type
vector-tensor
massive gravity
other observationally constrained extensions
```

Any candidate must be filtered by:

- theoretical motivation;
- ghost/pathology absence;
- solar-system constraints;
- gravitational-wave constraints;
- cosmology;
- stability;
- whether the repulsive behavior is actually physical rather than inserted by assumption.

---

# 51. Exact recommended next-session sequence

To maximize information gain and avoid losing this session's work:

1. **Run `git status --short`.**
   Determine exactly which 006B–006D files/results are untracked or modified.
2. **Preserve the milestone before more research.**
   Update `NOTES.md`, `RESEARCH_BUILDPLAN.md`, `README.md`, and `CLAIMS.md` with the results above.
3. **Add focused regression protection for 006C/006D.**
   Preserve the central independent-verification and conservation results.
4. **Run the complete known-solutions suite.**
   Current minimum expected count before adding tests:
   ```text
   72 passed
   ```
5. **Checkpoint/commit the entire classical gate.**
6. **Begin Simulation 007A.**
   Complete Casimir apparatus, not vacuum region alone.
7. **Run 007B QEI immediately after 007A unless 007A already decisively eliminates the branch.**
8. **Use 007C only if dynamics retains meaningful expected information gain.**
9. **Only after the quantum gate should modified gravity become active.**

---

# 52. Things not to do next

To preserve momentum:

```text
DO_NOT:
spend another session shaving C=23.43 to C=22 or C=20 without a new physical mechanism.

DO_NOT:
call the full-rz extrapolated 22.55 lower endpoint a discovered coefficient.

DO_NOT:
claim C=23.4267 is a universal GR lower bound.

DO_NOT:
claim 006D is a known-material solution.

DO_NOT:
claim exact nonlinear GR conservation.

DO_NOT:
claim dynamical stability.

DO_NOT:
claim global positive-mass repulsion.

DO_NOT:
claim an experimental antigravity effect.

DO_NOT:
claim practical antigravity is solved.

DO_NOT:
count Casimir negative energy while omitting the apparatus.

DO_NOT:
jump to modified gravity before the established-QFT gate is quantitatively closed.
```

---

# 53. Workflow lessons from this session

Several implementation lessons should be retained.

### Raw Python must not be pasted directly into zsh

Two early attempts generated:

```text
zsh: parse error near `)'
```

because Python/patch text was interpreted as shell syntax.

For direct multi-file creation, use complete quoted heredocs.

### Pipeline return codes need `pipefail`

Without:

```bash
set -o pipefail
```

a command like:

```bash
python simulation.py | tee log
```

may report the successful return code from `tee` even if Python crashed.

This happened during the first 006C run.

Future scientific run harnesses should use `pipefail`.

### Numerical root/bracket tests must not evaluate unnecessarily singular limits

006C's original y=10−6y=10^{-6} direct radial quadrature was poorly conditioned.

The variable transformation fixed it without sacrificing implementation independence.

### Convergence must be separated by direction

The full $r$-$z$ work demonstrated why a single mesh-refinement sequence can mislead:

- radial refinement alone suggested $C\sim26$;
- vertical refinement produced a large additional decrease;
- combined extrapolation then bracketed the thin result.

Future PDE/optimizer work must treat radial, vertical, domain-size, and model-regularization convergence separately.

---

# 54. Current scientific frontier after this session

Before this session, the central question was:

> Can a finite conserved positive-energy GR source actually produce useful local repulsion, or were the previous results artifacts of idealized stresses?

That question has been substantially answered at the linearized-model level.

The new frontier is:

> **What physically realizable matter/field mechanism—if any—can generate the required relativistic stress pattern, remain stable, and avoid the catastrophic ah2/Gah^2/G energy scale?**

For the classical static branch, no such mechanism has yet been identified.

Therefore the highest-information escape route is now established quantum stress-energy.

---

# 55. Project-level result to carry forward verbatim

Recommended concise statement:

> **ANTIGRAVITY_RESEARCH has established a project-derived constructive result in static linearized general relativity: a finite-radius, finite-thickness, nonsingular, positive-energy, locally conserved stress-energy configuration satisfying NEC, WEC, and DEC can generate a locally outward gravitational field while retaining positive far-field mass. The best verified thin architecture has $C=23.426710175391$ in $M=C a h^2/G$, and a finite-thickness regularization reaches $C=23.591586299249$, within 0.704% of that limit. Independent Green-function integration verifies the earlier 005B finite-disk result. No known material realization, dynamical stability, exact nonlinear-GR realization, energetic plausibility, experimental accessibility, or practical antigravity device has been established. The classical static coefficient-optimization branch should now be deprioritized in favor of the buildplan's quantum stress-energy gate, beginning with a complete Casimir apparatus benchmark and then quantum-energy-inequality bounds.**

That is the strongest scientifically conservative summary of where the project stands after this session.

### END NOTE - AUGUST 27 2026 - 03:30 CST



### BEGIN NOTE - AUGUST 28 2026 - 00:35 CST


# ANTIGRAVITY_RESEARCH — Comprehensive Carry-Forward Notes Through 009N

These notes are the authoritative conversational handoff for the next research session.

They summarize:

* the current scientific state;
* established results;
* project-derived results;
* negative results and closed branches;
* the exact status of the repository;
* permanent versus disposable calculations;
* Simulations/Gates 001 through 009N;
* current practical-antigravity probability calibration;
* literature/context that must be retained;
* unresolved theoretical and experimental questions;
* branches that must **not** be restarted;
* the highest-value surviving research directions;
* the exact decision logic for the next research slice.

The next session should read these notes together with:

```text
ANTIGRAVITY_RESEARCH_CODEBUNDLE_20260827-034521.md
RESEARCH_BUILDPLAN.md
FORMATTING_AND_CODE_STANDARDS.md
NOTES.md
README.md
```

Important: the current `RESEARCH_BUILDPLAN.md`, `README.md`, and older `NOTES.md` snapshot are now **substantially behind the live scientific frontier**. They remain authoritative for methodology, standards, definitions, and earlier verified results, but their stated active frontier around 006D/007 no longer reflects the actual work completed through 009N.

The next session must therefore use this handoff to avoid restarting completed work.

---

# 1. Governing scientific discipline

The central project goal remains:

> Determine whether physically consistent stress-energy configurations, spacetime geometries, quantum effects, or well-motivated extensions of established gravitational physics can produce controllable and measurable gravitational repulsion, while narrowing the search space toward physically realizable and ultimately practical mechanisms.

The project must continue to distinguish all of the following:

1. mathematical sign reversal;
2. invariant or operational local repulsion;
3. consistency with the governing field equations;
4. acceptable stress-energy;
5. finite localization;
6. local conservation;
7. stability;
8. physical field/material realization;
9. energetic plausibility;
10. experimental accessibility;
11. a useful practical apparatus.

A mathematical solution is not a device.

A locally repulsive field is not automatically a globally repulsive field.

A fifth force is not ordinary general-relativistic antigravity.

A measurable short-range repulsive force is not reactionless propulsion.

No project-derived calculation should be called a discovery until independently verified and compared with the literature.

---

# 2. GitHub mathematical formatting standard

All new Markdown must use the repository formatting standard.

Inline mathematics:

```markdown
The force range is $\lambda$.
```

Standalone mathematics:

````markdown
```math
a(r)
=
-\frac{GM}{r^2}
+
\frac{\Lambda c^2r}{3}
```
````

Do not use:

```text
\(...)
```

or:

```text
\[...\]
```

Do not append grammatical periods or commas inside display-math blocks.

For example:

```math
M
=
C\frac{ah^2}{G}
```

rather than putting a final period inside the equation.

---

# 3. Source-code documentation standard

All nontrivial permanent source or simulation files must contain unusually comprehensive top-of-file documentation covering:

* purpose;
* scientific question;
* physical model;
* governing equations;
* inputs and outputs;
* units;
* sign conventions;
* approximation level;
* assumptions;
* energy conditions where relevant;
* numerical method;
* validation strategy;
* limitations;
* related project files;
* claim classification.

Important functions need meaningful docstrings.

Important equations should be documented near their implementation.

Comments should explain why a calculation exists rather than simply translating code into English.

Do not permanently land speculative simulation machinery before the physics survives its cheapest decisive gate.

---

# 4. Research stop rules remain binding

The buildplan explicitly says to pause or reject a branch when:

* a fundamental physical assumption fails;
* independent verification fails;
* conservation fails;
* stability fails;
* known bounds exceed the required parameter range without a credible escape;
* repeated optimizations only change small coefficients while the remaining feasibility gap spans orders of magnitude;
* another branch has higher expected information value.

Do not protect sunk effort.

The 009-series work has followed this philosophy aggressively.

---

# 5. Critical meaning of a GREEN gate

This is especially important for the next session.

A gate ending with:

```text
...=GREEN
```

does **not** necessarily mean the physical mechanism survived.

It means:

> the gate executed successfully and produced the intended scientifically interpretable decision.

Examples:

```text
009I_TERRESTRIAL_SCREENING_COMPATIBILITY_GATE=GREEN
```

actually means the **monolithic terrestrial chameleon-vector route was rejected**.

Likewise:

```text
009N_ELECTROWEAK_CONSERVATION_GATE=GREEN
```

means the electroweak consistency falsification worked and the simplest gold-null vector realization was rejected.

Never count the number of GREEN outputs as progress toward a device.

---

# 6. Current repository / code state

The attached codebundle was generated:

```text
2026-08-27 03:45:32 CDT
```

with:

```text
branch: main
HEAD: 45a3e2060016f718f2f50a508260071de06815e5
included files: 76
working tree: DIRTY_OR_UNTRACKED
```

At codebundle generation time it showed:

```text
M NOTES.MD
```

However, subsequent work created additional untracked/permanent files.

The last explicit working-tree snapshot shown during the later research slice included approximately:

```text
?? results/data/008a_wall_current_loop_gate.csv
?? results/data/008b_distributed_field_representability_gate.csv
?? results/logs/008a_wall_current_loop_gate.log
?? results/logs/008b_distributed_field_representability_gate.log
?? simulations/008a_wall_current_loop_gate.py
?? simulations/008b_distributed_field_representability_gate.py
?? src/antigravity_research/geometry/canonical_scalar_representability.py
?? src/antigravity_research/geometry/charged_scalar_stability.py
?? src/antigravity_research/geometry/wall_current_loop.py
?? tests/known_solutions/test_006c_006d_regressions.py
?? tests/known_solutions/test_canonical_scalar_representability.py
?? tests/known_solutions/test_wall_current_loop.py
```

This may no longer be exact.

Therefore the **first repository command next session** must be:

```bash
git status --short
```

Do not assume anything has been committed since the codebundle snapshot.

---

# 7. Permanent versus disposable work

This distinction is essential.

## Permanent work known to have landed

Permanent 008A:

```text
src/antigravity_research/geometry/wall_current_loop.py
tests/known_solutions/test_wall_current_loop.py
simulations/008a_wall_current_loop_gate.py
results/data/008a_wall_current_loop_gate.csv
results/logs/008a_wall_current_loop_gate.log
```

Permanent 008B:

```text
src/antigravity_research/geometry/canonical_scalar_representability.py
tests/known_solutions/test_canonical_scalar_representability.py
simulations/008b_distributed_field_representability_gate.py
results/data/008b_distributed_field_representability_gate.csv
results/logs/008b_distributed_field_representability_gate.log
```

Permanent regression preservation:

```text
tests/known_solutions/test_006c_006d_regressions.py
```

A partial 008C source module was created:

```text
src/antigravity_research/geometry/charged_scalar_stability.py
```

but the associated permanent test and simulation were **not shown as successfully landed**.

The earlier shell attempt that was supposed to create the complete 008C slice exited with code 127.

Do not assume 008C is complete.

## Disposable-only work

The calculations from approximately 008C direct-gate onward, especially:

```text
008C
008D
008E
008F
009A
009B
009C
009D
009E
009F
009G
009H
009I
009J
009K
009L
009M
009N
```

were executed primarily as self-contained Python heredocs or literature/analytical gates.

Based on everything shown, **009A–009N did not permanently modify the repository**.

Do not search for `009*.py` and assume something went missing. Those simulations were intentionally disposable because the project was optimizing information gain before committing code.

---

# 8. Test-suite checkpoint

Permanent regression progression was:

```text
72 passed
```

after 006D.

Then:

```text
78 passed
```

after the six 006C/006D preservation tests.

Then:

```text
86 passed
```

after permanent 008A.

Then:

```text
94 passed
```

after permanent 008B.

Therefore the last verified full permanent baseline is:

```text
94 passed
```

No subsequent 009-series calculation intentionally changed the permanent test suite.

The next session should verify with:

```bash
ROOT="$(pwd)"
PY="$ROOT/.venv/bin/python"

PYTHONPATH="$ROOT/src" \
"$PY" -m pytest -q tests/known_solutions
```

Expected, unless files have changed:

```text
94 passed
```

Do not claim this expected count as current until it is actually rerun.

---

# 9. Shell-workflow lesson

Do not use `set -u` in the interactive macOS/zsh workflow.

An earlier shell slice interacted badly with shell variables such as `RPROMPT`.

For disposable gates prefer:

```bash
ROOT="$(pwd)"
PY="$ROOT/.venv/bin/python"

PYTHONPATH="$ROOT/src" "$PY" - <<'PY'
...
PY
```

Exit code:

```text
127
```

means a command/path failure, not a physics result.

---

# 10. Current overall scientific conclusion

The project has established with high confidence that **local repulsive gravitational behavior is possible within established general relativity**.

The core classical lesson remains:

```math
\text{gravity responds to the full stress-energy tensor, not merely positive mass density}
```

Large relativistic stresses or tensions can make the local active gravitational source repulsive even when energy density and total mass remain positive.

However, the best established-GR constructions retain catastrophic energetic scaling of approximately:

```math
M
=
C\frac{ah^2}{G}
```

with $C$ of order tens for the best explicit finite locally conserved source.

That prevents ordinary classical GR from presently constituting a plausible practical route.

The project therefore investigated quantum negative energy and then short-range repulsive fifth-force physics.

The fifth-force branch produced experimentally interesting possibilities but has not yet produced a healthy, allowed, human-scale practical mechanism.

---

# 11. Simulation 001A — Kottler / Schwarzschild–de Sitter

Weak-field acceleration:

```math
a(r)
=
-\frac{GM}{r^2}
+
\frac{\Lambda c^2r}{3}
```

Static radius:

```math
r_s
=
\left(
\frac{3GM}{\Lambda c^2}
\right)^{1/3}
```

For approximately $10^{12}M_\odot$:

```text
static radius ≈ 1.1139 Mpc
```

Classification:

```text
KNOWN_RESULT
REPRODUCED
```

Conclusion:

A positive cosmological constant creates genuine gravitational defocusing/repulsion, but the observed value of $\Lambda$ is useless for laboratory antigravity.

---

# 12. Simulation 001B — invariant Kottler tidal effect

Tidal eigenvalues:

```math
\lambda_r
=
\frac{2GM}{r^3}
+
\frac{\Lambda c^2}{3}
```

```math
\lambda_t
=
-\frac{GM}{r^3}
+
\frac{\Lambda c^2}{3}
```

This established that the effect is not merely coordinate acceleration.

Classification:

```text
KNOWN_RESULT
REPRODUCED
```

---

# 13. Simulation 002 — perfect-fluid defocusing

For a perfect fluid:

```math
\frac{\ddot\xi}{\xi}
=
-\frac{4\pi G}{3c^2}
(\epsilon+3p)
+
\frac{\Lambda c^2}{3}
```

Positive-energy defocusing is possible for:

```math
w<-\frac{1}{3}
```

For $w=-1$:

* NEC satisfied at equality;
* WEC satisfied;
* DEC satisfied;
* SEC violated.

A $1g$ effect over approximately $1$ m requires an energy density around:

```text
1.5763e27 J/m^3
```

Conclusion:

The sign is easy.

The energy scale is catastrophic.

---

# 14. Simulation 003A — finite vacuum-energy core

A $p=-\epsilon$ vacuum-energy region cannot simply taper smoothly to vacuum while maintaining the same equation of state and conservation.

A boundary layer or supporting stress is required.

A positive-energy core also produces positive exterior mass.

Conclusion:

Interior defocusing does not automatically generate an externally useful repulsive source.

---

# 15. Simulation 003B — Israel shell

The tested thin-shell construction required an unfavorable negative-ADM/exotic branch for outward Schwarzschild behavior.

This path was deprioritized.

Do not restart without a genuinely new analytical reason.

---

# 16. Simulation 004A — Reissner–Nordström / Einstein–Maxwell

Einstein–Maxwell provides a known example where:

* ADM mass is positive;
* Maxwell energy is positive;
* local neutral-particle gravitational repulsion can occur;
* the shell can satisfy WEC/DEC in the tested construction.

Repulsive radius:

```math
r_{\mathrm{rep}}
=
\frac{Q^2}
{4\pi\epsilon_0Mc^2}
```

For approximately $1g$ across $1$ m:

```text
electric field ≈ 2.67e19 V/m
```

which is roughly twenty times the Schwinger field.

A sub-Schwinger benchmark moved the scale to roughly:

```text
radius ≈ 407 m
mass ≈ 1.22e17 kg
charge ≈ 2.44e13 C
```

Classification:

```text
KNOWN_RESULT
REPRODUCED_REFERENCE_MECHANISM
```

Not an engineering route.

---

# 17. Simulation 005A — relativistic tension wall

Surface energy $U$ and tension:

```math
\tau=qU
```

Repulsion occurs for:

```math
q>\frac{1}{2}
```

DEC permits:

```math
q\le1
```

Therefore there is a positive-energy NEC/WEC/DEC-compatible repulsive region:

```math
\frac{1}{2}<q\le1
```

The optimal ideal domain-wall point is:

```math
q=1
```

For $1g$ planar acceleration:

```text
minimum U ≈ 2.1017e27 J/m^2
mass equivalent/area ≈ 2.3385e10 kg/m^2
```

Known domain-wall physics confirms the qualitative mechanism.

---

# 18. Simulation 005B — finite supported tension disk

The finite membrane needs compressive support.

For the optimized $q=1$ membrane plus minimum-DEC rim:

```text
R/h ≈ 4.00614967
zero crossing z/R ≈ 0.393319893
C ≈ 79.753148116
```

with:

```math
M
=
C\frac{ah^2}{G}
```

At $1g$, $h=1$ m:

```text
M ≈ 1.172e13 kg
```

Properties:

* positive energy;
* finite source;
* local repulsive near field;
* positive total mass;
* attractive far field;
* global mechanical balance.

This result was later independently verified.

---

# 19. Simulation 006A — abstract static DEC optimization

Within the stated abstract assumptions:

```text
optimistic coefficient C = 1
domain wall C = 2
finite supported disk C ≈ 79.753
```

Important:

```math
C=1
```

is **not** a universal theorem of GR.

It is an optimistic lower result inside the simplified optimization model.

At $1g$ and $1$ m:

```text
C = 1 mass scale ≈ 1.47e11 kg
```

Still catastrophic.

---

# 20. Simulation 006B — geometry-aware locally conserved thin source

This was the major classical optimization improvement.

Best verified thin architecture:

```text
C_thin = 23.426710175391
alpha = a/h = 1.437500564637
beta = R/h = 4.701437405300
```

The full finite-volume optimization did not verify a better coefficient.

Classification:

```text
PROJECT_DERIVED_NUMERICAL_OPTIMIZATION_RESULT
```

Not a universal GR lower bound.

---

# 21. Simulation 006C — independent Green-function verification

005B was independently reconstructed through a separate Green-function calculation.

Maximum absolute error:

```text
2.22e-16
```

relative error:

```text
1.419e-15
```

The independent calculation reproduced:

* zero location;
* $R/h$;
* mass coefficient.

Classification:

```text
INDEPENDENT_NUMERICAL_VERIFICATION
```

This considerably strengthened confidence in 005B.

---

# 22. Simulation 006D — finite-thickness locally conserved positive-energy source

This remains the strongest project-derived classical-GR source result.

The construction used an axisymmetric anisotropic stress architecture with:

```math
q(r)=rp_r
```

```math
p_\phi
=
\frac{dq}{dr}
```

```math
p_z=0
```

```math
T_{rz}=0
```

and:

```math
\epsilon
=
\max(
|p_r|,
|p_\phi|
)
```

Properties verified numerically:

* finite radius;
* finite thickness;
* nonsingular;
* positive energy density;
* local static conservation;
* NEC satisfied;
* WEC satisfied;
* DEC satisfied;
* locally outward gravitational field;
* positive far-field mass.

Best tested finite-thickness coefficient:

```text
C_finite = 23.591586299249
```

which is within approximately:

```text
0.704%
```

of the thin result.

Representative diagnostics:

```text
max conservation residual ≈ 3.103e-14
DEC violation = 0
minimum NEC margin = 0
integrated stress trace ≈ 2.922e-13
```

Classification:

```text
CONSTRUCTIVE_LINEARIZED_GR_STRESS_ENERGY_RESULT
```

Not established:

* exact nonlinear Einstein solution;
* complete dynamical stability;
* real material realization;
* experimentally accessible source;
* practical energy budget.

---

# 23. Classical-GR practicality conclusion

The strongest classical result still obeys:

```math
M
\sim
23.5\frac{ah^2}{G}
```

At approximately $1g$ and $1$ m this is on the order of:

```text
3.5e12 kg
```

The project therefore correctly stopped coefficient optimization.

Improving $C=23$ to $C=10$, $5$, or even $1$ does not solve the fundamental engineering problem.

Do not restart classical coefficient optimization unless a new mechanism changes the **parametric scaling** rather than merely the coefficient.

---

# 24. Quantum Simulation 007A — Casimir branch

Brown–Maclay ideal electromagnetic Casimir stress between perfect plates:

```math
K
=
\frac{\pi^2\hbar c}{720d^4}
```

with:

```math
\epsilon=-K
```

```math
p_x=p_y=+K
```

```math
p_z=-3K
```

Active gravitational combination:

```math
S
=
\epsilon+p_x+p_y+p_z
=
-2K
```

Thus the ideal vacuum region is locally repulsive in the relevant weak-field sense.

However the complete apparatus must include:

* plates;
* mechanical support;
* stabilizing stresses.

Published work such as Fulling et al. establishes that Casimir energy gravitates normally.

Costa and Matsas show that a mechanically complete DEC-supported Casimir apparatus has nonnegative total mass.

Vacuum-only planar acceleration:

```math
a_C
=
\frac{\pi^3G\hbar}
{180cd^3}
```

A $1g$ vacuum-only benchmark requires approximately:

```text
d ≈ 7.44e-19 m
```

This is physically useless.

Static Casimir antigravity is therefore strongly deprioritized.

---

# 25. Quantum Simulation 007B — quantum inequality gate

For the electromagnetic Lorentzian quantum inequality, the coefficient used was approximately:

```text
alpha_QI = 27/(1024 pi^2)
         ≈ 0.00267155
```

An optimistic acceleration scale:

```math
a_{\max}
=
\frac{4\pi\alpha_{\mathrm{QI}}G\hbar}
{c^4\tau^3}
```

Ignoring causality, $1g$ would require:

```text
tau ≈ 1.44e-27 s
c tau ≈ 4.32e-19 m
```

Imposing the causal near-zone requirement:

```math
\tau
\ge
\frac{h}{c}
```

gives:

```math
a_{\max}(h)
=
\frac{4\pi\alpha_{\mathrm{QI}}G\hbar}
{ch^3}
```

At:

```text
h = 1 m
```

the result is approximately:

```text
7.88e-55 m/s^2
```

A $1g$ effect again requires:

```text
h ≈ 4.32e-19 m
```

Conclusion:

The specific free-electromagnetic-field QEI route is catastrophically far from macroscopic usefulness.

This is not a universal no-go theorem for every quantum field theory.

But the established free-EM negative-energy loophole is closed for practical purposes.

---

# 26. 008A — finite wall plus current-loop support

A physically motivated alternative to the abstract collar was tested.

Effective energy:

```math
E(R)
=
\pi\sigma R^2
+
2\pi\mu R
+
\frac{J}{R}
```

Equilibrium:

```math
J
=
2\pi R^2(\sigma R+\mu)
```

The radial second derivative at equilibrium is positive.

Boundary energy/tension:

```math
U_b
=
\sigma R+2\mu
```

```math
T_b
=
-\sigma R
```

DEC requires:

```math
\mu\ge0
```

Results:

```text
m = 0 exactly reproduces the 005B q=1 limit
positive bare string energy worsens the coefficient
```

Decision:

```text
WALL_PLUS_CURRENT_LOOP_IMPROVES_006D=NO
```

The distributed collar remained more efficient.

Permanent source/tests/simulation were created.

---

# 27. 008B — canonical scalar representability

For static canonical real scalar fields:

```math
T_{ij}
=
M_{ij}
-
\rho\delta_{ij}
```

with local Gram components:

```math
M_{ii}
=
\rho+p_i
```

and potential:

```math
V
=
-\frac{1}{2}
\left(
\rho+\sum_i p_i
\right)
```

The 006D DEC structure makes the local Gram matrix positive semidefinite.

Therefore the stress tensor is **locally algebraically representable** by canonical scalar gradients.

However:

* a strictly axisymmetric real scalar has no $\phi$ gradient;
* 006D requires a nonzero azimuthal Gram sector;
* parts of the outer collar can require local rank 3.

Minimum local real-scalar component count:

```text
3
```

A Derrick scaling argument for a purely static canonical scalar gives:

```math
E(\lambda)
=
\frac{K}{\lambda}
+
\frac{U}{\lambda^3}
```

At stationary pressure:

```math
E''(1)
=
-3E
```

so the purely static canonical-scalar realization is dilation unstable.

Decisions:

```text
LOCAL_ALGEBRAIC_REPRESENTABILITY=YES
STRICT_AXISYMMETRIC_REAL_SCALAR=INSUFFICIENT
PURE_STATIC_CANONICAL_SCALAR_DERRICK_STABLE=NO
```

Therefore stabilization requires something like:

* time-dependent charge;
* current;
* gauge sector;
* higher derivatives;
* other additional physics.

Permanent source/tests/simulation were created.

---

# 28. 008C — fixed-charge dilation stability capacity

A stationary charged canonical scalar supplies a temporal kinetic component.

Define:

```math
D
=
\sum_a \dot\phi_a^2
```

with local capacity:

```math
D_{\max}
=
\min_i(\rho+p_i)
```

and:

```math
T
=
\frac{D}{2}
```

At fixed charge under dilation:

```math
E_Q(\lambda)
=
\lambda^3T
+
\frac{K}{\lambda}
+
\frac{U}{\lambda^3}
```

The second derivative satisfies:

```math
E_Q''(1)
=
24T
-
3E
-
5P
```

For approximately zero pressure:

```math
P\approx0
```

positive dilation curvature requires:

```math
\frac{T}{E}
>
\frac{1}{8}
```

At the finest tested 006D scale:

```text
Tmax/E = 0.186185265139
critical = 0.125
available/required = 1.489482121109
required fraction of capacity = 0.671374288975
maximum curvature/E = 1.468446363326
P/E ≈ 2.63e-14
```

Capacity localization was overwhelmingly in the outer collar:

```text
core ≈ 0
inner transition ≈ 0.0189%
transfer ≈ 0
outer collar ≈ 99.9811%
```

Decision:

```text
FIXED_CHARGE_DILATION_WINDOW=SURVIVES
EXACT_006D_STRESS_HAS_SUFFICIENT_TEMPORAL_KINETIC_CAPACITY=YES
GLOBAL_COMPLEX_SCALAR_SOLUTION=NOT_ESTABLISHED
FULL_DYNAMIC_STABILITY=NOT_ESTABLISHED
008C_DIRECT_GATE=GREEN
```

Important:

This only proves enough local temporal kinetic *capacity* exists to cure one Derrick dilation mode.

It does not construct a global field solution.

Permanent implementation is incomplete.

---

# 29. 008D — charged/winding sector separation

For one stationary complex scalar:

```math
\Phi
=
f e^{i(n\phi-\omega t)}
```

simultaneous temporal and angular gradient sectors imply:

```math
|T_{t\phi}|
=
\sqrt{DA}
```

The 006D target is static and diagonal:

```math
T_{t\phi}=0
```

The transfer annulus can require azimuthal stress while allowing:

```math
D_{\max}=0
```

Therefore a single charged winding scalar cannot realize the exact stress tensor.

Representative transfer point:

```text
r ≈ 3.06947
epsilon ≈ 0.2193257
p_r = -epsilon
p_phi = +epsilon
Dmax = 0
angular Gram ≈ 0.4386514
```

Representative outer-collar point:

```text
r ≈ 4.70456
epsilon ≈ 105.463
Dmax ≈ 105.416
D allocation ≈ 70.7738
angular remaining ≈ 140.152
T_tphi ≈ 99.5947
T_tphi/epsilon ≈ 0.94436
```

Dense audit:

```text
6932 / 10001 points
```

required angular stress but forbade nonzero charge capacity.

Only:

```text
15 points
```

simultaneously permitted nonzero charge capacity in that audit.

Decisions:

```text
ONE_COMPLEX_SCALAR_EXACT_006D_REALIZATION=REJECTED
STATIC_ANGULAR_SECTOR_AND_CHARGED_STABILIZER_MUST_BE_SEPARATED=YES
COUNTER_WINDING_PAIR_ALGEBRAIC_CANCELLATION=YES
008D_SECTOR_SEPARATION_GATE=GREEN
```

---

# 30. 008E — ungauged winding global-integrability gate

For a finite collection of ungauged canonical winding scalars, a necessary inequality was derived:

```math
N
\ge
\frac{
\left|
\frac{d}{dr}
\left(
r\sqrt{A}
\right)
\right|
}{
\sqrt{G_r}
}
```

where $N$ is maximum winding.

Near the outer boundary:

```text
delta/w = 0.1     N ≈ 6.73e3
delta/w = 0.03    N ≈ 2.45e4
delta/w = 0.01    N ≈ 7.50e4
delta/w = 0.003   N ≈ 2.52e5
delta/w = 0.001   N ≈ 7.57e5
delta/w = 0.0003  N ≈ 2.52e6
delta/w = 0.0001  N ≈ 7.57e6
```

The asymptotic behavior is:

```math
N
\sim
\frac{757}
{\delta/w}
```

so:

```math
N\to\infty
```

at the outer termination.

The disposable script initially printed the wrong asymptotic decision because a ratio was computed backwards.

That was a **test-logic bug, not a physics failure**.

Correct classification:

```text
FINITE_UNGAUGED_WINDING_SET_CAN_EXACTLY_REALIZE_006D_OUTER_TERMINATION=NO
UNGAUGED_CANONICAL_WINDING_GLOBAL_INTEGRABILITY=REJECTED
008C_FIXED_CHARGE_STABILITY_WINDOW=STILL_SURVIVES
006D_STRESS_TENSOR_ITSELF_INVALIDATED=NO
GAUGE_OR_OTHER_COMPENSATING_SECTOR_NOW_REQUIRED=YES
008E_GLOBAL_INTEGRABILITY_GATE=GREEN
```

---

# 31. 008F — local gauge boundary takeover

For the outer 006D collar:

```math
p_\phi=\epsilon
```

with:

```math
p_r\le0
```

```math
p_z=0
```

Define:

```math
g
=
\epsilon+p_r
```

An exact local decomposition exists:

Gauge sector:

```math
T_g
=
(g,0,g,0)
```

Residual scalar sector:

```math
T_s
=
(-p_r,p_r,-p_r,0)
```

The residual scalar Gram matrix is positive semidefinite.

The gate conservatively removed charged-scalar temporal capacity from an outer gauge layer and found how much layer could be replaced before fixed-charge Derrick stability failed.

Results:

```text
5% takeover:
T/E ≈ 0.18484

10%:
T/E ≈ 0.18097

20%:
T/E ≈ 0.16683

25%:
T/E ≈ 0.15710

30%:
T/E ≈ 0.14598
curvature/E ≈ 0.50344
gauge energy/E ≈ 0.08042

35%:
T/E ≈ 0.13374

38%:
T/E ≈ 0.12597
curvature/E ≈ 0.02337
```

Critical takeover width:

```text
≈ 38.3694%
```

Decisions:

```text
OUTER_COLLAR_HAS_EXACT_LOCAL_MAXWELL_PAIR_DECOMPOSITION=YES
FINITE_GAUGE_BOUNDARY_LAYER_COMPATIBLE_WITH_DERRICK_STABILITY=YES
THIRTY_PERCENT_GAUGE_TAKEOVER=YES
CHARGED_STABILIZER_AND_GAUGE_HAVE_NONZERO_BUDGET_WINDOW=YES
GLOBAL_SMOOTH_GAUGE_POTENTIALS=NOT_ESTABLISHED
008F_GAUGE_TAKEOVER_GATE=GREEN
```

Meaning:

There is a mathematically nonempty local field-theory realization window.

But none of this changes the catastrophic GR scaling.

Therefore the branch was correctly deprioritized before building a complicated global field solution.

---

# 32. Strategic pivot after 008F

The most important realization after 008F was:

> Even increasingly realistic field-theory realizations of 006D still inherit the same catastrophic $a h^2/G$ scaling.

Therefore a practical route requires **changing the interaction scale or effective coupling**, not merely reducing coefficient $C$.

Only after the established GR and quantum branches had been quantitatively squeezed did the project move into modified/fifth-force physics.

This was consistent with the original anti-drift rule.

---

# 33. 009A — generic repulsive Yukawa scaling escape

Potential convention:

```math
V(r)
=
-\frac{Gm_1m_2}{r}
\left[
1+\alpha e^{-r/\lambda}
\right]
```

Repulsion requires:

```math
\alpha<0
```

For a thick planar source:

```math
a_N
=
2\pi G\rho T
```

and the repulsive Yukawa magnitude is:

```math
a_Y
=
2\pi G\rho|\alpha|
\lambda
e^{-z/\lambda}
\left(
1-e^{-T/\lambda}
\right)
```

Benchmark:

```text
rho = 19300 kg/m^3
lambda = 10 um
T = 100 um
z = 10 um
```

Results:

```text
Newtonian acceleration ≈ 8.09e-10 m/s^2
Yukawa acceleration per |alpha| ≈ 2.98e-11 m/s^2
sign reversal |alpha| ≈ 27.18
net 1e-9 m/s^2 |alpha| ≈ 60.77
1g |alpha| ≈ 3.29e11
```

Decision:

```text
GENERIC_REPULSIVE_YUKAWA_CAN_REVERSE_FORCE=YES
LAB_MICROSCALE_REPULSION_POSSIBLE_IF_FORCE_EXISTS=YES
ONE_G_AT_10UM=NO
NEW_PHYSICS_REQUIRED=YES
009A_SCALING_ESCAPE_GATE=GREEN
```

This is a fifth force, not GR antigravity.

---

# 34. 009B — concrete $U(1)_{B-L}$ vector branch

A healthy concrete vector model was chosen.

For neutral atoms:

```math
B-L
\approx
N
```

because proton baryon charge and electron lepton charge cancel, leaving neutron number.

A massive vector exchanged between like $B-L$ charges is repulsive.

Standard anomaly cancellation can be achieved with three right-handed neutrinos.

Approximate material-dependent Yukawa strength:

```math
\alpha
=
\frac{\hbar c}{G}
\frac{g_{B-L}^2}
{4\pi m_p^2}
F_1F_2
```

For tungsten/gold:

```text
F_W ≈ 0.597826
F_Au ≈ 0.598985
```

At:

```text
g_BL = 1e-16
```

the effective strength was:

```text
alpha_eff ≈ 4.82477e4
```

The historical Stanford inverse-square-law points suggested potentially measurable micron-scale repulsion.

However those historical limits were not the strongest modern constraint everywhere.

The 2016 Casimir-less experiment later became the more important comparison.

---

# 35. 009C — modernized $B-L$ experimental synthesis

Primary experimental reference:

Chen et al., 2016:

```text
Phys. Rev. Lett. 116, 221102
arXiv:1410.7267
```

Important experiment features:

* approximately $149.3,\mu$m sphere radius;
* sapphire sphere;
* 10 nm Cr + 250 nm Au coating;
* rotating source;
* common 150 nm Au + 10 nm Cr coating;
* structured Au/Si source below coating;
* structured depth approximately 2.10 µm;
* gaps approximately 200–1000 nm;
* common Au layer suppresses differential Casimir background by more than roughly $10^6$;
* thermal force noise near 6 fN/$\sqrt{\mathrm{Hz}}$;
* measured short-gap random noise could be closer to 12 fN/$\sqrt{\mathrm{Hz}}$ due to wobble;
* long-integration differential force sensitivity approximately 0.1–0.2 fN.

For:

```text
g_BL = 1e-16
```

project recast differential forces were approximately:

```text
4 um:  0.0344 fN
5 um:  0.0549 fN
6 um:  0.0801 fN
7 um:  0.1101 fN
8 um:  0.1447 fN
```

A hypothetical hybrid combining the 2016 Casimir-less geometry with a 2008-style cryogenic 0.2 fN/$\sqrt{\mathrm{Hz}}$ force sensor yielded, for a 50% signal-transfer assumption at 6 µm:

```text
signal ≈ 0.0401 fN
1 h noise ≈ 0.00333 fN
SNR 1 h ≈ 12.0
SNR 24 h ≈ 58.9
5-sigma time ≈ 623 s
g reach 1 h ≈ 6.45e-17
g reach 24 h ≈ 2.91e-17
```

This was only a synthesis of separately demonstrated technologies.

It was not claimed as an existing apparatus.

---

# 36. CANNEX strategic improvement

CANNEX emerged as a better direct plane-parallel platform.

Important paper:

```text
arXiv:2403.10998
```

Key properties:

* plane-parallel force geometry;
* approximately 3–30 µm operating region;
* optimized for gravity-like/interfacial forces;
* Cavendish configuration uses a thin conducting shield to suppress electromagnetic/Casimir interactions;
* approximately 30 mg active masses;
* designed to measure gravity at very short range;
* reported representative pressure errors significantly below the earlier conservative 1 nN/m² project benchmark.

Representative published 1000-second errors used:

```text
statistical ≈ 0.324 nN/m^2
systematic ≈ 0.167 nN/m^2
combined ≈ 0.3645 nN/m^2
```

---

# 37. 009D — plane-parallel $B-L$ pressure gate

Benchmark:

```text
g_BL = 1e-16
lambda = 6 um
effective alpha = 4.824767e4
```

Dense active layer scan.

Central 10 µm gap result with 5 µm active layer:

```text
pressure ≈ 16.3821 nN/m^2
signal / 1 nN/m^2 ≈ 16.38
5-sigma g reach ≈ 5.52e-17
```

At 6 µm gap and 5 µm layer:

```text
pressure ≈ 31.9080 nN/m^2
5-sigma g reach ≈ 3.96e-17
```

Minimum active-layer thickness for 5 sigma at 10 µm under 1 nN/m² noise:

```text
≈ 2.247 um
```

Decisions:

```text
REPULSIVE_B_L_PRESSURE_EXCEEDS_CONSERVATIVE_PLANE_PLATE_SENSITIVITY=YES
REFERENCE_G_BL_1E_MINUS_16_IS_DECISIVE_AT_10UM_GAP=YES
FEW_MICRON_DENSE_ACTIVE_LAYER_SUFFICIENT=YES
PLANE_PARALLEL_GEOMETRY_BEATS_CURVED_GEOMETRY_FOR_THIS_FORCE=YES
CANNEX_CLASS_CAVENDISH_CONFIGURATION_DIRECTLY_MATCHES_VOLUME_FORCE_SEARCH=YES
EXISTENCE_OF_B_L_FORCE=NOT_ESTABLISHED
HUMAN_SCALE_ANTIGRAVITY=NO
LABORATORY_REPULSIVE_FORCE_DEMONSTRATOR_PATH=HIGH_PRIORITY
009D_CANNEX_VECTOR_GATE=GREEN
```

This remains a potentially excellent Level-9 experiment if the force exists.

---

# 38. 009E — CANNEX shield transparency and realistic error budget

The conducting shield was stress-tested.

Electromagnetic Thomas–Fermi screening was rescaled by roughly:

```math
\frac{g_{B-L}}{e}
```

At:

```text
g_BL = 1e-16
```

the inferred $B-L$ screening length was on the order of:

```text
6e4–6e5 m
```

depending on assumed electromagnetic Thomas–Fermi length.

Therefore matter polarization was negligible compared with a 6 µm mediator range in this simple preflight.

For a full 1 µm shield:

```text
Yukawa transmission ≈ 0.84648
```

Remaining signals:

```text
6 um gap:
27.0095 nN/m^2

10 um gap:
13.8671 nN/m^2
```

Against combined CANNEX error:

```text
6 um SNR ≈ 74.10
10 um SNR ≈ 38.04
```

Representative 5-sigma coupling reaches:

```text
6 um ≈ 2.60e-17
10 um ≈ 3.63e-17
```

Decisions:

```text
B_L_THOMAS_FERMI_SCREENING_NEGLIGIBLE=YES
SUB_MICRON_CONDUCTING_SHIELD_IS_EFFECTIVELY_TRANSPARENT_TO_B_L=YES
ONE_MICRON_SHIELD_RETAINS_MORE_THAN_80_PERCENT_SIGNAL=YES
B_L_SIGNAL_REMAINS_DECISIVE_VS_PUBLISHED_CANNEX_ERROR=YES
B_L_SIGNAL_REMAINS_DECISIVE_VS_1NN_M2_CONSERVATIVE_ERROR=YES
009E_SHIELD_AND_ERROR_GATE=GREEN
```

Caveat:

This is a project-derived screening estimate, not a full condensed-matter calculation of a $B-L$ plasma response.

The static $B-L$ charge of the shield still needs differential cancellation in a real experiment.

---

# 39. 009F — isotope null-source design

The source used alternating enriched:

```text
92Mo
100Mo
```

For neutral molybdenum:

```text
92Mo: Z = 42, N = 50
100Mo: Z = 42, N = 58
```

The layers were thickness-matched so that the universal mass-Yukawa finite-depth source response was equal:

```math
\rho_{92}
\left(
1-e^{-t_{92}/\lambda}
\right)
=
\rho_{100}
\left(
1-e^{-t_{100}/\lambda}
\right)
```

while $B-L$ charge remained different.

For:

```text
t_92 = 20 um
lambda = 6 um
```

the matching thickness was:

```text
t_100 ≈ 13.0876269 um
```

The exact script supplied in the session was independently evaluated by the assistant because the attached paste contained the **script rather than a user terminal printout**.

Result under its stated assumptions:

```text
B-L isotope differential pressure ≈ 2.05505 nN/m^2
combined CANNEX sigma ≈ 0.36451 nN/m^2
SNR ≈ 5.6379
universal mass-Yukawa differential ≈ 0
Newtonian differential ≈ -0.0046 nN/m^2
```

Thickness error giving a 10% false universal-Yukawa signal:

```text
≈ 294.46 nm
```

Classification:

```text
009F_ISOTOPE_NULL_GATE=GREEN
```

but note the evidence level:

```text
ASSISTANT_INDEPENDENT_EXECUTION_OF_USER_SUPPLIED_SCRIPT
```

rather than a user-pasted terminal verification.

Scientific value:

The isotope-null design is a potentially excellent **signal discrimination architecture**.

It is not itself a route to macroscopic lift.

---

# 40. 009G — constraint-limited unscreened vector practicality frontier

This was one of the most important gates in the entire project.

Current compiled limits were downloaded from AxionLimits for:

```text
InverseSquareLaw
Sun
HorizontalBranch
RedGiant
Casimir
EotwashEP
MICROSCOPE
```

Data hashes were printed in the terminal and therefore provenance was preserved for that run.

At the 6 µm reference:

```text
mediator mass ≈ 0.0328878 eV
current compiled g limit ≈ 2.63372e-16
dominant constraint = ISL
g = 1e-16 remains below compiled limit
```

The crucial geometry-independent source bound was then derived.

For an unscreened linear repulsive Yukawa force, filling the entire half-space below the target with maximum charge-density matter maximizes the upward field.

Therefore no ring, disk, multilayer, metamaterial, perforation, or finite geometry can beat the half-space result at fixed:

* coupling;
* interaction range;
* maximum ordinary-matter charge density.

Optimistic benchmark:

```text
rho = 23000 kg/m^3
source neutron fraction = 0.62
test neutron fraction = 0.62
```

The current compiled constraint envelope produced the maximum contact result:

```text
best mediator mass ≈ 1.75861 eV
best range ≈ 112.206 nm
g limit ≈ 1.96598e-13
dominant = ISL
maximum contact acceleration ≈ 0.216650 m/s^2
≈ 0.0220921 g
```

Coupling enhancement required for 1 g:

```text
≈ 6.72793
```

Force enhancement:

```text
≈ 45.265
```

Maximum stand-off retaining at least 1% of $g$:

```text
≈ 88.94 nm
```

Other stand-off results:

```text
50 nm  ≈ 0.01415 g
100 nm ≈ 0.00906 g
200 nm ≈ 0.00372 g
500 nm ≈ 2.62e-4 g
1 um   ≈ 1.49e-5 g
2 um   ≈ 3.32e-6 g
5 um   ≈ 9.72e-7 g
10 um  ≈ 4.36e-7 g
```

Decisions:

```text
HALFSPACE_IS_OPTIMISTIC_ORDINARY_MATTER_SOURCE_BOUND=YES
CLEVER_UNSCREENED_SOURCE_GEOMETRY_CAN_BEAT_HALFSPACE_BOUND=NO
UNSCREENED_B_L_CAN_REACH_1G_WITH_CURRENT_COMPILED_LIMITS=NO
UNSCREENED_B_L_CAN_REACH_10_PERCENT_G=NO
UNSCREENED_B_L_CAN_REACH_1_PERCENT_G_AT_CONTACT=YES
GEOMETRY_OPTIMIZATION_REMAINS_A_PRACTICAL_ESCAPE=NO
009G_CONSTRAINT_LIMITED_PRACTICALITY_GATE=GREEN
```

This formally ended ordinary unscreened-source geometry optimization as a practical route.

---

# 41. 009H — Nelson–Walsh chameleon-vector hierarchy preflight

Published model:

Nelson and Walsh:

```text
"Chameleon Vector Bosons"
Phys. Rev. D 77, 095006
arXiv:0802.0762
```

The idea:

A scalar charged under the new vector can condense inside sufficiently large matter distributions and screen the vector force.

The published order-of-magnitude self-energy criterion was used.

For the candidate device:

```text
tungsten source radius = 0.10 m
source mass ≈ 80.8437 kg
gap = 0.01 m
effective source/receiver scale = 1.20 m
scalar mass = 1e-9 eV
scalar Compton wavelength ≈ 197.327 m
```

At 1 g:

```text
required g_BL ≈ 2.13702e-15
effective W-W alpha ≈ 2.19915e7
q_max 10-cm source unscreened ≈ 5.29778e-4
q_max 1.2-m pair unscreened ≈ 3.67901e-6
q_min Earth screened ≈ 5.46228e-19
```

A tenfold device-unscreening margin used:

```text
q_design ≈ 3.67901e-7
```

giving a huge apparent Earth/device screening hierarchy:

```text
~6.74e12
```

Similar windows existed mathematically for 10 g and 100 g.

Decision at that stage:

```text
SMALL_SCALAR_CHARGE_OPENS_EARTH_SCREENED_DEVICE_UNSCREENED_WINDOW=YES
ONE_G_PARAMETER_WINDOW_EXISTS_AT_ORDER_OF_MAGNITUDE_LEVEL=YES
HUNDRED_G_LOCAL_RECEIVER_WINDOW_EXISTS_AT_ORDER_OF_MAGNITUDE_LEVEL=YES
009H_CHAMELEON_HIERARCHY_PREFLIGHT=GREEN
```

However this was later substantially downgraded by 009I.

Do not revive the naive 009H conclusion without incorporating 009I.

---

# 42. 009I — terrestrial chameleon compatibility no-go

This was the critical correction to 009H.

The same Nelson–Walsh relations imply a vector screening length in matter:

```math
\ell_V^2
\sim
\frac{m_s}
{qg^2\rho}
```

and the unscreened spherical self-energy condition.

For the actual 009H design:

```text
Earth vector screening length ≈ 42.8067 m
```

Thus at tabletop distances, the force would be almost completely unscreened.

Transmission:

```text
52 um ≈ 0.999998785
1 mm  ≈ 0.999976639
3 mm  ≈ 0.999929920
1 cm  ≈ 0.999766419
```

Maximum scalar charges preserving unscreened behavior:

```text
10-cm source q_max ≈ 5.10045e-4
1.2-m pair q_max ≈ 3.54198e-6
```

Shortest Earth vector range compatible with those objects remaining unscreened:

```text
10-cm source ≈ 1.14967 m
1.2-m pair ≈ 13.7960 m
```

Most importantly, combining Earth hiding and device unscreening eliminated $m_s$ and $g$.

For a 10-cm source:

```text
q-window conflict at 52 um ≈ 4.88808e8
q-window conflict at 0.1 um ≈ 1.32174e14
```

Maximum full-density source radius if Earth force range is below 52 µm:

```text
≈ 4.523 um
```

If Earth range is below 0.1 µm:

```text
≈ 8.698 nm
```

Decisions:

```text
009H_GLOBAL_EARTH_VS_DEVICE_SCREENING_HIERARCHY=MATHEMATICALLY_SURVIVES
009H_EARTH_SCREENING_SHORT_ENOUGH_TO_HIDE_TABLETOP_FORCE=NO
TEN_CM_SOURCE_CAN_REMAIN_UNSCREENED_WHILE_EARTH_RANGE_BELOW_52UM=NO
TEN_CM_SOURCE_CAN_REMAIN_UNSCREENED_WHILE_EARTH_RANGE_BELOW_0P1UM=NO
M_SCALAR_OR_G_TUNING_CAN_REPAIR_THIS_MONOLITHIC_CONFLICT=NO
MONOLITHIC_TERRESTRIAL_1G_CHAMELEON_VECTOR_PATH=REJECTED_AT_PREFLIGHT_LEVEL
009I_TERRESTRIAL_SCREENING_COMPATIBILITY_GATE=GREEN
```

This is a strong negative result.

Do not retune $m_s$ or $g$ to try to repair it.

They cancel from the crucial compatibility relation.

---

# 43. 009J — microstructured subcritical source / neutral matrix

The next loophole was to break the active source into tiny unscreened pieces embedded in a nearly $B-L$-neutral matrix.

Protium is conceptually interesting because neutral ordinary hydrogen has:

```math
B-L=0
```

but this does not automatically solve collective screening.

Nelson–Walsh screening depends on:

* source size;
* density;
* proximity to other sources.

Therefore neighboring grains contribute cross-energy and behave as a coarse-grained charged medium.

The active filling-fraction constraint was derived.

A Borexino light-$B-L$ particle-level coupling benchmark of:

```text
g_BL <= 6.3e-7
```

was used as an optimistic ceiling.

For only a generous 52 µm hiding requirement:

```text
critical full-density radius ≈ 4.523 um
10-cm active filling fraction ≈ 2.046e-9
active source mass ≈ 1.654e-7 kg
source field at particle bound ≈ 1.778e8 g
optimistic 1-kg payload acceleration ≈ 29.41 g
```

So 52 µm hiding alone did **not** kill microstructure.

But using the much more stringent 0.1 µm terrestrial/Casimir hiding scale:

```text
critical full-density radius ≈ 8.698 nm
10-cm active filling fraction ≈ 7.5658e-15
active source mass ≈ 6.1165e-13 kg
source field at particle bound ≈ 657.53 g
```

Despite the enormous local field on an ideal active grain, the allowed receiver contains so little active matter that:

```text
maximum 1-kg payload acceleration ≈ 4.0218e-10 g
```

Optimistic receiver radius needed for 1-kg 1-g lift:

```text
≈ 2.48646e8 m
≈ 248646 km
```

Required compact coupling:

```text
g ≈ 3.14146e-2
```

which is approximately:

```text
4.98645e4
```

times the Borexino benchmark.

Decisions:

```text
INDIVIDUAL_GRAIN_SUBCRITICALITY_IS_SUFFICIENT=NO
INTER_GRAIN_VECTOR_SELF_ENERGY_PRESENT=YES
COMPACT_GRAIN_ENSEMBLE_HAS_COARSE_GRAINED_SCREENING_BOUND=YES
B_L_NEUTRAL_MATRIX_CANCELS_VECTOR_FIELD=NO
TERRESTRIAL_MICROSTRUCTURED_CHAMELEON_B_L_1G_PATH=REJECTED_AT_PREFLIGHT_LEVEL
009J_MICROSTRUCTURE_COLLECTIVE_SCREENING_GATE=GREEN
```

This closes passive nanograin/protium-matrix rescue for a compact terrestrial device at preflight level.

---

# 44. 009K — screened thin-shell residual force

Instead of avoiding screening, 009K asked whether the residual thin-shell force itself could be useful.

## Low-density branch

The screened background identities imply a maximum vector pressure only about half the scalar attractive pressure at zero gap.

009H parameters:

```text
ell_V ≈ 42.8067 m
ell_S ≈ 197.327 m
ell_S / ell_V ≈ 4.60973
```

Maximum vector/scalar pressure ratio:

```text
zero gap = 0.5
1 m      ≈ 0.491
10 m     ≈ 0.416
ell_V    ≈ 0.229
```

Therefore:

```text
009H_SCREENED_THIN_SHELL_CAN_BECOME_NET_REPULSIVE=NO
LOW_DENSITY_SCREENED_CHAMELEON_NET_REPULSION=REJECTED
```

## High-density branch

A high-density branch can have:

```math
\frac{\ell_S}{\ell_V}
=
\frac{\sqrt{2}gq}{\sqrt{\epsilon}}
```

so $\ell_S<\ell_V$ is algebraically possible.

With:

```text
ell_V = 100 nm
epsilon = 4 pi
```

the sign threshold was:

```text
g ≈ 5.79127e-11
q ≈ 4.32829e10
g q ≈ 2.50663
```

Thus a net-repulsive thin-shell window exists algebraically without immediately requiring a blatantly nonperturbative $gq$.

However direct-force constraints become devastating.

An intentionally weak proxy allowed a new force no larger than 5% of the ideal Casimir pressure at the predicted optimum gap.

Proxy frontier:

```text
g ≈ 6.64529e-11
q ≈ 3.52133e10
gq ≈ 2.34002
ell_S/ell_V ≈ 0.933534
optimal gap ≈ 1.07015 um
maximum net repulsive pressure ≈ 4.95661e-5 Pa
```

Supporting 1 kg at $1g$:

```text
required area ≈ 197850 m^2
equivalent square side ≈ 444.8 m
```

Using only the particle bound gave an absurdly large predicted force:

```text
g = 6.3e-7
optimal gap ≈ 5.17 nm
net repulsive pressure ≈ 2.800 GPa
```

with the force exceeding the weak Casimir residual proxy by:

```text
≈ 3.08e4
```

Decisions:

```text
LOW_DENSITY_SCREENED_CHAMELEON_NET_REPULSION=REJECTED
HIGH_DENSITY_SHORT_SCALAR_SIGN_ESCAPE_EXISTS_ALGEBRAICALLY=YES
PARTICLE_BOUND_ONLY_HIGH_DENSITY_POINT_COMPATIBLE_WITH_FORCE_DATA=NO
WEAK_5PCT_CASIMIR_PROXY_ALLOWS_USEFUL_1M2_1KG_LIFT=NO
THIN_SHELL_RESIDUAL_FORCE_IS_A_PRACTICAL_TERRESTRIAL_ESCAPE=STRONGLY_DISFAVORED
009K_THIN_SHELL_NET_FORCE_GATE=GREEN
```

An exact modern experiment-specific recast would still be needed for a formal no-go, but this branch should no longer receive significant engineering effort.

---

# 45. Strategic re-ranking after 009K

At this stage:

* classical GR had failed energetically;
* free-EM quantum negative energy had failed macroscopically;
* unscreened $B-L$ was measurable but topped out near 2.2% of $g$ under then-assumed constraints;
* monolithic terrestrial chameleon screening failed;
* microstructure failed at the necessary hiding scale;
* residual thin-shell repulsion was strongly disfavored.

The project then searched for an **experimental composition blind direction**.

This produced 009L.

---

# 46. 009L — material-phobic / gold-null vector

Phenomenological neutral-atom charge:

```math
Q_5
=
N+\beta Z
```

Natural gold is essentially monoisotopic $^{197}$Au:

```text
Z = 79
N = 118
```

Therefore:

```math
\beta_{\mathrm{Au}}
=
-\frac{118}{79}
=
-1.493670886075949
```

makes natural gold exactly neutral at the nuclear-counting level:

```math
Q_5(^{197}{\mathrm{Au}})=0
```

Other material charge-to-mass factors at this direction:

```text
Au = 0
Pt ≈ +2.96114e-3
W  ≈ -3.76221e-3
Os ≈ +3.73765e-3
Si ≈ -0.243040
C  ≈ -0.245694
Be ≈ -0.106800
Al ≈ -0.201478
```

Thus carbon remains strongly charged while gold becomes almost blind.

## Exact 2016 layered response preflight

The actual 2016 geometry was modeled, including:

Test body:

```text
250 nm Au
10 nm Cr
sapphire substrate
```

Source:

```text
150 nm Au
10 nm Cr
Au/Si structured layer
depth ≈ 2.10 um
```

At the 009G optimum range:

```text
lambda ≈ 112.206 nm
mass ≈ 1.75861 eV
```

the gold-phobic layered response relative to $B-L$ became:

```text
≈ 5.16168e-4
```

therefore the 2016 coupling bound weakened by:

```text
≈ 44.0154
```

Recast ISL coupling:

```text
≈ 8.65334e-12
```

Carbon coupling needed for 1-g half-space contact acceleration:

```text
≈ 8.53807e-12
```

Therefore the **ISL-only material recast** allowed approximately:

```text
1.02718 g
```

at contact.

Stand-off at that ISL ceiling:

```text
0 nm   ≈ 1.027 g
10 nm  ≈ 0.940 g
25 nm  ≈ 0.822 g
50 nm  ≈ 0.658 g
100 nm ≈ 0.421 g
250 nm ≈ 0.111 g
```

However, to remain conservative, the separate compiled Casimir $B-L$ curve was initially left **completely unrescaled**.

At 112 nm that produced:

```text
conservative allowed g ≈ 2.73329e-12
carbon contact acceleration ≈ 0.10248 g
```

Only a coupling-bound relaxation of:

```text
≈ 3.12374
```

would have been needed to restore 1 g.

This was extremely promising phenomenologically.

## Full conservative scan

The scan ended at its imposed high-mass boundary:

```text
mass = 7.5 eV
range ≈ 26.3103 nm
```

and therefore the reported “best” point is **boundary-limited, not a proven global optimum**.

At that scan edge, using the unrescaled Casimir curve:

```text
conservative g ≈ 1.55998e-10
conservative carbon contact acceleration ≈ 78.2756 g
```

This number must **not** be treated as physically allowed until the model and experiment-specific constraints are properly recast.

## Nanostructure geometry proxy

At a 112-nm interaction range and local $1g$ carbon surface field:

```text
pressure ≈ 3.8678e-3 Pa
```

A 1-kg payload requires:

```text
interaction area ≈ 2535.46 m^2
```

Packing that into a 10-cm cube corresponds to an interface-area density giving a characteristic layer-pitch proxy:

```text
≈ 394 nm
```

A 50%-active carbon 10-cm cube would contain:

```text
≈ 1.7575 kg carbon
```

Therefore the interface area is geometrically conceivable in nanostructured matter.

But directional force summation and mechanical cancellation were **not established**.

Decisions:

```text
NATURAL_GOLD_VECTOR_CHARGE_NULL=YES
2016_AU_SI_RESPONSE_SUPPRESSED_BY_MORE_THAN_1000X=YES
RECAST_ISL_BOUND_PERMITS_1G_CARBON_CONTACT_FIELD=YES
EVEN_UNRESCALED_CASIMIR_CURVE_PERMITS_AT_LEAST_0P1G=YES
ONLY_FEW_FOLD_CASIMIR_COUPLING_RELAXATION_NEEDED_FOR_1G=YES
COMPACT_NANOSTRUCTURE_AREA_SCALE_IS_GEOMETRICALLY_PLAUSIBLE=YES
GENERALIZED_VECTOR_UV_COMPLETION=NOT_ESTABLISHED
ASTROPHYSICAL_CONSTRAINT_RECAST=NOT_ESTABLISHED
009L_MATERIAL_PHOBIC_VECTOR_GATE=GREEN
```

009L was the strongest phenomenological practicality opening found so far.

But 009M and 009N then attacked its quantum-field-theory viability.

---

# 47. 009M — gold-null UV and stellar consistency

First observation:

A flavor-universal combination of:

```text
B-L
+
electromagnetic current
```

cannot change neutral-atom composition charge away from neutron number because:

```math
Q_{\mathrm{EM}}=0
```

for a neutral atom.

Therefore the gold-null direction cannot arise from the simplest flavor-universal $B-L+$EM construction.

## Family-dependent anomaly-free realization

Consider:

```math
X
=
B+x_eL_e+x_\mu L_\mu+x_\tau L_\tau
```

with right-handed neutrinos and anomaly condition:

```math
3+x_e+x_\mu+x_\tau=0
```

For a neutral atom:

```math
Q_X
=
A+x_eZ
=
N+(1+x_e)Z
```

The gold null requires:

```text
x_e = -2.493670886075949
```

A symmetric anomaly-free choice gave:

```text
x_mu = x_tau = -0.253164556962025
```

and:

```text
3 + x_e + x_mu + x_tau = 0
```

exactly.

Thus an anomaly-free family-dependent charge direction exists algebraically.

However it has a large electron coupling.

A deliberately **weak** stellar preflight used only:

```text
|g_e| < 1e-12
```

which implies:

```text
g_max ≈ 4.01015e-13
```

for the gold-null family current.

This was deliberately less restrictive than much of the published stellar literature.

At 112 nm:

```text
g required for 1g ≈ 8.53807e-12
stellar proxy g_max ≈ 4.01015e-13
gap ≈ 21.29
maximum contact acceleration ≈ 0.002206 g
```

At 26 nm:

```text
g required for 1g ≈ 1.76322e-11
gap ≈ 43.97
maximum acceleration ≈ 5.17e-4 g
```

The 009L 1-g point has electron coupling:

```text
≈ 2.1291e-11
```

which exceeds even the intentionally weak $10^{-12}$ proxy by:

```text
≈ 21.29
```

At the 26-nm 009L conservative coupling the electron coupling exceeded the proxy by:

```text
≈ 389
```

Decisions:

```text
009L_PHENOMENOLOGICAL_MATERIAL_NULL=SURVIVES
MINIMAL_FLAVOR_UNIVERSAL_ANOMALY_FREE_UV_REALIZATION=REJECTED
FAMILY_DEPENDENT_ANOMALY_FREE_GOLD_NULL_EXISTS=YES
FAMILY_DEPENDENT_GOLD_NULL_1G_SURVIVES_WEAK_STELLAR_PREFLIGHT=NO
FAMILY_DEPENDENT_GOLD_NULL_0P1G_SURVIVES_WEAK_STELLAR_PREFLIGHT=NO
LEPTOPHOBIC_ISOSPIN_GOLD_NULL_ESCAPE=ONLY_SURVIVING_009L_UV_CLASS_AT_THIS_GATE
009M_GOLD_NULL_UV_STELLAR_GATE=GREEN
```

The next question became whether a leptophobic proton/neutron current could retain the gold blind spot.

---

# 48. 009N — electroweak conservation / unavoidable axial obstruction

Latest completed gate.

The leptophobic gold-null low-energy nucleon charges were normalized as:

```math
q_n=1
```

```math
q_p=-\frac{118}{79}
=-1.493670886075949
```

For vector $u$ and $d$ quark charges:

```math
q_p
=
2v_u+v_d
```

```math
q_n
=
v_u+2v_d
```

Solving:

```text
v_u = -1.329113924050633
v_d = +1.164556962025316
```

so the required isovector splitting is:

```text
v_u - v_d = -2.493670886075949
```

This is the central obstruction.

Above electroweak symmetry breaking, $u_L$ and $d_L$ belong to the same $SU(2)_L$ doublet and share a common left-handed gauge charge.

Therefore a simple electroweak-gauge-invariant realization cannot have these as simultaneously pure-vector unequal charges.

The required vector splitting becomes an unavoidable axial splitting or must be compensated by additional Higgs/$W$/UV interactions.

## Model-independent isovector nucleon axial floor

Using:

```text
g_A ≈ 1.2754
```

at least one nucleon must have an axial coefficient of magnitude:

```text
>= 1.590213924051
```

within this simple electroweak matching argument.

This is an order-one axial sector.

## One-Higgs illustration

The one-Higgs electroweak realization gave:

```text
X_Q = -0.082278481012658
X_H = -2.493670886075949
X_uR = -2.575949367088608
X_dR = +2.411392405063291
c_A^u = -1.246835443037975
c_A^d = +1.246835443037975
```

Thus:

```text
|X_H| ≈ 2.49367
```

and the large axial sector is explicit.

## Free-streaming stellar axial preflight

Using the literature-motivated approximate bound:

```math
\frac{|c_A^N|}{f_X}
\lesssim
(10^8\ {\mathrm{GeV}})^{-1}
```

with:

```math
f_X
=
\frac{m_X}{g_X}
```

gave at the 112-nm 1-g point:

```text
m_X ≈ 1.75861 eV
g required for 1g ≈ 8.53807e-12
f_X at 1g ≈ 205.973 GeV
free-streaming stellar g_max ≈ 1.10589e-17
maximum acceleration ≈ 1.67767e-12 g
```

The nucleon axial coefficient allowed at the desired 1-g coupling would be only:

```text
≈ 2.05973e-6
```

compared with the unavoidable natural value:

```text
≈ 1.59021
```

requiring an axial suppression/cancellation of:

```text
≈ 7.7205e5
```

At 26 nm:

```text
m_X = 7.5 eV
g required for 1g ≈ 1.76322e-11
stellar g_max ≈ 4.71635e-17
maximum acceleration ≈ 7.15484e-12 g
required axial suppression ≈ 3.73852e5
```

Decisions from the actual user terminal:

```text
009L_MATERIAL_BLIND_DIRECTION=PHENOMENOLOGICALLY_SURVIVES
PURE_VECTOR_LEPTOPHOBIC_ISOSPIN_CURRENT_IS_ELECTROWEAK_CONSERVED=NO
UNAVOIDABLE_ORDER_ONE_AXIAL_OR_EW_COMPENSATING_SECTOR=YES
SIMPLE_ONE_HIGGS_GOLD_NULL_VECTOR_1G_PATH=REJECTED_AT_PREFLIGHT_LEVEL
FREE_STREAMING_STELLAR_AXIAL_PREFLIGHT_PERMITS_1G=NO
STELLAR_TRAPPING_OR_EXOTIC_CANCELLATION_FORMALLY_EXCLUDED=NO
MULTI_HIGGS_OR_EW_COMPENSATED_UV_COMPLETION=NOT_ESTABLISHED
FINE_TUNED_FCNC_LONGITUDINAL_CANCELLATION=NOT_ESTABLISHED
PRACTICAL_GOLD_NULL_VECTOR=NOT_ESTABLISHED
PRACTICAL_ANTIGRAVITY=NOT_ESTABLISHED
NEXT=GLOBAL_RERANK_OPPOSITE_SIGN_SCALAR_FORCE_VS_EXOTIC_EW_COMPENSATED_VECTOR
009N_ELECTROWEAK_CONSERVATION_GATE=GREEN
```

This is the current frontier.

---

# 49. Exact interpretation of 009N

009N does **not** prove every imaginable gold-null vector theory impossible.

What it does prove at preflight level is:

> The simplest leptophobic isospin-violating pure-vector interpretation is not electroweak conserved.

The required neutron/proton contrast forces a very large $u/d$ isospin splitting.

In a simple gauge-invariant realization that translates into:

* order-one axial quark couplings;
* Higgs charge;
* weak-isospin-current nonconservation;
* or equivalent compensating electroweak interactions.

Very light vectors coupled to nonconserved currents have dangerous longitudinal production.

The free-streaming stellar estimate destroys the uncomplicated 1-g point by many orders of magnitude.

Still unresolved:

* stellar trapping at much stronger coupling;
* carefully arranged multi-Higgs models;
* UV completions with compensating electroweak amplitudes;
* tuned flavor structure;
* whether a fully anomaly-free light isospin vector can eliminate all dangerous longitudinal channels;
* exact FCNC/Wess–Zumino constraints for a specific such model.

Therefore the correct status is:

```text
SIMPLE_GOLD_NULL_VECTOR=REJECTED
EXOTIC_EW_COMPENSATED_GOLD_NULL_VECTOR=UNRESOLVED_BUT_HIGH_RISK
```

Do not spend major effort on the exotic vector unless it wins the global rerank.

---

# 50. Major literature references carried forward

Important references already used or identified:

## General GR / quantum

Brown and Maclay:

```text
Vacuum Stress between Conducting Plates
Phys. Rev. 184, 1272
```

Fulling et al.:

Casimir energy gravitates normally.

Costa and Matsas:

complete mechanically supported Casimir apparatus and positive total mass under DEC assumptions.

Pfenning:

electromagnetic quantum inequalities used for 007B.

## $B-L$ vector

Cheng, Sheng, Yanagida:

```text
Detecting a Fifth-Force Gauge Boson via Superconducting Josephson Junctions
arXiv:2402.14514
```

## 2016 Casimir-less force experiment

Chen et al.:

```text
Phys. Rev. Lett. 116, 221102
arXiv:1410.7267
```

This is central for any future material-dependent short-range force recast.

## CANNEX

Final-design paper:

```text
arXiv:2403.10998
```

## Chameleon vector

Nelson and Walsh:

```text
Chameleon Vector Bosons
Phys. Rev. D 77, 095006
arXiv:0802.0762
```

## AxionLimits

Used as a current compiled constraint source for vector $B-L$:

```text
VectorB-L/
InverseSquareLaw.txt
Sun.txt
HorizontalBranch.txt
RedGiant.txt
Casimir.txt
EotwashEP.txt
MICROSCOPE.txt
```

Important:

AxionLimits is a compilation.

Central conclusions should ultimately be checked against underlying experiments and model assumptions.

## Borexino

A light-$B-L$ vector particle-level bound of approximately:

```text
g_BL <= 6.3e-7
```

was used as an optimistic particle benchmark in 009J.

## Stellar electron-coupled vector work

Relevant older $U(1)_L$ stellar constraints:

```text
arXiv:1512.03179
```

## General plasma production of new vectors

Relevant discussion:

```text
arXiv:2304.12907
```

Important result:

general $U(1)$ vectors do not automatically receive the same low-mass plasma suppression as a photon-aligned dark photon.

## Nonconserved-current / longitudinal-vector constraints

Dror, Lasenby, Pospelov:

```text
Phys. Rev. D 96, 075036
```

and related:

```text
Phys. Rev. Lett. 119, 141803
```

These are central for the electroweak/axial obstruction discovered in 009N.

All external claims should be reverified against primary papers when reused.

---

# 51. Branch status matrix

## Classical positive-energy GR

Status:

```text
THEORETICALLY_STRONG
PRACTICALLY_ENERGETICALLY_POOR
```

Best project result:

```text
006D
```

Do not abandon scientifically.

Do not prioritize for engineering without a new scaling mechanism.

---

## Static Casimir / free-EM negative energy

Status:

```text
PRACTICAL_BRANCH_REJECTED
```

Reason:

required scales are around $10^{-19}$ m for $1g$.

---

## Free-EM quantum-inequality loophole

Status:

```text
MACROSCOPIC_PRACTICAL_BRANCH_REJECTED
```

Reason:

causal bound gives approximately $10^{-54}$–$10^{-55}$ m/s² at meter scale.

---

## 006D canonical scalar realization

Status:

```text
PARTIAL_LOCAL_REALIZATION_SURVIVES
GLOBAL_REALIZATION_NOT_ESTABLISHED
PRACTICAL_PRIORITY_LOW
```

One complex scalar rejected.

Ungauged winding finite set rejected.

Gauge-assisted local decomposition survives.

No reason to finish the complicated global solution until a scaling breakthrough appears.

---

## Ordinary unscreened $B-L$

Status:

```text
LAB_DETECTION_BRANCH_SURVIVES
PRACTICAL_MACROSCOPIC_BRANCH_REJECTED
```

Strongest use:

009D/009E/009F experimental search.

Absolute half-space ceiling under current compiled constraints:

```text
≈ 0.0221 g at contact
```

at:

```text
lambda ≈ 112 nm
```

---

## Monolithic terrestrial chameleon $B-L$

Status:

```text
REJECTED_AT_PREFLIGHT_LEVEL
```

Reason:

device unscreening and Earth short-range hiding are algebraically incompatible at relevant macroscopic size.

---

## Microstructured chameleon $B-L$

Status:

```text
REJECTED_AT_PREFLIGHT_LEVEL
```

for compact terrestrial $1g$ at a submicron hiding scale.

---

## Chameleon thin-shell residual repulsion

Status:

```text
LOW_DENSITY_REJECTED
HIGH_DENSITY_ALGEBRAIC_SIGN_WINDOW_EXISTS
PRACTICAL_TERRESTRIAL_USE_STRONGLY_DISFAVORED
```

An exact modern experimental recast would be needed for a formal no-go, but priority is low.

---

## Gold-phobic generalized vector

Phenomenological status:

```text
VERY_INTERESTING
```

QFT status:

```text
SIMPLE_REALIZATIONS_REJECTED
EXOTIC_EW_COMPENSATED_REALIZATION_UNRESOLVED_HIGH_RISK
```

Do not confuse the beautiful 009L phenomenological blind direction with a viable quantum field theory.

---

## Remote-space small-source chameleon regime

Status:

```text
NOT_REJECTED
```

But even if real, this is not presently a terrestrial lift mechanism.

Keep as a lower-priority theoretical branch.

---

# 52. Current practical-antigravity probability calibration

The current best calibrated subjective estimate discussed in this session was:

```text
practical human-scale antigravity:
~4%
```

with a rough subjective uncertainty band:

```text
~2–8%
```

This is not a statistical confidence interval.

It is a research-prior estimate conditioned on everything currently known.

Do **not** raise this because a new gate prints GREEN.

The user explicitly wants to push toward:

```text
20%
```

but this percentage must be **earned by physics**, not chosen motivationally.

009L briefly looked capable of materially increasing the estimate.

009M and 009N then eliminated the simplest realizations.

Therefore there is currently no scientifically defensible reason to claim 10% or 20% practical antigravity.

A rough milestone confidence ladder discussed was:

```text
local repulsion mathematically possible:
>99%

local repulsion within established GR:
~98%

finite positive-energy source can show local repulsion:
~95%

some sensible field theory can realize some repulsive source:
~60–70%

a genuinely new neutral-matter repulsive fifth force exists:
~10–20%

future experimentally accessible repulsive-force anomaly:
~10–15%

useful 0.01g–1g local mechanism:
~5–8%

controllable human-scale practical antigravity:
~4%

reactionless antigravity propulsion:
far below 1%
```

These are subjective research priors.

They should not be presented as measured probabilities.

---

# 53. What would justify moving toward 10–20%

A real probability increase requires a qualitatively different milestone.

Examples:

## Criterion A

A healthy field theory survives:

* UV consistency;
* radiative stability;
* laboratory fifth-force bounds;
* stellar bounds;
* cosmological bounds;

and still predicts at least approximately:

```text
0.1g–1g
```

at a useful geometry.

## Criterion B

A reproducible laboratory experiment observes neutral-matter repulsion not attributable to:

* electromagnetism;
* Casimir forces;
* thermal gradients;
* vibration;
* patch potentials;
* charging;
* ordinary gravity.

## Criterion C

A field/material realization of the 006D-type GR source is found that changes the scaling by **orders of magnitude**, not merely coefficient $C$.

## Criterion D

A new mechanism produces a controllable external force on kilogram-scale matter with a non-astronomical reaction/source infrastructure and survives existing constraints.

Until something like this occurs, 20% would be unjustified.

---

# 54. Crucial semantic distinction

The vector-force branch is not ordinary gravitational repulsion.

A repulsive fifth force acting on neutral matter may be useful for an “antigravity-like actuator,” but scientifically it must be labeled as:

```text
REPULSIVE_FIFTH_FORCE
```

or:

```text
ANTIGRAVITY_LIKE_FORCE
```

unless it actually modifies spacetime/gravity.

An anchored source producing upward force does not imply reactionless propulsion.

For an isolated source plus payload:

```math
\mathbf{F}_{12}
=
-\mathbf{F}_{21}
```

and the center of mass cannot accelerate without exchanging momentum with something external.

---

# 55. Highest-value next scientific action

The current live frontier from 009N is:

```text
NEXT=
GLOBAL_RERANK_OPPOSITE_SIGN_SCALAR_FORCE_VS_EXOTIC_EW_COMPENSATED_VECTOR
```

The next session should **not immediately write another large simulation**.

First perform a rigorous global rerank.

The leading two candidates are:

## Candidate 1 — composition-dependent scalar exchange

This is now the most interesting fresh branch.

Why:

A scalar mediator does not require conservation of a gauge current and therefore avoids the specific longitudinal-vector/electroweak obstruction that killed the simple 009L vector realization.

For a scalar Yukawa interaction schematically:

```math
V_s(r)
\propto
-\frac{g_1g_2}{4\pi r}
e^{-m_sr}
```

same-sign scalar charges attract while opposite-sign effective scalar charges can repel.

The central question is:

> Can stable neutral materials acquire opposite-sign effective scalar charges in a technically natural, experimentally allowed field theory with enough coupling strength and range to produce useful force?

This branch must be tested brutally against:

* equivalence-principle tests;
* fifth-force searches;
* stellar emission;
* scalar mixing;
* radiative naturalness;
* nucleon scalar matrix elements;
* electron coupling;
* Higgs mixing;
* cosmology;
* self-interaction/screening;
* whether stable ordinary materials can really have opposite effective charge signs.

Do not assume opposite signs are physically achievable just because the phenomenological formula permits them.

The smallest decisive gate should first answer:

```text
CAN_A_HEALTHY_SCALAR_GIVE_OPPOSITE_SIGN_CHARGES_TO_TWO_STABLE_NEUTRAL_MATERIALS?
```

and then:

```text
WHAT_IS_THE_ABSOLUTE_CONSTRAINT_LIMITED_HALFSPACE_ACCELERATION?
```

Only if both survive should a nanostructure actuator be considered.

## Candidate 2 — exotic electroweak-compensated gold-null vector

Keep only as a secondary competitor.

Required accomplishments:

* explicit anomaly-free UV completion;
* electroweak gauge invariance;
* no unavoidable dangerous longitudinal current;
* no unacceptable FCNC;
* no electron/stellar catastrophe;
* no Wess–Zumino catastrophe;
* enough low-energy proton/neutron isospin contrast to retain the gold blind spot;
* current force constraints still permit approximately $0.1g$–$1g$.

This is a very high bar.

Do not spend major implementation time unless a literature/analytical preflight demonstrates that such a model genuinely exists.

## Candidate 3 — remote-space vector/chameleon regime

Retain as fallback.

This branch is not presently killed because the large Earth/environment source causing terrestrial screening problems can be removed in deep space.

However it remains:

* speculative;
* experimentally unobserved;
* not reactionless;
* dependent on an external interaction partner/source.

It should rank below the scalar rerank unless a clear known model suddenly gives a dramatic advantage.

---

# 56. Recommended next-session decision procedure

The next session should start by creating a table like:

| Criterion                 | Opposite-sign scalar | Exotic compensated vector | Remote-space chameleon |
| ------------------------- | -------------------: | ------------------------: | ---------------------: |
| Known healthy QFT         |                    ? |                 High risk |                Partial |
| Repulsion sign available  |                    ? |    Yes phenomenologically |                    Yes |
| Current lab constraints   |                    ? |                    Severe |  Environment dependent |
| Stellar constraints       |                    ? |            Severe/unknown |        Model dependent |
| Naturalness               |                    ? |               Major issue |            Major issue |
| $0.1g$ possible           |                    ? |   Only phenomenologically |                Unknown |
| $1g$ possible             |                    ? |     Simple forms rejected |                Unknown |
| Useful range              |                    ? |        tens–100 nm so far |     potentially larger |
| Reactionless              |                   No |                        No |                     No |
| Expected information gain |              Highest |                    Medium |             Medium/low |

Then choose **one** cheapest analytical/literature gate.

The preferred next research question is:

> **Does a theoretically healthy scalar interaction admit opposite-sign effective charges for stable neutral materials and, after all existing constraints, can its half-space acceleration exceed the vector 009G ceiling by orders of magnitude?**

If the answer is no, close that branch immediately.

If yes, it becomes the next major candidate.

---

# 57. What NOT to do next

Do not:

* restart 006 coefficient optimization;
* rerun 007 Casimir/QEI with slightly different numbers;
* spend time finishing the global 006D charged/gauged field realization;
* retune 009H $m_s$, $g$, or $q$;
* retry monolithic chameleon geometry;
* retry passive chameleon nanograins;
* optimize a chameleon thin-shell actuator before exact force constraints;
* treat the 78-g 009L scan-edge result as physically allowed;
* optimize gold-null nanostructures before finding a healthy field theory;
* immediately build an exotic multi-Higgs vector model without a cheap consistency/literature gate;
* inflate practical-antigravity probability to 20% because the user wants that target.

The target is motivation.

The physics must earn the probability.

---

# 58. Important subtlety about the 009L 78-g number

The 009L full conservative scan reported:

```text
BEST_MASS_EV=7.5
BEST_RANGE_NM≈26.31
BEST_CONSERVATIVE_CONTACT_A_OVER_G≈78.28
```

This was at the **hard upper boundary of the scanned mass interval**.

Therefore it is not a verified interior optimum.

More importantly, it used the original compiled $B-L$ Casimir numerical curve without a proper composition-specific model recast.

It subsequently failed simple UV/stellar consistency in 009M/009N.

Do not quote:

```text
78 g allowed
```

without all of these caveats.

The scientifically correct statement is:

> A phenomenological gold-phobic charge assignment greatly weakens some gold-coated laboratory force responses and can yield formally large carbon half-space accelerations under incompletely recast constraints, but the simplest quantum-field-theory realizations are strongly disfavored by electron or unavoidable axial/electroweak couplings.

---

# 59. Important surviving experimental result independent of practicality

Even if all practical-actuator branches fail, the 009D–009F work remains scientifically valuable.

The project has identified a plausible **laboratory test architecture** for a repulsive short-range neutral-matter vector force:

```text
plane-parallel geometry
+
electromagnetic/Casimir shield
+
composition modulation
+
possibly isotope modulation
```

This could potentially reach couplings around:

```text
few × 1e-17
```

under the simplified CANNEX-class estimates.

That is a separate Level-9 scientific objective.

If practical antigravity remains elusive, this experimental branch could still be worth formalizing as a publishable proposal after exact constraint/systematic analysis.

---

# 60. Current strongest established result versus strongest speculative result

## Strongest established project-derived classical result

```text
006D
```

A finite, nonsingular, positive-energy, locally conserved, NEC/WEC/DEC-compatible linearized-GR source generates local outward gravity while retaining positive far-field mass.

This is the strongest **physics-established** project result.

## Strongest experimental new-force concept

```text
009D–009F
```

A CANNEX-class plane-parallel/isotope-modulated experiment could plausibly test a repulsive neutral-matter vector force in an interesting micron-scale parameter regime.

## Strongest phenomenological practicality opening

```text
009L
```

Material-response blind directions can weaken some gold-coated short-range force experiments enough that formally order-$g$ nanoscale forces become possible.

But:

```text
009M + 009N
```

show that the simplest healthy QFT realizations of that direction fail.

Therefore 009L is not currently the leading viable theory.

---

# 61. Current accomplishment ladder

For established GR, the project has approximately reached:

```text
Level 0 — YES
Level 1 — YES
Level 2 — YES within linearized stated model
Level 3 — YES for 006D
Level 4 — YES for 006D
Level 5 — YES for 006D
Level 6 — NOT ESTABLISHED
Level 7 — PARTIAL LOCAL FIELD-THEORY REPRESENTABILITY ONLY
Level 8 — NO
Level 9 — NO for gravitational 006D source
Level 10 — NO
```

For the fifth-force branch:

```text
mathematical repulsive interaction — YES
healthy minimal B-L theory — YES
existence in nature — NO
experimentally searchable — YES
possible Level-9 force experiment — YES
useful human-scale actuator — NO
reactionless propulsion — NO
```

---

# 62. Documentation debt

The current repository documentation is significantly stale.

The attached `RESEARCH_BUILDPLAN.md` still says the active phase is approximately:

```text
006B / 006C / 006D
then 007
then 008 modified gravity
```

The actual live frontier has progressed through 009N.

The attached README still says the immediate objective is 007A/007B.

This is now incorrect.

After the next global-rerank gate determines the new leading branch, the project should update:

```text
RESEARCH_BUILDPLAN.md
NOTES.md
README.md
CLAIMS.md
ASSUMPTIONS.md
RESEARCH_QUESTIONS.md
```

as needed.

Do **not** rewrite all documentation before the rerank.

First determine the new branch.

Then update documents once so they reflect a stable frontier.

---

# 63. Buildplan update that will eventually be needed

The revised buildplan should record:

```text
007A:
static Casimir practicality — deprioritized

007B:
free-EM QEI macroscopic route — closed

008A:
wall/current-loop support — no improvement

008B:
local scalar representability — yes

008C:
fixed-charge dilation capacity — survives

008D:
one complex scalar — rejected

008E:
finite ungauged winding set — rejected

008F:
finite local gauge takeover window — survives but does not solve energy scaling

009A:
generic repulsive Yukawa scaling escape — survives phenomenologically

009B:
B-L concrete vector model — laboratory-interesting

009C:
modern force-experiment synthesis

009D:
CANNEX plane-parallel force gate — laboratory path green

009E:
shield/error preflight — green

009F:
isotope-null design — green under stated assumptions

009G:
unscreened ordinary-matter vector practical ceiling ≈ 0.022g — practical geometry route closed

009H:
global Earth/device screening hierarchy appeared possible

009I:
terrestrial tabletop hiding conflict — monolithic chameleon rejected

009J:
microstructure/neutral-matrix rescue — rejected

009K:
thin-shell practical terrestrial escape — strongly disfavored

009L:
gold-phobic material blind direction — phenomenologically strong

009M:
simple family-dependent gold-null realization — stellar killed

009N:
simple leptophobic isospin gold-null realization — electroweak/axial killed

NEXT:
global rerank of opposite-sign scalar force versus exotic electroweak-compensated vector
```

---

# 64. Claims ledger to preserve

## KNOWN / REPRODUCED

* positive $\Lambda$ causes geodesic defocusing;
* Kottler static-radius behavior;
* domain-wall gravitational repulsion;
* Reissner–Nordström local neutral-particle repulsion;
* negative pressure/tension can contribute repulsively;
* Casimir vacuum stress has a locally repulsive active-stress combination;
* complete Casimir apparatus must include support energy/stress.

## PROJECT-DERIVED AND WELL SUPPORTED

* positive-energy local gravitational repulsion is possible;
* negative ADM mass is not required;
* 005B finite disk/rim result;
* 006B thin coefficient approximately 23.426710;
* 006C independently verifies 005B;
* 006D finite-thickness, positive-energy, locally conserved DEC-compatible source;
* static GR constructions examined retain $ah^2/G$ scaling;
* 006D local canonical-scalar Gram representability;
* static scalar Derrick instability;
* charged temporal kinetic capacity is sufficient for one dilation mode;
* one charged winding scalar cannot exactly reproduce 006D;
* finite ungauged winding set fails at the termination;
* finite local gauge boundary takeover window exists;
* unscreened ordinary-matter linear Yukawa source cannot beat the half-space field;
* current compiled $B-L$ constraints imply about 2.2% $g$ maximum unscreened contact acceleration under the optimistic benchmark;
* monolithic chameleon terrestrial hiding/device-unscreening conflict;
* collective microstructure does not evade the same screening problem at useful filling fraction;
* simple gold-null vector realizations face severe electron or electroweak/axial constraints.

## NOT ESTABLISHED

* exact nonlinear GR 006D solution;
* dynamical stability of 006D;
* known material producing 006D stress;
* practical classical GR antigravity;
* existence of any new repulsive fifth force;
* $B-L$ force detection;
* exact CANNEX $B-L$ sensitivity;
* exact $B-L$ condensed-matter shield response;
* practical chameleon vector;
* viable gold-null vector UV completion;
* practical composition-dependent scalar force;
* practical antigravity;
* reactionless propulsion;
* novel discovery.

---

# 65. Current best concise project statement

Recommended conservative statement:

> **ANTIGRAVITY_RESEARCH has established that local gravitational repulsion is physically allowed within ordinary general relativity and has constructed a finite-radius, finite-thickness, nonsingular, positive-energy, locally conserved linearized-GR stress-energy source satisfying NEC, WEC, and DEC that produces a locally outward gravitational field while retaining positive far-field mass. The principal obstacle in established GR is not the sign of gravity but the catastrophic source-energy scaling $M\sim C ah^2/G$, with the best verified explicit coefficient near $C=23.5$. Established free-field quantum negative-energy bounds do not provide a macroscopic escape. Repulsive short-range vector forces provide a much better force-per-source-mass scaling and could plausibly be tested with plane-parallel, shielded, composition- or isotope-modulated experiments, but current work has not established that such a force exists. Ordinary unscreened $B-L$ interactions are constraint-limited to roughly 2.2% of $g$ at nanoscale contact in an optimistic half-space benchmark, and multiple terrestrial chameleon-vector escape routes have been falsified or strongly disfavored. A phenomenological material-blind vector direction can weaken gold-coated force constraints dramatically, but the simplest anomaly-free or leptophobic electroweak realizations are strongly disfavored by stellar and longitudinal-vector consistency arguments. The current highest-value frontier is a global reranking between composition-dependent opposite-sign scalar exchange and much more exotic electroweak-compensated vector theories. Practical antigravity and reactionless propulsion remain unestablished.**

---

# 66. First actions next session

Do these in order.

## Step 1 — inspect repository state

```bash
git status --short
```

## Step 2 — verify permanent regression baseline

```bash
ROOT="$(pwd)"
PY="$ROOT/.venv/bin/python"

PYTHONPATH="$ROOT/src" \
"$PY" -m pytest -q tests/known_solutions
```

Expected if unchanged:

```text
94 passed
```

## Step 3 — do NOT patch anything yet

Use the current frontier:

```text
GLOBAL_RERANK_OPPOSITE_SIGN_SCALAR_FORCE_VS_EXOTIC_EW_COMPENSATED_VECTOR
```

## Step 4 — perform authoritative literature reconnaissance

Highest-priority scalar questions:

1. Can scalar couplings to stable neutral matter have opposite effective signs?
2. What operator structure generates those signs?
3. Does the same operator produce dangerous Higgs/electron/nucleon couplings?
4. Are there known technically natural ultralight/eV-range scalar constructions?
5. What stellar bounds apply?
6. What equivalence-principle bounds apply?
7. Are composition blind directions available analogous to 009L?
8. Can screening help without recreating the 009I/J tradeoff?
9. What is the maximum constraint-allowed half-space acceleration?
10. Does any surviving point reach at least $0.1g$?

## Step 5 — only then write the next disposable gate

The next gate should be small and falsifiable.

Do not make it permanent until the theory survives.

---

# 67. Recommended next research-slice success criterion

The next branch deserves serious priority only if it satisfies all three:

```text
THEORETICALLY_HEALTHY=YES
CURRENT_CONSTRAINTS_ALLOW_ORDER_0P1G_OR_MORE=YES
PRACTICAL_GEOMETRY_NOT_ASTRONOMICAL=YES
```

If not, close it quickly.

The threshold for raising the practical-antigravity probability toward 20% should be even stronger:

```text
HEALTHY_FIELD_THEORY=YES
EXISTING_LAB_CONSTRAINTS_SURVIVED=YES
STELLAR_CONSTRAINTS_SURVIVED=YES
COSMOLOGY_NOT_OBVIOUSLY_FATAL=YES
ORDER_1G_LOCAL_FORCE=YES
USEFUL_FORCE_ON_MACROSCOPIC_RECEIVER=YES
FINITE_PLAUSIBLE_GEOMETRY=YES
NO_HIDDEN_MANY_ORDERS_OF_MAGNITUDE_REQUIREMENT=YES
```

Until something close to this exists:

```text
PRACTICAL_ANTIGRAVITY_PROBABILITY ≈ 4%
```

remains the conservative project estimate.

---

# 68. Most important strategic lesson from this session

The project is now extracting far more information from **negative results** than from speculative optimization.

The sequence:

```text
009H -> 009I -> 009J -> 009K
```

is a model example.

009H found a large apparent hierarchy.

009I discovered the relevant tabletop-screening incompatibility.

009J tested the strongest geometric escape.

009K tested the residual thin-shell escape.

The whole terrestrial chameleon branch was narrowed without spending weeks building nonlinear PDE solvers.

Likewise:

```text
009L -> 009M -> 009N
```

found a powerful phenomenological loophole and then immediately attacked whether a healthy QFT could realize it.

That research style should continue.

The shortest path to practical antigravity is not to keep the most exciting equation alive.

It is to kill bad branches cheaply until only a physically viable mechanism remains.

---

# 69. Final handoff directive

At the beginning of the next session, use profound but disciplined analysis.

Do not repeat already solved work.

Do not restart classical coefficient optimization.

Do not restart free-EM quantum-negative-energy work.

Do not retune the rejected chameleon constructions.

Do not engineer the gold-null vector before solving its field-theory consistency problem.

The single active question is:

> **Does a composition-dependent scalar force, or any other theoretically healthy interaction not suffering the vector-current obstruction, provide an experimentally allowed route to order-$0.1g$–$1g$ repulsion on useful matter with a finite plausible architecture?**

The cheapest decisive experiment answering that question is the next priority.

If the scalar branch fails, perform the same ruthless rerank rather than forcing it.

If it survives theory, stellar, laboratory, and half-space-practicality gates simultaneously, then it will have earned permanent implementation and a genuine upward revision of the project's practical-antigravity probability.


### END NOTE - AUGUST 28 2026 - 00:35 CST


### BEGIN NOTE - AUGUST 28 2026 - 02:10 CST


# Current Project Headline — August 28, 2026

> # **We have a mathematical construction for antigravity-like gravitational repulsion.**

This sentence is now the preferred headline description of the strongest verified result in the project.

Its exact scientific meaning is:

> **Within static linearized general relativity, the project has constructed a finite-radius, finite-thickness, nonsingular, positive-energy, locally conserved stress-energy distribution satisfying NEC, WEC, and DEC that produces a locally outward gravitational field while retaining positive far-field active mass.**

The proof/construction is Simulation 006D, supported by the 006B conserved thin optimization and the independent 006C Green-function verification program.

The core construction is

```math
q(r)=r p_r(r)
```

with

```math
p_\phi(r)=\frac{dq}{dr}
```

and

```math
p_z=0
```

so

```math
\frac{dp_r}{dr}
+
\frac{p_r-p_\phi}{r}
=
0
```

identically.

Choosing

```math
\epsilon
=
\max
\left(
|p_r|,
|p_\phi|
\right)
```

gives pointwise positive energy and type-I DEC, hence WEC and NEC.

The source is regularized to finite radial support and finite thickness, and the axial linearized-GR Green-function integral evaluates to an outward field.

The best tested finite coefficient is

```math
C_{\mathrm{finite}}
=
23.591586299249
```

in

```math
M_{\mathrm{equiv}}
=
C\frac{a h^2}{G}
```

The exact claim boundary must always accompany the headline:

```text
MATHEMATICAL_LOCAL_REPULSION=ESTABLISHED
FINITE_POSITIVE_ENERGY_LINEARIZED_GR_CONSTRUCTION=ESTABLISHED
LOCAL_CONSERVATION_LINEARIZED_ORDER=ESTABLISHED
NEC_WEC_DEC=PASS
OUTWARD_LOCAL_GRAVITATIONAL_FIELD=ESTABLISHED

EXACT_NONLINEAR_GR_REALIZATION=NOT_ESTABLISHED
DYNAMIC_STABILITY=NOT_ESTABLISHED
KNOWN_MATERIAL_REALIZATION=NO
ENERGETIC_PRACTICALITY=NO
PRACTICAL_ANTIGRAVITY_DEVICE=NO
NEW_PHYSICS_DISCOVERY=NO
```

The headline must **not** be shortened to "we proved practical antigravity" or "we discovered antigravity." Those stronger claims are not supported.

---

### BEGIN NOTE - AUGUST 27 2026 - 01:00 CST

# ANTIGRAVITY_RESEARCH — Comprehensive Carry-Forward Notes

This is the right place to stop adding patches and consolidate what we actually know.

The project has advanced far enough that the problem is now much more sharply defined than when we started. We have **not discovered a new law of physics or a practical antigravity device**, but we have established something important and useful:

```math
\text{General relativity absolutely permits local gravitational repulsion.}
```

More specifically, we have reproduced several known GR mechanisms and constructed a finite linearized-GR model in which **positive energy, positive total mass, and classical energy conditions coexist with a locally repulsive gravitational field**. What has emerged as the dominant obstacle is no longer the **sign** of gravity. It is the **stress-energy cost and physical realizability** of the source.

Simulation 006A then sharpened that further: within its stated assumptions, the optimistic static energy cost scales as

```math
M_{\mathrm{equiv}}\sim\frac{a h^2}{G}
```

where $a$ is the desired repulsive acceleration and $h$ is the source-to-target scale. Your optimizer independently reproduced the coefficient 1.0 exactly, while the explicit finite disk/rim architecture costs 79.753 times more. 

That gap—**1 versus 79.753**—is now one of the most important open mathematical questions in the project.

---

# 1. Current scientific conclusion

The simplest useful description of everything we have learned is:

```math
\text{gravity responds to stress-energy, not merely mass density}
```

and therefore sufficiently large **negative pressure/tension** can make the local active gravitational source negative even when the actual energy density remains positive.

For type-I matter in its local rest frame,

```math
T^\mu{}_\nu
\sim
{\mathrm{diag}}(\epsilon,p_x,p_y,p_z)
```

and in static weak-field GR the relevant active combination is schematically

```math
S=\epsilon+p_x+p_y+p_z
```

Ordinary matter has relatively tiny stresses compared with its rest energy:

```math
|p_i|\ll\epsilon
```

Hence it attracts.

Relativistic fields can instead have

```math
|p_i|\sim\epsilon
```

and sufficiently negative principal pressures can make

```math
S<0
```

That is the recurring mechanism behind essentially every successful branch we found:

```math
\text{vacuum energy},
\quad
\text{domain walls},
\quad
\text{anisotropic Maxwell stress},
\quad
\text{relativistic tension}
```

This is not speculative. Exact GR domain-wall solutions are known to repel, and the planar-wall attraction/repulsion transition occurs at tension/surface-energy ratio $1/2$. ([APS Journals][1]) Reissner–Nordström spacetime likewise has a known repulsive region for neutral test particles. ([arXiv][2])

So a useful project-level statement is now:

> **Antigravity-like local gravitational repulsion does not inherently require negative mass or negative energy. Relativistic stress/tension can produce it within ordinary general relativity.**

That statement is supported.

What is **not** established is a practical apparatus capable of generating such stresses economically or stably.

---

# 2. Current repository / environment checkpoint

The development environment is healthy:

```text
Python 3.13.15
NumPy 2.5.2
SciPy 1.18.1
SymPy 1.14.0
Matplotlib 3.11.1
mpmath 1.3.0
pytest 9.1.1
```

The repo now has a real research structure with theory, simulations, reusable geometry modules, known-solution tests, figures, CSV results, and persistent run logs.

Licensing was also cleaned up:

```text
Software:
MIT OR Apache-2.0
Original research:
CC0-1.0
Human project lead / affirmer:
Stevan White
AI assistance:
ChatGPT by OpenAI disclosed in AI_ASSISTANCE.md
```

The last Git commit/push you showed was:

```text
447d35b  updated licenses :)
```

That commit already contained Simulations 001–002 and the licensing changes. Everything from 003A onward was created later in this session, so unless you committed again afterward, those newer simulations are probably still uncommitted. That is worth checking at the beginning of the next session with:

```bash
git status --short
```

Do not assume that 003–006 are safely on GitHub until checked.

---

# 3. Test-suite checkpoint

Before 006A, the entire known-solutions suite had reached:

```text
61 passed
```

Simulation 006A then added six more tests, which individually passed:

```text
6 passed
```

So the expected total current regression count is approximately:

```math
67\text{ tests}
```

assuming everything is still present and no test discovery issue exists.

The first verification command next session should therefore be:

```bash
ROOT="$(pwd)"
PY="$ROOT/.venv/bin/python"
PYTHONPATH="$ROOT/src" \
"$PY" -m pytest -q tests/known_solutions
```

Expected:

```text
67 passed
```

If it differs, inspect the discrepancy before doing new physics.

---

# 4. Simulation 001A — Kottler / Schwarzschild–de Sitter baseline

Files:

```text
src/antigravity_research/geometry/kottler.py
tests/known_solutions/test_kottler.py
simulations/001_kottler_weak_field.py
results/data/001_kottler_weak_field.csv
results/figures/001_kottler_weak_field.png
```

We began with known GR:

```math
a(r)=
-\frac{GM}{r^2}
+
\frac{\Lambda c^2r}{3}
```

The radius where attraction and cosmological repulsion balance is

```math
r_s=
\left(
\frac{3GM}{\Lambda c^2}
\right)^{1/3}
```

For a $10^{12}M_\odot$ mass and observed cosmological parameters, we reproduced:

```math
r_s\simeq1.1139\ {\mathrm{Mpc}}
```

Below that scale, gravity was inward.

Above it, the cosmological-$\Lambda$ contribution won.

### Conclusion

Cosmological repulsion is real GR physics.

But observed $\Lambda$ is fantastically too weak for laboratory antigravity.

Classification:

```text
KNOWN_RESULT=YES
REPRODUCED=YES
NOVEL_ANTIGRAVITY_CLAIM=NO
```

---

# 5. Simulation 001B — invariant geodesic-deviation check

Files:

```text
src/antigravity_research/geometry/kottler_tidal.py
tests/known_solutions/test_kottler_tidal.py
simulations/001b_kottler_tidal_eigenvalues.py
results/data/001b_kottler_tidal_eigenvalues.csv
results/figures/001b_kottler_tidal_eigenvalues.png
```

This was important because coordinate acceleration alone can be misleading in GR.

We therefore examined the local free-fall tidal eigenvalues:

```math
\lambda_r=
\frac{2GM}{r^3}
+\frac{\Lambda c^2}{3}
```

```math
\lambda_t=
-\frac{GM}{r^3}
+\frac{\Lambda c^2}{3}
```

We reproduced:

```math
\lambda_r+2\lambda_t=\Lambda c^2
```

At sufficiently large radius all three spatial modes become stretching modes.

The transverse transition occurred numerically essentially where expected:

```text
ANALYTICAL_THRESHOLD ≈ 1.1139216 Mpc
NUMERICAL_THRESHOLD  ≈ 1.1138830 Mpc
```

### Conclusion

The cosmological repulsion is not merely a coordinate artifact. Neighboring free-falling particles genuinely separate.

This established our preferred operational definition:

> **Repulsion should ultimately be diagnosed through invariant or observer-operational quantities such as geodesic deviation, relative free-fall acceleration, or proper acceleration—not arbitrary coordinate acceleration.**

---

# 6. Simulation 002 — required stress-energy

Files:

```text
src/antigravity_research/geometry/perfect_fluid_defocusing.py
tests/known_solutions/test_perfect_fluid_defocusing.py
simulations/002_required_stress_energy.py
results/data/002_required_stress_energy.csv
results/figures/002_required_energy_density_1m.png
```

For an ideal isotropic fluid we used

```math
\frac{\ddot\xi}{\xi}
=
-\frac{4\pi G}{3c^2}
(\epsilon+3p)
+
\frac{\Lambda c^2}{3}
```

For

```math
p=w\epsilon
```

the active combination is

```math
\epsilon(1+3w)
```

Positive-energy defocusing becomes possible when

```math
w<-\frac13
```

The especially interesting $w=-1$ case preserved classical NEC/WEC/DEC while violating SEC.

For $1g$ of relative acceleration across one meter:

```math
\epsilon
\simeq
1.5763\times10^{27}\ {\mathrm{J/m^3}}
```

with

```math
p=-\epsilon
```

### Conclusion

Negative energy is **not necessary** for the sign of gravitational repulsion.

Sufficiently negative pressure works.

But this was a local homogeneous/isotropic benchmark, not a localized object.

---

# 7. Simulation 003A — localization obstruction for vacuum energy

Files:

```text
src/antigravity_research/geometry/vacuum_energy_core.py
tests/known_solutions/test_vacuum_energy_core.py
simulations/003a_finite_vacuum_energy_core.py
```

We attempted to make a finite $w=-1$ region.

The TOV equation gave

```math
\frac{dp}{dr}=0
```

for pure

```math
p=-\epsilon
```

Therefore a pure vacuum-energy region cannot simply taper continuously to zero at a finite radius while retaining that same EOS.

The proposed de Sitter interior and Schwarzschild exterior had:

```math
f_{\mathrm{in}}(R)=f_{\mathrm{out}}(R)
```

but

```math
f'_{\mathrm{in}}(R)\ne f'_{\mathrm{out}}(R)
```

Specifically we found the derivative ratio:

```math
\frac{f'_{\mathrm{in}}}{f'_{\mathrm{out}}}=-2
```

Therefore boundary stress is needed.

Even more importantly, the positive-volume-energy core produced a **positive Schwarzschild exterior mass**, hence:

```text
INTERIOR_DEFOCUSING=YES
EXTERIOR_FIELD=INWARD
```

### Conclusion

Internal repulsion does not automatically imply external antigravity.

---

# 8. Simulation 003B — exact Israel shell search

Files:

```text
src/antigravity_research/geometry/israel_shell.py
tests/known_solutions/test_israel_shell.py
simulations/003b_israel_shell_mass_search.py
results/data/003b_israel_shell_mass_search.csv
results/figures/003b_israel_shell_conditions_1g.png
```

Here we calculated the thin-shell stress properly rather than relying on a derivative mismatch.

The central question was:

> Can the de Sitter core be surrounded by a shell that yields a repulsive Schwarzschild exterior?

For an asymptotically flat Schwarzschild exterior, outward weak-field behavior requires

```math
M_{\mathrm{ADM}}<0
```

The exact shell search showed:

```text
OUTWARD_CASE_WITH_NONNEGATIVE_SHELL_SURFACE_ENERGY=NO
OUTWARD_CASE_WITH_WEC=NO
OUTWARD_CASE_WITH_DEC=NO
OUTWARD_CASE_WITH_NEC=YES
NEGATIVE_SHELL_ENERGY_REQUIRED_FOR_OUTWARD_EXTERIOR=YES
```

The NEC survived approximately over the narrow region

```math
-\frac12M_v\lesssim M_{\mathrm{ADM}}<0
```

but WEC/DEC did not.

The mass relation closed to roughly

```math
5\times10^{-16}
```

fractional error.

### Conclusion

Negative Schwarzschild mass provides repulsion mathematically, but it buys that result using exotic negative shell energy.

This also fits the broader positive-mass theorem: for asymptotically flat initial data satisfying the dominant energy condition,

```math
E\ge |P|
```

so negative ADM energy is unavailable under those assumptions. ([arXiv][3])

This route should remain low priority.

---

# 9. Simulation 004A — Reissner–Nordström breakthrough

Files:

```text
src/antigravity_research/geometry/reissner_nordstrom.py
tests/known_solutions/test_reissner_nordstrom.py
simulations/004a_einstein_maxwell_repulsion.py
results/data/004a_einstein_maxwell_repulsion.csv
results/figures/004a_rn_neutral_gravity_1g_z1p2.png
```

This changed the project.

We tested an exact Einstein–Maxwell system:

```text
Minkowski interior
charged shell
Reissner–Nordström exterior
```

and recovered the known RN sign-change radius

```math
r_{\mathrm{rep}}
=
\frac{Q^2}
{4\pi\epsilon_0Mc^2}
```

Define

```math
z=\frac{r_{\mathrm{rep}}}{R}
```

Then

```math
z>1
```

puts part of the repulsive region **outside the physical source**.

Our search found:

```text
DEC_REPULSIVE_Z_MIN ≈ 1.001
DEC_REPULSIVE_Z_MAX ≈ 1.33317
```

and, decisively:

```text
POSITIVE_ADM_MASS=YES
MAXWELL_FIELD_ENERGY_POSITIVE=YES
EXTERNAL_NEUTRAL_GRAVITATIONAL_REPULSION=YES
REPULSION_WITH_NONNEGATIVE_SHELL_ENERGY=YES
REPULSION_WITH_SHELL_WEC=YES
REPULSION_WITH_SHELL_DEC=YES
NEGATIVE_ADM_MASS_REQUIRED=NO
NEGATIVE_ENERGY_REQUIRED=NO_FOR_THIS_EXACT_MODEL
```

This is consistent with known RN repulsive behavior for neutral test particles. ([arXiv][2])

### The physics insight

The electromagnetic field has anisotropic stresses:

```math
p_r=-\epsilon,
\qquad
p_t=+\epsilon
```

It therefore taught us that **anisotropic relativistic stress can reverse local gravity without negative energy**.

### Physical failure mode

For the $1g$, $1\,{\mathrm{m}}$ benchmark:

```math
E_{\mathrm{surface}}
\simeq
2.67\times10^{19}\ {\mathrm{V/m}}
```

around twenty Schwinger fields.

Even making the solution sub-Schwinger pushed the scale to roughly:

```text
radius ≈ 407 m
mass ≈ 1.22×10^17 kg
charge ≈ 2.44×10^13 C
```

So the gravitational equations work.

Electrical engineering does not.

RN remains extremely valuable as a **proof of principle**, not presently as the best implementation route.

---

# 10. Simulation 005A — relativistic-tension/domain-wall principle

Files:

```text
src/antigravity_research/geometry/relativistic_wall.py
tests/known_solutions/test_relativistic_wall.py
simulations/005a_relativistic_tension_wall.py
results/data/005a_relativistic_tension_wall.csv
results/figures/005a_tension_efficiency.png
```

This generalized the RN lesson.

For a membrane having surface energy $U$ and tension

```math
\tau=qU
```

the planar gravitational sign changes at:

```math
q=\frac12
```

Repulsion:

```math
q>\frac12
```

DEC:

```math
q\le1
```

Therefore the entire interval

```math
\frac12<q\le1
```

supports positive-energy repulsive gravity while satisfying NEC/WEC/DEC.

This matches established GR wall results: sufficiently high tension makes walls repulsive, with the transition at $\tau/\sigma=1/2$. ([APS Journals][4])

The most efficient member of this membrane class is

```math
q=1
```

the ideal domain-wall stress tensor.

### One-g benchmark

We obtained:

```math
U_{\min}
\simeq
2.1017\times10^{27}\ {\mathrm{J/m^2}}
```

Equivalent surface mass:

```math
2.3385\times10^{10}\ {\mathrm{kg/m^2}}
```

The toy $\phi^4$ mapping produced

```math
v\simeq81.5\ {\mathrm{GeV}}
```

for $\lambda=1$.

Important caveat:

**That does not mean electroweak physics provides a usable antigravity wall.**

It only means that a toy scalar potential with the required integrated wall tension can be parameterized with a VEV on that scale.

Exact scalar-domain-wall GR solutions are known and are repulsive. ([APS Journals][5])

---

# 11. Simulation 005B — finite supported wall

Files:

```text
src/antigravity_research/geometry/finite_tension_disk.py
tests/known_solutions/test_finite_tension_disk.py
simulations/005b_finite_supported_antigravity.py
results/data/005b_finite_supported_antigravity.csv
results/figures/005b_finite_supported_field.png
```

This was our first attempt to turn the infinite wall into a finite static source.

Architecture:

```text
relativistic-tension disk
+
minimum-energy DEC-compatible compressive rim
```

The support rim was included specifically because one cannot simply ignore the stresses required to hold a finite tension-bearing object together.

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

This is the key physical picture.

A finite positive-energy system can have:

```math
\text{repulsive near field}
```

while still having:

```math
\text{ordinary attractive far field}
```

There is no contradiction with positive total mass.

The optimal disk geometry in this model was

```math
q=1
```

```math
\frac{R}{h}
\simeq4.00615
```

with repulsion extending to

```math
\frac{z}{R}
\simeq0.393320
```

The architecture's mass law was:

```math
M_{\mathrm{disk}}
\simeq
79.753148
\frac{ah^2}{G}.
```

At $1g$ one meter away:

```math
M\simeq1.172\times10^{13}\ {\mathrm{kg}}
```

```math
E\simeq1.053\times10^{30}\ {\mathrm{J}}
```

At $10^{-6}g$, one centimeter away:

```math
M\simeq1.172\times10^3\ {\mathrm{kg}}
```

### Important qualification

005B is **linearized GR plus an idealized membrane/rim stress model**.

It is not yet:

* an exact Einstein solution;
* a realistic material;
* a demonstrated dynamically stable configuration;
* a proof that all local conservation laws can be satisfied by an actual finite-thickness field theory.

So classify it as:

```text
NUMERICAL_MODEL_RESULT
```

not:

```text
PRACTICAL_DEVICE
```

The Laue theorem itself has precise hypotheses involving stationary/localized stress-energy and spacetime symmetries, so we should preserve those assumptions explicitly rather than treating integrated stress cancellation as a universally applicable identity. ([arXiv][6])

---

# 12. Simulation 006A — abstract static DEC energy bound

Files:

```text
src/antigravity_research/geometry/energy_bounds.py
tests/known_solutions/test_energy_bounds.py
simulations/006a_static_dec_lower_bound.py
results/data/006a_static_dec_energy_bound.csv
results/figures/006a_static_dec_mass_bound.png
```

This is the current frontier.

The optimizer was given independent integrated stress variables and asked:

> What is the smallest positive energy capable of producing a normalized negative active gravitational source while satisfying DEC and static Laue balance?

It returned exactly:

```text
GENERAL_MIN_ENERGY_COEFFICIENT=1.000000
E_REP=0.500000
E_SUPPORT=0.500000
P_REP_X=-0.500000
P_REP_Y=-0.500000
P_REP_Z=-0.500000
P_SUPPORT_X=+0.500000
P_SUPPORT_Y=+0.500000
P_SUPPORT_Z=+0.500000
```

The domain-wall-restricted LP returned:

```text
DOMAIN_WALL_MIN_ENERGY_COEFFICIENT=2.000000
```

And:

```text
005B_ARCHITECTURE_COEFFICIENT=79.753148
```

So:

```math
1
<
79.753
```

by an enormous margin. 

The general solution tells us that the abstract optimum wants:

### Repulsive region

```math
p_x=p_y=p_z=-\epsilon
```

That is maximally negative pressure while saturating DEC.

### Supporting region

```math
p_x=p_y=p_z=+\epsilon
```

That is maximally positive stress.

Both carry positive energy.

The optimizer splits the energy equally.

---

# 13. Extremely important caveat about 006A

Do **not** promote

```math
M\ge\frac{ah^2}{G}
```

to a universal theorem yet.

006A proves the optimum **of the LP we formulated**.

That LP uses:

* linearized gravity;
* type-I stress-energy;
* DEC;
* integrated Laue balance;
* an optimistic $1/h^2$ gravitational kernel;
* no explicit spatial support geometry;
* no discrete local equation

```math
  \partial_jT^{ij}=0
```
* no exact Einstein constraint equations;
* no stability conditions;
* no finite-thickness field realization.

Therefore coefficient 1 should currently be labeled:

```text
OPTIMISTIC_ABSTRACT_STATIC_DEC_BOUND
```

not:

```text
PROVEN_UNIVERSAL_GR_BOUND
```

That distinction is critical.

The **pointwise** part is much stronger:

DEC gives

```math
|p_i|\le\epsilon
```

and therefore

```math
\epsilon+p_x+p_y+p_z
\ge
-2\epsilon
```

That really does identify

```math
p_x=p_y=p_z=-\epsilon
```

as the maximally negative active source within this type-I DEC framework.

But converting that local statement into the global coefficient exactly equal to 1 requires additional geometric assumptions.

---

# 14. Current fundamental scale estimates

006A produced an especially useful matrix.

For a static DEC source, the optimistic abstract bound is:

```math
M_{\mathrm{static}}
\approx
\frac{ah^2}{G}.
```

### $1g$

At $h=1\,{\mathrm{m}}$:

```math
M_{\min}
=
1.4693\times10^{11}\ {\mathrm{kg}}
```

```math
E_{\min}
=
1.3206\times10^{28}\ {\mathrm{J}}
```

At $h=1\,{\mathrm{cm}}$:

```math
M_{\min}
=
1.4693\times10^7\ {\mathrm{kg}}
```

At $h=1\,{\mathrm{mm}}$:

```math
M_{\min}
=
1.4693\times10^5\ {\mathrm{kg}}
```

At $h=1\,\mu{\mathrm{m}}$:

```math
M_{\min}
=
0.1469\ {\mathrm{kg}}
```

but still:

```math
E_{\min}
=
1.3206\times10^{16}\ {\mathrm{J}}
```

At $h=1\,{\mathrm{nm}}$:

```math
M_{\min}
=
1.4693\times10^{-7}\ {\mathrm{kg}}
```

with

```math
E_{\min}
\sim1.32\times10^{10}\ {\mathrm{J}}
```

The extremely important scaling is:

```math
M,E\propto h^2
```

This means microscopic stand-off helps enormously.

It does **not** make the corresponding energy density automatically feasible.

---

# 15. What has actually been discovered by this project

I would classify our results like this.

## KNOWN_RESULT — independently reproduced

### Cosmological-$\Lambda$ defocusing

Confirmed.

### Kottler static-radius behavior

Confirmed.

### Domain-wall gravitational repulsion

Confirmed and consistent with known exact GR results. ([APS Journals][1])

### Tension threshold near

```math
\tau/U=1/2
```

Confirmed and consistent with established planar-wall calculations. ([APS Journals][4])

### Reissner–Nordström repulsive region

Confirmed and consistent with known neutral-test-particle analyses. ([arXiv][2])

---

# 16. Project-derived results that are interesting but not yet independently established

### Finite disk/rim architecture

We obtained:

```math
R/h\simeq4.00615
```

```math
z_{\mathrm{zero}}/R\simeq0.393320
```

```math
M\simeq79.753\,ah^2/G
```

This appears internally consistent in our linearized model.

It needs independent analytical derivation and ideally an independent implementation.

### Abstract static DEC+Laue LP optimum

We obtained:

```math
C_{\mathrm{optimum}}=1
```

This is extremely interesting.

It is **not yet a universal theorem**.

The LP needs to be upgraded to include spatial geometry and local conservation.

---

# 17. Routes that now look comparatively weak

## Negative ADM mass

Mathematically repulsive.

Requires negative shell energy/WEC failure in our exact shell construction.

Positive-mass results additionally make this unattractive under conventional asymptotically flat DEC assumptions. ([arXiv][3])

Low priority.

## Pure cosmological constant

Correct sign.

Hopeless magnitude at observed $\Lambda$.

Low priority.

## Ordinary electrostatic RN device

Excellent mathematical proof of principle.

Engineering requires absurd net charge/field strength.

Keep as reference solution, not primary practical route.

## Ordinary mechanical tension

Far too small because ordinary matter has roughly

```math
\tau/U\ll1
```

Antigravity wants relativistic stresses:

```math
\tau/U\sim1
```

Low priority unless an exotic condensed-matter effective stress can mimic relativistic field stress gravitationally—which would require extremely careful treatment because effective pressure is not automatically the same as fundamental stress-energy.

---

# 18. Highest-priority next simulation: 006B

This should be the **geometry-aware stress-energy optimizer**.

This is, in my assessment, more important than immediately jumping to modified gravity or random exotic fields.

The unresolved question is:

```math
1
\le C_{\mathrm{real}}
\le79.753
```

where

```math
M=C_{\mathrm{real}}\frac{ah^2}{G}
```

We need to determine how close an actual spatially conserved source can get to 1.

### Simulation 006B should discretize space

Use axisymmetry initially.

Each cell should contain variables like:

```math
\epsilon,
p_r,
p_z,
p_\phi
```

and potentially shear stresses.

Impose pointwise:

```math
\epsilon\ge0
```

and DEC constraints such as

```math
|p_i|\le\epsilon
```

Then impose discrete local conservation:

```math
\partial_jT^{ij}=0
```

Not merely integrated Laue balance.

The target acceleration should be computed using the actual spatial Green-function kernel.

Objective:

```math
\min \int \epsilon\,dV
```

Constraint:

```math
a_z(\text{target})\ge a_{\mathrm{requested}}
```

Then optimize source geometry.

### What 006B would tell us

If it reaches:

```math
C\sim1-5
```

then our disk was extremely inefficient and there may be a much better classical architecture.

If it bottoms out around:

```math
C\sim10-100
```

then finite geometry/local stress conservation imposes a major penalty.

If it reproduces approximately:

```math
C\sim79.753
```

then our simple disk/rim architecture may already be surprisingly close to optimal.

This is probably the single most valuable next classical-GR computation.

---

# 19. Simulation 006C — independent verification of 005B

Before relying heavily on 79.753, independently reproduce the finite-disk field.

Do not reuse `finite_tension_disk.py`.

Write an independent numerical integration directly over the stress-energy:

```math
T_{\mu\nu}(\mathbf{x})
```

Numerically integrate the linearized Einstein Green function.

Compare the resulting axial acceleration against:

```text
dimensionless_axis_factor()
```

for many $q,z/R$.

Specifically reproduce:

```math
z_{\mathrm{zero}}/R
=
0.393319893190
```

for $q=1$,

and

```math
R/h
=
4.006149670781
```

at the optimum.

This is important because 005B currently uses an analytical formula and tests that mostly call the same implementation.

Independent numerical integration would substantially increase confidence.

---

# 20. Simulation 006D — exact conservation / finite-thickness support

The current disk and rim are ideal distributions.

Replace them with finite thickness.

Check:

```math
\nabla_\mu T^{\mu\nu}=0
```

throughout the entire source.

Specifically inspect the disk/rim boundary because this is where hidden forces or singular support stresses are most likely.

Then verify NEC/WEC/DEC locally rather than only in idealized components.

This is a prerequisite before calling 005B a physically self-consistent matter configuration.

---

# 21. Quantum negative energy: next major escape route

If 006B shows that ordinary DEC matter cannot reduce the coefficient enough, the next established-physics escape is quantum stress-energy.

Quantum fields can violate classical pointwise energy conditions.

However they obey quantum energy inequalities, which constrain negative energy averaged over time/space. Fewster's reviews describe these QEIs as surviving remnants of classical energy conditions. ([arXiv][7]) Ford/Pfenning/Roman similarly describe restrictions relating negative-energy magnitude and duration. ([arXiv][8])

This means quantum negative energy is worth investigating, but not assuming to be a magic loophole.

---

# 22. Proposed Simulation 007A — Casimir gravitational benchmark

This should be our first quantum calculation.

Use the parallel-plate Casimir stress tensor.

Calculate:

* negative vacuum energy density;
* principal pressures;
* active gravitational combination;
* predicted local gravitational acceleration;
* dependence on plate spacing $d$;
* apparatus support stresses;
* total apparatus mass;
* gravitational field including plates/support.

Scan:

```text
1 mm
100 μm
10 μm
1 μm
100 nm
10 nm
1 nm
```

The fundamental Casimir scaling is roughly:

```math
|\rho_C|\propto\frac{\hbar c}{d^4}
```

The corresponding gravitational scale is therefore roughly:

```math
a_{\mathrm{Casimir}}
\sim
\frac{G\hbar}{c\,d^3}
```

up to order-one/geometric factors.

That scaling is useful because it immediately tells us that quantum-vacuum gravity becomes appreciable only at extremely small length scales.

Casimir vacuum energy itself does gravitate consistently with the equivalence principle once the complete apparatus is treated properly. ([APS Journals][9])

That complete-apparatus point is crucial—we must not count the negative vacuum region while ignoring the plates holding it there.

---

# 23. Proposed Simulation 007B — quantum-energy-inequality benchmark

Instead of choosing a particular apparatus, impose a representative QEI bound.

Ask:

> Given a sampling duration $\tau$ and spatial scale $h$, what maximum negative stress-energy is quantum field theory plausibly allowed to sustain?

Then convert that into maximum gravitational acceleration.

Make the result a map:

```math
a_{\max}(h,\tau)
```

If QEI-limited negative energy remains hopelessly weak until near nuclear or Planck scales, we can deprioritize the whole quantum-vacuum branch.

This is much more informative than casually discussing Casimir plates.

---

# 24. Dynamic sources are another escape route—but probably only an O(1) improvement

006A assumes static stress balance.

A time-dependent source need not satisfy the same instantaneous Laue conditions.

Therefore a dynamic pulse could in principle avoid the factor-of-two support-energy penalty that changed:

```math
\frac{ah^2}{2G}
```

into:

```math
\frac{ah^2}{G}
```

But it does **not** automatically evade the pointwise DEC inequality

```math
S\ge-2\epsilon
```

Therefore I do not currently expect dynamics alone to reduce the energy requirement by dozens of orders of magnitude.

It may reduce coefficients.

It probably does not solve the basic energy scale.

Still, a future Simulation 007C should investigate:

* scalar-field pulses;
* oscillating domain walls;
* moving anisotropic stress;
* retarded gravitational fields;
* transient negative active source;
* gravitational-wave stress contributions.

---

# 25. Modified gravity should come later

Modified gravity gives us enormous freedom:

* scalar-tensor gravity;
* $f(R)$;
* Horndeski-type theories;
* vector-tensor models;
* massive gravity;
* emergent/effective gravity.

But we should not jump there yet.

Why?

Because if we allow ourselves to change Einstein's equations before we have mapped the strongest possible result in Einstein gravity, almost any desired behavior can be engineered into a model.

It becomes difficult to distinguish:

```text
REAL_PHYSICAL_INSIGHT
```

from:

```text
ASSUMED_THEORY_PRODUCES_DESIRED_RESULT
```

I would only move modified gravity ahead of classical/quantum GR once we can state a sharp no-go theorem under established physics.

---

# 26. Important conceptual distinction going forward

We should use three separate terms.

### Local gravitational repulsion

A nearby freely falling neutral object accelerates away from some source region.

We have this.

### Global gravitational repulsion

The asymptotic field of the entire isolated source points outward.

We do **not** have this with positive total ADM mass.

### Practical antigravity

A finite controllable device produces useful local repulsive acceleration with realizable energy/material requirements.

We definitely do **not** have this.

That terminology will prevent us from accidentally turning a valid local-GR result into an unjustified device claim.

---

# 27. Claims ledger

I would record the current claims as:

```text
KNOWN_RESULT:
Cosmological Lambda produces geodesic defocusing.
KNOWN_RESULT_REPRODUCED:
Kottler static-radius transition.
KNOWN_RESULT_REPRODUCED:
Reissner-Nordstrom geometry can produce local neutral-particle
gravitational repulsion.
KNOWN_RESULT_REPRODUCED:
Relativistic domain-wall tension can produce gravitational repulsion.
REPRODUCED:
Positive energy does not forbid local gravitational repulsion.
REPRODUCED:
Negative ADM mass is not required for local gravitational repulsion.
NUMERICAL_MODEL_RESULT:
Finite DEC-supported tension disk has a local repulsive region.
NUMERICAL_MODEL_RESULT:
005B optimum R/h ≈ 4.00614967.
NUMERICAL_MODEL_RESULT:
005B coefficient ≈ 79.753148.
NUMERICAL_OPTIMIZATION_RESULT:
Abstract static DEC+Laue LP coefficient = 1.
CONJECTURE / UNPROVEN:
Coefficient 1 is a universal attainable lower bound for finite static
DEC matter in GR.
NOT_ESTABLISHED:
Finite material capable of realizing required relativistic stress.
NOT_ESTABLISHED:
Stable laboratory domain-wall source.
NOT_ESTABLISHED:
Global positive-mass antigravity.
NOT_ESTABLISHED:
Practical antigravity device.
NOVEL_PHYSICS_CLAIM:
NO.
```

That is the scientifically defensible state.

---

# 28. How to rerun every current simulation

From repo root:

```bash
ROOT="$(pwd)"
PY="$ROOT/.venv/bin/python"
export PYTHONPATH="$ROOT/src"
```

Full verification:

```bash
"$PY" -m pytest -q tests/known_solutions
```

Then the simulations individually:

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

To preserve all output:

```bash
mkdir -p results/logs
for SIM in \
  simulations/001_kottler_weak_field.py \
  simulations/001b_kottler_tidal_eigenvalues.py \
  simulations/002_required_stress_energy.py \
  simulations/003a_finite_vacuum_energy_core.py \
  simulations/003b_israel_shell_mass_search.py \
  simulations/004a_einstein_maxwell_repulsion.py \
  simulations/005a_relativistic_tension_wall.py \
  simulations/005b_finite_supported_antigravity.py \
  simulations/006a_static_dec_lower_bound.py
do
    NAME="$(basename "$SIM" .py)"
    echo
    echo "===== $NAME ====="
    "$PY" "$SIM" 2>&1 |
      tee "results/logs/${NAME}_rerun.log"
done
```

That will let us reproduce the entire research chain without losing Terminal output.

---

# 29. Recommended order for the next research session

I would **not** continue randomly.

The highest-value path is:

```text
FIRST:
Run full ~67-test regression.
SECOND:
006B geometry-aware DEC optimizer with local conservation.
THIRD:
006C independently integrate the 005B stress-energy gravitational field.
FOURTH:
006D finite-thickness/local-conservation realization.
FIFTH:
007A Casimir negative-energy gravitational benchmark.
SIXTH:
007B quantum-energy-inequality bound.
SEVENTH:
007C dynamic/nonstatic stress sources.
ONLY THEN:
008 modified-gravity escape routes.
```

The single most important immediate question is therefore:

```math
\text{How close can an actual finite, locally conserved DEC source get to }
M=\frac{ah^2}{G}\text{?}
```

If we can reduce the explicit coefficient from

```math
79.753
```

toward

```math
1
```

that is a substantial improvement in the classical positive-energy antigravity architecture.

If local conservation forces it to remain large, then the classical route has effectively given us its answer, and we move into quantum negative energy.

---

# 30. Overall state of the project

The project began with the vague question:

> Can antigravity exist?

We now have a much more precise answer.

### Mathematically

**Yes—local gravitational repulsion exists in ordinary general relativity.**

We reproduced multiple independent examples.

### Positive energy?

**Yes.**

RN and domain-wall mechanisms establish that negative energy is not intrinsically required for local repulsion.

### Negative mass?

**No—not for local repulsion.**

Our positive-mass RN and tension models demonstrate this.

### Classical energy conditions?

**They can be satisfied locally.**

We found NEC/WEC/DEC-compatible repulsive configurations.

### Finite source?

**We have a finite linearized model with a repulsive near field.**

005B.

### Attractive far field?

**Yes.**

Finite positive-total-mass configurations return to attraction far away.

That is consistent with the positive-mass structure of GR rather than being a bug. ([arXiv][3])

### Practical?

**Not remotely yet.**

The required relativistic stress-energy densities are enormous.

### Best current physical interpretation

The project has converged on:

```math
\text{Antigravity in GR is fundamentally a stress-engineering problem.}
```

The source should not be thought of as “negative mass.”

The more useful target is:

```math
\text{positive energy with relativistically negative principal pressure/tension}
```

placed near the target while compensating positive stresses are arranged so that the complete isolated system remains physically consistent.

And 006A has now made the next research objective extraordinarily clear:

```math
\text{Find the minimum-energy spatial realization of that stress tensor.}
```

That is where I would resume. It gives us a focused mathematical optimization problem instead of another broad search for mysterious antigravity physics.

[1]: https://journals.aps.org/prd/abstract/10.1103/PhysRevD.30.712 "Gravitationally repulsive domain wall | Phys. Rev. D"
[2]: https://arxiv.org/abs/1012.5411 "Circular motion of neutral test particles in Reissner-Nordström spacetime"
[3]: https://arxiv.org/abs/1110.2087 "The spacetime positive mass theorem in dimensions less than eight"
[4]: https://journals.aps.org/prd/abstract/10.1103/PhysRevD.30.2452 "Repulsive and attractive planar walls in general relativity | Phys. Rev. D"
[5]: https://journals.aps.org/prd/abstract/10.1103/PhysRevD.39.3571 "General-relativistic domain walls | Phys. Rev. D"
[6]: https://arxiv.org/abs/1808.09320 "[1808.09320] Laue's Theorem Revisited: Energy-Momentum Tensors, Symmetries, and the Habitat of Globally Conserved Quantities"
[7]: https://arxiv.org/abs/math-ph/0501073 "Energy Inequalities in Quantum Field Theory"
[8]: https://arxiv.org/abs/gr-qc/9711030 "Quantum Inequalities and Singular Energy Densities"
[9]: https://journals.aps.org/prd/abstract/10.1103/PhysRevD.76.025008 "Relativistic mechanics of Casimir apparatuses in a weak gravitational field | Phys. Rev. D"

### END NOTE - AUGUST 27 2026 - 01:00 CST



### BEGIN NOTE - AUGUST 27 2026 - 03:30 CST

# ANTIGRAVITY_RESEARCH — Comprehensive Carry-Forward Notes

## Session ending August 27, 2026 — Simulations 006B, 006C, and 006D

These notes supersede the scientific frontier described in the currently attached `NOTES.md` and `RESEARCH_BUILDPLAN.md` for the classical positive-energy branch. At the beginning of this session, the buildplan identified Simulation 006B as the highest-value classical experiment, followed by independent verification in 006C and finite-thickness/local-conservation work in 006D. All three of those gates have now been materially completed at the **linearized-GR model level**.

The central outcome is:

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

The appropriate scientific interpretation is therefore:

> **The project has constructed a theoretical existence example of local antigravity-like gravitational repulsion within linearized general relativity using a finite, positive-energy, locally conserved stress-energy distribution satisfying NEC/WEC/DEC. It has not demonstrated a realizable material, a stable apparatus, an exact nonlinear GR solution, or practical antigravity.**

The buildplan explicitly requires those accomplishments to remain separate; its success ladder places finite source and local conservation well below stability, physical realization, energetic plausibility, experimental accessibility, and a practical device.

---

# 1. Scientific state entering this session

Before this session, the project had already established or reproduced several important results:

- cosmological-$\Lambda$ defocusing;
- Kottler static-radius behavior and invariant tidal/geodesic-deviation confirmation;
- positive-energy defocusing for sufficiently negative pressure;
- the localization obstruction for a finite pure $w=-1$ region;
- the Israel-shell result showing that globally repulsive Schwarzschild exterior mass requires negative ADM mass and exotic shell energy in the studied construction;
- Reissner–Nordström local repulsion as an exact Einstein-Maxwell proof of principle, but with extreme electric-field/charge requirements;
- relativistic tension/domain-wall repulsion;
- the finite 005B supported tension disk with $C_{005B}\approx79.753148$;
- the abstract 006A static DEC/Laue result $C_{\mathrm{abstract}}=1$, which was explicitly **not** a universal physical lower bound because spatial geometry and local conservation were missing.

The previous notes therefore identified the unresolved classical problem as roughly

```math
1 \le C_{\mathrm{physical}} \le 79.753148
```

and called 006B the single most important next classical-GR calculation.

---

# 2. Regression baseline before new work

The first action in this session was to reconstruct and run the existing known-solution suite from the provided codebundle.

Result:

```text
BASELINE_TESTS=67
BASELINE_RESULT=67 PASSED
```

This cleared the buildplan's Phase A regression-integrity gate before extending the physics.

The original codebundle contained nine established scientific test files and reflected the repository before 006B was added.

After the new 006B regression tests were added, the suite increased to:

```text
CURRENT_EXPECTED_KNOWN_SOLUTION_TESTS=72
```

Every subsequent major simulation run in this session ended with:

```text
72 passed
```

The final observed regression result after 006D was:

```text
........................................................................ [100%]
72 passed in 0.92s
REGRESSION_RC=0
```

So the scientific regression baseline is currently green.

---

# 3. Simulation 006B — geometry-aware conserved DEC optimization

## 3.1 Original question

006A had shown that, abstractly, DEC permits a very optimistic mass scaling

```math
M \sim \frac{a h^2}{G}
```

with coefficient $C=1$, but the explicit finite 005B disk/rim architecture required

```math
C \approx 79.753148
```

The buildplan asked whether an explicit spatial geometry with pointwise positive energy, pointwise DEC, actual gravitational kernels, and **local** conservation would remain near $79.75$ or approach $1$.

The buildplan's research-decision ranges were:

```text
C ~ 1–5:
    exceptionally promising classical architecture

C ~ 10–100:
    geometry/local conservation impose a substantial penalty

C ~ 79.753:
    original disk/rim may already be near-efficient
```

Those were research-management ranges, not fundamental bounds.

---

# 4. 006B first slice — conserved thin radial optimizer

Rather than immediately paying the complexity cost of a complete 2D $r$-$z$ optimizer, we first attacked the cheapest nontrivial geometry-aware problem: an axisymmetric thin source with arbitrary radial stress structure.

The essential local conservation equation is

```math
\frac{d p_r}{d r}
+
\frac{p_r-p_\phi}{r}
=
0
```

or equivalently

```math
\frac{d(r p_r)}{d r}
=
p_\phi
```

The active weak-field source is

```math
S
=
U+p_r+p_\phi
```

The actual axial spatial kernel was used rather than the optimistic $1/h^2$ bound from 006A. The new source module documents this formulation explicitly.

## 4.1 Efficient conserved architecture discovered

A substantially better architecture than 005B was found.

### Inner region

For

```math
0 \le r \le a
```

use

```math
U=U_0
```

```math
p_r=-U_0
```

```math
p_\phi=-U_0
```

This region has negative active density and provides the local repulsive field.

### Stress-transfer annulus

For

```math
a < r < R
```

use

```math
U
=
U_0\frac{a^2}{r^2}
```

```math
p_r=-U
```

```math
p_\phi=+U
```

This transports the radial tension toward the outside while saturating DEC.

### Outer support

The thin limiting architecture has the minimum-energy support line

```math
\lambda
=
\frac{U_0 a^2}{R}
```

with positive hoop compression of equal magnitude.

This construction obeys local conservation distributionally in the ideal thin-source model and saturates the relevant DEC inequalities.

---

# 5. Closed-form 006B thin optimum

The dimensionless geometry variables were

```math
\alpha=\frac{a}{h}
```

and

```math
\beta=\frac{R}{h}
```

Optimization gave:

```text
INNER_RADIUS_OVER_H=1.437500564637
OUTER_RADIUS_OVER_H=4.701437405300
CLOSED_FORM_COEFFICIENT=23.426710175391
```

Compared with 005B:

```text
005B_COEFFICIENT=79.753148116012
006B_THIN_COEFFICIENT=23.426710175391
IMPROVEMENT_OVER_005B=3.404368241162x
```

Equivalently, the energy-equivalent coefficient fell by approximately 70.6%.

This directly falsified the hypothesis that the simple 005B disk-plus-single-rim architecture might already be near-optimal within the locally conserved axisymmetric thin DEC class.

The newly added 006B source and tests encode the expected optimum near

```text
alpha = 1.43750056
beta  = 4.70143745
C     = 23.426710175391
```

and explicitly classify it as a restricted architecture result rather than a universal GR lower bound.

---

# 6. Independent radial LP verification of 006B

We did not rely only on the closed-form derivation.

A separate discretized radial linear program used:

```text
U_i
q_i = r p_r
```

with conservation reconstructed through

```math
p_\phi
=
\frac{d(r p_r)}{d r}
```

It enforced cellwise:

```math
U \ge 0
```

```math
|p_r| \le U
```

```math
|p_\phi| \le U
```

and minimized total energy using the actual gravitational kernel.

Convergence was:

```text
N=50
C=23.279848767693
relative error=-6.268972749406e-03

N=100
C=23.390094671093
relative error=-1.562981059804e-03

N=200
C=23.417573464368
relative error=-3.900125521157e-04

N=400
C=23.424535334824
relative error=-9.283593602616e-05

N=800
C=23.426231369342
relative error=-2.043846726030e-05
```

The LP converges toward the independent closed-form value:

```text
C=23.426710175391
```

This is strong evidence that the identified piecewise conserved solution is the thin radial optimum or extremely close to it within that restricted class.

Simulation summary:

```text
REGRESSION_BASELINE_RECONSTRUCTED=YES
INDEPENDENT_LP_CONVERGENCE=PASS
POINTWISE_POSITIVE_ENERGY=YES
POINTWISE_DEC=YES
LOCAL_RADIAL_CONSERVATION=YES
ACTUAL_SPATIAL_GRAVITATIONAL_KERNEL=YES
TARGET_OUTWARD_ACCELERATION_NORMALIZED=YES
TOTAL_ENERGY_MINIMIZED=YES_WITHIN_THIN_RADIAL_SUBCLASS
```

Claim:

```text
NUMERICAL_OPTIMIZATION_RESULT
```

Not:

```text
FULL_2D_GLOBAL_GR_OPTIMUM
```

---

# 7. New 006B regression tests

A new regression file was added:

```text
tests/known_solutions/test_axisymmetric_thin_stress.py
```

Five focused tests passed:

```text
5 passed
```

They protect:

- the radial kernel primitive;
- integrated stress-trace cancellation;
- local conservation in the smooth regions;
- pointwise DEC;
- independent reconstruction of the 005B optimum;
- the improved 006B conserved-annular optimum.

The full suite consequently rose from 67 to:

```text
72 passed
```

and remained there through the rest of the session.

---

# 8. 006B full $r$-$z$ exact-DEC solver prerequisite

The next question was whether genuine 2D geometry and $r$-$z$ shear could improve on $C=23.4267$.

Allowing shear gives the spatial stress block

```math
\begin{pmatrix}
p_r & T_{rz} \\
T_{rz} & p_z
\end{pmatrix}
```

Diagonal inequalities alone are not sufficient for DEC once $T_{rz}\neq0$.

Exact type-I DEC requires the principal-stress eigenvalues to obey

```math
|\lambda_i| \le \epsilon
```

For the $r$-$z$ block this can be expressed as a second-order-cone constraint.

Therefore CVXPY was added.

## 8.1 Dependency change

Installed:

```text
cvxpy==1.9.2
```

Observed available solvers:

```text
CLARABEL
SCS
SCIPY
HIGHS
OSQP
```

`pyproject.toml` was modified to record:

```text
cvxpy==1.9.2
```

The environment installed transitive solver packages including Clarabel, SCS, OSQP, HiGHS, and related dependencies.

---

# 9. Exact DEC conic self-test

Before trusting the optimizer, an independent numerical equivalence test compared direct stress eigenvalues against the conic DEC constraint.

Test stress eigenvalues:

```text
-0.937056879750
-0.600000000000
+0.487056879750
```

Direct required energy density:

```text
DIRECT_DEC_MIN_EPSILON=0.937056879750
```

Conic optimizer result:

```text
CONIC_DEC_MIN_EPSILON=0.937056878751
```

Difference:

```text
ABSOLUTE_ERROR=9.996471428408e-10
RELATIVE_ERROR=1.066794518500e-09
```

Result:

```text
EXACT_DEC_SOC_EQUIVALENCE=PASS
POINTWISE_SHEAR_DEC_SOLVER_GATE=GREEN
```

This removed a potentially serious formulation error before the full 2D calculation.

---

# 10. Full $r$-$z$ staggered finite-volume optimizer

A second 006B simulation was added:

```text
simulations/006b_full_rz_decision.py
```

The formulation used:

```text
STRESS_GRID=STAGGERED_FINITE_VOLUME
LOCAL_CONSERVATION=EXACT_CELL_FORCE_BALANCE
DEC=EXACT_EIGENVALUE_SOC
KERNEL=EXACT_ANNULAR_CELL_INTEGRAL
```

Variables included:

```text
epsilon
p_phi
p_r on radial faces
p_z on vertical faces
T_rz on vertices
```

Staggering was deliberately used to reduce the risk of checkerboard/odd-even stress modes that can occur with naive collocated centered discretizations.

The solver also independently reconstructed:

- exact DEC eigenvalue violations;
- cell conservation residuals;
- integrated Laue balances;
- achieved acceleration.

---

# 11. Initial full $r$-$z$ finite-grid results

The first five cases gave:

```text
6x4, RMAX=5, depth=1
C=326.856547069958

8x6, RMAX=5, depth=1
C=80.635416635818

10x8, RMAX=5, depth=1
C=51.238386636844

8x6, RMAX=7, depth=2
C=76.194048456460

10x8, RMAX=7, depth=2
C=53.002083298871
```

All had:

```text
ACCELERATION≈1
DEC residuals tiny
conservation residuals tiny
integrated stress trace≈0
```

The best initial value was:

```text
51.238386636844
```

but it was immediately recognized as **not converged** because the compact refinement sequence fell extremely rapidly:

```text
326.86 -> 80.64 -> 51.24
```

Therefore we explicitly did **not** promote $51.24$ to a physical coefficient.

---

# 12. Important analytical observation about the full 2D problem

The full 2D optimization placed no lower limit on thickness and no upper limit on energy density.

Therefore the known thin solution can be approached as a distributional limiting sequence by concentrating energy/stress into a thinner layer.

Consequently, within the assumptions of this unrestricted continuum problem, there is no reason for the continuum full $r$-$z$ infimum to be forced *above* the known admissible thin value.

This was an important reason not to misinterpret coarse finite-volume values such as $51.24$ as physical lower bounds.

---

# 13. Thin-limit recovery using the independent full $r$-$z$ code

We deliberately forced the full $r$-$z$ solver into a thin slab and increased radial resolution.

Results:

```text
12x2
depth=0.125
C=48.782287947292

16x2
depth=0.125
C=37.700669553189

20x2
depth=0.125
C=32.954754666944
```

A simple $1/N_r^2$ extrapolation produced:

```text
THIN_EXTRAPOLATED_C=23.902968107527
```

or:

```text
THIN_EXTRAPOLATED_RATIO=1.020329697536
```

This is only about 2.03% above the independently derived exact thin coefficient:

```text
23.426710175391
```

This was a major validation of the full 2D formulation.

---

# 14. Matched-resolution depth experiment

Holding the grid scales fixed at

```text
dr=0.3125
dz=0.125
```

while increasing available depth gave:

```text
depth=0.5
C=39.446944669376

depth=1.0
C=34.637229670751

depth=2.0
C=30.331762534312
```

The nested-domain test behaved correctly:

```text
NESTED_DOMAIN_MONOTONICITY=PASS
```

Energy improvements were:

```text
0.5 -> 1.0:
12.1928708%

1.0 -> 2.0:
12.4301717%
```

This showed that genuine 2D stress routing had some value at finite resolution.

---

# 15. Extended depth-asymptote test

Further matched-resolution depth tests gave:

```text
depth=4
C=28.253514148213

depth=8
C=27.523479508905
```

The improvement from $4h$ to $8h$ fell to only:

```text
2.5838719937%
```

Therefore the depth benefit was clearly beginning to saturate.

This also produced an important engineering interpretation:

> Increasing source depth is an increase in source size, not free improvement. Even if deeper stress routing lowers total energy at fixed target stand-off, it may make the apparatus less compact.

No depth-only route toward $C\sim1$-$5$ appeared.

---

# 16. Radial convergence at depth $8h$

At fixed:

```text
depth=8
dz=0.125
RMAX=5
```

radial refinement gave:

```text
NR=16
C=27.523479508905

NR=20
C=27.162622405315

NR=24
C=27.020680149787
```

Simple extrapolations gave:

```text
1/NR^2 fit:
C_inf=26.598356460580

1/NR fit:
C_inf=25.976148873579
```

So at fixed $dz=0.125$, the apparent continuum limit remained above the thin result.

But this was not the end of the convergence analysis.

---

# 17. Vertical-refinement result — critical 006B observation

The decisive additional test held:

```text
NR=16
depth=8
RMAX=5
```

fixed while halving vertical spacing from:

```text
dz=0.125
```

to:

```text
dz=0.0625.
```

The coefficient fell from:

```text
27.523479508905
```

to:

```text
25.994503758080.
```

This showed that a substantial portion of the apparent $26$-$27$ plateau was a **vertical-discretization artifact**.

The new case also remained numerically excellent:

```text
ACCELERATION=1.000000000014
MAX_DEC_VIOLATION=1.048e-09
MAX_CONSERVATION_RESIDUAL=1.350e-12
STRESS_TRACE_INTEGRAL=-1.891e-15
```

---

# 18. 2D continuum diagnostic

Using the available radial and vertical refinement points, four simple first-/second-order discretization models produced:

```text
radial order 1, vertical order 1:
C=22.949343418307

radial order 1, vertical order 2:
C=23.958278570064

radial order 2, vertical order 1:
C=23.556385155751

radial order 2, vertical order 2:
C=24.570375590694
```

Thus the depth-88 continuum diagnostic bracket was:

```text
22.949343418307
to
24.570375590694
```

The independent thin coefficient

```text
23.426710175391
```

lies inside this bracket.

After applying the diagnostic residual depth correction, the combined depth/grid bracket was:

```text
22.554042171855
to
24.175074344242
```

Again:

```text
23.426710175391
```

lies inside it.

Final 006B 2D interpretation:

```text
FULL_RZ_CONTINUUM_EVIDENCE=CONSISTENT_WITH_THIN_REFERENCE
VERIFIED_FULL_RZ_IMPROVEMENT_BELOW_THIN=NO
VERIFIED_FINITE_2D_PENALTY_ABOVE_THIN=NO
C_1_TO_5_ROUTE_FOUND=NO
GLOBAL_FULL_RZ_OPTIMUM=NOT_ESTABLISHED
```

The extrapolation itself remains diagnostic rather than proof.

---

# 19. Final 006B decision

The strong result of 006B is not a universal theorem that $C=23.4267$.

The defensible result is:

> Within the most mature static, axisymmetric, positive-energy, DEC-constrained, locally conserved linearized-GR architectures studied so far, the energy coefficient is of order $20$-$25$, with a rigorously characterized restricted thin architecture at $C=23.426710175391$. No evidence was found for a dramatic collapse to $C\sim1$-$5$.

This places the classical problem firmly in the buildplan's

```text
C ~ 10–100
```

decision regime, meaning spatial geometry and conservation impose a substantial penalty relative to the abstract 006A coefficient $C=1$.

---

# 20. Physical scaling of the best 006B architecture

Using

```math
M
=
C\frac{a h^2}{G}
```

with

```text
C≈23.4267
a=1g
```

gives approximately:

```text
h=1 m:
M≈3.44e12 kg

h=1 cm:
M≈3.44e8 kg

h=1 mm:
M≈3.44e6 kg

h=1 micrometer:
M≈3.44 kg
```

For $h=1\ \mathrm{m}$, the energy equivalent is roughly:

```text
E≈3.09e29 J
```

Even the abstract $C=1$ result would still require roughly:

```text
1.47e11 kg
```

of mass-energy equivalent for $1g$ at $1\ \mathrm{m}$.

This is why reducing $C$ from $79.75$ to $23.43$ is scientifically important but does not solve the practical energy problem.

---

# 21. Simulation 006C — independent 005B Green-function verification

The buildplan explicitly required the 005B gravitational field to be reconstructed without reusing its analytic production formula before treating $79.753148$ as highly reliable.

A new simulation was created:

```text
simulations/006c_independent_finite_disk_field.py
```

Its primary computation directly numerically integrates the linearized gravitational Green function over:

- the membrane active stress-energy;
- the complete support rim contribution.

Only after the independent values are obtained is the production 005B field implementation imported for comparison.

---

# 22. 006C initial numerical failure and repair

The first 006C run already produced an extremely strong field comparison:

```text
COMPARISON_POINT_COUNT=30
MAX_ABSOLUTE_FIELD_ERROR=2.220446049250e-16
MAX_RELATIVE_FIELD_ERROR=1.419475206905e-15
FIELD_GRID_MATCH=PASS
```

However, the root finder then failed.

Cause:

- the independent membrane radial integral was evaluated at $y=z/R=10^{-6}$;
- the original adaptive radial quadrature became sharply localized near $r=0$;
- SciPy emitted an integration warning;
- the inaccurate endpoint value prevented `brentq` from seeing the correct sign-changing bracket.

This was a numerical-conditioning problem, not a physics disagreement.

A separate shell-harness problem was also discovered:

```text
python ... | tee ...
```

without `set -o pipefail` caused the shell to report the success code from `tee` instead of the crashed Python process.

That workflow bug was corrected.

---

# 23. 006C stable Green-function coordinate transform

The numerical integration was repaired using the variable transformation

```math
r
=
y\tan\theta
```

The problematic radial kernel

```math
\int_0^1
\frac{y r}{(r^2+y^2)^{3/2}}
\,dr
```

becomes the regular numerical integral

```math
\int_0^{\arctan(1/y)}
\sin\theta
\,d\theta
```

The transformed integral was **still evaluated numerically**.

The code did not substitute the known analytic 005B field formula.

The root finder was also changed to scan the independently computed field and discover its own sign-changing interval rather than assuming the known root.

---

# 24. Final 006C results

The repaired implementation produced:

```text
FIELD GRID:
30 comparison points

MAX_ABSOLUTE_FIELD_ERROR=
2.220446049250e-16

MAX_RELATIVE_FIELD_ERROR=
1.419475206905e-15

FIELD_GRID_MATCH=PASS
```

Independent repulsive zero:

```text
NUMERIC_Z_ZERO_OVER_R=
0.393319893190334

REFERENCE_Z_ZERO_OVER_R=
0.393319893190329

ABSOLUTE_ERROR=
4.773959005888e-15

REPULSIVE_ZERO_MATCH=PASS
```

Independent optimized geometry:

```text
OPTIMAL_H_OVER_R=
0.249616231845956

OPTIMAL_R_OVER_H=
4.006149730747969

REFERENCE_R_OVER_H=
4.006149670781000

ABSOLUTE_ERROR=
5.996696916810e-08
```

Independent coefficient:

```text
NUMERIC_005B_COEFFICIENT=
79.753148116012255

REFERENCE_005B_COEFFICIENT=
79.753148116011999

ABSOLUTE_ERROR=
2.557953848736e-13
```

Final:

```text
FIELD_GRID_VERIFIED=YES
REPULSIVE_ZERO_VERIFIED=YES
005B_OPTIMUM_VERIFIED=YES
SIMULATION_006C=GREEN
CLAIM_CLASSIFICATION=INDEPENDENT_NUMERICAL_VERIFICATION
```

This materially upgrades confidence in Simulation 005B.

---

# 25. Simulation 006D — finite-thickness conserved source

The buildplan's Phase D required replacing ideal membranes/rims with finite-thickness stress-energy and explicitly evaluating local conservation and energy conditions throughout the source.

A new simulation was created:

```text
simulations/006d_finite_thickness_conserved_source.py
```

This produced the strongest project-derived classical result so far.

---

# 26. Central 006D analytical construction

Define

```math
q(r)
=
r p_r(r)
```

Then impose

```math
p_\phi(r)
=
\frac{d q}{d r}
```

With

```math
p_z=0
```

and

```math
T_{rz}=0
```

the static cylindrical radial conservation equation becomes identically

```math
\frac{d p_r}{d r}
+
\frac{p_r-p_\phi}{r}
=
0
```

Equivalently:

```math
\frac{1}{r}
\left[
\frac{d(r p_r)}{d r}
-
p_\phi
\right]
=
0
```

The vertical conservation equation is also identically satisfied because:

```text
p_z=0
T_rz=0.
```

---

# 27. Finite vertical thickness

The complete in-plane energy/stress distribution was multiplied by a smooth, compact, nonnegative finite-thickness vertical profile.

The tested slab occupies:

```math
-t \le z \le 0
```

with target surface stand-off $h=1$.

A normalized compact polynomial bump of the form

```math
30x^2(1-x)^2
```

was used across the slab.

Because all components carrying a $z$ index are zero, multiplying the in-plane conserved source by this static $z$ profile does not generate a new vertical stress divergence in the linearized flat-background conservation equations.

This converts the zero-thickness source into a genuine nonzero-thickness distribution.

---

# 28. Finite radial support collar

The singular thin support line of 006B was removed.

A smooth cubic `smoothstep` transition was used to bring $q(r)$ continuously to zero over a finite outer radial collar.

At the outer boundary:

```text
q=0
dq/dr=0
```

so there is no remaining hidden line force.

The inner transition was also smoothed.

Therefore 006D has:

```text
SINGULAR_OUTER_RING=NO
FINITE_RADIAL_SUPPORT_COLLAR=YES
```

This falsifies the idea that the repulsive architecture intrinsically requires an ideal singular rim.

---

# 29. Pointwise energy conditions in 006D

Energy density was chosen as

```math
\epsilon
=
\max\left(
|p_r|,
|p_\phi|
\right)
```

With $p_z=0$, this enforces the static type-I DEC by construction.

The numerical checks found:

```text
MAX_DEC_VIOLATION=
0.000000000000e+00

MIN_NEC_MARGIN=
0.000000000000e+00
```

Therefore:

```text
NEC=PASS
WEC=PASS
DEC=PASS
POINTWISE_POSITIVE_ENERGY=YES
```

The zero NEC margin means parts of the optimized source **saturate** the energy condition; it does not mean the check was absent.

---

# 30. Local-conservation verification in 006D

Although the source is analytically constructed to satisfy radial conservation, an independent control-volume reconstruction was also performed.

Result:

```text
MAX_CONTROL_VOLUME_CONSERVATION_RESIDUAL=
3.103073353827e-14
```

Integrated stress balance:

```text
MAX_INTEGRATED_STRESS_TRACE=
2.922107000813e-13
```

Therefore:

```text
LOCAL_CONSERVATION=PASS
LAUE_STRESS_BALANCE=PASS
```

This is local conservation at the **linearized/static background order**.

It is not yet an exact nonlinear demonstration of:

```math
\nabla_\mu T^{\mu\nu}=0
```

in the self-consistent full metric.

The simulation correctly prints:

```text
EXACT_NONLINEAR_GR_CONSERVATION=NOT_ESTABLISHED
```

---

# 31. 006D finite-thickness convergence

The finite thickness and outer support-collar scale were reduced systematically.

Results:

```text
scale=0.40000
thickness/h=0.40000
C=38.037638025730

scale=0.20000
thickness/h=0.20000
C=29.559369544823

scale=0.10000
thickness/h=0.10000
C=26.258214373557

scale=0.05000
thickness/h=0.05000
C=24.789414887263

scale=0.02500
thickness/h=0.02500
C=24.095429926871

scale=0.01250
thickness/h=0.01250
C=23.757986246352

scale=0.00625
thickness/h=0.00625
C=23.591586299249
```

The independently established thin limit is:

```text
23.426710175391
```

The finest finite source differs by only:

```text
0.7037954651904%
```

Result:

```text
MONOTONIC_APPROACH_TO_THIN=YES
THIN_LIMIT_RECOVERY=PASS
```

---

# 32. Final 006D result

Final terminal classification:

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

C_FINITE_BEST_TESTED=
23.591586299249

C_THIN_LIMIT=
23.426710175391

SIMULATION_006D=GREEN

CLAIM_CLASSIFICATION=
CONSTRUCTIVE_LINEARIZED_GR_STRESS_ENERGY_RESULT
```

The simulation correctly retains:

```text
EXACT_NONLINEAR_GR_CONSERVATION=NOT_ESTABLISHED
DYNAMIC_STABILITY=NOT_ESTABLISHED
KNOWN_MATERIAL_REALIZATION=NO
PRACTICAL_ANTIGRAVITY_DEVICE=NO
```

---

# 33. What 006D actually establishes

The strongest defensible project statement is now:

> **There exists, within static linearized general relativity, an explicit finite-radius, finite-thickness, nonsingular, positive-energy, locally conserved stress-energy distribution satisfying NEC/WEC/DEC that produces a locally outward gravitational field while retaining positive total/far-field gravitational mass.**

This is stronger than merely showing a negative active-density cell or an infinite domain wall.

It addresses:

- finite source;
- positive energy;
- classical energy conditions;
- support completion;
- local conservation;
- finite thickness;
- removal of the singular rim;
- local gravitational repulsion;
- positive far-field mass.

It remains a **stress-energy construction**, not a known material or device.

---

# 34. Current success-ladder position

Using the buildplan's success ladder, the project has now effectively reached approximately **Level 5 within the stated linearized-GR approximation**:

```text
LEVEL 0 — Mathematical sign:
YES

LEVEL 1 — Physical gravitational observable:
YES
Local outward acceleration of a neutral test body in the weak-field model.

LEVEL 2 — Established-theory consistency:
YES WITHIN LINEARIZED GR
NOT YET A SELF-CONSISTENT EXACT NONLINEAR SOLUTION

LEVEL 3 — Acceptable stress-energy characterized:
YES
Positive energy and NEC/WEC/DEC.

LEVEL 4 — Finite source:
YES

LEVEL 5 — Local conservation:
YES AT LINEARIZED/STATIC ORDER

LEVEL 6 — Stability:
NO

LEVEL 7 — Physical realization:
NO

LEVEL 8 — Energetic plausibility:
NO

LEVEL 9 — Experimental accessibility:
NO

LEVEL 10 — Practical antigravity:
NO
```

The formal ladder itself warns not to describe progress as reaching levels whose requirements have not been satisfied.

---

# 35. What was falsified or weakened in this session

Several hypotheses were materially weakened or falsified.

### Hypothesis: 005B might already be near-optimal

Falsified within the thin radial DEC/conservation subclass.

```text
79.753 -> 23.427
```

is a 3.404× improvement.

### Hypothesis: finite geometry/local conservation might permit $C\sim1$-$5$

Not supported.

All mature results remain approximately:

```text
C ~ 20–25
```

rather than:

```text
C ~ 1–5.
```

### Hypothesis: the coarse full $r$-$z$ $C=51.24$ represented a physical finite-thickness penalty

Falsified.

The value collapsed substantially under spatial refinement, particularly vertical refinement.

### Hypothesis: genuine 2D shear clearly beats the thin architecture

Not established.

Continuum diagnostics bracket the thin value rather than showing a stable coefficient below it.

### Hypothesis: finite thickness necessarily destroys the local repulsive source

Falsified within linearized GR.

006D gives an explicit finite-thickness sequence retaining the effect.

### Hypothesis: a singular support ring is required

Falsified.

A finite smooth radial support collar works.

### Hypothesis: positive energy plus DEC prevents local gravitational repulsion

Falsified within the stated linearized model.

006D has:

```text
epsilon >= 0
NEC/WEC/DEC pass
outward local field
```

simultaneously.

### Hypothesis: these results imply practical antigravity

Not supported.

Energetics, stability, material realization, and experiment remain unresolved.

---

# 36. Important terminology going forward

The older project notes already made this distinction, and it is now more important than ever.

### Local gravitational repulsion

A neutral test object in the relevant near-field region accelerates away from the source.

```text
PROJECT_STATUS=YES
```

### Global gravitational repulsion

The entire isolated positive-total-mass source has an outward asymptotic gravitational field.

```text
PROJECT_STATUS=NO
```

The 006D far field remains attractive.

### Practical antigravity

A controllable physical apparatus generates useful gravitational repulsion with realizable material, energy, stability, and experimental requirements.

```text
PROJECT_STATUS=NO
```

Avoid using “antigravity proved” without explicitly attaching the word **local**, **theoretical**, and **within linearized GR**.

---

# 37. Current claim ledger

Recommended claim classifications:

```text
KNOWN_RESULT_REPRODUCED:
Cosmological-Lambda gravitational defocusing.

KNOWN_RESULT_REPRODUCED:
Kottler static-radius and tidal behavior.

KNOWN_RESULT_REPRODUCED:
Positive-energy relativistic tension/domain-wall repulsion.

KNOWN_RESULT_REPRODUCED:
Reissner-Nordstrom local repulsive region.

PROJECT_DERIVED_INDEPENDENTLY_VERIFIED_RESULT:
005B finite supported tension disk:
R/h ≈ 4.0061497
z_zero/R ≈ 0.393319893
C ≈ 79.753148116012.

PROJECT_DERIVED_NUMERICAL_OPTIMIZATION_RESULT:
006B thin locally conserved DEC architecture:
C = 23.426710175391.

PROJECT_DERIVED_NUMERICAL_OBSERVATION:
Full-rz optimizer continuum diagnostics are consistent with the thin
C≈23.43 result.
No stable 2D improvement below it has been demonstrated.

PROJECT_DERIVED_CONSTRUCTIVE_LINEARIZED_GR_STRESS_ENERGY_RESULT:
006D finite-radius, finite-thickness, locally conserved,
positive-energy NEC/WEC/DEC source with local outward gravity.

NOT_ESTABLISHED:
Exact nonlinear-GR realization.

NOT_ESTABLISHED:
Dynamical stability.

NOT_ESTABLISHED:
Known material/field realization.

NOT_ESTABLISHED:
Energetically practical antigravity.

NOT_ESTABLISHED:
Laboratory antigravity.

NOT_ESTABLISHED:
Practical antigravity device.
```

---

# 38. New and modified source files from this session

The following substantive files were added during this session:

```text
src/antigravity_research/geometry/axisymmetric_thin_stress.py

tests/known_solutions/test_axisymmetric_thin_stress.py

simulations/006b_geometry_aware_dec_optimizer.py

simulations/006b_full_rz_decision.py

simulations/006c_independent_finite_disk_field.py

simulations/006d_finite_thickness_conserved_source.py
```

Modified:

```text
pyproject.toml
```

to add:

```text
cvxpy==1.9.2
```

The 006B patch source itself documented the restricted thin architecture, assumptions, local conservation, DEC, validation plan, and explicit prohibition against promoting its coefficient to a universal GR bound.

---

# 39. New generated scientific outputs

Known generated files include:

```text
results/data/006b_geometry_aware_dec_optimizer.csv
results/figures/006b_geometry_aware_dec_convergence.png
results/logs/006b_geometry_aware_dec_optimizer.log

results/data/006b_full_rz_decision.csv
results/logs/006b_full_rz_decision.log

results/data/006b_depth_asymptote.csv

results/data/006c_independent_finite_disk_field.csv
results/logs/006c_independent_finite_disk_field.log

results/data/006d_finite_thickness_conserved_source.csv
results/logs/006d_finite_thickness_conserved_source.log
```

Some later 006B radial/vertical convergence experiments were run as inline terminal programs and **were not necessarily persisted into dedicated CSV/log files**.

Their important numbers must therefore be copied into `NOTES.md` or a consolidated result artifact before relying on the terminal history as the sole record.

---

# 40. Repository state / Git warning

The original codebundle already showed a dirty/untracked working tree before this session.

The last explicit `git status --short` shown during this session, before 006C/006D were added, included:

```text
M pyproject.toml

?? results/data/006b_full_rz_decision.csv
?? results/data/006b_geometry_aware_dec_optimizer.csv
?? results/figures/006b_geometry_aware_dec_convergence.png
?? results/logs/006b_full_rz_decision.log
?? results/logs/006b_geometry_aware_dec_optimizer.log

?? simulations/006b_full_rz_decision.py
?? simulations/006b_geometry_aware_dec_optimizer.py

?? src/antigravity_research/geometry/axisymmetric_thin_stress.py
?? tests/known_solutions/test_axisymmetric_thin_stress.py
```

006C and 006D were created afterward and are therefore also likely untracked unless separately saved/committed outside the shown terminal output.

**Do not assume this session is committed or pushed.**

First repository action next session:

```text
git status --short
```

Then inspect and preserve the complete scientific slice.

---

# 41. Regression protection still needed

Current full suite:

```text
72 passed
```

However, 006C and 006D are currently protected mainly by their simulation self-checks rather than dedicated known-solution regression files.

Before large refactors, add focused tests for at least:

### 006C

Protect:

```text
z_zero/R ≈ 0.393319893190334
R/h ≈ 4.00614973
C_005B ≈ 79.753148116012
```

and at least several direct Green-function field points.

### 006D

Protect:

- $q=r p_r$ conservation identity;
- $p_\phi=dq/dr$;
- outer collar termination;
- DEC;
- NEC/WEC;
- integrated stress balance;
- monotonic finite-thickness convergence;
- one or two benchmark coefficients;
- finest tested $C\approx23.5915863$.

The next expected regression count should rise above 72 once these are added.

---

# 42. Documentation that must be updated

The currently attached `RESEARCH_BUILDPLAN.md` is now scientifically stale because it still lists 006B/006C/006D as the active future path.

It should be updated to state:

```text
PHASE_A_REGRESSION=COMPLETE

PHASE_B_006B=COMPLETE_AT_DECISION_LEVEL
C_THIN=23.426710175391
FULL_RZ_EVIDENCE=CONSISTENT_WITH_THIN
C_1_TO_5_ROUTE_FOUND=NO

PHASE_C_006C=COMPLETE
005B_FIELD_INDEPENDENTLY_VERIFIED=YES

PHASE_D_006D=COMPLETE_AT_LINEARIZED_MODEL_LEVEL
FINITE_THICKNESS=YES
LOCAL_CONSERVATION=YES
NEC_WEC_DEC=YES
C_FINITE_BEST_TESTED=23.591586299249

CLASSICAL_DECISION_GATE=REACHED
```

Also update:

```text
NOTES.md
README.md
CLAIMS.md
ASSUMPTIONS.md
```

where appropriate.

Do not overwrite the historical 006A/005B discussion; append the new result and explicitly explain which earlier uncertainties were resolved.

---

# 43. Classical-GR decision gate

The buildplan states that after 006B, 006C, and 006D the project must make an explicit decision rather than indefinitely preserving the branch.

Its continuation criteria include:

- local conservation works;
- repulsive near field survives;
- coefficient falls substantially;
- plausible field-theory source exists;
- more optimization has clear expected value.

Our status is mixed:

```text
LOCAL_CONSERVATION=YES
REPULSIVE_FIELD_SURVIVES=YES
COEFFICIENT_REDUCED_SUBSTANTIALLY_FROM_005B=YES

PLAUSIBLE_FIELD_THEORY_REALIZATION=NO
ENERGY_REQUIREMENT_REMAINS_ENORMOUS=YES
MORE_STATIC_GEOMETRY_OPTIMIZATION_HIGH_VALUE=NO
```

Recommended decision:

```text
CLASSICAL_POSITIVE_ENERGY_STATIC_BRANCH=
PRESERVE_AS_STRONG_REFERENCE_RESULT

FURTHER_C_COEFFICIENT_TUNING=
DEPRIORITIZE

CLASSICAL_STABILITY_OR_REALIZABILITY_WORK=
ONLY_IF_A_SPECIFIC_PLAUSIBLE_MATTER_FIELD_MODEL_IS_IDENTIFIED

NEXT_PRIMARY_BRANCH=
QUANTUM_STRESS_ENERGY
```

This follows the buildplan stop rule rather than protecting sunk effort.

---

# 44. Why we should not spend the next session chasing $23.43\rightarrow20$

Even an order-unity coefficient cannot fix the fundamental scale

```math
M
\sim
\frac{a h^2}{G}
```

At $1g$ and $1\ \mathrm{m}$, even the abstract $C=1$ result still corresponds to approximately:

```text
1.47e11 kg
```

of mass-energy equivalent.

Therefore a modest coefficient improvement:

```text
23.4 -> 20
```

cannot alter the engineering conclusion.

A genuinely game-changing pathway must instead:

- change the scaling;
- exploit a fundamentally different source;
- find a large coherent/dynamical effect;
- use quantum stress-energy in a way not eliminated by complete-apparatus costs/QEIs;
- or eventually motivate an observationally viable modification of gravity.

---

# 45. Preliminary quantum reconnaissance performed this session

No 007-series repository simulation was completed.

However, the literature/analytical reconnaissance at the end of the session identified the correct next targets.

Brown and Maclay explicitly calculated the electromagnetic vacuum stress-energy tensor between perfectly conducting parallel plates, providing the foundational stress tensor needed for a proper Casimir calculation. ([APS Journals](https://journals.aps.org/pr/abstract/10.1103/PhysRev.184.1272 "Vacuum Stress between Conducting Plates: An Image Solution | Phys. Rev."))

Costa and Matsas showed that a complete Casimir apparatus held in equilibrium has nonnegative total mass when the additional supporting matter satisfies the DEC. This reinforces the project's rule that one must not count the negative vacuum region while ignoring the plates/support system. ([APS Journals](https://journals.aps.org/prd/abstract/10.1103/PhysRevD.105.085016 "Can quantum mechanics breed negative masses? | Phys. Rev. D"))

Ford and Roman established quantum-inequality constraints limiting the magnitude and duration of negative energy density in four-dimensional Minkowski spacetime for free quantum fields. ([DOI](https://doi.org/10.1103/PhysRevD.51.4277 "Averaged energy conditions and quantum inequalities | Phys. Rev. D"))

These support exactly the quantum sequence already specified in the buildplan.

---

# 46. Preliminary Casimir scale estimate — NOT YET SIMULATION 007A

For ideal parallel plates with separation $d$, the standard zero-temperature Casimir scale is

```math
K
=
\frac{\pi^2\hbar c}{720d^4}
```

For the ideal electromagnetic region, the active gravitational source is negative.

A simple infinite-plane linearized estimate gives the outward acceleration scale

```math
a_{\mathrm{Casimir}}
\sim
\frac{\pi^3G\hbar}{180c\,d^3}
```

Setting this optimistic ideal expression equal to $1g$ gives approximately:

```text
d ≈ 7.44e-19 m
```

which is vastly below ordinary nuclear dimensions.

This was **only an analytical reconnaissance estimate**.

It has not yet been promoted to a repository result and does not include the complete apparatus.

The complete-apparatus requirement is precisely why Simulation 007A must come next.

---

# 47. Highest-value next action — Simulation 007A

The buildplan already specifies the first quantum experiment:

## Simulation 007A — Complete Casimir Benchmark

It should model:

```text
negative Casimir-region stress-energy
plates
supports
total apparatus energy
total apparatus stress-energy
complete gravitational response
```

The crucial rule is:

> **Never calculate the gravitational benefit of the negative vacuum region without including the matter and stresses required to produce and hold the configuration.**

Primary outputs should include:

```text
vacuum energy density
principal stresses
active gravitational density
plate/support energy
total apparatus mass
local gravitational acceleration
far-field mass
dependence on separation d
energy-condition behavior of complete apparatus
```

Recommended spacing scan remains:

```text
1 mm
100 micrometers
10 micrometers
1 micrometer
100 nm
10 nm
1 nm
```

with smaller scales added only as a theoretical asymptotic benchmark.

---

# 48. Simulation 007B — quantum energy inequality bound

After 007A, implement the buildplan's QEI benchmark.

Question:

> Given spatial scale $h$ and sampling duration $\tau$, what negative stress-energy can established QFT sustain, and what is the corresponding maximum gravitational acceleration?

Target output:

```math
a_{\max}(h,\tau)
```

If the QEI result shows that useful negative-energy gravity requires nuclear, subnuclear, or still smaller scales, the quantum-vacuum branch can be deprioritized rapidly.

The buildplan explicitly identifies this as the second quantum gate.

---

# 49. Simulation 007C — dynamic sources

Only after 007A/007B, unless a cheaper analytic no-go check changes priority.

Candidate systems:

```text
scalar-field pulses
moving domain walls
oscillating anisotropic stresses
transient field configurations
retarded gravitational response
```

The project already has an important constraint:

Time dependence may relax static Laue/support relations, but it does **not** automatically evade pointwise stress-energy constraints.

The earlier notes therefore expected dynamics to perhaps improve order-unity coefficients rather than eliminate dozens of orders of magnitude of energy cost.

The key question for 007C should be:

> Can dynamics improve the **parametric scaling**, rather than merely modify $C$ by a factor of order unity?

If not, close it rapidly.

---

# 50. Modified gravity remains deferred

Do not jump to modified gravity yet.

The buildplan explicitly places modified gravity after established GR and QFT have been quantitatively constrained.

Later candidates may include:

```text
scalar-tensor
f(R)
Horndeski-type
vector-tensor
massive gravity
other observationally constrained extensions
```

Any candidate must be filtered by:

- theoretical motivation;
- ghost/pathology absence;
- solar-system constraints;
- gravitational-wave constraints;
- cosmology;
- stability;
- whether the repulsive behavior is actually physical rather than inserted by assumption.

---

# 51. Exact recommended next-session sequence

To maximize information gain and avoid losing this session's work:

1. **Run `git status --short`.**
   Determine exactly which 006B–006D files/results are untracked or modified.
2. **Preserve the milestone before more research.**
   Update `NOTES.md`, `RESEARCH_BUILDPLAN.md`, `README.md`, and `CLAIMS.md` with the results above.
3. **Add focused regression protection for 006C/006D.**
   Preserve the central independent-verification and conservation results.
4. **Run the complete known-solutions suite.**
   Current minimum expected count before adding tests:
   ```text
   72 passed
   ```
5. **Checkpoint/commit the entire classical gate.**
6. **Begin Simulation 007A.**
   Complete Casimir apparatus, not vacuum region alone.
7. **Run 007B QEI immediately after 007A unless 007A already decisively eliminates the branch.**
8. **Use 007C only if dynamics retains meaningful expected information gain.**
9. **Only after the quantum gate should modified gravity become active.**

---

# 52. Things not to do next

To preserve momentum:

```text
DO_NOT:
spend another session shaving C=23.43 to C=22 or C=20 without a new physical mechanism.

DO_NOT:
call the full-rz extrapolated 22.55 lower endpoint a discovered coefficient.

DO_NOT:
claim C=23.4267 is a universal GR lower bound.

DO_NOT:
claim 006D is a known-material solution.

DO_NOT:
claim exact nonlinear GR conservation.

DO_NOT:
claim dynamical stability.

DO_NOT:
claim global positive-mass repulsion.

DO_NOT:
claim an experimental antigravity effect.

DO_NOT:
claim practical antigravity is solved.

DO_NOT:
count Casimir negative energy while omitting the apparatus.

DO_NOT:
jump to modified gravity before the established-QFT gate is quantitatively closed.
```

---

# 53. Workflow lessons from this session

Several implementation lessons should be retained.

### Raw Python must not be pasted directly into zsh

Two early attempts generated:

```text
zsh: parse error near `)'
```

because Python/patch text was interpreted as shell syntax.

For direct multi-file creation, use complete quoted heredocs.

### Pipeline return codes need `pipefail`

Without:

```bash
set -o pipefail
```

a command like:

```bash
python simulation.py | tee log
```

may report the successful return code from `tee` even if Python crashed.

This happened during the first 006C run.

Future scientific run harnesses should use `pipefail`.

### Numerical root/bracket tests must not evaluate unnecessarily singular limits

006C's original y=10−6y=10^{-6} direct radial quadrature was poorly conditioned.

The variable transformation fixed it without sacrificing implementation independence.

### Convergence must be separated by direction

The full $r$-$z$ work demonstrated why a single mesh-refinement sequence can mislead:

- radial refinement alone suggested $C\sim26$;
- vertical refinement produced a large additional decrease;
- combined extrapolation then bracketed the thin result.

Future PDE/optimizer work must treat radial, vertical, domain-size, and model-regularization convergence separately.

---

# 54. Current scientific frontier after this session

Before this session, the central question was:

> Can a finite conserved positive-energy GR source actually produce useful local repulsion, or were the previous results artifacts of idealized stresses?

That question has been substantially answered at the linearized-model level.

The new frontier is:

> **What physically realizable matter/field mechanism—if any—can generate the required relativistic stress pattern, remain stable, and avoid the catastrophic ah2/Gah^2/G energy scale?**

For the classical static branch, no such mechanism has yet been identified.

Therefore the highest-information escape route is now established quantum stress-energy.

---

# 55. Project-level result to carry forward verbatim

Recommended concise statement:

> **ANTIGRAVITY_RESEARCH has established a project-derived constructive result in static linearized general relativity: a finite-radius, finite-thickness, nonsingular, positive-energy, locally conserved stress-energy configuration satisfying NEC, WEC, and DEC can generate a locally outward gravitational field while retaining positive far-field mass. The best verified thin architecture has $C=23.426710175391$ in $M=C a h^2/G$, and a finite-thickness regularization reaches $C=23.591586299249$, within 0.704% of that limit. Independent Green-function integration verifies the earlier 005B finite-disk result. No known material realization, dynamical stability, exact nonlinear-GR realization, energetic plausibility, experimental accessibility, or practical antigravity device has been established. The classical static coefficient-optimization branch should now be deprioritized in favor of the buildplan's quantum stress-energy gate, beginning with a complete Casimir apparatus benchmark and then quantum-energy-inequality bounds.**

That is the strongest scientifically conservative summary of where the project stands after this session.

### END NOTE - AUGUST 27 2026 - 03:30 CST



### BEGIN NOTE - AUGUST 28 2026 - 00:35 CST


# ANTIGRAVITY_RESEARCH — Comprehensive Carry-Forward Notes Through 009N

These notes are the authoritative conversational handoff for the next research session.

They summarize:

* the current scientific state;
* established results;
* project-derived results;
* negative results and closed branches;
* the exact status of the repository;
* permanent versus disposable calculations;
* Simulations/Gates 001 through 009N;
* current practical-antigravity probability calibration;
* literature/context that must be retained;
* unresolved theoretical and experimental questions;
* branches that must **not** be restarted;
* the highest-value surviving research directions;
* the exact decision logic for the next research slice.

The next session should read these notes together with:

```text
ANTIGRAVITY_RESEARCH_CODEBUNDLE_20260827-034521.md
RESEARCH_BUILDPLAN.md
FORMATTING_AND_CODE_STANDARDS.md
NOTES.md
README.md
```

Important: the current `RESEARCH_BUILDPLAN.md`, `README.md`, and older `NOTES.md` snapshot are now **substantially behind the live scientific frontier**. They remain authoritative for methodology, standards, definitions, and earlier verified results, but their stated active frontier around 006D/007 no longer reflects the actual work completed through 009N.

The next session must therefore use this handoff to avoid restarting completed work.

---

# 1. Governing scientific discipline

The central project goal remains:

> Determine whether physically consistent stress-energy configurations, spacetime geometries, quantum effects, or well-motivated extensions of established gravitational physics can produce controllable and measurable gravitational repulsion, while narrowing the search space toward physically realizable and ultimately practical mechanisms.

The project must continue to distinguish all of the following:

1. mathematical sign reversal;
2. invariant or operational local repulsion;
3. consistency with the governing field equations;
4. acceptable stress-energy;
5. finite localization;
6. local conservation;
7. stability;
8. physical field/material realization;
9. energetic plausibility;
10. experimental accessibility;
11. a useful practical apparatus.

A mathematical solution is not a device.

A locally repulsive field is not automatically a globally repulsive field.

A fifth force is not ordinary general-relativistic antigravity.

A measurable short-range repulsive force is not reactionless propulsion.

No project-derived calculation should be called a discovery until independently verified and compared with the literature.

---

# 2. GitHub mathematical formatting standard

All new Markdown must use the repository formatting standard.

Inline mathematics:

```markdown
The force range is $\lambda$.
```

Standalone mathematics:

````markdown
```math
a(r)
=
-\frac{GM}{r^2}
+
\frac{\Lambda c^2r}{3}
```
````

Do not use:

```text
\(...)
```

or:

```text
\[...\]
```

Do not append grammatical periods or commas inside display-math blocks.

For example:

```math
M
=
C\frac{ah^2}{G}
```

rather than putting a final period inside the equation.

---

# 3. Source-code documentation standard

All nontrivial permanent source or simulation files must contain unusually comprehensive top-of-file documentation covering:

* purpose;
* scientific question;
* physical model;
* governing equations;
* inputs and outputs;
* units;
* sign conventions;
* approximation level;
* assumptions;
* energy conditions where relevant;
* numerical method;
* validation strategy;
* limitations;
* related project files;
* claim classification.

Important functions need meaningful docstrings.

Important equations should be documented near their implementation.

Comments should explain why a calculation exists rather than simply translating code into English.

Do not permanently land speculative simulation machinery before the physics survives its cheapest decisive gate.

---

# 4. Research stop rules remain binding

The buildplan explicitly says to pause or reject a branch when:

* a fundamental physical assumption fails;
* independent verification fails;
* conservation fails;
* stability fails;
* known bounds exceed the required parameter range without a credible escape;
* repeated optimizations only change small coefficients while the remaining feasibility gap spans orders of magnitude;
* another branch has higher expected information value.

Do not protect sunk effort.

The 009-series work has followed this philosophy aggressively.

---

# 5. Critical meaning of a GREEN gate

This is especially important for the next session.

A gate ending with:

```text
...=GREEN
```

does **not** necessarily mean the physical mechanism survived.

It means:

> the gate executed successfully and produced the intended scientifically interpretable decision.

Examples:

```text
009I_TERRESTRIAL_SCREENING_COMPATIBILITY_GATE=GREEN
```

actually means the **monolithic terrestrial chameleon-vector route was rejected**.

Likewise:

```text
009N_ELECTROWEAK_CONSERVATION_GATE=GREEN
```

means the electroweak consistency falsification worked and the simplest gold-null vector realization was rejected.

Never count the number of GREEN outputs as progress toward a device.

---

# 6. Current repository / code state

The attached codebundle was generated:

```text
2026-08-27 03:45:32 CDT
```

with:

```text
branch: main
HEAD: 45a3e2060016f718f2f50a508260071de06815e5
included files: 76
working tree: DIRTY_OR_UNTRACKED
```

At codebundle generation time it showed:

```text
M NOTES.MD
```

However, subsequent work created additional untracked/permanent files.

The last explicit working-tree snapshot shown during the later research slice included approximately:

```text
?? results/data/008a_wall_current_loop_gate.csv
?? results/data/008b_distributed_field_representability_gate.csv
?? results/logs/008a_wall_current_loop_gate.log
?? results/logs/008b_distributed_field_representability_gate.log
?? simulations/008a_wall_current_loop_gate.py
?? simulations/008b_distributed_field_representability_gate.py
?? src/antigravity_research/geometry/canonical_scalar_representability.py
?? src/antigravity_research/geometry/charged_scalar_stability.py
?? src/antigravity_research/geometry/wall_current_loop.py
?? tests/known_solutions/test_006c_006d_regressions.py
?? tests/known_solutions/test_canonical_scalar_representability.py
?? tests/known_solutions/test_wall_current_loop.py
```

This may no longer be exact.

Therefore the **first repository command next session** must be:

```bash
git status --short
```

Do not assume anything has been committed since the codebundle snapshot.

---

# 7. Permanent versus disposable work

This distinction is essential.

## Permanent work known to have landed

Permanent 008A:

```text
src/antigravity_research/geometry/wall_current_loop.py
tests/known_solutions/test_wall_current_loop.py
simulations/008a_wall_current_loop_gate.py
results/data/008a_wall_current_loop_gate.csv
results/logs/008a_wall_current_loop_gate.log
```

Permanent 008B:

```text
src/antigravity_research/geometry/canonical_scalar_representability.py
tests/known_solutions/test_canonical_scalar_representability.py
simulations/008b_distributed_field_representability_gate.py
results/data/008b_distributed_field_representability_gate.csv
results/logs/008b_distributed_field_representability_gate.log
```

Permanent regression preservation:

```text
tests/known_solutions/test_006c_006d_regressions.py
```

A partial 008C source module was created:

```text
src/antigravity_research/geometry/charged_scalar_stability.py
```

but the associated permanent test and simulation were **not shown as successfully landed**.

The earlier shell attempt that was supposed to create the complete 008C slice exited with code 127.

Do not assume 008C is complete.

## Disposable-only work

The calculations from approximately 008C direct-gate onward, especially:

```text
008C
008D
008E
008F
009A
009B
009C
009D
009E
009F
009G
009H
009I
009J
009K
009L
009M
009N
```

were executed primarily as self-contained Python heredocs or literature/analytical gates.

Based on everything shown, **009A–009N did not permanently modify the repository**.

Do not search for `009*.py` and assume something went missing. Those simulations were intentionally disposable because the project was optimizing information gain before committing code.

---

# 8. Test-suite checkpoint

Permanent regression progression was:

```text
72 passed
```

after 006D.

Then:

```text
78 passed
```

after the six 006C/006D preservation tests.

Then:

```text
86 passed
```

after permanent 008A.

Then:

```text
94 passed
```

after permanent 008B.

Therefore the last verified full permanent baseline is:

```text
94 passed
```

No subsequent 009-series calculation intentionally changed the permanent test suite.

The next session should verify with:

```bash
ROOT="$(pwd)"
PY="$ROOT/.venv/bin/python"

PYTHONPATH="$ROOT/src" \
"$PY" -m pytest -q tests/known_solutions
```

Expected, unless files have changed:

```text
94 passed
```

Do not claim this expected count as current until it is actually rerun.

---

# 9. Shell-workflow lesson

Do not use `set -u` in the interactive macOS/zsh workflow.

An earlier shell slice interacted badly with shell variables such as `RPROMPT`.

For disposable gates prefer:

```bash
ROOT="$(pwd)"
PY="$ROOT/.venv/bin/python"

PYTHONPATH="$ROOT/src" "$PY" - <<'PY'
...
PY
```

Exit code:

```text
127
```

means a command/path failure, not a physics result.

---

# 10. Current overall scientific conclusion

The project has established with high confidence that **local repulsive gravitational behavior is possible within established general relativity**.

The core classical lesson remains:

```math
\text{gravity responds to the full stress-energy tensor, not merely positive mass density}
```

Large relativistic stresses or tensions can make the local active gravitational source repulsive even when energy density and total mass remain positive.

However, the best established-GR constructions retain catastrophic energetic scaling of approximately:

```math
M
=
C\frac{ah^2}{G}
```

with $C$ of order tens for the best explicit finite locally conserved source.

That prevents ordinary classical GR from presently constituting a plausible practical route.

The project therefore investigated quantum negative energy and then short-range repulsive fifth-force physics.

The fifth-force branch produced experimentally interesting possibilities but has not yet produced a healthy, allowed, human-scale practical mechanism.

---

# 11. Simulation 001A — Kottler / Schwarzschild–de Sitter

Weak-field acceleration:

```math
a(r)
=
-\frac{GM}{r^2}
+
\frac{\Lambda c^2r}{3}
```

Static radius:

```math
r_s
=
\left(
\frac{3GM}{\Lambda c^2}
\right)^{1/3}
```

For approximately $10^{12}M_\odot$:

```text
static radius ≈ 1.1139 Mpc
```

Classification:

```text
KNOWN_RESULT
REPRODUCED
```

Conclusion:

A positive cosmological constant creates genuine gravitational defocusing/repulsion, but the observed value of $\Lambda$ is useless for laboratory antigravity.

---

# 12. Simulation 001B — invariant Kottler tidal effect

Tidal eigenvalues:

```math
\lambda_r
=
\frac{2GM}{r^3}
+
\frac{\Lambda c^2}{3}
```

```math
\lambda_t
=
-\frac{GM}{r^3}
+
\frac{\Lambda c^2}{3}
```

This established that the effect is not merely coordinate acceleration.

Classification:

```text
KNOWN_RESULT
REPRODUCED
```

---

# 13. Simulation 002 — perfect-fluid defocusing

For a perfect fluid:

```math
\frac{\ddot\xi}{\xi}
=
-\frac{4\pi G}{3c^2}
(\epsilon+3p)
+
\frac{\Lambda c^2}{3}
```

Positive-energy defocusing is possible for:

```math
w<-\frac{1}{3}
```

For $w=-1$:

* NEC satisfied at equality;
* WEC satisfied;
* DEC satisfied;
* SEC violated.

A $1g$ effect over approximately $1$ m requires an energy density around:

```text
1.5763e27 J/m^3
```

Conclusion:

The sign is easy.

The energy scale is catastrophic.

---

# 14. Simulation 003A — finite vacuum-energy core

A $p=-\epsilon$ vacuum-energy region cannot simply taper smoothly to vacuum while maintaining the same equation of state and conservation.

A boundary layer or supporting stress is required.

A positive-energy core also produces positive exterior mass.

Conclusion:

Interior defocusing does not automatically generate an externally useful repulsive source.

---

# 15. Simulation 003B — Israel shell

The tested thin-shell construction required an unfavorable negative-ADM/exotic branch for outward Schwarzschild behavior.

This path was deprioritized.

Do not restart without a genuinely new analytical reason.

---

# 16. Simulation 004A — Reissner–Nordström / Einstein–Maxwell

Einstein–Maxwell provides a known example where:

* ADM mass is positive;
* Maxwell energy is positive;
* local neutral-particle gravitational repulsion can occur;
* the shell can satisfy WEC/DEC in the tested construction.

Repulsive radius:

```math
r_{\mathrm{rep}}
=
\frac{Q^2}
{4\pi\epsilon_0Mc^2}
```

For approximately $1g$ across $1$ m:

```text
electric field ≈ 2.67e19 V/m
```

which is roughly twenty times the Schwinger field.

A sub-Schwinger benchmark moved the scale to roughly:

```text
radius ≈ 407 m
mass ≈ 1.22e17 kg
charge ≈ 2.44e13 C
```

Classification:

```text
KNOWN_RESULT
REPRODUCED_REFERENCE_MECHANISM
```

Not an engineering route.

---

# 17. Simulation 005A — relativistic tension wall

Surface energy $U$ and tension:

```math
\tau=qU
```

Repulsion occurs for:

```math
q>\frac{1}{2}
```

DEC permits:

```math
q\le1
```

Therefore there is a positive-energy NEC/WEC/DEC-compatible repulsive region:

```math
\frac{1}{2}<q\le1
```

The optimal ideal domain-wall point is:

```math
q=1
```

For $1g$ planar acceleration:

```text
minimum U ≈ 2.1017e27 J/m^2
mass equivalent/area ≈ 2.3385e10 kg/m^2
```

Known domain-wall physics confirms the qualitative mechanism.

---

# 18. Simulation 005B — finite supported tension disk

The finite membrane needs compressive support.

For the optimized $q=1$ membrane plus minimum-DEC rim:

```text
R/h ≈ 4.00614967
zero crossing z/R ≈ 0.393319893
C ≈ 79.753148116
```

with:

```math
M
=
C\frac{ah^2}{G}
```

At $1g$, $h=1$ m:

```text
M ≈ 1.172e13 kg
```

Properties:

* positive energy;
* finite source;
* local repulsive near field;
* positive total mass;
* attractive far field;
* global mechanical balance.

This result was later independently verified.

---

# 19. Simulation 006A — abstract static DEC optimization

Within the stated abstract assumptions:

```text
optimistic coefficient C = 1
domain wall C = 2
finite supported disk C ≈ 79.753
```

Important:

```math
C=1
```

is **not** a universal theorem of GR.

It is an optimistic lower result inside the simplified optimization model.

At $1g$ and $1$ m:

```text
C = 1 mass scale ≈ 1.47e11 kg
```

Still catastrophic.

---

# 20. Simulation 006B — geometry-aware locally conserved thin source

This was the major classical optimization improvement.

Best verified thin architecture:

```text
C_thin = 23.426710175391
alpha = a/h = 1.437500564637
beta = R/h = 4.701437405300
```

The full finite-volume optimization did not verify a better coefficient.

Classification:

```text
PROJECT_DERIVED_NUMERICAL_OPTIMIZATION_RESULT
```

Not a universal GR lower bound.

---

# 21. Simulation 006C — independent Green-function verification

005B was independently reconstructed through a separate Green-function calculation.

Maximum absolute error:

```text
2.22e-16
```

relative error:

```text
1.419e-15
```

The independent calculation reproduced:

* zero location;
* $R/h$;
* mass coefficient.

Classification:

```text
INDEPENDENT_NUMERICAL_VERIFICATION
```

This considerably strengthened confidence in 005B.

---

# 22. Simulation 006D — finite-thickness locally conserved positive-energy source

This remains the strongest project-derived classical-GR source result.

The construction used an axisymmetric anisotropic stress architecture with:

```math
q(r)=rp_r
```

```math
p_\phi
=
\frac{dq}{dr}
```

```math
p_z=0
```

```math
T_{rz}=0
```

and:

```math
\epsilon
=
\max(
|p_r|,
|p_\phi|
)
```

Properties verified numerically:

* finite radius;
* finite thickness;
* nonsingular;
* positive energy density;
* local static conservation;
* NEC satisfied;
* WEC satisfied;
* DEC satisfied;
* locally outward gravitational field;
* positive far-field mass.

Best tested finite-thickness coefficient:

```text
C_finite = 23.591586299249
```

which is within approximately:

```text
0.704%
```

of the thin result.

Representative diagnostics:

```text
max conservation residual ≈ 3.103e-14
DEC violation = 0
minimum NEC margin = 0
integrated stress trace ≈ 2.922e-13
```

Classification:

```text
CONSTRUCTIVE_LINEARIZED_GR_STRESS_ENERGY_RESULT
```

Not established:

* exact nonlinear Einstein solution;
* complete dynamical stability;
* real material realization;
* experimentally accessible source;
* practical energy budget.

---

# 23. Classical-GR practicality conclusion

The strongest classical result still obeys:

```math
M
\sim
23.5\frac{ah^2}{G}
```

At approximately $1g$ and $1$ m this is on the order of:

```text
3.5e12 kg
```

The project therefore correctly stopped coefficient optimization.

Improving $C=23$ to $C=10$, $5$, or even $1$ does not solve the fundamental engineering problem.

Do not restart classical coefficient optimization unless a new mechanism changes the **parametric scaling** rather than merely the coefficient.

---

# 24. Quantum Simulation 007A — Casimir branch

Brown–Maclay ideal electromagnetic Casimir stress between perfect plates:

```math
K
=
\frac{\pi^2\hbar c}{720d^4}
```

with:

```math
\epsilon=-K
```

```math
p_x=p_y=+K
```

```math
p_z=-3K
```

Active gravitational combination:

```math
S
=
\epsilon+p_x+p_y+p_z
=
-2K
```

Thus the ideal vacuum region is locally repulsive in the relevant weak-field sense.

However the complete apparatus must include:

* plates;
* mechanical support;
* stabilizing stresses.

Published work such as Fulling et al. establishes that Casimir energy gravitates normally.

Costa and Matsas show that a mechanically complete DEC-supported Casimir apparatus has nonnegative total mass.

Vacuum-only planar acceleration:

```math
a_C
=
\frac{\pi^3G\hbar}
{180cd^3}
```

A $1g$ vacuum-only benchmark requires approximately:

```text
d ≈ 7.44e-19 m
```

This is physically useless.

Static Casimir antigravity is therefore strongly deprioritized.

---

# 25. Quantum Simulation 007B — quantum inequality gate

For the electromagnetic Lorentzian quantum inequality, the coefficient used was approximately:

```text
alpha_QI = 27/(1024 pi^2)
         ≈ 0.00267155
```

An optimistic acceleration scale:

```math
a_{\max}
=
\frac{4\pi\alpha_{\mathrm{QI}}G\hbar}
{c^4\tau^3}
```

Ignoring causality, $1g$ would require:

```text
tau ≈ 1.44e-27 s
c tau ≈ 4.32e-19 m
```

Imposing the causal near-zone requirement:

```math
\tau
\ge
\frac{h}{c}
```

gives:

```math
a_{\max}(h)
=
\frac{4\pi\alpha_{\mathrm{QI}}G\hbar}
{ch^3}
```

At:

```text
h = 1 m
```

the result is approximately:

```text
7.88e-55 m/s^2
```

A $1g$ effect again requires:

```text
h ≈ 4.32e-19 m
```

Conclusion:

The specific free-electromagnetic-field QEI route is catastrophically far from macroscopic usefulness.

This is not a universal no-go theorem for every quantum field theory.

But the established free-EM negative-energy loophole is closed for practical purposes.

---

# 26. 008A — finite wall plus current-loop support

A physically motivated alternative to the abstract collar was tested.

Effective energy:

```math
E(R)
=
\pi\sigma R^2
+
2\pi\mu R
+
\frac{J}{R}
```

Equilibrium:

```math
J
=
2\pi R^2(\sigma R+\mu)
```

The radial second derivative at equilibrium is positive.

Boundary energy/tension:

```math
U_b
=
\sigma R+2\mu
```

```math
T_b
=
-\sigma R
```

DEC requires:

```math
\mu\ge0
```

Results:

```text
m = 0 exactly reproduces the 005B q=1 limit
positive bare string energy worsens the coefficient
```

Decision:

```text
WALL_PLUS_CURRENT_LOOP_IMPROVES_006D=NO
```

The distributed collar remained more efficient.

Permanent source/tests/simulation were created.

---

# 27. 008B — canonical scalar representability

For static canonical real scalar fields:

```math
T_{ij}
=
M_{ij}
-
\rho\delta_{ij}
```

with local Gram components:

```math
M_{ii}
=
\rho+p_i
```

and potential:

```math
V
=
-\frac{1}{2}
\left(
\rho+\sum_i p_i
\right)
```

The 006D DEC structure makes the local Gram matrix positive semidefinite.

Therefore the stress tensor is **locally algebraically representable** by canonical scalar gradients.

However:

* a strictly axisymmetric real scalar has no $\phi$ gradient;
* 006D requires a nonzero azimuthal Gram sector;
* parts of the outer collar can require local rank 3.

Minimum local real-scalar component count:

```text
3
```

A Derrick scaling argument for a purely static canonical scalar gives:

```math
E(\lambda)
=
\frac{K}{\lambda}
+
\frac{U}{\lambda^3}
```

At stationary pressure:

```math
E''(1)
=
-3E
```

so the purely static canonical-scalar realization is dilation unstable.

Decisions:

```text
LOCAL_ALGEBRAIC_REPRESENTABILITY=YES
STRICT_AXISYMMETRIC_REAL_SCALAR=INSUFFICIENT
PURE_STATIC_CANONICAL_SCALAR_DERRICK_STABLE=NO
```

Therefore stabilization requires something like:

* time-dependent charge;
* current;
* gauge sector;
* higher derivatives;
* other additional physics.

Permanent source/tests/simulation were created.

---

# 28. 008C — fixed-charge dilation stability capacity

A stationary charged canonical scalar supplies a temporal kinetic component.

Define:

```math
D
=
\sum_a \dot\phi_a^2
```

with local capacity:

```math
D_{\max}
=
\min_i(\rho+p_i)
```

and:

```math
T
=
\frac{D}{2}
```

At fixed charge under dilation:

```math
E_Q(\lambda)
=
\lambda^3T
+
\frac{K}{\lambda}
+
\frac{U}{\lambda^3}
```

The second derivative satisfies:

```math
E_Q''(1)
=
24T
-
3E
-
5P
```

For approximately zero pressure:

```math
P\approx0
```

positive dilation curvature requires:

```math
\frac{T}{E}
>
\frac{1}{8}
```

At the finest tested 006D scale:

```text
Tmax/E = 0.186185265139
critical = 0.125
available/required = 1.489482121109
required fraction of capacity = 0.671374288975
maximum curvature/E = 1.468446363326
P/E ≈ 2.63e-14
```

Capacity localization was overwhelmingly in the outer collar:

```text
core ≈ 0
inner transition ≈ 0.0189%
transfer ≈ 0
outer collar ≈ 99.9811%
```

Decision:

```text
FIXED_CHARGE_DILATION_WINDOW=SURVIVES
EXACT_006D_STRESS_HAS_SUFFICIENT_TEMPORAL_KINETIC_CAPACITY=YES
GLOBAL_COMPLEX_SCALAR_SOLUTION=NOT_ESTABLISHED
FULL_DYNAMIC_STABILITY=NOT_ESTABLISHED
008C_DIRECT_GATE=GREEN
```

Important:

This only proves enough local temporal kinetic *capacity* exists to cure one Derrick dilation mode.

It does not construct a global field solution.

Permanent implementation is incomplete.

---

# 29. 008D — charged/winding sector separation

For one stationary complex scalar:

```math
\Phi
=
f e^{i(n\phi-\omega t)}
```

simultaneous temporal and angular gradient sectors imply:

```math
|T_{t\phi}|
=
\sqrt{DA}
```

The 006D target is static and diagonal:

```math
T_{t\phi}=0
```

The transfer annulus can require azimuthal stress while allowing:

```math
D_{\max}=0
```

Therefore a single charged winding scalar cannot realize the exact stress tensor.

Representative transfer point:

```text
r ≈ 3.06947
epsilon ≈ 0.2193257
p_r = -epsilon
p_phi = +epsilon
Dmax = 0
angular Gram ≈ 0.4386514
```

Representative outer-collar point:

```text
r ≈ 4.70456
epsilon ≈ 105.463
Dmax ≈ 105.416
D allocation ≈ 70.7738
angular remaining ≈ 140.152
T_tphi ≈ 99.5947
T_tphi/epsilon ≈ 0.94436
```

Dense audit:

```text
6932 / 10001 points
```

required angular stress but forbade nonzero charge capacity.

Only:

```text
15 points
```

simultaneously permitted nonzero charge capacity in that audit.

Decisions:

```text
ONE_COMPLEX_SCALAR_EXACT_006D_REALIZATION=REJECTED
STATIC_ANGULAR_SECTOR_AND_CHARGED_STABILIZER_MUST_BE_SEPARATED=YES
COUNTER_WINDING_PAIR_ALGEBRAIC_CANCELLATION=YES
008D_SECTOR_SEPARATION_GATE=GREEN
```

---

# 30. 008E — ungauged winding global-integrability gate

For a finite collection of ungauged canonical winding scalars, a necessary inequality was derived:

```math
N
\ge
\frac{
\left|
\frac{d}{dr}
\left(
r\sqrt{A}
\right)
\right|
}{
\sqrt{G_r}
}
```

where $N$ is maximum winding.

Near the outer boundary:

```text
delta/w = 0.1     N ≈ 6.73e3
delta/w = 0.03    N ≈ 2.45e4
delta/w = 0.01    N ≈ 7.50e4
delta/w = 0.003   N ≈ 2.52e5
delta/w = 0.001   N ≈ 7.57e5
delta/w = 0.0003  N ≈ 2.52e6
delta/w = 0.0001  N ≈ 7.57e6
```

The asymptotic behavior is:

```math
N
\sim
\frac{757}
{\delta/w}
```

so:

```math
N\to\infty
```

at the outer termination.

The disposable script initially printed the wrong asymptotic decision because a ratio was computed backwards.

That was a **test-logic bug, not a physics failure**.

Correct classification:

```text
FINITE_UNGAUGED_WINDING_SET_CAN_EXACTLY_REALIZE_006D_OUTER_TERMINATION=NO
UNGAUGED_CANONICAL_WINDING_GLOBAL_INTEGRABILITY=REJECTED
008C_FIXED_CHARGE_STABILITY_WINDOW=STILL_SURVIVES
006D_STRESS_TENSOR_ITSELF_INVALIDATED=NO
GAUGE_OR_OTHER_COMPENSATING_SECTOR_NOW_REQUIRED=YES
008E_GLOBAL_INTEGRABILITY_GATE=GREEN
```

---

# 31. 008F — local gauge boundary takeover

For the outer 006D collar:

```math
p_\phi=\epsilon
```

with:

```math
p_r\le0
```

```math
p_z=0
```

Define:

```math
g
=
\epsilon+p_r
```

An exact local decomposition exists:

Gauge sector:

```math
T_g
=
(g,0,g,0)
```

Residual scalar sector:

```math
T_s
=
(-p_r,p_r,-p_r,0)
```

The residual scalar Gram matrix is positive semidefinite.

The gate conservatively removed charged-scalar temporal capacity from an outer gauge layer and found how much layer could be replaced before fixed-charge Derrick stability failed.

Results:

```text
5% takeover:
T/E ≈ 0.18484

10%:
T/E ≈ 0.18097

20%:
T/E ≈ 0.16683

25%:
T/E ≈ 0.15710

30%:
T/E ≈ 0.14598
curvature/E ≈ 0.50344
gauge energy/E ≈ 0.08042

35%:
T/E ≈ 0.13374

38%:
T/E ≈ 0.12597
curvature/E ≈ 0.02337
```

Critical takeover width:

```text
≈ 38.3694%
```

Decisions:

```text
OUTER_COLLAR_HAS_EXACT_LOCAL_MAXWELL_PAIR_DECOMPOSITION=YES
FINITE_GAUGE_BOUNDARY_LAYER_COMPATIBLE_WITH_DERRICK_STABILITY=YES
THIRTY_PERCENT_GAUGE_TAKEOVER=YES
CHARGED_STABILIZER_AND_GAUGE_HAVE_NONZERO_BUDGET_WINDOW=YES
GLOBAL_SMOOTH_GAUGE_POTENTIALS=NOT_ESTABLISHED
008F_GAUGE_TAKEOVER_GATE=GREEN
```

Meaning:

There is a mathematically nonempty local field-theory realization window.

But none of this changes the catastrophic GR scaling.

Therefore the branch was correctly deprioritized before building a complicated global field solution.

---

# 32. Strategic pivot after 008F

The most important realization after 008F was:

> Even increasingly realistic field-theory realizations of 006D still inherit the same catastrophic $a h^2/G$ scaling.

Therefore a practical route requires **changing the interaction scale or effective coupling**, not merely reducing coefficient $C$.

Only after the established GR and quantum branches had been quantitatively squeezed did the project move into modified/fifth-force physics.

This was consistent with the original anti-drift rule.

---

# 33. 009A — generic repulsive Yukawa scaling escape

Potential convention:

```math
V(r)
=
-\frac{Gm_1m_2}{r}
\left[
1+\alpha e^{-r/\lambda}
\right]
```

Repulsion requires:

```math
\alpha<0
```

For a thick planar source:

```math
a_N
=
2\pi G\rho T
```

and the repulsive Yukawa magnitude is:

```math
a_Y
=
2\pi G\rho|\alpha|
\lambda
e^{-z/\lambda}
\left(
1-e^{-T/\lambda}
\right)
```

Benchmark:

```text
rho = 19300 kg/m^3
lambda = 10 um
T = 100 um
z = 10 um
```

Results:

```text
Newtonian acceleration ≈ 8.09e-10 m/s^2
Yukawa acceleration per |alpha| ≈ 2.98e-11 m/s^2
sign reversal |alpha| ≈ 27.18
net 1e-9 m/s^2 |alpha| ≈ 60.77
1g |alpha| ≈ 3.29e11
```

Decision:

```text
GENERIC_REPULSIVE_YUKAWA_CAN_REVERSE_FORCE=YES
LAB_MICROSCALE_REPULSION_POSSIBLE_IF_FORCE_EXISTS=YES
ONE_G_AT_10UM=NO
NEW_PHYSICS_REQUIRED=YES
009A_SCALING_ESCAPE_GATE=GREEN
```

This is a fifth force, not GR antigravity.

---

# 34. 009B — concrete $U(1)_{B-L}$ vector branch

A healthy concrete vector model was chosen.

For neutral atoms:

```math
B-L
\approx
N
```

because proton baryon charge and electron lepton charge cancel, leaving neutron number.

A massive vector exchanged between like $B-L$ charges is repulsive.

Standard anomaly cancellation can be achieved with three right-handed neutrinos.

Approximate material-dependent Yukawa strength:

```math
\alpha
=
\frac{\hbar c}{G}
\frac{g_{B-L}^2}
{4\pi m_p^2}
F_1F_2
```

For tungsten/gold:

```text
F_W ≈ 0.597826
F_Au ≈ 0.598985
```

At:

```text
g_BL = 1e-16
```

the effective strength was:

```text
alpha_eff ≈ 4.82477e4
```

The historical Stanford inverse-square-law points suggested potentially measurable micron-scale repulsion.

However those historical limits were not the strongest modern constraint everywhere.

The 2016 Casimir-less experiment later became the more important comparison.

---

# 35. 009C — modernized $B-L$ experimental synthesis

Primary experimental reference:

Chen et al., 2016:

```text
Phys. Rev. Lett. 116, 221102
arXiv:1410.7267
```

Important experiment features:

* approximately $149.3,\mu$m sphere radius;
* sapphire sphere;
* 10 nm Cr + 250 nm Au coating;
* rotating source;
* common 150 nm Au + 10 nm Cr coating;
* structured Au/Si source below coating;
* structured depth approximately 2.10 µm;
* gaps approximately 200–1000 nm;
* common Au layer suppresses differential Casimir background by more than roughly $10^6$;
* thermal force noise near 6 fN/$\sqrt{\mathrm{Hz}}$;
* measured short-gap random noise could be closer to 12 fN/$\sqrt{\mathrm{Hz}}$ due to wobble;
* long-integration differential force sensitivity approximately 0.1–0.2 fN.

For:

```text
g_BL = 1e-16
```

project recast differential forces were approximately:

```text
4 um:  0.0344 fN
5 um:  0.0549 fN
6 um:  0.0801 fN
7 um:  0.1101 fN
8 um:  0.1447 fN
```

A hypothetical hybrid combining the 2016 Casimir-less geometry with a 2008-style cryogenic 0.2 fN/$\sqrt{\mathrm{Hz}}$ force sensor yielded, for a 50% signal-transfer assumption at 6 µm:

```text
signal ≈ 0.0401 fN
1 h noise ≈ 0.00333 fN
SNR 1 h ≈ 12.0
SNR 24 h ≈ 58.9
5-sigma time ≈ 623 s
g reach 1 h ≈ 6.45e-17
g reach 24 h ≈ 2.91e-17
```

This was only a synthesis of separately demonstrated technologies.

It was not claimed as an existing apparatus.

---

# 36. CANNEX strategic improvement

CANNEX emerged as a better direct plane-parallel platform.

Important paper:

```text
arXiv:2403.10998
```

Key properties:

* plane-parallel force geometry;
* approximately 3–30 µm operating region;
* optimized for gravity-like/interfacial forces;
* Cavendish configuration uses a thin conducting shield to suppress electromagnetic/Casimir interactions;
* approximately 30 mg active masses;
* designed to measure gravity at very short range;
* reported representative pressure errors significantly below the earlier conservative 1 nN/m² project benchmark.

Representative published 1000-second errors used:

```text
statistical ≈ 0.324 nN/m^2
systematic ≈ 0.167 nN/m^2
combined ≈ 0.3645 nN/m^2
```

---

# 37. 009D — plane-parallel $B-L$ pressure gate

Benchmark:

```text
g_BL = 1e-16
lambda = 6 um
effective alpha = 4.824767e4
```

Dense active layer scan.

Central 10 µm gap result with 5 µm active layer:

```text
pressure ≈ 16.3821 nN/m^2
signal / 1 nN/m^2 ≈ 16.38
5-sigma g reach ≈ 5.52e-17
```

At 6 µm gap and 5 µm layer:

```text
pressure ≈ 31.9080 nN/m^2
5-sigma g reach ≈ 3.96e-17
```

Minimum active-layer thickness for 5 sigma at 10 µm under 1 nN/m² noise:

```text
≈ 2.247 um
```

Decisions:

```text
REPULSIVE_B_L_PRESSURE_EXCEEDS_CONSERVATIVE_PLANE_PLATE_SENSITIVITY=YES
REFERENCE_G_BL_1E_MINUS_16_IS_DECISIVE_AT_10UM_GAP=YES
FEW_MICRON_DENSE_ACTIVE_LAYER_SUFFICIENT=YES
PLANE_PARALLEL_GEOMETRY_BEATS_CURVED_GEOMETRY_FOR_THIS_FORCE=YES
CANNEX_CLASS_CAVENDISH_CONFIGURATION_DIRECTLY_MATCHES_VOLUME_FORCE_SEARCH=YES
EXISTENCE_OF_B_L_FORCE=NOT_ESTABLISHED
HUMAN_SCALE_ANTIGRAVITY=NO
LABORATORY_REPULSIVE_FORCE_DEMONSTRATOR_PATH=HIGH_PRIORITY
009D_CANNEX_VECTOR_GATE=GREEN
```

This remains a potentially excellent Level-9 experiment if the force exists.

---

# 38. 009E — CANNEX shield transparency and realistic error budget

The conducting shield was stress-tested.

Electromagnetic Thomas–Fermi screening was rescaled by roughly:

```math
\frac{g_{B-L}}{e}
```

At:

```text
g_BL = 1e-16
```

the inferred $B-L$ screening length was on the order of:

```text
6e4–6e5 m
```

depending on assumed electromagnetic Thomas–Fermi length.

Therefore matter polarization was negligible compared with a 6 µm mediator range in this simple preflight.

For a full 1 µm shield:

```text
Yukawa transmission ≈ 0.84648
```

Remaining signals:

```text
6 um gap:
27.0095 nN/m^2

10 um gap:
13.8671 nN/m^2
```

Against combined CANNEX error:

```text
6 um SNR ≈ 74.10
10 um SNR ≈ 38.04
```

Representative 5-sigma coupling reaches:

```text
6 um ≈ 2.60e-17
10 um ≈ 3.63e-17
```

Decisions:

```text
B_L_THOMAS_FERMI_SCREENING_NEGLIGIBLE=YES
SUB_MICRON_CONDUCTING_SHIELD_IS_EFFECTIVELY_TRANSPARENT_TO_B_L=YES
ONE_MICRON_SHIELD_RETAINS_MORE_THAN_80_PERCENT_SIGNAL=YES
B_L_SIGNAL_REMAINS_DECISIVE_VS_PUBLISHED_CANNEX_ERROR=YES
B_L_SIGNAL_REMAINS_DECISIVE_VS_1NN_M2_CONSERVATIVE_ERROR=YES
009E_SHIELD_AND_ERROR_GATE=GREEN
```

Caveat:

This is a project-derived screening estimate, not a full condensed-matter calculation of a $B-L$ plasma response.

The static $B-L$ charge of the shield still needs differential cancellation in a real experiment.

---

# 39. 009F — isotope null-source design

The source used alternating enriched:

```text
92Mo
100Mo
```

For neutral molybdenum:

```text
92Mo: Z = 42, N = 50
100Mo: Z = 42, N = 58
```

The layers were thickness-matched so that the universal mass-Yukawa finite-depth source response was equal:

```math
\rho_{92}
\left(
1-e^{-t_{92}/\lambda}
\right)
=
\rho_{100}
\left(
1-e^{-t_{100}/\lambda}
\right)
```

while $B-L$ charge remained different.

For:

```text
t_92 = 20 um
lambda = 6 um
```

the matching thickness was:

```text
t_100 ≈ 13.0876269 um
```

The exact script supplied in the session was independently evaluated by the assistant because the attached paste contained the **script rather than a user terminal printout**.

Result under its stated assumptions:

```text
B-L isotope differential pressure ≈ 2.05505 nN/m^2
combined CANNEX sigma ≈ 0.36451 nN/m^2
SNR ≈ 5.6379
universal mass-Yukawa differential ≈ 0
Newtonian differential ≈ -0.0046 nN/m^2
```

Thickness error giving a 10% false universal-Yukawa signal:

```text
≈ 294.46 nm
```

Classification:

```text
009F_ISOTOPE_NULL_GATE=GREEN
```

but note the evidence level:

```text
ASSISTANT_INDEPENDENT_EXECUTION_OF_USER_SUPPLIED_SCRIPT
```

rather than a user-pasted terminal verification.

Scientific value:

The isotope-null design is a potentially excellent **signal discrimination architecture**.

It is not itself a route to macroscopic lift.

---

# 40. 009G — constraint-limited unscreened vector practicality frontier

This was one of the most important gates in the entire project.

Current compiled limits were downloaded from AxionLimits for:

```text
InverseSquareLaw
Sun
HorizontalBranch
RedGiant
Casimir
EotwashEP
MICROSCOPE
```

Data hashes were printed in the terminal and therefore provenance was preserved for that run.

At the 6 µm reference:

```text
mediator mass ≈ 0.0328878 eV
current compiled g limit ≈ 2.63372e-16
dominant constraint = ISL
g = 1e-16 remains below compiled limit
```

The crucial geometry-independent source bound was then derived.

For an unscreened linear repulsive Yukawa force, filling the entire half-space below the target with maximum charge-density matter maximizes the upward field.

Therefore no ring, disk, multilayer, metamaterial, perforation, or finite geometry can beat the half-space result at fixed:

* coupling;
* interaction range;
* maximum ordinary-matter charge density.

Optimistic benchmark:

```text
rho = 23000 kg/m^3
source neutron fraction = 0.62
test neutron fraction = 0.62
```

The current compiled constraint envelope produced the maximum contact result:

```text
best mediator mass ≈ 1.75861 eV
best range ≈ 112.206 nm
g limit ≈ 1.96598e-13
dominant = ISL
maximum contact acceleration ≈ 0.216650 m/s^2
≈ 0.0220921 g
```

Coupling enhancement required for 1 g:

```text
≈ 6.72793
```

Force enhancement:

```text
≈ 45.265
```

Maximum stand-off retaining at least 1% of $g$:

```text
≈ 88.94 nm
```

Other stand-off results:

```text
50 nm  ≈ 0.01415 g
100 nm ≈ 0.00906 g
200 nm ≈ 0.00372 g
500 nm ≈ 2.62e-4 g
1 um   ≈ 1.49e-5 g
2 um   ≈ 3.32e-6 g
5 um   ≈ 9.72e-7 g
10 um  ≈ 4.36e-7 g
```

Decisions:

```text
HALFSPACE_IS_OPTIMISTIC_ORDINARY_MATTER_SOURCE_BOUND=YES
CLEVER_UNSCREENED_SOURCE_GEOMETRY_CAN_BEAT_HALFSPACE_BOUND=NO
UNSCREENED_B_L_CAN_REACH_1G_WITH_CURRENT_COMPILED_LIMITS=NO
UNSCREENED_B_L_CAN_REACH_10_PERCENT_G=NO
UNSCREENED_B_L_CAN_REACH_1_PERCENT_G_AT_CONTACT=YES
GEOMETRY_OPTIMIZATION_REMAINS_A_PRACTICAL_ESCAPE=NO
009G_CONSTRAINT_LIMITED_PRACTICALITY_GATE=GREEN
```

This formally ended ordinary unscreened-source geometry optimization as a practical route.

---

# 41. 009H — Nelson–Walsh chameleon-vector hierarchy preflight

Published model:

Nelson and Walsh:

```text
"Chameleon Vector Bosons"
Phys. Rev. D 77, 095006
arXiv:0802.0762
```

The idea:

A scalar charged under the new vector can condense inside sufficiently large matter distributions and screen the vector force.

The published order-of-magnitude self-energy criterion was used.

For the candidate device:

```text
tungsten source radius = 0.10 m
source mass ≈ 80.8437 kg
gap = 0.01 m
effective source/receiver scale = 1.20 m
scalar mass = 1e-9 eV
scalar Compton wavelength ≈ 197.327 m
```

At 1 g:

```text
required g_BL ≈ 2.13702e-15
effective W-W alpha ≈ 2.19915e7
q_max 10-cm source unscreened ≈ 5.29778e-4
q_max 1.2-m pair unscreened ≈ 3.67901e-6
q_min Earth screened ≈ 5.46228e-19
```

A tenfold device-unscreening margin used:

```text
q_design ≈ 3.67901e-7
```

giving a huge apparent Earth/device screening hierarchy:

```text
~6.74e12
```

Similar windows existed mathematically for 10 g and 100 g.

Decision at that stage:

```text
SMALL_SCALAR_CHARGE_OPENS_EARTH_SCREENED_DEVICE_UNSCREENED_WINDOW=YES
ONE_G_PARAMETER_WINDOW_EXISTS_AT_ORDER_OF_MAGNITUDE_LEVEL=YES
HUNDRED_G_LOCAL_RECEIVER_WINDOW_EXISTS_AT_ORDER_OF_MAGNITUDE_LEVEL=YES
009H_CHAMELEON_HIERARCHY_PREFLIGHT=GREEN
```

However this was later substantially downgraded by 009I.

Do not revive the naive 009H conclusion without incorporating 009I.

---

# 42. 009I — terrestrial chameleon compatibility no-go

This was the critical correction to 009H.

The same Nelson–Walsh relations imply a vector screening length in matter:

```math
\ell_V^2
\sim
\frac{m_s}
{qg^2\rho}
```

and the unscreened spherical self-energy condition.

For the actual 009H design:

```text
Earth vector screening length ≈ 42.8067 m
```

Thus at tabletop distances, the force would be almost completely unscreened.

Transmission:

```text
52 um ≈ 0.999998785
1 mm  ≈ 0.999976639
3 mm  ≈ 0.999929920
1 cm  ≈ 0.999766419
```

Maximum scalar charges preserving unscreened behavior:

```text
10-cm source q_max ≈ 5.10045e-4
1.2-m pair q_max ≈ 3.54198e-6
```

Shortest Earth vector range compatible with those objects remaining unscreened:

```text
10-cm source ≈ 1.14967 m
1.2-m pair ≈ 13.7960 m
```

Most importantly, combining Earth hiding and device unscreening eliminated $m_s$ and $g$.

For a 10-cm source:

```text
q-window conflict at 52 um ≈ 4.88808e8
q-window conflict at 0.1 um ≈ 1.32174e14
```

Maximum full-density source radius if Earth force range is below 52 µm:

```text
≈ 4.523 um
```

If Earth range is below 0.1 µm:

```text
≈ 8.698 nm
```

Decisions:

```text
009H_GLOBAL_EARTH_VS_DEVICE_SCREENING_HIERARCHY=MATHEMATICALLY_SURVIVES
009H_EARTH_SCREENING_SHORT_ENOUGH_TO_HIDE_TABLETOP_FORCE=NO
TEN_CM_SOURCE_CAN_REMAIN_UNSCREENED_WHILE_EARTH_RANGE_BELOW_52UM=NO
TEN_CM_SOURCE_CAN_REMAIN_UNSCREENED_WHILE_EARTH_RANGE_BELOW_0P1UM=NO
M_SCALAR_OR_G_TUNING_CAN_REPAIR_THIS_MONOLITHIC_CONFLICT=NO
MONOLITHIC_TERRESTRIAL_1G_CHAMELEON_VECTOR_PATH=REJECTED_AT_PREFLIGHT_LEVEL
009I_TERRESTRIAL_SCREENING_COMPATIBILITY_GATE=GREEN
```

This is a strong negative result.

Do not retune $m_s$ or $g$ to try to repair it.

They cancel from the crucial compatibility relation.

---

# 43. 009J — microstructured subcritical source / neutral matrix

The next loophole was to break the active source into tiny unscreened pieces embedded in a nearly $B-L$-neutral matrix.

Protium is conceptually interesting because neutral ordinary hydrogen has:

```math
B-L=0
```

but this does not automatically solve collective screening.

Nelson–Walsh screening depends on:

* source size;
* density;
* proximity to other sources.

Therefore neighboring grains contribute cross-energy and behave as a coarse-grained charged medium.

The active filling-fraction constraint was derived.

A Borexino light-$B-L$ particle-level coupling benchmark of:

```text
g_BL <= 6.3e-7
```

was used as an optimistic ceiling.

For only a generous 52 µm hiding requirement:

```text
critical full-density radius ≈ 4.523 um
10-cm active filling fraction ≈ 2.046e-9
active source mass ≈ 1.654e-7 kg
source field at particle bound ≈ 1.778e8 g
optimistic 1-kg payload acceleration ≈ 29.41 g
```

So 52 µm hiding alone did **not** kill microstructure.

But using the much more stringent 0.1 µm terrestrial/Casimir hiding scale:

```text
critical full-density radius ≈ 8.698 nm
10-cm active filling fraction ≈ 7.5658e-15
active source mass ≈ 6.1165e-13 kg
source field at particle bound ≈ 657.53 g
```

Despite the enormous local field on an ideal active grain, the allowed receiver contains so little active matter that:

```text
maximum 1-kg payload acceleration ≈ 4.0218e-10 g
```

Optimistic receiver radius needed for 1-kg 1-g lift:

```text
≈ 2.48646e8 m
≈ 248646 km
```

Required compact coupling:

```text
g ≈ 3.14146e-2
```

which is approximately:

```text
4.98645e4
```

times the Borexino benchmark.

Decisions:

```text
INDIVIDUAL_GRAIN_SUBCRITICALITY_IS_SUFFICIENT=NO
INTER_GRAIN_VECTOR_SELF_ENERGY_PRESENT=YES
COMPACT_GRAIN_ENSEMBLE_HAS_COARSE_GRAINED_SCREENING_BOUND=YES
B_L_NEUTRAL_MATRIX_CANCELS_VECTOR_FIELD=NO
TERRESTRIAL_MICROSTRUCTURED_CHAMELEON_B_L_1G_PATH=REJECTED_AT_PREFLIGHT_LEVEL
009J_MICROSTRUCTURE_COLLECTIVE_SCREENING_GATE=GREEN
```

This closes passive nanograin/protium-matrix rescue for a compact terrestrial device at preflight level.

---

# 44. 009K — screened thin-shell residual force

Instead of avoiding screening, 009K asked whether the residual thin-shell force itself could be useful.

## Low-density branch

The screened background identities imply a maximum vector pressure only about half the scalar attractive pressure at zero gap.

009H parameters:

```text
ell_V ≈ 42.8067 m
ell_S ≈ 197.327 m
ell_S / ell_V ≈ 4.60973
```

Maximum vector/scalar pressure ratio:

```text
zero gap = 0.5
1 m      ≈ 0.491
10 m     ≈ 0.416
ell_V    ≈ 0.229
```

Therefore:

```text
009H_SCREENED_THIN_SHELL_CAN_BECOME_NET_REPULSIVE=NO
LOW_DENSITY_SCREENED_CHAMELEON_NET_REPULSION=REJECTED
```

## High-density branch

A high-density branch can have:

```math
\frac{\ell_S}{\ell_V}
=
\frac{\sqrt{2}gq}{\sqrt{\epsilon}}
```

so $\ell_S<\ell_V$ is algebraically possible.

With:

```text
ell_V = 100 nm
epsilon = 4 pi
```

the sign threshold was:

```text
g ≈ 5.79127e-11
q ≈ 4.32829e10
g q ≈ 2.50663
```

Thus a net-repulsive thin-shell window exists algebraically without immediately requiring a blatantly nonperturbative $gq$.

However direct-force constraints become devastating.

An intentionally weak proxy allowed a new force no larger than 5% of the ideal Casimir pressure at the predicted optimum gap.

Proxy frontier:

```text
g ≈ 6.64529e-11
q ≈ 3.52133e10
gq ≈ 2.34002
ell_S/ell_V ≈ 0.933534
optimal gap ≈ 1.07015 um
maximum net repulsive pressure ≈ 4.95661e-5 Pa
```

Supporting 1 kg at $1g$:

```text
required area ≈ 197850 m^2
equivalent square side ≈ 444.8 m
```

Using only the particle bound gave an absurdly large predicted force:

```text
g = 6.3e-7
optimal gap ≈ 5.17 nm
net repulsive pressure ≈ 2.800 GPa
```

with the force exceeding the weak Casimir residual proxy by:

```text
≈ 3.08e4
```

Decisions:

```text
LOW_DENSITY_SCREENED_CHAMELEON_NET_REPULSION=REJECTED
HIGH_DENSITY_SHORT_SCALAR_SIGN_ESCAPE_EXISTS_ALGEBRAICALLY=YES
PARTICLE_BOUND_ONLY_HIGH_DENSITY_POINT_COMPATIBLE_WITH_FORCE_DATA=NO
WEAK_5PCT_CASIMIR_PROXY_ALLOWS_USEFUL_1M2_1KG_LIFT=NO
THIN_SHELL_RESIDUAL_FORCE_IS_A_PRACTICAL_TERRESTRIAL_ESCAPE=STRONGLY_DISFAVORED
009K_THIN_SHELL_NET_FORCE_GATE=GREEN
```

An exact modern experiment-specific recast would still be needed for a formal no-go, but this branch should no longer receive significant engineering effort.

---

# 45. Strategic re-ranking after 009K

At this stage:

* classical GR had failed energetically;
* free-EM quantum negative energy had failed macroscopically;
* unscreened $B-L$ was measurable but topped out near 2.2% of $g$ under then-assumed constraints;
* monolithic terrestrial chameleon screening failed;
* microstructure failed at the necessary hiding scale;
* residual thin-shell repulsion was strongly disfavored.

The project then searched for an **experimental composition blind direction**.

This produced 009L.

---

# 46. 009L — material-phobic / gold-null vector

Phenomenological neutral-atom charge:

```math
Q_5
=
N+\beta Z
```

Natural gold is essentially monoisotopic $^{197}$Au:

```text
Z = 79
N = 118
```

Therefore:

```math
\beta_{\mathrm{Au}}
=
-\frac{118}{79}
=
-1.493670886075949
```

makes natural gold exactly neutral at the nuclear-counting level:

```math
Q_5(^{197}{\mathrm{Au}})=0
```

Other material charge-to-mass factors at this direction:

```text
Au = 0
Pt ≈ +2.96114e-3
W  ≈ -3.76221e-3
Os ≈ +3.73765e-3
Si ≈ -0.243040
C  ≈ -0.245694
Be ≈ -0.106800
Al ≈ -0.201478
```

Thus carbon remains strongly charged while gold becomes almost blind.

## Exact 2016 layered response preflight

The actual 2016 geometry was modeled, including:

Test body:

```text
250 nm Au
10 nm Cr
sapphire substrate
```

Source:

```text
150 nm Au
10 nm Cr
Au/Si structured layer
depth ≈ 2.10 um
```

At the 009G optimum range:

```text
lambda ≈ 112.206 nm
mass ≈ 1.75861 eV
```

the gold-phobic layered response relative to $B-L$ became:

```text
≈ 5.16168e-4
```

therefore the 2016 coupling bound weakened by:

```text
≈ 44.0154
```

Recast ISL coupling:

```text
≈ 8.65334e-12
```

Carbon coupling needed for 1-g half-space contact acceleration:

```text
≈ 8.53807e-12
```

Therefore the **ISL-only material recast** allowed approximately:

```text
1.02718 g
```

at contact.

Stand-off at that ISL ceiling:

```text
0 nm   ≈ 1.027 g
10 nm  ≈ 0.940 g
25 nm  ≈ 0.822 g
50 nm  ≈ 0.658 g
100 nm ≈ 0.421 g
250 nm ≈ 0.111 g
```

However, to remain conservative, the separate compiled Casimir $B-L$ curve was initially left **completely unrescaled**.

At 112 nm that produced:

```text
conservative allowed g ≈ 2.73329e-12
carbon contact acceleration ≈ 0.10248 g
```

Only a coupling-bound relaxation of:

```text
≈ 3.12374
```

would have been needed to restore 1 g.

This was extremely promising phenomenologically.

## Full conservative scan

The scan ended at its imposed high-mass boundary:

```text
mass = 7.5 eV
range ≈ 26.3103 nm
```

and therefore the reported “best” point is **boundary-limited, not a proven global optimum**.

At that scan edge, using the unrescaled Casimir curve:

```text
conservative g ≈ 1.55998e-10
conservative carbon contact acceleration ≈ 78.2756 g
```

This number must **not** be treated as physically allowed until the model and experiment-specific constraints are properly recast.

## Nanostructure geometry proxy

At a 112-nm interaction range and local $1g$ carbon surface field:

```text
pressure ≈ 3.8678e-3 Pa
```

A 1-kg payload requires:

```text
interaction area ≈ 2535.46 m^2
```

Packing that into a 10-cm cube corresponds to an interface-area density giving a characteristic layer-pitch proxy:

```text
≈ 394 nm
```

A 50%-active carbon 10-cm cube would contain:

```text
≈ 1.7575 kg carbon
```

Therefore the interface area is geometrically conceivable in nanostructured matter.

But directional force summation and mechanical cancellation were **not established**.

Decisions:

```text
NATURAL_GOLD_VECTOR_CHARGE_NULL=YES
2016_AU_SI_RESPONSE_SUPPRESSED_BY_MORE_THAN_1000X=YES
RECAST_ISL_BOUND_PERMITS_1G_CARBON_CONTACT_FIELD=YES
EVEN_UNRESCALED_CASIMIR_CURVE_PERMITS_AT_LEAST_0P1G=YES
ONLY_FEW_FOLD_CASIMIR_COUPLING_RELAXATION_NEEDED_FOR_1G=YES
COMPACT_NANOSTRUCTURE_AREA_SCALE_IS_GEOMETRICALLY_PLAUSIBLE=YES
GENERALIZED_VECTOR_UV_COMPLETION=NOT_ESTABLISHED
ASTROPHYSICAL_CONSTRAINT_RECAST=NOT_ESTABLISHED
009L_MATERIAL_PHOBIC_VECTOR_GATE=GREEN
```

009L was the strongest phenomenological practicality opening found so far.

But 009M and 009N then attacked its quantum-field-theory viability.

---

# 47. 009M — gold-null UV and stellar consistency

First observation:

A flavor-universal combination of:

```text
B-L
+
electromagnetic current
```

cannot change neutral-atom composition charge away from neutron number because:

```math
Q_{\mathrm{EM}}=0
```

for a neutral atom.

Therefore the gold-null direction cannot arise from the simplest flavor-universal $B-L+$EM construction.

## Family-dependent anomaly-free realization

Consider:

```math
X
=
B+x_eL_e+x_\mu L_\mu+x_\tau L_\tau
```

with right-handed neutrinos and anomaly condition:

```math
3+x_e+x_\mu+x_\tau=0
```

For a neutral atom:

```math
Q_X
=
A+x_eZ
=
N+(1+x_e)Z
```

The gold null requires:

```text
x_e = -2.493670886075949
```

A symmetric anomaly-free choice gave:

```text
x_mu = x_tau = -0.253164556962025
```

and:

```text
3 + x_e + x_mu + x_tau = 0
```

exactly.

Thus an anomaly-free family-dependent charge direction exists algebraically.

However it has a large electron coupling.

A deliberately **weak** stellar preflight used only:

```text
|g_e| < 1e-12
```

which implies:

```text
g_max ≈ 4.01015e-13
```

for the gold-null family current.

This was deliberately less restrictive than much of the published stellar literature.

At 112 nm:

```text
g required for 1g ≈ 8.53807e-12
stellar proxy g_max ≈ 4.01015e-13
gap ≈ 21.29
maximum contact acceleration ≈ 0.002206 g
```

At 26 nm:

```text
g required for 1g ≈ 1.76322e-11
gap ≈ 43.97
maximum acceleration ≈ 5.17e-4 g
```

The 009L 1-g point has electron coupling:

```text
≈ 2.1291e-11
```

which exceeds even the intentionally weak $10^{-12}$ proxy by:

```text
≈ 21.29
```

At the 26-nm 009L conservative coupling the electron coupling exceeded the proxy by:

```text
≈ 389
```

Decisions:

```text
009L_PHENOMENOLOGICAL_MATERIAL_NULL=SURVIVES
MINIMAL_FLAVOR_UNIVERSAL_ANOMALY_FREE_UV_REALIZATION=REJECTED
FAMILY_DEPENDENT_ANOMALY_FREE_GOLD_NULL_EXISTS=YES
FAMILY_DEPENDENT_GOLD_NULL_1G_SURVIVES_WEAK_STELLAR_PREFLIGHT=NO
FAMILY_DEPENDENT_GOLD_NULL_0P1G_SURVIVES_WEAK_STELLAR_PREFLIGHT=NO
LEPTOPHOBIC_ISOSPIN_GOLD_NULL_ESCAPE=ONLY_SURVIVING_009L_UV_CLASS_AT_THIS_GATE
009M_GOLD_NULL_UV_STELLAR_GATE=GREEN
```

The next question became whether a leptophobic proton/neutron current could retain the gold blind spot.

---

# 48. 009N — electroweak conservation / unavoidable axial obstruction

Latest completed gate.

The leptophobic gold-null low-energy nucleon charges were normalized as:

```math
q_n=1
```

```math
q_p=-\frac{118}{79}
=-1.493670886075949
```

For vector $u$ and $d$ quark charges:

```math
q_p
=
2v_u+v_d
```

```math
q_n
=
v_u+2v_d
```

Solving:

```text
v_u = -1.329113924050633
v_d = +1.164556962025316
```

so the required isovector splitting is:

```text
v_u - v_d = -2.493670886075949
```

This is the central obstruction.

Above electroweak symmetry breaking, $u_L$ and $d_L$ belong to the same $SU(2)_L$ doublet and share a common left-handed gauge charge.

Therefore a simple electroweak-gauge-invariant realization cannot have these as simultaneously pure-vector unequal charges.

The required vector splitting becomes an unavoidable axial splitting or must be compensated by additional Higgs/$W$/UV interactions.

## Model-independent isovector nucleon axial floor

Using:

```text
g_A ≈ 1.2754
```

at least one nucleon must have an axial coefficient of magnitude:

```text
>= 1.590213924051
```

within this simple electroweak matching argument.

This is an order-one axial sector.

## One-Higgs illustration

The one-Higgs electroweak realization gave:

```text
X_Q = -0.082278481012658
X_H = -2.493670886075949
X_uR = -2.575949367088608
X_dR = +2.411392405063291
c_A^u = -1.246835443037975
c_A^d = +1.246835443037975
```

Thus:

```text
|X_H| ≈ 2.49367
```

and the large axial sector is explicit.

## Free-streaming stellar axial preflight

Using the literature-motivated approximate bound:

```math
\frac{|c_A^N|}{f_X}
\lesssim
(10^8\ {\mathrm{GeV}})^{-1}
```

with:

```math
f_X
=
\frac{m_X}{g_X}
```

gave at the 112-nm 1-g point:

```text
m_X ≈ 1.75861 eV
g required for 1g ≈ 8.53807e-12
f_X at 1g ≈ 205.973 GeV
free-streaming stellar g_max ≈ 1.10589e-17
maximum acceleration ≈ 1.67767e-12 g
```

The nucleon axial coefficient allowed at the desired 1-g coupling would be only:

```text
≈ 2.05973e-6
```

compared with the unavoidable natural value:

```text
≈ 1.59021
```

requiring an axial suppression/cancellation of:

```text
≈ 7.7205e5
```

At 26 nm:

```text
m_X = 7.5 eV
g required for 1g ≈ 1.76322e-11
stellar g_max ≈ 4.71635e-17
maximum acceleration ≈ 7.15484e-12 g
required axial suppression ≈ 3.73852e5
```

Decisions from the actual user terminal:

```text
009L_MATERIAL_BLIND_DIRECTION=PHENOMENOLOGICALLY_SURVIVES
PURE_VECTOR_LEPTOPHOBIC_ISOSPIN_CURRENT_IS_ELECTROWEAK_CONSERVED=NO
UNAVOIDABLE_ORDER_ONE_AXIAL_OR_EW_COMPENSATING_SECTOR=YES
SIMPLE_ONE_HIGGS_GOLD_NULL_VECTOR_1G_PATH=REJECTED_AT_PREFLIGHT_LEVEL
FREE_STREAMING_STELLAR_AXIAL_PREFLIGHT_PERMITS_1G=NO
STELLAR_TRAPPING_OR_EXOTIC_CANCELLATION_FORMALLY_EXCLUDED=NO
MULTI_HIGGS_OR_EW_COMPENSATED_UV_COMPLETION=NOT_ESTABLISHED
FINE_TUNED_FCNC_LONGITUDINAL_CANCELLATION=NOT_ESTABLISHED
PRACTICAL_GOLD_NULL_VECTOR=NOT_ESTABLISHED
PRACTICAL_ANTIGRAVITY=NOT_ESTABLISHED
NEXT=GLOBAL_RERANK_OPPOSITE_SIGN_SCALAR_FORCE_VS_EXOTIC_EW_COMPENSATED_VECTOR
009N_ELECTROWEAK_CONSERVATION_GATE=GREEN
```

This is the current frontier.

---

# 49. Exact interpretation of 009N

009N does **not** prove every imaginable gold-null vector theory impossible.

What it does prove at preflight level is:

> The simplest leptophobic isospin-violating pure-vector interpretation is not electroweak conserved.

The required neutron/proton contrast forces a very large $u/d$ isospin splitting.

In a simple gauge-invariant realization that translates into:

* order-one axial quark couplings;
* Higgs charge;
* weak-isospin-current nonconservation;
* or equivalent compensating electroweak interactions.

Very light vectors coupled to nonconserved currents have dangerous longitudinal production.

The free-streaming stellar estimate destroys the uncomplicated 1-g point by many orders of magnitude.

Still unresolved:

* stellar trapping at much stronger coupling;
* carefully arranged multi-Higgs models;
* UV completions with compensating electroweak amplitudes;
* tuned flavor structure;
* whether a fully anomaly-free light isospin vector can eliminate all dangerous longitudinal channels;
* exact FCNC/Wess–Zumino constraints for a specific such model.

Therefore the correct status is:

```text
SIMPLE_GOLD_NULL_VECTOR=REJECTED
EXOTIC_EW_COMPENSATED_GOLD_NULL_VECTOR=UNRESOLVED_BUT_HIGH_RISK
```

Do not spend major effort on the exotic vector unless it wins the global rerank.

---

# 50. Major literature references carried forward

Important references already used or identified:

## General GR / quantum

Brown and Maclay:

```text
Vacuum Stress between Conducting Plates
Phys. Rev. 184, 1272
```

Fulling et al.:

Casimir energy gravitates normally.

Costa and Matsas:

complete mechanically supported Casimir apparatus and positive total mass under DEC assumptions.

Pfenning:

electromagnetic quantum inequalities used for 007B.

## $B-L$ vector

Cheng, Sheng, Yanagida:

```text
Detecting a Fifth-Force Gauge Boson via Superconducting Josephson Junctions
arXiv:2402.14514
```

## 2016 Casimir-less force experiment

Chen et al.:

```text
Phys. Rev. Lett. 116, 221102
arXiv:1410.7267
```

This is central for any future material-dependent short-range force recast.

## CANNEX

Final-design paper:

```text
arXiv:2403.10998
```

## Chameleon vector

Nelson and Walsh:

```text
Chameleon Vector Bosons
Phys. Rev. D 77, 095006
arXiv:0802.0762
```

## AxionLimits

Used as a current compiled constraint source for vector $B-L$:

```text
VectorB-L/
InverseSquareLaw.txt
Sun.txt
HorizontalBranch.txt
RedGiant.txt
Casimir.txt
EotwashEP.txt
MICROSCOPE.txt
```

Important:

AxionLimits is a compilation.

Central conclusions should ultimately be checked against underlying experiments and model assumptions.

## Borexino

A light-$B-L$ vector particle-level bound of approximately:

```text
g_BL <= 6.3e-7
```

was used as an optimistic particle benchmark in 009J.

## Stellar electron-coupled vector work

Relevant older $U(1)_L$ stellar constraints:

```text
arXiv:1512.03179
```

## General plasma production of new vectors

Relevant discussion:

```text
arXiv:2304.12907
```

Important result:

general $U(1)$ vectors do not automatically receive the same low-mass plasma suppression as a photon-aligned dark photon.

## Nonconserved-current / longitudinal-vector constraints

Dror, Lasenby, Pospelov:

```text
Phys. Rev. D 96, 075036
```

and related:

```text
Phys. Rev. Lett. 119, 141803
```

These are central for the electroweak/axial obstruction discovered in 009N.

All external claims should be reverified against primary papers when reused.

---

# 51. Branch status matrix

## Classical positive-energy GR

Status:

```text
THEORETICALLY_STRONG
PRACTICALLY_ENERGETICALLY_POOR
```

Best project result:

```text
006D
```

Do not abandon scientifically.

Do not prioritize for engineering without a new scaling mechanism.

---

## Static Casimir / free-EM negative energy

Status:

```text
PRACTICAL_BRANCH_REJECTED
```

Reason:

required scales are around $10^{-19}$ m for $1g$.

---

## Free-EM quantum-inequality loophole

Status:

```text
MACROSCOPIC_PRACTICAL_BRANCH_REJECTED
```

Reason:

causal bound gives approximately $10^{-54}$–$10^{-55}$ m/s² at meter scale.

---

## 006D canonical scalar realization

Status:

```text
PARTIAL_LOCAL_REALIZATION_SURVIVES
GLOBAL_REALIZATION_NOT_ESTABLISHED
PRACTICAL_PRIORITY_LOW
```

One complex scalar rejected.

Ungauged winding finite set rejected.

Gauge-assisted local decomposition survives.

No reason to finish the complicated global solution until a scaling breakthrough appears.

---

## Ordinary unscreened $B-L$

Status:

```text
LAB_DETECTION_BRANCH_SURVIVES
PRACTICAL_MACROSCOPIC_BRANCH_REJECTED
```

Strongest use:

009D/009E/009F experimental search.

Absolute half-space ceiling under current compiled constraints:

```text
≈ 0.0221 g at contact
```

at:

```text
lambda ≈ 112 nm
```

---

## Monolithic terrestrial chameleon $B-L$

Status:

```text
REJECTED_AT_PREFLIGHT_LEVEL
```

Reason:

device unscreening and Earth short-range hiding are algebraically incompatible at relevant macroscopic size.

---

## Microstructured chameleon $B-L$

Status:

```text
REJECTED_AT_PREFLIGHT_LEVEL
```

for compact terrestrial $1g$ at a submicron hiding scale.

---

## Chameleon thin-shell residual repulsion

Status:

```text
LOW_DENSITY_REJECTED
HIGH_DENSITY_ALGEBRAIC_SIGN_WINDOW_EXISTS
PRACTICAL_TERRESTRIAL_USE_STRONGLY_DISFAVORED
```

An exact modern experimental recast would be needed for a formal no-go, but priority is low.

---

## Gold-phobic generalized vector

Phenomenological status:

```text
VERY_INTERESTING
```

QFT status:

```text
SIMPLE_REALIZATIONS_REJECTED
EXOTIC_EW_COMPENSATED_REALIZATION_UNRESOLVED_HIGH_RISK
```

Do not confuse the beautiful 009L phenomenological blind direction with a viable quantum field theory.

---

## Remote-space small-source chameleon regime

Status:

```text
NOT_REJECTED
```

But even if real, this is not presently a terrestrial lift mechanism.

Keep as a lower-priority theoretical branch.

---

# 52. Current practical-antigravity probability calibration

The current best calibrated subjective estimate discussed in this session was:

```text
practical human-scale antigravity:
~4%
```

with a rough subjective uncertainty band:

```text
~2–8%
```

This is not a statistical confidence interval.

It is a research-prior estimate conditioned on everything currently known.

Do **not** raise this because a new gate prints GREEN.

The user explicitly wants to push toward:

```text
20%
```

but this percentage must be **earned by physics**, not chosen motivationally.

009L briefly looked capable of materially increasing the estimate.

009M and 009N then eliminated the simplest realizations.

Therefore there is currently no scientifically defensible reason to claim 10% or 20% practical antigravity.

A rough milestone confidence ladder discussed was:

```text
local repulsion mathematically possible:
>99%

local repulsion within established GR:
~98%

finite positive-energy source can show local repulsion:
~95%

some sensible field theory can realize some repulsive source:
~60–70%

a genuinely new neutral-matter repulsive fifth force exists:
~10–20%

future experimentally accessible repulsive-force anomaly:
~10–15%

useful 0.01g–1g local mechanism:
~5–8%

controllable human-scale practical antigravity:
~4%

reactionless antigravity propulsion:
far below 1%
```

These are subjective research priors.

They should not be presented as measured probabilities.

---

# 53. What would justify moving toward 10–20%

A real probability increase requires a qualitatively different milestone.

Examples:

## Criterion A

A healthy field theory survives:

* UV consistency;
* radiative stability;
* laboratory fifth-force bounds;
* stellar bounds;
* cosmological bounds;

and still predicts at least approximately:

```text
0.1g–1g
```

at a useful geometry.

## Criterion B

A reproducible laboratory experiment observes neutral-matter repulsion not attributable to:

* electromagnetism;
* Casimir forces;
* thermal gradients;
* vibration;
* patch potentials;
* charging;
* ordinary gravity.

## Criterion C

A field/material realization of the 006D-type GR source is found that changes the scaling by **orders of magnitude**, not merely coefficient $C$.

## Criterion D

A new mechanism produces a controllable external force on kilogram-scale matter with a non-astronomical reaction/source infrastructure and survives existing constraints.

Until something like this occurs, 20% would be unjustified.

---

# 54. Crucial semantic distinction

The vector-force branch is not ordinary gravitational repulsion.

A repulsive fifth force acting on neutral matter may be useful for an “antigravity-like actuator,” but scientifically it must be labeled as:

```text
REPULSIVE_FIFTH_FORCE
```

or:

```text
ANTIGRAVITY_LIKE_FORCE
```

unless it actually modifies spacetime/gravity.

An anchored source producing upward force does not imply reactionless propulsion.

For an isolated source plus payload:

```math
\mathbf{F}_{12}
=
-\mathbf{F}_{21}
```

and the center of mass cannot accelerate without exchanging momentum with something external.

---

# 55. Highest-value next scientific action

The current live frontier from 009N is:

```text
NEXT=
GLOBAL_RERANK_OPPOSITE_SIGN_SCALAR_FORCE_VS_EXOTIC_EW_COMPENSATED_VECTOR
```

The next session should **not immediately write another large simulation**.

First perform a rigorous global rerank.

The leading two candidates are:

## Candidate 1 — composition-dependent scalar exchange

This is now the most interesting fresh branch.

Why:

A scalar mediator does not require conservation of a gauge current and therefore avoids the specific longitudinal-vector/electroweak obstruction that killed the simple 009L vector realization.

For a scalar Yukawa interaction schematically:

```math
V_s(r)
\propto
-\frac{g_1g_2}{4\pi r}
e^{-m_sr}
```

same-sign scalar charges attract while opposite-sign effective scalar charges can repel.

The central question is:

> Can stable neutral materials acquire opposite-sign effective scalar charges in a technically natural, experimentally allowed field theory with enough coupling strength and range to produce useful force?

This branch must be tested brutally against:

* equivalence-principle tests;
* fifth-force searches;
* stellar emission;
* scalar mixing;
* radiative naturalness;
* nucleon scalar matrix elements;
* electron coupling;
* Higgs mixing;
* cosmology;
* self-interaction/screening;
* whether stable ordinary materials can really have opposite effective charge signs.

Do not assume opposite signs are physically achievable just because the phenomenological formula permits them.

The smallest decisive gate should first answer:

```text
CAN_A_HEALTHY_SCALAR_GIVE_OPPOSITE_SIGN_CHARGES_TO_TWO_STABLE_NEUTRAL_MATERIALS?
```

and then:

```text
WHAT_IS_THE_ABSOLUTE_CONSTRAINT_LIMITED_HALFSPACE_ACCELERATION?
```

Only if both survive should a nanostructure actuator be considered.

## Candidate 2 — exotic electroweak-compensated gold-null vector

Keep only as a secondary competitor.

Required accomplishments:

* explicit anomaly-free UV completion;
* electroweak gauge invariance;
* no unavoidable dangerous longitudinal current;
* no unacceptable FCNC;
* no electron/stellar catastrophe;
* no Wess–Zumino catastrophe;
* enough low-energy proton/neutron isospin contrast to retain the gold blind spot;
* current force constraints still permit approximately $0.1g$–$1g$.

This is a very high bar.

Do not spend major implementation time unless a literature/analytical preflight demonstrates that such a model genuinely exists.

## Candidate 3 — remote-space vector/chameleon regime

Retain as fallback.

This branch is not presently killed because the large Earth/environment source causing terrestrial screening problems can be removed in deep space.

However it remains:

* speculative;
* experimentally unobserved;
* not reactionless;
* dependent on an external interaction partner/source.

It should rank below the scalar rerank unless a clear known model suddenly gives a dramatic advantage.

---

# 56. Recommended next-session decision procedure

The next session should start by creating a table like:

| Criterion                 | Opposite-sign scalar | Exotic compensated vector | Remote-space chameleon |
| ------------------------- | -------------------: | ------------------------: | ---------------------: |
| Known healthy QFT         |                    ? |                 High risk |                Partial |
| Repulsion sign available  |                    ? |    Yes phenomenologically |                    Yes |
| Current lab constraints   |                    ? |                    Severe |  Environment dependent |
| Stellar constraints       |                    ? |            Severe/unknown |        Model dependent |
| Naturalness               |                    ? |               Major issue |            Major issue |
| $0.1g$ possible           |                    ? |   Only phenomenologically |                Unknown |
| $1g$ possible             |                    ? |     Simple forms rejected |                Unknown |
| Useful range              |                    ? |        tens–100 nm so far |     potentially larger |
| Reactionless              |                   No |                        No |                     No |
| Expected information gain |              Highest |                    Medium |             Medium/low |

Then choose **one** cheapest analytical/literature gate.

The preferred next research question is:

> **Does a theoretically healthy scalar interaction admit opposite-sign effective charges for stable neutral materials and, after all existing constraints, can its half-space acceleration exceed the vector 009G ceiling by orders of magnitude?**

If the answer is no, close that branch immediately.

If yes, it becomes the next major candidate.

---

# 57. What NOT to do next

Do not:

* restart 006 coefficient optimization;
* rerun 007 Casimir/QEI with slightly different numbers;
* spend time finishing the global 006D charged/gauged field realization;
* retune 009H $m_s$, $g$, or $q$;
* retry monolithic chameleon geometry;
* retry passive chameleon nanograins;
* optimize a chameleon thin-shell actuator before exact force constraints;
* treat the 78-g 009L scan-edge result as physically allowed;
* optimize gold-null nanostructures before finding a healthy field theory;
* immediately build an exotic multi-Higgs vector model without a cheap consistency/literature gate;
* inflate practical-antigravity probability to 20% because the user wants that target.

The target is motivation.

The physics must earn the probability.

---

# 58. Important subtlety about the 009L 78-g number

The 009L full conservative scan reported:

```text
BEST_MASS_EV=7.5
BEST_RANGE_NM≈26.31
BEST_CONSERVATIVE_CONTACT_A_OVER_G≈78.28
```

This was at the **hard upper boundary of the scanned mass interval**.

Therefore it is not a verified interior optimum.

More importantly, it used the original compiled $B-L$ Casimir numerical curve without a proper composition-specific model recast.

It subsequently failed simple UV/stellar consistency in 009M/009N.

Do not quote:

```text
78 g allowed
```

without all of these caveats.

The scientifically correct statement is:

> A phenomenological gold-phobic charge assignment greatly weakens some gold-coated laboratory force responses and can yield formally large carbon half-space accelerations under incompletely recast constraints, but the simplest quantum-field-theory realizations are strongly disfavored by electron or unavoidable axial/electroweak couplings.

---

# 59. Important surviving experimental result independent of practicality

Even if all practical-actuator branches fail, the 009D–009F work remains scientifically valuable.

The project has identified a plausible **laboratory test architecture** for a repulsive short-range neutral-matter vector force:

```text
plane-parallel geometry
+
electromagnetic/Casimir shield
+
composition modulation
+
possibly isotope modulation
```

This could potentially reach couplings around:

```text
few × 1e-17
```

under the simplified CANNEX-class estimates.

That is a separate Level-9 scientific objective.

If practical antigravity remains elusive, this experimental branch could still be worth formalizing as a publishable proposal after exact constraint/systematic analysis.

---

# 60. Current strongest established result versus strongest speculative result

## Strongest established project-derived classical result

```text
006D
```

A finite, nonsingular, positive-energy, locally conserved, NEC/WEC/DEC-compatible linearized-GR source generates local outward gravity while retaining positive far-field mass.

This is the strongest **physics-established** project result.

## Strongest experimental new-force concept

```text
009D–009F
```

A CANNEX-class plane-parallel/isotope-modulated experiment could plausibly test a repulsive neutral-matter vector force in an interesting micron-scale parameter regime.

## Strongest phenomenological practicality opening

```text
009L
```

Material-response blind directions can weaken some gold-coated short-range force experiments enough that formally order-$g$ nanoscale forces become possible.

But:

```text
009M + 009N
```

show that the simplest healthy QFT realizations of that direction fail.

Therefore 009L is not currently the leading viable theory.

---

# 61. Current accomplishment ladder

For established GR, the project has approximately reached:

```text
Level 0 — YES
Level 1 — YES
Level 2 — YES within linearized stated model
Level 3 — YES for 006D
Level 4 — YES for 006D
Level 5 — YES for 006D
Level 6 — NOT ESTABLISHED
Level 7 — PARTIAL LOCAL FIELD-THEORY REPRESENTABILITY ONLY
Level 8 — NO
Level 9 — NO for gravitational 006D source
Level 10 — NO
```

For the fifth-force branch:

```text
mathematical repulsive interaction — YES
healthy minimal B-L theory — YES
existence in nature — NO
experimentally searchable — YES
possible Level-9 force experiment — YES
useful human-scale actuator — NO
reactionless propulsion — NO
```

---

# 62. Documentation debt

The current repository documentation is significantly stale.

The attached `RESEARCH_BUILDPLAN.md` still says the active phase is approximately:

```text
006B / 006C / 006D
then 007
then 008 modified gravity
```

The actual live frontier has progressed through 009N.

The attached README still says the immediate objective is 007A/007B.

This is now incorrect.

After the next global-rerank gate determines the new leading branch, the project should update:

```text
RESEARCH_BUILDPLAN.md
NOTES.md
README.md
CLAIMS.md
ASSUMPTIONS.md
RESEARCH_QUESTIONS.md
```

as needed.

Do **not** rewrite all documentation before the rerank.

First determine the new branch.

Then update documents once so they reflect a stable frontier.

---

# 63. Buildplan update that will eventually be needed

The revised buildplan should record:

```text
007A:
static Casimir practicality — deprioritized

007B:
free-EM QEI macroscopic route — closed

008A:
wall/current-loop support — no improvement

008B:
local scalar representability — yes

008C:
fixed-charge dilation capacity — survives

008D:
one complex scalar — rejected

008E:
finite ungauged winding set — rejected

008F:
finite local gauge takeover window — survives but does not solve energy scaling

009A:
generic repulsive Yukawa scaling escape — survives phenomenologically

009B:
B-L concrete vector model — laboratory-interesting

009C:
modern force-experiment synthesis

009D:
CANNEX plane-parallel force gate — laboratory path green

009E:
shield/error preflight — green

009F:
isotope-null design — green under stated assumptions

009G:
unscreened ordinary-matter vector practical ceiling ≈ 0.022g — practical geometry route closed

009H:
global Earth/device screening hierarchy appeared possible

009I:
terrestrial tabletop hiding conflict — monolithic chameleon rejected

009J:
microstructure/neutral-matrix rescue — rejected

009K:
thin-shell practical terrestrial escape — strongly disfavored

009L:
gold-phobic material blind direction — phenomenologically strong

009M:
simple family-dependent gold-null realization — stellar killed

009N:
simple leptophobic isospin gold-null realization — electroweak/axial killed

NEXT:
global rerank of opposite-sign scalar force versus exotic electroweak-compensated vector
```

---

# 64. Claims ledger to preserve

## KNOWN / REPRODUCED

* positive $\Lambda$ causes geodesic defocusing;
* Kottler static-radius behavior;
* domain-wall gravitational repulsion;
* Reissner–Nordström local neutral-particle repulsion;
* negative pressure/tension can contribute repulsively;
* Casimir vacuum stress has a locally repulsive active-stress combination;
* complete Casimir apparatus must include support energy/stress.

## PROJECT-DERIVED AND WELL SUPPORTED

* positive-energy local gravitational repulsion is possible;
* negative ADM mass is not required;
* 005B finite disk/rim result;
* 006B thin coefficient approximately 23.426710;
* 006C independently verifies 005B;
* 006D finite-thickness, positive-energy, locally conserved DEC-compatible source;
* static GR constructions examined retain $ah^2/G$ scaling;
* 006D local canonical-scalar Gram representability;
* static scalar Derrick instability;
* charged temporal kinetic capacity is sufficient for one dilation mode;
* one charged winding scalar cannot exactly reproduce 006D;
* finite ungauged winding set fails at the termination;
* finite local gauge boundary takeover window exists;
* unscreened ordinary-matter linear Yukawa source cannot beat the half-space field;
* current compiled $B-L$ constraints imply about 2.2% $g$ maximum unscreened contact acceleration under the optimistic benchmark;
* monolithic chameleon terrestrial hiding/device-unscreening conflict;
* collective microstructure does not evade the same screening problem at useful filling fraction;
* simple gold-null vector realizations face severe electron or electroweak/axial constraints.

## NOT ESTABLISHED

* exact nonlinear GR 006D solution;
* dynamical stability of 006D;
* known material producing 006D stress;
* practical classical GR antigravity;
* existence of any new repulsive fifth force;
* $B-L$ force detection;
* exact CANNEX $B-L$ sensitivity;
* exact $B-L$ condensed-matter shield response;
* practical chameleon vector;
* viable gold-null vector UV completion;
* practical composition-dependent scalar force;
* practical antigravity;
* reactionless propulsion;
* novel discovery.

---

# 65. Current best concise project statement

Recommended conservative statement:

> **ANTIGRAVITY_RESEARCH has established that local gravitational repulsion is physically allowed within ordinary general relativity and has constructed a finite-radius, finite-thickness, nonsingular, positive-energy, locally conserved linearized-GR stress-energy source satisfying NEC, WEC, and DEC that produces a locally outward gravitational field while retaining positive far-field mass. The principal obstacle in established GR is not the sign of gravity but the catastrophic source-energy scaling $M\sim C ah^2/G$, with the best verified explicit coefficient near $C=23.5$. Established free-field quantum negative-energy bounds do not provide a macroscopic escape. Repulsive short-range vector forces provide a much better force-per-source-mass scaling and could plausibly be tested with plane-parallel, shielded, composition- or isotope-modulated experiments, but current work has not established that such a force exists. Ordinary unscreened $B-L$ interactions are constraint-limited to roughly 2.2% of $g$ at nanoscale contact in an optimistic half-space benchmark, and multiple terrestrial chameleon-vector escape routes have been falsified or strongly disfavored. A phenomenological material-blind vector direction can weaken gold-coated force constraints dramatically, but the simplest anomaly-free or leptophobic electroweak realizations are strongly disfavored by stellar and longitudinal-vector consistency arguments. The current highest-value frontier is a global reranking between composition-dependent opposite-sign scalar exchange and much more exotic electroweak-compensated vector theories. Practical antigravity and reactionless propulsion remain unestablished.**

---

# 66. First actions next session

Do these in order.

## Step 1 — inspect repository state

```bash
git status --short
```

## Step 2 — verify permanent regression baseline

```bash
ROOT="$(pwd)"
PY="$ROOT/.venv/bin/python"

PYTHONPATH="$ROOT/src" \
"$PY" -m pytest -q tests/known_solutions
```

Expected if unchanged:

```text
94 passed
```

## Step 3 — do NOT patch anything yet

Use the current frontier:

```text
GLOBAL_RERANK_OPPOSITE_SIGN_SCALAR_FORCE_VS_EXOTIC_EW_COMPENSATED_VECTOR
```

## Step 4 — perform authoritative literature reconnaissance

Highest-priority scalar questions:

1. Can scalar couplings to stable neutral matter have opposite effective signs?
2. What operator structure generates those signs?
3. Does the same operator produce dangerous Higgs/electron/nucleon couplings?
4. Are there known technically natural ultralight/eV-range scalar constructions?
5. What stellar bounds apply?
6. What equivalence-principle bounds apply?
7. Are composition blind directions available analogous to 009L?
8. Can screening help without recreating the 009I/J tradeoff?
9. What is the maximum constraint-allowed half-space acceleration?
10. Does any surviving point reach at least $0.1g$?

## Step 5 — only then write the next disposable gate

The next gate should be small and falsifiable.

Do not make it permanent until the theory survives.

---

# 67. Recommended next research-slice success criterion

The next branch deserves serious priority only if it satisfies all three:

```text
THEORETICALLY_HEALTHY=YES
CURRENT_CONSTRAINTS_ALLOW_ORDER_0P1G_OR_MORE=YES
PRACTICAL_GEOMETRY_NOT_ASTRONOMICAL=YES
```

If not, close it quickly.

The threshold for raising the practical-antigravity probability toward 20% should be even stronger:

```text
HEALTHY_FIELD_THEORY=YES
EXISTING_LAB_CONSTRAINTS_SURVIVED=YES
STELLAR_CONSTRAINTS_SURVIVED=YES
COSMOLOGY_NOT_OBVIOUSLY_FATAL=YES
ORDER_1G_LOCAL_FORCE=YES
USEFUL_FORCE_ON_MACROSCOPIC_RECEIVER=YES
FINITE_PLAUSIBLE_GEOMETRY=YES
NO_HIDDEN_MANY_ORDERS_OF_MAGNITUDE_REQUIREMENT=YES
```

Until something close to this exists:

```text
PRACTICAL_ANTIGRAVITY_PROBABILITY ≈ 4%
```

remains the conservative project estimate.

---

# 68. Most important strategic lesson from this session

The project is now extracting far more information from **negative results** than from speculative optimization.

The sequence:

```text
009H -> 009I -> 009J -> 009K
```

is a model example.

009H found a large apparent hierarchy.

009I discovered the relevant tabletop-screening incompatibility.

009J tested the strongest geometric escape.

009K tested the residual thin-shell escape.

The whole terrestrial chameleon branch was narrowed without spending weeks building nonlinear PDE solvers.

Likewise:

```text
009L -> 009M -> 009N
```

found a powerful phenomenological loophole and then immediately attacked whether a healthy QFT could realize it.

That research style should continue.

The shortest path to practical antigravity is not to keep the most exciting equation alive.

It is to kill bad branches cheaply until only a physically viable mechanism remains.

---

# 69. Final handoff directive

At the beginning of the next session, use profound but disciplined analysis.

Do not repeat already solved work.

Do not restart classical coefficient optimization.

Do not restart free-EM quantum-negative-energy work.

Do not retune the rejected chameleon constructions.

Do not engineer the gold-null vector before solving its field-theory consistency problem.

The single active question is:

> **Does a composition-dependent scalar force, or any other theoretically healthy interaction not suffering the vector-current obstruction, provide an experimentally allowed route to order-$0.1g$–$1g$ repulsion on useful matter with a finite plausible architecture?**

The cheapest decisive experiment answering that question is the next priority.

If the scalar branch fails, perform the same ruthless rerank rather than forcing it.

If it survives theory, stellar, laboratory, and half-space-practicality gates simultaneously, then it will have earned permanent implementation and a genuine upward revision of the project's practical-antigravity probability.


### END NOTE - AUGUST 28 2026 - 00:35 CST

---

### BEGIN NOTE - AUGUST 28 2026 - POST-009N / 010D FRONTIER UPDATE

# 70. Headline claim promoted to primary project language

The strongest verified project result should now be stated prominently as:

> **We have a mathematical construction for antigravity-like gravitational repulsion.**

This wording is intentionally stronger than merely saying that GR contains repulsive examples, but narrower than claiming a practical device.

The construction is specifically the finite-thickness 006D linearized-GR stress-energy source.

Analytic construction:

```math
q(r)=r p_r(r)
```

```math
p_\phi(r)=\frac{dq}{dr}
```

```math
p_z=0
```

```math
\epsilon
=
\max
\left(
|p_r|,
|p_\phi|
\right)
```

which provides local radial conservation and pointwise DEC/WEC/NEC for the static type-I tensor.

The finite source is evaluated with the axial Green-function expression

```math
a_z(h)
=
-\frac{2\pi G}{c^2}
\int dz
\int_0^\infty dr\,
r
\left(
\epsilon+p_r+p_\phi+p_z
\right)
\frac{h-z}
{\left[r^2+(h-z)^2\right]^{3/2}}
```

and the verified source gives an outward near field while its integrated active mass remains positive.

Best tested finite coefficient:

```math
C_{\mathrm{finite}}
=
23.591586299249
```

with

```math
M_{\mathrm{equiv}}
=
C\frac{a h^2}{G}
```

This is the mathematical basis of the headline claim.

The proof scope remains:

```text
CONSTRUCTIVE_LINEARIZED_GR_STRESS_ENERGY_RESULT
```

not:

```text
PRACTICAL_ANTIGRAVITY_DEVICE
```

---

# 71. Regression baseline reconfirmed

The known-solution suite was rerun at the start of the post-009N slice.

Result:

```text
94 passed in 4.42s
TEST_RC=0
```

Working-tree state matched the expected post-008B / partial-008C repository state.

No repository defect blocked the frontier calculations.

---

# 72. 009O — opposite-sign scalar stellar / half-space gate

The low-energy scalar sign question survived:

```text
SCALAR_OPPOSITE_SIGN_CHARGE=YES_AT_LOW_ENERGY_EFT_LEVEL
```

However, neutron-star cooling is especially damaging for unequal proton and neutron scalar couplings because the neutron-proton bremsstrahlung channel contains an isospin-violating contribution that is less velocity-suppressed than the equal-coupling term.

A broad analytical/literature-normalized scan used an optimistic geometry:

```text
SOURCE=OSMIUM_192_INFINITE_HALF_SPACE
TEST=HYDROGEN_1
CONTACT_GAP=ZERO
SOURCE_THICKNESS=INFINITE
```

Best point:

```text
BEST_GP_OVER_GN=-0.712781680480
BEST_ALLOWED_GN=4.641510896240e-14
BEST_CONTACT_A_OVER_G=7.327295675071e-04
```

Comparison:

```text
VECTOR_009G_CEILING_A_OVER_G=2.200000000000e-02
PRACTICAL_TARGET_A_OVER_G=1.000000000000e-01
MARGIN_TO_009G=3.002471986336e+01
MARGIN_TO_0P1G=1.364759993789e+02
```

Decision:

```text
009O_A_PREFLIGHT_DECISION=UNSCREENED_OPPOSITE_SIGN_SCALAR_STRONGLY_DISFAVORED
```

A full NSCool likelihood recast was not performed, so this is not a formal universal exclusion. The margin is nevertheless large enough that the ordinary unscreened scalar branch lost global priority.

---

# 73. 009P — effective-Z' UV and momentum-conservation gate

The material-blind 009L force remained the only low-energy phenomenological fifth-force branch that had formally crossed $1g$, but its UV completion was unresolved.

The effective-$Z'$ portal preflight found, at the $1g$ benchmark:

```text
PERTURBATIVE_1G_UP_PARTNER_MAX_GEV=388.452933
PERTURBATIVE_1G_DOWN_PARTNER_MAX_GEV=443.343021
EXTREME_4PI_1G_UP_PARTNER_MAX_GEV=1377.029794
EXTREME_4PI_1G_DOWN_PARTNER_MAX_GEV=1571.610091
```

At $6g$ even the extreme $y=4\pi$ ceilings fell to:

```text
UP_PARTNER_MAX_GEV=562.170059
DOWN_PARTNER_MAX_GEV=641.607133
```

The same gate established an independent practical classification:

```text
PAIR_FORCE_SUM=F12_PLUS_F21=0
SELF_CONTAINED_STATIC_FIFTH_FORCE_COM_ACCELERATION=0
SELF_CONTAINED_MULTILAYER_FIFTH_FORCE_LIFT=REJECTED
GROUND_REFERENCED_EXTERNAL_SOURCE_LEVITATION=NOT_REJECTED_BY_THIS_ARGUMENT
```

This is a central distinction.

A short-range fifth force may produce force relative to an external source plate, but reciprocal internal force layers do not accelerate an isolated craft's center of energy.

---

# 74. 009Q — electroweak dichotomy / UV-scale gate

The required gold-null low-energy vector coefficients are

```text
V_U=-1.329113924050633
V_D=1.164556962025316
```

If the left-handed $u$ and $d$ currents remain in a normal $SU(2)_L$ doublet, the minimum unavoidable axial coefficient is

```math
\frac{|v_u-v_d|}{2}
=
1.246835443037975
```

and at the $1g$ coupling:

```text
UNAVOIDABLE_AXIAL_COUPLING_AT_1G=1.064556829114e-11
```

Thus the $SU(2)_L$-preserving branch returns to the 009N axial/longitudinal obstruction.

For the pure-vector EWSB-compensated branch, the dimension-eight preflight gave:

```text
C_EQ_1_LAMBDA_U_MAX_GEV=164.185307
C_EQ_1_LAMBDA_D_MAX_GEV=169.701100

C_EQ_4PI_LAMBDA_U_MAX_GEV=309.126870
C_EQ_4PI_LAMBDA_D_MAX_GEV=319.511963

C_EQ_4PI_SQUARED_LAMBDA_U_MAX_GEV=582.021760
C_EQ_4PI_SQUARED_LAMBDA_D_MAX_GEV=601.574737
```

Even with the extreme $y=4\pi$ choice, a $1.5\ {\mathrm{TeV}}$ up-type partner required

```text
M1500_UP_SIN2=1.186576777155e+00
M1500_UP_PHYSICAL=NO
```

Decision:

```text
009Q_DECISION=EXOTIC_EW_COMPENSATED_VECTOR_SEVERELY_STRESSED_NOT_YET_CLOSED
```

The project should not claim a model-independent exclusion of all possible exotic vectors, but the simple effective-$Z'$ rescue is no longer a high-value engineering branch.

---

# 75. 010A — healthy universal scalar-tensor sign gate

For a healthy universally coupled canonical scalar, the force correction between identical ordinary bodies is proportional to a nonnegative charge product.

The scan returned:

```text
MIN_UNIVERSAL_CANONICAL_F_OVER_FGR=1.000000000000000e+00
UNIVERSAL_CANONICAL_SCALAR_REPULSION=NO
```

Metric $f(R)$ reproduced:

```text
FR_SHORT_RANGE_UNSCREENED_LIMIT=1.333333333333333e+00
FR_REPULSIVE_BRANCH=NO
```

Screening suppresses the extra force back toward GR but does not reverse its sign.

Opposite scalar charges can repel but return to the 009O fifth-force class.

Wrong-sign scalar kinetic energy can reverse the sign but introduces a ghost and is physically rejected.

---

# 76. 010B — vector-tensor / spin-2 weak-field sign gate

Einstein-aether Newtonian response was tested through

```math
G_N
=
\frac{G}
{1-c_{14}/2}
```

A sign reversal with positive bare $G$ requires crossing $c_{14}=2$, which is a singular/pathological point rather than a viable laboratory regime.

Positive-residue extra spin-2 exchange gave:

```text
MIN_POSITIVE_RESIDUE_F_OVER_FGR=1.000000000000000e+00
POSITIVE_RESIDUE_SPIN2_REPULSION=NO
```

A negative residue can reverse the sign but is ghost-like at the ordinary linear level.

A healthy vector can repel like charges, but only when matter carries an explicit vector current:

```text
HEALTHY_VECTOR_CAN_REPEL_LIKE_CHARGES=YES
DIRECT_VECTOR_CURRENT_MAPS_TO_009_FIFTH_FORCE_CLASS=YES
```

Thus merely adding a vector gravitational degree of freedom does not automatically solve the antigravity problem.

---

# 77. 010C — nonperturbative scalarization / nonminimal metric gate

The constant-density spontaneous-scalarization threshold was derived as

```math
|\beta|
\frac{GM}{Rc^2}
=
\frac{\pi^2}{12}
```

For compactness $0.2$:

```text
NS_CONSTANT_DENSITY_BETA_ABS_CRIT=4.112335167121e+00
```

which correctly reproduces the order-unity neutron-star scalarization scale.

For a one-meter osmium sphere:

```text
OS_R_1P0_M_COMPACTNESS=7.026987128408e-23
OS_R_1P0_M_BETA_ABS_CRIT=1.170440500879e+22
ONE_METER_OSMIUM_VS_NS_BETA_RATIO=2.846170006367e+21
```

Therefore standard self-gravity-driven scalarization is a compact-object mechanism, not a plausible laboratory-material phase transition.

The same gate showed, within the stated general conformal scalar-tensor form and healthy sign conditions:

```text
NEGATIVE_EFFECTIVE_G_SAMPLE_COUNT=0
HEALTHY_CONFORMAL_SCALAR_TENSOR_GCAV_NEGATIVE=NO
```

Pure static disformal coupling also did not provide a leading classical static force.

---

# 78. 010D — equivalence principle / center-of-energy gate

Define

```math
\chi
=
\frac{m_{\mathrm{passive}}}
{m_{\mathrm{inertial}}}
```

so

```math
a=\chi g
```

Then:

```text
NORMAL_FREE_FALL_CHI=1
WEIGHT_CANCELLATION_CHI=0
UPWARD_1G_FREE_FALL_CHI=-1
```

Therefore true upward $1g$ gravitational response requires

```math
\Delta\chi=-2
```

relative to ordinary matter.

The gate found:

```text
WEP_PRESERVED_INTERNAL_ENERGY_CHANGES_CHI=NO
ISOLATED_CENTER_OF_ENERGY_SELF_ACCELERATION=NO
INTERNAL_TIME_DEPENDENT_BACKGROUND_ALONE_PRODUCES_REACTIONLESS_THRUST=NO
```

Ideal photon thrust requires

```text
RADIATIVE_1G_MIN_POWER_W_PER_KG=2.939959708246e+09
```

and is ordinary reaction propulsion because momentum is exported.

Final 010D classification:

```text
WEP_PRESERVING_INTERNAL_STATE_WEIGHT_MODULATION=REJECTED
ISOLATED_INTERNAL_BACKGROUND_SELF_ACCELERATION=REJECTED_BY_TOTAL_MOMENTUM_CONSERVATION
TIME_DEPENDENT_INTERNAL_FIELD_ESCAPE=REQUIRES_MOMENTUM_EXPORT_OR_EXTERNAL_BACKGROUND
SELF_CONTAINED_PRACTICAL_ANTIGRAVITY_WITHIN_TESTED_HEALTHY_METRIC_FRAMEWORK=NOT_FOUND
PRACTICAL_ANTIGRAVITY_DEVICE=NOT_ESTABLISHED
```

---

# 79. Updated global interpretation

The project now has a substantially sharper distinction between what has been solved and what remains.

Solved at the mathematical/theoretical-construction level:

```text
CAN_LOCAL_GRAVITY_POINT_OUTWARD=YES
CAN_POSITIVE_ENERGY_PRODUCE_LOCAL_REPULSION=YES
CAN_A_FINITE_LINEARIZED_GR_SOURCE_BE_LOCALLY_CONSERVED_AND_DEC_COMPATIBLE=YES
DO_WE_HAVE_AN_EXPLICIT_CONSTRUCTION=YES
```

Not solved:

```text
DO_WE_HAVE_A_KNOWN_STABLE_MATERIAL_REALIZATION=NO
DO_WE_HAVE_PRACTICAL_ENERGY_SCALING=NO
DO_WE_HAVE_A_HEALTHY_ALLOWED_ORDER_1G_NEW_FORCE=NO
DO_WE_HAVE_SWITCHABLE_NEGATIVE_PASSIVE_GRAVITATIONAL_RESPONSE=NO
DO_WE_HAVE_SELF_CONTAINED_PRACTICAL_ANTIGRAVITY=NO
```

The central project sentence should therefore remain:

> **We have a mathematical construction for antigravity-like gravitational repulsion.**

and the immediate caveat should remain:

> **We have not yet established a practical antigravity device or a physically realizable human-scale source.**

---

# 80. Current theory-side frontier

Do not restart:

- classical order-unity coefficient tuning;
- free-EM quantum negative-energy work;
- rejected chameleon variants;
- ordinary unscreened scalar/vector fifth-force variants;
- simple gold-null vector completions;
- standard universal scalar-tensor sign-reversal searches.

The highest-value theoretical question is now:

> **Is there any physically consistent mechanism that changes the practical scaling or the gravitational response itself without requiring ghosts, forbidden material charges, pathological UV structure, astronomical energy, or violation of total energy-momentum conservation?**

Potential surviving logical classes include:

```text
PHYSICALLY_REALIZABLE_RELATIVISTIC_TENSION_WITH_NEW_SCALING
OBSERVATIONALLY_VIABLE_NONSTANDARD_GRAVITATIONAL_RESPONSE
CONTROLLABLE_EXTERNAL_GRAVITATIONAL_BACKGROUND_COUPLING
GENUINELY_NEW_STATE_DEPENDENT_PASSIVE_GRAVITATIONAL_RESPONSE
```

None is established.

The next research slice should continue to maximize information gain and should not be described as an experimental-design phase unless explicitly chosen.

### END NOTE - AUGUST 28 2026 - POST-010D FRONTIER UPDATE

---

# ANTIGRAVITY_RESEARCH — Comprehensive Session Carry-Forward Notes

**Session date:** August 28, 2026  
**Session scope:** Post-009N global rerank through 010D, plus README/NOTES claim consolidation  
**Repository:** `ANTIGRAVITY_RESEARCH`  
**Purpose of this document:** Preserve the complete scientific, mathematical, computational, strategic, and documentation state reached in this session so that the next session can resume without re-deriving solved work or reopening rejected branches.

---

# 0. Executive Summary

The most important project-level result was clarified and promoted to the primary public-facing statement:

> # **We have a mathematical construction for antigravity-like gravitational repulsion.**

The exact meaning of that statement is:

> **Within static linearized general relativity, the project has constructed a finite-radius, finite-thickness, nonsingular, positive-energy, locally conserved stress-energy distribution satisfying NEC, WEC, and DEC that produces a locally outward gravitational field while retaining positive far-field active mass.**

This is a **constructive linearized-GR stress-energy result**.

It is **not** a proof that practical antigravity has been solved.

The correct claim ledger remains:

```text
MATHEMATICAL_LOCAL_REPULSION=ESTABLISHED
FINITE_POSITIVE_ENERGY_LINEARIZED_GR_CONSTRUCTION=ESTABLISHED
LOCAL_CONSERVATION_LINEARIZED_ORDER=ESTABLISHED
NEC_WEC_DEC=PASS
OUTWARD_LOCAL_GRAVITATIONAL_FIELD=ESTABLISHED
POSITIVE_FAR_FIELD_ACTIVE_MASS=ESTABLISHED

EXACT_NONLINEAR_GR_REALIZATION=NOT_ESTABLISHED
DYNAMIC_STABILITY=NOT_ESTABLISHED
KNOWN_MATERIAL_REALIZATION=NO
ENERGETIC_PRACTICALITY=NO
SWITCHABLE_NEGATIVE_PASSIVE_GRAVITATIONAL_RESPONSE=NOT_ESTABLISHED
SELF_CONTAINED_PRACTICAL_ANTIGRAVITY=NOT_ESTABLISHED
PRACTICAL_ANTIGRAVITY_DEVICE=NO
NEW_PHYSICS_DISCOVERY=NO
```

The second major achievement of the session was the **aggressive narrowing of the practical search space**.

The session tested and strongly constrained or rejected, within stated scopes:

- ordinary unscreened opposite-sign scalar fifth forces at useful acceleration;
- simple effective-$Z'$ ultraviolet completions of the gold-null vector idea;
- $SU(2)_L$-preserving pure-vector isospin splitting;
- universal healthy canonical scalar-tensor sign reversal;
- metric $f(R)$ sign reversal;
- standard screening as a sign-reversal mechanism;
- healthy weak-field positive-residue spin-2 repulsion;
- viable Einstein-æther Newtonian sign reversal;
- laboratory spontaneous scalarization of ordinary-density matter;
- healthy general conformal scalar-tensor negative $G_{\mathrm{Cav}}$;
- static pure-disformal lift at leading classical order;
- self-contained reciprocal fifth-force multilayer lift;
- WEP-preserving internal-state weight modulation;
- self-contained center-of-energy acceleration from internal time-dependent fields.

The session therefore moved the project from:

```text
"Which candidate antigravity mechanism should we try?"
```

toward the much narrower question:

```text
"What physically consistent new mechanism can change the practical
stress-energy scaling or the gravitational response itself without
ghosts, pathological UV structure, already-excluded fifth forces,
astronomical energy, or violation of total energy-momentum conservation?"
```

The user explicitly stated near the end of the session that **experimental design should not be the next focus yet**. The next session should therefore remain theory-side unless that instruction changes.

---

# 1. Repository and Regression Baseline at Session Start

The session began by verifying that the permanent codebase was healthy before opening the new theoretical frontier.

The working tree was:

```text
 M NOTES.MD
?? results/data/008a_wall_current_loop_gate.csv
?? results/data/008b_distributed_field_representability_gate.csv
?? results/logs/008a_wall_current_loop_gate.log
?? results/logs/008b_distributed_field_representability_gate.log
?? simulations/008a_wall_current_loop_gate.py
?? simulations/008b_distributed_field_representability_gate.py
?? src/antigravity_research/geometry/canonical_scalar_representability.py
?? src/antigravity_research/geometry/charged_scalar_stability.py
?? src/antigravity_research/geometry/wall_current_loop.py
?? tests/known_solutions/test_006c_006d_regressions.py
?? tests/known_solutions/test_canonical_scalar_representability.py
?? tests/known_solutions/test_wall_current_loop.py
```

This matched the expected post-008B / partial-008C state.

The known-solution regression suite was run:

```text
.............................................................................................. [100%]
94 passed in 4.42s

TEST_RC=0
```

Therefore:

```text
KNOWN_SOLUTION_BASELINE=94_PASSED
REPOSITORY_BLOCKING_REGRESSION=NO
ACTIVE_FRONTIER=009O_OPPOSITE_SIGN_SCALAR_STELLAR_HALFSPACE_GATE
PERMANENT_009O_CODE_WRITTEN=NO
```

The codebundle snapshot used during this session reported:

```text
Generated: 2026-08-28 00:35:43 CDT
Branch: main
HEAD: ab66e27113686b5cad3dfcbb227c6ee3d53b8265
Working tree: DIRTY_OR_UNTRACKED
```

The 009O through 010D calculations were intentionally run as **disposable analytical/literature gates** and were not landed as permanent simulation files.

This matters for the next session:

```text
DO_NOT_ASSUME_009O_TO_010D_EXIST_AS_REPOSITORY_PY_FILES
```

Their authoritative record is the session notes / conversation until they are deliberately promoted to permanent code.

---

# 2. Starting Scientific Frontier: Post-009N Global Rerank

The prior session had ended at 009N.

The gold-null low-energy vector target was:

```text
Q_PROTON=-1.493670886075949
Q_NEUTRON=1.000000000000000
VECTOR_U=-1.329113924050633
VECTOR_D=1.164556962025316
VECTOR_ISOVECTOR_SPLITTING=-2.493670886075949
```

The key 009N conclusion was:

```text
PURE_VECTOR_LEPTOPHOBIC_ISOSPIN_CURRENT_IS_ELECTROWEAK_CONSERVED=NO
SIMPLE_ONE_HIGGS_GOLD_NULL_VECTOR_1G_PATH=REJECTED_AT_PREFLIGHT_LEVEL
PRACTICAL_GOLD_NULL_VECTOR=NOT_ESTABLISHED
```

The active rerank was therefore:

```text
NEXT=GLOBAL_RERANK_OPPOSITE_SIGN_SCALAR_FORCE_VS_EXOTIC_EW_COMPENSATED_VECTOR
```

The two principal candidate branches entering this session were:

1. opposite-sign scalar force;
2. exotic electroweak-compensated vector.

The scalar was attractive as a fresh branch because a scalar interaction does not require a conserved vector current and therefore does not automatically inherit the specific longitudinal-current obstruction that killed the simple 009N vector.

---

# 3. 009O Preliminary Scalar Sign Analysis

## 3.1 Low-energy scalar charge algebra

For proton and neutron scalar couplings $g_p$ and $g_n$, define the nuclear scalar charge per nucleon for a nucleus $(A,Z)$:

```math
s_{A,Z}
=
\frac{
Zg_p+(A-Z)g_n
}{A}
```

For scalar exchange between sources with scalar charges $Q_1$ and $Q_2$, the Yukawa potential is

```math
V_{12}(r)
=
-\frac{\hbar c}{4\pi}
\frac{Q_1Q_2}{r}
e^{-r/\lambda}
```

Therefore:

```text
Q1*Q2 > 0  -> attraction
Q1*Q2 < 0  -> repulsion
```

Thus opposite-sign scalar charges for two ordinary materials are sufficient for a repulsive scalar fifth force.

This survived at the low-energy EFT level.

## 3.2 Gold-null scalar direction

The gold-blind nucleon direction satisfies

```math
79g_p+118g_n=0
```

so

```math
\frac{g_p}{g_n}
=
-\frac{118}{79}
=
-1.493670886075949
```

Examples:

For carbon-12,

```math
\frac{s_{\mathrm{C}}}{g_n}
=
-0.24683544303797467
```

For osmium-192,

```math
\frac{s_{\mathrm{Os}}}{g_n}
=
0.01292194092827007
```

The signs differ, so stable ordinary nuclei can carry opposite effective scalar charge in a low-energy EFT.

This was classified as:

```text
SCALAR_OPPOSITE_SIGN_CHARGE=YES_AT_LOW_ENERGY_EFT_LEVEL
GAUGE_INVARIANT_OPERATOR_AVAILABLE=YES
TECHNICALLY_NATURAL_UV_COMPLETION=NOT_ESTABLISHED
EXPERIMENTALLY_ALLOWED_USEFUL_STRENGTH=NOT_ESTABLISHED
PRACTICAL_ANTIGRAVITY=NO
```

## 3.3 Gauge-invariant scalar operator

A representative electroweak-gauge-invariant operator structure was noted:

```math
\mathcal{L}_{\mathrm{eff}}
\supset
-\frac{\phi}{\Lambda}
\left[
c_u\bar Q_L\widetilde H u_R
+
c_d\bar Q_LH d_R
\right]
+
\mathrm{h.c.}
```

After electroweak symmetry breaking this permits independent effective scalar couplings to up and down quarks, including opposite signs.

The important point is limited:

```text
ELECTROWEAK_GAUGE_INVARIANCE_OF_AN_EFFECTIVE_OPERATOR=YES
FULL_HEALTHY_UV_COMPLETION=NOT_PROVED
```

---

# 4. New 2025 Neutron-Star Cooling Constraint Used in 009O

A major literature input in this session was:

**Fiorillo, Lella, O'Hare, Vitagliano, "Leading Bounds on Micrometer to Picometer Fifth Forces from Neutron Star Cooling," Phys. Rev. Lett. 135, 211003 (2025), arXiv:2506.19906.**

The published equal-nucleon-coupling scale used for the preflight was approximately:

```math
g_N
\lesssim
5\times10^{-14}
```

for sufficiently light scalars, including the $\sim1.76\ {\mathrm{eV}}$ mediator relevant to the $112\ {\mathrm{nm}}$ benchmark.

The paper's more important feature for this project was its treatment of unequal proton and neutron couplings.

Define

```math
g
=
\frac{g_p+g_n}{2}
```

and

```math
\delta g
=
\frac{g_n-g_p}{2}
```

The neutron-proton bremsstrahlung contribution contains a structure of the form

```math
Q_{np}^{S}
\propto
\delta g^2
+
\frac{p_n^2}{5m_N^2}
g^2
```

within the nuclear model used in the supplemental analysis.

This is crucial.

For an isospin-violating scalar with $g_p$ and $g_n$ of opposite sign:

```math
|\delta g|
```

is generally large.

The $\delta g^2$ term is less velocity-suppressed than the equal-coupling $g^2$ contribution.

Therefore:

> **The isospin violation needed to make ordinary materials carry opposite scalar charges also tends to enhance neutron-star scalar emission rather than creating a stellar blind direction.**

This transformed the scalar branch from an attractive loophole into a strongly constrained candidate.

Important limitation:

```text
PUBLISHED_5E-14_CURVE_IS_FOR_EQUAL_GP_GN=YES
DIRECT_APPLICATION_TO_ARBITRARY_GP_GN=NO
```

The project therefore used it only as a **literature-normalized preflight**, not as a formally published arbitrary-isospin exclusion.

---

# 5. Scalar Infinite-Half-Space Force Formula

For a scalar source with density $\rho$, range $\lambda$, source specific scalar charge $s_{\mathrm{src}}$, test specific scalar charge $s_{\mathrm{test}}$, stand-off $z$, and a sufficiently thick half-space, the project derived:

```math
a_{\mathrm{half}}
=
\frac{\hbar c}{2m_u^2}
\rho\lambda
|s_{\mathrm{src}}s_{\mathrm{test}}|
e^{-z/\lambda}
```

For finite source thickness $T$, multiply by:

```math
1-e^{-T/\lambda}
```

The expression passes dimensional analysis.

In the universal-charge limit it maps to the standard Yukawa half-space form:

```math
a_{\mathrm{half}}
=
2\pi G\rho\alpha\lambda
```

up to the corresponding conversion between microscopic coupling and Yukawa strength.

This half-space configuration is intentionally optimistic:

```text
INFINITE_LATERAL_SOURCE=YES
THICK_SOURCE=YES
ZERO_GAP_ALLOWED=YES
FINITE_ENGINEERING_GEOMETRY_CAN_ONLY_BE_WORSE_AT_FIXED_PARAMETERS=YES
```

Therefore a failed half-space ceiling is a strong branch-killing result.

---

# 6. 009O-A — Opposite-Sign Scalar Stellar / Half-Space Preflight

The actual disposable calculation then combined:

- the Fiorillo et al. $nn$, $pp$, and $np$ bremsstrahlung structure;
- a broad neutron-star state scan;
- arbitrary $g_p/g_n$;
- an optimistic dense source;
- a very proton-rich test body;
- zero gap;
- infinite source thickness.

## 6.1 Geometry and mediator benchmark

```text
LAMBDA_NM=112.206000
M_PHI_EV=1.758613446696
PUBLISHED_EQUAL_COUPLING_LIMIT=5.000000e-14
SOURCE=OSMIUM_192_OPTIMISTIC_HALF_SPACE
TEST=HYDROGEN_1
CONTACT_GAP=ZERO_OPTIMISTIC
SOURCE_THICKNESS=INFINITE_OPTIMISTIC
```

Hydrogen was chosen over carbon because its proton fraction provides a larger opposite-sign material lever arm.

## 6.2 Scan size

```text
SCENARIO_COUNT=630000
```

The scan varied:

- temperature;
- neutron Fermi momentum;
- proton fraction;
- coupling ratio $g_p/g_n$.

## 6.3 Best point

The best result found was:

```text
BEST_GP_OVER_GN=-0.712781680480
BEST_ALLOWED_GN=4.641510896240e-14
BEST_GN_SCALE_SQ_VS_EQUAL_LIMIT=8.617449359966e-01
BEST_TEMP_KEV=1.500
BEST_PFN_MEV=500.000
BEST_PROTON_FRACTION=0.010000
BEST_EQUAL_QNN_OVER_QNP=7.345296251215e+01
BEST_EQUAL_QPP_OVER_QNP=1.356792606499e-02
BEST_CANDIDATE_NP_FACTOR_OVER_EQUAL_NP=1.295380017415e+01
BEST_SOURCE_CHARGE_OVER_GN=3.220239181433e-01
BEST_TEST_CHARGE_OVER_GN=-7.127816804801e-01
```

The force ceiling was:

```text
BEST_CONTACT_A_OVER_G=7.327295675071e-04
```

or

```math
\frac{a_{\mathrm{scalar,max}}}{g}
\approx
7.33\times10^{-4}
```

for this deliberately optimistic preflight.

## 6.4 Comparison with project targets

The earlier 009G optimistic unscreened vector ceiling was:

```text
VECTOR_009G_CEILING_A_OVER_G=2.200000000000e-02
```

The scalar result therefore missed the vector by:

```text
MARGIN_TO_009G=3.002471986336e+01
```

approximately a factor of $30$ in acceleration.

The scalar missed the $0.1g$ practical-screening threshold by:

```text
MARGIN_TO_0P1G=1.364759993789e+02
```

approximately a factor of $136.5$.

The preflight decision was:

```text
SCALAR_BEATS_009G_VECTOR_CEILING=NO
SCALAR_REACHES_0P1G=NO
009O_A_PREFLIGHT_DECISION=UNSCREENED_OPPOSITE_SIGN_SCALAR_STRONGLY_DISFAVORED
```

## 6.5 Correct claim classification

This was explicitly **not** a full NSCool likelihood recast:

```text
CLAIM_CLASSIFICATION=ANALYTIC_LITERATURE_NORMALIZED_PREFLIGHT
FULL_NSCOOL_LIKELIHOOD_RECAST=NO
FINITE_GEOMETRY_INCLUDED=NO
LAB_COMPOSITION_SPECIFIC_RECAST=NO
PRACTICAL_ANTIGRAVITY_DEVICE=NO
```

The correct interpretation is:

> **Ordinary unscreened opposite-sign scalar fifth forces lost global priority because even an optimistic half-space benchmark remains far below useful acceleration after neutron-star normalization.**

Do not state:

```text
ALL_SCALAR_THEORIES_EXCLUDED
```

because screened, environment-dependent, nonlinear, or qualitatively different scalar models were not all covered.

---

# 7. Global Rerank After 009O

After 009O, the scalar branch no longer justified the highest priority.

The rerank became:

1. **009L-style material-blind / gold-null vector**
   - only low-energy fifth-force branch found to formally cross order-$1g$;
   - UV completion not established;
   - simple realizations already stressed.

2. **Exotic electroweak-compensated vector**
   - high theoretical burden;
   - required explicit UV completion.

3. **Environment-dependent / remote-background mechanisms**
   - still logically open;
   - no demonstrated practical route.

4. **Classical GR**
   - retained as rigorous reference result;
   - not engineering priority without new parametric scaling.

A new practical distinction also became central:

```text
GROUND_REFERENCED_FORCE
!=
SELF_CONTAINED_FREE_FLIGHT
```

This distinction drove 009P and later 010D.

---

# 8. 009P — Effective-$Z'$ UV / Momentum-Conservation Practicality Gate

## 8.1 Motivation

The 009L phenomenological force direction remained interesting because its low-energy recast could reach approximately order-$1g$.

However, 009N showed that a naive pure-vector isovector quark current is not electroweak-conserved above EWSB.

A published loophole exists in **effective-$Z'$** models:

- Standard Model fermions need not carry fundamental $U(1)'$ charge;
- anomaly-free vectorlike fermions can mix with SM fermions;
- low-energy $Z'$ couplings arise effectively.

The session used the relation associated with this construction:

```math
g_{\mathrm{eff}}
=
g'\sin^2\theta
```

and

```math
M_Q
=
\frac{y}{\sqrt2}
\frac{M_X}
{\sqrt{g'g_{\mathrm{eff}}}}
```

Since

```math
g'\ge g_{\mathrm{eff}}
```

one obtains the optimistic ceiling:

```math
M_Q
\le
\frac{y}{\sqrt2}
\frac{M_X}{g_{\mathrm{eff}}}
```

This is a very cheap UV consistency test.

## 8.2 Low-energy target

```text
M_X_EV=1.758613446696
G_X_AT_1G=8.538070000000e-12
V_U=-1.329113924050633
V_D=1.164556962025316
ISOVECTOR_SPLITTING=-2.493670886075949
```

The effective quark couplings at $1g$ were:

```text
ABS_G_U=1.134806772152e-11
ABS_G_D=9.943068860759e-12
```

## 8.3 1g partner ceilings

For $y=1$:

```text
UP_PARTNER_MAX_GEV=109.580549
DOWN_PARTNER_MAX_GEV=125.064757
```

For the perturbative benchmark $y=\sqrt{4\pi}$:

```text
UP_PARTNER_MAX_GEV=388.452933
DOWN_PARTNER_MAX_GEV=443.343021
```

For the deliberately extreme $y=4\pi$ benchmark:

```text
UP_PARTNER_MAX_GEV=1377.029794
DOWN_PARTNER_MAX_GEV=1571.610091
```

Required Yukawa values for selected target masses:

```text
Y_REQUIRED_UP_FOR_500GEV=4.562853567580
Y_REQUIRED_DOWN_FOR_500GEV=3.997928840165

Y_REQUIRED_UP_FOR_845GEV=7.711222529209
Y_REQUIRED_DOWN_FOR_845GEV=6.756499739879

Y_REQUIRED_UP_FOR_1500GEV=13.688560702739
Y_REQUIRED_DOWN_FOR_1500GEV=11.993786520495
```

## 8.4 2g benchmark

```text
G_X=1.207465439049e-11

Y_SQRT_4PI_UP_PARTNER_MAX_GEV=274.677703
Y_SQRT_4PI_DOWN_PARTNER_MAX_GEV=313.490857

Y_EQ_4PI_EXTREME_UP_PARTNER_MAX_GEV=973.707105
Y_EQ_4PI_EXTREME_DOWN_PARTNER_MAX_GEV=1111.296153
```

## 8.5 6g benchmark

```text
G_X=2.091391488816e-11

Y_SQRT_4PI_UP_PARTNER_MAX_GEV=158.585246
Y_SQRT_4PI_DOWN_PARTNER_MAX_GEV=180.994031

Y_EQ_4PI_EXTREME_UP_PARTNER_MAX_GEV=562.170059
Y_EQ_4PI_EXTREME_DOWN_PARTNER_MAX_GEV=641.607133
```

## 8.6 10g benchmark

```text
G_X=2.699974802195e-11

Y_SQRT_4PI_UP_PARTNER_MAX_GEV=122.839603
Y_SQRT_4PI_DOWN_PARTNER_MAX_GEV=140.197373

Y_EQ_4PI_EXTREME_UP_PARTNER_MAX_GEV=435.455055
Y_EQ_4PI_EXTREME_DOWN_PARTNER_MAX_GEV=496.986748
```

The practical pattern is clear:

```text
MORE_REQUIRED_FORCE
-> LARGER_EFFECTIVE_COUPLING
-> LOWER_ALLOWED_VECTORLIKE_PARTNER_MASS
-> STRONGER_COLLIDER/UV_TENSION
```

## 8.7 Momentum-conservation gate

009P also made a critical device-level correction.

For two internal subsystems:

```math
\mathbf{F}_{12}
=
-\mathbf{F}_{21}
```

so:

```math
\mathbf{F}_{12}
+
\mathbf{F}_{21}
=
0
```

Including field momentum does not rescue an isolated device.

Therefore:

```text
PAIR_FORCE_SUM=F12_PLUS_F21=0
SELF_CONTAINED_STATIC_FIFTH_FORCE_COM_ACCELERATION=0
SELF_CONTAINED_MULTILAYER_FIFTH_FORCE_LIFT=REJECTED
GROUND_REFERENCED_EXTERNAL_SOURCE_LEVITATION=NOT_REJECTED_BY_THIS_ARGUMENT
```

This is one of the most important conceptual results of the session.

It means:

> **A short-range reciprocal fifth force can potentially push a payload relative to an external source, but internal fifth-force layers cannot create self-contained center-of-mass lift.**

This prevents future work from confusing a force actuator with reactionless gravitational propulsion.

## 8.8 009P classification

```text
SIMPLE_EFFECTIVE_ZPRIME_UV_1G=SEVERELY_COLLIDER_STRESSED
SIMPLE_EFFECTIVE_ZPRIME_UV_MULTI_G=MORE_SEVERELY_STRESSED
ALL_EFFECTIVE_ZPRIME_UV_COMPLETIONS_EXCLUDED=NO
EXOTIC_DECAY_COLLIDER_RECAST_REQUIRED=YES
EW_ISOSPIN_COMPENSATION_REQUIRED=YES
GROUND_REFERENCED_009L_FORCE=PHENOMENOLOGICALLY_UNRESOLVED
SELF_CONTAINED_009L_MULTILAYER_ANTIGRAVITY=REJECTED_BY_MOMENTUM_CONSERVATION
PRACTICAL_ANTIGRAVITY_DEVICE=NOT_ESTABLISHED
```

---

# 9. 009Q — Electroweak Dichotomy / Effective-$Z'$ UV-Scale Gate

009Q sharpened the vector problem into a two-branch field-theory dichotomy.

---

## 9.1 Branch A — Preserve $SU(2)_L$ equality of left-handed currents

Let the desired low-energy vector coefficients be:

```math
v_u=-1.329113924050633
```

and

```math
v_d=1.164556962025316
```

For a Dirac quark:

```math
v
=
\frac{g_L+g_R}{2}
```

and

```math
a
=
\frac{g_R-g_L}{2}
```

If electroweak symmetry requires:

```math
g_L^u=g_L^d=L
```

then:

```math
a_u=v_u-L
```

```math
a_d=v_d-L
```

The minimax choice is:

```math
L
=
\frac{v_u+v_d}{2}
```

which gives:

```math
|a|_{\min}
=
\frac{|v_u-v_d|}{2}
```

Numerically:

```text
COMMON_LEFT_OPTIMUM=-0.082278481012659
AXIAL_U_COEFF=-1.246835443037975
AXIAL_D_COEFF=1.246835443037975
UNAVOIDABLE_AXIAL_FLOOR_COEFF=1.246835443037975
UNAVOIDABLE_AXIAL_COUPLING_AT_1G=1.064556829114e-11
SU2L_PRESERVING_PURE_VECTOR_POSSIBLE=NO
```

This route returns directly to the axial / nonconserved-current / longitudinal-mode problem already exposed in 009N:

```text
BRANCH_A_STATUS=RETURNS_TO_009N_AXIAL_LONGITUDINAL_OBSTRUCTION
```

Thus:

> **Preserving ordinary $SU(2)_L$ structure prevents the required gold-null force from remaining purely vector.**

---

## 9.2 Branch B — Split $u_L$ and $d_L$ after electroweak symmetry breaking

Published effective-$Z'$ constructions show that explicit left-handed isospin splitting can be generated by Higgs-inserted higher-dimensional structure.

The session modeled the relevant scale schematically as:

```math
\frac{C}{\Lambda^4}
\left(
\bar q\gamma_\mu q
\right)
\left(
\phi^\ast D^\mu\phi
\right)
\left(
H^\ast H
\right)
```

After symmetry breaking:

```math
g_{\mathrm{eff}}
\sim
\frac{
C g' v_\phi^2v_H^2
}{
\Lambda^4
}
```

with:

```math
M_X
=
\sqrt2\,g'v_\phi
```

giving:

```math
\Lambda^4
\sim
\frac{
C M_X^2v_H^2
}{
2g'g_{\mathrm{eff}}
}
```

under the adopted convention.

The most optimistic minimum gauge coupling was taken as:

```text
ASSUMED_GPRIME_MIN=1.134806772152e-11
```

which gave:

```text
VPHI_MAX_GEV=109.580549
```

So even the new symmetry-breaking scale is tied to the electroweak scale rather than decoupling arbitrarily high.

## 9.3 Dimension-eight cutoff preflight

For $C=1$:

```text
C_EQ_1_LAMBDA_U_MAX_GEV=164.185307
C_EQ_1_LAMBDA_D_MAX_GEV=169.701100
```

For $C=4\pi$:

```text
C_EQ_4PI_LAMBDA_U_MAX_GEV=309.126870
C_EQ_4PI_LAMBDA_D_MAX_GEV=319.511963
```

For the extreme strong-NDA choice $C=(4\pi)^2$:

```text
C_EQ_4PI_SQUARED_LAMBDA_U_MAX_GEV=582.021760
C_EQ_4PI_SQUARED_LAMBDA_D_MAX_GEV=601.574737
```

Therefore the pure-vector isospin-splitting UV sector does **not** naturally decouple to very high scales.

---

## 9.4 Portal mixing at $y=\sqrt{4\pi}$

Absolute mass ceilings:

```text
UP_PARTNER_ABSOLUTE_MAX_GEV=388.452933
DOWN_PARTNER_ABSOLUTE_MAX_GEV=443.343021
```

Required $\sin^2\theta$:

| Partner mass | Up-type $\sin^2\theta$ | Physical? | Down-type $\sin^2\theta$ | Physical? |
|---:|---:|:---:|---:|:---:|
| 500 GeV | 1.656773727124 | NO | 1.271921344796 | NO |
| 845 GeV | 4.731911442039 | NO | 3.632734552872 | NO |
| 1200 GeV | 9.543016668234 | NO | 7.326266946026 | NO |
| 1500 GeV | 14.91096354412 | NO | 11.44729210317 | NO |
| 1530 GeV | 15.51336647130 | NO | 11.90976270413 | NO |
| 1700 GeV | 19.15230428555 | NO | 14.70341074584 | NO |

Thus the simple perturbative portal cannot support even a $500\ {\mathrm{GeV}}$ partner at the required $1g$ couplings.

---

## 9.5 Portal mixing at extreme $y=4\pi$

Absolute mass ceilings:

```text
UP_PARTNER_ABSOLUTE_MAX_GEV=1377.029794
DOWN_PARTNER_ABSOLUTE_MAX_GEV=1571.610091
```

Required $\sin^2\theta$:

| Partner mass | Up-type $\sin^2\theta$ | Physical? | Down-type $\sin^2\theta$ | Physical? |
|---:|---:|:---:|---:|:---:|
| 500 GeV | 0.1318418641283 | YES | 0.1012162846242 | YES |
| 845 GeV | 0.3765535481368 | YES | 0.2890838305152 | YES |
| 1200 GeV | 0.7594091373789 | YES | 0.5830057994354 | YES |
| 1500 GeV | 1.186576777155 | NO | 0.9109465616178 | YES |
| 1530 GeV | 1.234514478952 | NO | 0.9477488027072 | YES |
| 1700 GeV | 1.524091949323 | NO | 1.170060250256 | NO |

The decisive line was:

```text
EXTREME_4PI_1500_UP_SIN2=1.186576777155e+00
EXTREME_4PI_1500_DOWN_SIN2=9.109465616178e-01
EXTREME_4PI_1500_BOTH_PARTNERS_PHYSICAL=NO
```

## 9.6 009Q decision

```text
SU2L_PRESERVING_BRANCH=REJECTED_BY_EXISTING_009N_OBSTRUCTION
PURE_VECTOR_ISOSPIN_BRANCH_REQUIRES_DIM8_EWSB=YES
DECOUPLED_MULTI_TEV_PERTURBATIVE_UV=NO_IN_SIMPLE_EFFECTIVE_ZPRIME_REALIZATION
CURRENT_STANDARD_DECAY_VLQ_LIMIT_DIRECTLY_APPLICABLE=NO_MODEL_SPECIFIC_BRANCHING_RECAST_REQUIRED
EXACT_EW_PRECISION_FIT_DONE=NO
EXACT_EXOTIC_Q_TO_qZPRIME_COLLIDER_RECAST_DONE=NO
ALL_EXOTIC_EW_COMPENSATED_VECTORS_EXCLUDED=NO
GROUND_REFERENCED_1G_VECTOR_DEVICE_ESTABLISHED=NO
SELF_CONTAINED_FREE_FLIGHT_DEVICE_ESTABLISHED=NO
009Q_DECISION=EXOTIC_EW_COMPENSATED_VECTOR_SEVERELY_STRESSED_NOT_YET_CLOSED
```

The correct strategic interpretation was:

> **Do not spend large effort on collider simulation unless an explicit, internally coherent UV Lagrangian survives the cheaper field-theory gates.**

The simple effective-$Z'$ rescue became low priority.

---

# 10. Strategic Pivot: From Fifth Forces to True Gravitational Response

After 009Q, a deeper point became decisive.

Even if the gold-null vector were miraculously UV-completed:

```text
it would still be a reciprocal short-range fifth force
```

and therefore:

```text
it would not provide isolated center-of-mass acceleration
```

through internal multilayer construction.

Therefore the search was reranked toward theories that might change the **gravitational response itself** rather than merely adding another force.

The next question became:

> **Can healthy modified gravity produce a local sign reversal or order-unity suppression of ordinary neutral matter's gravitational response without an explicit new material charge?**

---

# 11. 010A — Healthy Universal Scalar-Tensor Sign Gate

## 11.1 Model

Consider Einstein-frame scalar-tensor gravity:

```math
S
=
\int d^4x\sqrt{-g}
\left[
\frac{M_{\mathrm{Pl}}^2}{2}R
-
\frac12(\partial\phi)^2
-
V(\phi)
\right]
+
S_m[A^2(\phi)g_{\mu\nu},\psi]
```

Define a scalar coupling:

```math
\alpha_A
=
M_{\mathrm{Pl}}
\frac{\partial\ln m_A}
{\partial\phi}
```

The weak-field interaction has the form:

```math
V(r)
=
-\frac{Gm_Am_B}{r}
\left[
1+
2\alpha_A\alpha_B
e^{-r/\lambda}
\right]
```

and the corresponding force ratio can be written:

```math
\frac{F}{F_{\mathrm{GR}}}
=
1+
2\alpha_A\alpha_B
\left(
1+\frac{r}{\lambda}
\right)
e^{-r/\lambda}
```

For universally coupled identical ordinary matter:

```math
\alpha_A=\alpha_B=\alpha
```

so:

```math
\alpha_A\alpha_B=\alpha^2\ge0
```

therefore:

```math
\frac{F}{F_{\mathrm{GR}}}
\ge1
```

for a healthy canonical scalar.

That is the key sign theorem used in 010A.

---

## 11.2 Generic numerical sign scan

The scan returned:

```text
MIN_UNIVERSAL_CANONICAL_F_OVER_FGR=1.000000000000000e+00
UNIVERSAL_CANONICAL_SCALAR_REPULSION=NO
UNIVERSAL_CANONICAL_SCALAR_CAN_ONLY_ENHANCE_OR_APPROACH_GR=YES
```

---

## 11.3 Metric $f(R)$ benchmark

For metric $f(R)$:

```math
\alpha
=
\frac{1}{\sqrt6}
```

so the short-range unscreened force becomes:

```math
\frac{F}{F_{\mathrm{GR}}}
\to
\frac43
```

The numerical check gave:

```text
FR_X_0_F_OVER_FGR=1.333333333333333e+00
FR_X_0.1_F_OVER_FGR=1.331773719946518e+00
FR_X_1_F_OVER_FGR=1.245252960780962e+00
FR_X_10_F_OVER_FGR=1.000166466409129e+00
FR_X_100_F_OVER_FGR=1.000000000000000e+00
FR_REPULSIVE_BRANCH=NO
```

Thus ordinary metric $f(R)$ strengthens attraction in the unscreened regime rather than reversing it.

---

## 11.4 Screening

The screen-factor test gave:

```text
SCREENING_1.000e+00_F_OVER_FGR=3.000000000000000e+00
SCREENING_5.000e-01_F_OVER_FGR=1.500000000000000e+00
SCREENING_1.000e-01_F_OVER_FGR=1.020000000000000e+00
SCREENING_1.000e-03_F_OVER_FGR=1.000002000000000e+00
SCREENING_0.000e+00_F_OVER_FGR=1.000000000000000e+00
```

Therefore:

```text
SCREENING_CAN_SUPPRESS_EXTRA_FORCE=YES
SCREENING_FLIPS_UNIVERSAL_FORCE_SIGN=NO
```

---

## 11.5 Opposite-charge scalar escape

Using:

```text
ALPHA_A=1
ALPHA_B=-1
```

gave:

```text
CONTACT_F_OVER_FGR=-1
OPPOSITE_CHARGES_CAN_REPEL=YES
```

But this is not universal metric gravity:

```text
OPPOSITE_CHARGE_ROUTE_IS_UNIVERSAL_METRIC_GRAVITY=NO
OPPOSITE_CHARGE_ROUTE_MAPS_TO_009O_STYLE_PHYSICS=YES
```

So the escape simply returns to the fifth-force branch already strongly constrained in 009O.

---

## 11.6 Ghost escape

A wrong-sign scalar kinetic term reverses the sign of the exchange contribution.

The contact reversal threshold was:

```math
\alpha
=
\frac{1}{\sqrt2}
```

The scan gave:

```text
GHOST_ALPHA_0.500000_F_OVER_FGR=0.5
GHOST_ALPHA_0.707107_F_OVER_FGR≈0
GHOST_ALPHA_1.000000_F_OVER_FGR=-1
GHOST_ALPHA_2.000000_F_OVER_FGR=-7
```

Therefore:

```text
GHOST_CAN_REVERSE_SIGN=YES
GHOST_KINETIC_ENERGY_POSITIVE=NO
GHOST_ROUTE_PHYSICALLY_ACCEPTABLE=NO
```

---

## 11.7 010A decision

```text
HEALTHY_UNIVERSAL_CANONICAL_SCALAR_TENSOR=REJECTED_AS_REPULSIVE_ROUTE
METRIC_F_R=REJECTED_AS_REPULSIVE_ROUTE
STANDARD_SCREENED_SCALAR_BRANCH=REJECTED_AS_SIGN_REVERSAL_ROUTE
OPPOSITE_SCALAR_CHARGE=ALREADY_COVERED_BY_009O_CLASS
WRONG_SIGN_SCALAR=REJECTED_BY_GHOST_INSTABILITY
STRONG_FIELD_SCALARIZATION=NOT_A_LAB_ORDINARY_MATTER_ROUTE
010A_GATE=GREEN
```

Remember:

```text
GATE_GREEN
```

means the **scientific decision gate executed successfully**.

It does not mean the candidate antigravity mechanism succeeded.

---

# 12. 010B — Healthy Vector-Tensor / Spin-2 Weak-Field Sign Gate

010B tested whether healthy vector-tensor or extra spin-2 gravitational modes add a genuinely new sign freedom.

---

## 12.1 Einstein-æther Newtonian sign

The published weak-field coupling used was:

```math
G_N
=
\frac{G}
{1-c_{14}/2}
```

For positive bare $G$, a sign reversal requires:

```math
c_{14}>2
```

The numerical scan gave:

```text
C14_-2.00_GN_OVER_G=5.000000000000e-01
C14_-1.00_GN_OVER_G=6.666666666667e-01
C14_0.00_GN_OVER_G=1.000000000000e+00
C14_0.50_GN_OVER_G=1.333333333333e+00
C14_1.00_GN_OVER_G=2.000000000000e+00
C14_1.50_GN_OVER_G=4.000000000000e+00
C14_1.90_GN_OVER_G=2.000000000000e+01
C14_1.99_GN_OVER_G=2.000000000000e+02
C14_2.00_GN_OVER_G=SINGULAR
C14_2.01_GN_OVER_G=-2.000000000000e+02
C14_2.10_GN_OVER_G=-2.000000000000e+01
C14_3.00_GN_OVER_G=-2.000000000000e+00
```

This shows the sign reversal occurs only after crossing the singular point.

The session also recorded the post-GW170817 scale:

```text
GW170817_C13_ABS_BOUND_APPROX=1e-15
```

The decision was:

```text
VIABLE_EINSTEIN_AETHER_NEWTONIAN_SIGN=ATTRACTIVE
EINSTEIN_AETHER_LAB_ANTIGRAVITY_ROUTE=STRONGLY_REJECTED
```

---

## 12.2 Positive-residue massive spin-2

A schematic extra-spin-2 force was modeled as:

```math
\frac{F}{F_{\mathrm{GR}}}
=
1
+
A(1+x)e^{-x}
```

with:

```math
x=\frac{r}{\lambda}
```

For healthy positive residue:

```math
A\ge0
```

the scan returned:

```text
MIN_POSITIVE_RESIDUE_F_OVER_FGR=1.000000000000000e+00
A_EQ_1_OVER_3_CONTACT_F_OVER_FGR=1.333333333333333e+00
A_EQ_1_OVER_3_X_EQ_1_F_OVER_FGR=1.245252960780961e+00
POSITIVE_RESIDUE_SPIN2_REPULSION=NO
POSITIVE_RESIDUE_SPIN2_ADDS_ATTRACTION=YES
```

Negative residues gave:

```text
NEGATIVE_RESIDUE_-0.5_CONTACT_F_OVER_FGR=0.5
NEGATIVE_RESIDUE_-1.0_CONTACT_F_OVER_FGR=0
NEGATIVE_RESIDUE_-2.0_CONTACT_F_OVER_FGR=-1
```

but:

```text
NEGATIVE_RESIDUE_HEALTHY_LINEAR_SPIN2=NO
```

Therefore:

```text
GHOST_FREE_MASSIVE_SPIN2_WEAK_FIELD_REPULSION=REJECTED
```

within the weak-field positive-residue scope.

---

## 12.3 Healthy vector exchange

A repulsive vector Yukawa contribution was written schematically:

```math
\frac{F}{F_{\mathrm{GR}}}
=
1
-
\alpha_v(1+x)e^{-x}
```

The contact values demonstrated:

```text
VECTOR_ALPHA_0.1_CONTACT_F_OVER_FGR=0.9
VECTOR_ALPHA_0.5_CONTACT_F_OVER_FGR=0.5
VECTOR_ALPHA_1.0_CONTACT_F_OVER_FGR=0
VECTOR_ALPHA_2.0_CONTACT_F_OVER_FGR=-1
VECTOR_ALPHA_10.0_CONTACT_F_OVER_FGR=-9
```

Thus:

```text
HEALTHY_VECTOR_CAN_REPEL_LIKE_CHARGES=YES
```

but:

```text
VECTOR_REPULSION_REQUIRES_MATTER_CURRENT_OR_CHARGE=YES
DIRECT_VECTOR_CURRENT_IS_PURE_METRIC_GRAVITY=NO
DIRECT_VECTOR_CURRENT_MAPS_TO_009_FIFTH_FORCE_CLASS=YES
```

This is the central classification.

A spin-1 field can certainly repel.

That does **not** automatically constitute modified gravitational response.

---

## 12.4 Generalized Proca interpretation

The session recorded:

```text
STANDARD_MINIMAL_MATTER_COUPLING_HAS_INDEPENDENT_VECTOR_CHARGE=NO
VIABLE_SOLAR_SYSTEM_GENERALIZED_PROCA_USES_VAINSHTEIN_SCREENING=YES
SCREENING_PURPOSE=SUPPRESS_EXTRA_LONGITUDINAL_FORCE
SCREENING_ALONE_ESTABLISHES_SIGN_REVERSAL=NO
ALL_GENERALIZED_PROCA_THEORIES_EXCLUDED=NO
```

---

## 12.5 010B decision

```text
EINSTEIN_AETHER_HEALTHY_NEWTONIAN_REPULSION=REJECTED
HEALTHY_POSITIVE_RESIDUE_MASSIVE_SPIN2_REPULSION=REJECTED_AT_WEAK_FIELD_LEVEL
HEALTHY_VECTOR_REPULSION=YES_BUT_REQUIRES_EXPLICIT_MATTER_CHARGE
EXPLICIT_VECTOR_CHARGE=ALREADY_COVERED_BY_009_SERIES
STANDARD_SCREENED_GENERALIZED_PROCA_SIGN_REVERSAL=NOT_ESTABLISHED
ALL_VECTOR_TENSOR_THEORIES_EXCLUDED=NO
ALL_BIGRAVITY_THEORIES_EXCLUDED=NO
WEAK_FIELD_POSITIVE_RESIDUE_UNIVERSAL_MEDIATOR_ROUTE=STRONGLY_NARROWED
010B_GATE=GREEN
```

The surviving high-level class was then phrased as:

```text
NONPERTURBATIVE_BACKGROUND_DEPENDENT_OR_NONMINIMAL_METRIC_RESPONSE
```

---

# 13. 010C — Nonperturbative Scalarization / Nonminimal Metric Sign Gate

010C tested whether a nonlinear phase transition or nonminimal metric response could create laboratory gravitational inversion.

---

## 13.1 Spontaneous scalarization onset derivation

For a DEF-type quadratic scalar coupling:

```math
A(\phi)
=
\exp
\left(
\frac{\beta\phi^2}{2}
\right)
```

linearization inside nonrelativistic matter with $\beta<0$ gives an effective tachyonic equation:

```math
\nabla^2\delta\phi
+
\mu^2\delta\phi
=
0
```

with:

```math
\mu^2
=
\frac{4\pi G|\beta|\rho}{c^2}
```

For a constant-density sphere, matching the lowest regular interior mode to the exterior solution gives the onset condition:

```math
\mu R
=
\frac{\pi}{2}
```

Using:

```math
\frac{GM}{Rc^2}
=
\frac{
4\pi G\rho R^2
}{
3c^2
}
```

gives:

```math
|\beta|
\frac{GM}{Rc^2}
=
\frac{\pi^2}{12}
```

This was an important analytical result because it reproduces the correct order of magnitude for neutron-star scalarization.

---

## 13.2 Neutron-star validation

For:

```text
NS_REFERENCE_COMPACTNESS=0.2
```

the toy threshold is:

```text
NS_CONSTANT_DENSITY_BETA_ABS_CRIT=4.112335167121e+00
```

compared with the known realistic DEF onset scale of roughly:

```text
4.35
```

Therefore:

```text
TOY_THRESHOLD_REPRODUCES_NS_ORDER_ONE_SCALE=YES
```

This validates the toy expression as a useful compactness preflight.

---

## 13.3 Earth

Earth's compactness was calculated as:

```text
EARTH_COMPACTNESS=6.961311310505e-10
```

giving:

```text
EARTH_BETA_ABS_CRIT=1.181482908519e+09
```

Already far beyond the neutron-star coupling scale.

---

## 13.4 Uniform osmium laboratory objects

For density:

```text
OSMIUM_DENSITY=22590 kg/m^3
```

the results were:

### Radius 0.1 m

```text
MASS=9.462477072612e+01 kg
COMPACTNESS=7.026987128408e-25
BETA_ABS_CRIT=1.170440500879e+24
```

### Radius 1 m

```text
MASS=9.462477072612e+04 kg
COMPACTNESS=7.026987128408e-23
BETA_ABS_CRIT=1.170440500879e+22
```

### Radius 10 m

```text
MASS=9.462477072612e+07 kg
COMPACTNESS=7.026987128408e-21
BETA_ABS_CRIT=1.170440500879e+20
```

### Radius 1000 m

```text
MASS=9.462477072612e+13 kg
COMPACTNESS=7.026987128408e-17
BETA_ABS_CRIT=1.170440500879e+16
```

The 1-meter object is separated from the neutron-star threshold by:

```text
ONE_METER_OSMIUM_VS_NS_BETA_RATIO=2.846170006367e+21
```

That is approximately **21 orders of magnitude**.

Therefore:

```text
LAB_SELF_GRAVITY_SCALARIZATION_PLAUSIBLE=NO
ORDINARY_LAB_SPONTANEOUS_SCALARIZATION=REJECTED_BY_COMPACTNESS
```

---

## 13.5 What would scalarize osmium at $\beta\approx-4.5$?

The toy model gave:

```text
OSMIUM_RADIUS_FOR_BETA_4P5_M=5.099979304704e+10
OSMIUM_MASS_FOR_BETA_4P5_KG=1.255191765703e+37
OSMIUM_MASS_FOR_BETA_4P5_SOLAR=6.312349523518e+06
```

So ordinary-density osmium would need a radius of order:

```math
5.1\times10^{10}\ {\mathrm{m}}
```

and a mass of order:

```math
6.3\times10^6 M_\odot
```

for standard strong-field scalarization at $\beta\sim-4.5$.

This is not a materials-engineering effect.

It is compact-object gravity.

---

# 14. Healthy General Conformal Scalar-Tensor Sign

010C also examined the general conformally coupled scalar-tensor form:

```math
S
=
\frac{1}{16\pi G_*}
\int d^4x\sqrt{-g}
\left[
F(\phi)R
-
Z(\phi)(\partial\phi)^2
-
2U(\phi)
\right]
+
S_m[g_{\mu\nu},\psi]
```

The standard massless-scalar Cavendish coupling is:

```math
G_{\mathrm{Cav}}
=
\frac{G_*}{F}
\frac{
2FZ+4F_{,\phi}^2
}{
2FZ+3F_{,\phi}^2
}
```

Healthy tensor propagation requires:

```math
F>0
```

Healthy scalar kinetic structure requires:

```math
Q
=
2FZ+3F_{,\phi}^2
>
0
```

Then the numerator is:

```math
2FZ+4F_{,\phi}^2
=
Q+F_{,\phi}^2
>
0
```

Therefore:

```math
G_{\mathrm{Cav}}>0
```

within this class.

The numerical parameter scan returned:

```text
HEALTHY_PARAMETER_SAMPLE_COUNT=90300
MIN_GCAV_OVER_GTENSOR=1.000000000000000e+00
MAX_GCAV_OVER_GTENSOR=1.000000000000000e+24
NEGATIVE_EFFECTIVE_G_SAMPLE_COUNT=0
HEALTHY_CONFORMAL_SCALAR_TENSOR_GCAV_NEGATIVE=NO
```

This is a strong sign result.

It is not a theorem covering every DHOST, nonlocal, time-dependent, nonuniversal, or strongly nonlinear theory.

---

# 15. Pure Disformal Static Limit and Horndeski Cross-Check

The session recorded the literature-supported static-limit classification:

```text
PURE_DISFORMAL_STATIC_NONREL_SOURCE_CLASSICAL_PROFILE=NO_AT_LEADING_ORDER
PURE_DISFORMAL_STATIC_FIFTH_FORCE=NO_AT_LEADING_ORDER
TIME_DEPENDENT_DISFORMAL_BACKGROUND=NOT_EXCLUDED_BY_THIS_STATIC_ARGUMENT
TIME_DEPENDENT_BACKGROUND_REQUIRES_EXTERNAL_FIELD_ENERGY_OR_FLUX=YES
```

A stable luminal Horndeski EFT cross-check was also recorded:

```text
STABLE_EFT_HAS_POSITIVE_EFFECTIVE_PLANCK_MASS=YES
STABLE_EFT_HAS_POSITIVE_SCALAR_KINETIC_COEFFICIENT=YES
STABLE_EFT_HAS_POSITIVE_SCALAR_SOUND_SPEED_SQUARED=YES
PUBLISHED_STABLE_EFT_LINEAR_ANTIGRAVITY=EXCLUDED_IN_ITS_STATED_SCOPE
THIS_IS_A_LOCAL_NONLINEAR_ALL_THEORIES_THEOREM=NO
```

Correct interpretation:

> **Healthy scalar/nonminimal frameworks continue to resist negative gravitational response; obtaining the wrong sign tends to require leaving the stable region or moving into qualitatively new physics.**

---

# 16. 010C Decision

```text
ONE_METER_OSMIUM_BETA_ABS_CRIT=1.170440500879e+22
ONE_METER_OSMIUM_VS_NS_BETA_RATIO=2.846170006367e+21
ORDINARY_LAB_SPONTANEOUS_SCALARIZATION=REJECTED_BY_COMPACTNESS
HEALTHY_GENERAL_CONFORMAL_SCALAR_TENSOR_NEGATIVE_G=REJECTED
STATIC_PURE_DISFORMAL_LIFT=REJECTED_AT_LEADING_CLASSICAL_ORDER
STABLE_LUMINAL_HORNDESKI_LINEAR_ANTIGRAVITY=REJECTED_IN_PUBLISHED_EFT_SCOPE
ALL_NONLINEAR_MODIFIED_GRAVITY_THEORIES_EXCLUDED=NO
PRACTICAL_ANTIGRAVITY_DEVICE=NOT_ESTABLISHED
010C_GATE=GREEN
```

This closed the idea that ordinary-density matter might simply be pushed into a known scalarized gravitational phase.

---

# 17. 010D — Equivalence-Principle / Center-of-Energy / Background Gate

010D addressed the most important device-level theoretical question of the session:

> **Can a self-contained apparatus alter its gravitational acceleration merely by rearranging its internal state or fields while keeping ordinary equivalence-principle and conservation physics?**

The answer within the tested framework was no.

---

## 17.1 Passive/inertial gravitational response parameter

Define:

```math
\chi
=
\frac{
m_{\mathrm{passive}}
}{
m_{\mathrm{inertial}}
}
```

Then in a uniform external gravitational field:

```math
a
=
\chi g
```

The target values are:

```text
NORMAL_FREE_FALL_CHI=1
WEIGHT_CANCELLATION_CHI=0
UPWARD_1G_FREE_FALL_CHI=-1
```

Therefore:

```text
DELTA_CHI_FOR_WEIGHT_CANCELLATION=-1
DELTA_CHI_FOR_UPWARD_1G=-2
```

This is a central result for the project.

A true $1g$ gravitational inversion is not a small perturbation.

It requires an order-unity reversal in passive gravitational response.

---

# 18. Internal-Energy Anomaly Parametrization

A hypothetical anomalous coupling of a controllable internal-energy fraction $f$ was parametrized as:

```math
\chi
=
1+\eta f
```

where:

```math
f
=
\frac{E_{\mathrm{internal}}}
{m_{\mathrm{inertial}}c^2}
```

To reach a target $\chi$:

```math
\eta
=
\frac{\chi-1}{f}
```

The required values were:

| Internal energy fraction $f$ | $\eta$ for zero weight | $\eta$ for upward $1g$ |
|---:|---:|---:|
| $10^{-15}$ | $-10^{15}$ | $-2\times10^{15}$ |
| $10^{-12}$ | $-10^{12}$ | $-2\times10^{12}$ |
| $10^{-9}$ | $-10^9$ | $-2\times10^9$ |
| $10^{-6}$ | $-10^6$ | $-2\times10^6$ |
| $10^{-3}$ | $-10^3$ | $-2\times10^3$ |
| $10^{-1}$ | $-10$ | $-20$ |
| $1$ | $-1$ | $-2$ |

The interpretation was:

```text
ORDINARY_INTERNAL_ENERGY_ADDED_TO_INERTIAL_MASS=YES
ORDINARY_INTERNAL_ENERGY_ADDED_TO_GRAVITATIONAL_MASS=YES
WEP_PRESERVED_INTERNAL_ENERGY_CHANGES_CHI=NO
STATE_DEPENDENT_WEIGHT_CONTROL_REQUIRES_EP_VIOLATION_OR_NEW_EXTERNAL_FORCE=YES
```

Thus merely storing energy, changing phase, energizing a capacitor, exciting an atom, or generating a bound internal field does not change free-fall acceleration if the equivalence principle continues to hold.

---

# 19. MICROSCOPE Scale Comparison

The session used the final MICROSCOPE Ti/Pt result as an **experimental scale benchmark**, not as a universal bound on every imaginable switchable state.

The quadrature $1\sigma$ scale used was:

```text
MICROSCOPE_TI_PT_ETA_1SIGMA_QUADRATURE=2.745906043549e-15
```

The order-unity upward-$1g$ change corresponds to:

```text
UPWARD_1G_REQUIRED_DELTA_CHI_MAGNITUDE=2
UPWARD_1G_SHIFT_OVER_MICROSCOPE_SCALE=7.283570407292e+14
```

The correct caveat was explicitly preserved:

```text
MICROSCOPE_DIRECTLY_EXCLUDES_EVERY_STATE_DEPENDENT_MODEL=NO
MICROSCOPE_SHOWS_ORDINARY_COMPOSITION_DEPENDENCE_IS_TINY=YES
```

Do not misuse MICROSCOPE as a model-independent exclusion of every possible engineered state-dependent gravitational effect.

---

# 20. Isolated Center-of-Energy Gate

For internal forces:

```math
\mathbf{F}_{AB}
+
\mathbf{F}_{BA}
=
0
```

The toy check returned:

```text
PAIR_INTERNAL_FORCE_SUM_N=0.000000000000e+00
```

The physical conclusion was:

```text
BOUND_INTERNAL_FIELD_MOMENTUM_INCLUDED_IN_TOTAL_SYSTEM=YES
ISOLATED_TOTAL_FOUR_MOMENTUM_CONSERVED=YES
ISOLATED_CENTER_OF_ENERGY_SELF_ACCELERATION=NO
INTERNAL_TIME_DEPENDENT_BACKGROUND_ALONE_PRODUCES_REACTIONLESS_THRUST=NO
```

This generalizes the 009P multilayer result.

It applies not just to the specific fifth-force stack but to **any isolated internal conservative field system** once the field momentum is included.

The central lesson is:

> **Do not mistake internal force redistribution for motion of the total center of energy.**

---

# 21. Radiation Reaction Benchmark

If momentum is exported as perfectly collimated massless radiation:

```math
F
=
\frac{P_{\mathrm{rad}}}{c}
```

so:

```math
\frac{P_{\mathrm{rad}}}{m}
=
ac
```

The absolute ideal power benchmarks were:

```text
RADIATIVE_0.1G_MIN_POWER_W_PER_KG=2.939959708246e+08
RADIATIVE_1G_MIN_POWER_W_PER_KG=2.939959708246e+09
RADIATIVE_10G_MIN_POWER_W_PER_KG=2.939959708246e+10
```

Thus an ideal photon rocket requires roughly:

```math
2.94\ {\mathrm{GW/kg}}
```

for $1g$.

Classification:

```text
RADIATION_CAN_ACCELERATE_CLOSED_PAYLOAD_AFTER_RADIATION_LEAVES=YES
RADIATION_REQUIRES_EXPORTED_MOMENTUM=YES
RADIATIVE_THRUST_IS_REACTIONLESS_ANTIGRAVITY=NO
```

This is ordinary reaction propulsion.

---

# 22. External Background Classification

010D preserved a logically open class:

```text
EXTERNAL_BACKGROUND_CAN_EXCHANGE_ENERGY_MOMENTUM_WITH_DEVICE=YES
EXTERNAL_BACKGROUND_PROPULSION_IS_DYNAMically_ISOLATED=NO
GROUND_REFERENCED_LEVITATION_NOT_FORBIDDEN_BY_CENTER_OF_ENERGY_THEOREM=YES
KNOWN_PRACTICAL_GRAVITATIONAL_BACKGROUND_ACTUATOR=NO
```

This distinction must remain explicit.

An apparatus pushing against:

- Earth;
- an external source mass;
- an electromagnetic field generated elsewhere;
- a cosmological/background field;
- emitted radiation;

is not an isolated reactionless device.

It may still be useful engineering, but it is a different accomplishment level.

---

# 23. Earth Tidal Benchmark

The Earth-surface tidal-gradient scale calculated was:

```text
EARTH_SURFACE_TIDAL_GRADIENT_S^-2=1.539263851829e-06
```

Representative differential accelerations:

```text
SIZE_0.01M_TIDAL_DELTA_A_OVER_G=1.569612305760e-09
SIZE_1M_TIDAL_DELTA_A_OVER_G=1.569612305760e-07
SIZE_10M_TIDAL_DELTA_A_OVER_G=1.569612305760e-06
SIZE_100M_TIDAL_DELTA_A_OVER_G=1.569612305760e-05
```

Therefore:

```text
TIDAL_MULTIPOLE_EFFECTS_EXIST=YES
TIDAL_EFFECTS_ARE_UNIFORM_FIELD_SIGN_REVERSAL=NO
```

This prevents ordinary tidal engineering from being confused with a sign reversal of gravitational response.

---

# 24. 010D Decision

The final 010D status was:

```text
WEP_PRESERVING_INTERNAL_STATE_WEIGHT_MODULATION=REJECTED
ISOLATED_INTERNAL_BACKGROUND_SELF_ACCELERATION=REJECTED_BY_TOTAL_MOMENTUM_CONSERVATION
TIME_DEPENDENT_INTERNAL_FIELD_ESCAPE=REQUIRES_MOMENTUM_EXPORT_OR_EXTERNAL_BACKGROUND
MOMENTUM_EXPORT_ROUTE=ORDINARY_REACTION_PROPULSION
EXTERNAL_BACKGROUND_ROUTE=NOT_SELF_CONTAINED_AND_NOT_YET_REALIZED
ORDER_UNITY_GRAVITATIONAL_RESPONSE_CONTROL=REQUIRES_EP_VIOLATION_OR_EXTERNAL_FORCE_OR_NEW_CONSERVATION_PHYSICS
SELF_CONTAINED_PRACTICAL_ANTIGRAVITY_WITHIN_TESTED_HEALTHY_METRIC_FRAMEWORK=NOT_FOUND
ALL_LOGICALLY_POSSIBLE_NEW_PHYSICS_EXCLUDED=NO
PRACTICAL_ANTIGRAVITY_DEVICE=NOT_ESTABLISHED
010D_GATE=GREEN
```

This is one of the strongest conceptual consolidation points of the project.

---

# 25. What the Session Established About "Practical Antigravity"

Near the end of the session the user asked directly whether the mathematics had proved practical antigravity possible and whether the project had "the formula."

The answer was clarified carefully.

## 25.1 What is proved

The project has an explicit constructive mathematical formula for local antigravity-like gravitational repulsion in linearized GR.

The central active-source structure is:

```math
S
=
\epsilon+p_r+p_\phi+p_z
```

The 006D source is locally conserved through:

```math
q(r)
=
rp_r(r)
```

```math
p_\phi(r)
=
\frac{dq}{dr}
```

with:

```math
p_z=0
```

so:

```math
\frac{dp_r}{dr}
+
\frac{p_r-p_\phi}{r}
=
0
```

The energy density is chosen as:

```math
\epsilon
=
\max
\left(
|p_r|,
|p_\phi|
\right)
```

which enforces pointwise type-I DEC for the constructed static tensor.

The finite-source axial field is evaluated as:

```math
a_z(h)
=
-\frac{2\pi G}{c^2}
\int dz
\int_0^\infty dr\,
r
\left(
\epsilon+p_r+p_\phi+p_z
\right)
\frac{h-z}
{\left[
r^2+(h-z)^2
\right]^{3/2}}
```

The verified source gives a locally outward field while keeping positive far-field active mass.

That is the basis for the new project headline.

---

## 25.2 Best finite scaling formula

The best tested finite-thickness coefficient remains:

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

For:

```math
a=g
```

and:

```math
h=1\ {\mathrm{m}}
```

the required energy-equivalent mass is approximately:

```math
M_{\mathrm{equiv}}
\approx
3.47\times10^{12}\ {\mathrm{kg}}
```

and:

```math
E
=
M_{\mathrm{equiv}}c^2
\approx
3.12\times10^{29}\ {\mathrm{J}}
```

Therefore the formula works mathematically but is catastrophically impractical at human scales.

---

## 25.3 Formula for true gravitational response inversion

A second formula clarified the actual practical target:

```math
\chi
=
\frac{
m_{\mathrm{passive}}
}{
m_{\mathrm{inertial}}
}
```

with:

```math
a=\chi g
```

Then:

```text
chi=+1 -> ordinary downward free fall
chi=0  -> zero passive weight response
chi=-1 -> upward gravitational acceleration of magnitude g
```

Thus:

```math
\chi=-1
```

is a compact **target condition** for true gravitational inversion.

It is not a mechanism.

No healthy experimentally allowed theory has been found that lets ordinary matter be controllably switched from:

```math
\chi=+1
```

to:

```math
\chi=-1
```

---

# 26. Public-Facing Headline Decision

The user explicitly selected the README headline:

> # **We have a mathematical construction for antigravity-like gravitational repulsion.**

This is now the preferred public description of the strongest result.

The README was rewritten so that the claim appears immediately under:

```text
# Antigravity Research
```

It is followed immediately by the exact scientific qualification:

> **Within static linearized general relativity, this repository constructs a finite-radius, finite-thickness, nonsingular, positive-energy, locally conserved stress-energy distribution that satisfies the null, weak, and dominant energy conditions and produces a locally outward gravitational field while retaining positive far-field active mass.**

The README then contains a dedicated section:

```text
# Mathematical Proof of the Headline Claim
```

This was intentionally done so that the headline is backed by equations at the top of the repository rather than appearing as unsupported promotional language.

---

# 27. README Mathematical Proof Added in This Session

The rewritten README explicitly includes:

## 27.1 Weak-field active source

```math
S
=
\epsilon+p_r+p_\phi+p_z
```

and:

```math
\nabla^2\Phi
=
\frac{4\pi G}{c^2}S
```

## 27.2 Axisymmetric field integral

```math
a_z(h)
=
-\frac{2\pi G}{c^2}
\int dz
\int_0^\infty dr\,
r
S(r,z)
\frac{h-z}
{\left[r^2+(h-z)^2\right]^{3/2}}
```

## 27.3 Conservation construction

```math
q(r)=rp_r(r)
```

```math
p_\phi(r)=\frac{dq}{dr}
```

and the explicit cancellation:

```math
\frac{dp_r}{dr}
+
\frac{p_r-p_\phi}{r}
=
0
```

## 27.4 Explicit radial architecture

The inherited optimized geometry is:

```math
\alpha
=
\frac{a}{h}
=
1.437500564637
```

```math
\beta
=
\frac{R}{h}
=
4.701437405300
```

with thin-profile pieces:

```math
q_{\mathrm{core}}(r)=-r
```

and:

```math
q_{\mathrm{annulus}}(r)
=
-\frac{\alpha^2}{r}
```

and finite smoothing through:

```math
s(t)
=
t^2(3-2t)
```

## 27.5 Finite vertical profile

The finite-thickness profile included is:

```math
\phi(z)
=
\frac{30}{t}
x^2(1-x)^2
```

inside the compact slab, with zero support outside.

## 27.6 Pointwise energy conditions

```math
\epsilon
=
\max
\left(
|p_r|,
|p_\phi|
\right)
```

with:

```math
p_z=0
```

immediately gives:

```math
|p_i|\le\epsilon
```

and therefore DEC/WEC/NEC for the constructed static type-I stress tensor.

## 27.7 Numerical verification values

The README now records:

```text
MAX_CONTROL_VOLUME_CONSERVATION_RESIDUAL=3.103073353827e-14
MAX_DEC_VIOLATION=0
MIN_NEC_MARGIN=0
MAX_INTEGRATED_STRESS_TRACE=2.922107000813e-13

LOCAL_CONSERVATION=PASS
NEC=PASS
WEC=PASS
DEC=PASS
LAUE_STRESS_BALANCE=PASS
```

It also records:

```text
OUTWARD_GRAVITATIONAL_FIELD=YES
POSITIVE_FAR_FIELD_ACTIVE_MASS=YES
```

## 27.8 Finite-thickness convergence

```text
scale=0.40000  C=38.037638025730
scale=0.20000  C=29.559369544823
scale=0.10000  C=26.258214373557
scale=0.05000  C=24.789414887263
scale=0.02500  C=24.095429926871
scale=0.01250  C=23.757986246352
scale=0.00625  C=23.591586299249
```

with:

```math
C_{\mathrm{thin}}
=
23.426710175391
```

and:

```math
C_{\mathrm{finite}}
=
23.591586299249
```

The README therefore now presents the strongest claim with its mathematical basis and limitations in one place.

---

# 28. NOTES.md Changes Made in This Session

The notes were also updated so the headline is not confined to the README.

A new top-level current-project headline section was added:

> **We have a mathematical construction for antigravity-like gravitational repulsion.**

The notes immediately state the precise scope and preserve the claim boundary:

```text
MATHEMATICAL_LOCAL_REPULSION=ESTABLISHED
FINITE_POSITIVE_ENERGY_LINEARIZED_GR_CONSTRUCTION=ESTABLISHED
LOCAL_CONSERVATION_LINEARIZED_ORDER=ESTABLISHED
NEC_WEC_DEC=PASS
OUTWARD_LOCAL_GRAVITATIONAL_FIELD=ESTABLISHED

EXACT_NONLINEAR_GR_REALIZATION=NOT_ESTABLISHED
DYNAMIC_STABILITY=NOT_ESTABLISHED
KNOWN_MATERIAL_REALIZATION=NO
ENERGETIC_PRACTICALITY=NO
PRACTICAL_ANTIGRAVITY_DEVICE=NO
NEW_PHYSICS_DISCOVERY=NO
```

The notes were also extended with post-009N / 010D frontier summaries.

The user requested the headline be **emphasized in the notes**, and that has been done.

---

# 29. GitHub Math Formatting Standard Preserved

The README rewrite was deliberately formatted for GitHub.

Repository standard:

Inline math:

```text
$...$
```

Display math:

````text
```math
...
```
````

Avoid:

```text
\(...\)
```

and:

```text
\[...\]
```

The new README and notes use fenced GitHub `math` blocks for display equations.

This is important because previous README versions had rendering problems on GitHub.

---

# 30. Stale README State Corrected

The attached README at the beginning of the documentation task was significantly behind the actual scientific frontier.

It still said:

```text
active next branch = established quantum field theory
next = 007A Casimir benchmark
then = 007B quantum energy inequalities
```

This was no longer true.

It also reported:

```text
72 passed
```

which was stale.

The rewritten README now reports:

```text
94 passed
```

and summarizes the research through 010D.

Therefore:

```text
README_FRONTIER_STALENESS=FIXED
README_TEST_BASELINE_STALENESS=FIXED
README_HEADLINE_CLAIM_ADDED=YES
README_HEADLINE_PROOF_ADDED=YES
```

---

# 31. Literature Used or Reconfirmed During This Session

The following literature was central to the reasoning.

This list records what was used; bibliographic metadata should be reverified before formal publication if exact citation formatting matters.

## Scalar fifth-force / neutron-star cooling

**Fiorillo, Lella, O'Hare, Vitagliano**  
"Leading Bounds on Micrometer to Picometer Fifth Forces from Neutron Star Cooling"  
Phys. Rev. Lett. 135, 211003 (2025)  
arXiv:2506.19906

Used for:

- equal-coupling scalar neutron-star bound scale;
- explicit $g_p,g_n$ decomposition;
- enhanced isospin-violating $np$ bremsstrahlung;
- 009O preflight normalization.

## Composition-dependent scalar couplings

**Damour & Donoghue**  
Phys. Rev. D 82, 084033 (2010)

Used as background support that light scalars can have composition-dependent effective charges.

## Scalar isospin / blind-direction algebra

**Aristizabal Sierra et al.**  
JHEP 12 (2019) 124

Used as background support for isospin-dependent scalar nuclear couplings and blind directions.

This was not treated as a full fifth-force UV completion.

## Effective-$Z'$ / vectorlike mixing

**Fox, Liu, Tucker-Smith, Weiner**  
arXiv:1104.4127

Used for:

- effective $Z'$ generation from vectorlike fermion mixing;
- relation between $g_{\mathrm{eff}}$, $g'$, mixing angle, and partner mass;
- difficulty of unequal $u_L,d_L$ couplings under $SU(2)_L$;
- dimension-eight Higgs-inserted isospin violation;
- custodial / electroweak precision concerns.

## Scalarization

Standard Damour–Esposito-Farèse spontaneous scalarization literature and modern reviews were used as the benchmark context for:

```text
realistic onset beta ~ -4.35
```

The session's constant-density derivation independently produced:

```text
beta_crit ~ 4.11
```

for compactness $0.2$.

## Einstein-æther

Published weak-field Einstein-æther results were used for:

```math
G_N
=
\frac{G}
{1-c_{14}/2}
```

and for the classification of $c_{14}=2$ as a singular/special point.

GW170817-era constraints were used only as a scale reminder.

## Stable Horndeski / EFT

A published stable-EFT result for luminal Horndeski was used as a scope-limited cross-check that stable linear cosmological parameter space excludes antigravity behavior in that framework.

This was explicitly **not** promoted to a theorem covering every local nonlinear modified-gravity theory.

## Equivalence principle

MICROSCOPE final Ti/Pt results were used as a benchmark showing extraordinarily small ordinary composition-dependent WEP violation.

The experiment was **not** treated as a direct exclusion of every imaginable state-dependent macroscopic gravitational phase.

---

# 32. Major Conceptual Lessons Learned This Session

## 32.1 The sign problem is solved more than the engineering problem

The project no longer needs to ask:

```text
CAN_GRAVITY_EVER_POINT_OUTWARD?
```

The answer is yes.

The actual open questions are:

```text
CAN_THE_REQUIRED_STRESS_ENERGY_BE_REALIZED?
CAN_IT_BE_STABLE?
CAN_THE_ENERGY_SCALE_BE_REDUCED_PARAMETRICALLY?
CAN_AN_ORDER_UNITY_GRAVITATIONAL_RESPONSE_CHANGE_OCCUR?
```

---

## 32.2 Positive energy does not forbid local repulsion

The 006D result remains the anchor.

One can have:

```text
positive energy
+ NEC/WEC/DEC
+ local conservation
+ finite support
+ positive far-field mass
+ local outward gravitational field
```

at linearized-GR order.

This is exactly why the new README headline is defensible.

---

## 32.3 Energy-condition satisfaction is not enough

The session repeatedly reinforced:

```text
ENERGY_CONDITIONS_PASS
!=
STABLE_MATERIAL_REALIZATION
```

The 006D tensor can satisfy NEC/WEC/DEC while remaining far beyond known material stresses.

Likewise:

```text
THEORETICAL_FORCE_SIGN
!=
PRACTICAL_DEVICE
```

---

## 32.4 A new repulsive fifth force is not automatically "gravity"

A healthy vector can repel like charges.

That is unsurprising.

The difficult question is whether ordinary neutral matter can experience useful repulsion while the model remains:

- UV consistent;
- electroweak consistent;
- anomaly free;
- stellar safe;
- laboratory safe;
- collider safe.

The 009-series increasingly showed that the required low-energy material-blind charge engineering creates severe high-energy problems.

---

## 32.5 Internal force is not self-contained lift

This is a major stop rule.

Any design that consists entirely of internal source/receiver layers for a reciprocal force must include all reaction forces and field momentum.

If the total system is isolated:

```math
\frac{d\mathbf{P}_{\mathrm{total}}}{dt}=0
```

Therefore:

```text
INTERNAL_FIFTH_FORCE_STACKING
```

must never again be described as a self-contained antigravity propulsion mechanism unless some external momentum reservoir is identified.

---

## 32.6 Screening is usually a suppression mechanism, not a sign-reversal mechanism

The scalar and Proca investigations reinforced that known screening mechanisms are typically designed to drive a new force back toward GR in dense environments.

They do not automatically produce:

```text
attraction -> repulsion
```

---

## 32.7 Strong-field gravitational phases require strong gravity

The 010C scalarization calculation quantified this dramatically.

A neutron star has compactness of order:

```math
10^{-1}
```

A 1-meter osmium sphere has compactness of order:

```math
10^{-22}
```

That difference is why standard scalarization is not a laboratory phase transition.

---

## 32.8 Universal healthy scalar exchange has the wrong sign for antigravity

For ordinary same-sign universal scalar charge:

```math
\alpha_A\alpha_B\ge0
```

so the scalar contribution is attractive.

To make it repulsive one must use:

- opposite charges;
- a ghost sign;
- nonuniversal coupling;
- qualitatively different physics.

Each of these has its own major cost.

---

## 32.9 Positive-residue extra spin-2 modes also do not provide the desired sign

The weak-field spectral interpretation again gives:

```text
positive residue -> healthy -> attraction
negative residue -> repulsive contribution -> ghost-like
```

This is not a proof covering every nonlinear multimetric phase, but it eliminates a large naive branch.

---

## 32.10 Practical gravitational inversion requires a large response change

The $\chi$ parameter made the target explicit:

```text
ordinary matter: chi = +1
zero weight:     chi = 0
upward 1g:       chi = -1
```

Therefore a useful antigravity state is an **order-unity** change in gravitational response.

This is not a tiny correction hiding just below current equivalence-principle precision.

---

# 33. Branches Closed or Strongly Deprioritized by the End of the Session

Within their tested scopes:

```text
CLASSICAL_GR_COEFFICIENT_MICROTUNING_WITHOUT_NEW_SCALING
    DEPRIORITIZED

STATIC_CASIMIR_COMPLETE_APPARATUS
    DEPRIORITIZED

FREE_EM_QEI_MACROSCOPIC_NEGATIVE_ENERGY
    CLOSED_OR_STRONGLY_DEPRIORITIZED

ORDINARY_UNSCREENED_B-L_VECTOR_ORDER_1G
    REJECTED

TERRESTRIAL_MONOLITHIC_CHAMELEON
    REJECTED

MICROSTRUCTURED_CHAMELEON_MATRIX
    REJECTED

RESIDUAL_THIN_SHELL_CHAMELEON
    STRONGLY_DISFAVORED

OPPOSITE_SIGN_UNSCREENED_SCALAR_ORDER_0P1G_TO_1G
    STRONGLY_DISFAVORED

SIMPLE_ONE_HIGGS_GOLD_NULL_VECTOR
    REJECTED

SU2L_PRESERVING_PURE_VECTOR_GOLD_NULL_CURRENT
    REJECTED

SIMPLE_EFFECTIVE_ZPRIME_1G_RESCUE
    SEVERELY_STRESSED / LOW PRIORITY

UNIVERSAL_CANONICAL_SCALAR_TENSOR_SIGN_REVERSAL
    REJECTED

METRIC_F_R_SIGN_REVERSAL
    REJECTED

STANDARD_SCREENING_AS_SIGN_REVERSAL
    REJECTED

WRONG_SIGN_SCALAR
    REJECTED_BY_GHOST

VIABLE_EINSTEIN_AETHER_NEWTONIAN_SIGN_REVERSAL
    REJECTED

HEALTHY_POSITIVE_RESIDUE_WEAK_FIELD_SPIN2_REPULSION
    REJECTED

LAB_SELF_GRAVITY_SCALARIZATION
    REJECTED_BY_COMPACTNESS

HEALTHY_GENERAL_CONFORMAL_SCALAR_TENSOR_NEGATIVE_G
    REJECTED

STATIC_PURE_DISFORMAL_LIFT_AT_LEADING_ORDER
    REJECTED

SELF_CONTAINED_RECIPROCAL_FIFTH_FORCE_STACK
    REJECTED_BY_MOMENTUM_CONSERVATION

WEP_PRESERVING_INTERNAL_STATE_WEIGHT_SWITCHING
    REJECTED

ISOLATED_INTERNAL_TIME_DEPENDENT_FIELD_SELF_THRUST
    REJECTED_BY_CENTER_OF_ENERGY CONSERVATION
```

These branches should not be reopened without a clearly identified qualitative change in mechanism.

---

# 34. Branches Not Universally Closed

The project must remain careful not to overgeneralize.

The following broad categories are **not universally excluded**:

```text
ALL_SCALAR_THEORIES
ALL_SCREENED_SCALAR_THEORIES
ALL_EFFECTIVE_ZPRIME_MODELS
ALL_EXOTIC_VECTOR_MODELS
ALL_GENERALIZED_PROCA_THEORIES
ALL_BIGRAVITY_THEORIES
ALL_DHOST_THEORIES
ALL_NONLOCAL_GRAVITY
ALL_BACKGROUND_DEPENDENT_GRAVITY
ALL_TIME_DEPENDENT_DISFORMAL_THEORIES
ALL_EXPLICIT_EQUIVALENCE_PRINCIPLE_VIOLATING_MODELS
ALL_NEW_PHYSICS
```

The session only rejected specific well-defined mechanisms or broad sign structures within their assumptions.

This distinction is mandatory for future claims.

---

# 35. Current Strongest Positive Results

At session end the strongest positive results are still:

## 35.1 Established-GR sign result

Local gravitational repulsion is physically allowed in GR.

## 35.2 006D constructive finite-source result

A finite, positive-energy, locally conserved, energy-condition-compatible linearized-GR source can produce local outward gravity.

## 35.3 Exact known-theory examples

Reissner–Nordström and domain-wall-type GR solutions provide known exact examples of repulsive behavior under appropriate conditions.

## 35.4 Low-energy fifth-force phenomenology

Some engineered composition-dependent force laws can mathematically yield strong repulsion.

However:

```text
LOW_ENERGY_FORCE_PHENOMENOLOGY
!=
HEALTHY_UV_COMPLETION
```

009M–009Q strongly reinforced this distinction.

---

# 36. Current Strongest Negative Results

The most important negative results are:

1. **Classical scaling problem**
   ```math
   M_{\mathrm{equiv}}
   \sim
   C\frac{ah^2}{G}
   ```
   remains catastrophic at human scale.

2. **Ordinary unscreened scalar/vector fifth forces**
   remain far below useful acceleration after constraints.

3. **Material-blind vector engineering**
   becomes severely stressed by electroweak and UV consistency.

4. **Internal reciprocal forces**
   cannot produce isolated center-of-energy acceleration.

5. **Healthy universal scalar-tensor gravity**
   does not reverse its sign.

6. **Healthy weak-field extra spin-2 modes**
   do not provide repulsion between ordinary positive masses.

7. **Known scalarization mechanisms**
   require compact-object self-gravity.

8. **WEP-preserving internal state changes**
   do not alter gravitational acceleration.

---

# 37. Current Headline Claim — Exact Permitted Wording

Preferred:

> **We have a mathematical construction for antigravity-like gravitational repulsion.**

Preferred precise expansion:

> **Within static linearized general relativity, we have constructed a finite-radius, finite-thickness, nonsingular, positive-energy, locally conserved stress-energy configuration satisfying NEC, WEC, and DEC that produces a locally outward gravitational field while retaining positive far-field active mass.**

Acceptable shorter technical wording:

> **We have a constructive linearized-GR positive-energy stress-energy source for local gravitational repulsion.**

Do not use:

```text
"We proved practical antigravity."
"We discovered antigravity."
"We proved antigravity devices are possible."
"We found negative gravitational mass."
"We built reactionless propulsion."
"We proved a new law of physics."
```

None of those stronger statements is supported.

---

# 38. Distinguish the Levels of Accomplishment

The project must continue to separate:

```text
LEVEL A:
mathematical sign possibility

LEVEL B:
local measurable gravitational repulsion

LEVEL C:
finite physically admissible stress-energy source

LEVEL D:
known realizable matter/field source

LEVEL E:
dynamic stability

LEVEL F:
experimentally accessible signal

LEVEL G:
useful ground-referenced levitation

LEVEL H:
self-contained gravitational response control

LEVEL I:
practical antigravity device
```

The project is strongest around Levels B/C within linearized GR.

It has not reached the final engineering levels.

---

# 39. Important Formula Ledger

## Active gravitational source

```math
S
=
\epsilon+p_x+p_y+p_z
```

or for the axisymmetric construction:

```math
S
=
\epsilon+p_r+p_\phi+p_z
```

## Linearized Poisson source

```math
\nabla^2\Phi
=
\frac{4\pi G}{c^2}S
```

## Axisymmetric axial field

```math
a_z(h)
=
-\frac{2\pi G}{c^2}
\int dz
\int_0^\infty dr\,
rS(r,z)
\frac{h-z}
{\left[
r^2+(h-z)^2
\right]^{3/2}}
```

## 006D conservation construction

```math
q(r)=rp_r(r)
```

```math
p_\phi(r)=\frac{dq}{dr}
```

## 006D pointwise energy density

```math
\epsilon
=
\max
\left(
|p_r|,
|p_\phi|
\right)
```

## Best finite classical scaling

```math
M_{\mathrm{equiv}}
=
23.591586299249
\frac{ah^2}{G}
```

## Scalar material charge

```math
s_{A,Z}
=
\frac{
Zg_p+(A-Z)g_n
}{A}
```

## Scalar Yukawa potential

```math
V_{12}(r)
=
-\frac{\hbar c}{4\pi}
\frac{Q_1Q_2}{r}
e^{-r/\lambda}
```

## Scalar half-space acceleration

```math
a_{\mathrm{half}}
=
\frac{\hbar c}{2m_u^2}
\rho\lambda
|s_{\mathrm{src}}s_{\mathrm{test}}|
e^{-z/\lambda}
```

## Isospin decomposition for stellar scalar emission

```math
g
=
\frac{g_p+g_n}{2}
```

```math
\delta g
=
\frac{g_n-g_p}{2}
```

## Effective-$Z'$ portal

```math
g_{\mathrm{eff}}
=
g'\sin^2\theta
```

```math
M_Q
=
\frac{y}{\sqrt2}
\frac{M_X}
{\sqrt{g'g_{\mathrm{eff}}}}
```

## Effective-$Z'$ optimistic partner ceiling

```math
M_Q
\le
\frac{y}{\sqrt2}
\frac{M_X}{g_{\mathrm{eff}}}
```

## $SU(2)_L$ axial floor

```math
|a|_{\min}
=
\frac{
|v_u-v_d|
}{2}
```

## Dimension-eight isospin-splitting preflight

```math
\Lambda^4
\sim
\frac{
C M_X^2v_H^2
}{
2g'g_{\mathrm{eff}}
}
```

## Universal scalar-tensor force

```math
\frac{F}{F_{\mathrm{GR}}}
=
1+
2\alpha_A\alpha_B
\left(
1+\frac{r}{\lambda}
\right)
e^{-r/\lambda}
```

## Einstein-æther Newtonian coupling

```math
G_N
=
\frac{G}
{1-c_{14}/2}
```

## Scalarization onset

```math
|\beta|
\frac{GM}{Rc^2}
=
\frac{\pi^2}{12}
```

## General conformal scalar-tensor Cavendish coupling

```math
G_{\mathrm{Cav}}
=
\frac{G_*}{F}
\frac{
2FZ+4F_{,\phi}^2
}{
2FZ+3F_{,\phi}^2
}
```

## Gravitational response parameter

```math
\chi
=
\frac{
m_{\mathrm{passive}}
}{
m_{\mathrm{inertial}}
}
```

```math
a=\chi g
```

with:

```math
\chi=-1
```

as the target condition for upward gravitational acceleration equal in magnitude to ordinary $g$.

## Ideal radiation thrust

```math
F
=
\frac{P}{c}
```

```math
\frac{P}{m}
=
ac
```

---

# 40. Numerical Benchmark Ledger

## 006D

```text
C_THIN=23.426710175391
C_FINITE=23.591586299249
```

## 009G

```text
UNSCREENED_VECTOR_HALFSPACE_MAX≈0.0220921g
```

## 009O

```text
UNSCREENED_OPPOSITE_SCALAR_HALFSPACE_MAX≈7.3273e-4g
```

## 009L phenomenological low-energy direction

```text
ISL_ONLY_CONTACT_FORCE≈1.027g
```

but:

```text
HEALTHY_UV_REALIZATION=NOT_ESTABLISHED
```

## 009Q axial floor

```text
UNAVOIDABLE_AXIAL_COUPLING_AT_1G=1.064556829114e-11
```

## 009Q strong-NDA dimension-eight cutoff

```text
LAMBDA_U_MAX≈582 GeV
LAMBDA_D_MAX≈602 GeV
```

## 010C scalarization

```text
NS_BETA_CRIT≈4.112
EARTH_BETA_CRIT≈1.181e9
ONE_METER_OSMIUM_BETA_CRIT≈1.170e22
```

## 010D

```text
UPWARD_1G_DELTA_CHI=-2
MICROSCOPE_SCALE≈2.746e-15
IDEAL_PHOTON_1G_POWER≈2.94e9 W/kg
```

---

# 41. What Was Proposed but NOT Completed

This section is important.

The assistant proposed:

```text
010E_GLOBAL_SURVIVOR_AND_EXPERIMENTAL_ACCESSIBILITY_DECISION_GATE
```

but the user did **not** execute it.

Therefore:

```text
010E_STATUS=PROPOSED_NOT_RUN
010E_RESULTS=NONE
```

Do not treat any expected 010E output as established.

The user then clarified:

> experimental design is not desired just yet.

Therefore the previously proposed next step:

```text
011A_SWITCHABLE_STATE_GRAVITATIONAL_RESPONSE_EXPERIMENT_DESIGN
```

must **not** be treated as the active next task unless the user later changes direction.

This is a key carry-forward instruction.

---

# 42. Current Theory-Side Frontier

The next session should remain theory-focused.

The strongest theory-side question is now:

> **Can any physically consistent mechanism change the practical scaling or the gravitational response itself without requiring ghosts, forbidden independent material charges, pathological low-scale UV completion, astronomical energy, or violation of total energy-momentum conservation?**

Potential surviving logical classes include:

```text
1. PHYSICALLY_REALIZABLE_RELATIVISTIC_TENSION_WITH_NEW_PARAMETRIC_SCALING

2. OBSERVATIONALLY_VIABLE_NONSTANDARD_GRAVITATIONAL_RESPONSE
   NOT REDUCIBLE TO THE HEALTHY UNIVERSAL SCALAR / POSITIVE-RESIDUE
   SPIN-2 / EXPLICIT VECTOR-CHARGE CLASSES ALREADY TESTED

3. CONTROLLABLE BACKGROUND-DEPENDENT GRAVITATIONAL RESPONSE
   WITH AN EXPLICIT EXTERNAL MOMENTUM/ENERGY RESERVOIR

4. GENUINE STATE-DEPENDENT PASSIVE GRAVITATIONAL RESPONSE
   WITH A CONSISTENT FIELD THEORY

5. OTHER CONSERVATIVE NEW PHYSICS THAT CHANGES THE a*h^2/G SCALING
   RATHER THAN ONLY ITS ORDER-UNITY COEFFICIENT
```

None is established.

---

# 43. Highest-Value Next Analytical Work

Given the user's instruction not to move into experimental design yet, the next slice should be a **theory-only global survivor gate**.

A good active question is:

> **Can we prove a broader no-go theorem for self-contained static antigravity under local Lorentz invariance, positive-energy propagating modes, universal matter coupling, and local stress-energy conservation, and then identify exactly which assumption must be relaxed for any remaining viable mechanism?**

This would generalize the pattern already seen:

```text
healthy scalar universal exchange -> attractive
healthy positive-residue spin-2 -> attractive
healthy vector -> can repel but requires independent charge
internal reciprocal fields -> zero COM thrust
ordinary WEP internal energy -> no weight switch
```

A useful theorem-style decomposition could classify candidate theories by which assumption they violate:

```text
UNIVERSALITY
POSITIVITY / NO-GHOST
LOCALITY
LORENTZ INVARIANCE
STRESS_ENERGY_CONSERVATION
STATICITY
ISOLATION
WEAK_FIELD EXPANSION
SINGLE-METRIC MATTER COUPLING
```

This may be the highest-information theoretical action before opening another speculative Lagrangian.

---

# 44. Alternative Theory-Side Next Branch: Stress-Energy Realizability

A second high-value theory branch would return to the **strongest positive result**, not to coefficient tuning.

Question:

> **Is there any known stable classical or quantum field configuration whose stress tensor approaches the 006D target while changing the parametric energy scaling?**

This must not become another arbitrary field search.

The decisive requirement is:

```text
NEW_MECHANISM_MUST_CHANGE_SCALING
```

not merely:

```text
C=23.6 -> C=18
```

The existing classical branch remains dominated by:

```math
M
\sim
\frac{ah^2}{G}
```

An order-unity coefficient improvement is not enough.

A new field model should only be pursued if there is an analytical reason it might replace:

```math
h^2/G
```

with a qualitatively better scale.

---

# 45. Stop Rules for the Next Session

Do not reopen a branch merely because it is interesting.

Stop immediately if:

```text
1. Repulsion requires a negative-residue propagating degree of freedom.
2. A candidate is simply an explicit material fifth-force charge already covered by 009.
3. A candidate only screens an attractive force back toward GR.
4. A candidate requires compactness characteristic of neutron stars.
5. A candidate gives internal forces but no external momentum exchange.
6. A candidate improves only an order-unity coefficient while retaining ah^2/G.
7. A candidate violates current constraints by many orders of magnitude with no explicit screening mechanism.
8. A purported UV completion requires nonphysical sin^2(theta)>1.
9. A candidate relies on a singular sign flip across a zero kinetic/Planck-mass point.
10. A claim of practical antigravity cannot identify the physical source, stability mechanism, and energy scale.
```

Preserve the negative result and move on.

---

# 46. Claims Discipline for Future Sessions

Always distinguish:

## Published literature result

A statement taken from an external paper.

## Project-derived analytic result

A derivation performed within the project.

## Project-derived numerical result

A simulation or numerical scan result.

## Literature-normalized preflight

A calculation that reuses a published constraint as a proxy but does not reproduce the full likelihood/analysis.

009O is in this category.

## Constructive linearized-GR result

006D.

## Unverified hypothesis

A new mechanism not yet tested.

## Practical device claim

Requires:

- realizable source;
- stability;
- useful field;
- energy/material plausibility;
- control;
- geometry;
- independent verification.

The project has not reached this level.

---

# 47. README / Notes Files Produced in This Session

Two user-facing replacement files were generated:

```text
README.md
NOTES.md
```

The README was rewritten to:

- place the headline at the top;
- put the mathematical proof immediately beneath it;
- update the frontier through 010D;
- update the test baseline to 94 passed;
- remove stale 007A/007B "next active" language;
- preserve GitHub-compatible mathematics;
- preserve conservative claim boundaries.

The NOTES file was updated to:

- put the same headline and exact qualification at the top;
- preserve prior chronological research history;
- add the new post-009N/010D results;
- explicitly distinguish the mathematical construction from a practical device.

These should be treated as the newest documentation artifacts produced in the session.

---

# 48. Recommended Buildplan Update

`RESEARCH_BUILDPLAN.md` is now stale relative to the actual frontier.

The codebundle version still reflects much earlier 006-era active-task language in some sections.

A future documentation pass should update the buildplan to include:

```text
009O=COMPLETE_PREFLIGHT
009P=COMPLETE
009Q=COMPLETE
010A=COMPLETE
010B=COMPLETE
010C=COMPLETE
010D=COMPLETE
010E=PROPOSED_NOT_RUN
```

The buildplan should also state explicitly:

```text
USER_DIRECTION=DO_NOT_MOVE_TO_EXPERIMENT_DESIGN_YET
```

and make the active frontier theory-only.

Do not silently treat the stale buildplan's 006/007 "NEXT" fields as current.

---

# 49. Current Repository Hygiene / Permanent-Code Note

At the last verified baseline:

```text
94 passed
```

The working tree still contained untracked 008-era permanent work.

The session intentionally did **not** land 009O–010D as permanent code.

Before making permanent scientific code from these gates:

1. decide which results are central enough to preserve;
2. follow `FORMATTING_AND_CODE_STANDARDS.md`;
3. add unusually thorough top-of-file scientific documentation;
4. include equations, units, sign conventions, assumptions, limitations, and claim classification;
5. add focused regression tests;
6. do not test an implementation only against itself;
7. preserve literature-derived constants with citations/comments;
8. rerun the known-solution suite.

---

# 50. Suggested Permanent Results Worth Eventually Landing

If the project chooses to promote the disposable gates, the strongest candidates are:

```text
009O:
opposite-sign scalar neutron-star / half-space preflight

009P:
effective-Z' portal ceiling + internal-force COM theorem regression

009Q:
SU2L axial-floor + dimension-eight UV-scale preflight

010A:
universal canonical scalar-tensor sign theorem

010C:
scalarization compactness threshold

010D:
gravitational response chi bookkeeping / center-of-energy classification
```

010B contains useful sign logic but may be better represented in documentation unless a more rigorous spectral implementation is added.

Do not land disposable exploratory code merely for completeness.

---

# 51. Deep Scientific Interpretation at Session End

The project began by asking whether "antigravity" was even mathematically meaningful within serious gravitational physics.

The answer is now clearly:

```text
YES_FOR_LOCAL_GRAVITATIONAL_REPULSION
```

The 006D construction is an explicit demonstration.

However, the subsequent session results increasingly show that Nature protects ordinary gravity through multiple layers:

```text
GENERAL_RELATIVITY:
repulsive stress-energy allowed
but expensive

QUANTUM FIELD THEORY:
negative energy allowed
but tightly constrained

SCALAR FIFTH FORCES:
composition engineering possible
but stellar/lab bounds severe

VECTOR FIFTH FORCES:
repulsion natural
but material charge / UV consistency severe

SCALAR-TENSOR GRAVITY:
healthy universal sign stays attractive

EXTRA SPIN-2:
healthy weak-field residue stays attractive

NONPERTURBATIVE SCALARIZATION:
requires compact-object gravity

INTERNAL FIELDS:
momentum conservation prevents self-thrust

EQUIVALENCE PRINCIPLE:
ordinary internal-state changes do not switch weight
```

This repeated pattern is itself scientifically informative.

It suggests that a practical antigravity mechanism, if one exists, is unlikely to be a minor variation of already-tested weak-field mediators.

It would probably require at least one genuinely new ingredient such as:

```text
a new realizable relativistic stress source,
a new gravitational phase,
a nonstandard matter-metric coupling,
a controllable external gravitational reservoir,
or other physics outside the tested healthy weak-field classes.
```

That is a much narrower and more useful conclusion than where the project began.

---

# 52. Final Session State

Use the following as the carry-forward terminal-style summary:

```text
=== ANTIGRAVITY_RESEARCH — END OF SESSION STATE ===

REGRESSION_BASELINE=94_PASSED
REPOSITORY_BLOCKING_REGRESSION=NO

HEADLINE_CLAIM=
WE_HAVE_A_MATHEMATICAL_CONSTRUCTION_FOR_ANTIGRAVITY_LIKE_GRAVITATIONAL_REPULSION

HEADLINE_SCOPE=
FINITE_POSITIVE_ENERGY_LOCALLY_CONSERVED_NEC_WEC_DEC_LINEARIZED_GR_LOCAL_REPULSION

006D_CONSTRUCTIVE_LINEARIZED_GR_RESULT=ESTABLISHED
006D_C_FINITE=23.591586299249
006D_C_THIN=23.426710175391
006D_PRACTICAL_ENERGY_SCALE=NO

009O_OPPOSITE_SIGN_SCALAR=STRONGLY_DISFAVORED
009O_BEST_A_OVER_G=7.327295675071e-04

009P_SIMPLE_EFFECTIVE_ZPRIME=SEVERELY_STRESSED
009P_SELF_CONTAINED_MULTILAYER_FIFTH_FORCE_LIFT=REJECTED

009Q_SU2L_PRESERVING_PURE_VECTOR=REJECTED
009Q_EXOTIC_EW_COMPENSATED_VECTOR=SEVERELY_STRESSED_NOT_CLOSED
009Q_STRONG_NDA_LAMBDA_U_MAX_GEV=582.021760
009Q_STRONG_NDA_LAMBDA_D_MAX_GEV=601.574737

010A_UNIVERSAL_CANONICAL_SCALAR_TENSOR_REPULSION=REJECTED
010A_METRIC_FR_REPULSION=REJECTED
010A_STANDARD_SCREENING_SIGN_FLIP=REJECTED

010B_EINSTEIN_AETHER_HEALTHY_NEWTONIAN_REPULSION=REJECTED
010B_POSITIVE_RESIDUE_SPIN2_REPULSION=REJECTED_AT_WEAK_FIELD_LEVEL
010B_VECTOR_REPULSION=YES_BUT_MAPS_TO_FIFTH_FORCE_CHARGE

010C_LAB_SCALARIZATION=REJECTED_BY_COMPACTNESS
010C_ONE_METER_OSMIUM_BETA_CRIT=1.170440500879e22
010C_HEALTHY_CONFORMAL_NEGATIVE_G=REJECTED
010C_STATIC_PURE_DISFORMAL_LIFT=REJECTED_AT_LEADING_ORDER

010D_WEP_PRESERVING_WEIGHT_SWITCH=REJECTED
010D_ISOLATED_INTERNAL_SELF_ACCELERATION=REJECTED
010D_UPWARD_1G_TARGET_CHI=-1
010D_DELTA_CHI_FROM_NORMAL=-2
010D_IDEAL_PHOTON_1G_POWER_W_PER_KG=2.939959708246e09

010E=PROPOSED_NOT_RUN
EXPERIMENT_DESIGN_NEXT=NO_PER_CURRENT_USER_DIRECTION

EXACT_NONLINEAR_GR_REALIZATION=NOT_ESTABLISHED
DYNAMIC_STABILITY=NOT_ESTABLISHED
KNOWN_MATERIAL_REALIZATION=NO
PRACTICAL_ANTIGRAVITY_DEVICE=NO

ACTIVE_THEORY_QUESTION=
CAN_ANY_PHYSICALLY_CONSISTENT_MECHANISM_CHANGE_THE_PRACTICAL_SCALING_OR_GRAVITATIONAL_RESPONSE_ITSELF_WITHOUT_GHOSTS_PATHOLOGICAL_UV_ASTRONOMICAL_ENERGY_OR_MOMENTUM_CONSERVATION_FAILURE

NEXT_RECOMMENDED_ACTION=
THEORY_ONLY_GLOBAL_NO_GO_AND_SURVIVOR_CLASSIFICATION_BEFORE_OPENING_ANOTHER_MODEL
```

---

# 53. One-Sentence Carry-Forward

If only one sentence from this entire session is preserved, use:

> **We have a mathematically explicit finite positive-energy linearized-GR construction for local antigravity-like gravitational repulsion, but this session's scalar, vector, modified-gravity, equivalence-principle, and momentum-conservation gates substantially narrowed the remaining route to practical antigravity and did not establish a realizable device.**




### END NOTE - AUGUST 28 2026 - 02:10 CST



### BEGIN NOTE - AUGUST 28 2026 - 23:25 CST 


I consolidated this as a next-session handoff rather than a README-style summary. It preserves 006D as the strongest established result, records the full 010E-O through 010E-Y chain—including the routes we killed—and makes the protected relativistic two-body matching problem the single active frontier. The equations and Markdown follow the repository’s fenced-`math` GitHub standard.   

### BEGIN NOTE — AUGUST 28, 2026 — 010E-Y SESSION CLOSEOUT / NEXT-SESSION CARRY-FORWARD

# ANTIGRAVITY_RESEARCH — Comprehensive Carry-Forward Notes

## Session scope

These notes are intended to provide the complete scientific handoff needed to begin the next Antigravity Research session without reconstructing the work from conversation history.

They consolidate:

* the strongest established project result;
* the current repository/test state;
* the theoretical context entering the late 010E work;
* the complete 010E-O through 010E-Y progression;
* all major negative results discovered during that progression;
* the mathematical basis of the surviving low-energy model;
* the precise claim limits;
* the decisive unresolved ultraviolet problem;
* the stop rules that should terminate the branch if violated;
* the recommended next-session execution order.

The central project headline remains unchanged:

> # **We have a mathematical construction for antigravity-like gravitational repulsion.**

The exact scientific meaning of that sentence is still the 006D result:

> Within static linearized general relativity, there exists an explicit finite-radius, finite-thickness, nonsingular, positive-energy, locally conserved type-I stress-energy configuration satisfying NEC, WEC, and DEC whose calculated near gravitational field points outward while its far-field active mass remains positive.

Nothing in 010E-O through 010E-Y upgrades this to:

```text
NEW_FORCE_DISCOVERY
PRACTICAL_ANTIGRAVITY_DEVICE
KNOWN_ANTIGRAVITY_MATERIAL
EXPERIMENTALLY_DEMONSTRATED_ANTIGRAVITY
EXACT_NONLINEAR_GR_ANTIGRAVITY_SOLUTION
```

The late 010E work instead produced a much narrower speculative result:

> **A protected, material-specific, nonrelativistic bound-composite scalar response can be constructed consistently at low energy, with a cooperative dinuclear spin-crossover state as the present lowest-complexity host architecture.**

Whether Nature possesses the required interaction remains completely unestablished.

---

# 1. Governing scientific discipline

Every future session must continue to distinguish the following levels of achievement.

1. Mathematical sign reversal.
2. Operationally meaningful local gravitational or fifth-force repulsion.
3. Consistency with the governing field equations.
4. Acceptable stress-energy or quantum-field content.
5. Finite localization.
6. Local conservation.
7. Stability.
8. Physical field/material realization.
9. Energetic plausibility.
10. Experimental accessibility.
11. Practical useful apparatus.

These levels are not interchangeable.

A mathematical solution is not a device.

A locally outward field is not necessarily globally repulsive.

A fifth force is not ordinary general-relativistic antigravity.

A ground-referenced scalar force is not reactionless propulsion.

A successful EFT model is not evidence that the required interaction exists in Nature.

A GREEN computational gate means that the calculation completed and produced a scientifically interpretable decision. It does not automatically mean the proposed physical branch survived.

The project should continue to use the following philosophy:

> Prefer the cheapest decisive falsification test before introducing additional degrees of freedom or model complexity.

When a branch fails a fundamental physical constraint, record the failure and rerank. Do not protect sunk effort by adding knobs.

---

# 2. GitHub mathematical-formatting rules

Use inline mathematics only with single dollar signs.

Example:

```markdown
The mediator range is $\lambda=5\,{\rm km}$.
```

Use fenced `math` blocks for standalone mathematics.

Correct:

```math
m_\phi
=
\frac{\hbar c}{\lambda}
```

Do not use:

```text
\[
...
\]
```

Do not use:

```text
\(...)
```

Do not put grammatical punctuation at the end of display-math blocks.

Keep units visible:

```math
E
=
1.06\times10^8\ {\mathrm{J}}
```

Important equations may be boxed, but boxing should be reserved for central thresholds or results.

---

# 3. Source-code standard reminder

If any 010E result is promoted from disposable analytical gate to permanent source code, the file must include unusually complete top-of-file scientific documentation covering at least:

* purpose;
* scientific question;
* physical model;
* equations;
* units;
* sign conventions;
* assumptions;
* approximation level;
* numerical method;
* validation;
* limitations;
* related files;
* claim classification;
* what the file does not establish.

Important equations should be documented close to their implementation.

Important functions should have meaningful docstrings.

Comments should explain why the operation exists scientifically, not merely restate the code.

---

# 4. Repository and test-state checkpoint

The latest attached codebundle was generated at:

```text
2026-08-28 13:56:55 CDT
```

with:

```text
PROJECT=ANTIGRAVITY_RESEARCH
BRANCH=main
HEAD=0fe32225b5430ed1adb6c64bd1424bd365b68377
INCLUDED_FILES=84
WORKING_TREE=CLEAN
```

However, most of the very late 010E analytical gates were run after the codebundle snapshot as shell/Python heredocs.

Therefore the beginning of the next session should still verify current repository state directly.

First commands:

```bash
git status --short

ROOT="$(pwd)"
PY="$ROOT/.venv/bin/python"

PYTHONPATH="$ROOT/src" \
"$PY" -m pytest -q tests/known_solutions
```

The regression baseline at the end of 010E-Y was:

```text
94 passed in 4.58s
```

Therefore:

```text
KNOWN_SOLUTION_BASELINE=94_PASSED
REPOSITORY_BLOCKING_REGRESSION=NO
```

Do not assume that the 010E-O through 010E-Y gates exist as permanent `simulations/*.py` files.

They were primarily analytical preflights.

Their scientific conclusions should be preserved in `NOTES.md` before terminal history is lost.

---

# 5. Strongest established project result remains 006D

The central 006D construction uses axisymmetric anisotropic stress.

Define:

```math
q(r)
=
r p_r(r)
```

and choose:

```math
p_\phi(r)
=
\frac{dq}{dr}
```

with:

```math
p_z=0
```

For a static diagonal axisymmetric stress tensor, radial conservation is:

```math
\frac{dp_r}{dr}
+
\frac{p_r-p_\phi}{r}
=
0
```

Because:

```math
p_r
=
\frac{q}{r}
```

we have:

```math
\frac{dp_r}{dr}
=
\frac{q'}{r}
-
\frac{q}{r^2}
```

and:

```math
\frac{p_r-p_\phi}{r}
=
\frac{q}{r^2}
-
\frac{q'}{r}
```

Therefore:

```math
\frac{dp_r}{dr}
+
\frac{p_r-p_\phi}{r}
=
0
```

identically.

This is not merely a numerically optimized integrated balance. Local radial conservation is built into the stress profile at the stated approximation order.

Choose the positive energy density:

```math
\epsilon
=
\max
\left(
|p_r|,
|p_\phi|
\right)
```

with $p_z=0$.

For type-I matter, the dominant energy condition requires:

```math
\epsilon\ge0
```

and:

```math
|p_i|\le\epsilon
```

for every principal pressure.

The above choice therefore enforces:

```math
\epsilon\ge|p_r|
```

```math
\epsilon\ge|p_\phi|
```

```math
\epsilon\ge|p_z|=0
```

so DEC holds by construction.

DEC implies WEC, and for this type-I structure the relevant NEC inequalities are also satisfied:

```math
\epsilon+p_i\ge0
```

The actual numerical source was regularized to finite radial support and finite vertical thickness.

Verified numerical diagnostics include:

```text
MAX_CONTROL_VOLUME_CONSERVATION_RESIDUAL=
3.103073353827e-14

MAX_DEC_VIOLATION=
0

MIN_NEC_MARGIN=
0

MAX_INTEGRATED_STRESS_TRACE=
2.922107000813e-13
```

The zero NEC margin means the optimized configuration saturates an energy-condition boundary in some regions. It does not mean the NEC test was absent.

The axial weak-field Green-function acceleration is of the schematic form:

```math
a_z(h)
=
-\frac{2\pi G}{c^2}
\int dz
\int_0^\infty dr\,
r
\left(
\epsilon+p_r+p_\phi+p_z
\right)
\frac{h-z}
{\left[r^2+(h-z)^2\right]^{3/2}}
```

The calculated near field is outward.

The integrated active mass remains positive, so the far field remains attractive.

Best tested finite-thickness coefficient:

```math
C_{\mathrm{finite}}
=
23.591586299249
```

with:

```math
M_{\mathrm{equiv}}
=
C\frac{ah^2}{G}
```

Thin-limit result:

```math
C_{\mathrm{thin}}
=
23.426710175391
```

The finite source differs from the thin limit by approximately:

```math
\frac{
23.591586299249
-
23.426710175391
}{
23.426710175391
}
\approx
7.04\times10^{-3}
```

or about:

```math
0.704\%
```

For a $1g$ effect at $h=1,{\mathrm{m}}$:

```math
M
=
23.591586299249
\frac{
9.80665\times(1\,{\mathrm{m}})^2
}{
6.67430\times10^{-11}
}
```

which gives approximately:

```math
M
\approx
3.47\times10^{12}\ {\mathrm{kg}}
```

The corresponding rest-energy equivalent is approximately:

```math
E
=
Mc^2
\approx
3.12\times10^{29}\ {\mathrm{J}}
```

This illustrates why 006D establishes mathematical repulsion but not energetic practicality.

Correct 006D classifications:

```text
MATHEMATICAL_LOCAL_REPULSION=ESTABLISHED
FINITE_POSITIVE_ENERGY_LINEARIZED_GR_CONSTRUCTION=ESTABLISHED
LOCAL_CONSERVATION_LINEARIZED_ORDER=ESTABLISHED
NEC_WEC_DEC=PASS
OUTWARD_LOCAL_GRAVITATIONAL_FIELD=ESTABLISHED
POSITIVE_FAR_FIELD_ACTIVE_MASS=ESTABLISHED

EXACT_NONLINEAR_GR_REALIZATION=NOT_ESTABLISHED
EXACT_NONLINEAR_CONSERVATION=NOT_ESTABLISHED
DYNAMIC_STABILITY=NOT_ESTABLISHED
KNOWN_MATERIAL_REALIZATION=NO
ENERGETIC_PRACTICALITY=NO
PRACTICAL_ANTIGRAVITY_DEVICE=NO
NEW_PHYSICS_DISCOVERY=NO
```

---

# 6. Important classical static scaling theorem from 010E-A

The late classical analysis produced a useful standoff bound for a static, finite, one-sided, locally conserved DEC source.

The result is:

```math
a_{\mathrm{out}}
\le
\frac{GE}{c^2h^2}
```

Since:

```math
M
=
\frac{E}{c^2}
```

this becomes:

```math
a_{\mathrm{out}}
\le
\frac{GM}{h^2}
```

Therefore:

```math
M
\ge
\frac{ah^2}{G}
```

under the stated assumptions.

For $a=g$ and $h=1,{\mathrm{m}}$:

```math
M_{\min}
=
\frac{9.80665}
{6.67430\times10^{-11}}
```

giving:

```math
M_{\min}
\approx
1.4693\times10^{11}\ {\mathrm{kg}}
```

Thus even the optimistic coefficient-one static-DEC limit is catastrophically large at meter standoff.

006D is roughly:

```math
23.59
```

times that coefficient-one bound.

This is why further small improvements in the 006D coefficient are not currently high-value unless a new mechanism changes the scaling itself.

---

# 7. Nonlinear-GR correction gate

At acceleration $a$ across distance $h$, a useful dimensionless weak-field parameter is:

```math
\frac{ah}{c^2}
```

For $a=g$ and $h=1,{\mathrm{m}}$:

```math
\frac{gh}{c^2}
=
\frac{
9.80665
}{
(2.99792458\times10^8)^2
}
```

which gives approximately:

```math
1.09\times10^{-16}
```

Therefore ordinary Einstein nonlinear corrections at this target field strength are tiny.

The project accordingly rejected:

```text
PURE_EINSTEIN_NONLINEAR_CORRECTION_ESCAPE_FOR_006D
```

as a path to fixing the enormous classical mass scale.

A strongly nonlinear additional matter field can still exist in a weak metric, but that becomes a new-field problem rather than a pure nonlinear-GR escape.

---

# 8. Important prior branch conclusions that should not be reopened casually

Before the late 010E material work, the project had already established or strongly supported the following.

## 8.1 Cosmological constant

Kottler/Schwarzschild-de Sitter repulsion exists.

It is far too weak at laboratory scale.

## 8.2 Perfect-fluid negative pressure

For:

```math
p=w\epsilon
```

positive-energy gravitational defocusing occurs for:

```math
w<-\frac13
```

but the required energy density for laboratory-scale acceleration is enormous.

## 8.3 Negative Schwarzschild/ADM mass

Provides outward exterior acceleration mathematically.

The tested shell construction required negative shell energy and violated WEC/DEC.

Not a preferred physical route.

## 8.4 Reissner-Nordström

Positive ADM mass plus Maxwell energy can give a locally repulsive region for neutral particles.

The electric fields required for practical-scale effects are catastrophic.

## 8.5 Tension/domain-wall sources

Positive-energy tension can produce local repulsion.

Finite supported versions survive energy conditions but remain energetically catastrophic.

## 8.6 Casimir / free-QFT negative energy

The ideal Casimir vacuum contribution has the correct local sign.

Complete apparatus and quantum-energy-inequality constraints make macroscopic usefulness effectively hopeless in the tested established-QFT routes.

## 8.7 Healthy scalar-tensor and positive-residue spin-2 modifications

Standard healthy scalar exchange between same-sign masses adds attraction.

Healthy positive-residue spin-2 exchange also adds attraction.

Wrong-sign spin-2 solutions introduce ghosts.

## 8.8 Spontaneous scalarization / screening

Laboratory scalarization at ordinary compactness was rejected.

K-mouflage/nDGP-type screening suppresses deviations toward GR rather than naturally reversing gravity.

## 8.9 Reactionless internal self-thrust

An isolated conservative internal system cannot accelerate its total center of energy.

The present fifth-force branch is ground/Earth referenced and therefore uses the Earth/environment as momentum reservoir.

It is not reactionless propulsion.

---

# 9. Working fifth-force benchmark entering late 010E

The late 010E branch used a phenomenological Yukawa scalar with range:

```math
\lambda
=
5000\ {\mathrm{m}}
```

and pure-Yukawa strength:

```math
\alpha_Y
=
2.0\times10^{-4}
```

The working source coupling is defined through:

```math
\alpha_{\mathrm{source}}
=
\sqrt{
\frac{\alpha_Y}{2}
}
```

Therefore:

```math
\alpha_{\mathrm{source}}
=
10^{-2}
```

For a thick source approximated as a half-space with density $\rho$, the scalar acceleration was modeled as:

```math
a_\phi
=
-4\pi G
\rho
\alpha_{\mathrm{source}}
\alpha_{\mathrm{test}}
\lambda
```

Using:

```text
rho = 3000 kg/m^3
lambda = 5000 m
alpha_source = 0.01
```

and demanding approximately $1g$ upward acceleration gives:

```math
\alpha_{\mathrm{activated}}
=
-
\frac{
g
}{
4\pi G
\rho
\alpha_{\mathrm{source}}
\lambda
}
```

Numerically:

```text
ALPHA_ACTIVATED=
-1.558991777087370e5
```

This is an enormous effective test-body scalar response.

The mediator mass corresponding to the $5,{\mathrm{km}}$ range is:

```math
m_\phi
=
\frac{\hbar c}{\lambda}
```

Using:

```math
\hbar c
\approx
1.973269804\times10^{-7}\ {\mathrm{eV\,m}}
```

gives:

```math
m_\phi
=
3.946539608\times10^{-11}\ {\mathrm{eV}}
```

The extra dimensionless microscopic scalar coupling per nucleon required by the activated state is:

```math
g_N
\sim
|\Delta\alpha|
\frac{m_N}{M_{\mathrm{Pl}}}
```

with:

```text
m_N = 0.939 GeV
M_Pl,reduced = 2.435e18 GeV
```

which gives:

```text
ACTIVATED_EXTRA_COUPLING_PER_NUCLEON=
6.011882433614129e-14
```

This small microscopic number should not be confused with the enormous macroscopic $\alpha_{\mathrm{activated}}$. The macroscopic enhancement arises from coherent mass-normalized scalar charge.

---

# 10. Experimental status of the 5-km working point

The historical ocean result used by the project provides a conservative approximate pure-Yukawa ceiling:

```math
\alpha_Y
<
2\times10^{-3}
```

through the relevant intermediate-range region.

The selected point:

```math
\alpha_Y
=
2\times10^{-4}
```

is therefore a factor:

```math
\frac{
2\times10^{-3}
}{
2\times10^{-4}
}
=
10
```

below that historical ceiling.

The 2026 inverse-square-law review visually appears consistent with the selected point.

However:

```text
CURRENT_EXACT_2026_5KM_NUMERICAL_MARGIN=NOT_CLOSED
```

The exact modern curve has not been reconstructed from machine-readable data.

Do not state that the present benchmark is definitively allowed by a quantified 2026 margin until either:

1. the numerical source data are obtained, or
2. the curve is independently digitized with uncertainty.

This remains a potentially branch-fatal empirical gate.

---

# 11. Late-session chronology overview

The late session followed this progression:

```text
010E-O
explicit microscopic Z2-even lattice model

010E-P
light hidden-carrier matching

010E-Q
point-carrier localization no-go
compact-phase replacement

010E-R
unique hidden vacuum
material-gated host portal

010E-S
invariant control-burden optimization

010E-T
real gauge-invariant electronic high-spin projector

010E-U
direct electron mediator rejected
spin-lattice bridge survives

010E-V
finite-size scalar stability correction
hidden compact phase becomes unnecessary

010E-W
off-state thermal purity and material selectivity

010E-X
cooperative exact-selector cluster window

010E-Y
local NR composite matching
Feynman-Hellmann
two-body contact representation
generic relativistic UV failure
```

The most important strategic fact is that many apparently promising intermediate constructions were intentionally abandoned when a cheaper or more fundamental issue was found.

Do not restart O/P/Q/R/S merely because those gates were GREEN.

Several of their physical interpretations were superseded.

---

# 12. 010E-O — explicit microscopic Z2-even lattice phase

O replaced an arbitrary continuous state-dependent coupling with a discrete microscopic occupation construction.

Reference material cell:

```text
NUCLEONS_PER_CELL=100
CELL_SPACING_M≈5.49646e-10
```

An exact even occupation operator gave identical charge for the two activated signs and zero/ordinary charge in the normal state.

Representative model parameters:

```text
LATTICE_J_EV=1
LATTICE_D_EV=3
```

Scalar/environmental energy per reference cell:

```text
EXTERNAL_SCALAR_BIAS_CELL_EV≈0.10164
```

Switching energy:

```text
SWITCH_CONTROL_CELL_EV≈0.20328
```

Microscopic wall tension:

```text
LATTICE_WALL_TENSION_J_M2≈0.5303
```

Critical bubble radius:

```text
R_c≈1.08e-8 m
```

Critical bubble barrier:

```text
≈1622 eV
```

O established that an explicit microscopic low-energy first-order model could reproduce the required state-dependent scalar charge without relying on an arbitrary polynomial interpolation.

However, O did not establish a real material or UV origin.

---

# 13. 010E-P — hidden light carrier matching

P attempted to explain the activated cell charge through approximately one hidden carrier associated with each material cell.

A two-scalar matching model was constructed with a light hidden carrier and a heavier scalar.

Representative values included:

```text
HIDDEN_CARRIER_MASS≈1 eV
SIGMA_MASS≈0.3 eV
YUKAWA≈0.3
HIDDEN_CUTOFF≈5 eV
```

The low-energy scalar coupling could be reproduced parametrically.

However, a later localization analysis invalidated the pointlike-carrier interpretation.

Therefore:

```text
010E_P_LOCALIZED_POINT_CARRIER_INTERPRETATION=SUPERSEDED_AND_REJECTED
```

Do not revive P without solving the localization/naturalness problem.

---

# 14. 010E-Q — localization no-go

For a 100-nucleon reference cell, spacing:

```math
a
=
5.496459502753594\times10^{-10}\ {\mathrm{m}}
```

A $1,{\mathrm{eV}}$ particle has reduced Compton wavelength:

```math
\bar\lambda_C
=
\frac{\hbar c}{m}
```

which gives:

```math
\bar\lambda_C
\approx
1.97327\times10^{-7}\ {\mathrm{m}}
```

Therefore:

```math
\frac{\bar\lambda_C}{a}
\approx
359
```

Localizing such a particle to one cell requires characteristic momentum:

```math
pc
\sim
\frac{\hbar c}{a}
\approx
359\ {\mathrm{eV}}
```

The exact relativistic localization kinetic energy is:

```math
T
=
\sqrt{
p^2c^2+m^2c^4
}
-
mc^2
```

which gives approximately:

```text
358 eV
```

for $m=1,{\mathrm{eV}}$.

That is vastly above the intended $5,{\mathrm{eV}}$ matching cutoff.

Demanding localization kinetic energy $\le5,{\mathrm{eV}}$ requires:

```text
m_X >= 1.2886e4 eV
```

while unprotected scalar naturalness gave approximately:

```text
m_X <= 58.33 eV
```

Hence:

```math
\frac{
m_{\mathrm{localization,min}}
}{
m_{\mathrm{naturalness,max}}
}
\approx
221
```

for the 100-nucleon cell.

Even one carrier per nucleon did not close the gap.

Decision:

```text
ONE_POINTLIKE_UNPROTECTED_CARRIER_PER_CELL=
REJECTED_BY_LOCALIZATION_NATURALNESS_NO_OVERLAP
```

This was a genuine negative result.

---

# 15. 010E-Q compact-phase replacement

Q replaced localized particles with a collective relative phase.

Two hidden condensates were written schematically as:

```math
\Psi
=
f e^{i\theta}
```

and:

```math
H=f
```

The difference portal was:

```math
V_{\mathrm{portal}}
=
\epsilon\phi
|\Psi-H|^2
```

Since:

```math
|\Psi-H|^2
=
2f^2
(1-\cos\theta)
```

the normal state $\theta=0$ gives zero extra scalar source while $\theta=\pi$ gives maximal source.

The source derivative is proportional to:

```math
\sin\theta
```

and therefore vanishes at both endpoints.

This removed the arbitrary continuous $\alpha(s)$ function.

Representative Q benchmark:

```text
f=10 keV
phase cutoff=200 eV
radial mass=10 keV
```

Portal coefficient:

```text
epsilon≈6.95e-13 eV
```

Full conservative portal-loop correction:

```text
≈1.57e-5 of target m_phi^2
```

Radial threshold correction:

```text
≈9.94e-3 of target m_phi^2
```

Thus the low-energy compact phase passed its first naturalness checks.

However, creating the full hidden condensate from zero inside matter cost roughly:

```text
2.61e13 J/kg
```

which is catastrophic.

Therefore only:

```text
PREEXISTING_HIDDEN_CONDENSATE_RELATIVE_PHASE_CONTROL
```

survived.

---

# 16. 010E-R — unique hidden vacuum and emergent host portal

The original compact-phase potential had two degenerate minima.

R added an explicit bias:

```math
V_{\mathrm{vac}}(\theta)
=
V_0\sin^2\theta
+
\Delta V_{\mathrm{vac}}
\frac{1-\cos\theta}{2}
```

Endpoint curvatures are:

```math
V''(0)
=
2V_0
+
\frac{
\Delta V_{\mathrm{vac}}
}{2}
```

and:

```math
V''(\pi)
=
2V_0
-
\frac{
\Delta V_{\mathrm{vac}}
}{2}
```

Therefore:

```math
\Delta V_{\mathrm{vac}}
>
4V_0
```

makes $\theta=\pi$ cease to be a local vacuum.

The selected benchmark used:

```math
\Delta V_{\mathrm{vac}}
=
5V_0
```

which gave:

```text
VACUUM_BIAS_OVER_4V0=1.25
VACUUM_SECOND_LOCAL_MINIMUM_AT_PI=NO
```

This removed the tree-level degenerate-vacuum/domain-wall issue inside the toy model.

R then introduced a generic material host field $\chi$.

However, because an unmatched composite field can be rescaled, the apparently tiny individual $\chi$ coupling was later recognized as not itself an invariant physical achievement.

That motivated S.

---

# 17. 010E-S — invariant control-burden optimization

S replaced arbitrary host-field normalization with invariant energy density and energy per material cell.

The compact-phase model:

```math
V(\theta)
=
V_0\sin^2\theta
+
b
\frac{1-\cos\theta}{2}
```

was optimized subject to:

* unique normal vacuum;
* finite thermal phase mass;
* finite nucleation radius;
* thin-wall consistency;
* portal naturalness;
* radial naturalness;
* perturbative radial self-coupling.

The hidden phase scale had a hard floor:

```text
PHASE_F_HARD_MIN_EV≈7071
```

and S chose:

```text
PHASE_F_EV=8000
```

Key optimized values:

```text
OPTIMIZED_CONTROL_DRIVE_OVER_EXTERNAL≈0.0279812
OPTIMIZED_V0_OVER_EXTERNAL≈0.461741
OPTIMIZED_VACUUM_BIAS_OVER_EXTERNAL≈1.93931
OPTIMIZED_TOTAL_CONTROL_OVER_EXTERNAL≈2.96729
```

This reduced the total control free-energy density to:

```text
2.90992e8 J/m^3
```

or:

```text
2.90992e5 J/kg
```

For a one-ton benchmark:

```text
2.90992e8 J
```

The physical host-hidden cross energy became:

```text
0.301592 eV
```

per 100-nucleon reference cell.

This was a large reduction from R.

But the host operator was still abstract.

---

# 18. 010E-T — real electronic spin-crossover projector

T introduced a concrete low-energy electronic observable.

For total spin $S$, define:

```math
x
=
S(S+1)
```

and in the truncated $S=0,1,2$ manifold:

```math
P_{\mathrm{HS}}
=
\frac{
x(x-2)
}{
24
}
```

Then:

```math
P_{\mathrm{HS}}(S=0)
=
0
```

```math
P_{\mathrm{HS}}(S=1)
=
0
```

```math
P_{\mathrm{HS}}(S=2)
=
1
```

Thus the high-spin state can be selected by an exact projector inside the truncated electronic Hilbert space.

This observable is:

```text
U(1)_EM gauge invariant
rotationally invariant
time-reversal even
```

The compact phase function:

```math
q(\theta)
=
\frac{
1-\cos\theta
}{2}
```

has:

```math
q'(0)=0
```

and:

```math
q'(\pi)=0
```

so there is no linear single-phase-quantum vertex at either endpoint.

T compared the required cross-energy scale with Fe many-body scales:

```text
U≈5 eV
J_H≈0.85 eV
```

A dense site near 72 nucleons requires approximately:

```text
0.217 eV
```

of host-hidden energy.

Thus the energy scale itself is not absurd relative to strongly correlated electronic physics.

However, T also killed the simplest direct electron-mass portal.

Required fractional electron-mass modulation:

```text
≈1.18e-8
```

looks small, but the Coleman-Weinberg scale associated with the electron mass produced:

```text
ELECTRON_CW_TO_REQUIRED_CONTROL_RATIO≈1.46e6
```

Decision:

```text
DIRECT_UNPROTECTED_ELECTRON_MASS_PORTAL=
REJECTED_BY_PHASE_POTENTIAL_NATURALNESS
```

---

# 19. 010E-U — Hund-scale map, electron mediator no-go, spin-lattice bridge

The rotationally invariant Kanamori spin term contains:

```math
-2J_H\mathbf{S}^2
```

For:

```math
S_{\mathrm{LS}}=0
```

and:

```math
S_{\mathrm{HS}}=2
```

the difference in $S(S+1)$ is:

```math
6
```

so the spin-term energy difference is parametrically:

```math
\Delta E
=
-12J_H
```

For the FeO-like active-site benchmark, required control energy:

```text
0.216676 eV/site
```

corresponds to a Hund-scale change of:

```math
\delta J_H
\sim
\frac{
0.216676
}{
12
}
\approx
0.01806\ {\mathrm{eV}}
```

Relative to:

```math
J_H\approx0.85\ {\mathrm{eV}}
```

this is approximately:

```math
\frac{
0.01806
}{
0.85
}
\approx
2.12\%
```

This was an encouraging energy-scale comparison only, not a microscopic derivation.

U then tested a direct short-range electron mediator.

The required contact interaction was translated into an electron-boson coupling and checked against the electron anomalous magnetic moment.

Best-case result for an aggressive $0.3,\mathrm{\AA}$ orbital:

```text
BEST_CASE_ABS_DELTA_A_E=
2.5235e-6
```

against a deliberately loose acceptable scale:

```text
1e-12
```

giving:

```text
EXCLUSION_FACTOR≈2.52e6
```

The $1,\mathrm{\AA}$ case was worse:

```text
EXCLUSION_FACTOR≈1.04e7
```

Decision:

```text
SIMPLE_SINGLE_FUNDAMENTAL_ELECTRON_CURRENT_MEDIATOR=
REJECTED_BY_G_MINUS_2_PREFLIGHT
```

U then used a physical structural coordinate:

```math
E(x,P,q)
=
\frac12Kx^2
-
F_sPx
-
F_hqx
```

with observed spin-crossover displacement scale:

```math
\Delta x
\sim
0.2\ {\mathrm{\AA}}
```

Since:

```math
F_s
=
K\Delta x
```

integrating out $x$ gives a cross term:

```math
J_{\mathrm{cross}}
=
\frac{
F_sF_h
}{
K
}
=
\Delta x F_h
```

For representative stiffness:

```text
K=20 eV/A^2
```

U found:

```text
REQUIRED_HIDDEN_PHASE_FORCE≈0.9666 eV/A
```

or:

```text
≈1.55e-9 N
```

The induced structural displacement was:

```text
≈0.0483 A
```

and the phonon energy:

```text
≈0.0864 eV
```

This showed that the required material-scale force was chemically ordinary in magnitude inside the low-energy model.

But the fundamental origin of that force remained absent.

---

# 20. 010E-V — finite-size scalar-stability correction

V made one of the most important conceptual corrections of the entire late session.

Earlier reasoning often treated:

```math
m_{\mathrm{eff}}^2<0
```

inside material as immediate instability.

That criterion is appropriate for an infinite homogeneous medium.

A finite body instead requires a spatial eigenmode capable of fitting inside the material.

For a spherical region of radius $R$ with interior effective mass:

```math
m_{\mathrm{in}}^2
=
-\mu^2
```

and ordinary exterior mediator mass:

```math
m_{\mathrm{out}}
=
m_\phi
```

write:

```math
\phi(r)
=
\frac{
u(r)
}{
r
}
```

The regular interior zero-mode solution is:

```math
u_{\mathrm{in}}
\propto
\sin(\mu r)
```

The decaying exterior solution is:

```math
u_{\mathrm{out}}
\propto
e^{-m_\phi(r-R)}
```

Matching logarithmic derivatives at $r=R$ gives:

```math
\mu
\cot(\mu R)
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

For the one-ton benchmark with density $1000,{\mathrm{kg/m^3}}$:

```text
PAYLOAD_RADIUS_M=
0.6203504908994001
```

and:

```text
m_phi R≈1.2407e-4
```

so the first zero-mode threshold is very close to:

```math
\frac{\pi}{2}
```

Numerically:

```text
FINITE_SPHERE_ZERO_MODE_X_CRITICAL=
1.570875308300910
```

The representative $K=20,{\mathrm{eV/\AA^2}}$ model had worst combined susceptibility:

```text
MU_R=
0.3649986914819186
```

Therefore stability margin:

```math
\frac{
1.5708753
}{
0.3649987
}
\approx
4.304
```

The estimated critical radius was:

```text
2.66985 m
```

and corresponding mass at $1000,{\mathrm{kg/m^3}}$:

```text
7.97e4 kg
```

Thus the one-ton benchmark passed this finite-size stability preflight even though the local infinite-medium mass-squared criterion would have rejected it.

This allowed the hidden compact phase to be removed from the leading low-energy branch.

That was an important simplification.

---

# 21. Direct state-gated scalar/phonon coupling after V

V used:

```math
E(x,P,\Phi)
=
\frac12Kx^2
-
F_sPx
+
c\Phi Px
```

where:

* $P=0$ is low spin;
* $P=1$ is high spin;
* $\Phi$ is the magnitude of the terrestrial scalar background;
* $c$ is the state-gated scalar/phonon coefficient.

For $P=1$, minimizing with respect to $x$ gives:

```math
x_{\mathrm{HS}}
=
\Delta x
-
\frac{
c\Phi
}{
K
}
```

The scalar charge magnitude is:

```math
g_{\mathrm{site}}
=
c x_{\mathrm{HS}}
```

so:

```math
g_{\mathrm{site}}
=
c
\left(
\Delta x
-
\frac{
c\Phi
}{
K
}
\right)
```

This quadratic relation was solved exactly for $c$.

For:

```text
K=20 eV/A^2
```

the gate found:

```text
DIRECT_SCALAR_PHONON_COEFFICIENT_PER_A=
2.403813617458705e-11

SCALAR_INDUCED_BOND_FORCE_EV_PER_A=
0.4063962494963003

SCALAR_INDUCED_BOND_FORCE_N=
6.511185750882065e-10

ACTIVATED_BOND_DISPLACEMENT_A=
0.1796801875251850
```

The scalar activation energy penalty was:

```text
0.07715030210914353 eV/site
```

The desired activated-state free-energy advantage was:

```text
0.002043222608870487 eV/site
```

Thus a near-coexistence material would need approximately:

```text
0.07919352471801402 eV/site
```

of ordinary control in the idealized low-energy model.

At this point it looked much cheaper than the hidden compact-phase architecture.

W later showed that this conclusion was incomplete because off-state purity matters.

---

# 22. 010E-W — thermal off-state purity

The activated scalar charge is huge.

Therefore even an extremely small equilibrium population of activated/high-spin material in the off state can violate fifth-force limits.

The conservative leakage fraction inherited from the historical Yukawa bound is:

```text
MAXIMUM_PORTAL_LEAKAGE_FRACTION=
5.772961445324848e-7
```

For Fe(II):

```math
S_{\mathrm{LS}}=0
```

```math
S_{\mathrm{HS}}=2
```

The minimal spin multiplicities are:

```math
g_{\mathrm{LS}}
=
2S_{\mathrm{LS}}+1
=
1
```

and:

```math
g_{\mathrm{HS}}
=
2S_{\mathrm{HS}}+1
=
5
```

For total free-energy gap $\Delta$:

```math
p_{\mathrm{HS}}
=
\frac{
5e^{-\Delta/k_BT}
}{
1+5e^{-\Delta/k_BT}
}
```

Demand:

```math
p_{\mathrm{HS}}
\le
f_{\mathrm{leak}}
```

Solving gives:

```math
\Delta
\ge
k_BT
\ln
\left[
\frac{
5(1-f_{\mathrm{leak}})
}{
f_{\mathrm{leak}}
}
\right]
```

At $300,{\mathrm{K}}$:

```text
REQUIRED_TOTAL_OFF_STATE_GAP=
0.4129688356163971 eV
```

The scalar penalty already supplies:

```text
0.07715030210914353 eV
```

so additional ordinary material gap required is:

```text
0.3358185335072536 eV
```

The total control shift becomes:

```text
0.4150120582252676 eV/site
```

or for the one-ton reference:

```text
5.57354e8 J
```

Thus:

```text
ROOM_TEMPERATURE_NEAR_COEXISTENCE_DIRECT_ROUTE=
REJECTED_BY_OFF_STATE_THERMAL_LEAKAGE
```

At $77,{\mathrm{K}}$:

```text
REQUIRED_TOTAL_OFF_STATE_GAP=
0.1059953344748753 eV
```

and total control:

```text
0.1080385570837458 eV/site
```

At $4.2,{\mathrm{K}}$ the scalar penalty alone makes the activated thermal fraction negligible.

But X later showed that very low temperature worsens switching-point scalar susceptibility.

Therefore colder is not monotonically better.

---

# 23. 010E-W — continuous structural selector failures

W tested whether structural variables alone could suppress the unwanted scalar charge sufficiently.

The target leakage level is:

```math
f_{\mathrm{leak}}
\approx
5.77\times10^{-7}
```

## Linear structural selector

Scalar-induced normal displacement:

```text
0.0203198 A
```

Activated displacement:

```text
0.179680 A
```

Thus leakage:

```math
f_{\mathrm{linear}}
=
\frac{
0.0203198
}{
0.179680
}
\approx
0.11309
```

Relative to allowed leakage:

```math
\frac{
0.11309
}{
5.77\times10^{-7}
}
\approx
1.96\times10^5
```

Therefore:

```text
LINEAR_STRUCTURAL_SELECTOR_WITHOUT_PROJECTOR=REJECTED
```

## Even analytic monomials

For:

```math
g_n(x)
\propto
x^{2n}
```

a Gaussian oscillator has:

```math
\langle x^{2n}\rangle
=
(2n-1)!!
\sigma^{2n}
```

Quantum zero-point fluctuations therefore produce nonzero normal-state charge even when:

```math
\langle x\rangle=0
```

Best tested order at $300,{\mathrm{K}}$:

```text
n=7
```

with leakage:

```text
1.330943115663350e-3
```

Excess:

```text
≈2305
```

times the conservative allowance.

## Normal-ordered quadratic

Cancelling the $T=0$ zero-point expectation by hand still leaves thermal leakage:

```text
5.256338715769595e-3
```

or:

```text
≈9105
```

times too large.

Therefore:

```text
SIMPLE_CONTINUOUS_STRUCTURAL_SELECTOR_IN_TESTED_CLASSES=REJECTED
```

This is why the discrete projector architecture became essential.

---

# 24. Universal high-spin selector also rejected

If every ordinary high-spin site in matter possessed the enormous activated scalar charge, ordinary matter would already violate the conservative fifth-force limit.

Maximum target-equivalent active fraction:

```text
5.772961445324848e-7
```

or:

```text
0.577296 ppm
```

Therefore:

```text
UNIVERSAL_HIGH_SPIN_SCALAR_PORTAL=REJECTED
```

The interaction must be material specific.

This is a critical requirement.

It is not enough to say:

```text
HIGH_SPIN = ANTIGRAVITY
```

The survivor requires something more like:

```text
SPECIFIC_BOUND_MATERIAL_IDENTITY
AND
SPECIFIC_INTERNAL HIGH-SPIN CONFIGURATION
```

---

# 25. Approximate material identity is difficult

W modeled mixing between a target configuration $|T\rangle$ and ordinary configuration $|O\rangle$:

```math
H
=
\begin{pmatrix}
0&t\\
t&\Delta
\end{pmatrix}
```

The target-state admixture in the lower eigenstate is:

```math
p_T
=
\frac12
\left(
1
-
\frac{
\Delta
}{
\sqrt{
\Delta^2+4t^2
}
}
\right)
```

Requiring:

```math
p_T
\le
f_{\mathrm{leak}}
```

gives approximately:

```math
\frac{\Delta}{t}
\gtrsim
1316
```

or:

```math
\frac{t}{\Delta}
\lesssim
7.60\times10^{-4}
```

Therefore generic weakly distinct orbital/environment labels are not automatically enough.

An exact or strongly symmetry-protected material selector is preferred.

---

# 26. 010E-X — factorized exact selector

X resolved the apparent contradiction between:

```text
exact material identity
```

and:

```text
switchability
```

by separating them.

Define:

```math
Q_N
=
B_{\mathrm{material}}
\prod_{i=1}^N
P_{{\mathrm{HS}},i}
```

where:

* $B_{\mathrm{material}}$ is a fixed projector onto a specific bound material/cluster species;
* $P_{{\mathrm{HS}},i}$ are switchable high-spin projectors.

Then it is possible to have:

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

An explicit matrix model gave:

```text
MATERIAL_IDENTITY_CONTROL_COMMUTATOR_NORM=
0

PORTAL_PROJECTOR_CONTROL_COMMUTATOR_NORM=
1.414213562373095
```

Therefore the material identity can remain exact while the internal state—and thus scalar response—is switched.

This was an important logical result.

---

# 27. Product projector versus accidental polynomial tuning

For binary high-spin occupation variables:

```math
P_i\in\{0,1\}
```

the exact all-high-spin selector is:

```math
Q_N
=
\prod_iP_i
```

It can also be represented algebraically using total occupation:

```math
n
=
\sum_iP_i
```

through a falling-factorial polynomial.

But implementing that polynomial as unrelated Wilson coefficients would require severe cancellation precision.

X found:

```text
N=2:
MAX_INDEPENDENT_COEFFICIENT_ERROR≈5.77e-7

N=4:
≈3.85e-8

N=11:
≈3.44e-12
```

Therefore:

```text
GENERIC_EXPANDED_POLYNOMIAL_SELECTOR=
REJECTED_AS_UNPROTECTED_FINE_TUNING
```

The physical survivor must use a genuine product projector, bound-state identity, exact selection rule, or equivalent protected structure.

---

# 28. Cooperative cluster leakage scaling

For an $N$-site all-high-spin cluster with only scalar activation penalty $E_s$ per site, a conservative weight is:

```math
W_N
=
5^N
\exp
\left(
-\frac{
NE_s
}{
k_BT
}
\right)
```

and:

```math
p_{\mathrm{all-HS}}
\le
\frac{
W_N
}{
1+W_N
}
```

Thus leakage decreases approximately exponentially with $N$.

This gives a lower bound:

```math
N
\ge
N_{\min}
```

from off-state purity.

---

# 29. Cooperative cluster susceptibility scaling

The scalar-charge difference of an $N$-site cluster is:

```math
G_N
=
Ng_{\mathrm{site}}
```

The number density of clusters is:

```math
n_{\mathrm{cluster}}
=
\frac{
n_{\mathrm{site}}
}{
N
}
```

At maximal equilibrium two-state susceptibility:

```math
|\Delta m_\phi^2|
=
\frac{
n_{\mathrm{cluster}}
G_N^2
}{
4k_BT
}
```

Substitute:

```math
n_{\mathrm{cluster}}
=
\frac{
n_{\mathrm{site}}
}{
N
}
```

and:

```math
G_N^2
=
N^2g_{\mathrm{site}}^2
```

to obtain:

```math
|\Delta m_\phi^2|
=
N
\frac{
n_{\mathrm{site}}
g_{\mathrm{site}}^2
}{
4k_BT
}
```

Thus susceptibility grows linearly with cluster size $N$.

Finite-size stability therefore produces an upper bound:

```math
N
\le
N_{\max}
```

The coexistence of:

```math
N_{\min}
\le
N
\le
N_{\max}
```

is the cluster-selector window.

---

# 30. X selector window results

For the one-ton spherical benchmark:

```text
300 K:
N_MIN_LEAKAGE=11
N_MAX_STABILITY=21

200 K:
N_MIN=6
N_MAX=14

150 K:
N_MIN=4
N_MAX=10

100 K:
N_MIN=2
N_MAX=7

95 K:
N_MIN=2
N_MAX=6

77 K:
N_MIN=2
N_MAX=5

50 K:
N_MIN=1
N_MAX=3

30 K:
N_MIN=1
N_MAX=2

20 K:
N_MIN=1
N_MAX=1

10 K:
NO WINDOW

4.2 K:
NO WINDOW
```

This produced an important non-intuitive result:

> **Arbitrarily colder is not always better.**

Off-state thermal leakage improves as $T$ decreases.

But switching-point scalar susceptibility scales as:

```math
\chi_\phi
\propto
\frac1T
```

and therefore worsens at very low temperature.

---

# 31. Dinuclear selector is the lowest-complexity survivor

For $N=2$, the model-side allowed temperature interval is:

```text
DINUCLEAR_STABILITY_T_MIN_K=
28.13102372293623

DINUCLEAR_LEAKAGE_T_MAX_K=
101.8315502857560
```

Thus:

```math
28.13\ {\mathrm{K}}
<
T
<
101.83\ {\mathrm{K}}
```

for the selected idealized one-ton benchmark without extra off-state material gap.

At $77,{\mathrm{K}}$:

```text
DINUCLEAR_ALL_HS_LEAKAGE=
1.989338055378181e-9
```

Relative to:

```text
5.772961445324848e-7
```

the leakage margin is:

```math
\frac{
5.772961445324848\times10^{-7}
}{
1.989338055378181\times10^{-9}
}
\approx
290.2
```

Finite-size susceptibility:

```text
DINUCLEAR_77K_MU_R=
0.9556137730170507
```

Threshold:

```text
1.570875308300910
```

Thus stability margin:

```math
\frac{
1.570875308300910
}{
0.9556137730170507
}
\approx
1.644
```

Maximum tolerated multiplicative susceptibility enhancement:

```text
≈2.737
```

before the finite-size threshold is reached.

Therefore:

```text
DINUCLEAR_BOUND_CLUSTER_SELECTOR=
CURRENT_LOWEST_COMPLEXITY_LOW_ENERGY_SURVIVOR
```

This is a model conclusion, not identification of an actual material.

---

# 32. Balanced dinuclear point

X solved for a temperature where the leakage margin and susceptibility-correlation margin are equal.

Result:

```text
BALANCED_DINUCLEAR_TEMPERATURE_K=
95.22770993335909

BALANCED_LEAKAGE_MARGIN=
3.385149110507368

BALANCED_CORRELATION_MARGIN=
3.385149110507362

BALANCED_MU_R=
0.8613483591959621

BALANCED_STABILITY_MARGIN=
1.823739827829086
```

The corresponding finite-size mass extrapolation in the same toy spherical susceptibility model is:

```text
BALANCED_CRITICAL_PAYLOAD_MASS_KG=
6065.807834674159
```

Do not interpret $6066,{\mathrm{kg}}$ as a universal maximum antigravity payload.

It is the specific zero-mode extrapolation of the selected effective susceptibility model.

---

# 33. Control burden after cooperative selectivity

Because the cooperative selector itself supplies off-state purity, the model no longer requires W's $0.336,{\mathrm{eV/site}}$ additional room-temperature gap in the selected moderate-temperature window.

Minimum selected control shift:

```text
MINIMUM_DINUCLEAR_CONTROL_SITE_EV=
0.07919352471801402
```

For two sites:

```text
MINIMUM_DINUCLEAR_CONTROL_CLUSTER_EV=
0.1583870494360280
```

Equivalent free-energy scale per kilogram:

```text
1.063556252028522e5 J/kg
```

For one ton:

```text
1.063556252028522e8 J
```

or approximately:

```math
106\ {\mathrm{MJ}}
```

This is a free-energy scale in the model.

It is not demonstrated electrical input energy.

It is not continuous power.

It is not yet associated with an actual switching technology.

---

# 34. Cooperative stabilization robustness

Real spin-crossover clusters can have cooperative stabilization of the all-high-spin state.

At $77,{\mathrm{K}}$, the dimer can tolerate approximately:

```text
0.0376 eV/dimer
```

of all-high-spin cooperative stabilization before extra ordinary material gap becomes necessary.

At:

```text
0.050 eV/dimer
```

stabilization, required additional material gap is only:

```text
0.00619 eV/site
```

and total control:

```text
0.08538 eV/site
```

At:

```text
0.100 eV/dimer
```

stabilization, total control becomes:

```text
0.11038 eV/site
```

Thus modest cooperativity does not immediately destroy the low-energy selector window.

A real material calculation would still need its actual many-body free-energy landscape.

---

# 35. X virtual-process hierarchy

For an illustrative electronic gap:

```math
\Delta_{\mathrm{UV}}
=
5\ {\mathrm{eV}}
```

a schematic $N$th-order process:

```math
J_N
\sim
\Delta_{\mathrm{UV}}
\left(
\frac{t}{\Delta_{\mathrm{UV}}}
\right)^N
```

was inverted.

Results:

```text
N=2:
t/Delta≈0.1757

N=3:
≈0.3591

N=4:
≈0.4984

N=5:
≈0.5991

N=11:
≈0.8511
```

Therefore the dinuclear second-order construction is parametrically much cleaner than an $N=11$ high-order room-temperature selector.

This was not a derivation of the scalar portal.

It was only a perturbative hierarchy diagnostic.

---

# 36. 010E-Y — decisive locality question

Y asked:

> Does locality or Feynman-Hellmann force the scalar charge of the bound dimer onto the isolated constituent sectors?

Within a strict particle-number-conserving nonrelativistic composite EFT, the answer is:

```text
NO
```

This is a low-energy theorem/model statement only.

It is not yet a theorem about every relativistic UV completion.

---

# 37. Y auxiliary dimer EFT

Introduce nonrelativistic fields:

```text
A
B
D
```

where $D$ is an emergent bound-state/dimer field.

Assign constituent number:

```math
N_A=1
```

```math
N_B=1
```

```math
N_D=2
```

Total number:

```math
N
=
N_A
+
N_B
+
2N_D
```

The local conversion interaction is:

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

and the scalar couples only to the dimer:

```math
H_\phi
=
g_D\phi D^\dagger D
```

Therefore:

```math
[
H,N
]
=
0
```

The one-particle sectors contain no $D$ state.

Hence:

```math
\frac{
\partial E_A
}{
\partial\phi
}
=
0
```

and:

```math
\frac{
\partial E_B
}{
\partial\phi
}
=
0
```

exactly inside this EFT.

The two-particle sector contains:

```text
|AB>
|D>
```

and can carry nonzero scalar response.

This is the essential mechanism by which bound-state-specific scalar charge avoids automatically becoming constituent charge at low energy.

---

# 38. Y explicit two-channel Hamiltonian

The two-particle Hamiltonian is:

```math
H_2(\phi)
=
\begin{pmatrix}
0&h\\
h&\Delta_D+g_D\phi
\end{pmatrix}
```

The benchmark used:

```text
DIMER_BARE_DETUNING_EV=
-5

DIMER_PAIR_MIXING_EV=
0.8783524469661568
```

The required physical dinuclear scalar coupling is:

```text
TARGET_DINUCLEAR_COUPLING=
8.638353631211470e-12
```

Solving for the bare dimer coupling at the terrestrial scalar background gave:

```text
BARE_DIMER_SCALAR_COUPLING=
8.904546001587151e-12
```

Dimer fraction:

```text
ZERO_PHI=
0.9717316000818251

EARTH_PHI=
0.9701060143517443
```

Thus the selected dressed bound state is approximately $97\%$ dimer-like.

---

# 39. Feynman-Hellmann verification

For an eigenstate $|\psi\rangle$:

```math
\frac{
dE
}{
d\phi
}
=
\left\langle
\psi
\left|
\frac{
\partial H
}{
\partial\phi
}
\right|
\psi
\right\rangle
```

Here:

```math
\frac{
\partial H
}{
\partial\phi
}
=
g_D
|D\rangle\langle D|
```

Therefore:

```math
\frac{
dE_{\mathrm{bound}}
}{
d\phi
}
=
g_D Z_D
```

where $Z_D$ is the dimer probability.

At Earth's scalar background:

```text
DRESSED_DIMER_CHARGE=
8.638353631211473e-12
```

Independent finite difference:

```text
8.638353628551620e-12
```

Relative error:

```text
3.079119804066939e-10
```

Therefore:

```text
FEYNMAN_HELLMANN_BOUND_STATE_CHARGE=PASS
```

This is an important internal consistency check.

---

# 40. Exact one-body sector result

The explicit number-sector Hamiltonian gave:

```text
NUMBER_OPERATOR_COMMUTATOR_NORM=
0
```

and:

```text
ISOLATED_A_SCALAR_CHARGE=
0

ISOLATED_B_SCALAR_CHARGE=
0
```

Therefore:

```text
BOUND_STATE_SCALAR_CHARGE_WITH_ZERO_ISOLATED_CONSTITUENT_CHARGE=
EXPLICITLY_CONSTRUCTED_AT_LOCAL_NR_EFT_LEVEL
```

This statement must always retain the qualifier:

```text
AT_LOCAL_NR_EFT_LEVEL
```

It is not a proof that a relativistic microscopic theory can generate the same operator hierarchy.

---

# 41. Earth-background linearity

The huge terrestrial scalar background is:

```text
EXTERNAL_PHI_EV=
1.690631280830914e10
```

Bare dimer shift:

```text
0.1505430401188108 eV
```

Physical dressed bound-state shift:

```text
0.1461667280041015 eV
```

Linear target:

```text
0.1460427086380542 eV
```

Nonlinearity:

```math
\left|
\frac{
0.1461667280
}{
0.1460427086
}
-
1
\right|
\approx
8.49\times10^{-4}
```

or approximately:

```text
0.085%
```

Dimer-fraction change:

```text
0.0016256
```

Thus the terrestrial scalar background does not drive the selected two-channel model near a dramatic resonance or breakdown.

This is an internal model result, not evidence for the actual interaction.

---

# 42. Y independent two-body contact representation

The same low-energy physics was represented independently as:

```math
\mathcal{H}_{\phi,2}
=
C_\phi
\phi
A^\dagger
B^\dagger
BA
```

This operator has:

```math
\langle A|
A^\dagger B^\dagger BA
|A\rangle
=
0
```

and:

```math
\langle B|
A^\dagger B^\dagger BA
|B\rangle
=
0
```

but a nonzero matrix element in the two-body sector.

For an exponential $S$-wave pair of characteristic radius $a$:

```math
|\psi(0)|^2
=
\frac{
1
}{
\pi a^3
}
```

Matching requires:

```math
C_\phi
|\psi(0)|^2
=
G_{\mathrm{dimer}}
```

so:

```math
C_\phi
=
\frac{
G_{\mathrm{dimer}}
}{
|\psi(0)|^2
}
```

For:

```math
a=3\ {\mathrm{\AA}}
```

Y found:

```text
C_PHI=
9.536416387852626e-20 eV^-3
```

The formal coefficient scale:

```math
\Lambda_{\mathrm{pair}}
=
C_\phi^{-1/3}
```

is:

```text
≈2.19 MeV
```

This must not be interpreted as a new mediator mass.

The actual atomic EFT cutoff is:

```math
\Lambda_{\mathrm{EFT}}
\sim
\frac{
\hbar c
}{
a
}
```

For $a=3,{\mathrm{\AA}}$:

```text
≈657.76 eV
```

The dimensionless Wilson strength is:

```math
C_\phi
\Lambda_{\mathrm{EFT}}^3
=
2.713818830692468e-11
```

Thus the required pair operator is extremely weak at the atomic EFT cutoff.

This passed the low-energy perturbativity preflight.

---

# 43. Why the auxiliary dimer and contact representations matter

The project now has two independent low-energy descriptions of the same qualitative response:

```text
AUXILIARY_DIMER_FIELD
```

and:

```text
DIRECT_TWO_BODY_CONTACT_OPERATOR
```

Both produce:

```text
ONE_BODY_EXTRA_CHARGE=ZERO
TWO_BODY_BOUND_STATE_EXTRA_CHARGE=NONZERO
```

Therefore the result is not merely an artifact of one convenient field parametrization.

Correct classification:

```text
INDEPENDENT_LOW_ENERGY_REPRESENTATION_CHECK=PASS
```

This still falls short of independent UV derivations of an actual microscopic theory.

---

# 44. Nonrelativistic zero-density vacuum-loop protection

A Schrödinger propagator has the form:

```math
G(\omega,\mathbf{p})
=
\frac{
i
}{
\omega
-
E_{\mathbf{p}}
+
i\epsilon
}
```

Its pole lies in one half of the complex $\omega$ plane.

For a closed oriented nonrelativistic particle-number loop, all poles can lie in the same half plane.

If the frequency integral is sufficiently UV convergent, the contour can be closed in the empty half plane, giving zero.

Therefore strict zero-density NR density-coupling loops can obey:

```text
CLOSED_PARTICLE_LOOP=ZERO
```

This is why the emergent NR dimer field does not automatically create the same relativistic vacuum-polarization naturalness catastrophe as a fundamental particle/antiparticle field.

However:

* finite-density susceptibility does not vanish;
* finite-temperature susceptibility does not vanish;
* relativistic matching can reintroduce thresholds and loops;
* antiparticle/high-energy states do not exist in the strict NR model.

Therefore:

```text
NR_ZERO_DENSITY_VACUUM_PROTECTION=
LOW_ENERGY_PROPERTY_ONLY
```

Do not promote it to a UV solution.

---

# 45. Y finite-density stability recheck

Y reproduced the dinuclear finite-size results.

At $77,{\mathrm{K}}$:

```text
DINUCLEAR_MU_R=
0.9556137730170507
```

with threshold:

```text
1.570875308300910
```

giving:

```text
STABILITY_MARGIN=
1.643839124818559
```

At the balanced temperature:

```text
95.22770993335909 K
```

the model gives:

```text
MU_R=
0.8613483591959621
```

and:

```text
STABILITY_MARGIN=
1.823739827829086
```

The $77,{\mathrm{K}}$ leakage result is:

```text
1.989338055378181e-9
```

with margin:

```text
290.1950942786034
```

Thus the local dimer EFT did not secretly destroy the X finite-density window.

---

# 46. Fundamental relativistic dimer interpretation is dead

The approximate rest energy of one active site is:

```text
6.692226229426247e10 eV
```

The dinuclear object is approximately:

```text
1.338445245885249e11 eV
```

or about:

```math
134\ {\mathrm{GeV}}
```

If this entire object were treated as a fundamental relativistic fermion-like particle with coupling $g_D$, the scalar-mass correction is parametrically:

```math
\delta m_\phi^2
\sim
\frac{
g_D^2M_D^2
}{
8\pi^2
}
```

Y found:

```text
RELATIVISTIC_FERMION_DIMER_LOOP_TO_TARGET_MASS2=
1.155053548350539e19
```

For a fundamental scalar-like dimer with trilinear:

```math
\mu_\phi
\sim
2M_Dg_D
```

the correction:

```math
\delta m_\phi^2
\sim
\frac{
\mu_\phi^2
}{
16\pi^2
}
```

gave:

```text
RELATIVISTIC_SCALAR_DIMER_LOOP_TO_TARGET_MASS2=
2.310107096701078e19
```

Therefore:

```text
FUNDAMENTAL_RELATIVISTIC_DIMER_CARRIER=
REJECTED_BY_ULTRALIGHT_SCALAR_NATURALNESS
```

Only an emergent low-energy composite interpretation survives.

This negative result is important and should not be forgotten.

---

# 47. Generic unprotected relativistic UV matching also fails

A typical one-loop mixing factor is:

```math
\frac{
1
}{
16\pi^2
}
\approx
6.3326\times10^{-3}
```

Allowed target-equivalent ordinary-matter leakage is:

```math
f_{\mathrm{leak}}
=
5.77296\times10^{-7}
```

The ratio is:

```math
\frac{
6.3326\times10^{-3}
}{
5.77296\times10^{-7}
}
\approx
1.0969\times10^4
```

Therefore generic loop suppression is about:

```text
11,000 times too weak
```

to protect the required material specificity.

The additional suppression relative to a generic one-loop coefficient must be roughly:

```math
\frac{
5.77\times10^{-7}
}{
6.33\times10^{-3}
}
\approx
9.1\times10^{-5}
```

or stronger.

Decision:

```text
GENERIC_UNPROTECTED_RELATIVISTIC_UV_MATCH=
REJECTED
```

This is now the central theoretical wall.

---

# 48. Nonrelativistic hierarchy diagnostic

The physical scalar-dependent dimer energy shift is approximately:

```text
0.146 eV
```

The dimer rest energy is:

```text
1.338e11 eV
```

Ratio:

```math
\frac{
0.146
}{
1.338\times10^{11}
}
\approx
1.09\times10^{-12}
```

The allowed leakage fraction is:

```text
5.77e-7
```

Thus if relativistic corrections were genuinely controlled only by $E_{\mathrm{low}}/M_{\mathrm{rest}}$, there would be a hierarchy margin of approximately:

```math
\frac{
5.77\times10^{-7}
}{
1.09\times10^{-12}
}
\approx
5.29\times10^5
```

This is encouraging as a hierarchy diagnostic.

It is not a proof.

There is no demonstrated symmetry yet showing that every dangerous one-body operator is suppressed by that ratio.

---

# 49. Scientific meaning of Y

The strongest defensible conclusion from Y is:

> **Locality and Feynman-Hellmann do not, by themselves, forbid a bound-state-specific scalar response in a strict particle-number-conserving nonrelativistic composite EFT.**

More explicitly:

```text
LOCALITY_FORCES_BOUND_STATE_CHARGE_ONTO_ISOLATED_CONSTITUENTS=
NO_IN_STRICT_NR_COMPOSITE_EFT

FEYNMAN_HELLMANN_BOUND_STATE_CHARGE=
PASS

INDEPENDENT_DIMER_FIELD_AND_TWO_BODY_CONTACT_REPRESENTATIONS=
AGREE

BOUND_STATE_SPECIFIC_SCALAR_RESPONSE=
EXPLICIT_LOCAL_LOW_ENERGY_EFT_CONSTRUCTION
```

This is a meaningful low-energy result.

It does not imply:

```text
STANDARD_MODEL_GENERATES_C_PHI
```

or:

```text
REAL_MATERIAL_HAS_C_PHI
```

or:

```text
UV_COMPLETION_EXISTS
```

---

# 50. Current leading low-energy architecture

The current fifth-force/material architecture is now substantially simpler than the Q-R hidden-phase architecture.

The leading schematic chain is:

```text
EARTH / GROUND MASS
        |
        v
ULTRALIGHT 5-km SCALAR phi
        |
        v
MATERIAL-SPECIFIC TWO-BODY / DIMER OPERATOR
        |
        v
FIXED BOUND DINUCLEAR MATERIAL IDENTITY
        |
        v
COOPERATIVE HIGH-SPIN INTERNAL STATE
        |
        v
REAL SPIN-LATTICE / STRUCTURAL RESPONSE
        |
        v
MACROSCOPIC PAYLOAD
```

The hidden compact phase is not presently required in the leading finite-payload low-energy model.

Therefore:

```text
PREEXISTING_HIDDEN_COMPACT_PHASE_REQUIRED=NO_IN_CURRENT_LEADING_LOW_ENERGY_EFT

PREEXISTING_10KEV_HIDDEN_CONDENSATE_REQUIRED=NO

HIDDEN_COSMOLOGICAL_PHASE_VACUUM_REQUIRED=NO
```

The old compact-phase work remains valuable because it helped identify and solve intermediate consistency problems, but it is not the current minimal architecture.

---

# 51. What is real physics in the current architecture

The following ingredients correspond to known general physical structures or material classes:

```text
ULTRALIGHT_SCALAR_FIELD_AS_A_THEORETICAL_QFT_OBJECT
NONRELATIVISTIC_BOUND_STATE_EFT
AUXILIARY_DIMER_FIELDS
TWO_BODY_CONTACT_OPERATORS
FEYNMAN_HELLMANN_THEOREM
SPIN_CROSSOVER
FEII_S=0_TO_S=2_TRANSITIONS
SPIN_LATTICE_COUPLING
COOPERATIVE_DINUCLEAR/POLYNUCLEAR_SPIN_CROSSOVER_CLASSES
FINITE_SIZE_EIGENMODE_STABILITY
```

What is not known to exist is the crucial new interaction:

```math
C_\phi
\phi
A^\dagger B^\dagger BA
```

with the required strength, sign, material specificity, and UV protection.

The existence of known dimer EFTs or spin-crossover chemistry does not constitute evidence that this scalar operator exists.

---

# 52. Major branches falsified during O-Y

Preserve this list so they are not casually reopened.

```text
LIGHT_POINTLIKE_HIDDEN_CARRIER_PER_ATOMIC_CELL
= REJECTED_BY_LOCALIZATION/NATURALNESS

MATERIAL_CREATED_10KEV_HIDDEN_CONDENSATE
= REJECTED_AS_PRACTICAL_ENERGY_ROUTE

DIRECT_UNPROTECTED_ELECTRON_MASS_PORTAL
= REJECTED_BY_RADIATIVE_NATURALNESS

SIMPLE_FUNDAMENTAL_ELECTRON_CURRENT_MEDIATOR
= REJECTED_BY_ELECTRON_G_MINUS_2_PREFLIGHT

CONTINUOUS_LINEAR_STRUCTURAL_SELECTOR
= REJECTED_BY_SCALAR_POLARIZATION

SIMPLE_EVEN_STRUCTURAL_MONOMIAL_SELECTOR
= REJECTED_BY_ZERO_POINT/THERMAL_LEAKAGE

NORMAL_ORDERED_QUADRATIC_SELECTOR
= REJECTED_BY_FINITE_TEMPERATURE_LEAKAGE

UNIVERSAL_HIGH_SPIN_PORTAL
= REJECTED_BY ORDINARY-MATTER LEAKAGE

ACCIDENTALLY_TUNED_POLYNOMIAL_PROJECTOR
= REJECTED_AS UNPROTECTED FINE TUNING

FUNDAMENTAL_RELATIVISTIC_DIMER_CARRIER
= REJECTED_BY ULTRALIGHT-SCALAR NATURALNESS

GENERIC_UNPROTECTED_RELATIVISTIC_UV_MATCH
= REJECTED BY OPERATOR-LEAKAGE PREFLIGHT
```

Do not add new compensating fields to rescue any of these unless a genuine new physical principle changes the relevant no-go calculation.

---

# 53. Superseded but not useless results

Several earlier results are not wrong; they are simply no longer the preferred architecture.

## Compact hidden phase

Still a mathematically viable low-energy parametric model.

No longer necessary after finite-size stabilization reopened direct material charge.

## Generic host scalar $\chi$

Useful pedagogically.

Its normalization-dependent small coupling is not an invariant material success criterion.

## Room-temperature near-coexistence direct state switching

Fails off-state leakage.

A sufficiently gapped room-temperature cluster could still survive, but moderate-temperature cooperative dimers are currently simpler.

## Coherent avoided crossing

Finite-size analysis reopened the stability criterion dramatically, reducing the old infinite-medium $\Omega$ requirement by about:

```text
1.6e8
```

but endpoint purity and real-material dynamics remain problematic.

It is not the leading switching route.

---

# 54. Current experimental leakage requirement

The conservative historical force bound implies maximum target-equivalent ordinary-matter contamination:

```text
f_leak=
5.772961445324848e-7
```

Any microscopic UV completion must enumerate induced scalar charge on:

* electrons;
* protons;
* neutrons;
* quarks;
* gluonic mass;
* electromagnetic binding energy;
* nuclear binding energy;
* ordinary atoms;
* ordinary molecules;
* unrelated transition-metal complexes;
* unrelated spin-crossover systems;
* lattice binding;
* bulk material.

The sum of all unwanted effective target-equivalent scalar response must remain below the experimental allowance.

This may be the single hardest constraint.

---

# 55. Current ultralight-scalar naturalness requirement

The mediator range is:

```math
\lambda
=
5\times10^3\ {\mathrm{m}}
```

Thus:

```math
m_\phi
=
3.946539608\times10^{-11}\ {\mathrm{eV}}
```

Any proposed relativistic completion must calculate its threshold correction:

```math
\delta m_\phi^2
```

and require, absent a demonstrated protective symmetry:

```math
|\delta m_\phi^2|
\lesssim
m_\phi^2
```

A candidate that generates:

```math
\frac{
|\delta m_\phi^2|
}{
m_\phi^2
}
\gg1
```

without a technically natural protection mechanism should be rejected.

Do not merely retune the bare scalar mass against loops.

---

# 56. Current single active scientific question

The next session should begin with exactly one high-priority question:

> **Can a local relativistic microscopic theory matched to Standard Model constituents and a technically natural ultralight scalar generate the required protected two-body material Wilson coefficient while keeping all induced one-body ordinary-matter scalar charge below the leakage limit and preserving the ultralight mediator mass?**

In symbols, the low-energy target is:

```math
\mathcal{H}_{\mathrm{EFT}}
\supset
C_\phi
\phi
A^\dagger B^\dagger BA
```

with approximately:

```text
C_PHI≈9.54e-20 eV^-3
```

for the representative $3,\mathrm{\AA}$ normalization.

But the UV theory must not simultaneously generate dangerous terms such as:

```math
g_A\phi A^\dagger A
```

```math
g_B\phi B^\dagger B
```

or their Standard Model constituent equivalents above the leakage allowance.

That is the decisive bridge between:

```text
LOW_ENERGY_MATHEMATICAL_MODEL
```

and:

```text
PHYSICAL_REALIZABILITY
```

---

# 57. The next session should not begin by designing another material model

Do not begin by:

* changing the spin-crossover molecule;
* adjusting $K$;
* optimizing the phonon coordinate;
* changing cluster size;
* retuning temperature;
* adding another hidden scalar;
* adding another selector function;
* changing the dimer radius;
* optimizing the control energy.

Those are now lower-information tasks.

The dominant uncertainty is UV matching.

If the UV matching fails, further low-energy optimization is irrelevant.

---

# 58. Recommended next-session execution order

## Step 0 — verify baseline

Run:

```bash
git status --short

ROOT="$(pwd)"
PY="$ROOT/.venv/bin/python"

PYTHONPATH="$ROOT/src" \
"$PY" -m pytest -q tests/known_solutions
```

Expected:

```text
94 passed
```

Do not continue scientific inference if the known-solution baseline unexpectedly fails.

---

## Step 1 — literature/operator-mixing reconstruction

Search for the smallest known class of relativistic theories in which:

* an ultralight scalar couples to a two-body/bound-state operator;
* an exact symmetry forbids or parametrically suppresses one-body scalar operators;
* the low-energy NR matching yields an operator of the form:

```math
\phi
A^\dagger B^\dagger BA
```

Relevant theoretical concepts may include:

```text
CONSERVed currents
selection rules
spurion analysis
shift symmetry
chiral symmetry
heavy-particle EFT
bound-state EFT
Feshbach-type matching
dibaryon EFT
multi-fermion operators
operator mixing under renormalization
Ward identities
nonrenormalization structures
emergent symmetries
```

Do not assume any of these solve the problem.

Use them as candidate protection mechanisms to test.

---

## Step 2 — write the smallest candidate relativistic operator basis

For each plausible symmetry class, enumerate all operators up to the lowest relevant mass dimension.

The central task is not merely to write the desired two-body operator.

It is to identify every symmetry-allowed one-body operator.

For example, schematically:

```math
\mathcal{L}
=
\mathcal{L}_{\mathrm{SM}}
+
\frac12
(\partial\phi)^2
-
\frac12
m_\phi^2\phi^2
+
\sum_i
c_i
\mathcal{O}_i
```

Then classify:

```text
DESIRED_TWO_BODY_OPERATOR
DANGEROUS_ONE_BODY_OPERATOR
DANGEROUS_ELECTRON_OPERATOR
DANGEROUS_NUCLEON_OPERATOR
DANGEROUS_HIGGS_OPERATOR
DANGEROUS_PHOTON_OPERATOR
```

If the exact symmetry that allows the two-body operator also allows a one-body operator of equal or lower dimension, that is immediately bad news.

---

## Step 3 — renormalization/operator-mixing gate

Calculate whether the desired operator radiatively induces one-body couplings.

If:

```math
C_2
```

is the desired two-body coefficient and loops generate:

```math
C_1
\sim
\frac{
C_2
}{
16\pi^2
}
```

with no further suppression, the branch is already in severe trouble because:

```math
\frac1{16\pi^2}
\approx
6.33\times10^{-3}
```

while:

```math
f_{\mathrm{leak}}
\approx
5.77\times10^{-7}
```

The generic ratio is:

```math
\frac{
6.33\times10^{-3}
}{
5.77\times10^{-7}
}
\approx
1.10\times10^4
```

So a mere loop factor is not enough.

There must be an additional symmetry/hierarchy of at least roughly four orders of magnitude beyond ordinary one-loop suppression.

---

# 59. Independent matching requirement

If a relativistic candidate survives Step 3, derive the NR coefficient independently in at least two ways.

Preferred possibilities:

1. direct matching of the relativistic scattering amplitude;
2. bound-state Feynman-Hellmann derivative;
3. integrating out a heavy mediator;
4. Schrieffer-Wolff / second-order perturbative reduction;
5. matching to a dimer auxiliary field;
6. direct two-body potential expectation value.

The two calculations should agree on:

* sign;
* mass dimensions;
* dependence on UV scales;
* dependence on wavefunction overlap;
* decoupling limits.

Do not test an implementation only against itself.

---

# 60. Required limiting cases

Every candidate UV completion should pass the following limits.

## No-binding limit

As the dimer/bound state disappears:

```math
E_{\mathrm{bind}}\to0
```

the bound-specific scalar charge should behave consistently with the claimed mechanism.

If the charge remains huge while the material-specific state ceases to exist, explain why.

## Zero-mixing limit

If:

```math
t\to0
```

the bound-state coupling should reduce to the appropriate unmixed limit.

## Infinite-detuning limit

If:

```math
\Delta\to\infty
```

unwanted target-state admixture should vanish.

## Scalar-decoupling limit

If:

```math
C_\phi\to0
```

all new scalar effects must vanish continuously.

## Infinite-volume / finite-volume distinction

Do not confuse the finite-body scalar stability result with infinite-medium stability.

---

# 61. Naturalness gate after actual UV matching

Once the actual microscopic couplings are known, calculate:

```math
\delta m_\phi^2
```

from every relevant field.

This includes:

* constituent fermions;
* heavy mediators;
* Higgs mixing if present;
* scalar thresholds;
* gauge fields;
* bound-state channels;
* symmetry-breaking scales.

The selected mediator mass is:

```math
m_\phi
=
3.94654\times10^{-11}\ {\mathrm{eV}}
```

so:

```math
m_\phi^2
\approx
1.56\times10^{-21}\ {\mathrm{eV^2}}
```

This is extraordinarily small.

Any coupling to ordinary high-energy degrees of freedom is potentially dangerous.

A valid completion must explain technically why this mass remains small.

---

# 62. Exact experimental-bound closure

If a microscopic completion survives operator mixing and naturalness, the next empirical gate should be the exact $5,{\mathrm{km}}$ Yukawa boundary.

Target point:

```text
lambda=5000 m
alpha_Y=2e-4
```

Required work:

* obtain author-provided source data if available;
* or independently digitize the 2026 review curve;
* estimate graphical uncertainty;
* compare the benchmark with the actual modern 95% CL envelope;
* record the numerical margin.

Do not continue to rely on:

```text
VISUALLY_LOOKS_ALLOWED
```

once the model survives enough theory to make the empirical margin decisive.

---

# 63. Stellar and cosmological tests come after actual portal specification

Do not perform generic hand-waving stellar calculations on the present dimer EFT.

The stellar/cosmological behavior depends on the actual microscopic operator.

Once a UV model is specified, test:

* stellar production;
* stellar trapping;
* supernova transport;
* red-giant/HB constraints;
* neutron-star matter;
* early-Universe thermalization;
* BBN;
* CMB;
* dark radiation;
* cosmological scalar background;
* phase transitions;
* relic bound states if any.

A material-only NR EFT cannot by itself answer these questions.

---

# 64. Stop rules for the current branch

Close or severely demote the direct-material fifth-force branch immediately if any of the following is established.

```text
ONE_BODY_OPERATOR_INDUCED_ABOVE_LEAKAGE_LIMIT
```

```text
REQUIRED_PROTECTION_IS_FINE_TUNED_CANCELLATION_RATHER_THAN_SYMMETRY
```

```text
ULTRALIGHT_SCALAR_MASS_DESTABILIZED_WITHOUT_TECHNICAL_PROTECTION
```

```text
CURRENT_EXACT_5KM_BOUND_EXCLUDES_ALPHA_Y_2E_MINUS_4
```

```text
STELLAR_OR_COSMOLOGICAL_COMPLETION_FORCES_FORBIDDEN_ORDINARY_COUPLING
```

```text
MATERIAL_SPECIFIC_TWO_BODY_SCALAR_COUPLING_CANNOT_BE_MATCHED_IN_LOCAL_RELATIVISTIC_QFT
```

```text
BOUND_STATE_SPECIFIC_CHARGE_REQUIRES_CONSTITUENT_CHARGE_ABOVE_LEAKAGE_LIMIT
```

If a stop rule fires:

1. record the negative result;
2. preserve any useful theorem/test;
3. do not add more hidden knobs;
4. globally rerank the remaining research landscape.

---

# 65. Claim classifications at session close

## Established project result

```text
006D_MATHEMATICAL_LOCAL_REPULSION=ESTABLISHED
```

```text
006D_FINITE_POSITIVE_ENERGY_LINEARIZED_GR_CONSTRUCTION=ESTABLISHED
```

```text
006D_NEC_WEC_DEC=PASS
```

```text
006D_LOCAL_CONSERVATION_LINEARIZED_ORDER=ESTABLISHED
```

```text
006D_OUTWARD_NEAR_FIELD=ESTABLISHED
```

```text
006D_POSITIVE_FAR_FIELD_ACTIVE_MASS=ESTABLISHED
```

## Late 010E project-derived low-energy results

```text
FINITE_SIZE_SCALAR_ZERO_MODE_THRESHOLD=DERIVED_AND_NUMERICALLY_EVALUATED
```

```text
COOPERATIVE_SELECTOR_WINDOW=FOUND_IN_SELECTED_MODEL
```

```text
DINUCLEAR_LOW_ENERGY_SELECTOR=PARAMETRIC_SURVIVOR
```

```text
BOUND_STATE_SPECIFIC_SCALAR_CHARGE_WITH_ZERO_ONE_BODY_CHARGE=
EXPLICIT_LOCAL_NR_EFT_CONSTRUCTION
```

```text
FEYNMAN_HELLMANN_CHECK=PASS
```

```text
INDEPENDENT_TWO_BODY_CONTACT_REPRESENTATION=PASS
```

```text
LOW_ENERGY_PAIR_WILSON_COEFFICIENT=PERTURBATIVE_AT_ATOMIC_EFT_SCALE
```

## Rejected interpretations

```text
FUNDAMENTAL_RELATIVISTIC_DIMER=REJECTED
```

```text
GENERIC_UNPROTECTED_RELATIVISTIC_UV_MATCH=REJECTED
```

```text
UNIVERSAL_HIGH_SPIN_PORTAL=REJECTED
```

```text
CONTINUOUS_STRUCTURAL_SELECTORS_TESTED=REJECTED
```

## Not established

```text
FULL_STANDARD_MODEL_PLUS_HIDDEN_UV_COMPLETION=NOT_ESTABLISHED
```

```text
ACTUAL_MICROSCOPIC_ORIGIN_OF_C_PHI=NOT_ESTABLISHED
```

```text
KNOWN_REAL_MATERIAL_WITH_C_PHI=NO
```

```text
CURRENT_EXACT_5KM_STATE_DEPENDENT_BOUND=NOT_CLOSED
```

```text
FULL_STELLAR_SAFETY=NOT_ESTABLISHED
```

```text
FULL_COSMOLOGICAL_SAFETY=NOT_ESTABLISHED
```

```text
PRACTICAL_ANTIGRAVITY_DEVICE=NOT_ESTABLISHED
```

```text
NEW_PHYSICS_DISCOVERY=NO
```

```text
NOVELTY=NOT_ESTABLISHED
```

---

# 66. Why Y is scientifically important but not a discovery

Y removed one potential low-energy no-go.

Before Y, one could object:

> A huge scalar charge on a material bound state must necessarily mean the underlying constituents possess the same huge scalar coupling.

Y demonstrates that this statement is false in general at the level of a strict number-conserving NR composite EFT.

The dimer can have:

```math
\frac{
dE_D
}{
d\phi
}
\ne0
```

while isolated one-body sectors have:

```math
\frac{
dE_A
}{
d\phi
}
=
0
```

and:

```math
\frac{
dE_B
}{
d\phi
}
=
0
```

This is a useful theoretical result.

But the actual physical question is harder:

> Can the Standard Model plus a technically natural ultralight scalar produce such a protected low-energy operator?

Y does not answer that.

Therefore Y is best described as:

```text
LOW_ENERGY_NO_GO_AVOIDED
```

not:

```text
NEW_FORCE_FOUND
```

---

# 67. Current practical interpretation

The project has made substantial theoretical progress in narrowing the problem.

It has not made comparable progress toward hardware.

There is:

```text
NO_KNOWN_ACTIVE_MATERIAL
NO_DEMONSTRATED_SCALAR_PORTAL
NO_EXPERIMENTAL_SIGNAL
NO_DEVICE_ARCHITECTURE
NO_CONTROL_HARDWARE
NO_ENGINEERING_PATH
```

The present scalar-material branch is still several fundamental layers upstream of engineering.

Do not interpret model control energies such as:

```text
106 MJ per tonne
```

as a design specification for a real device.

They are internal free-energy scales of the selected effective model.

---

# 68. What should count as a true major breakthrough next session

A genuine next-level theoretical breakthrough would be one of the following.

## Positive breakthrough

Construct a relativistic, gauge-consistent microscopic theory in which:

1. the desired two-body material operator is generated;
2. one-body ordinary-matter couplings are symmetry forbidden or sufficiently suppressed;
3. the ultralight scalar mass remains technically natural;
4. the NR matching reproduces the required $C_\phi$;
5. the selected fifth-force benchmark remains experimentally allowed.

That would move the project from:

```text
LOW_ENERGY_PARAMETRIC_SURVIVOR
```

toward:

```text
MICROSCOPIC_THEORETICAL_MECHANISM
```

It would still not be a device.

## Negative breakthrough

Prove that any local relativistic completion generating the required two-body operator necessarily induces a one-body operator above the leakage bound or destabilizes $m_\phi$.

That would cleanly close the current scalar-material branch.

A rigorous negative result would be equally valuable.

---

# 69. What not to do next session

Do not:

* optimize 006D coefficients again;
* restart Casimir searches;
* retune rejected chameleon screening;
* revive the simple gold-null vector without fixing electroweak current consistency;
* revive the localized 1-eV hidden carrier;
* recreate the 10-keV hidden condensate inside material;
* use a direct electron-mass scalar portal;
* use a simple electron-current mediator;
* rely on a continuous structural coordinate for $10^{-6}$ selectivity;
* assume universal high spin can carry the scalar charge;
* use polynomial coefficient cancellation as an exact selector;
* treat the dimer as a fundamental 134-GeV relativistic particle;
* claim generic loop suppression is enough;
* move to experimental design before a microscopic portal survives.

---

# 70. Literature anchors to preserve

The following published topics/results were used as external anchors during the project.

## Gravity / fifth-force

* Murata, Fujiie, Suzuki, 2026, review of short-range/inverse-square-law gravitational tests.
* March et al., 2019, intermediate-range/ocean Yukawa constraint.

The exact modern $5,{\mathrm{km}}$ numerical boundary remains to be reconstructed.

## Spin crossover

Published Fe(II) spin-crossover literature establishes real:

* low-spin/high-spin states;
* approximately $S=0$ to $S=2$ switching in relevant Fe(II) systems;
* strong spin-lattice coupling;
* cooperative molecular/solid-state transitions;
* dinuclear and polynuclear spin-crossover material classes;
* Fe$_4$ grid-type cooperative spin-state systems.

These facts support the host **class**.

They do not establish the scalar portal.

## Nonrelativistic composite EFT

Published EFT literature establishes the legitimacy of:

* auxiliary molecular/dimer fields;
* bound-state effective fields;
* two-body contact operators;
* Feshbach-type atom/molecule EFT organization;
* dibaryon-style EFT organization;
* nonrelativistic particle-number sectors;
* closed oriented particle-loop vacuum selection rules.

These provide known field-theory analogies/structures.

They do not demonstrate the antigravity coupling.

---

# 71. Numerical reference sheet

Keep the following values immediately available in the next session.

## 006D

```text
C_FINITE=
23.591586299249

C_THIN=
23.426710175391

MAX_CONSERVATION_RESIDUAL=
3.103073353827e-14

MAX_DEC_VIOLATION=
0

MIN_NEC_MARGIN=
0
```

## Fifth-force benchmark

```text
SCALAR_RANGE_M=
5000

MEDIATOR_MASS_EV=
3.946539608e-11

ALPHA_Y=
2e-4

ALPHA_SOURCE=
1e-2

ALPHA_ACTIVATED=
-1.558991777087370e5

ACTIVATED_EXTRA_COUPLING_PER_NUCLEON=
6.011882433614129e-14
```

## Leakage

```text
MAXIMUM_PORTAL_LEAKAGE_FRACTION=
5.772961445324848e-7
```

## Representative active site

```text
ACTIVE_SITE_MASS_U=
71.844

TARGET_EXTRA_COUPLING_PER_ACTIVE_SITE=
4.319176815605735e-12

SCALAR_ACTIVATION_PENALTY_SITE_EV=
0.07715030210914353
```

## Dinuclear target

```text
TARGET_DINUCLEAR_COUPLING=
8.638353631211470e-12

MINIMUM_CONTROL_SITE_EV=
0.07919352471801402

MINIMUM_CONTROL_DIMER_EV=
0.1583870494360280

MINIMUM_1000KG_CONTROL_FREE_ENERGY_SCALE_J=
1.063556252028522e8
```

## Finite-size selector window

```text
DINUCLEAR_STABILITY_T_MIN_K=
28.13102372293623

DINUCLEAR_LEAKAGE_T_MAX_K=
101.8315502857560

DINUCLEAR_77K_LEAKAGE=
1.989338055378181e-9

DINUCLEAR_77K_LEAKAGE_MARGIN=
290.1950942786034

DINUCLEAR_77K_MU_R=
0.9556137730170507

DINUCLEAR_77K_STABILITY_MARGIN=
1.643839124818559
```

## Balanced point

```text
BALANCED_T_K=
95.22770993335909

BALANCED_LEAKAGE_MARGIN=
3.385149110507368

BALANCED_CORRELATION_MARGIN=
3.385149110507362

BALANCED_STABILITY_MARGIN=
1.823739827829086
```

## Dimer EFT

```text
DIMER_BARE_DETUNING_EV=
-5

DIMER_PAIR_MIXING_EV=
0.8783524469661568

BARE_DIMER_SCALAR_COUPLING=
8.904546001587151e-12

DIMER_FRACTION_ZERO_PHI=
0.9717316000818251

DIMER_FRACTION_EARTH_PHI=
0.9701060143517443

FEYNMAN_HELLMANN_RELATIVE_ERROR=
3.079119804066939e-10
```

## Two-body contact at 3 angstrom

```text
PAIR_RADIUS_A=
3

C_PHI_EV_MINUS3=
9.536416387852626e-20

ATOMIC_EFT_CUTOFF_EV=
657.7566013333334

DIMENSIONLESS_PAIR_WILSON=
2.713818830692468e-11
```

## UV failures

```text
RELATIVISTIC_FERMION_DIMER_LOOP_TO_TARGET_MASS2=
1.155053548350539e19

RELATIVISTIC_SCALAR_DIMER_LOOP_TO_TARGET_MASS2=
2.310107096701078e19

GENERIC_ONE_LOOP_OPERATOR_MIXING=
6.332573977646111e-3

GENERIC_ONE_LOOP_LEAKAGE_EXCESS=
1.096936821356127e4
```

---

# 72. Exact next-session active frontier

The project should resume from:

```text
ACTIVE_FRONTIER=
RELATIVISTIC_PROTECTED_TWO_BODY_MATCH_OR_BRANCH_CLOSE
```

The active question is:

> **Can a technically natural local relativistic microscopic theory generate the material-specific two-body coefficient required by the dinuclear NR EFT while forbidding or sufficiently suppressing all one-body scalar couplings?**

Do not open another speculative branch until this is answered or clearly stalled.

The required low-energy target is:

```math
\mathcal{H}_{\phi,2}
=
C_\phi
\phi
A^\dagger B^\dagger BA
```

with representative:

```math
C_\phi
\approx
9.54\times10^{-20}\ {\mathrm{eV^{-3}}}
```

and one-body leakage below approximately:

```math
5.77\times10^{-7}
```

of the activated target-equivalent response.

The ultralight scalar must retain:

```math
m_\phi
\approx
3.95\times10^{-11}\ {\mathrm{eV}}
```

without fine-tuned cancellation.

---

# 73. Recommended first analytical gate next session

A strong next analytical gate should attempt to classify relativistic operator structures by symmetry.

The gate should ask:

1. What exact symmetry allows the desired multi-body/bound-state response?
2. Does that symmetry forbid $\phi\bar\psi\psi$-type one-body terms?
3. Does RG running regenerate them?
4. Does electroweak symmetry breaking regenerate them?
5. Does confinement/nuclear matching regenerate them?
6. Does integrating out the proposed mediator generate ordinary composition-dependent fifth forces?
7. Does the mechanism protect $m_\phi$?
8. Does the NR matching reproduce the correct sign and magnitude of $C_\phi$?

Do not accept:

```text
TREE_LEVEL_ONE_BODY_TERM=ZERO
```

as sufficient.

The loop/RG result is essential.

---

# 74. Claim-promotion rule for the current survivor

The protected dinuclear EFT must remain classified:

```text
PARAMETRIC_LOW_ENERGY_SURVIVOR
```

until all of the following are complete:

```text
RELATIVISTIC_OPERATOR_MATCH=PASS
ONE_BODY_LEAKAGE=PASS
ULTRALIGHT_NATURALNESS=PASS
INDEPENDENT_MATCH=PASS
EXACT_5KM_BOUND=PASS
STELLAR_CONSTRAINTS=PASS
COSMOLOGY=PASS
REAL_MATERIAL_MAPPING=PASS
```

Only then should discussion move toward:

```text
PHYSICAL_REALIZATION_CANDIDATE
```

Experimental accessibility and practical engineering would still be separate later stages.

---

# 75. Final scientific assessment at session close

The project has accomplished two substantially different things.

First, it has established a robust classical mathematical result:

> **Positive-energy, energy-condition-respecting stress-energy can produce a locally outward gravitational near field in static linearized GR.**

That is 006D.

Second, it has conducted a broad falsification campaign on possible ways to obtain useful repulsion without the impossible 006D stress-energy burden.

The strongest speculative survivor is now extremely narrow:

> **A ground-referenced ultralight scalar whose large opposite-sign charge appears only in a protected bound dinuclear material state through a genuinely two-body low-energy operator, with zero extra scalar charge on isolated constituents in the strict NR EFT.**

This survivor has passed:

```text
LOW_ENERGY_SIGN
LOW_ENERGY_COUPLING_MAGNITUDE
FINITE_PAYLOAD_STABILITY
THERMAL_SELECTIVITY_WINDOW
COOPERATIVE_CLUSTER_WINDOW
EXACT_PROJECTOR_LOGIC
FEYNMAN_HELLMANN
INDEPENDENT_TWO_BODY_REPRESENTATION
ATOMIC_EFT_PERTURBATIVITY
```

It has not passed:

```text
RELATIVISTIC_UV_COMPLETION
ONE_BODY_OPERATOR_MIXING
ULTRALIGHT_SCALAR_UV_NATURALNESS
EXACT_CURRENT_5KM_BOUND
FULL_STELLAR_PHYSICS
FULL_COSMOLOGY
REAL_MATERIAL_IDENTIFICATION
EXPERIMENT
ENGINEERING
```

That distinction must remain explicit.

---

# 76. Most important negative result from the session

The project should not interpret the survival of the NR EFT as evidence that generic UV physics can realize it.

In fact, the opposite was found.

Generic one-loop operator mixing is approximately:

```math
6.33\times10^{-3}
```

while allowed leakage is approximately:

```math
5.77\times10^{-7}
```

and a fundamental relativistic dimer destroys the ultralight scalar mass by approximately:

```math
10^{19}
```

relative to the desired $m_\phi^2$.

Therefore:

> **The low-energy architecture survives only if the relativistic microscopic theory contains a genuinely powerful protection mechanism.**

This is not a minor detail.

It is the dominant remaining theoretical obstacle.

---

# 77. Most important positive result from the session

The strongest positive result is not the precise $77,{\mathrm{K}}$ number or the $106,{\mathrm{MJ}}$ control scale.

It is the structural result:

```text
BOUND_STATE_RESPONSE
DOES_NOT_LOGICALLY_REQUIRE
ONE_BODY_RESPONSE
IN_A_STRICT_NR_COMPOSITE_EFT
```

This keeps alive a class of material-specific interactions that would otherwise have been dismissed immediately.

The next session must determine whether that low-energy separation can survive relativistic microscopic matching.

---

# 78. Carry-forward stop rule in one sentence

> **If the desired protected two-body scalar operator cannot be generated by a local technically natural relativistic theory without inducing forbidden one-body scalar charge, close the current fifth-force/material branch rather than adding new hidden structure.**

---

# 79. One-paragraph handoff for the next session

The strongest established project result remains 006D: an explicit finite, positive-energy, locally conserved, NEC/WEC/DEC-compatible static linearized-GR source with a locally outward near field and positive far-field active mass. The late 010E search then investigated whether a much more practical ground-referenced scalar fifth force could produce order-$1g$ repulsion. After rejecting localized hidden carriers, material-created hidden condensates, direct electron-mass portals, simple electron mediators, continuous structural selectors, universal high-spin charge, accidental polynomial selectors, fundamental relativistic dimers, and generic unprotected UV matching, the remaining low-energy survivor is a cooperative dinuclear bound-state scalar response. In the selected NR EFT, the dimer carries target coupling $8.638\times10^{-12}$ while isolated constituents carry exactly zero extra scalar charge; Feynman-Hellmann and an independent two-body contact representation agree, and a one-ton dinuclear material model possesses a finite thermal/stability window. The decisive unresolved question is now whether a technically natural relativistic microscopic theory can generate the required two-body coefficient while suppressing induced one-body couplings below the approximately $5.77\times10^{-7}$ leakage allowance and preserving the $3.95\times10^{-11},{\mathrm{eV}}$ mediator mass. That is the only high-priority frontier that should be opened next.

---

# 80. Final status block

```text
PROJECT=ANTIGRAVITY_RESEARCH

REGRESSION_BASELINE=94_PASSED

STRONGEST_ESTABLISHED_RESULT=
006D_FINITE_POSITIVE_ENERGY_LINEARIZED_GR_LOCAL_REPULSION

PUBLIC_HEADLINE=
WE_HAVE_A_MATHEMATICAL_CONSTRUCTION_FOR_ANTIGRAVITY_LIKE_GRAVITATIONAL_REPULSION

CLASSICAL_PRACTICAL_SOURCE=
NO

CURRENT_SPECULATIVE_BRANCH=
GROUND_REFERENCED_ULTRALIGHT_SCALAR

CURRENT_LOW_ENERGY_HOST=
COOPERATIVE_DINUCLEAR_BOUND_COMPOSITE

CURRENT_SELECTOR=
FIXED_MATERIAL_IDENTITY_X_PRODUCT_OF_HIGH_SPIN_PROJECTORS

CURRENT_LOW_ENERGY_OPERATOR=
C_PHI_PHI_A_DAGGER_B_DAGGER_B_A

ISOLATED_CONSTITUENT_EXTRA_CHARGE_IN_STRICT_NR_EFT=
ZERO

BOUND_DIMER_EXTRA_CHARGE=
NONZERO

FEYNMAN_HELLMANN=
PASS

INDEPENDENT_TWO_BODY_REPRESENTATION=
PASS

FINITE_SIZE_SELECTOR_WINDOW=
PASS_IN_SELECTED_MODEL

DINUCLEAR_77K_LEAKAGE_MARGIN=
290.195

DINUCLEAR_77K_STABILITY_MARGIN=
1.64384

FUNDAMENTAL_RELATIVISTIC_DIMER=
REJECTED

GENERIC_UNPROTECTED_RELATIVISTIC_MATCH=
REJECTED

PROTECTED_RELATIVISTIC_MICROSCOPIC_MATCH=
NOT_ESTABLISHED

ACTUAL_MICROSCOPIC_ORIGIN_OF_C_PHI=
NOT_ESTABLISHED

KNOWN_REAL_MATERIAL_WITH_REQUIRED_PORTAL=
NO

CURRENT_EXACT_5KM_BOUND=
NOT_CLOSED

FULL_STELLAR_SAFETY=
NOT_ESTABLISHED

FULL_COSMOLOGICAL_SAFETY=
NOT_ESTABLISHED

PRACTICAL_ANTIGRAVITY_DEVICE=
NO

NEW_PHYSICS_DISCOVERY=
NO

NOVELTY=
NOT_ESTABLISHED

ACTIVE_NEXT_QUESTION=
CAN_A_PROTECTED_RELATIVISTIC_MICROSCOPIC_THEORY_GENERATE_THE_REQUIRED_TWO_BODY_OPERATOR_WITHOUT_ONE_BODY_LEAKAGE_OR_ULTRALIGHT_SCALAR_NATURALNESS_FAILURE

NEXT=
RELATIVISTIC_PROTECTED_TWO_BODY_MATCH_OR_BRANCH_CLOSE
```

### END NOTE — AUGUST 28, 2026 — 010E-Y SESSION CLOSEOUT

These are ready to paste as the carry-forward section of `NOTES.md`; they preserve the 94-test checkpoint, the O–Y decision chain, and the current UV stop-rule frontier without promoting the low-energy dimer construction beyond what the calculations support.



### END NOTE - AUGUST 28 2026 - 23:25 CST


### BEGIN NOTE - AUGUST 29 2026 - 02:15 CST


# ANTIGRAVITY_RESEARCH — Comprehensive Carry-Forward Notes Through 012G

**Session closeout:** August 29, 2026
**Current active frontier:** Relativistic coherent-field expectation value of the ghost-free nonlocal $O(G\hbar^2)$ repulsive term
**Known-solution regression baseline:** `94 passed`
**Practical antigravity device:** `NOT_ESTABLISHED`

---

# 1. Purpose of these notes

These notes are the authoritative conversational handoff for the next research session.

They are intended to preserve:

* the full scientific state reached through Gate 012G;
* the strongest established project result;
* all important positive and negative results from this session;
* explicit mathematical proofs for the project-derived results that now matter;
* the precise boundaries of every claim;
* branches that should not be reopened without genuinely new information;
* repository and validation status;
* unresolved theoretical and empirical questions;
* the shortest high-information path toward determining whether practical antigravity is physically possible.

The next session should read these notes alongside:

```text
ANTIGRAVITY_RESEARCH_CODEBUNDLE_20260828-234920.md
RESEARCH_BUILDPLAN.md
FORMATTING_AND_CODE_STANDARDS.md
NOTES.md
README.md
journal/2026-08-28_006d_constructive_linearized_gr_repulsion.md
```

Important:

The checked-in `RESEARCH_BUILDPLAN.md` and `README.md` snapshot used at the start of this session are now behind the live research frontier. They remain authoritative for methodology, claim discipline, the 006D result, and the previously completed 010E-Y low-energy result, but their stated active frontier at protected scalar matching has been superseded by the work recorded here.

The next session must therefore use this handoff to avoid restarting completed branches.

---

# 2. Governing research discipline

The project remains governed by the following rule:

> The objective is not to find equations containing a repulsive sign. The objective is to identify a physically consistent, experimentally viable, controllable mechanism that produces useful gravitational repulsion or an operationally equivalent force on neutral matter.

The repository success ladder remains:

```text
LEVEL_0  = MATHEMATICAL_SIGN
LEVEL_1  = OPERATIONAL_REPULSION
LEVEL_2  = GOVERNING_THEORY_CONSISTENCY
LEVEL_3  = SOURCE_OR_CHARGE_CONSISTENCY
LEVEL_4  = FINITE_LOCALIZATION
LEVEL_5  = CONSERVATION
LEVEL_6  = STABILITY_AND_NATURALNESS
LEVEL_7  = MICROSCOPIC_PHYSICAL_REALIZATION
LEVEL_8  = EMPIRICAL_VIABILITY
LEVEL_9  = MATERIAL_AND_CONTROL_REALIZATION
LEVEL_10 = EXPERIMENTAL_ACCESSIBILITY
LEVEL_11 = PRACTICAL_ANTIGRAVITY
```

These levels must never be conflated.

A mathematical repulsive force is not a material.

A material is not an experiment.

An experiment is not a practical antigravity device.

The project buildplan explicitly prioritizes tasks that maximize:

```text
INFORMATION_GAIN
+
FALSIFICATION_POWER
+
INDEPENDENT_VERIFICATION_VALUE
+
ABILITY_TO_CLOSE_AN_ENTIRE_BRANCH
```

and specifically instructs us not to increase model complexity merely to protect a failing branch.

---

# 3. Repository state at the end of the session

At the beginning of this session a fresh codebundle was generated:

```text
ANTIGRAVITY_RESEARCH_CODEBUNDLE_20260828-234920.md
INCLUDED_FILES=85
BUNDLE_MIB=1.06
STATUS=GREEN
```

Documentation and the 006D journal were then committed:

```text
COMMIT=c0c37f3
MESSAGE="updated docs and notes"
```

and pushed:

```text
0fe3222..c0c37f3  main -> main
```

All later research gates repeatedly printed an empty:

```text
=== REPOSITORY STATE ===
```

from:

```bash
git status --short
```

Therefore the demonstrated working tree remained clean throughout the analytical gates.

The known-solution regression suite repeatedly produced:

```text
94 passed
```

The permanent repository baseline is independently documented as `94 passed`.

Important implementation status:

The late-session gates:

```text
010E-Z1
010E-Z2
010E-Z3
011A
012A
012B
012C
012C-V2
012D
012E
012F
012G
```

were run primarily as shell/Python analytical preflights.

Do not assume all of them currently exist as permanent:

```text
simulations/*.py
tests/*.py
results/*.csv
```

files.

Before the next major research session closes, the strongest durable new results should be promoted into permanent code/tests/journal documentation.

---

# 4. Strongest established project result remains 006D

The strongest established project-derived gravitational result remains Simulation 006D.

The exact supported claim is:

> Within static linearized general relativity, there exists an explicit finite-radius, finite-thickness, nonsingular, positive-energy, locally conserved type-I stress-energy configuration satisfying NEC, WEC, and DEC whose calculated near gravitational field points outward while its far-field active mass remains positive.

The repository's 006D journal permanently records this construction and its assumptions.

The verified diagnostics include:

```text
MAX_CONTROL_VOLUME_CONSERVATION_RESIDUAL=
3.103073353827313e-14

MAX_DEC_VIOLATION=
0

MIN_NEC_MARGIN=
0

MAX_INTEGRATED_STRESS_TRACE=
2.922107000813e-13
```

The two independent field quadratures gave:

```text
FIELD_FACTOR_GL64=
2.352695737495157e-01

FIELD_FACTOR_NESTED=
2.352695737495351e-01

FIELD_METHOD_ABS_DIFFERENCE=
1.942890293094024e-14
```

The finite source coefficient is:

```math
C_{\mathrm{finite}}
=
23.591586299249
```

in:

```math
M_{\mathrm{equiv}}
=
C\frac{a h^2}{G}
```

The independently established conserved thin architecture is:

```math
C_{\mathrm{thin}}
=
23.426710175391
```

The finite source is therefore only approximately:

```math
0.704\%
```

above the thin result.

---

# 5. Mathematical proof underlying 006D

This proof must remain in the carry-forward context because it is the strongest established result.

## 5.1 Linearized active gravitational source

Use metric signature $(-,+,+,+)$.

For a static type-I stress tensor:

```math
T_{\hat\mu\hat\nu}
=
\mathrm{diag}
\left(
\epsilon,
p_r,
p_\phi,
p_z
\right)
```

the static weak-field Einstein equations give:

```math
\nabla^2\Phi
=
\frac{4\pi G}{c^2}
\left(
\epsilon+p_r+p_\phi+p_z
\right)
```

Define:

```math
S
=
\epsilon+p_r+p_\phi+p_z
```

The Green-function potential is:

```math
\Phi(\mathbf{x})
=
-\frac{G}{c^2}
\int
\frac{S(\mathbf{x}')}
{|\mathbf{x}-\mathbf{x}'|}
\,d^3x'
```

and:

```math
\mathbf{a}
=
-\nabla\Phi
```

For an axisymmetric source and an axial target:

```math
a_z(h)
=
-\frac{2\pi G}{c^2}
\int dz
\int_0^\infty dr\,
rS(r,z)
\frac{h-z}
{\left[r^2+(h-z)^2\right]^{3/2}}
```

The project's sign convention is:

```text
a_z > 0 = outward
a_z < 0 = inward
```

---

## 5.2 Exact local conservation construction

Define:

```math
q(r)
=
r p_r(r)
```

and choose:

```math
p_\phi(r)
=
\frac{dq}{dr}
```

with:

```math
p_z=0
```

The cylindrical radial conservation equation is:

```math
\frac{dp_r}{dr}
+
\frac{p_r-p_\phi}{r}
=
0
```

Since:

```math
p_r
=
\frac{q}{r}
```

we have:

```math
\frac{dp_r}{dr}
=
\frac{q'}{r}
-
\frac{q}{r^2}
```

and:

```math
\frac{p_r-p_\phi}{r}
=
\frac{q}{r^2}
-
\frac{q'}{r}
```

Therefore:

```math
\frac{dp_r}{dr}
+
\frac{p_r-p_\phi}{r}
=
0
```

identically.

Thus radial stress-energy conservation is built into the source rather than numerically approximated.

---

## 5.3 Energy-condition proof

Choose:

```math
\epsilon
=
\max
\left(
|p_r|,
|p_\phi|
\right)
```

with:

```math
p_z=0
```

Then:

```math
\epsilon\ge0
```

and:

```math
|p_r|\le\epsilon
```

```math
|p_\phi|\le\epsilon
```

```math
|p_z|=0\le\epsilon
```

which is precisely the pointwise type-I dominant energy condition.

Therefore:

```text
DEC=PASS
```

and DEC implies WEC and NEC for this type-I stress tensor.

The numerical result:

```text
MIN_NEC_MARGIN=0
```

means parts of the optimized source saturate NEC; it does not mean NEC was ignored.

---

## 5.4 Positive far-field active mass

The integrated stress trace is numerically zero to approximately:

```text
2.92e-13
```

so the far-field active mass is dominated by the positive energy integral.

The numerical calculation gives:

```text
ACTIVE_MASS_FACTOR=
1.110076490539859e+01
```

which is positive.

Thus:

```text
LOCAL_NEAR_FIELD=OUTWARD
FAR_FIELD_ACTIVE_MASS=POSITIVE
```

can coexist.

This is local, not global, antigravity.

---

# 6. Static classical energy scaling remains catastrophic

A previously established static one-sided conserved-DEC bound gives:

```math
a_{\mathrm{out}}
\le
\frac{GE}{c^2h^2}
```

and therefore:

```math
M
=
\frac{E}{c^2}
\ge
\frac{a h^2}{G}
```

For:

```math
a=g
```

and:

```math
h=1\,{\mathrm{m}}
```

the absolute coefficient-one optimistic floor is:

```text
M_MIN=
1.469315134171374e11 kg
```

The actual 006D coefficient gives:

```text
M_006D=
3.466347478859659e12 kg
```

with rest-energy equivalent:

```text
E_006D=
3.115397747926430e29 J
```

Therefore the classical GR branch solved the sign problem but did not solve practicality.

---

# 7. State entering this session: 010E-Y scalar composite EFT

Before the new Z gates, the leading speculative branch was a ground-referenced ultralight scalar fifth force with material-specific two-body response.

The low-energy construction used constituent fields $A,B$ and a dimer field $D$ with conserved particle number.

The interaction included:

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

and:

```math
H_\phi
=
g_D\phi D^\dagger D
```

Because the Hamiltonian preserves particle number, isolated one-particle sectors cannot mix with the bound dimer sector.

Consequently:

```math
\frac{dE_A}{d\phi}=0
```

```math
\frac{dE_B}{d\phi}=0
```

while the bound state has:

```math
\frac{dE_{\mathrm{bound}}}{d\phi}
=
g_D Z_D
```

The explicit 010E-Y numbers included:

```text
TARGET_DINUCLEAR_COUPLING=
8.638353631211470e-12

BARE_DIMER_SCALAR_COUPLING=
8.904546001587151e-12

DIMER_FRACTION_AT_EARTH_PHI=
0.9701060143517443

ISOLATED_A_SCALAR_CHARGE=
0

ISOLATED_B_SCALAR_CHARGE=
0
```

and finite-difference/Feynman-Hellmann agreement at relative error:

```text
3.079119804066939e-10
```

The independent contact representation was:

```math
\mathcal{H}_{\phi,2}
=
C_\phi
\phi
A^\dagger B^\dagger BA
```

with:

```text
C_PHI_EV_MINUS3=
9.536416387852626e-20

ATOMIC_EFT_CUTOFF_EV=
657.7566013333334

DIMENSIONLESS_PAIR_WILSON=
2.713818830692468e-11
```

The correct conclusion was:

> Locality and Feynman-Hellmann alone do not forbid a bound-state-specific scalar response in a strict low-energy particle-number-conserving nonrelativistic EFT.

This was never a relativistic UV completion.

---

# 8. 010E-Z1 — symmetry/background portal preflight

Z1 reproduced:

```text
MAX_ORDINARY_ONE_BODY_G_N=
3.470636550308009e-20

EARTH_PHI_EV=
1.690631280830914e10

C_PHI_EV_MINUS3=
9.536416387852626e-20

DIMENSIONLESS_PAIR_WILSON=
2.713818830692468e-11

GENERIC_QUADRATIC_ONE_BODY_C2_MAX_EV_MINUS1=
1.026432135043146e-30

EQUIVALENT_C2_SUPPRESSION_SCALE_GEV=
9.742485312562478e20

EQUIVALENT_SCALE_OVER_REDUCED_PLANCK=
4.001020662243317e2
```

Classification:

```text
PHASE_NUMBER_SYMMETRY_PAIR_PROTECTION=REJECTED

DUAL_CHARGE_CONJUGATION_OPERATOR_WITNESS=
YES_ABSTRACT_VACUUM_LEVEL

DUAL_CHARGE_CONJUGATION_EXACT_SM_PROTECTION=NO

Z2_ONLY_LINEAR_PORTAL_PROTECTION=INSUFFICIENT

BACKGROUND_INDUCED_QUADRATIC_PORTAL_PROBLEM=SEVERE
```

## Z1 proof of the background-induced portal issue

Suppose a symmetry forbids the linear portal:

```math
\phi\bar N N
```

but allows:

```math
c_2\phi^2\bar N N
```

Write:

```math
\phi
=
\phi_\oplus+\varphi
```

Then:

```math
\phi^2
=
\phi_\oplus^2
+
2\phi_\oplus\varphi
+
\varphi^2
```

Therefore:

```math
c_2\phi^2\bar N N
\supset
2c_2\phi_\oplus
\varphi\bar N N
```

which is an effective ordinary one-body linear coupling:

```math
g_{\mathrm{eff}}
=
2c_2\phi_\oplus
```

Requiring:

```math
g_{\mathrm{eff}}
\le
3.470636550308009\times10^{-20}
```

gives:

```math
c_2
\le
\frac{
3.470636550308009\times10^{-20}
}{
2\left(
1.690631280830914\times10^{10}\ {\mathrm{eV}}
\right)
}
```

or:

```math
c_2
\lesssim
1.026432135043146\times10^{-30}
\ {\mathrm{eV^{-1}}}
```

The corresponding inverse scale is:

```math
\Lambda_{c_2}
\sim
9.7425\times10^{20}\ {\mathrm{GeV}}
```

approximately:

```math
400
```

reduced Planck masses.

This does not prove all such operators impossible, but demonstrates that simple $Z_2$ protection is inadequate in the assumed terrestrial background.

---

# 9. 010E-Z2 — simple relativistic mediator leakage

Consider:

```math
\mathcal{L}
\supset
-\frac12
\left(
M_X^2+\kappa\phi
\right)X^2
-
g_A X\bar A A
-
g_B X\bar B B
```

Integrating out $X$ gives approximately:

```math
C_\phi
\sim
\frac{
\kappa g_Ag_B
}{
M_X^4
}
```

The same mediator generates a one-body self-energy response.

In the regime:

```math
M_X\ll m_A
```

the derivative behaves as:

```math
\left|
\frac{\partial m_A}
{\partial M_X^2}
\right|
\sim
\frac{
g_A^2
}{
16\pi M_X
}
```

For balanced couplings and the selected atomic contact normalization, the minimum one-body/pair ratio became:

```text
SINGLE_MEDIATOR_MIN_ONE_BODY_OVER_PAIR=
6.249998918419297e-02
```

while the permitted leakage fraction was:

```text
5.772961445324848e-7
```

Therefore:

```text
SINGLE_MEDIATOR_LEAKAGE_EXCESS=
1.082633060624504e5
```

The minimal single-mediator UV completion is rejected by approximately five orders of magnitude.

The numerical loop integral independently reproduced the asymptotic formula:

```text
EXACT_OVER_ASYMPTOTIC=
9.999998269470876e-1
```

---

# 10. 010E-Z2 naturalness/multiplicity envelope

Grant a stronger structure with $N$ independently protected mediator pairs.

Using the deliberately optimistic conditions:

```math
g_Ag_B
\le
4\pi
```

and scalar mass naturalness:

```math
\delta m_\phi^2
\sim
\frac{
N\mu^2
}{
16\pi^2
}
\le
m_\phi^2
```

gives:

```math
\mu
\le
\frac{
4\pi m_\phi
}{
\sqrt N
}
```

Tree matching then yields:

```math
C_{\phi,\max}
=
\frac{
16\pi^2m_\phi\sqrt N
}{
M^4
}
```

so:

```math
N
\ge
\left[
\frac{
C_\phi M^4
}{
16\pi^2m_\phi
}
\right]^2
```

Numerically:

```text
M=LAMBDA_EFT:
N_MIN=9

M=2 LAMBDA_EFT:
N_MIN=2101

M=3 LAMBDA_EFT:
N_MIN=53826

M=5 LAMBDA_EFT:
N_MIN=3204644
```

This already strongly disfavors an ordinary controlled heavy-mediator contact origin.

---

# 11. 010E-Z3 — dual-current terrestrial-background leakage

The most favorable simple protected dual-current architecture was modeled by:

```math
\mathcal{L}
\supset
g_A X_\mu J_A^\mu
+
g_B Y_\mu J_B^\mu
+
\mu\phi X_\mu Y^\mu
```

with equal mediator mass $M$.

The field-dependent mediator matrix is:

```math
K(\phi)
=
\begin{pmatrix}
M^2 & \mu\phi \\
\mu\phi & M^2
\end{pmatrix}
```

and:

```math
K^{-1}
=
\frac{1}{
M^4-\mu^2\phi^2
}
\begin{pmatrix}
M^2 & -\mu\phi \\
-\mu\phi & M^2
\end{pmatrix}
```

The desired cross-sector term exists.

However the diagonal interactions depend on $\phi^2$.

Expanding:

```math
\phi
=
\phi_\oplus+\varphi
```

therefore creates a linear scalar response in the same-sector interaction.

For small mixing:

```math
R_{\mathrm{same}}
\sim
\frac{
\mu\phi_\oplus
}{
M^2
}
```

---

# 12. Z3 Cauchy-Schwarz lower bound

For $N$ channels:

```math
C_\phi
\approx
\frac{1}{M^4}
\sum_i
g_{Ai}g_{Bi}\mu_i
```

while the background-induced same-sector response scales as:

```math
C_{AA}
\approx
\frac{
\phi_\oplus
}{
M^6
}
\sum_i
g_{Ai}^2\mu_i^2
```

Cauchy-Schwarz gives:

```math
\left(
\sum_i
g_{Ai}g_{Bi}\mu_i
\right)^2
\le
\left(
\sum_i
g_{Ai}^2\mu_i^2
\right)
\left(
\sum_i
g_{Bi}^2
\right)
```

Using:

```math
g_{Bi}^2
\le
4\pi
```

gives:

```math
\sum_i
g_{Bi}^2
\le
4\pi N
```

and hence:

```math
\sum_i
g_{Ai}^2\mu_i^2
\ge
\frac{
C_\phi^2M^8
}{
4\pi N
}
```

Substitution into $C_{AA}$ yields:

```math
\frac{
|C_{AA}|
}{
|C_\phi|
}
\gtrsim
\frac{
C_\phi\phi_\oplus M^2
}{
4\pi N
}
```

Therefore the leakage requirement imposes:

```math
N
\gtrsim
\frac{
C_\phi\phi_\oplus M^2
}{
4\pi f_{\mathrm{leak}}
}
```

The exact numerical gate found:

```text
M=LAMBDA_EFT:
N_MIN_EXACT=97

M=1.5 LAMBDA_EFT:
N_MIN_EXACT=217

M=2 LAMBDA_EFT:
N_MIN_EXACT=2101

M=3 LAMBDA_EFT:
N_MIN_EXACT=53826

M=5 LAMBDA_EFT:
N_MIN_EXACT=3204644
```

A single channel could satisfy the background bound only for:

```text
M_MAX=
67.07909701897688 eV
```

corresponding to a range:

```text
2.941705973534134 nm
```

which is already far larger than the selected approximately $3,\mathrm{\AA}$ local pair scale.

Classification:

```text
SINGLE_CHANNEL_CONTACT_COMPLETION=REJECTED

LOW_COMPLEXITY_DUAL_CURRENT_COMPLETION=
STRONGLY_DISFAVORED
```

---

# 13. Z4 analytical gauge-current realization issue

This was an analytical argument performed in-session rather than a separately run permanent numerical gate.

It must therefore be classified more conservatively than Z1-Z3.

For an exact gauge current:

```math
Q
=
\int d^3x\,J^0
```

the charge is the generator of the gauge symmetry.

For a composite built from microscopic constituents:

```math
Q_{\mathrm{composite}}
=
\sum_i q_i
```

Binding changes matrix elements and spatial distributions, but does not ordinarily create a new exact additive gauge charge from constituents whose total microscopic charge is zero.

Therefore a proposed selector of the form:

```text
ordinary constituents = uncharged
specific bound high-spin dimer = large exact gauge charge
```

is incompatible with the simplest exact gauge-current interpretation.

The next possible realization would require higher-dimensional transition, polarizability, or collective operators.

That is a qualitatively new microscopic mechanism rather than a simple completion of the existing current model.

Accordingly the 010E material-scalar branch was closed or strongly demoted rather than protected by adding arbitrary new fields.

Correct status:

```text
LOW_ENERGY_010E_Y_EFT=
VALID_PARAMETRIC_CONSTRUCTION

SIMPLE_RELATIVISTIC_UV_COMPLETION=
REJECTED_OR_STRONGLY_DISFAVORED

GLOBAL_QFT_NO_GO=
NOT_ESTABLISHED

KNOWN_REAL_MATERIAL=
NO
```

---

# 14. 011A — periodic dynamic GR

011A tested whether periodic dynamics could evade the static $ah^2/G$ scaling.

The run reproduced:

```text
STATIC_DEC_COEFFICIENT_ONE_MASS_FLOOR_KG=
1.469315134171374e11

006D_1G_1M_MASS_EQUIVALENT_KG=
3.466347478859659e12
```

and a $1g$, $1,{\mathrm{m}}$ gravitational-wave benchmark:

```text
BETA=0.10
FLUX=
8.593824393981e20 W/m^2
```

while the mean first-order oscillatory acceleration was:

```text
-3.609526609646901e-16 m/s^2
```

consistent with zero.

---

# 15. Proof: periodic linearized GR DC component is static

The linearized field equation schematically is:

```math
\Box\bar h_{\mu\nu}
=
-\frac{
16\pi G
}{
c^4
}
T_{\mu\nu}
```

For a periodic steady state, average over one complete period $T$.

Because:

```math
\left\langle
\frac{
\partial^2\bar h_{\mu\nu}
}{
\partial t^2
}
\right\rangle
=
\frac{1}{T}
\left[
\frac{
\partial\bar h_{\mu\nu}
}{
\partial t
}
\right]_0^T
=
0
```

the averaged field equation becomes static:

```math
\nabla^2
\left\langle
\bar h_{\mu\nu}
\right\rangle
=
-\frac{
16\pi G
}{
c^4
}
\left\langle
T_{\mu\nu}
\right\rangle
```

Stress-energy conservation gives:

```math
\partial_tT^{0\nu}
+
\partial_jT^{j\nu}
=
0
```

Period averaging gives:

```math
\partial_j
\left\langle
T^{j\nu}
\right\rangle
=
0
```

Therefore the zero-frequency source is a static conserved averaged stress tensor.

If instantaneous stress-energy remains within the DEC cone with common time orientation, convexity preserves DEC under averaging.

Thus under the same one-sided linearized assumptions as the static bound:

```text
PERIODIC_DYNAMIC_GR_DC_PARAMETRIC_ESCAPE=
NO
```

The genuinely radiative component remains oscillatory rather than producing sustained common-mode lift.

This is not a theorem against arbitrary nonperiodic or strong-field nonlinear GR.

---

# 16. 012A — healthy linear modified gravity sign prefilter

012A examined a broad healthy universally coupled spin-0/spin-2 linear class.

Write:

```math
\Phi(r)
=
-\frac{GM}{r}
\left[
1+
\sum_i
\alpha_i e^{-\mu_i r}
\right]
```

with healthy positive residues:

```math
\alpha_i\ge0
```

Then:

```math
a_r
=
-\frac{GM}{r^2}
\left[
1+
\sum_i
\alpha_i
(1+\mu_i r)
e^{-\mu_i r}
\right]
```

Every added factor is nonnegative:

```math
\alpha_i
(1+\mu_i r)
e^{-\mu_i r}
\ge0
```

so:

```math
a_r<0
```

for ordinary positive masses.

The 50,000-case random positive-spectrum sweep found:

```text
POSITIVE_SPECTRAL_MIN_FORCE_FACTOR=
1.000000000000000
```

with no reversal.

A single Yukawa correction reverses only if:

```math
1+
\alpha(1+x)e^{-x}
<
0
```

which requires:

```math
\alpha
<
-\frac{
e^x
}{
1+x
}
```

Thus the standard linear spin-0/spin-2 route requires a negative effective residue/weight.

Correct classification:

```text
HEALTHY_LINEAR_UNIVERSAL_SPIN0_SPIN2_ANTIGRAVITY=
REJECTED
```

This is a class-level sign result under its assumptions, not a global modified-gravity theorem.

---

# 17. 012B — healthy nonlinear scalar screening

012B tested whether standard nonlinear screening could reverse an attractive universal scalar force.

Write the static spherical field equation schematically as:

```math
\frac1{r^2}
\frac{d}{dr}
\left[
r^2 Z(\phi,\phi')\phi'
\right]
=
\frac{
\beta\rho
}{
M_{\mathrm{Pl}}
}
```

Integrating around positive enclosed mass gives:

```math
Z\phi'
\propto
\beta M(<r)
```

For the healthy physical branch:

```math
Z>0
```

Therefore:

```math
\mathrm{sgn}(\phi')
=
\mathrm{sgn}(\beta)
```

A universally coupled test body experiences:

```math
a_\phi
=
-\frac{
\beta\phi'
}{
M_{\mathrm{Pl}}
}
```

so:

```math
\beta\phi'>0
```

and therefore:

```math
a_\phi<0
```

The sign of $\beta$ does not help because it appears once in sourcing the field and once in the test-body force.

Hence:

```text
HEALTHY_UNIVERSAL_KINETIC_SCREENING_SIGN_REVERSAL=
REJECTED
```

Screening can modify magnitude but not reverse sign without:

* opposite source/test charges;
* negative kinetic response;
* an environmental coupling-sign transition;
* a different vacuum/domain;
* nonuniversality;
* a theory outside this class.

The numerical gate found zero outward cases in 50,000 healthy kinetic-screening trials and zero standard chameleon/symmetron reversal cases.

---

# 18. 012C / 012C-V2 — canonical ghost-free nonlocal gravity

For the canonical exponential nonlocal form factor, the point-mass potential is:

```math
\Phi(r)
=
-\frac{GM}{r}
\mathrm{erf}
\left(
\frac{M_s r}{2}
\right)
```

Define:

```math
z
=
\frac{M_sr}{2}
```

Then:

```math
a_r
=
-\frac{GM}{r^2}
F(z)
```

with:

```math
F(z)
=
\mathrm{erf}(z)
-
\frac{
2z
}{
\sqrt\pi
}
e^{-z^2}
```

The exact derivative is:

```math
F'(z)
=
\frac{
4z^2
}{
\sqrt\pi
}
e^{-z^2}
```

For:

```math
z>0
```

we have:

```math
F'(z)>0
```

and:

```math
F(0)=0
```

Therefore:

```math
F(z)>0
```

for all finite $z>0$.

Thus:

```math
a_r<0
```

everywhere.

Conclusion:

```text
CANONICAL_EXPONENTIAL_GHOST_FREE_IDG_FORCE=
ATTRACTIVE_AT_ALL_FINITE_POSITIVE_RADII

SHORT_DISTANCE_EFFECT=
ATTRACTION_SOFTENS_TO_ZERO
```

The original 012C failed only because a double-precision finite-difference tolerance was too strict:

```text
RELERR=
1.725711604204034e-08

ASSERTION=
<1e-08
```

012C-V2 replaced that check with 80-digit differentiation and obtained maximum derivative relative error:

```text
1.969818344295905e-81
```

Thus the original failure was numerical validation fragility, not physics.

---

# 19. Important correction: sign-changing real-space kernels do not automatically imply ghosts

A naive argument suggested that sign-changing nonlocal response might necessarily correspond to negative spectral weight/ghosts.

Literature verification showed that this is too strong.

The ghost-free infinite-derivative literature studies higher-order entire form factors, and published work shows oscillatory real-space behavior can arise without adding ordinary extra propagator poles.

The 2025 paper:

**Vinckers, de la Cruz-Dombriz, Mazumdar — “Smearing out contact terms in ghost-free infinite derivative quantum gravity”**

explicitly computes linearized single-graviton exchange between spinless particles and finds a smeared nonlocal $O(G\hbar^2)$ correction with nonzero finite-separation support.

Therefore:

```text
SIGN_CHANGING_REAL_SPACE_RESPONSE
!=
AUTOMATIC_GHOST
```

This correction prevented us from prematurely closing a genuine loophole.

---

# 20. 012D — higher-order $GF_N$ classical force

The higher-order ghost-free family was reconstructed with:

```math
w_N(q)
=
e^{-q^{2N}}
```

and:

```math
I_N(x)
=
\int_0^\infty
dq\,
e^{-q^{2N}}
\frac{\sin(qx)}{q}
```

The classical force factor is:

```math
C_N(x)
=
\frac2\pi
\left[
I_N(x)-xJ_N(x)
\right]
```

where:

```math
J_N(x)
=
\int_0^\infty
dq\,
e^{-q^{2N}}
\cos(qx)
```

The force is:

```math
a_r
=
-\frac{GM}{r^2}
C_N(x)
```

The numerical scan found:

```text
TOTAL_CLASSICAL_REPULSIVE_GRID_POINTS=0
```

for:

```text
N=1,2,4,6,8,16,32
```

and also no reversal in the $N\rightarrow\infty$ sharp-cutoff limit.

Important quantitative observations included:

```text
N=2:
FIRST_PEAK_F≈1.3317
FIRST_TROUGH_F≈0.9286

N=4:
FIRST_PEAK_F≈1.5544
FIRST_TROUGH_F≈0.6373

N=16:
FIRST_PEAK_F≈1.66585
FIRST_TROUGH_F≈0.37657

N->infinity:
FIRST_PEAK_F≈1.67538
FIRST_TROUGH_F≈0.34863
```

Therefore:

```text
HIGHER_ORDER_GF_N_CLASSICAL_FORCE_OSCILLATES=
YES

CLASSICAL_FORCE_SIGN_REVERSAL_FOUND=
NO
```

This is a strong numerical result for the tested family, not a theorem against all possible ghost-free nonlocal theories.

---

# 21. 012E — major new project-derived total-force result

This was the most important positive theoretical result of the session.

The published 2025 $GF_1$ static two-spinless-particle potential contains:

```math
V(r)
=
-\frac{
Gm_A m_B
}{
r
}
\mathrm{erf}
\left(
\frac{r}{2\ell}
\right)
+
\frac{
G\hbar^2
}{
2\sqrt\pi c^2\ell^3
}
e^{-r^2/(4\ell^2)}
```

The second term is a smeared nonlocal analogue of the local contact term.

It occurs in the published linearized single-graviton-exchange result.

It must not be called a one-loop correction.

Define:

```math
x
=
\frac r\ell
```

and:

```math
\eta
=
\frac{
\hbar^2
}{
m_A m_B c^2\ell^2
}
```

The signed total force normalized to the ordinary Newtonian magnitude can be written:

```math
S_N(x,\eta)
=
-C_N(x)
+
\eta Q_N(x)
```

where positive $S_N$ means outward force.

---

# 22. Exact $GF_1$ force-reversal proof

For $N=1$:

```math
C_1(x)
=
\mathrm{erf}
\left(
\frac x2
\right)
-
\frac{x}{\sqrt\pi}
e^{-x^2/4}
```

and:

```math
Q_1(x)
=
\frac{
x^3
}{
4\sqrt\pi
}
e^{-x^2/4}
```

Expand for small $x$.

First:

```math
\mathrm{erf}
\left(
\frac x2
\right)
=
\frac{x}{\sqrt\pi}
-
\frac{x^3}{12\sqrt\pi}
+
O(x^5)
```

and:

```math
\frac{x}{\sqrt\pi}
e^{-x^2/4}
=
\frac{x}{\sqrt\pi}
-
\frac{x^3}{4\sqrt\pi}
+
O(x^5)
```

Therefore:

```math
C_1(x)
=
\frac{
x^3
}{
6\sqrt\pi
}
+
O(x^5)
```

Similarly:

```math
Q_1(x)
=
\frac{
x^3
}{
4\sqrt\pi
}
+
O(x^5)
```

Thus:

```math
S_1
=
\frac{x^3}{\sqrt\pi}
\left(
-\frac16
+
\frac{\eta}{4}
\right)
+
O(x^5)
```

The force is outward when:

```math
-\frac16
+
\frac{\eta}{4}
>
0
```

or:

```math
\eta>\frac23
```

Therefore:

> In the published linearized $GF_1$ two-spinless-particle potential, the complete force—not merely the correction term—reverses at sufficiently small separation whenever $\eta>2/3$.

This is a **project-derived consequence of a published potential**.

It is not claimed as an independent discovery until it receives external verification and literature comparison.

---

# 23. General $GF_N$ small-distance threshold

The relevant moments are:

```math
M_p
=
\int_0^\infty
dq\,
q^p e^{-q^{2N}}
=
\frac1{2N}
\Gamma
\left(
\frac{p+1}{2N}
\right)
```

The small-$x$ expansions give:

```math
C_N(x)
=
\frac{
2M_2
}{
3\pi
}
x^3
+
O(x^5)
```

and:

```math
Q_N(x)
=
\frac{
2M_4
}{
3\pi
}
x^3
+
O(x^5)
```

Therefore:

```math
\eta_{\mathrm{crit}}(0)
=
\frac{
M_2
}{
M_4
}
```

or:

```math
\eta_{\mathrm{crit}}(0)
=
\frac{
\Gamma\left(\frac{3}{2N}\right)
}{
\Gamma\left(\frac{5}{2N}\right)
}
```

For $N=1$ this exactly gives:

```math
\eta_{\mathrm{crit}}
=
\frac23
```

The numerical scan independently reproduced the analytic threshold.

---

# 24. 012E numerical total-force result

For reference:

```text
N=1:
ETA2_MAX_OUTWARD_FACTOR≈0.402621

N=2:
ETA2_MAX_OUTWARD_FACTOR≈0.136905

N=4:
ETA2_MAX_OUTWARD_FACTOR≈0.056902

N=8:
ETA2_MAX_OUTWARD_FACTOR≈0.047635

N=16:
ETA2_MAX_OUTWARD_FACTOR≈0.055367
```

Every tested order:

```text
N=1,2,4,8,16
```

showed total force reversal at the selected reference $\eta=2$.

Classification:

```text
TREE_LEVEL_GF_N_TOTAL_TWO_PARTICLE_FORCE_REVERSAL=
FOUND
```

This is one of the strongest mathematical sign results obtained after 006D.

---

# 25. 012E Compton-control result

For reduced Compton wavelengths:

```math
\lambda_A
=
\frac{\hbar}{m_Ac}
```

```math
\lambda_B
=
\frac{\hbar}{m_Bc}
```

we have:

```math
\sqrt{
\lambda_A\lambda_B
}
=
\ell\sqrt\eta
```

Define:

```math
\rho
=
\frac{
r
}{
\sqrt{\lambda_A\lambda_B}
}
=
\frac{x}{\sqrt\eta}
```

The $N=16$ scan found an interesting threshold point:

```text
X=
54.90343390565095

ETA=
7.940699127009948

RHO=
19.48364184189438
```

This was independently reconstructed with arbitrary precision.

Thus point-particle force reversal is not mathematically confined to:

```text
r < geometric mean Compton wavelength
```

at the level of the delta-particle potential.

This result initially appeared promising.

---

# 26. Ordinary-matter realization problem from 012E

For one ordinary proton at that $N=16$ operating point, the partner mass would need to be:

```text
2.147496400994147e-15 eV
```

whose reduced Compton wavelength is:

```text
9.188699003576949e7 m
```

For one electron the partner mass would need:

```text
3.943131257856524e-12 eV
```

with reduced Compton wavelength:

```text
5.004321882687376e4 m
```

Thus a naïve localized ordinary-particle plus ultralight-particle picture is not physically controlled.

This motivated 012F and 012G.

---

# 27. 012F — many-body coherent/planar scaling

012F asked whether the two-particle effect grows into a useful bulk force.

The full terminal output confirmed the results summarized here.

The first major result was:

```text
HOMOGENEOUS_COHERENT_BULK_O_G_HBAR2_FORCE=
ZERO_AT_LEADING_PAIRWISE_ORDER
```

This kills the naïve idea that merely having $N^2$ particle pairs gives an $N^2$ volume-enhanced antigravity field.

---

# 28. Proof: homogeneous bulk smeared-contact force is zero

The published smeared contact kernel may be written:

```math
f_0(\mathbf{r})
=
4\pi
\int
\frac{d^3k}{(2\pi)^3}
\frac{
e^{i\mathbf{k}\cdot\mathbf{r}}
}{
F(-k^2)
}
```

For an infrared-normalized form factor:

```math
F(0)=1
```

integrating over all space gives:

```math
\int d^3r\,
f_0(\mathbf{r})
=
4\pi
```

because:

```math
\int d^3r\,
e^{i\mathbf{k}\cdot\mathbf{r}}
=
(2\pi)^3\delta^3(\mathbf{k})
```

For homogeneous particle number density $n_0$:

```math
U_q(\mathbf{x})
=
\frac{
G\hbar^2
}{
c^2
}
\int
d^3x'\,
n_0
f_0(\mathbf{x}-\mathbf{x}')
```

so:

```math
U_q
=
\frac{
4\pi G\hbar^2 n_0
}{
c^2
}
```

which is spatially constant.

Therefore:

```math
\nabla U_q=0
```

Thus the smeared contact term cannot generate a force inside an infinite homogeneous medium at leading pairwise order.

Any macroscopic force must come from:

```text
BOUNDARIES
DENSITY_GRADIENTS
INTERFACES
```

not uniform bulk.

---

# 29. Proof: thin-sheet many-body result

For an infinite thin source sheet with surface mass density $\Sigma$, summing radial pair forces over the transverse plane gives:

```math
a_z
=
2\pi G\Sigma x
\int_x^\infty
du\,
\frac{
S_N(u)
}{
u^2
}
```

where:

```math
S_N
=
-C_N+\eta Q_N
```

The potential functions satisfy:

```math
C_N
=
P_N-xP_N'
```

and:

```math
Q_N
=
R_N-xR_N'
```

Observe:

```math
\frac{d}{dx}
\left(
\frac{P_N}{x}
\right)
=
\frac{
xP_N'-P_N
}{
x^2
}
=
-\frac{
C_N
}{
x^2
}
```

and similarly:

```math
\frac{d}{dx}
\left(
\frac{R_N}{x}
\right)
=
-\frac{
Q_N
}{
x^2
}
```

Therefore:

```math
x
\int_x^\infty
du\,
\frac{-C_N(u)}{u^2}
=
-P_N(x)
```

and:

```math
x
\int_x^\infty
du\,
\frac{Q_N(u)}{u^2}
=
R_N(x)
```

assuming the boundary terms vanish appropriately.

Hence:

```math
a_z
=
2\pi G\Sigma
\left[
-P_N(x)+\eta R_N(x)
\right]
```

Define:

```math
B_N(x,\eta)
=
2\pi
\left[
-P_N(x)+\eta R_N(x)
\right]
```

Then:

```math
a_z
=
G\Sigma B_N
```

and the surface mass necessary for $1g$ is:

```math
\Sigma_{1g}
=
\frac{
g
}{
GB_N
}
```

At fixed dimensionless $x,\eta$, this contains no explicit $\ell$.

Therefore shrinking the nonlocal length does not improve the required areal mass at the same dimensionless operating point.

---

# 30. 012F numerical macroscopic result

The Newtonian $1g$ infinite-sheet mass scale is:

```text
2.338487665631055e10 kg/m^2
```

The best tested $N\le64$ result with:

```text
rho >= 5
```

was:

```text
N=64

B=
4.432758473063044

SIGMA_1G=
3.314674469859113e10 kg/m^2

SIGMA_OVER_NEWTONIAN_SHEET=
1.417443640424175
```

The arbitrary-precision reconstruction gave:

```text
B=
4.432758473011125

SIGMA_1G=
3.314674469897937e10 kg/m^2
```

At the historical $0.004,\mathrm{eV}$ nonlocal scale:

```text
OPERATING_RADIUS=
6.059395472014241 mm

GEOMETRIC_COMPTON=
1.211879094402848 mm

R_OVER_COMPTON=
5

EQUAL_PARTICLE_MASS=
1.628272831104761e-4 eV
```

For:

```text
rho >= 10
```

no planar reversal was found for:

```text
N<=64
x<=300
```

The key result:

```text
POINT_PARTICLE_REPULSION=YES

OPTIMISTIC_DELTA_PARTICLE_PLANAR_REPULSION=YES

USEFUL_MACROSCOPIC_MASS_SCALING=
NO_IN_TESTED_CONTROLLED_CASE
```

---

# 31. 012G — Gaussian wavepacket / Compton consistency

012G was designed to test whether the repulsive contact-like effect survives when particles are not treated as mathematical delta functions.

For Gaussian one-particle densities:

```math
\rho_i(\mathbf{r})
\propto
e^{-r^2/(2\sigma_i^2)}
```

the momentum-space form factor is:

```math
\rho_i(\mathbf{k})
=
e^{-\sigma_i^2k^2/2}
```

For a pair, the interaction therefore acquires:

```math
\exp
\left[
-\frac{
k^2
}{
2
}
\left(
\sigma_A^2+\sigma_B^2
\right)
\right]
```

Define:

```math
A^2
=
\frac{
\sigma_A^2+\sigma_B^2
}{
2\ell^2
}
```

and retain:

```math
\eta
=
\frac{
\lambda_A\lambda_B
}{
\ell^2
}
```

Introduce a localization-control criterion:

```math
\sigma_i
\ge
\chi\lambda_i
```

---

# 32. Proof: wavepacket localization bound

From:

```math
\sigma_A^2
\ge
\chi^2\lambda_A^2
```

and:

```math
\sigma_B^2
\ge
\chi^2\lambda_B^2
```

we obtain:

```math
A^2
\ge
\frac{
\chi^2
}{
2\ell^2
}
\left(
\lambda_A^2+\lambda_B^2
\right)
```

AM-GM gives:

```math
\frac{
\lambda_A^2+\lambda_B^2
}{2}
\ge
\lambda_A\lambda_B
```

therefore:

```math
A^2
\ge
\chi^2
\frac{
\lambda_A\lambda_B
}{
\ell^2
}
```

or:

```math
A^2
\ge
\chi^2\eta
```

Hence:

```math
\frac{\eta}{A^2}
\le
\frac1{\chi^2}
```

This is the maximum quantum-contact strength available after imposing the Gaussian localization condition.

---

# 33. Proof: asymptotic critical localization threshold

Use the rescaled momentum:

```math
u=Aq
```

At large $A$ and finite $N$:

```math
e^{-(u/A)^{2N}}
\rightarrow
1
```

so every finite-order $GF_N$ form factor approaches the same Gaussian wavepacket envelope.

The effective smeared force therefore reduces asymptotically to the Gaussian $GF_1$ structure.

The point-force reversal condition was:

```math
\eta_{\mathrm{effective}}
>
\frac23
```

but the localization bound gives:

```math
\eta_{\mathrm{effective}}
=
\frac{\eta}{A^2}
\le
\frac1{\chi^2}
```

Therefore a necessary condition for repulsion is:

```math
\frac1{\chi^2}
>
\frac23
```

or:

```math
\chi^2
<
\frac32
```

and hence:

```math
\chi
<
\sqrt{\frac32}
```

Numerically:

```text
CHI_CRITICAL=
1.224744871391589
```

This is the key 012G theorem inside the Gaussian model.

---

# 34. 012G numerical result

The global scan covered:

```text
N=
1,2,4,8,16,32,64

A=
0.5 to 1000

broad y grid
```

and found:

```text
CHI=1.00:
BEST_OUTWARD≈4.3196e-2

CHI=1.10:
BEST_OUTWARD≈9.9408e-3

CHI=1.20:
BEST_OUTWARD≈1.7906e-4

CHI=sqrt(3/2):
OUTWARD_GRID_POINTS=0

CHI=1.25:
OUTWARD_GRID_POINTS=0

CHI=1.50:
OUTWARD_GRID_POINTS=0

CHI=2:
OUTWARD_GRID_POINTS=0

CHI=3:
OUTWARD_GRID_POINTS=0

CHI=5:
OUTWARD_GRID_POINTS=0
```

The previous 012E control point became:

```text
012E_N16_SMEARED_TOTAL_SIGNED_FORCE=
-1.000000268027463
```

at:

```text
CHI=1.25
```

The previous 012F $N=64,\rho=5$ control became:

```text
012F_N64_RHO5_SMEARED_TOTAL_SIGNED_FORCE=
-0.848173329297821
```

Thus both headline delta-particle configurations reverted to attraction with only modest Gaussian localization.

The correct interpretation is:

```text
POINT_PARTICLE_012E_FORCE_REVERSAL=
PRESERVED_AS_MATHEMATICAL_RESULT

DELTA_PARTICLE_012F_PLANAR_REPULSION=
PRESERVED_AS_OPTIMISTIC_MODEL

CONTROLLED_GAUSSIAN_REPULSION_FOR_CHI>=1.25=
NOT_FOUND_IN_TESTED_DOMAIN

REPULSION_REQUIRES_MARGINAL_COMPTON_SCALE_LOCALIZATION=
YES_IN_TESTED_GAUSSIAN_MODEL
```

This is a severe realization constraint.

---

# 35. Current status of the ghost-free nonlocal branch

The nonlocal branch is now unusually well characterized.

## What survives

```text
GHOST_FREE_LINEARIZED_NONLOCAL_FRAMEWORK=
PUBLISHED_AT_TREE_LEVEL

CLASSICAL_POINT_MASS_GF_N_FORCE_OSCILLATIONS=
YES

CLASSICAL_POINT_MASS_FORCE_REVERSAL=
NO_IN_TESTED_GF_N_CLASS

PUBLISHED_O_G_HBAR2_FINITE_SEPARATION_TERM=
YES

TOTAL_DELTA_PARTICLE_FORCE_REVERSAL=
YES_PROJECT_DERIVED

TOTAL_DELTA_PARTICLE_PLANAR_REPULSION=
YES_IN_OPTIMISTIC_PAIRWISE_MODEL
```

## What has failed or been strongly demoted

```text
NAIVE_N2_HOMOGENEOUS_BULK_AMPLIFICATION=
REJECTED

CONTROLLED_DELTA_PARTICLE_MACROSCOPIC_MASS_SCALE=
CATASTROPHIC_AT_RHO5

RHO10_PLANAR_REPULSION_N<=64_X<=300=
NOT_FOUND

LOCALIZED_GAUSSIAN_PARTICLE_REPULSION_CHI>=1.25=
NOT_FOUND

ORDINARY_PROTON_OR_ELECTRON_DIRECT_PARTNER_REALIZATION=
SEVERELY_DISFAVORED
```

## What remains genuinely open

```text
FULL_RELATIVISTIC_COHERENT_FIELD_STATE=
NOT_TESTED

MANY_BODY_QFT_EXPECTATION_VALUE=
NOT_ESTABLISHED

LOOP_LEVEL_UNITARITY=
NOT_ESTABLISHED

NONLINEAR_IN_G_COMPLETION=
NOT_ESTABLISHED

ORDINARY_PAYLOAD_COUPLING=
NOT_ESTABLISHED

EXACT_SHORT_RANGE_EXPERIMENTAL_GF_N_REFIT=
NOT_DONE

MACROSCOPIC_CONTROLLED_SOURCE=
NOT_ESTABLISHED
```

---

# 36. Why the relativistic coherent-field gate is now the single highest-value task

The ultralight masses required by the point-particle repulsive regime make individual localized-particle language questionable.

For an ultralight bosonic system, the physically appropriate object may instead be:

```text
RELATIVISTIC_QUANTUM_FIELD_STATE

COHERENT_STATE

CLASSICAL_FIELD_LIMIT

CONDENSATE_OR_WAVE_BACKGROUND
```

rather than a collection of distinguishable localized particles.

This is not an arbitrary rescue mechanism.

It is the correct next validity test because 012G specifically showed the single-localized-particle interpretation becoming marginal at approximately one Compton wavelength.

The next scientific question is therefore:

> Does the published $O(G\hbar^2)$ repulsive term survive, cancel, or become parametrically negligible when the source and test systems are treated as controlled relativistic field/coherent states instead of localized one-particle wavepackets?

This question has maximum information gain because either answer is decisive.

---

# 37. The shortest possible path toward practical antigravity

The fastest rigorous path is not to explore more theories.

It is to attack the remaining bottlenecks in descending order of their ability to kill or promote the only current mechanism with a healthy-looking repulsive total force.

The shortest path is:

```text
012H
RELATIVISTIC_COHERENT_FIELD_EXPECTATION_VALUE
          |
          +---- REPULSIVE TERM DOES NOT SURVIVE
          |          |
          |          v
          |   CLOSE / STRONGLY DEMOTE
          |   GF_N NONLOCAL PRACTICAL BRANCH
          |          |
          |          v
          |   GLOBAL RERANK
          |
          +---- REPULSIVE TERM SURVIVES
                     |
                     v
012I
MACROSCOPIC COHERENT SOURCE SCALING
+ ORDINARY PAYLOAD COUPLING
                     |
                     +---- FAILS
                     |       |
                     |       v
                     |   CLOSE BRANCH
                     |
                     +---- SURVIVES
                              |
                              v
012J
EXACT SHORT-RANGE EXPERIMENT GEOMETRY REFIT
                              |
                              +---- EXCLUDED
                              |       |
                              |       v
                              |   CLOSE BRANCH
                              |
                              +---- ALLOWED
                                       |
                                       v
012K
NONLINEAR + LOOP + BACKREACTION + STABILITY
                                       |
                                       +---- FAILS
                                       |       |
                                       |       v
                                       |   CLOSE BRANCH
                                       |
                                       +---- SURVIVES
                                                |
                                                v
012L
FINITE DEVICE ARCHITECTURE
ENERGY / SOURCE DENSITY / CONTROL
                                                |
                                                v
012M
REAL EXPERIMENT DESIGN
```

Do not reorder this sequence unless a cheaper theorem appears.

---

# 38. Step 1 — 012H relativistic coherent-field expectation value

This should be the very first new research slice.

Do not begin with experimental apparatus modeling.

Do not begin by pushing $N$ from 64 to 128, 256, or 1024.

Do not begin with another Gaussian wavepacket.

Instead derive the field-theoretic object.

Candidate approach:

Start from the same linearized gravitational interaction that generated the published two-particle amplitude.

Replace external one-particle states by coherent states of a relativistic scalar field.

Compute:

```math
\langle\Psi|
T_{\mu\nu}(x)
|\Psi\rangle
```

and the relevant connected matrix elements entering single-graviton exchange.

Determine whether the term corresponding to the point-particle:

```math
O(G\hbar^2)
```

contact contribution scales as:

```text
N
N^2
N^0
1/N
```

or vanishes in the coherent/classical-field limit.

Specific questions:

```text
DOES_THE_HBAR2_CONTACT_TERM_SURVIVE_COHERENT_EXPECTATION?
```

```text
IS_IT_A_GENUINE_STATE_INDEPENDENT_FORCE_OR_A_SINGLE_PARTICLE_RECOIL_CONTACT_TERM?
```

```text
DOES_NORMAL_ORDERING_OR_CONNECTED_DISCONNECTED_DECOMPOSITION_CANCEL_IT?
```

```text
DOES_THE_TERM_SCALE_WITH_NUMBER_DENSITY_OR_ONLY_DENSITY_GRADIENT?
```

```text
DOES_THE_CLASSICAL_FIELD_LIMIT_HBAR_TO_ZERO_REMOVE_THE_ONLY_REPULSIVE_PIECE?
```

If the term vanishes in the controlled coherent limit:

```text
GF_N_PRACTICAL_BRANCH=
CLOSE_OR_STRONGLY_DEMOTE
```

immediately.

Do not rescue it with arbitrary new interactions.

---

# 39. Step 2 — macroscopic scaling and ordinary payload coupling

Only if 012H survives.

The mechanism is useless as practical antigravity unless an ordinary macroscopic payload can experience an outward acceleration.

012E already showed naïve proton/electron plus ultralight localized-particle pairing to be severely uncontrolled.

Therefore the next calculation must directly determine whether:

```text
ORDINARY_BARYONIC_MATTER
```

coupled gravitationally to a coherent ultralight field experiences:

```text
OUTWARD
```

rather than simply:

```text
ATTRACTIVE_OR_NEGLIGIBLE
```

force.

The relevant goal is not merely:

```text
ULTRALIGHT_FIELD_SELF_REPULSION
```

The goal is:

```text
ORDINARY_PAYLOAD_REPULSION
```

If the repulsive term exists only between specially ultralight quanta:

```text
PRACTICAL_PAYLOAD_PATH=
FAIL
```

unless a rigorous conversion mechanism is found without adding a new fifth force.

At the same time derive:

```math
a_{\mathrm{payload}}
\left(
\rho_\phi,
\ell,
N,
m_\phi,
R,
h
\right)
```

and determine whether the source requirement still scales like:

```math
\frac aG
```

or:

```math
\frac{ah^2}{G}
```

If it does, the mechanism has not solved practicality.

---

# 40. Step 3 — experimental geometry refit

Only perform this if 012H and 012I survive.

The historical nonlocal benchmark used:

```text
M_s=0.004 eV

ell≈49.33 micrometers
```

012F showed very large point-pair deviations over the historical short-range gravity window.

However point-particle deviations cannot be directly compared with finite torsion-balance constraints.

The correct calculation must convolve the actual experimental geometry with:

```math
P_N(r/\ell)
```

and the relevant quantum/contact kernel.

At minimum compare against modern short-range inverse-square-law experiments.

The 2020 Eöt-Wash experiment tested Newtonian gravity over approximately $52,\mu{\mathrm{m}}$ to $3,{\mathrm{mm}}$ and found consistency with Newtonian behavior in that regime; its published Yukawa limits cannot simply be substituted for the oscillatory $GF_N$ kernel.

Therefore perform a geometry-specific likelihood or conservative exclusion reconstruction rather than reading a Yukawa plot.

Stop immediately if the parameter region required for repulsion is excluded.

---

# 41. Step 4 — nonlinear, loop, stability and backreaction gate

Only if the mechanism remains empirically open.

Required checks:

```text
LOOP_LEVEL_UNITY_OR_GHOST_FREEDOM

NONLINEAR_IN_G_CORRECTIONS

BACKGROUND_STABILITY

FIELD_ENERGY_POSITIVITY

SOURCE_BACKREACTION

GRAVITATIONAL_COLLAPSE

COHERENT_STATE_DEPLETION

RADIATIVE_DECAY

VACUUM_INSTABILITY

COSMOLOGICAL_CONSISTENCY

GRAVITATIONAL_WAVE_CONSTRAINTS
```

Tree-level no-extra-pole structure is not enough to claim a complete healthy quantum gravitational theory.

The published 2025 calculation is explicitly a linearized single-graviton-exchange calculation.

---

# 42. Step 5 — finite source/device architecture

Only after theory and experiment survive.

Do not discuss a practical device before there exists:

```text
FINITE_SOURCE

FINITE_PAYLOAD

CONTROLLED_STATE

STABLE_OPERATION

ENERGY_ACCOUNTING

BACKREACTION

MOMENTUM_ACCOUNTING

MEASURABLE_OUTWARD_ACCELERATION
```

The first target does not need to be $1g$.

An experimentally decisive architecture producing:

```text
1e-12 g
1e-9 g
1e-6 g
```

with controlled systematics would be far more scientifically valuable than an unphysical $1g$ numerical model.

---

# 43. Stop rules for the current nonlocal branch

Close or strongly demote the branch immediately if any of the following becomes established:

```text
COHERENT_FIELD_EXPECTATION_REMOVES_REPULSIVE_TERM
```

```text
REPULSIVE_TERM_ONLY_EXISTS_FOR_UNCONTROLLED_LOCALIZED_PARTICLES
```

```text
ORDINARY_PAYLOAD_FORCE_REMAINS_ATTRACTIVE
```

```text
MACROSCOPIC_SOURCE_SCALING_RETURNS_TO_CATASTROPHIC_A_OVER_G_OR_AH2_OVER_G_WITH_NO_COMPENSATING_ADVANTAGE
```

```text
REQUIRED_HIGH_N_FORM_FACTOR_EXCLUDED_BY_SHORT_RANGE_GRAVITY_DATA
```

```text
LOOP_LEVEL_PATHOLOGY_OR_INSTABILITY_UNAVOIDABLE
```

```text
REQUIRED_SOURCE_STATE_HAS_NO_CONTROLLED_RELATIVISTIC_QFT_REALIZATION
```

Do not add additional species, arbitrary counterterms, material-specific couplings, or new forces simply to bypass one of these failures.

That would constitute a new branch and must be evaluated from zero.

---

# 44. Branches that should not be casually reopened

## Classical static GR coefficient optimization

Status:

```text
DEPRIORITIZED
```

Reason:

The sign issue is solved; the problem is catastrophic scaling.

Do not spend time reducing:

```text
C=23.59
```

to:

```text
C=20
```

unless a new physical theorem changes the scaling.

---

## Periodic dynamic GR

Status:

```text
STRONGLY_DEMOTED
```

Reason:

The DC component reduces to a static conserved averaged source and the oscillatory component has zero first-order mean.

---

## Ordinary gravitational-wave lift

Status:

```text
REJECTED_AS_PRACTICAL_SUSTAINED_ROUTE
```

Reason:

The effect is oscillatory tidal acceleration and the controlled $1g$, $1,{\mathrm{m}}$ flux scale is approximately:

```text
8.59e20 W/m^2
```

---

## Healthy linear universal scalar/spin-2 modified gravity

Status:

```text
REJECTED_AT_SIGN_LEVEL
```

Reason:

Positive residues add attraction.

---

## Standard healthy nonlinear universal scalar screening

Status:

```text
STRONGLY_DEMOTED_AT_SIGN_LEVEL
```

Reason:

Healthy positive kinetic response preserves the source/test sign.

---

## Minimal material-specific scalar fifth-force UV completions

Status:

```text
CLOSED_OR_STRONGLY_DEMOTED
```

Reason:

Z1-Z3 showed severe one-body leakage/background/naturalness problems.

---

## Simple vector fifth forces

Status:

```text
STRONGLY_DISFAVORED_IN_PREVIOUS_GATES
```

Do not reopen without a genuinely new symmetry mechanism.

---

## Casimir/free negative-energy route

Status:

```text
CONSTRAINED_REFERENCE_BRANCH
```

The complete apparatus and QEI scaling have not produced a practical macroscopic escape.

---

## Domain-wall/tension repulsion

Status:

```text
REAL_SIGN_EFFECT
ENERGETICALLY_CATASTROPHIC
```

Do not treat this as a newly unexplored route.

---

## Reissner-Nordström / electromagnetic exact repulsion

Status:

```text
EXACT_REFERENCE
PRACTICALLY_CATASTROPHIC
```

Required charges/fields are not a plausible device route.

---

# 45. Current overall scientific position

The project can now state the following with strong discipline.

## Established

```text
LOCAL_GRAVITATIONAL_REPULSION_IS_ALLOWED_BY_GR=
YES
```

```text
FINITE_POSITIVE_ENERGY_DEC_LINEARIZED_GR_SOURCE_WITH_OUTWARD_NEAR_FIELD=
ESTABLISHED
```

```text
STATIC_CLASSICAL_GR_PRACTICAL_SCALING=
CATASTROPHIC
```

```text
PERIODIC_DYNAMIC_LINEARIZED_GR_SCALING_ESCAPE=
NOT_FOUND
```

```text
HEALTHY_LINEAR_UNIVERSAL_SPIN0_SPIN2_REPULSION=
REJECTED
```

```text
STANDARD_HEALTHY_NONLINEAR_UNIVERSAL_SCALAR_SCREENING_SIGN_REVERSAL=
REJECTED_IN_TESTED_CLASS
```

```text
CANONICAL_GHOST_FREE_IDG_CLASSICAL_POINT_FORCE=
ATTRACTIVE
```

```text
HIGHER_ORDER_GF_N_CLASSICAL_FORCE=
OSCILLATORY_BUT_NO_TESTED_SIGN_REVERSAL
```

```text
GF_N_TOTAL_DELTA_PARTICLE_FORCE_WITH_PUBLISHED_O_G_HBAR2_TERM=
REPULSIVE_IN_PARAMETER_WINDOWS
```

```text
HOMOGENEOUS_BULK_N2_FORCE_AMPLIFICATION=
REJECTED_AT_LEADING_PAIRWISE_ORDER
```

```text
GAUSSIAN_LOCALIZED_PARTICLE_REPULSION_FOR_CHI>=1.25=
NOT_FOUND_IN_TESTED_GF_N_DOMAIN
```

---

# 46. Things that have NOT been established

```text
EXACT_NONLINEAR_GR_006D_SOLUTION=
NO
```

```text
DYNAMIC_STABILITY_OF_006D=
NO
```

```text
KNOWN_006D_MATERIAL=
NO
```

```text
KNOWN_REAL_GF_N_ANTIGRAVITY_MATERIAL=
NO
```

```text
FULL_RELATIVISTIC_COHERENT_FIELD_REPULSION=
NO
```

```text
MACROSCOPIC_CONTROLLED_NONLOCAL_SOURCE=
NO
```

```text
ORDINARY_PAYLOAD_REPULSION_IN_GF_N=
NO
```

```text
LOOP_LEVEL_NONLOCAL_GRAVITY_COMPLETION=
NO
```

```text
EMPIRICAL_VIABILITY_OF_REPULSIVE_GF_N_REGION=
NO
```

```text
EXPERIMENTAL_ACCESSIBILITY=
NO
```

```text
PRACTICAL_ANTIGRAVITY=
NO
```

```text
NEW_PHYSICS_DISCOVERY=
NO
```

---

# 47. Practical-antigravity progress calibration

The last calibrated estimate was approximately:

```text
CONCEPTUAL_MATHEMATICAL_MAP=
~70%

PHYSICALLY_VIABLE_MECHANISM_PROGRESS=
~15-20%

PRACTICAL_DEVICE_PROGRESS=
~5-7%
```

These numbers are subjective research-progress estimates, not physical probabilities.

Do not increase the practical-device percentage merely because another mathematical repulsive effect is found.

A major increase should require the mechanism to cross several of:

```text
CONTROLLED_RELATIVISTIC_REALIZATION

MACROSCOPIC_SCALING

ORDINARY_PAYLOAD_COUPLING

EMPIRICAL_SURVIVAL

STABILITY

FINITE_SOURCE

CONTROL
```

The current nonlocal result has not crossed those gates.

---

# 48. What would justify a large progress jump

A result deserving movement toward something like 25-50% practical progress would need to establish several of the following simultaneously:

```text
1. HEALTHY RELATIVISTIC FIELD THEORY
2. REAL REPULSIVE FORCE
3. MACROSCOPIC COHERENT AMPLIFICATION
4. ORDINARY NEUTRAL PAYLOAD RESPONSE
5. SOURCE REQUIREMENT MANY ORDERS BELOW A/G OR AH^2/G
6. EXISTING EXPERIMENTAL SURVIVAL
7. DYNAMIC STABILITY
8. FINITE CONTROLLABLE SOURCE
```

At present we have primarily:

```text
1. PARTIAL
2. YES_IN_IDEALIZED_MODEL
3. NO_OR_UNKNOWN
4. UNKNOWN
5. NO_IN_TESTED_PLANAR_CASE
6. UNKNOWN
7. UNKNOWN
8. NO
```

Therefore 50% is not currently scientifically justified.

---

# 49. Recommended exact next-session sequence

At the start of the next session:

```bash
git status --short

ROOT="$(pwd)"
PY="$ROOT/.venv/bin/python"

PYTHONPATH="$ROOT/src" \
"$PY" -m pytest -q tests/known_solutions
```

Expected:

```text
94 passed
```

Then:

## Step 1

Read:

```text
RESEARCH_BUILDPLAN.md
NOTES.md
README.md
FORMATTING_AND_CODE_STANDARDS.md
latest codebundle
this carry-forward document
```

## Step 2

State one active scientific question only:

> Does the $O(G\hbar^2)$ finite-separation repulsive term of the ghost-free nonlocal spinless-particle potential survive in a controlled relativistic coherent-field expectation value?

## Step 3

Build the cheapest analytical field-theory calculation capable of answering it.

Do not begin with a large simulation.

## Step 4

Attempt to falsify the effect analytically.

Inspect:

```text
NORMAL_ORDERING

CONNECTED_VS_DISCONNECTED_MATRIX_ELEMENTS

CLASSICAL_FIELD_LIMIT

HBAR_SCALING

COHERENT_STATE_NUMBER_SCALING

MOMENTUM_TRANSFER_SUPPORT

STRESS_ENERGY_EXPECTATION_VALUE

SOURCE_TEST_BACKREACTION
```

## Step 5

Only if a nonzero repulsive coherent term survives analytically, build a numerical reconstruction.

## Step 6

If it survives both:

```text
NEXT=
MACROSCOPIC_COHERENT_SOURCE_PLUS_ORDINARY_PAYLOAD_GATE
```

If not:

```text
NEXT=
CLOSE_NONLOCAL_PRACTICAL_BRANCH_AND_GLOBAL_RERANK
```

---

# 50. Permanent-code recommendation

The late gates have accumulated enough scientific importance that, before moving too far beyond 012H, the following should eventually receive permanent reproducible implementations and focused tests:

```text
012E_GF_N_TOTAL_TWO_PARTICLE_FORCE
012F_MANY_BODY_PLANAR_SCALING
012G_GAUSSIAN_WAVEPACKET_CONTROL
```

Minimum permanent regression targets:

```text
GF1_EXACT_FORCE_THRESHOLD_ETA=2/3

N16_012E_HIGH_PRECISION_CONTROL

F0_HOMOGENEOUS_BULK_FORCE=0

N64_RHO5_PLANAR_CONTROL

CHI_CRITICAL=sqrt(3/2)

NO_OUTWARD_GAUSSIAN_CASE_FOR_CHI>=1.25_IN_DECLARED_TEST_DOMAIN
```

Substantial new simulation files must follow `FORMATTING_AND_CODE_STANDARDS.md` with detailed top-of-file documentation.

---

# 51. Documentation updates required

The repository currently needs a frontier rollover.

The checked-in README/buildplan still emphasize 010E-Y and protected scalar UV matching as the leading speculative branch.

That is no longer the live frontier.

At the appropriate session-closeout point:

## NOTES.md

Append the chronological sequence:

```text
010E-Z1
010E-Z2
010E-Z3
011A
012A
012B
012C/V2
012D
012E
012F
012G
```

with exact claim classifications.

## RESEARCH_BUILDPLAN.md

Update:

```text
CURRENT_FRONTIER=
RELATIVISTIC_COHERENT_FIELD_EXPECTATION_VALUE_FOR_GF_N_O_G_HBAR2_TERM
```

and move protected scalar matching to:

```text
CLOSED_OR_STRONGLY_DEMOTED
```

## README.md

Do **not** replace the 006D established headline with 012E.

006D remains the strongest established project-derived result because it has a fully explicit finite positive-energy conserved stress source.

Instead add a clearly separated section:

```text
CURRENT_SPECULATIVE_MODIFIED_GRAVITY_FRONTIER
```

stating that a published ghost-free nonlocal two-particle potential has a project-derived total-force reversal window, but straightforward localized-particle/macroscopic realization has failed important gates.

## Journal

If 012E is judged durable enough after coherent-state analysis and literature comparison, create a dedicated dated journal entry preserving:

```text
published starting equation
project-derived force reversal theorem
independent numerical reconstruction
012F many-body result
012G localization obstruction
claim boundaries
```

Do not call it a discovery journal until novelty has been independently assessed.

---

# 52. Literature facts that must remain clearly distinguished

## Published

The 2025 paper by Vinckers, de la Cruz-Dombriz, and Mazumdar computes ghost-free infinite-derivative gravitational potentials from single-graviton exchange and shows the local contact correction becomes spatially smeared and nonzero at finite separation.

Published fact:

```text
SMEARED_FINITE_SEPARATION_O_G_HBAR2_TERM=
YES
```

Published context:

```text
LINEARIZED
SINGLE_GRAVITON_EXCHANGE
```

The paper does not by itself establish practical antigravity.

Earlier ghost-free infinite-derivative literature establishes that the Newtonian potential can become nonsingular at short distance while recovering $1/r$ gravity in the infrared.

## Project-derived

The following are our derivations/reconstructions:

```text
GF1_TOTAL_FORCE_REVERSAL_THRESHOLD_ETA=2/3

GENERAL_SMALL_X_GF_N_ETA_CRIT_GAMMA_RATIO

N16_RHO~19.48_POINT_PARTICLE_CONTROL

HOMOGENEOUS_BULK_CONTACT_FORCE=ZERO

PLANAR_SHEET_EXACT_FORCE_FORMULA

N64_RHO5_SIGMA_1G~3.315e10 KG/M2

GAUSSIAN_LOCALIZATION_BOUND_A2>=CHI2_ETA

ASYMPTOTIC_CHI_CRITICAL=sqrt(3/2)

NO_TESTED_OUTWARD_CASES_FOR_CHI>=1.25
```

These must be described as:

```text
PROJECT_DERIVED
```

until independently reproduced outside the project and compared exhaustively with the literature.

---

# 53. Critical unresolved theoretical questions

The next session must keep these visible.

## Nonlocal coherent-state questions

```text
Does the O(G hbar^2) term survive coherent states?
```

```text
What is its scaling with occupation number?
```

```text
Does it vanish in the classical-field limit?
```

```text
Is the two-particle repulsion fundamentally a recoil/contact effect?
```

```text
Does the term exist in connected stress-energy correlators for coherent matter?
```

```text
Can an ordinary massive test body couple repulsively to the coherent source?
```

## Theory-health questions

```text
Is loop-level unitarity preserved?
```

```text
What happens beyond linear order in G?
```

```text
Are high-N form factors radiatively stable?
```

```text
Do nonlinear backgrounds preserve the assumed form factor?
```

## Empirical questions

```text
What are the exact current bounds on the relevant high-N GF_N kernels?
```

```text
Does a geometry-specific torsion-balance convolution exclude the required ell,N region?
```

```text
Are there astrophysical/cosmological bounds stronger than laboratory constraints?
```

## Device questions

```text
How would the source state be generated?
```

```text
What energy density is required?
```

```text
How does the source react mechanically?
```

```text
Can the effect act on ordinary material?
```

```text
Can it be switched?
```

None of these are solved.

---

# 54. Highest-value falsification questions

If time is limited, ask these in this order:

```text
1.
DOES_THE_COHERENT_RELATIVISTIC_FIELD_REMOVE_THE_REPULSIVE_HBAR2_TERM?
```

If yes, close branch.

```text
2.
IF_NOT, DOES_ORDINARY_MATTER_FEEL_THE_REPULSIVE_SIGN?
```

If no, close practical branch.

```text
3.
IF_YES, DOES_MACROSCOPIC_SOURCE_SCALING_BEAT_A/G_BY_ORDERS_OF_MAGNITUDE?
```

If no, strongly demote.

```text
4.
IF_YES, IS_THE_PARAMETER_REGION_ALREADY_EXCLUDED?
```

If yes, close branch.

```text
5.
IF_NOT, DOES_THE_FULL_THEORY_REMAIN_STABLE_AND_UNITARY?
```

If no, close branch.

Only after all five survive is engineering a rational priority.

---

# 55. Things not to do next

```text
DO_NOT:
push N from 64 to enormous values before coherent-state validity is resolved.
```

```text
DO_NOT:
fit Eot-Wash geometry before checking whether the physical source state exists.
```

```text
DO_NOT:
invent a new material coupling to make ordinary matter respond.
```

```text
DO_NOT:
call 012E a practical antigravity discovery.
```

```text
DO_NOT:
discard 012E because 012G failed localized particles.
```

012E remains a valid point-particle model result.

```text
DO_NOT:
reopen the 010E scalar UV branch without a genuinely new exact symmetry.
```

```text
DO_NOT:
return to small classical-GR coefficient optimization.
```

```text
DO_NOT:
count model parameter coincidences as mechanisms.
```

```text
DO_NOT:
increase the practical progress estimate to satisfy a target percentage.
```

The physics must earn any promotion.

---

# 56. Current conservative claim ledger

```text
MATHEMATICAL_LOCAL_GR_REPULSION=
ESTABLISHED
```

```text
FINITE_POSITIVE_ENERGY_LINEARIZED_GR_REPULSIVE_SOURCE=
ESTABLISHED
```

```text
STATIC_GR_PRACTICALITY=
NO
```

```text
PERIODIC_DYNAMIC_GR_SCALING_ESCAPE=
NO_UNDER_STATED_ASSUMPTIONS
```

```text
HEALTHY_LINEAR_UNIVERSAL_SCALAR_SPIN2_REPULSION=
REJECTED
```

```text
STANDARD_HEALTHY_NONLINEAR_SCALAR_SCREENING_REPULSION=
REJECTED_IN_TESTED_CLASS
```

```text
CANONICAL_GHOST_FREE_IDG_CLASSICAL_REPULSION=
REJECTED
```

```text
HIGHER_ORDER_GF_N_CLASSICAL_TOTAL_FORCE_REVERSAL=
NOT_FOUND
```

```text
GF_N_PUBLISHED_O_G_HBAR2_REPULSIVE_CONTRIBUTION=
YES
```

```text
GF_N_PROJECT_DERIVED_TOTAL_DELTA_PARTICLE_FORCE_REVERSAL=
ESTABLISHED_IN_TESTED_LINEARIZED_MODEL
```

```text
GF_N_HOMOGENEOUS_BULK_ANTIGRAVITY=
NO_AT_LEADING_PAIRWISE_ORDER
```

```text
GF_N_OPTIMISTIC_PLANAR_DELTA_PARTICLE_REPULSION=
YES
```

```text
GF_N_CONTROLLED_MACROSCOPIC_AREAL_MASS_SCALE=
POOR_IN_TESTED_RHO5_CASE
```

```text
GF_N_GAUSSIAN_LOCALIZED_PARTICLE_REPULSION_CHI>=1.25=
NOT_FOUND
```

```text
RELATIVISTIC_COHERENT_FIELD_GF_N_REPULSION=
UNKNOWN
```

```text
KNOWN_REAL_ANTIGRAVITY_MATERIAL=
NO
```

```text
EMPIRICAL_ANTIGRAVITY_SIGNAL=
NO
```

```text
PRACTICAL_ANTIGRAVITY_DEVICE=
NO
```

```text
NEW_PHYSICS_DISCOVERY=
NO
```

---

# 57. Most important conceptual lesson from the entire project so far

The project began with the question:

> Is gravitational repulsion physically possible?

That question is no longer the frontier.

We have multiple mathematical and known-physics examples demonstrating that repulsive gravitational behavior is possible.

The real problem has successively become:

```text
SIGN
 ->
CONSISTENCY
 ->
FINITE_SOURCE
 ->
CONSERVATION
 ->
ENERGY_COST
 ->
MICROSCOPIC_REALIZATION
 ->
QUANTUM_CONTROL
 ->
MACROSCOPIC SCALING
 ->
EMPIRICAL VIABILITY
 ->
DEVICE
```

The strongest recurring lesson is:

> **Producing a repulsive sign is much easier than producing useful, controllable, stable, macroscopic repulsion at reasonable source cost.**

006D solves an important part of the sign/consistency/source problem but pays catastrophic energy.

010E-Y found a clever low-energy material-specific force architecture but failed the relativistic microscopic protection gate.

012E found a surprisingly real total-force reversal in a published ghost-free nonlocal two-particle model, but 012F and 012G show that the effect may lose its practical leverage once physical many-body and localization requirements are imposed.

The remaining coherent-field calculation is therefore not a minor technical detail.

It decides whether the most interesting current loophole is a physically meaningful field effect or primarily an artifact of applying point-particle scattering potentials to ultralight objects outside a controlled localized-particle regime.

---

# 58. Exact active question for the next session

Use this wording:

> **In the same linearized ghost-free infinite-derivative gravity framework underlying the published spinless-particle potential, what is the gravitational interaction energy and force between controlled relativistic coherent field states, and does the finite-separation $O(G\hbar^2)$ repulsive contribution survive with a macroscopic scaling capable of acting on ordinary neutral matter?**

Do not broaden the question until it is answered.

---

# 59. Decision gate for the next session

```text
IF:
COHERENT_FIELD_REPULSIVE_TERM=ABSENT_OR_PARAMETRICALLY_NEGLIGIBLE

THEN:
CLOSE_GF_N_PRACTICAL_BRANCH
GLOBAL_RERANK
```

```text
IF:
COHERENT_FIELD_REPULSIVE_TERM=SURVIVES

BUT:
ORDINARY_PAYLOAD_FORCE=ATTRACTIVE_OR_ZERO

THEN:
CLOSE_PRACTICAL_BRANCH
```

```text
IF:
COHERENT_FIELD_REPULSION=SURVIVES
AND
ORDINARY_PAYLOAD_REPULSION=SURVIVES

THEN:
RUN_MACROSCOPIC_SCALING_GATE
```

```text
IF:
MACROSCOPIC_SCALING_BEATS_EXISTING_A/G_OR_AH2/G_COST_BY_MANY_ORDERS

THEN:
RUN_EXPERIMENTAL_GEOMETRY_REFIT
```

Only after all of this:

```text
CONSIDER_DEVICE_ARCHITECTURE
```

---

# 60. Final carry-forward summary

The project currently has **two especially important constructive mathematical results**.

First:

> A finite, positive-energy, nonsingular, locally conserved, DEC/WEC/NEC-respecting stress-energy source in static linearized GR can produce a locally outward gravitational field while retaining positive far-field active mass.

This is 006D and remains the strongest established project result.

Second:

> The published ghost-free nonlocal $O(G\hbar^2)$ spinless-particle potential admits project-derived parameter regimes where the complete two-particle force becomes outward; for $GF_1$, the small-distance reversal threshold is exactly $\eta>2/3$.

This second result is theoretically interesting but substantially less mature physically.

Subsequent gates found:

```text
HOMOGENEOUS_BULK_AMPLIFICATION=
NO

CONTROLLED_RHO5_PLANAR_SOURCE_COST=
~3.31e10 KG/M2

GAUSSIAN_LOCALIZED_PARTICLE_REPULSION_FOR_CHI>=1.25=
NOT_FOUND
```

The shortest path is therefore **not** another broad theory search.

It is:

```text
RELATIVISTIC_COHERENT_FIELD_EXPECTATION VALUE
        ->
ORDINARY PAYLOAD COUPLING
        ->
MACROSCOPIC SCALING
        ->
EXPERIMENTAL REFIT
        ->
FULL THEORY HEALTH
        ->
FINITE DEVICE
```

with an immediate stop rule at every failure.

Current conservative bottom line:

```text
MATHEMATICAL_ANTIGRAVITY_LIKE_REPULSION=
YES

PHYSICALLY_REALIZABLE_USEFUL_ANTIGRAVITY=
NOT_ESTABLISHED

PRACTICAL_ANTIGRAVITY=
NOT_ESTABLISHED

NEXT=
RELATIVISTIC_COHERENT_FIELD_EXPECTATION_VALUE_GATE
```


### END NOTE - AUGUST 29 2026 - 02:15 CST


### BEGIN NOTE - AUGUST 29 2026 - 12:35 CST


# ANTIGRAVITY_RESEARCH — Comprehensive Carry-Forward Notes Through 014E

**Session date:** August 29, 2026
**Project:** `ANTIGRAVITY_RESEARCH`
**Regression baseline at close:** `94 passed`
**Working-tree state repeatedly observed during the session:** `M NOTES.MD`
**Primary new frontier:** non-static disformal modified gravity
**Strongest new positive result:** project-reproduced local total-force reversal in a controlled reduced disformal model
**Strongest new negative result:** the minimal constant-$B$ bridge from that model to ordinary Standard-Model matter fails by approximately $3.46\times10^{57}$ in coupling strength under the declared EFT comparison
**Practical antigravity device:** not established

---

# 0. Purpose of these notes

These notes are the authoritative carry-forward context for the next research session.

They preserve:

* the scientific state entering this session;
* the sequence from 013E through 014E;
* the new positive and negative results;
* analytical proofs developed during the session;
* numerical validation evidence;
* precise limitations on every claim;
* the updated ranking of candidate mechanisms;
* repository/permanent-code debt;
* branches that should not be casually reopened;
* the exact remaining theoretical problem;
* the highest-value continuation condition.

The next session should read these notes together with:

```text
ANTIGRAVITY_RESEARCH_CODEBUNDLE_20260829-021116.md
RESEARCH_BUILDPLAN.md
FORMATTING_AND_CODE_STANDARDS.md
NOTES.md
README.md
CLAIMS.md
```

The repository documentation was already behind the live frontier before this session, and the new 014-series work moves the frontier substantially farther.

The documentation must therefore be updated before another major research branch is opened.

---

# 1. Scientific discipline that must remain in force

The project must continue to distinguish:

1. mathematical possibility;
2. local force sign reversal;
3. operationally measurable local repulsion;
4. reversal of the total local acceleration;
5. global force on a complete body;
6. conservation and momentum accounting;
7. stability;
8. existence of a physical source;
9. coupling to ordinary matter;
10. consistency with experiment;
11. practical energy and material requirements;
12. an actual antigravity device.

These are not equivalent achievements.

In particular:

> A repulsive fifth-force component is not automatically total antigravity.

> A local total-force reversal is not automatically global lift of a complete body.

> A consistent mathematical model is not automatically realized by nature.

> A dark-sector coupling is not automatically a force on baryonic matter.

> A numerical solution is not a practical device.

No internally generated result should be described as a new scientific discovery without independent reproduction and literature comparison.

---

# 2. GitHub mathematics standard

All project Markdown must continue to use single-dollar inline mathematics.

Example:

```markdown
The coupling is $B(\phi)$.
```

Display mathematics must use fenced `math` blocks.

Example:

````markdown
```math
\mathbf F_{\rm tot}
=
\mathbf F_\Psi+\mathbf F_\phi
```
````

Do not use:

```text
\(...)
```

or:

```text
\[...\]
```

Do not put grammatical punctuation at the end of display equations.

---

# 3. Repository status at the end of the research slice

Every major gate in this session reconfirmed:

```text
94 passed
```

for:

```text
tests/known_solutions
```

The repeatedly observed working tree was:

```text
 M NOTES.MD
```

No new permanent 014-series implementation was added to the repository during these gates.

The important scripts currently exist only as disposable `/tmp` research calculations:

```text
/tmp/013e_spin_mass_ceiling.py
/tmp/013f_global_closure.py
/tmp/014a_symmetron_image_force.py
/tmp/014b_disformal_repulsion_prerequisite.py
/tmp/014c_decisive_disformal_force.py
/tmp/014d_disformal_total_reversal.py
/tmp/014e_baryonic_disformal_bridge.py
```

These should not be treated as durable repository artifacts.

The strongest 014C, 014D, and 014E results should eventually be promoted into permanent, heavily documented simulation/analysis files and focused regression tests.

---

# 4. Strongest inherited result before this session — 006D

The strongest established-physics constructive result remains 006D.

Within static linearized GR, the project constructed a source that is:

```text
FINITE_RADIUS=YES
FINITE_THICKNESS=YES
NONSINGULAR=YES
POSITIVE_ENERGY=YES
LOCAL_CONSERVATION_LINEARIZED_ORDER=YES
NEC=PASS
WEC=PASS
DEC=PASS
OUTWARD_LOCAL_FIELD=YES
POSITIVE_FAR_FIELD_ACTIVE_MASS=YES
```

The best finite-thickness coefficient remains:

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

The central constructive result therefore remains:

> Within static linearized GR, finite positive-energy locally conserved stress-energy satisfying NEC/WEC/DEC can produce a locally outward gravitational field.

This result does not establish:

```text
EXACT_NONLINEAR_GR_REALIZATION
DYNAMIC_STABILITY
KNOWN_MATERIAL_REALIZATION
ENERGETIC_PRACTICALITY
PRACTICAL_DEVICE
```

The catastrophic classical scale also remains.

At coefficient one:

```math
M
\gtrsim
\frac{ah^2}{G}
```

For $a=g$ and $h=1,{\mathrm{m}}$:

```text
M ≈ 1.4693e11 kg
```

The explicit 006D source gives approximately:

```text
3.466e12 kg
```

at the same nominal target.

This is why later research moved toward interactions whose effective coupling scale is not simply $G$.

---

# 5. State immediately before the new 014-series work

The project had already aggressively investigated:

* static GR stress architectures;
* complete-apparatus Casimir physics;
* quantum inequalities;
* ordinary scalar and vector Yukawa forces;
* screened scalar/vector models;
* material-specific scalar response;
* healthy scalar-tensor gravity;
* $f(R)$;
* spin-2 exchange;
* Einstein-aether-type ideas;
* scalarization;
* static disformal coupling;
* ghost-free infinite-derivative gravity;
* coherent relativistic fields;
* state-dependent conservative response;
* static spin-dependent fifth forces.

The recurring result was:

> Finding a repulsive sign is much easier than producing a realizable, controllable, macroscopic repulsive acceleration.

This session then moved from broad closure to a genuinely new nonlinear, time-dependent modified-gravity branch.

---

# 6. 013E — polarized spin-mass practical ceiling

## 6.1 Question

Could a standard static scalar-pseudoscalar monopole-dipole force acting between polarized electron spin and ordinary nucleon mass produce practical antigravity?

The point potential used was of the standard form:

```math
V_{SP}(r)
=
\frac{
\hbar^2 g_s^N g_p^e
}{
8\pi m_e
}
(\boldsymbol{\sigma}\cdot\hat{\mathbf{r}})
\left(
\frac{1}{\lambda r}
+
\frac{1}{r^2}
\right)
e^{-r/\lambda}
```

For an infinite source slab, exact integration reduced the force magnitude to:

```math
|F_{\mathrm{spin}}|
=
\frac{
|g_s^N g_p^e|
\hbar^2 n_N
}{
4m_e
}
e^{-z/\lambda}
\left(
1-e^{-d/\lambda}
\right)
```

The analytical slab result was independently validated with finite-cylinder numerical quadrature.

Observed relative error:

```text
1.36e-10
```

## 6.2 Optimistic practical ceiling

Using a lead source and an experimentally constrained coupling benchmark:

```text
PUBLISHED_GP_E_GS_N_BOUND=5.7e-32
```

gave:

```text
MAX_FORCE_PER_POLARIZED_ELECTRON_N=
1.1880703206294257e-39
```

An intentionally absurd upper limit of one perfectly aligned useful spin per atomic mass unit gave:

```text
EXTREME_SPINS_PER_KG=
6.0221407620811229e26

MAX_ACCELERATION_OVER_G=
7.2957908216172233e-14
```

The coupling required for $1g$ was:

```text
REQUIRED_GP_E_GS_N_FOR_1G=
7.8127239930057480e-19
```

giving:

```text
REQUIRED_TO_PUBLISHED_BOUND_RATIO=
1.3706533321062715e13
```

Thus even an extreme optimistic benchmark misses $1g$ by more than thirteen orders of magnitude.

Final result:

```text
STATIC_ELECTRON_SPIN_NUCLEON_MASS_1G_PRACTICALITY=
REJECTED_BY_MORE_THAN_13_ORDERS_IN_OPTIMISTIC_BENCHMARK

CLAIM_CLASSIFICATION=
PROJECT_DERIVED_POLARIZED_SPIN_MASS_EMPIRICAL_CEILING
```

This does not exclude all possible spin-dependent forces.

---

# 7. 013F — established-physics practical closure gate

013F combined the strongest previous results into one explicit-scope closure calculation.

## 7.1 Unpolarized stationary spin filter

For a completely unpolarized spin-$1/2$ ensemble:

```math
\rho
=
\frac{I}{2}
```

For two independent spins:

```math
\rho_{12}
=
\frac{I_4}{4}
```

Since every Pauli matrix is traceless:

```math
{\mathrm{Tr}}(\sigma_i)=0
```

we have:

```math
\langle\sigma_i\rangle
=
{\mathrm{Tr}}
\left(
\frac{I}{2}\sigma_i
\right)
=
0
```

For independent unpolarized particles:

```math
\langle
\sigma_{1i}\sigma_{2j}
\rangle
=
\langle\sigma_{1i}\rangle
\langle\sigma_{2j}\rangle
=
0
```

Thus ordinary static unpolarized matter removes the leading spin-sensitive operator classes.

Velocity-dependent terms also disappear when the relevant center-of-mass relative velocity is zero.

013F numerically checked representative operators and obtained exactly zero expectations within machine precision.

Result:

```text
STATIC_UNPOLARIZED_NONCENTRAL_EXPECTATIONS=ZERO
UNPOLARIZED_STATIONARY_SURVIVING_OPERATOR_CLASS=SPIN_INDEPENDENT_CENTRAL
```

This is not a theorem against polarized or correlated macroscopic matter.

## 7.2 Closure result

The gate assembled:

* classical GR energy floors;
* Casimir/QEI failure;
* unscreened scalar/vector ceilings;
* static spin-mass ceiling;
* observed cosmological constant;
* GF1 coherent-field attraction.

It found:

```text
VERIFIED_PRACTICAL_1G_ROUTE_COUNT=0
```

and concluded:

```text
CURRENT_PROJECT_ESTABLISHED_PHYSICS_PRACTICAL_SEARCH=
CLOSED_AT_PRESENT_EVIDENCE_LEVEL
```

with explicit caveat:

```text
UNKNOWN_NEW_PHYSICS_GENERAL_NO_GO=NO
```

Classification:

```text
PROJECT_DERIVED_ESTABLISHED_PHYSICS_CLOSURE_WITH_EXPLICIT_SCOPE
```

This was a closure of the tested search space, not a theorem that all future physics forbids antigravity.

---

# 8. Decision to continue beyond 013F

The research was intentionally reopened only for candidate mechanisms that genuinely violated a closure assumption for a principled reason.

The first candidate was nonlinear symmetron image-force physics.

The second, and much more productive, candidate was explicitly time-dependent nonsymmetric disformal gravity.

This distinction matters:

> The project did not simply continue inventing arbitrary Lagrangians after 013F.

It searched for published nonlinear mechanisms that lay outside the closure assumptions.

---

# 9. 014A — full nonlinear symmetron image-force gate

## 9.1 Motivation

A published symmetron image-force approximation suggested that a small body near a strongly screened large body could experience a repulsive image contribution.

The key unresolved question was whether this survived solving the full nonlinear scalar field with the small body's backreaction included.

The dimensionless field equation tested was:

```math
\frac{\partial^2\varphi}{\partial r^2}
+
\frac{1}{r}
\frac{\partial\varphi}{\partial r}
+
\frac{\partial^2\varphi}{\partial z^2}
=
(\hat\rho-1)\varphi
+
\varphi^3
```

The exact screened-plane background is:

```math
\varphi_{\mathrm{bg}}(z)
=
\tanh
\left(
\frac{z}{\sqrt{2}}
\right)
```

The code symbolically verified that this solves:

```math
\varphi''
=
-\varphi+\varphi^3
```

under the stated half-space convention.

## 9.2 Important cylindrical-axis discretization correction

At $r=0$, the cylindrical radial Laplacian is not simply the Cartesian second derivative.

For a smooth axisymmetric field:

```math
\varphi(r)
=
\varphi_0
+
A r^2
+
O(r^4)
```

Therefore:

```math
\frac{\partial\varphi}{\partial r}
=
2Ar+O(r^3)
```

and:

```math
\frac{1}{r}
\frac{\partial\varphi}{\partial r}
=
2A+O(r^2)
```

while:

```math
\frac{\partial^2\varphi}{\partial r^2}
=
2A+O(r^2)
```

so:

```math
\left[
\frac{\partial^2\varphi}{\partial r^2}
+
\frac{1}{r}
\frac{\partial\varphi}{\partial r}
\right]_{r=0}
=
4A
```

With:

```math
\varphi_1-\varphi_0
=
A\Delta r^2+O(\Delta r^4)
```

the second-order finite-difference axis stencil becomes:

```math
\left[
\nabla_r^2\varphi
\right]_{r=0}
=
4
\frac{
\varphi_1-\varphi_0
}{
\Delta r^2
}
+
O(\Delta r^2)
```

This correction was incorporated before trusting the 014A result.

## 9.3 Force extraction

Two independent force estimators were used.

Volume/matter-force form:

```math
F_z
=
-\int
\hat\rho\,
\varphi
\frac{\partial\varphi}{\partial z}
\,dV
```

Translation/Hellmann-Feynman form:

```math
F_z
=
-\frac12
\int
\frac{\partial\hat\rho}{\partial z_c}
\varphi^2
\,dV
```

Agreement between these independent estimators was required.

## 9.4 Result

Twenty tested configurations for which the approximate image formula predicted repulsion instead produced attraction in the full nonlinear calculation.

Observed:

```text
IMAGE_APPROX_PREDICTED_REPULSIVE_CASES=20
FULL_NONLINEAR_REPULSIVE_CASES=0
IMAGE_REPULSIVE_BUT_FULL_ATTRACTIVE_CASES=20
```

Force estimators agreed extremely well:

```text
MAX_FORCE_ESTIMATOR_REL_DISAGREEMENT=
1.2910282915070713e-04
```

Maximum nonlinear PDE residual:

```text
2.7863523488491637e-08
```

Grid refinement:

```text
61x121 -> attractive
81x161 -> attractive
101x201 -> attractive
121x241 -> attractive
```

High-grid force relative change:

```text
2.6123e-03
```

Boundary-smoothing variation also retained the attractive sign.

Final:

```text
FULL_NONLINEAR_REPULSIVE_FORCE=
NOT_FOUND_IN_TESTED_PLANAR_ASYMMETRIC_DOMAIN

ELECTROSTATIC_IMAGE_REPULSION_SURVIVES_FULL_NONLINEAR_GATE=
NO_IN_TESTED_DOMAIN

CLAIM_CLASSIFICATION=
PROJECT_DERIVED_FULL_NONLINEAR_SYMMETRON_IMAGE_FORCE_NEGATIVE_PREFLIGHT
```

This strongly demoted the symmetron image branch.

---

# 10. Analytical finite-curvature rerank after 014A

Define:

```math
L
=
\frac{R_{\mathrm{large}}}{a}
```

and:

```math
d
=
1+\frac{\text{gap}}{a}
```

The approximate image-force ratio can be written:

```math
R_{\mathrm{image}}
=
\frac{\alpha}{3}
\frac{(L+d)^3}
{
d^2(2L+d)^2
}
```

Differentiate with respect to $L$:

```math
\frac{\partial R_{\mathrm{image}}}{\partial L}
=
\frac{\alpha}{3d^2}
\frac{
\partial
}{
\partial L
}
\left[
\frac{(L+d)^3}{(2L+d)^2}
\right]
```

Using logarithmic differentiation:

```math
\frac{1}{R_{\mathrm{image}}}
\frac{\partial R_{\mathrm{image}}}{\partial L}
=
\frac{3}{L+d}
-
\frac{4}{2L+d}
```

Combining:

```math
\frac{3}{L+d}
-
\frac{4}{2L+d}
=
\frac{
3(2L+d)-4(L+d)
}{
(L+d)(2L+d)
}
```

so:

```math
=
\frac{
2L-d
}{
(L+d)(2L+d)
}
```

Therefore:

```math
\frac{\partial R_{\mathrm{image}}}{\partial L}
=
\frac{
\alpha(2L-d)(L+d)^2
}{
3d^2(2L+d)^3
}
```

For:

```math
L>\frac{d}{2}
```

we have:

```math
\frac{\partial R_{\mathrm{image}}}{\partial L}>0
```

Thus within the approximation itself, increasing the large-body radius makes the relative image effect more favorable.

Since 014A tested the large-radius local-planar limit and found attraction, finite curvature was demoted in priority.

This is not a proof that every finite-curvature nonlinear symmetron configuration is attractive.

---

# 11. 014B — non-static disformal repulsion prerequisite gate

## 11.1 Why this branch was genuinely new

Earlier project work had shown:

```text
PURE_DISFORMAL_STATIC_FIFTH_FORCE=
NO_AT_LEADING_ORDER
```

but explicitly had not excluded:

```text
TIME_DEPENDENT_DISFORMAL_BACKGROUND
```

The new branch therefore targeted a truly different regime:

```text
NONSTATIC
+
PERTURBED
+
NONSYMMETRIC
+
NONLINEAR
```

rather than restarting the rejected static calculation.

## 11.2 Force-divergence structure

The published weak-field structure motivating the gate had the form:

```math
\nabla\cdot\mathbf{F}_\phi
=
(1-\delta_d)\eta^2
\nabla\cdot\mathbf{F}_\Psi
```

with:

```math
\eta^2
\propto
\frac{\xi^2}{g_\phi}
```

For a healthy/invertible branch:

```math
g_\phi>0
```

and therefore:

```math
\eta^2\ge0
```

If $\eta^2>0$, the divergence changes sign relative to Newtonian gravity precisely when:

```math
1-\delta_d<0
```

or:

```math
\delta_d>1
```

At homogeneous background order:

```math
\delta_d=0
```

so the background force itself remains gravity-like.

Therefore actual reversal requires spatial/nonlinear corrections.

## 11.3 Background dynamics

For the tested $\beta=0$ background, the dimensionless equation was:

```math
\ddot\chi
=
-\frac{2t}{t^2+D}\dot\chi
+
\frac{t^2}{t^2+D}
e^{-\chi}
```

For $\beta=0$, the relevant background coefficient satisfies:

```math
\xi_0
\propto
\ddot\chi
```

so roots of:

```math
\ddot\chi=0
```

identify the high-sensitivity windows associated with the published repulsive behavior.

## 11.4 Numerical reproduction

The early-time analytical solution was independently reproduced with maximum relative error:

```text
1.4488209440023864e-04
```

All four tested background families developed a $\xi_0$ crossing:

```text
FIDUCIAL:  t ≈ 3.50612
VF:        t ≈ 3.50612
STEEP:     t ≈ 5.34931
FF_BASE:   t ≈ 18.87736
```

Critically, every crossing occurred while:

```math
g_\phi>0
```

with minimum tested:

```text
MIN_G_PHI_ACROSS_TESTED_BACKGROUNDS=
0.675686...
```

Result:

```text
ALL_TESTED_BETA0_MODELS_HAVE_XI0_SIGN_CHANGE=YES

ALL_TESTED_XI0_SIGN_CHANGES_OCCUR_WITH_G_PHI_POSITIVE=YES
```

Near the roots:

```text
1/xi_proxy^2 ~ 1e5 to several e6
```

showing a large nonlinear-sensitivity window.

Important limitation:

```text
XI_ZERO_ALONE_PROVES_REPULSION=NO
```

014B established the prerequisite only.

Classification:

```text
PROJECT_DERIVED_REPRODUCTION_OF_PUBLISHED_DISFORMAL_REPULSION_PREREQUISITE
```

---

# 12. 014C — project reproduction of antiparallel disformal fifth force

014C was the first genuinely positive result of the new branch.

## 12.1 Force definitions

The reduced model used:

```math
\mathbf{F}_\Psi
=
-\frac{\nabla\Psi}{a^2}
```

and:

```math
\mathbf{F}_\phi
=
-\frac12
\frac{\xi}{g_\phi}
\nabla\phi
```

For the constant-$B$, $\beta=0$ branch:

```math
\xi
=
2B\ddot\phi
```

with:

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

The field equation was evolved without a quasistatic approximation.

---

# 13. New analytic result from 014C — weak-perturbation order theorem

This is one of the most important analytical results from the session.

Consider a smooth perturbation expansion around a homogeneous $\xi_0=0$ background.

Write:

```math
\phi
=
\phi_0
+
\epsilon\phi_1
+
O(\epsilon^2)
```

and:

```math
\Psi
=
\epsilon\Psi_1
+
O(\epsilon^2)
```

At the background root:

```math
\xi_0=0
```

so regular perturbation theory gives:

```math
\xi
=
\epsilon\xi_1
+
O(\epsilon^2)
```

Also:

```math
g_\phi
=
g_0
+
O(\epsilon)
```

with:

```math
g_0>0
```

Because the homogeneous part $\phi_0$ has no spatial gradient:

```math
\nabla\phi
=
\epsilon\nabla\phi_1
+
O(\epsilon^2)
```

Substitute into the fifth-force expression:

```math
\mathbf{F}_\phi
=
-\frac12
\frac{
\epsilon\xi_1+O(\epsilon^2)
}{
g_0+O(\epsilon)
}
\left[
\epsilon\nabla\phi_1
+
O(\epsilon^2)
\right]
```

Expanding the denominator:

```math
\frac{1}{g_0+O(\epsilon)}
=
\frac{1}{g_0}
+
O(\epsilon)
```

therefore:

```math
\mathbf{F}_\phi
=
-\frac{
\epsilon^2
}{
2g_0
}
\xi_1\nabla\phi_1
+
O(\epsilon^3)
```

Hence:

```math
\mathbf{F}_\phi
=
O(\epsilon^2)
```

Newtonian gravity is:

```math
\mathbf{F}_\Psi
=
-\frac{\nabla\Psi}{a^2}
```

and since:

```math
\Psi
=
\epsilon\Psi_1
+
O(\epsilon^2)
```

we obtain:

```math
\mathbf{F}_\Psi
=
O(\epsilon)
```

Therefore:

```math
\frac{
|\mathbf{F}_\phi|
}{
|\mathbf{F}_\Psi|
}
=
O(\epsilon)
```

and consequently:

```math
\lim_{\epsilon\to0}
\frac{
|\mathbf{F}_\phi|
}{
|\mathbf{F}_\Psi|
}
=
0
```

within a regular weak-field expansion about the $\xi_0=0$ background.

This is not a no-go theorem against nonperturbative disformal enhancement.

It is a theorem about the regular perturbative limit of this mechanism.

---

# 14. Numerical confirmation of the 014C scaling theorem

The numerical amplitude scan measured:

```text
ASYMPTOTIC_F_PHI_POWER=
1.9911392202550136

ASYMPTOTIC_F_PSI_POWER=
1.0000000000000002

ASYMPTOTIC_FORCE_RATIO_POWER=
0.9911392202550122
```

Thus:

```math
F_\phi
\propto
\epsilon^{1.991}
```

and:

```math
F_\Psi
\propto
\epsilon^{1.000}
```

while:

```math
\frac{F_\phi}{F_\Psi}
\propto
\epsilon^{0.991}
```

This is excellent numerical confirmation of the analytical prediction:

```math
2,\quad1,\quad1
```

for the corresponding exponents.

---

# 15. 014C antiparallel force result

At the $\xi_0$ root, 2D refinement found approximately:

```text
REPULSIVE_FRACTION ≈ 0.49
STRONGLY_ANTIPARALLEL_FRACTION ≈ 0.378
MIN_COS ≈ -1
```

The sign survived:

```text
48x48
72x72
96x96
128x128
```

with high-grid RMS-ratio change:

```text
0.00645
```

Independent 3D calculations found approximately:

```text
REPULSIVE_FRACTION ≈ 0.57
STRONGLY_ANTIPARALLEL_FRACTION ≈ 0.57
MIN_COS ≈ -1
```

across:

```text
24^3
32^3
40^3
```

with high-grid RMS-ratio change:

```text
0.0213
```

The minimum $g_\phi$ remained:

```text
0.66736
```

and therefore safely positive.

Result:

```text
HEALTHY_GPHI_ANTIPARALLEL_FIFTH_FORCE=YES
```

However:

```text
MAX_REPULSIVE_F5_OVER_FN_ANY_TESTED_MEANINGFUL_POINT=
0.0307172

TOTAL_FORCE_REVERSAL_FOUND=NO
```

So 014C established an actual force component opposite gravity, not yet reversal of the total acceleration.

Final classification:

```text
PROJECT_DERIVED_REDUCED_NONSTATIC_DISFORMAL_FORCE_REPRODUCTION_AND_SCALING_GATE
```

---

# 16. 014D — local total-force reversal

014D was the strongest positive result of this session.

## 16.1 Stronger operational criterion

Define:

```math
\mathbf{F}_{\mathrm{tot}}
=
\mathbf{F}_\Psi
+
\mathbf{F}_\phi
```

A merely antiparallel fifth force requires:

```math
\mathbf{F}_\phi
\cdot
\mathbf{F}_\Psi
<
0
```

Actual reversal of the total local acceleration projection requires:

```math
\mathbf{F}_{\mathrm{tot}}
\cdot
\mathbf{F}_\Psi
<
0
```

Substituting:

```math
\left(
\mathbf{F}_\Psi
+
\mathbf{F}_\phi
\right)
\cdot
\mathbf{F}_\Psi
<
0
```

gives:

```math
|\mathbf{F}_\Psi|^2
+
\mathbf{F}_\phi
\cdot
\mathbf{F}_\Psi
<
0
```

or:

```math
-\mathbf{F}_\phi
\cdot
\mathbf{F}_\Psi
>
|\mathbf{F}_\Psi|^2
```

Thus the anti-gravity component along the Newtonian direction must exceed the Newtonian field itself.

For perfectly antiparallel forces this reduces to:

```math
|\mathbf{F}_\phi|
>
|\mathbf{F}_\Psi|
```

014D computed the full vector projection directly rather than inferring reversal solely from magnitudes.

---

# 17. Coupling scan in 014D

The dimensionless disformal parameter was scanned through:

```text
b0 =
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

No local total reversal occurred through:

```text
b0=0.22
```

The first coarse reversal occurred at:

```text
b0=0.24
```

with:

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

Thus reversal appeared while $g_\phi$ was still comfortably above zero.

At:

```text
b0=0.28
```

the coarse result became much stronger:

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

---

# 18. 014D 2D convergence

The fully validated candidate was:

```text
b0=0.28
```

Refinements:

```text
64x64
96x96
128x128
```

all showed total reversal.

Highest-resolution root result:

```text
ROOT_TOTAL_REVERSAL_FRAC=
0.253981

ROOT_MAX_F5_OVER_FN=
3.79043

ROOT_MAX_OUTWARD_TOTAL_PROJ=
2.51518

ROOT_MIN_TOTAL_COS≈-1

ROOT_MIN_GPHI=
0.139705
```

The high-grid outward-projection relative change was:

```text
0.0031517
```

or approximately $0.315\%$.

Result:

```text
2D_LOCAL_TOTAL_FORCE_REVERSAL_REFINEMENT_STABLE=YES
```

---

# 19. 014D independent 3D validation

Independent three-dimensional refinements were:

```text
24^3
32^3
40^3
```

All showed local total reversal.

At $40^3$:

```text
ROOT_TOTAL_REVERSAL_FRAC=
0.00981109

ROOT_MAX_F5_OVER_FN=
1.59193

ROOT_MAX_OUTWARD_TOTAL_PROJ=
0.579614

ROOT_MIN_TOTAL_COS=
-0.999434

ROOT_MIN_GPHI=
0.147219
```

Although the reversing spatial fraction was smaller in 3D than in 2D, the sign survived all resolutions.

High-grid 3D outward-projection relative change:

```text
0.0466575
```

or approximately $4.67\%$.

Result:

```text
3D_LOCAL_TOTAL_FORCE_REVERSAL_REFINEMENT_STABLE=YES
```

---

# 20. 014D timestep-halving control

The $96^2$ calculation was rerun with the timestep halved.

Standard timestep:

```text
ROOT_MAX_OUTWARD_TOTAL_PROJ=
2.5072529385302480
```

Half timestep:

```text
ROOT_MAX_OUTWARD_TOTAL_PROJ=
2.5075111943614803
```

Relative change:

```text
1.0299289263913065e-04
```

or approximately:

```text
0.0103%
```

The total-reversal fraction was unchanged at the printed precision.

Result:

```text
TIMESTEP_HALVING_REVERSAL_SIGN_STABLE=YES
```

This is strong evidence that the reversal is not an explicit integration-step artifact.

---

# 21. 014D nondegeneracy / health checks

Across the validated calculations:

```text
MIN_GPHI_VALIDATED_RUNS=
0.13850683595823443

GPHI_ACCEPTANCE_FLOOR=
0.1
```

Thus:

```text
REVERSAL_REQUIRES_GPHI_BELOW_0P1=NO
```

The minimum kinetic denominator was:

```text
1.076254466508298
```

and therefore remained positive.

Maximum tested Newtonian potential:

```text
MAX_ABS_PSI_VALIDATED_RUNS=
0.02249234255491472
```

so the deliberately weak-field metric condition used by the reduced calculation remained within the declared test threshold.

Final result:

```text
PROJECT_REPRODUCED_LOCAL_TOTAL_FORCE_REVERSAL=
YES_IN_CONTROLLED_REDUCED_DISFORMAL_MODEL

NONSYMMETRIC_2D_TOTAL_FORCE_REVERSAL=YES
NONSYMMETRIC_3D_TOTAL_FORCE_REVERSAL=YES
TOTAL_FORCE_REVERSAL_SURVIVES_GRID_REFINEMENT=YES
TOTAL_FORCE_REVERSAL_SURVIVES_TIMESTEP_HALVING=YES
DISFORMAL_METRIC_MARGIN_GPHI_GT_0P1=YES
LOCAL_TOTAL_ACCELERATION_PROJECTION_OPPOSITE_NEWTONIAN_GRAVITY=YES
```

Classification:

```text
PROJECT_DERIVED_REDUCED_DISFORMAL_LOCAL_TOTAL_FORCE_REVERSAL
```

---

# 22. Exactly what 014D establishes

The supported statement is:

> In the controlled reduced, non-static, nonsymmetric disformal model tested by the project, there exist local regions in which the total acceleration vector has a component opposite the direction produced by Newtonian gravity alone, and this sign reversal survives 2D and 3D grid refinement and timestep halving while remaining on a positive-$g_\phi$ nondegenerate branch.

This is materially stronger than the 014C statement.

The project has crossed the following conceptual ladder:

```text
REPULSIVE_FIFTH_FORCE_COMPONENT=
YES

FIFTH_FORCE_STRONGER_THAN_NEWTONIAN_LOCALLY=
YES_IN_014D_REGIONS

LOCAL_TOTAL_FORCE_PROJECTION_REVERSAL=
YES
```

This is a genuine project-derived numerical result.

---

# 23. What 014D does NOT establish

014D does not establish:

```text
GLOBAL_BODY_REPULSION
GLOBAL_CENTER_OF_MASS_LIFT
REACTIONLESS_PROPULSION
ORDINARY_BARYONIC_COUPLING
EXPERIMENTAL_REALIZATION
STABLE_MATERIAL_REALIZATION
MACROSCOPIC_DEVICE
PRACTICAL_ANTIGRAVITY
```

The density field was imposed rather than generated by a complete self-consistent matter/N-body evolution.

The model is a controlled reduced calculation, not a complete laboratory apparatus.

The reference matter coupling is to the dark sector rather than ordinary Standard-Model baryons.

The numerical result therefore must not be promoted to:

> "We built ordinary-matter antigravity."

It should instead be described as:

> **Local total-force reversal in a controlled non-static disformal modified-gravity model.**

---

# 24. Numerical evidence versus mathematical proof for 014D

The 014D force reversal is not presently an analytic theorem.

It is a numerical proposition supported by:

* direct evaluation of the total vector force criterion;
* a coupling scan locating the onset;
* 2D resolution refinement;
* independent 3D calculations;
* timestep halving;
* positive $g_\phi$ margin;
* positive kinetic denominator;
* weak-potential check.

Therefore documentation should use phrases such as:

```text
PROJECT-DERIVED NUMERICAL RESULT
NUMERICALLY REPRODUCED
NUMERICALLY CONVERGED WITHIN TESTED DOMAIN
```

rather than:

```text
MATHEMATICALLY PROVED FOR ALL DISFORMAL CONFIGURATIONS
```

No universal disformal-gravity theorem has been established.

---

# 25. 014E — baryonic bridge feasibility gate

Once 014D solved the local sign-and-magnitude problem inside the reduced model, the next question became physical realization.

Specifically:

> Can the coupling that produces the 014D reversal act on ordinary Standard-Model matter without violating constraints or requiring catastrophic energy?

This was the correct next gate.

---

# 26. Important notation correction from 014E

The parameter numerically called `B0` inside the reduced 014C/014D natural-unit code corresponds to the published **dimensionless** parameter $b_0$, not directly to the dimensionful coefficient $B_0$.

The relation is:

```math
b_0
=
H_0^2 M_{\mathrm{Pl}}^2 B_0
```

For the minimal constant disformal operator:

```math
B_0
=
\frac{1}{M_D^4}
```

so:

```math
b_0
=
\frac{
H_0^2 M_{\mathrm{Pl}}^2
}{
M_D^4
}
```

This mapping was symbolically checked in 014E.

---

# 27. Mathematical proof of the 014E physical scale map

Start from:

```math
b_0
=
\frac{
H_0^2 M_{\mathrm{Pl}}^2
}{
M_D^4
}
```

Multiply both sides by $M_D^4$:

```math
b_0M_D^4
=
H_0^2M_{\mathrm{Pl}}^2
```

Then:

```math
M_D^4
=
\frac{
H_0^2M_{\mathrm{Pl}}^2
}{
b_0
}
```

Taking the positive fourth root:

```math
M_D
=
\left(
H_0^2M_{\mathrm{Pl}}^2
\right)^{1/4}
b_0^{-1/4}
```

Since:

```math
\left(
H_0^2M_{\mathrm{Pl}}^2
\right)^{1/4}
=
\sqrt{
H_0M_{\mathrm{Pl}}
}
```

we obtain:

```math
M_D
=
\sqrt{
H_0M_{\mathrm{Pl}}
}
\,b_0^{-1/4}
```

This is exact under the declared constant-$B$ normalization.

014E checked the symbolic round-trip residual and obtained zero.

---

# 28. 014E physical disformal scales

Using:

```text
H0 = 67.74 km/s/Mpc
```

the calculation obtained:

```text
H0_EV=
1.4449752698678296e-33 eV

H0_TIMES_MPL_EV2=
3.5185147821281649e-06 eV^2

SQRT_H0_MPL_EV=
1.8757704502758766e-03 eV
```

The first 014D reversal:

```text
b0=0.24
```

maps to:

```text
M_D=
2.6799511607263058e-03 eV
```

or:

```text
2.679951 meV
```

The validated $b_0=0.28$ candidate maps to:

```text
M_D=
2.5786368350373110e-03 eV
```

or approximately:

```text
2.579 meV
```

---

# 29. Minimal Standard-Model constant-$B$ bridge

The primary external constraint used in 014E was the directly corresponding constant-disformal collider EFT benchmark:

```text
M_D >= 650 GeV
```

The comparison was intentionally made only within that declared constant universal operator scope.

The collider-safe maximum dimensionless coupling was:

```text
COLLIDER_ALLOWED_CONSTANT_B_b0_MAX=
6.9353012973239908e-59
```

The first local reversal requires:

```text
b0=0.24
```

Thus:

```math
\frac{
b_{0,\mathrm{reversal}}
}{
b_{0,\mathrm{collider}}
}
=
\frac{
0.24
}{
6.9353012973239908\times10^{-59}
}
```

giving:

```math
\frac{
b_{0,\mathrm{reversal}}
}{
b_{0,\mathrm{collider}}
}
=
3.4605562139399018\times10^{57}
```

Therefore the minimal constant-$B$ Standard-Model bridge misses the required coupling by approximately:

```text
57.54 orders of magnitude
```

in $B$.

---

# 30. Equivalent disformal-energy-scale gap

Because:

```math
B
\propto
M_D^{-4}
```

the corresponding energy-scale mismatch is the fourth root.

Numerically:

```text
COLLIDER_MD_OVER_FIRST_REVERSAL_MD=
2.4254173341869428e14
```

Thus the required 014D operating scale is approximately:

```math
2.43\times10^{14}
```

times lower in $M_D$ than the direct constant-coupling collider benchmark.

That is:

```text
14.3848 orders of magnitude
```

in the suppression scale.

---

# 31. 014E result for ordinary symmetron conformal screening

The gate distinguished conformal symmetron screening from the minimal constant derivative disformal interaction.

The carried-forward structural result is:

```text
CONVENTIONAL_SYMMETRON_CONFORMAL_COUPLING=
VEV_DEPENDENT

DENSE_PHASE_SYMMETRON_CONFORMAL_SCREENING=
YES

MINIMAL_CONSTANT_DISFORMAL_OPERATOR=
NO_ADDITIONAL_VEV_SUPPRESSION
```

Therefore:

```text
CONFORMAL_SYMMETRON_SCREENING_ALONE_HIDES_CONSTANT_DISFORMAL_OPERATOR=
NO
```

This does not rule out every possible disformal screening mechanism.

It only prevents us from claiming that ordinary conformal symmetron screening automatically solves the constant-$B$ baryonic-coupling problem.

---

# 32. Canonical kinetic-compensation idea

Suppose one tries to respect the collider-safe small $B$ but compensates by increasing $\dot\phi$ so that the same disformal deformation is retained.

For a homogeneous field:

```math
g_\phi
=
1-B\dot\phi^2
```

Define:

```math
q
=
B\dot\phi^2
=
1-g_\phi
```

At the first 014D reversal:

```text
g_phi≈0.2573528613
```

therefore:

```text
q≈0.7426471387
```

If:

```math
B
=
\frac{1}{M_D^4}
```

then:

```math
q
=
\frac{\dot\phi^2}{M_D^4}
```

and therefore:

```math
\dot\phi^2
=
qM_D^4
```

For a canonical scalar, the temporal kinetic energy density is:

```math
K
=
\frac12\dot\phi^2
```

so:

```math
K
=
\frac{q}{2}
M_D^4
```

This relation is exact under the canonical homogeneous assumptions.

---

# 33. Kinetic-energy result using collider-safe $M_D$

Using:

```text
M_D=650 GeV
```

and:

```text
q=0.742647...
```

014E obtained:

```text
MATCHED_Q_CANONICAL_KINETIC_EV4=
6.6283577903452425e46
```

Using:

```text
1 eV^4 =
20.852156864043042 J/m^3
```

gave:

```text
MATCHED_Q_CANONICAL_KINETIC_J_M3=
1.3821555639528073e48
```

Equivalent mass density:

```text
1.5378554657069117e31 kg/m^3
```

This is not a minor engineering inconvenience.

It catastrophically invalidates an ordinary macroscopic weak-field interpretation.

---

# 34. Mathematical proof of the 014E compactness relation

For a uniform spherical region of radius $R$ and energy density $u$:

```math
E
=
\frac{4\pi}{3}
R^3u
```

Its mass equivalent is:

```math
M
=
\frac{E}{c^2}
=
\frac{4\pi}{3}
\frac{
R^3u
}{
c^2
}
```

The Schwarzschild compactness parameter is:

```math
\mathcal{C}
=
\frac{
2GM
}{
Rc^2
}
```

Substitute $M$:

```math
\mathcal{C}
=
\frac{
2G
}{
Rc^2
}
\left[
\frac{4\pi}{3}
\frac{
R^3u
}{
c^2
}
\right]
```

Therefore:

```math
\mathcal{C}
=
\frac{
8\pi G uR^2
}{
3c^4
}
```

Set $\mathcal{C}=1$:

```math
1
=
\frac{
8\pi G uR_{\mathrm{crit}}^2
}{
3c^4
}
```

so:

```math
R_{\mathrm{crit}}^2
=
\frac{
3c^4
}{
8\pi G u
}
```

and:

```math
R_{\mathrm{crit}}
=
\sqrt{
\frac{
3c^4
}{
8\pi G u
}
}
```

For the 014E kinetic density:

```math
u
=
1.3821555639528073\times10^{48}
\ {\mathrm{J/m^3}}
```

the result is:

```text
R_CRIT=
3.2329633279144379e-03 m
```

or:

```text
3.233 mm
```

Thus a homogeneous region only a few millimeters across would already have order-unity compactness.

---

# 35. Explicit compactness benchmarks

014E found:

```text
R = 1 m
2GM/(Rc^2) ≈ 9.5675e4
```

```text
R = 0.1 m
2GM/(Rc^2) ≈ 956.75
```

```text
R = 0.01 m
2GM/(Rc^2) ≈ 9.5675
```

```text
R = 0.001 m
2GM/(Rc^2) ≈ 0.095675
```

Therefore:

```text
MATCHED_014D_Q_WITH_COLLIDER_SAFE_CONSTANT_B_MACROSCOPIC_WEAK_FIELD=
NO_FOR_CANONICAL_UNIFORM_ENERGY_REALIZATION
```

This does not exclude every noncanonical or exotic realization.

It decisively rejects the simplest brute-force canonical kinetic compensation.

---

# 36. Environment-dependent $B(\phi)$ remains logically open

A field-dependent coupling can in principle differ dramatically between constrained and operating environments.

The minimum required hierarchy is:

```math
\frac{
B_{\mathrm{operating}}
}{
B_{\mathrm{dense}}
}
\gtrsim
3.4605562139399018\times10^{57}
```

Taking the natural logarithm:

```math
\Delta\ln B
=
\ln
\left(
\frac{
B_{\mathrm{operating}}
}{
B_{\mathrm{dense}}
}
\right)
```

gives:

```math
\Delta\ln B
\gtrsim
132.48877963228443
```

This is the exact hierarchy that any simple environment-dependent rescue must explain.

---

# 37. Exponential $B(\phi)$ proof

Consider:

```math
B(\phi)
=
B_{\mathrm{dense}}
\exp
\left[
\beta
\frac{
\phi-\phi_{\mathrm{dense}}
}{
M_{\mathrm{Pl}}
}
\right]
```

Then:

```math
\frac{
B_{\mathrm{operating}}
}{
B_{\mathrm{dense}}
}
=
\exp
\left[
\beta
\frac{
\Delta\phi
}{
M_{\mathrm{Pl}}
}
\right]
```

Take $\ln$:

```math
\ln
\left(
\frac{
B_{\mathrm{operating}}
}{
B_{\mathrm{dense}}
}
\right)
=
\beta
\frac{
\Delta\phi
}{
M_{\mathrm{Pl}}
}
```

Therefore the hierarchy condition requires:

```math
\left|
\beta
\frac{
\Delta\phi
}{
M_{\mathrm{Pl}}
}
\right|
\gtrsim
132.49
```

Examples from 014E:

```text
|Delta phi|/M_Pl = 0.1
|beta| >= 1324.89
```

```text
|Delta phi|/M_Pl = 1
|beta| >= 132.49
```

```text
|Delta phi|/M_Pl = 10
|beta| >= 13.25
```

```text
|Delta phi|/M_Pl = 100
|beta| >= 1.325
```

This is not a proof that such a function is impossible.

It quantifies how nontrivial the required environment dependence must be.

---

# 38. 014E final decision

The direct decision matrix was:

```text
DIRECT_CONSTANT_B_BRIDGE_SURVIVES=NO

CONFORMAL_SYMMETRON_VEV_SCREENING_ALONE_SURVIVES=NO

CANONICAL_KINETIC_COMPENSATION_AT_1M_WEAK_FIELD_SURVIVES=NO

FIELD_DEPENDENT_OR_UV_COMPLETED_DISFORMAL_BRIDGE=NOT_EXCLUDED
```

Final:

```text
014D_LOCAL_TOTAL_FORCE_REVERSAL_RESULT=PRESERVED

014D_REPULSIVE_SIGN_OR_TOTAL_REVERSAL_RETRACTED=NO

MINIMAL_CONSTANT_B_BARYONIC_BRIDGE=
REJECTED_IN_DECLARED_EFT_SCOPE

CANONICAL_KINETIC_COMPENSATION_TO_014D_Q=
CATASTROPHIC_FOR_MACROSCOPIC_WEAK_FIELD_SOURCE

ENVIRONMENT_DEPENDENT_DISFORMAL_OR_UV_COMPLETION_GENERAL_NO_GO=
NO

ORDINARY_BARYONIC_LOCAL_TOTAL_FORCE_REVERSAL=
NOT_ESTABLISHED

PRACTICAL_BARYONIC_ANTIGRAVITY_DEVICE=
NO
```

Classification:

```text
PROJECT_DERIVED_BARYONIC_DISFORMAL_BRIDGE_FEASIBILITY_BOUND
```

---

# 39. The most important new scientific result of the session

The strongest new result is 014D.

The exact conservative statement is:

> **The project numerically reproduced local total-force reversal in a controlled reduced, non-static, nonsymmetric disformal modified-gravity model. The reversal appears in both 2D and 3D, survives grid refinement and timestep halving, and occurs while the tested disformal metric remains safely on the positive-$g_\phi$ branch.**

This is stronger than:

```text
LOCAL_REPULSIVE_COMPONENT=YES
```

because the complete local force satisfies:

```math
\left(
\mathbf{F}_\Psi
+
\mathbf{F}_\phi
\right)
\cdot
\mathbf{F}_\Psi
<
0
```

in the identified regions.

This means the local total acceleration projection is opposite ordinary Newtonian gravity.

---

# 40. The most important new analytical result of the session

The strongest new analytic theorem is the 014C weak-perturbation scaling result:

```math
F_\phi=O(\epsilon^2)
```

while:

```math
F_\Psi=O(\epsilon)
```

at a regular $\xi_0=0$ background.

Therefore:

```math
\frac{
F_\phi
}{
F_\Psi
}
=
O(\epsilon)
```

and the fifth-force advantage vanishes toward the regular weak-perturbation limit.

014D demonstrates that the mechanism can nevertheless cross into local total reversal at sufficiently strong nonlinear disformal coupling before the tested $g_\phi=0.1$ safety margin is crossed.

This combination is scientifically important:

> Weak perturbations suppress the mechanism, but sufficiently nonlinear coupling can overcome Newtonian gravity locally in the reduced model.

---

# 41. The most important new negative result of the session

014E shows that the straightforward ordinary-matter realization fails extremely strongly.

The first 014D reversal corresponds to:

```text
M_D≈2.68 meV
```

whereas the declared direct constant-operator collider comparison requires approximately:

```text
M_D>=650 GeV
```

The coupling mismatch is:

```math
3.46\times10^{57}
```

in $B$.

The corresponding energy-scale mismatch is:

```math
2.43\times10^{14}
```

in $M_D$.

Therefore the project must not describe the constant-$B$ model as a candidate ordinary-matter device.

---

# 42. Updated accomplishment ladder

## Level A — Mathematical gravitational repulsion

```text
YES
```

Established previously.

## Level B — Positive-energy locally repulsive GR source

```text
YES
```

006D within static linearized GR.

## Level C — Repulsive modified-gravity fifth-force component

```text
YES
```

014C in controlled reduced non-static disformal model.

## Level D — Local total-force reversal

```text
YES
```

014D in controlled reduced disformal model.

## Level E — Global force reversal of a complete body

```text
NOT ESTABLISHED
```

## Level F — Ordinary baryonic matter realization

```text
NOT ESTABLISHED
```

The minimal constant-$B$ bridge is rejected.

## Level G — Experimentally allowed laboratory source

```text
NOT ESTABLISHED
```

## Level H — Practical device

```text
NO
```

---

# 43. Current informal practical-antigravity progress estimate

This is not a scientific probability and should not be placed in formal claims.

Informal project-progress estimate at session close:

```text
MATHEMATICAL / LOCAL REPULSION:
100%

LOCAL TOTAL-FORCE REVERSAL IN CONTROLLED THEORY MODEL:
100%

PHYSICALLY CONSISTENT ORDINARY-MATTER REALIZATION:
~15%

EXPERIMENTALLY ALLOWED LAB REALIZATION:
~5%

PRACTICAL DEVICE:
~2-5%

OVERALL PROJECT PROGRESS TOWARD PRACTICAL ANTIGRAVITY:
~10%
```

The reason the overall number increased somewhat after 014D is that the project no longer needs to ask only:

```text
CAN_A_HEALTHY_MODEL_OVERPOWER_GRAVITY_LOCALLY?
```

Within the reduced disformal model, the answer is now numerically:

```text
YES
```

The dominant problem is now source/coupling realization.

---

# 44. Claim ledger after 014E

## Supported established-physics project claim

```text
FINITE_POSITIVE_ENERGY_LINEARIZED_GR_LOCAL_REPULSION=
YES_006D
```

## Supported project-derived analytic results

```text
STATIC/PERIODIC_CLASSICAL_SCALING_BOUNDS=
YES_WITH_DECLARED_SCOPE

CONSERVATIVE_STATE_RESPONSE_IDENTITY=
YES

STATIC_MEDIATOR_SIGN_CLASSIFICATION=
YES_WITH_DECLARED_SCOPE

UNPOLARIZED_STATIC_SPIN_FILTER=
YES_WITH_DECLARED_SCOPE

XI0_ZERO_WEAK_PERTURBATION_SCALING=
F_PHI_O_EPSILON2
F_PSI_O_EPSILON
RATIO_O_EPSILON

DISFORMAL_NORMALIZATION_MAP=
PROVED

CANONICAL_KINETIC_COMPACTNESS_RELATION=
PROVED

ENVIRONMENTAL_B_HIERARCHY_RELATION=
PROVED
```

## Supported project-derived numerical results

```text
014A_FULL_NONLINEAR_SYMMETRON_IMAGE_REPULSION=
NOT_FOUND_IN_TESTED_DOMAIN

014B_STABLE_XI0_ZERO_WINDOWS=
FOUND

014C_2D_ANTIPARALLEL_FIFTH_FORCE=
REPRODUCED

014C_3D_ANTIPARALLEL_FIFTH_FORCE=
REPRODUCED

014D_2D_LOCAL_TOTAL_FORCE_REVERSAL=
REPRODUCED

014D_3D_LOCAL_TOTAL_FORCE_REVERSAL=
REPRODUCED

014D_TOTAL_FORCE_REVERSAL_GRID_REFINEMENT=
PASS

014D_TIMESTEP_HALVING=
PASS

014D_NONDEGENERATE_GPHI_MARGIN=
PASS
```

## Strong negative practical results

```text
STATIC_SPIN_MASS_1G=
REJECTED_BY_GT_13_ORDERS

STANDARD_TESTED_ESTABLISHED_PHYSICS_1G_ROUTE=
NONE_FOUND

SYMMETRON_IMAGE_REPULSION_APPROXIMATION=
FAILED_FULL_NONLINEAR_TESTED_DOMAIN

MINIMAL_CONSTANT_B_BARYONIC_DISFORMAL_BRIDGE=
REJECTED_IN_DECLARED_EFT_SCOPE

CANONICAL_KINETIC_COMPENSATION=
MACROSCOPIC_WEAK_FIELD_FAILURE
```

## Open

```text
GLOBAL_BODY_DISFORMAL_REPULSION

SELF_CONSISTENT_MATTER_DYNAMICS

BARYONIC_DISFORMAL_TOTAL_REVERSAL

FIELD_DEPENDENT_B_PHI_REALIZATION

UV_COMPLETE_DISFORMAL_REALIZATION

ENVIRONMENT_DEPENDENT_DISFORMAL_SCREENING

STABILITY_OF_A_REAL_SOURCE

EXPERIMENTAL_ACCESSIBILITY

PRACTICAL_DEVICE
```

---

# 45. Claims that must NOT be made

Do not claim:

```text
PRACTICAL_ANTIGRAVITY_SOLVED
```

Do not claim:

```text
ORDINARY_MATTER_ANTIGRAVITY_PROVED
```

Do not claim:

```text
DISFORMAL_GRAVITY_IS_REAL_IN_NATURE
```

Do not claim:

```text
014D_IS_A_NEW_PHYSICS_DISCOVERY
```

Do not claim:

```text
GLOBAL_OBJECT_LIFT_WAS_SIMULATED
```

Do not claim:

```text
REACTIONLESS_PROPULSION
```

Do not claim:

```text
ALL_BARYONIC_DISFORMAL_MODELS_ARE_EXCLUDED
```

Do not claim:

```text
ALL_SYMMETRON_REPULSION_IS_IMPOSSIBLE
```

Do not claim:

```text
ALL_UNKNOWN_PHYSICS_ANTIGRAVITY_IS_IMPOSSIBLE
```

The scientifically correct 014D claim is narrower and still significant.

---

# 46. Permanent-code priorities

Before continuing major physics research, the highest-value new results should be permanentized.

Suggested files:

```text
simulations/014a_full_nonlinear_symmetron_image_force.py
simulations/014b_disformal_background_prerequisite.py
simulations/014c_nonstatic_disformal_antiparallel_force.py
simulations/014d_disformal_local_total_force_reversal.py
simulations/014e_baryonic_disformal_bridge_bound.py
```

At minimum 014C, 014D, and 014E deserve permanent preservation.

Each permanent file must follow `FORMATTING_AND_CODE_STANDARDS.md` and document:

* scientific question;
* literature basis;
* equations;
* normalization;
* units;
* sign conventions;
* exact interpretation of $b_0$ versus $B_0$;
* approximation level;
* matter model;
* numerical method;
* CFL choice;
* grid geometry;
* validation strategy;
* force definitions;
* $g_\phi$ condition;
* weak-field condition;
* known limitations;
* claim classification;
* related earlier files.

---

# 47. Regression tests worth adding

Focused tests should preserve at least the following.

## 014C analytical scaling

Test that symbolic power counting gives:

```text
F_PHI_ORDER=2
F_PSI_ORDER=1
RATIO_ORDER=1
```

## 014C numerical scaling

Protect approximate fitted values near:

```text
F_PHI_POWER≈1.991
F_PSI_POWER≈1.000
FORCE_RATIO_POWER≈0.991
```

with tolerances wide enough to survive harmless solver changes.

## 014D reversal threshold

Do not hard-code that the universal threshold is exactly $0.24$.

Instead preserve:

```text
b0=0.22:
NO_REVERSAL_IN_REFERENCE_SCAN

b0=0.24:
REVERSAL_PRESENT_IN_REFERENCE_SCAN
```

under exactly the same model, grid, density field, and numerical conventions.

This is a reference-domain numerical threshold, not a universal theorem.

## 014D 3D sign

Protect a modest 3D reference grid showing:

```text
TOTAL_REVERSAL_FRACTION>0
GPHI>0.1
KINETIC_DENOMINATOR>0
```

## 014E normalization

Test round-trip:

```math
b_0
\rightarrow
M_D
\rightarrow
b_0
```

## 014E compactness

Protect:

```math
R_{\mathrm{crit}}
=
\sqrt{
\frac{
3c^4
}{
8\pi G u
}
}
```

and the approximately:

```text
3.233 mm
```

reference value for the declared input.

---

# 48. Independent verification still needed

014D is internally well checked but not yet publication-grade independently reproduced.

A stronger verification should use at least one independently authored implementation with a meaningfully different numerical method.

Possibilities:

* pseudo-spectral spatial derivatives rather than finite differences;
* RK4 or implicit-explicit time evolution rather than SSPRK3;
* independent FFT/Poisson implementation;
* different asymmetric density realization;
* dynamically evolved matter rather than imposed growing-mode density;
* alternative boundary/domain formulation.

The key reproduction target is:

```math
\left(
\mathbf{F}_\Psi+\mathbf{F}_\phi
\right)
\cdot
\mathbf{F}_\Psi
<
0
```

with:

```math
g_\phi>0
```

and nonzero spatial volume.

Until independent implementation exists, 014D should remain:

```text
PROJECT_DERIVED_NUMERICAL_RESULT
```

rather than a stronger novelty claim.

---

# 49. Highest-value open theoretical question

The active question is no longer:

> Can disformal gravity produce a locally repulsive contribution?

014C answered yes in the controlled reduced model.

It is no longer:

> Can that contribution overpower Newtonian gravity locally?

014D answered yes in the controlled reduced model.

The active question is now:

> **Can a theoretically consistent, stable, environment-dependent or UV-complete disformal coupling act on ordinary baryonic matter with a sufficiently large effective operating-region coupling to retain the 014D total-force reversal, while satisfying high-energy, local-gravity, cosmological, and stability constraints?**

This is the precise frontier.

---

# 50. Quantitative target for any future baryonic model

Any proposed baryonic continuation must explain why the effective coupling can differ by at least:

```math
\frac{
B_{\mathrm{operating}}
}{
B_{\mathrm{constrained}}
}
\sim
3.46\times10^{57}
```

or equivalently:

```math
\Delta\ln B
\gtrsim
132.49
```

between the relevant environments, unless it changes the mechanism sufficiently that the 014D constant-$B$ normalization no longer applies.

This number should be treated as the primary model-building target.

A candidate that merely changes $B$ by a factor of $10^2$, $10^6$, or even $10^{20}$ does not solve the current gap.

---

# 51. What could actually reopen the branch

The branch should be reopened only if a specific theory supplies one or more of the following:

1. a field-dependent $B(\phi)$ with a controlled dynamical reason for a $\Delta\ln B\sim132$ hierarchy;
2. a density-dependent disformal coupling;
3. a phase-transition mechanism that strongly redresses the coupling;
4. a UV completion in which the low-energy effective disformal interaction becomes large while high-energy Standard-Model processes remain suppressed;
5. a noncanonical kinetic structure that achieves the required dimensionless deformation without the canonical $10^{48},{\mathrm{J/m^3}}$ energy density;
6. a screened baryonic model whose screening acts directly on the derivative/disformal operator rather than only on a conformal VEV coupling;
7. an empirical anomaly pointing toward such environment dependence.

Without one of these, additional brute-force PDE scans are unlikely to produce new information.

---

# 52. Stop rules for the next disformal phase

Stop immediately if a proposed continuation:

```text
1.
merely increases constant B beyond experimental bounds.

2.
claims ordinary symmetron conformal screening automatically screens the
constant derivative operator without deriving it.

3.
uses canonical kinetic compensation while ignoring its stress-energy.

4.
requires g_phi -> 0 as the mechanism of force amplification.

5.
crosses g_phi=0.

6.
produces total reversal only through a singular kinetic denominator.

7.
uses a parameter hierarchy but does not explain its radiative stability.

8.
couples only to dark matter and then describes the result as ordinary
baryonic antigravity.

9.
shows local reversed cells but no force on a complete body and calls it
global lift.

10.
violates known constraints by dozens of orders without an explicit
environment-dependent mechanism.

11.
adds arbitrary functions solely to fit the desired answer without an
independent theoretical principle.

12.
fails to identify the physical source, stability mechanism, energy scale,
and coupling to the payload.
```

When a stop rule fires, preserve the negative result and rerank.

---

# 53. Branches that should not be reopened casually

Do not restart without new evidence:

```text
PURE_EINSTEIN_NONLINEAR_GR_SCALING_ESCAPE
```

The weak-field target has:

```math
\frac{gh}{c^2}
\sim
10^{-16}
```

at $1g$, $1,{\mathrm{m}}$.

Do not restart generic Casimir negative-energy device searches without a genuinely new quantum state or theorem.

Do not restart ordinary unscreened scalar/vector fifth forces without a new constraint-evasion principle.

Do not restart simple gold-null vector UV completions.

Do not restart static universal healthy scalar/spin-2 sign-flip searches.

Do not restart the GF1 coherent-field branch without new physics beyond the already tested coherent-state behavior.

Do not restart the symmetron image approximation solely because finite curvature has not been exhaustively scanned.

014A strongly demoted it.

---

# 54. What changed scientifically during this session

At entry, the project had reached an explicit established-physics closure:

```text
VERIFIED_PRACTICAL_1G_ROUTE_COUNT=0
```

The new 014-series work then found something important:

```text
LOCAL_TOTAL_FORCE_REVERSAL=
YES_IN_CONTROLLED_REDUCED_DISFORMAL_MODEL
```

This means 013F was not "wrong."

013F closed the classes it explicitly tested.

The disformal mechanism survives because it leaves those assumptions:

```text
NONSTATIC
NONSYMMETRIC
NONLINEAR
DERIVATIVE_COUPLING
MODIFIED_GRAVITY
```

The session therefore materially improved the search-space map.

---

# 55. What was falsified during this session

## Falsified / strongly demoted

The published symmetron electrostatic image-repulsion approximation did not survive the tested full nonlinear planar-asymmetric calculations.

```text
20 approximate repulsive predictions
20 full nonlinear attractive results
```

## Falsified as a practical ordinary-matter bridge

The minimal universal constant-$B$ Standard-Model continuation of the 014D mechanism.

Required coupling gap:

```text
3.46e57
```

## Falsified

Simple conformal symmetron VEV screening as a sufficient solution for the minimal constant derivative coupling.

## Falsified in canonical macroscopic weak-field realization

Collider-safe $B$ plus brute-force canonical $\dot\phi$ compensation.

Required energy density:

```text
1.38e48 J/m^3
```

with compactness unity at approximately:

```text
3.23 mm
```

---

# 56. What remains unresolved

The following remain genuinely open:

```text
DOES_AN_ENVIRONMENT_DEPENDENT_BARYONIC_DISFORMAL_THEORY_EXIST
```

```text
CAN_SUCH_A_THEORY_RETAIN_014D_FORCE_REVERSAL
```

```text
IS_THE_REQUIRED_B_HIERARCHY_TECHNICALLY_NATURAL
```

```text
CAN_THE_DERIVATIVE_OPERATOR_ITSELF_BE_SCREENED
```

```text
CAN_TOTAL_FORCE_REVERSAL_OCCUR_ON_A_COMPLETE_BARYONIC_BODY
```

```text
IS_GLOBAL_MOMENTUM_ACCOUNTING_COMPATIBLE_WITH_A_USEFUL_APPARATUS
```

```text
CAN_A_LABORATORY_CONFIGURATION_EXIST_WITH_ACCEPTABLE_TOTAL_ENERGY
```

```text
CAN_THE_EFFECT_SURVIVE_REAL_EXPERIMENTAL_CONSTRAINTS
```

```text
PRACTICAL_ANTIGRAVITY_DEVICE
```

---

# 57. Documentation updates now required

The user intends to work on documentation after these carryover notes.

The documentation pass should update, in roughly this order:

```text
1. journal/
2. NOTES.md
3. RESEARCH_BUILDPLAN.md
4. CLAIMS.md
5. README.md
6. ASSUMPTIONS.md if needed
7. RESEARCH_QUESTIONS.md if needed
```

Because the README currently highlights earlier results, preserve historical material before replacing the public-facing frontier.

Follow the established project rule:

> If a newer result supersedes what the README emphasizes, preserve the superseded result in the journal/history first, then update the README.

006D should not disappear from the README.

The correct public story now contains two distinct positive milestones:

```text
006D:
constructive positive-energy local repulsion in linearized GR

014D:
local total-force reversal in a controlled reduced non-static
disformal modified-gravity model
```

and one essential practicality qualification:

```text
014E:
minimal constant-B ordinary-matter bridge fails catastrophically
```

---

# 58. Suggested journal entry

A new journal entry should be created with a title similar to:

```text
2026-08-29_014d_disformal_local_total_force_reversal.md
```

It should contain:

* model definition;
* literature context;
* exact force definitions;
* 014B prerequisite;
* 014C antiparallel force reproduction;
* 014C perturbation theorem;
* 014D coupling scan;
* first reversal at $b_0=0.24$;
* validated $b_0=0.28$ result;
* 2D convergence;
* 3D convergence;
* timestep-halving result;
* $g_\phi$ margin;
* exact claim limitations;
* 014E physical-scale translation;
* constant-$B$ baryonic failure;
* compactness proof;
* future reopen condition.

A second journal entry could separately preserve the 014A negative result if desired.

---

# 59. Suggested README headline structure

Do not replace the established 006D headline with a sensational modified-gravity claim.

A scientifically appropriate structure would be:

```text
1. Established GR result:
   finite positive-energy local gravitational repulsion is possible.

2. New modified-gravity result:
   a controlled non-static disformal model exhibits numerically
   reproduced local total-force reversal.

3. Practicality status:
   no ordinary-matter or practical antigravity device is established.

4. Current barrier:
   minimal constant-B baryonic realization fails by ~3.46e57 in
   coupling strength under the declared EFT comparison.
```

This tells the truth without understating the new result or overstating it.

---

# 60. Suggested CLAIMS.md additions

Potential entries:

```text
CLAIM_ID=014C_DISFORMAL_ANTIPARALLEL_FORCE
TYPE=PROJECT_DERIVED_NUMERICAL_RESULT
STATUS=SUPPORTED_WITHIN_TESTED_REDUCED_MODEL
```

```text
CLAIM_ID=014C_XI0_ZERO_SCALING
TYPE=PROJECT_DERIVED_ANALYTIC_RESULT
STATUS=PROVED_WITHIN_REGULAR_PERTURBATIVE_ASSUMPTIONS
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
CLAIM_ID=014E_ENVIRONMENT_DEPENDENT_DISFORMAL_ESCAPE
TYPE=UNVERIFIED_HYPOTHESIS
STATUS=LOGICALLY_OPEN
```

---

# 61. Suggested buildplan frontier

The active frontier should become approximately:

```text
CURRENT_FRONTIER=
ENVIRONMENT_DEPENDENT_OR_UV_COMPLETE_BARYONIC_DISFORMAL_REALIZATION

ANCHOR_POSITIVE_RESULT=
014D_LOCAL_TOTAL_FORCE_REVERSAL

ANCHOR_ANALYTIC_RESULT=
014C_XI0_ZERO_FORCE_RATIO_SCALING

ANCHOR_NEGATIVE_RESULT=
014E_MINIMAL_CONSTANT_B_BARYONIC_BRIDGE_FAILURE

PRIMARY_OPEN_QUESTION=
CAN_AN_EXPLICIT_STABLE_ENVIRONMENT_DEPENDENT_BARYONIC_DISFORMAL_THEORY
PRODUCE_THE_EFFECTIVE_014D_OPERATING_COUPLING_WHILE_REMAINING_COMPATIBLE
WITH_HIGH_ENERGY_AND_LOCAL_GRAVITY_CONSTRAINTS

REQUIRED_EFFECTIVE_B_HIERARCHY=
3.4605562139399018e57

REQUIRED_DELTA_LN_B=
132.48877963228443

PRACTICAL_ANTIGRAVITY_DEVICE=
NO
```

---

# 62. Highest-value action if research resumes after documentation

Do not begin with another large PDE solver.

The next calculation should be a **model-definition / consistency gate**.

The project should first identify a concrete candidate $B(\phi,\rho,X,\ldots)$ or UV mechanism.

Then ask, analytically:

1. Does it produce the required hierarchy?
2. Is the hierarchy radiatively stable?
3. Does $g_\phi$ stay positive?
4. Does the kinetic matrix stay hyperbolic and ghost-free?
5. Does the effective theory remain below its cutoff?
6. Is the high-energy Standard-Model interaction suppressed?
7. Can baryons actually feel the operating-region force?
8. Does the 014D nonlinear mechanism survive after adding the screening/environment dependence?

Only after those checks should another expensive spatial simulation be run.

---

# 63. Candidate next theorem to seek

A particularly valuable theoretical result would be either:

## Positive

An explicit function $B(\phi)$ or other coupling structure satisfying:

```math
\frac{
B_{\mathrm{operating}}
}{
B_{\mathrm{constrained}}
}
\gtrsim
3.46\times10^{57}
```

while maintaining:

```math
g_\phi>0
```

and a controlled EFT.

That would justify building the next baryonic 3D simulation.

## Negative

A theorem showing that obtaining:

```math
\Delta\ln B
\gtrsim132.49
```

in a technically natural local theory necessarily causes:

* loss of EFT control;
* unacceptable fifth forces;
* radiative instability;
* singular kinetic structure;
* superluminality/causality failure under the project's chosen health conditions;
* or forbidden Standard-Model couplings.

Either outcome would be major progress.

---

# 64. Key numerical values to preserve exactly

```text
REGRESSION_BASELINE=
94 passed
```

## 014A

```text
IMAGE_APPROX_PREDICTED_REPULSIVE_CASES=20
FULL_NONLINEAR_REPULSIVE_CASES=0

MAX_FORCE_ESTIMATOR_REL_DISAGREEMENT=
1.2910282915070713e-04

MAX_NONLINEAR_RESIDUAL=
2.7863523488491637e-08
```

## 014B

```text
MIN_G_PHI_ACROSS_TESTED_BACKGROUNDS=
6.7568601471089274e-01

ALL_TESTED_BETA0_MODELS_HAVE_XI0_SIGN_CHANGE=
YES
```

## 014C

```text
MIN_GPHI_ALL_REFINEMENT_RUNS=
6.6736404459014953e-01

MAX_ROOT_RMS_F5_OVER_FN=
8.1544302935138016e-04

MAX_REPULSIVE_F5_OVER_FN_ANY_TESTED_MEANINGFUL_POINT=
3.0717239259386252e-02

ASYMPTOTIC_F_PHI_POWER=
1.9911392202550136

ASYMPTOTIC_F_PSI_POWER=
1.0000000000000002

ASYMPTOTIC_FORCE_RATIO_POWER=
9.9113922025501222e-01
```

## 014D

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

## 014E

```text
FIRST_REVERSAL_DISFORMAL_SCALE=
2.6799511607263058e-03 eV

VALIDATED_REVERSAL_DISFORMAL_SCALE=
2.5786368350373110e-03 eV

COLLIDER_ALLOWED_CONSTANT_B_b0_MAX=
6.9353012973239908e-59

CONSTANT_B_COUPLING_GAP=
3.4605562139399018e57

DISFORMAL_SCALE_GAP=
2.4254173341869428e14

MATCHED_CANONICAL_KINETIC_ENERGY_DENSITY=
1.3821555639528073e48 J/m^3

MATCHED_MASS_EQUIVALENT_DENSITY=
1.5378554657069117e31 kg/m^3

COMPACTNESS_ONE_RADIUS=
3.2329633279144379e-03 m

REQUIRED_ENVIRONMENTAL_DELTA_LN_B=
132.48877963228443
```

---

# 65. Concise scientific summary for the next researcher

The project now has two particularly important constructive results.

First, 006D demonstrates that finite, nonsingular, positive-energy, locally conserved, energy-condition-compatible stress-energy can produce local gravitational repulsion in static linearized GR.

Second, 014D demonstrates numerically that a controlled reduced non-static disformal modified-gravity model can produce **local total-force reversal**, not merely a repulsive correction. The result survives 2D and 3D refinement, timestep halving, and a conservative positive-$g_\phi$ margin.

However, 014E finds that the direct minimal constant-$B$ extension to Standard-Model matter is not viable in its declared EFT scope. The first reversal corresponds to a physical constant-disformal suppression scale of only about $2.68,{\mathrm{meV}}$, while the directly compared collider benchmark is about $650,{\mathrm{GeV}}$. This is a coupling mismatch of approximately $3.46\times10^{57}$.

Attempting to compensate with canonical scalar kinetic energy requires approximately $1.38\times10^{48},{\mathrm{J/m^3}}$ and reaches compactness unity at only about $3.23,{\mathrm{mm}}$.

Therefore:

```text
LOCAL_TOTAL_FORCE_REVERSAL=
ESTABLISHED_NUMERICALLY_IN_CONTROLLED_REDUCED_MODEL

ORDINARY_BARYONIC_REALIZATION=
NOT_ESTABLISHED

MINIMAL_CONSTANT_B_BARYONIC_BRIDGE=
REJECTED_IN_DECLARED_SCOPE

ENVIRONMENT_DEPENDENT_OR_UV_COMPLETE_BARYONIC_DISFORMAL_ROUTE=
LOGICALLY_OPEN

PRACTICAL_ANTIGRAVITY_DEVICE=
NO
```

---

# 66. Exact next-session start instruction

At the start of the next research session:

```text
1.
Read these carry-forward notes.

2.
Read the newest NOTES.md, RESEARCH_BUILDPLAN.md, README.md,
CLAIMS.md, and codebundle after the documentation update.

3.
Reconfirm the 94-test baseline or the new expected baseline if
permanent 014-series regressions have been added.

4.
Do not restart 014A symmetron image scans.

5.
Do not rerun generic constant-B disformal parameter scans.

6.
Do not claim ordinary baryonic antigravity from 014D.

7.
Treat 014D as the positive anchor.

8.
Treat 014E as the minimal-realization obstruction.

9.
Make the single active question:

CAN_AN_EXPLICIT_ENVIRONMENT_DEPENDENT_OR_UV_COMPLETE_BARYONIC
DISFORMAL_THEORY_BRIDGE_THE_014E_GAP_WHILE_RETAINING_THE_014D
TOTAL_FORCE_REVERSAL?

10.
Perform the cheapest analytical consistency/no-go test before
another expensive PDE simulation.
```

---

# 67. Final session classification

```text
006D_CONSTRUCTIVE_LINEARIZED_GR_REPULSION=
PRESERVED

013F_ESTABLISHED_PHYSICS_CLOSURE=
PRESERVED_WITH_EXPLICIT_SCOPE

014A_SYMMETRON_IMAGE_BRANCH=
STRONGLY_DEMOTED

014B_NONSTATIC_DISFORMAL_PREREQUISITE=
GREEN

014C_ANTIPARALLEL_DISFORMAL_FIFTH_FORCE=
REPRODUCED

014C_WEAK_LIMIT_SCALING_THEOREM=
PROVED_AND_NUMERICALLY_CONFIRMED

014D_LOCAL_TOTAL_FORCE_REVERSAL=
REPRODUCED_IN_CONTROLLED_REDUCED_MODEL

014D_GRID_CONVERGENCE=
PASS

014D_TIMESTEP_CONTROL=
PASS

014D_NONDEGENERATE_METRIC_MARGIN=
PASS

014E_MINIMAL_CONSTANT_B_BARYONIC_BRIDGE=
REJECTED_IN_DECLARED_EFT_SCOPE

014E_CANONICAL_KINETIC_COMPENSATION=
MACROSCOPIC_WEAK_FIELD_FAILURE

ENVIRONMENT_DEPENDENT_OR_UV_COMPLETE_DISFORMAL_ESCAPE=
OPEN

ORDINARY_BARYONIC_TOTAL_FORCE_REVERSAL=
NOT_ESTABLISHED

GLOBAL_BODY_REPULSION=
NOT_ESTABLISHED

PRACTICAL_ANTIGRAVITY_DEVICE=
NO

CURRENT_FRONTIER=
ENVIRONMENT_DEPENDENT_OR_UV_COMPLETE_BARYONIC_DISFORMAL_REALIZATION

CURRENT_HIGHEST_VALUE_NEXT_ACTION=
DOCUMENT_AND_PERMANENTIZE_014C_014D_014E_THEN_REQUIRE_EXPLICIT_MODEL_BEFORE_MORE_NUMERICS
```

---

# 68. Final perspective

The project made a meaningful advance in this session.

Before the 014-series work, the practical search could reasonably be summarized as:

> No tested established-physics mechanism had produced a credible path to practical antigravity.

The project can now say something stronger and more nuanced:

> **A controlled non-static disformal modified-gravity model can numerically produce a local total acceleration whose projection is opposite Newtonian gravity. The difficulty is no longer purely the mathematical sign or even local force magnitude. The dominant unresolved barrier is constructing a physically allowed ordinary-matter realization.**

That is real progress.

But the gap between the reduced-model phenomenon and a practical device remains enormous.

The scientifically disciplined frontier is therefore not:

```text
FIND_MORE_REPULSIVE_SIGNS
```

It is:

```text
MAKE_THE_014D_EFFECT_PHYSICALLY_REALIZABLE_ON_ORDINARY_MATTER
WITHOUT_PATHOLOGY_OR_CONSTRAINT_VIOLATION
```

Until that bridge exists:

```text
PRACTICAL_ANTIGRAVITY=
NOT_SOLVED
```

### END NOTE - AUGUST 29 2026 - 12:35 CST


### BEGIN NOTE - AUGUST 29 2026 - 15:10 CST

# ANTIGRAVITY_RESEARCH — Comprehensive Carry-Forward Notes

**Session closeout:** August 29, 2026
**Research slice:** 014B–015C disformal practicality gates, followed by 016A–016H renewed 006D physical-realization program
**Repository:** `ANTIGRAVITY_RESEARCH`
**Known-solution regression baseline:** `94 passed`
**Current informal practical-antigravity progress heuristic:** approximately **44%**
**Important:** the 44% figure is a project-management/progress heuristic only. It is **not a scientific probability** that practical antigravity exists or can be built.

---

# 0. Executive Summary

The project remains anchored by one strong constructive result:

> # **We have a mathematical construction for antigravity-like gravitational repulsion.**

The precise supported statement remains:

> **Within static linearized general relativity, there exists an explicit finite-radius, finite-thickness, nonsingular, positive-energy, locally conserved type-I stress-energy configuration satisfying NEC, WEC, and DEC whose calculated near gravitational field points outward while its far-field active mass remains positive.**

This is Simulation **006D**.

It remains the strongest established project-derived positive result. The README correctly classifies it as a constructive linearized-GR stress-energy result rather than a material realization, stability proof, nonlinear Einstein solution, experiment, or device.

The research slice completed in this session substantially advanced the next question:

> **Can physically motivated fields actually realize something sufficiently close to the 006D stress organization to retain its outward field?**

The answer is now considerably sharper.

We learned:

```text
CAN_THICKER_006D_SOURCES_REDUCE_PEAK_STRESS=
YES

DO_THEY_KEEP_FIXED_CHARGE_STABILITY_CAPACITY=
YES

DOES_THE_SIMPLEST_GLOBAL_ELECTROSTATIC_GAUGE_REALIZATION_WORK=
NO

CAN_SMOOTH_NONCOMPACT_TAILS_REMOVE_THE_COMPACT_BOUNDARY_DIVERGENCE=
YES

DOES_THE_EXPONENTIAL_TAIL_WORK_FOR_THE_MINIMAL_GAUGED_WINDING_SECTOR=
NO

DOES_A_C2_POWER_LAW_TAIL_PASS_THE_FINITE_GAUGE_ENERGY_PREFLIGHT=
YES

CAN_TEMPORAL_CHARGE_AND_WINDING_COEXIST_KINEMATICALLY=
YES

CAN_THE_REQUIRED_GAUGE_MISMATCH_BE_REDUCED_FROM ~130 TO ~10=
YES

DOES_THE_EXACT_POWER_LAW_TARGET SATISFY_THE_MINIMAL_CANONICAL_WINDING_EULER_LAGRANGE_ASYMPTOTICS=
NO

DO_GENERIC_HEALTHY_FLS_LIKE_BOUND_FIELD_EQUILIBRIA_WITH_NEGATIVE_ACTIVE_DENSITY_AUTOMATICALLY_REPEL=
NO
```

The deepest lesson of the slice is therefore:

> **The 006D result is not successful merely because it contains negative active gravitational density. Its success depends on the spatial organization of negative and positive active stress relative to the gravitational Green-function kernel.**

016H made that distinction particularly clear. Sixty-three bound, internally consistent variational field configurations developed genuine negative active-density regions, in one case totaling approximately `26.66%` of the total energy scale, yet none generated outward gravitational acceleration even in the near field. The attractive sign was stable under independent quadrature refinement.

This suggests that the highest-value established-GR continuation is **not another generic co-spatial Q-ball/FLS configuration** and not further exact fitting of the 006D tensor.

The next established-GR architecture should instead deliberately reproduce the **spatial sign segregation** of 006D:

```text
CENTRAL / NEAR-TARGET REGION:
strong negative active stress

OUTER / LOW-KERNEL REGION:
positive compensating support, charge, current, gauge energy, and total mass
```

A natural candidate is a spatially separated:

```text
DOMAIN-WALL / MEMBRANE "DRUM"
+
CHARGED / COUNTER-WINDING "RIM" OR VORTON
```

with the actual matter equations allowed to determine the detailed stress tensor while **outward gravity itself**, rather than exact 006D tensor matching, is used as the optimization objective.

However, even a successful matter realization would still face the project's largest pure-GR practicality obstacle:

```math
M
\sim
C\frac{a h^2}{G}
```

and, for tiled source cells covering a macroscopic payload area,

```math
\frac{E}{A}
\sim
\frac{Cac^2}
{\pi x_{\max}^2G},
```

for which the microstandoff scale $h$ cancels.

Therefore reaching a practical device almost certainly requires **two distinct breakthroughs**:

1. realize an outward-gravity stress pattern with actual stable fields;
2. find a mechanism that changes the catastrophic macroscopic energy scaling or uses a stronger effective interaction.

The current project should be viewed as approximately **44% along an informal success ladder**, not 44% likely to produce a device.

---

# 1. Claim Hierarchy at Session Close

It is essential that the next session not collapse different achievement levels together.

## Level A — mathematical sign possibility

```text
ESTABLISHED
```

General relativity permits local repulsive gravitational behavior.

Known GR examples reproduced by the project include:

* cosmological-constant / Kottler repulsion;
* Reissner–Nordström repulsive behavior;
* relativistic domain-wall repulsion;
* negative-pressure gravitational defocusing.

## Level B — explicit positive-energy local repulsion

```text
ESTABLISHED_IN_STATIC_LINEARIZED_GR
```

006D constructs a finite positive-energy source satisfying NEC/WEC/DEC and local linearized conservation that produces an outward near field.

## Level C — physical matter realization

```text
NOT_ESTABLISHED
```

No known field or material has yet been demonstrated to generate the required stress distribution as a genuine solution of its equations of motion.

## Level D — dynamic stability

```text
PARTIAL_PREFLIGHT_ONLY
```

Fixed-charge capacity exists against one Derrick-type scaling mode.

No complete perturbation spectrum has been solved.

## Level E — nonlinear Einstein-matter realization

```text
NOT_ESTABLISHED
```

The source has not been solved self-consistently with the full nonlinear Einstein equations.

## Level F — finite-payload operational lift

```text
NOT_ESTABLISHED
```

Local point acceleration is not enough.

The 015C disformal work reinforced that local force reversal can disappear when integrated across a finite passive payload.

## Level G — practical energy and materials

```text
NOT_ESTABLISHED
```

Pure-GR energy scaling remains catastrophic.

## Level H — experiment

```text
NO
```

## Level I — practical antigravity device

```text
NO
```

---

# 2. Strongest Established Result — Simulation 006D

## 2.1 Exact claim

The strongest positive result should be carried forward verbatim:

> **Within static linearized general relativity, there exists an explicit finite-radius, finite-thickness, nonsingular, positive-energy, locally conserved type-I stress-energy configuration satisfying NEC, WEC, and DEC whose calculated near field points outward while its far-field active mass remains positive.**

The repository README contains sufficient information to independently reconstruct the source and its Green-function field calculation.

Classification:

```text
CLAIM_CLASSIFICATION=
CONSTRUCTIVE_LINEARIZED_GR_STRESS_ENERGY_RESULT

NOVEL_PHYSICS_DISCOVERY=
NO

PRACTICAL_DEVICE=
NO
```

---

# 3. Mathematical Proof of the 006D Headline Result

This is the proof that should remain the foundation of the project.

## 3.1 Conventions

Metric signature:

```math
(-,+,+,+)
```

Use a local orthonormal frame with static type-I stress energy:

```math
T_{\hat\mu\hat\nu}
=
\mathrm{diag}
\left(
\epsilon,
p_r,
p_\phi,
p_z
\right).
```

Positive $p_i$ denotes pressure and negative $p_i$ denotes tension.

---

## 3.2 Linearized Einstein equation and active gravitational source

Write:

```math
g_{\mu\nu}
=
\eta_{\mu\nu}
+
h_{\mu\nu}
```

with:

```math
|h_{\mu\nu}|\ll1.
```

Define trace reversal:

```math
\bar h_{\mu\nu}
=
h_{\mu\nu}
-
\frac12\eta_{\mu\nu}h.
```

In harmonic gauge:

```math
\Box\bar h_{\mu\nu}
=
-\frac{16\pi G}{c^4}T_{\mu\nu}.
```

For a static source:

```math
\nabla^2\bar h_{\mu\nu}
=
-\frac{16\pi G}{c^4}T_{\mu\nu}.
```

Using:

```math
h_{00}
=
\frac12
\left(
\bar h_{00}
+
\bar h_{11}
+
\bar h_{22}
+
\bar h_{33}
\right)
```

and:

```math
g_{00}
=
-\left(
1+\frac{2\Phi}{c^2}
\right),
```

one obtains:

```math
\nabla^2\Phi
=
\frac{4\pi G}{c^2}
\left(
\epsilon+p_r+p_\phi+p_z
\right)
.
```

Define:

```math
S
=
\epsilon+p_r+p_\phi+p_z.
```

This is the active weak-field source.

The Green-function solution is:

```math
\Phi(\mathbf{x})
=
-\frac{G}{c^2}
\int
\frac{S(\mathbf{x}')}
{|\mathbf{x}-\mathbf{x}'|}
\,d^3x'.
```

Physical acceleration is:

```math
\mathbf{a}=-\nabla\Phi.
```

For an axisymmetric source and an on-axis target at $z=h$:

```math
a_z(h)
=
-\frac{2\pi G}{c^2}
\int dz
\int_0^\infty dr\,
r S(r,z)
\frac{h-z}
{\left[
r^2+(h-z)^2
\right]^{3/2}}.
```

Repository convention:

```text
a_z > 0  = outward, away from the source
a_z < 0  = inward, toward the source
```

The kernel:

```math
K_h(r,z)
=
\frac{h-z}
{\left[
r^2+(h-z)^2
\right]^{3/2}}
```

is positive for source points below the target.

Therefore outward acceleration requires:

```math
\int S K_h\,dV<0.
```

Crucially, this does **not** require:

```math
\int S\,dV<0.
```

This is the mathematical opening that allows local outward gravity while preserving positive total far-field mass.

---

# 4. Dimensionless 006D Source

Define:

```math
x=\frac rh,
\qquad
\zeta=\frac zh.
```

Target:

```math
\zeta_{\mathrm{target}}=1.
```

Finest tested finite construction:

```text
ALPHA=1.437500564637
BETA=4.701437405300
DELTA=0.00625
INNER_WIDTH=0.0015625
OUTER_WIDTH=0.00625
OUTER_RADIUS=4.707687405300
```

---

# 5. Exact Radial Conservation Construction

Define:

```math
q(x)=x p_r(x)
```

and impose:

```math
p_\phi(x)=q'(x).
```

Set:

```math
p_z=0,
\qquad
T_{rz}=0.
```

Then:

```math
p_r=\frac qx.
```

Differentiating:

```math
\frac{dp_r}{dx}
=
\frac{q'}x
-
\frac{q}{x^2}.
```

The cylindrical static radial conservation equation is:

```math
\frac{dp_r}{dx}
+
\frac{p_r-p_\phi}{x}
=
0.
```

Substitution gives:

```math
\frac{q'}x
-
\frac{q}{x^2}
+
\frac{q/x-q'}x
=
0.
```

Therefore:

```math
\frac{dp_r}{dx}
+
\frac{p_r-p_\phi}{x}
=
0
```

identically.

This is the core analytic conservation proof.

It is conservation in the flat-background/static linearized construction.

It does **not** yet establish exact curved-spacetime:

```math
\nabla_\mu T^{\mu\nu}=0
```

in a self-consistent nonlinear metric.

---

# 6. Explicit Radial Stress Profile

Core branch:

```math
q_{\mathrm{core}}(x)=-x.
```

Therefore:

```math
p_r=-1,
\qquad
p_\phi=-1.
```

This gives the central tension-dominated active source.

Transfer annulus:

```math
q_{\mathrm{ann}}(x)
=
-\frac{\alpha^2}{x}.
```

Therefore:

```math
p_r
=
-\frac{\alpha^2}{x^2}
```

and:

```math
p_\phi
=
+\frac{\alpha^2}{x^2}.
```

Thus:

```math
p_r+p_\phi=0
```

through the transfer annulus.

Cubic smoothstep transitions are used to connect regions:

```math
s(u)
=
u^2(3-2u).
```

The outer collar smoothly drives:

```math
q\rightarrow0
```

and:

```math
q'\rightarrow0.
```

Consequently the finite source does not require the singular support ring of the earlier thin construction.

---

# 7. Finite Vertical Profile

For:

```math
-\delta\le\zeta\le0
```

define:

```math
\varphi_\delta(\zeta)
=
\frac{30}{\delta}
y^2(1-y)^2
```

with:

```math
y
=
\frac{\zeta+\delta}{\delta}.
```

Outside the slab:

```math
\varphi_\delta=0.
```

Normalization:

```math
\int_{-\delta}^0
\varphi_\delta(\zeta)\,d\zeta
=
1.
```

Peak:

```math
\varphi_{\delta,\max}
=
\frac{1.875}{\delta}.
```

Physical stress scale:

```math
p_r^{\mathrm{phys}}
=
\frac{U_0}{h}
p_r(x)
\varphi_\delta(\zeta)
```

with analogous expressions for $p_\phi$ and $\epsilon$.

---

# 8. Energy-Condition Proof

Choose:

```math
\epsilon
=
\max
\left(
|p_r|,
|p_\phi|
\right).
```

Since:

```math
p_z=0,
```

we immediately have:

```math
\epsilon\ge0,
```

```math
|p_r|\le\epsilon,
```

```math
|p_\phi|\le\epsilon,
```

and:

```math
|p_z|\le\epsilon.
```

For static type-I matter this is precisely the pointwise dominant-energy-condition requirement.

Thus:

```text
DEC=PASS
WEC=PASS
NEC=PASS
```

for the constructed source.

The numerical audit returned:

```text
MAX_DEC_VIOLATION=0
MIN_NEC_MARGIN=0
```

where the zero NEC margin indicates saturation in some regions, not failure.

---

# 9. Positive Far-Field Active-Mass Proof

Define the dimensionless integrated spatial-stress trace:

```math
\tau
=
2\int x
\left(
p_r+p_\phi
\right)
dx.
```

Using:

```math
p_r=\frac qx,
\qquad
p_\phi=q',
```

gives:

```math
x(p_r+p_\phi)
=
q+xq'.
```

But:

```math
q+xq'
=
\frac{d}{dx}(xq).
```

Therefore:

```math
\tau
=
2[xq]_0^{x_{\max}}.
```

The construction obeys:

```math
q(0)=0
```

and:

```math
q(x_{\max})=0.
```

Hence:

```math
\tau=0
.
```

Since:

```math
\epsilon\ge0
```

and the source contains nonzero energy:

```math
\int\epsilon\,dV>0.
```

Therefore the integrated active gravitational mass is positive.

The near field may point outward while the asymptotic monopole remains attractive.

This distinction is central:

```text
LOCAL_REPULSION=YES

POSITIVE_TOTAL_ACTIVE_MASS=YES

GLOBAL_ASYMPTOTIC_REPULSION=NO
```

---

# 10. Direct 006D Field Calculation

Define:

```math
A(x)
=
\epsilon+p_r+p_\phi.
```

For the finite vertical profile:

```math
K_\delta(x)
=
\int_{-\delta}^0
\varphi_\delta(\zeta)
\frac{1-\zeta}
{\left[
x^2+(1-\zeta)^2
\right]^{3/2}}
\,d\zeta.
```

Then:

```math
F_\delta
=
-\int_0^{x_{\max}}
xA(x)K_\delta(x)\,dx.
```

The physical acceleration is:

```math
a_z
=
\frac{2\pi G U_0}{c^2}
F_\delta.
```

Thus:

```math
F_\delta>0
```

means outward acceleration.

The mass has form:

```math
M
=
\frac{\pi U_0h^2}{c^2}
m_\delta.
```

Eliminating $U_0$ gives:

```math
M
=
C\frac{ah^2}{G}
```

with:

```math
C
=
\frac{m_\delta}
{2F_\delta}
.
```

---

# 11. Central 006D Numerical Verification

Best tested finite construction:

```text
C_FINITE=
23.591586299249
```

Independent thin conserved architecture:

```text
C_THIN=
23.426710175391
```

Relative finite-to-thin difference:

```text
≈0.704%
```

Independent field quadratures:

```text
FIELD_FACTOR_GL64=
2.352695737495157e-01

FIELD_FACTOR_NESTED=
2.352695737495351e-01
```

Agreement is approximately:

```text
1.94e-14
```

in absolute field factor.

Additional invariants:

```text
MASS_FACTOR=
1.110076490539830e+01

TRACE_FACTOR=
2.922107000813412e-13

ACTIVE_MASS_FACTOR=
1.110076490539859e+01

MAX_CONTROL_VOLUME_CONSERVATION_RESIDUAL=
3.103073353827313e-14

MAX_DEC_VIOLATION=
0

MIN_NEC_MARGIN=
0
```

The README and prior journal preserve these as the central reproduction targets.

---

# 12. Human-Scale 006D Energy Benchmark

For:

```math
a=g
```

and:

```math
h=1\ {\mathrm{m}},
```

the finest 006D source requires approximately:

```text
M_equiv≈3.466e12 kg
```

and:

```text
E≈3.115e29 J.
```

Compactness remains tiny:

```math
\frac{GM}{hc^2}
\approx
2.6\times10^{-15}.
```

Therefore the difficulty is not that the source automatically forms a black hole.

The problem is the enormous quantity and organization of relativistic stress energy.

This remains the principal pure-GR practicality barrier.

---

# 13. Important Pre-016 Field-Realization Results

The 016 series must not be interpreted without the 008 field-realization work.

## 13.1 008A — wall plus current loop

Model:

```math
E(R)
=
\pi\sigma R^2
+
2\pi\mu R
+
\frac JR.
```

Equilibrium:

```math
J
=
2\pi R^2
(\sigma R+\mu).
```

Positive second derivative provides a radial equilibrium mode.

Boundary stress:

```math
U_b
=
\sigma R+2\mu,
```

```math
T_b
=
-\sigma R.
```

DEC requires:

```math
\mu\ge0.
```

The lowest-energy limit $\mu=0$ simply recovers the previous domain-wall-like stress ratio.

Decision:

```text
WALL_PLUS_CURRENT_LOOP_IMPROVES_006D=
NO
```

It may help stabilization but does not improve the fundamental energy efficiency.

---

# 14. 008B — Canonical Scalar Representability and Derrick Failure

For static canonical real scalars:

```math
T_{ij}
=
M_{ij}
-
\rho\delta_{ij}.
```

Diagonal Gram entries satisfy:

```math
M_{ii}
=
\rho+p_i.
```

The potential is:

```math
V
=
-\frac12
\left(
\rho+\sum_i p_i
\right).
```

Because 006D satisfies DEC, the local Gram matrix is positive semidefinite.

Therefore:

```text
LOCAL_ALGEBRAIC_CANONICAL_SCALAR_REPRESENTABILITY=
YES
```

but strict axisymmetry and angular-gradient requirements prevent a single simple real scalar from realizing the source globally.

For a static canonical scalar configuration:

```math
E(\lambda)
=
\frac K\lambda
+
\frac U{\lambda^3}.
```

At a stationary point, the virial relation implies:

```math
E''(1)
=
-3E.
```

Therefore:

```text
PURE_STATIC_CANONICAL_SCALAR_DERRICK_STABLE=
NO
```

for positive total energy.

---

# 15. 008C — Fixed-Charge Stability Capacity

Stationary complex scalar time dependence can provide temporal kinetic energy.

Define:

```math
D
=
\sum_a
\dot\phi_a^2.
```

Local maximum permitted by the stress tensor:

```math
D_{\max}
=
\min_i
(\rho+p_i).
```

Temporal kinetic energy:

```math
T
=
\frac D2.
```

At fixed conserved charge:

```math
E_Q(\lambda)
=
\lambda^3T
+
\frac K\lambda
+
\frac U{\lambda^3}.
```

The second derivative is:

```math
E_Q''(1)
=
24T-3E-5P.
```

With integrated pressure:

```math
P\approx0,
```

one-mode stability requires:

```math
\frac TE>\frac18
.
```

For the finest original 006D source:

```text
TMAX/E=
0.186185265139

CRITICAL=
0.125

CAPACITY/CRITICAL≈
1.48948
```

Therefore sufficient temporal kinetic **capacity** exists to stabilize one Derrick dilation mode.

This is not full dynamic stability.

---

# 16. 008D — Charge and Winding Must Be Separate

One stationary winding scalar:

```math
\Phi
=
f
e^{i(n\phi-\omega t)}
```

contains both temporal and angular gradients.

Their cross product generates:

```math
T_{t\phi}\neq0.
```

The engineered 006D target is static and diagonal:

```math
T_{t\phi}=0.
```

Therefore:

```text
ONE_COMPLEX_SCALAR_EXACT_006D_REALIZATION=
REJECTED

TEMPORAL_CHARGE_AND_STATIC_ANGULAR_STRESS_SECTORS_MUST_BE_SEPARATE=
YES
```

Counter-winding fields can cancel net angular momentum algebraically.

---

# 17. 008E — Finite Ungauged Winding Termination Fails

A necessary winding bound was derived of the schematic form:

```math
N
\ge
\frac{
\left|
\frac{d}{dr}
(r\sqrt A)
\right|
}
{\sqrt{G_r}}.
```

Near the original compact outer boundary:

```math
N
\sim
\frac{757}
{\delta/w}
```

and therefore:

```math
N\rightarrow\infty
```

as the termination is approached.

Decision:

```text
FINITE_UNGAUGED_WINDING_SET_CAN_EXACTLY_REALIZE_006D_OUTER_TERMINATION=
NO

GAUGE_OR_OTHER_COMPENSATING_SECTOR_REQUIRED=
YES
```

---

# 18. 008F — Local Gauge Takeover

The outer collar has:

```math
p_\phi=\epsilon,
\qquad
p_r\le0,
\qquad
p_z=0.
```

Define:

```math
g
=
\epsilon+p_r.
```

A local decomposition is:

```math
T_g
=
(g,0,g,0)
```

plus residual:

```math
T_s
=
(-p_r,p_r,-p_r,0).
```

The residual scalar Gram matrix remains positive semidefinite.

A 30% gauge takeover retained:

```text
T/E≈0.14598
```

above the Derrick threshold:

```text
0.125
```

and gave positive dilation curvature.

Critical gauge takeover was approximately:

```text
38.37%
```

Decision:

```text
LOCAL_GAUGE_STRESS_DECOMPOSITION=
YES

FINITE_GAUGE_LAYER_AND_FIXED_CHARGE_CAPACITY_HAVE_NONZERO_WINDOW=
YES

GLOBAL_SMOOTH_GAUGE_POTENTIALS=
NOT_ESTABLISHED
```

This distinction directly motivated 016C–016G.

---

# 19. Disformal Slice Immediately Before the 016 Program

The current session also included important work on the modified-gravity route.

These results should remain documented because they are part of the reranking after the new pure-GR field-realization failures.

---

# 20. 014D — Controlled Disformal Local Total-Force Reversal

The exact vector criterion for the total force to reverse relative to the Newtonian direction is:

```math
\mathbf{F}_{\mathrm{tot}}
\cdot
\mathbf{F}_\Psi
<
0.
```

With:

```math
\mathbf{F}_{\mathrm{tot}}
=
\mathbf{F}_\Psi
+
\mathbf{F}_\phi,
```

this becomes:

```math
|\mathbf{F}_\Psi|^2
+
\mathbf{F}_\phi
\cdot
\mathbf{F}_\Psi
<
0.
```

Therefore:

```math
-\mathbf{F}_\phi
\cdot
\mathbf{F}_\Psi
>
|\mathbf{F}_\Psi|^2
.
```

For perfectly antiparallel forces:

```math
|\mathbf{F}_\phi|
>
|\mathbf{F}_\Psi|.
```

014D found local total-force reversal in a controlled reduced, non-static, nonsymmetric disformal model.

First coarse safe reversal:

```text
b0=0.24
```

Validated point:

```text
b0=0.28
```

with 2D and independent 3D refinement plus timestep-halving.

Health checks included:

```text
MIN_GPHI≈0.1385 > 0.1 floor

MIN_KINETIC_DENOMINATOR≈1.076 > 0
```

The project therefore has a genuine numerical local-force-reversal result in that reduced model.

But it does not provide ordinary-matter antigravity.

---

# 21. 014E — Ordinary-Matter Bridge Failure

Mapping the reduced disformal parameter to a minimal constant disformal operator gave:

```math
b_0
=
H_0^2M_{\mathrm{Pl}}^2B_0,
```

with:

```math
B_0
=
M_D^{-4}.
```

Matching the 014D operating coupling while respecting the constrained ordinary-matter scale required approximately:

```math
\frac{
B_{\mathrm{operating}}
}{
B_{\mathrm{dense}}
}
\gtrsim
3.46\times10^{57}.
```

Equivalently:

```math
\Delta\ln B
\gtrsim
132.49
.
```

The simplest constant-$B$ ordinary-baryon bridge was therefore rejected.

This is an enormous hierarchy, not an order-unity engineering problem.

---

# 22. 015A — Minimal Protected Pair Portal Failure

The project attempted to protect a material-specific pair scalar portal using ordinary additive symmetries.

Enumeration through the tested $Z_N$ classes found no simple assignment that permitted the desired pair operator while forbidding all dangerous one-body operators.

The one-body counterterm was also logarithmically divergent by power counting in the minimal setup.

Therefore:

```text
SIMPLE_ADDITIVE_SYMMETRY_PROTECTION=
REJECTED
```

More elaborate structural protection remains logically open.

---

# 23. 015C — Finite-Payload Disformal Gate

015C asked a crucial operational question:

> Does the locally reversed force survive integration over a finite passive payload?

The first root-time finite-payload search found:

```text
DISCOVERY_SAFE_GLOBAL_REVERSAL_CASES=
0
```

and:

```text
GLOBAL_BODY_REPULSION=
NOT_ESTABLISHED.
```

The strongest safe candidate canceled approximately half the inward Newtonian component but remained inward overall.

Core lesson:

```text
LOCAL_REVERSED_CELLS=
YES

FINITE_PAYLOAD_CENTER_OF_MASS_REVERSAL=
NO_IN_TESTED_SCAN
```

This result established a permanent project rule:

> **Every future candidate must eventually be tested against a finite-payload center-of-mass observable, not merely a pointwise or grid-cell sign.**

The disformal journal explicitly preserves this distinction and the remaining dynamic-time / original-geometry finite-payload controls.

---

# 24. Simulation 016A — Practicality-Optimized Thickness

## Scientific question

Does the mathematically optimal extremely thin 006D source actually make the best physical realization target?

Answer:

```text
NO
```

The source was re-evaluated at larger finite thickness.

Results:

```text
delta=.40000
C=38.037638025730
C penalty vs fine≈1.61234x
peak-stress relief≈2635.7x
feature-width gain=64x

delta=.20000
C=29.559369544823
C penalty≈1.25296x
peak-stress relief≈832.5x
feature-width gain=32x

delta=.10000
C=26.258214373557
C penalty≈1.11303x
peak-stress relief≈232.1x
feature-width gain=16x

delta=.00625
C=23.591586299249
```

The peak stress behaves roughly as:

```math
\epsilon_{\mathrm{peak}}
\propto
\frac1{h\delta^2}.
```

Thus modest thickening buys enormous relief in local stress.

Preferred practical bracket became:

```text
delta≈0.10–0.20.
```

This was an important design improvement.

---

# 25. 016A Macroscopic Coverage No-Free-Lunch Result

For one cell:

```math
E_{\mathrm{cell}}
=
C\frac{ah^2c^2}{G}.
```

Its footprint is approximately:

```math
A_{\mathrm{cell}}
=
\pi x_{\max}^2h^2.
```

Therefore:

```math
\frac{E_{\mathrm{cell}}}
{A_{\mathrm{cell}}}
=
\frac{
Cac^2
}{
\pi x_{\max}^2G
}
.
```

The factor:

```math
h^2
```

cancels exactly.

This is a major practicality result.

Miniaturizing each cell decreases its individual energy as $h^2$, but the number of cells required to cover a fixed macroscopic area increases as $1/h^2$.

Consequently simple tiling does not solve the macroscopic energy problem.

At $1g$, the tested 006D-like architectures remain around:

```text
~4.5–5.2e27 J/m²
```

or order:

```text
~5e10 kg-equivalent/m².
```

This is one of the most important barriers in the entire project.

---

# 26. Simulation 016B — Thick Charge/Gauge Capacity

016B checked whether the practical thickness advantage destroyed the previous fixed-charge stabilization window.

It did not.

Representative:

```text
delta=.10
Tmax/E≈0.185637

delta=.20
Tmax/E≈0.185067
```

Both remain comfortably above:

```math
\frac18
=
0.125.
```

Thirty-percent and thirty-five-percent gauge takeover windows also survived.

Thus:

```text
THICKER_REALIZATION_TARGET=
MUCH_LOWER_PEAK_STRESS

FIXED_CHARGE_CAPACITY=
ESSENTIALLY_PRESERVED

LOCAL_GAUGE_BUDGET=
PRESERVED
```

This promoted the thick source from a mere stress-relief trick to a serious field-realization target.

---

# 27. Simulation 016C — Global Electrostatic Integrability No-Go

The 008F local gauge stress:

```math
T_g
=
(g,0,g,0)
```

can be produced locally by a pair of orthogonal electrostatic gradients.

For two potentials $\Phi_1,\Phi_2$, exact matching requires:

```math
\sum_a E_{r,a}^2=g,
```

```math
\sum_a E_{z,a}^2=g,
```

and:

```math
\sum_a E_{r,a}E_{z,a}=0.
```

Thus their Jacobian satisfies:

```math
J^TJ=gI.
```

This means the map is locally conformal with scale $\sqrt g$.

A necessary integrability condition is:

```math
\left(
\partial_r^2+\partial_z^2
\right)\ln g
=
0
.
```

For the compact 006D collar:

```math
g(r,z)
\propto
\frac{
v(1-v)
}{r}
y^2(1-y)^2.
```

Then:

```math
\Delta\ln g
=
\frac1{r^2}
-
\frac1{\delta^2}
\left[
\frac1{v^2}
+
\frac1{(1-v)^2}
+
\frac2{y^2}
+
\frac2{(1-y)^2}
\right].
```

At:

```math
v=y=\frac12,
```

one obtains:

```math
\Delta\ln g
=
\frac1{r^2}
-
\frac{24}{\delta^2}
<
0
.
```

Therefore the harmonicity requirement fails.

Independent finite differences reproduced the result.

Decision:

```text
TWO_INDEPENDENT_STATIC_ELECTROSTATIC_U1_EXACT_GLOBAL_TARGET=
REJECTED
```

while:

```text
008F_LOCAL_DECOMPOSITION=
PRESERVED

006D=
NOT_INVALIDATED
```

This was the correct kind of negative result: a cheap analytical obstruction that prevented wasting effort on a doomed exact electrostatic solver.

---

# 28. Simulation 016D — Smooth Exponential Tail

016D tested whether the **compact boundary itself** was creating much of the gauge-realization difficulty.

Define:

```math
x
=
\frac{r-\beta}{\ell}
```

and:

```math
f(x)
=
\exp
\left[
-\frac{x^3}
{1+x^2}
\right].
```

Properties:

```math
f(0)=1,
```

```math
f'(0)=0,
```

```math
f''(0)=0,
```

and:

```math
f(x)\sim e^{-x}.
```

Use:

```math
q(r)
=
-\frac{\alpha^2}{r}
f
\left(
\frac{r-\beta}{\ell}
\right).
```

The conservation construction remains:

```math
p_r=\frac qr,
\qquad
p_\phi=q'.
```

Because:

```math
q(r)\rightarrow0
```

exponentially,

```math
\int r
(p_r+p_\phi)\,dr
=
[rq]_0^\infty
=
0.
```

Thus integrated stress balance survives.

The vertical compact polynomial was replaced by:

```math
\varphi(z)
=
\frac1{2w}
\mathrm{sech}^2
\left(
\frac{z-z_0}{w}
\right),
```

with:

```math
z_0=-\frac\delta2,
\qquad
w=\frac\delta4.
```

All tested cases retained:

```text
OUTWARD_FIELD=YES
TRACE_BALANCE=PASS
T/E>1/8
FINITE_ENERGY=YES
```

Standout:

```text
delta=.20
ell=.40
C≈29.47049
T/E≈0.17908
peak-stress relief≈1868x
```

At this point the exponential-tail candidate looked very strong.

016E then found its hidden asymptotic failure.

---

# 29. Simulation 016E — Gauge-Tail Asymptotic Gate

Let winding-field amplitude be $F(r)$ and gauge-covariant winding mismatch:

```math
k(r)
=
n-eA_\phi(r).
```

Angular stress:

```math
A(r)
=
\frac{
k^2F^2
}{r^2}.
```

Available radial gradient budget:

```math
G_r.
```

Because:

```math
F'^2\le G_r
```

and finite energy requires:

```math
F(\infty)=0,
```

we obtain the rigorous amplitude bound:

```math
F(r)
\le
I(r),
```

where:

```math
I(r)
=
\int_r^\infty
\sqrt{G_r(s)}
\,ds.
```

Therefore:

```math
|k(r)|
\ge
K_{\min}(r)
=
\frac{
r\sqrt{A(r)}
}{
I(r)
}
.
```

---

# 30. Why the Exponential Tail Failed

For the 016D exponential tail:

```math
f(r)\sim e^{-r/\ell}.
```

Asymptotically:

```math
G_r
\sim
{\mathrm{const}}
\frac{
e^{-r/\ell}
}{r}
```

and:

```math
A\sim2G_r.
```

The amplitude integral becomes:

```math
I(r)
\sim
2\ell
\sqrt{G_r}.
```

Thus:

```math
K_{\min}(r)
\sim
\frac r{\sqrt2\,\ell}
.
```

Hence:

```math
K_{\min}'(r)
\rightarrow
\frac1{\sqrt2\,\ell}.
```

For cylindrical gauge mismatch $k=n-eA_\phi$, the magnetic-energy asymptotic contains:

```math
\int
\frac{k'^2}{r}
\,dr.
```

With nonzero constant asymptotic $k'$:

```math
\int^\infty
\frac{dr}{r}
```

diverges logarithmically.

Therefore:

```text
EXPONENTIAL_TAIL_SINGLE_GAUGED_WINDING_FINITE_ENERGY_ASYMPTOTIC=
REJECTED
```

for the simplest exact gauged-winding realization.

This does not invalidate the stress-energy construction itself.

---

# 31. 016E Power-Law Tail Escape

Replace the exponential tail with:

```math
f_m(x)
=
(1+x^3)^{-m/3}.
```

This preserves:

```math
f_m(0)=1,
```

```math
f_m'(0)=0,
```

```math
f_m''(0)=0,
```

while:

```math
f_m(x)\sim x^{-m}.
```

The asymptotic gauge mismatch now tends to:

```math
K_\infty
=
\sqrt{
\frac{
m(m+1)
}{2}
}
.
```

Therefore it remains finite.

Examples:

```text
m=2 -> K∞=sqrt(3)≈1.73205
m=3 -> K∞=sqrt(6)≈2.44949
m=4 -> K∞=sqrt(10)≈3.16228
```

Preferred minimum-complexity candidate:

```text
delta=.20
ell=.40
m=2

C=
29.552822107488

Tmax/E=
0.177926001088

K∞=
1.732050807569

peak-stress relief≈
1874.913x
```

All tested power-law cases retained outward gravity and integrated stress balance.

Thus:

```text
POWER_LAW_C2_TAIL=
PROMOTED
```

kinematically.

This was not yet an Euler–Lagrange solution.

---

# 32. Simulation 016F — Simultaneous Charge/Winding Coexistence

016F exposed another hidden coupling.

The earlier charge and winding tests had effectively treated their available stress budgets independently.

But assigning temporal kinetic energy $D$ reduces the remaining spatial Gram budget.

After charge allocation:

```math
G_r
=
\epsilon+p_r-D
```

and:

```math
A
=
\epsilon+p_\phi-D.
```

For the inner winding turn-on:

```math
F(r)
\le
\int_{r_-}^{r}
\sqrt{G_r(s)}
\,ds.
```

Therefore:

```math
K_{\mathrm{inner}}(r)
=
\frac{
r\sqrt{A(r)}
}{
\displaystyle
\int_{r_-}^r
\sqrt{G_r(s)}
\,ds
}.
```

For the outer decay:

```math
K_{\mathrm{outer}}(r)
=
\frac{
r\sqrt{A(r)}
}{
\displaystyle
\int_r^\infty
\sqrt{G_r(s)}
\,ds
}.
```

Hence:

```math
K_{\mathrm{required}}
=
\max
\left(
K_{\mathrm{inner}},
K_{\mathrm{outer}}
\right).
```

---

# 33. 016F Hidden Narrow-Transition Problem

For the narrow realization inherited from the old source:

```text
W=.05
ell=.40
```

the combined charge/winding requirement became:

```text
K_REQUIRED≈130.61
```

and the conservative nonovershooting winding estimate was:

```text
n≈131.
```

This was much worse than the tail-only $K_\infty$ value suggested.

The actual bottleneck was therefore **the inner transition**, not the far tail.

---

# 34. 016F Transition Broadening Breakthrough

The inner transition half-width $W$ was freed from the old relation:

```math
W=\delta/4.
```

Increasing $W$ allowed the field amplitude to grow gradually over a much larger radial interval.

This reduced the required winding dramatically.

Preferred tested low-complexity point:

```text
W=
1.000000

ell=
0.600000

C=
40.749886771113

Tmax/E=
0.180278569163

target T/E=
0.140000000000

eta=
0.776575943831

Derrick curvature/E=
+0.360000

K_REQUIRED=
9.589406109611

conservative nonovershoot winding=
10

peak-stress relief vs fine 006D=
1400.489x
```

This was a major positive result.

The difficult gauge/winding requirement fell from approximately:

```text
131
```

to:

```text
10
```

at the cost of increasing $C$ from approximately:

```text
29.55
```

to:

```text
40.75.
```

The source still retained very large peak-stress relief.

Decision:

```text
FINITE_CHARGE_WINDING_COEXISTENCE_WINDOW=
YES_IN_TESTED_KINEMATIC_ALLOCATION

LOWER_COMPLEXITY_NONOVERSHOOT_TARGET=
FOUND
```

This was the strongest **kinematic** matter-realization preflight of the session.

It was still not a field solution.

---

# 35. Simulation 016G — Exact Asymptotic Euler–Lagrange No-Go

016G was deliberately performed before launching a large PDE solve.

It asked:

> **Can the exact 016E/016F power-law stress target satisfy the asymptotic Euler–Lagrange equation of the minimal asymptotically decoupled canonical winding field?**

The answer was:

```text
NO
```

under the stated assumptions.

The run compiled successfully, preserved the 94-test regression baseline, and independently verified its analytic coefficient using finite differences.

This proof should be preserved carefully.

---

# 36. Mathematical Proof of the 016G No-Go

For an $m$-power target tail:

```math
q(r)
\propto
-r^{-m-1}.
```

Asymptotically:

```math
p_r
\sim
-C_\infty r^{-m-2}
```

and:

```math
p_\phi
\sim
(m+1)
C_\infty r^{-m-2}.
```

Because:

```math
\epsilon=p_\phi
```

in the target tail, the available radial Gram before temporal allocation is:

```math
\epsilon+p_r
\sim
mC_\infty r^{-m-2}.
```

Allocate a fraction $\eta$ of that capacity to temporal charge:

```math
D
=
\eta mC_\infty r^{-m-2}.
```

Then remaining radial gradient capacity is:

```math
G_r
\sim
(1-\eta)
mC_\infty
r^{-m-2}
.
```

The required angular Gram becomes:

```math
A
\sim
\left[
2(m+1)
-
\eta m
\right]
C_\infty
r^{-m-2}
.
```

---

# 37. Slowest Possible Finite-Energy Winding Amplitude

Since:

```math
F'^2\le G_r
```

and:

```math
F(\infty)=0,
```

we have:

```math
F(r)
\le
\int_r^\infty
\sqrt{G_r(s)}
\,ds.
```

Because:

```math
\sqrt{G_r}
\propto
r^{-(m+2)/2},
```

the integral scales as:

```math
r^{-m/2}.
```

Therefore the **slowest allowed** finite-energy amplitude behaves as:

```math
F
\propto
r^{-s},
```

with:

```math
s=\frac m2
.
```

Any faster power-law decay has:

```math
s>\frac m2.
```

---

# 38. Minimum Required Asymptotic Winding

Angular matching requires:

```math
\frac{
k^2F^2
}{r^2}
=
A.
```

Using the maximum available amplitude gives the smallest possible $k$.

This yields:

```math
k_\infty^2
\ge
\frac{
m
\left[
2(m+1)-\eta m
\right]
}{
4(1-\eta)
}
.
```

Since:

```math
s^2
=
\frac{m^2}{4},
```

subtract:

```math
k_\infty^2-s^2
=
\frac{
m
\left[
2(m+1)-\eta m
\right]
}{
4(1-\eta)
}
-
\frac{m^2}{4}.
```

Put over common denominator:

```math
k_\infty^2-s^2
=
\frac{
m
\left[
2(m+1)-\eta m
-
m(1-\eta)
\right]
}{
4(1-\eta)
}.
```

The $\eta m$ terms cancel:

```math
2(m+1)-\eta m-m+\eta m
=
m+2.
```

Therefore:

```math
k_\infty^2-s^2
=
\frac{
m(m+2)
}{
4(1-\eta)
}
.
```

For:

```math
m>0
```

and:

```math
0\le\eta<1,
```

the numerator and denominator are positive.

Hence:

```math
k_\infty^2>s^2
.
```

This is not a numerical accident.

It is an exact asymptotic identity for the tested target class.

---

# 39. Euler–Lagrange Sign Conflict

For a gapless canonical winding amplitude in the asymptotic region:

```math
F''
+
\frac1rF'
-
\frac{k^2}{r^2}F
-
U_{\mathrm{eff}}'(F)
=
0.
```

For:

```math
F=Ar^{-s},
```

we have:

```math
F'
=
-sAr^{-s-1},
```

and:

```math
F''
=
s(s+1)Ar^{-s-2}.
```

Thus:

```math
F''
+
\frac1rF'
=
s^2Ar^{-s-2}
=
\frac{s^2}{r^2}F.
```

The E-L equation requires:

```math
U_{\mathrm{eff}}'(F)
=
\frac{
s^2-k^2
}{r^2}
F.
```

But 016G proved:

```math
k^2>s^2.
```

Therefore:

```math
U_{\mathrm{eff}}'(F)<0
```

for sufficiently small positive asymptotic $F$.

A regular asymptotically decoupled canonical scalar whose vacuum at $F=0$ is a stable local minimum requires the opposite restoring sign sufficiently near the vacuum.

Therefore the exact target is incompatible with that minimal field class.

---

# 40. Preferred $m=2$ Numerical Specialization

For 016F:

```text
m=2
eta≈0.77657594383
```

so:

```math
s=\frac m2=1.
```

The reconstructed asymptotic mismatch:

```text
k∞≈3.154613692967.
```

Therefore:

```text
k∞²-s²≈+8.951587551854
```

and:

```text
s²-k∞²≈-8.951587551854.
```

For $m=2$, the associated lowest matching local self-interaction is quartic.

The required effective quartic coefficient has the negative sign, while a standalone stable decoupled quartic vacuum needs the positive sign.

Independent finite-difference evaluation recovered approximately:

```text
-8.95158755
```

at radii:

```text
10
100
1000
10000
```

with relative errors around:

```text
1e-10–1e-9.
```

The 016G output confirms the analytic identity and finite-difference E-L check.

---

# 41. Charge Does Not Create the 016G Obstruction

At:

```text
eta=0
```

for $m=2$:

```text
K_INFINITY_NO_CHARGE=
1.732050807569

K²-S²=
2.0
```

So the obstruction already exists without the stabilizing charge.

Temporal charge makes it stronger but does not cause it.

Thus:

```text
TEMPORAL_CHARGE_CREATES_OBSTRUCTION=
NO

TEMPORAL_CHARGE_WORSENS_OBSTRUCTION=
YES
```

This matters strategically: removing the charged stabilizer alone cannot rescue the exact power-law target.

---

# 42. Faster Power-Law Decay Does Not Rescue It

For:

```math
s>\frac m2,
```

angular matching requires:

```math
k^2
\propto
r^{2s-m}.
```

Since:

```math
2s-m>0,
```

the required angular term grows relative to the radial Laplacian.

The 016G numerical controls showed increasingly negative E-L residuals at large radius.

Therefore faster amplitude decay does not repair the sign problem.

---

# 43. Correct Interpretation of 016G

016G does **not** prove:

```text
CANONICAL_FIELD_REALIZATION_OF_ANY_REPULSIVE_GR_SOURCE=
IMPOSSIBLE
```

It proves a narrower statement:

> **The exact 016E/016F power-law stress target is incompatible with the minimum asymptotically decoupled canonical winding scalar with a regular stable-vacuum self-potential, under the assumptions used in the derivation.**

Therefore:

```text
006D=
PRESERVED

016F_KINEMATIC_COEXISTENCE=
PRESERVED

EXACT_016F_MINIMAL_CANONICAL_FIELD_REALIZATION=
DEMOTED
```

Potential logical escapes include:

* relax exact stress matching;
* allow additional asymptotically coupled fields;
* use a justified larger field multiplet;
* use noncanonical or higher-derivative physics;
* use a different spatial architecture;
* allow an actual E-L solution to choose a nearby stress tensor that still produces outward gravity.

016H tested the most conservative of these:

```text
RELAX_EXACT_STRESS_MATCHING
```

and optimize actual fields instead.

---

# 44. Simulation 016H — Explicit Healthy Field-Model Gravity Gate

016H represented a major methodological shift:

> **Stop prescribing the desired $T_{\mu\nu}$ and ask whether an explicit local relativistic field model naturally generates outward gravity.**

Model:

```text
REAL SYMMETRY-BREAKING SCALAR X
+
COMPLEX FIELD Phi_plus WITH +n WINDING
+
COMPLEX FIELD Phi_minus WITH -n WINDING
```

The opposite windings cancel net:

```math
T_{t\phi}.
```

The potential was nonnegative.

The gauge field was omitted deliberately, making the sign test optimistic because ordinary electromagnetic field energy generally adds positive active gravitational source.

---

# 45. 016H Trial Fields

Real scalar:

```math
X
=
1
-
A
\exp
\left[
-\frac12
\left(
\frac{r^2}{R_X^2}
+
\frac{z^2}{Z_X^2}
\right)
\right].
```

Counter-winding fields:

```math
\Phi_\pm
=
Y(r,z)
e^{i(\omega t\pm n\phi)}.
```

Amplitude:

```math
Y
=
B
\left(
\frac r{R_Y}
\right)^n
\exp
\left[
-\frac12
\left(
\frac{r^2}{R_Y^2}
+
\frac{z^2}{Z_Y^2}
\right)
\right].
```

The factor $r^n$ enforces regularity on the axis.

Energy was minimized at fixed total Noether charge over independent radial and vertical widths.

This was more physically meaningful than fitting a prescribed stress tensor.

---

# 46. Crucial 016H Active-Source Identity

For this field normalization, the full combination:

```math
S
=
\rho+p_r+p_\phi+p_z
```

simplifies exactly to:

```math
S
=
8\omega^2Y^2
-
2V
.
```

All spatial-gradient pieces cancel from the active trace.

This identity exposes the competition directly:

```text
TEMPORAL CHARGE:
positive active gravitational source

SCALAR POTENTIAL / TENSION:
negative active gravitational source
```

Therefore the model genuinely possessed a mechanism capable of creating:

```math
S<0
```

locally.

The question was whether equilibrium spatially arranged that negative contribution in a way capable of producing an outward field.

---

# 47. 016H Gravitational Observable

On the symmetry axis:

```math
a_z(h)
\propto
-
\int
S(r,z)
\frac{h-z}
{
\left[
r^2+(h-z)^2
\right]^{3/2}
}
\,dV.
```

No 006D target stress was imposed.

The fields chose their own profiles through variational energy minimization.

This made 016H the cleanest observable-first canonical field test yet attempted in the project.

---

# 48. 016H Results

The repaired run compiled and completed successfully.

Number of promoted bound states:

```text
63
```

Internally consistent bound states:

```text
63
```

Result:

```text
NEGATIVE_ACTIVE_DENSITY_EXISTS=
True
```

but:

```text
ANY_NEAR_FIELD_OUTWARD_ACCELERATION=
False

ANY_CLEAN_EXTERIOR_OUTWARD_ACCELERATION=
False
```

Largest negative active fraction:

```text
0.266601491354
```

or approximately:

```text
26.66%.
```

Yet even that was not enough to reverse the gravitational field.

The best exterior case still had:

```text
A_KERNEL≈-0.77021758
```

where negative means inward under the run's convention.

Independent quadratures:

```text
ORDER=64
ORDER=96
ORDER=128
```

all retained the same attractive sign.

At high order:

```text
ACTIVE_MASS/E≈0.9999999953

PRESSURE_TRACE/E≈-4.66e-9

EXTERIOR_MAX_A≈-0.7702175795
```

The run explicitly concluded:

```text
EXPLICIT_CANONICAL_FIELD_VARIATIONAL_EXTERIOR_REPULSION=
NOT_FOUND_IN_TESTED_SCAN

EXPLICIT_CANONICAL_FIELD_VARIATIONAL_NEAR_FIELD_REPULSION=
NOT_FOUND_IN_TESTED_SCAN

NEGATIVE_ACTIVE_DENSITY_WITHOUT_REPULSIVE_FIELD=
True
```

The complete output preserves the 63 bound states and independent force-sign check.

---

# 49. The Deepest New Physical Lesson — Spatial Moment, Not Just Negative Density

006D and 016H together identify what may be the most important design principle found in the project so far.

The target acceleration is:

```math
a_z(h)
=
-\frac{G}{c^2}
\int
S(\mathbf{x})
K_h(\mathbf{x})
\,dV,
```

with:

```math
K_h>0.
```

To have outward near-field acceleration:

```math
\int
S K_h
\,dV
<
0
.
```

At the same time, to retain positive far-field mass:

```math
\int S\,dV>0
.
```

These conditions can coexist only if the signs of $S$ are **spatially segregated**.

A useful abstract decomposition is:

```math
S
=
S_-+S_+
```

where:

```math
S_-\le0,
\qquad
S_+\ge0.
```

Positive far-field mass requires:

```math
\int S_+\,dV
>
\left|
\int S_-\,dV
\right|.
```

But near-field outward gravity requires:

```math
\int K_h S_+\,dV
<
\left|
\int K_h S_-\,dV
\right|.
```

These can both be true if the negative active source is concentrated where $K_h$ is large and the positive compensation is moved where $K_h$ is small.

Because approximately:

```math
K_h
\sim
\frac{h-z}
{
\left[
r^2+(h-z)^2
\right]^{3/2}
},
```

the kernel is strongest near the target-facing central region and weaker at large radius.

This is exactly what 006D does:

```text
INNER CORE:
negative active tension
high gravitational kernel

TRANSFER REGION / OUTER COLLAR:
positive compensating energy/stress
lower gravitational kernel
```

016H, by contrast, used largely co-spatial centered Gaussian fields.

It generated negative $S$ but failed to establish the required spatial moment.

Therefore the correct next field-model question is no longer:

> Can a field theory produce negative active density?

016H answered:

```text
YES
```

The question is:

> **Can a field theory naturally segregate negative active stress toward the high-kernel region and compensating positive energy toward a lower-kernel support/rim while remaining a genuine stable solution?**

That is the active established-GR frontier.

---

# 50. Current Best Model After 016H

There are now three different meanings of "best model," and they must remain separate.

## Strongest established gravitational construction

```text
006D
```

Why:

* explicit finite source;
* positive energy;
* NEC/WEC/DEC;
* linearized local conservation;
* outward near field;
* positive far-field active mass;
* independently reproducible.

## Strongest positive matter-realization preflight

```text
016F
```

Specifically:

```text
W=1
ell=.6
m=2
n≈10
C≈40.75
Tmax/E≈.1803
peak-stress relief≈1400x
```

But 016G proved the **exact** power-law target cannot be the minimal decoupled canonical winding solution.

Thus 016F is a design/kinematic guide, not a current exact matter candidate.

## Strongest explicit healthy field-model test

```text
016H
```

Result:

```text
NEGATIVE
```

Generic centered FLS-like equilibrium did not repel despite large negative active-density regions.

Therefore the strongest actual positive model remains 006D.

---

# 51. Current Practical-Antigravity Heuristic

Current informal progress ruler:

```text
~44%
```

This is **not a probability**.

It means roughly:

```text
SIGN POSSIBILITY:
SOLVED

EXPLICIT POSITIVE-ENERGY REPULSIVE STRESS CONSTRUCTION:
SOLVED

FINITE / NONSINGULAR LINEARIZED SOURCE:
SOLVED

POINTWISE ENERGY CONDITIONS:
SOLVED

LINEARIZED LOCAL CONSERVATION:
SOLVED

ONE-MODE CHARGE STABILITY CAPACITY:
SOLVED AS CAPACITY

SMOOTH FIELD-LIKE REALIZATION PREFLIGHT:
SUBSTANTIAL PROGRESS

ACTUAL FIELD EQUATIONS:
NOT SOLVED

FULL STABILITY:
NOT SOLVED

NONLINEAR EINSTEIN-MATTER:
NOT SOLVED

FINITE PAYLOAD:
NOT SOLVED

PRACTICAL ENERGY:
NOT SOLVED

EXPERIMENT:
NOT SOLVED

DEVICE:
NOT SOLVED
```

The estimate rose during 016A–F because physical realization became much less obviously impossible.

It was reduced after 016G/H because two of the simplest actual canonical realization routes were then closed.

This is scientific progress despite the lower heuristic because the uncertainty has been reduced substantially.

---

# 52. Dominant Remaining Barriers

There are five distinct barriers, and they should not be attacked out of order.

## Barrier 1 — actual field realization

Need a local relativistic matter model whose own equations produce the correct spatial stress moment.

## Barrier 2 — dynamic stability

Need full perturbation stability, not one Derrick direction.

## Barrier 3 — nonlinear gravity

Need self-consistent Einstein-matter solution or a rigorous demonstration that weak-field treatment remains adequate for the realized matter configuration.

## Barrier 4 — finite payload

Need center-of-mass acceleration of a finite payload.

## Barrier 5 — practical energy scaling

Need to beat many orders of magnitude beyond any order-unity improvement in $C$.

Barrier 5 is likely the hardest path to an actual device.

---

# 53. Highest-Value Next Path A — Spatially Separated Drum-Vorton Architecture

This should probably be the first established-GR investigation next session after documentation and reranking.

Concept:

```text
CENTRAL DRUM / MEMBRANE:
domain-wall-like scalar sector
large negative pressure/tension
localized beneath payload
high Green-kernel leverage

OUTER RIM:
charged/counter-winding/gauged soliton
provides radial support and stability
stores positive compensation at larger radius
lower Green-kernel leverage
```

This architecture directly embodies the 006D spatial design principle.

Unlike 016H, the negative potential/tension and charge/current support should **not be forced to share the same center and widths**.

Potential field content:

```text
SECTOR X:
real symmetry-breaking scalar forming drum/wall

SECTOR Q:
nonwinding stationary complex scalar carrying charge

SECTOR W:
counter-winding complex pair concentrated near rim

GAUGE SECTOR:
U(1) field concentrated primarily in rim
```

The counter-winding pair should maintain:

```math
T_{t\phi}\approx0.
```

---

# 54. First Gate for Path A

Do **not** begin immediately with a large nonlinear PDE solve.

The cheapest next calculation should be a flexible finite-dimensional **ring-plus-drum variational ansatz**.

Allow independent:

```text
drum radius
drum thickness
drum vertical position
rim radius
rim width
rim vertical position
charge amplitude
winding amplitude
wall amplitude
gauge mismatch proxy
```

Optimize the actual field-model energy while monitoring:

```math
a_z
```

directly.

The objective should **not** be:

```text
MINIMIZE_DISTANCE_TO_006D_T_MUNU
```

The objective should be:

```text
FIND_STATIONARY_OR_NEAR_STATIONARY_BOUND_CONFIGURATION
+
OUTWARD_GRAVITATIONAL_FIELD
```

subject to health constraints.

Pass criteria:

```text
FINITE_TOTAL_ENERGY=YES

LOCALIZED_FIELDS=YES

BOUND_STATE=YES

ENERGY_VARIATIONAL_STATIONARITY=YES

T_TPHI≈0

POSITIVE_TOTAL_ACTIVE_MASS=YES

NEGATIVE_ACTIVE_REGION=YES

WEIGHTED_ACTIVE_MOMENT_OUTWARD=YES

INDEPENDENT_FORCE_QUADRATURE=PASS
```

If no outward case appears after a sufficiently flexible separated ansatz, stop the generic canonical 006D-realization branch rather than escalating blindly.

---

# 55. Path A — Second Gate

Only after a positive variational case:

```text
FULL_2D_EULER_LAGRANGE_BOUNDARY_VALUE_SOLVE
```

Solve actual coupled field equations.

Need separate convergence in:

```text
radial resolution
vertical resolution
domain size
boundary location
initial guess
continuation parameter
```

Do not trust one solver branch.

Required outputs:

```text
PDE_RESIDUAL
TOTAL_ENERGY
NOETHER_CHARGE
GAUGE_CHARGE
NET_ANGULAR_MOMENTUM
T_TPHI
PRESSURE_TRACE
ACTIVE_SOURCE
OUTWARD_FIELD
BOUNDARY_DECAY
```

---

# 56. Path A — Third Gate: Stability

If a genuine field solution exists:

1. radial/dilation stability;
2. axial perturbations;
3. azimuthal perturbations;
4. charge-transfer modes;
5. gauge modes;
6. winding/vortex splitting;
7. wall-rim relative displacement;
8. collapse/expansion modes.

Need solve a linearized eigenvalue problem.

Pass only if no unacceptable growing mode exists in the operational configuration.

---

# 57. Path A — Fourth Gate: Nonlinear Einstein-Matter

Once field realization and stability are established, solve:

```math
G_{\mu\nu}
=
\frac{8\pi G}{c^4}
T_{\mu\nu}[\Psi].
```

Need verify:

```math
\nabla_\mu T^{\mu\nu}=0
```

automatically through matter equations and Bianchi identity.

Check:

```text
metric regularity
horizon formation
compactness
proper acceleration
geodesic response
curvature invariants
asymptotic mass
```

If compactness remains at the old $10^{-15}$-type scale, nonlinear corrections may be tiny, but that must be demonstrated for the realized source rather than assumed.

---

# 58. Path A — Fifth Gate: Finite Payload

This is mandatory.

For payload density $\rho_P(\mathbf{x})$:

```math
\mathbf{a}_{\mathrm{CM}}
=
\frac{
\int
\rho_P(\mathbf{x})
\mathbf{a}(\mathbf{x})\,dV
}{
\int
\rho_P(\mathbf{x})\,dV
}.
```

Need:

```text
POINT_ACCELERATION>0
```

and:

```text
FINITE_PAYLOAD_CM_ACCELERATION>0.
```

015C proved these are not interchangeable.

Also account for:

```text
source reaction
supports
ground coupling
field momentum
energy flow
```

so the result is not accidentally interpreted as reactionless propulsion.

---

# 59. Path A — Sixth Gate: Energy Scaling

Even if all previous gates pass, pure GR still faces:

```math
M
\sim
C\frac{ah^2}{G}.
```

Order-unity changes in $C$ cannot bridge the practicality gap.

For a human-scale lift area, simple tiling gives:

```math
\frac EA
\sim
\frac{Cac^2}
{\pi x_{\max}^2G}.
```

The stand-off length cancels.

Therefore a pure-GR route can reach a practical device only if something qualitatively different is discovered, such as:

* geometric leverage that avoids simple area tiling;
* a field geometry with far better kernel leverage than current 006D class;
* a coherent distributed source interacting with the entire payload without cell-by-cell coverage;
* externally supplied/gravitationally amplified stress;
* some physically allowed mechanism changing effective coupling strength.

Without such a change, pure GR may top out at a beautiful theoretical demonstration rather than an engineering device.

---

# 60. Highest-Value Next Path B — Reopen 014D Disformal Branch Selectively

This is the most mature non-GR sign-reversal branch.

Strengths:

```text
LOCAL_TOTAL_FORCE_REVERSAL=
YES

2D_REFINEMENT=
YES

INDEPENDENT_3D=
YES

TIMESTEP_HALVING=
YES

METRIC_HEALTH_MARGIN=
POSITIVE
```

Weaknesses:

```text
ORDINARY_MATTER_BRIDGE=
FAILED_IN_SIMPLE_CONSTANT_B_MODEL

FINITE_PAYLOAD_REVERSAL=
NOT_FOUND

FULL_THEORY_REALIZATION=
NOT_ESTABLISHED
```

If reopened, do **not** rerun 014D.

The next high-value controls are already identified.

---

# 61. Path B — Original 014D Geometry + Finite Payload

015C changed both the source geometry and the observable.

Therefore perform:

```text
ORIGINAL_VALIDATED_014D_SOURCE
+
FINITE_PASSIVE_PAYLOAD_INTEGRATION
```

This distinguishes:

```text
PAYLOAD_AVERAGING_FAILURE
```

from:

```text
LOCALIZATION_GEOMETRY_FAILURE.
```

If original 014D geometry cannot produce finite-body reversal, the branch weakens considerably.

---

# 62. Path B — Dynamic-Time Payload Search

015C primarily tested root-time configurations.

014D is explicitly non-static.

Therefore a rigorous next test would search:

```math
a_{\mathrm{CM}}(t)
```

through the full controlled time evolution.

Need distinguish:

```text
transient force reversal

net impulse

periodic zero-average response

sustained outward force.
```

The operational quantity is not merely instantaneous force but possibly:

```math
\Delta v
=
\int a_{\mathrm{CM}}(t)\,dt.
```

A time-dependent local reversal with zero integrated impulse is not a practical lift mechanism.

---

# 63. Path B — Ordinary-Matter Coupling Stop Rule

Any disformal route must overcome:

```math
\Delta\ln B
\gtrsim132.49
```

for the simple environment-dependent rescue.

Do not accept arbitrary $B(\phi)$ functions merely because they can be written.

Require:

```text
EFT_CONTROL=YES

NO_GHOST_OR_GRADIENT_INSTABILITY=YES

RADIATIVE_STABILITY=YES

STANDARD_MODEL_BOUNDS=PASS

DISFORMAL_METRIC_INVERTIBLE=YES

USEFUL_FINITE_PAYLOAD_FORCE=YES
```

If no natural mechanism can generate the necessary environmental hierarchy, close the ordinary-matter disformal route.

---

# 64. Highest-Value Next Path C — Protected Material-Specific Scalar Force

This branch remains attractive for one reason:

> It can change the interaction scale rather than attempting to generate ordinary gravitational acceleration using $G$ alone.

The low-energy branch previously produced an explicit material-specific bound-composite response, but the required relativistic microscopic origin is unresolved.

The current real question is not whether one can write the desired NR operator.

That has already been demonstrated parametrically.

The decisive question is:

> **Can a technically natural local relativistic theory generate the required bound-state-specific two-body scalar response without producing forbidden one-body scalar charge or destabilizing the ultralight mediator?**

The existing buildplan still points toward this protected relativistic operator/mixing problem, but that plan now predates the 016A–H results and should be reranked before execution. The buildplan itself emphasizes that branch ranking should compare theory confidence, feasibility gap, speculative assumptions, experimental constraints, and information gain.

Possible microscopic protection mechanisms worth testing only if clearly motivated:

```text
NONTRIVIAL_PAIR_REPRESENTATION

EMERGENT_COMPOSITE_SELECTION_RULE

PARTNER_CANCELLATION

DERIVATIVE_OR_TOPOLOGICAL_COUPLING

NONPERTURBATIVE_PROTECTION
```

But each must explicitly survive loop-induced one-body mixing.

---

# 65. Why Path C Matters for the 100% Goal

Pure GR contains the factor:

```math
G
```

and therefore the catastrophic scale:

```math
\frac{a}{G}.
```

A new but allowed fifth-force coupling could be vastly stronger than gravity.

Therefore even though Path C is more speculative theoretically, it has much greater potential to solve the **practical energy** problem.

The central tradeoff is:

```text
PATH A / PURE GR:
high theoretical confidence
terrible energy scaling

PATH C / NEW FORCE:
lower theoretical confidence
potentially useful interaction strength
```

This is why both should remain in the global reranking.

---

# 66. A Possible Path D — Hybrid Architecture

A longer-term possibility is that 006D supplies the **geometry principle** while a new interaction supplies the **strength**.

The important thing learned from 006D may not be its literal stress-energy tensor.

It may be the spatial design rule:

```text
REPULSIVE CONTRIBUTION:
close to target

COMPENSATING ATTRACTIVE / POSITIVE CONTRIBUTION:
farther away
```

A short-range scalar/vector/disformal interaction could potentially exploit an analogous weighted-moment architecture more cheaply.

This is speculative and should only be pursued after A/B/C reranking.

---

# 67. Global Route From ~44% to "100%"

Again, these percentages are not probabilities.

They are a milestone ruler.

## ~44% — Current position

Established:

* gravity can point outward locally;
* positive energy is compatible with this;
* finite conserved source exists in linearized GR;
* NEC/WEC/DEC can all hold;
* field-realization requirements are much better understood;
* several minimal matter realizations have been falsified.

---

## ~44% → ~55% — Actual matter-field realization

Required breakthrough:

> An explicit healthy local field theory admits a localized stationary solution whose self-generated stress tensor produces an outward operational gravitational field.

Best current candidate:

```text
SPATIALLY_SEPARATED_DRUM_PLUS_RIM / VORTON
```

Need actual E-L solution or an exceptionally strong converged preflight.

This would be a major milestone.

---

## ~55% → ~65% — Full dynamical stability

Need demonstrate:

```text
NO_DERRICK_INSTABILITY
NO_RADIAL_INSTABILITY
NO_VERTICAL_INSTABILITY
NO_AZIMUTHAL_INSTABILITY
NO_VORTEX_SPLITTING
NO_CHARGE_RUNAWAY
NO_GAUGE_INSTABILITY
```

One-mode fixed-charge capacity is insufficient.

---

## ~65% → ~72% — Nonlinear Einstein-Matter Consistency

Need:

```text
SELF_CONSISTENT_METRIC
REGULAR_GEOMETRY
FULL_CURVED_CONSERVATION
OUTWARD_OPERATIONAL_FIELD
POSITIVE_ASYMPTOTIC_MASS_OR_CORRECT_EXTERNAL_BOOKKEEPING
```

---

## ~72% → ~80% — Finite Payload

Need:

```text
FINITE_PAYLOAD_CM_LIFT=
YES
```

with proper energy/momentum bookkeeping.

This is where many local-force mechanisms may fail.

---

## ~80% → ~90% — Practical Scaling Breakthrough

This is probably the hardest jump.

Need remove many orders of magnitude of energetic burden.

Pure order-unity coefficient optimization cannot do it.

One of the following must occur:

```text
NEW_GEOMETRIC_LEVERAGE

NONLOCAL_OR_COLLECTIVE_PAYLOAD_COUPLING

MUCH_STRONGER_ALLOWED_INTERACTION

EXTERNAL_BACKGROUND_COUPLING

OTHER_PHYSICALLY_JUSTIFIED_SCALING_CHANGE
```

If none exists, practical antigravity may be impossible even though local GR repulsion is mathematically real.

---

## ~90% → ~96% — Experimental-Accessibility Gate

Need a physically buildable prediction with:

```text
KNOWN MATERIALS OR SYNTHESIZABLE FIELDS

FINITE CONTROL ENERGY

FINITE HEAT LOAD

FINITE ELECTRIC/MAGNETIC FIELDS

SHIELDING UNDERSTOOD

ENVIRONMENTAL COUPLING UNDERSTOOD

CURRENT FIFTH_FORCE / EP / COLLIDER / ASTROPHYSICAL CONSTRAINTS PASSED

SIGNAL ABOVE SYSTEMATIC BACKGROUND
```

---

## ~96% → 100% — Independent Device Demonstration

"100%" should mean something extremely demanding:

```text
REPEATABLE
CONTROLLABLE
STABLE
INDEPENDENTLY_REPLICATED
FINITE-PAYLOAD
USEFUL-MAGNITUDE
UPWARD / REPULSIVE ACCELERATION
COMPLETE ENERGY-MOMENTUM ACCOUNTING
NO CONVENTIONAL FORCE EXPLANATION
```

Only then should the project use language equivalent to:

```text
PRACTICAL_ANTIGRAVITY=
ESTABLISHED
```

There is no presently known guaranteed path to 100%.

The steps above are the gates a successful path would have to cross.

---

# 68. Recommended Global Reranking Next Session

After documentation is updated, rank these three active classes:

| Rank candidate                                | Theory confidence | Current positive evidence                        | Dominant blocker                                 |
| --------------------------------------------- | ----------------- | ------------------------------------------------ | ------------------------------------------------ |
| 006D-inspired spatially separated drum-vorton | Highest           | 006D theorem + 016A–F design progress            | Actual E-L solution and catastrophic $G$ scaling |
| 014D disformal finite-payload continuation    | Medium/low        | Numerically converged local total-force reversal | Ordinary-matter coupling + finite-payload lift   |
| Protected material-specific scalar force      | Low/speculative   | Low-energy parametric survivor                   | Technically natural relativistic UV completion   |

The ranking should explicitly score:

```text
THEORY_CONFIDENCE
CURRENT_CONSTRAINTS
NUMBER_OF_SPECULATIVE_ASSUMPTIONS
FINITE_PAYLOAD_PROSPECT
ENERGY_SCALING
NEXT_CALCULATION_INFORMATION_GAIN
```

My current expectation is:

```text
FIRST SCIENTIFIC NEXT STEP:
DRUM_VORTON_VARIATIONAL_GATE

FIRST PRACTICAL-SCALING ALTERNATIVE:
PROTECTED_SCALAR_UV_COMPLETION

DISFORMAL:
KEEP AS THIRD CONTENDER UNTIL FINITE_PAYLOAD CONTROL
```

But this should be formalized in the updated buildplan rather than treated as irreversible.

---

# 69. Strong Stop Rules Going Forward

## Do not return to coefficient shaving

Do not spend substantial time changing:

```text
C=23.4
```

to:

```text
C=20
```

or:

```text
C=15
```

unless a physical matter model makes that change meaningful.

The practicality gap is many orders of magnitude.

---

## Do not fit exact 006D stress again without a reason

016G demonstrated the danger of overconstraining matter to an engineered tensor.

Future field models should optimize the **observable**:

```math
a_z
```

rather than exact tensor residual, unless exact matching is analytically motivated.

---

## Do not repeat generic centered FLS/Q-ball scans

016H already demonstrated:

```text
NEGATIVE_ACTIVE_DENSITY=
YES

REPULSIVE_FIELD=
NO
```

across 63 bound internally consistent configurations.

A new FLS-like calculation is justified only if it introduces the new ingredient:

```text
SPATIAL_SEPARATION
```

or another physically meaningful structural difference.

---

## Do not equate local negative $S$ with antigravity

016H explicitly falsified that inference.

The real observable is the kernel-weighted integral.

---

## Do not equate point lift with payload lift

015C explicitly falsified that inference in another branch.

---

## Do not assume stability from $T/E>1/8$

That protects only the chosen Derrick scaling mode.

---

## Do not assume low compactness means practical

Low compactness only says nonlinear gravitational collapse is not the immediate problem.

The raw energy remains catastrophic.

---

## Do not call 016G a universal scalar no-go theorem

Its scope is the stated exact target and minimal asymptotically decoupled canonical winding assumptions.

---

## Do not call 016H a theorem against FLS models

It is a finite-dimensional variational scan.

It strongly deprioritizes the generic co-spatial architecture but does not exclude every possible FLS-like PDE solution.

---

# 70. What Should Be Preserved in Documentation

This session is important enough to justify a dedicated journal entry.

Recommended journal filename:

```text
journal/2026-08-29_016a_016h_006d_realizability_and_canonical_field_gates.md
```

The journal should include:

1. 016A thickness/stress tradeoff;
2. macroscopic area-energy cancellation;
3. 016B fixed-charge/gauge survival;
4. 016C electrostatic conformal-integrability no-go;
5. 016D exponential-tail construction;
6. 016E exponential gauge-energy failure and power-law replacement;
7. 016F charge/winding coexistence and $n\sim10$ target;
8. full 016G asymptotic E-L proof;
9. 016H explicit FLS-like field model;
10. 63-state negative result;
11. independent force-sign convergence;
12. new spatial-segregation principle;
13. new reranking.

The project documentation standard requires GitHub mathematics to remain:

```text
$...$
```

for inline math and fenced:

````text
```math
...
```
````

for display math. Existing project documentation also emphasizes distinct roles for README, buildplan, claims, and chronological notes.

---

# 71. Required README Update

The README headline should **not** be replaced.

Keep:

> **We have a mathematical construction for antigravity-like gravitational repulsion.**

But update the frontier beneath it.

The current README/buildplan still describes older speculative branches as the current frontier and predates 016A–H.

The new README should explain succinctly:

```text
006D remains strongest established positive result.

016A–F made a much more field-friendly realization target.

016G proved the exact minimal canonical power-law target fails its
asymptotic Euler-Lagrange equation.

016H tested an explicit healthy FLS-like field model and found substantial
negative active density but no outward near or exterior gravitational field.

Therefore the current established-GR realization frontier is spatial
segregation of a central tension/drum sector from an outer stabilizing
charge/current/gauge rim.
```

---

# 72. Required RESEARCH_BUILDPLAN Update

The current active-task section is stale relative to this session.

Do not simply resume the old:

```text
PROTECTED_RELATIVISTIC_TWO_BODY_OPERATOR_MIXING_GATE
```

without reranking it against 016A–H.

New high-level buildplan should probably become:

```text
ACTIVE_FRONTIER=
GLOBAL_RERANK_POST_016H

PRIMARY_QUESTION=
WHICH_SURVIVING_ROUTE_HAS_THE_HIGHEST_INFORMATION_GAIN_TOWARD_A_PHYSICAL_FINITE_PAYLOAD_LOW_ENERGY_ANTIGRAVITY_MECHANISM

CONTENDER_A=
SPATIALLY_SEPARATED_006D_INSPIRED_DRUM_VORTON_FIELD_MODEL

CONTENDER_B=
014D_DISFORMAL_DYNAMIC_FINITE_PAYLOAD

CONTENDER_C=
PROTECTED_BOUND_STATE_SCALAR_RELATIVISTIC_UV_COMPLETION
```

Then choose one active task only.

---

# 73. Suggested Immediate Buildplan After Reranking

If established-GR continuity wins:

```text
ACTIVE_TASK=
016I_SPATIALLY_SEPARATED_DRUM_VORTON_VARIATIONAL_GRAVITY_GATE
```

Scientific question:

> Can an explicit healthy local canonical field model with a central wall/tension sector and spatially separated outer charge/current support naturally generate a negative kernel-weighted active gravitational moment while retaining positive total mass and approximate stationary balance?

Primary observable:

```math
a_z(h).
```

Stop rule:

```text
IF_NO_OUTWARD_CASE_AFTER_FLEXIBLE_SEPARATED_VARIATIONAL_SEARCH:
DEPRIORITIZE_GENERIC_CANONICAL_006D_MATTER_REALIZATION
```

Do not escalate to full PDE unless that preflight is green.

---

# 74. First Actions Next Session

Perform in this order.

## Step 1 — inspect repository state

Run:

```bash
git status --short
```

Do not assume the current working tree from memory.

The last explicit status showed many untracked 014–016 scripts and logs plus modified `NOTES.MD`.

016H was subsequently added and generated a repaired log.

---

## Step 2 — verify tests

Run:

```bash
ROOT="$(pwd)"
PY="$ROOT/.venv/bin/python"

PYTHONPATH="$ROOT/src" \
"$PY" -m pytest -q tests/known_solutions
```

Expected baseline if unchanged:

```text
94 passed
```

But verify rather than assume.

---

## Step 3 — documentation before new science

Finish:

```text
journal 016A–H
NOTES.md
RESEARCH_BUILDPLAN.md
README.md
CLAIMS.md if present/current
```

Ensure the 016G proof is preserved exactly.

---

## Step 4 — checkpoint scientific evidence

Preserve the logs:

```text
016a
016b clean/current log
016c
016d
016e
016f
016g
016h repaired
```

Do not accidentally treat the first duplicate/failed logs as the canonical successful run.

---

## Step 5 — formal rerank

Score:

```text
A drum-vorton
B disformal finite payload
C protected scalar UV
```

and select one.

---

## Step 6 — only then begin the next experiment

Do not reopen several branches simultaneously.

---

# 75. Repository State at the End of the Slice

Latest known working tree before the final additions included:

```text
M NOTES.MD

?? journal/2026-08-29_014b_015c_disformal_force_reversal_and_practicality_gates.md

?? results/logs/015a_practical_path_20260829-131608.log
?? results/logs/015c_finite_payload_20260829-132639.log
?? results/logs/015c_finite_payload_repaired_20260829-132812.log

?? results/logs/016a_006d_practicality_20260829-135143.log
?? results/logs/016b_006d_thick_charge_gauge_20260829-135613.log
?? results/logs/016b_006d_thick_charge_gauge_20260829-135747.log
?? results/logs/016c_006d_global_gauge_integrability_20260829-140234.log
?? results/logs/016d_006d_exponential_tail_20260829-140903.log
?? results/logs/016e_006d_two_sector_gauge_tail_20260829-142241.log
?? results/logs/016f_006d_charge_winding_20260829-143455.log
?? results/logs/016g_006d_asymptotic_euler_lagrange_20260829-144318.log

?? simulations/014b_disformal_repulsion_prerequisite.py
?? simulations/014c_decisive_disformal_force.py
?? simulations/014d_disformal_total_reversal.py
?? simulations/014e_baryonic_disformal_bridge.py
?? simulations/015a_practical_path_protected_pair_portal_gate.py
?? simulations/015c_disformal_finite_payload_global_force.py
?? simulations/016a_006d_practicality_optimized_thickness.py
?? simulations/016b_006d_thick_charge_gauge_capacity.py
?? simulations/016c_006d_global_gauge_integrability.py
?? simulations/016d_006d_exponential_tail_realizability.py
?? simulations/016e_006d_two_sector_gauge_tail_preflight.py
?? simulations/016f_006d_charge_winding_coexistence.py
?? simulations/016g_006d_asymptotic_euler_lagrange_gate.py
```

After that status, the following were also created:

```text
simulations/016h_explicit_canonical_field_gravity_gate.py
```

and:

```text
results/logs/016h_explicit_canonical_field_gravity_repaired_20260829-145700.log
```

The first 016H attempt failed only because of a Python syntax typo:

```text
)**1.5
```

being split across statements.

The one-line repair compiled successfully and the scientific run completed with:

```text
RUN_RC=0.
```

The next session must rerun `git status --short` rather than assuming this list remains exact.

---

# 76. Canonical Successful Logs

When cleaning documentation references, prefer:

```text
016b_006d_thick_charge_gauge_20260829-135747.log
```

over the earlier duplicate 016B log.

Use:

```text
016h_explicit_canonical_field_gravity_repaired_20260829-145700.log
```

as the canonical successful 016H scientific run.

Do not delete earlier logs unless deliberately cleaning history.

They provide useful debugging provenance.

---

# 77. Current Claims Ledger

```text
CLAIM:
GENERAL_RELATIVITY_PERMITS_LOCAL_GRAVITATIONAL_REPULSION
STATUS:
ESTABLISHED / KNOWN PHYSICS

CLAIM:
FINITE_POSITIVE_ENERGY_LINEARIZED_GR_REPULSIVE_SOURCE_EXISTS
STATUS:
PROJECT_DERIVED_CONSTRUCTIVE_RESULT

CLAIM:
006D_LOCAL_CONSERVATION
STATUS:
ANALYTIC_AT_LINEARIZED_BACKGROUND_ORDER

CLAIM:
006D_NEC_WEC_DEC
STATUS:
ANALYTIC / NUMERICALLY_AUDITED

CLAIM:
006D_OUTWARD_NEAR_FIELD
STATUS:
NUMERICALLY_REPRODUCED

CLAIM:
006D_POSITIVE_FAR_FIELD_ACTIVE_MASS
STATUS:
ANALYTIC_PLUS_NUMERICAL_AUDIT

CLAIM:
006D_EXACT_NONLINEAR_EINSTEIN_SOLUTION
STATUS:
NOT_ESTABLISHED

CLAIM:
006D_DYNAMIC_STABILITY
STATUS:
NOT_ESTABLISHED

CLAIM:
FIXED_CHARGE_DERRICK_CAPACITY_EXISTS
STATUS:
PROJECT_DERIVED_PREFLIGHT

CLAIM:
GLOBAL_SMOOTH_EXACT_ELECTROSTATIC_008F_REALIZATION
STATUS:
REJECTED_FOR_TESTED_SIMPLE_CLASS

CLAIM:
016D_EXPONENTIAL_TAIL_MINIMAL_GAUGED_WINDING_REALIZATION
STATUS:
REJECTED_ASYMPTOTICALLY

CLAIM:
016E_POWER_LAW_TAIL_FINITE_GAUGE_ENERGY_PREFLIGHT
STATUS:
GREEN_KINEMATICALLY

CLAIM:
016F_CHARGE_WINDING_COEXISTENCE_WINDOW
STATUS:
GREEN_KINEMATICALLY

CLAIM:
016F_EXACT_MINIMAL_CANONICAL_FIELD_REALIZATION
STATUS:
DEMOTED_BY_016G

CLAIM:
016G_MINIMAL_DECOUPLED_CANONICAL_EXACT_POWER_LAW_TARGET
STATUS:
REJECTED_BY_ASYMPTOTIC_EULER_LAGRANGE_SIGN_CONFLICT

CLAIM:
GENERIC_016H_COUNTERWINDING_FLS_LIKE_VARIATIONAL_REPULSION
STATUS:
NOT_FOUND_IN_63_BOUND_TESTED_CASES

CLAIM:
NEGATIVE_ACTIVE_DENSITY_IS_SUFFICIENT_FOR_LOCAL_REPULSION
STATUS:
FALSE_AS_GENERAL_INFERENCE

CLAIM:
SPATIAL_WEIGHTING_OF_ACTIVE_STRESS_IS_CRITICAL
STATUS:
STRONGLY_SUPPORTED_BY_006D_VS_016H_COMPARISON

CLAIM:
PURE_GR_MICROSTANDOFF_ALONE_SOLVES_MACROSCOPIC_ENERGY
STATUS:
NO

CLAIM:
PRACTICAL_ANTIGRAVITY_DEVICE
STATUS:
NO

CLAIM:
REACTIONLESS_PROPULSION
STATUS:
NO

CLAIM:
NEW_PHYSICS_DISCOVERY
STATUS:
NO

CLAIM:
NOVELTY_OF_PROJECT_DERIVED_MATHEMATICS
STATUS:
NOT_ESTABLISHED_PENDING_INDEPENDENT_LITERATURE_COMPARISON
```

---

# 78. Most Important Equations to Carry Into the Next Session

## Active weak-field source

```math
S
=
\epsilon+p_r+p_\phi+p_z.
```

## Axisymmetric target acceleration

```math
a_z(h)
=
-\frac{2\pi G}{c^2}
\int dz
\int dr\,
rS
\frac{h-z}
{
[r^2+(h-z)^2]^{3/2}
}.
```

## 006D conservation generator

```math
q=rp_r,
\qquad
p_\phi=q'.
```

## Local conservation identity

```math
\frac{dp_r}{dr}
+
\frac{p_r-p_\phi}{r}
=
0.
```

## Positive-energy choice

```math
\epsilon
=
\max
(|p_r|,|p_\phi|).
```

## Laue stress cancellation

```math
\int r(p_r+p_\phi)\,dr
=
[rq]_0^\infty.
```

## Source scaling

```math
M
=
C\frac{ah^2}{G}.
```

## Coverage-energy scaling

```math
\frac EA
=
\frac{Cac^2}
{\pi x_{\max}^2G}.
```

## Fixed-charge stability condition

```math
\frac TE>\frac18.
```

## Gauge/winding amplitude bound

```math
|k(r)|
\ge
\frac{
r\sqrt A
}{
\int_r^\infty\sqrt{G_r}\,ds
}.
```

## 016G asymptotic identity

```math
k_\infty^2-s^2
=
\frac{
m(m+2)
}{
4(1-\eta)
}
>0
.
```

## 016H explicit field active-source identity

```math
S
=
8\omega^2Y^2
-
2V
.
```

## New spatial-moment requirement

```math
\int S\,dV>0
\quad\text{while}\quad
\int S K_h\,dV<0
.
```

This final pair may be the most important design equation for the next established-GR slice.

---

# 79. Highest-Value Conceptual Insight to Preserve

The project began by asking:

> Can positive-energy gravity point outward at all?

006D answered:

```text
YES.
```

The next question became:

> Can known or reasonable fields generate negative active gravitational density?

016H demonstrated:

```text
YES.
```

But 016H simultaneously showed:

```text
NEGATIVE_ACTIVE_DENSITY
DOES_NOT_IMPLY
OUTWARD_GRAVITY.
```

The frontier is therefore now more precise:

> **Can physically realizable fields generate the correct spatial multipole/moment of active stress—negative where gravitational leverage is high, positive where leverage is low—while remaining stable and conserving energy-momentum?**

That is a materially better-defined scientific problem than the project had at the start of the session.

---

# 80. Recommended One-Sentence Carry-Forward

If only one sentence survives into the next session, preserve this:

> **ANTIGRAVITY_RESEARCH still has its strongest established positive result in 006D—a finite positive-energy, NEC/WEC/DEC-compatible, locally conserved static linearized-GR source with outward near gravity and positive far-field mass—but 016A–016H showed that physical realization requires not merely negative active stress but a highly specific spatial segregation of tension and compensating positive support; the simplest exact canonical winding target and generic co-spatial FLS-like field realization have now been rejected, making a spatially separated drum-plus-vorton field architecture, reranked against the surviving disformal and protected-scalar routes, the highest-value next frontier.**

---

# 81. Session Closeout Classification

```text
STRONGEST_ESTABLISHED_RESULT=
006D_FINITE_POSITIVE_ENERGY_LINEARIZED_GR_LOCAL_REPULSION

STRONGEST_POSITIVE_REALIZABILITY_PREFLIGHT=
016F_SPATIALLY_SMOOTH_CHARGE_WINDING_COEXISTENCE

016F_EXACT_MINIMAL_CANONICAL_REALIZATION=
DEMOTED_BY_016G

016G_ASYMPTOTIC_CANONICAL_NO_GO=
ESTABLISHED_UNDER_STATED_ASSUMPTIONS

016H_EXPLICIT_HEALTHY_FIELD_REPULSION=
NOT_FOUND_IN_TESTED_VARIATIONAL_SCAN

NEW_MAJOR_DESIGN_PRINCIPLE=
SPATIALLY_SEGREGATE_NEGATIVE_ACTIVE_STRESS_FROM_POSITIVE_SUPPORT_BY_GREEN_FUNCTION_LEVERAGE

PURE_GR_MACROSCOPIC_ENERGY_BARRIER=
UNCHANGED

FINITE_PAYLOAD_REPULSION=
NOT_ESTABLISHED

PRACTICAL_ANTIGRAVITY=
NO

INFORMAL_PROJECT_PROGRESS_HEURISTIC=
~44_PERCENT

NEXT=
DOCUMENT_016A_THROUGH_016H
THEN_GLOBAL_RERANK
THEN_PROBABLY_016I_SPATIALLY_SEPARATED_DRUM_VORTON_PREFLIGHT
```

---

# 82. Final Scientific Assessment

This session should be regarded as a successful research slice even though its final runs were negative.

At the start of the renewed 006D investigation, we knew that an engineered positive-energy stress tensor could repel in linearized GR, but we did not know whether its severe thinness, boundary behavior, gauge support, charge requirement, or scalar representation made it obviously unrealizable.

By the end of the slice:

* source thickness was increased by orders of magnitude in practical feature size while retaining most gravitational efficiency;
* peak stresses were reduced by up to roughly three orders of magnitude;
* the fixed-charge stabilization margin survived;
* the first global electrostatic realization was analytically rejected;
* smooth tails removed the sharp-boundary problem;
* the apparently attractive exponential tail was then correctly rejected by a deeper gauge-energy asymptotic test;
* a power-law replacement survived that test;
* simultaneous charge and winding were shown to have a finite kinematic coexistence window;
* the required winding burden was reduced by over an order of magnitude through spatial redesign;
* a clean asymptotic Euler–Lagrange proof then showed why exact tensor matching still fails in the minimum canonical model;
* an explicit healthy field model was allowed to determine its own stress tensor;
* that model generated substantial negative active density but nevertheless remained attractive;
* this isolated **spatial stress organization** as the next decisive physical variable.

That is meaningful progress.

The project has not moved closer to a device merely by accumulating models. It has instead eliminated several plausible but incorrect shortcuts and reduced the problem to a sharper physical design criterion.

That is exactly the research behavior the project should continue.


### END NOTE - AUGUST 29 2026 - 15:10 CST

### BEGIN NOTE - AUGUST 29 2026 - DUAL NOTES FORMAT POLICY

# ANTIGRAVITY_RESEARCH — Monolithic Notes and Chronology Policy

## Purpose

The project intentionally maintains the research history in two complementary forms.

`NOTES.MD` remains the complete long-running monolithic research record.

`notes/chronology/` contains the same research history divided into smaller chronological Markdown files.

Both forms are intentional and should be preserved.

## Why the monolithic notes remain important

The monolithic `NOTES.MD` file is especially useful for project continuity.

It provides one file containing the accumulated research history, mathematical results, failed branches, decision gates, implementation context, and carry-forward instructions.

This makes it convenient to provide the complete project history to a new ChatGPT or other AI-assisted research session without uploading many separate chronology files.

It is also useful for whole-project searching, archival continuity, and human review of the research as one continuous record.

Therefore:

NOTES.MD must not be replaced by a small index or discarded merely because it is large.

## Why the smaller chronology also remains important

The monolithic notes have grown to approximately tens of thousands of lines and contain more than one thousand mathematical display expressions.

During the August 29, 2026 documentation audit, otherwise valid mathematics was observed to render successfully when placed in the smaller chronology files while the same mathematics could fail with GitHub's `Unable to render expression` message inside the very large monolithic document.

The live-math syntax was separately audited and repaired.

This provides strong evidence that at least some remaining failures in the monolithic page are caused by GitHub rendering scale or complexity rather than malformed equations.

The chronology files therefore provide the preferred GitHub-readable representation of the research history.

For mathematical reading on GitHub:

`notes/chronology/` is preferred.

For single-file project handoff, archival continuity, and AI-session context:

`NOTES.MD` is preferred.

## August 29, 2026 documentation repair

The previous monolithic notes were split into chronological slices so that the mathematical record could be inspected and rendered in smaller documents.

The split was verified by reconstructing the chronology and confirming byte-for-byte equality with the repaired monolithic research history before the monolithic form was restored.

A repository-wide live-math audit was also performed.

The audit removed or normalized known GitHub-sensitive live-math constructs while preserving the intended scientific content and numerical values.

The README was then updated to explain the distinction between the two note representations and to direct GitHub readers toward `notes/chronology/` when reliable mathematical rendering is required.

## Going-forward workflow

Every substantial new carry-forward research note should be preserved in both representations.

The preferred workflow is:

1. Write each new research handoff as a self-contained chronological note.
2. Store that note as the next numbered file under `notes/chronology/`.
3. Append the same note content to the end of `NOTES.MD`.
4. Preserve chronological order in both representations.
5. Run the Markdown live-math audit before closeout when the note contains substantial mathematics.
6. Run `git diff --check` before committing.
7. Do not silently rewrite valid mathematics merely because the giant monolithic GitHub page fails to render it.
8. When an equation fails in `NOTES.MD`, first check whether the identical expression renders correctly in its smaller chronology file.
9. If the smaller file renders correctly and the live-math audit is clean, treat large-document rendering exhaustion as the leading explanation rather than changing scientifically correct mathematics.
10. Never delete historical research merely to reduce the size of the monolithic handoff file.

## Synchronization rule

The scientific content of a chronological note and its corresponding monolithic entry should remain identical.

The two representations serve different operational purposes, not different scientific purposes.

Changes to an old research note that alter scientific meaning should therefore be made deliberately and propagated to both representations.

Pure navigation material may differ where necessary, but the actual research record should not drift.

## Authority and interpretation

The two notes representations are historical and carry-forward records.

They do not supersede the project's authority hierarchy.

The active scientific frontier, branch ranking, decision gates, and stop rules remain governed by `RESEARCH_BUILDPLAN.md`.

Durable completed proofs, falsifications, and major research slices remain preserved in `journal/`.

The README remains the concise public-facing project state.

The codebundle remains the authoritative representation of current source code, tests, simulations, and implementation state.

## Permanent policy summary

MONOLITHIC_NOTES=

PRESERVE

MONOLITHIC_NOTES_PURPOSE=

SINGLE_FILE_HISTORY_AND_AI_SESSION_HANDOFF

CHRONOLOGY_NOTES=

PRESERVE

CHRONOLOGY_NOTES_PURPOSE=

GITHUB_READING_AND_RELIABLE_MATH_RENDERING

NEW_CARRY_FORWARD_NOTES=

ADD_TO_BOTH_FORMS

SCIENTIFIC_CONTENT_BETWEEN_FORMS=

KEEP_SYNCHRONIZED

VALID_MATH_FAILING_ONLY_IN_GIANT_MONOLITH=

CHECK_SMALL_CHRONOLOGY_VERSION_BEFORE_REWRITING

ACTIVE_FRONTIER_AUTHORITY=

RESEARCH_BUILDPLAN.md

DURABLE_COMPLETED_RESULT_AUTHORITY=

journal/

### END NOTE - AUGUST 29 2026 - DUAL NOTES FORMAT POLICY

