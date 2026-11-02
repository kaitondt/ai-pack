# AI Pack — Skill Packs for Claude Code, Codex, Gemini CLI, Antigravity and GitHub Copilot

A set of **project-agnostic AI skill packs** for delivering and managing software projects.
The methodology lives in the pack; everything project-specific (stack, IDs, paths, gates,
templates) lives in one profile file per project.

This repository is the **hub**: it holds the pack sources and the build scripts. Each AI's
installable build is generated from here and published in its own repository, linked below as a
git submodule.

## The packs

| Pack | Use it for | Prefix | Skills | Commands | Agents |
|---|---|---|---|---|---|
| [`sdlc-standard`](packs/sdlc-standard/README.md) | Building something new (greenfield or a new subsystem), P0 Inception → P9 Maintenance | `sdlc-` | 33 | 38 | 14 |
| [`migration-standard`](packs/migration-standard/README.md) | Rewriting or replatforming a legacy system where behaviour must be preserved | `mig-` | 28 | 32 | 14 |
| [`pm-standard`](packs/pm-standard/README.md) | Managing the project itself (PMBOK-aligned): charter, scope, cost, schedule, reporting, quality, risk, closing | `pm-` | 16 | 28 | 7 |
| [`vibe-standard`](packs/vibe-standard/README.md) | Vibe coding — building fast with AI (spike → prototype → MVP → production), with intents, small slices, evidence and guard rails | `vibe-` | 13 | 21 | 6 |

The two technical packs (`sdlc`, `migration`) manage the **product** — what is built and
whether it is correct. `pm-standard` manages the **project** — what was committed, at what
cost, by which date, approved by whom — and runs alongside either of them or standalone.
`vibe-standard` takes the parts of `sdlc` and `pm` that survive at vibe speed and manages the
**loop** — intent → slice → run → verify → commit — then hands a project over to them via
`/vibe-graduate` when it outgrows vibe coding.

### Which pack do I want?

| Situation | Pack |
|---|---|
| Building something new | `sdlc-standard` |
| Building fast with AI — prototype, side project, MVP, internal tool | `vibe-standard` |
| A vibe-coded product that now has contracts, investors or a growing team | `vibe-standard` → `/vibe-graduate handoff` to `sdlc` / `pm` |
| Rewriting or replatforming an existing system | `migration-standard` |
| Migration that also adds significant new capability | `migration-standard` as base, plus `sdlc-requirements`, `sdlc-nfr-design`, `sdlc-test-st` for the new parts |
| Maintaining a system either pack delivered | `sdlc-standard`, phase P9 |
| Planning, costing, reporting and governing the project | `pm-standard`, alongside a technical pack |
| Managing a project whose engineering is done elsewhere | `pm-standard` standalone |

---

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
| Claude Code | [ai-pack-claude](https://github.com/kaitondt/ai-pack-claude) | [claude/README.md](claude/README.md) |
| Codex | [ai-pack-codex](https://github.com/kaitondt/ai-pack-codex) | [codex/README.md](codex/README.md) |
| Gemini CLI | `ai-pack-gemini-<pack>` (one per pack) | [gemini/README.md](gemini/README.md) |
| Antigravity (CLI `agy`, IDE) | [ai-pack-antigravity](https://github.com/kaitondt/ai-pack-antigravity) | [antigravity/README.md](antigravity/README.md) |
| GitHub Copilot (CLI, VS Code) | [ai-pack-copilot](https://github.com/kaitondt/ai-pack-copilot) | [copilot/README.md](copilot/README.md) |

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

### Install for one project only

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

### Where each AI keeps the project files

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

---

## Shared architecture

All four packs live in [`packs/`](packs/README.md) and are built the same way. Their `.claude/`
folder is the **canonical source for every AI**, not a Claude-only copy: the build scripts
translate it into each AI's format. Edit packs here; never edit the generated submodules.

```
packs/<pack>/
├── README.md             ← what the pack is, its invariant rules, phase/area model
├── ADOPTION.md           ← ~30-minute onboarding for a new project
├── COMMAND-FLOW.md       ← how the commands chain, and the refine loop
├── profile/
│   ├── <pack>.profile.yaml   ← template: the ONLY file you edit per project
│   ├── PROFILE-SCHEMA.md     ← field-by-field spec
│   └── examples/             ← worked profiles for typical project shapes
└── .claude/
    ├── CLAUDE.md         ← project-instruction template
    ├── settings.json     ← hook registrations
    ├── hooks/            ← guard hooks (Python 3)
    ├── rules/            ← invariant standards, loaded for every task
    ├── skills/           ← phase/area knowledge, loaded on demand
    ├── commands/         ← slash-command entry points
    └── agents/           ← delegated workers with narrow tool sets
```

Skills never hardcode project values. They write `{{profile.*}}` tokens that the spine skill
(`sdlc-project`, `mig-project`, `pm-project`, `vibe-project`) resolves from the profile at load
time.

Principles common to all packs:

- **Traceability is explicit and machine-checkable** — every artifact cites its source ID
  (in `vibe-standard`, lightly: intent → slice → commit → check).
- **Baselines are change-controlled** — approved documents change only through a CR.
- **No invention** — nothing is specified without an anchor (legacy source, requirement,
  recorded decision, or approved change); otherwise it is an open question or a labelled
  assumption.
- **No deliverable templates shipped** — the client's own forms (Excel/Word/Markdown/CSV) are
  registered and outrank the pack's skeleton.
- **Guard hooks enforce the hard rules** (read-only paths, baselines, secrets, irreversible
  commands) and stay inactive in any repository without the pack's profile.

---

## Repository layout

```
ai-pack/
├── packs/          ← pack SOURCES: sdlc-standard/ migration-standard/ pm-standard/ vibe-standard/
├── scripts/
│   ├── build-claude-plugins.py      → claude/
│   ├── build-codex-plugins.py       → codex/
│   ├── build-gemini-extensions.py   → gemini/<pack>/
│   ├── build-antigravity-plugins.py → antigravity/
│   ├── build-copilot-plugins.py     → copilot/
│   ├── migrate-project-names.py     ← upgrade a 1.x project to 2.0 names
│   └── readme/                      ← README sources for generated repositories
├── claude/            (submodule → ai-pack-claude)
├── codex/             (submodule → ai-pack-codex)
├── copilot/           (submodule → ai-pack-copilot)
├── gemini/<pack>/     (submodules → ai-pack-gemini-sdlc | -migration | -pm | -vibe)
└── antigravity/       (submodule → ai-pack-antigravity)
```

Clone with `git clone --recurse-submodules https://github.com/kaitondt/ai-pack`, or run
`git submodule update --init` in an existing clone.

### Releasing

Never edit the generated submodules by hand. Edit the pack sources, then for each AI:

```bash
python scripts/build-<ai>-*.py                            # rebuild the submodule
git -C <submodule> add -A && git -C <submodule> commit -m "..." && git -C <submodule> push
git add <submodule> && git commit -m "Bump <ai> build"     # record the new pointer here
```

Bump the `VERSION` constant in the build script when a change must reach installed copies;
each AI's README describes how users then update.

---

## License

Licensed under either of

- Apache License, Version 2.0 ([LICENSE-APACHE](LICENSE-APACHE))
- MIT license ([LICENSE-MIT](LICENSE-MIT))

at your option.
