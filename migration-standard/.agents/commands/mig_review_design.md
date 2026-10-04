---
description: "Review deliverables against the enabled checklist families and cross-validate them against the legacy source. Writes one report per artifact. Usage: /mig_review_design [file, directory, module id, or category key]"
---

# Review design deliverables

## Step 1 — Load

`mig_project`, `mig_review_framework`, and the category skill for whatever is under
review.

## Step 2 — Resolve the target set

File → that file. Directory or category key → every deliverable in it. Module id → every
deliverable for that module across all categories. No argument → ask; a full-repository
review is long and should be a deliberate choice.

## Step 3 — Review each artifact

Apply the enabled families from `{{profile.review.families}}`: C (always), then SD / FD /
API / DB / BT as applicable.

Then run the legacy cross-validation: for each behavioural statement, follow its anchor,
**read the legacy source**, and compare. An anchor that is merely present is not checked;
a statement with no anchor is a Critical (NI-01).

## Step 4 — Cross-document checks

For a multi-artifact target, run the X-01..X-07 pairs that the target set supports.

## Step 5 — Write reports

One file per artifact under `{{profile.review.output_dir}}`, in the format defined by
`mig_review_framework`, including the mandatory **Not verifiable** section.

## Step 6 — Report

```
Review — {target}
  Artifacts   : {n}
  Critical {n} · Warning {n} · Suggestion {n}
  Not verifiable : {n}   ({what would be needed})
  Cross-checks : {pass|fail each}
  Verdict : {PASS|FAIL}   — FAIL blocks the P2/P3 gate
```

List the Critical findings inline in the response. Do not make the user open files to
learn that the review failed.
