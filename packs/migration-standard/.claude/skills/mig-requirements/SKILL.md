---
name: mig-requirements
description: "P1 — requirements documents. Produces requirement.md, BRD (business requirements), TSD (technical specification) and FRD (functional requirements) from the P0 legacy catalogue, with REQ-* ids traced to LEG-* ids. Load for ALL requirement-authoring tasks."
---

# P1 — Requirements

> Prerequisite: `mig-project` loaded; P0 gate passed.
> Every `REQ-*` cites at least one `LEG-*` (P1 gate).

---

## The document chain

```
legacy-inventory.md + requirement.md   (P0 output, evidence)
        ↓
BRD   what the business needs the system to do        ← REQ-* ids issued here
        ↓
TSD   how the target system will be built            ← architecture decisions
        ↓
FRD   screen-by-screen / job-by-job specification    ← the input to P2
```

Generate in this order. Each document reads the previous one; regenerating an earlier
document invalidates the later ones and they must be re-checked.

---

## BRD — Business Requirements Document

Audience: client business owners. Contains no technology.

| § | Content |
|---|---|
| 1 | Purpose, scope, out-of-scope (from `{{profile.legacy.excluded}}`) |
| 2 | Stakeholders and roles |
| 3 | Current-state business process, per business area |
| 4 | Business requirements — the `REQ-*` table |
| 5 | Business rules — conditions, calculations, state transitions |
| 6 | Data owned by the business — logical entities only |
| 7 | Non-functional expectations — volume, timing, availability |
| 8 | Assumptions, constraints, dependencies |
| 9 | Open Items (DS-09) |

**REQ table shape:**

| ID | Requirement | Priority | Legacy anchor | Migration type | Note |
|---|---|---|---|---|---|
| `REQ-RCV-012` | The system shall … | Must | `LEG-RCV-004` | As-is | |

`Migration type`: `As-is` (reproduce), `Adapted` (platform forces a change),
`New` (explicitly funded addition — requires a written client decision reference).
`New` without a decision reference is a Critical finding.

**Writing rules:**
- one requirement per row, testable, no conjunctions hiding two requirements
- "shall" for mandatory, "should" for recommended — used consistently
- no UI wording, no field names, no technology
- every row's anchor resolves to a real `LEG-*`

---

## TSD — Technical Specification Document

Audience: the implementation team. This is where `{{profile.target.stack}}` is quoted.

| § | Content |
|---|---|
| 1 | Target architecture — `{{profile.target.architecture}}`, layer responsibilities |
| 2 | Technology stack, verbatim from the profile, with the reason for each choice |
| 3 | Environment matrix — local / test / production differences |
| 4 | Repository and module layout |
| 5 | Cross-cutting concerns — auth, logging, error handling, validation, i18n |
| 6 | Data strategy — schema frozen or converted, access pattern, transaction policy |
| 7 | Integration points — external systems, file interfaces, schedules |
| 8 | Security deviations from legacy (see `rules/common/security.md`) |
| 9 | Build, deploy and rollback |
| 10 | Open Items |

**Rules:**
- decisions are recorded with their alternatives and the reason for rejection;
  a decision without a rationale gets re-litigated every sprint
- constraints from `{{profile.constraints}}` are stated explicitly, not implied
- no requirement text restated here — link to `REQ-*`

---

## FRD — Functional Requirements Document

Audience: designers and testers. This is the direct input to P2.

Organised by module. Per module:

| § | Content |
|---|---|
| a | Module id, name, surface, business area, `REQ-*` covered |
| b | Purpose and trigger |
| c | Actors and permissions |
| d | Inputs — every field: logical name, type, required, length, format, default |
| e | Processing — the rules that apply, each with a `LEG-*` anchor |
| f | Outputs — what is displayed, written, printed or sent |
| g | Messages — the `MSG-*` table, verbatim text (NI-03) |
| h | Navigation — entry and exit |
| i | Acceptance criteria — Given/When/Then, one per rule in (e) |
| j | Open Items |

**Rules:**
- acceptance criteria are the seed of the P5/P6 test cases — write them testable
- one FRD section per module id; no module without a section, no section without a module
- field lengths and formats come from the legacy definition, not from judgement
- no screen layout here — layout is P2

---

## Cross-document consistency

Before declaring P1 complete:

| Check | Assertion |
|---|---|
| R-01 | every `REQ-*` in the BRD appears in at least one FRD module |
| R-02 | every FRD module cites at least one `REQ-*` |
| R-03 | every `REQ-*` has a resolvable `LEG-*` anchor |
| R-04 | every `LEG-*` in scope is covered by at least one `REQ-*` (else: missed scope) |
| R-05 | TSD constraints do not contradict `{{profile.constraints}}` |
| R-06 | message texts in the FRD match the P0 catalogue byte-for-byte |

Write the results into `{{profile.paths.traceability}}` and report counts.

---

## Exit gate

- [ ] BRD, TSD, FRD generated, each with an Open Items section
- [ ] R-01..R-06 pass
- [ ] no `New` requirement without a client decision reference
- [ ] `{{profile.gates.P1_requirements}}` assertions hold
