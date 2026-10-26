---
description: "Convert reviewed manual test cases into automated scripts following the repository's existing conventions, one variant per surface, with data-driven values for transactional search. Usage: /mig-generate-testscript <MODULE or FLOW> [--surface PC|HH]"
---

# Generate test scripts

## Step 1 — Load

`mig-project`, `mig-test-design`, then `mig-test-automation`.

## Step 2 — Pre-check

The manual cases must exist and have passed `/mig-review-testcase`. Automating unreviewed
cases encodes their gaps into code, where they are far more expensive to correct.

Resolve the surface from the module id suffix against `{{profile.target.surfaces}}`. A
module whose surface has no automation layout configured → stop and ask.

## Step 3 — Read the repository first

Read the existing specs, page objects, data files, fixtures, config and data-access
modules named in `{{profile.testing.automation.layout}}`. Report what conventions you
found before generating anything.

Repository conventions outrank the skill. Where they differ, follow the repository and say
where it diverges — a project that has settled on a pattern does not want a second one.

## Step 4 — Generate

Layered per `mig-test-automation`: business assertions in specs, locators in page objects,
every value in data files. Spec file names follow the manual flow numbering.

Transactional search data is read from a real record at setup — never hardcoded. Master
data may be hardcoded.

One case, one test: every generated test names exactly one manual TC ID. Nothing the skill's
Step 7 forbids — no mocked system under test, no silent skip, every expected result asserted,
including the persisted state when the case changes data.

When the cases already have scripts and only some changed, generate for the changed TC IDs
only (skill Step 10) and leave the rest untouched.

## Step 5 — Reconcile, run and report

Count the tests with `{{profile.testing.automation.list_command}}` — never with grep — and
reconcile them one-to-one against the cases (skill Step 8). Then run them and report the real
output.

```
Test scripts — {module or flow} · surface {id}
  Manual cases     : {n}   automated {n}   not automatable {n} ({why})
  Files written    : specs {n} · page objects {n} · data {n} · fixtures {n}
  Data-driven      : {n} searches read from real records
  Reconciliation   : runner lists {n} · matched {n} · case without test {n} ·
                     test without case {n} · duplicates {n}
  Run              : {passed}/{total}   failed {n}   skipped {n}   flaky {n}
  Convention notes : {divergences found in the repo}
```

Failing tests are reported failing, with their output. Do not adjust an assertion to make a
test pass — a test that fails against real behaviour is either a defect or a wrong case,
and both go to `/mig-triage-failures`.
