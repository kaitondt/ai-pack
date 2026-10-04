---
name: sdlc-test-automation
description: "Convert manual test cases into automated scripts following the repository's existing conventions — spec/page-object/data/fixture layout, no hardcoded transactional data, per-surface variants, locator strategy, CI integration and flake policy. Load for ALL test script generation tasks."
---

# Test Automation — manual cases to scripts

> Prerequisite: `sdlc-project` resolved; the manual cases exist and have passed review.
> Framework and layout from `{{profile.testing.automation}}`.

Automation encodes cases that already exist. It is not a second place to decide what to
test — a script asserting something no manual case asserts is untraceable coverage, and it
will be deleted by whoever cannot explain it.

---

## Step 1 — Read the repository before writing

Never generate against an imagined structure. Read, from
`{{profile.testing.automation.layout}}`:

- existing specs — how tests are structured, named and grouped
- existing page objects — the locator strategy actually in use
- existing data files — where values live
- existing fixtures — what setup is already provided
- the config — path aliases, base URLs, viewports, projects
- the data-access client, when the target screens search transactional data

The conventions in the repository outrank the conventions in this skill. Where they
conflict, follow the repository and note the divergence.

---

## Step 2 — Decide what to automate, and in what order

Automate in this order, because it is the order of payback:

| Priority | What | Why |
|---|---|---|
| 1 | Regression scenarios that run every release | the recurring cost automation removes |
| 2 | Data-heavy validation cases (VP-03b, VP-10) | tedious and error-prone by hand |
| 3 | Happy-path flows across modules | the smoke suite the release gate needs |
| 4 | Failure and dependency cases (VP-06) | valuable, but needs fault injection to be honest |
| — | Layout and rendering judgement (VP-09) | usually cheaper to keep manual, or as visual snapshots |

A case marked `Automatable: No` in the design stays manual, and the reason is recorded.
Automating it badly is worse than not automating it: a test that passes without checking
what the case checks converts coverage into false confidence.

---

## Step 3 — Layer the code

| Layer | Holds | Never holds |
|---|---|---|
| Spec | test structure, business assertions, steps | locators, raw DOM actions, business data |
| Page object | locators declared together, behaviour-named methods, page-level assertions | business assertions, test data |
| Data | every input and expected value, typed and named | logic |
| Fixture | shared setup and teardown | assertions |

**Naming follows the manual cases.** A spec file maps to the flow or module id in the test
case document, not to an independent numbering. When the two diverge, tracing a failure
back to its case becomes manual archaeology — and that tracing is exactly what is needed on
the morning a regression appears.

---

## Step 4 — The data rule that matters most

**Never hardcode transactional data.** Dates, document numbers, lot numbers and reference
codes drift between environments and over time. A script asserting a hardcoded document
number passes on the machine it was written on and fails everywhere else — and the failure
looks like a product defect.

Instead, for search and list screens over transactional data:

- create the record the test needs in setup, or read one real record deterministically
- derive both the search input and the expected assertion from that record
- make any read deterministic: a single top row under an explicit, stable ordering
- parameterise queries; never build them by string concatenation
- clean up what the test created, in teardown

Master data (fixed code lists, roles) may be hardcoded — it is stable by definition. State
which category a value falls into when it is not obvious.

---

## Step 5 — Surfaces

One variant per entry in `{{profile.system.surfaces}}`. They differ in viewport, base URL,
input mechanism and available controls, and a script written for one will fail silently on
the other — passing because it never found the element it was supposed to assert on.

Never let a single spec straddle two surfaces. If a flow crosses surfaces, that is an
integration scenario with an explicit hand-off, not one script with two viewports.

---

## Step 6 — Locators and stability

- Prefer stable, semantic locators. Add explicit test identifiers to the application where
  needed — that is a legitimate, reviewable code change, not a hack.
- Avoid position-based and text-only selectors: a translation or a reorder breaks them.
- When a locator breaks, fix the locator strategy — do not add a wait and hope.
- Waits are on state, never on elapsed time.
- Each test sets up and tears down its own state; no test depends on another's leftovers.

**Flake policy.** A flaky test is a defect in the test until proven otherwise. Quarantine
it with a reason and an owner, and fix it within a stated window. Never retry it into
green: a suite with retries hides the one real intermittent product defect among the noise,
and that defect is always the expensive one.

---

## Step 7 — CI integration

- The suite runs on every merge to the integration branch, and before every release build.
- Split by duration: a fast smoke suite gates merges; the full suite runs on a schedule.
- A red suite blocks the release. A suite that is "usually red" has stopped being a gate —
  fix it or delete it, but do not keep it as decoration.
- Results are published in `{{profile.testing.automation.results_format}}` and kept per
  build, so a regression can be traced to the change that introduced it.

---

## Step 8 — Verify and report

Run the generated tests. Report real output.

```
Automation — {module or flow}
  Cases automated  : {n}/{n manual}   not automatable: {n} ({why})
  Files            : specs {n}, page objects {n}, data {n}
  Data-driven      : {n} searches derived from created or read records
  Run              : {passed}/{total}   flaky {n} (quarantined {n})
  Traceability     : every spec names its TC ID: {yes|no}
```

Every generated test names the manual TC ID it implements — in the test title or a tag.
Without it, coverage cannot be reconciled and a failing test cannot be triaged.
