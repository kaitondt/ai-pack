# Common Patterns

## Boundaries

- Domain logic does not import framework, transport or persistence types.
- Persistence and transport shapes (DTOs, DAOs, wire models) are separate types from
  domain models even when the fields currently coincide. They diverge later; migrations
  guarantee it.
- Cross-layer changes are planned before they are written — see `/mig-context-map`.

## Data flow

- Prefer explicit arguments over ambient state. Global mutable state is the leading cause
  of "works in test, fails in the second run".
- Derive rather than store. A field that can be computed from two others will eventually
  disagree with them.
- Idempotency: any operation that can be retried must be safe to retry. In migrations this
  is not optional — batch reruns and parallel-run comparisons depend on it.

## Concurrency

- Serialise on the smallest unit that preserves correctness.
- User-triggered async actions lock their trigger immediately, stay locked until the
  response resolves, and unlock in a `finally`-equivalent. Double submission is the most
  common defect class in migrated transactional screens.

## Configuration

- Configuration is injected, never read from a global at point of use.
- Environment differences live in configuration, not in branches in code.
- Every configuration key is documented in an example file committed to the repository.

## Legacy-parity patterns

| Legacy shape | Target pattern | Trap |
|---|---|---|
| Screen-scoped global variables | explicit state object per workflow | hidden cross-screen coupling |
| Server round-trip per keystroke | debounced client validation, server revalidation | dropping the server check |
| Cursor loops over a result set | set-based query | changed row order; sort must be explicit |
| Implicit numeric conversion | explicit typed conversion | rounding and truncation differences |
| Sequential batch with no restart | checkpointed batch | restart semantics must be designed, not assumed |

## Refactoring during a migration

Refactor the *target* freely. Never refactor *behaviour* — that is a scope change and
belongs in Open Items (see `../migration/no-invention.md` NI-02).
