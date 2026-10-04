# RULE FAMILY: REPORTING INTEGRITY

A status report exists so that someone can make a decision. Everything else in it is
decoration, and anything in it that is not true is worse than nothing — it removes the
chance to act while acting is still cheap.

Cadences, audiences and content come from `{{profile.reporting}}`.

## RI-01 — A report answers four questions, in this order

1. **Where are we against the baseline?** — with numbers, not adjectives.
2. **What is off, and by how much?** — variance, and whether it is recoverable.
3. **What decision or action is needed, from whom, by when?**
4. **What has changed since the last report?** — risks, scope, resources, assumptions.

A report that describes activity ("the team worked on the design") without position
against the plan is a diary entry. Activity is not progress.

## RI-02 — Every number comes from evidence, and the evidence is named

Sources are `{{profile.reporting.data_sources}}`. A number in a report carries, at least
implicitly, the run or the extract it came from and its as-of date.

Forbidden, in every case:

- carrying a number forward from the last report because nothing was collected this period
- estimating progress from memory or from a stand-up impression
- reporting a test as passed when it was skipped, blocked or not run
- reporting effort from the plan rather than from the timesheet

If a number could not be collected, the report says **not collected**, why, and when it
will be. That is a legitimate status. A fabricated number is not.

## RI-03 — Percent-complete follows the profile method, never self-assessment

Progress is measured by `{{profile.schedule.progress_measurement}}`. Under `0-50-100`: not
started is 0%, in progress is 50%, **done means done and accepted** at 100%, and there is no
other value.

"90% complete" reported by the person doing the work is the most reliable early indicator of
a late project, because the last 10% contains the integration, the review, the rework and
the defects. A work package sitting at 50% for three reporting periods is a red flag; the
same package sliding 70% → 80% → 90% → 95% is the same problem, disguised.

## RI-04 — RAG follows from the numbers, not from the mood

Green / Amber / Red are defined in `{{profile.reporting.rag_definitions}}` and thresholded
by `{{profile.schedule.variance_thresholds}}`. The status is computed, then explained — not
chosen and then justified.

Two specific prohibitions:

- **No green-shifting.** A status that meets the Amber definition is reported Amber, even
  when a recovery plan exists. The recovery plan is reported next to it.
- **No watermelon reporting** — green on the cover, red inside. If any section of the report
  contains an unrecoverable variance, the overall status is not green.

A project that goes from green to red in one step has been reported wrongly for weeks; the
Amber period is exactly the window in which a decision would have been cheap.

## RI-05 — Bad news travels immediately, not on the cadence

A material event does not wait for Friday. Report immediately, through the escalation path
in `{{profile.governance.escalation}}`, when:

a payment milestone becomes at risk · a critical dependency will be late · a key person
leaves or becomes unavailable · a high-exposure risk materialises · a defect threatens
acceptance · the contingency reserve crosses half consumed · a client decision is now
blocking work · an assumption the baseline depends on turns out to be wrong.

The weekly report then records that it was raised, when, to whom, and what was decided.

## RI-06 — Each report is written for its audience, and stops there

| Report | Reader | Decision it supports | What does not belong |
|---|---|---|---|
| Daily | delivery team | unblock today | metrics, forecasts, narrative |
| Weekly | client PM, delivery manager | keep the plan on track | task-level detail, individual names against slippage |
| Monthly | sponsor, steering | fund, re-scope, re-plan | task lists, tool output |
| Quarterly | sponsor, steering | is the business case still valid | operational detail of any kind |
| Quality | QA lead, client PM | is the product ready to progress | schedule commentary |

Padding a weekly report with task detail to look diligent buries the two lines that
required a decision. Length is not evidence of control.

## RI-07 — Forecast, do not extrapolate the wish

The forecast (EAC, forecast finish) is computed from actual performance to date, using
`{{profile.cost.earned_value.eac_formula}}`. A forecast that assumes the remaining work will
suddenly run faster than all the work so far requires a **named reason** — more people
(with a ramp cost), removed scope, a resolved blocker — recorded in the report.

"We will catch up" is not a reason. It is the most expensive sentence in project management,
because it postpones the decision until the options are gone.

## RI-08 — Actions have an owner, a date and an ageing count

Every action, decision request and blocker carries: what, who (one named person, never a
team), by when, and how long it has been open. Age is the diagnostic — an item open for
five weeks is not an action, it is an unescalated issue.

`{{profile.reporting.action_item_log}}` is the register; the report shows the open subset.

## RI-09 — A metric is never improved by reclassifying the work behind it

Forbidden, without exception:

- lowering a defect severity to satisfy an exit criterion
- closing a defect as "not reproducible" with no investigation record
- merging defects to reduce a count
- moving scope out of the current release without a CR to make a milestone
- counting a partially delivered work package as complete because the milestone date arrived
- re-attributing a defect to a later phase to protect a containment number
- deferring an open item with no named approver and no target date

Each of these makes the report better and the project worse. The report exists to inform a
decision; a tuned number disables the decision silently, and nobody notices until the client
does.
