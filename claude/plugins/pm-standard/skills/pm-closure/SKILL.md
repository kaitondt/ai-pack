---
name: pm-closure
description: "Project closing — deliverable acceptance, handover and knowledge transfer, contract closure, final report, lessons learned, resource release, archiving and the post-implementation review. Load for ALL closing, acceptance, handover, lessons-learned and project-archive tasks."
---

# Project Closing

> Prerequisite: `pm-project` loaded.

Closing is a phase with work in it, and it is the phase most reliably under-planned: the team
has already moved on, the client considers it finished, and the effort is not in the WBS. The
result is a project that never formally ends — resources still charging, obligations unclear,
lessons never captured, and a final invoice nobody will approve.

Plan closing at planning time. It belongs in the WBS with effort against it (WB-02).

---

## The sequence

```
1. Deliverable acceptance      each deliverable formally accepted, or not
2. Handover                    to operations / support / the client's team
3. Open items disposition      defects, CRs and risks: closed, deferred or transferred
4. Contract closure            final invoice, obligations, warranty
5. Final report                against the charter, not against the last plan
6. Lessons learned             with the actuals behind them
7. Resource release            people, licences, environments, accesses
8. Archive                     what the organisation keeps
9. Post-implementation review  after {{profile.closing.post_implementation_review_after_days}} days
```

---

## CL-01 — Acceptance is per deliverable, against the criteria written at planning time

For every `{{profile.scope.deliverables}}` entry: checked against the acceptance criteria
agreed under SM-06, by the named acceptor, on a date, with a verdict.

```
{D-id} {deliverable}   Criteria: {as written at planning}
  Verified by {name} on {date}   Verdict: accepted | accepted with conditions | rejected
  Conditions: {each an ACT-* with owner and date}
  Evidence  : {test results, demo record, document version, review record}
```

**Accepted with conditions is a real state**, and it must not be allowed to blur into
accepted. Each condition is tracked to closure like any other action, and the final invoice
condition (`{{profile.closing.contract_closure.final_invoice_condition}}`) states which
states satisfy it.

Where acceptance criteria were never agreed in writing, say so plainly and negotiate now —
but record that this happened, because it is the lesson: the acceptance argument was created
at planning time, by an omission.

## CL-02 — Handover is a transfer of capability, not a transfer of files

`{{profile.closing.handover.items}}`. The receiving team can operate the system without the
project team. The test is behavioural, not documentary:

| Item | Done means |
|---|---|
| Source and build pipeline | the receiving team has built and deployed it themselves, once |
| Deployment runbook | someone outside the project followed it successfully |
| Operations manual | covers monitoring, backup, restore, common failures |
| Known issues and workarounds | written down, including the embarrassing ones |
| Support contacts and escalation | named people, with the arrangement agreed by them |
| Credentials transfer | recorded, with project accounts revoked afterwards |
| Training | delivered, with attendees and a competence check |
| Open CR backlog | transferred with estimates, so nothing is silently dropped |

A handover meeting where documents are presented is not a handover. A handover where the
receiving team performs the operation while the project team watches is.

The "known issues, including the embarrassing ones" line is worth insisting on. Every
undisclosed known issue becomes a support incident that the receiving team hits blind, and it
costs more trust than the disclosure ever would.

## CL-03 — Dispose of every open item explicitly

Nothing is left in an undefined state:

| Item | Dispositions |
|---|---|
| Open defects | fixed · deferred to warranty with an approver · accepted by the client with the impact stated |
| Open CRs | approved for a later phase · rejected · transferred to the support backlog |
| Open risks | closed · transferred to the operations team with its response |
| Open actions | closed · transferred with a named owner in the receiving organisation |
| Open assumptions | confirmed · converted to a known limitation |

An item with no disposition becomes the receiving team's problem without their knowledge, and
it is the origin of the first post-go-live argument.

## CL-04 — Contract closure

`{{profile.closing.contract_closure}}`:

- final invoice raised on the stated condition, and its acceptance evidence attached
- all milestone payments reconciled — invoiced, accepted, paid
- retained obligations documented: warranty scope, duration, response times, what is
  explicitly *not* covered
- subcontractor closure, if `{{profile.resource.subcontract.used}}`
- licences and third-party agreements transferred or terminated, deliberately
- claims, disputes and outstanding CRs settled or explicitly recorded as open

Warranty scope is the clause that most often ends in disagreement. Write what it covers and
what it does not — a defect against a baselined specification is warranty; behaviour nobody
specified is a change request, even after go-live (IC-02).

## CL-05 — The final report measures against the charter

Not against the last re-baselined plan. Against what was authorised at the start (CH-02),
with the baseline history in between (PB-06):

```
Final Report — {project}
1. Objectives      : each charter objective, its metric, target vs achieved, verdict
2. Scope           : delivered vs baselined; changes, with their cumulative impact
3. Schedule        : original baseline → final; every re-baseline with its reason
4. Cost            : original budget → final; reserves consumed; variance explained
5. Quality         : final metrics; escaped defects; open items at handover
6. Risk            : what materialised, whether it was foreseen, whether the response worked
7. Client feedback : in the client's own words, gathered before this is written
8. Lessons         : the top ones, with the evidence
9. Recommendations : for the receiving team and for the next project of this kind
```

Section 1 is why the report exists. A project can hit its final re-baselined plan exactly and
have failed its charter objectives entirely — that is the outcome nobody reports, because at
that point everyone is measuring against the plan they last agreed rather than the one they
were funded for.

Section 6 is the honest one. Of everything that went wrong, how much was in the risk register
before it happened? That ratio is the project's real risk-management score.

## CL-06 — Release resources deliberately

`{{profile.closing.resource_release}}`: people (with their release dates and where they go),
licences, environments, cloud resources, system accesses, physical assets.

An unreleased resource is still being billed somewhere, and a still-active access is a
security finding. A project that is "finished" but has not released its team has not
finished — it has stopped, and the cost continues.

Release accesses on a date, not "when convenient". The project account that stays live for
eight months is found by an audit, not by the team.

---

## Lessons learned

### CL-07 — Capture lessons throughout, not at the end

A lesson captured six months after the event has lost its detail and its evidence, and the
people who lived it have moved on. `/pm-lessons` runs at every gate, after every major issue,
and after every CR that went badly — not only at closing.

Each lesson (`LL-*`):

| Field | Content |
|---|---|
| What happened | the specific event, with dates and evidence |
| Impact | effort, schedule, cost, quality — quantified |
| Root cause | why, not who |
| What we would do differently | concrete and actionable |
| Where it belongs | a rule, a checklist, a template, a hook, an estimating rate |
| Owner | who carries it into the organisation |

### CL-08 — A lesson that changes nothing is an anecdote

The last two fields are what makes this real. "Communication could have been better" is an
anecdote. "Client design decisions took 6 working days on average against a 2-day assumption,
costing 11 days across the project; add a decision-latency line to the estimating template
and put the SLA in the next contract" is a lesson.

Route each one:

| Lesson about | Goes to |
|---|---|
| Estimating accuracy | `{{profile.cost.productivity}}` rates, with the measured actuals (ES-08) |
| A missed check | a rule or checklist — `/pm-refine-skill` |
| A recurring risk | the standard risk checklist (RK-04) |
| A process gap | `{{profile.process.process_assets}}` |
| A contract clause | the organisation's contracting template |

### CL-09 — Estimate versus actual, per work package

The single most valuable artifact closing produces. For every work package: estimated effort,
actual effort, variance, and why.

This is what turns an organisation's estimating from habit into capability (ES-08). It takes
a day at closing and it is the first thing cut. Cutting it means the next bid is produced with
exactly the information this one had.

---

## Archive

`{{profile.closing.archive_root}}`: baselines and their history, all approved deliverables,
the registers (risk, issue, change, decision, action), reports, acceptance records, contracts
and amendments, lessons, and the estimate-versus-actual data.

Archive the **register**, not the conversation. What matters in three years is what was
decided, when, by whom, and against which version.

---

## Post-implementation review

After `{{profile.closing.post_implementation_review_after_days}}` days, with the users:

- are the charter objectives actually being realised in operation? (CH-02 metrics, measured)
- what has the support load been, and against which components?
- what did the project get wrong that only shows up in use?
- what should the next project of this kind do differently?

This is the only feedback loop that reaches past acceptance, and it is where the difference
between "delivered" and "worked" becomes visible.

---

## Exit criteria

- [ ] Every deliverable formally accepted, or its state explicitly recorded (CL-01)
- [ ] Handover completed and demonstrated, not just documented (CL-02)
- [ ] Every open defect, CR, risk, action and assumption has a disposition (CL-03)
- [ ] Contract closed: final invoice, obligations, warranty scope written (CL-04)
- [ ] Final report measured against the **charter** (CL-05)
- [ ] Lessons captured with owners and destinations (CL-07, CL-08)
- [ ] Estimate vs actual recorded per work package (CL-09)
- [ ] Resources, licences and accesses released on dated records (CL-06)
- [ ] Archive complete
- [ ] PIR scheduled
- [ ] Closure approved by `{{profile.governance.approvals.closure}}`
