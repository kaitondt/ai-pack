---
paths:
  - "**/*.tsx"
  - "**/*.jsx"
  - "**/components/**"
  - "**/hooks/**"
  - "**/pages/**"
  - "**/routes/**"
---
# RULE FAMILY: REACT

Stack rules for React front ends. They extend `rules/typescript/typescript.md` and
`rules/common/*`; where they disagree, this file wins for React code.

**Order of authority.** A client coding standard registered in
`{{profile.target.coding_standards}}` outranks this file. Before applying a rule here, check
which kind of React application this is — a client-rendered SPA (Vite, CRA) or a
server-rendering framework (Next.js, Remix). Rules that only apply to one kind say so; never
introduce server components, server actions or framework routing into a project that does
not already use them.

**Parity outranks idiom.** In a migration, where the legacy behaviour (rounding, ordering,
trimming, collation, error order) differs from what is idiomatic here, reproduce the
legacy behaviour as the design records it (NI-02) — and never "fix" it in passing.

## RX-01 — The screen design is the component contract

- Every item in the screen design's item list maps to exactly one rendered element, in the
  design's order, with the design's label, type and state per screen mode. An element the
  design does not list is unrequested scope (NI-02).
- The physical field name in the screen design is the join key to the API field. Form field
  names, state keys and request properties use it unchanged.
- Visibility and enablement per mode (create, edit, view, and any others the design names)
  are derived from one mode value and the user's permissions, in one place — not scattered
  through `&&` conditions in the markup.

## RX-02 — Components

- Function components only. One exported component per file; the file is named after it.
- Reuse the repository's component library before writing a new control. A second date
  picker, modal or table implementation is a defect even when it looks better.
- Props are typed; no spreading of unknown props onto DOM elements.
- A component past ~200 lines, or with more than one reason to re-render, is split:
  container (data, effects) and presentation (markup).
- Keys are stable identities from the data, never the array index for a list that can be
  reordered, filtered or edited.

## RX-03 — Hooks

- Rules of hooks hold everywhere: top level only, same order every render. The lint rule
  `react-hooks/rules-of-hooks` is an error, `exhaustive-deps` is not silenced.
- An effect synchronises with something outside React. Derived values are computed during
  render (or `useMemo` when measured to be expensive), not stored in state by an effect.
- Every effect that subscribes, starts a timer or sends a request cleans up, and every
  request it starts can be aborted.
- Custom hooks start with `use`, own one concern, and return a stable shape.

## RX-04 — State

Choose the smallest scope that works, in this order: local state → lifted state → context
for rarely-changing values (theme, current user) → the repository's store. Server data is
cache, not state: fetch it through the repository's data library (TanStack Query, SWR, RTK
Query) and do not copy it into a global store.

- Never mutate state; never derive state from props by copying them.
- URL state (filters, page, sort, selected tab) lives in the URL so a reload and a shared link
  reproduce the screen.
- Unsaved-change detection is explicit when the design asks for a leave-page warning.

## RX-05 — Forms and validation

- Use the repository's form library and schema; the schema's limits equal the screen and
  interface designs' limits.
- Client-side validation is for the user's convenience. The server validates again; the
  client never assumes it did.
- Errors render where the design puts them, with the catalogue text for the MSG-ID. The
  order in which errors are reported follows the function design.
- Prevent double submission: the submit control is disabled while a request is in flight, and
  the request is idempotent where the design says so (VP-05).

## RX-06 — Data fetching and API calls

- All HTTP goes through the project's API client: base URL, authentication header, timeout,
  error mapping and retry policy in one module.
- Every fetching component renders the four states the design defines: loading, empty,
  error and data. "Nothing happened" is not a state.
- A response arriving after the user changed the input is discarded (abort, or a query key
  that includes the input).

## RX-07 — Security

- No `dangerouslySetInnerHTML` with anything that did not pass through the repository's
  sanitiser. User-provided URLs are validated for scheme before going into `href` or `src`.
- No secret in front-end code or configuration, whatever its prefix (TS-06).
- Authentication tokens are stored where the authentication design says — never moved to
  `localStorage` "for convenience".
- Permission-gated UI hides or disables what the user cannot do, **and** the server still
  enforces it. The UI check is presentation only.

## RX-08 — Accessibility and layout

- Semantic elements first (`button`, `a`, `label`, `table`); ARIA only where no element fits.
- Every input has a programmatic label; every icon-only button has an accessible name.
- Focus order and initial focus follow the screen design; a dialog traps focus and returns it.
- The layout holds at every viewport in `{{profile.target.surfaces}}` (VP-09).
- Text, labels and messages come from the message catalogue or the i18n resources, never
  inline literals in the markup.

## RX-09 — Performance

Measure before optimising. Then, in this order: avoid the waterfall (fetch in parallel,
start early), avoid shipping code that is not used (route-level splitting), avoid the
re-render (stable props, memoised context values), and only then `memo` / `useMemo` /
`useCallback`. Long lists are virtualised when the design's volumes say they will be long.

## RX-10 — Tests

- Component tests with Testing Library: query by role and label as the user would, assert
  what the user sees. No assertions on internal state or implementation details.
- The network is mocked at the boundary (MSW); the API client is real.
- Every state in RX-06 and every mode in RX-01 has a case.
- Expected texts are the catalogue texts for the MSG-IDs the design specifies.

## Review checklist

| # | Check | Rule |
|---|---|---|
| 1 | Items, order, labels and per-mode states match the screen design; nothing extra | RX-01 |
| 2 | Field names equal the design's physical names | RX-01 |
| 3 | Existing components reused; keys stable | RX-02 |
| 4 | No state set from an effect that could be derived; effects clean up | RX-03 |
| 5 | Server data in the data library, not the global store; URL state in the URL | RX-04 |
| 6 | Validation limits equal the design; double submission prevented | RX-05 |
| 7 | Loading / empty / error / data rendered; stale responses discarded | RX-06 |
| 8 | No unsanitised HTML; tokens where the auth design says; server still enforces | RX-07 |
| 9 | Labels, focus, catalogue texts; layout per surface | RX-08 |
| 10 | Tests query by role and assert visible behaviour | RX-10 |
