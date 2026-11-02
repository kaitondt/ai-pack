# Adoption Guide

Getting the Vibe Skill Pack running. About 20 minutes on a new repo; plan an hour on an
existing vibe-coded one, most of it spent looking honestly at what is there.

---

## 0. Prerequisites

| # | What | Why |
|---|---|---|
| 1 | **Git** | checkpoints, slice IDs in commits, `attempt/*` branches — the pack is built on them |
| 2 | **Node.js 18+** and **Claude Code** | runs the pack |
| 3 | **Python 3.9+** | the four hooks are Python. **Without it they fail silently** — secrets and destructive commands are then not blocked |
| 4 | *(recommended)* a browser the AI can drive — Playwright, or a browser tool | so "seen running" for UI work does not always need a human |

Installing Git, Node, Claude Code and Python from nothing on macOS, Windows and Linux is covered
step by step in [`sdlc-standard/ADOPTION.md` §0](../sdlc-standard/ADOPTION.md) — the same
steps apply here. On Windows, make sure `python --version` prints a version rather than opening
the Microsoft Store (*Settings → Apps → App execution aliases*).

Playwright, if you want it:

```bash
npm init playwright@latest        # or: pip install playwright && playwright install
```

---

## 1. Install

### New or empty `.claude/`

```bash
cp -r vibe-standard/.claude                 <your-project>/.claude
cp vibe-standard/profile/vibe.profile.yaml  <your-project>/.claude/vibe.profile.yaml
```

### The project already has a `.claude/`

Merge, do not overwrite:

- copy `rules/vibe/`, `skills/vibe-*`, `commands/vibe-*`, `agents/vibe-*`, `hooks/*vibe*` and
  `hooks/check-slice-size.py`
- **merge** `settings.json` hook entries into the existing file — add, never replace, the
  existing `hooks` arrays
- append the pack's `CLAUDE.md` as a section (`/vibe-init` does this)

### Alongside `pm-standard`

Works as is: install both, run `/pm-init` with `technical_pack: none`. The PM pack manages
commitments, cost and reporting; this pack keeps the engineering loop honest. Both use
`DEC-{NNN}` — **point both at the same decision log** (`paths.decisions` here,
`paths.decision_log` there) so there is one sequence.

### Alongside `sdlc-standard`

Not recommended for the same codebase: the two packs answer "what is the source of truth?"
differently (an approved requirement vs. the owner's intent). Use `/vibe-graduate handoff` to
move from this pack to `sdlc-standard`, rather than running both.

---

## 2. Initialise

Inside Claude Code, in the project:

```
/vibe-init
```

It inspects the repo, asks only what it cannot infer (one batch), writes the profile, creates
`vibe/`, and generates `CLAUDE.md`. Answer the stage questions honestly — *public URL? other
users? real personal data?* — because they decide which security rules are in force.

Then:

```
/vibe-profile-check
```

Fix anything Critical before building. Two Criticals matter most: `.env` not ignored, and
**hooks not running**.

---

## 3. First slice

New project:

```
/vibe-scaffold                    ← boring stack, DEC-001, lint/test wired, real commands
/vibe-product                     ← one page; insist on three non-goals
/vibe-intent "sign up and sign in"
/vibe-plan INT-{NNN}
/vibe-build INT-{NNN}.1
/vibe-handoff
```

Existing vibe-coded repo — follow [COMMAND-FLOW.md §5](COMMAND-FLOW.md): retrofit tooling
without fixing, intents for existing features, `/vibe-verify all`, `/vibe-debt sweep`,
`/vibe-security-check`. Resist fixing things during adoption; record them. The ledger is the
plan.

---

## 4. Daily use

```
/vibe-resume   →   /vibe-build …   →   /vibe-build …   →   /vibe-handoff
```

- Talk normally. Ask for a feature in your own words — `/vibe-build` turns it into an intent
  and shows it to you before writing code. Read those four lines; it is the cheapest review
  you will ever do.
- When it starts going in circles, say so or type `/vibe-unstuck`. Do not paste the fourth
  error.
- When you have an idea mid-slice, `/vibe-park` it. Finish the slice.
- When the AI asks you a question, it is because the answer changes the code. A guess from you
  is better than a guess from it — at least it is recorded as yours.
- When you have corrected the same thing twice, make it a rule. One line goes under *Project
  conventions* in `CLAUDE.md`; a longer or file-scoped one goes through
  `/vibe-rule-register`, which writes `.claude/rules/project/<topic>.md` — a folder the pack
  never touches, so a plugin update leaves it alone. A project rule may tighten the pack's
  rules, never relax them (no loosening the secret guard, the slice size or
  verify-before-trust); the command refuses and points you at `/vibe-refine-skill`.

---

## 5. Troubleshooting

### The hooks do not seem to run

Symptom: the AI wrote a key into a file, or ran `git reset --hard`, without being blocked.

```bash
python --version
echo '{"tool_input":{"command":"git reset --hard"}}' | python .claude/hooks/guard-vibe-bash.py; echo "exit=$?"
```

- `exit=2` and a `[SB-02] BLOCKED` message → the hook works; check `settings.json` was merged
  and that the session was restarted after installing.
- `python: command not found` → install Python, or edit `settings.json` to use `python3` / `py`.
- Windows opens the Store → disable the `python.exe` app execution alias.

### The secret guard blocks a legitimate file

- A **test fixture**: use an obviously fake value — `sk_test_FAKE…`, `AKIAEXAMPLE…` with
  `EXAMPLE` in it, or read from an env var in the test.
- A **local env file** with a different name (`.env.dev`): add it to `security.env_files`
  **and** make sure it is gitignored.
- A **docs example**: write `<your-key>` or `sk-...`; the guard ignores placeholders.

Never work around it by splitting the key across lines or encoding it. If a real key reached a
file or the chat, rotate it.

### The bash guard blocks something I need

It is meant to. Run the command yourself in your own terminal — that is the rule (SB-02). If a
built-in pattern is wrong for your project (e.g. you use `terraform apply` against a local-only
sandbox), edit `BUILTIN` in `guard-vibe-bash.py` and record why as a `DEC-*`.

### The slice-size warning fires constantly

Either slices are genuinely too big — split them (`/vibe-plan`) — or generated files are being
counted: add their globs to `slices.exclude_from_budget`. Do not raise the budget because it
keeps firing; that is the refine loop's "illegitimate" edit.

### The session starts without knowing where we were

`vibe/STATE.md` is missing or stale. The SessionStart hook prints it when it exists. End every
session with `/vibe-handoff`.

---

## 6. FAQ

**Isn't this too much process for vibe coding?**
Each rule costs seconds: a four-line intent, a clean `git status`, a one-line `DEBT-*`. What it
buys is not having the afternoon in which the AI builds the wrong thing well, the evening in
which each fix breaks something else, and the day a key leaks. At `spike` almost everything is
off.

**Can I skip intents for tiny changes?**
A tiny change is a one-slice intent — four lines. The value is less the file than the moment
the AI restates what it is about to do and you can say "no, not that".

**Why does the AI keep asking me questions?**
IF-04: when the answer changes the code, it asks instead of guessing. If it asks about things
that do not matter, that is a refine-loop finding — tell it, and it goes into `CLAUDE.md`.

**What model should I run?**
<!-- model-policy:claude -->
See README "Model policy". `balanced` by default: Opus at `high` effort for the planner,
reviewer, security auditor and debugger, Sonnet at `medium` for the builder and verifier.
<!-- /model-policy:claude -->

**When should I leave this pack?**
When someone other than the owner has to approve what gets built, when there are contracts or
investors to report to, or when the team passes ~5 people. `/vibe-graduate handoff`.
