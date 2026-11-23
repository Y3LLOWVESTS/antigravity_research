# ANTIGRAVITY_RESEARCH — GRAVITY2 BUILD PLAN

## R3B-ACTIONMINER: Bounded, theorem-first Python source-to-gravity discovery engine

**Proposed repository file:** `gravity2buildplan.md`  
**Status:** DESIGN / IMPLEMENTATION PLAN — **NOT AN EXECUTED MINER OR A PHYSICAL RESULT**  
**Prepared:** November 20, 2026 (America/Chicago)  
**Program ID:** `GRAVITY2-R3B-ACTIONMINER`  
**Primary candidate:** historical `032H17A12D1R3B`, preserved, **not presumed physically valid**  
**Scientific authority:** `RESEARCH_BUILDPLAN.md` for physical strategy; current `ARTIFICIAL_BUILDPLAN.MD` for DELTA-1/F0 and action-bridge decisions; `AGMINER_BUILDPLAN.MD` for historical failures and mining methodology; `FORMATTING_AND_CODE_STANDARDS.md` for documentation and code; actual immutable source/JSON/SHA/logs outrank prose.  
**Document relationship:** This is a new subsystem implementation plan. It does **not** overwrite or silently supersede the existing physical-research buildplans or historical results.

> **Mission:** Build a restartable, local Python program that investigates a small, explicitly defined family of physically motivated **same-action completions** of R3B. Spend computation on deriving or falsifying the missing **real source → X/Y fields → universal physical metric → neutral payload → Earth/craft reaction** chain. Use fast theorem and sourceability gates before numerical solvers, limit wall time/memory/disk, preserve failures, and never convert a prescribed-field capacity into a device claim.

---

# 0. Immutable scientific baseline and truthful objective

## 0.1 What is and is not established

| Anchor | Preserve exactly | What it establishes | What it does **not** establish |
|---|---|---|---|
| `R3B` | `1.5429162116460216 J` | Original prescribed mixed-field **capacity** in its reference geometry | Physical current/source, stable loaded field, real Einstein response or complete operating energy |
| `R3X1` / strong load | Fine-grid preloaded approximately `+9.80665 m/s²`, `1.537764 J`; **loaded `−129.67185782242464 m/s²`, `1.5211390382733165 J`** | A severe adverse reciprocal-loading result in the recorded strong-loading model | A converged no-go against every possible new source action |
| `DELTA1-02` | `3,304/3,304` full regression, `10/10` focused at its checkpoint | One-invariant reciprocity; a simple extra $F_Y^2$ direction nearly collinear with the original payload gradient | An independent physical source or gravitational lift |
| `006D` | $C=23.591586299249$ | Historical finite positive-energy, conserved linearized-GR locally outward field witness | A practical low-energy source; its energy scales catastrophically with $1/G$ |
| `PH16-04R2` | `2,943/2,943` at checkpoint | Coupled finite-lattice canonical stationarity with source/field/fluid variables | Full Lorentzian dynamics, continuum Einstein gravity or spacecraft force |
| `F0C` | Scoped trial, independent `25/25` | Underdetermined physically selected polarization mode / inconclusive continuum | A loaded gravitational survivor |
| `F0D` | Exact quadratic negative trial; APPLY success | Specific natural-boundary quadratic off-state obstruction | Completed independent verification/full regression; universal R3B failure |
| `F0E-R1` | `35/35` independent checks | Necessary surface/stiffness and conditional switching **trial** conditions | Microscopic source coefficients or complete stability |
| `F0F` | `32/32` independent checks | Fixed-scalar topological four-form has zero **direct** Hilbert stress; conditional GR energy obstruction | The full R3B metric coupling is zero; a universal device no-go |
| `F0G` | `41/41` independent checks | Isolated exterior Maxwell dipole-stress contribution has inward sign at $\ge1$ m clearance | Complete conserved Einstein source or Earth/craft lift |

**Current physical maturity:** approximately **37% as a heuristic**, **not** probability or algorithmic score. Software construction and additional tests do not automatically increase it. **No complete physical gravity model, 50% milestone, demonstrated whole-craft lift or certified $<10\,\mathrm{MJ}$ engine exists.**

**Evidence integrity:** `F0D`'s long full regression was interrupted; `F0E-R1`, `F0F` and `F0G` explicitly did **not** run the full suite. An independent focused PASS is not a full-regression PASS.

## 0.1A Exact parent locks for initial implementation

The following source/result SHA-256 strings come from the supplied repository codebundle, current buildplan or user-run console evidence. They are **expected locks**, not permission to fabricate an absent file. GRAVITY2 must inspect and hash the actual repository files at runtime; mismatch or missing evidence is an explicit stop.

| Parent input | Expected SHA-256 | Initial use |
|---|---|---|
| `src/antigravity_research/agminer/hook17_fdual_f_global_mirror_prefight.py` | `aa8f196fcae6a63405181ca62674e22ac67e5da88303759bdd99d25716fa2263` | Original R3B source/geometry/energy |
| `src/antigravity_research/agminer/hook17_f2_strong_payload_loading_rescue.py` | `e1296794c25a4d0e4d5634c7e7d543a0b488b8d2a1963afcf7878bea1c1b99e7` | Original strong-loading source class and torus density |
| `src/antigravity_research/delta1/delta1_02_r3b_portal_rank.py` | `04d8d669adb1e4b067e75a285dd13f0fbaa6bbd879090b88e850a277baca9395` | Local reciprocity and rank comparator |
| `DELTA1-02` scientific JSON | `3bd142aacf1b068268e0a4322274382f66c7f249035db0c25a8710d690774fc3` | Prior scientific checkpoint |
| `DELTA1-02` independent JSON | `db7be8e1399e0bf04db1ca21f87fd0ed5c8e2807cfcb438c278fa817993c8ded` | Prior verification |
| `F0C` scientific JSON | `3c671e54a44a23bd12d2fe2451aed6388bb3c4f6da37408d7abe54c808540f7f` | Underdetermined source mode control |
| `F0D` scientific JSON | `2db67eea46adf84327c14c0177c1863148893217a377ac67a1f3a39ec9cb6465` | Quadratic obstruction trial |
| `F0E-R1` science / independent JSON | `bdc6d1b27befa108cc982d392e8bf265c17b96f814f54810d49b180d0dc834d4` / `63ca7c612bf5d39e6fa238c9a992b31500f3067e090e3cc43047ca7d87a8503e` | Conditional boundary and switching gates |
| `F0F` science / independent JSON | `145f7db67b440cbd5e5f0c2023ccb1ac7ad9d2151b777f459e1c2fc3964c9e73` / `db52ae4365636ec72cb399fa380c13d5333d98db64aaa8d03e5c8e07e0376c50` | Topological metric and conditional SI bound |
| `F0G` science / independent JSON | `c8e74278c73b4d74f43560f7dec275c8061ef3f83c33d52afe703a7360a91c1f` / `b2def664dae9363fffc4be1d9d6e145f94e6d6ec9b793d0f24d4e39a33cbd566` | Exterior-dipole stress negative control |

`F0C`–`F0G` live under separate `results/data/delta1_f0.../` run directories on the user's Mac, **not** necessarily inside the older codebundle. The November 20 12:27 CST codebundle predates the evening F0 runs; never infer that their absence from that bundle means they were not executed. The user's F0D independent/full-suite closeout was interrupted and must remain explicitly incomplete.

## 0.2 Frozen target

- Onboard, finite **physical** source, including actual currents, confinement, supports, hull and power system.
- Universal gravitational/metric response of an **electrically neutral 1 kg finite torus**.
- **At least $9.80665\,\mathrm{m/s^2}$ outward at every material point** of that torus, not merely one sample or its center.
- **At least 1 m true separation** from the entire source/support material and relevant bounding surfaces; independently track field stress that may extend across the gap.
- Independently derive **Earth down, the entire craft up** including source/hull/support/power/payload/field momenta and external flux. An internal neutral-payload force does not qualify.
- Complete, non-double-counted operating energy **strictly below $10,000,000\,\mathrm{J}$**; equality fails. Distinguish operating energy, total gravitating rest energy and prescribed-field capacity.
- Gauge/Ward/Noether/Bianchi identities; real-source conservation and finite support; constrained mode health; continuum/exterior convergence; SI, empirical, quantum/UV and causal consistency.

## 0.3 Success definition for GRAVITY2 itself

**Software success is different from physics success.** A successful *first version* of the miner can independently reconstruct the parent evidence, enumerate a *small* admissible source-action library, derive candidate-specific equations and stop at the earliest decisive obstruction, all within a user-chosen resource budget. **Zero survivors with reproducible explanations is a valid software/scientific outcome.**

A **physical survivor** cannot be reported merely because a candidate passes symbolic syntax, Gaussian constraints, source-current conservation, a frozen inverse field or a selected force-sign sample. It needs an independently varied common action and subsequently the missing physical closures. The program cannot promise discovery of physics not present in its explicitly represented candidate class.

---

# 1. Strategy: solve R3B blocker #1, not repeat a broad AGMINER

## 1.1 Core research question

> Does any **physically motivated, finite and stable** microscopic source/support completion, with one well-defined covariant action, generate the original useful R3B field/metric response **after full reciprocal neutral-matter loading**, while preserving a healthy universal physical metric and offering a viable exterior Earth/craft interaction?

This is a *constrained source-completion/existence* search, not energy minimization or general gravity-theory enumeration.

## 1.2 Freeze-and-vary contract

**Freeze as exact provenance, not as guaranteed on-shell fields:**

- R3B original producing source, reference capacity, fitted source geometry, multipole normalization, $P=-4\mathbf E\cdot\mathbf B$ in the documented sign convention, source radius and torus geometry.
- Reference $1\,\mathrm{keV}$ metric scale, when comparing to the original model, and the historical preloaded-versus-loaded failure.
- Corrected Lorentzian signs and source/interface negative controls from R3X1, B6 and B11–B16.
- DELTA1-02 local reciprocity and near-collinear $F_Y^2$ counterexample.
- 006D GR stress-energy reference and PH16-04R2 as a **different** conditional source/Noether architecture.

**Allow physically justified variation only in:**

- Source field content and its microscopic action; conserved source currents and support constraints.
- Realizable source boundary conditions and material interface/response.
- Additional dynamical mediator **only if** it breaks a named obstruction and passes its own health/empirical tests.
- Physically derived source geometry and material state, when permitted by the action; do not silently retune the payload target.

A change in the physical portal/operator or frame is a **new action family**. Tag it explicitly; it is not a same-kernel R3B rescue by default.

## 1.3 Evidence precedence

1. Immutable original Python/source, actual numerical JSON, independent verifier, SHA-256 and execution log.
2. Journal entries with source/results.
3. Current active physical and artificial buildplans.
4. `NOTES.md`, README and secondary prose.

When evidence conflicts: **halt and label `PARENT_CONFLICT`** until reconciled; never silently pick the more favorable number.

## 1.4 Hard avoid-repeat policy

- No broad random Wilson-coefficient sweep or 100,000-configuration field geometry search.
- No sub-100-J field-energy polishing of R3B/A12C.
- No repetition of the unchanged R3B loaded inversion, B15 angle-only routes, B16 weak-loading, R3A ordinary-material suppression, or near-collinear $F_Y^2$ coefficient sweep.
- No relabeling ALPHA inverse design or BETA prescribed scalar charge pairs as source physics.
- No F0D/F0E polarization-model assumption automatically imported into the original R3B action.
- No reuse of PH16's fixed-Noether Schur term without deriving the **same constraints** for the actual candidate.
- Every reopen proposal must record **the exact historical hypothesis it changes** and a cheap falsifier that distinguishes the new action from that failed hypothesis.

---

# 2. Scope of the automated search

## 2.1 Candidate = one action-completion card

Each card is an explicit versioned record with:

1. Exact covariant action terms, signs, dimensions, assumptions and bibliographic/derivation provenance where known.
2. Fields and dynamical versus fixed variables (including physical versus Einstein metric).
3. Symmetries and conserved charges; whether anomalies or boundary current inflow are relevant.
4. Source matter constituents, microscopic couplings, physical current $J_X,J_Y$, finite boundary, support action and stress.
5. Neutral material and Earth matter actions with **the same universal physical metric**.
6. Canonical energy, rest mass, formation, off-state and switching obligations, with known versus unknown SI entries.
7. Declared relation to R3B $P$, $\sigma(P)$ and corrected loading operator.
8. Previous failure potentially escaped, and its **specific new physical term**.
9. Complete gate verdicts, independent-verifier IDs, source fingerprints and unresolved derivations.

**Deduplicate by canonicalized full action/assumption fingerprint**, not by a parameter value or filename. The fingerprint covers operator AST, field redefinitions, metric convention, boundary, source species and conserved-number sector, sign/unit normalization, and source/matter profile. Different physical assumptions must not hash as identical; equivalent coordinate relabelings must not be treated as new physics.

## 2.2 Initial library: at most two nontrivial candidate families

Do not seed 35 unrelated candidates. The initial registry contains:

| ID | Candidate | Why it exists | Preliminary status |
|---|---|---|---|
| `R3B-NULL` | Original prescribed currents and fields, **not** a physical completion | Reproduce published R3B preloaded/loaded mismatch and prove nonphysical fields are rejected | Required **negative control**, never survivor |
| `R3B-SRC-A` | One finite, explicitly charged matter source (complex scalar/charged fluid *or* Dirac matter) plus actual support fields | Test whether an **action-derived** compact conserved current can realize the R3B exterior without fictitious current knobs | Candidate only after exact action chosen |
| `R3B-SRC-B` | One **genuinely distinct** dynamical polarization/magnetization/condensate source with physically derived boundary | Test a new source response/control direction, with previous Pauli/source-basis failures respected | Conditional; no default promotion |

These labels are **templates to be instantiated** with real couplings and defensible equations, not claims that such matter is viable. If existing AGMINER failure memory already excludes a given instantiation under the same premises, generate a one-row `HISTORICAL_NO_GO` and do not rerun it. If none is scientifically justified, output `NO_JUSTIFIED_CANDIDATE_ACTION` rather than filling slots with synthetic models.

**No arbitrary new metric operator by default.** A new operator is a separate, explicitly authorized action fork only if it is covariant, changes an independently meaningful response direction and has a concrete physical motivation. Quantum/semiclassical branches remain reserved for a justified, calculable hypothesis.

## 2.3 Necessary representation, not an assumed solution

A candidate's declared action has the schematic form

```math
S=S_{\rm EH}[g]+S_{X,Y}[g,A_X,A_Y]
+S_{\rm source}[g,A_X,A_Y,\Psi,\Xi]
+S_{\rm neutral}[\widetilde g,\psi_m]
+S_{\rm Earth}[\widetilde g,\psi_E]+S_{\rm boundaries}
```

For the original conformal mechanism:

```math
\widetilde g_{\mu\nu}=e^{2\sigma(P)}g_{\mu\nu}
```

The precise $P$ must be constructed from **covariant field tensors and the correct Hodge dual**, with the original normalization and metric dependence—not entered as an arbitrary external scalar. Recover $P=-4\mathbf E\cdot\mathbf B$ in the declared local frame/sign convention. The Einstein–Hilbert term must carry the proper SI normalization and boundary prescription. Source and support sectors must be actual variables with equations, not prescribed numerical currents.

**Key F0F distinction:** $\theta F_X\wedge F_Y$ has zero *direct* Hilbert stress at fixed metric-independent $\theta$, but a physical $\theta(P)$, $P$ involving a Hodge dual, metric-dependent matter, and the other carrier/source/support terms require their **full chain-rule metric variations**. The miner must not infer that R3B's complete gravitational response is identically zero from F0F's scoped result.

**Action first, force second:** a candidate cannot supply Earth forces, a sign-adjusted material coupling, or a new source-current profile as independently prescribed inputs to a force optimizer.

---

# 3. Scientific gate architecture — earliest decisive failure wins

A worker runs a **fixed, ordered gate DAG**, preserving every resolved gate and leaving unrun gates `NOT_RUN`. A software error is never a scientific falsification.

| Gate | Scientific task | Minimum acceptance evidence | Early-exit classification |
|---|---|---|---|
| `G00_PARENT` | Lock exact R3B, R3X1 and DELTA parents and unit/sign conventions | Producing-code and JSON SHA, historical negative control | `PARENT_MISSING`, `PARENT_DRIFT`, `PARENT_CONFLICT` |
| `G01_ACTION` | Parse one **fully specified** local covariant action, source/interface/boundaries, dynamical variables | Canonical typed action AST, physical metric and complete variation inventory | `ACTION_INCOMPLETE`, `NO_COVARIANT_COMPLETION` |
| `G02_VARIATION` | Derive Einstein/physical-metric, X, Y, source, support, neutral and Earth EOM | Exact symbolic/hand-verified variational identities with metric/Hodge chain rule | `METRIC_VARIATION_MISSING`, `EOM_INCOMPLETE` |
| `G03_WARD` | Check gauge, Ward, Noether, Bianchi, diffeo and charge-flux identities | Off-shell identities plus on-shell boundary/current conservation | `WARD_FAIL`, `NONCONSERVED_SOURCE` |
| `G04_HEALTH` | Canonical sign/kinetic constraints and genuine physical modes | Constrained propagating-mode and static-sector checks; no ghost by gauge counting alone | `GHOST`, `GRADIENT_INSTABILITY`, `UNRESOLVED_CONSTRAINTS` |
| `G05_SOURCE` | Finite source realizability, current range, interface traction and supports | Action-derived $J$, finite support, no hidden external anchor/charge | `SOURCE_NOT_REALIZABLE`, `SUPPORT_MISSING` |
| `G06_LOAD` | **Exact reciprocal** loading of finite neutral torus | Same-action Hessian/JVP and independently verified R3X1 negative control | `LOADING_SIGN_FAIL`, `LOADED_OPERATOR_MISSING`, `SUSCEPTIBILITY_UNRESOLVED` |
| `G07_METRIC` | Physical metric, sign, frame/coordinate invariant and linearized Einstein stress | Neutral geodesic/metric acceleration; full source/support stress at tested order | `NO_METRIC_REPULSION`, `FIFTH_FORCE_ONLY`, `METRIC_UNDERDETERMINED` |
| `G08_ENERGY` | Conservative SI lower bound and complete energy ledger | Canonically normalized, source/support and rest-energy accounting | `ENERGY_FLOOR_GE_10MJ`, `ENERGY_UNDETERMINED` |
| `G09_EXTERIOR` | Real exterior transmission and source/field support | True 1m material clearance, field-stress map, continuum/box/BC consistency | `NO_EXTERIOR`, `NUMERICAL_INCONCLUSIVE` |
| `G10_REACTION` | Earth-down and complete-craft-up with field flux | Derived force/energy-momentum accounting from identical action | `ONLY_INTERNAL_FORCES`, `EARTH_CRAFT_NOT_DERIVED` |
| `G11_REALISM` | Quantum/UV, naturalness, fifth force, EP, laboratory/astrophysical constraints | Independently supported EFT/regime and observational bound ledger | `UV_OR_EMPIRICAL_FAIL`, `EMPIRICAL_OPEN` |

**Computational ordering is flexible only when scientifically justified.** Cheap fatal energy or empirical bounds may run before an expensive source/field solve. Expensive gates never run merely because earlier checks returned `UNDERDETERMINED`.

## 3.1 Exact invariants that must be independently derived

For the declared Jordan/universal metric, check the original local relation (with explicit trace convention)

```math
\mathbf a_{\rm neutral}=-c^2\sigma_P\boldsymbol\nabla P
```

and the reciprocal matter-loading multiplier

```math
\lambda=e^{4\sigma}T\sigma_P
```

with transverse identity

```math
\boldsymbol\nabla\lambda\times\boldsymbol\nabla P
=e^{4\sigma}\sigma_P\boldsymbol\nabla T\times\boldsymbol\nabla P
```

These are **scoped original single-invariant formulas**. Their sign/trace conventions must be checked against actual action variations; never assume they are unchanged with an extra mediator or operator.

The action compiler must also generate a proof obligation for:

- $\delta S/\delta g_{\mu\nu}$, including Hodge dual and physical metric dependence; Jordan–Einstein frame bookkeeping.
- $\delta S/\delta A_X$, $\delta S/\delta A_Y$ with the correct R3X1 Lorentzian signs.
- $\delta S/\delta\Psi$, $\delta S/\delta\Xi$ for all source and support variables, with boundary traction.
- Both U(1) Ward identities, Gauss constraints and gauge null spaces; source-charge continuity.
- Diffeomorphism identity and **total** stress-energy conservation, not merely exterior $T_{\rm EM}$.
- Einstein Bianchi identity $\nabla_\mu G^{\mu\nu}=0$ consistent with the derived total source.
- Correct constrained canonical Hessian, eliminating gauge and fixed-charge directions only with justified constraints.
- Off/on initial and final material states, and source-support response to the moving neutral payload.

**No proof by a preprinted formula.** When symbolic general-relativistic expressions are intractable, produce a documented derivation obligation, a reduced symbolic test and an independent finite-difference variation. Output `UNDERDETERMINED`, not fabricated closed-form Einstein EOM.

## 3.2 Sourceability is the core discriminator

The miner asks whether the **action-derived source current** can create the R3B fields:

```math
\frac{\delta S}{\delta A_X}=0,
\qquad
\frac{\delta S}{\delta A_Y}=0
```

subject to matter equations, finite support, conserved charge and support stress. In a linearized candidate, form a permitted source-to-field map and a **constraint-projected** response subspace. Report singular values and uncertainty rather than declaring an arbitrary inverse current physically realizable. Demand the source work/energy implied by those currents. If a current basis has the same physical premises as a historical failed basis, use the stored no-go.

**When the true loaded Jacobian is absent, STOP:** report exactly which state, derivative, boundary or EOM is missing. Do not manufacture it from fitted preloaded arrays.

## 3.3 Negative controls that must run automatically

- Frozen original R3B preloaded favorable response versus the corrected historical loaded **$-129.67185782242464\,\mathrm{m/s^2}$** result; retain both energies and configurations separately.
- Incorrect sign-flipped R3X1 block rejected; correct canonical signs pass.
- Source prescribed externally rather than obtained by variation **rejected**.
- Matter trace/loading off, constant $T$ interface and vanishing $P$ cases where mathematically applicable.
- Pure constant-$\theta$ topological term has zero bulk current; variable-$\theta$ may source bulk field equations but fixed-scalar direct Hilbert stress remains zero.
- Perfect mirror $P/Q$ rank-one degeneracy and DELTA1-02's 0.16–0.18% independent-direction witness; no coefficient-only rescue.
- F0D uniform unstable quadratic trial and F0E hypothetical boundaries/saturation labeled **separate trial action**, not automatically physical R3B.
- F0G exterior-only Maxwell result rejected as a **complete conserved Einstein source** even when its restricted field integral checks pass.
- Arbitrary prescribed Earth charge, an internal reaction pair and a manually selected net lift **rejected**.
- Positive-mass Newtonian attraction is a force-sign negative control; coordinate relabeling cannot create gravitational repulsion.
- Dimension, SI normalization, ghost sign, gauge breaking, continuum-resolution and disconnected-source controls.

---

# 4. Two independent axes: scientific fidelity and resource budget

**Important:** A runtime preset must not silently authorize a higher scientific fidelity level. The user selects both. `--level` chooses **what physics gates may execute**; `--minutes`/resource options determine **when to stop**. If the budget expires, save `TIME_BUDGET_EXCEEDED` with unfinished gates and no implied scientific failure.

## 4.1 Scientific levels

| Level | Permitted work | Excluded work | Promotion |
|---|---|---|---|
| `L0 INVENTORY` | Evidence lock, historical failure lookup, action AST and units, fast exact algebra/no-go | Mesh solves, nonlinear state search | Candidate completeness/obstruction only |
| `L1 ACTION` | Exact or reduced symbolic variations, Ward/Noether/Bianchi tests, independent FD identities, cheap energy bounds | New multi-dimensional PDE | Candidate *theoretical* necessary-gate verdict |
| `L2 RESPONSE` | Restricted finite-source/current-map JVP, gauge-projector, small sparse linear solve, R3B loaded-sensitivity diagnostic | Full-scale PDE, high-res continuum and full repo regression | Conditional source/response evidence, **not** full survivor |
| `L3 STATIONARY` | At most **one** justified nonlinear source+X/Y+neutral stationary solve, coarse-to-fine if earned | Arbitrary batch PDE, Lorentzian-stability/whole-craft claims by inference | Scoped mathematical stationary candidate |
| `L4 INTEGRATION` | Independently derived Einstein/exterior/whole-craft/modes, convergence, full regression and complete-energy validation | Automatic access from lower levels | Human-authorized physical integration only |

`L3` and `L4` start **disabled** and require explicit `--authorize-stationary` / `--authorize-integration`, including named action and scientific question. An unproved source-variation gate cannot be bypassed by requesting a higher level.

## 4.2 Runtime presets (defaults; adjustable only within safe ceilings)

| Preset | Wall-clock cap | Worker cap | Process-tree RSS soft cap | Permanent-output cap | Typical use |
|---|---:|---:|---:|---:|---|
| `quick` | **60 s** | 1 | **384 MiB** | **4 MiB** | Parent SHA/inventory, one theorem |
| `short` | **180 s** | 1 | **640 MiB** | **8 MiB** | Two small action candidates |
| `focused` | **300 s** | 1 | **768 MiB** | **12 MiB** | Independent action/sensitivity gates |
| `extended` | **900 s** | 2 (explicit opt-in) | **1536 MiB** | **30 MiB** | One preauthorized L2/L3 step |

Other limits: default global GRAVITY2 persistent storage **200 MiB**, transient scratch per run **32 MiB**, persistent SQLite database **64 MiB including WAL/shm**, per-candidate stdout/stderr captured **64 KiB each maximum**, zero figures and zero retained full-field arrays at L0/L1. Lower levels must usually finish in seconds to minutes; these are **ceilings**, not runtime promises. A user-specified `--minutes 2` or `--minutes 7` is a hard wall-clock request, capped by the selected preset's safe maximum unless the user explicitly chooses a larger preset.

**Policy under disk pressure:** never delete existing immutable evidence or historical AGMINER records. Stop scheduling new candidates, seal an `STORAGE_LIMIT` summary if space allows, report how to archive manually, and do not claim new verification. Auto-pruning applies **only** to run-owned temporary files and recomputable unpinned caches, never to accepted science evidence.

## 4.3 Enforcement implementation (macOS-first)

- Use `time.monotonic()` deadlines, fixed dispatch queue and a per-worker watchdog. Every nontrivial candidate/gate runs in a **child process**, not as an unstoppable in-process SymPy call.
- Use `subprocess.Popen(..., start_new_session=True)`, track the process group; on timeout/cancellation send `SIGTERM`, allow a short grace, then `SIGKILL` to remaining process group. Record attempted signals and actual process exit/timeout.
- Monitor **worker + descendants** RSS with `psutil` (declare dependency); if unavailable, fail closed for memory-limited L2+ work, rather than pretending RSS is enforced. macOS `RLIMIT_RSS` is not a dependable hard guarantee. Apply conservative worker counts; no concurrent factorization by default.
- Limit NumPy/OpenBLAS/Accelerate/MKL/OpenMP threads (normally 1) in worker environment; bound solver iterations, matrix dimension and sparse fill. CPU core counts are policy caps, not a portable hard per-process CPU guarantee on macOS.
- Treat disk quotas as **application-enforced** with preflight free-space checks, bounded output writers, bounded cache and scratch monitoring. OS processes can transiently exceed quotas; if exact hard disk reservation is unavailable, the report must say `SOFT_LIMIT_WITH_WATCHDOG`, not falsely claim kernel enforcement.
- Use stream-to-bounded-tail capture, truncation metadata and incremental log SHA; never buffer unlimited subprocess output in memory.
- Parent scheduler is the **only SQLite writer**. Workers return bounded structured messages; no worker writes to the shared DB.
- Do not kill unrelated processes; only the miner's own recorded child process groups. `stop` acts on a miner run PID/lease, not a broad `pkill python`.
- On sleep, thermal slowdown, low battery, low free disk or shutdown, checkpoint and stop. Battery/thermal integrations can be advisory; only promise enforcement where the platform provides a reliable signal.

## 4.4 Scheduling, prioritization and no compute wastage

1. One candidate is examined at a time by default; at most **two genuinely distinct new source completions** per focused batch.
2. Cache exact *pure* symbolic kernels and parent-array reconstructions by full SHA of action, parameters, metric/boundary/mesh and code/dependency versions. Never reuse loaded solver output across different actions or source states.
3. Prefer an analytic obstruction over a mesh solve. Start with the smallest valid discriminating geometry; h=`0.075 m` is the historical low-cost R3B diagnostic. `0.050 m` is **conditional** and does not alone certify convergence.
4. No full pytest suite in automatic 1/3/5-minute sessions. Targeted project tests and an independent different-method check are mandatory for any acceptance. Full regression runs only for an integrated accepted code checkpoint, publication/transfer or explicitly requested `L4` job.
5. Stop a candidate immediately after a **proven** fatal failure. An `UNDERDETERMINED` or solver timeout does not license rejection or reranking as viable.
6. Rank **expected information gain / predicted wall-clock minute** using auditable deterministic features: unresolved physical obligation, historical failure coverage, cheapest decisive test, source novelty and projected resource cost. Do **not** rank by raw field capacity, arbitrary success probabilities, or number of passing Python assertions.
7. Revisit only when one named new assumption defeats an old falsifier. Reject endless coefficient polishing.

---

# 5. Python architecture and repository layout

## 5.1 Proposed files (none claimed to exist yet)

```text
gravity2buildplan.md
src/antigravity_research/gravity2/
    __init__.py
    __main__.py               # argparse CLI
    config.py                 # versioned scientific/runtime config
    models.py                 # typed immutable action/candidate/gate dataclasses
    provenance.py             # parent SHA and original R3B loaders
    canonical_action.py       # restricted covariant operator AST
    action_templates.py      # at most two explicit source completions
    variations.py            # symbolic/reduced Euler/Hilbert variations
    identities.py            # Ward/Noether/Bianchi/constraint checks
    sourceability.py         # physical current/support response range
    loading.py               # corrected R3X1 and exact reciprocal JVP
    metric.py                # physical metric, neutral sign, stress
    energy.py                # separate conservative SI ledgers
    historical.py            # failure memory and negative controls
    gates.py                 # stop/underdetermination policy
    scheduler.py             # deterministic priority, checkpoint/resume
    worker.py                # isolated child-process scientific jobs
    resource_guard.py        # watchdog/time/RSS/disk/cancellation
    cache.py                 # small disposable content-addressed cache
    storage.py               # single-writer SQLite + immutable JSON
    verification.py          # independent-result orchestration
    reporting.py             # compact terminal + Markdown summary
simulations/gravity2/
    run_gravity2.py          # thin entrypoint if repo convention requires
    verify_gravity2.py       # independent offline science verifier
tests/gravity2/
    test_config_and_limits.py
    test_parent_provenance.py
    test_action_ast.py
    test_variations_and_ward.py
    test_source_and_loading.py
    test_scheduler_and_resume.py
    test_negative_controls.py
    test_resource_guard.py
    test_serialization_and_storage.py
    test_scientific_claim_boundaries.py
results/gravity2/
    gravity2.sqlite3
    runs/<run_id>/
        manifest.json
        science.json
        independent_verification.json
        hashes.sha256
        report.md
    cache/                   # disposable, content-addressed
    scratch/                 # cleaned after every completed run
```

Where current AGMINER storage utilities are appropriate, **reuse their implementation without copying their entire historic database**. The existing database remains source-of-truth for historical failed premises. An optional read-only AGMINER adapter imports just required fingerprints and failure rules. No schema migration to the historical AGMINER DB in `GRAVITY2-00`.

## 5.2 Types and explicit state machine

Essential conceptual types:

```text
ActionSpec
  action_id, version, fields, metric_frames, terms, boundaries,
  source_species, constraints, parameters_with_units, assumptions,
  historical_failure_delta, action_sha256

Candidate
  candidate_id, action_spec, parent_lock, source_profile,
  status, scientific_level, next_gate, fingerprint

GateResult
  gate_id, verdict, proven_scope, equations, residuals,
  units, uncertainty, negative_controls, evidence_files,
  independent_verifier, wall_s, peak_rss_mib, disk_bytes

RunManifest
  run_id, seed, CLI, scientific_level, runtime_preset,
  deadlines, CPU/threads/RSS/disk limits, exact parent hashes,
  versions, safety_flags, resume_cursor
```

Verdicts: `PASS_SCOPED`, `FAIL_SCOPED`, `UNDERDETERMINED`, `NUMERICAL_INCONCLUSIVE`, `TIME_BUDGET_EXCEEDED`, `MEMORY_LIMIT`, `STORAGE_LIMIT`, `NOT_RUN`, `SOFTWARE_ERROR`. Distinguish **scientific theorem failure** from **test or implementation failure** and from **candidate not yet physical**. A PASS at `G03` cannot silently set `G07`–`G11` PASS.

Run lifecycle: `CREATED → PARENT_LOCKED → ACTIVE → STOP_REQUESTED / RESOURCE_STOP / COMPLETED → SEALED`. Resume creates a **new immutable continuation ID** that cites the previous run and restarts only an incomplete gate with identical action/assumption fingerprint. Never append into a sealed science JSON or alter a previous failed result.

## 5.3 Small persistent database

SQLite main-process writer, WAL mode with bounded checkpoints, unique constraints on fingerprints and run IDs; fixed schema/version. Tables:

```text
runs
candidates
actions
gate_results
failure_rules
parent_evidence
cache_index
resource_events
resume_links
```

Store short statuses, hashes, paths, scalar observables and obstruction proofs. Do **not** store large arrays, raw SymPy expression trees, solver histories or duplicate codebundles in SQLite. WAL/shm count toward the disk cap; checkpoint during idle transitions. No database auto-`VACUUM` during a timed science run.

## 5.4 Evidence and data hygiene

- Create a unique UTC run ID and manifest with `open(...,'x')`; never overwrite existing files.
- Compute script/parent input hashes once at stage boundary, not during each solver iteration. Save parent-producing SHA, dependencies, Python/NumPy/SciPy/SymPy versions and precise SI/sign conventions.
- Write temporary output to the run scratch path, validate with JSON `allow_nan=False`, flush and `fsync`, then **seal without overwrite** using same-filesystem exclusive `os.link(temp, final)` followed by unlinking the temporary name, or an equivalent rigorously no-clobber atomic create. Do not rely on `os.replace` alone: it overwrites existing destinations. The parent is the sole sealer.
- Prefer scalar observables, proofs and tiny compressed sampled arrays. Large numerical fields retained only for explicitly promoted L3/L4 checkpoints, with user opt-in and known quota; record array shape/dtype/units/mesh/BC/source-hash.
- Record process exit code, wall-clock, CPU/RSS monitoring quality, disk usage, truncation flags and why incomplete gates were skipped.
- Track exact survivor-to-parent links, verified theorem assumptions, and hash any reported immutable science/verification file.
- No external telemetry, network services or cloud requirement; local-only by default.

---

# 6. Planned CLI — simple operation in minutes

**These commands are specification examples; the package does not exist yet.** They become paste-ready commands **after implementation and acceptance of `GRAVITY2-00`**.

From the repository root:

```bash
PYTHONPATH="$PWD/src" .venv/bin/python -m antigravity_research.gravity2 --help

# 1 minute: audit parent evidence and cheap source-action no-gos.
PYTHONPATH="$PWD/src" .venv/bin/python -m antigravity_research.gravity2 run \
  --level L0 --preset quick --minutes 1 --workers 1

# 3 minutes: bounded source-action and identities investigation.
PYTHONPATH="$PWD/src" .venv/bin/python -m antigravity_research.gravity2 run \
  --level L1 --preset short --minutes 3 --workers 1

# 5 minutes: source controllability / loaded-response screening if authorized by L1.
PYTHONPATH="$PWD/src" .venv/bin/python -m antigravity_research.gravity2 run \
  --level L2 --preset focused --minutes 5 --workers 1

# Progress and scientific state without launching work.
PYTHONPATH="$PWD/src" .venv/bin/python -m antigravity_research.gravity2 status
PYTHONPATH="$PWD/src" .venv/bin/python -m antigravity_research.gravity2 top --max 5
PYTHONPATH="$PWD/src" .venv/bin/python -m antigravity_research.gravity2 failures --max 10

# Explicit safe stop and independently audited resume.
PYTHONPATH="$PWD/src" .venv/bin/python -m antigravity_research.gravity2 stop --run-id RUN_ID
PYTHONPATH="$PWD/src" .venv/bin/python -m antigravity_research.gravity2 resume \
  --run-id RUN_ID --level L1 --preset focused --minutes 5

# Explicit offline verification of sealed evidence.
PYTHONPATH="$PWD/src" .venv/bin/python -m antigravity_research.gravity2 verify \
  --run-id RUN_ID
```

**CLI guarantees:** `run --dry-run` previews source files, candidates, next gates, constraints and estimated cost; `--list-candidates` identifies locked and conditional candidates; `--explain CANDIDATE_ID` displays proven failures and open equations. No `run` command defaults to broad search, L3, 2+ workers, bulk disk persistence or the full test suite.

Provide short human-readable terminal progress such as:

```text
GRAVITY2 | L1 | 03:00 budget | 1 worker | 640 MiB RSS | 8 MiB output
R3B parent lock: PASS
R3B-NULL historical loaded failure: REPRODUCED
R3B-SRC-A G02 variation: UNDERDETERMINED (missing support term)
Remaining: 01:42 | CPU/RSS/disk: reported | next: G05 source action
STOP: NO PROMOTION; immutable report sealed
```

This is **illustrative format**, not an executed result or promised runtime.

---

# 7. Implementation sequence with strict acceptance gates

## `GRAVITY2-00` — Runner, provenance and resource safety (first build)

**Build:** CLI, typed schema, parent-hash loader, scheduler/worker/watchdog, SQLite single writer, bounded logs/JSON, crash-safe resume, negative controls and compact report. No speculative new physics. Load exact R3B, R3X1, DELTA1-02 and the F0C–F0G parent manifests where present; missing optional latter files are explicit missing evidence, not fabricated. Import historical source/checkpoint SHAs and status.

**Acceptance:**

- A 60-second `L0` run terminates by its deadline, seals immutable evidence, and reports peak RSS/disk.
- Timeouts or memory/storage exhaustion preserve previous completed gates, kill only miner-owned worker children, and never write false scientific FAIL.
- Cold-start/restart/resume determinism; duplicate fingerprints never create duplicate candidates.
- Forced crash and corrupt checkpoint produce a bounded recoverable status; original reports never mutate.
- Injected NumPy scalars/bools, NaN, Unicode and missing parent sidecars are handled intentionally—**no repeat of F0E's serialization defect**.
- Dummy worker that sleeps past deadline and dummy worker that allocates memory are contained.
- All new focused unit and independent source/JSON tests pass. Full regression only once after integrating these modules into repository code, in a separately scheduled bounded job.

**Exit:** `GRAVITY2-00_INFRA_ACCEPTED`, or explicit infrastructure HOLD. **Not physics progress.**

## `GRAVITY2-01` — Original R3B action and current-provenance compiler

**Build:** exact original R3B source/field/metric/strong-loading inventory; typed covariant action AST; symbolic/independent variational test harness; original sign, dimension and source-current identity tests. Distinguish generating scripts that calculate fields from actual covariant spacetime actions. Produce a matrix of **solved/fixed/prescribed/missing** variables.

**Acceptance:** original R3B capacity reproduces within source tolerance; historical loaded negative result is recorded and separately reconstructable only if the original state/action are actually present; no silent claim that a source action exists when only a field recipe exists. `G01` and `G02` missing terms reported by name.

**Exit:** action-completeness/undertermination atlas with SHA; permits source templates **only** where their missing terms are specified.

## `GRAVITY2-02` — At most two physically motivated source completions

**Build:** instantiate `R3B-SRC-A/B` if and only if source currents/support terms are physically specified, units are matched, and historical exclusions are addressed. Derive exact X/Y, source, neutral, support and Einstein variation requirements; independent Ward/diffeo checks. Tie any extra mode to a named new mechanism rather than coefficient fitting.

**Acceptance:** for every candidate, source-current conservation and support boundary arise from its action, not injected to satisfy field equations. If one necessary action cannot be completed, report `NO_JUSTIFIED_ACTION` and halt that branch. Never consume the unused candidate slot with an arbitrary model.

**Exit:** 0–2 `ACTION_THEORY_CONDITIONAL` cards, or scoped falsifications.

## `GRAVITY2-03` — Reciprocal finite-neutral loading and control range

**Prerequisite:** actual candidate source action and sufficient static reduction. **Build:** gauge-projected same-action sensitivity/Hessian/JVP, neutral trace/interface response, source/current permitted control subspace, source work and signed acceleration. Recover R3X1 failure as a negative control; compare only legitimate new action terms. Retain uncertainties and compare mesh/boundary when a candidate changes conclusion.

**Acceptance:** nonzero physical source-control direction beyond the already nearly collinear simple $F_Y^2$ channel; source/current/support consistency and residuals independently verified; no claim of full stability from one frozen Schur block.

**Exit:** conditional action-derived loaded response, `UNDERDETERMINED`, or precise scope-bounded failure. **No automatic new PDE**.

## `GRAVITY2-04` — Earned stationary/exterior and complete force evidence

**Prerequisite:** L1/L2 sourceability, health, energy and sign bounds pass plus explicit research authorization. Only **one** candidate/geometry per expensive session. Couple source, X/Y, finite neutral material and supports; verify full static action residuals, regular boundaries, at least two independent discretizations and exterior/box checks. Transfer to physical metric, Earth/craft action and momentum/field flux; independently assess physical-mode spectrum and complete energy. Schedule a separately bounded full regression after accepted integration.

**Exit:** real physical milestone **only if independently established**, else preserved failure/unknown. Do not equate this phase with engine certification.

## `GRAVITY2-05` — Independent review, transfer and documentation

Generate a compact reproducible technical packet: complete source/action, each EOM and identity, source/support provenance, actual neutral-payload minimum, Earth/craft reaction, SI/UV/empirical ledger, numerical error/convergence, negative controls, producer and independent SHA, regression scope, known failures and explicit future work. Compare with 006D and the original R3B data. No heuristic percent change without **independent** source-to-gravity and Earth/whole-craft closure.

---

# 8. Test strategy and scientific acceptance conditions

## 8.1 Three separate verification layers

1. **Implementation:** unit tests, pure function tests, timeout/resume/cache/SQLite tests and type/schema checks.
2. **Independent mathematics:** separately constructed metric variation, Ward identity, SI bound, source support/current and finite-difference Jacobian; do not have the verifier simply read the science file and assert expected status strings.
3. **Physical evidence:** real source action, actual loaded neutral/Einstein/exterior/whole-craft response, energy and independent parameter/domain checks. A calculation may pass layers 1–2 but fail or leave layer 3 unknown.

## 8.2 Mandatory acceptance checks

- `python -m compileall` scoped to new modules; selected pytest modules; strict JSON schema including `numpy.bool_`/scalar conversion at deliberate serializer boundary.
- Existing reference SHA and numeric anchors, including negative loaded sign and original R3B capacity.
- Mismatched producer SHA, changed BC, altered normalization or absent parent → immediate `PARENT_DRIFT` / `PARENT_MISSING`.
- Source-current and stress conservation with support terms. On-shell vs off-shell explicitly distinguished.
- Wrong-index, wrong-sign and wrong-metric controls fail; identical fields under gauge transform do not change physical observables.
- Independent variation or a mathematically distinct method for every scientific acceptance, not assertions that compare the same function to itself.
- Hard stop during worker iteration and process-tree cancellation; no endless pytest when `--minutes 5` was requested.
- Incomplete execution produces `TIME_BUDGET_EXCEEDED` or `NUMERICAL_INCONCLUSIVE`; does not fabricate a failing theorem.
- A reported total force must include **whole spacecraft** and Earth, not just neutral material and a pair of toy forces.
- A reported $E<10\,\mathrm{MJ}$ includes explicitly accounted source formation/rest/reference, supports, power, field, off state, backreaction, dissipative cycles and significant UV/empirical obligations; unknown entries prevent certification.

## 8.3 Full regression cadence

A full `pytest` suite is **not part of** `quick`, `short`, or `focused` research runs. The latest explicitly established historical suite baseline from `DELTA1-02` is 3,304 tests; use the true live count when the new modules are integrated. Run the complete suite:

- Once per accepted integrated feature checkpoint; run explicitly outside the short research deadline, with a separately declared cap.
- Before publishing/transferring a physical claim or modifying shared source.
- At a deliberate closeout checkpoint if accepted code changes were made.

Record `FULL_REGRESSION_PENDING` otherwise. A skipped suite cannot be displayed as a current PASS.

---

# 9. Minimal JSON science/report contract

The exact schema will be versioned in `models.py`; this **illustrative skeleton** contains no execution claims:

```json
{
  "schema_version": "gravity2.v1",
  "run_id": "EXAMPLE_NOT_EXECUTED",
  "program": "GRAVITY2-R3B-ACTIONMINER",
  "run_state": "COMPLETED",
  "level": "L1",
  "preset": "short",
  "budget_seconds": 180,
  "candidate_id": "R3B-SRC-A",
  "action_sha256": "NOT_YET_DERIVED",
  "parent_sha256": {},
  "gates": {
    "G00_PARENT": "NOT_RUN",
    "G01_ACTION": "NOT_RUN",
    "G02_VARIATION": "NOT_RUN",
    "G03_WARD": "NOT_RUN",
    "G04_HEALTH": "NOT_RUN",
    "G05_SOURCE": "NOT_RUN",
    "G06_LOAD": "NOT_RUN",
    "G07_METRIC": "NOT_RUN",
    "G08_ENERGY": "NOT_RUN",
    "G09_EXTERIOR": "NOT_RUN",
    "G10_REACTION": "NOT_RUN",
    "G11_REALISM": "NOT_RUN"
  },
  "reference_field_capacity_j": 1.5429162116460216,
  "certified_operating_energy_j": null,
  "certified_minimum_payload_acceleration_m_s2": null,
  "whole_craft_gravitational_force_n": null,
  "physical_success": false,
  "full_regression": "NOT_RUN",
  "independent_verification": "NOT_RUN",
  "next_gate": "G01_ACTION",
  "limitations": ["SCHEMA_EXAMPLE_ONLY"]
}
```

Accepted evidence includes the exact SHA-256 of `science.json`, `independent_verification.json`, the producing code, action AST and locked parent files. Counters include actual candidate count, scoped false hypotheses removed, genuine new action directions, peak RSS, wall time, elapsed CPU, disk bytes and cache hits. A numerical error or empty survivor set is reported plainly.

---

# 10. Release criteria and immediate next work

## 10.1 Definition of done for first useful release

`GRAVITY2-00` is ready for unattended bounded runs when:

1. The original R3B kernel, historical $-129.67185782242464\,\mathrm{m/s^2}$ loaded failure, DELTA1-02 identity and parent hashes are reproduced/read with explicit scope.
2. A worker cannot exceed the configured wall-time policy without being terminated and classified; memory/disk limits are monitored with truthful caveats.
3. The miner can run 1, 3 and 5 minutes locally, stop and resume, leave compact immutable SHA evidence, and never duplicate old work by fingerprint.
4. The system refuses arbitrary currents, incomplete actions, incorrect metric variations and force-sign/energy promotion.
5. Scientific gates are independently testable and an empty survivor list is a valid output.
6. No new parameter search, source synthesis or long PDE is silently authorized by merely starting the software.

## 10.2 First actual scientific batch (only after infrastructure acceptance)

**`GRAVITY2-R3B-01_SOURCE_ACTION_COMPLETENESS_AND_CONTROL_FORK`**

One coherent question: *what exact source/support/metric variations are absent from the original R3B construction, and which one physically distinct action completion—if any—can provide a new conserved response direction that addresses the loaded sign reversal?*

Expected cheap discriminators:

- Reconstruct $P$, $\sigma(P)$, torus $T$, current locations, source geometry and R3X1 sign from original code and results.
- Declare every dynamical, fixed and prescribed variable, including Earth and supports, and mark absent EOM.
- Compute exact response dependencies from the original action sector; only attempt a controlled candidate if its full source/support term is present.
- Test a real conserved-current basis against the required R3B field profile; do not infer physical current by inverting free Maxwell equations alone.
- Compare with the fixed R3B loaded failure and near-collinear second-invariant control. Produce `ACTION_INCOMPLETE`, `NO_NEW_SOURCE_DIRECTION`, or one independently supported conditional source-action candidate—not a preloaded field-energy improvement.

**Strict initial budget:** `L1`, 180–300 seconds, 1 worker, 640–768 MiB RSS soft cap, 8–12 MiB permanent output cap, no full suite, no 3D PDE. Only escalate from a documented mechanism that survives its cheapest falsifiers.

## 10.3 Decision rule at the end of each batch

```text
IF action is incomplete:
    name missing variation(s); preserve evidence; STOP
ELSE IF Ward/Noether/Bianchi or ghost/energy necessary gate fails:
    save scoped no-go; STOP
ELSE IF source current or support is not physically realizable:
    save sourceability obstruction; STOP
ELSE IF a new action-derived loaded response survives:
    mark CONDITIONAL_SURVIVOR; request explicit L2/L3 authorization
ELSE:
    UNDERDETERMINED or NUMERICAL_INCONCLUSIVE; retain provenance
```

No report may set `SUCCEEDS_006D`, `PHYSICAL_LIFT`, `E_COMPLETE_LT_10MJ` or **research maturity $\ge50\%$** from automated fitting, a partial static source, test counts or a few-joule capacity. The first genuinely meaningful milestone is an **independently derived, sourceable, same-action universal-metric mechanism**, followed by a demonstrated physical external Earth/whole-craft interaction.

---

# 11. Compatibility notes and research governance

- **Existing project files:** no change to `ARTIFICIAL_BUILDPLAN.MD`, `AGMINER_BUILDPLAN.MD`, `NOTES.md`, `RESEARCH_BUILDPLAN.md`, historical journal or immutable artifacts is implied by creating this plan. Any later documentation updates should explicitly state their evidence boundary.
- **Python target:** project's Python 3.13 environment and existing NumPy/SciPy/SymPy stack. Small additional dependency `psutil` is justified only for process-tree memory monitoring; version pin and fail-closed fallback as specified.
- **macOS/Intel:** use single-worker by default, control BLAS threads, avoid large dense Hessians/automatic differentiated full-grid actions, and check available memory before any L2+ stage.
- **Observability:** terminal output is compact and live (gate, timer, memory/disk, candidate, last scientific result); full evidence is a small sealed file set, not a giant continuously appended console transcript.
- **No arbitrary async claim:** automation exists only while the local process is actually running. It cannot discover new physics or send reports after shutdown without an explicitly operating scheduler outside this chat.
- **User-facing delivery policy for future implementation:** separate complete paste-ready `APPLY` and `VERIFY` Bash blocks, source comments/docstrings per `FORMATTING_AND_CODE_STANDARDS.md`, no encoded patches, no hidden Git operations, no downloadable scripts unless specifically requested.

**Bottom line:** This miner is a **time-bounded physics falsifier and source-action completion assistant**, not an automatic engine designer. Its highest value is to find out—cheaply, reproducibly and decisively—whether the celebrated R3B prescribed field admits a realistic source-to-Einstein/metric completion, and to retain exact reasons when it does not.
