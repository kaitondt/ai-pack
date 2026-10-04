---
description: "Identify, analyse and plan responses for risks; update the risk register. Runs at planning, at gates, on change requests, and whenever the situation changes. Usage: /pm_risk_assess [area | CR-nnn | 'pre-mortem']"
---

# Risk assessment

## Step 1 — Load

`pm_project`, then `pm_risk`. Agent: `pm_risk_manager`.

## Step 2 — Identify (RK-02)

Work through the techniques that actually yield, in this order:

1. **Assumption analysis** — every `ASM-*` in the assumption log is a risk wearing a different
   label. Start here; it is the highest-yield source and it is already written down.
2. **Dependency analysis** — every `DEP-*` outside the project's control.
3. **Estimate uncertainty** — the work packages with the widest O–P spread (EM-01).
4. **Lessons learned** — `LL-*` from past projects; the risks this organisation repeats.
5. **Pre-mortem** — "it is six months later and the project failed; what happened?" People
   who will not raise a concern in a status meeting will describe a failure in detail when it
   is hypothetical.
6. **Checklist** — `{{profile.risk.categories}}` and the standard list in RK-04.

## Step 3 — Write each risk as cause → event → effect (RK-03)

A single noun — "integration risk" — cannot be analysed, assigned or closed. The cause is
where the response attaches; the effect is where the impact is measured.

## Step 4 — Analyse (RK-05, RK-06)

Score probability and impact on `{{profile.risk.probability_scale}}` and
`{{profile.risk.impact_scale}}`, naming which dimension the impact is scored on. Exposure =
P × I, banded by `{{profile.risk.exposure_thresholds}}`.

For high-exposure risks, compute EMV = probability × cost impact, to size contingency and to
compare responses — the arithmetic ends most debates faster than the discussion would.

## Step 5 — Plan responses (RK-08, RK-09, RK-10)

One of avoid / mitigate / transfer / accept / escalate, each with a concrete action, an owner
and a date. **"Monitor" is not a response.**

Then, for each: the **secondary risk** the response itself creates, the **residual risk** that
remains, and the **trigger** — the observable event that says execute now.

## Step 6 — Reconcile with contingency

Sum the EMV of accepted and mitigated-but-residual risks and compare against the remaining
contingency balance (`{{profile.risk.contingency_drawdown_log}}`). Exposure exceeding the
remaining reserve is itself a finding, and it goes to the sponsor.

## Step 7 — Update and report

```
Risk assessment — {scope}, {date}
  Identified new  : {n}   Re-scored: {n}   Closed: {n}
  Profile         : high {n} (was {n}) · medium {n} · low {n}
  Top exposures   : {id, title, P×I, owner, response, trigger}
  Without response: {ids}          ← should be empty
  Without trigger : {ids}          ← for high exposures, should be empty
  Secondary risks : {n} created by the responses planned here
  EMV vs reserve  : {EMV total} vs {remaining contingency} — {covered | short by X}
  Escalated       : {ids above {{profile.risk.escalate_above_exposure}}}
```
