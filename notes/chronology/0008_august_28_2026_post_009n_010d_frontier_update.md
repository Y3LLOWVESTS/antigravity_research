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



