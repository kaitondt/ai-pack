# RULE FAMILY: DECISION AUTHORITY

Most project failures that look like execution failures are decision failures: the decision
was never made, was made by someone without the authority, or was made and never recorded.

Roles and approvals come from `{{profile.governance}}`.

## DA-01 — Every decision has one named owner

Not a team, not a department, not "the client". One person from
`{{profile.governance}}`, who can say yes and make it stick.

A decision with no named owner is an assumption (see `ASM-*` in `pm_scope`), and it is
tracked as one — with a confirm-by date and an impact-if-wrong — until someone owns it.

When the profile leaves a governance role unfilled, stop and ask. Producing a plan that
routes approvals to an empty role produces a project where nothing can be approved.

## DA-02 — Authority is matched to impact, in writing

`{{profile.change_control.authority}}` states which body decides at which size of impact.
Below the first threshold the PM absorbs and records; above it, the named body decides.

Two failure directions, both common:

- **Under-escalation** — the PM absorbs decisions above their authority to avoid friction.
  It works until the accumulated absorptions become a variance nobody authorised.
- **Over-escalation** — every trivial decision goes to the steering committee, which stops
  attending, and then the important one gets no attention either.

## DA-03 — A decision is recorded when it is made, or it did not happen

Every decision goes into `{{profile.paths.decision_log}}` as `DEC-*`, at the time, with:
the question, the options considered, the decision, the owner, the date, and what it
affects.

The log is **append-only**. A reversal is a new entry superseding the old one by ID, never
an edit — the history of what was believed when is exactly what a dispute needs.

The cost of the missing record is asymmetric: nobody needs the log while things go well,
and everybody needs it the week they stop.

## DA-04 — Verbal is not approved

An approval exists when it is written and attributable: a signature, an email, a ticket
transition, a recorded meeting decision confirmed in minutes. A statement on a call is a
step toward approval, and it is recorded as such — "pending written confirmation, requested
on <date>".

The minutes route is legitimate and cheap: circulate the decision in writing, state that
silence by a named date is acceptance, and keep the record.

## DA-05 — Escalate on the clock, not on frustration

`{{profile.governance.escalation}}` gives each level a response SLA. When a decision request
passes its SLA, it escalates automatically to the next level — as a fact, not as a
complaint.

Escalation is a process step, not an accusation, and framing it that way is what keeps it
usable. The message states: the decision needed, who was asked and when, what is blocked
now, what will be blocked next, and the recommendation.

An issue that ages past two escalation levels is reported in the next monthly report
regardless of whether it has since been resolved. Repeated escalation of the same kind of
decision is a governance defect, and it belongs in the lessons learned.

## DA-06 — RACI has exactly one A per row

For every deliverable and every significant activity in `{{profile.resource.raci_path}}`:
one **Accountable**, at least one **Responsible**, Consulted and Informed as needed.

Two people accountable means nobody is. Zero means the PM is, whether they know it or not.
An RACI where the same person is A on everything is an org chart, not an assignment — and
it names the project's key-person risk (`RSK-*`).
