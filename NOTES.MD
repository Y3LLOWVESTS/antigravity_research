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
