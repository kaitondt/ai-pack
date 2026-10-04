---
name: mig-test-automation
description: "Convert manual test cases into automated scripts following the repository's existing conventions — spec/page-object/data/fixture layout, no hardcoded business data, data-driven values for transactional search, per-surface variants, locator strategy and debugging. Load for ALL test script generation tasks."
---

# Test Automation — manual cases to scripts

> Prerequisite: `mig-project` resolved; the manual cases exist and have passed review.
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
- the data-access client and repositories, when the target screens search transactional data

The conventions in the repository outrank the conventions in this skill. Where they
conflict, follow the repository and note the divergence.

---

## Step 2 — Choose the path

| Path | When | Cost |
|---|---|---|
| Quick | display verification, light interaction | low |
| Standard | CRUD, auth, multi-step workflows | medium |
| Data-driven | any search or list over **transactional** data | higher, and mandatory |

---

## Step 3 — Layer the code

| Layer | Holds | Never holds |
|---|---|---|
| Spec | test structure, business assertions, steps | locators, raw DOM actions, business data |
| Page object | locators declared together, behaviour-named methods, page-level assertions | business assertions, test data |
| Data | every input and expected value, typed and named | logic |
| Fixture | shared setup and teardown | assertions |

**Naming follows the manual cases.** A spec file maps to the flow number in the test case
document, not to an independent numbering. When the two diverge, tracing a failure back to
its case becomes manual archaeology — and that tracing is exactly what you need on the
morning a regression appears.

- consecutive small flows may share one file, named for the range it covers
- a second variant of an existing flow gets a suffix; the original is left untouched
- a spec matching no flow (shared setup, for instance) gets a descriptive name, not a number

---

## Step 4 — The data rule that matters most

**Never hardcode transactional data.** Dates, document numbers, lot numbers and product
codes drift between environments and over time. A script asserting a hardcoded document
number passes on the machine it was written on and fails everywhere else — and the failure
looks like a product defect.

Instead, for search and list screens over transactional data:

- read one real record at suite setup, and derive both the search input and the expected
  assertion from it
- make the read deterministic: a single top row under an explicit, stable ordering
- parameterise the query; never build it by string concatenation
- put new data-reading methods in their own module rather than editing the repository
  file that master-data lookups already depend on

Master data (fixed code lists, roles) may be hardcoded — it is stable by definition. State
which category a value falls into when it is not obvious.

---

## Step 5 — Surfaces

One variant per entry in `{{profile.target.surfaces}}`. They differ in viewport, base URL,
input mechanism and available controls, and a script written for one will fail silently on
the other — passing because it never found the element it was supposed to assert on.

Never let a single spec straddle two surfaces. If a flow crosses surfaces, that is an
integration scenario with an explicit hand-off, not one script with two viewports.

---

## Step 6 — Locators and stability

- prefer stable, semantic locators; avoid position- and text-only selectors that a
  translation will break
- when a locator breaks, fix the locator strategy — do not add a wait and hope
- waits are on state, never on elapsed time
- each test sets up and tears down its own state; no test depends on another's leftovers
- a flaky test is a defect in the test until proven otherwise, and it is quarantined with a
  reason, not retried into green

---

## Step 7 — Verify and report

Run the generated tests. Report real output.

```
Automation — {module or flow}
  Cases automated  : {n}/{n manual}   not automatable: {n} ({why})
  Files            : specs {n}, page objects {n}, data {n}
  Data-driven      : {n} searches read from real records
  Run              : {passed}/{total}   flaky {n}
  Traceability     : every spec names its TC ID: {yes|no}
```

Every generated test names the manual TC ID it implements — in the test title or a tag.
Without it, coverage cannot be reconciled and a failing test cannot be triaged.
