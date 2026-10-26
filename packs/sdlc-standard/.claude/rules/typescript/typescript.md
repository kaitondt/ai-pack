---
paths:
  - "**/*.ts"
  - "**/*.tsx"
  - "**/*.mts"
  - "**/*.cts"
  - "**/tsconfig*.json"
  - "**/package.json"
---
# RULE FAMILY: TYPESCRIPT

Stack rules for TypeScript, front end and back end alike. They extend `rules/common/*`;
React-specific rules are in `rules/react/react.md` and apply on top of these.

**Order of authority.** A client coding standard registered in
`{{profile.system.coding_standards}}` outranks this file. The repository's `tsconfig`,
ESLint and Prettier configuration is its mechanical form: never loosen a compiler flag or
disable a lint rule to make a change pass. A suppression comment (`eslint-disable-next-line`,
`@ts-expect-error`) names the rule and the reason on the same line.

## TS-01 — The compiler is strict, and stays strict

- `strict: true`, plus `noUncheckedIndexedAccess` and `exactOptionalPropertyTypes` where the
  repository has them. A change never turns one off.
- No `any`. Use `unknown` at the boundary and narrow. An `any` copied from a library type is
  wrapped once, at the edge, not propagated.
- No non-null assertion (`!`) to silence the compiler. Narrow, or make the invariant explicit
  with a guard that throws.
- `@ts-ignore` is never used; `@ts-expect-error` with a reason, and only for a known upstream
  typing defect.

## TS-02 — Types follow the contract

- Types for API requests and responses are generated from, or written to match, the
  interface design — field names, optionality and nullability exactly as specified. `null`
  and `undefined` are not interchangeable when the design distinguishes absent from empty.
- Validate untrusted data at runtime where it enters (HTTP responses, `localStorage`, URL
  parameters, file contents) with a schema (zod, valibot, io-ts — whichever the repository
  uses). A type annotation on `JSON.parse` output is a claim, not a check.
- Prefer union types and discriminated unions over enums with behaviour attached; prefer
  `as const` objects over TypeScript `enum` unless the repository already uses enums.
- `type` for unions and shapes, `interface` for extendable contracts — follow the
  repository's choice where it has made one.

## TS-03 — Immutability and functions

- `const` by default; `let` only when reassignment is the point.
- Do not mutate arguments. Return new objects and arrays (`toSorted`, spread, `map`).
- `readonly` on properties and `ReadonlyArray` on parameters that must not be mutated.
- Functions take an options object past three parameters, so call sites stay readable and
  adding a parameter does not reorder the others.
- Explicit return types on exported functions; inference inside.

## TS-04 — Async

- Every promise is awaited, returned or explicitly handled. A floating promise is a defect
  (`@typescript-eslint/no-floating-promises`).
- No `async` callback passed to `forEach`. Use `for…of` for sequence, `Promise.all` for
  independent work, and a concurrency limit when the count is unbounded.
- Every network call has a timeout and an `AbortSignal` path. A request whose result can
  arrive after the user has moved on is cancelled or ignored, never applied to stale state.
- Errors are `unknown` in `catch`; narrow before reading `.message`.

## TS-05 — Errors

- Throw `Error` subclasses, never strings or plain objects.
- Map transport errors to the project's error model once, in the API client — components and
  services do not parse HTTP status codes or error bodies themselves.
- Messages shown to users come from the message catalogue by MSG-ID, never inline literals,
  and never a raw server message.

## TS-06 — Modules and dependencies

- Named exports. Default exports only where a framework requires them.
- Import through the repository's path aliases; no deep relative chains (`../../../`).
- No circular imports. A cycle means a boundary is in the wrong place.
- No new dependency for something the platform or an existing dependency does. A new
  dependency is named in the PR with its reason, and the lockfile is committed with it.
- Environment variables are read and validated in one configuration module; nothing secret
  is ever read into front-end code, whatever its prefix (`VITE_*`, `NEXT_PUBLIC_*` and
  `REACT_APP_*` values ship to every browser).

## TS-07 — Dates, numbers and text

- Money and scaled quantities never use binary floating point for arithmetic the design
  specifies with a scale. Use integer minor units or a decimal library, with the rounding
  mode from the design.
- Dates cross the wire as ISO-8601 strings with an explicit offset, or as the format the
  interface design states. Formatting for display happens in one place, in the time zone the
  design names, through `Intl` or the repository's date library — never by string slicing.
- Comparisons that users see (sorting names, searching) use `Intl.Collator` with the
  project locale; `localeCompare` without a locale differs between machines.

## TS-08 — Tests

- Vitest or Jest, as the repository uses. Test files sit where the repository puts them.
- Mock the network at the boundary (MSW or the repository's equivalent), not the module that
  calls it — a mocked API client tests the mock.
- Expected values come from the specification (`rules/common/testing.md`).
- No `.only`, no `.skip` without a ticket id in the reason, no snapshot accepted without
  reading it.

## Review checklist

| # | Check | Rule |
|---|---|---|
| 1 | No `any`, no `!`, no `@ts-ignore`; strictness unchanged | TS-01 |
| 2 | Contract types match the interface design, nullability included | TS-02 |
| 3 | Untrusted input validated at runtime | TS-02 |
| 4 | No floating promises; requests cancellable; no `async` in `forEach` | TS-04 |
| 5 | Error mapping in one place; user messages by MSG-ID | TS-05 |
| 6 | No secret in front-end configuration; new dependencies justified | TS-06 |
| 7 | No float arithmetic on scaled values; dates with explicit zone | TS-07 |
| 8 | Network mocked at the boundary; no `.only` / unexplained `.skip` | TS-08 |
