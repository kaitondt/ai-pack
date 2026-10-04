# RULE FAMILY: LEGACY IS READ-ONLY

## LR-01 — Never modify the source system

Everything under `{{profile.legacy.root}}` is read-only for the entire project.
Read, quote, and analyse it. Never `Write`, `Edit`, reformat, "fix", or reorganise it.

This is enforced mechanically by `hooks/guard-readonly-paths.py` against
`{{profile.constraints.readonly_globs}}`. If a hook blocks you, the hook is right.

Reasons this matters more than it looks:
- the legacy system is usually still in production during the migration;
- it is the reference oracle for every parallel-run comparison;
- a reformat destroys `git blame`, the only archaeology available for undocumented code.

## LR-02 — Frozen database objects

When `{{profile.constraints.stored_procedures_readonly}}` is true, stored procedures,
views and functions are **inputs**, not code you own.

If the direct cause of a defect is inside a frozen DB object:

> **STOP.** Report: "Root cause is in `<object>`, which is frozen under project
> constraints. This needs a client decision before it can be fixed."

Do not work around it silently, and do not propose a workaround as if it were the fix —
state the root cause first, then the workaround as an option.

## LR-03 — Frozen schema

When `{{profile.constraints.db_schema_frozen}}` is true:
- no migration tooling, no auto-generated DDL, no `EnsureCreated`;
- new columns require a written client decision;
- the ORM is configured to map to the existing schema, never to shape it.

## LR-04 — Generated files

Files matching `{{profile.constraints.generated_files_glob}}` are never hand-edited.
Change the generator input and regenerate.

**Before relying on a regeneration command, verify it exists.** Hand-written files are
frequently mistaken for generated ones. Check the package scripts / build targets first;
if the generator does not exist, the file is hand-written and is edited by hand — and the
profile's `generated_files_glob` should be corrected.

## LR-05 — Analysis writes go elsewhere

Analysis output about the legacy system is written to `{{profile.paths.docs_root}}`,
never next to the legacy source. No `NOTES.md` inside the legacy tree.

## LR-06 — Submodules and vendored trees

When legacy lives in a git submodule or vendored directory, know which repository you are
in before any commit. Report file paths from the workspace root so the distinction stays
visible.
