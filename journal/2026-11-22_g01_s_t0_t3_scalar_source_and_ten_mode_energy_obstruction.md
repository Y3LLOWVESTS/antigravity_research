# Research Journal — 2026-11-22

## GRAVITY2 G01-S and G01-T0–T3: Conditional Scalar Source, Exact R3B Multipole Control, and the 10-MJ Dual Obstruction

## Objective

Investigate whether a finite physically plausible new source response, or a richer finite X/Y field-control basis, can overcome the historical R3B reciprocal-loading failure while remaining compatible with the strict antigravity objective: at least 1g outward over the complete neutral 1kg torus at at least 1m genuine stand-off and strictly less than 10 MJ complete operating energy.

Determine separately whether a mathematical control space is capable of the desired response and whether a real source can actually produce it. Avoid treating an optimizer success, sampled near-zero force, low prescribed field energy or a conditional ground force as a physically realized gravitational lift.

## Starting State

- Original R3B prescribed mixed-field capacity: `1.5429162116460216 J`.
- Historical loaded R3B result remained inward: worst fine-grid value `-129.67185782242464 m/s²`; coarse-grid signed minimum `-46.40607408464625 m/s²`.
- The previous DELTA F0 studies documented missing source/material action, spatial-control and stability constraints.
- GRAVITY2 had established a bounded science-workflow with immutable results and negative controls; its infrastructure did not imply that any source-to-gravity candidate survived.
- The existing R3B source geometry and X/Y action were to remain locked in comparisons unless a genuinely new physical hypothesis was explicitly introduced.

## Work Performed

### 1. G01-S — Source-dependent scalar capacitor-screen

G01-S screened `24,200` finite-range/onset/radius source parameters, including a massless control. This was a **preflight atlas**, not 24,200 coupled spacecraft or Einstein simulations.

One hypothetical source-dependent nonlinear hidden-carrier/electrostatic capacitor scalar family produced two *conditional* positive neutral-torus sampled minima:

| Screened case | Conditional outward sampled minimum | Independent calculation |
| --- | ---: | ---: |
| Lower representative | ~`60.11179 m/s²` | ~`60.13804 m/s²` |
| Upper representative | ~`437.90449 m/s²` | ~`438.60598 m/s²` |

The lower example yielded an illustrative modeled ground-reaction/craft-coordinate force of approximately `30,165 N` in its idealized ground/source electrostatic system. That is not proof of full Earth-down/whole-craft-up Einstein gravity or a net propulsion system.

The lower-case **modeled active static energy increment** was approximately `7.472835 MJ`, decomposed into electric `5.31613 MJ`, scalar `2.12377 MJ` and conformal rest increment approximately `0.03294 MJ`. The upper case was approximately `7.734019 MJ` in its modeled accounting.

The remaining arithmetic margin to 10 MJ did not include real charged material, source supports, operating cycle, actual current-generation cost, experimental constraints, full metric backreaction or losses. The model was therefore **conditional**, even where its computed source response was strong.

The concentric ideal capacitor had zero exterior X electric field in the specified reference geometry and did not provide R3B's exterior Y magnetic structure. Consequently, its scalar positive signal could not simply be transplanted into R3B as the same action/source state.

### 2. G01-T0/T1 — Exact finite-shell multipole response

G01-T0/T1 evaluated ten ideal boundary-supported exterior field controls on a radius-2m shell:

- X electric multipoles and Y magnetic multipoles for `ell = 1,2,4,8,12`.
- Both original coarse and fine R3B signed and loaded configurations.
- Positive canonical modeled field energy on the shell basis.
- Linearized response, exact quadratic/bilinear response and reversed-control negative cases.

**Preserved initial baselines:**

| Grid h | Exact loaded minimum | Modeled field energy | Sampled stand-off |
| --- | ---: | ---: | ---: |
| `0.075m` | `-46.40607408464625 m/s²` | `1.4433196404756485 J` | `1.0364452901376788m` |
| `0.050m` | `-129.67185782242464 m/s²` | `1.5211390382733163 J` | `1.0041637771601337m` |

The ten-mode response matrix had algebraic rank 10 on both sampled grids. That says only that the ten prescribed control profiles are linearly independent in that numerical representation; it does **not** establish ten independent physically sourceable, Lorentzian-healthy degrees of freedom.

Linearized optimization misleadingly predicted nearly zero inward acceleration at certain controls. When the exact bilinear force was re-evaluated, the best representative minima remained approximately `-11.58 m/s²` coarse and `-32.42 m/s²` fine. Roughly 75% mitigation of the adverse initial response is **not** outward antigravity.

A direct sparse reference check yielded relative residual approximately `4.592e-15` and acceleration discrepancy approximately `1.024e-10 m/s²` in the declared static subproblem.

Scientific artifact and producing source:

- Result directory: `results/gravity2/g01t_t0t1_20261122T040953Z_21912`.
- Science SHA-256: `e7a265f3963131e2f0a06e2d0f04c688658bad68cb00bfb49b5ec91a90cc4e39`.
- Producer SHA-256: `57efe5406cd8dde4a9a040a102e9781c2fbb22508fe323d5465ea0928921a3b0`.

A full repository regression attempted in this portion of the work was interrupted. A partial period/progress log must not be represented as a completed full-suite pass. Physical X/Y surface charges and currents were still unspecified.

### 3. G01-T2 — Exact quadratic optimization and sampled energy bounds

The next control test used the **exact** bilinear field response, avoiding the tangent-only error identified by T0/T1. It found a near-zero but still inward best sampled acceleration in the tested mode family, with an approximately `18.97 kJ` model-side necessary bound from a specific optimistic optimization.

The early single-point dual bounds ruled out ≥1g at modeled field-energy caps of 2, 10, 100 and 10,000 J for the sampled finite R3B basis. At 10 MJ, the loose single-point bound was **inconclusive**, so it could not be cited as either success or a 10 MJ exclusion.

Selected original screening bounds on the sampled worst point:

| Cap on modeled field energy | Optimistic single-point joint bound (m/s²) |
| --- | ---: |
| `2 J` | `0.00061015995716123` |
| `10 J` | `0.0047852567982486` |
| `100 J` | `0.051449002437458` |
| `10,000 J` | `5.1707998907935` |
| `10,000,000 J` | `5169.2782748526` (inconclusive) |

The last number is an *upper bound*, not a reachable physical acceleration or a proposed engine output.

### 4. G01-T3 — Stronger 10 MJ multi-point dual certificate

G01-T3 replaced the too-loose single-point upper bound with a multi-point dual on **48 fine-grid target samples** and all ten original ideal shell controls, keeping the frozen R3B coupling and positive canonical modeled field energy.

For nonnegative normalized weights `w_i`, the exact inequality is

`min_i a_i(u) <= sum_i w_i a_i(u)`.

With a nonnegative dual multiplier `lambda`, and `M=lambda*K - sum_i w_i*Q_i` positive definite for the chosen quadratic acceleration forms, completing the square supplies a global upper bound for every control vector with `E(u)<=C` in this finite basis.

**Recorded certified parameters and result:**

- Modeled field-energy cap `C=10,000,000 J`.
- Dual multiplier `lambda=5e-7`.
- Minimum eigenvalue of the dual matrix `4.621701779603397e-7` (>0).
- Sum of nonnegative weights `1.0`.
- Upper bound on the minimum acceleration: **`4.999999576116771 m/s²`**.
- Required target: **`9.80665 m/s²`**.
- Therefore `NO_1G_CANDIDATE` for *this frozen ten-mode sampled problem at a modeled-field cap of 10 MJ*.

Independent checks included a different Cholesky factorization, parent hash and matrix-weight positivity tests. The result is stronger than failure of an optimizer to find a witness. It is **not** a no-go for different physical operators, other source geometries, full angular scalar degrees of freedom, the complete charged material/Einstein system, or all hypothetical propulsion schemes.

Scientific provenance:

- Result directory: `results/gravity2/g01t3_certificate_20261122T044728Z_74926`.
- Science SHA-256: `1cfe07d9c3e10a21ac01243b2288d6d4380d0e906768906166165681e9c7e4eb`.
- Corrected producing source SHA-256: `0a937619437505577a13c3c63ca300cb42f0f7ad0797fe28090bf6edd07ab247`.

The **first attempted T3 run** stopped due to a truncated 41-character parent SHA literal; the corrected run succeeded. Do not erase the initial provenance failure or confuse it with the physical theorem result. A post-hoc tighter dual estimate at a different multiplier was not a separately archived user-executed certificate and must not supersede the accepted 4.999999576 bound.

## Result

G01-S demonstrates that a source-dependent response can give a promising *conditional fifth-force-like* loaded sign in an ideal capacitor, but provides no original R3B X/Y source transfer or full gravity. G01-T0/T1 and T2 show that exact reciprocal loading defeats simplistic linearized control optimism. G01-T3 gives a **scoped analytical-numerical 10 MJ exclusion** for the finite original ten-mode shell basis.

These are complementary constraints, not evidence of a physical engine. They narrow the action/operator search and justify moving to different, explicitly formulated source physics rather than reoptimizing the same ten control modes.

## Verification

- **Analytical:** The weighted-minimum inequality and positive-definite quadratic dual provide a global bound within the finite T3 model.
- **Numerical:** Source-locked T0/T1 signed baselines; static sparse residual checks; T3 independent Cholesky/weight/eigenvalue reconstruction; science/producers SHA-256 references above.
- **Dimensional:** Acceleration reported in `m/s²`; modeled field-energy caps in J. The field cap is not the complete operating energy of any source-supported device.
- **Limiting cases:** Reversed controls, zero shell amplitudes, both original R3B grids, low-energy and 10 MJ dual limits.
- **Literature comparison:** No experimental fifth-force compatibility or exact material charge/current model was established. No new physics claim is supported by these calculations alone.

## Falsification Attempt

The project attempted to replace first-order control fitting by exact bilinear response, increase the finite basis to ten multipoles, test two grid scales, reverse source controls and derive a model-wide upper bound independent of optimizer termination. The exact force remained inward and the 10 MJ dual closed the chosen sampled basis.

A failure in a finite basis does not exclude a different, genuinely sourced field theory. In particular, no solver in this series varied all source material, X/Y fields, Einstein geometry, Earth and supports from one action.

## Claims Status

`CLAIMS.md` was not evidenced as updated. Suggested permanent classifications:

```text
G01_S_CAPACITOR_SCALAR=CONDITIONAL_SOURCE_MODEL
G01_S_GROUND_FORCE=IDEALIZED_NOT_GRAVITY_OR_THRUST
G01_T0_T1_TEN_SHELL_MODES=EXECUTED
G01_T0_T1_EXACT_FORCE=STILL_INWARD
G01_T2_EXACT_QUADRATIC=NO_OUTWARD_1G_WITNESS
G01_T3_TEN_MODE_10MJ_DUAL=SCOPED_EXCLUSION
G01_T3_SOURCE_MATERIAL=NOT_DERIVED
R3B_LOADED_NEGATIVE_REFERENCE=PRESERVED
FULL_REGRESSION_WHERE_INTERRUPTED=NOT_PASSED
TRUE_ANTIGRAVITY_OR_NET_THRUST=NOT_ESTABLISHED
```

## Open Questions

1. Can a new source-derived operator evade the ten-mode bound without smuggling in arbitrary field currents or boundary work?
2. What physical source/current topology yields a nonzero transverse Y response after loading?
3. Can any independently identified source provide exterior fields with converged flux and finite material supports?
4. Does a completely varied neutral-matter action preserve an outward sign throughout the torus, not just sampled points?
5. Can G01-S's nonlinear source mechanism be embedded in an actual original R3B X/Y action? The capacitor's symmetry currently blocks direct substitution.
6. Does any surviving model satisfy empirical, UV and complete operating-energy limits?

## AI Assistance

AI assistant used: **ChatGPT by OpenAI**. The assistant assisted with the derivation of bounded source-control screens, interpretation of conditional capacitor forces, exact bilinear response, dual-certificate design, code generation and independent validation protocols. The user's executed scientific artifacts and solver source remain the evidentiary record. Independent experimental confirmation does not exist.

## Next Action

At the historical close, test one physically motivated new coupled source mechanism instead of enlarging the closed finite-shell parameter scan. The subsequent G01-U1–U4A axion/pseudoscalar work is recorded in the next dated journal. On later resumption, the T3 result should be treated as a locked **basis-specific** no-go, not reopened by changing optimizer seeds.
