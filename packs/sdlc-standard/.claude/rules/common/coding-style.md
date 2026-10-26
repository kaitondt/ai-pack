# Common Coding Style

Stack-neutral baseline. The stack files — `../java/java.md`, `../typescript/typescript.md`,
`../react/react.md`, `../sql/sql.md` — extend this and load only with the files they govern;
where they disagree, the stack file wins. A client coding standard registered in
`{{profile.system.coding_standards}}` outranks both.

## Match the surroundings first

New code reads like the code next to it: same naming, same comment density, same file
layout, same error-handling idiom. A file that is stylistically obvious as "the AI-written
one" is a maintenance liability regardless of its quality.

## Naming

- Names state intent, not type or implementation. `retryBudget`, not `intRetry3`.
- Use the domain vocabulary from `{{profile.paths.glossary}}`. When the glossary says
  "consignment", the code says `consignment` — not `shipment`, not `delivery`. A synonym
  introduced in code becomes a synonym in the API, then in the client's vocabulary, and
  then nobody can tell whether two documents are describing the same thing.
- Abbreviations only where the domain uses them; then use them consistently everywhere.
- Booleans read as assertions: `isPosted`, `hasBackorder`, `canApprove`.

## Structure

- One responsibility per file, and a file name that predicts its contents.
- Organise by feature or bounded context, not by technical layer-of-the-week.
- Hard limit 800 lines per file; a file past ~400 usually wants splitting.
- Functions: one level of abstraction per function. Extract when the body mixes
  orchestration with detail.
- The module boundary in code matches the module boundary in the design. When they drift,
  the detail design stops being navigable and the drift report starts firing (X-08).

## Comments

- Comment the **why**, never the what. The code says what.
- The highest-value comment is the requirement anchor on non-obvious behaviour:
  `// REQ-ORD-014: credit check runs before approval, not after (DEC-031)`.
  It stops a future reader from "simplifying" a rule they cannot see the reason for.
- No commented-out code. It is in version control.
- No decorative banners or section art.

## Error handling

- Fail loudly at the boundary, handle deliberately inside.
- Never swallow an exception without either handling it or re-raising with context.
- User-facing messages come from the message catalogue by MSG-ID, never typed inline.
  A message written at the call site is a message no reviewer, translator or tester can
  find.
- Internal error text states what failed, with which input, and what the caller can do.
  It never leaks internals to the user (see `security.md`).

## Formatting

- The repository's formatter is the authority. Do not hand-format around it.
- No trailing whitespace; one newline at end of file; consistent line endings per repo
  configuration.

## Dependencies

- Prefer the standard library, then an existing project dependency, then a new one.
- A new dependency needs a stated reason, a licence check, and — where it affects the
  architecture — a `DEC-*` entry.
- Never pull a remote script at build or hook time.
