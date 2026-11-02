# Installing AI Pack

Install guide for the skill packs in [AI Pack](../README.md): the AI CLIs, the per-AI install
commands, project-only installs and where each AI keeps the project files.

## Install the AI CLIs

Every install below goes through the AI's own CLI (or its chat), so install the CLI first. The
packs also need, on every machine:

- **git** with access to the private `kaitondt/ai-pack-*` repositories — e.g. install the
  GitHub CLI and run `gh auth login`;
- **Python 3** on `PATH` as `python` — the guard hooks are Python and fail silently without it.

| AI | macOS / Linux | Windows | Alternatives | First run |
|---|---|---|---|---|
| Claude Code | `curl -fsSL https://claude.ai/install.sh \| bash` | PowerShell: `irm https://claude.ai/install.ps1 \| iex` | `brew install --cask claude-code` · `winget install Anthropic.ClaudeCode` · `npm install -g @anthropic-ai/claude-code` | `claude`, sign in in the browser (Pro, Max, Team, Enterprise or Console account) |
| Codex | `curl -fsSL https://chatgpt.com/codex/install.sh \| sh` | `npm install -g @openai/codex` | `brew install --cask codex` | `codex` → **Sign in with ChatGPT** |
| Gemini CLI | `npm install -g @google/gemini-cli` (Node.js 20+) | same | `brew install gemini-cli` · `npx @google/gemini-cli` | `gemini`, sign in with Google |
| Antigravity CLI (`agy`) | `curl -fsSL https://antigravity.google/cli/install.sh \| bash` | PowerShell: `irm https://antigravity.google/cli/install.ps1 \| iex` | the Antigravity IDE (no CLI needed for the IDE install) | `agy`, sign in in the browser |
| GitHub Copilot CLI | `curl -fsSL https://gh.io/copilot-install \| bash` | `winget install GitHub.Copilot` | `npm install -g @github/copilot` (Node.js 22+) · `brew install --cask copilot-cli` | `copilot` → `/login` (needs a Copilot subscription) |

Check each with `<cli> --version` (`claude`, `codex`, `gemini`, `agy`, `copilot`). Since
2026-06-18 Gemini CLI is replaced by the Antigravity CLI for unpaid and Google One users — if
that is you, use the Antigravity plugins.

---

## Quick install

All repositories are private: the machine needs `git` credentials with access to them (for
example `gh auth login`). The guard hooks need Python 3 on `PATH` as `python`. Run the commands
from the root of your project; the examples install `vibe-standard` — swap in the pack you
chose.

| AI | Repository | Details |
|---|---|---|
| Claude Code | [ai-pack-claude](https://github.com/kaitondt/ai-pack-claude) | [claude/README.md](../claude/README.md) |
| Codex | [ai-pack-codex](https://github.com/kaitondt/ai-pack-codex) | [codex/README.md](../codex/README.md) |
| Gemini CLI | `ai-pack-gemini-<pack>` (one per pack) | [gemini/README.md](../gemini/README.md) |
| Antigravity (CLI `agy`, IDE) | [ai-pack-antigravity](https://github.com/kaitondt/ai-pack-antigravity) | [antigravity/README.md](../antigravity/README.md) |
| GitHub Copilot (CLI, VS Code) | [ai-pack-copilot](https://github.com/kaitondt/ai-pack-copilot) | [copilot/README.md](../copilot/README.md) |

Each AI can be set up from a **terminal** or from **inside the chat** (slash commands typed in
the AI's own session). Both end the same way: a new session, then the pack's init command.

### Claude Code

Terminal:

```bash
claude plugin marketplace add kaitondt/ai-pack-claude
claude plugin install vibe-standard@ai-pack --scope project
```

In chat (a Claude Code session opened in the project):

```text
/plugin marketplace add kaitondt/ai-pack-claude
/plugin install vibe-standard@ai-pack
```

The second command opens the plugin's panel: install it with the **project** scope so it is
recorded in `.claude/settings.json` for the whole team. Or browse with `/plugin` → **Discover** → `ai-pack`. Then run `/reload-plugins` (or open
a new session) and `/vibe-init`.

### Codex

Terminal:

```bash
codex plugin marketplace add kaitondt/ai-pack-codex
codex plugin add vibe-standard@ai-pack
```

In chat: the marketplace still has to be added once from a terminal (the first line above);
then, in the Codex TUI, run `/plugins`, switch to the **ai-pack** tab, select `vibe-standard` and
install it. Start a new thread afterwards.

Either way, copy the adoption files from a clone
(`git clone https://github.com/kaitondt/ai-pack-codex <dir>/ai-pack-codex`) —
`<dir>/ai-pack-codex/plugins/vibe-standard/templates/`
(`profile/vibe.profile.yaml` → `.codex/`, `rules/` → `.codex/rules/`, `AGENTS.md` → repository
root) and ask Codex in chat: *"Use the `vibe-workflow` skill to run the `vibe-init` procedure."*

### Gemini CLI

Terminal:

```bash
gemini extensions install https://github.com/kaitondt/ai-pack-gemini-vibe
```

In chat (a `gemini` session):

```text
/extensions install https://github.com/kaitondt/ai-pack-gemini-vibe
/extensions list
```

Restart `gemini` (or run `/extensions restart`) so the commands and skills load, then
`/vibe-init`.

### Antigravity

Antigravity (CLI and IDE) has its own plugin format: the Gemini CLI extensions above do **not**
install there. Clone the Antigravity build and install a plugin folder:

```bash
git clone https://github.com/kaitondt/ai-pack-antigravity <dir>/ai-pack-antigravity
agy plugin install <dir>/ai-pack-antigravity/plugins/vibe-standard
```

In chat (an `agy` session): `/plugin install <dir>/ai-pack-antigravity/plugins/vibe-standard`.
Antigravity IDE: copy `plugins/vibe-standard` into `~/.gemini/config/plugins/` (Windows:
`%USERPROFILE%\.gemini\config\plugins\`) and restart the IDE. Then run `/vibe-init` (commands are
shipped as skills of the same name).

### GitHub Copilot

Terminal (Copilot CLI):

```bash
copilot plugin marketplace add kaitondt/ai-pack-copilot
copilot plugin install vibe-standard@ai-pack-copilot
```

In chat — Copilot CLI session:

```text
/plugin marketplace add kaitondt/ai-pack-copilot
/plugin install vibe-standard@ai-pack-copilot
```

In chat — VS Code: open the Chat view → **gear icon** → **Plugins**, or run
**Chat: Install Plugin From Source** from the Command Palette with
`https://github.com/kaitondt/ai-pack-copilot.git`. To browse the marketplace there instead, add
it to the `chat.plugins.marketplaces` setting
(`"chat.plugins.marketplaces": ["https://github.com/kaitondt/ai-pack-copilot.git"]` — the
`.git` URL form works for private repositories) and install `vibe-standard` from the Plugins
list or from **Extensions → `@agentPlugins`**.

Then start a new session and run `/vibe-init`.

### Claude Code without the plugin (copy `.claude/`)

From a clone of this repository, copy one or more packs into a project (Python 3.9+, nothing
else to install):

```bash
python scripts/install-claude-project.py <project> vibe-standard
python scripts/install-claude-project.py <project> sdlc-standard pm-standard
python scripts/install-claude-project.py <project> all --dry-run     # preview only
```

It copies the pack's `.claude/` (skills, commands, agents, rules, hooks) and the profile template,
and merges the hooks into the project's `.claude/settings.json`. Existing files are kept; pass
`--force` to update a copy to a newer version (the profile, `CLAUDE.md` and `settings.json` are
never overwritten). Then run `/vibe-init` (or `/sdlc-init`, `/mig-init`, `/pm-init`). Do not
combine this with the plugin for the same pack — the hooks would run twice.

---

## Install for one project only

Only Claude Code (and Copilot in VS Code) record a true project-level install in a settings file
committed with the repository. Gemini CLI, Codex and Copilot CLI always install per machine; you
then limit where the pack is active. Either way, the guard hooks only act in a repository that
has the pack's profile — elsewhere the pack changes nothing, it only adds its skill descriptions
to the context.

| AI | Project-only? | How |
|---|---|---|
| Claude Code | **Yes** | `--scope project` (whole team, `.claude/settings.json`) or `--scope local` (only you, `.claude/settings.local.json`) |
| Copilot – VS Code | **Yes** | Commit `.github/copilot/settings.json` (below) |
| Copilot – CLI | No | Installed per machine |
| Gemini CLI | Limit it | Install, `disable --scope user`, then `enable --scope workspace` in the project |
| Codex | No | Installed per machine; or vendor the skills into `.agents/skills/` (no guard hooks) |
| Antigravity | **Yes** | Copy the plugin folder into the project's `.agents/plugins/` |

**Claude Code** — commit `.claude/settings.json` so the repository itself declares the
marketplace and the plugin; teammates are offered both when they open the project, and no other
repository has it enabled:

```json
{
  "extraKnownMarketplaces": {
    "ai-pack": { "source": { "source": "github", "repo": "kaitondt/ai-pack-claude" } }
  },
  "enabledPlugins": { "vibe-standard@ai-pack": true }
}
```

**Copilot in VS Code** — commit `.github/copilot/settings.json`; VS Code recommends the plugin
the first time a chat message is sent in the workspace:

```json
{
  "extraKnownMarketplaces": {
    "ai-pack-copilot": { "source": { "source": "github", "repo": "kaitondt/ai-pack-copilot" } }
  },
  "enabledPlugins": { "vibe-standard@ai-pack-copilot": true }
}
```

**Gemini CLI** — install once, switch it off everywhere, then on for this project:

```bash
gemini extensions install https://github.com/kaitondt/ai-pack-gemini-vibe
gemini extensions disable vibe-standard --scope user
cd <project> && gemini extensions enable vibe-standard --scope workspace
```

(In chat: `/extensions disable …` / `/extensions enable …`, then restart `gemini`.)

**Codex** — there is no project install: plugin state lives in `~/.codex/config.toml`. Install
normally (the guards stay inactive in repositories without `.codex/vibe.profile.yaml`; `/plugins`
→ Space toggles the plugin off machine-wide when you need to), or keep the pack inside the
repository by copying only its skills, which Codex reads from `.agents/skills/`:

```bash
mkdir -p .agents/skills
cp -r <dir>/ai-pack-codex/plugins/vibe-standard/skills/* .agents/skills/
```

That vendored copy has no guard hooks and must be re-copied when the pack is updated.

---

## Where each AI keeps the project files

The init command writes the profile, the rules and a context file into the project:

| AI | Profile | Rules | Context file |
|---|---|---|---|
| Claude Code | `.claude/<pack>.profile.yaml` | `.claude/rules/` | `CLAUDE.md` |
| Codex | `.codex/<pack>.profile.yaml` | `.codex/rules/` | `AGENTS.md` |
| Gemini CLI | `.gemini/<pack>.profile.yaml` | `.gemini/rules/` (imported) | `GEMINI.md` |
| Antigravity | `.agents/<pack>.profile.yaml` | `.agents/rules/` (always-on) | `.agents/rules/<prefix>-context.md` |
| GitHub Copilot | `.github/<pack>.profile.yaml` | `.github/instructions/` | `.github/copilot-instructions.md` |

Several AIs can work on the same project: initialise once, copy the filled profile to the other
AIs' locations and keep the copies identical (each AI's guard hooks read only its own profile).
Deliverables (e.g. `vibe/`, `docs/`) are shared.
