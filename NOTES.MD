### BEGIN NOTE - AUGUST 27 2026 - 01:00 CST

# ANTIGRAVITY_RESEARCH — Comprehensive Carry-Forward Notes

This is the right place to stop adding patches and consolidate what we actually know.

The project has advanced far enough that the problem is now much more sharply defined than when we started. We have **not discovered a new law of physics or a practical antigravity device**, but we have established something important and useful:

```math
\boxed{\text{General relativity absolutely permits local gravitational repulsion.}}
```

More specifically, we have reproduced several known GR mechanisms and constructed a finite linearized-GR model in which **positive energy, positive total mass, and classical energy conditions coexist with a locally repulsive gravitational field**. What has emerged as the dominant obstacle is no longer the **sign** of gravity. It is the **stress-energy cost and physical realizability** of the source.

Simulation 006A then sharpened that further: within its stated assumptions, the optimistic static energy cost scales as

```math
\boxed{M_{\rm equiv}\sim\frac{a h^2}{G}}
```

where $a$ is the desired repulsive acceleration and $h$ is the source-to-target scale. Your optimizer independently reproduced the coefficient 1.0 exactly, while the explicit finite disk/rim architecture costs 79.753 times more. 

That gap—**1 versus 79.753**—is now one of the most important open mathematical questions in the project.

---

# 1. Current scientific conclusion

The simplest useful description of everything we have learned is:

```math
\boxed{\text{gravity responds to stress-energy, not merely mass density}}
```

and therefore sufficiently large **negative pressure/tension** can make the local active gravitational source negative even when the actual energy density remains positive.

For type-I matter in its local rest frame,

```math
T^\mu{}_\nu
\sim
{\rm diag}(\epsilon,p_x,p_y,p_z)
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
\boxed{67\text{ tests}}
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
r_s\simeq1.1139\ {\rm Mpc}
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
\boxed{w<-\frac13}
```

The especially interesting $w=-1$ case preserved classical NEC/WEC/DEC while violating SEC.

For $1g$ of relative acceleration across one meter:

```math
\epsilon
\simeq
1.5763\times10^{27}\ {\rm J/m^3}
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
f_{\rm in}(R)=f_{\rm out}(R)
```

but

```math
f'_{\rm in}(R)\ne f'_{\rm out}(R)
```

Specifically we found the derivative ratio:

```math
\frac{f'_{\rm in}}{f'_{\rm out}}=-2
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
M_{\rm ADM}<0
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
-\frac12M_v\lesssim M_{\rm ADM}<0
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
r_{\rm rep}
=
\frac{Q^2}
{4\pi\epsilon_0Mc^2}
```

Define

```math
z=\frac{r_{\rm rep}}{R}
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

For the $1g$, $1\,{\rm m}$ benchmark:

```math
E_{\rm surface}
\simeq
2.67\times10^{19}\ {\rm V/m}
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
\boxed{q=\frac12}
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
\boxed{
\frac12<q\le1
}
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
2.1017\times10^{27}\ {\rm J/m^2}
```

Equivalent surface mass:

```math
2.3385\times10^{10}\ {\rm kg/m^2}
```

The toy $\phi^4$ mapping produced

```math
v\simeq81.5\ {\rm GeV}
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
\boxed{\text{repulsive near field}}
```

while still having:

```math
\boxed{\text{ordinary attractive far field}}
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
\boxed{
M_{\rm disk}
\simeq
79.753148
\frac{ah^2}{G}.
}
```

At $1g$ one meter away:

```math
M\simeq1.172\times10^{13}\ {\rm kg}
```

```math
E\simeq1.053\times10^{30}\ {\rm J}
```

At $10^{-6}g$, one centimeter away:

```math
M\simeq1.172\times10^3\ {\rm kg}
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
\boxed{
1
<
79.753
}
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
\boxed{
M_{\rm static}
\approx
\frac{ah^2}{G}.
}
```

### $1g$

At $h=1\,{\rm m}$:

```math
M_{\min}
=
1.4693\times10^{11}\ {\rm kg}
```

```math
E_{\min}
=
1.3206\times10^{28}\ {\rm J}
```

At $h=1\,{\rm cm}$:

```math
M_{\min}
=
1.4693\times10^7\ {\rm kg}
```

At $h=1\,{\rm mm}$:

```math
M_{\min}
=
1.4693\times10^5\ {\rm kg}
```

At $h=1\,\mu{\rm m}$:

```math
M_{\min}
=
0.1469\ {\rm kg}
```

but still:

```math
E_{\min}
=
1.3206\times10^{16}\ {\rm J}
```

At $h=1\,{\rm nm}$:

```math
M_{\min}
=
1.4693\times10^{-7}\ {\rm kg}
```

with

```math
E_{\min}
\sim1.32\times10^{10}\ {\rm J}
```

The extremely important scaling is:

```math
\boxed{M,E\propto h^2}
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
z_{\rm zero}/R\simeq0.393320
```

```math
M\simeq79.753\,ah^2/G
```

This appears internally consistent in our linearized model.

It needs independent analytical derivation and ideally an independent implementation.

### Abstract static DEC+Laue LP optimum

We obtained:

```math
C_{\rm optimum}=1
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
\boxed{
1
\le C_{\rm real}
\le79.753
}
```

where

```math
M=C_{\rm real}\frac{ah^2}{G}
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
a_z(\text{target})\ge a_{\rm requested}
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
T_{\mu\nu}(\mathbf x)
```

Numerically integrate the linearized Einstein Green function.

Compare the resulting axial acceleration against:

```text
dimensionless_axis_factor()
```

for many $q,z/R$.

Specifically reproduce:

```math
z_{\rm zero}/R
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
a_{\rm Casimir}
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
\boxed{
\textbf{How close can an actual finite, locally conserved DEC source get to }
M=\frac{ah^2}{G}\textbf{?}
}
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
\boxed{
\textbf{Antigravity in GR is fundamentally a stress-engineering problem.}
}
```

The source should not be thought of as “negative mass.”

The more useful target is:

```math
\boxed{
\text{positive energy with relativistically negative principal pressure/tension}
}
```

placed near the target while compensating positive stresses are arranged so that the complete isolated system remains physically consistent.

And 006A has now made the next research objective extraordinarily clear:

```math
\boxed{
\textbf{Find the minimum-energy spatial realization of that stress tensor.}
}
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