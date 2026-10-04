---
description: "P2 — create or update the mockups for the screens, in the form this project uses, held to the legacy screen at the profile's fidelity level, and cross-check them against the screen design (X-09) and the legacy screen (X-10). Usage: /mig-generate-mockup [module id, screen id, or nothing for all]"
---

# P2 — Generate mockups

## Step 1 — Load

`mig-project`, then `mig-mockup`, then `mig-screen-design`.

## Step 2 — Pre-check

Required: the screen design for the scope, a resolved `{{profile.mockup.kind}}`, and a
resolved `{{profile.mockup.fidelity}}`.

- screen design missing → run `/mig-generate-basic-design screen` first. A mockup drawn
  before the screen design is a design decision made in a prototype (MU-01).
- `kind: none` → say the project has no mockup deliverable and stop. That is an answer.
- `figma` with no connector and no dated export → say the design is unavailable and ask.
  Do not proceed from the screen design alone; the point of X-09 is that the two were
  produced independently.
- `fidelity: redesigned` without a written client decision → **stop**. Redesign is a funded
  decision, not a default (MU-02).

## Step 3 — Plan

| # | Screen id | Surface | Legacy capture | Legacy UI source | Fidelity | Existing mockup | Action |
|---|---|---|---|---|---|---|---|

Derive the screen list from the screen-design directory, not from memory. Surfaces from
`{{profile.mockup.surfaces}}`.

The two legacy columns are the useful part of this plan: a screen with **neither** a capture
nor a UI source cannot be mocked up faithfully, and it is listed as a SPEC-GAP here rather
than drawn plausibly and discovered at review.

List screens with no mockup and mockups with no screen design in the same table.

## Step 4 — Generate or update

Delegate to `mig-mockup-designer`, one call per module or business area — the same batching
rule as basic design, for the same reason.

Per screen: all five states, every label and message verbatim by `MSG-*`, representative data
only, blocked controls rendered blocked, and **nothing present that is in neither the screen
design nor the legacy screen**.

By kind:
- `html` — self-contained files under `{{profile.mockup.dir}}`; must open from the filesystem
- `canvas` — the agent drafts the artboards; **publish from this session** to
  `{{profile.mockup.canvas.artifact_url}}`, reusing that URL. Record it on first publish
- `figma` — read and check only; changes go out as a change request against the design
- `image` — maintain the index document; the exports come from their own tool

After each batch, count the files on disk. Not the files the agent reported writing.

## Step 5 — Cross-checks

**X-09 — mockup ↔ screen design**, sub-checks a..h: fields, grid columns, buttons, messages
(by id **and exact text**), states, navigation targets, permission-dependent elements,
dialogs.

**X-10 — mockup ↔ legacy screen**, sub-checks a..f: field set, field order and grouping, tab
order, grid columns, label text verbatim, blocked controls. Run unless `fidelity:
redesigned`, in which case state the skip and its decision reference.

Each mismatch is **Critical**. **Do not resolve one by editing either side** — decide against
the legacy source; where the legacy is silent, raise a SPEC-GAP with an owner.

## Step 6 — Report against the gate

```
P2 — Mockup ({{profile.mockup.kind}}, fidelity {{profile.mockup.fidelity}})
  Screens        : {mockups}/{screens}       surfaces: {covered}/{required}
  States         : {screens with all 5}/{screens}
  X-09 a..h      : {pass|fail each}          Critical: {n}
  X-10 a..f      : {pass|fail each | not run: redesigned per {decision}}
  Fidelity excpt : {n}  ({n} with no recorded decision  <- inventions, NI-02)
  Blocked        : {n} controls rendered blocked and escalated
  Orphans        : mockup without design {n} · design without mockup {n}
  SPEC-GAPs      : {n}  (no capture and no UI source: {screens})
  Location       : {dir | artifact URL | Figma file + export date}
```

Then `/mig-review-design` over the screen category, and the P2 gate when the cross-checks
come back clean.
