---
name: pm_cost
description: "Cost and effort control — cost baseline, budget structure, reserves, effort tracking, earned value management (SPI, CPI, SV, CV, EAC, ETC, VAC, TCPI), forecasting, variance analysis and invoicing. Load for ALL budget, cost-baseline, EVM, burn-rate, forecast and billing tasks."
---

# Cost and Effort Management

> Prerequisite: `pm_project` loaded, and an estimate produced by `pm_estimation`.

Cost management is the discipline of knowing, at any moment: what has been spent, what has
been *earned* for it, and what the total will be. The third number is the one that matters,
and it is the one most projects cannot produce until it is too late to act on.

---

## Part 1 — The cost baseline

### CT-01 — Structure: what is inside and what is outside

```
        work package costs (effort × rate, plus non-labour)
      + contingency reserve            ← identified risks, owned by the PM
      ─────────────────────────────
      = COST BASELINE                  ← what performance is measured against
      + management reserve             ← unknown-unknowns, owned by the sponsor
      ─────────────────────────────
      = PROJECT BUDGET
```

Contingency is **inside** the baseline; management reserve is **outside** it (ES-06).
Spending contingency is normal project management and is logged. Spending management
reserve requires the sponsor and, in most contracts, changes the baseline.

Merging them means the PM spends the sponsor's money without asking, and the project loses
its only early signal that risk exposure is being consumed.

### CT-02 — Cost is time-phased, or it cannot be controlled

The baseline is a **curve**, not a total: budgeted cost per period, cumulative. Without the
time phasing there is no planned value to compare against, so there is no variance until
the money runs out.

Phase it from the schedule — cost follows the activities, which follow the WBS (PB-04). A
cost curve produced independently of the schedule is a spreadsheet, and it will disagree
with reality by the second month.

### CT-03 — Non-labour cost is real cost

Licences and subscriptions · cloud and infrastructure · environments · third-party services
and APIs · hardware and devices · travel and visas · training · translation · certification
and audit fees · contingency for currency movement when the contract and the costs are in
different currencies.

An estimate with only labour in it is incomplete (ES-04), and the gap surfaces as an
unbudgeted invoice at the worst moment.

---

## Part 2 — Earned value

Three numbers, measured at the same date, per control account
(`{{profile.wbs.control_account_level}}`):

| Term | Meaning | Source |
|---|---|---|
| **PV** planned value | budgeted cost of work *scheduled* by now | cost baseline |
| **EV** earned value | budgeted cost of work *completed* by now | progress × budget (RI-03) |
| **AC** actual cost | what has actually been spent | timesheets and invoices |

The insight is entirely in EV: it converts physical progress into money, so schedule and
cost become comparable. Its integrity depends completely on honest progress measurement —
`{{profile.schedule.progress_measurement}}`, never self-assessed percentages (RI-03).

### CT-04 — The formulas, and what each one is for

```
SV  = EV − PV            schedule variance in money      < 0 = behind
SPI = EV / PV            schedule performance index      < 1 = behind
CV  = EV − AC            cost variance                   < 0 = over
CPI = EV / AC            cost performance index          < 1 = over

BAC = budget at completion                               the baseline total
EAC = AC + (BAC − EV) / CPI     forecast total, if performance continues (current-rate)
EAC = AC + (BAC − EV)           forecast total, if the rest runs to plan (budget-rate)
ETC = EAC − AC                  what remains to be spent
VAC = BAC − EAC                 forecast over/under at the end
TCPI = (BAC − EV) / (BAC − AC)  the efficiency required from here to hit BAC
```

`{{profile.cost.earned_value.eac_formula}}` sets the default. Prefer **current-rate**: it
assumes the project continues to behave as it has, which is the honest assumption absent a
named, funded reason for improvement (RI-07).

TCPI is the reality check nobody likes: when the project has run at CPI 0.85 and TCPI says
1.25 is now needed, the recovery plan is asking the same team to become 47% more efficient
than they have ever been. That number is the argument for a decision.

### CT-05 — Read the two indices together

| SPI | CPI | Reading |
|---|---|---|
| < 1 | < 1 | behind and over — the common case; scope or date must give |
| < 1 | > 1 | behind but efficient — usually under-staffed, or blocked waiting |
| > 1 | < 1 | ahead but expensive — overtime, crashing, or too many senior people |
| > 1 | > 1 | ahead and under — verify EV first; usually optimistic progress claims |

The last row deserves suspicion, not celebration. Genuine early over-performance is rare;
overstated progress is not. Check a sample of packages reported complete against their
acceptance criteria (WB-05) before reporting it.

### CT-06 — EVM fails silently when progress is dishonest

Every EVM number is downstream of EV, and EV is downstream of percent-complete. Three
integrity rules:

1. Progress by `{{profile.schedule.progress_measurement}}` only. Under 0-50-100 there is no
   such thing as 90%.
2. 100% means accepted against the acceptance criteria, not "the developer finished".
3. Effort comes from timesheets, not from the plan. A project that books plan hours as
   actuals has a CPI of exactly 1.00 forever and learns nothing.

An EVM report built on self-assessed percentages is not just wrong, it is confidently
wrong — the numbers look rigorous, so nobody questions them until the milestone is missed.

---

## Part 3 — Control

### CT-07 — Variance analysis explains, then proposes

For every control account outside the threshold in
`{{profile.schedule.variance_thresholds}}`:

```
{control account}  SV {x}  SPI {x.xx}  CV {y}  CPI {y.yy}
  Cause     : {the specific reason — not "took longer than expected"}
  Since     : {when it started; is it one event or a trend}
  Trend     : {improving | stable | worsening}
  Impact    : {on the milestone, on the critical path, on EAC}
  Action    : {what, who, by when}
  Recovery  : {realistic — with the TCPI it implies}
```

"Effort was underestimated" is a symptom. "The interface specification arrived four weeks
late, so three packages were re-planned against an assumption that proved wrong (ASM-014)"
is a cause, and it points at both the fix and the lesson.

### CT-08 — Contingency drawdown is logged, always

Every draw records: date, amount, the `RSK-*` or `ISS-*` it covers, the approver, and the
remaining balance — in `{{profile.risk.contingency_drawdown_log}}`.

The burn rate of the reserve is a leading indicator, and it leads by months: at 30% elapsed
with 60% of contingency consumed, the project is failing regardless of what SPI currently
says, because the remaining risks now have nothing behind them.

Contingency is never used to cover a **scope** addition. That is a change request (PB-07).
Using reserve to absorb scope hides the change and exhausts the protection against the risks
that were actually identified.

### CT-09 — Forecast honestly (RI-07)

The EAC assumes today's performance continues, unless a **named, funded reason** says
otherwise: people added (with their ramp cost), scope removed (with its CR), a blocker
resolved (with its date).

"We will catch up in the next phase" is not a reason. Projects do not spontaneously become
more efficient; they become more efficient when something changes, and that something is
either in the plan or it is not going to happen.

Report EAC as a range when the estimate stage justifies it, and always state which formula
produced it.

### CT-10 — Effort tracking that survives an audit

Timesheets book to WBS codes, not to "project". Without that, effort cannot be compared to
the estimate at package level, and the organisation learns nothing for the next bid.

Book overtime as hours worked. Suppressing it makes CPI look healthy while the team burns
out — and the exhaustion arrives as a quality problem and then a resignation, both of which
cost more than the number would have.

### CT-11 — Invoicing follows acceptance, not activity

`{{profile.cost.billing}}`. Under milestone billing, the invoice trigger is the signed
acceptance of the milestone's deliverables (SM-05), not the calendar date.

Track: milestone → acceptance record → invoice → payment, with dates. Unbilled accepted
work and unpaid invoices are both project risks and both belong in the monthly report — an
unpaid invoice is frequently the first visible symptom of a dispute nobody has raised yet.

---

## Reporting format

```
Cost — {period}, as of {date}
  BAC {amount}   PV {amount}   EV {amount}   AC {amount}
  SV {amount} ({SPI})          CV {amount} ({CPI})
  EAC {amount} ({formula})     ETC {amount}   VAC {amount}   TCPI {x.xx}
  Contingency  : {used}/{total} ({%}) — remaining covers RSK-{ids}
  Mgmt reserve : {used}/{total}
  Burn rate    : {amount}/period vs planned {amount}/period
  Variances    : {control accounts outside threshold, each with cause and action}
  Forecast     : {EAC reasoning; what would change it}
  Billing      : {invoiced}/{accepted}/{paid}
```

Every figure carries its as-of date and its source (RI-02). A cost report whose numbers
cannot be recomputed from the timesheets and the progress record is an assertion.
