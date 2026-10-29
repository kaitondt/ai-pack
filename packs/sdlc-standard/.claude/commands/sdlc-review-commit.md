---
description: "Review the staged or current diff against the design documents, the coding rules and the security rules, before it is committed. Read-only. Usage: /sdlc-review-commit [module id, or nothing for the current diff]"
---

# Review before commit

**Read-only.** Findings, not fixes.

## Step 1 — Load

`sdlc-project`, then `sdlc-review-framework`, then `sdlc-implementation` and the stack
rules for the files in the diff (`rules/java/`, `rules/typescript/`, `rules/react/`,
`rules/sql/`), plus the client coding-standard digest named in
`{{profile.system.coding_standards}}` — the client's standard wins where they differ — and
the project rules in `{{profile.project_rules}}`, cited as `PRJ-*`.

## Step 2 — Establish what the diff is supposed to do

Read the design documents for the module — SC, FC, API, DT, DD — and the requirement or CR
that motivated the change. A diff reviewed without its specification can only be reviewed
for style.

## Step 3 — Review, in this order

| # | Focus | Checks |
|---|---|---|
| 1 | Specification fidelity | the code implements the DD: rules, order, rounding, error paths, permissions (IM-01..IM-08) |
| 2 | Unrequested behaviour | anything the design does not call for — an extra field, a helpful default, a silent trim (RS-06, IM-05) |
| 3 | Security | `rules/common/security.md`: authorisation server-side, parameterised queries, no secrets, no internals in errors |
| 4 | Boundaries | layer discipline; domain not importing framework or transport types |
| 5 | Concurrency | async triggers locked, idempotency where the design states it |
| 6 | Data | precision, scale, null handling and time zone as the data design specifies |
| 7 | Tests | expectations sourced from the design, not from the implementation; the changed rules have cases |
| 8 | Stack conventions | each touched stack rule file's review checklist (`JV-*`, `TS-*`, `RX-*`, `SQ-*`) and the client standard; run the repository's linter on the changed files and cite its output rather than restating it |
| 9 | Hygiene | naming per the glossary, no commented-out code, no debug output, no `.only` left in a test |
| 10 | Traceability | the register updated with the code references |

Item 2 is the one a normal code review misses, because the code looks *better* for having
it. Check the diff against the design item list, not against your judgement of what the
feature needs.

## Step 4 — Report

```
Commit review — {module or diff}
  Files          : {n}   (+{added} / -{removed} lines)
  Specification  : {n} items implemented / {n} in the design
  Findings       : Critical {n} · Warning {n} · Suggestion {n}
    {each Critical: file:line — rule — problem — fix}
  Unrequested    : {n}   {what, and where it should go instead}
  Security       : {n}
  Tests          : {n} added   expectations anchored: {yes|no}
  Not verifiable : {what could not be checked}
  Verdict        : {PASS|FAIL}
```

A Critical blocks the commit. Say so plainly rather than listing it among suggestions.

Where the diff turns out to be right and the design wrong, that is a drift item and a
document change (through a CR if it is baselined) — not a note in the commit message.
