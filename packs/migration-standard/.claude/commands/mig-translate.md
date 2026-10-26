---
description: "Translate or sync a deliverable between the project languages, preserving structure, ids and verbatim message text. Usage: /mig-translate <file path or directory> [target language]"
---

# Translate a deliverable

## Step 1 — Load

`mig-project`, then `mig-translation`.

## Step 2 — Determine the direction

From the destination path via `{{profile.language.by_path}}` — not from the language of
the request (TL-01). State the direction you determined before starting.

## Step 3 — Determine the mode

- **New translation** — the target file does not exist yet.
- **Sync** — the target exists. Diff the source against the target, apply only the
  semantic changes, in the target's own language, leaving reviewed phrasing untouched
  (TL-02). Never overwrite a hand-written target with a wholesale re-translation.
- **Correction** — the client's reviewers corrected the translation. Log each correction
  (TL-09), then apply it everywhere it recurs.
- **Review** — an existing translation is to be checked, not changed. Findings only (TL-09).

## Step 4 — Translate

Read the client correction log at `{{profile.language.correction_log}}` when set — no
rendering the client has already rejected is used again (TL-09). Apply the dictionary at
`{{profile.language.dictionary}}` when set, then the corrections at
`{{profile.language.grammar_fixes}}`.

Preserve exactly: section structure and numbering, table columns and order, row count,
every immutable token from `{{profile.language.immutable_tokens}}`, code blocks, and
legacy message text (TL-03, TL-04, TL-05).

## Step 5 — Verify and report

Diff the structures: same headings, same table shapes, same ids. A structural difference
means one of the two files is wrong.

```
Translation — {source} -> {target}
  Direction : {a} -> {b}   Mode : {new|sync}
  Sections {n}/{n}   Tables {n}/{n}   Ids preserved {n}/{n}
  Dictionary terms applied : {n}   New terms proposed : {list}
  Correction log : {n} logged corrections applied · {n} new appended · {n} recurrences fixed elsewhere
  Source file modified : no
```

The source file is never modified (TL-08).
