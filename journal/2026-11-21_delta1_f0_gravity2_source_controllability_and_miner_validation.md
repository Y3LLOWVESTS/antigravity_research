# Research Journal — 2026-11-21

## DELTA1-F0 through F0G, GRAVITY2 Action-Miner Construction, and R3B Source-Controllability Obstructions

## Objective

Determine whether the historical R3B loaded-force reversal can be assigned to a physically admissible, conserved source and material response, rather than being repaired through a prescribed field or favorable interface coefficient. Build a bounded, independently verifiable GRAVITY2 action-mining platform to accelerate genuinely informative future checks without elevating test throughput into a claim of physical success.

This journal supplements, and does not rewrite, the November 20 DELTA1-00–02 journal. Those experiments preceded the work recorded here. The later freeze record and future R3B Engine build plan determine priorities after November 22, but not the November 21 findings.

## Starting State

- Protected conservative GR anchor: 006D, finite positive-energy locally conserved linearized-GR source, NEC/WEC/DEC, outward near field, positive far active mass, coefficient `C=23.591586299249`, enormous practical energy scale proportional to `1/G`.
- A12C prescribed F² field capacity: `2.6568591420597114 J`; not physically sourced.
- R3B prescribed mixed-field capacity: `1.5429162116460216 J`; still not source-supported.
- Historical adverse loaded-torus acceleration: `-129.67185782242464 m/s²` in the recorded R3B loading case; other B14/B16 hotspot signals and sign failures remain protected separately.
- PH16-04R2: accepted jointly stationary finite-lattice charged matter/X/Y/neutral-fluid Routhian, 12/12 identities, 19/19 scientific gates, 60/60 focused tests and 2,943/2,943 full regression. This is not a complete continuum, Einstein or source-material realization.
- ALPHA-1 and BETA-1 artificial witnesses are frozen; neither is a gravitational lift or thrust demonstration.
- DELTA1-00, 01 and 02 had already shown major action-specific energy and operator-rank problems.
- The existing November 20 journal called DELTA1-F0 **NEXT / NOT EXECUTED**. This became obsolete when the later F0 experiments and GRAVITY2 campaign actually ran.

## Work Performed

### 1. Original R3B response and action audit: DELTA1-F0

A scoped archive audit passed `31/31` checks. It reconstructed the previously prescribed interface and source/loading evidence without assuming a complete material action that the archive did not contain.

Weak neutral loading could initially improve a selected previously worst point. Under full loading, the worst point shifted and the sampled response became inward again. Therefore a success measured at one fixed point was not an acceptable finite-torus criterion.

An inverse compensation construction required effective source contributions approximately `3.04–3.25 m` from the origin, outside the declared onboard source radius of `2 m`. That result was a controllability warning, not a physical source located there.

The historical data did not uniquely separate direct neutral-matter trace, source relaxation, interface response and finite-domain effects. The precise dynamic material/source Jacobian was missing; fitting a compensating field was not a derivation of one.

### 2. F0A — Exterior dipolar structure and conditional polar-material control

The historical exterior electric multipole energy was approximately `99.999985%` dipolar in the examined basis. An optimistic polar-sphere control could access a similar angular mode.

For a restricted isolated-X curl test, the necessary threshold was

`epsilon*kappa/R**2 > 0.07692973043`.

This was not a solution of the fully loaded X/Y/material system. No experimentally calibrated microscopic polar material or complete source/support action was supplied. A jump in the trace coefficient with nonzero tangential X field can induce Y response and must be varied through the full action.

### 3. F0B — Restricted affine-solid mechanical preflight

- Representative induced ratio: `B_Y/E_X ≈ -0.08232375`.
- An admissible slip variation had negative work per unit volume: `-0.0019391448469490622`.
- A nonuniform leading quadrupole balanced certain bulk/surface residuals to approximately `7.24e-17` and `1.85e-17`.
- Reported focused verification: `23/23` checks.

These tests supported a restricted mechanical-balance calculation, not an experimentally realizable stable constitutive solid or full finite-source stationarity. The negative slip-work direction was a stability warning.

### 4. F0C — Reciprocal interface and nonconvergence controls

F0C compared portal-off, vacuum and several fully loaded cases. Portal-off response vanished; a prescribed vacuum axial trial was outward; all four recorded fully loaded trial grids had inward minima.

The normalized diagnostic `a_z/(c**2*q**2)` had units of inverse meters. Values were:

| Trial | Minimum (m⁻¹) |
| --- | ---: |
| Coarse loaded | -0.00072499 |
| `h=0.05 m`, `L=6 m` | -0.01066272 |
| `h=0.05 m`, `L=7.5 m` | -0.01005511 |
| Diagonal flipped, same resolution | -0.00737820 |

Flipping the discretization diagonal moved the worst point from approximately `(1.175,3.125) m` to `(0.825,2.975) m` and changed a sampled interior chord mean from `-1.00652e-5` to `+9.20105e-5`. The independent weak residual was approximately `9.063725670460845e-12`; verification recorded `25/25` independent checks.

The local linear system had been solved accurately, but the physically relevant minima and profiles were **not continuum-converged**. It would be incorrect to set a free normalization `q` to force the result to 1g.

Recorded F0C hashes:

- Science SHA-256: `3c671e54a44a23bd12d2fe2451aed6388bb3c4f6da37408d7abe54c808540f7`.
- Verification SHA-256: `bafc1cf1d415e33a6da251fade2a29b1497d456f8d3aff5316d4b95936bbd9c6`.

### 5. F0D — Uniform instability resistant to stiffness tuning

For the tested polarization constitutive model at `a=-0.35` with natural boundary conditions, the spatially uniform trial had zero gradient penalty and a negative second-variation curvature `<= -1/60` for every nonnegative stiffness. Increasing stiffness alone therefore could not stabilize that uniform mode *within the stated model*.

A separate circulating mode changed its sign at `kappa/R**2≈0.08077621695`. These are distinct mode questions; the circulating threshold cannot negate the uniform-mode obstruction.

**Verification caveat:** the available full test run was interrupted after `2,285` passing tests, at approximately 517.43 seconds. A completed full-regression closeout for F0D was not evidenced. Never label this stage `FULL_REGRESSION=PASS`.

### 6. F0E/R1 — Hypothetical surface penalty and switching cost

A hypothetical surface penalty removed the particular negative uniform direction only if `gamma/R >= 1/180`. At that boundary, the toroidal trial additionally required `kappa/R**2 >= 0.07601354721`.

Original F0E encountered a NumPy Boolean JSON-serialization failure. F0E-R1 repaired the serialization issue without rewriting the scientific failed attempt; the corrected run reported `35/35` checks.

Negative quartic/positive sextic potential choices could yield a bistable reduced model, but real material coefficients, switching dissipation, thermal modes, full dynamic spectrum and support-energy ledger were absent. No physically sourceable stabilization was certified.

### 7. F0F — Topological mixing is not Hilbert stress

For a metric-independent scalar `theta` in `int theta F_X wedge F_Y`, direct Hilbert stress from that topological term vanishes, although a nonconstant `theta` can change the X/Y currents. If `theta` depends on a metric or matter invariant, all hidden dependencies must be varied.

Under the declared static weak-GR, DEC and stress-separated stand-off assumptions, an illustrative ≥1g field at ≥1m demanded gravitating energy `U >= 3.301386465e27 J`. This is an assumption-scoped gravitational-stress bound, not a universal theorem against every possible new metric or field operator. Reported verification: `32/32` tests.

### 8. F0G — Isolated exterior Maxwell-dipole gravitational sign

For a positive-energy isolated dipolar exterior tail outside a radius `R=2m` with a 1m axial gap, the calculated axial weak-GR acceleration was inward. A 10 MJ illustrative tail gave `-1.503568252e-21 m/s²`; achieving inward magnitude 1g in this isolated tail would require approximately `6.522251309e28 J`.

A near-axis outward collar extended only about `0.08124 m`; it did not reach the target 1m stand-off. Reported tests: `41/41`.

- F0G science SHA-256: `c8e74278c73b4d74f43560f7dec275c8061ef3f83c33d52afe703a7360a91c1f`.
- F0G verifier SHA-256: `b2def664dae9363fffc4be1d9d6e145f94e6d6ec9b793d0f24d4e39a33cbd566`.

This is an *isolated exterior-tail* result. Interior source/support stresses were excluded and could in principle change a full solution; simply amplifying the failed exterior dipole cannot change its signed axial contribution.

### 9. GRAVITY2 action-miner and independent campaign

A new bounded Python source/action-mining platform was constructed to replace one-off unprioritized numerical work with reproducible, resource-capped candidate decisions. GRAVITY2's intended scope: protected parent inputs; exact operator/identity gates; physical source rank and response audits; negative controls; bounded worker scheduling; independent verification; immutable evidence and caching.

The implementation stages advanced through `GRAVITY2-00`–`08`, including runner/provenance, source action cards, convex/Hessian screening, portal polarization/Gauss response, 2D Hodge/Bianchi Y checks and periodic charged-source obstruction. This was platform construction, **not** an engine simulation.

Historical GRAVITY2 targeted/independent test counts progressed through `42/39`, `52/54`, `62/29`, `73/29`, `86/53`, `99/74`, `111/52` and `119/91` across corresponding stages and campaigns. These are not cumulative physical discoveries or replacements for a complete repository regression.

The four-gate source/reciprocity campaign classified:

| Gate | Verdict |
| --- | --- |
| `JPAIR_ACTION_INVENTORY` | `BLOCKED_ACTION_INCOMPLETE` |
| `JPAIR_CHARGE_CONTROL` | `SCOPED_CONTROL_ONLY` |
| `F0_PARENT_STATE_AUDIT` | `UNDERDETERMINED` |
| `F0_LOADED_RECIPROCITY` | `SCOPED_CONTROL_ONLY` |

The fresh and cache-reuse campaign successfully completed `4/4` gates, matched `6/6` historical input-source hashes, passed `119/119` targeted tests, `91/91` independent checks and `8/8` new provider tests. Fresh dispatch-loop timing was ~4.2465 s, verified reuse ~0.0473 s. This is cache efficiency for a fixed workload, **not** a measured 1000x acceleration of scientific discovery.

- Fresh campaign ID: `g2camp_20261121T165808Z_9aba14a5`.
- Fresh science SHA-256: `f08d998b05c7a23e0e800269af850763c032282a9f7dc81e78ae1a4a8dbcfe18`.
- Fresh verification SHA-256: `7dfec7290972f57527546c9eedd46482ff23145e837d95f273ed68b7f1e1c0a4`.
- Reuse campaign ID: `g2camp_20261121T165814Z_8fd90f83`.
- Reuse science SHA-256: `389df300ccb5550966a048fe1592b5f2134da774559b1200975bb6ea9a31e1e7`.
- Reuse verifier SHA-256: `5caaded64891138ff42ad1e49a678dec38e12bf2ab68ce488b90b753c3f997b2`.

## Result

The significant result is **an assumption-scoped physical-source controllability obstruction**, not a novel engine. The original R3B response could not be promoted from a field prescription to a fully derived stable source/material interface, and large numerical or artificial control spaces did not resolve this underdetermination.

GRAVITY2 was functional for controlled theorem/source campaigns and useful independent cache reuse, but had not discovered a real conserved onboard current, full Einstein source, complete Lorentzian stability or Earth–craft force.

## Verification

- **Analytical:** F0D uniform test direction, F0F fixed-theta Hilbert-stress identity and F0G isolated tail sign were scoped derived statements.
- **Numerical:** F0B `23/23`, F0C `25/25`, F0E-R1 `35/35`, F0F `32/32`, F0G `41/41`; F0D full suite interrupted. GRAVITY2 campaign targeted `119/119` and independent `91/91`.
- **Dimensional:** F0C normalized acceleration carries `m^-1`; do not interpret its coefficient as SI acceleration without an independently calibrated source.
- **Limiting cases:** Portal-off null, zero coupling, positive-energy exterior-tail sign, uniform constant-polarization mode and finite-boundary controls.
- **Literature comparison:** New complete literature/empirical comparison not established by these runs; physical promotion needs updated fifth-force, equivalence-principle, material, Maxwell and GR constraints.

## Falsification Attempt

Key attempts included source-off/portal-off controls; the shifted global worst point; diagonal-sensitivity test; varying radius/box; the stable-uniform-mode contradiction; source support outside hull; topological metric-stress separation and isolated dipolar exterior. None established a complete positive physical source. The existence of a small discrete residual must never be used to mask failed continuum or material closure.

No numerical optimizer convergence alone can disprove or establish physically realizable thrust or universal gravitational response.

## Claims Status

`CLAIMS.md` was **not evidenced as modified in this work**. Any future documentation revision must preserve the full negative evidence and label old artificial force claims correctly.

```text
DELTA1_F0_TO_F0G=EXECUTED_IN_SCOPED_RECORD
F0C_CONTINUUM_SOURCE_LOADING=NONCONVERGED
F0D_FULL_REGRESSION=INTERRUPTED_NOT_PASSED
F0G_EXTERIOR_AXIAL_SIGN=INWARD_IN_DECLARED_MODEL
F0G_INTERIOR_SUPPORT_STRESS=NOT_INCLUDED
GRAVITY2_CAMPAIGN=FOUR_GATES_VERIFIED
SOURCE_ACTION=INCOMPLETE
REAL_ONBOARD_SOURCE=NOT_DERIVED
EARTH_CRAFT_WHOLE_MOMENTUM=NOT_DERIVED
NEW_GRAVITATIONAL_LIFT=NO
NEW_PROPULSION_ENGINE=NO
```

## Open Questions

1. Which independently sourced action operator, if any, can alter the R3B reciprocal field response without merely fitting the interface field?
2. Can the actual finite charged material and supports enforce the needed boundary conditions while retaining positive constrained energy?
3. Can one derive the exact material/switching terms missing from F0E rather than choosing arbitrary stabilizing coefficients?
4. How does the physically correct full source/Einstein Hilbert stress affect the F0F/G partial bounds?
5. Can the full metric and X/Y exterior converge before any claim of force transmission?
6. Can GRAVITY2 identify a genuinely new operator under a tested sourceability, empirical/UV and energy ledger rather than ranking toy responses?

## AI Assistance

AI assistant used: **ChatGPT by OpenAI**.

AI assistance included model interpretation, source/action audit criteria, code and independent-verifier proposals, analysis of failed and scoped controls, build-plan methods and research strategy. User-supplied terminal outputs and original immutable artifacts remain authoritative. AI suggestions are not independent physical certification.

## Next Action

At the 2026-11-21 close, continue action-derived, resource-bounded source-response investigations; do not repeat closed F0 stiffness, mirror, topological-stress or dipole-amplitude tricks. Subsequent G01-S/T/U and EPSILON experiments actually ran on November 22 and are documented in distinct following entries.

**Future resumption after the November 22 strategy pivot:** treat this journal as a frozen antigravity obstruction ledger. Do not automatically restart DELTA1-F0 or GRAVITY2 campaign generation. The newly active R3B Engine must explicitly justify its own source, momentum and energy transfer before reusing any F0 control.
