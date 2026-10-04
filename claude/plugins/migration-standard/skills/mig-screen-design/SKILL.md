---
name: mig-screen-design
description: "P2 category — screen/UI design documents. Rule families SD-S (structure), SD-F (fields), SD-M (messages), SD-B (behaviour scope), SD-L (legacy fidelity). Section skeleton, field-type vocabulary, focus notation, dialog placement, pagination reference. Load for ALL screen-design tasks."
---

# P2 — Screen Design

> Load with `mig-basic-design`. Prerequisite: `mig-project` resolved.

Applies to every surface in `{{profile.target.surfaces}}`. Surface-specific differences
(viewport, key handling, control vocabulary) are stated per surface, never mixed into one
document.

---

## Section skeleton (SD-S01) — fixed order, nothing omitted

```
# {ScreenName}（{MODULE}-SC-{NNN}）
  <Revision history>
  <Contents>

## 1-1  Screen information      ← the info table lives INSIDE this section
## 1-2  Screen layout
## 1-3  Screen item list
     1-3-1  Input items
     1-3-2  Buttons / actions
     1-3-3  Grid / list columns
     1-3-4  Other items         ← dialogs, popups, read-only panels
## 1-4  Screen behaviour        ← client-side only
## 1-5  Screen transitions
## 1-6  Message list

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
| Input | `TextInput` `NumberInput` `DateInput` `DateRangeInput` `TextArea` |
| Choice | `Select` `Checkbox` `Radio` `Lookup` |
| Display | `Label` `Image` `Link` |
| Action | `Primary` `Secondary` `Danger` `Ghost` `IconButton` |

Forbidden: platform control names (`TextBox`, `ComboBox`, `DataGridView`, `DatePicker`)
and the bare word `Button`. Extend the vocabulary in this skill if a project genuinely
needs a new type — never ad hoc in one document.

**SD-F02 — user-facing names only.** The item-name column holds the label the user sees.
No physical column names, in the column or in parentheses beside it (DS-05).

**SD-F03 — attribute and length columns apply to editable fields only.** A read-only or
composite/customised field leaves them blank. Length format: `N` for integers, `N.M` where
a decimal part exists.

**SD-F04 — focus notation.** `1D` = initial focus; `2`, `3`, … = tab order;
`—` = not focusable. Read-only fields have no focus value.

**SD-F05 — shared components are referenced, not copied.** A reused component (pagination
bar, master lookup, address block) is referenced by name and document id in one line.
Copying its item list duplicates a source of truth that will drift.

**SD-F06 — every field traces to a legacy control** or is listed in Open Items as a
`PROPOSAL`. Field lists are validated against the legacy form definition, not against the
prose of the FRD (X-02).

---

## Message rules (SD-M)

- **SD-M01** — `MSG-*` format per `{{profile.ids.message_id_format}}`; module **base**,
  correct zero padding (ID-03).
- **SD-M02** — message text verbatim from the P0 catalogue (NI-03).
- **SD-M03** — system-wide messages (`MSG-COMMON-*`) are referenced, never listed in a
  module's §1-6.
- **SD-M04** — every `MSG-*` used in §1-4/§1-5 appears in §1-6, and every §1-6 entry is
  used somewhere (X-06 against the function design).

---

## Behaviour-scope rules (SD-B)

§1-4 and §1-5 describe **what the user sees and does**. Nothing else.

**Forbidden in §1-4/§1-5:** route paths, component or class names, state-store names,
auth-guard wording, HTTP status codes, stored-procedure names, server-side validation,
API call mechanics, default parameters the user never sees.

Server-side processing belongs in the function design; the screen document links to it by
id.

---

## Legacy-fidelity rules (SD-L)

- **SD-L01** — layout, field order, tab order and grid column order match the legacy
  screen. Reordering "for usability" is NI-02.
- **SD-L02** — no comparative references to the legacy system in the body prose (NI-06).
  A metadata cell such as `Migration type: As-is` is fine.
- **SD-L03** — controls that the target platform has no equivalent for (window-close
  buttons, function-key legends on a mouse-driven surface, MDI parents) are omitted, and
  the omission is recorded once in Open Items.
- **SD-L04** — surface-specific input mechanisms (function keys, scanner triggers) appear
  **only** in that surface's documents. A desktop document containing function-key
  mappings is a Critical finding, and vice versa.

---

## Table cell conventions

Per DS-06: one point per line via `<br>`; no sentence punctuation in cells outside the
message-text column; `—` for not-applicable.

---

## Self-check

- [ ] section skeleton complete and in order; continuous `No` counter
- [ ] every type value from the controlled vocabulary
- [ ] no physical names, no route paths, no component names
- [ ] attribute/length blank for read-only; focus blank for read-only
- [ ] every `MSG-*` well-formed, verbatim, and cross-consistent with the function design
- [ ] field list reconciled against the legacy form definition
- [ ] Open Items present
