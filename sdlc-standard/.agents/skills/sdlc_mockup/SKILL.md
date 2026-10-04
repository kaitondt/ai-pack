---
name: sdlc_mockup
description: "P2 mockup deliverables in whatever form the project uses — HTML prototype, AI-generated design canvas, Figma, or exported images. Creating, reading and editing each; the five required states; and the X-11 cross-check that keeps the mockup and the screen design from diverging. Load for ANY mockup task, alongside sdlc_screen_design."
---

# Mockup — the visual counterpart of the screen design

> Prerequisite: `sdlc_project` resolved, and `sdlc_screen_design` loaded for any task that
> touches both. Form comes from `{{profile.mockup.kind}}`; it is a project decision, and
> the pack supports each kind for **create, read and edit**.

A mockup exists so that a screen design can be reviewed by someone who does not read
specifications — which is most of the client. It is the cheapest place to discover that a
screen is wrong, and it is worth exactly as much as its agreement with the document beside
it.

---

## MU-01 — The mockup is never the specification

The screen design is. When the two disagree, the screen design is not "out of date" and the
mockup is not "what we actually agreed": one of them is wrong, and which one is decided
against the baselined SRS (X-11).

This matters because the mockup is the artifact everybody looks at. A field that exists only
in the mockup gets built; a rule that exists only in the document gets missed. Neither is
acceptable, and the cross-check is what prevents both.

Practical consequence: **no behaviour is introduced in a mockup**. Not a field, not a
button, not a status, not a default. If the design needs one, it goes into the screen design
first and the mockup follows (RS-06).

## MU-02 — Every screen shows all five states

`{{profile.mockup.states_required}}`, by default: `normal`, `empty`, `loading`, `error`,
`no-permission`.

Four of the five are what the review is for. A mockup that shows only the happy path with
three rows of tidy data has demonstrated nothing anybody was uncertain about — and the empty
state, the long-value overflow and the permission-denied view are exactly where the
disagreements are.

Show states as separate artboards, separate files, or a state switcher in the prototype —
whichever the kind supports. Name them so the reviewer can ask for one by name.

## MU-03 — Data in a mockup is representative and obviously not real

Realistic in shape — the longest name the field allows, a full-width date, a number at the
declared precision, a grid at its paging boundary. Never real customer data, never a real
name, never a plausible invoice that could be mistaken for a record.

Two failure modes, both common: lorem-ipsum placeholder text that hides how a real value
overflows, and copied production data that turns a review deck into a data-protection
incident.

## MU-04 — Labels and messages are quoted, not written

Every visible label, column header, button caption and message comes from the screen design
and the message catalogue, in the deliverable's language, by `MSG-*` id. A mockup that
invents its own wording creates a third source of UI text, and the one the developer copies
is whichever they opened last.

## MU-05 — A mockup is in the change cascade

`{{profile.change_request.cascade}}` lists `mockup` for a reason: a rename, a field
addition or a message change propagates to the mockup in the same CR, not in a tidy-up
afterwards. A half-updated mockup is worse than a stale one, because it looks current.

---

## Resolving the kind

Read `{{profile.mockup.kind}}`. Each kind below covers **create**, **read** and **edit** —
a mid-project adoption usually starts with *read*, against mockups that already exist.

### `html` — self-contained prototype in the repository

The default, and the only kind that is diffable, greppable and reviewable in a pull request.

**Create.** One file per screen at `{{profile.mockup.dir}}`, named by
`{{profile.mockup.naming}}`. Self-contained when `html.self_contained` is true: inline CSS
and JS, no CDN, no build step, no network fetch — it must open from the filesystem on a
client machine with no toolchain and no internet, because that is how it will be reviewed.
Honour the surface viewport from `{{profile.system.surfaces}}` when
`html.viewport_per_surface` is set. Shared styling goes in `html.shared_assets`, referenced
relatively.

States as MU-02: either one file per state, or one file with a state switcher that is
visibly a review control and not part of the design.

**Read.** Open the file. Extract the field set, the column set, the button set and the
visible text, and check them against the screen design (X-11). For a legacy prototype nobody
documented, this is the fastest route to a screen design — but what you extract is
*observed*, not specified: every item goes into the document as an open question until an
owner confirms it (RS-01).

**Edit.** Edit the file in place. Keep the change minimal and matched to the surrounding
markup; a mockup rewritten in a different style stops being comparable to its siblings.

### `canvas` — Claude Design canvas artboards

For projects where the client wants to move things around themselves rather than read a
document.

**Create.** Invoke the `design` skill to draft the canvas: multi-artboard `.dc.html`
artboards on one pan/zoom canvas, one artboard per screen state, published as an Artifact.
Record the published URL in `{{profile.mockup.canvas.artifact_url}}` on the first publish
and reuse it on every update, so the client's link never changes and the version history
stays on one page.

**Read.** Read the published artifact, or the `.dc.html` sources where they are committed.

**Edit.** Update the artboard sources and republish to the **same** URL. Never publish a
second artifact for the same screen set — two links is how a client reviews last month's
design and approves it.

Where the canvas is edited by the client in the published editor, their saved version is
ahead of the repository: re-read before editing, and treat their changes as review findings
against the screen design, not as agreed specification (MU-01).

### `figma` — the design lives in Figma

The common case on projects with a design team, and the case where this pack owns the least.

**Read.** Through a Figma MCP connector when one is configured, otherwise from the exports
in `{{profile.mockup.figma.export_dir}}`. When neither is available, say so and ask for an
export — do not describe a Figma file you have not opened, and do not infer the design from
the screen design you were about to check it against.

**Edit.** `{{profile.mockup.figma.writable}}` is `false` by default and should usually stay
that way: the design team owns the file, and a change made from a build tool is invisible in
their process. Produce a **change request against the design** — the screen, the element,
what should change and which `REQ-*` or `CR-*` requires it — and record who it went to.

**Create.** Only when the client has asked for it and `writable` is true. Otherwise the
project's own visual work goes in `html` or `canvas`, and Figma stays the design team's
artifact.

Record the file URL and the export date wherever a document cites the design. "Per Figma" is
not a citation (DIO-06).

### `image` — PNG/PDF exports from any tool

**Read** them directly; they are images and can be inspected. Extract fields, labels and
states, and mark every extracted item as observed rather than specified.

**Create/edit** is not possible in this kind — the tool that made them owns them. What the
pack produces here is the **index**: one document listing every export, the screen it
belongs to, its source tool, its export date, and its X-11 result. Without that index a
folder of screenshots is unreviewable and silently goes stale.

### `none`

No mockup deliverable. Say so in the P2 plan rather than leaving the category silently
absent — a missing category and a category that was decided against look identical three
months later.

---

## X-11 — Mockup ↔ screen design cross-check

Run per screen, at the end of the mockup category and again at the P2 gate. Each mismatch is
**Critical**.

| # | Left (mockup) | Right (screen design) |
|---|---|---|
| X-11a | every visible field | the screen item list, including type and max length |
| X-11b | every grid column, in order | the screen's grid definition |
| X-11c | every button and its enabled/disabled condition | the screen's action list |
| X-11d | every message shown | the screen's `MSG-*` set, by id and by text |
| X-11e | every state present | `{{profile.mockup.states_required}}` |
| X-11f | every navigation target | the screen transition diagram |
| X-11g | permission-dependent elements | the screen's permission matrix |

Report as `check · screen id · mockup file · verdict`. **Do not resolve a mismatch by editing
one side to match the other** — decide against the baselined SRS, and where the SRS is
silent, raise it as an open question with an owner (MU-01, RS-01).

A screen with no mockup, or a mockup with no screen design, is reported as an orphan and
carried into the gate. It is the same defect class as a traceability orphan and it is found
the same way: by counting both sides, not by reading one.

---

## Common failure modes

| Symptom | Cause | Fix |
|---|---|---|
| Mockup and document disagree at UAT | X-11 never run, or run once at the start | run it per screen, at category end and at the gate |
| Client approved a design nobody can build | mockup showed behaviour with no requirement | MU-01 — no behaviour originates in a mockup |
| Only the happy path was reviewed | states treated as optional | MU-02, all five, named |
| Developer used the mockup's wording | labels invented in the mockup | MU-04 — quote by `MSG-*` |
| Prototype does not open on the client's machine | CDN link, build step, or absolute path | `self_contained`, relative references only |
| Two artifact links for one screen set | republished to a new URL | reuse `canvas.artifact_url` |
| Figma described but never opened | no connector, no export, described anyway | say it is unavailable and ask |
| Mockups stale after a CR | mockup treated as a tidy-up | MU-05 — it is in the cascade |

## Self-check before reporting the category done

- [ ] the kind actually used matches `{{profile.mockup.kind}}`, and every surface in
      `{{profile.mockup.surfaces}}` is covered
- [ ] every screen in the screen-design category has a mockup, or an explicit recorded
      exclusion — counts reported both ways
- [ ] all five states present per screen, named
- [ ] every label and message quoted from the catalogue by id, in the directory's language
- [ ] no field, button, column or status exists in the mockup that is absent from the
      screen design
- [ ] representative data only; nothing real, nothing lorem-ipsum
- [ ] X-11a..g run per screen, mismatches reported with both artifact ids, none resolved by
      editing one side
- [ ] `html`: opens from the filesystem, no network dependency
- [ ] `canvas`: published to the recorded `artifact_url`, not a new one
- [ ] `figma`: read from a connector or a dated export; change requests raised, not edits
- [ ] `image`: the index document exists and lists every file with its export date

## Report

```
Mockup — {{profile.mockup.kind}}
  Screens        : {mockups}/{screens in screen design}
  Surfaces       : {covered}/{required}
  States         : {screens with all 5}/{screens}
  X-11           : a..g {pass|fail each}   Critical: {n}
  Orphans        : mockup without design {n} · design without mockup {n}
  Open Items     : {n} ({n} without an owner)
  Location       : {dir, or artifact URL, or Figma file + export date}
```
