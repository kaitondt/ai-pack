---
description: "Translate or sync a deliverable between the project languages, preserving structure, ids and approved user-facing text. Usage: /sdlc-translate <file path or directory> [target language]"
---

# Translate a deliverable

## Step 1 — Load

`sdlc-project`, then `sdlc-translation`.

## Step 2 — Determine the direction from the destination path

`{{profile.language.by_path}}` decides. The language of the request does not (TL-01). A
Vietnamese request targeting a Japanese directory produces a Japanese document.

Print the resolved direction before starting. Getting this backwards produces a document in
the wrong directory that reads correctly, which is the hardest kind to notice.

## Step 3 — Choose the mode

| Mode | When |
|---|---|
| First translation | the counterpart does not exist yet |
| **Sync** | the counterpart exists and the source changed |
| Correction | the client's reviewers corrected the translation — log each correction (TL-10), then apply it everywhere it recurs |
| Review | an existing translation is to be checked, not changed — findings only (TL-10) |

**Sync is the common case and it is not a re-translation** (TL-02). Diff the source against
its last synced state, identify the semantic changes, and apply each one to the target
natively. Never machine-translate a whole file over a hand-written one — it destroys
reviewed phrasing, and the client notices immediately.

## Step 4 — Translate

- structure identical: sections, numbering, table columns and order, row count, ids (TL-05)
- never translate `{{profile.language.immutable_tokens}}` (TL-03)
- user-facing text is **quoted from the target language's catalogue**, not translated from
  the other version (TL-04); a missing catalogue entry is an open item, not a translation
  task
- `{{profile.language.dictionary}}` is authoritative for domain terms, and must agree with
  `{{profile.paths.glossary}}` (TL-06)
- `{{profile.language.correction_log}}` is read first: no rendering the client has already
  rejected is used again (TL-10)
- target-language punctuation, applied consistently within the document (TL-07)
- the source file is never modified (TL-08)

## Step 5 — Baseline check

If either version is baselined, both are (TL-09). The change goes through the CR, and the
two versions are updated together. A document pair that disagrees is worse than either
version alone, because a reader cannot tell which one was approved.

## Step 6 — Report

```
Translation — {file}
  Direction     : {source lang} → {target lang}   (from the destination path)
  Mode          : {first|sync}
  Structure     : sections {n}={n} · tables {n}={n} · ids {n}={n}
  Immutable tokens preserved : {n}
  Catalogue text quoted      : {n}   missing entries: {n}
  Dictionary terms applied   : {n}   new terms proposed: {list}
  Correction log : {n} logged corrections applied · {n} new appended · {n} recurrences fixed elsewhere
  Baselined     : {yes — CR {id} | no}
  Source file modified : no
```

Errors found in the source are reported, not silently corrected in one language only.
