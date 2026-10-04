---
description: "Compute earned value for the period — PV, EV, AC, SPI, CPI, SV, CV, EAC, ETC, VAC, TCPI — per control account, with variance causes and an honest forecast. Usage: /pm-evm [period]"
---

# Earned value

## Step 1 — Load

`pm-project`, then `pm-cost`. Requires `/pm-status-collect` for the period.
Agent: `pm-controller`.

## Step 2 — Verify EV integrity before computing anything (CT-06)

Every EVM number is downstream of EV, and EV is downstream of percent-complete. Check first:

- progress measured by `{{profile.schedule.progress_measurement}}` only, never self-assessed
- 100% means accepted against acceptance criteria, not "the developer finished"
- effort from timesheets, not from the plan — a project booking plan hours as actuals has a
  CPI of exactly 1.00 forever and learns nothing

If any of these fails, say so and **stop**. An EVM report built on self-assessed percentages is
confidently wrong, which is worse than absent: the numbers look rigorous, so nobody questions
them until the milestone is missed.

## Step 3 — Compute per control account

```
PV, EV, AC at the same as-of date
SV = EV − PV     SPI = EV / PV
CV = EV − AC     CPI = EV / AC
EAC per {{profile.cost.earned_value.eac_formula}}
ETC = EAC − AC   VAC = BAC − EAC   TCPI = (BAC − EV) / (BAC − AC)
```

Roll up to project level, but report the control accounts — a healthy project average hides
the one account that is failing.

## Step 4 — Read the indices together (CT-05)

| SPI | CPI | Reading |
|---|---|---|
| < 1 | < 1 | behind and over — scope or date must give |
| < 1 | > 1 | behind but efficient — under-staffed, or blocked waiting |
| > 1 | < 1 | ahead but expensive — overtime, crashing, or over-senior staffing |
| > 1 | > 1 | verify EV before celebrating; usually optimistic progress claims |

For the last row, sample packages reported complete against their acceptance criteria before
reporting it as good news.

## Step 5 — Forecast honestly (CT-09, RI-07)

Prefer current-rate EAC: assume the project continues as it has, unless a **named, funded
reason** says otherwise — people added with their ramp cost, scope removed with its CR, a
blocker resolved with a date.

Report TCPI next to it. When performance has run at CPI 0.85 and TCPI says 1.25 is now
required, the recovery plan is asking the team to become 47% more efficient than they have ever
been — and that number is the argument for a decision, not a target.

## Step 6 — Reserve position (CT-08)

Contingency used versus elapsed, and what the remaining balance still has to cover. At 30%
elapsed with 60% of contingency consumed, the project is failing regardless of what SPI says,
because the remaining risks now have nothing behind them.

## Report

```
EVM — {period}, as of {date}
  BAC {amount}   PV {amount}   EV {amount}   AC {amount}
  SV {amount} (SPI {x.xx})     CV {amount} (CPI {x.xx})
  EAC {amount} ({formula})   ETC {amount}   VAC {amount}   TCPI {x.xx}
  Per control account:
    {code} SPI {x.xx} CPI {x.xx} — {reading}
  Variances      : {accounts outside threshold, each with cause and action}
  Contingency    : {used}/{total} ({x}%) vs elapsed {x}%
  Forecast       : {finish date, cost} — assumes {what}; would change if {what}
  EV integrity   : {verified | the check that failed}
```
