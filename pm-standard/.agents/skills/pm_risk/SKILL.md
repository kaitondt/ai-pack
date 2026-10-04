---
name: pm_risk
description: "Risk and issue management — risk identification, qualitative and quantitative analysis, response planning, the risk register, the issue log, contingency drawdown, escalation, secondary and residual risk, and risk review cadence. Load for ALL risk, issue, escalation and contingency tasks."
---

# Risk and Issue Management

> Prerequisite: `pm_project` loaded.

Risk management is the only project discipline that pays off before anything goes wrong. Its
failure mode is not being wrong about a risk; it is producing a register at kickoff, never
reviewing it, and discovering at the post-mortem that the thing that sank the project was on
page two.

---

## RK-01 — A risk and an issue are different objects

| | Risk | Issue |
|---|---|---|
| State | might happen | has happened |
| Register | `{{profile.risk.register}}` | `{{profile.risk.issue_log}}` |
| Managed by | probability × impact, with a planned response | resolution, with an owner and an SLA |
| Money | contingency reserve | contingency drawdown, logged |
| Question | what do we do if? | who is fixing it, by when? |

When a risk materialises it becomes an issue **and keeps its risk ID as its ancestor**
(PN-04). That link is what lets the post-mortem answer the only question that improves the
next project: did we see it coming, and did our response work?

A register full of items that are actually issues means nobody is looking forward. It is a
common and diagnostic pattern.

---

## Part 1 — Identification

### RK-02 — Identify continuously, not once

At: planning, every gate, every change request, every new dependency, every team change, and
on the review cadence `{{profile.risk.review_cadence}}`.

Techniques that actually surface things, in rough order of yield:

| Technique | Finds |
|---|---|
| Assumption analysis | every `ASM-*` is a risk wearing a different label — start here |
| Dependency analysis | every `DEP-*` outside your control |
| Estimate uncertainty | packages with the widest O–P spread (EM-01) |
| Lessons learned from past projects | the risks this organisation reliably repeats |
| Pre-mortem | "it is six months later and the project failed — what happened?" |
| Interface and integration points | where two teams' assumptions meet |
| Checklist by category | `{{profile.risk.categories}}` |

The pre-mortem is worth the hour it takes. People who will not raise a concern in a status
meeting will describe a failure in detail when it is framed as hypothetical.

### RK-03 — Write the risk as cause → event → effect

> **Because** the interface specification is owned by a third party with no committed date,
> **there is a risk that** it arrives after design starts, **which would** stall PRJ.4.2 and
> PRJ.4.3 and put M2 at risk.

A risk written as a single noun — "integration risk", "resource risk" — cannot be analysed,
assigned a response, or closed. The cause is where the response attaches; the effect is
where the impact is measured.

### RK-04 — The risks worth checking for on every project

An unavailable decision-maker · an external interface not yet specified · data volume or
quality nobody has measured · a single-holder role (key-person risk, per
`{{profile.resource.key_person_risk}}`) · a dependency on a team with its own schedule and
priorities · a technology nobody in the team has used in production · a client-side resource
commitment not secured in writing · an environment that does not exist yet · a regulatory
date outside the project's control · acceptance criteria not agreed before build · a
fixed-price contract with an unbaselined scope.

The last one is not a risk in the usual sense. It is a certainty with an unknown size.

---

## Part 2 — Analysis

### RK-05 — Qualitative first: probability × impact

Scales from `{{profile.risk.probability_scale}}` and `{{profile.risk.impact_scale}}`, both
with numeric anchors so two people score alike. Exposure = P × I, banded by
`{{profile.risk.exposure_thresholds}}`.

Score impact on the dimension that actually matters for that risk — schedule, cost, quality,
scope or reputation — and say which. A risk with a 3-day schedule impact and a 3-week
reputational one has been scored wrongly if only the schedule was considered.

Re-score at each review. A risk whose probability rises as its trigger date approaches is
the normal case, and watching that movement is most of the value of the register.

### RK-06 — Quantitative where the money justifies it

For high-exposure risks:

```
expected monetary value = probability × cost impact
```

Use it to size contingency and to compare responses: a mitigation costing 20 hours against
an EMV of 200 hours is obviously worth doing, and the arithmetic ends the debate faster than
the discussion would.

For schedule risk on the critical path, three-point durations plus a simple simulation give
a completion-date distribution rather than a single date. Worth it on large projects; on
small ones the register plus honest buffers does the same job for less effort.

### RK-07 — Do not average the register into a single number

"Total risk exposure: 47" tells nobody anything. Report the **profile**: how many high, what
changed, which are approaching their trigger dates, and which have no response.

---

## Part 3 — Response

### RK-08 — Five responses, each with a concrete action

| Response | Means | Example |
|---|---|---|
| **Avoid** | remove the cause | drop the feature that needs the unspecified interface |
| **Mitigate** | reduce probability or impact | build against a stub; agree a fallback format |
| **Transfer** | move it to whoever can bear it | contractual clause, insurance, vendor SLA |
| **Accept** | do nothing, knowingly | with a named acceptor and a contingency allocation |
| **Escalate** | it is outside the PM's authority | to the owner in `{{profile.governance.escalation}}` |

Every response names a concrete action, an owner and a date. **"Monitor" is not a response.**
It is the absence of one, written in a way that survives review, and it is the most common
entry in weak registers.

Acceptance is a legitimate and often correct response — but it is a *decision*, with a named
acceptor (DA-01) and money behind it, not a shrug.

### RK-09 — Secondary and residual risk

- **Secondary risk** — created by the response itself. Fast-tracking to recover schedule
  creates rework risk. Adding people creates onboarding and consistency risk. Every mitigation
  gets this question asked.
- **Residual risk** — what remains after the response. State it, with its exposure. A
  mitigation that reduces exposure from 20 to 12 has not closed the risk.

A register where every response reduces exposure to zero has not been thought about.

### RK-10 — Triggers make the response executable

Each significant risk carries a trigger: the observable event that says *now*.

> Trigger: interface specification not received by 2026/04/15.
> Then: switch PRJ.4.2 to the stub-based approach (adds 24 h, already estimated) and notify
> the client the same day.

Without a trigger, the response is a good intention that gets executed after the impact has
already landed. With one, the decision is pre-made and can be taken by whoever notices.

---

## Part 4 — Issues

### RK-11 — Issues have owners, SLAs and ages

`{{profile.risk.issue_log}}`, SLA from `{{profile.risk.issue_sla_hours}}`.

| Field | Content |
|---|---|
| `ISS-*` | id |
| Description | what happened, and what it is currently blocking |
| From risk | the `RSK-*` it materialised from, or "unforeseen" |
| Severity | per the SLA table |
| Owner | one named person (DA-01) |
| Raised / due / age | age is the diagnostic |
| Resolution | what was done |
| Cost | effort and money consumed; contingency drawn (CT-08) |

Report ageing, not just counts. An issue open for three weeks is not being managed; it is
either escalated (DA-05) or it has been accepted without anyone saying so.

Every issue that came from an unforeseen source is a lesson (`/pm_lessons`): what would have
had to be true for us to have seen this coming?

### RK-12 — Escalate on the clock (DA-05)

Above `{{profile.risk.escalate_above_exposure}}`, or past the SLA, escalation is automatic
and factual: the issue, who was asked and when, what is blocked now, what is blocked next,
and the recommendation.

Escalation is a process step, not an accusation. Framing it that way is what keeps people
willing to use it — and a project where escalation feels like failure is a project where
issues age silently.

---

## Review and reporting

`{{profile.risk.review_cadence}}`. Every review: re-score, check triggers, verify responses
are actually happening, close what is gone, add what is new, and check the contingency
balance against the remaining exposure.

```
Risk — {date}
  High {n} (was {n})   Medium {n}   Low {n}
  New this period      : {ids and titles}
  Closed               : {ids, and why — passed, avoided, or materialised}
  Exposure changed     : {ids, from → to, why}
  Approaching trigger  : {ids, trigger date}
  Without a response   : {ids}   ← this line should be empty
  Materialised         : {RSK → ISS}, contingency drawn {amount}
  Contingency          : {used}/{total}; remaining covers {which risks}
```

The "without a response" line is the register's own quality metric. So is the ratio of risks
identified in planning to issues arriving unforeseen — a project where most issues were never
risks is not doing risk management, whatever the register looks like.
