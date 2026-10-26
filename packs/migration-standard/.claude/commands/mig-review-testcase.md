---
description: "Review test case documents in format mode (strip non-test content) or coverage mode (UI/UX/logic completeness against design, legacy and mockups), or audit the automated scripts against the cases in script mode. Usage: /mig-review-testcase [format|coverage|both|script] <file or module>"
---

# Review test cases

## Step 1 — Load

`mig-project`, `mig-test-design`, then `mig-test-review`.

## Step 2 — Resolve mode and target

Mode defaults to `both`, and `both` means **format first, then coverage** — reviewing
coverage through a document full of working notes wastes the expensive pass on the cheap
problem.

## Step 3 — Format mode

Read the whole file before editing; a long file needs several reads and editing early
produces inconsistent results.

Remove working notes, quoted Q&A, open-question markers, rule references and reviewer
comments. Never touch TC IDs, steps, expected results, preconditions, result columns, or
verbatim message text.

Re-scan at least twice — blocks become adjacent only after earlier deletions. Keep
genuinely ambiguous blocks and list them rather than guessing.

## Step 4 — Coverage mode

Read the sources first: screen and function design, interface design, data design, the
legacy screen and logic, and the mockup where one exists. Reviewing cases against cases is
circular.

Check UI, UX and Logic groups separately, then report gaps and contradictions apart from
each other. A contradiction between two sources is the more valuable finding: it means the
cases silently chose an answer nobody approved — ask, do not choose (NI-05).

## Step 4b — Script mode

Not part of `both`: it reviews code, not the document, and runs after the cases have passed
coverage review. **Read-only.** Also load `mig-test-automation`. List the tests with
`{{profile.testing.automation.list_command}}` — never count them from the source — and map
them to the reviewed cases by TC ID. Then apply checks S-01..S-09 from the skill's Mode 3; for
S-04 and S-05, follow sampled assertions back to the case and the case to its legacy anchor.
Report with the skill's Mode 3 format instead of the one below.

## Step 5 — Report

Write to `{{profile.paths.reviews}}` and summarise inline:

```
Test review — {file}
  Format   : {n} blocks removed ({categories}), {n} kept ambiguous
  Coverage : UI {n} · UX {n} · Logic {n} gaps · {n} contradictions
  Viewpoints missing  : {list}
  Duplicate partitions: {n}
  Not verifiable      : {what, and what is needed}
  Verdict  : {PASS|FAIL}
```

Findings feed `/mig-refine-skill`: a gap appearing across several modules is a rule missing
from the test skill, not a slip in one document.
