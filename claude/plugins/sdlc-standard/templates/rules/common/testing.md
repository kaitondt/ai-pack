# Common Testing

## What the test levels are for

Each level verifies a different specification. Confusing them is what produces a project
with thousands of tests and no confidence.

| Level | Verifies | Scope | Environment | Phase |
|---|---|---|---|---|
| Unit | the detail design | one function / handler / validator, no I/O | test | P5 |
| Integration | the basic design | one feature across real boundaries, seeded data | test | P6 |
| System | the requirements | a business process end to end, plus NFRs | staging | P7 |
| Acceptance | the business need | the client's own scenarios, their data | uat | P8 |

The binding is fixed by `{{profile.testing.levels}}` and by `../sdlc/traceability.md`
TR-03. A "system test" written per screen is an integration suite that runs too late; an
integration test that mocks every boundary is a unit test that runs too slowly.

## Sourcing expectations

Expected values come from the specification, in this order of authority:

1. The baselined requirement or design document
2. A recorded decision (`DEC-*`)
3. An external standard or interface contract

**Never from what the implementation currently returns.** A test written by running the
code and pasting the output passes forever and proves nothing. This is the single most
common way a green suite coexists with a failing UAT.

Where the specification is silent, the test cannot be written: that is an open question
(RS-01), and it is worth more than the test would have been.

## Test case design

- One assertion subject per test; the name states the condition and the expectation.
- For every function design: happy path, each validation branch, each error branch with
  its MSG-ID, boundary values from the field definitions, and the authorisation cases.
- Numeric behaviour deserves explicit cases: rounding direction, truncation, precision,
  sign handling, currency scale.
- Date behaviour deserves explicit cases: time zone, day boundaries, month ends, leap day,
  and any business calendar.
- Empty, single-row and page-boundary cases for every list.
- Concurrency cases wherever two users can touch the same record.

## Determinism

- No wall-clock, no random, no network in unit tests. Inject them.
- No dependence on test execution order or on data left by another test.
- Prefer explicit waits on state over timeouts.
- Seed data belongs in fixtures under version control, not in a database somebody set up
  by hand once.

## Coverage

Coverage is a floor, never a goal. Targets live in `{{profile.quality.targets}}`. The real
gate is the traceability one: **every design rule has at least one case, and every case
names the design item it verifies.**

A module at 95% coverage with no case for a stated business rule fails its gate. A module
at 70% coverage with every rule covered passes.

## Evidence

Levels listed in `{{profile.testing.evidence.required_for}}` produce evidence per case:
screenshots, exported data, log excerpts, measured numbers for NFRs. Evidence is named by
`{{profile.testing.evidence.naming}}` and stored under
`{{profile.testing.paths.evidence_root}}`.

A result column filled in with no evidence behind it is a claim, and at acceptance it will
be treated as one.
