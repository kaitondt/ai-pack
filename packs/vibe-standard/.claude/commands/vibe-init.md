---
description: "Set up the Vibe Skill Pack on a project — new or existing: inspect the repo, ask only what cannot be inferred, write vibe.profile.yaml, create the vibe/ memory folder, generate CLAUDE.md, and set the stage honestly. Usage: /vibe-init"
---

# Initialise the Vibe pack

## Step 1 — Inspect before asking

Determine from the repository, without asking:

| Signal | Tells you |
|---|---|
| `package.json` / `pyproject.toml` / `go.mod` / `Cargo.toml` + lockfile | language, framework, package manager, **real** scripts for dev/build/test/lint |
| framework config files | framework and version |
| test files and runner config | whether tests exist, and the command |
| `.env.example`, `.gitignore` | env var names; whether `.env*` is ignored (SB-01) |
| CI config | what is already enforced |
| deploy config (`vercel.json`, `fly.toml`, Dockerfile, …) | hosting, deploy path |
| git log | project age, commit style, activity |
| `.claude/sdlc.profile.yaml` / `.claude/pm.profile.yaml` | a sibling pack is installed — read `vibe-graduation` GR-03 before continuing |
| existing `vibe/` | already initialised — run `/vibe-profile-check` instead; never overwrite |

Report what you found **before** asking.

If the repo already has **committed secrets** or `.env` not ignored, say so now as the first
finding — before anything else is set up.

## Step 2 — Ask, in one batch, only what is missing

1. **What is it** — one sentence, for whom (→ `project.one_liner`).
2. **Owner** — who decides.
3. **Stage** — and the honest questions behind it: *Does it have a public URL? Does anyone
   other than you use it? Is there real personal data?* Any yes → at least `mvp` risk (SB-07).
4. **Core flows** — the 3–7 things it must do.
5. **Stack** — only if it could not be inferred; if new, offer `vibe-scaffolding` SF-01 defaults.
6. **UI verification** — can the AI drive a browser here (Playwright / browser tool), or will
   the human look?
7. **Deploy and rollback** — how, if it deploys at all.

## Step 3 — Write the profile

Copy `profile/vibe.profile.yaml` → `.claude/vibe.profile.yaml`. Fill every field you can;
commands with the **real** scripts, each run once to confirm (SF-02). Leave `<...>` only where
the user could not answer, and list them in the report.

## Step 4 — Create the memory folder

From `{{profile.paths}}`:

```
vibe/PRODUCT.md        ← from the answers (vibe-intent-spec IN-01); non-goals left as a prompt to fill
vibe/STATE.md          ← vibe-session SN-01 template, "Now: initialised"
vibe/decisions.md      ← header + DEC-001 (stack, or "adopted vibe pack on existing repo")
vibe/debt.md           ← header row (vibe-debt-ledger DT-01)
vibe/bugs.md           ← header
vibe/backlog.md        ← header
vibe/intents/          ← empty, or one INT per existing feature (existing repo, see below)
vibe/reviews/  vibe/releases/
```

**Existing codebase:** follow `vibe-scaffolding` SF-04 — inventory, intents for existing features
(status `done`, checks to be verified), a first debt sweep (`vibe-debt-ledger` DT-02). Do not fix
anything in this command.

Ensure `.gitignore` covers `.env*` except `.env.example`, and `.claude/.slice_warned`.

## Step 5 — Choose the commit message format

`/vibe-commit` and the `guard-vibe-git` hook hold every commit to one format, and this is where the
project chooses it. Ask it as its own question — not folded into the earlier round — because the
answer is visible in every commit from now on and is awkward to change later.

1. **Read the history first.** `git log -50 --format=%s` (skip merges). If most subjects follow
   one convention — a ticket key first, Conventional Commits, a bracketed id — name it and show
   three real subjects. A team that already has a convention keeps it unless it says otherwise.
   Look for a commit-message tool too (`commitlint.config.*`, `.husky/commit-msg`,
   `.pre-commit-config.yaml` with a `commit-msg` stage, `.git/hooks/commit-msg`): it will run
   beside the pack's hook, and the two must agree.
2. **Offer the presets**, each with an example built from this project's own ids:

   | Preset | Format | Example |
   |---|---|---|
   | `id-action-summary` (default) | `{ID} {ACTION} {SUMMARY}` | `INT-003.2 ADD edit a note` |
   | `bracketed` | `[{ID}] {ACTION}: {SUMMARY}` | `[INT-003.2] ADD: edit a note` |
   | `conventional` | `{ACTION}({ID}): {SUMMARY}`, actions `feat`/`fix`/`docs`/`test`/`refactor`/`perf`/`build`/`ci`/`chore`/`revert` | `fix(BUG-004): keep the draft on reload` |
   | `existing` | the convention found in step 1 — only when one was found | three real subjects |
   | `custom` | the user's own string, from the tokens `{ID}`, `{ACTION}`, `{SUMMARY}` | — |

   `{ID}` is the id of what the change is about (the slice `INT-{NNN}.{n}`, `BUG-*`, `DEBT-*`, `DEC-*`); `{ACTION}` is what the commit does
   to it; `{SUMMARY}` is a short imperative description. Recommend `existing` when step 1 found
   a consistent convention, otherwise the default.
3. **Settle the details in the same round**, with the defaults pre-filled:
   - the action vocabulary — default `ADD`, `UPDATE`, `DELETE`, `FIX`, `REVIEW`, `CONFIRM`,
     `REFACTOR`, `REVERT`; the team may rename, add or remove words (keep them one word each);
   - the summary language (`commit.summary_language`) and maximum length (72);
   - a token for housekeeping commits with no id (`commit.no_id`, e.g. `NOID`), or none —
     then every commit needs a real id;
   - protected branches that never take a direct commit (propose the default branch when the
     team merges through pull requests);
   - whether the AI may push (default no) or amend an unpushed commit (default no).
4. **Validate before writing.** A custom format contains `{SUMMARY}`, and `{ID}` unless
   `no_id` is set; it uses no token other than the three. Build the pattern the hook will apply
   and test it on the example and on the last ten subjects from `git log`: say how many would
   pass. Old history is not rewritten — the format applies from the next commit.
5. **Write `commit:`** in the profile — `preset`, `format`, `actions` and the switches — and
   record the choice as a `DEC-*` in `{{profile.paths.decisions}}`. An existing profile that still has `slices.commit_format` is migrated here: offer its format as `custom` (`{SLICE_ID}` becomes `{ID}`), write it to `commit.format`, and delete the old key — the pack no longer reads it. When an existing commit-message tool disagrees with the chosen
   format, say so: align the tool's configuration or the profile, so one commit cannot pass one
   and fail the other.

## Step 6 — Apply the model policy

<!-- model-policy:claude -->
Resolve a model and an effort level for every `.claude/agents/vibe-*.md` from
`{{profile.execution.model_profile}}`:

| `model_profile` | heavy tier | standard tier |
|---|---|---|
| `quality` | opus · `xhigh` | opus · `high` |
| `balanced` | opus · `high` | sonnet · `medium` |
| `budget` | sonnet · `high` | sonnet · `medium` |

- **heavy** — `vibe-planner`, `vibe-reviewer`, `vibe-security-auditor`, `vibe-debugger`
- **standard** — `vibe-builder`, `vibe-verifier`

An entry in `{{profile.execution.agent_model_overrides}}` or
`{{profile.execution.agent_effort_overrides}}` wins over the table for that agent. A profile
that still sets the deprecated `execution.agent_model` and no `model_profile` reads `opus` as
`quality` and `sonnet` as `budget`; offer to replace the field.

Set each agent's `model:` and `effort:` frontmatter to the resolved values. The pack ships the
`balanced` values, so a `balanced` profile with no overrides changes no file — say so instead of
rewriting them.

Then tell the user that `{{profile.execution.intended_effort}}` is for their own session,
where the commands run: Claude Code takes the session level from `/effort`, not from the
profile, so they set it there. Agents are not affected by it.
<!-- /model-policy:claude -->

## Step 7 — Generate CLAUDE.md

From the pack's `.claude/CLAUDE.md` template with profile values resolved. If a `CLAUDE.md`
exists, **append** the vibe section rather than overwriting.

**Existing rules.** If the repo already has a `.claude/rules/` or a style guide the AI should
follow, do not overwrite it: leave the files that are not the pack's where they are, or move
them under `.claude/rules/project/` and run `/vibe-rule-register --list`. Otherwise say once
that `/vibe-rule-register` is how a rule is added later, after a correction has been given
twice — and leave `project_rules: []`. Do not interview for rules at init; there is nothing
to learn from yet.

## Step 8 — Check the hooks run

```bash
python --version
echo '{"tool_input":{"command":"git reset --hard"}}' | python .claude/hooks/guard-vibe-bash.py; echo "exit=$?"
echo '{"tool_input":{"command":"git commit --no-verify -m x"}}' | python .claude/hooks/guard-vibe-git.py; echo "exit=$?"
```

Exit `2` from both means the guards work. Anything else: the hooks are not running and
SB-01/SB-02 and GT-01..GT-08 enforcement is off — see ADOPTION.md troubleshooting.

## Step 9 — Report

```
Vibe pack initialised
  Profile     : .claude/vibe.profile.yaml
  Agent model : {{profile.execution.model_profile}} — {n} opus · {n} sonnet · {n} overridden
  Effort      : agents {n} xhigh · {n} high · {n} medium; session {{profile.execution.intended_effort}} — set with /effort
  Stage       : {stage}   (reality check: public URL {y/n} · other users {y/n} · real data {y/n})
  Stack       : {language / framework / db}
  Commands    : dev {ok} · test {ok|none} · lint {ok|none} · typecheck {ok|none} · build {ok}
  Memory      : vibe/ created — PRODUCT, STATE, 4 logs, {n} intents
  Own rules   : {n} found under .claude/rules/ and listed   (add more: /vibe-rule-register)
  Findings    : {secrets / .env not ignored / no tests / …}
  Commit      : {format}   e.g. {example}   push: {AI|user}
  Hooks       : {working | NOT RUNNING}
  Unfilled    : {fields still <...>}
  Next        : /vibe-product (fill non-goals) → /vibe-intent → /vibe-build
```
