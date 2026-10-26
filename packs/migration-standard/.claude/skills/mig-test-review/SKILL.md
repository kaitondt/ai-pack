---
name: mig-test-review
description: "Review test case documents in two separate modes — format (strip non-test content, normalise structure) and coverage (UI/UX/logic completeness against the design, legacy and mockups) — and audit automated scripts against the cases in a third, script mode (one-to-one mapping, no mocked system under test, no silent skips, assertion completeness). Load for ALL test case and test script review tasks."
---

# Test Case Review

> Prerequisite: `mig-project` resolved. Load `mig-test-design` for the rules being checked.

Three modes, deliberately separate. Running them together produces a report where structural
noise buries the coverage findings, and the coverage findings are the ones that matter.

| Mode | Question | Output |
|---|---|---|
| **Format** | is this document clean and executable? | the file, edited |
| **Coverage** | does it test the right things? | a review report |
| **Script** | do the automated scripts test what the cases test? | a review report |

Format first: reviewing coverage on a document full of leftover working notes wastes the
expensive pass on the cheap problem.

---

## Mode 1 — Format

Test case files accumulate content that is not test content: working notes, quoted Q&A,
open-question markers, rule references, reviewer comments, uncertainty flags.

**Delete** anything that is not executable test content or required structure. It confuses
the tester, and worse, it leaks internal uncertainty into a document the client may read.

**Never touch:**

| Protected | Why |
|---|---|
| TC IDs | renumbering breaks results and traceability (TR-ID01) |
| Steps and expected results | this mode does not change meaning |
| Preconditions | same |
| Result columns | filled during execution, not by a reviewer |
| Message text and labels | verbatim by rule (NI-03) |

Method:
1. read the **whole** file first — a long file takes several reads, and editing before
   reading the end produces inconsistent results
2. classify each non-test block before deleting; when a block is genuinely ambiguous, keep
   it and list it in the report rather than guessing
3. apply edits precisely, not by rewriting the file
4. re-scan at least twice — the first pass reliably misses blocks that only became
   adjacent after earlier deletions
5. report what was removed, by category and count

**The rule that keeps this safe:** if removing a block would remove information a tester
needs, it was not a note — it was an under-formatted precondition. Reformat it, do not
delete it.

---

## Mode 2 — Coverage

### Sources to read before reviewing

The screen and function design, the interface design, the legacy screen and logic, the
data design, and the UI mockup or prototype where one exists. Reviewing test cases against
the test cases is circular; the review has to re-derive from the sources.

### Three groups, checked separately

**UI** — every field, label, control, column and dialog on the screen appears in some case.
Missing controls are the most common gap, because case writers work from the function
design and the function design does not list every label.

**UX** — the behaviours a user experiences: focus order, default values, what is enabled
in which mode, confirmation and success feedback, where the user lands after each action,
and what survives a back navigation.

**Logic** — every rule and error in the function design, every calculation with its
rounding, every state transition, every permission partition, and the migration hazards in
`mig-test-design` §6.

### Coverage gaps and internal contradictions

Two findings kinds, reported separately:

| Kind | Meaning |
|---|---|
| Gap | something in the sources has no case |
| Contradiction | two sources disagree, and the cases silently picked one |

A contradiction is the more valuable finding. It means the test set has encoded an
assumption nobody approved — and per `NI-05` the resolution is to ask, not to pick.

### Report

Write to `{{profile.paths.reviews}}`, one file per reviewed document. Findings carry the
source that proves them: a gap cites the design item with no case; a contradiction cites
both sources.

```
Test review — {file}
  Mode          : {format|coverage}
  Format        : {n} blocks removed ({by category}), {n} kept as ambiguous
  Coverage
    UI gaps     : {n}   {list}
    UX gaps     : {n}   {list}
    Logic gaps  : {n}   {list}
    Contradictions : {n}   {list, with both sources}
  Viewpoints missing entirely : {list}      ← T-06
  Duplicate partitions        : {n}         ← TR-DD01
  Verdict : {PASS|FAIL}
```

Do not mark a check passed that you could not perform — say what you could not verify and
what would be needed, as in `mig-review-framework`.

---

## Mode 3 — Script

Audits the **automated scripts** for a module or flow against the reviewed cases they
implement. Read-only: findings, not fixes. Run it before an automation suite is declared done,
when scripts were written by another session or agent, and after any bulk healing.

### Sources to read before reviewing

The reviewed case document, the specs, page objects, data files and fixtures for the target,
and the runner's own listing (`{{profile.testing.automation.list_command}}`). Never count or
map tests by reading the spec files alone.

### Checks

| # | Check | Severity when it fails |
|---|---|---|
| S-01 | **One-to-one.** Every automatable case has exactly one test; every test names exactly one existing TC ID | Critical for a case without a test or a test without a case; Warning for a duplicate |
| S-02 | **No mocked system under test** at IT/UAT level; every stub is outside the migration's scope and declared with a reason | Critical |
| S-03 | **No silent skip.** Every `skip` / `fixme` / disabled test carries a ticket and an owner | Critical when none |
| S-04 | **Assertion completeness.** Each expected result of the case has an assertion — screen state, verbatim MSG-ID text, navigation, and the persisted state when the case changes data | Critical for a missing expected result |
| S-05 | **Expected values from the case**, not from the target application: compare a sample of asserted values with the case and its legacy anchor | Critical |
| S-06 | **Data rule.** No hardcoded transactional search values; values read from a real record | Warning |
| S-07 | **Layering.** No locators or raw DOM actions in specs; no business assertions in page objects | Warning |
| S-08 | **Stability.** No waits on elapsed time; no test depending on another's state; no retry used to pass | Warning |
| S-09 | **Granularity.** Steps inside a test follow the case's steps closely enough that a failure names the step that failed | Suggestion |

S-04 and S-05 are the checks a passing suite hides. Sample at least one case per viewpoint
present, and follow each sampled assertion back to the case and the case back to its anchor.

### Report

```
Script review — {module or flow}
  Cases (automatable) : {n}   runner lists: {n} tests
  S-01 one-to-one     : matched {n} · case without test {n} · test without case {n} · duplicates {n}
  S-02 mocked SUT     : {n}   {file:line}
  S-03 silent skips   : {n}   {file:line}
  S-04 under-asserted : {n}   {TC ID — expected result not asserted}
  S-05 unsourced values : {n}/{sampled}
  S-06..S-09          : Warning {n} · Suggestion {n}
  Not verifiable      : {what, and what is needed}
  Verdict : {PASS|FAIL}
```

A Critical in S-01 to S-05 fails the review: the suite's pass rate cannot be reported as
coverage of the cases until it is fixed.
