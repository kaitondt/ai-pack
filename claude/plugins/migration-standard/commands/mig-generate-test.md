---
description: "P5/P6 — generate unit test design (UT) and integration test design (IT) documents for a module, covering the nine viewpoints and every screen flow. Usage: /mig-generate-test [ut|it|both] MODULE"
---

# P5 / P6 — Generate test design

## Step 1 — Load

`mig-project`, then `mig-test-design` (shared spine), then `mig-test-ut` for UT or
`mig-test-it` for IT — they carry the checkpoint pipeline, the human pauses and the
retry rules.

## Step 2 — Resolve arguments

Kind (`ut`, `it`, `both` — default `both`) and module id, validated against
`{{profile.ids.module_pattern}}`. Missing module → ask; do not guess.

## Step 3 — Pre-check

- **UT** requires the module's FC documents. Missing → stop.
- **IT** requires the SC transition diagram and the API documents. Missing → warn and
  continue with reduced coverage, stating what is uncovered.

## Step 4 — Generate through the pipeline

The pipeline has two human pauses (`{{profile.testing.pipeline.human_pauses}}`): after the
open questions, and after the coverage checklist. Do not skip them to finish faster — each
buys a review at the stage where a correction is cheap.

### Generation

Delegate to `mig-tester`.

**UT** — one section per FC id. Every applicable viewpoint from the nine. Viewpoint 9
(numeric and date edge cases) is mandatory wherever the function computes, formats or
compares numbers or dates — this is where migration defects concentrate.

**IT** — scenario groups per flow, including the layout-integrity group for each surface
in `{{profile.target.surfaces}}`.

Expected values come from the legacy system, with anchors. Never from the current
implementation's output.

## Step 5 — Coverage check

| Check | Assertion |
|---|---|
| T-01 | every FC has at least one UT case |
| T-02 | every FC error row has a UT case naming its MSG-ID |
| T-03 | every screen flow has an IT scenario |
| T-04 | every endpoint appears in an IT scenario |
| T-05 | every expected value is anchored or structural |

## Step 6 — Report

```
P5/P6 — {MODULE}
  UT : {n} cases over {n} FCs   viewpoints covered {list}
  IT : {n} scenarios in {n} groups
  Coverage T-01..T-05 : {pass|fail each}
  Uncovered : {list}
  Gate : {pass|fail}
```
