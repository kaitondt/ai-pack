---
description: "Review test case documents in format mode (clean the file) or coverage mode (check completeness against the level's basis document), or audit the automated scripts against the cases in script mode. Usage: /sdlc-review-testcase <format|coverage|script> <file or module>"
---

# Review test cases

## Step 1 — Load

`sdlc-project`, then `sdlc-test-review`, then `sdlc-test-design` for the rules being
checked, then the level skill for the basis document.

## Step 2 — Choose the mode

| Mode | Question | Output |
|---|---|---|
| `format` | is this document clean and executable? | the file, edited |
| `coverage` | does it test the right things? | a review report |
| `script` | do the automated scripts test what the cases test? | a review report |

**Format first.** Reviewing coverage on a document full of leftover working notes spends
the expensive pass on the cheap problem. **Script last**: auditing scripts against cases whose
coverage has not been reviewed checks them against a moving target.

No mode given → ask; the modes do different work and produce different artifacts.

## Step 3 — Format mode

Read the whole file before editing anything. Delete what is not executable test content or
required structure: working notes, quoted Q&A, open-question markers, rule references,
reviewer comments.

Never touch: TC IDs, steps, expected results, preconditions, result columns, quoted UI text.

Re-scan at least twice — the first pass reliably misses blocks that only became adjacent
after earlier deletions. When a block is genuinely ambiguous, keep it and list it.

## Step 4 — Coverage mode

Re-derive from the level's basis document (`{{profile.testing.levels}}`), the data design,
and the mockup where one exists. Reviewing test cases against the test cases is circular.

Check the three groups separately — UI, UX, Logic — plus:

- the level boundary: cases sitting at the wrong level, in either direction
- expectation sourcing: sample the business values and follow their anchors (TR-AN01)
- viewpoint completeness (T-09) and duplicate partitions (TR-DD01)

## Step 4b — Script mode

**Read-only.** Also load `sdlc-test-automation`. List the tests with
`{{profile.testing.automation.list_command}}` — never count them from the source — and map
them to the reviewed cases by TC ID. Then apply checks S-01..S-09 from the skill's Mode 3;
for S-04 and S-05, follow sampled assertions back to the case and the case to its anchor.
Report with the skill's Mode 3 format instead of the one below.

## Step 5 — Report

```
Test review — {file}
  Mode          : {format|coverage}
  Level         : {UT|IT|ST|UAT}   basis: {document}   baselined: {yes|no}
  Format        : {n} blocks removed ({categories}), {n} kept as ambiguous
  Coverage
    UI gaps     : {n}   {list}
    UX gaps     : {n}   {list}
    Logic gaps  : {n}   {list}
    Contradictions : {n}   {list, with both sources}
  Level boundary       : {n} cases at the wrong level
  Unanchored expectations : {n}/{sampled}
  Viewpoints missing   : {list}
  Verdict : {PASS|FAIL}
```

A contradiction — two sources disagreeing, with the cases having silently picked one — is
the most valuable finding here. Report it; do not resolve it (RS-05).
