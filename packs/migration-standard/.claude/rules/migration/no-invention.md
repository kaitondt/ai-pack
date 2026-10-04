# RULE FAMILY: NO-INVENTION

> The single most important rule in a migration project. Everything else in the pack
> exists to make this rule checkable.

## NI-01 — Every documented behaviour must be traceable to legacy source

Any behaviour, message, validation, default value, sort order, field length, error case
or screen transition written into a deliverable MUST be anchored to at least one of:

1. **Legacy source code** — `{{profile.legacy.logic_source}}`, `{{profile.legacy.ui_source}}`
2. **Legacy data definitions** — `{{profile.legacy.db_source}}`
3. **An explicit written client decision** — recorded with date and author

If none of the three says anything about the behaviour in question, it is a **SPEC-GAP**.
Classify it as such, stop, and ask. Do **not** fill the hole with "good practice",
"industry standard", or "what a modern app would do".

**Anchor format.** Every non-obvious statement carries its anchor:

```
Sort order: 入荷予定日 ascending, then 伝票番号 ascending.
  ← LEG-RCV-004 : PcGamen/frmNyukaYotei.vb:412 (dgv.Sort call)
```

The anchor may be shortened in the body and expanded in a source table, but it must exist.

## NI-02 — Reproduce, do not improve

A migration reproduces observable behaviour. Improvements are a separate, funded decision.

**Forbidden without explicit approval:**
- adding validation the legacy did not have
- removing validation the legacy did have (even if it looks redundant)
- changing a message wording, including fixing its typos
- reordering fields, columns or tab order
- changing rounding, truncation or numeric precision
- adding "helpful" defaults, autofills, confirmations or empty states

If you believe an improvement is warranted, write it in the deliverable's
**Open Items** section as a proposal. Do not implement it.

## NI-03 — Verbatim message text

Messages are copied byte-for-byte from legacy source, including:
- half-width / full-width character choice
- trailing spaces and punctuation
- typographical errors

Normalising message text silently breaks the client's operator training material and
their test expectations.

## NI-04 — BLOCKED features stop the run (blocking)

A **blocked feature** is a legacy feature that exists in source but is unreachable at
runtime — a button disabled in every code path, a menu item behind a permanently false
flag, a form with no navigation into it.

When you detect one:

1. Document it as **disabled**, matching the legacy runtime state.
2. Add a visible marker: `⚠️ BLOCKED — <evidence>`.
3. **Stop and ask the user.** Do not proceed with that item.
4. Resume only after an explicit yes/no decision, and record that decision in the
   deliverable's revision history.

Never enable a blocked feature on your own judgement. The feature may be disabled
because of an unresolved business problem that is not visible in the code.

## NI-05 — Uncertainty is reported, not resolved

When two legacy sources disagree (the form validates one way, the stored procedure
another), report both with anchors and ask. Do not pick the one that looks more correct.

## NI-06 — No legacy references in target deliverables

The design documents describe the **new** system. Comparisons to the old system belong in
analysis documents (P0/P1) and in commit messages, not in P2/P3 deliverables.

**Forbidden in design-document prose:** "same as the old system", "as before",
"legacy behaviour retained", "detail omitted, follows current system", VB.NET/COBOL
property notation.

Allowed: a classification cell in a metadata table (e.g. a `Migration type` column whose
value is `As-is`), and the revision history.

**Fix:** restate the behaviour positively in terms of the new system.

## Self-check before finishing any P1–P3 deliverable

- [ ] Every behavioural claim has an anchor, or sits under **Open Items**
- [ ] Messages are verbatim
- [ ] No improvement was introduced silently
- [ ] Blocked features were escalated, not enabled
- [ ] No comparative references to the legacy system in the body prose
