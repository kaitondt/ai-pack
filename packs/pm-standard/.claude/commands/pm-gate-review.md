---
description: "Run a management gate or milestone review: entry criteria, evidence from baselines and metrics, the proceed/conditions/hold/stop decision, conditions with owners, and the recorded outcome. Usage: /pm-gate-review <milestone or gate id>"
---

# Gate review

A gate review decides whether the project may proceed. It is not a status meeting, and the
difference is that it has an outcome (PP-04).

## Step 1 — Load

`pm-project`, then `pm-management-plan`. Also `pm-quality` when the gate covers a test level.

## Step 2 — Check entry criteria

The criteria for holding the review at all — usually that the evidence exists. A review held
without its evidence produces a decision made on impressions, and it is then quoted for
months as though it were verified.

## Step 3 — Gather evidence, never impressions

| Dimension | Evidence |
|---|---|
| Scope | deliverables due by this gate: complete, accepted, or explicitly deferred |
| Schedule | milestone criteria met; SPI; critical path and buffer position |
| Cost | CPI, EAC, VAC, contingency consumed vs elapsed |
| Quality | the quality report: containment, open defects by severity, coverage, S-curve shape |
| Risk | exposure profile, high risks with responses, contingency vs remaining exposure |
| Change | CRs approved since the last gate, cumulative baseline impact |
| Resource | availability for the next phase, key-person risk |
| Client | decisions outstanding, acceptance readiness, environment and data readiness |

When a technical pack is installed, its phase gate (`/sdlc-phase-gate`, or the equivalent)
evaluates the engineering exit criteria. **Consume that result; do not re-run its checks.**
This review adds the management dimensions.

## Step 4 — Decide

| Outcome | Meaning |
|---|---|
| **Proceed** | every criterion holds |
| **Proceed with conditions** | conditions as `ACT-*` with owners and dates, tracked to closure |
| **Hold** | proceed only when named items are resolved; re-review on a date |
| **Stop** | the business case or the plan no longer holds; escalate to the sponsor |

Two disciplines that keep gates meaningful:

- **A gate that cannot fail is a status meeting.** If no project has ever been held at this
  gate, the criteria are not criteria.
- **Conditions accumulate.** Carry forward every open condition from previous gates and report
  the total. Three gates with two conditions each is six unfinished obligations riding into
  the next phase, and the gate report says so.

## Step 5 — Record

`{{profile.paths.reports_root}}/gates/gate_{milestone}_{YYYYMMDD}.md`:

```
Gate {id} — {date}                                  Decision: {PROCEED | CONDITIONS | HOLD | STOP}
  Entry criteria  : {each, met/not}
  Evidence        : {each dimension, with the numbers and their source}
  Technical gate  : {result, from the technical pack} | {n/a}
  Conditions      : {each, ACT-id, owner, due date}
  Carried forward : {open conditions from previous gates, with age}
  Risk into next  : {what the numbers predict, and for which work packages}
  Baselined       : {documents this gate baselines, if any}
  Decided by      : {name}, {date}
```

**Do not record a gate as passed when a criterion could not be evaluated.** Record it as not
evaluated, and say what is needed. A gate that certifies checks it did not run is worse than no
gate, because everything downstream then trusts it.
