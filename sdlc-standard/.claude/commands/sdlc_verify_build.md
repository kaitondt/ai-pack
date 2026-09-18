---
description: "Verify the project builds and its checks pass, in the order the profile mandates: build order, typecheck, lint, unit tests, integration tests. Reports real output. Usage: /sdlc_verify_build [step name to start from]"
---

# Verify the build

## Step 1 — Load

`sdlc_project`. Read `{{profile.system.build}}`.

## Step 2 — Check the environment first

Before running anything: the required toolchain versions, the package manager, the
dependencies installed, and any service the tests need. Report what is missing rather than
producing a build failure that is really a setup failure — the two get confused, and the
confusion costs an hour every time.

## Step 3 — Run in order, stop at the first failure

```
{{profile.system.build.order}}      each step, in sequence
{{profile.system.build.typecheck}}
{{profile.system.build.lint}}
{{profile.system.build.test_unit}}
{{profile.system.build.test_integration}}
```

The order matters: later steps consume earlier steps' output. Running them out of order
produces confusing failures against stale artifacts.

Stop at the first failure. Continuing past a failed build produces cascading errors that
hide the real one.

## Step 4 — Parse failures into locations

For each error, produce `file:line — message`. A wall of compiler output is not a report;
the point of this command is to turn it into a list someone can act on.

Group repeated errors by root cause — one missing type generating forty errors is one
finding.

## Step 5 — Report

```
Build verification
  Environment : {tool versions found}   missing: {list}
  {step}      : {PASS|FAIL}   {duration}
  ...
  First failure : {step}
    {file}:{line} — {message}
    ... (grouped by root cause: {n} distinct behind {n} errors)
  Verdict : {PASS|FAIL}
```

**Report what actually happened.** A step that was skipped is reported as skipped, not as
passed. A step that could not run because of a missing tool is reported as not run. A build
that fails is reported as failing, with the output — never as "mostly working".

That rule exists because this command's output is quoted into gate reports, CR reports and
incident reports, where nobody re-runs it to check.
