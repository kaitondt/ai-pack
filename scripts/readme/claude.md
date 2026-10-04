# AI Pack for Claude Code

This repository is the Claude Code plugin marketplace **`ai-pack`**, generated from
[kaitondt/ai-pack](https://github.com/kaitondt/ai-pack) (where the pack sources live). It offers
one plugin per pack:

| Plugin | Init command | Profile it creates |
|---|---|---|
| `sdlc-standard@ai-pack` | `/sdlc-init` | `.claude/sdlc.profile.yaml` |
| `migration-standard@ai-pack` | `/mig-init` | `.claude/migration.profile.yaml` |
| `pm-standard@ai-pack` | `/pm-init` | `.claude/pm.profile.yaml` |
| `vibe-standard@ai-pack` | `/vibe-init` | `.claude/vibe.profile.yaml` |

**Requirements:** Claude Code with plugin support, `git` (to fetch the marketplace), and
Python 3 on `PATH` as `python` (the guard hooks are Python; without it they fail silently).

Install Claude Code, then run `claude` once to sign in (Pro, Max, Team, Enterprise or Console
account):

```bash
curl -fsSL https://claude.ai/install.sh | bash          # macOS, Linux, WSL
irm https://claude.ai/install.ps1 | iex                 # Windows PowerShell
brew install --cask claude-code                         # or Homebrew
winget install Anthropic.ClaudeCode                     # or WinGet
claude --version
```

## Install as a Claude Code plugin

### 1. Add the marketplace (once per machine)

Inside Claude Code:

```text
/plugin marketplace add kaitondt/ai-pack-claude
```

or from a terminal — any of these forms works:

```bash
claude plugin marketplace add kaitondt/ai-pack-claude                          # GitHub shorthand
claude plugin marketplace add https://github.com/kaitondt/ai-pack-claude.git   # full git URL
claude plugin marketplace add <path-to>/ai-pack/claude                         # local clone (pack authors)
```

The repository is private: the machine needs git credentials that can clone it.

### 2. Install the pack(s) you need

Run this from the root of the project that will use the pack:

```bash
claude plugin install sdlc-standard@ai-pack --scope project
```

or from the chat, in a Claude Code session opened in the project:

```text
/plugin install sdlc-standard@ai-pack
```

which opens the plugin's panel — pick the **project** scope there. `/plugin` → **Discover** →
`ai-pack` browses all four packs the same way. Run `/reload-plugins` (or open a new session)
after installing.

| Scope | Where it is recorded | Use it when |
|---|---|---|
| `project` (recommended) | `<project>/.claude/settings.json` — commit it | the whole team uses the pack in this repository |
| `local` | `<project>/.claude/settings.local.json` — not committed | only you, only this repository |
| `user` (default) | `~/.claude/settings.json` | you want the pack in every repository |

**Project only:** `project` and `local` enable the plugin in this repository and nowhere else
(the plugin files sit in your user cache, but are only active where a settings file enables
them). For a repository that declares everything itself — no `marketplace add` needed on any
machine — commit the snippet in [Team setup](#team-setup-install-automatically-for-everyone).

Each pack adds roughly 4k–9k tokens of skill descriptions to every session, so enable only the
packs a project uses. `pm-standard` combines with `sdlc-standard` or `migration-standard`:
install both.

### 3. Initialise the project

In a new Claude Code session in the project, run the pack's init command (`/sdlc-init`,
`/mig-init`, `/pm-init`, `/vibe-init`; the namespaced form `/sdlc-standard:sdlc-init` also
works). It writes the profile, copies the pack's rules into `.claude/rules/`, and generates
`CLAUDE.md`. Commit what it creates. Then continue as the pack's `ADOPTION.md` describes
(`plugins/<pack>/ADOPTION.md`).

In scripts and CI (`claude -p`), use the namespaced form — `claude -p "/vibe-standard:vibe-status"`
is expanded directly, while a bare `/vibe-status` is passed to the model as text and only works
if the model decides to run it. From Git Bash on Windows, also set `MSYS_NO_PATHCONV=1`, or
Bash rewrites `/vibe-status` into a Windows path before Claude Code sees it.

To check the install: `claude plugin list` shows the pack as enabled, and a new session
prints `[sdlc] plugin root: …` (or `[migration]`, `[pm]`, `[vibe]`) followed by the profile
status.

### Team setup: install automatically for everyone

Commit this to the project's `.claude/settings.json`. Teammates who trust the folder are
offered the marketplace and the pack on their first session:

```json
{
  "extraKnownMarketplaces": {
    "ai-pack": { "source": { "source": "github", "repo": "kaitondt/ai-pack-claude" } }
  },
  "enabledPlugins": {
    "sdlc-standard@ai-pack": true,
    "pm-standard@ai-pack": true
  }
}
```

### Update and uninstall

```bash
claude plugin marketplace update ai-pack          # fetch the latest catalogue
claude plugin update sdlc-standard@ai-pack        # then restart Claude Code
claude plugin uninstall sdlc-standard@ai-pack --scope project
```

Uninstalling removes the pack's commands, skills, agents and hooks. It leaves the profile,
`.claude/rules/`, `CLAUDE.md` and every generated deliverable in the project.

In a session, `/plugin` opens the plugin manager, where marketplaces can be refreshed and
plugins updated. Installed copies only change when the pack's version is bumped.

### After updating: bring the project in line

Updating the plugin replaces the pack's commands, skills, agents and hooks. It does **not** touch
what `/<prefix>-init` copied into each project:

- `.claude/rules/` — compare it with the plugin's `templates/rules/` and copy the files that changed.
  Keep your own edits: a local rule change belongs in the pack's source, not only in one project.
- `CLAUDE.md` — regenerate the pack's section only when the release notes say its template
  changed.
- `.claude/<profile>.yaml` — run `/<prefix>-profile-check` in a new session after the restart. It reports fields a new release
  added or renamed; fill them in and run it again until it is clean.

### Upgrading a project to 2.1

2.1.0 replaces the single `execution.agent_model` with a **model and effort profile**.
Analysis, design, review and triage agents stay on Opus; production agents (implementer, tester,
infra, mockup, …) move to Sonnet, and every agent now carries an `effort:` level. See each pack's
README, "Model policy".

The plugin agents ship the `balanced` values, so they take effect as soon as the plugin is
updated. To bring the profile in line, edit `execution` in the project's profile:

```yaml
execution:
  model_profile: balanced        # quality = every agent on Opus, as before 2.1 · budget = all Sonnet
  agent_model_overrides: {}
  agent_effort_overrides: {}
  intended_effort: "xhigh"       # your session's effort; set it with /effort
```

and delete the `agent_model:` line. A profile that keeps `agent_model: opus` is read as
`quality`; `/<prefix>-profile-check` then reports the plugin agents as drift until you either
switch to `balanced` or run the `/<prefix>-init` model-policy step, which copies the agents into
`.claude/agents/` with Opus.

### Upgrading a project from 1.x to 2.0

2.0.0 renamed every command, skill, agent and hook from snake_case to kebab-case
(`/vibe_build` → `/vibe-build`, `vibe_project` → `vibe-project`). After updating the plugin,
rewrite the names in the files the pack put into the project (`CLAUDE.md`, `.claude/rules/`,
agent/skill overrides; profile keys are left alone), using the script in kaitondt/ai-pack:

```bash
python <ai-pack>/scripts/migrate-project-names.py <project>            # preview
python <ai-pack>/scripts/migrate-project-names.py <project> --apply    # write
```

Add `--docs` to also update mentions in the project's other Markdown files.

### Moving from the old marketplace source

Until 2.0.0 the marketplace lived at the root of `kaitondt/ai-pack`. It now lives in this
repository; the marketplace name (`ai-pack`) and the plugin ids (`vibe-standard@ai-pack`, ...)
are unchanged. In a project that installed from the old source:

1. In the project's `.claude/settings.json`, change `extraKnownMarketplaces.ai-pack.source.repo`
   to `kaitondt/ai-pack-claude` (skip if the file has no `extraKnownMarketplaces`).
2. Re-point the marketplace and reinstall (removing a marketplace uninstalls its plugins; the
   profile, rules, `CLAUDE.md` and deliverables in the project are not touched):

   ```bash
   claude plugin marketplace remove ai-pack
   claude plugin marketplace add kaitondt/ai-pack-claude
   claude plugin install vibe-standard@ai-pack --scope project
   ```

3. Restart Claude Code and check for the `[vibe] plugin root: ...` line.

### How the plugin install differs from the copy install

- **Hooks** come from the plugin and only act in projects that have the pack's profile
  (`.claude/<pack>.profile.yaml`). Elsewhere they are no-ops apart from a session-start hint.
- **Rules** cannot be loaded by a plugin, so `/<prefix>-init` copies them from the plugin's
  `templates/rules/` into the project's `.claude/rules/`, and generates `CLAUDE.md` from
  `templates/CLAUDE.md`.
- **Agents and skills are read-only** in the plugin cache. To change an agent's model, copy it
  into the project's `.claude/agents/`, where a project agent overrides the plugin one.
- **Do not mix both installs** in one project: a copied `.claude/settings.json` plus the plugin
  runs every hook twice.

### Troubleshooting

| Symptom | Cause / fix |
|---|---|
| `/sdlc-init` is not found | The session started before the install — restart Claude Code. Check `claude plugin list`. |
| No `plugin root:` line at session start | The plugin is disabled in this scope, or `python` is not on `PATH`. |
| Guards never block anything | The profile `.claude/<pack>.profile.yaml` does not exist yet — run the init command. |
| `marketplace add` fails | No git access to the repository, or a typo in `kaitondt/ai-pack-claude`. |
| `its network source differs from the one declared for it in settings` | A marketplace named `ai-pack` is already declared with another source (e.g. the old `kaitondt/ai-pack`, a local path, or the shorthand instead of the full URL). Fix `extraKnownMarketplaces` in settings, run `claude plugin marketplace remove ai-pack`, then add it again. |

## Copy install (without the plugin system)

The packs can also be copied straight into a project from a clone of
[kaitondt/ai-pack](https://github.com/kaitondt/ai-pack), then initialised inside Claude Code:

```bash
# Development project
cp -r packs/sdlc-standard/.claude                <your-project>/.claude
cp packs/sdlc-standard/profile/sdlc.profile.yaml <your-project>/.claude/sdlc.profile.yaml
# in Claude Code:  /sdlc-init  then  /sdlc-template-register

# Migration project
cp -r packs/migration-standard/.claude                     <your-project>/.claude
cp packs/migration-standard/profile/migration.profile.yaml <your-project>/.claude/migration.profile.yaml
# in Claude Code:  /mig-init  then  /mig-template-register

# Vibe coding
cp -r packs/vibe-standard/.claude                <your-project>/.claude
cp packs/vibe-standard/profile/vibe.profile.yaml <your-project>/.claude/vibe.profile.yaml
# in Claude Code:  /vibe-init  then  /vibe-intent "..."  →  /vibe-plan  →  /vibe-build

# Project management (merge into an existing .claude/ if a technical pack is installed)
cp -r packs/pm-standard/.claude              <your-project>/.claude
cp packs/pm-standard/profile/pm.profile.yaml <your-project>/.claude/pm.profile.yaml
# in Claude Code:  /pm-init
```

When combining `pm-standard` with a technical pack, merge the `.claude/` folders rather than
overwriting — see `plugins/pm-standard/ADOPTION.md`. `/pm-init` detects the installed technical
pack automatically.

**Requirements:** Python 3 for the guard hooks (without it they fail silently and the
protections are off), plus `openpyxl` / `python-docx` if deliverables are Excel or Word. Each
pack's `ADOPTION.md` covers installation and troubleshooting.

## For pack maintainers

Everything in this repository is **generated** by `scripts/build-claude-plugins.py` in
kaitondt/ai-pack, where this repository is the `claude/` submodule. Edit the packs there, then
rebuild, validate, and publish:

```bash
python scripts/build-claude-plugins.py
claude plugin validate ./claude
git -C claude add -A && git -C claude commit -m "..." && git -C claude push
git add claude && git commit -m "Bump Claude plugins"
```

Bump `VERSION` in `scripts/build-claude-plugins.py` when releasing; installed copies only update
when the version changes. Users then run `claude plugin marketplace update ai-pack` and
`claude plugin update <pack>@ai-pack`. This README's source is `scripts/readme/claude.md`.
