# Antigravity Research — Research Buildplan

This document is the active execution plan for Antigravity Research.

It is intended to keep the project focused on the experiments, derivations,
simulations, and falsification tests that provide the greatest increase in
scientific knowledge per unit of research time.

This is a living document.

It should be updated whenever:

- a major simulation is completed;
- a major branch is falsified;
- a new constraint changes research priorities;
- a substantially better pathway is identified;
- the active scientific frontier changes.

It should not be rewritten after every small code change.

---

# 1. Purpose

The purpose of this buildplan is to answer one question as efficiently and
rigorously as possible:

> **What physically consistent mechanism offers the most plausible path toward
> controllable, measurable local gravitational repulsion?**

The goal is not merely to produce mathematical examples of repulsion.

The project should progressively narrow the space of possibilities toward
configurations that satisfy increasingly demanding physical requirements.

---

# 2. Operational Definition of the Target

For this project, a useful antigravity candidate should ultimately produce a
measurable outward gravitational effect on neutral matter.

The preferred observables are:

- relative free-fall acceleration;
- geodesic deviation;
- proper acceleration requirements;
- invariant curvature effects;
- other clearly operational gravitational observables.

Coordinate acceleration alone is not sufficient evidence.

The primary target is **local gravitational repulsion**.

A successful local source does not need to produce an outward asymptotic field.

A finite positive-total-mass system may have:

```math
\text{repulsive near field}
```

and simultaneously:

```math
\text{attractive far field}
```

That is acceptable.

---

# 3. Success Ladder

Research candidates should be evaluated against the following ladder.

## Level 0 — Mathematical sign

A calculation contains a quantity that appears repulsive.

This is only a preliminary observation.

## Level 1 — Physical gravitational observable

The repulsion survives an invariant or operational gravitational test.

Examples:

- geodesic deviation;
- proper acceleration;
- relative free-fall acceleration.

## Level 2 — Established-theory consistency

The configuration satisfies the equations of the stated theory.

For baseline work this means ordinary general relativity or
Einstein-Maxwell theory.

## Level 3 — Acceptable stress-energy

The required stress-energy is characterized.

Relevant questions include:

- positive or negative energy;
- NEC;
- WEC;
- SEC;
- DEC;
- anisotropy;
- pressure or tension magnitude.

## Level 4 — Finite source

The effect is produced by a finite localized configuration rather than an
infinite idealization.

## Level 5 — Local conservation

The complete source satisfies the appropriate local conservation equations.

For a static weak-field source this includes the appropriate form of

```math
\nabla_\mu T^{\mu\nu}=0
```

rather than merely an integrated stress-balance condition.

## Level 6 — Stability

The source survives:

- mechanical stability analysis;
- dynamical perturbations;
- field instability;
- discharge;
- collapse;
- runaway behavior;
- relevant quantum instability.

## Level 7 — Physical realization

A known or theoretically plausible field or material can generate the required
stress-energy.

## Level 8 — Energetic plausibility

Required total energy, energy density, pressure, field strength, and geometry
are within remotely plausible physical ranges.

## Level 9 — Experimental accessibility

A measurable laboratory-scale test can be defined.

## Level 10 — Practical antigravity

A controllable apparatus produces useful gravitational repulsion.

The project is not currently at Level 10.

Progress should never be described as though a higher level has been reached
before its requirements are actually satisfied.

---

# 4. Scientific Priority Rule

When choosing between two research tasks, prefer the task that most strongly
does one or more of the following:

1. falsifies an important candidate;
2. removes a major uncertainty;
3. independently verifies a central result;
4. establishes a stronger physical constraint;
5. reduces required energy or stress by a substantial factor;
6. converts an idealized source into a more physically complete source;
7. produces a clear decision about whether an entire research branch should
   continue.

Prefer decisive calculations over broad speculative exploration.

---

# 5. Evidence Hierarchy

Evidence should generally be weighted in the following order.

## Strongest

- exact analytical result;
- exact known GR solution;
- independent derivations agreeing;
- independent numerical implementations agreeing;
- comparison with peer-reviewed literature;
- experimentally established physics.

## Strong

- converged numerical solution;
- verified conservation laws;
- multiple independent tests;
- dimensional and limiting-case checks;
- stable numerical optimization with independent reconstruction.

## Intermediate

- one internally tested numerical model;
- linearized approximation;
- idealized thin-shell or thin-wall model;
- optimization with incomplete geometry.

## Weak

- one unverified numerical result;
- analogy;
- coordinate acceleration;
- dimensional coincidence;
- speculative mechanism without a stress-energy model.

Research priority should increase when a weak but promising result can cheaply
be promoted to a stronger evidence class.

---

# 6. Current Scientific Frontier

The current classical-GR problem is the gap between the optimistic abstract
static DEC result

```math
M_{\mathrm{abstract}}
\sim
1\frac{ah^2}{G}
```

and the explicit finite supported disk architecture

```math
M_{\mathrm{disk}}
\approx
79.753148\frac{ah^2}{G}
```

Therefore the active uncertainty is approximately

```math
1
\le
C_{\mathrm{physical}}
\le
79.753148
```

where

```math
M
=
C_{\mathrm{physical}}
\frac{ah^2}{G}
```

The coefficient $1$ is not currently a universal GR theorem.

The coefficient $79.753148$ is not currently known to be optimal.

Determining the actual penalty imposed by geometry and local conservation is
the highest-value classical problem.

---

# 7. Active Research Path

## Phase A — Regression Integrity

Before adding major new physics:

```text
GOAL:
Verify the complete existing known-solution suite.

PASS:
All expected tests pass.

FAIL:
Investigate the regression before extending the model.
```

Do not build new conclusions on a broken baseline.

---

## Phase B — Simulation 006B

### Geometry-Aware DEC Stress-Energy Optimizer

This is the current highest-priority simulation.

### Scientific question

How close can a finite spatially resolved source satisfying local conservation
and pointwise DEC approach

```math
M
=
\frac{ah^2}{G}
```

### Initial geometry

Use axisymmetry to reduce computational cost while retaining meaningful source
geometry.

### Candidate variables

Spatial cells may contain quantities such as

```math
\epsilon,\quad
p_r,\quad
p_z,\quad
p_\phi
```

and shear stresses if required.

### Required constraints

At minimum:

```math
\epsilon\ge0
```

pointwise DEC constraints,

```math
|p_i|\le\epsilon
```

and discrete local stress-energy conservation.

### Objective

Minimize

```math
\int\epsilon\,dV
```

while requiring a specified outward gravitational acceleration at the target.

### Most important output

Determine the optimized coefficient

```math
C_{\mathrm{006B}}
```

in

```math
M
=
C_{\mathrm{006B}}
\frac{ah^2}{G}
```

### Decision interpretation

If

```math
C_{\mathrm{006B}}\sim1-5
```

then the existing disk architecture is highly inefficient and classical
positive-energy stress engineering remains especially interesting.

If

```math
C_{\mathrm{006B}}\sim10-100
```

then finite geometry and local conservation impose a substantial penalty.

If

```math
C_{\mathrm{006B}}\approx79.753
```

then the existing disk architecture may already be surprisingly efficient.

No numerical threshold above should be treated as a fundamental physical
boundary. They are research-decision ranges.

---

## Phase C — Simulation 006C

### Independent Finite-Disk Field Verification

Simulation 005B should be independently reconstructed without reusing its
analytic field implementation.

Targets include reproduction of

```math
\frac{z_{\mathrm{zero}}}{R}
\approx
0.393319893
```

and

```math
\frac{R}{h}
\approx
4.00614967
```

for the appropriate optimized configuration.

### Gate

Do not treat the coefficient

```math
79.753148
```

as highly reliable until an independent implementation reproduces the
underlying gravitational field.

---

## Phase D — Simulation 006D

### Finite-Thickness Locally Conserved Source

Replace ideal distributional membranes and rims with finite-thickness
stress-energy.

Explicitly evaluate local conservation through the entire source, especially
near interfaces and support regions.

Evaluate:

- NEC;
- WEC;
- DEC;
- stress gradients;
- support forces;
- compactness;
- numerical convergence.

### Gate

A finite source should not be promoted to a physically self-consistent matter
configuration until its complete stress-energy is locally conserved.

---

# 8. Classical-GR Decision Gate

After 006B, 006C, and 006D, make an explicit decision.

## Continue classical positive-energy stress engineering if

- local conservation can be satisfied;
- the repulsive near field survives;
- the energy coefficient falls substantially;
- a plausible field-theory stress source can be identified;
- additional optimization has clear expected value.

## Deprioritize the classical branch if

- conservation destroys the repulsive field;
- every physically complete architecture remains enormously expensive;
- stability creates unavoidable failure;
- no plausible stress-energy realization exists;
- repeated geometry changes produce only minor coefficient improvements.

A negative result is useful.

The objective is to eliminate weak routes quickly rather than preserve them
indefinitely.

---

# 9. Quantum Branch

The quantum branch begins only after the classical decision gate unless new
evidence strongly changes priorities.

## Simulation 007A — Complete Casimir Benchmark

Model:

- negative Casimir-region stress-energy;
- plates;
- supports;
- total apparatus energy;
- complete gravitational response.

Never count only the negative vacuum contribution while ignoring the apparatus
required to produce it.

## Simulation 007B — Quantum Energy Inequality Bound

Estimate allowed negative stress-energy as a function of spatial and temporal
scale.

Construct a bound of the approximate form

```math
a_{\max}(h,\tau)
```

and determine whether quantum negative energy can materially outperform the
classical positive-energy route.

## Simulation 007C — Dynamic Sources

Investigate whether nonstatic stress-energy can reduce support penalties.

Candidate systems include:

- scalar-field pulses;
- moving domain walls;
- oscillating anisotropic stress;
- transient field configurations.

Do not assume time dependence removes pointwise energy constraints.

---

# 10. Modified-Gravity Gate

Modified gravity should remain deferred until established physics has been
quantitatively constrained.

Candidate later theories may include:

- scalar-tensor gravity;
- $f(R)$ gravity;
- Horndeski-type models;
- vector-tensor gravity;
- massive gravity;
- other observationally constrained theories.

A modified theory should not be selected merely because it permits repulsion.

A candidate theory must also be evaluated for:

- independent motivation;
- internal consistency;
- absence of pathological degrees of freedom;
- observational constraints;
- gravitational-wave constraints;
- solar-system constraints;
- cosmological consistency.

---

# 11. Pathway Priority Matrix

Use a qualitative score from 0 to 5.

This matrix is a research-management tool, not a scientific measurement.

| Criterion | Meaning |
| --- | --- |
| Theory confidence | How firmly established is the underlying physics? |
| Repulsion evidence | How strongly is actual gravitational repulsion established? |
| Finite-source maturity | How close is the model to a finite complete source? |
| Energy prospects | Is there evidence the energy requirement can become reasonable? |
| Realizability | Is there a plausible physical stress-energy source? |
| Testability | Could the mechanism eventually produce an observable experiment? |
| Information gain | Will the next calculation strongly change our decisions? |

Priority should be driven especially strongly by:

```text
THEORY_CONFIDENCE
+
INFORMATION_GAIN
+
FALSIFICATION_POWER
```

rather than novelty alone.

---

# 12. Current Pathway Ranking

## Priority 1 — Finite positive-energy relativistic stress

Examples:

```text
006B
006C
006D
```

Reason:

- established GR;
- local repulsion already demonstrated in related models;
- finite source exists at linearized level;
- major unresolved coefficient gap;
- next calculations have high information value.

Status:

```text
ACTIVE
```

---

## Priority 2 — Quantum stress-energy

Examples:

```text
007A
007B
007C
```

Reason:

- established quantum field theory can violate classical pointwise energy
  conditions;
- may provide a route around classical constraints;
- severe quantum inequalities may instead eliminate the route quickly.

Status:

```text
QUEUED_AFTER_CLASSICAL_GATE
```

---

## Priority 3 — Einstein-Maxwell / Reissner-Nordstrom

Reason:

- exact GR mechanism;
- positive-energy local repulsion;
- strong proof of principle;
- extreme charge and electric-field requirements make it poor as the primary
  engineering route.

Status:

```text
REFERENCE_SOLUTION
```

---

## Priority 4 — Pure cosmological constant

Reason:

- physically valid repulsion;
- observed magnitude is far too small.

Status:

```text
REFERENCE_BASELINE
```

---

## Priority 5 — Negative ADM mass

Reason:

- mathematically repulsive;
- current shell construction requires exotic negative surface energy;
- conventional positive-energy assumptions strongly disfavor the branch.

Status:

```text
LOW_PRIORITY
```

---

## Priority 6 — Modified gravity

Reason:

- potentially broad design freedom;
- enormous theory space;
- easy to generate desired effects by assumption;
- lower scientific information value until ordinary GR and semiclassical
  routes are sharply constrained.

Status:

```text
DEFERRED
```

---

# 13. Research Stop Rules

A branch should be paused or rejected when one or more of the following occurs.

1. The apparent repulsion is shown to be a coordinate artifact.
2. Independent calculation fails to reproduce the effect.
3. Required stress-energy violates assumptions that defined the branch.
4. Local conservation cannot be satisfied.
5. Stability destroys the configuration.
6. A physical requirement exceeds a known fundamental bound with no available
   escape mechanism.
7. Several successive optimizations improve only minor numerical factors while
   the remaining feasibility gap spans many orders of magnitude.
8. Continuing the branch has substantially lower expected information value
   than another available experiment.

Do not keep a branch alive merely because substantial time has already been
spent on it.

---

# 14. Anti-Drift Rules

Do not:

- jump to modified gravity because classical calculations are difficult;
- confuse mathematical existence with engineering feasibility;
- interpret coordinate acceleration as sufficient evidence;
- optimize an unverified formula indefinitely;
- repeatedly test the same implementation against itself;
- ignore support stresses;
- ignore the rest of an apparatus when counting exotic energy;
- call a result novel because it has not yet appeared in our literature
  search;
- spend large amounts of time polishing code before the underlying physics
  survives its next scientific gate;
- increase model complexity before the simpler model's failure mode is
  understood.

---

# 15. Independent Verification Rule

Central quantitative results should eventually have at least two independent
paths of verification.

Examples:

```text
analytic derivation
vs
numerical integration
```

or

```text
independent implementation A
vs
independent implementation B
```

or

```text
project calculation
vs
published benchmark
```

Tests that simply call the same production function used by the simulation are
important regression tests but are not independent scientific verification.

---

# 16. Efficiency Protocol for a Research Session

Default short-session workflow:

## Step 1 — Orient

Read:

```text
RESEARCH_BUILDPLAN.md
```

and identify the single active `NEXT` action.

Avoid opening new research branches before the active task is understood.

## Step 2 — State the question

Write one sentence describing exactly what the session is attempting to learn.

## Step 3 — Choose the cheapest decisive test

Before implementing a large model, ask whether:

- algebra;
- dimensional analysis;
- a limiting case;
- a small numerical experiment;
- a literature check

could answer the question faster.

## Step 4 — Implement one coherent slice

Avoid mixing:

- new physics;
- major refactors;
- unrelated documentation cleanup;
- multiple speculative branches

inside one research slice.

## Step 5 — Verify

Use the cheapest appropriate combination of:

- focused tests;
- analytic checks;
- known limits;
- dimensional analysis;
- numerical reconstruction.

## Step 6 — Interpret

Record:

```text
WHAT_CHANGED
WHAT_WAS_LEARNED
WHAT_WAS_FALSIFIED
CLAIM_CLASSIFICATION
NEXT
```

## Step 7 — Preserve

Store durable results in the appropriate:

```text
results/data/
results/figures/
results/logs/
NOTES.md
```

location.

---

# 17. Default Time Allocation

For approximately one hour of research time, use the following as a default,
not a rigid rule:

```text
5 minutes:
Orient and define the question.

35-40 minutes:
Perform the highest-value calculation or implementation.

10-15 minutes:
Verify, falsify, and inspect the result.

5 minutes:
Update notes and set the next action.
```

If a failure occurs, prioritize understanding the failure rather than forcing
the planned task to completion.

---

# 18. Required Output for Every Major Simulation

Every major simulation should identify:

```text
SCIENTIFIC_QUESTION
MODEL
APPROXIMATION_LEVEL
ASSUMPTIONS
INPUTS
OUTPUTS
PRIMARY_OBSERVABLE
ENERGY_CONDITIONS
CONSERVATION_STATUS
VALIDATION_METHOD
LIMITATIONS
CLAIM_CLASSIFICATION
NEXT
```

Important output should be preserved in:

```text
results/logs/
```

when practical.

---

# 19. Quantities to Track Across Candidate Architectures

To compare different antigravity pathways consistently, track wherever
applicable:

```math
C
```

in

```math
M
=
C\frac{ah^2}{G}
```

as well as:

- total energy;
- energy density;
- principal pressures;
- stress-to-energy ratios;
- source-target distance;
- source size;
- compactness;
- local-conservation residual;
- energy-condition margins;
- repulsive-zone extent;
- field strength;
- stability indicators;
- required charge;
- required quantum sampling time;
- sensitivity to geometry.

This allows very different mechanisms to be compared using common physical
criteria.

---

# 20. Claim Promotion Gates

A result may move from `NUMERICAL_OBSERVATION` toward a stronger project claim
only after appropriate checks.

A central result should ideally survive:

```text
DIMENSIONAL_CHECK
LIMITING_CASE_CHECK
FOCUSED_TEST
INDEPENDENT_RECONSTRUCTION
LITERATURE_COMPARISON
ASSUMPTION_AUDIT
```

where applicable.

No internal result should be called a discovery solely because it survives
project tests.

---

# 21. Documentation Discipline

Use the repository files for distinct purposes.

```text
README.md
    Public project overview.

RESEARCH_BUILDPLAN.md
    Active research strategy and execution order.

ROADMAP.md
    Broad long-term subject map.

RESEARCH_QUESTIONS.md
    Question inventory.

ASSUMPTIONS.md
    Shared assumptions.

CLAIMS.md
    Formal claim classifications.

NOTES.md
    Detailed chronological research history.

FORMATTING_AND_CODE_STANDARDS.md
    Documentation, Markdown, math, and source-code standards.
```

Avoid duplicating large amounts of chronological detail in this buildplan.

The buildplan should stay focused on:

```text
CURRENT_FRONTIER
ACTIVE_TASK
DECISION_GATES
PRIORITIES
STOP_RULES
NEXT
```

---

# 22. Current Checkpoint

Current strongest project interpretation:

> **Local gravitational repulsion is permitted in ordinary general relativity,
> and relativistic stress/tension is a recurring mechanism capable of producing
> it without requiring negative energy.**

Current finite-source status:

```text
FINITE_LINEARIZED_REPULSIVE_MODEL=YES
POSITIVE_TOTAL_ENERGY=YES
ATTRACTIVE_FAR_FIELD=YES
FULL_LOCAL_CONSERVATION=NOT_YET_ESTABLISHED
FINITE_THICKNESS_REALIZATION=NOT_YET_ESTABLISHED
DYNAMIC_STABILITY=NOT_YET_ESTABLISHED
KNOWN_PRACTICAL_MATERIAL=NO
PRACTICAL_ANTIGRAVITY_DEVICE=NO
```

Current optimization status:

```text
ABSTRACT_STATIC_DEC_COEFFICIENT=1
DOMAIN_WALL_ABSTRACT_COEFFICIENT=2
FINITE_DISK_COEFFICIENT=79.753148
```

The coefficient $1$ remains an optimistic abstract result under stated
assumptions rather than a universal theorem.

---

# 23. Current Active Task

```text
ACTIVE_PHASE=006B
ACTIVE_TASK=GEOMETRY_AWARE_DEC_STRESS_ENERGY_OPTIMIZER
PRIMARY_QUESTION=HOW_MUCH_DO_GEOMETRY_AND_LOCAL_CONSERVATION_INCREASE_C
BASELINE_LOWER_REFERENCE=1
CURRENT_EXPLICIT_ARCHITECTURE=79.753148
```

Primary target:

```math
\boxed{
\text{Determine the lowest coefficient achievable by a finite locally conserved DEC source}
}
```

---

# 24. Planned Execution Order

```text
0. Full regression verification

1. 006B
   Geometry-aware DEC optimizer with local conservation

2. 006C
   Independent numerical verification of 005B

3. 006D
   Finite-thickness locally conserved realization

4. CLASSICAL DECISION GATE

5. 007A
   Complete Casimir apparatus benchmark

6. 007B
   Quantum-energy-inequality bound

7. 007C
   Dynamic stress-energy sources

8. QUANTUM DECISION GATE

9. 008
   Constrained modified-gravity investigation
```

This order may change only when new evidence materially changes expected
scientific value.

---

# 25. Immediate Next Action

```text
NEXT=VERIFY_FULL_REGRESSION_THEN_BEGIN_006B
```

The first 006B implementation should be the smallest axisymmetric model capable
of simultaneously testing:

```text
POINTWISE_POSITIVE_ENERGY
POINTWISE_DEC
DISCRETE_LOCAL_CONSERVATION
ACTUAL_SPATIAL_GRAVITATIONAL_KERNEL
TARGET_OUTWARD_ACCELERATION
TOTAL_ENERGY_MINIMIZATION
```

Do not begin with an unnecessarily high-resolution or fully general tensor
optimization.

First prove the optimization formulation is correct on a small grid.

Then establish convergence.
