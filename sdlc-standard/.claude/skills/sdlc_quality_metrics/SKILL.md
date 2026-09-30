---
name: sdlc_quality_metrics
description: "How to compute, interpret and report the project's quality metrics — review density, defect density, phase containment, test density and coverage, escaped defects, the defect S-curve — and how the gate report uses them. Load for ALL metrics, gate-report and quality-status tasks."
---

# Quality Metrics

> Prerequisite: `sdlc_project` resolved. Rules in `rules/sdlc/quality-metrics.md`; this
> skill is how to produce the numbers.

Metrics exist to inform a gate decision. Produced continuously they invite tuning;
produced at gates they force a decision (QM-09).

---

## Data sources — collect from artifacts, not from memory

| Metric | Source |
|---|---|
| Review density | the review record in each document (DS-03) and review reports |
| Design defect density | review findings, Critical + Warning, per document |
| Code defect density | defect register, filtered by injection phase P4 |
| Phase containment | defect register: injection phase vs found phase |
| Test density | case counts / checkpoints (`sdlc_test_artifact_lifecycle` §4) per size unit |
| Coverage | the test runner's own report, from a named run |
| Escaped defects | defect register: first found in P8 or P9 |
| S-curve | defect register: found date and closed date, cumulative |

**Every number carries its population, its date and its method** (QM-01). A metric that
cannot be recomputed by someone else from the same artifacts is an assertion.

---

## Computing each metric

### Review density

```
review_density(doc) = findings recorded in the review record ÷ 1 document
```

Compare against `{{profile.quality.targets.review_density}}`. Report the distribution, not
only the mean — one document with 30 findings and nine with zero averages to 3 and hides
both problems.

**Interpretation:**

| Observation | What it usually means |
|---|---|
| Density near zero | the document was not read, or the reviewer lacked the domain knowledge |
| Density far above target | the upstream document was not ready for review |
| High Suggestion, low Critical | the reviewer checked format, not content |
| Findings all from one reviewer | the review is one person's opinion, not a process |

### Defect density

```
defect_density(phase, module) = defects injected in that phase ÷ size
```

Size in `{{profile.quality.size_unit}}`. Report both bounds
(`{{profile.quality.targets.design_defect_density}}`,
`{{profile.quality.targets.code_defect_density}}`).

A module far **below** the lower bound is reported as a **risk**, not a success: it was
probably not tested hard enough, and it is the one that surprises everyone at UAT.

### Phase containment

```
containment(P) = defects injected in P and found in P ÷ defects injected in P
```

Requires honest injection attribution (`sdlc_defect_management` §2). Report the full
matrix — it is more informative than the ratio:

| Injected ↓ / Found → | P1 | P2 | P3 | P4 | P5 | P6 | P7 | P8 | P9 |
|---|---|---|---|---|---|---|---|---|---|
| P1 requirements | | | | | | | | | |
| P2 basic design | — | | | | | | | | |
| P3 detail design | — | — | | | | | | | |
| P4 code | — | — | — | | | | | | |

Everything below the diagonal is an escape, and the further from the diagonal, the more it
cost. A cluster in the P1→P8 cell says the requirements process is where to invest — not
the testing process, which is where teams usually react.

### Test density and coverage

```
test_density = test checkpoints ÷ size
```

Coverage comes from the runner, for a named run and build. Report line and branch
separately; a high line coverage with low branch coverage means the error paths are
untested, which is where the defects are.

Neither replaces the traceability check: every design rule has a case (T-01..T-07).

### Escaped defects

```
escape_rate = defects first found in P8 or P9 ÷ all defects
```

Compare against `{{profile.quality.targets.escaped_defects}}`. For each escape, record the
check that should have caught it — that list is the agenda for `/sdlc_refine_skill`.

### The S-curve

Per test phase, cumulative found and cumulative closed, by date. Report the **shape** in
words:

| Shape | Reading |
|---|---|
| Found flattening, closed converging | ready to exit |
| Found still rising at the exit date | the phase is not finished |
| Closed lagging by a widening gap | fix capacity is the bottleneck; more testers make it worse |
| Both flat, early | testing has stopped, not converged — check execution progress |
| A step change in found | either a new build broke something, or a new tester started |

---

## The gate report

Produced by `/sdlc_quality_report` at each gate, written to
`{{profile.quality.metrics_report}}`. It answers three questions in order:

```
Gate {P} — {date}

1. EXIT CRITERIA
   {each assertion from {{profile.gates.<P>.exit}}}   pass | fail | waived by {who}

2. NUMBERS
   Review density        {value}  target {target}   {reading}
   Defect density        {value}  target {target}   {reading}
   Phase containment     {value}  target {target}   {reading}
   Test density/coverage {value}  target {target}   {reading}
   Escapes so far        {value}  target {target}   {reading}
   Curve                 {shape}

3. RISK INTO THE NEXT PHASE
   {what the numbers say will happen next, and to which modules}

4. CARRIED FORWARD
   {open defects deferred, with approver and target release}
   {waived criteria, with who waived and what risk was accepted}
```

**Section 3 is what the gate is for.** A report that lists numbers without saying what
they predict is a status update, not a decision aid. The sentence to write is of the form:
*"modules X and Y have half the defect density of the rest at the same size — expect them
to produce the P8 surprises."*

---

## Reporting honestly

- A metric that could not be produced is reported as not produced, with what is needed.
- A waived criterion is named, with who waived it.
- A number that looks good for a bad reason is reported with the reason — a 100% pass rate
  over 40% of the planned cases is not a 100% pass rate.
- Never adjust a severity, merge defects, or reattribute an injection phase to move a
  number (QM-08). The gate is downstream of the numbers; tuning them disables it silently,
  and nobody notices until the client does.
