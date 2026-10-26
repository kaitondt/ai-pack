---
paths:
  - "**/*.java"
  - "**/pom.xml"
  - "**/build.gradle"
  - "**/build.gradle.kts"
  - "**/src/main/resources/**/*.yml"
  - "**/src/main/resources/**/*.yaml"
  - "**/src/main/resources/**/*.properties"
---
# RULE FAMILY: JAVA AND SPRING BOOT

Stack rules for Java services, written for Spring Boot and valid for any layered Java
backend. They extend `rules/common/*`; where the two disagree, this file wins for Java code.

**Order of authority.** A client coding standard registered in
`{{profile.target.coding_standards}}` outranks this file — read it first and follow it where
it is stricter or simply different. The repository's own Checkstyle, Spotless, PMD or
SpotBugs configuration is the mechanical form of that standard: never weaken it to make a
change pass, and never add a suppression without a comment naming the reason and the rule.

**Parity outranks idiom.** In a migration, where the legacy behaviour (rounding, ordering,
trimming, collation, error order) differs from what is idiomatic here, reproduce the
legacy behaviour as the design records it (NI-02) — and never "fix" it in passing.

## JV-01 — The layers and their direction

`controller → service → repository/mapper`, and `domain` imported by all three, importing
none of them. A controller holds transport concerns only: binding, validation trigger,
status code, response mapping. A service holds the business rule and the transaction. A
repository or mapper holds the query.

- A controller never calls a repository or mapper directly.
- A service never returns or accepts an HTTP type (`ResponseEntity`, `HttpServletRequest`).
- An entity never leaves the service layer. Requests and responses are DTOs, and the mapping
  is explicit (hand-written or MapStruct), so a new column cannot silently become a new API
  field (`rules/common/security.md` — no internals in responses).
- The module boundary in packages matches the module boundary in the design. One
  module, one package root.

## JV-02 — Injection and component shape

- Constructor injection only; dependencies `private final`. No field injection, no setter
  injection. A class with more than five collaborators is doing two jobs.
- One public top-level type per file. Utility classes are `final` with a private
  constructor; prefer a component over a static utility when the code needs collaborators.
- Configuration is bound with `@ConfigurationProperties` into an immutable type and
  validated at startup. No `@Value` scattered through business classes, no default that
  hides a missing setting in production.

## JV-03 — Immutability and nulls

- `record` for DTOs and value objects. Fields `final` by default.
- Collections returned from public methods are unmodifiable (`List.copyOf`). Never return the
  internal collection.
- `Optional` is a return type for "may be absent". It is not a field type, not a parameter
  type, and never `Optional.get()` without a presence check — use `orElseThrow` with the
  domain exception.
- Null handling follows the data design's nullability per column. A `null` that the design
  says cannot occur is asserted, not silently defaulted.

## JV-04 — Exceptions and the error envelope

- Business failures are domain exceptions carrying the MSG-ID the design specifies. One
  `@RestControllerAdvice` maps them to the project's error envelope and status codes — the
  mapping table in the interface design is the authority, not the developer's sense of
  which status fits.
- Never catch `Exception` or `Throwable` to continue. Catch what you can handle; let the
  rest reach the advice.
- Never swallow: an empty `catch`, or a `catch` that only logs and continues, is a defect
  unless the design names the failure as ignorable.
- No stack trace, SQL, class name or exception message in a response body. Log it with a
  correlation id; return the id.

## JV-05 — Transactions

- `@Transactional` on the service method that owns the unit of work, never on a controller
  and never on a repository method the service composes.
- Read paths are `@Transactional(readOnly = true)`.
- Self-invocation bypasses the proxy: a `@Transactional` method called from the same class
  runs without a transaction. Split the class or move the boundary.
- Checked exceptions do not roll back by default. Either declare `rollbackFor` or throw
  unchecked domain exceptions.
- Side effects that cannot be rolled back — file storage, messages, mail, external calls —
  run after commit (`TransactionSynchronization` or `@TransactionalEventListener(phase =
  AFTER_COMMIT)`), with the compensation the function design specifies when they fail.
- Optimistic locking uses the version column the data design names; a lost update is
  reported with its MSG-ID, never retried silently.

## JV-06 — Validation

- Single-field validation is Bean Validation on the request DTO (`@NotNull`, `@Size`,
  `@Pattern`), triggered by `@Valid` at the controller. Limits come from the interface and
  data designs — a `@Size(max = 50)` on a column the data design sizes at 40 is a defect.
- Cross-field and code-existence checks live in the service, in the order the function
  design lists them, because the order decides which error the user sees first.
- Validation messages come from the message catalogue by MSG-ID, never inline literals.

## JV-07 — Data access

- Parameter binding only. JPA: bind parameters or criteria. MyBatis: `#{}` always; `${}` only
  for identifiers drawn from a closed whitelist in code, with a comment saying so.
- No query in a loop. Fetch the set, or batch. Watch `@OneToMany` lazy loading inside a
  loop — it is the same defect with better manners.
- Every list query is bounded: paging, or a hard limit the design states.
- Sorting includes a unique tie-breaker so paging is deterministic.
- Schema changes go through the migration tool (`rules/sql/sql.md`), never through
  `ddl-auto` outside a throwaway local profile.

## JV-08 — Concurrency, time and money

- No shared mutable state in singletons. A field on a `@Service` is a constant or a
  collaborator.
- `BigDecimal` for money and every quantity the design gives a scale; construct from a
  `String`, never from a `double`, and state the `RoundingMode` the design specifies.
  `equals` on `BigDecimal` compares scale — use `compareTo`.
- `java.time` only. The time zone is explicit and comes from the design; `LocalDateTime.now()`
  without a `Clock` is untestable and is replaced by an injected `Clock`.
- `@Async` and scheduled jobs state their executor and their failure handling; a default
  executor in production is an unbounded queue.

## JV-09 — Security specifics

- Authentication and authorisation are configured in one `SecurityFilterChain`. Every
  endpoint is denied by default and opened explicitly, with the permission the API design
  names.
- Method security (`@PreAuthorize`) or an interceptor checks the business permission
  **before** any business logic runs, on every call — a hidden button is not authorisation.
- Secrets come from the environment or the secret store named in
  `{{profile.infrastructure.secrets}}`; nothing secret in `application*.yml` in the
  repository.
- Logging never writes passwords, tokens, full card or ID numbers, or personal data the data
  design classifies as restricted.

## JV-10 — Logging

SLF4J with parameterised messages (`log.info("Saved {}", id)`), never string concatenation
and never `System.out`. Log at the boundary where the decision is made, once — not once per
layer on the way up.

## JV-11 — Tests

- JUnit 5 + AssertJ; Mockito for collaborators of the unit under test. Controllers through
  `MockMvc` or `@WebMvcTest`, asserting status, the error envelope and the MSG-ID.
- Repository and mapper tests run against the real database engine (Testcontainers or the
  project's test database), not an in-memory substitute with a different dialect — H2 passes
  SQL that PostgreSQL rejects.
- Expected values come from the specification (`rules/common/testing.md`). A test that
  stubs the class it is testing tests Mockito.
- Coverage is measured by JaCoCo against the threshold the project agreed.

## JV-12 — Build hygiene

- Build through the wrapper (`./mvnw`, `./gradlew`), at the versions the repository pins.
- No new dependency without a reason in the PR description, and never a SNAPSHOT or a
  version range in a release build.
- Lombok, MapStruct and other annotation processors are used as the repository already uses
  them — not introduced by a single change.
- Compiler warnings are not noise. A new `@SuppressWarnings` carries the reason.

## Review checklist

| # | Check | Rule |
|---|---|---|
| 1 | Controller has no business logic and no repository call | JV-01 |
| 2 | No entity in a request or response | JV-01 |
| 3 | Constructor injection, `final` dependencies | JV-02 |
| 4 | Exceptions mapped once, no swallowed `catch`, no internals in the body | JV-04 |
| 5 | Transaction boundary on the service; no self-invocation; post-commit side effects | JV-05 |
| 6 | Validation limits equal the design's limits; order matches the function design | JV-06 |
| 7 | No `${}` / string-built SQL; no query in a loop; lists bounded | JV-07 |
| 8 | `BigDecimal` from `String`, explicit rounding; `Clock` injected | JV-08 |
| 9 | Permission checked server-side before business logic | JV-09 |
| 10 | Tests on the real DB engine; expectations from the specification | JV-11 |
