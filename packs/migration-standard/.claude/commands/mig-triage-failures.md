---
description: "Classify a failing test run into product defect, script error, needs-review and infrastructure, grouped by root cause, with the fix named for script errors and anchors for product defects — plus, with bug-list, the client-facing bug list. Usage: /mig-triage-failures [run id or results path] [bug-list]"
---

# Triage a failing test run

## Step 1 — Load

`mig-project`, then `mig-defect-triage`.

## Step 2 — Identify the run

Resolve the run under `{{profile.testing.paths.results_root}}`. When several runs exist,
ask which one rather than assuming the newest — triage of the wrong run is worse than no
triage, because it looks authoritative.

State the run id and timestamp in the report. A triage without its run cannot be compared
against the next round, and that comparison is how convergence is measured.

Result formats keep every attempt (retries, re-runs, history). Collapse to one result per TC
ID — the last attempt of this run — before counting anything, and say so in the report.

## Step 3 — Apply the decision tree, in order

1. infrastructure signature → `INFRA`, stop, the run needs re-running
2. failed before reaching its assertion → `SCRIPT-ERROR` or `INFRA`, never a product defect
3. passes on re-run with no change → flaky → `SCRIPT-ERROR`, quarantine with a reason
4. actual behaviour matches design and legacy → the case is wrong → `SCRIPT-ERROR`
5. ambiguous (element not found, not visible, interaction timeout) → `NEEDS-REVIEW`

Order matters. Out of order, infrastructure failures land in the defect list and the report
stops being believed.

## Step 4 — Resolve the ambiguous ones

Open the screenshot or trace before classifying. "Element not found" has two opposite
causes and the log distinguishes neither. Where no evidence was captured, say so — that is
a gap in the automation setup to fix before the next round.

## Step 5 — Name the fix, anchor the defect

- `SCRIPT-ERROR` → read the page object, locator and data file, and name the file, line and
  fix. "Script error" with no fix hands the whole investigation back.
- `PRODUCT-DEFECT` → anchor the expected behaviour to the design document and, for parity
  questions, to the legacy source. Unanchored defects get disputed.

## Step 6 — Group by root cause

In a migrated system defects arrive in families: one locator pattern across twenty screens,
one rounding difference across every monetary field. Report the root cause with its
instance list, not twenty separate defects.

## Step 7 — Report

```
Triage — run {id}, {date}
  Total {n} · passed {n} · failed {n}
  PRODUCT-DEFECT {n} · SCRIPT-ERROR {n} · NEEDS-REVIEW {n} · INFRA {n}
  Root causes : {n} distinct behind {n} failures
  {per class: the grouped list with anchors or fixes}
  Blocked     : {tests not run because of INFRA}
```

Product defects go to `/mig-uat-investigate` for root cause before any fix.

## Step 8 — The bug list (only with `bug-list`)

After the report above, and only from its classification, write the client-facing bug list
per `mig-defect-triage` (*The client-facing bug list*): `PRODUCT-DEFECT` rows only, one bug
per root cause with its affected TC IDs, written in the deliverable language with the anchors
and the copied evidence, in the format of the `bug_list` template. Unresolved `NEEDS-REVIEW`
rows are listed as excluded, never guessed into the list.
