---
name: mig-test-ut
description: "P5 — the unit test case generation pipeline: source analysis and Q&A, human pause, final analysis, checklist, coverage pause, detailed case writing, bounded self-review. Checkpoint files, retry rules, output layout. Load with mig-test-design for ALL UT authoring tasks."
---

# P5 — Unit Test Case Pipeline

> Load with `mig-test-design` (viewpoints, writing rules, formats).
> Prerequisite: `mig-project` resolved; the module has approved FC and SC documents.

Unit test here means **module-level functional test cases** written against the design and
the legacy source — the document a tester executes. Automated developer tests are a
separate artifact, produced by `mig-test-automation`.

---

## Working layout

```
{{profile.testing.paths.testcase_root}}/
└── {{profile.testing.naming.module_dir}}/           e.g. UT_Batch{N}_{MODULE}/
    ├── Step/
    │   ├── {MODULE}_step1_sources_{TS}.md
    │   ├── {MODULE}_step1_analysis_{TS}.md
    │   ├── {MODULE}_step1_questions_{TS}.md      ← the human fills this in
    │   ├── {MODULE}_step1_final_{TS}.md          ← single source of truth for step 2
    │   ├── {MODULE}_step2_checklist_{TS}.md
    │   └── {MODULE}_step4_review_{TS}.md         ← one per review round
    └── {{profile.testing.naming.ut_file}}         ← draft, fixed, final (all kept)
```

Rules that make this layout work:
- a step reads the **newest** file of the prefix it needs, by timestamp
- a retry writes a new timestamp and **deletes nothing**
- the module directory is found by globbing on `{MODULE}` when `{BATCH}` is not yet known

---

## Step 1 — Sources, analysis, questions

**1a. Locate and verify the sources.** Function design, screen design, interface design for
the module, plus the legacy screen and logic. Write what was found and whether it is
sufficient.

**Stop here if the function design or screen design is missing.** Do not analyse around a
missing source and do not reconstruct it from the code — say what is missing and ask.

**1b. Analyse.** Produce, in one file:
- screen modes and the item state matrix per mode (feeds VP-03a)
- every input field with type, length, format, required, default — **from the legacy field
  definition**, cross-checked against the data design
- business rules with their legacy anchors
- messages with their MSG-IDs, verbatim
- data mapping: which data objects each action reads and writes
- a first case list by viewpoint, with boundaries named

**1c. Ask.** Write a questions file with one section per open point. Two groups, both
mandatory:

| Group | Contents |
|---|---|
| Open | the sources genuinely disagree or are silent (`NI-05`, SPEC-GAP) |
| Rare | edge cases you believe exist but cannot confirm are reachable |

The Rare group is the one teams skip, and it is where the expensive UAT defects come from.
An unanswered Rare item is not a reason to proceed — it is a reason to wait.

## ⏸ Pause 1 — the human answers

Stop. Tell the user which file to fill in and that **every** item, Rare included, needs an
answer. Resume only when none are blank.

If the questions file is empty, say so and ask whether to continue — an empty questions
file usually means the analysis was shallow, not that the module is simple.

## Step 1d — Final analysis

Merge the answers into the analysis. This file, not the original analysis, is the single
source of truth for everything downstream. Do not re-derive from the sources here; do not
re-open questions that were answered.

---

## Step 2 — Checklist

One row per intended case: TC ID, viewpoint, priority, one-line scenario. No preconditions,
no steps, no expected results — the point is to review coverage before paying for detail.

Self-check before presenting:
- every enabled viewpoint represented where it applies (T-06)
- every function-design rule and error row covered (T-01, T-02)
- every migration hazard from `mig-test-design` §6 that applies to this module
- no two rows covering the same partition (TR-DD01)

If the self-check finds missing information rather than missing cases, stop and ask.

## ⏸ Pause 2 — the human reviews coverage

Stop. This is a **business** review by a QA lead or BA, not a repeat of the self-check:
are the flows right, is anything missing that only domain knowledge would catch, are the
priorities right.

On feedback, regenerate the checklist with the feedback as additional input, new timestamp,
and return to this same pause. Do not skip ahead to step 3 with unreviewed changes.

---

## Step 3 — Write the cases

From the checklist and the final analysis. Every case follows the table format and the
writing rules in `mig-test-design` — particularly TR-SE01 (concrete steps), TR-PC01
(numbered preconditions) and TR-AT01 (split by automatability).

TC IDs must match the checklist exactly. A case that appears here but not in the checklist
bypassed the coverage review.

---

## Step 4 — Bounded self-review

Two independent passes, then fix, then repeat:

| Pass | Question |
|---|---|
| A — specification | does every case match the design and the legacy source? |
| B — coverage | is every checklist row present, every viewpoint covered, no duplicates? |

Also check: TC ID uniqueness, case ordering, result columns empty.

Fix, write a new timestamped file, review again. At most
`{{profile.testing.pipeline.max_review_rounds}}` rounds. Still failing → stop and report
what will not converge; do not keep looping.

---

## Reporting

```
UT — {MODULE}
  Sources        : {found}/{required}   missing: {list}
  Questions      : {n} open, {n} rare — all answered: {yes|no}
  Checklist      : {n} cases   reviewed by human: {yes}
  Written        : {n} cases   file: {path}
  Self-review    : round {n}/{max} — {PASS|FAIL}
  Coverage T-01..T-07 : {pass|fail each}
  Anchored expectations : {n}/{n}
```
