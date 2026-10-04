# RULE FAMILY: QUALITY METRICS

A development project has no legacy oracle to compare against, so it substitutes
**process evidence**: how much review happened, how many defects each phase produced, and
where they were caught. These numbers are the argument that the system is ready — at the
gates, at acceptance, and in the maintenance contract negotiation afterwards.

Targets come from `{{profile.quality.targets}}`. They are project agreements calibrated
from your own history, not universal constants.

## QM-01 — A metric is evidence or it is decoration

Every metric reported must state: the number, the population it was measured over, the
date, and how it was obtained. "Coverage is 78%" is decoration. "Line coverage 78.4%
across 142 modules, from the P5 run on 2026/04/12, `test_unit` output attached" is
evidence.

Never report a metric that was not measured. If a number could not be produced, say so and
say what would be needed — the same rule as the review "Not verifiable" section.

## QM-02 — Review density

`findings ÷ document` (or per page, per KLOC — whichever `{{profile.quality.size_unit}}`
implies), taken from the review record in each document (DS-03).

Target: `{{profile.quality.targets.review_density}}`.

**Low density is a warning about the review, not a compliment to the author.** A design
document that produced zero findings was either not read or was reviewed by someone
without the domain knowledge to disagree. Investigate before celebrating.

High density is also a signal: past roughly 3× the target, the upstream document was not
ready for review.

## QM-03 — Defect density

`defects ÷ size`, computed per phase and per module.

| Phase | Target |
|---|---|
| Design (P2/P3) | `{{profile.quality.targets.design_defect_density}}` |
| Code (P4/P5) | `{{profile.quality.targets.code_defect_density}}` |

Both bounds matter. A module far **below** the lower bound has not been tested hard enough;
that is the module that produces the UAT surprise. Report it as a risk, not a success.

## QM-04 — Phase containment

The single most useful number in the pack.

```
containment(P) = defects injected in P and found in P
                 ─────────────────────────────────────
                       defects injected in P
```

Target: `{{profile.quality.targets.phase_containment}}`.

Every defect is attributed to the phase that **injected** it, not the phase that found it
(TR-07). Attribution is a judgement and it must be made honestly:

| The defect is | Injected in |
|---|---|
| The requirement was wrong or missing | P1 |
| The requirement was right, the design contradicted it | P2 |
| The design was right, the detail design was wrong | P3 |
| The design was right, the code did something else | P4 |
| The code was right, the test asserted the wrong thing | the test's phase |

Recording everything as "injected in P4" because coding is where the fix happened makes
containment report a flat 100% for every upstream phase and tells you nothing. The metric
is only worth collecting if the attribution can embarrass someone.

## QM-05 — Test density and coverage

- Test density: `{{profile.quality.targets.test_density}}`, cases per size unit.
- Unit coverage: `{{profile.quality.targets.unit_coverage}}`.

Coverage is a floor, never a goal. The gate is the traceability one: every design rule has
a case (`traceability.md` TR-03). 100% line coverage with no case for a stated business
rule is a failing module that reports green.

## QM-06 — Escaped defects

`defects first found in P8 ÷ all defects`. Target:
`{{profile.quality.targets.escaped_defects}}`.

This is the number the client experiences. Every escape is also a phase-containment
failure somewhere upstream, and the retrospective question is always the same: *which
check would have caught this, and why did we not run it?* The answer becomes a rule, a
checklist row or a hook — see `/sdlc-refine-skill`.

## QM-07 — Defect ageing and the S-curve

Track, per test phase: cumulative found vs cumulative closed, by date.

- The two curves converging and flattening is what "ready to exit" looks like.
- Found still climbing at the planned exit date means the phase is not finished, whatever
  the schedule says.
- Closed lagging found by a widening gap means fix capacity is the bottleneck, not test
  capacity — adding testers makes it worse.

Report the shape in words at every gate. A gate passed while the found-curve is still
rising is the most common way a project moves its defects into UAT rather than fixing them.

## QM-08 — Metrics are never improved by hiding work

Forbidden, in every case, without exception:

- reclassifying a defect to a lower severity to satisfy an exit criterion
- closing a defect as "not reproducible" without an investigation record
- merging several defects into one ticket to reduce the count
- deferring an open defect without a named approver and a target release
- counting a test as passed when it was skipped, blocked or not run
- attributing an upstream defect to the coding phase to protect a containment number

Each of these makes the report look better and the release worse. The gate exists to
be informed by the numbers; a tuned number disables the gate silently, which is the one
failure mode nobody notices until the client finds it.

## QM-09 — Report at gates, not continuously

Metrics are produced by `/sdlc-quality-report` at each phase gate and written to
`{{profile.quality.metrics_report}}`. Continuous dashboards invite tuning; gate reports
invite decisions.

The gate report answers three questions, in this order:

1. Is the exit criterion met, per assertion?
2. What do the numbers say about the *next* phase's risk?
3. What is being carried forward, and who approved carrying it?
