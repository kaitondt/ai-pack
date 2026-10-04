---
description: "Run a process/quality audit: sample artifacts against the defined process, record non-conformances with evidence, open corrective actions, and check the effectiveness of previous ones. Usage: /pm-audit [scope]"
---

# Process audit

QA, not QC (PR-04): this examines whether the project is working the way it agreed to, not
whether a particular artifact is correct.

## Step 1 — Load

`pm-project`, then `pm-process`. Agent: `pm-quality-manager`.

The auditor must not be the person whose work is being audited (PR-04). Say who performed it.

## Step 2 — Sample artifacts, not opinions (PR-06)

| Check | Sample |
|---|---|
| Are reviews happening? | review records in documents; review density against target |
| Are exit criteria applied? | gate records; artifacts that passed with open Criticals |
| Is traceability maintained? | the RTM against the artifacts actually on disk |
| Are tests run and recorded? | results from a named run and build, not a summary |
| Is change control followed? | baselined documents modified with no CR (the hook log helps) |
| Are defects classified honestly? | severity distribution; any re-classification history |
| Is the tailoring record current? | observed practice against the recorded process |
| Is effort booked properly? | timesheets against WBS codes, not to "project" |
| Are the registers live? | last-updated dates; risks with no review in two cycles |

Sample by evidence, and say what was sampled and how much. "Reviewed the process with the
team" is not an audit.

## Step 3 — Record non-conformances

Each: what was observed, the evidence, which process element it violates, severity, owner and
due date. Then open a `CAPA-*` for anything above minor.

An audit that finds nothing, repeatedly, is sampling the wrong things (PR-06). Real projects
deviate; the question is whether the deviation is known and accepted.

## Step 4 — Check previous corrective actions (PR-07)

For every CAPA past its effectiveness-check date: did the non-conformance recur? If it did,
the root cause was wrong — re-analyse rather than re-issuing the same action.

## Step 5 — Report

```
Audit — {scope}, {date}, performed by {name}
  Sampled        : {what, how many, from where}
  Conformant     : {n} checks
  Non-conformant : {n}
    {CAPA-id} {what was observed} — evidence {ref} — violates {process element}
              severity {…} owner {…} due {…}
  Previous CAPAs : {n} due, {n} effective, {n} recurred — {ids}
  Trend          : {compared with the last audit}
  Systemic       : {any pattern across findings — usually more valuable than the findings}
```

Where a finding points at a missing check rather than a lapse, route it to
`/pm-refine-skill`. That is how an audit improves the process instead of only policing it.
