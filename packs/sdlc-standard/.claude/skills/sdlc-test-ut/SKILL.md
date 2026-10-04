---
name: sdlc-test-ut
description: "P5 — the unit test pipeline: source analysis and Q&A, human pause, final analysis, checklist, coverage pause, detailed case writing, bounded self-review. Covers both the module-level test case document and the automated developer tests. Load with sdlc-test-design for ALL UT tasks."
---

# P5 — Unit Test

> Load with `sdlc-test-design` (levels, viewpoints, writing rules, formats).
> Prerequisite: `sdlc-project` resolved; the module has an approved detail design.
> **UT verifies the detail design** (TR-03).

Two artifacts, one phase:

| Artifact | Produced by | Lives in |
|---|---|---|
| Unit test case document — what a tester executes | this pipeline | `{{profile.testing.paths.testcase_root}}` |
| Automated developer tests — what CI runs | P4, alongside the code | the source tree |

They are not substitutes. The document proves coverage against the design; the automated
tests prove it still holds tomorrow. A project with only automated tests cannot show a
client which rules are covered; a project with only documents cannot detect a regression.

---

## Working layout

```
{{profile.testing.paths.testcase_root}}/
└── {{profile.testing.naming.module_dir}}/           e.g. UT_Batch1_SL0030PG/
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

**1a. Locate and verify the sources.** Detail design, function design, screen design and
data design for the module. Write what was found and whether it is sufficient.

**Stop here if the detail design is missing or is a paraphrase of the function design.**
Do not analyse around it and do not reconstruct it from the code — say what is missing and
ask. A UT suite derived from the code tests that the code does what it does.

**1b. Analyse.** Produce, in one file:
- screen modes and the item state matrix per mode (feeds VP-03a)
- every input field with type, length, format, required, default — **from the data
  design**, cross-checked against the detail design
- every rule from DD §5 with its algorithm, inputs and boundary values
- messages with their `MSG-*`
- which data objects each action reads and writes
- a first case list by viewpoint, with the boundaries named

**1c. Ask.** Write a questions file with one section per open point. Two groups, both
mandatory:

| Group | Contents |
|---|---|
| Open | the specification is silent or two documents disagree (RS-01, RS-05) |
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
re-open questions that were answered. Answers that changed a specification go back as a
`DEC-*` — and, if the document is baselined, as a CR (BL-02).

---

## Step 2 — Checklist

One row per intended case: TC ID, viewpoint, the design id it verifies, priority, one-line
scenario. No preconditions, no steps, no expected results — the point is to review coverage
before paying for detail.

Self-check before presenting:
- every enabled viewpoint represented where it applies (T-09)
- every DD §5 rule and every function-design error row covered (T-01, T-02)
- every hazard from `sdlc-test-design` §7 that applies to this module
- no two rows covering the same partition (TR-DD01)

If the self-check finds missing information rather than missing cases, stop and ask.

## ⏸ Pause 2 — the human reviews coverage

Stop. This is a **business and design** review by a QA lead or BA, not a repeat of the
self-check: are the flows right, is anything missing that only domain knowledge would
catch, are the priorities right.

On feedback, regenerate the checklist with the feedback as additional input, new timestamp,
and return to this same pause. Do not skip ahead to step 3 with unreviewed changes.

---

## Step 3 — Write the cases

From the checklist and the final analysis. Every case follows the table format and the
writing rules in `sdlc-test-design` — particularly TR-SE01 (concrete steps), TR-PC01
(numbered preconditions), TR-AN01 (anchored expectations) and TR-AT01 (split by
automatability).

TC IDs must match the checklist exactly. A case appearing here but not in the checklist
bypassed the coverage review.

---

## Step 4 — Bounded self-review

Two independent passes, then fix, then repeat:

| Pass | Question |
|---|---|
| A — specification | does every case match the detail design and the data design? |
| B — coverage | is every checklist row present, every viewpoint covered, no duplicates? |

Also check: TC ID uniqueness, case ordering, result columns empty.

Fix, write a new timestamped file, review again. At most
`{{profile.testing.pipeline.max_review_rounds}}` rounds. Still failing → stop and report
what will not converge; do not keep looping.

---

## Automated developer tests

Written in P4 with the code, against the same detail design:

- one behaviour per test; the name states the condition and the expectation
- expected values from the DD, never from running the code
- use the seams from DD §8 — no wall-clock, no random, no network
- every rule in DD §5 has at least one automated test, or a recorded reason why it is
  covered only manually
- coverage target from `{{profile.quality.targets.unit_coverage}}` — a floor, not the gate

---

## Exit gate

- [ ] every DD rule has ≥ 1 case (T-01) and every function-design error has one (T-02)
- [ ] all questions answered; specification changes recorded as `DEC-*` / CR
- [ ] automated suite green; coverage meets target
- [ ] defects found are recorded with an injection phase (TR-07)
- [ ] `{{profile.gates.P5_unit_test.exit}}` assertions hold

## Reporting

```
UT — {MODULE}
  Sources        : {found}/{required}   missing: {list}
  Questions      : {n} open, {n} rare — all answered: {yes|no}
  Checklist      : {n} cases   reviewed by human: {yes}
  Written        : {n} cases   file: {path}
  Self-review    : round {n}/{max} — {PASS|FAIL}
  Coverage T-01, T-02, T-08..T-10 : {pass|fail each}
  Automated      : {n} tests, {pass}/{total}, coverage {line}/{branch}
  Defects        : {n} ({by injection phase})
```
