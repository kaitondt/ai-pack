# RULE FAMILY: BASELINE INTEGRITY

A project has exactly three baselines — **scope, schedule, cost** — plus the charter that
authorises them. Everything this pack reports is a comparison against one of them.

The failure mode these rules exist to prevent is quiet and universal: the plan drifts to
match reality, so every variance disappears, every report is green, and nobody can say
what was promised. A baseline that moves to match the actuals is not a baseline; it is a
diary.

Values come from `{{profile.constraints}}`, `{{profile.change_control}}` and
`{{profile.governance.approvals}}`.

## PB-01 — A baseline exists only after a named approval

A document is baselined when: the approvers named in
`{{profile.governance.approvals.<artifact>}}` have approved it, the approval is recorded in
its revision history with a date, and its path is registered in the baseline register.

Until then it is a draft, and it is reported as a draft. "Effectively agreed", "sent for
approval last week" and "verbally confirmed on the call" are drafts.

## PB-02 — The scope baseline is three documents, not one

Scope baseline = **scope statement + WBS + WBS dictionary**. A scope statement without a
WBS cannot be scheduled or costed; a WBS without a dictionary means every work package is
interpreted differently by the person who executes it.

A change to any of the three is a change to the scope baseline.

## PB-03 — A baseline changes only through approved change control

Once baselined, an artifact changes only through a change request approved at the
authority level `{{profile.change_control.authority}}` requires for its impact.

This is enforced mechanically by `hooks/guard_pm_baselines.py`: edits to a registered
baselined path are blocked unless `.claude/.active_pm_cr` names an approved CR.

The one exception is an **editorial** correction that changes no commitment — a typo, a
broken link, a formatting fix. It is still recorded in the revision history, and it never
touches a number, a date, a scope item or an acceptance criterion.

## PB-04 — The baselines are consistent or the project is not planned

These must always agree; when they do not, the plan is fiction:

| Consistency | Check |
|---|---|
| Scope ↔ schedule | every WBS work package appears in the schedule |
| Schedule ↔ cost | every scheduled activity has effort and cost in the cost baseline |
| Cost ↔ scope | the budget totals the work packages plus reserves, and nothing else |
| Scope ↔ deliverables | every contract deliverable maps to at least one work package |
| Scope ↔ requirements | every baselined requirement maps to at least one work package |

`/pm_trace_check` runs these. A work package with no schedule entry is work nobody will
do; a schedule entry with no work package is work nobody costed.

## PB-05 — Actuals never overwrite the baseline

The baseline file and the working file are different files
(`{{profile.schedule.baseline_path}}` vs `{{profile.schedule.working_file}}`). Progress,
re-planning and re-forecasting happen in the working file. The baseline is read-only until
a re-baseline is approved.

If the two are ever the same file, every variance the project has ever had has been erased.

## PB-06 — Re-baselining is a governance decision with a retained history

A re-baseline requires the approval named in `{{profile.change_control.rebaseline_policy}}`
and records, in the new baseline:

- which baseline it supersedes, and its version
- the cumulative variance at the moment of the reset (SV, CV, scope delta, date delta)
- **why** the old baseline is no longer a useful comparison
- what changes about how the project is run, so the same drift does not recur

The old baseline is kept. A project on its third baseline with no history of the first two
is a project that has been reporting green while slipping twice.

Re-baselining to make a variance disappear is forbidden. The variance is the information.

## PB-07 — Nothing enters scope without a change request

Not an extra report, not a helpful validation, not a small field the client mentioned on a
call, not a refactor the team wants. Under a fixed-price contract this rule *is* the
margin; under time-and-materials it is the client's budget.

The correct response to a small useful addition is: record it as a CR, estimate it, and let
the authority in `{{profile.change_control.authority}}` decide. The incorrect response —
absorbing it because it is small — is invisible in every report and is the single largest
source of unexplained overrun.

Ten absorbed changes of four hours each is a week nobody planned and nobody can point to.

## PB-08 — A baseline with unresolved assumptions is provisional, and says so

If the estimate or the schedule depends on an open `ASM-*` — an unconfirmed interface, an
unmeasured volume, an unavailable environment — the baseline carries the assumption
explicitly, with its owner, its confirm-by date and what changes if it is wrong.

Baselining over an open assumption without labelling it converts someone else's uncertainty
into the delivery team's commitment.
