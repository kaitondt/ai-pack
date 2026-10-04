---
description: "Apply an approved change request: record the decision, update the scope, schedule and cost baselines, hand execution to the technical pack, then verify consistency and close the CR with actual versus estimated effort. Usage: /pm_change_apply <CR-nnn>"
---

# Apply an approved change request

Phases 4–6. Requires an approval recorded by the authority `/pm_change_assess` identified.

## Step 1 — Load and verify the approval

`pm_project`, then `pm_change_control`. Agent: `pm_change_analyst`.

Refuse to proceed unless the register shows: the option chosen, the approver by name, the
date, and the baseline impact accepted (IC-08). "Approved on the call" is not an approval
(DA-04) — record it in writing first.

## Step 2 — Record the decision

`DEC-*` in `{{profile.paths.decision_log}}`: the question, the options presented, the choice,
who decided, when, and what it affects. Reference it from the CR.

## Step 3 — Update the baselines, in order (IC-09)

1. Scope baseline — scope statement, WBS, WBS dictionary (all three, PB-02)
2. Schedule baseline, or record the float consumed and the new float remaining
3. Cost baseline and the affected control account
4. RTM, quality plan and test plan, if affected
5. Each document's revision history, citing the CR (MD-02)

Baselines move **before** execution. Executing first means every subsequent report measures
against a plan nobody is following.

The baseline guard hook blocks edits to baselined paths unless a CR is active. Write the CR id
to `.codex/.active_pm_cr` for the duration of this command, and clear it at step 6.

## Step 4 — Hand off execution (IC-10)

| Technical pack | Hand off to |
|---|---|
| `sdlc` | `/sdlc_cr_design` → `/sdlc_cr_implement` → `/sdlc_cr_report` |
| `migration` | `/mig_cr_design` → `/mig_cr_implement` → `/mig_cr_report` |
| none | the team, against the updated baselines |

Their cascade rules govern document and code order. Do not duplicate that work here.

## Step 5 — Verify

- the change is present in the deliverables
- the baselines are internally consistent again (PB-04)
- test cases updated; previously passed cases invalidated by the change are marked for re-run
- traceability rows updated, citing the CR as the ancestor (PN-04)
- **no unrelated change rode along with it** — the most common way a CR delivers more than was
  approved

## Step 6 — Close with actual versus estimate

Record actual effort against the estimate, and why it differed if it is material. This is the
only input that improves the next CR estimate, and it is the first thing dropped when the
project is busy.

Clear `.codex/.active_pm_cr`.

## Report

```
CR-{nnn} — {title}                                              APPLIED
  Approved by   : {name}, {date}   Option: {chosen}
  Decision      : DEC-{nnn}
  Baselines     : scope v{x} · schedule v{y} · cost v{z}
  Documents     : {n} updated, each with a revision row citing CR-{nnn}
  Executed by   : {technical pack commands, or the team}
  Test cases    : {n} added · {n} changed · {n} invalidated and marked for re-run
  Traceability  : {n} rows updated
  Consistency   : {PB-04 checks, pass/fail}
  Actual vs est.: {h} vs {h} ({x}%) — {why, if material}
  Cumulative    : {n} CRs to date, +{h}h, +{d}d, +{amount} against the original baseline
```
