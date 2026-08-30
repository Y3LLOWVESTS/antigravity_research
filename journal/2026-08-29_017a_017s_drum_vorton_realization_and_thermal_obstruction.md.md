# Research Journal — 2026-08-29

## Post-016H Drum-Vorton Realization Program: Finite-Payload Repulsion, Nonaxisymmetric Stability, Gauged-Vorton Field-EOS Bridge, Robust Physical-EM Worldsheet Basin, and Thermal-Gravity Obstruction

## Objective

The primary scientific question of this research slice was:

> **Can the spatially separated drum/rim architecture suggested by 006D and 016H be promoted from an engineered stress-energy construction toward a physically motivated field realization that preserves finite-payload outward gravity, stability, positive far-field mass, and useful energy efficiency?**

The research deliberately separated several levels of accomplishment:

```text
MATHEMATICAL_STRESS_ARCHITECTURE

EFFECTIVE_MECHANICAL_REALIZATION

FIELD_EOS_REALIZATION

MICROSCOPIC_ORIGIN_OF_STRING_AND_MEMBRANE

ROBUST_PARAMETER_BASIN

FULL_FINITE_THICKNESS_EULER_LAGRANGE_SOLUTION

FULL_DYNAMICAL_STABILITY

NONLINEAR_EINSTEIN_MATTER_REALIZATION

PRACTICAL_DEVICE
```

The strongest established project result entering this slice remained 006D:

> **Within static linearized general relativity, an explicit finite, nonsingular, positive-energy, locally conserved NEC/WEC/DEC-compatible stress-energy configuration can produce a locally outward gravitational near field while retaining positive far-field active mass.**

The best tested finite 006D coefficient remained

```math
C_{006D}
=
23.591586299249
```

in

```math
M
=
C\frac{ah^2}{G}
```

The post-016H frontier was not the sign of gravity. It was whether a physically motivated matter system could naturally produce the required **spatial active-stress segregation** while remaining stable and energetically finite.

The strongest positive result of this journaled slice is the 017P field-EOS bridge and the 017R robust physical-electromagnetic worldsheet basin.

The strongest new negative result is 017S:

> **For the literal localized thermally stabilized O(4) drum-vorton implementation tested in 017Q/017R, even the minimum equilibrium photon bath required by the thermal description produces positive active gravity that overwhelms the defect's outward field throughout the entire tested robust basin.**

The final active frontier is therefore:

```text
NONTHERMAL_GAUGED_VORTON_RIM
+
TOPOLOGY_CONSISTENT_MICROSCOPIC_WALL_SECTOR
```

not the literal localized thermal O(4) implementation.

This journal does **not** establish:

* a complete finite-thickness drum-vorton field solution;
* full nonlinear stability of a wall-loaded vorton;
* a self-consistent Einstein-matter solution;
* payload backreaction;
* experimental accessibility;
* practical absolute energy requirements;
* a practical antigravity device;
* a new-physics discovery.

---

## Starting State

### 1. Result carried forward from 016H

016H tested an explicit positive-energy counter-winding FLS-like variational field family.

It found substantial negative active density but no outward near or clean-exterior gravitational field.

The central lesson was that negative active density by itself is insufficient.

Let

```math
S
=
\rho+p_r+p_\phi+p_z
```

be the static linearized active source and

```math
K_h(r,z)
=
\frac{h-z}
{\left[r^2+(h-z)^2\right]^{3/2}}
```

be the positive on-axis Green-function kernel.

Positive far-field active mass requires

```math
\int S\,dV
>
0
```

while local outward acceleration requires

```math
\int S K_h\,dV
<
0
```

The two can coexist only if the negative and positive active components have different spatial leverage.

This produced the central design rule:

```text
HIGH_KERNEL_REGION:
CONCENTRATE NEGATIVE ACTIVE STRESS

LOW_KERNEL_REGION:
MOVE POSITIVE SUPPORT / CHARGE / CURRENT ENERGY OUTWARD
```

### 2. Project progress ladder

The buildplan separates the following milestones:

```text
~50–55%:
robust operational finite-payload architecture

~55–65%:
actual healthy full Euler-Lagrange field solution

~65–72%:
meaningful dynamical stability

~72–80%:
self-consistent nonlinear Einstein-matter continuation

~80–90%:
qualitative practical scaling breakthrough
```

These percentages are project-management milestones, **not probabilities that practical antigravity exists**.

The buildplan also explicitly warns:

```text
DO_NOT_RAISE_PROGRESS_HEURISTIC_FROM_PARAMETER_OPTIMIZATION_ALONE
```

### 3. Regression baseline

All major runs in this slice began from the known-solution baseline

```text
94 passed
```

and the reported 017P, 017Q, 017R, and 017S runs all completed with

```text
TEST_RC=0
RUN_RC=0
```

---

# Work Performed

## 1. 017A–017C — spatial-leverage preflight and effective drum-vorton architecture

The early part of the post-016H program translated the spatial-segregation principle into a finite-payload design problem.

### 017A — kernel-leverage requirement

017A quantified the fact that positive total active mass and negative kernel-weighted active moment can coexist only when the negative active source is systematically closer to the payload, or otherwise better coupled to the relevant Green-function kernel, than the compensating positive source.

The governing inequalities were

```math
\int S\,dV
>
0
```

and

```math
\int S K_P\,dV
<
0
```

where $K_P$ denotes the payload-averaged kernel for a finite test body.

This gate established a quantitative spatial-leverage target before further field complexity was introduced.

### 017B — separated canonical variational family

A flexible spatially separated canonical variational ansatz was tested.

The tested family became attractive or physically unhealthy before producing a useful realization of the target effect.

This negative result discouraged simply adding more centered/canonical profiles and motivated a more structured support architecture.

### 017C — effective drum-vorton

017C combined:

```text
CENTRAL NEGATIVE-ACTIVE MEMBRANE / DRUM
+
CURRENT-SUPPORTED OUTER RIM
```

and found a finite-payload outward-acceleration region in the effective model.

The circular effective energy had the form

```math
E(R)
=
\pi\sigma R^2
+
2\pi\mu R
+
\frac{J}{2\pi R}
```

which is equivalently

```math
E
=
\sigma A
+
\mu L
+
\frac{J}{L}
```

for

```math
A=\pi R^2
```

and

```math
L=2\pi R
```

The circular solution had positive radial curvature at equilibrium.

The point-target coefficient at the best zero-bare-string limit reproduced the historical disk/rim value

```math
C
\approx
79.753148116012
```

and the finite-payload effective coefficient remained of order $10^2$.

This was a major operational improvement over 016H because finite-payload outward acceleration was now explicit.

But 017C tested only radial/effective stability.

It did **not** establish nonaxisymmetric stability or a microscopic matter realization.

---

## 2. Parallel global reranking before 017O

The project also used several gates to determine whether a different branch should outrank the established-GR drum/rim program.

These results are preserved here because they explain why the project returned to the vorton architecture.

### 017H–017J — disformal transient reversal versus full-cycle impulse

The dynamic disformal branch produced a reproducible transient finite-payload reversal and positive transient impulse, but the complete validated history remained net inward.

A representative 017J control result was

```text
I_NEWTON=
-1.053520266008e-02

I_FIFTH=
-5.243363164794e-03

I_TOTAL=
-1.577856582487e-02

I_HEALTH_B_ORACLE_FIFTH=
+2.085977197514e-03

REQUIRED_POSITIVE_FIFTH_AMPLIFICATION=
5.546392485660

REQUIRED_FACTOR_BEYOND_HEALTH_ORACLE=
5.050487930853
```

The resulting decision was

```text
SIMPLE_PHASE_SELECTIVE_SCREENING_AND_HEALTH_CONSTRAINED_B_MODULATION
CANNOT_CLOSE_FULL_HISTORY_IMPULSE_ON_VALIDATED_TRAJECTORY
```

The branch remained logically open only to more complicated cyclic source/reset and full variable-$B$ dynamics.

### 017K–017M — gold-null vector UV gates

The phenomenological gold-null vector direction was progressively tested against simple UV realizations.

The minimal single-scale completion required major collider/multiscale loopholes.

The explicit two-stage singlet vector-like-quark completion then failed the combined CKM and scale-separation gate.

Representative 017M companion-mass ceilings were

```text
0.1g perturbative sqrt(4pi):
37.861708500112 GeV

0.1g extreme 4pi:
134.216262065770 GeV

1g perturbative:
11.972923496571 GeV

1g extreme 4pi:
42.442908716189 GeV
```

The minimal practical vector completion was therefore closed as a priority route, while highly tuned/nonminimal vector models remained logically possible but low priority.

### 017N — axion-photon topological actuator upper bound

017N tested an extremely favorable direct topological actuator using the model-independent energy inequality

```math
\left|
\int \mathbf E\cdot\mathbf B\,dV
\right|
\le
U_{\rm EM}
```

and a massless mediator to maximize range/force.

At the CAST-scale coupling, the best-case energy requirements included approximately

```text
1 kg, 0.1g, 1 cm:
5.453800382333e11 J per device

1 kg, 0.1g, 1 m:
5.453800382333e13 J per device

1000 kg, 1g, 1 m:
5.453800382333e15 J per device
```

The direct axion-photon actuator was strongly demoted.

This global rerank left the established-GR separated drum/vorton route as the strongest next theoretical target.

---

## 3. 017O — nonaxisymmetric stability theorem for the bare effective drum

017O tested the hidden stability question left open by 017C.

The result was analytically clean and numerically reconstructed.

### 3.1 Bare effective energy

Take

```math
E
=
\sigma A
+
\mu L
+
\frac{J}{L}
```

For a circular loop of radius $R$,

```math
A_0
=
\pi R^2
```

and

```math
L_0
=
2\pi R
```

The radial equilibrium condition is

```math
\frac{dE}{dR}
=
0
```

which gives

```math
J
=
4\pi^2R^2
\left(
\sigma R+\mu
\right)
```

### 3.2 Nonaxisymmetric perturbation

Perturb the boundary by

```math
r(\phi)
=
R
\left[
1+\epsilon\cos(m\phi)
\right]
```

for integer

```math
m\ge2
```

The enclosed area is

```math
A
=
\frac12
\int_0^{2\pi}
r^2\,d\phi
```

and expands to

```math
A
=
\pi R^2
\left(
1+\frac{\epsilon^2}{2}
\right)
+
O(\epsilon^3)
```

The perimeter is

```math
L
=
\int_0^{2\pi}
\sqrt{
r^2
+
\left(
\frac{dr}{d\phi}
\right)^2
}
\,d\phi
```

and expands to

```math
L
=
2\pi R
\left(
1+\frac{m^2\epsilon^2}{4}
\right)
+
O(\epsilon^3)
```

Substituting the expansions into $E$ and imposing the circular radial equilibrium relation gives

```math
\boxed{
\Delta E_m
=
-\frac{\pi\sigma R^2}{2}
\left(
m^2-1
\right)
\epsilon^2
+
O(\epsilon^3)
}
```

Therefore

```math
\Delta E_m<0
```

for every

```math
m\ge2
```

in this minimal effective extension.

Thus the bare 017C circular drum is nonaxisymmetrically unstable.

This result does **not** imply that all vortons are unstable.

Published gauged field-theory vortons are known to possess stable regimes.

The result applies to the specific minimal mechanical energy used by 017C.

### 3.3 Curvature-rigidity rescue

Introduce

```math
E_B
=
\frac{B}{2}
\oint \kappa^2 ds
```

and define

```math
b
=
\frac{B}{\sigma R^3}
```

For the perturbed circle,

```math
\oint \kappa^2 ds
=
\frac{2\pi}{R}
+
\frac{\pi}{R}
\left(
m^4
-\frac52m^2
+1
\right)
\epsilon^2
+
O(\epsilon^3)
```

After imposing the $B$-corrected circular radial equilibrium relation, the quadratic mode energy becomes

```math
\boxed{
\Delta E_m
=
\frac{\pi\sigma R^2}{2}
\left(
m^2-1
\right)
\left[
b
\left(
m^2-1
\right)
-1
\right]
\epsilon^2
}
```

Therefore mode $m$ is stabilized when

```math
b
>
\frac{1}{m^2-1}
```

The controlling mode is $m=2$:

```math
\boxed{
b_{\rm crit}
=
\frac13
}
```

017O numerically verified that $b=0.32$ does not stabilize the complete tested spectrum while $b=0.34$ does.

### 3.4 Thin-core rigidity penalty

For the favorable scaling estimate

```math
B
\sim
\kappa_B\mu\delta^2
```

with

```math
q
=
\frac{\delta}{R}
```

and

```math
\eta
=
\frac{\mu}{\sigma R}
```

one has

```math
b
\sim
\kappa_B\eta q^2
```

so $m=2$ stability requires

```math
\eta
\gtrsim
\frac{1}{3\kappa_Bq^2}
```

For

```text
q=0.1
kappa_B=1
```

this implies

```text
eta≈33.333
```

The inherited favorable gravity estimate then gave approximately

```text
C_min≈2.2326e6

penalty vs bare 017C≈2.80e4

penalty orders≈4.45
```

Thus simple phenomenological thin-core bending can repair shape stability only at severe inherited gravitational-energy cost.

### 3.5 017O decision

```text
BARE_017C_EFFECTIVE_DRUM_NONAXIAL_STABILITY=
FAIL

CURVATURE_RIGIDITY_CAN_STABILIZE_QUADRATIC_SHAPE_MODES=
YES

SIMPLE_THIN_CORE_RIGIDITY_RESCUE=
ENERGETICALLY_SEVERE
```

The correct response was not to abandon vortons generally.

It was to replace the mechanical rim by a field-theoretic vorton whose own equation of state and internal degrees of freedom can supply stability.

---

## 4. 017P — literature-backed gauged-vorton field-EOS bridge

017P replaced the invented mechanical rim equation of state by a superconducting-string equation of state obtained from the published gauged-vorton field equations studied by Battye, Cotterill, and Pearson.

### 4.1 Field model

The working field theory was

```math
\mathcal L
=
(D_\mu\phi)^*D^\mu\phi
+
\partial_\mu\sigma^*\partial^\mu\sigma
-
\frac14F_{\mu\nu}F^{\mu\nu}
-
V(\phi,\sigma)
```

with

```math
V
=
\frac{\lambda_\phi}{4}
\left(
|\phi|^2-\eta_\phi^2
\right)^2
+
\frac{\lambda_\sigma}{4}
\left(
|\sigma|^2-\eta_\sigma^2
\right)^2
+
\beta|\phi|^2|\sigma|^2
```

The straight-string ansatz used unit vortex winding in $\phi$ and a charged/current-carrying condensate in $\sigma$.

Define

```math
\chi
=
\omega^2-k^2
```

The BVP solved the coupled radial Euler-Lagrange equations for the vortex amplitude, condensate amplitude, and azimuthal gauge potential.

### 4.2 Integrated string quantities

Define

```math
\Sigma_n
=
2\pi
\int_0^\infty
\rho |\sigma|^n\,d\rho
```

and

```math
A_{\rm string}
=
\mu
-
\frac{\lambda_\sigma}{4}
\Sigma_4
```

The fixed-charge thin-string energy is

```math
E
=
A_{\rm string}L
+
\frac{2Q^2}
{\Sigma_2L}
```

The independently checked variational identity is

```math
\frac{dA_{\rm string}}{d\chi}
=
-\Sigma_2
```

### 4.3 Published set-B reconstruction

The run first reconstructed the published set-B vorton benchmark.

Numerical result:

```text
SET_B_PREDICTED_Q_OVER_N=
32.561171477037

SET_B_PUBLISHED_Q_OVER_N=
31.880000000000

RELERR=
2.136673390956e-02

SET_B_PREDICTED_RADIUS_N50=
57.542051037500

SET_B_PUBLISHED_RADIUS=
56.600000000000

RELERR=
1.664401126324e-02

SET_B_LOWER_CHARGE_BRANCH_SELECTED=
True

SET_B_PUBLISHED_VORTON_RECONSTRUCTION=
PASS
```

This was a nontrivial literature normalization check before using the field solver for the antigravity architecture.

### 4.4 Set-G domain convergence

At $\chi=0.004$, increasing the radial domain from 40 to 60 changed the main integrated quantities only at approximately the $3\times10^{-7}$ relative level:

```text
SIGMA2_REL_CHANGE=
3.419064763459e-07

A_REL_CHANGE=
3.179045615615e-07

Q_REL_CHANGE=
3.421836584529e-07

SET_G_DOMAIN_CONVERGENCE=
PASS
```

The variational identity satisfied

```text
MAX_RELERR_DA_DCHI_PLUS_SIGMA2=
3.548959375252e-08

STRAIGHT_STRING_VARIATIONAL_IDENTITY=
PASS
```

### 4.5 Stability band

The thin-string characteristic speeds were computed as

```math
c_T^2
=
\frac{1}
{1+2\chi\Sigma_2/A_{\rm string}}
```

and

```math
c_L^2
=
\frac{1}
{1+2\chi\Sigma_2'/\Sigma_2}
```

The published cubic extrinsic-mode stability test was evaluated for

```text
m=2,...,40
```

using both the analytic cubic discriminant and a direct polynomial-root reality check.

The robust neighboring-point stable interval was

```text
ROBUST_STABLE_CHI_MIN=
0.00150000

ROBUST_STABLE_CHI_MAX=
0.00475000
```

The selected point was

```text
CHI=
0.004750000000

PHASE_RATIO=
0.990000000000

CT2=
0.9990018050154

CL2=
0.9930155006037

MIN_M2_TO_M40_DISCRIMINANT=
+1.811949895680e-12

MAX_STABILITY_ROOT_IMAG=
0
```

### 4.6 Counterrotation and weak membrane

Two equal vorton copies with opposite current/winding direction were combined so that

```math
T_{t\phi}^{(+)}
+
T_{t\phi}^{(-)}
=
0
```

while their diagonal energy/stress contributions add.

A weak membrane was then introduced only at the effective level.

Its loading was **not hand tuned**; it was fixed by the radial variational/stress-balance condition.

The selected wall energy fraction was

```text
1.036278747843e-02
```

or approximately $1.04\%$.

The stationarity residual was

```text
4.952298528680e-11
```

and the wall-loaded radial second derivative remained positive.

### 4.7 Positive far mass and finite payload

For the selected case:

```text
TOTAL_ENERGY_PER_RADIUS=
2.601697932595e+02

FAR_ACTIVE_MASS_PER_RADIUS=
2.601697932595e+02

RELERR=
2.184858516765e-16

POSITIVE_FAR_FIELD_ACTIVE_MASS=
True
```

Independent direct disk/ring quadrature gave positive outward acceleration.

A finite spherical payload also accelerated outward.

The payload average equaled the center field to numerical precision.

This follows analytically from the mean-value theorem.

Inside a source-free ball,

```math
\nabla^2\Phi
=
0
```

and therefore each acceleration component

```math
a_i
=
-\partial_i\Phi
```

is harmonic:

```math
\nabla^2a_i
=
0
```

For a uniform spherical test payload centered at $\mathbf x_0$,

```math
\frac{1}{V}
\int_V
a_i\,dV
=
a_i(\mathbf x_0)
```

provided the entire sphere lies inside the source-free region.

Thus, within the passive-test-body linearized calculation,

```math
\boxed{
\mathbf a_{\rm CM}
=
\mathbf a(\mathbf x_{\rm center})
}
```

The direct numerical payload calculation agreed at approximately $10^{-15}$ relative level.

### 4.8 Efficiency

The selected coefficient was

```text
SELECTED_C_MIN=
8.056470330320e+05
```

or

```math
C_{017P}
\approx
8.06\times10^5
```

This is approximately

```text
3.414976097040e4
```

times the finite 006D coefficient.

Therefore 017P was a **field-realization advance but an energetic regression**.

### 4.9 017P decision

```text
017P_GATE_PASS=
True

017P_DECISION=
LITERATURE_BACKED_GAUGED_VORTON_EOS_PLUS_WEAK_MEMBRANE_VARIATIONAL_GRAVITY_BRIDGE_SUPPORTED
```

The correct claim is:

> **A literature-backed gauged-vorton microscopic rim equation of state can support an effective weak-wall stationary architecture with positive far-field mass and finite-payload outward linearized gravity.**

The membrane itself remained effective.

Therefore 017P did **not** yet satisfy the buildplan requirement for a complete field-theoretical candidate.

---

## 5. 017Q — published same-model O(4) string/membrane compatibility gate

017Q investigated whether a published field theory already containing both superconducting string and attached membrane could remove the effective-membrane idealization.

The tested framework was the O(4) sigma-model drum-vorton analysis of Carter, Brandenberger, and Davis.

That published work shows that thermal electromagnetic effects can stabilize superconducting sigma strings and that weak explicit symmetry breaking can make the string the boundary of a membrane, producing a drum-vorton worldsheet equilibrium.

017Q used the paper's approximate worldsheet relations rather than solving the complete curved two-dimensional string/membrane field configuration.

### 5.1 Physical electromagnetic scan

The physical electromagnetic value was

```math
e^2
=
\alpha_{\rm EM}
\approx
\frac{1}{137.035999084}
```

so

```text
E_PHYSICAL=
8.542454313184e-02
```

The dense scan evaluated

```text
829440
```

physical-EM parameter points.

The initial strict worldsheet/stability/gravity filter retained

```text
38680
```

points.

Thus:

```text
PHYSICAL_EM_ROBUST_PARAMETER_WINDOW_FOUND=
True
```

A secondary generic-$e=0.30$ scan retained 183232 points.

### 5.2 Selected low-C physical point

The lowest-$C$ selected physical-EM point had approximately

```text
LAMBDA=
0.5

THETA=
0.5978947368421

M_TILDE=
0.05250733148307

NU_OVER_NUQ=
0.2204347826087

R_OVER_RSIGMA=
20

RSIGMA_OVER_RPHI=
3.012048964150

MIN_STABILITY_MARGIN=
0.1071739500783
```

The optimized gravitational coefficient was

```text
SELECTED_C_OPT=
8.994719113230e+01
```

or

```math
C_{017Q}
\approx
89.95
```

This was only about

```text
3.812680927486
```

times the finite 006D coefficient and approximately $9\times10^3$ times more efficient than 017P.

The finite-payload outward field, positive far mass, exact equilibrium relation, and integer winding all passed.

The nearest closed-loop winding was

```text
N=291
```

with radius adjustment only

```text
1.838053461929e-04
```

relative.

### 5.3 Robustness failure

The selected point survived only

```text
25 / 81
```

of the simultaneous $\pm5\%$ local parameter perturbations:

```text
NEIGHBORHOOD_PASS_FRACTION=
0.308641975309

ROBUST_PARAMETER_NEIGHBORHOOD=
False
```

Therefore

```text
017Q_GATE_PASS=
False
```

### 5.4 Important decision-label correction

The terminal output printed

```text
017Q_DECISION=
MICROSCOPIC_DRUM_WINDOW_SURVIVES_ONLY_GENERIC_STRONGER_GAUGE_BENCHMARK
```

That label is **too strong and logically inconsistent with the same output**, which also printed

```text
PHYSICAL_EM_ROBUST_PARAMETER_WINDOW_FOUND=True
```

The actual 017Q conclusion is:

> **A large physical-EM feasible window exists, but the particular lowest-$C$ physical point selected by the optimization failed the imposed local-neighborhood robustness threshold.**

017Q did **not** prove that physical electromagnetic coupling failed.

017R was designed specifically to resolve this ambiguity by optimizing robustness first rather than lowest $C$ first.

---

## 6. 017R — robustness-first physical-EM maximin basin

017R reversed the optimization order.

Instead of minimizing $C$ and testing robustness afterward, it required a robust interior basin first and then minimized the worst-case coefficient inside that basin.

### 6.1 Reference reconstruction

017R imported the exact 017Q implementation and reconstructed the 017Q physical point:

```text
017Q_REFERENCE_RECONSTRUCTION=
PASS
```

with relative coefficient reconstruction errors of order $10^{-13}$.

This protected the calculation from silently changing the 017Q equations while searching for a better basin.

### 6.2 Two global maximin searches

Two independently seeded differential-evolution searches found finite robust solutions with worst extreme-corner coefficients

```text
SEARCH_A_WORST_EXTREME_C=
93.52177614548

SEARCH_B_WORST_EXTREME_C=
93.37273848137
```

Both optimizer objects reported

```text
SUCCESS=False
```

because their formal convergence/stopping criterion had not been met within the configured iteration budget.

This must not be misread as a physical failure.

The optimizer outputs were treated only as candidate generators.

The scientific result rests on the subsequent deterministic and random robustness reconstructions.

### 6.3 Selected physical-EM interior point

The selected point was

```text
LAMBDA=
1.461079448136

THETA=
0.7475194883170

M_TILDE=
0.04319284396633

NU_OVER_NUQ=
0.1276494041917

R_OVER_RSIGMA=
24.99172696831
```

The nominal worst-EOS optimized coefficient was

```text
NOMINAL_WORST_EOS_C_OPT=
9.089990209433e+01
```

or

```math
C_{017R}
\approx
90.90
```

Thus the robustness penalty relative to the fragile 017Q optimum was extremely small.

### 6.4 Complete $\pm10\%$ deterministic five-dimensional lattice

The five parameters were each varied over

```text
0.90
0.95
1.00
1.05
1.10
```

for a total of

```math
5^5
=
3125
```

models.

Result:

```text
LATTICE_TOTAL=
3125

LATTICE_PASSING=
3125

LATTICE_PASS_FRACTION=
1.000000000000

LATTICE_MAX_C_OPT=
9.342715902963e+01

LATTICE_MIN_STABILITY_MARGIN=
5.856205431641e-02

LATTICE_MIN_RSIGMA_OVER_RPHI=
3.021474789250

DENSE_10PCT_ROBUSTNESS=
PASS
```

Thus every deterministic model in the full tested $\pm10\%$ hyperlattice survived both EOS variants and the worldsheet/gravity health gates.

### 6.5 20,000 random $\pm10\%$ hypercube perturbations

An independent random hypercube test gave

```text
MC_TOTAL=
20000

MC_PASSING=
20000

MC_PASS_FRACTION=
1.000000000000

MC_C_SUBSET_MAX=
9.315536443462e+01

RANDOM_10PCT_ROBUSTNESS=
PASS
```

This strongly reduced the probability that the deterministic lattice happened to miss a narrow failure channel.

### 6.6 Expanded $\pm15\%$ stress

The non-promotion stress test at $\pm15\%$ gave

```text
186 / 243
```

or

```text
0.765432098765
```

survival.

This usefully identified the approximate outer scale of the basin.

The promoted claim remains the $\pm10\%$ result.

### 6.7 Closed-loop quantization and gravity

The nearest integer winding was

```text
N=470
```

with relative radius adjustment

```text
2.970724695321e-04
```

Both EOS variants passed independent gravity quadrature and finite-payload outward acceleration.

Representative optimized results:

```text
PUBLISHED_SMALL_EPS:
C_OPT=90.42629405546

FULL_MCHI_STRESS:
C_OPT=90.89990209433
```

The direct and analytic center accelerations agreed to approximately $10^{-14}$ relative precision, and the finite spherical payload average again agreed with the center value to approximately $10^{-14}$.

### 6.8 Stationarity and far mass

For both EOS variants:

```text
STATIONARITY_BOTH_EOS=
PASS

POSITIVE_FAR_FIELD_ACTIVE_MASS_BOTH_EOS=
PASS
```

The active-mass/energy agreement was at approximately $10^{-14}$ or better.

### 6.9 017R decision

```text
017R_GATE_PASS=
True

017R_DECISION=
PHYSICAL_EM_MICROSCOPIC_DRUM_VORTON_ROBUST_INTERIOR_BASIN_SUPPORTED_NEAR_006D_EFFICIENCY_TIER
```

The phrase "microscopic" here must be interpreted carefully.

017R used a published microscopic-origin O(4) model through its approximate superconducting-string/membrane worldsheet description.

It did **not** solve the complete finite-thickness curved drum-vorton field equations.

The correct claim is:

> **The published physical-electromagnetic O(4) drum-vorton worldsheet model contains a deep, robust parameter basin in which the approximate same-model string/membrane architecture remains stationary, positive in far active mass, and finite-payload repulsive in linearized GR, with optimized $C\approx91$ and worst tested $\pm10\%$ lattice $C<94$.**

At this point further worldsheet parameter optimization was low value.

The nominal next step would have been the full finite-thickness Euler-Lagrange field solution.

017S was inserted first as a cheaper source-bookkeeping falsification gate.

---

## 7. 017S — thermal-support active-gravity obstruction

017S tested a physical contribution omitted by 017Q/017R:

> **the stress-energy of the thermal environment responsible for thermal stabilization in the O(4) model.**

This was a decisive gate because a background contribution can be dynamically irrelevant to the defect field equations while remaining gravitationally important.

### 7.1 Published thermal scale requirement

The Carter-Brandenberger-Davis thermal effective potential is derived by averaging short-wavelength thermal fluctuations.

The paper explicitly states that, for the thermal-potential approximation to be meaningful, the background variation length scale must be large compared with the thermal length scale.

Define

```math
\ell_T
=
\Theta^{-1}
```

in natural units.

Therefore a thermal layer only one $\ell_T$ thick is already an intentionally favorable localization assumption compared with a literal slowly varying equilibrium background.

### 7.2 Minimum photon active density

017S counted only equilibrium photons.

For blackbody photons,

```math
\rho_\gamma
=
\frac{\pi^2}{15}
\Theta^4
```

and

```math
p_\gamma
=
\frac13\rho_\gamma
```

The linearized active source is

```math
S_\gamma
=
\rho_\gamma
+p_x+p_y+p_z
```

so

```math
\boxed{
S_\gamma
=
2\rho_\gamma
}
```

This is a deliberately optimistic lower floor.

017S did **not** include thermal scalars, fermions, enclosure mass, heaters, pumps, control hardware, or containment energy.

### 7.3 Maximally favorable one-sided thermal geometry

To minimize attractive leverage, the entire uniform thermal layer was placed behind the membrane:

```text
-H <= z <= 0

0 <= rho <= R
```

with the payload above $z=0$.

For a uniform positive active density $S$ and an on-axis target at height $h$, the inward acceleration magnitude is

```math
\frac{|a_{\rm bath}|}{G}
=
2\pi S I
```

where

```math
I
=
\int_{-H}^{0}
dz'
\int_0^R
\rho\,d\rho
\frac{h-z'}
{\left[\rho^2+(h-z')^2\right]^{3/2}}
```

The radial integral is

```math
\int_0^R
\rho\,d\rho
\frac{a}
{\left(\rho^2+a^2\right)^{3/2}}
=
1
-
\frac{a}
{\sqrt{R^2+a^2}}
```

with $a=h-z'$.

Integrating over $z'$ gives

```math
\boxed{
I
=
H
+
\sqrt{h^2+R^2}
-
\sqrt{(h+H)^2+R^2}
}
```

This exact finite-cylinder formula was used for the thermal gravity floor.

### 7.4 Nominal 017R reconstruction

017S first reconstructed 017R:

```text
017R_RECONSTRUCTED_C_PUBLISHED=
90.42629405546

017R_RECONSTRUCTED_C_FULL=
90.89990209433

017R_SELECTED_POINT_RECONSTRUCTION=
PASS
```

Independent direct defect gravity again passed at approximately $10^{-14}$ relative error.

Thus the subsequent negative result was not caused by loss of the 017R repulsive solution.

### 7.5 Nominal photon floor

For the published-small-$\epsilon$ EOS at the selected 017R point:

```text
THETA_OVER_ETA=
1.057152198516

THERMAL_LENGTH=
0.9459375872307

R_SIGMA=
18.86907765920

ELLT_OVER_RSIGMA=
0.05013162828175
```

The photon energy and active densities were

```text
RHO_GAMMA=
0.8217856542331

ACTIVE_RHO_GAMMA=
1.643571308466
```

The optimized outward defect acceleration was

```text
DEFECT_OUT_OVER_G=
+4.462870285801e-02
```

while a one-$\ell_T$ one-sided photon layer produced

```text
BATH_DOWN_OVER_G_AT_1_ELLT=
7.474223654187
```

Therefore

```text
BATH_TO_DEFECT_RATIO=
1.674757090289e+02
```

or approximately

```math
\boxed{
\frac{|a_{\rm bath}|}
{a_{\rm defect}}
\approx
167.5
}
```

The full-$m_\chi$ EOS gave the same conclusion:

```text
BATH_TO_DEFECT_RATIO=
1.675069991769e+02
```

### 7.6 Critical thermal localization

Define $H_{\rm crit}$ by

```math
|a_{\rm bath}(H_{\rm crit})|
=
a_{\rm defect}
```

For the nominal case:

```text
H_CRIT=
5.641455004048e-03

H_CRIT_OVER_ELLT=
5.963876560359e-03

H_CRIT_OVER_RSIGMA=
2.989788428422e-04
```

Thus the photon bath would have to be confined to only about

```math
0.006\,\ell_T
```

to avoid erasing the repulsive field.

This is much smaller than one thermal length, whereas the thermal effective-potential derivation requires background variation scales large compared with the thermal length.

At one thermal length, the maximum allowed local blackbody occupation fraction was only

```text
5.971015174668e-03
```

or approximately $0.6\%$.

### 7.7 Thermal energy scale

For the one-$\ell_T$ layer:

```text
ONE_ELLT_PHOTON_LAYER_ENERGY=
5.430812263033e+05

DEFECT_ENERGY=
5.196241627180e+04

BATH_TO_DEFECT_ENERGY_RATIO=
1.045142364941e+01
```

Thus even the minimum photon layer carried approximately ten times the defect energy in the chosen normalization.

This energy comparison is secondary to the local force obstruction but points in the same direction.

### 7.8 Full 017R robust-basin thermal test

017S repeated the thermal bookkeeping over the complete 017R deterministic $\pm10\%$ basin:

```text
THERMAL_LATTICE_MODELS=
3125

THERMAL_LATTICE_PAIR_FAILURES=
0

THERMAL_LATTICE_EOS_RECORDS=
6250
```

The most favorable bath/defect acceleration ratio anywhere in the entire basin was still

```text
MIN_BATH_TO_DEFECT_ACCEL_RATIO_AT_ONE_THERMAL_LENGTH=
9.432678144215e+01
```

or approximately $94.3$.

The largest survivable layer thickness anywhere in the basin was

```text
MAX_SURVIVABLE_LAYER_THICKNESS_OVER_THERMAL_LENGTH=
1.058814945999e-02
```

or about $1.06\%$ of one thermal length.

The largest allowed local blackbody fraction at one thermal length was

```text
MAX_ALLOWED_BLACKBODY_FRACTION_AT_ONE_THERMAL_LENGTH=
1.060144303358e-02
```

The one-$\ell_T$ photon energy ranged from approximately

```text
5.87
```

to

```text
19.50
```

times the defect energy across the tested basin.

Therefore:

```text
ONE_THERMAL_LENGTH_PHOTON_FLOOR_ALWAYS_OVERWHELMS_REPULSION=
True

ALL_SURVIVING_LOCALIZED_BATH_THICKNESSES_SUBTHERMAL=
True
```

### 7.9 017S decision

```text
LOCALIZED_PHYSICAL_THERMAL_SUPPORT_PRESERVES_REPULSION=
False

017S_DECISION=
LITERAL_LOCALIZED_THERMAL_O4_DRUM_ROUTE_STRONGLY_DEMOTED_BY_MINIMUM_PHOTON_ACTIVE_GRAVITY
```

This is the principal negative result of the slice.

It does **not** invalidate 017R as a worldsheet/matter-mechanics result.

It says that the literal localized thermal environment used to justify that worldsheet state cannot be omitted from the gravitational source budget.

Once the minimum photon bath is included, the outward field is overwhelmed throughout the tested robust basin.

---

# Result

The post-016H program produced a clear sequence of promotion and falsification.

## Positive results

```text
017C_EFFECTIVE_DRUM_FINITE_PAYLOAD_REPULSION=
YES

017O_BARE_EFFECTIVE_DRUM_NONAXIAL_STABILITY=
FAIL

017O_CURVATURE_RIGIDITY_THRESHOLD=
B_CRIT_OVER_SIGMA_R3_EQUALS_1_OVER_3

017P_GAUGED_VORTON_FIELD_EOS_RECONSTRUCTION=
PASS

017P_SET_B_LITERATURE_BENCHMARK=
PASS

017P_SET_G_DOMAIN_CONVERGENCE=
PASS

017P_M2_TO_M40_STABLE_REGION=
YES

017P_EFFECTIVE_WEAK_WALL_FINITE_PAYLOAD_REPULSION=
YES

017P_POSITIVE_FAR_FIELD_ACTIVE_MASS=
YES

017Q_PHYSICAL_EM_FEASIBLE_WINDOW=
YES_38680_OF_829440_INITIAL_SCAN_POINTS

017Q_LOW_C_PHYSICAL_POINT=
C_APPROX_89P95_BUT_LOCAL_ROBUSTNESS_FAIL

017R_PHYSICAL_EM_ROBUST_INTERIOR_BASIN=
SUPPORTED

017R_DENSE_PLUS_MINUS_10_PERCENT_LATTICE=
3125_OF_3125_PASS

017R_RANDOM_PLUS_MINUS_10_PERCENT_HYPERCUBE=
20000_OF_20000_PASS

017R_NOMINAL_WORST_EOS_C=
90.89990209433

017R_WORST_DENSE_10_PERCENT_C=
93.42715902963

017R_FINITE_PAYLOAD_OUTWARD_BOTH_EOS=
YES

017R_POSITIVE_FAR_FIELD_ACTIVE_MASS_BOTH_EOS=
PASS
```

## Negative / limiting results

```text
017O_BARE_MECHANICAL_DRUM=
NONAXISYMMETRICALLY_UNSTABLE

017O_SIMPLE_THIN_CORE_BENDING_RESCUE=
ENERGETICALLY_SEVERE

017P_ENERGY_EFFICIENCY=
MUCH_WORSE_THAN_006D

017Q_SELECTED_LOW_C_POINT_LOCAL_ROBUSTNESS=
FAIL

017S_LITERAL_LOCALIZED_THERMAL_O4_IMPLEMENTATION=
STRONGLY_DEMOTED

017S_MINIMUM_ONE_THERMAL_LENGTH_PHOTON_ATTRACTION_OVER_DEFECT_REPULSION_IN_ROBUST_BASIN=
GREATER_THAN_94

017S_ALL_FORCE_PRESERVING_THERMAL_LAYER_THICKNESSES=
LESS_THAN_0P011_THERMAL_LENGTH
```

## Central scientific interpretation

The strongest field-realization lesson is now:

> **The spatial drum/rim architecture is not obviously the problem. A field-theoretic vorton rim can be stable, and a same-model string/membrane worldsheet can exhibit a remarkably robust finite-payload repulsive basin. But every physical support sector must be included in the gravitational stress-energy budget. In the literal thermally stabilized O(4) implementation, the thermal support energy itself destroys the desired gravitational sign.**

Therefore the new frontier is not another O(4) worldsheet optimization.

It is:

```text
NONTHERMAL_STABILIZATION
```

specifically:

```text
017P_LITERATURE_BACKED_GAUGED_VORTON_RIM
+
TOPOLOGY_CONSISTENT_MICROSCOPIC_NONTHERMAL_WALL_SECTOR
```

The objective is to retain the positive 017P/017R architectural lessons without paying the fatal thermal active-gravity floor.

---

# Verification

## Analytical

### 017O

The bare nonaxisymmetric instability was derived analytically:

```math
\Delta E_m
=
-\frac{\pi\sigma R^2}{2}
(m^2-1)
\epsilon^2
```

for every $m\ge2$.

The curvature-rigidity threshold was also derived analytically:

```math
b_{\rm crit}(m)
=
\frac{1}{m^2-1}
```

with the controlling mode

```math
b_{\rm crit}
=
\frac13
```

for $m=2$.

### 017P finite payload

The finite spherical payload identity follows from harmonicity of the acceleration components in a source-free ball:

```math
\mathbf a_{\rm CM}
=
\mathbf a(\mathbf x_{\rm center})
```

for a uniform spherical passive payload wholly inside that source-free region.

### 017S radiation source

For equilibrium radiation,

```math
S_\gamma
=
\rho_\gamma+3p_\gamma
=
2\rho_\gamma
```

The one-sided finite-cylinder force kernel was integrated analytically:

```math
I(H)
=
H
+
\sqrt{h^2+R^2}
-
\sqrt{(h+H)^2+R^2}
```

This made the thermal obstruction a direct source-bound calculation rather than a numerical field-mesh artifact.

---

## Numerical

The following independent numerical checks were central:

```text
KNOWN_SOLUTION_BASELINE=
94_PASSED

017O_DIRECT_SHAPE_INTEGRATION=
AGREES_WITH_QUADRATIC_ANALYTIC_MODE_COEFFICIENTS

017P_SET_B_PUBLISHED_BENCHMARK=
PASS

017P_SET_G_DOMAIN_CONVERGENCE=
~3e-7_RELATIVE

017P_VARIATIONAL_IDENTITY=
3.55e-8_MAX_RELATIVE_ERROR

017P_STABILITY_ROOT_CHECK=
PASS_M2_TO_M40_IN_SELECTED_REGION

017P_DIRECT_GRAVITY_QUADRATURE=
PASS

017P_FINITE_PAYLOAD_MEAN_VALUE_CHECK=
PASS

017Q_DIRECT_GRAVITY_QUADRATURE=
PASS

017R_DENSE_10_PERCENT_LATTICE=
3125_OF_3125

017R_RANDOM_10_PERCENT_HYPERCUBE=
20000_OF_20000

017R_DIRECT_GRAVITY_BOTH_EOS=
PASS

017S_017R_RECONSTRUCTION=
PASS

017S_DEFECT_GRAVITY_RECONSTRUCTION=
PASS

017S_THERMAL_BASIN_RECORDS=
6250
```

The strongest positive and negative signs are therefore not single-grid observations.

---

## Dimensional

### GR efficiency coefficient

The project efficiency measure remains

```math
M
=
C\frac{ah^2}{G}
```

Since

```math
\left[
\frac{ah^2}{G}
\right]
=
{\rm kg}
```

$C$ is dimensionless.

### Thermal length

In natural units,

```math
\ell_T
=
\Theta^{-1}
```

has dimensions of length.

The critical localization ratio

```math
\frac{H_{\rm crit}}{\ell_T}
```

is dimensionless and therefore directly comparable to the scale-separation requirement underlying the thermal effective potential.

### Radiation active density

$\rho_\gamma$ and $S_\gamma$ both have energy-density dimensions.

The finite-cylinder expression

```math
2\pi G S_\gamma I
```

has acceleration dimensions because $I$ has dimensions of length.

---

## Limiting cases

### 017O

As $B\rightarrow0$,

```math
b\rightarrow0
```

and every $m\ge2$ mode returns to the bare negative quadratic energy.

As $b$ exceeds $1/3$, all modes $m\ge2$ satisfy the quadratic stability threshold because $m=2$ is the most restrictive.

### 017P / 017R finite payload

As the passive spherical payload radius tends to zero, the payload-averaged acceleration trivially approaches the center acceleration.

For any finite spherical radius that stays inside the source-free region, the harmonic mean-value result gives the same equality exactly within the test-body linearized model.

### 017S

As thermal thickness

```math
H\rightarrow0
```

the bath attraction vanishes linearly.

The calculation therefore explicitly determines how small $H$ would have to become before repulsion reappears.

The resulting

```math
H_{\rm crit}\ll\ell_T
```

is the obstruction.

---

## Literature comparison

The field-theory ingredients used in this slice are not project inventions.

### Stable gauged vortons

Battye, Cotterill, and Pearson constructed and dynamically simulated gauged vortons and showed good agreement between straight superconducting-string thin-string analysis, energy-minimized vorton solutions, and three-dimensional evolution.

Relevant references:

```text
R. A. Battye, S. J. Cotterill, J. A. Pearson,
A detailed study of the stability of vortons,
JHEP 04 (2022) 005,
arXiv:2112.08066.
```

and the preceding fully stable vorton result

```text
R. A. Battye, S. J. Cotterill,
Stable Cosmic Vortons in Bosonic Field Theory,
Phys. Rev. Lett. 127, 241601 (2021),
arXiv:2111.07822.
```

These publications mean that 017O cannot be interpreted as a theorem that all vorton-like rings are unstable.

It only rejects the minimal 017C mechanical equation of state.

### Drum vortons

The same-model string-plus-membrane concept was published by Carter, Brandenberger, and Davis:

```text
B. Carter, R. H. Brandenberger, A.-C. Davis,
Thermal stabilization of superconducting sigma strings and their drum vortons,
Phys. Rev. D 65, 103520 (2002),
hep-ph/0201155.
```

The paper explicitly derives a thermally modified model, discusses superconducting strings, weak explicit symmetry breaking, attached sigma membranes, and drum-vorton equilibrium.

It also explicitly states that the thermal effective-potential treatment assumes a background variation scale large compared with the thermal length scale.

That assumption is central to the interpretation of 017S.

### Gravitating vortons

Full gravitating vorton solutions are known in the literature, for example:

```text
J. Kunz, E. Radu, B. Subagyo,
Gravitating vortons as ring solitons in general relativity,
Phys. Rev. D 87, 104022 (2013),
arXiv:1303.1003.
```

This establishes that coupling vorton field theories to Einstein gravity is a legitimate published problem class.

It does **not** establish that the project’s repulsive drum architecture has a nonlinear Einstein-matter continuation.

### Novelty status

The project-derived combination of gravitational optimization, finite-payload criterion, 017O shape-stability theorem for the specific effective drum, and 017S thermal active-gravity bookkeeping has not been established as novel relative to the complete literature.

Therefore:

```text
NOVELTY=
NOT_ESTABLISHED

NEW_PHYSICS_DISCOVERY=
NO
```

---

# Falsification Attempt

The research slice was explicitly organized to try to destroy its own promising drum/vorton results.

## 1. Could 017C be radially stable but nonaxisymmetrically unstable?

017O:

```text
YES
```

The bare effective drum failed every tested $m\ge2$ quadratic shape mode.

This falsified the sufficiency of radial stability.

## 2. Could a simple bending modulus rescue 017C cheaply?

017O:

```text
NO_IN_THE_TESTED_THIN_CORE_SCALING
```

Order-one thin-core rigidity required very large support energy and severe inherited $C$ penalties.

## 3. Could a real field-theory vorton EOS repair the rim?

017P:

```text
YES_AT_THE_RIM_EOS_PLUS_EFFECTIVE_WALL_LEVEL
```

The published field equations were solved, the literature benchmark was reconstructed, and a stable neighboring-$\chi$ band was found.

## 4. Could 017P’s finite-payload result be a force-kernel implementation artifact?

Independent direct source quadrature and the harmonic mean-value theorem both reproduced the outward finite-payload result.

This failure mode was not supported.

## 5. Could the published physical-EM O(4) drum architecture exist only at isolated fine-tuned points?

017Q initially appeared fragile because its lowest-$C$ point passed only 25/81 local perturbations.

017R then directly falsified the stronger fine-tuning concern:

```text
3125 / 3125
```

deterministic $\pm10\%$ models and

```text
20000 / 20000
```

random $\pm10\%$ perturbations survived.

Thus the worldsheet parameter basin is genuinely broad in the tested model.

## 6. Could the 017Q failure mean physical electromagnetic coupling was impossible?

No.

The original scan already contained 38,680 physical-EM feasible points.

017R found a deep physical-EM robust basin.

The misleading 017Q terminal decision label must not be carried forward as a physical conclusion.

## 7. Could the thermal support be gravitationally negligible because it is omitted from the defect potential?

017S:

```text
NO
```

A field-independent or averaged background term can be irrelevant to the local defect Euler-Lagrange variation while still gravitating.

The photon-only floor overwhelmed the defect by at least $94\times$ throughout the robust basin at one thermal length.

## 8. Could favorable placement of the bath solve the problem?

017S already used an intentionally favorable geometry:

```text
ALL THERMAL ENERGY BEHIND THE MEMBRANE
NO THERMAL MATERIAL BETWEEN PAYLOAD AND DRUM
```

The obstruction remained overwhelming.

A symmetric bath was even worse.

## 9. Could reducing thermal thickness save the effect?

Only by requiring

```math
H\lesssim0.01\ell_T
```

throughout the robust basin.

This lies on the wrong side of the thermal scale-separation assumption used to derive the equilibrium thermal effective potential.

Thus the literal localized equilibrium-thermal realization is strongly demoted.

## 10. Does 017S close all O(4), vorton, or membrane physics?

No.

017S does not close:

```text
UNIFORM_COSMOLOGICAL_THERMAL_BACKGROUND

NONTHERMAL_EFFECTIVE_STABILIZATION

GAUGED_VORTONS_GENERALLY

NONTHERMAL_MICROSCOPIC_WALL_SECTORS

OTHER_DRUM_VORTON_FIELD_THEORIES
```

It closes only the literal localized thermal-support interpretation tested by 017Q/017R as a practical asymptotically local source.

---

# Claims Status

`CLAIMS.md` should eventually be synchronized with the following durable records.

```text
CLAIM_ID=017O_BARE_EFFECTIVE_DRUM_NONAXIAL_STABILITY

TYPE=
PROJECT_DERIVED_ANALYTIC_AND_NUMERICAL_STABILITY_RESULT

STATUS=
REJECTED_FOR_MINIMAL_017C_EFFECTIVE_ENERGY
```

```text
CLAIM_ID=017O_CURVATURE_RIGIDITY_THRESHOLD

TYPE=
PROJECT_DERIVED_ANALYTIC_RESULT

STATUS=
SUPPORTED_WITH_DIRECT_NUMERICAL_SHAPE_RECONSTRUCTION

RESULT=
B_OVER_SIGMA_R3_GREATER_THAN_1_OVER_3_CONTROLS_M2
```

```text
CLAIM_ID=017P_GAUGED_VORTON_FIELD_EOS_WEAK_WALL_BRIDGE

TYPE=
PROJECT_DERIVED_LITERATURE_BACKED_FIELD_EOS_VARIATIONAL_GRAVITY_RESULT

STATUS=
SUPPORTED_WITHIN_STRAIGHT_STRING_PLUS_EFFECTIVE_WALL_APPROXIMATION
```

```text
CLAIM_ID=017P_FINITE_PASSIVE_PAYLOAD_OUTWARD_GRAVITY

TYPE=
PROJECT_DERIVED_LINEARIZED_GR_TEST_BODY_RESULT

STATUS=
SUPPORTED_WITH_DIRECT_QUADRATURE_AND_HARMONIC_MEAN_VALUE_CHECK
```

```text
CLAIM_ID=017Q_PHYSICAL_EM_WORLD_SHEET_FEASIBLE_WINDOW

TYPE=
PROJECT_DERIVED_PARAMETER_SCAN_RESULT

STATUS=
SUPPORTED

NOTE=
017Q_GATE_FAILURE_WAS_SELECTED_POINT_ROBUSTNESS_NOT_ABSENCE_OF_PHYSICAL_EM_WINDOW
```

```text
CLAIM_ID=017R_PHYSICAL_EM_ROBUST_INTERIOR_DRUM_VORTON_BASIN

TYPE=
PROJECT_DERIVED_WORLD_SHEET_ROBUSTNESS_RESULT

STATUS=
SUPPORTED_IN_TESTED_PUBLISHED_APPROXIMATE_O4_WORLD_SHEET_MODEL
```

```text
CLAIM_ID=017R_DENSE_10_PERCENT_ROBUSTNESS

STATUS=
3125_OF_3125_PASS
```

```text
CLAIM_ID=017R_RANDOM_10_PERCENT_ROBUSTNESS

STATUS=
20000_OF_20000_PASS
```

```text
CLAIM_ID=017S_LOCALIZED_THERMAL_SUPPORT_ACTIVE_GRAVITY

TYPE=
PROJECT_DERIVED_ANALYTIC_AND_NUMERICAL_FEASIBILITY_BOUND

STATUS=
LITERAL_LOCALIZED_THERMAL_O4_ROUTE_STRONGLY_DEMOTED
```

```text
CLAIM_ID=017S_MINIMUM_PHOTON_FLOOR

STATUS=
ONE_THERMAL_LENGTH_PHOTON_ACTIVE_GRAVITY_EXCEEDS_DEFECT_REPULSION_THROUGHOUT_TESTED_017R_ROBUST_BASIN
```

The following claims remain prohibited:

```text
FULL_2D_DRUM_VORTON_FIELD_SOLUTION=
ESTABLISHED

FULL_NONAXISYMMETRIC_WALL_LOADED_STABILITY=
ESTABLISHED

NONLINEAR_EINSTEIN_MATTER_REPULSION=
ESTABLISHED

PAYLOAD_BACKREACTION=
ESTABLISHED

PRACTICAL_ABSOLUTE_ENERGY=
SOLVED

PRACTICAL_ANTIGRAVITY_DEVICE=
ESTABLISHED

NEW_PHYSICS_DISCOVERY=
ESTABLISHED
```

---

# Open Questions

## 1. Can the 017P nonthermal gauged-vorton rim be combined with a topology-consistent microscopic wall sector?

This is now the highest-value established-GR matter-realization question.

The wall sector must satisfy a topological requirement:

> A finite membrane cannot simply terminate on an unrelated ring by fiat. The field-space vacuum structure and couplings must make the vorton/string a legitimate boundary of the wall.

The next model must therefore establish the topology/coupling structure before launching a full PDE.

## 2. Can the microscopic wall be nonthermal?

017S strongly demotes the localized equilibrium-thermal support mechanism.

Candidate nonthermal wall sectors may involve:

* explicit weak symmetry breaking in a field whose phase/vacuum structure is tied to the vortex;
* axion-like or sine-Gordon wall bounded by string, provided its own energy budget is included;
* a separate symmetry-breaking field with a justified junction interaction to the gauged-vorton rim;
* another known string-wall system whose complete stress tensor is healthy and finite.

The next step should prefer established field-theory structures over arbitrary phenomenological wall tension.

## 3. Does the complete finite-thickness field solution exist?

A positive topology/model-selection preflight must be followed by a genuine coupled Euler-Lagrange solve.

The buildplan promotion requirement is:

```text
FINITE_ENERGY
GLOBAL_REGULARITY
FULL_EULER_LAGRANGE_EQUATIONS
CONSERVATION
FINITE_PAYLOAD_REPULSION
INDEPENDENT_RECONSTRUCTION
```

Only then may the architecture be promoted to

```text
FIELD_THEORETICAL_CANDIDATE
```

## 4. Does the repulsive effect survive full composite stability?

Worldsheet/extrinsic stability is not enough.

The complete field configuration must test at least:

```text
RADIAL_MODE
VERTICAL_MODE
M2_ELLIPTIC_MODE
HIGHER_AZIMUTHAL_MODES
WALL_RIM_RELATIVE_DISPLACEMENT
CHARGE_TRANSFER
CURRENT_PERTURBATIONS
GAUGE_PERTURBATIONS
VORTEX_SPLITTING
MEMBRANE_RIPPLE_MODES
COLLAPSE / EXPANSION
```

This is the milestone required for the approximate $65$–$72\%$ project tier.

## 5. Does a nonlinear Einstein-matter continuation preserve finite-payload repulsion?

If the matter solution survives, solve

```math
G_{\mu\nu}
=
\frac{8\pi G}{c^4}
T_{\mu\nu}
```

self-consistently.

For stationary rotating sources, frame dragging must be retained.

The O(4) worldsheet candidate carried large nonzero angular momentum; a future nonthermal construction may also be stationary rather than static.

The finite-payload observable must remain operational rather than coordinate-dependent.

## 6. Can practical energy scaling ever be solved?

Even the most attractive worldsheet coefficient in this slice,

```math
C\sim90
```

remains an order-unity geometric coefficient multiplying

```math
\frac{ah^2}{G}
```

in pure GR.

That is still catastrophically large at human scales.

A practical device therefore still requires a qualitative scaling breakthrough, not merely a better $C$.

## 7. Should the protected disformal or modified-gravity branches remain alive?

Yes, as ranked alternatives.

017J, 017M, and 017N strongly demoted several straightforward alternatives, but the project should preserve them as fallbacks if the nonthermal established-GR field-realization route fails.

No speculative branch should be reopened merely to avoid a difficult negative result in GR.

---

# Practical-Progress Heuristic

This journal records the live conversational heuristic only for continuity.

It is **not** a physical probability and should not be used as evidence.

The live interpretation during the session was roughly:

```text
AFTER_017P:
~60%

AFTER_017Q:
~62%

AFTER_017R:
~64_TO_65%

AFTER_017S_THERMAL_OBSTRUCTION:
~62_TO_63%
```

The decrease after 017S is not scientific regression.

It reflects removal of a physical realization that had previously appeared promising.

The checked-in buildplan snapshot still carried an older lower milestone estimate and should be updated separately.

The only scientifically meaningful promotion toward the next tier is now an actual nonthermal finite-energy full Euler-Lagrange field solution with finite-payload repulsion.

---

# AI Assistance

AI assistant used: **ChatGPT by OpenAI**

Substantial AI-assisted work in this research slice included:

* global reranking of the surviving established-GR, disformal, vector, axion, and modified-gravity branches;
* derivation of the 017O nonaxisymmetric shape-mode expansion;
* derivation of the curvature-rigidity threshold $b_{\rm crit}=1/3$;
* design of the independent direct-shape numerical reconstruction;
* literature identification of stable gauged vortons and gravitating vortons;
* construction of the 017P straight-string BVP and integrated EOS checks;
* design of the set-B published-benchmark reconstruction;
* derivation and implementation of the straight-string variational identity check;
* implementation of the $m=2$ through $40$ thin-string stability discriminant and independent polynomial-root check;
* derivation of the counterrotating-pair active source and weak-wall stationarity condition;
* derivation and numerical verification of the finite spherical payload mean-value result;
* identification of the published O(4) same-model string/membrane drum-vorton framework;
* construction of 017Q's physical-EM and generic-gauge scans;
* identification and correction of the 017Q decision-label interpretation;
* design of 017R's robustness-first maximin search;
* construction of the complete 3125-point deterministic $\pm10\%$ lattice and 20,000-point random robustness test;
* identification of the thermal-background gravitational bookkeeping omission;
* derivation of the equilibrium photon active-density floor;
* derivation of the exact one-sided finite-cylinder thermal gravity kernel;
* construction of the complete 017S robust-basin thermal obstruction test;
* literature comparison and claim-boundary analysis;
* preparation of this journal record.

AI-generated mathematics, code, and scientific interpretations are not assumed correct solely because they were AI-generated.

All major claims remain subject to:

```text
ANALYTIC_CHECK
NUMERICAL_CHECK
DIMENSIONAL_CHECK
LIMITING_CASE_CHECK
INDEPENDENT_IMPLEMENTATION
LITERATURE_COMPARISON
ASSUMPTION_AUDIT
```

No result in this journal should be promoted to a scientific discovery without independent external verification and literature comparison.

---

# Next Action

The literal localized thermal O(4) route should be considered strongly demoted unless a genuinely different non-equilibrium or curved-background thermal implementation is proposed and its complete gravitational stress-energy is included.

Do **not** spend the next session optimizing the 017R thermal worldsheet basin further.

Do **not** launch the full thermal O(4) 2D PDE merely because 017R was robust.

The highest-value next scientific question is:

> **Can a nonthermal, topology-consistent microscopic wall sector be attached to the already literature-backed stable gauged-vorton rim of 017P while preserving finite energy, stationarity, positive far-field mass, and finite-payload outward gravity?**

The cheapest decisive next gate should therefore be a topology/coupling and energy-budget preflight for a known nonthermal string-wall field theory.

A positive result should immediately promote to:

```text
FULL_2D_COUPLED_GAUGED_VORTON_PLUS_MICROSCOPIC_NONTHERMAL_WALL_EULER_LAGRANGE_SOLVE
```

Required outputs of that full solve must include:

```text
FIELD_EQUATION_RESIDUALS

FINITE_TOTAL_ENERGY

GLOBAL_REGULARITY

NOETHER_CHARGE

GAUGE_CHARGE

NET_ANGULAR_MOMENTUM

COMPLETE_T_MUNU

LOCAL_CONSERVATION

TOTAL_ACTIVE_MASS

FINITE_PAYLOAD_ACCELERATION

FINITE_SOURCE_THICKNESS

DOMAIN_CONVERGENCE

GRID_CONVERGENCE

INDEPENDENT_STRESS_AND_FORCE_RECONSTRUCTION
```

If no topology-consistent nonthermal wall can coexist with the stable gauged-vorton rim without destroying the repulsive active moment, the established-GR drum/vorton realization branch should be demoted rather than protected by increasingly arbitrary hidden structure.

---

# Final Scientific State at Journal Close

```text
REGRESSION_BASELINE=
94_PASSED

006D_CONSTRUCTIVE_LINEARIZED_GR_REPULSION=
PRESERVED

006D_FINITE_C=
23.591586299249

017C_EFFECTIVE_DRUM_FINITE_PAYLOAD_REPULSION=
YES

017O_BARE_017C_NONAXISYMMETRIC_STABILITY=
FAIL

017O_RIGIDITY_THRESHOLD_B_OVER_SIGMA_R3=
1_OVER_3

017O_SIMPLE_THIN_CORE_BENDING_RESCUE=
ENERGETICALLY_SEVERE

017P_PUBLISHED_GAUGED_VORTON_BENCHMARK_RECONSTRUCTION=
PASS

017P_GAUGED_VORTON_FIELD_EOS=
SOLVED_FOR_STRAIGHT_STRING_BVP

017P_M2_TO_M40_STABLE_NEIGHBOR_REGION=
YES

017P_WEAK_EFFECTIVE_WALL_STATIONARITY=
PASS

017P_FINITE_PAYLOAD_OUTWARD_LINEARIZED_GRAVITY=
YES

017P_POSITIVE_FAR_FIELD_ACTIVE_MASS=
YES

017P_C=
8.056470330320e5

017Q_PHYSICAL_EM_INITIAL_FEASIBLE_POINTS=
38680_OF_829440

017Q_PHYSICAL_EM_WINDOW=
YES

017Q_LOWEST_C_SELECTED_POINT=
C_APPROX_89P947

017Q_SELECTED_POINT_LOCAL_ROBUSTNESS=
25_OF_81_FAILS_PROMOTION_THRESHOLD

017Q_TERMINAL_DECISION_LABEL_PHYSICAL_EM_ONLY_GENERIC=
DO_NOT_CARRY_FORWARD_AS_LITERAL_CONCLUSION

017R_PHYSICAL_EM_ROBUST_INTERIOR=
SUPPORTED

017R_DENSE_PLUS_MINUS_10_PERCENT=
3125_OF_3125_PASS

017R_RANDOM_PLUS_MINUS_10_PERCENT=
20000_OF_20000_PASS

017R_PLUS_MINUS_15_PERCENT_STRESS=
186_OF_243_PASS

017R_NOMINAL_WORST_EOS_C=
90.89990209433

017R_WORST_DENSE_10_PERCENT_C=
93.42715902963

017R_INTEGER_WINDING=
470

017R_DIRECT_GRAVITY_BOTH_EOS=
PASS

017R_FINITE_PAYLOAD_OUTWARD_BOTH_EOS=
YES

017R_POSITIVE_FAR_FIELD_ACTIVE_MASS_BOTH_EOS=
PASS

017S_017R_RECONSTRUCTION=
PASS

017S_NOMINAL_ONE_ELLT_PHOTON_BATH_TO_DEFECT_ACCELERATION=
APPROX_167P5

017S_MINIMUM_ONE_ELLT_BATH_TO_DEFECT_RATIO_ACROSS_ROBUST_BASIN=
94.32678144215

017S_MAX_SURVIVABLE_THERMAL_LAYER_OVER_ELLT=
0.01058814945999

017S_MAX_ALLOWED_BLACKBODY_FRACTION_AT_ONE_ELLT=
0.01060144303358

017S_LITERAL_LOCALIZED_THERMAL_O4_ROUTE=
STRONGLY_DEMOTED

FULL_FINITE_THICKNESS_DRUM_VORTON_EULER_LAGRANGE_SOLUTION=
NOT_ESTABLISHED

FULL_COMPOSITE_DYNAMICAL_STABILITY=
NOT_ESTABLISHED

NONLINEAR_EINSTEIN_MATTER_REALIZATION=
NOT_ESTABLISHED

PAYLOAD_BACKREACTION=
NOT_INCLUDED

PRACTICAL_ABSOLUTE_ENERGY=
NOT_SOLVED

PRACTICAL_ANTIGRAVITY_DEVICE=
NO

NEW_PHYSICS_DISCOVERY=
NO

NOVELTY=
NOT_ESTABLISHED

ACTIVE_NEXT_FRONTIER=
NONTHERMAL_GAUGED_VORTON_RIM_PLUS_TOPOLOGY_CONSISTENT_MICROSCOPIC_WALL
```

---

# Final Journal Classification

The durable positive conclusion is:

> **The 006D spatial-segregation principle can be carried substantially closer to known field theory than the earlier engineered stress tensor alone suggested. A published gauged superconducting-string EOS supports a stable rim preflight, and a published same-model string/membrane worldsheet approximation contains a broad physical-electromagnetic finite-payload-repulsive basin with $C$ of order $10^2$.**

The durable negative conclusion is equally important:

> **The literal localized equilibrium-thermal mechanism used to stabilize the tested O(4) drum-vorton cannot be treated as gravitationally free. Even the minimum photon-only active source overwhelms the outward defect field by at least roughly two orders of magnitude throughout the entire tested robust basin, unless the thermal layer is confined to a sub-thermal scale incompatible with the approximation used to derive the thermal effective potential.**

Therefore the project has **not** reached a complete physical antigravity realization.

The spatial architecture remains scientifically promising, but the next realization must be nonthermal or otherwise include a support environment whose full gravitational stress-energy does not erase the effect.

The strongest established public headline remains the 006D result:

> **We have a mathematical construction for antigravity-like gravitational repulsion.**

The project must not replace that statement with a claim of a practical device or a new force.
