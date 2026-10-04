---
name: sdlc_screen_design
description: "P2 category — screen/UI design documents. Rule families SD-S (structure), SD-F (fields), SD-M (messages), SD-B (behaviour scope), SD-A (accessibility and state). Section skeleton, field-type vocabulary, focus notation, dialog placement, empty/loading/error states. Load for ALL screen-design tasks."
---

# P2 — Screen Design

> Load with `sdlc_basic_design`. Prerequisite: `sdlc_project` resolved; SRS baselined.

Applies to every surface in `{{profile.system.surfaces}}`. Surface-specific differences
(viewport, input mechanism, control vocabulary) are stated per surface, never mixed into
one document.

---

## Section skeleton (SD-S01) — fixed order, nothing omitted

```
# {ScreenName}（{MODULE}-SC-{NNN}）
  <Revision history>  <Review record>  <Contents>

## 1-1  Screen information      ← the info table lives INSIDE this section
## 1-2  Screen layout
## 1-3  Screen item list
     1-3-1  Input items
     1-3-2  Buttons / actions
     1-3-3  Grid / list columns
     1-3-4  Other items         ← dialogs, popups, read-only panels
## 1-4  Screen behaviour        ← client-side only
## 1-5  Screen states           ← initial, loading, empty, error, no-permission
## 1-6  Screen transitions
## 1-7  Message list

## Open Items
```

- **SD-S02** — the screen-information table goes *inside* §1-1, never between the H1 and
  §1-1.
- **SD-S03** — dialogs belong in §1-3-4, never in §1-3-1.
- **SD-S04** — the `No` counter runs **continuously** across §1-3-1 → 1-3-4. It never
  restarts at a subsection.
- **SD-S05** — subsection order is fixed even when a subsection is empty; write "None."

---

## Field rules (SD-F)

**SD-F01 — controlled type vocabulary.** Only these values in the type column:

| Group | Values |
|---|---|
| Input | `TextInput` `NumberInput` `DateInput` `DateRangeInput` `TextArea` `FileInput` |
| Choice | `Select` `MultiSelect` `Checkbox` `Radio` `Lookup` `Toggle` |
| Display | `Label` `Image` `Link` `Badge` `Chart` |
| Action | `Primary` `Secondary` `Danger` `Ghost` `IconButton` |

Forbidden: framework component names (`MuiTextField`, `Select2`, `DataGridView`) and the
bare word `Button`. Extend the vocabulary in this skill if a project genuinely needs a new
type — never ad hoc in one document.

**SD-F02 — user-facing names only.** The item-name column holds the label the user sees.
No physical column names, in the column or in parentheses beside it (DS-06).

**SD-F03 — attribute and length columns apply to editable fields only.** A read-only or
composite field leaves them blank. Length format: `N` for integers, `N.M` where a decimal
part exists. **Every length and format traces to the data design**, not to judgement
(X-02).

**SD-F04 — focus notation.** `1D` = initial focus; `2`, `3`, … = tab order;
`—` = not focusable. Read-only fields have no focus value.

**SD-F05 — shared components are referenced, not copied.** A reused component (pagination
bar, master lookup, address block) is referenced by name and document id in one line.
Copying its item list duplicates a source of truth that will drift.

**SD-F06 — every field traces to a requirement.** A field the SRS does not call for is
unrequested scope (RS-06), even a "useful" one — an updated-by column, a remarks box, an
export button. It goes to Open Items as a `PROPOSAL`, not into the design.

**SD-F07 — validation is specified with its message.** Per field: the rule, when it fires
(on blur / on submit), the `MSG-*` shown, and what the field looks like in error. A rule
with no message is half a specification.

---

## Message rules (SD-M)

- **SD-M01** — `MSG-*` format per `{{profile.ids.message_id_format}}`; module **base**,
  correct zero padding (ID-04).
- **SD-M02** — message text is written once, in the catalogue, and referenced. Do not
  retype it into §1-4.
- **SD-M03** — system-wide messages (`MSG-COMMON-*`) are referenced, never listed in a
  module's §1-7.
- **SD-M04** — every `MSG-*` used in §1-4/§1-5/§1-6 appears in §1-7, and every §1-7 entry
  is used somewhere (X-06 against the function design).
- **SD-M05** — messages say what happened and what to do next. No internal detail, no
  error codes the user cannot act on, no blame.

---

## Behaviour-scope rules (SD-B)

§1-4 to §1-6 describe **what the user sees and does**. Nothing else.

**Forbidden in §1-4/§1-5/§1-6:** route paths, component or class names, state-store names,
auth-guard wording, HTTP status codes, table or procedure names, server-side validation,
API call mechanics, default parameters the user never sees.

Server-side processing belongs in the function design; the screen document links to it by
id. The test: if changing the sentence would require changing the function design too, it
is in the wrong document (DS-05).

---

## State rules (SD-A)

**SD-A01 — five states, always.** §1-5 specifies every one, for every screen:

| State | Must specify |
|---|---|
| Initial | what is shown before any user action; which fields are enabled |
| Loading | what the user sees; whether interaction is blocked; whether it is cancellable |
| Empty | the text shown when a search returns nothing, and the next action offered |
| Error | what is shown when the server or a dependency fails, and how to retry |
| No permission | what a user without the right sees — the screen, or nothing |

The empty and error states are the ones omitted, and they are the two the UAT tester finds
in the first hour.

**SD-A02 — async actions lock their trigger.** Every action that calls the server states:
disabled on click, visible pending state, re-enabled on completion. Double submission is
the most common transactional defect (`references/rules/common/patterns.md`).

**SD-A03 — destructive actions confirm, and say what is being destroyed.** The
confirmation names the object and the consequence, not "Are you sure?".

**SD-A04 — accessibility per `NFR-USE-*`.** Keyboard reachability for every action, focus
order matching the visual order, labels bound to inputs, and error text associated with
its field. If the project has an accessibility standard, the screen document states the
level it targets.

**SD-A05 — responsive behaviour per surface.** Where a surface has a smaller viewport,
state what collapses, what scrolls and what is hidden — do not leave it to implementation.

---

## Table cell conventions

Per DS-07: one point per line via `<br>`; no sentence punctuation in cells outside the
message-text column; `—` for not-applicable.

---

## Self-check

- [ ] section skeleton complete and in order; continuous `No` counter
- [ ] every type value from the controlled vocabulary
- [ ] no physical names, no route paths, no component names
- [ ] attribute/length blank for read-only; focus blank for read-only
- [ ] every field traces to a `REQ-*`; extras are Open Items, not design
- [ ] every validation rule has a `MSG-*`; every `MSG-*` is used and listed
- [ ] all five states specified, including empty and no-permission
- [ ] async triggers locked; destructive actions name what they destroy
- [ ] Open Items present
