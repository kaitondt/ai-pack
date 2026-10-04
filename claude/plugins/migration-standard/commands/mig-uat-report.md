---
description: "P7 phase 3 — write the UAT bug report to the configured report directory, in the five-section format, appending a new round to an existing report rather than overwriting it. Usage: /mig-uat-report [BUG-ID] [existing report path]"
---

# P7.3 — Write the UAT bug report

## Step 1 — Load

`mig-project`, then `mig-uat-bug`.

## Step 2 — Get the bug id

The bug id comes from the user's bug list (C4). Never invent one, never derive it from the
module id, never number it from the count of files already in the report directory.

Not in context → ask:
> "Which bug id from the bug list should this report be filed under (e.g. UAT-001)?"

Normalise the case, keep the number exactly as given.

## Step 3 — Determine the file

`{{profile.paths.uat_reports}}/{BUG-ID}_{MODULE}_{short-slug}.md`

**Existing file → append a new investigation round.** Never overwrite. The record of what
was tried and rejected is what stops the next round repeating it.

## Step 4 — Write, in the language bound to that path

Five sections: Summary · Root cause · Solution · Verification · Follow-up.

- **Root cause** carries the anchors from the investigation: target `file:line`, design
  document id and section, legacy `file:line`.
- **Verification** contains real output from runs that actually happened. A test that was
  not run is written as not run. A failing test is written as failing, with its output
  (C6).
- **Follow-up** names the regression test and any sibling modules sharing the pattern.

## Step 5 — Report

```
UAT report — {BUG-ID}
  File   : {path}   ({created|round {n} appended})
  Language : {lang}
  Sections : 5/5
  Verification entries : {n} real runs
```
