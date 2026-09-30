---
description: "Review test case documents in either format mode (strip non-test content) or coverage mode (UI/UX/logic completeness against design, legacy and mockups). Usage: /mig_review_testcase [format|coverage|both] <file or module>"
---

# Review test cases

## Step 1 — Load

`mig_project`, `mig_test_design`, then `mig_test_review`.

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

Findings feed `/mig_refine_skill`: a gap appearing across several modules is a rule missing
from the test skill, not a slip in one document.
