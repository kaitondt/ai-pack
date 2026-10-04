# AI Pack for Google Antigravity

Four Google Antigravity plugins (Antigravity CLI `agy` and the Antigravity IDE), generated from
[kaitondt/ai-pack](https://github.com/kaitondt/ai-pack):

| Plugin | Init command | Profile it creates |
|---|---|---|
| `sdlc-standard` | `/sdlc-init` | `.agents/sdlc.profile.yaml` |
| `migration-standard` | `/mig-init` | `.agents/migration.profile.yaml` |
| `pm-standard` | `/pm-init` | `.agents/pm.profile.yaml` |
| `vibe-standard` | `/vibe-init` | `.agents/vibe.profile.yaml` |

> **Not the Gemini CLI extensions.** Antigravity has its own plugin format (`plugin.json`,
> skills, agents, rules, hooks). The `ai-pack-gemini-*` repositories are Gemini CLI extensions
> (`gemini-extension.json`) and are rejected by `agy plugin install`; use the plugins here.

## Requirements

- Antigravity CLI — macOS / Linux: `curl -fsSL https://antigravity.google/cli/install.sh | bash`;
  Windows PowerShell: `irm https://antigravity.google/cli/install.ps1 | iex`. Run `agy` once to
  sign in. The Antigravity IDE shares the same plugins.
- `git` with access to this private repository, and Python 3 on `PATH` as `python` (guard hooks).

## Install

Antigravity installs a plugin from a local directory (the IDE's Marketplace tab only lists
published plugins), so clone this repository first. Each plugin is the folder
`plugins/<pack>/` — install that folder, **not** the repository root.

Antigravity CLI:

```bash
git clone https://github.com/kaitondt/ai-pack-antigravity <dir>/ai-pack-antigravity
agy plugin install <dir>/ai-pack-antigravity/plugins/vibe-standard
agy plugin list
```

In an `agy` session (chat): `/plugin install <dir>/ai-pack-antigravity/plugins/vibe-standard`,
or `/plugin` to open the Plugins Manager.

Antigravity IDE (no CLI needed) — copy the plugin folder into the global plugins root, then
**restart** the IDE (a new plugin directory is only discovered on startup):

```bash
# macOS / Linux
cp -r <dir>/ai-pack-antigravity/plugins/vibe-standard ~/.gemini/config/plugins/
```

```powershell
# Windows PowerShell
Copy-Item -Recurse <dir>\ai-pack-antigravity\plugins\vibe-standard $HOME\.gemini\config\plugins\
```

It then appears in the agent side panel → **Customizations** → Plugins, where it can be turned
on and off.

### Project-only install

Antigravity reads plugins from the workspace's `.agents/plugins/` folder, so copying the plugin
there installs it for that project only (and the team gets it with the repository):

```bash
mkdir -p .agents/plugins
cp -r <dir>/ai-pack-antigravity/plugins/vibe-standard .agents/plugins/
```

## Update

Antigravity has no update command: `agy plugin install` copies the folder, so pull the new
version and install it again.

```bash
git -C <dir>/ai-pack-antigravity pull
agy plugin uninstall vibe-standard
agy plugin install <dir>/ai-pack-antigravity/plugins/vibe-standard
```

Antigravity IDE and project-only installs: delete the old folder
(`~/.gemini/config/plugins/vibe-standard` or `.agents/plugins/vibe-standard`), copy the new one
in its place, then **restart** the IDE.

### After updating: bring the project in line

Updating the plugin replaces the pack's commands, skills, agents and hooks. It does **not** touch
what `/<prefix>-init` copied into each project:

- `.agents/rules/` — compare it with the plugin's `templates/rules/` and copy the files that changed.
  Keep your own edits: a local rule change belongs in the pack's source, not only in one project.
- `.agents/rules/<prefix>-context.md` — regenerate the pack's section only when the release notes say its template
  changed.
- `.agents/<profile>.yaml` — run `/<prefix>-profile-check` in a new session. It reports fields a new release
  added or renamed; fill them in and run it again until it is clean.

## Adopt in a project

Run `/vibe-init` (each slash command is shipped as a skill of the same name, invoked with
`/<name>`). It writes `.agents/vibe.profile.yaml`, copies the rules into `.agents/rules/` as
always-on rules, and adds `.agents/rules/vibe-context.md` (the project context). The guard hooks
only act in a workspace that has `.agents/<profile>.yaml`.

## Choosing the model and effort

In this build every command and agent runs on the model and reasoning effort of your session —
the per-agent `model:` / `effort:` tiers of the Claude Code build do not carry over. Match the
session to the work, and switch between commands when the kind of work changes:

| Work | Commands (examples) | Model | Effort |
|---|---|---|---|
| Analysis, design, review, triage, estimating, planning | `*-generate-requirements`, `*-generate-basic-design`, `*-generate-detail-design`, `*-review-*`, `*-cr-analyze`, `*-trace-bug`, `*-uat-investigate`, `sdlc-maintain-intake`, `pm-estimate`, `pm-risk-assess`, `pm-change-assess`, `vibe-plan`, `vibe-review`, `vibe-security-check`, `vibe-fix` | your strongest | high — the highest level for fixed-price or regulated work |
| Production from an approved document | `*-implement-feature`, `*-cr-implement`, `*-generate-test`, `*-generate-testscript`, `*-generate-infra`, `*-generate-mockup`, `*-uat-fix`, `pm-report`, `pm-evm`, `vibe-build`, `vibe-verify` | a fast, capable one | medium |
| Mechanical checks | `*-verify-build`, `*-profile-check`, `*-trace-check`, `*-template-register`, `vibe-status` | the fastest | low |

Do not drop the first row to save cost: its mistakes are silent and plausible, and surface only
at review, UAT or acceptance. The `execution` block of the profile (`model_profile`, overrides)
is read only by the Claude Code build; `intended_effort` is still a useful record of the level
the team agreed.

### How to set it in Antigravity

- **Model:** pick it from the model selector under the conversation prompt box — for example
  Claude Opus (thinking) or Gemini Pro for the first row, Claude Sonnet (thinking) or Gemini
  Flash for production work, Gemini Flash for mechanical checks. Where a model is offered at
  several levels (Fast / Medium / High), the level is the effort.
- **Conversation mode:** **Planning** for the first row (the agent researches and produces a plan
  before acting); **Fast** for mechanical checks and small, local edits.
- **Antigravity CLI:** `agy --mode=plan` starts in plan mode; **Shift+Tab** cycles the mode
  mid-session; `agentMode` in `~/.gemini/antigravity-cli/settings.json` sets the default.

## Differences from the Claude plugins

- Project files live under `.agents/` instead of `.claude/`; rules are flattened to
  `.agents/rules/<group>-<name>.md` with `trigger: always_on`.
- Slash commands become skills (`/vibe-build` still works); Antigravity has no command format.
- Custom agents list Antigravity tools (`view_file`, `write_to_file`, `replace_file_content`,
  `grep_search`, `find_by_name`, `run_command`, ...) and inherit the session model.
- Only the PreToolUse guards are carried over (read-only/baseline paths, secrets, irreversible
  commands). Antigravity has no session-start event and PostToolUse cannot add context, so the
  profile-status, document-rule and slice-size hooks are not included.

## Troubleshooting

| Symptom | Cause / fix |
|---|---|
| The plugin does not appear | The folder has no `plugin.json` at its top — you installed the repository root or a Gemini CLI extension (`ai-pack-gemini-*`). Install `plugins/<pack>/` from this repository, then restart. |
| `/vibe-init` is not offered | Antigravity was not restarted after the install, or the plugin is disabled (Customizations → Plugins). |
| Guards never block anything | The workspace has no `.agents/<profile>.yaml` yet — run the init command — or `python` is not on `PATH`. Hook commands run from the plugin folder (`python ./hooks/run-hook.py ...`). |
| Rules look truncated | Always-on rules share a 20,000-token budget; over budget, Antigravity keeps them as file pointers and reads them on demand. |

Generated by `python scripts/build-antigravity-plugins.py` in ai-pack; do not edit by hand.
This README's source is `scripts/readme/antigravity.md`.
