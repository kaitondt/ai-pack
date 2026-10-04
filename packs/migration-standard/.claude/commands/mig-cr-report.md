---
description: "CR phase 6 — write the change-request report to the configured directory in the six-section format, appending a new round to an existing report rather than overwriting it. Usage: /mig-cr-report [CR-ID] [existing report path]"
---

# CR.4 — Write the change-request report

## Step 1 — Load

`mig-project`, then `mig-change-request`.

## Step 2 — Get the CR id

It comes from the client's CR list (C5). Never invent one, never derive it from the module
id, never number it from the files already in the report directory.

Not in context → ask:
> "Which id from the CR list should this report be filed under (e.g. CR-014)?"

Normalise the case, keep the number exactly as given, and match
`{{profile.change_request.id_format}}`.

## Step 3 — Determine the file

`{{profile.paths.change_requests}}/{CR-ID}_{MODULE}_{short-slug}.md`

Module: the affected module id, or the shared marker when several are touched. Slug: a few
words, kebab-case, no date — the date belongs in the metadata block.

**Existing file for that id → append a new round.** Never overwrite. Rounds are how the
client sees which parts were the original request and which were their second thoughts.

## Step 4 — Write, in the language bound to that path

Six sections: the request · impact · options · what was done · verification · conclusion.

- **§1-1 is verbatim.** The original wording, not the interpretation, and not a
  back-translation of it.
- **§2** carries the impact matrix with the unaffected rows still in it, and any
  pre-existing defect found and deliberately not fixed (C6).
- **§3** names the option chosen, who approved it and when. A CR report without an
  identifiable approver is not evidence of anything.
- **§4** is document diffs then code diffs, in that order (C4), plus test-case changes.
- **§5** is real output from runs that happened. Not run is written as not run; failing is
  written as failing, with the output (C10).
- **§6** states what is still waiting on the client and what still has to be deployed.

Class variants: `CR-DATA` blocked on a frozen object, `CR-CLARIFY`, and `CR-OUT-OF-SCOPE`
have no §4 code diff — the skill's Phase 6 says what each carries instead.

## Step 5 — Report

```
CR report — {CR-ID}
  File     : {path}   ({created | round {n} appended})
  Language : {lang}
  Module   : {module}   Class : {class}   Option : {A|B|C}
  Sections : 6/6
  Verification entries : {n} real runs
  Open with the client : {n} questions
```
