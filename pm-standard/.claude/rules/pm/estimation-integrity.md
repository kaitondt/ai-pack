# RULE FAMILY: ESTIMATION INTEGRITY

An estimate is a **prediction with a stated method, a stated basis and a stated
uncertainty**. A single number with none of those is a wish, and it will be treated as a
commitment by everyone who reads it.

Values come from `{{profile.cost}}` and `{{profile.calendar}}`.

## ES-01 — Every estimate carries method, basis, range and assumptions

No estimate is issued as a bare number. The minimum record:

| Field | Content |
|---|---|
| Method | one of `{{profile.cost.estimation_methods}}` |
| Basis | what it was derived from — which work packages, which historical project, which measured rate |
| Range | optimistic / most likely / pessimistic, or a ± percentage tied to the estimating stage |
| Assumptions | each as an `ASM-*` with an owner and an impact-if-wrong |
| Exclusions | what the number does **not** cover |
| Confidence | and what would raise it |
| Estimator and date | who produced it and when |

An estimate whose basis cannot be reconstructed cannot be defended in a change request, and
it cannot be improved next time — which is how organisations estimate at the same accuracy
for a decade.

## ES-02 — Estimate the work, not the answer

When a target date or a target price exists, produce the estimate **first**, then compare.
Never derive the estimate backwards from the target.

If the estimate exceeds the target, that is a finding, and the response is a decision about
scope, quality, resources or date — taken by the people in
`{{profile.governance}}`, not absorbed by shrinking numbers until they fit.

Back-fitting is the most damaging thing in this file, because it destroys the one signal
that could have prevented the failure while it was still cheap.

## ES-03 — Estimate at the level you actually know

| Stage | Method | Expected accuracy |
|---|---|---|
| Pre-charter / bid | analogous or parametric | −25% to +75% |
| Post-requirements | parametric plus partial bottom-up | −15% to +30% |
| Post-design, per work package | WBS bottom-up, three-point | −10% to +15% |

State the stage with the number. A ±10% figure presented before requirements exist is not
precision, it is a fabrication with decimal places.

Re-estimate at every stage boundary and at every approved CR. An estimate that has not been
revisited since the bid is a historical artifact, not a forecast.

## ES-04 — Effort, duration and cost are three different numbers

- **Effort** = person-hours of work.
- **Duration** = calendar time, derived from effort ÷ (available people ×
  `{{profile.calendar.productive_hours_per_day}}` × availability), plus dependency waits.
- **Cost** = effort × rate, plus non-labour costs.

Conflating them is the most common arithmetic error in project planning. 80 hours is not
two weeks: at 6.5 productive hours per day and 85% allocation it is closer to fifteen
working days, and that is before a single dependency, review cycle or clarification.

Non-labour cost is real: licences, environments, travel, third-party services, hardware.
An estimate with only labour in it is incomplete.

## ES-05 — Padding is forbidden; buffers are mandatory

Every individual estimate is the honest expected value for that work package. Uncertainty
is handled **visibly**, at project level:

- a schedule buffer sized by `{{profile.schedule.buffer_policy}}`, owned by the PM
- a contingency reserve sized by `{{profile.cost.contingency_percent}}`, drawn down against
  identified risks and logged in `{{profile.risk.contingency_drawdown_log}}`

Padding hidden inside estimates cannot be measured, cannot be recovered when the risk does
not occur, and is silently consumed by Parkinson's law. It also destroys the only data the
organisation has for estimating the next project.

## ES-06 — Contingency and management reserve are different money

| Reserve | Covers | Owned by | Spent on |
|---|---|---|---|
| Contingency | identified risks in the register | project_manager | a risk that materialised, logged against its `RSK-*` |
| Management reserve | unknown-unknowns | sponsor | a scope or situation nobody foresaw, released by decision |

Contingency is inside the cost baseline; management reserve is outside it, inside the
budget. Merging them means the PM spends the sponsor's money without asking, and the
project has no visible signal that its risk exposure is being consumed.

Every drawdown records: date, amount, which `RSK-*` or `ISS-*`, approver, remaining balance.
A reserve with no drawdown log is a reserve nobody can prove still exists.

## ES-07 — Every estimate includes the work people forget

Bottom-up totals are wrong in a predictable direction. These are work packages, not
overhead, and they belong in the WBS with effort attached:

project management and reporting · requirement clarification and rework · design and code
review effort (for reviewers, not only authors) · test case design · defect fixing and
re-testing · environment setup and data preparation · release, deployment and rehearsal ·
documentation and handover · client meetings, demos and UAT support · knowledge transfer ·
onboarding and ramp-up for anyone joining after kickoff.

Cross-check the total against `{{profile.cost.productivity.phase_distribution}}`. A plan
whose testing share is far below the distribution is not efficient; it has simply not
estimated the testing yet.

## ES-08 — Productivity rates are measured, or the estimate is marked unverified

`{{profile.cost.productivity.rates}}` must state its `basis` — which past project, measured
how. Rates copied from a template, a textbook or another organisation are unverified, and
any estimate built on them says so in its confidence field.

After delivery, feed the actuals back (`/pm_lessons`). An organisation that never compares
estimate to actual has no estimating capability, only estimating habits.
