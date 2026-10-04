# RULE FAMILY: VERIFY BEFORE TRUST

> AI-generated code is fluent. Fluency is not correctness, and in vibe coding the human often
> reads less of the code than they would have written. So the pack moves the trust from the
> code to the **evidence**: what was run, what it showed, and whether that matches the intent.
>
> Derived from `sdlc-standard` `rules/common/testing.md` (expected values from the spec) and
> the "report honestly" rule shared by all packs, plus the failure modes specific to
> AI-written code: invented APIs, invented packages, and tests bent until they pass.

## VT-01 — Nothing is done until it has been seen running

A slice is done when **every done-when check of that slice was executed, and its output
observed** — the page loaded, the request returned, the test ran. "The code looks right" and
"it compiles" are not done.

When a check cannot be run here (needs a device, a paid API, a human eye), say so explicitly
and hand it to the human as a numbered step. Never mark it passed.

## VT-02 — The diff is read before it is accepted

At stage `prototype` and above, every slice ends with a **diff summary** for the human: files
changed, what each change does in one line, anything surprising. The human's acceptance is of
something they have seen.

A slice whose diff contains a change the summary does not explain is not finished.

## VT-03 — No phantom dependencies, no phantom APIs

AI models invent package names, function signatures and config keys that look exactly right.
Before depending on one:

| Introducing | Verify |
|---|---|
| a new package | it exists in the registry under that exact name; it is the package you think it is (owner, downloads, last release); pinned version; licence compatible with `{{profile.security.allowed_licenses}}` |
| an API / method / option of a library | it exists **in the installed version** — read the type definitions, the source in the dependency folder, or the version's docs; not memory |
| a CLI flag, env var or config key | the tool's `--help` or docs for the installed version |

A plausible package name that does not exist is an invitation for someone to register it
(typosquatting / "slopsquatting"). Installing it is a supply-chain incident.

Adding a dependency that is not trivially replaceable is a decision (IF-05).

## VT-04 — Expected values come from the intent, never from the output

A test's expected value is derived from the intent's done-when checks, `PRODUCT.md`, or a
recorded decision. **Never** by running the code and pasting what it returned — that test
passes forever and proves only that the code does what the code does.

Where the intent is silent on the expected value, that is an open question (IF-04), not a
test to be written by observation.

## VT-05 — Checks are never bent to go green

To make a failing check pass, the code changes — never the check. Specifically forbidden
without a `DEC-*` that the human approved:

- deleting, skipping (`.skip`, `xit`, `@Ignore`, `pytest.mark.skip`) or commenting out a test
- loosening an assertion (`toEqual` → `toBeTruthy`, exact → `contains`, removing a field)
- widening a type to `any` / `object` / `# type: ignore` to silence the checker
- disabling a lint rule inline to pass lint
- wrapping the failing call in `try/catch` that swallows the error
- mocking the unit under test

A green run obtained this way is worse than a red one: it certifies the defect.

## VT-06 — Report exactly what happened

- A check that ran and failed is reported **failed**, with its output.
- A check that was not run is reported **not run**, with the reason — never as passed.
- A build that "mostly works" is a failing build.
- "Should work", "this will fix it" and "done ✅" before running are forbidden phrasings.

## VT-07 — Every fixed bug leaves a check behind

A bug is fixed when the code changes **and** a check exists that fails on the old code and
passes on the new — a test from stage `mvp`, a recorded manual step before that. Without it the
same bug is re-introduced by the next prompt that rewrites the file, which in vibe coding is
soon.

## VT-08 — Verification is proportional to the stage

| Check | spike | prototype | mvp | production |
|---|---|---|---|---|
| Done-when checks executed (VT-01) | ✅ | ✅ | ✅ | ✅ |
| Diff summary shown (VT-02) | — | ✅ | ✅ | ✅ |
| Build / typecheck / lint green | — | ✅ | ✅ | ✅ |
| Core-flow checks automated | — | — | ✅ | ✅ |
| Full test suite green before commit | — | — | ✅ | ✅ |
| Independent review of each slice (`/vibe-review`) | — | on request | ✅ | ✅ |
| CI runs the suite on every push | — | — | ✅ | ✅ |
| E2E smoke on a production-like environment before release | — | — | — | ✅ |

`{{profile.verification}}` may **add** checks to a stage; it may not remove the ones marked here.

## Self-check before reporting a slice done

- [ ] Every done-when check was run, and the report shows what it showed
- [ ] Any check not run is listed as not run, with why
- [ ] Every new package and API was verified against the installed version
- [ ] No test, assertion, type or lint rule was weakened to get green
- [ ] Expected values trace to the intent, not to the output
