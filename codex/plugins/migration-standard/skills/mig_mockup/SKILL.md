---
name: mig_mockup
description: "P2 mockup deliverables in whatever form the project uses — HTML prototype, design canvas, Figma or exported images — held to the legacy screen as the UI oracle. Fidelity levels, the five states, reading legacy captures, and the X-09/X-10 cross-checks. Load for ANY mockup task, alongside mig_screen_design."
---

# Mockup — the visual counterpart of the screen design

> Prerequisite: `mig_project` resolved, and `mig_screen_design` loaded for any task
> touching both. Form comes from `{{profile.mockup.kind}}`; faithfulness from
> `{{profile.mockup.fidelity}}`. The pack supports each kind for **create, read and edit**.

A mockup exists so the screen design can be reviewed by someone who does not read
specifications — which is most of the client. In a migration it does something more: it is
the artifact the client's operators compare against the screen they have used for fifteen
years, and it is where they notice that a field moved.

---

## MU-01 — The mockup is never the specification

The screen design is. When the two disagree, one of them is wrong, and which one is decided
against the **legacy source** (X-09), not against whichever is easier to change.

No behaviour originates in a mockup. Not a field, not a button, not a status, not a default.
This is RS-free territory: in a migration, a control that appears in the mockup and in
neither the screen design nor the legacy screen is an **invention** (NI-01), and it will be
built.

## MU-02 — The legacy screen is the UI oracle, to the degree the profile says

`{{profile.mockup.fidelity}}` is the field that decides whether a visual difference is a
defect or a deliverable. It is not a style preference; it is a contractual position.

| `fidelity` | What the mockup reproduces | A layout difference is |
|---|---|---|
| `as-is` | the legacy screen: same fields, same order, same grouping, same tab order. Restyling limited to the target platform's own controls | a **defect** |
| `restyled` | the same information in the same order, in a modern visual language. Layout changes need a recorded decision per screen | a defect unless a decision covers it |
| `redesigned` | a deliberately re-thought UI. The legacy is then the **behaviour** oracle only, never the layout oracle | expected |

`redesigned` requires a funded, written client decision, and `as-is` is the default for a
reason: the client is paying to keep a system their staff already know how to operate.

`{{profile.mockup.fidelity_exceptions}}` lists screens agreed to differ, each with the
decision that authorised it. **An exception with no decision is an invention** (NI-02) —
report it, do not honour it.

## MU-03 — NI-02 applies to pixels

"Reproduce, do not improve" is hardest to hold in a mockup, because the work is visual and
the instinct of anyone drawing a screen is to make it better. Under `as-is`, all of the
following are forbidden without a decision:

- reordering fields, columns or tab order, however illogical the legacy order looks
- regrouping fields into tidier sections
- widening, narrowing or realigning a column to "balance" the layout
- replacing a legacy control with a nicer modern equivalent that behaves differently
  (a free-text field that was free text does not become a dropdown)
- adding placeholder text, helper text, empty-state illustrations, confirmations or
  autofills the legacy did not have
- removing a field that looks redundant
- fixing a typo in a label

Every one of these is a **PROPOSAL in Open Items**, not an edit. The client may well accept
several of them — but as a decision with a cost, not as something that arrived in a
prototype.

## MU-04 — Every screen shows all five states

`{{profile.mockup.states_required}}`, by default `normal · empty · loading · error ·
no-permission`.

Four of the five are what the review is for. A mockup showing only the happy path with three
tidy rows has demonstrated nothing anybody was uncertain about — and the empty grid, the
overflowing value and the permission-denied view are where the disagreements live.

Under `as-is`, each state reproduces what the legacy did in that state, which usually has to
be **discovered** rather than remembered: a legacy screen's empty-result behaviour is often
a message box, not an empty grid, and the message is a `MSG-*` with verbatim text (NI-03).

## MU-05 — BLOCKED features appear blocked

A legacy control that exists but is unreachable at runtime (NI-04) appears in the mockup in
the state the legacy runtime has it in — disabled, hidden, or absent — with the `⚠️ BLOCKED`
marker carried through from the screen design.

Never render a blocked control as working because the mockup "looks broken" otherwise. The
mockup looking broken is the point: it is what makes the client look at it and decide.

## MU-06 — Labels and messages are quoted, never written

Every label, column header, button caption and message comes from the screen design and the
message catalogue by `MSG-*`, **verbatim** (NI-03) — including half-width/full-width
choices, trailing spaces, and typographical errors.

A mockup that retypes a message creates a third source of UI text, and the one the developer
copies is whichever they opened last. Under `as-is`, a corrected typo in a mockup is a defect
against the legacy.

## MU-07 — Data in a mockup is representative, and never real

Realistic in shape — the longest value the field allows, a full-width date, a number at the
declared precision, a grid at its paging boundary. Never real customer data.

This bites harder in a migration than in a greenfield project, because the easiest way to
make a faithful mockup is to copy a legacy screen capture — and those captures frequently
contain live production data. `references/rules/common/security.md` requires masking before anything is
committed to `{{profile.legacy.screen_capture_dir}}`; the same applies to anything derived
from it.

## MU-08 — A mockup is in the change cascade

`{{profile.change_request.cascade}}` lists `mockup`. A rename, a field addition or a message
change propagates to it in the same CR, not in a tidy-up afterwards. A half-updated mockup is
worse than a stale one, because it looks current.

---

## Resolving the kind

Read `{{profile.mockup.kind}}`. Each kind covers **create**, **read** and **edit** — and on a
migration, *read* usually comes first, against legacy captures and sometimes against a
prototype the client already commissioned.

### `html` — self-contained prototype in the repository

The default, and the only kind that is diffable, greppable and reviewable in a
`{{profile.infrastructure.scm.review_unit}}`.

**Create.** One file per screen under `{{profile.mockup.dir}}`, named by
`{{profile.mockup.naming}}`. Self-contained when `html.self_contained` is true: inline CSS
and JS, no CDN, no build step, no network fetch — it must open from a file share on a client
machine with no toolchain and no internet, because that is how the operators will review it.
Honour the surface viewport from `{{profile.target.surfaces}}`; under `as-is` on a handheld
surface, the viewport is a constraint the legacy screen was designed around and the layout
must survive it.

**Read.** Extract the field set, column set, button set and visible text, and check against
the screen design (X-09) and the legacy capture (X-10).

**Edit.** In place, minimally, matching the surrounding markup. A mockup rewritten in a
different style stops being comparable to its siblings.

### `canvas` — design-canvas artboards

For clients who want to move things around themselves rather than read a document.

**Create.** Invoke the `design` skill to draft the canvas: one artboard per screen state,
published as an Artifact. Record the URL in `{{profile.mockup.canvas.artifact_url}}` on the
first publish and reuse it on every update, so the client's link never changes.

**Read.** The published artifact, or the committed `.dc.html` sources.

**Edit.** Update the sources and republish to the **same** URL. Never publish a second
artifact for one screen set — two links is how a client reviews last month's design and
approves it.

Where the client edits the canvas themselves, their saved version is ahead of the repository:
re-read before editing, and treat their changes as **change requests against the screen
design**, not as agreed specification. Under `as-is` a client edit that departs from the
legacy layout is exactly the decision that `fidelity_exceptions` exists to record.

### `figma` — the design lives in Figma

**Read.** Through a Figma MCP connector where one is configured, otherwise from the exports
in `{{profile.mockup.figma.export_dir}}`. With neither, **say the file is unavailable and
ask**. Never describe a Figma file you have not opened, and never infer the design from the
screen design you were about to check it against.

**Edit.** `{{profile.mockup.figma.writable}}` is `false` by default and should stay there:
the design team owns the file, and an edit from a build tool is invisible in their process.
Produce a change request against the design — the screen, the element, what should change,
and the `LEG-*` or `CR-*` that requires it.

**Create.** Only when asked and `writable` is true.

Cite the file URL and the export date wherever a document depends on it (DIO-06).

### `image` — exports from any tool

**Read** them directly. **Create/edit** is not possible; the tool that made them owns them.
What the pack produces is the **index**: every export, its screen, its source tool, its
export date, and its X-09/X-10 results. Without that index a folder of images is unreviewable
and goes stale silently.

### `none`

No mockup deliverable. Say so in the P2 plan rather than leaving the category absent — a
missing category and a category decided against look identical three months later.

---

## Reading the legacy screen

The input that makes a migration mockup possible, in order of authority:

1. **The legacy UI source** — `{{profile.legacy.ui_source}}`. Form definitions carry the
   control list, the tab order, the sizes and the enabled/disabled logic. This is the oracle,
   and it is the only source that says what the screen does in states nobody captured.
2. **Legacy screen captures** — `{{profile.legacy.screen_capture_dir}}`. What it looked like
   in practice, with real proportions. Best evidence for layout; no evidence at all for the
   states nobody screenshotted.
3. **Legacy documents** — evidence of intent, never of behaviour (DIO-08). A screen layout
   diagram in a ten-year-old specification frequently shows fields that were removed.

Where the capture and the source disagree, **report both and ask** (NI-05). Do not pick the
one that looks more correct: a control present in source and absent from every capture is
usually a BLOCKED feature (NI-04), which is a decision, not a drawing problem.

Where neither exists for a screen, that is a SPEC-GAP. Say so; do not compose a plausible
layout from the field list, because it will be reviewed as though somebody knew.

---

## X-09 and X-10 — the cross-checks

Run per screen, at the end of the mockup category and again at the P2 gate. Each mismatch is
**Critical**.

### X-09 — mockup ↔ screen design

| # | Left (mockup) | Right (screen design) |
|---|---|---|
| X-09a | every visible field | §1-3-1 input items, with type and length |
| X-09b | every grid column, in order | §1-3-3 grid columns |
| X-09c | every button, and its enabled/disabled condition | §1-3-2 buttons / actions |
| X-09d | every message shown | §1-6 message list, by `MSG-*` **and by exact text** |
| X-09e | every state present | `{{profile.mockup.states_required}}` |
| X-09f | every navigation target | §1-5 screen transitions |
| X-09g | permission-dependent elements | the screen's permission rules |
| X-09h | dialogs and popups | §1-3-4 other items |

### X-10 — mockup ↔ legacy screen

Only where `fidelity` is `as-is` or `restyled`. Under `redesigned`, X-10 is not run and the
report says so explicitly, with the decision reference.

| # | Check |
|---|---|
| X-10a | field set matches the legacy form's control list — nothing added, nothing dropped |
| X-10b | field **order** and grouping match |
| X-10c | tab order matches (`as-is` only) |
| X-10d | grid column set and order match the legacy grid definition |
| X-10e | label text verbatim, including width and punctuation conventions |
| X-10f | controls that are disabled or hidden in the legacy runtime are disabled or hidden here (NI-04) |

**Do not resolve a mismatch by editing one side to match the other.** Decide against the
legacy source. Where the legacy is silent, it is a SPEC-GAP with an owner, in Open Items.

Count both directions: screens with no mockup, and mockups with no screen design. Both are
orphans and both go in the report.

---

## Common failure modes

| Symptom | Cause | Fix |
|---|---|---|
| Operators reject the UI at UAT | mockup quietly modernised under `as-is` | MU-03; X-10b and X-10c per screen |
| A field nobody asked for reached production | it originated in the mockup | MU-01 — it is an invention (NI-01) |
| Message wording differs from the legacy | retyped rather than quoted | MU-06, X-09d compares **text**, not just ids |
| Only the happy path was reviewed | states treated as optional | MU-04, all five, named |
| A disabled legacy button appears working | "the mockup looked broken" | MU-05 — that appearance is the point |
| Production data in a review deck | copied from a legacy capture | MU-07; mask before committing |
| Prototype does not open on the client's machine | CDN link, build step, absolute path | `self_contained`, relative references |
| Two artifact links for one screen set | republished to a new URL | reuse `canvas.artifact_url` |
| Figma described but never opened | no connector, no export, described anyway | say it is unavailable and ask |
| Layout invented for a screen with no capture | no source, no capture, drawn anyway | SPEC-GAP |

## Self-check before reporting the category done

- [ ] kind and fidelity actually used match `{{profile.mockup.kind}}` and
      `{{profile.mockup.fidelity}}`; every exception cites its decision
- [ ] every surface in `{{profile.mockup.surfaces}}` covered
- [ ] every screen in the screen-design category has a mockup, or a recorded exclusion —
      counts reported both ways
- [ ] all five states per screen, named
- [ ] every label and message quoted verbatim by `MSG-*`, in the directory's language
- [ ] nothing present that is absent from both the screen design and the legacy screen
- [ ] blocked controls rendered blocked, marked, escalated — not enabled
- [ ] representative data only; nothing real, nothing lorem-ipsum
- [ ] X-09a..h run per screen; X-10a..f run unless `redesigned`, and the skip is stated
- [ ] no mismatch resolved by editing one side; each decided against the legacy source
- [ ] `html` opens from the filesystem with no network · `canvas` published to the recorded
      URL · `figma` read from a connector or a dated export · `image` index complete

## Report

```
Mockup — {{profile.mockup.kind}}, fidelity {{profile.mockup.fidelity}}
  Screens        : {mockups}/{screens in screen design}
  Surfaces       : {covered}/{required}
  States         : {screens with all 5}/{screens}
  X-09 a..h      : {pass|fail each}          Critical: {n}
  X-10 a..f      : {pass|fail each | not run: redesigned per DEC-xxx}
  Fidelity excpt : {n}  ({n} without a recorded decision  <- these are inventions)
  Blocked        : {n} controls rendered blocked
  Orphans        : mockup without design {n} · design without mockup {n}
  SPEC-GAPs      : {n}  (screens with neither source nor capture: {list})
  Location       : {dir | artifact URL | Figma file + export date}
```
