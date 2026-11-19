# GAMMA1-00R2 — Stationary evidence and Lorentzian completion ledger

**Scope:** exact algebra, unmodified PH16-04R2 producing-source inspection, and
raw-byte-locked read-only PH16 scientific result summary review. This is
**not** a new PH16/Einstein solve, a kinetic certificate, a material proposal,
or a force calculation. All earlier results remain immutable.

## Question

Can the saved PH16-04R2 stationary Routhian and its numerical JSON alone
uniquely establish the kinetic constraint spectrum, physically transmitted
exterior metric response, or Earth-down/whole-craft-up force?

**Answer at the level tested:** No. The saved JSON reports scalar diagnostics
for the final joint solutions, but does not return the actual final
$F_+(r,z)$, $F_-(r,z)$, $A_X(r,z)$ or $A_Y(r,z)$ arrays. Moreover, the
stationary Routhian is not a unique complete Lorentzian covariant action.
This is an **insufficiency/identifiability finding**, not evidence that the
actual PH16-04R2 source has unstable physical modes.

## Evidence-sufficiency audit

The exact PH16 source SHA is
`b5468671f6418fad7b6ed01d916ea65a95a1d59252b84d4411beed9709f86df0`.
Its `case()` routine solves the Routhian for `pre_x`, then returns the
`pre_solved` dictionary of summaries. The final arrays are not returned.
Its `evaluate(..., details=True)` computes local $E_X$, $B_Y$, $P$,
portal derivatives and frozen magnetic margin, then exports selected norms,
minima and maxima only.

The original raw PH16-04R2 JSON (not a generated approximation) must be
matched to SHA
`ff700285effc35841fbb8d0e20cffa3c8e4b812e6629b549785a2304b716b2b0`.
We check all three source meshes, recorded 400/400 Noether values, native
joint convergence and positive **frozen** magnetic margin, while explicitly
preserving the 18/L12 weak-seed failure. Do not treat the latter as proof of
uniqueness or healthy dynamics.

## Exact covariant-completion nonuniqueness witness

Take a normalized timelike four-velocity $u^\mu$ of a hypothetical dynamical
neutral fluid and the Y field strength $F^Y_{\mu\nu}$. Consider the *diagnostic
family* (not a proposed new mechanism or a tuned gravity operator):

$\Delta\mathcal L_\eta = (\eta/2)
(u^\mu F^Y_{\mu\nu})(u^\rho F^Y_{\rho}{}^{\nu})$.

The term is gauge invariant and a diffeomorphism scalar when $u^\mu$ is
dynamical and transforms as a four-vector. It is quadratic in the Y electric
field measured by the fluid; it **vanishes on the PH16 static Y-magnetic
ansatz** and so do its first variations along that ansatz. It does not by
itself impose Earth charge, source current or an external anchor.

In an instantaneous local Minkowski rest frame, with transverse Y electric
amplitude $e$ and magnetic amplitude $b$, the quadratic density is

$\mathcal L^{(2)}_\eta=(1+\eta)e^2/2-b^2/2$.

The electric Hessian is $1+\eta$; for $\eta=-2,0,+2$ it is $-1,+1,+3$.
All three choices agree on the entire magnetostatic sector to first order,
but have different Lorentzian kinetic and characteristic behavior. In a
frozen-fluid, transverse linear test,
$(1+\eta)\omega^2=k^2$. Both SymPy and independently calculated exact
rational finite differences check the Hessian values.

This is **not** evidence for a ghost on PH16. In particular, choosing
$\eta=-2$ defines a different theory, not a property of the existing
stationary model. The point is logical: stationary data cannot tell us
which covariant completion, or which physical constraints, was actually
realized. A covariant addition must eventually be justified by a specified
source/kinetic action, fluid equations, gauge/Noether/Bianchi identities,
empirical restrictions and EFT/UV completion, not merely by preserving a
static Routhian.

## Controls and limits

- The witness never modifies PH16 field equations or original data.
- Y electric off, coupling off and $\eta=0$ serve as null/Maxwell controls.
- $\eta=+2$ and $-2$ discriminate healthy-looking and unhealthy local
  transverse signs without certifying full constrained stability.
- The gauge variation is zero because $F_Y=dA_Y$ and $d^2=0$.
- Exact all-stress GR energy obstructions from GAMMA1-00 remain conditional;
  source-free *material* stand-off does not imply a stress-free gap.
- No externally sourced metric field, whole-craft reaction, emitted momentum,
  genuine SI normalization, 1-kg torus force, or strict $<10$ MJ energy is
  supplied by this test.
- 006D remains the strongest conservative finite positive-energy local
  repulsion reference, with $C=23.591586299249$, and is **unreplaced**.
- Historical PH14, PH15, PH16, ALPHA/M5V, BETA1-04 and AGMINER negative
  outcomes remain frozen; no past failure is relabeled.

## Research decision

**STOP generic artificial scans.** GAMMA1-01, PH16-05 and PH17 are not
implicitly authorized. The actual next *physics* contract is to (i) specify a
unique full Lorentzian action with charged source, X/Y, neutrals, fluid
velocity, supports, Earth, gravity and boundary terms, (ii) archive the native
joint field arrays plus gauge and units in a new immutable artifact, using a
justified source replay only if strictly necessary, (iii) derive constrained
modes and metric/exterior/Earth-craft response, and (iv) re-evaluate SI and
empirical/quantum/UV energy gates. Do not re-solve all PH16 meshes or initiate
an expensive continuum solver simply to increase test counts.
