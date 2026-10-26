---
name: mig-test-automation
description: "Convert manual test cases into automated scripts following the repository's existing conventions — spec/page-object/data/fixture layout, no hardcoded business data, data-driven values for transactional search, per-surface variants, locator strategy, what a script may not do (mock the system under test, skip silently, under-assert), one-to-one TC reconciliation counted by the runner, fix-or-report healing and incremental sync when cases change. Load for ALL test script generation and maintenance tasks."
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

## Step 7 — What a script may not do

A script that does any of these passes without testing what its case tests. Each is a
Critical finding in `/mig-review-testcase script`.

- **Mock the system under test.** At IT and UAT level the target application, its API and its
  database are real. Only systems outside the migration's scope may be stubbed, each stub
  declared in the fixture with the reason. At UT level the unit's own collaborators may be
  mocked — never the unit.
- **Skip silently.** No `skip`, `fixme`, `xit`, `@Disabled` or commented-out test without a
  defect or ticket id and an owner in the reason. A skipped test is reported as not run, never
  as passed.
- **Assert less than the case.** Every expected result in the case is asserted — the screen
  state, the message text by MSG-ID, the navigation, **and the persisted state** when the case
  expects data to change. A case that says "the order is saved with status 2" is not covered by
  a test that checks for the success message. Read back through the API or the data-access
  client (`{{profile.testing.automation.layout.db_client}}`) and compare — the stored values
  are where parity with the legacy system is won or lost.
- **Change an expected value to make a test pass.** Expected values come from the case, which
  comes from the design and its legacy anchor. A mismatch is triaged (Step 9), never resolved
  by editing the expectation to what the target returned.
- **Depend on order or on another test.** Each test creates or reads what it needs and cleans
  up after.
- **Wait on time.** Waits are on state (Step 6).

One case, one test. A case with several expected results is still one test with several
assertions — or, where the framework supports it, one test with named steps. Merging several
cases into one test, or splitting one case into several tests, breaks the count in Step 8
and the result carry-forward between rounds (`mig-test-artifact-lifecycle`).

---

## Step 8 — Reconcile, verify and report

Every generated test names the manual TC ID it implements, where
`{{profile.testing.automation.tc_id_in}}` says (title prefix, tag or annotation) — exactly one
TC ID per test. Without it, coverage cannot be reconciled and a failing test cannot be
triaged.

**Count with the runner, never with grep.** Run `{{profile.testing.automation.list_command}}`
and extract the TC IDs from its output. A text search over the spec files miscounts in both
directions: it counts step blocks and helper calls as tests, and it misses every test
generated by a loop or a parameter table — which in a data-driven suite is most of them.

Then reconcile against the manual cases (the automatable ones):

| Bucket | Meaning | Action |
|---|---|---|
| matched | case has exactly one test | — |
| case without test | coverage gap | automate it, or record why it is not automatable |
| test without case | untraceable test | find its case, or delete it — automation does not decide what to test |
| duplicate | one TC ID in several tests, or several in one | split or merge until one-to-one |

Run the generated tests. Report real output.

```
Automation — {module or flow}
  Cases automated  : {n}/{n manual}   not automatable: {n} ({why})
  Files            : specs {n}, page objects {n}, data {n}
  Data-driven      : {n} searches read from real records
  Reconciliation   : runner lists {n} tests · matched {n} · case without test {n} ·
                     test without case {n} · duplicates {n}
  Run              : {passed}/{total}   skipped {n} (each with a ticket)   flaky {n}
  Persisted state  : {n}/{n} cases that change data assert it after the action
```

A reconciliation that is not one-to-one is reported as such, with the IDs — never rounded to
"all cases automated".

---

## Step 9 — When a script goes red: fix the test, or report the product

Classify **before** touching anything, with the decision tree in `mig-defect-triage`. Then
act by class:

| Root cause | Example | Action |
|---|---|---|
| Script defect | stale locator, wrong page object method, wait on time, data hardcoded and drifted | fix the script; name the file and line |
| Message text changed | the catalogue entry for a MSG-ID was corrected to the verbatim legacy string | update the data file from the **catalogue**, by MSG-ID — never copy the text from the screen |
| Environment or data | expired account, missing seed, service down, token not refreshed | fix the fixture or the environment; re-run; never edit an assertion |
| Product defect | expected value from the case is not what the target does | report it with the case's anchor (`/mig-triage-failures`); the test stays red |

Never make a red test green by weakening it: no added `skip`, no loosened assertion, no
broadened locator that now matches something else, no retry. A test healed into green over a
real parity defect is the most expensive line in the suite. Bound the healing: after three
attempts on the same test without a confirmed root cause, stop and report it as NEEDS-REVIEW.

---

## Step 10 — When the manual cases change

Test cases change between rounds — a review correction, a CR, or a reviewer's edit in the
delivered workbook imported back under `mig-document-io` DIO-10. Update the suite
**incrementally**:

1. Diff the cases by TC ID: added, changed (steps, data or expected result), removed.
2. Generate tests for the added IDs; regenerate only the changed IDs; delete the tests of the
   removed IDs. Tests whose case did not change are not touched — not even reformatted.
3. Re-run the reconciliation in Step 8 and report the diff with the result.

Regenerating the whole suite for a three-case change rewrites every hand-tuned locator and
fixture in it, and turns a reviewable diff into an unreviewable one.
