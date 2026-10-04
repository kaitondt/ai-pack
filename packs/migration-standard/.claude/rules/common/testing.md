# Common Testing

## What a migration test suite is for

Not "does the code work" but **"does the new system do what the old one did"**. That
reframing changes what to test and how to source expectations.

## Sourcing expectations

Expected values come from the legacy system, in this order of authority:

1. Legacy output captured from a real run (report file, DB state, screen capture)
2. Legacy source code read directly
3. A written client decision

Never from what the new implementation currently returns. A test written by observing the
new code passes forever and proves nothing.

## Layers

| Layer | Scope | Owner phase |
|---|---|---|
| Unit | one function/handler/validator, no I/O | P5 |
| Integration | one feature across real boundaries, seeded data | P6 |
| End-to-end | one user journey through the real UI | P6 |
| Parallel run | legacy vs target on the same input set | P6/P7 |

Parallel run is the migration-specific layer and usually the most convincing evidence the
client will accept. Design for it early: deterministic ordering, fixed clock, seeded
identifiers.

## Test case design

- One assertion subject per test; name states the condition and the expectation.
- Cover, for every migrated function: happy path, each validation branch, each error
  branch with its MSG-ID, boundary values from the legacy field definitions, and the
  authorisation cases.
- Numeric behaviour deserves explicit cases: rounding direction, truncation, precision,
  and sign handling. Legacy platforms differ from modern ones here more often than teams
  expect.
- Empty, single-row and page-boundary cases for every list.

## Determinism

- No wall-clock, no random, no network in unit tests. Inject them.
- No dependence on test execution order or on data left by another test.
- Prefer explicit waits on state over timeouts.

## Coverage

Coverage is a floor, not a goal. The real gate is the traceability one:
**every function design has at least one test case, and every test case names the design
item it verifies** (`../migration/traceability.md` TR-03).
