---
description: "Produce the stakeholder register and communications plan: engagement approach by influence and impact, the communication matrix, meeting design, minutes practice and the escalation path. Usage: /pm-comm-plan"
---

# Stakeholder and communications plan

## Step 1 — Load

`pm-project`, then `pm-stakeholder`. Agent: `pm-planner`.

## Step 2 — Build the stakeholder register

Beyond `{{profile.governance}}`: everyone whose position affects the project. Per the skill's
fields, with the column that does the work — **concern** (SE-01).

Interest is what people say at kickoff; concern is what drives their behaviour in month four.
A stakeholder whose concern is unaddressed does not argue — they become unavailable, escalate
late, and find the deliverable unacceptable for reasons that surface at acceptance and turn
out to be old.

## Step 3 — Set the engagement approach (SE-02)

By influence × impact. Pay attention to the low-influence/high-impact quadrant — the people
whose daily work changes most, who have no formal authority, and who determine whether the
system is used or worked around.

## Step 4 — Build the communication matrix

One row per recurring communication: what · to whom · **which decision it serves** (SE-03) ·
format · frequency · owner · language. Derived from `{{profile.reporting.cadences}}` plus the
ad-hoc channels: escalation, decision requests, defect notifications, release announcements,
CR submissions.

Delete any row that serves no decision. Then ask the more useful question: which decisions are
being made repeatedly on poor information? That gap is a missing row.

## Step 5 — Design the meetings (SE-05)

Each recurring meeting: purpose, the decisions it makes, quorum, inputs circulated beforehand,
outputs. A meeting whose material could be an email should be one; a decision being made by
email over five days should be a meeting.

## Step 6 — Fix the minutes and escalation practice

Minutes within one working day, decisions as `DEC-*`, actions as `ACT-*` with owners and dates,
silence-by-a-named-date as acceptance (RG-04, DA-04).

Publish `{{profile.governance.escalation}}` with its SLAs, and make sure the team knows
escalation is a process step rather than an accusation (DA-05). A project where escalation
feels like failure is a project where issues age silently.

## Step 7 — Offshore adjustments (SE-07)

Where `{{profile.project.engagement_model}}` is offshore or hybrid: agree the daily overlap
window, the question format (context · options · recommendation · consequence · deadline ·
default — SE-08), and a demo cadence that makes progress visible rather than asserted.

Distributed teams' problems surface later than co-located ones, so the reporting discipline is
the only early-warning system available.

## Report

```
Communications plan — v{n}
  Stakeholders   : {n} registered, {n} with concerns recorded, {n} opposing or neutral
  Engagement     : {n} manage closely · {n} keep satisfied · {n} keep informed · {n} monitor
  Matrix         : {n} rows, all serving a named decision? {yes | which do not}
  Meetings       : {n} recurring, all with purpose + quorum + outputs? {yes|no}
  Escalation     : published? {yes|no}   SLAs {levels}
  Minutes        : within {n} working day(s), acceptance-by-silence deadline {n} days
  Offshore       : overlap window {…} · question format agreed {yes|no} · demo cadence {…}
```
