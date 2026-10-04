---
name: sdlc-api-design
description: "P2 category — interface/API design. Rule families API-S (structure), API-U (URL and verbs), API-C (contract and types), API-E (errors), API-V (versioning and compatibility), API-X (cross-checks). Covers REST endpoints, file interfaces and message interfaces. Load for ALL interface-design tasks."
---

# P2 — Interface Design

> Load with `sdlc-basic-design`. Prerequisite: `sdlc-project` resolved.

An interface document is a **contract**. It says what a caller may send, what it will get
back, and how failure is expressed. It says nothing about why, and nothing about what the
UI does with the result.

Covers three interface kinds; the section skeleton differs only in §3.

---

## Section skeleton (API-S01)

```
# {InterfaceName}（{MODULE}-API-{NNN}）
  <Revision history>  <Review record>  <Contents>

## 1  Interface information   purpose, consumer, owning function (FC id), auth
## 2  Endpoint / channel      method + path, or file layout, or topic + schema
## 3  Request                 path, query, header, body — every field typed
## 4  Response                success shape, every field typed
## 5  Error responses         the envelope and every error the contract can return
## 6  Constraints             rate limits, size limits, timeout, idempotency
## 7  Compatibility           version, deprecation policy, breaking-change rule

## Open Items
```

- **API-S02 — contract only.** No business rationale, no UI behaviour, no processing
  description. The function design owns those; link by id (DS-05).
- **API-S03 — one interface, one document.** A document covering "the order APIs" cannot
  be cross-checked or versioned.

---

## URL and verb rules (API-U)

- **API-U01** — resource-oriented paths, plural nouns, no verbs in the path.
  `/orders/{id}/lines`, not `/getOrderLines`.
- **API-U02** — the verb carries the semantics: `GET` safe and cacheable, `POST` creates or
  invokes, `PUT` replaces, `PATCH` partially updates, `DELETE` removes. A `GET` with side
  effects is a defect, not a style choice — proxies and prefetchers will call it.
- **API-U03** — one naming convention for path segments and one for field names, chosen
  once for the whole project and stated in the architecture document. Mixed conventions in
  one API are the most visible sign of a design nobody owned.
- **API-U04** — collection parameters are project-wide, not per endpoint: the same page,
  size, sort and filter parameter names everywhere (X-03 against the function design).

---

## Contract rules (API-C)

**API-C01 — every field carries: name, type, format, required, nullable, constraints,
example.** "Nullable" and "required" are different questions and both must be answered.

**API-C02 — types are precise.** Number is not a type: state integer or decimal, and for
decimals the scale. Date is not a type: state date, date-time or timestamp, and the zone
(DT-05). Enumerations list their legal values, and state what a client should do with an
unknown one.

**API-C03 — request field names match the function design parameters byte-for-byte**
(X-03); response field names match its outputs (X-04). A rename on either side is Critical.

**API-C04 — no internal shape leaks into the contract.** Database column names, ORM entity
shapes and stored-procedure parameter lists are implementation. When the API mirrors the
table, it inherits every schema change as a breaking change.

**API-C05 — collections return an envelope**, with the item array and the paging metadata,
never a bare array. A bare array cannot grow a total count without breaking every client.

**API-C06 — the contract states what is *not* returned**: fields omitted for
authorisation, fields omitted when null, and whether omission and null mean the same thing.

---

## Error rules (API-E)

**API-E01 — one error envelope for the whole project**, defined once in the architecture
document and referenced here: a stable machine-readable code, a message id (`MSG-*`), a
human-readable message, and optional field-level detail.

**API-E02 — the error set matches the function design exactly** (X-05). Every error the
function can produce is in the contract; every contract error is producible.

**API-E03 — status codes are used for their meaning**: 400 malformed, 401 unauthenticated,
403 unauthorised, 404 absent, 409 conflicting state, 422 valid shape but rejected by a
business rule, 429 rate-limited, 5xx the server's fault. A 200 carrying `{"success":
false}` defeats every client library, proxy and monitor in the path.

**API-E04 — no internals in an error response.** No stack traces, SQL text, internal
hostnames or library versions (`rules/common/security.md`).

**API-E05 — the client's obligation is stated**: which errors are retryable, with what
backoff, and which are permanent.

---

## Constraints (§6)

Rate limits, maximum page size, maximum payload size, timeout, and the idempotency
mechanism for anything that creates or moves money or stock (FD-T03). State the key, its
lifetime, and what a repeat returns.

An interface with no stated limits has limits anyway — the ones the infrastructure imposes
under load, discovered at P7.

---

## Versioning and compatibility (API-V)

- **API-V01** — a version segment exists from the first release. Adding versioning later
  requires changing every client, which is exactly the situation versioning exists to
  avoid.
- **API-V02** — the breaking-change rule is stated: what counts as breaking (removing a
  field, narrowing a type, adding a required request field, changing an error code) and
  what does not (adding an optional field, adding an enum value if API-C02 was answered).
- **API-V03** — deprecation has a policy: how it is announced, how long the old version
  runs, and how a client discovers it is calling a deprecated endpoint.
- **API-V04** — for an interface with a system in `{{profile.scope.external_systems}}`,
  their version change is a change request on this project (`rules/common/patterns.md`).

---

## File and message interfaces

Same document, different §2/§3:

| Kind | §2 states | §3 states |
|---|---|---|
| File | direction, transport, path convention, filename pattern, schedule, trigger | record layout with offsets or delimiters, header and trailer, encoding, line ending, control totals |
| Message | broker, topic/queue, delivery guarantee, ordering, partitioning key | schema, schema registry reference, and the poison-message behaviour |

For files: state the empty-file convention, the duplicate-file behaviour, and what happens
when a file arrives late or twice. These three account for most integration incidents in
P9, and all three are cheap to specify now.

---

## Cross-checks (API-X)

| Check | Assertion |
|---|---|
| X-03 | request fields ≡ function design input parameters |
| X-04 | response fields ≡ function design outputs |
| X-05 | error set ≡ function design error cases |
| API-X06 | paging, sorting and filter parameter names match the project convention |
| API-X07 | every endpoint names the function design it exposes, and vice versa |

---

## Self-check

- [ ] contract only — no rationale, no UI, no processing description
- [ ] every field typed with format, required, nullable, constraints and example
- [ ] naming convention consistent with the project-wide one
- [ ] collections use the envelope and the standard paging parameters
- [ ] one error envelope; status codes used for their meaning; retryability stated
- [ ] limits, timeout and idempotency stated
- [ ] version segment present; breaking-change rule stated
- [ ] X-03, X-04, X-05, API-X06, API-X07 pass
- [ ] Open Items present
