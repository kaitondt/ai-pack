# Common Patterns

## Boundaries

- Domain logic does not import framework, transport or persistence types.
- Persistence and transport shapes (DTOs, entities, wire models) are separate types from
  domain models even when the fields currently coincide. They diverge later; the first
  change request guarantees it.
- Cross-layer changes are planned before they are written — see `/sdlc-context-map`.
- A module owns its data. Another module reads it through the owner's interface, never by
  reaching into its tables. Shared tables become shared assumptions, and shared assumptions
  break in whichever release nobody was looking.

## Data flow

- Prefer explicit arguments over ambient state. Global mutable state is the leading cause
  of "works in test, fails in the second run".
- Derive rather than store. A field that can be computed from two others will eventually
  disagree with them.
- Idempotency: any operation that can be retried must be safe to retry. Users double-click,
  networks retry, batches rerun.
- State transitions are explicit and enumerated. An order that can be in any combination of
  five booleans has 32 states, of which the design describes four.

## Concurrency

- Serialise on the smallest unit that preserves correctness.
- User-triggered async actions lock their trigger immediately, stay locked until the
  response resolves, and unlock in a `finally`-equivalent. Double submission is the most
  common defect class in transactional screens, and the one UAT finds first.
- Concurrent edits need a stated policy — last-write-wins, optimistic version check, or a
  lock — and it belongs in the design, not in whatever the ORM does by default.

## Configuration

- Configuration is injected, never read from a global at point of use.
- Environment differences live in configuration, not in branches in code. A `if (env ==
  "prod")` is a test gap by construction: the production path is the one never exercised.
- Every configuration key is documented in an example file committed to the repository,
  and the environment matrix in the TSD says which environments set it.

## Interfaces with systems you do not own

For every entry in `{{profile.scope.external_systems}}`:

| Concern | Rule |
|---|---|
| Contract | pinned to a version, stored in the repository, referenced by the design |
| Failure | every call has a defined timeout, retry policy and fallback behaviour |
| Unavailability | the design says what the user sees when the other side is down |
| Data shape | validated at the boundary; never trusted because "they always send it" |
| Change | their version change is a CR on this project, not a surprise at IT |

The integration test level (P6) exists mainly for these boundaries. If it can only be
tested against the real external system, that is a project risk (`RSK-*`), not a detail.

## Refactoring

Refactor structure freely, inside a module, with tests green before and after.
Never refactor **behaviour** — that is a scope change and belongs in a change request
(`../sdlc/requirement-sourcing.md` RS-06). If a refactor changes what a test asserts, it
was not a refactor.
