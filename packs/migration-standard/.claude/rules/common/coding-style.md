# Common Coding Style

Stack-neutral baseline. The stack files — `../java/java.md`, `../typescript/typescript.md`,
`../react/react.md`, `../sql/sql.md` — extend this and load only with the files they govern;
where they disagree, the stack file wins. A client coding standard registered in
`{{profile.target.coding_standards}}` outranks both, and legacy parity outranks all of them.

## Match the surroundings first

New code reads like the code next to it: same naming, same comment density, same file
layout, same error-handling idiom. A file that is stylistically obvious as "the AI-written
one" is a maintenance liability regardless of its quality.

## Naming

- Names state intent, not type or implementation. `retryBudget`, not `intRetry3`.
- Migration code frequently needs both the legacy name and the target name. Keep them in
  a mapping table (data-design deliverable), not in identifiers: `itemDate`, not
  `itemDate_ITM_YMD`.
- Abbreviations only where the domain uses them; then use them consistently everywhere.
- Booleans read as assertions: `isPosted`, `hasBackorder`, `canApprove`.

## Structure

- One responsibility per file, and a file name that predicts its contents.
- Organise by feature or bounded context, not by technical layer-of-the-week.
- Hard limit 800 lines per file; a file past ~400 usually wants splitting.
- Functions: one level of abstraction per function. Extract when the body mixes
  orchestration with detail.

## Comments

- Comment the **why**, never the what. The code says what.
- In migration code, the highest-value comment is the legacy anchor:
  `// LEG-{AREA}-{NNN}: legacy rounds half-up here (frmItemList.vb:512)`.
  Keep those; they explain otherwise-inexplicable behaviour.
- No commented-out code. It is in version control.
- No decorative banners or section art.

## Error handling

- Fail loudly at the boundary, handle deliberately inside.
- Never swallow an exception without either handling or re-raising with context.
- Error messages state what failed, with which input, and what the caller can do.
- Do not invent user-facing error text in a migration — see `../migration/no-invention.md` NI-03.

## Formatting

- The repository's formatter is the authority. Do not hand-format around it.
- No trailing whitespace; one newline at end of file; consistent line endings per repo
  configuration.

## Dependencies

- Prefer the standard library, then an existing project dependency, then a new one.
- A new dependency needs a stated reason and a licence check.
- Never pull a remote script at build or hook time.
