---
name: sdlc-review-framework
description: "Cross-cutting review framework — checklist families (C common, RQ requirement, SD screen, FD function, API interface, DT data, NF non-functional, BT batch), severity model, the specification cross-validation method, review report format and the review-record obligation. Load for ALL review tasks on deliverables or code."
---

# Review Framework

> Prerequisite: `sdlc-project` resolved. Families enabled by `{{profile.review.families}}`.

A review produces **findings with evidence**, not opinions. Every finding names the rule it
violates and where.

---

## Severity

| Level | Definition | Consequence |
|---|---|---|
| **Critical** | Wrong behaviour, broken traceability, unrequested scope, or a rule violation that blocks approval | phase gate fails |
| **Warning** | Correct but non-conforming: format, consistency, missing cross-reference | fix before client review |
| **Suggestion** | Improvement with no correctness impact | optional |

A finding without a rule id and a location is not a finding. A finding that cannot be acted
on is a Suggestion at best.

Do not inflate. A Suggestion promoted to Critical to get attention destroys the signal the
gate depends on — and the next reviewer's Criticals get discounted with it.

---

## Family C — common document hygiene

Applies to every deliverable.

| ID | Check |
|---|---|
| C01 | correct template and section skeleton (DS-01, DS-04) |
| C02 | all mandated sections present; none empty without an explicit marker |
| C03 | content matches its source document (SRS for design, design for detail) |
| C04 | numbers, dates and settings cross-checked against the source |
| C05 | proper nouns correct: people, departments, systems, products |
| C06 | terminology consistent, and consistent with `{{profile.paths.glossary}}` |
| C07 | nothing contradicts a stated constraint or the scope statement |
| C08 | no skipped steps or logical gaps in a described process |
| C09 | no contradiction between sections |
| C10 | every reference and link resolves to something that exists |
| C11 | professional register; no filler, no rhetorical padding |
| C12 | spelling and grammar, especially in long generated sentences |
| C13 | tables, lists and headings follow the template |
| C14 | no sensitive data introduced; no secrets, no unmasked personal data |
| C15 | the document renders without error in the client's viewer |
| C16 | no duplicated content between sections |
| C17 | diagrams, tables and prose agree with each other |
| C18 | ids well-formed and unique (ID-01..ID-09) |
| C19 | Open Items present, each with an owner and a due date (DS-10) |
| C20 | every specification claim anchored, or in Open Items (RS-01) |
| C21 | no TBD in a document being put forward for baseline (RS-03) |
| C22 | version and `status` front matter agree (DS-01, BL-08) |
| C23 | review record present and filled (DS-03) |

## Family RQ — requirements

Load `sdlc-requirements`. Check RQ-01..RQ-07 and NF-01..NF-04, plus:

| ID | Check |
|---|---|
| RQ-A | every `REQ-*` is testable, and its verification reference is filled |
| RQ-B | every `REQ-*` cites a `BR-*`, `DEC-*` or external obligation |
| RQ-C | no requirement contains two requirements |
| RQ-D | no solution disguised as a requirement (RQ-04) |
| RQ-E | every `NFR-*` has target, condition, measurement and phase |
| RQ-F | R-01..R-08 cross-document checks pass |

## Family SD — screen design

Load `sdlc-screen-design`: every SD-S / SD-F / SD-M / SD-B / SD-A rule, plus item list
against the requirement fields (X-01), grid columns against the data design (X-02), and the
message set against the function design (X-06).

## Family FD — function design

Load `sdlc-function-design`: FD-S / FD-P / FD-D / FD-R / FD-E / FD-T, plus parameter and
error agreement with the interface design (X-03, X-04, X-05), and diagram-to-table
completeness in both directions (FD-D04).

## Family API — interface design

Load `sdlc-api-design`: API-S / API-U / API-C / API-E / API-V, plus X-03, X-04, X-05 and
API-X06, API-X07.

## Family DT — data design

Load `sdlc-data-design`: column traceability (DT-02), null semantics (DT-03), precision
(DT-04), time policy (DT-05), index-to-query mapping, integrity enforcement points,
retention and classification, and DDL agreement (X-07).

## Family NF — non-functional

Load `sdlc-nfr-design`: every `NFR-*` has a mechanism, a budget and a measurement (X-09);
failure modes named per dependency; authorisation enforcement layer stated; verification
plan complete.

## Family BT — batch design

Load `sdlc-batch-design`: BT-S / BT-V / BT-R / BT-E / BT-O, with particular attention to
restart and rerun, which is the most frequently missing section.

---

## Specification cross-validation

The part of review that finds real defects. For each behavioural statement in the document
under review:

1. locate its anchor — the `REQ-*`, `DEC-*` or upstream design item;
2. **read the anchor** — do not trust the statement's summary of it;
3. compare: values, order, conditions, messages, arithmetic, boundaries;
4. record a Critical for any divergence not covered by an approved change.

Where the anchor is missing, that is itself a Critical (RS-01). Where the anchor exists but
says something else, that is the most valuable finding the review will produce.

**An anchor that merely exists has not been checked.** The most common review failure is
confirming that a citation is present rather than that it says what the document claims.

---

## Reviewing code

Same severity model, applied against `rules/common/*` and the language rules:

| Focus | Check |
|---|---|
| Specification fidelity | the code implements the DD, including order, rounding and error paths (IM-01..IM-08) |
| Unrequested behaviour | anything the design does not call for (RS-06, IM-05) |
| Security | `rules/common/security.md` — authorisation, injection, secrets, error leakage |
| Boundaries | layer discipline, no domain importing framework types |
| Stack conventions | the review checklist of each stack rule file the diff touches (`JV-*`, `TS-*`, `RX-*`, `SQ-*`), with the client coding standard in `{{profile.system.coding_standards}}` taking precedence, then the project rules in `{{profile.project_rules}}` (`PRJ-*`); a finding the repository's linter already reports is cited as the linter's, not restated |
| Concurrency | async triggers locked, idempotency where stated |
| Tests | expectations sourced from the design, not from the implementation |
| Traceability | the register updated with the code references |

---

## Report format

One file per reviewed artifact:
`{{profile.review.output_dir}}/{category}/review_{ID}_{YYYYMMDDHHmm}.md`

```markdown
# Review: {ID} — {title}
Reviewed: {timestamp} · Families: {list} · Verdict: {PASS | FAIL}

## Summary
Critical {n} · Warning {n} · Suggestion {n} · density {findings per document}

## Findings
| # | Severity | Rule | Location | Finding | Evidence | Fix |
|---|---|---|---|---|---|---|

## Checklist results
| ID | Check | Result | Note |

## Not verifiable
Items that could not be checked, and what is needed to check them.
```

When `{{profile.review.record_in_document}}` is true, also add the round to the document's
own review record (DS-03) — that table is the input to review density (QM-02).

**The "Not verifiable" section is mandatory.** A check that could not be performed is
reported as such — never silently marked pass. A review that claims to have verified what
it could not is worse than no review, because the gate then trusts it.

**A review round that produced zero findings is reported as a signal**, not an achievement
(QM-02). Say which sources you read; if the answer is "the document only", the review has
not happened yet.
