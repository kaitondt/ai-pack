---
description: "Verify the project builds in the mandated order, then type-check and run tests. Read-only: reports failures, never edits source to make them pass. Usage: /mig-verify-build [--with-tests]"
---

# Verify the build

## Step 1 — Load

`mig-project`.

## Step 2 — Environment check

Verify the toolchain the profile implies is present and at a workable version — runtime,
package manager, SDK. A missing tool is reported as a missing tool, not as a build
failure; they need different fixes.

## Step 3 — Build in the mandated order

Run `{{profile.target.build.order}}` in sequence. **Stop at the first failure.** Later
steps consume earlier steps' output, so running on regardless produces failures that are
consequences, not causes, and hides the real one.

## Step 4 — Type-check and tests

`{{profile.target.build.typecheck}}`, then with `--with-tests`,
`{{profile.target.build.test_unit}}`.

## Step 5 — Parse and report

Convert compiler and linter output into `file:line — message`, grouped by file, most
frequent root cause first.

```
Build verification
  step 1 {command} : {pass|fail}
  ...
  Type-check : {pass|fail}   {n} errors
  Tests      : {passed}/{total}
  Verdict    : {PASS|FAIL}

  Errors:
    {file}:{line} — {message}
```

This command is **read-only**. It never edits source to make a build pass. Report the
failure and, if asked, propose the fix separately.
