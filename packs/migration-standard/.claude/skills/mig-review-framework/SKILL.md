---
name: mig-review-framework
description: "Cross-cutting review framework — checklist families (C common, SD screen, FD function, API interface, DB data, BT batch), severity model, review report format, and the legacy cross-validation method. Load for ALL review tasks on deliverables or code."
---

# Review Framework

> Prerequisite: `mig-project` resolved. Families enabled by `{{profile.review.families}}`.

A review produces **findings with evidence**, not opinions. Every finding names the rule
it violates and where.

---

## Severity

| Level | Definition | Consequence |
|---|---|---|
| **Critical** | Wrong behaviour, broken traceability, invented content, or a rule violation that blocks approval | phase gate fails |
| **Warning** | Correct but non-conforming: format, consistency, missing cross-reference | fix before client review |
| **Suggestion** | Improvement with no correctness impact | optional |

A finding without a rule id and a location is not a finding. A finding that cannot be
acted on is a Suggestion at best.

---

## Family C — common document hygiene

Applies to every deliverable.

| ID | Check |
|---|---|
| C01 | correct template and section skeleton (DS-01, DS-03) |
| C02 | all mandated sections present; none empty without an explicit marker |
| C03 | content matches its source document (FRD for design, design for detail) |
| C04 | numbers, dates and settings cross-checked against the source |
| C05 | proper nouns correct: people, departments, systems, products |
| C06 | terminology consistent throughout, and consistent with the dictionary |
| C07 | nothing contradicts a stated constraint |
| C08 | no skipped steps or logical gaps in a described process |
| C09 | no contradiction between sections |
| C10 | every reference and link resolves to something that exists |
| C11 | professional register; no filler, no rhetorical padding |
| C12 | spelling and grammar, especially in long generated sentences |
| C13 | tables, lists and headings follow the template |
| C14 | no sensitive data introduced |
| C15 | the document renders without error in the client's viewer |
| C16 | no duplicated content between sections |
| C17 | diagrams, tables and prose agree with each other |
| C18 | ids well-formed and unique (ID-01..ID-07) |
| C19 | Open Items section present (DS-09) |
| C20 | every behavioural claim anchored, or in Open Items (NI-01) |

## Family SD — screen design

Load `mig-screen-design` and check every SD-S / SD-F / SD-M / SD-B / SD-L rule, plus:
field list vs legacy form definition (X-02), grid columns vs legacy grid (X-01),
message set vs function design (X-06).

## Family FD — function design

Load `mig-function-design`: FD-S / FD-P / FD-D / FD-E / FD-L, plus parameter and error
agreement with the interface design (X-03, X-04, X-05), and diagram-to-table completeness.

## Family API — interface design

Load `mig-api-design`: API-S / API-U / API-C / API-E, plus API-X01..X06.

## Family DB — data design

Load `mig-data-design`: column reconciliation against the legacy definition (X-07),
conversion-trap decisions, null vs empty, sentinel mapping, key constraints checked
against real data.

## Family BT — batch design

Load `mig-batch-design`: BT-S / BT-R / BT-E / BT-L, with particular attention to restart
and rerun, which is the most frequently missing section.

---

## Legacy cross-validation

The part of review that only a migration needs, and the part that finds real defects.
For each behavioural statement in the document under review:

1. locate the legacy equivalent through the anchor;
2. read it — do not trust the anchor's summary;
3. compare: values, order, conditions, messages, arithmetic;
4. record a Critical for any divergence not listed as an approved deviation.

Where the anchor is missing, that is itself a Critical (NI-01).

---

## Report format

One file per reviewed artifact:
`{{profile.review.output_dir}}/{category}/review_{ID}_{YYYYMMDDHHmm}.md`

```markdown
# Review: {ID} — {title}
Reviewed: {timestamp} · Families: {list} · Verdict: {PASS | FAIL}

## Summary
Critical {n} · Warning {n} · Suggestion {n}

## Findings
| # | Severity | Rule | Location | Finding | Evidence | Fix |
|---|---|---|---|---|---|---|

## Checklist results
| ID | Check | Result | Note |

## Not verifiable
Items that could not be checked, and what is needed to check them.
```

**The "Not verifiable" section is mandatory.** A check that could not be performed is
reported as such — never silently marked pass. A review that claims to have verified what
it could not is worse than no review.
