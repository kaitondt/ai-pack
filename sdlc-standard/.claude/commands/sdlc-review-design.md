---
description: "Review deliverables against the enabled checklist families, with specification cross-validation and the cross-document checks. Read-only. Usage: /sdlc-review-design [file path, module id, category, or nothing for the whole current phase]"
---

# Review deliverables

**Read-only.** This command produces findings. It does not fix them — that is
`/sdlc-refine-skill` for systemic ones, and a normal edit for one-off ones.

## Step 1 — Load

`sdlc-project`, then `sdlc-review-framework`, then the category skill for whatever is under
review.

## Step 2 — Run it in a fresh session

If this session generated the documents, say so and recommend a new session. A generator
reviewing its own output does not fail from laziness — the reasoning that produced the
error is still in context and still looks correct, so it re-derives the same conclusion and
confirms it. A fresh read-only session has to re-derive from the sources, which is the only
computation that can disagree.

## Step 3 — Select the families

From `{{profile.review.families}}`, plus family C on everything. Print which families apply
to this target before starting.

## Step 4 — Review

Delegate to `sdlc-reviewer` — read-only by construction, so it cannot quietly fix what it
should be reporting.

For each behavioural statement: **follow the anchor and read it.** An anchor that merely
exists has not been checked; confirming that a citation is present rather than that it says
what the document claims is the most common review failure.

## Step 5 — Cross-document checks

Run the pairs the target set supports: X-01..X-07, X-09, X-10.

Do not "fix" a mismatch by editing one side to match the other. Determine which side is
wrong against the baselined requirement, and report that.

## Step 6 — Report

One file per artifact under `{{profile.review.output_dir}}`, plus a rollup:

```
Review — {target}
  Artifacts     : {n}
  Findings      : Critical {n} · Warning {n} · Suggestion {n}
  Density       : {findings per document}   target {{profile.quality.targets.review_density}}
  Cross-checks  : {each, pass/fail with the ids}
  Not verifiable: {n}   {what, and what would be needed}
  Verdict       : {PASS|FAIL}
```

When `{{profile.review.record_in_document}}` is true, also add the round to each document's
own review record (DS-03).

**A round with zero findings is a signal, not an achievement** (QM-02). Say which sources
you read; if the answer is "the document only", the review has not happened yet.

## Step 7 — Route the findings

Findings appearing in two or more artifacts are skill defects, not artifact defects. Send
them to `/sdlc-refine-skill` rather than fixing 40 documents by hand — that costs 40 units
and buys nothing for document 41.
