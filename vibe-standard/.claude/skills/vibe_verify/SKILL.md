---
name: vibe_verify
description: "Prove a slice or the whole app works — run the done-when checks, the build/typecheck/lint/test commands for the stage, drive the UI, write tests whose expected values come from the intent, and report exactly what ran and what it showed. Use for 'does it work', 'test this', 'verify', 'write tests', and at the end of every slice."
---

# Verify — Seen Running, or Not Done

> `sdlc-standard` has four test levels bound to four specifications by the V-model. A vibe
> project collapses them into one question asked at every slice — *did the done-when checks
> visibly pass?* — plus a stage-scaled set of automated checks around it. The one rule taken
> over unchanged: expected values come from the specification, never from the output.

Load `vibe_project` and the intent.

---

## VE-01 — Run the done-when checks

For each check of the slice, pick the cheapest way to **observe** it:

| The check is about | Observe it by |
|---|---|
| a function's result | a unit test, or a one-off script run, with its output shown |
| an API | an HTTP call (`curl` / test client) against the running dev server, with status and body |
| a page / UI behaviour | `{{profile.verification.ui_check}}`: drive a browser (Playwright, browser tool) and screenshot / assert — or give the human numbered steps |
| data | query the dev database after the action |
| an error path | trigger it deliberately; show the message and that nothing was saved |
| ownership / auth (SB-03) | two users; show that B cannot read/modify A's record via the UI **and the API directly** |

Record per check: ✅ with what was observed · ❌ with the output · ⏸ not run, with why and the
steps handed to the human. Never infer ✅ from reading the code.

## VE-02 — Run the stage's checks

From VT-08 and `{{profile.verification.add}}`, in this order, stopping at the first failure:

```
{{profile.commands.typecheck}} → {{profile.commands.lint}} → {{profile.commands.test}}
  → {{profile.commands.build}} → (production) {{profile.commands.test_e2e}} / {{profile.commands.smoke}}
```

Show the real output tail for failures. A command that is `""` in the profile is reported as
**not configured**, which at `mvp`+ is itself a finding.

## VE-03 — Writing tests at vibe speed

- **Test the done-when checks, not the implementation.** A test per check, named after it:
  `it("rejects an empty title with 'Title is required'")`.
- **Expected values from the intent** (VT-04). Where the intent does not say, ask — do not run
  the code to find out what to expect.
- **Prefer a few high-level tests over many mocked ones.** One test that calls the API against
  a real (test) database catches more AI-introduced breakage than ten that mock the ORM.
- **Every bug fixed gets its test** (VT-07) — written first, seen failing, then the fix.
- **Make the test fail once.** Break the code (or the expectation) deliberately and see red.
  A test that has never failed may not be testing anything.

## VE-04 — Checks are never bent (VT-05)

When a test fails, the question is "is the code wrong, or is the test's expectation wrong?"
Answer it from the intent:

- **Code wrong** → fix the code.
- **Expectation wrong** (the intent changed, or the test was written against a misreading) →
  cite the intent/decision that shows it, then change the test. That citation goes in the
  commit message.
- **Neither is clear** → it is an open question. Ask.

Never: skip, delete, loosen, `any`, swallow, or mock the unit under test to get green.

## VE-05 — AI-specific checks

After any slice with new dependencies or unfamiliar APIs:

- Every new import resolves; every new package is in the lockfile at a pinned version (VT-03)
- No call to a method/option that does not exist in the installed version — the typechecker
  helps; for untyped code, grep the dependency source
- No leftover debug code: `console.log`, `print`, `debugger`, commented-out blocks, test data
- No placeholder that reads as real: `TODO: implement`, lorem ipsum in production paths,
  `example.com`, fake API keys

## VE-06 — Report

```
Verify — INT-007.2                                     stage: prototype
  Done-when   1 ✅ edit form pre-filled (screenshot vibe/reviews/INT-007.2-1.png)
              2 ✅ save → list shows new title
              3 ❌ user B GET /api/notes/12 → 200 (expected 404)   ← output below
  Typecheck ✅  Lint ✅  Tests 11/12 ❌ (notes.spec: ownership)  Build ⏸ not reached
  AI checks   ✅ no new deps · ⚠ console.log in src/lib/notes.ts:41
  Verdict     NOT DONE — ownership check missing on GET
```

Update STATE.md "Last verified" only with checks that actually ran green.

## Self-check

- [ ] Every done-when check has ✅/❌/⏸ with evidence
- [ ] Stage commands ran in order; failures shown with output
- [ ] Tests assert the intent's expectations, and each was seen failing once
- [ ] Nothing was skipped, deleted or loosened to get green
- [ ] Debug leftovers and phantom APIs checked
