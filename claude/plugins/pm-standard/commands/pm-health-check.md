---
description: "Independent project health assessment across all ten management areas, with a RAG per area, the evidence behind each, and the three things most likely to cause failure. Usage: /pm-health-check [area]"
---

# Project health check

An honest second opinion, for a PM taking over a project, a delivery manager reviewing one, or
a team that suspects its own reporting has drifted. Read-only.

## Step 1 — Load

`pm-project`. Read the artifacts on disk — not what the last report claimed.

## Step 2 — Assess each area against evidence

| # | Area | Healthy looks like | Common failure found here |
|---|---|---|---|
| 1 | Charter | signed, objectives measurable, still describes the project | objectives unmeasurable, or the project has drifted from them |
| 2 | Scope | baselined; RTM has no orphans; exclusions have reasons | requirements agreed but unplanned; absorbed changes |
| 3 | Cost | baseline time-phased; EVM from honest EV; reserves tracked | actuals booked to "project"; CPI of exactly 1.00 |
| 4 | Plan and governance | every decision type has a named owner; CCB meets | plan describing ceremonies nobody performs |
| 5 | Process | defined, tailored with reasons, audited | defined once, never audited, quietly abandoned |
| 6 | Schedule | WBS to 8/80; critical path named; buffer visible | percent-complete self-assessed; buffer already gone |
| 7 | Reporting | numbers traceable to sources; RAG follows thresholds | green over a red section; carried-forward figures |
| 8 | Quality | targets agreed; containment tracked; entry criteria enforced | test entry criteria waived silently; severity drift |
| 9 | Risk | responses concrete with triggers; issues aged | "monitor" as a response; issues that were never risks |
| 10 | Closing | closing effort in the WBS; acceptance criteria pre-agreed | no closing plan; criteria to be agreed at delivery |

## Step 3 — Run the mechanical checks

`/pm-trace-check` and `/pm-profile-check`. Their findings are evidence for this assessment, not
a substitute for reading the artifacts.

## Step 4 — Look for the specific tells

The signals that most reliably precede trouble, in rough order of predictive value:

1. **The buffer is consumed faster than the schedule is elapsed.** 60% of buffer at 30%
   elapsed is failing, whatever SPI says.
2. **Contingency drawdown outpacing elapsed time**, with the remaining risks uncovered.
3. **Work packages stalled at 50%** for three or more reporting periods.
4. **Issues that were never risks** — the register is not looking forward.
5. **Zero absorbed changes recorded** alongside a team that reports "small extras" verbally.
6. **Review density near zero** on design documents — the reviews are not happening.
7. **A defect S-curve still rising** at a planned exit date.
8. **Actions older than two escalation SLAs**, still listed rather than escalated.
9. **Every report green, then one red** — the Amber period was skipped.
10. **The PMP untouched since kickoff.**

## Step 5 — Report

```
Health check — {project}, {date}                     Overall: {G|A|R}
  Area                     RAG   Evidence                       Finding
  1 Charter                {…}   {what was checked}             {…}
  ... (all ten)
  Mechanical checks        : trace {n findings} · profile {n Critical}
  Tells present            : {which of the ten, with the numbers}
  Three things most likely to cause failure here:
    1. {finding} — {why it matters} — {what would fix it, and who}
    2. …
    3. …
  Quick wins               : {things fixable this week}
  Not assessable           : {what, and what evidence is needed}
```

Say what the evidence supports, including when it contradicts the current reporting. A health
check that agrees with the status report by default has not been performed.
