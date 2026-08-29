# Antigravity Research — Formatting and Code Standards

This document defines the mathematical Markdown, scientific source-code documentation, commenting, validation, and readability standards for **Antigravity Research**.

The central rule is:

> **Write every important document and source file so that a human researcher, developer, reviewer, or AI with no access to previous conversations can understand what it does, why it exists, what assumptions it makes, how it was validated, and what conclusions may or may not be drawn from it.**

The repository deliberately uses a **restricted GitHub-math subset** rather than every feature available in general LaTeX or MathJax.

Reliability on GitHub is more important than decorative mathematical formatting.

---

# 1. GitHub Mathematical Markdown

## 1.1 General rule

Repository Markdown must render correctly on GitHub.

Do not assume that a command supported by LaTeX, KaTeX, a local editor, or another MathJax installation is supported by GitHub's renderer.

Use simple mathematical markup whenever possible.

Preferred hierarchy:

```text
PLAIN_LATEX_SYMBOLS
>
SIMPLE_STANDARD_MACROS
>
COMPLICATED_OR_DECORATIVE_MACROS
```

If two representations are mathematically equivalent, use the simpler one.

---

## 1.2 Inline mathematics

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

Do not use inline mathematics for long derivations.

---

## 1.3 Display mathematics

Use fenced `math` blocks for standalone equations.

Correct:

````markdown
```math
M_{\mathrm{equiv}}
=
C\frac{ah^2}{G}
```
````

Correct:

````markdown
```math
\epsilon+p_x+p_y+p_z
\ge
-2\epsilon
```
````

Do not use:

```text
\[
...
\]
```

Do not use:

```text
$$
...
$$
```

Fenced `math` blocks are the repository standard.

---

## 1.4 Do not use `\boxed`

Do **not** use:

```text
\boxed{...}
```

in repository Markdown.

GitHub rendering failures have occurred with boxed expressions, particularly multiline expressions.

Instead, emphasize important results in surrounding Markdown.

Preferred:

````markdown
The central result is:

```math
M
=
C\frac{ah^2}{G}
```

> **This is the principal energy-scaling relation for the tested source class.**
````

Do not write:

````markdown
```math
\boxed{
M
=
C\frac{ah^2}{G}
}
```
````

Mathematical emphasis should come from the document structure, not decorative TeX wrappers.

---

## 1.5 Do not use `\operatorname`

GitHub has rejected `\operatorname` in this repository.

Do not use:

```text
\operatorname{diag}
\operatorname{sign}
\operatorname{erf}
\operatorname{sech}
```

Use conservative alternatives:

```math
\mathrm{diag}
```

```math
\mathrm{sgn}
```

```math
\mathrm{erf}
```

```math
\mathrm{sech}
```

Example:

```math
T_{\hat\mu\hat\nu}
=
\mathrm{diag}
\left(
\epsilon,
p_r,
p_\phi,
p_z
\right)
```

---

## 1.6 Avoid formatting commands inside mathematics

Do not use:

```text
\textbf{...}
```

inside math blocks.

Use Markdown bold outside the equation instead.

Avoid putting long prose inside mathematics when ordinary Markdown prose is clearer.

Short labels using `\text{...}` may be used only when mathematically necessary and known to render correctly.

Prefer:

````markdown
The condition corresponds to the stable branch:

```math
E''(1)>0
````

````

over embedding an explanatory sentence inside the equation.

---

## 1.7 Preferred function and unit notation

Use `\mathrm{...}` for short mathematical function names and physical units.

Preferred:

```math
\mathrm{diag}
````

```math
\mathrm{erf}
```

```math
\mathrm{sech}
```

Preferred units:

```math
E
=
1.32\times10^{16}\ \mathrm{J}
```

```math
M
=
1.47\times10^{-1}\ \mathrm{kg}
```

```math
a
=
9.80665\ \mathrm{m\,s^{-2}}
```

Prefer `\mathrm{...}` over older forms such as:

```text
{\rm J}
{\rm kg}
```

when writing new documentation.

Existing correctly rendered historical mathematics does not need to be rewritten solely for style.

---

## 1.8 Do not escape LaTeX inside math blocks

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

Incorrect:

```text
\frac\{R\}\{h\}
```

---

## 1.9 Inequalities and operators

Write mathematical operators directly.

Correct:

```math
\frac12<q\le1
```

Incorrect:

```text
\frac12\<q\le1
```

Correct:

```math
M_{\mathrm{ADM}}<0
```

Correct:

```math
k_\infty^2>s^2
```

---

## 1.10 Greek symbols

Use ordinary LaTeX notation.

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

```math
\eta
```

---

## 1.11 Braces and delimiters

Every math block must have balanced braces.

Correct:

```math
\frac{
m(m+2)
}{
4(1-\eta)
}
```

Every `\left` must have a corresponding `\right`.

Correct:

```math
\left(
1+x^2
\right)
```

Every environment must be closed.

Correct:

```math
\begin{pmatrix}
a & b \\
c & d
\end{pmatrix}
```

Before committing important Markdown, verify:

```text
BRACES_BALANCED=YES
LEFT_RIGHT_BALANCED=YES
BEGIN_END_BALANCED=YES
```

---

## 1.12 Keep display mathematics structurally simple

Prefer several simple equations over one deeply nested decorated expression.

Preferred:

```math
Q_+
=
\int S_+\,dV
```

followed by:

```math
Q_-
=
\int S_-\,dV
```

and then:

```math
Q_+>Q_-
```

rather than wrapping an entire multi-equation derivation inside a decorative environment.

This improves:

* GitHub reliability;
* human readability;
* diff readability;
* AI parsing;
* future automated auditing.

---

## 1.13 Display-equation punctuation

Do not place grammatical punctuation at the end of standalone equations when the punctuation serves only the surrounding sentence.

Preferred:

```math
q>\frac12
```

Avoid:

```text
q>\frac12.
```

Preferred:

```math
\partial_jT^{ij}=0
```

Avoid:

```text
\partial_jT^{ij}=0;
```

Mathematically meaningful punctuation remains valid.

Correct:

```math
\epsilon,\quad
p_r,\quad
p_\phi,\quad
p_z
```

Decimal points remain unchanged:

```math
C_{\mathrm{finite}}
=
23.591586299249
```

---

## 1.14 Blank lines around display mathematics

Keep display equations visually separated from prose.

Preferred:

````markdown
The active gravitational source is

```math
S
=
\epsilon+p_r+p_\phi+p_z
```

The sign of its weighted spatial integral determines the local field direction.
````

---

# 2. Mandatory GitHub-Math Audit

Rendering problems should be caught **before** committing important Markdown.

At minimum, important repository Markdown must be checked for known-problematic constructs.

The following must normally return no matches:

```bash
git grep -nF '\operatorname' -- '*.md' || true
git grep -nF '\boxed' -- '*.md' || true
git grep -nF '\textbf' -- '*.md' || true
```

Interpretation:

```text
OPERATORNAME_IN_MARKDOWN=
FORBIDDEN

BOXED_IN_MARKDOWN=
FORBIDDEN

TEXTBF_IN_MATH=
FORBIDDEN
```

A `\textbf` occurrence in ordinary explanatory code examples may require manual inspection, but it should not occur inside repository math blocks.

For major README, journal, notes, claims, or buildplan changes, also verify:

```text
MATH_FENCES_BALANCED
BRACES_BALANCED
LEFT_RIGHT_BALANCED
BEGIN_END_BALANCED
```

If an automated Markdown math-audit script exists in the repository, it should be run before committing major documentation changes.

---

# 3. General Markdown Formatting

## 3.1 Headings

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

## 3.2 Lists

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

## 3.3 Blockquotes

Correct:

```markdown
> Important research conclusion.
```

Incorrect:

```text
\> Important research conclusion.
```

---

## 3.4 Links

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

## 3.5 Paths

Use inline code for short paths:

```markdown
`results/data/`
```

Use fenced text blocks for inventories:

```text
src/antigravity_research/geometry/kottler.py
tests/known_solutions/test_kottler.py
simulations/001_kottler_weak_field.py
```

Never escape underscores in filenames.

---

## 3.6 Shell commands

Use fenced Bash blocks:

```bash
PYTHONPATH="$ROOT/src" \
"$PY" -m pytest -q tests/known_solutions
```

Commands intended for users should remain directly paste-ready.

For the project's interactive macOS/zsh workflow, avoid relying on shell state from previous command blocks.

Do not use `set -u` in interactive research blocks unless there is a specific reason and compatibility has been verified.

When command success is obscured by a pipeline such as:

```bash
python simulation.py | tee output.log
```

preserve the actual program return code or enable an appropriate pipe-failure check.

---

# 4. Scientific Source-Code Documentation Standard

Every nontrivial scientific source file must begin with substantial top-of-file documentation.

The header should allow a researcher to understand the scientific role of the file before reading the implementation.

Document, where applicable:

1. Purpose
2. Scientific question
3. Physical model
4. Governing equations
5. Operational observable
6. Inputs
7. Outputs
8. Units
9. Sign conventions
10. Coordinates or observer conventions
11. Assumptions
12. Approximation level
13. Energy conditions or other physical constraints
14. Conservation requirements
15. Stability assumptions
16. Numerical method
17. Validation strategy
18. Falsification strategy
19. Known limitations
20. Related source files
21. Related tests
22. Related simulations
23. Related journal or notes entry
24. Claim classification
25. What the file does **not** establish

Scientific source documentation is intentionally more extensive than ordinary application code because the implementation encodes physical assumptions as well as software behavior.

---

# 5. Preferred Python Module Header

A substantial scientific Python module should use a module docstring similar to:

```python
"""Finite supported relativistic-stress source model.

PURPOSE
-------
Model the gravitational field generated by a finite anisotropic source.

SCIENTIFIC QUESTION
-------------------
Can a finite positive-energy source generate outward gravitational
acceleration while satisfying the declared conservation and energy-condition
constraints?

PHYSICAL MODEL
--------------
Static linearized general relativity with an axisymmetric type-I source.

PRIMARY OBSERVABLE
------------------
Finite-payload or point-target axial gravitational acceleration, as declared
by the associated simulation.

CORE EQUATIONS
--------------
The active source is

    S = epsilon + p_r + p_phi + p_z.

The physical weak-field acceleration follows from the linearized-GR
Green-function integral.

INPUTS
------
Document every important parameter and its physical meaning.

OUTPUTS
-------
Document returned observables, diagnostics, and persistent result files.

UNITS
-----
SI units unless explicitly declared otherwise.

SIGN CONVENTIONS
----------------
Positive axial acceleration means outward from the source toward the target.

ASSUMPTIONS
-----------
List physical and numerical assumptions explicitly.

APPROXIMATION LEVEL
-------------------
Static linearized general relativity.

CONSERVATION
------------
State exactly which conservation equation is imposed and at what
approximation level.

ENERGY CONDITIONS
-----------------
State which conditions are required or tested.

NUMERICAL METHOD
----------------
Describe quadrature, optimization, PDE solve, discretization, tolerances,
and domain treatment as applicable.

VALIDATION
----------
Describe independent calculations, limiting cases, tests, and convergence
checks.

FALSIFICATION STRATEGY
----------------------
State what result would reject or demote the modeled mechanism.

LIMITATIONS
-----------
State what the model does not establish.

RELATED FILES
-------------
List relevant source, tests, simulations, results, notes, and journal files.

CLAIM CLASSIFICATION
--------------------
State the strongest permitted project claim.

PRACTICAL DEVICE CLAIM
----------------------
NO unless explicitly and independently established.
"""
```

Exact headings may vary, but equivalent information must be preserved.

---

# 6. Simulation File Standard

Simulation files document the scientific experiment, not merely the code.

A simulation header must answer:

* What single scientific question is being tested?
* Why is this the highest-value current test?
* What operational observable determines success?
* What hypothesis or branch is being tested?
* What equations or source modules are used?
* Which parameters are scanned?
* What assumptions are fixed?
* What result promotes the branch?
* What result falsifies or demotes the branch?
* What numerical convergence is required?
* What independent verification is required?
* What outputs are persisted?
* What claims are permitted?
* What claims remain prohibited?

A simulation should not be created merely because a parameter space is available to scan.

The experiment should have a predeclared scientific decision gate.

---

# 7. Current Operational-Observable Standard

For antigravity-related simulations, distinguish:

```text
POINTWISE_SIGN
FINITE_PAYLOAD_RESPONSE
TOTAL_ACTIVE_MASS
ENERGY_COST
STABILITY
REALIZABILITY
```

Pointwise outward acceleration alone is not sufficient once finite-payload integration is computationally affordable.

For a finite payload:

```math
\mathbf a_{\mathrm{CM}}
=
\frac{
\int \rho_P\mathbf a\,dV
}{
\int \rho_P\,dV
}
```

Future practical-branch simulations should use finite-payload acceleration as an early promotion criterion whenever possible.

---

# 8. Test File Headers

Test files should explain what scientific regressions they protect.

Example:

```python
"""Regression tests for a finite relativistic-stress source.

These tests protect established algebraic identities, limiting cases,
sign conventions, conservation checks, energy-condition checks, and benchmark
numerical results.

They are intended to detect:

- algebraic regressions;
- dimensional errors;
- sign-convention errors;
- numerical instability;
- accidental changes to established benchmark values.

Passing these tests provides regression protection.

It does not independently establish physical realizability or scientific
correctness when the tests reuse the same implementation as the simulation.
"""
```

---

# 9. Independent Verification Standard

Regression testing and scientific verification are different.

A test that calls the same implementation as the simulation is:

```text
REGRESSION_PROTECTION=
YES
```

but:

```text
INDEPENDENT_SCIENTIFIC_VERIFICATION=
NO
```

Central quantitative results should ideally have at least two genuinely independent routes.

Examples:

```text
ANALYTIC_DERIVATION
VS
NUMERICAL_INTEGRATION
```

```text
DIRECT_VOLUME_FORCE
VS
INDEPENDENT_QUADRATURE
```

```text
FIELD_EQUATION_SOLVER
VS
VIRIAL_IDENTITY
```

```text
PROJECT_CALCULATION
VS
PUBLISHED_EXPERIMENTAL_RESULT
```

---

# 10. Function and Class Documentation

Scientifically significant functions should have docstrings documenting:

* physical meaning;
* parameter meaning;
* units;
* return meaning;
* sign convention;
* valid domain;
* exceptions;
* approximation assumptions.

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
        Dimensionless stress ratio.

    Returns
    -------
    float
        Axial acceleration in m/s^2.

        Positive:
            Outward.

        Negative:
            Inward.

    Assumptions
    -----------
    Uses the declared finite-source linearized-GR model.

    Strong-field corrections and full dynamical stability are not included.
    """
```

---

# 11. Comments Explain Why

Weak:

```python
# Multiply by radius.
value *= radius
```

Better:

```python
# Convert the local surface quantity into the integrated annular contribution.
value *= radius
```

Scientifically useful:

```python
# The support contribution must be retained because omitting it would preserve
# the repulsive stress of the central region while discarding the stresses
# required to hold the finite configuration in equilibrium.
support_term = tension * radius
```

Preserve reasoning that would otherwise disappear from the implementation.

---

# 12. Important Equations Near Their Implementation

Important implemented equations should appear near the corresponding code.

Example:

```python
# Reissner-Nordstrom neutral-test-particle sign-change scale:
#
#     r_rep = Q^2 / (4*pi*epsilon_0*M*c^2)
#
# The associated branch interpretation is documented in the module header.
repulsion_radius_m = (
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

The comment should explain physical meaning, not merely duplicate Python syntax.

---

# 13. Avoid Magic Constants

Avoid:

```python
value = 23.591586299249
```

Prefer:

```python
# Finest validated finite-thickness 006D coefficient from the declared
# reference simulation and journal reconstruction.
C_006D_FINITE_REFERENCE = 23.591586299249
```

Whenever practical, derive constants instead of hardcoding them.

If a benchmark is hardcoded for regression purposes, document its provenance.

---

# 14. Units Must Be Visible

Prefer:

```text
radius_m
mass_kg
energy_j
pressure_pa
surface_energy_j_m2
acceleration_m_s2
time_s
frequency_hz
```

Dimensionless values should be named or documented as dimensionless.

Avoid ambiguous names such as:

```text
radius
mass
energy
value
```

unless context is truly unambiguous.

---

# 15. Sign Conventions Must Be Explicit

Any source involving:

* gravitational direction;
* pressure;
* tension;
* curvature;
* energy flow;
* gauge charge;
* junction conditions;
* force direction;

must explicitly state its sign convention.

Example:

```text
positive acceleration =
outward

negative acceleration =
inward
```

Never require a reviewer to infer a central sign from implementation details.

---

# 16. Approximation Level Must Be Explicit

Every scientific model should identify itself as one or more of:

```text
EXACT_GENERAL_RELATIVITY
LINEARIZED_GENERAL_RELATIVITY
WEAK_FIELD_EXPANSION
NEWTONIAN_APPROXIMATION
SEMICLASSICAL_GRAVITY
EFFECTIVE_FIELD_THEORY
VARIATIONAL_PREFLIGHT
ASYMPTOTIC_PREFLIGHT
TOY_MODEL
NUMERICAL_APPROXIMATION
```

An approximation must never be allowed to look like an exact result.

---

# 17. Physical Constraints Must Be Explicit

Where relevant, a scientific file should state the status of:

```text
NEC
WEC
SEC
DEC
LOCAL_CONSERVATION
GLOBAL_CONSERVATION
FINITE_ENERGY
FINITE_SUPPORT
BOUNDARY_REGULARITY
STABILITY
FIELD_EQUATION_RESIDUAL
FINITE_PAYLOAD_RESPONSE
```

Do not silently omit a required support sector or conservation term because it worsens the desired result.

---

# 18. Separate Mathematical Possibility From Practical Realization

Use explicit distinctions such as:

```text
MATHEMATICAL_CONFIGURATION=
YES

LOCAL_OUTWARD_FIELD=
YES

FINITE_PAYLOAD_OUTWARD_ACCELERATION=
NOT_ESTABLISHED

ENERGY_CONDITIONS=
PASS

FIELD_EQUATION_SOLUTION=
NOT_ESTABLISHED

FULL_DYNAMIC_STABILITY=
NOT_ESTABLISHED

KNOWN_MATERIAL_REALIZATION=
NO

PRACTICAL_ENERGY_SCALING=
NO

PRACTICAL_DEVICE=
NO
```

Never collapse these into a single success/failure label.

---

# 19. Claim Classification

Use project classifications consistently.

Examples:

```text
KNOWN_RESULT

REPRODUCED

PROJECT_DERIVED_ANALYTIC_RESULT

PROJECT_DERIVED_CONSTRUCTIVE_RESULT

NUMERICAL_OBSERVATION

NUMERICAL_MODEL_RESULT

NUMERICAL_OPTIMIZATION_RESULT

VARIATIONAL_PREFLIGHT

ASYMPTOTIC_NO_GO

CONJECTURE

NOVEL_CANDIDATE

REJECTED

NOT_ESTABLISHED
```

`NOVEL_CANDIDATE` does not mean discovery.

Novelty requires dedicated literature comparison and external verification.

---

# 20. Result Files and Logs

Important simulations should identify:

* output CSV;
* output figures;
* output logs;
* important result labels;
* reference run.

Persistent logs belong under:

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

A result that exists only in transient terminal output should be transferred into durable documentation if future reasoning depends on it.

---

# 21. Numerical Validation Standard

Important calculations should use the applicable subset of:

1. dimensional analysis;
2. sign checks;
3. limiting cases;
4. analytic identities;
5. known-solution reproduction;
6. regression tests;
7. independent implementation;
8. convergence testing;
9. domain-size testing;
10. quadrature-order testing;
11. sensitivity analysis;
12. parameter-neighborhood robustness;
13. literature comparison;
14. assumption audit.

For multidimensional calculations, convergence should be separated by direction when appropriate.

Do not infer continuum convergence from one refinement direction alone.

---

# 22. Positive-Result Robustness Standard

An optimizer finding one point is not sufficient for a major positive claim.

Where applicable, test a finite neighborhood around the candidate.

Useful perturbations include:

```text
-10%
-5%
REFERENCE
+5%
+10%
```

for important continuous parameters.

A stronger statement is:

```text
FINITE_OPERATING_REGION_EXISTS
```

rather than merely:

```text
OPTIMIZER_FOUND_ONE_POINT
```

---

# 23. Falsification Standard

Before a substantial simulation is implemented, document what result would falsify or demote the branch.

Examples:

```text
CONSERVATION_FAILURE

ENERGY_CONDITION_FAILURE

FIELD_EQUATION_SIGN_CONFLICT

NO_FINITE_PAYLOAD_REVERSAL

INSTABILITY

DIVERGENT_TOTAL_ENERGY

REQUIRED_PARAMETER_EXCLUDED_BY_EXPERIMENT

PATHOLOGICAL_FINE_TUNING
```

A successful negative result is a legitimate research result and should be preserved.

---

# 24. Bash Script Standards

Nontrivial shell scripts should explain:

* purpose;
* expected working directory;
* inputs;
* outputs;
* destructive behavior;
* failure behavior.

For scientific run harnesses, ensure Python failures are not hidden by `tee`.

Example:

```bash
#!/usr/bin/env bash

set +u
set -o pipefail

ROOT="$(pwd)"
PY="$ROOT/.venv/bin/python"

PYTHONPATH="$ROOT/src" \
"$PY" simulations/example.py 2>&1 |
  tee results/logs/example.log

RC="${PIPESTATUS[1]:-${pipestatus[1]:-0}}"
```

Because shell behavior differs between Bash and zsh, use repository-tested harness patterns rather than assuming portability.

For interactive zsh blocks, prefer the project's known-safe pattern:

```bash
set +e
set +u
unsetopt PIPE_FAIL 2>/dev/null || true
```

and explicitly preserve the return code of the scientific process.

---

# 25. AI Readability Standard

Files must not depend on hidden conversational history.

Another researcher or AI should be able to understand the file from repository contents alone.

Therefore:

* expand uncommon acronyms when first used;
* explain the scientific problem;
* describe equations by physical meaning;
* state units;
* state signs;
* state assumptions;
* state approximation level;
* identify validation already performed;
* identify unresolved questions;
* identify related files;
* explain numerical constants;
* explain result labels;
* state permitted and prohibited claims.

Avoid:

```python
# Fix old problem.
```

Prefer:

```python
# Rewrite the kernel in a numerically stable form because the direct
# subtraction loses precision when both compactness parameters are much
# smaller than unity.
```

---

# 26. Scientific File Definition of Done

Before considering an important scientific file complete:

* [ ] Purpose is documented.
* [ ] Scientific question is stated.
* [ ] Operational observable is stated.
* [ ] Theory/model is stated.
* [ ] Approximation level is stated.
* [ ] Governing equations are documented.
* [ ] Inputs and units are documented.
* [ ] Outputs and units are documented.
* [ ] Sign conventions are documented.
* [ ] Assumptions are documented.
* [ ] Conservation assumptions are documented.
* [ ] Energy-condition assumptions are documented where relevant.
* [ ] Stability assumptions are documented where relevant.
* [ ] Falsification criterion is stated.
* [ ] Limitations are documented.
* [ ] Claim limits are documented.
* [ ] Related files are identified.
* [ ] Important functions have docstrings.
* [ ] Important constants have provenance.
* [ ] Focused tests exist.
* [ ] Relevant limiting cases are tested.
* [ ] Numerical convergence is assessed where necessary.
* [ ] Simulation output is reproducible.
* [ ] Important positive results have independent validation where feasible.
* [ ] Results are not overstated.

---

# 27. Markdown Definition of Done

Before committing an important Markdown document:

* [ ] Real Markdown headings are used.
* [ ] Bullets are not escaped.
* [ ] Blockquotes are not escaped.
* [ ] Links are not escaped.
* [ ] File paths do not contain escaped underscores.
* [ ] Inline mathematics uses `$...$`.
* [ ] Display mathematics uses fenced `math` blocks.
* [ ] `$$...$$` is not used.
* [ ] `\(...\)` is not used.
* [ ] `\[...\]` is not used.
* [ ] LaTeX underscores inside math are not escaped.
* [ ] `\operatorname` does not occur.
* [ ] `\boxed` does not occur.
* [ ] `\textbf` does not occur inside math.
* [ ] Function names use conservative forms such as `\mathrm{erf}`.
* [ ] New units preferably use `\mathrm{...}`.
* [ ] Math braces are balanced.
* [ ] `\left` and `\right` are balanced.
* [ ] `\begin` and `\end` environments are balanced.
* [ ] Display equations do not end in grammatical punctuation.
* [ ] Decimal points remain intact.
* [ ] Mathematically meaningful punctuation remains intact.
* [ ] Important equations are structurally simple.
* [ ] Bash examples remain paste-ready.
* [ ] The repository math audit passes.
* [ ] Important pages are visually checked on GitHub after commit/push when practical.

---

# 28. Documentation Roles

Use repository documents for distinct purposes.

```text
README.md
    Concise public-facing project state and strongest reproducible claims.

RESEARCH_BUILDPLAN.md
    Active frontier, pathway ranking, decision gates, stop rules, and NEXT.

NOTES.md
    Detailed chronological research history and carry-forward context.

journal/
    Durable completed research slices, proofs, falsifications, and
    claim boundaries.

CLAIMS.md
    Formal claim classifications when maintained.

ASSUMPTIONS.md
    Shared physical and methodological assumptions.

FORMATTING_AND_CODE_STANDARDS.md
    Markdown, mathematics, code, validation, and documentation rules.

results/
    Persistent numerical evidence.
```

Do not force every detail into the README or buildplan.

---

# 29. Journal Standard

A journal entry should preserve a completed scientific slice.

It should normally record:

```text
OBJECTIVE

STARTING_STATE

SCIENTIFIC_QUESTION

WORK_PERFORMED

MATHEMATICAL_DERIVATIONS

NUMERICAL_RESULTS

VALIDATION

FALSIFICATION_ATTEMPTS

NEGATIVE_RESULTS

CLAIM_CLASSIFICATION

WHAT_REMAINS_UNRESOLVED

NEXT_ACTION
```

A journal entry should be detailed enough to reconstruct why the project's frontier changed.

It should not rely on chat history.

All journal mathematics follows the same GitHub-safe rules in this document.

---

# 30. Project Documentation Rule

The preferred standard is:

> **Write documentation for the next researcher, developer, reviewer, or AI that has never seen the previous conversation.**

Important scientific work should explain not only **what it computes**, but:

* why it exists;
* which physical question it addresses;
* which observable determines success;
* which equations justify it;
* which assumptions it makes;
* how it has been validated;
* how it was challenged or falsified;
* where it may fail;
* what conclusions may be drawn;
* what conclusions may not be drawn.

---

# 31. Final Formatting Rule

When there is uncertainty about whether a Markdown mathematical construct will render correctly on GitHub:

> **Choose the simpler representation.**

Do not sacrifice scientific content.

Do sacrifice decorative TeX.

A plain, reproducible equation that renders everywhere is preferable to a visually elaborate equation that may fail.
