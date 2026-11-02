---
name: sdlc-nfr-design
description: "P2 category — non-functional and architecture design. Turns each NFR-* into a mechanism, a budget and a measurement; covers performance budgets, availability and failure modes, security architecture, operability, and the X-09 NFR-to-decision table. Load for ALL architecture and quality-attribute design tasks."
---

# P2 — Non-Functional & Architecture Design

> Load with `sdlc-basic-design`. Prerequisite: `sdlc-project` resolved; SRS baselined.

Functional design decides what the system does. This decides whether it survives contact
with real load, real failures and real operators. It is the category most often written
last, reviewed least, and discovered missing at P7 — when nothing can be changed cheaply.

---

## Section skeleton

```
# Non-functional design — {area or system}

## 1  NFR realisation table        ← X-09, the core of this document
## 2  Performance design           budgets, hot paths, data volumes, caching
## 3  Availability and failure     failure modes, degraded mode, RPO/RTO
## 4  Security architecture        identity, authorisation, data protection, audit
## 5  Operability                  logging, monitoring, alerting, backup, runbook
## 6  Scalability and capacity     growth assumptions, scaling levers, limits
## 7  Compliance and retention     obligations, evidence, data lifecycle
## 8  Verification plan            which ST case measures what, on which environment

## Open Items
```

---

## NF-01 — Every NFR gets a mechanism, a budget and a measurement

The §1 table is the deliverable. Everything else elaborates it.

| NFR | Target | Mechanism that delivers it | Budget allocation | Measured by | Residual risk |
|---|---|---|---|---|---|
| `NFR-{CATEGORY}-{NNN}` | ≤2.0 s p95 order search | server-side paging, covering index `IX_ORD_CUST_DT`, no N+1 | API 1.2 s / render 0.5 s / network 0.3 s | `ST-PERF-004` on staging, 50 VU | index unusable if free-text search is added later (`RSK-{NNN}`) |

Rules:
- **Every `NFR-*` has a row.** A missing row is a Critical finding at review.
- A mechanism is a specific technical decision, not a category. "Caching" is not a
  mechanism; "5-minute cache of the category master, invalidated on master update" is.
- The budget allocation is what makes a target actionable at P4. "2 seconds end to end"
  tells a developer nothing; "1.2 s server budget" tells them when they are over.
- **Residual risk is mandatory and is usually the most useful column.** It says what would
  invalidate the design, which is what the next change request will do.

## NF-02 — Performance is designed against volume, not against feel

For every hot path, state: rows involved today, rows at +3 years, concurrency at peak,
and the access pattern. Then design.

The three recurring failures, all cheap to prevent and expensive to fix after P7:

1. **The unbounded query.** Any list without server-side paging is a defect (see
   `rules/common/performance.md`). Name the index behind every list the design promises to
   be fast.
2. **The chatty screen.** A screen making twelve calls to render is fine on a LAN and slow
   on a phone. Batch at the API boundary, and design what the screen shows while waiting.
3. **The N+1 that arrives with the second feature.** Design the query for the shape the
   screen needs, not for the entity graph.

## NF-03 — Availability means naming the failure modes

For each dependency (database, external system, queue, file share, identity provider):

| Dependency | Failure mode | Detection | System behaviour | User-visible behaviour | Recovery |
|---|---|---|---|---|---|

"Degraded mode" must be a concrete answer. When the pricing service is down, does the
order screen block, queue, or use a cached price — and who decided (`DEC-*`)?

Also state RPO and RTO with the backup and restore procedure that achieves them, and when
the restore was last rehearsed. A backup whose restore has never been tested is a belief.

## NF-04 — Security architecture is a design, not a checklist

Per `rules/common/security.md`, decide and document:

- the identity model and session lifetime;
- the authorisation model — roles, permissions, and **the layer where each is enforced**;
- data classification per entity, and what that implies for logging, exports and fixtures;
- audit: which operations, with what fields, retained how long, readable by whom;
- secrets: where they live, who rotates them, on what schedule.

The most common design defect: authorisation described at the screen level only. Every
operation needs its server-side check named, including the ones with no UI entry point.

## NF-05 — Operability is a first-class requirement

The system will be run by someone who did not build it. Design for them:

| Concern | What the design must state |
|---|---|
| Logging | levels, structure, correlation id, what is never logged (PII, secrets, tokens) |
| Monitoring | the signals that indicate health, and their thresholds |
| Alerting | who is paged, for what, and what the first response step is |
| Batch visibility | how an operator sees a job ran, succeeded, and processed how many rows |
| Recovery | restart, rerun, and reprocessing procedures per job and per integration |
| Runbook | `{{profile.paths.runbook}}` — the artifact ops actually reads |

A system with no operability design generates its P9 incident volume from the first week
of production, mostly as "cannot tell what happened".

## NF-06 — Capacity assumptions are dated and owned

Every growth number is an `ASM-*` with an owner. Design the scaling lever, state the limit
at which it stops working, and name what would have to change past that point. A design
that has no stated limit has an unstated one, and it will be discovered under load.

---

## Verification plan (§8)

Every row in §1 maps to an ST case, an environment and a method. Fill this in at P2, not
at P7 — the P7 team should be executing a plan, not inventing one.

| NFR | ST case | Environment | Method | Pass criterion | Evidence |
|---|---|---|---|---|---|

An NFR whose verification is "manual observation" is not verified. If measuring it needs a
tool the project does not have, that is a P2 open item with a date, not a P7 surprise.

---

## Self-check

- [ ] every `NFR-*` from the SRS has a §1 row with mechanism, budget and measurement
- [ ] every hot path has a stated data volume and concurrency
- [ ] every dependency has a named failure mode and a user-visible behaviour
- [ ] authorisation enforcement layer named per operation
- [ ] logging states what is never logged
- [ ] every §1 row has an ST case in §8
- [ ] capacity assumptions are `ASM-*` with owners
- [ ] Open Items present
