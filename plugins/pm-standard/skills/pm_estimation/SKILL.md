---
name: pm_estimation
description: "Effort, duration and cost estimation — method selection, WBS bottom-up, three-point PERT, analogous and parametric estimating, productivity rates, the work people forget, estimate review and re-estimation at stage boundaries and change requests. Load for ALL estimating, sizing, bid-support and estimate-review tasks."
---

# Estimation (Effort · Duration · Cost)

> Prerequisite: `pm_project` loaded. The rules are in
> `rules/pm/estimation-integrity.md`; this skill is how to produce the numbers.

An estimate is a prediction with a method, a basis and a range (ES-01). This skill produces
one that can be defended in a change request and improved on the next project.

---

## Choose the method by what is actually known

| Method | Use when | Accuracy | Cost to produce |
|---|---|---|---|
| **Analogous** | a similar past project exists, little detail available | −25% to +75% | hours |
| **Parametric** | a size driver is countable (screens, endpoints, tables, function points) | −15% to +30% | a day |
| **Three-point / PERT** | the work is understood but uncertain | −15% to +25% | a day |
| **WBS bottom-up** | the WBS exists to work-package level | −10% to +15% | days |
| **Expert / Delphi** | novel work with no historical basis | wide, but honest about it | a day |

Use **at least two** methods for any estimate that will become a commitment, and reconcile
them. When bottom-up and parametric differ by more than ~20%, one of them is wrong and
finding out which is the highest-value hour in the estimating process — usually it is a
missing work package in the bottom-up.

Record the method with the number (ES-01). An estimate whose method is unrecorded cannot be
re-derived when the scope changes.

## EM-01 — Three-point, done properly

```
E   = (O + 4M + P) / 6            expected value (beta / PERT)
σ   = (P − O) / 6                 standard deviation
range at ~95% = E ± 2σ
```

The three points mean specific things, and the discipline is in the definitions:

- **O** — everything goes right; no rework, no clarification, no waiting. Not a fantasy: a
  genuine best case that has actually happened before.
- **M** — the most likely single outcome, based on how work normally goes here.
- **P** — the realistic bad case: the interface is undocumented, the reviewer is away, two
  rounds of rework. **Not** the catastrophe — a catastrophe is a risk, and it belongs in the
  risk register with a contingency response, not inside a duration estimate.

Do not aggregate by summing the pessimistic values. Sum the expected values and combine the
variances: `σ_total = √(Σσᵢ²)`. Summing the P values produces a total no project has ever
taken, and it destroys the credibility of the whole estimate.

## EM-02 — Parametric estimating needs a measured rate

```
effort = count × rate_per_unit × complexity_factor × (1 + risk_factor)
```

Rates come from `{{profile.cost.productivity.rates}}`, and that block must state its
`basis` — which past project, measured how (ES-08). Rates copied from a template are
unverified, and the estimate says so in its confidence field.

Complexity factors are stated and justified, not applied as a mood. Define the bands
concretely for this project, once:

| Band | Definition example (screens) | Factor |
|---|---|---|
| Simple | single entity, no calculation, standard CRUD | 1.0 |
| Medium | multiple entities, validation rules, one integration | 1.6 |
| Complex | transactional logic, concurrency, multi-step workflow | 2.5 |

Then classify every item against those definitions, and count. A parametric estimate with
undefined bands is an analogous estimate with extra arithmetic.

## EM-03 — Bottom-up: the checklist of what gets forgotten (ES-07)

Bottom-up totals err in a predictable direction. Every one of these is a work package with
effort, not overhead absorbed silently:

**Per feature** — requirement clarification · design · design review (the reviewer's hours,
not only the author's) · implementation · code review · unit test writing · unit test
execution and fixing · integration · test case design · test execution · defect fixing and
re-testing · documentation update · traceability update.

**Per project** — project management and reporting (`{{profile.cost.productivity.phase_distribution.management}}`)
· environment setup and data preparation · build and deployment pipeline · release and
release rehearsal · client meetings, demos and UAT support · training material and delivery
· knowledge transfer and handover · onboarding for anyone joining after kickoff · rework
from review findings · translation, if the project has two document languages.

Then sanity-check the shape against
`{{profile.cost.productivity.phase_distribution}}`. A total with 5% testing is not a lean
plan; the testing has simply not been estimated yet.

## EM-04 — Effort is not duration (ES-04)

The conversion, in full:

```
available_hours_per_person_day = {{profile.calendar.productive_hours_per_day}}
                               × allocation_percent
                               × (1 − {{profile.calendar.planned_absence_allowance}})

duration_days = effort_hours ÷ (people × available_hours_per_person_day)
              + waiting time
```

Worked example, and it is worth doing this arithmetic out loud with anyone who proposes a
date first: 80 hours, one person, 85% allocation, 6.5 productive hours, 8% absence
allowance → 80 ÷ (6.5 × 0.85 × 0.92) ≈ **15.7 working days**, plus review waiting. Three
calendar weeks, not two.

## EM-05 — Estimate the work, then compare to the target (ES-02)

When a target exists, produce the estimate independently first. Then present the comparison,
not a reconciled number:

```
Estimate    : 1,240 person-hours (bottom-up, ±15%, post-design stage)
Target      : 900 person-hours
Gap         : 340 hours (38%)
Options     : 1. Remove scope X and Y      → 950 h, no quality change
              2. Extend the date by 3 weeks → 1,240 h, same scope
              3. Add 2 developers          → 1,340 h (ramp-up), date held, higher defect risk
Recommend   : option 1 — X and Y are Could-priority and have no dependents
```

Three options with consequences turn an argument into a decision. A single reconciled
number that happens to equal the target turns a decision into a future overrun that nobody
can explain.

## EM-06 — Re-estimate at every stage boundary and every CR

Per ES-03: the estimate is refreshed after requirements, after design, and at each approved
change request. Keep the history — estimate versus actual per work package is the only
input that improves the next estimate (`/pm_lessons`).

An estimate untouched since the bid is a historical artifact. It is also, invariably, the
number the client still remembers.

## EM-07 — Reviewing someone else's estimate

The questions that find real problems, in order:

1. What is the method and the basis? (No answer → not an estimate.)
2. Which of ES-07's forgotten items are missing? (Check the list explicitly; it is almost
   never zero.)
3. Is testing effort at least in the region of the phase distribution?
4. Are the productivity rates measured or copied? (ES-08)
5. Is the range stated, and does it match the estimating stage?
6. Does it include the reviewer's hours, not only the author's?
7. Is padding hidden inside the lines instead of held as buffer? (Ask for the O/M/P triples
   — hidden padding shows up as a suspiciously narrow spread.)
8. What are the assumptions, and who owns each one?
9. Does the duration derivation use real productive hours and allocation? (EM-04)
10. Does it happen to equal the target? (ES-02 — if so, ask which came first.)

## EM-08 — Estimate a change request the same way

A CR estimate covers the whole cascade, not just the new code:

analysis and impact assessment · design document updates (every affected document) · code ·
unit tests, new and modified · integration and regression testing · test case updates ·
documentation · release · re-verification of anything the change touches · the management
overhead of the change itself.

Then state the **schedule** impact separately from the effort impact. Forty hours of work
can be a two-week delay if it lands on the critical path, and no delay at all if it does
not — and the client is deciding about the delay, not the hours.

---

## Output — the estimate record

```
Estimate — {scope}, {date}, v{n}
  Stage        : {pre-charter | post-requirements | post-design}
  Method       : {primary} cross-checked with {secondary}
  Basis        : {WBS version / historical project / measured rates and their source}
  Effort       : {E} person-hours   range {E−}..{E+} ({confidence}%)
  Duration     : {d} working days   (people {n}, allocation {x}%, productive {h} h/day)
  Cost         : {currency} {amount}   (labour {a}, non-labour {b})
  Contingency  : {x}% = {amount}  — covers RSK-{ids}
  Excludes     : {what this number does not cover}
  Assumptions  : ASM-{ids}, each with owner and confirm-by date
  Sanity check : phase distribution {actual vs profile}; cross-method delta {x}%
  Estimator    : {name}   Reviewed by: {name}
```

Never issue a bare number. The record is what makes the estimate defensible in six months,
when the person who produced it is on another project.
