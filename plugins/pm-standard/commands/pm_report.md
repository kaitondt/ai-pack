---
description: "Produce a status report at the given cadence — daily, weekly, monthly, quarterly, or the quality report — from collected evidence, with RAG computed from thresholds and every variance carrying a cause, an impact and an action. Usage: /pm_report <daily|weekly|monthly|quarterly|quality>"
---

# Report

## Step 1 — Load

`pm_project`, then `pm_reporting`. For the quality report, also `pm_quality`.
Agent: `pm_controller` (quality report: `pm_quality_manager`).

## Step 2 — Require collected data

Read `{{profile.paths.status_data}}/{period}.md`. If it does not exist for this period, run
`/pm_status_collect` first — **never** assemble a report from memory or from the previous
report's figures (RI-02).

For monthly and quarterly, also run `/pm_evm` so the performance indices in the report come
from one computation rather than two.

## Step 3 — Write the cadence's structure

Contents from `{{profile.reporting.cadences}}` and the templates in `pm_reporting`:

| Cadence | Shape | Discipline |
|---|---|---|
| `daily` | one screen: done / planned / blockers with age / defect inflow | no metrics, no narrative |
| `weekly` | 7 sections: RAG · milestones · progress · risks · decisions needed · CRs · quality · resources | section 4 names consequences and by-dates |
| `monthly` | 10 sections, decision-oriented | include the **cumulative** CR impact, not only this month's |
| `quarterly` | business review: is the business case still valid | section 1 measures charter objectives |
| `quality` | 8 sections, ending in what the numbers predict | metric definitions from `pm_quality` |

## Step 4 — Compute RAG, then explain it (RG-02)

```
RED   : a payment milestone at risk, or SPI < 0.90, or the buffer consumed,
        or any unrecoverable variance
AMBER : a decision or action is needed to stay on plan, or SPI 0.90-0.95
GREEN : on plan, or recoverable inside the buffer with no decision needed
```

Then one sentence saying why, naming the specific thing. Never green over a red section
(RI-04) — the Amber period a project skips is exactly the window when the decision was cheap.

## Step 5 — Write variances as cause → impact → action (RG-03)

Specific causes only. "Unforeseen complexity" is a way of not naming one; "the interface
specification arrived six days late, so PRJ.4.3 starts 2026/04/22 or M2 moves" is a cause with
a consequence and a decision attached.

## Step 6 — Check before sending

- [ ] Every number has a source and an as-of date
- [ ] Nothing carried forward unverified
- [ ] RAG computed, explained in one sentence
- [ ] Every variance: cause, impact, action, owner, date
- [ ] Every decision request: by-date and stated consequence
- [ ] Actions carry age; anything past two escalation SLAs is escalated, not merely listed
- [ ] Nothing present that serves no decision (RI-06)
- [ ] Not-collected items stated as such
- [ ] Audience-appropriate: no internal margin, no individual performance commentary in a
      client-facing version (RG-05)

## Step 7 — Write and distribute

To the cadence's `path`, named `{cadence}_{YYYYMMDD}.md` (PN-05). Distribute per
`{{profile.reporting.distribution_list}}`.

If anything in the report meets the immediate-escalation bar (RI-05) — a payment milestone at
risk, a key person gone, contingency past half consumed, a blocking client decision — raise it
through `{{profile.governance.escalation}}` **now**, and note in the report that it was raised,
when, and to whom.
