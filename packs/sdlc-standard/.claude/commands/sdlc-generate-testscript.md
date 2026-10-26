---
description: "Convert reviewed manual test cases into automated scripts following the repository's existing conventions. Usage: /sdlc-generate-testscript <MODULE | FLOW> [level]"
---

# Generate automated test scripts

## Step 1 — Load

`sdlc-project`, then `sdlc-test-automation`.

## Step 2 — Pre-check

Required: manual cases that exist and have **passed review**. Automating unreviewed cases
encodes their defects, and a wrong assertion in a script is harder to spot than a wrong
assertion in a document — it passes.

Also required: `{{profile.testing.automation.framework}}` set, and the automation repository
present.

## Step 3 — Read the repository first

Read the existing specs, page objects, data files, fixtures and config before writing
anything. The conventions in the repository outrank the conventions in the skill; where
they conflict, follow the repository and note the divergence.

## Step 4 — Select what to automate

Per the priority order in the skill. Cases marked `Automatable: No` stay manual, with the
reason recorded. Do not automate a case by weakening its assertion — a test that passes
without checking what the case checks converts coverage into false confidence.

## Step 5 — Generate

Delegate to `sdlc-test-automator`, one call per module or flow.

- layer the code: spec / page object / data / fixture
- never hardcode transactional data — create it or read it deterministically
- one variant per surface; never straddle two in one spec
- one case, one test: every test names exactly one manual TC ID
- nothing the skill's Step 7 forbids — no mocked system under test, no silent skip, every
  expected result asserted, including the persisted state when the case changes data

When the cases already have scripts and only some changed, generate for the changed TC IDs
only (skill Step 11) and leave the rest untouched.

## Step 6 — Reconcile, run and report

Count the tests with `{{profile.testing.automation.list_command}}` — never with grep — and
reconcile them one-to-one against the cases (skill Step 9). Then run them. Report real output.

```
Automation — {target}
  Cases automated  : {n}/{n manual}   not automatable: {n} ({why})
  Files            : specs {n}, page objects {n}, data {n}, fixtures {n}
  Data-driven      : {n} of {n} searches
  Reconciliation   : runner lists {n} · matched {n} · case without test {n} ·
                     test without case {n} · duplicates {n}
  Run              : {passed}/{total}   skipped {n}   flaky {n} (quarantined {n})
  Repository divergences noted : {list}
```

Failures go to `/sdlc-triage-defects` — do not classify them here, and never retry a flaky
test into green.
