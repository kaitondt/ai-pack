---
name: pm_reporting
description: "Progress and status reporting — daily, weekly, monthly and quarterly reports, the quality report, status data collection from evidence, RAG determination, variance narrative, dashboards and meeting minutes. Load for ALL reporting, status-collection, RAG, dashboard and minutes tasks."
---

# Reporting (Daily · Weekly · Monthly · Quarterly · Quality)

> Prerequisite: `pm_project` loaded. Rules in `references/rules/pm/reporting-integrity.md`.

A report exists so someone can make a decision. Everything in it that does not serve a
decision is cost — the writer's time, the reader's attention, and the credibility spent when
the important line is buried among the unimportant ones.

Cadences, audiences and contents come from `{{profile.reporting.cadences}}`.

---

## Step 0 — Collect before writing (RI-02)

Never assemble a report from memory or from the previous report's numbers. Collect from
`{{profile.reporting.data_sources}}` into `{{profile.paths.status_data}}` first:

| Data | From | Used for |
|---|---|---|
| Work package status | task tracker / schedule working file | progress, EV |
| Effort actuals | timesheets | AC, CPI, utilisation |
| Defects | defect tracker | quality, containment, S-curve |
| Test execution | test results | test progress, pass rate |
| Build / deploy | CI | build health, release readiness |
| Risks and issues | registers | exposure, ageing |
| Change requests | change register | scope movement, baseline impact |
| Decisions and actions | decision and action logs | blockers, ageing |

Each collected figure carries its as-of date and its source. Anything not collectable this
period is recorded as **not collected**, with why — that is a legitimate status, and it is
frequently the most informative line in the report.

---

## RG-01 — The four questions, in order (RI-01)

Every report, at every cadence, answers:

1. Where are we against the baseline?
2. What is off, by how much, and is it recoverable?
3. What decision or action is needed, from whom, by when?
4. What changed since last time?

If a section serves none of the four, it is padding. Length is not evidence of control, and
the person who most needs the report has the least time to read it.

---

## The five reports

### Daily — for the delivery team

Audience `{{profile.reporting.cadences}}` daily. One screen, no more.

```
{date}
  Done yesterday   : {work packages advanced, by code}
  Planned today    : {work packages}
  Blockers         : {what, owner, age in days, what it stops}
  Defects          : {new / fixed / open by severity}
```

No metrics, no forecast, no narrative. Its only job is to surface blockers within a day of
their appearing. A blocker aged three days on a daily report is a process failure, not a
status.

### Weekly — for the client PM and delivery manager

The workhorse. It keeps the plan on track and creates the paper trail.

```
Week {n} ({from} – {to})          Overall: {G|A|R} — {one sentence why}

1. Progress vs plan
   Milestone {M}   : {on track | at risk | slipped {n}d}   {next checkpoint}
   SPI {x.xx}  CPI {x.xx}   Completed {n}/{m} work packages this week
   Critical path   : {current chain}, {changed | unchanged}   Buffer used {x}%

2. Completed this week / planned next week
   {work package codes and names, not activity narrative}

3. Risks and issues (top 5 by exposure)
   {ID} {title}  exposure {n}  owner {name}  action {what, by when}

4. Decisions needed from the client
   {what}  needed by {date}  blocks {what}  asked on {date}

5. Change requests
   {CR-nnn} {status} {effort} {schedule impact}

6. Quality snapshot
   Defects open by severity, found/fixed this week, test progress by level

7. Resources
   {changes, absences, onboarding, allocation issues}
```

Section 4 is the section clients actually act on, and the one most often written too
politely to be actionable. "Awaiting client feedback" states nothing; "Decision on the
rounding rule (DEC-021) needed by 2026/04/18, or work package PRJ.4.2 stops on 2026/04/19"
states a consequence with a date, and it is what gets the decision made.

### Monthly — for the sponsor and steering committee

Decision-oriented, one to three pages of substance.

```
Month {m}                          Overall: {G|A|R}   Trend: {improving|stable|worsening}

1. Executive summary — 3-5 sentences: position, the one thing that matters, what is needed
2. Earned value      — SPI, CPI, EAC, VAC, TCPI, with the reading and the forecast reasoning
3. Milestones        — each with status, baseline date, forecast date, variance
4. Deliverables      — produced, accepted, pending acceptance
5. Quality           — the quality report's summary; the trend, not just the snapshot
6. Risk profile      — what entered, what closed, what changed exposure; contingency burn
7. Change requests   — approved this month and their cumulative baseline impact
8. Resources         — utilisation, gaps, key-person risk
9. Decisions needed  — with by-dates and consequences
10. Forecast         — completion date and cost, with the assumptions behind them
```

Section 7 deserves a cumulative line, not just the month's: *"14 CRs approved to date,
+186 hours and +6 days against the original baseline."* Individually every change was
reasonable; the cumulative number is what the steering committee is actually deciding about,
and it is invisible unless someone adds it up.

### Quarterly — for the sponsor and the business

Not a longer monthly. The question is whether the **business case still holds**.

```
Quarter {q}
1. Objective attainment — each charter objective, its metric, current vs target (CH-02)
2. Financial performance — budget vs actual vs forecast; reserve position; billing status
3. Baseline history     — every re-baseline, with the variance at reset and the reason (PB-06)
4. Risk outlook         — the profile ahead, not the log behind
5. Process and quality trend — quarter over quarter, with what changed
6. Lessons applied      — what was learned and what changed as a result
7. Next quarter         — plan, decisions required, resources required
```

Section 1 is why this report exists. A project can be green on schedule and cost while its
business case has evaporated — the market moved, the regulation changed, the sponsoring
department reorganised. Nobody else is checking, and the earlier it is said, the more of the
budget survives.

### Quality report — for the QA lead and the client

See `pm_quality` for the metric definitions. Structure:

```
Quality — {period}
1. Review effectiveness — density and finding distribution vs target
2. Defect profile       — density by phase and module; inflow vs outflow
3. Phase containment    — the injected × found matrix
4. Test progress        — planned/executed/passed per level; blocked cases
5. Coverage             — line and branch, from a named run and build
6. Escaped defects      — count, and the check that should have caught each one
7. Audit and CAPA       — findings, open corrective actions, effectiveness checks
8. What this predicts   — the section that makes the report worth producing
```

---

## RG-02 — Determine RAG from the numbers, then explain it (RI-04)

```
IF   any payment milestone at risk, OR SPI < 0.90, OR buffer consumed, OR
     an unrecoverable variance exists                                    → RED
ELIF a decision or action is required to stay on plan, OR SPI 0.90-0.95  → AMBER
ELSE                                                                     → GREEN
```

Thresholds from `{{profile.schedule.variance_thresholds}}` and
`{{profile.reporting.rag_definitions}}`.

Then write the one sentence that explains it. "Amber: the interface specification is 6 days
late; PRJ.4.3 starts 2026/04/22 or M2 moves" is a status. "Amber: some delays" is not.

Never report green over a red section (RI-04). A project that jumps green → red in one
period was mis-reported for weeks, and the Amber period it skipped was exactly when a
decision would have been cheap.

## RG-03 — Write the variance narrative in cause–impact–action form

```
{what varied}: {by how much} — {cause, specific} — {impact on milestone/cost/quality} —
{action, owner, by when} — {residual risk}
```

"Behind schedule due to unforeseen complexity" is not a cause; it is a way of not naming
one. Causes are specific and often uncomfortable: a late input from the client, an
underestimated package, an absent reviewer, an environment that was not ready, a decision
that took three weeks.

Uncomfortable is fine. Unnamed is not — an unnamed cause cannot be acted on, and it will
recur next month.

## RG-04 — Meeting minutes are a decision record

`{{profile.reporting.meeting_minutes}}`, id `MTG-{YYYYMMDD}-{NN}`:

attendees (and absent invitees) · agenda · **decisions** as `DEC-*` with owners ·
**actions** as `ACT-*` with owner and due date · items deferred, with when they return ·
disagreements recorded as such, not smoothed over.

Circulate within one working day, and state that silence by a named date is acceptance
(DA-04). Minutes that arrive a week later are archaeology; nobody can correct a record they
no longer remember.

Discussion narrative is not the point. Six months later, the only lines that matter are the
decisions and the actions.

## RG-05 — Distribution is deliberate

`{{profile.reporting.distribution_list}}`. Consider what each recipient can act on. A
sponsor receiving weekly operational detail stops reading, and then misses the month the
report says something important.

Never send a client-facing report containing internal cost margin, individual performance
commentary, or unresolved internal disagreement. Prepare the internal and external versions
separately when they differ — and keep both, so the record shows what was said to whom.

---

## Output check before sending

- [ ] Every number has a source and an as-of date (RI-02)
- [ ] Nothing carried forward from the last report unchanged without verification
- [ ] RAG computed from thresholds, explained in one sentence (RG-02)
- [ ] Every variance has a specific cause, an impact and an action with an owner and date
- [ ] Every decision request has a by-date and a stated consequence
- [ ] Actions carry age; anything past two escalation SLAs is escalated, not just listed
- [ ] Nothing in it that serves no decision (RI-06)
- [ ] Anything not collected is stated as not collected, with why
