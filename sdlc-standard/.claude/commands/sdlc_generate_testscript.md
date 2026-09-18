---
description: "Convert reviewed manual test cases into automated scripts following the repository's existing conventions. Usage: /sdlc_generate_testscript <MODULE | FLOW> [level]"
---

# Generate automated test scripts

## Step 1 — Load

`sdlc_project`, then `sdlc_test_automation`.

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

Delegate to `sdlc_test_automator`, one call per module or flow.

- layer the code: spec / page object / data / fixture
- never hardcode transactional data — create it or read it deterministically
- one variant per surface; never straddle two in one spec
- every test names the manual TC ID it implements

## Step 6 — Run and report

Run the generated tests. Report real output.

```
Automation — {target}
  Cases automated  : {n}/{n manual}   not automatable: {n} ({why})
  Files            : specs {n}, page objects {n}, data {n}, fixtures {n}
  Data-driven      : {n} of {n} searches
  Run              : {passed}/{total}   flaky {n} (quarantined {n})
  Traceability     : every spec names its TC ID: {yes|no}
  Repository divergences noted : {list}
```

Failures go to `/sdlc_triage_defects` — do not classify them here, and never retry a flaky
test into green.
