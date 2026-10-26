---
name: mig-translation
description: "Cross-cutting translation of deliverables between the project languages. Direction detection, the never-translate token list, business-equivalence syncing rather than raw copying, dictionary use, table/CSV structural preservation, the client correction log, and reviewing an existing translation. Load for ALL translation and translation-review tasks."
---

# Translation of Deliverables

> Prerequisite: `mig-project` resolved. Language bindings come from
> `{{profile.language.by_path}}`; the never-translate list from
> `{{profile.language.immutable_tokens}}`.

Migration projects are usually multilingual: the client reads one language, the
implementation team works in another. Both sets of deliverables are real deliverables,
and they drift unless the sync rule is explicit.

---

## TL-01 — Direction is decided by the destination path, not the request

The language of a document is a property of its directory. A request phrased in one
language that targets a directory bound to another produces a document in the directory's
language. There is no "translate this into the language you are being asked in".

## TL-02 — Sync business changes, do not copy text

When a change is made in one language's copy, the other copy receives the **equivalent
business change**, written natively in its own language. Never paste the source language
into the target document, and never machine-translate a whole file over a hand-written one
— it destroys reviewed phrasing and the client notices immediately.

Procedure for a sync:
1. diff the source document against its last synced state;
2. identify the semantic changes, ignoring pure formatting;
3. apply each semantic change to the target document in its own language;
4. leave everything else untouched.

## TL-03 — Never translate

From `{{profile.language.immutable_tokens}}`, always including: module ids, document ids,
message ids, table and column names, procedure and program names, file paths, URLs, and
the contents of code blocks. These appear byte-identical in every language version.

Field labels are the delicate case: a label is user-facing text and **is** translated in
prose, but the physical name behind it never is, and the label must match whatever the
UI actually shows in that language.

## TL-04 — Message text is not translated

Legacy message text is verbatim (NI-03). It is quoted in its original form in every
language version, with an explanatory gloss beside it if the reader needs one. Translating
a message and letting it flow back into the implementation is how a UI ends up with
messages the operators do not recognise.

## TL-05 — Structure is preserved exactly

Same sections, same section numbers, same table columns in the same order, same row
count, same ids. A translated document is diffable against its source. If the structures
differ, one of them is wrong.

For CSV and other structured formats: identical column count and order, quoting valid for
the format, no rows added or removed, no comments introduced.

## TL-06 — Dictionary first

When `{{profile.language.dictionary}}` is set, it is authoritative for domain terms — even
where a more natural rendering exists. Consistency across hundreds of documents beats
elegance in one. Terms missing from the dictionary that recur are added to it, not
improvised per document.

When `{{profile.language.grammar_fixes}}` is set, apply it after translating.

## TL-07 — Punctuation and separator conventions follow the target language

Bracket style, list separators and spacing follow the target language's convention, and
one convention is used consistently within a document (ID-06). Do not carry the source
language's punctuation across.

## TL-08 — Never modify the source

Translation writes a new file or edits the designated target copy. The source document is
not touched, not reformatted, and not "fixed" along the way. Errors found in the source
are reported, not silently corrected in one language only.

## TL-09 — Every client correction is recorded once, and never needed twice

The client's reviewers are the final authority on their own language. When they correct a
translated deliverable — a term, a phrasing, a level of politeness, a word order in a label —
the correction is the most valuable translation input the project will ever get, and it is
lost the moment it is applied to one file and forgotten.

When `{{profile.language.correction_log}}` is set:

- **Append every correction as it arrives**, one row each: date, source document and
  location, the source-language text, the rejected translation, the accepted translation,
  the reviewer, and the reason when one was given. Append; never rewrite earlier rows.
- **Read the log before translating and before reviewing a translation**, alongside the
  dictionary. A correction already in the log that recurs in a new document is a defect of
  the translation, not a new finding.
- **Apply a correction everywhere it applies**, not only where the reviewer saw it: search the
  other documents of the same language for the rejected rendering and list each hit.
- **Promote what recurs.** A correction about a domain term belongs in
  `{{profile.language.dictionary}}`; one about phrasing belongs in
  `{{profile.language.grammar_fixes}}`. A correction made three times is proposed for
  promotion through `/mig-refine-skill`, so it stops depending on someone reading the log.
- **A correction never touches message text.** Legacy message strings are verbatim (TL-04);
  a reviewer asking to reword one is asking for a change, which is a change request.

When the log is not set and the client starts correcting translations, propose setting it —
the second correction of the same term is the moment the cost becomes visible.

**Reviewing an existing translation** applies the same sources in the same order — immutable
tokens (TL-03), message text (TL-04), structure (TL-05), dictionary (TL-06), correction log
(TL-09) — and reports findings by category with the source line, the current rendering and
the proposed one. A reviewer's rewrite that changes meaning, not only wording, is reported to
the source document's owner, not silently applied.

---

## Self-check

- [ ] direction determined from the destination path
- [ ] structure identical: sections, numbering, columns, ids
- [ ] no immutable token translated
- [ ] message text verbatim
- [ ] dictionary applied; new recurring terms proposed for it
- [ ] target-language punctuation, applied consistently
- [ ] source file untouched
- [ ] correction log read first; no logged correction repeated; new client corrections
      appended and applied wherever they recur
