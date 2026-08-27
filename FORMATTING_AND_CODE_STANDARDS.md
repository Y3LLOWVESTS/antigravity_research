# Antigravity Research — Formatting and Code Standards

This document defines the mathematical Markdown, source-code documentation,
commenting, and readability standards for the Antigravity Research project.

The central rule is:

> **Write every important document and source file so that a human researcher,
> developer, reviewer, or AI with no access to previous conversations can
> understand what it does, why it exists, what assumptions it makes, and what
> conclusions may or may not be drawn from it.**

---

# 1. GitHub Mathematical Markdown

GitHub supports mathematical expressions using MathJax.

This repository uses a deliberately restricted formatting standard so that
mathematics renders consistently in GitHub and VS Code.

---

## 1.1 Inline mathematics

Use single dollar signs for short expressions inside prose.

Correct:

```markdown
The domain-wall limit occurs at $q=1$.
```

Correct:

```markdown
Repulsion begins when $q>1/2$.
```

Correct:

```markdown
The observed value of $\Lambda$ is too small for laboratory-scale effects.
```

Do not use:

```text
\(q=1\)
```

Do not use:

```text
\\(q=1\\)
```

---

## 1.2 Display mathematics

Use fenced `math` blocks for standalone equations.

Correct:

````markdown
```math
M_{\mathrm{equiv}}
\approx
79.7531\frac{ah^2}{G}
```
````

Another example:

````markdown
```math
\epsilon+p_x+p_y+p_z
\ge
-2\epsilon
```
````

Important results may be boxed:

````markdown
```math
\boxed{
\frac{1}{2}<q\le1
}
```
````

Do not use old display delimiters such as:

```text
\[
...
\]
```

Fenced `math` blocks are the preferred project standard.

---

## 1.3 Do not escape LaTeX inside math blocks

Correct:

```math
M_{\mathrm{equiv}}
```

Incorrect:

```text
M\_{\mathrm{equiv}}
```

Correct:

```math
p_x
```

Incorrect:

```text
p\_x
```

Correct:

```math
\frac{R}{h}
```

---

## 1.4 Do not put grammar punctuation at the end of display equations

Standalone equations should not contain a final period, comma, or semicolon
when that punctuation exists only to complete the surrounding sentence.

Preferred:

```math
q>\frac{1}{2}
```

Avoid:

```text
q>\frac{1}{2}.
```

Preferred:

```math
q=1
```

Avoid:

```text
q=1,
```

Preferred:

```math
\partial_jT^{ij}=0
```

Avoid:

```text
\partial_jT^{ij}=0;
```

This rule applies only to grammatical punctuation.

Mathematically meaningful punctuation remains.

Correct:

```math
\epsilon,\quad
p_r,\quad
p_z,\quad
p_\phi
```

Decimal points must remain:

```math
C_{\mathrm{disk}}=79.753148
```

---

## 1.5 Blank lines around equations

Keep display equations visually separated from prose.

Preferred:

````markdown
The active gravitational source contains

```math
\epsilon+p_x+p_y+p_z
```

Ordinary matter generally has comparatively small stresses.
````

---

## 1.6 Boxing important results

Use `\boxed{}` only for especially important:

- thresholds;
- bounds;
- central equations;
- design principles;
- major simulation conclusions.

Example:

```math
\boxed{
M_{\mathrm{equiv}}
\sim
\frac{ah^2}{G}
}
```

Do not box every equation.

---

## 1.7 Units

Keep units visible when a numerical result includes them.

Example:

```math
E_{\min}
\approx
1.32\times10^{16}\ {\rm J}
```

Example:

```math
M_{\min}
\approx
1.47\times10^{-1}\ {\rm kg}
```

---

## 1.8 Inequalities

Write operators directly.

Correct:

```math
\frac{1}{2}<q\le1
```

Incorrect:

```text
\frac{1}{2}\<q\le1
```

Correct:

```math
M_{\mathrm{ADM}}<0
```

---

## 1.9 Greek symbols

Use normal LaTeX notation.

Examples:

```math
\Lambda
```

```math
\epsilon
```

```math
\tau
```

```math
\phi
```

---

# 2. General Markdown Formatting

## 2.1 Headings

Correct:

```markdown
# Main Heading

## Section

### Subsection
```

Do not wrap headings in bold markers.

Incorrect:

```text
**# Main Heading**
```

---

## 2.2 Lists

Correct:

```markdown
- First item
- Second item
```

Incorrect:

```text
\- First item
```

---

## 2.3 Blockquotes

Correct:

```markdown
> Important research conclusion.
```

Incorrect:

```text
\> Important research conclusion.
```

---

## 2.4 Links

Correct:

```markdown
[`NOTES.md`](NOTES.md)
```

Correct:

```markdown
[APS Journals](https://journals.aps.org/)
```

Do not escape URL punctuation.

---

## 2.5 Paths

Use inline code for short paths:

```markdown
`results/data/`
```

Use fenced blocks for inventories:

```text
src/antigravity_research/geometry/kottler.py
tests/known_solutions/test_kottler.py
simulations/001_kottler_weak_field.py
```

Never escape underscores in filenames.

---

## 2.6 Shell commands

Use fenced Bash blocks:

```bash
PYTHONPATH="$ROOT/src" \
"$PY" -m pytest -q tests/known_solutions
```

Commands stored in documentation should remain directly paste-ready.

---

# 3. Scientific Source-Code Documentation Standard

Every nontrivial scientific source file must begin with substantial
top-of-file documentation.

The header should allow somebody to understand the scientific role of the
file before reading its implementation.

Important files should document, where applicable:

1. Purpose
2. Scientific question
3. Theory or physical model
4. Core equations
5. Inputs
6. Outputs
7. Units
8. Sign conventions
9. Coordinate or observer conventions
10. Assumptions
11. Energy conditions or physical constraints
12. Numerical method
13. Validation strategy
14. Known limitations
15. Interpretation rules
16. Related source modules
17. Related tests
18. Related simulations
19. Claim classification
20. What the file does not establish

This level of documentation is intentionally more extensive than ordinary
application code because these files encode scientific assumptions as well as
software behavior.

---

# 4. Preferred Python Module Header

Use a module docstring near the beginning of each substantial Python source
file.

Example:

```python
"""Finite supported relativistic-tension source model.

PURPOSE
-------
Model the axial gravitational field produced by a finite circular membrane
with relativistic tangential tension and a supporting rim.

SCIENTIFIC QUESTION
-------------------
Can a finite, positive-energy, DEC-compatible source possess a locally
repulsive gravitational near field while retaining positive total mass?

THEORY / MODEL
--------------
Linearized general relativity.

The source consists of:

1. a circular membrane of radius R;
2. positive surface energy density U;
3. tangential tension tau = q U;
4. the support stress required to hold the membrane static.

CORE EQUATIONS
--------------
The static weak-field active source contains

    epsilon + p_x + p_y + p_z.

The membrane tension is

    tau = q U.

The planar local-repulsion threshold is

    q > 1/2.

INPUTS
------
radius_m:
    Membrane radius in meters.

surface_energy_j_m2:
    Surface energy density in joules per square meter.

q:
    Dimensionless ratio tau/U.

OUTPUTS
-------
Functions in this module return quantities including:

- active mass density;
- support stress;
- total mass-energy;
- axial gravitational acceleration;
- dimensionless field factors.

UNITS
-----
SI units unless explicitly documented otherwise.

SIGN CONVENTIONS
----------------
Positive axial acceleration means acceleration away from the upper face of
the source.

Positive tau denotes tension.

ASSUMPTIONS
-----------
- linearized general relativity;
- weak gravitational field;
- static source;
- axisymmetry;
- idealized thin membrane;
- idealized support;
- type-I stress-energy;
- no radiation.

ENERGY CONDITIONS
-----------------
The principal physical branch is intended to satisfy the dominant energy
condition unless explicitly stated otherwise.

NUMERICAL METHOD
----------------
Closed-form expressions are implemented here. Parameter optimization is
performed by the associated simulation files.

VALIDATION
----------
Validation includes:

- analytic limiting cases;
- dimensional checks;
- stress-balance identities;
- pytest regression tests;
- comparison with independently reproduced benchmarks.

LIMITATIONS
-----------
This module does not establish:

- an exact nonlinear Einstein solution;
- finite-thickness material realizability;
- dynamic stability;
- a practical antigravity device.

INTERPRETATION
--------------
A positive outward acceleration in this module represents local gravitational
repulsion in the stated model.

It must not be described as a demonstrated practical antigravity device.

RELATED FILES
-------------
Tests:
    tests/known_solutions/test_finite_tension_disk.py

Simulation:
    simulations/005b_finite_supported_antigravity.py

CLAIM CLASSIFICATION
--------------------
NUMERICAL_MODEL_RESULT

NOVEL PHYSICS CLAIM
-------------------
NO
"""
```

The exact headings may vary, but equivalent information should be preserved.

---

# 5. Simulation File Headers

Simulation files need documentation explaining the experiment itself.

A simulation header should answer:

- What question are we testing?
- Why are we testing it?
- What is the hypothesis?
- Which equations or modules are used?
- Which parameters are scanned?
- What result counts as success?
- What result would falsify or weaken the hypothesis?
- What outputs are produced?
- What claims are permitted?
- What claims remain prohibited?

Example:

```python
"""Simulation 006B — geometry-aware stress-energy optimization.

PURPOSE
-------
Determine how closely a finite, spatially resolved, locally conserved source
can approach the optimistic static DEC energy bound found in Simulation 006A.

HYPOTHESIS
----------
Part of the large coefficient found in Simulation 005B may result from the
specific disk-plus-rim geometry rather than a fundamental GR limitation.

TARGET
------
Minimize total positive energy while producing a required outward
gravitational acceleration at a target point.

OPTIMIZATION VARIABLES
----------------------
Candidate spatial variables include:

    epsilon
    p_r
    p_z
    p_phi
    optional shear stresses

CONSTRAINTS
-----------
- epsilon >= 0
- pointwise dominant energy condition
- discrete local stress-energy conservation
- finite spatial support
- specified target acceleration

SUCCESS CRITERION
-----------------
Find a locally conserved configuration with an energy coefficient
substantially below the Simulation 005B value of approximately 79.753148.

NEGATIVE RESULT
---------------
If local conservation forces the optimum to remain near the 005B coefficient,
that would indicate the finite disk architecture is already relatively
efficient within the modeled class.

OUTPUTS
-------
Expected output types include:

    results/data/
    results/figures/
    results/logs/

CLAIM LIMITS
------------
An optimizer result does not establish a physical material realization, exact
nonlinear GR solution, dynamic stability, or practical device.
"""
```

---

# 6. Test File Headers

Test files should state what scientific regressions they protect against.

Example:

```python
"""Regression tests for the finite tension-disk model.

These tests verify known identities, limiting cases, sign conventions,
energy-condition behavior, and previously established benchmark values.

They are intended to detect:

- algebraic regressions;
- unit errors;
- sign-convention errors;
- numerical instability;
- accidental changes to established benchmark results.

Passing these tests does not independently prove that the underlying physical
model is realizable.
"""
```

---

# 7. Bash Script Headers

Nontrivial Bash scripts should also explain themselves.

Example:

```bash
#!/usr/bin/env bash

# ============================================================================
# Antigravity Research — Full Simulation Regression Runner
#
# PURPOSE
# -------
# Run the known-solution tests and supported simulations while preserving
# timestamped output logs.
#
# EXPECTED LOCATION
# -----------------
# Run from the antigravity_research repository root.
#
# OUTPUTS
# -------
# Test output:
#   terminal
#
# Persistent simulation logs:
#   results/logs/
#
# BEHAVIOR
# --------
# - exits on shell error;
# - does not delete prior results;
# - does not modify scientific source modules;
# - creates timestamped logs.
# ============================================================================
```

---

# 8. Function and Class Documentation

Scientifically significant functions should have docstrings.

At minimum document:

- physical meaning;
- input meaning;
- units;
- return meaning;
- sign convention;
- domain restrictions;
- exceptions;
- important approximation assumptions.

Example:

```python
def axial_acceleration_m_s2(
    height_m: float,
    radius_m: float,
    surface_energy_j_m2: float,
    q: float,
) -> float:
    """Return axial gravitational acceleration above the source.

    Parameters
    ----------
    height_m:
        Height above the source center in meters.

    radius_m:
        Source radius in meters.

    surface_energy_j_m2:
        Positive surface energy density in J/m^2.

    q:
        Dimensionless tension ratio tau/U.

    Returns
    -------
    float
        Axial acceleration in m/s^2.

        Positive:
            outward from the upper face.

        Negative:
            inward toward the source.

    Assumptions
    -----------
    Uses the finite-source linearized-GR model.

    Strong-field corrections and dynamical stability are not included.
    """
```

---

# 9. Comments Explain Why, Not Merely What

Weak comment:

```python
# Multiply by radius.
value *= radius
```

Better:

```python
# Convert the surface quantity into the corresponding integrated rim term.
value *= radius
```

Scientifically useful:

```python
# Mechanical equilibrium requires rim compression C = tau R.
#
# This support term cannot be omitted: doing so would preserve the
# membrane's repulsive stress contribution while ignoring the stresses
# necessary to hold a finite membrane static.
compression = tension * radius
```

Preserve reasoning that would otherwise disappear from the implementation.

---

# 10. Important Equations Near Their Implementation

When code implements an important formula, place the equation nearby.

Example:

```python
# Reissner-Nordstrom neutral-gravity sign-change radius:
#
#     r_rep = Q^2 / (4*pi*epsilon_0*M*c^2)
#
# r < r_rep:
#     local RN gravitational tendency is repulsive
#
# r > r_rep:
#     ordinary attractive tendency
repulsion_radius = (
    charge_c**2
    / (
        4.0
        * math.pi
        * EPSILON_0
        * mass_kg
        * C**2
    )
)
```

---

# 11. Avoid Magic Constants

Avoid:

```python
value = 79.753148116012
```

Prefer:

```python
# Optimized mass coefficient obtained in Simulation 005B for the
# finite q=1 disk-plus-minimum-DEC-rim architecture.
DISK_005B_MASS_COEFFICIENT = 79.753148116012
```

Derive constants whenever practical.

---

# 12. Units Should Be Visible in Variable Names

Prefer:

```text
radius_m
mass_kg
energy_j
pressure_pa
surface_energy_j_m2
acceleration_m_s2
```

Avoid ambiguous names such as:

```text
radius
mass
energy
value
```

unless the quantity is dimensionless or its units are unmistakably documented.

---

# 13. Sign Conventions Must Be Explicit

Any source file involving gravitational direction, pressure, tension,
curvature, junction conditions, or energy flow must state its sign convention.

Example:

```text
positive acceleration = outward
negative acceleration = inward
```

Example:

```text
positive tau = tension
```

Never require a reviewer to infer important signs from the implementation.

---

# 14. Approximation Level Must Be Explicit

Every scientific model should identify itself as one or more of:

- exact general relativity;
- linearized general relativity;
- weak-field expansion;
- Newtonian approximation;
- semiclassical gravity;
- effective theory;
- toy model;
- numerical approximation.

An approximation must never be allowed to look like an exact result.

---

# 15. Separate Mathematical Possibility From Physical Realizability

Successful mathematical calculations should use explicit limitations.

Example:

```text
MATHEMATICAL_CONFIGURATION=YES
LOCAL_REPULSIVE_FIELD=YES
ENERGY_CONDITIONS=PASS
KNOWN_MATERIAL_REALIZATION=NO
DYNAMIC_STABILITY=NOT_ESTABLISHED
PRACTICAL_DEVICE=NO
```

---

# 16. Claim Classification

Use project classifications consistently:

```text
KNOWN_RESULT
REPRODUCED
NUMERICAL_OBSERVATION
NUMERICAL_MODEL_RESULT
NUMERICAL_OPTIMIZATION_RESULT
CONJECTURE
NOVEL_CANDIDATE
REJECTED
NOT_ESTABLISHED
```

A result is not `NOVEL_CANDIDATE` merely because it has not yet appeared in
the project's literature search.

---

# 17. Result Files and Logs

Important simulation files should document:

- output CSV;
- output figures;
- output log;
- primary result labels.

Persistent run logs belong under:

```text
results/logs/
```

Numerical datasets belong under:

```text
results/data/
```

Figures belong under:

```text
results/figures/
```

---

# 18. Validation Standard

Important calculations should ideally have multiple independent validation
layers.

Preferred layers include:

1. dimensional analysis;
2. limiting cases;
3. analytic identities;
4. known-solution reproduction;
5. regression tests;
6. independent numerical implementation;
7. comparison with literature;
8. convergence testing;
9. sensitivity analysis.

A test that merely calls the same function used by a simulation is useful for
regression protection but is not independent scientific validation.

---

# 19. AI Readability Standard

Files must not depend on hidden conversational history.

Another AI should be able to understand the file from repository contents
alone.

Therefore:

- expand uncommon acronyms when first used;
- explain the scientific problem explicitly;
- describe equations by physical meaning;
- state units;
- state signs;
- state assumptions;
- state approximation level;
- identify previous validation;
- identify unresolved questions;
- identify related files;
- explain numerical constants;
- explain result labels.

Avoid:

```python
# Fix old problem.
```

Prefer:

```python
# Use the stable algebraic form of sqrt(1-x)-sqrt(1-y) to avoid
# catastrophic cancellation when both compactness parameters are much
# smaller than floating-point resolution relative to unity.
```

---

# 20. Scientific File Definition of Done

Before considering an important scientific source file complete:

- [ ] Top-of-file documentation is comprehensive.
- [ ] Scientific question is stated.
- [ ] Theory/model is stated.
- [ ] Approximation level is stated.
- [ ] Important equations are documented.
- [ ] Inputs and units are documented.
- [ ] Outputs and units are documented.
- [ ] Sign conventions are documented.
- [ ] Assumptions are documented.
- [ ] Energy-condition assumptions are documented where relevant.
- [ ] Limitations are documented.
- [ ] Claim limits are documented.
- [ ] Related files are identified.
- [ ] Important functions have docstrings.
- [ ] Important constants are explained.
- [ ] Tests exist.
- [ ] Known limiting cases are tested.
- [ ] Simulation output is reproducible.
- [ ] Results are not overstated.

---

# 21. Markdown Definition of Done

Before committing an important Markdown document:

- [ ] Real Markdown headings are used.
- [ ] Bullets are not escaped.
- [ ] Blockquotes are not escaped.
- [ ] Links are not escaped.
- [ ] File paths do not contain escaped underscores.
- [ ] Inline mathematics uses `$...$`.
- [ ] Display mathematics uses fenced `math` blocks.
- [ ] LaTeX underscores inside math are not escaped.
- [ ] Display equations do not end in grammar punctuation.
- [ ] Decimal points remain intact.
- [ ] Mathematically meaningful commas remain intact.
- [ ] Equations render correctly in VS Code or GitHub preview.
- [ ] Bash examples remain paste-ready.

---

# 22. Project Documentation Rule

The preferred standard is:

> **Write documentation for the next researcher, developer, reviewer, or AI
> that has never seen the previous conversation.**

Important scientific code should explain not only **what it computes**, but
also:

- why it exists;
- which physical question it addresses;
- which equations justify it;
- which assumptions it makes;
- how it has been validated;
- where it may fail;
- what conclusions can be drawn;
- what conclusions cannot be drawn.
