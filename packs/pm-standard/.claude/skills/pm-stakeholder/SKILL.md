---
name: pm-stakeholder
description: "Stakeholder and communications management — stakeholder register and engagement assessment, the communications plan and matrix, meeting design and cadence, minutes, escalation practice, and offshore/cross-cultural communication. Load for ALL stakeholder, communication-plan, meeting, minutes and escalation-design tasks."
---

# Stakeholder and Communications Management

> Prerequisite: `pm-project` loaded. Decision authority in `rules/pm/decision-authority.md`.

Most projects that fail on communication do not fail from too little of it. They fail because
the person who needed to decide something never received the thing they needed to decide, in
a form they could act on, in time.

---

## Stakeholder register

Beyond `{{profile.governance}}`, which names decision owners, the register covers everyone
whose position affects the project:

| Field | Content |
|---|---|
| Name / role / organisation | who |
| Interest | what they want from the project |
| Concern | what they are afraid of — usually more predictive than interest |
| Influence | high / medium / low over decisions, resources or acceptance |
| Impact on them | how their work changes when this ships |
| Current stance | opposing · neutral · supportive · champion |
| Desired stance | and what would move them |
| Engagement | frequency, channel, who owns the relationship |

### SE-01 — The concern column is the useful one

Interest is what people say in the kickoff. Concern is what actually drives their behaviour
in month four: the operations manager afraid of a support burden they did not ask for, the
team lead whose people are being reassigned, the department whose process is being automated.

A stakeholder whose concern is unaddressed does not argue with the project. They become
unavailable, they escalate late, and they find the deliverable unacceptable for reasons that
appear at acceptance and turn out to be old.

### SE-02 — Engagement effort follows influence × impact

| | High influence | Low influence |
|---|---|---|
| **High impact on them** | manage closely: involve in decisions, brief before meetings | keep informed and consulted; they know the operational truth |
| **Low impact on them** | keep satisfied: short, decision-focused, no operational detail | monitor; do not spend the project's attention here |

The bottom-left quadrant is the one projects neglect and then regret. The people whose daily
work changes most often have no formal authority — and they are the ones who make the system
succeed or quietly work around it.

---

## Communications plan

One row per recurring communication:

| What | To whom | Why (which decision) | Format | Frequency | Owner | Language |
|---|---|---|---|---|---|---|

Derived from `{{profile.reporting.cadences}}` plus the ad-hoc channels: escalation, decision
requests, defect notifications, release announcements, and change-request submissions.

### SE-03 — Every communication serves a decision or it is deleted

For each row, name the decision it supports. A report that supports no decision is a habit
with a distribution list, and it consumes the attention the important message will need.

The corollary is more useful: when a decision is being made repeatedly with poor information,
there is a missing row. That is the gap worth filling, not the one nobody is reading.

### SE-04 — Push, pull and interactive have different jobs

| Mode | Use for | Fails at |
|---|---|---|
| Push (report, email) | status, records, notifications | anything requiring agreement |
| Pull (dashboard, repository) | reference material, detail on demand | anything urgent |
| Interactive (call, meeting) | decisions, disagreement, bad news, ambiguity | creating a record |

Two rules follow. **Bad news is interactive first, written second** — sending a red status by
email and waiting for the reaction wastes the day when the recovery decision was cheapest.
And **every interactive decision is written down afterwards** (RG-04), or it did not happen
(DA-04).

---

## Meetings

### SE-05 — A meeting without a decision is a status broadcast

Every recurring meeting states: its purpose, the decisions it makes, who must attend for it
to be quorate, its inputs (circulated beforehand), and its outputs.

| Meeting | Decides | Attendees | Cadence |
|---|---|---|---|
| Daily standup | today's blockers and re-allocation | team | daily, 15 min |
| Weekly status | corrective action within the plan | PM, client PM, leads | weekly |
| CCB | change requests within its authority | `{{profile.governance.ccb.members}}` | `{{profile.governance.ccb.cadence}}` |
| Steering committee | baselines, trade-offs, escalations | `{{profile.governance.steering_committee.members}}` | monthly |
| Gate review | proceed / conditions / hold / stop | per `{{profile.governance}}` | per gate |
| Retrospective | process changes | team | per phase or sprint |

A meeting whose material could have been an email should be an email. A decision that is
being made by email over five days should be a meeting.

### SE-06 — Minutes within one working day (RG-04)

Decisions as `DEC-*`, actions as `ACT-*` with owners and due dates, disagreements recorded as
disagreements. Circulate with a correction deadline and state that silence by that date is
acceptance.

Minutes arriving a week later are archaeology: nobody can correct a record they no longer
remember, so the record stands unverified — which is worse than no record, because it will
be quoted.

---

## SE-07 — Offshore and cross-cultural communication

Where `{{profile.project.engagement_model}}` is offshore or hybrid, several things that work
onshore stop working, and none of them announce themselves.

| Reality | Consequence | Practice |
|---|---|---|
| Time-zone gap | one question per day costs a day of duration | batch questions; hold a daily overlap window; give context so an answer is possible without a follow-up |
| Written asynchronous default | ambiguity is expensive and slow to resolve | write questions with options and a recommendation, so a one-word reply is actionable |
| Cultural difference in disagreement | silence or "we will try" may not mean yes | confirm understanding by asking for a restatement, never by asking "is that clear?" |
| Distance from the business | the team cannot see the process the software serves | invest in domain walkthroughs early; it is cheaper than the defects it prevents |
| Reduced informal signal | trouble becomes visible later than onshore | make status structurally visible: boards, evidence, demos, not verbal assurance |

The pattern worth naming: a distributed team's problems surface later than a co-located
team's, so the reporting discipline in `rules/pm/reporting-integrity.md` is not bureaucracy
here — it is the only early-warning system available.

### SE-08 — Ask questions that can be answered in one reply

An offshore question that reads "How should the rounding work?" costs a full day and produces
"Please use standard rounding", which costs another day. This costs one:

> **Q (blocks PRJ.4.2 from 2026/04/18):** For order totals, should tax be rounded per line
> item or on the invoice total?
> **Option A** — per line item. Matches the legacy system. May differ from the client's ERP by
> up to 0.02 per invoice.
> **Option B** — on the total. Matches the ERP. Differs from historical invoices.
> **We recommend B**, because reconciliation with the ERP is a stated objective (BR-FIN-003).
> **Reply with A or B.** If we do not hear by 2026/04/17 we will proceed with B and record it
> as ASM-021.

Context, options, recommendation, consequence, deadline, and a default. The default is what
keeps the project moving; the record is what keeps it honest.

---

## Exit criteria

- [ ] Stakeholder register complete, with concerns and current stance (SE-01)
- [ ] Engagement approach matched to influence × impact (SE-02)
- [ ] Every recurring communication names the decision it serves (SE-03)
- [ ] Every recurring meeting has a purpose, a quorum and stated outputs (SE-05)
- [ ] Escalation path published, with SLAs, and known to the team (DA-05)
- [ ] Minutes practice agreed: within one working day, silence-is-acceptance deadline
- [ ] For offshore engagements: overlap window, question format and demo cadence agreed
