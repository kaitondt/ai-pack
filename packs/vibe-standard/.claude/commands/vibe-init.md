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

## Step 5 — Generate CLAUDE.md

From the pack's `.claude/CLAUDE.md` template with profile values resolved. If a `CLAUDE.md`
exists, **append** the vibe section rather than overwriting.

## Step 6 — Check the hooks run

```bash
python --version
echo '{"tool_input":{"command":"git reset --hard"}}' | python .claude/hooks/guard-vibe-bash.py; echo "exit=$?"
```

Exit `2` means the guard works. Anything else: the hooks are not running and SB-01/SB-02
enforcement is off — see ADOPTION.md troubleshooting.

## Step 7 — Report

```
Vibe pack initialised
  Profile     : .claude/vibe.profile.yaml
  Stage       : {stage}   (reality check: public URL {y/n} · other users {y/n} · real data {y/n})
  Stack       : {language / framework / db}
  Commands    : dev {ok} · test {ok|none} · lint {ok|none} · typecheck {ok|none} · build {ok}
  Memory      : vibe/ created — PRODUCT, STATE, 4 logs, {n} intents
  Findings    : {secrets / .env not ignored / no tests / …}
  Hooks       : {working | NOT RUNNING}
  Unfilled    : {fields still <...>}
  Next        : /vibe-product (fill non-goals) → /vibe-intent → /vibe-build
```
