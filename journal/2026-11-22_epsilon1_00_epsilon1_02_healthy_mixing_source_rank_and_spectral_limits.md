# Research Journal — 2026-11-22

## EPSILON1-00 through EPSILON1-02: Healthy Quadratic Control, Independent Auxiliary-Source Rank, and Spectral/Noether Symmetry Obstructions

## Objective

Determine whether a **genuinely new, healthy, independently sourced auxiliary field** can correct the G01-U3B/U4A scalar-source deficit without reproducing the original loaded X/Y obstruction, assuming a finite positive scalar quadratic energy and the strict `<10MJ` overall antigravity target.

This is an **artificial mathematical discovery branch**, not thrust optimization, not a physical source realization and not a new gravitational model. It was created after G01-U4A to find precise necessary conditions for a candidate to deserve full source-action construction.

## Starting State

- U1's conditional scalar-only outward signal required `7,333,333.333333331 J` of modeled scalar energy.
- U3B's four reciprocal Maxwell source projections were nonconverged and ranged from approximately `-0.0667` to `+0.000725` relative to the fixed U1 source overlap.
- U4A's loaded frozen-profile stationarity required a ratio `1.000001486546953`, leaving projected gaps approximately `1.061430`, `1.066716`, `0.999276`, `1.003306`.
- U4A's fixed-profile conditional feedback estimate was `18,462,966.536208488 J`, above 10 MJ; not a general lower bound for all scalar/source profiles.
- Neither the original R3B 1.542916 J field-only capacity nor the original A12C capacity is the same physically sourced energy as U1's separate scalar geometry.
- The actual microscopic origin of any auxiliary source, its full dynamic stability, Fourier content and physical Einstein response were unknown.

## Work Performed

### 1. EPSILON1-00 — Exact positive-Hessian Schur control

The tested static quadratic functional was schematically

`E[f,chi] = 1/2<f,Af> + 1/2<chi,Bchi> - <f,Kchi> - <J_f,f> - <J_chi,chi>`.

For positive `A,B`, define global mixing strength

`s = ||A^(-1/2) K B^(-1/2)||`.

A sufficient strict positive-quadratic condition is `s<1`. Cauchy–Schwarz gives

`|<f,Kchi>| <= s sqrt(<f,Af><chi,Bchi>)`.

The model then computed an **optimistic conditional quadratic-energy screening bound** for a chosen target scalar field and a hypothetical auxiliary source/field capable of supplying the missing source overlap `gamma`.

Under its fixed normalization, the favorable expression was

`E_screen >= E_f * (1 + gamma^2/s^2 - 2*gamma) + E_EM_reference`.

This is not certified on-shell total physical energy; the external drive terms, material energy, supports, operating cycle and other degrees of freedom are not included. It cannot certify a low-power spacecraft engine.

The computed minimum `s` necessary for the optimistic energy expression to fall below `10,000,000 J` was:

| U3B case | Missing overlap gamma | Minimum screening s |
| --- | ---: | ---: |
| `64m,h=.2,ell5` | `1.061429819409942` | `0.673127629678965` |
| `80m,h=.2,ell5` | `1.0667159438722729` | `0.6750463532810645` |
| `80m,h=.1,ell5` | `0.9992760015664254` | `0.6501719227169409` |
| `80m,h=.1,ell7` | `1.0033063780993687` | `0.6516833008025271` |

At hypothetical `s=0.8` the optimistic scalar-coupled quadratic-plus-illustrative-EM values fell below 10 MJ. This demonstrated an *algebraic feasible interval only*. It neither produced a new source nor transferred the energy bound to the original R3B shell.

EPSILON1-00 successful APPLY/VERIFY output:

- Producer SHA-256: `0314fc109153181da619090afa425b955dd96c726ed431345ebc1ae602635b8c`.
- Scientific JSON SHA-256: `2840555051406416bcf4bfc9a8bc17f736d61a97e623f5019aa8dcbe39e23f16`.
- Science parent U4A SHA-256: `5e29b2d389fee45ff4a3098b29f1ac3c8bd436cb678d9c8df2c24535e14450f5`.
- Verification JSON SHA-256: `804a205000cf37d8b214d926185032c03f59a18df818595ed4738e9930b6cf8c`.
- Result directory: `results/gravity2/epsilon1_00_20261122T195249Z_36810`.
- Physical survivors: `0`; full regression: `NOT_RUN`.

### 2. EPSILON1-01 — Actual independent drive demanded

The next exact single-mode model used the matrix equations

`[(1+delta), -s; -s, 1] [x,y]^T = [r,j]^T`.

Here `r` is the recorded loaded Maxwell-source projection, `j` is the independently required auxiliary drive, and `x=1` is the target original scalar-profile amplitude. The equations give

`j_required = (1 + delta - r)/s - s`.

Setting `j=0` tests whether passive positive mixing alone supplies the correction. At a fixed positive Hessian, the resulting response is `x=r/(1+delta-s^2)`. Three of the four parent projections were negative. Those cases cannot restore positive `x=1` without some new independent source in this one-mode model.

The single small-positive-r parent could restore the amplitude with no explicit j only when `s≈0.9996379352377667`, producing a near-soft-mode condition number of approximately `5511.561165182167` in the toy 2x2 matrix. A healthy static Hessian near a zero mode is not automatically a healthy, robust complete Lorentzian material theory.

At `s=0.8`, EPSILON1-01 required:

| Parent trial | Required `j` | If artificially tied to `r`, `q=j/r` |
| --- | ---: | ---: |
| `64m,.2,5` | `0.5267872742624276` | `-8.575640094895363` |
| `80m,.2,5` | `0.5333949298403409` | `-7.995192514859968` |
| `80m,.1,5` | `0.44909500195803154` | `+619.0272907253532` |
| `80m,.1,7` | `0.4541329726242107` | `-137.41236752300082` |

The extreme variability and sign of `q` reflects the **nonconverged source overlap** and is strong evidence against claiming that one fixed co-source multiplier has solved the issue. It is not a general continuum exclusion of all physical sources.

Reported algebraic controls: passed. Source action: not supplied. Gravitational survivors: zero.

- Producer SHA-256: `ed115ca4d81361bd9822b061bb2b12a9b064b264631942bea59e9fb22c7e1d67`.
- Science SHA-256: `adfa83e0171ba8102d82d275e4749ffa5ab951ab0b088686333055ebeb9ebd70`.
- Verification SHA-256: `46616b3d30149ca644a5120bd3620cedb5e4f307cf97c13211ebd26e29bfb5d2`.
- Result directory: `results/gravity2/epsilon1_01_20261122T195837Z_52825`.
- Full regression: `NOT_RUN`.

### 3. EPSILON1-02 — Canonical local spectral mixing

EPSILON1-02 tested a **specific canonical two-scalar mass-mixing** model rather than arbitrary nonlocal source control. If both scalar fields have ordinary positive spatial-gradient terms, positive mass parameters `m_f` and `m_chi`, and nondifferentiated mixing `nu^2 f chi`, strict homogeneous mass stability requires

`|nu^2| < m_f*m_chi`.

The resulting modewise normalized mixing is

`s(k) = |nu^2|/sqrt[(k^2+m_f^2)(k^2+m_chi^2)]`.

The maximal attainable modewise mixing decreases with spatial wavenumber. For `m_f=1 m^-1`, the **equal-mass limiting upper** is `1/(1+k^2)`; maximizing over the auxiliary mass gives `1/sqrt(1+k^2)`.

| k (m⁻¹) | Equal-mass bound | Any auxiliary mass bound |
| --- | ---: | ---: |
| 0 | Approaches 1 | Approaches 1 |
| 1 | 0.5 | 0.7071067812 |
| 2 | 0.2 | 0.4472135955 |
| 5 | 0.03846153846 | 0.1961161351 |

The 0.65–0.675 **global quadratic energy threshold** was compared with modewise mixing as a *conditional screening heuristic*. Without the actual Fourier decomposition of the missing source correction, it would be scientifically wrong to assert that every wavenumber must meet the global threshold.

Recorded threshold / first idealized cutoff ranges:

- Global optimistic mixing threshold `s≈0.6501721273–0.6750465542` after including the positive scalar matter-loading term in the new screen.
- Equal-mass cutoff `k≈0.6938–0.7335 m^-1`.
- Any auxiliary-mass limiting cutoff `k≈1.0929–1.1686 m^-1`.

These cutoffs are statements about comparing a global threshold to modewise upper bounds, not measured source spectra or verified finite-body instability boundaries.

### 4. EPSILON1-02 — Operator-level source symmetry screen

The candidate source term `chi*(|Fplus|^2+|Fminus|^2)` preserves the separate charged-scalar global phase/number symmetries at the **operator level** when the two complex fields have appropriate charges, but if `chi` is a pseudoscalar and the densities are parity-even, that term violates parity. This is a physical and empirical design cost, not automatically a ghost.

Other screen candidates and caveats:

- `chi * i bar(Psi) gamma5 Psi` is parity-even for a pseudoscalar `chi` and can preserve fermion-number phase symmetry, but no polarized fermion material, drive magnitude, spin energy or UV consistency was derived.
- `chi F_X wedge F_Y` shares the existing mixed Maxwell channel; an **independent** new source is not thereby established.
- A cross bilinear `chi Im(Fplus Fminus)` can break the two separate Noether symmetries; mere gauge neutrality under opposite charges is insufficient to preserve both separately conserved PH16 numbers.

The actual complete action for original X/Y, charged source, neutral matter, supports, Earth and Einstein gravity was **not** constructed. The new field source remained hypothetical.

EPSILON1-02 user-executed outputs:

- Producer SHA-256: `28305918d1a1b4be228119fc91e4cc93aea978f7afc4b1dd7cb34dfa6352a4af`.
- Scientific JSON SHA-256: `4dfcf4f998224046f9eaca2c4494c39f525b330fa938919f81eaa2be896e4ec0`.
- Verification SHA-256: `11e17c7747609848c69610b2701924ae1f514aac6f5e84ffd678716f6e8866f1`.
- Parent EPSILON1-01 SHA-256: `adfa83e0171ba8102d82d275e4749ffa5ab951ab0b088686333055ebeb9ebd70`.
- Result directory: `results/gravity2/epsilon1_02_20261122T200406Z_69377`.
- Five focused operator-level/control categories: `PASS`.
- Independent spectral verifier: `PASS` in stated algebraic scope.
- Physical source survivors: `0`; gravitational survivors: `0`; full regression: `NOT_RUN`.

## Result

EPSILON-1 produced an important three-stage **necessary-condition atlas**, not a self-sourced field or vehicle:

1. EPSILON1-00 found a mathematically positive quadratic mixing/energy-screen interval.
2. EPSILON1-01 established how large an *independent auxiliary drive* would be required and why passive mixing of the recorded unconverged sources was insufficient in the tested cases.
3. EPSILON1-02 showed modewise spectral suppression and exact symmetry/parity tradeoffs in a local canonical mass-mixing family.

**No new physical source was actually constructed.** EPSILON1-03 was proposed as the next action-level microscopic-source test but never executed before the strategy freeze.

## Verification

- **Analytical:** Static Schur norm inequality, exact 2x2 matrix inversion and source demand, ordinary canonical modewise mass-mixing bound, global `U(1)` operator-phase controls.
- **Numerical:** User-executed APPLY/VERIFY runs for all three; science and verification SHA-256 recorded above; original parent hashes checked. `0` physical survivors, no complete repository regression.
- **Dimensional:** The matrix x/y/r/j terms are normalized amplitudes, **not physical amperes, charges or Newtons**. `s` is dimensionless, `k` and masses are inverse meters in the stated canonicalized parameterization. Field screening energies in J cannot be equated with complete operating energy.
- **Limiting cases:** `s=0`, `s→1-`, zero auxiliary drive, positive/negative parent projections, `k→0`, `k→infinity`, equal and disparate auxiliary masses, parity-even/odd coupling.
- **Literature comparison:** No new experimental fifth-force, EDM, axion-like, stellar, matter-coupling or UV viability determination was completed.

## Falsification Attempt

The runs explicitly attempted to destroy the hoped-for passive rescue using missing-source controls, sign-mixed parent ratios, near-critical Hessian sensitivity, high-k suppression, parity and Noether restrictions. Each constrains the hypotheses but none proves a universal no-go for all exotic source actions.

A particularly important caution is that a positive **static** Hessian or favorable quadratic interaction subtraction does not demonstrate positive Lorentzian kinetic residues, stable real source materials, acceptable quantum corrections or a complete energy supply. The term `-<J,f>` is not automatically included in the bound used for the favorable screen.

## Claims Status

`CLAIMS.md` was not evidenced as modified. Suggested freeze state:

```text
EPSILON_1=ARTIFICIAL_SOURCE_DISCOVERY_BRANCH
EPSILON1_00=SCOPED_STATIC_SCHUR_SCREEN_PASS
EPSILON1_01=SCOPED_SOURCE_DEMAND_DERIVED
EPSILON1_02=OPERATOR_SYMMETRY_AND_SPECTRAL_SCREEN_PASS
EPSILON1_03=PROPOSED_NOT_EXECUTED
PHYSICAL_AUXILIARY_CURRENT=NOT_DERIVED
COUPLED_SOURCE_MATERIAL=NOT_SOLVED
FULL_LORENTZIAN_HEALTH=NOT_ESTABLISHED
REAL_GRAVITY_EARTH_CRAFT=NOT_ESTABLISHED
REAL_THRUST=NOT_ESTABLISHED
COMPLETE_ENERGY_LT10MJ=NOT_CERTIFIED
PHYSICAL_SURVIVORS=0
```

## Open Questions

1. Can a real microscopic charged material or spin ensemble independently source `chi` without changing all original PH16 Noether constraints?
2. Does the fully coupled action yield a positive Schur complement after material and neutral-fluid modes are included?
3. What is the exact Fourier/multipole spectrum of the source deficit in a converged coupled solution?
4. Can derivative operators, new symmetry or protected source structure improve the high-k response without a ghost or forbidden direct ordinary-matter force?
5. Do the source and support energies exceed 10 MJ once their actual production and switching are included?
6. Does the new sector provide gravitational repulsion from Einstein stress or only a new fifth force?
7. Can an independent physical source be found without reopening earlier AGMINER failures under merely relabeled coefficients?

## AI Assistance

AI assistant used: **ChatGPT by OpenAI**. AI assistance included design and drafting of the three Python experimental producers, the Schur/2x2/spectral derivations, independent verification code, checksum-based interpretation and the artificial-branch research decision. The user executed the producers/verifiers locally and supplied the resulting artifacts. AI-assisted derivation is not an experimental physics discovery.

## Next Action

At the moment EPSILON1-02 completed, an EPSILON1-03 explicit local covariant source/material action was the next *proposed*, unexecuted research step. After the November 22 antigravity pause, EPSILON-1 must remain **frozen**, not silently continued as the new propulsion program. The R3B Engine's future build plan may borrow its negative controls only after an explicit independent same-action transfer argument.
