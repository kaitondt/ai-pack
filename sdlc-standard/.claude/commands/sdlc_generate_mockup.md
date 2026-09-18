---
description: "P2 — create or update the mockups for the screens, in the form this project uses (HTML prototype, design canvas, Figma reference or image index), and cross-check them against the screen design. Usage: /sdlc_generate_mockup [module id, screen id, or nothing for all]"
---

# P2 — Generate mockups

## Step 1 — Load

`sdlc_project`, then `sdlc_mockup`, then `sdlc_screen_design`.

## Step 2 — Pre-check

Required: the screen design for the scope you are mocking up, and a resolved
`{{profile.mockup.kind}}`.

- screen design missing → run `/sdlc_generate_basic_design screen` first. A mockup drawn
  before the screen design is a design decision made in a prototype (MU-01).
- `kind: none` → say the project has no mockup deliverable and stop. That is an answer.
- `kind: figma` with no connector and no export → say the design is unavailable and ask for
  an export. Do not proceed from the screen design alone; the point of the check is that the
  two were produced independently.

## Step 3 — Plan

| # | Screen id | Surface | States | Existing mockup | Action |
|---|---|---|---|---|---|

Derive the screen list from the screen-design directory, not from memory. Surfaces from
`{{profile.mockup.surfaces}}`. Print the plan; a screen with no mockup and a mockup with no
screen are both listed here, before anything is generated.

## Step 4 — Generate or update

Delegate to `sdlc_mockup_designer`, one call per module or business area — the same batching
rule as basic design, for the same reason.

Per screen: all five states in `{{profile.mockup.states_required}}`, every label and message
quoted by `MSG-*`, representative data only, nothing present that the screen design does not
specify.

By kind:
- `html` — self-contained files under `{{profile.mockup.dir}}`; must open from the filesystem
- `canvas` — the agent drafts the artboards; **publish from this session** to
  `{{profile.mockup.canvas.artifact_url}}`, reusing that URL so the client's link never
  changes. Record the URL in the profile on the first publish
- `figma` — read and check only; changes go out as a change request against the design
- `image` — maintain the index document; the exports themselves come from their own tool

After each batch, count the files on disk. Not the files the agent reported writing.

## Step 5 — Cross-check X-11

Per screen, a..g: fields, grid columns, buttons, messages, states, navigation targets,
permission-dependent elements. Each mismatch is **Critical** and is reported with both
artifact ids.

**Do not resolve a mismatch by editing either side to match the other.** Decide against the
baselined SRS; where the SRS is silent, it is an Open Item with an owner.

## Step 6 — Report against the gate

```
P2 — Mockup ({{profile.mockup.kind}})
  Screens        : {mockups}/{screens}       surfaces: {covered}/{required}
  States         : {screens with all 5}/{screens}
  X-11 a..g      : {pass|fail each}          Critical: {n}
  Orphans        : mockup without design {n} · design without mockup {n}
  Open Items     : {n}  ({n} without an owner)
  Location       : {dir | artifact URL | Figma file + export date}
```

Then `/sdlc_review_design` over the screen category, and `/sdlc_phase_gate P2` when the
cross-checks come back clean.
