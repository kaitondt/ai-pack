---
name: sdlc-test-review
description: "Review test case documents in two separate modes — format (strip non-test content, normalise structure) and coverage (UI/UX/logic completeness against the specification and mockups). Load for ALL test case review tasks."
---

# Test Case Review

> Prerequisite: `sdlc-project` resolved. Load `sdlc-test-design` for the rules being
> checked.

Two modes, deliberately separate. Running them together produces a report where structural
noise buries the coverage findings, and the coverage findings are the ones that matter.

| Mode | Question | Output |
|---|---|---|
| **Format** | is this document clean and executable? | the file, edited |
| **Coverage** | does it test the right things? | a review report |

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
| Message text and labels | quoted exactly as the UI shows them (TR-L01) |

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

The level's basis document (`{{profile.testing.levels}}`): the detail design for UT, the
basic design for IT, the SRS for ST and UAT — plus the data design and the UI mockup where
one exists. Reviewing test cases against the test cases is circular; the review has to
re-derive from the sources.

### Three groups, checked separately

**UI** — every field, label, control, column and dialog on the screen appears in some case.
Missing controls are the most common gap, because case writers work from the function
design and the function design does not list every label.

**UX** — the behaviours a user experiences: focus order, default values, what is enabled in
which mode, the five screen states (SD-A01), confirmation and success feedback, where the
user lands after each action, and what survives a back navigation.

**Logic** — every rule and error in the function design, every calculation with its
rounding, every state transition, every permission partition, and the hazards in
`sdlc-test-design` §7.

### The level-boundary check

Also verify the case set sits at the right level (`sdlc-test-it` §boundaries):

- a UT case in an IT file — move it down
- an IT case in an ST file — move it down
- an ST-only concern (load, failover, operability) in an IT file — move it up

Cases at the wrong level are how a project ends up with high case counts and low coverage:
the same validation is tested three times and the month-end process is tested never.

### Gaps and contradictions

Two finding kinds, reported separately:

| Kind | Meaning |
|---|---|
| Gap | something in the sources has no case |
| Contradiction | two sources disagree, and the cases silently picked one |

A contradiction is the more valuable finding. It means the test set has encoded an
assumption nobody approved — and per RS-05 the resolution is to ask, not to pick.

### Expectation sourcing check

For a sample of cases with business values in the expected result, verify the value traces
to the specification (TR-AN01). An expected result matching the current implementation with
no anchor is the failure mode this check exists for, and it is invisible from the document
alone — you have to follow the anchor.

### Report

Write to `{{profile.paths.reviews}}`, one file per reviewed document. Findings carry the
source that proves them: a gap cites the design item with no case; a contradiction cites
both sources.

```
Test review — {file}
  Mode          : {format|coverage}
  Level         : {UT|IT|ST|UAT}   basis: {document}
  Format        : {n} blocks removed ({by category}), {n} kept as ambiguous
  Coverage
    UI gaps     : {n}   {list}
    UX gaps     : {n}   {list}
    Logic gaps  : {n}   {list}
    Contradictions : {n}   {list, with both sources}
  Level boundary : {n} cases at the wrong level {list}
  Unanchored expectations : {n}/{sampled}   ← TR-AN01
  Viewpoints missing entirely : {list}      ← T-09
  Duplicate partitions        : {n}         ← TR-DD01
  Verdict : {PASS|FAIL}
```

Do not mark a check passed that you could not perform — say what you could not verify and
what would be needed, as in `sdlc-review-framework`.
