---
name: mig-api-design
description: "P2 category — interface/API design documents. Rule families API-S (structure), API-U (URL and verb), API-C (contract), API-E (errors), API-X (cross-checks). Endpoint naming, auth, paging, uniform error envelope. Load for ALL interface-design tasks."
---

# P2 — Interface (API) Design

> Load with `mig-basic-design`. Prerequisite: `mig-project` resolved.

One document per endpoint. The API design is a **contract**: it states what crosses the
wire, and nothing about why.

---

## Section skeleton (API-S01)

```
# {EndpointName}（{MODULE}-API-{NNN}）
  <Revision history>
  <Contents>

## 1  Overview            purpose, calling screen / function ids
## 2  Endpoint            method, path, auth, content type
## 3  Request             path params, query params, body fields
## 4  Response            success shape, status code
## 5  Errors              status, code, MSG-*, condition
## 6  Related documents   SC / FC ids

## Open Items
```

**API-S02 — scope.** No UI behaviour, no business rationale, no processing steps. Those
belong to the screen and function documents; link to them by id.

---

## URL rules (API-U)

- **API-U01 — one URL convention for the whole project**, declared in the TSD and applied
  without exception. Per-surface prefixes are part of that convention, not a per-endpoint
  decision.
- **API-U02 — resource names in the project interface language** (normally English),
  kebab-case, plural for collections. Never transliterate a domain term from the legacy
  locale into the URL.
- **API-U03 — the version segment is always present.**
- **API-U04 — verbs match semantics.** GET never mutates; POST creates or performs an
  action; PUT and PATCH update; DELETE removes. A legacy screen that searches via a form
  submit becomes a GET with query parameters, or a documented POST search endpoint when
  the parameter set exceeds what a URL can carry. Decide once, project-wide.
- **API-U05 — authentication stated per endpoint**, including the exceptions such as login
  and health. The exception list is short and enumerated in the TSD.

---

## Contract rules (API-C)

- **API-C01 — every field** carries name, type, required, length or format, default and
  description.
- **API-C02 — names match the function design** (X-03 and X-04), exactly, both directions.
- **API-C03 — paging and sorting use the project-wide names** fixed by FD-P04, with the
  same defaults on every list endpoint.
- **API-C04 — the response envelope is uniform** across the project: the same shape for
  success, the same shape for errors, the same place for the total count.
- **API-C05 — nullability is explicit.** "Not required" and "may be null" are different
  statements; make both.
- **API-C06 — no field that no screen or function uses.** Unused fields are removed, or
  justified in Open Items.

---

## Error rules (API-E)

- **API-E01 — error table**: HTTP status, application code, `MSG-*`, condition.
- **API-E02 — the set matches the function design error table** (X-05).
- **API-E03 — status codes follow one project-wide mapping**: validation 400,
  unauthenticated 401, forbidden 403, not found 404, conflict 409, unexpected 500.
  Business-rule failures use that mapping consistently rather than being decided per
  endpoint.
- **API-E04 — error responses never leak internals**: no stack traces, no procedure names,
  no SQL, no file paths.

---

## Cross-checks (API-X)

Run before declaring an endpoint document done:

| Check | Assertion |
|---|---|
| API-X01 | request fields equal the function input parameters |
| API-X02 | response fields equal the function output fields |
| API-X03 | error set equals the function error set |
| API-X04 | every endpoint is referenced by at least one screen or job |
| API-X05 | every screen action reaching the server has an endpoint |
| API-X06 | naming, paging and envelope match the project-wide convention |

---

## Self-check

- [ ] method, path, version segment and auth all stated
- [ ] every field fully specified; nullability explicit
- [ ] paging and sorting names match the project convention
- [ ] error table complete and cross-consistent with the function design
- [ ] no internals leaked in error responses
- [ ] Open Items present
