---
description: "Assess a change request without changing anything: classify defect vs clarification vs change, assess impact across every baseline dimension, estimate the full cascade, and present options with a recommendation for the approving authority. Usage: /pm-change-assess <CR text, id, or file>"
---

# Assess a change request

Phases 1–2 of integrated change control. **Nothing is changed by this command** — no
documents, no code, no baselines.

## Step 1 — Load

`pm-project`, then `pm-change-control`. Agent: `pm-change-analyst`.

## Step 2 — Log it (IC-01)

Register it in `{{profile.change_control.register}}` with the next `{{profile.change_control.id_format}}`:
what was asked, by whom, when, why, urgency claimed, and source.

Log it even if it is trivially small. Ten absorbed four-hour changes is a week nobody can
account for, precisely because nothing recorded them (PB-07).

## Step 3 — Determine what it actually is (IC-02)

| It is | When | Who pays |
|---|---|---|
| **Defect** | delivered behaviour contradicts a baselined document | vendor |
| **Clarification** | the document is silent or genuinely ambiguous | per contract |
| **Change** | it contradicts or extends a baselined document | decided by the authority |

Quote the **exact text** of the baselined document, with its version and section. Make the
determination **before** any fix, never after — after the work is done, the argument is about
money already spent.

Classify into `{{profile.change_control.classes}}`.

## Step 4 — Build the impact matrix (IC-04)

Every dimension in `{{profile.change_control.impact_dimensions}}`, including the ones that
come back "none". The two most often skipped are **documentation** (the full cascade, not just
the obvious document) and **test** (previously passed cases now invalid and needing re-run).

When a technical pack is installed, use its context-mapping command
(`/sdlc-context-map`, `/mig-context-map`) to enumerate the affected files rather than guessing.

## Step 5 — Estimate the whole cascade (IC-07, EM-08)

Analysis · every affected design document · code · unit tests new and modified · integration
and regression · test case updates · documentation · release · re-verification · translation ·
the management overhead of the change itself.

Then state **schedule impact separately from effort impact** (IC-05): 40 hours is a two-week
delay on the critical path and no delay off it, and the client is deciding about the delay.
Note float consumed — absorbing into float is free once, and the report should say so before
the second change arrives.

## Step 6 — Options (IC-06)

At least `{{profile.change_control.min_options}}`, each with effort, schedule, cost, risk and
what it costs the client operationally. Then a recommendation with a reason.

## Step 7 — Route to the authority (IC-08)

Determine from `{{profile.change_control.authority}}` who decides at this impact level, and
say so explicitly in the output. **Stop here.** Approval is a separate step; work does not
start before it.

## Report

```
CR-{nnn} — {title}                                   ASSESSED, awaiting decision
  Source        : {who, when}   Urgency claimed: {what}
  Determination : {defect | clarification | change} — per {doc} v{ver} §{sec}: "{quote}"
  Class         : {class}
  Impact:
    scope       : {requirements, deliverables, work packages}
    effort      : {h}       schedule: {d} ({critical path | float, n days remaining})
    cost        : {amount}  from {control account}
    quality     : {test cases new/changed, regression scope, targets affected}
    risk        : {new RSK ids, changed exposures}
    resource    : {who, availability, what it displaces}
    contract    : {deliverables, milestones, acceptance criteria, SLA}
    dependencies / test / documentation : {…}
  Options       : {n} — {summary of each}
  Recommend     : {option}, because {reason}
  Decides       : {authority per profile}   by {date needed}
```
