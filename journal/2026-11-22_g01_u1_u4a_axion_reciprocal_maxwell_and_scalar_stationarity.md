# Research Journal — 2026-11-22

## GRAVITY2 G01-U1 through U4A: Axion-Like Source, Reciprocal Maxwell Suppression, Exterior Convergence Failure, and Fixed-Profile Scalar Stationarity

## Objective

Test a genuinely different proposed scalar/X/Y coupling capable of giving a finite neutral torus an outward *universal-metric test response*, then stress that promising frozen-field result with reciprocal Maxwell equations, angular structure, exterior-domain refinement and a projected scalar Euler–Lagrange stationarity requirement.

The experiment must distinguish a scalar-only, physically prescribed field configuration from a self-consistent finite source. It must not equate a scalar conformal fifth-force signal with Einstein gravitational repulsion or whole-spacecraft lift.

## Starting State

The original R3B 1.5429162116460216 J mixed-field capacity remained a prescribed reference with severe loaded negative acceleration. The G01-T3 ten-mode control basis was excluded by an exact sampled-model dual at 10 MJ, but that theorem did not apply to a newly formulated dynamical pseudoscalar operator.

The proposed U1 route was therefore new in action content: a pseudoscalar sourced by a mixed two-U(1) invariant with an even universal metric coupling to ordinary neutral matter. In every comparison, source currents, charged shell material, X/Y reciprocal equations and full Einstein force are independent obligations.

## Work Performed

### 1. G01-U1 — Proposed local mixed-axion action

The **hypothetical** covariant action ingredients were:

- Einstein–Hilbert gravitational action.
- Two protected Maxwell-like `U(1)_X` and `U(1)_Y` sectors.
- A canonical massive pseudoscalar `phi`, inverse range `mu=1 m^-1`.
- A mixed operator schematically `phi * F_X *dual(F_Y)`, equivalently involving `E_X dot B_Y` in a suitable static frame.
- Universal neutral-matter physical metric schematically `g_tilde = exp(beta*phi^2) g`.
- Potential charged material/source supports, not actually constructed in the U1 run.

The mixed Maxwell pseudoscalar may integrate to a topological null under suitable localization/no-monopole assumptions while remaining **locally nonzero**. The source uses angular content, so radial-only reductions do not automatically preserve the induced scalar field.

A shell of radius 2m had a prescribed X electric dipolar surface-charge profile and Y azimuthal current/dipole field; the on-shell charged-shell material action was not solved.

The scalar profile was decomposed into spherical harmonics with `f0(r) + f2(r) P2(cos theta)`. This nontrivial `ell=2` content was essential for the reported finite-torus force sign.

The finite payload was a 1kg torus with major radius 1m, minor radius 0.2m, center distance 3.2m. The smallest sampled shell-to-payload gap was approximately `1.00000016515 m`.

### 2. G01-U1 — Conditional positive scalar-only result

Selected model parameters:

- `beta = 1.998780722774814e23`.
- Axion scalar amplitude `A = 2.269703885395593e-18`.
- Illustrative mixed-source calibration `kappa = 3.267847142631918e-17 m/J`.
- Canonical scalar kinetic/mass-energy term `7,333,333.333333331 J`.
- Sampled minimum outward scalar-metric acceleration: **`+10.781595872566479 m/s²`**.
- Number of sampled torus points: `82,944` (`81 x 1024`).

The scalar-only loaded numerical check used a prescribed torus density and a linearized local scalar backreaction rather than a fully stationary physical neutral solid/fluid. Scalar mesh refinement `h=0.16,0.10,0.08m` converged to approximately `10.7824236428`, `10.7818973119`, `10.7815958726 m/s²` at the sampled minimum. The last-two relative difference was `2.7957907691944506e-5`. The scalar-correction box comparison at h=0.08 m was approximately `1.0554682683405758e-9`; the radial scalar-energy shape difference was approximately `4.890415674196902e-6`.

**Those convergence figures certify only the restricted frozen-X/Y scalar correction.** They do not establish reciprocal Maxwell convergence or a physical source.

`max |beta*phi^2| ≈ 3.213297460832022e-16` is a small conformal exponent, but the derivative `beta*phi` and source/material couplings can still be enormous. The computed reciprocal gauge control `R |grad theta|` was approximately `8,501,043.9436`, so neglecting field response was not a controlled small-coupling approximation.

One heuristic perturbative field-feedback estimate gave an electromagnetic contribution near `13.1164 MJ`, bringing scalar plus estimated gauge response near `20.4497 MJ`. This was *illustrative*, not a rigorous source-energy lower bound.

U1 science and provenance:

- Result directory: `results/gravity2/g01u1_axion_20261122T052145Z_7105`.
- Science SHA-256: `0f5b138a22d9da0088cdb9d6c2bfdcfbb046603845447d250878809c454616c3`.
- Radial reference NPZ SHA-256: `cfe54027edcd6a33532faa5eec138455bc35a89193f9b3af1d4cd4f5bf727999`.
- Producer SHA-256: `4b6b6001ffbd5c80f90cc8d078704e41161275cebd3095e36308c62bff833816`.

Physical survivors: `0`. Real hidden current, supports, full Einstein metric and whole-craft force were not established.

### 3. G01-U2 — Restricted radial reciprocal Maxwell dipole

U2 allowed part of the prescribed shell Maxwell system to respond to the axion-like background. It was restricted to radial/dipolar source modes and did **not** include the original U1 scalar `f2(r)P2` angular response in the necessary form. Thus it was deliberately a scoped reciprocal stress test, not a full falsification of U1.

The source-induced pseudoscalar projection was strongly suppressed/collapsed in the restricted radial sector; no 1g physical survivor was found. The correct interpretation is failure of this **radial-only reciprocal realization**, rather than proof that every fully angular scalar source is impossible.

- U2 science experiment: `G01-U2-RECIPROCAL-MAXWELL-RADIAL-DIPOLE-FORK`.
- Result science SHA-256: `a91e6c325e9a12f2aff4b28b7fc7dede7a95644fb9776fba7fc0d1dd4b0c1d2b`.
- Source SHA-256: `950cc136c513ca3d37f171341b2b36678f5f864554fee784df328cca6562c8d3` (recorded from contemporary notes; recheck live repository before reuse).
- Full repository regression: `NOT_RUN`.

### 4. G01-U3A — Full-angular reciprocal static Maxwell preflight

U3A restored the `f0+f2P2` scalar background and examined Maxwell multipoles `[1,3]` and `[1,3,5]` across several grids and boxes, with the scalar still frozen and the shell source currents prescribed.

The solved **linear static Maxwell subsystem** had residuals of order `1e-15`, but the physical source projection and electromagnetic field energy changed dramatically under independent refinement:

| U3A diagnostic | Observed variation |
| --- | ---: |
| Radial grid energy comparison | ~52.20% |
| Angular truncation energy comparison | ~23.28% |
| Box energy comparison | ~16.59% |

Representative projected source ratios moved from approximately `0.1918043` on one coarse trial to `0.00645587`, `0.00699751`, and `0.000910854` on other trials. The nonconvergence prevented promotion regardless of tiny linear solve residual.

The scalar local EOM, charged-source material, Lorentzian modes and metric backreaction were not solved.

- U3A science SHA-256: `bd1c3226646f0e82ef14ab4826e00b1cbb9bdeedb9f05a4d9dbf7069151d8fd6`.
- U3A producer SHA-256: `a894b741012e8445f711b3ed4fde3a881c6f84391ee6221f479fdcd401a0f46a`.
- Physical survivors: `0`.

### 5. G01-U3B — Extended nonuniform exterior

U3B extended radial boxes to 64m and 80m, using a uniform near field to 8m and 96 geometrically spaced exterior cells. Independent comparisons used near-grid spacing `h=0.2m` or `0.1m`, and angular truncations `ell_max=5` or `7`.

Even at the enlarged radius, the scalar/Maxwell coupling was extremely stiff (`log10` condition indicator approximately `30.63` in the recorded large-scale estimate). The maximal inner-source `|theta|` was ~45 million. Some far-boundary `|theta|` values diminished, but exterior stress and source projection were still not demonstrably converged.

Energy diagnostic differences:

- Box 64m→80m: `3.715677%`.
- Inner radial spacing refinement: `8.139961%`.
- Angular truncation refinement: `16.561149%`.

The four normalized source projections were:

| Box, h, ell | Recorded ratio |
| --- | ---: |
| `64m,0.2m,5` | `-0.06142833286298907` |
| `80m,0.2m,5` | `-0.0667144573253197` |
| `80m,0.1m,5` | `+0.0007254849805277547` |
| `80m,0.1m,7` | `-0.0033048915524157276` |

Constant-theta topological-null and zero-coupling controls were included. U3B's verdict was `HOLD_NUMERICAL_NONCONVERGENCE`. There were no physical survivors.

- U3B science SHA-256: `44f14ce4ba14e46d3fd4816d9fad2395fd1fef133a35894e884ad8ace9335126`.
- U3B producer SHA-256: `103416a4b816af2b4b6a586f135eb0dafc945e1a1c3734315afa6b3352c535ff`.
- U3B full regression: `NOT_RUN`.

### 6. G01-U4A — Exact frozen scalar stationarity and conditional energy

U4A asked whether the original U1 fixed scalar profile could satisfy its own local scalar equation after inserting the reciprocal U3B Maxwell source, rather than merely passing a test-particle force sign.

For a fixed profile `f`, the scalar equation was written

`(-laplacian + mu^2 + delta_m^2) f = P_loaded`.

The original parent satisfies

`(-laplacian + mu^2) f = P_0`.

Consequently, multiplying by `f` and integrating over the declared volume gives the necessary projected identity

`<f,P_loaded>/<f,P_0> = 1 + <delta_m^2 f,f>/<f,P_0>`.

For the tested positive matter-loading term and positive parent overlap, the required ratio was

**`1.000001486546953`**.

The four measured U3B ratios, listed above, did not meet it. The deficits were:

`1.061429819409942`, `1.0667159438722729`, `0.9992760015664254`, `1.0033063780993687`.

The 1kg neutral-torus quadrature passed in this restricted model. But because the U3B parent gauge fields were nonconverged, U4A proves **a scoped incompatibility of the chosen frozen scalar profile with these recorded gauge trial fields**, not a theorem against all reshaped jointly solved scalar/Maxwell sources.

A conditional weak-feedback fixed-profile energy estimate was:

- Scalar reference: `7,333,333.333333331 J`.
- Added modeled electromagnetic feedback: `11,129,633.202875158 J`.
- Combined conditional cost: **`18,462,966.536208488 J`**, above the strict 10 MJ limit.

This is not a general source/energy lower bound because both the shape and the reciprocal field families were constrained. A reported operator scale near `15.475963 eV` is not a demonstrated UV completion, cutoff, naturalness or laboratory consistency result.

- U4A science SHA-256: `5e29b2d389fee45ff4a3098b29f1ac3c8bd436cb678d9c8df2c24535e14450f5`.
- U4A producer SHA-256: `8a07597deb37d1d0bb5ccf92583f3a355b3fa78856b864e4711af3d5d1`.
- U4A parent U3B science SHA-256: `44f14ce4ba14e46d3fd4816d9fad2395fd1fef133a35894e884ad8ace9335126`.
- Physical survivors: `0`; full regression: `NOT_RUN`.

## Result

U1 found a **conditional positive scalar-metric torus signal** under prescribed Maxwell shell fields, not a true physical Einstein or spacecraft solution. U2 showed a restricted radial-only reciprocal failure; U3A/U3B restored angular fidelity but failed continuum/exterior convergence; U4A quantified a direct frozen-profile stationarity mismatch and an assumption-scoped energy overrun.

The key transferable discovery is not a 7.3 MJ antigravity device. It is the identification of the missing independently sourceable response and the need to co-vary scalar and Maxwell fields without imposing the desired scalar profile.

## Verification

- **Analytical:** Mixed-invariant topological-null interpretation, angular `f0/f2` decomposition and U4A projection identity within stated boundary/source assumptions.
- **Numerical:** U1 scalar subproblem refinement; U3A/U3B Maxwell linear system residuals; U3B strong nonconvergence; U4A mass-quadrature and source-overlap checks.
- **Dimensional:** Acceleration `m/s²`, stand-off `m`, scalar and feedback energy `J`, canonical coefficient scales; calibration from the original 1.54 J R3B geometry does not establish equivalent source geometry.
- **Limiting cases:** Zero coupling and constant-theta nulls, radial-only `f2=0` comparison, box/angular/radial refinements, frozen-to-loaded source-overlap discrepancy.
- **Literature comparison:** No independently confirmed phenomenologically acceptable axion/pseudoscalar source material, strong-coupling limit, universal metric or UV theory was provided.

## Falsification Attempt

The project attacked the most flattering U1 signal by requiring the Maxwell fields to respond to the same mixed action, restoring missing angular components, extending the exterior box, refining the mesh, and checking scalar stationarity instead of only output acceleration. Every stronger gate left zero physically qualified survivors.

Do not claim that the angular U3B Maxwell nonconvergence itself establishes a universal no-go; it instead forbids treating U4A's profile-specific mismatch as complete theory falsification. Do not let a very small static linear-system residual substitute for actual continuum convergence.

## Claims Status

`CLAIMS.md` was not evidenced as changed. Freeze classifications:

```text
G01_U1_OUTWARD_SCALAR_METRIC=CONDITIONAL_FROZEN_MAXWELL
G01_U1_7P333MJ=SCALAR_ONLY_NOT_COMPLETE
G01_U1_MICROSCOPIC_SOURCE=NOT_DERIVED
G01_U2_RADIAL_RECIPROCITY=RESTRICTED_NEGATIVE
G01_U3A_STATIC_MAXWELL_EOM_RESIDUAL=SMALL
G01_U3A_PHYSICAL_CONVERGENCE=NO
G01_U3B_EXTERIOR_CONVERGENCE=NO
G01_U3B_SOURCE_RATIO_SIGN=UNSTABLE_ACROSS_GRIDS
G01_U4A_FROZEN_PROFILE_STATIONARITY=FAIL_IN_RECORDED_TRIALS
G01_U4A_ENERGY_LT10MJ=NO_IN_FIXED_PROFILE_WEAK_FEEDBACK_ESTIMATE
G01_U4A_GENERAL_ACTION_NO_GO=NO
FULL_SOURCE_EARTH_CRAFT_GRAVITY=NOT_DERIVED
PHYSICAL_SURVIVORS=0
```

## Open Questions

1. Which stable, conserved source supports produce the mixed X/Y pseudoscalar invariant in an actual finite apparatus?
2. How should the scalar profile respond when both X/Y fields, source currents and neutral material are simultaneously varied?
3. Can a numerically well-conditioned, continuum-converged joint solve be constructed without an uncontrolled enormous coupling?
4. Can local proper-force, Einstein/metric geometry and field/support momentum be distinguished and independently tested?
5. Does any physically calibrated field stay within complete strict `<10MJ` operating energy, including source and off-state?
6. Which angular and Fourier components dominate the missing scalar source, and can a healthy auxiliary field source them independently?

## AI Assistance

AI assistant used: **ChatGPT by OpenAI**. AI-assisted work included alternative action formulation, calculation and numerical-solver design, momentum/source projection analysis, independent-check protocols, energy interpretation and preservation of the executed logs/hashes. AI derivation is not independent physical verification.

## Next Action

At the historical experimental close, open a small theorem-first auxiliary source-controllability branch rather than launch another expensive U3B box expansion. This became **EPSILON-1**, documented in the following journal. At the subsequent November 22 strategic freeze, hold U1–U4A and their immutable evidence pending a genuinely new physical operator and actual full source variation.
