# AI Pack — Claude Code Skill Packs

A set of **project-agnostic Claude Code skill packs** for delivering and managing software
projects. Each pack is a drop-in `.claude/` folder plus one profile file: the methodology lives
in the pack, and everything project-specific (stack, IDs, paths, gates, templates) lives in
the profile.

| Pack | Use it for | Prefix | Skills | Commands | Agents |
|---|---|---|---|---|---|
| [`sdlc-standard`](sdlc-standard/README.md) | Building something new (greenfield or a new subsystem), P0 Inception → P9 Maintenance | `sdlc_` | 33 | 37 | 14 |
| [`migration-standard`](migration-standard/README.md) | Rewriting or replatforming a legacy system where behaviour must be preserved | `mig_` | 28 | 31 | 14 |
| [`pm-standard`](pm-standard/README.md) | Managing the project itself (PMBOK-aligned): charter, scope, cost, schedule, reporting, quality, risk, closing | `pm_` | 16 | 28 | 7 |
| [`vibe-standard`](vibe-standard/README.md) | Vibe coding — building fast with AI (spike → prototype → MVP → production), with intents, small slices, evidence and guard rails | `vibe_` | 13 | 20 | 6 |

The two technical packs (`sdlc`, `migration`) manage the **product** — what is built and
whether it is correct. `pm-standard` manages the **project** — what was committed, at what
cost, by which date, approved by whom — and runs alongside either of them or standalone.
`vibe-standard` takes the parts of `sdlc` and `pm` that survive at vibe speed and manages the
**loop** — intent → slice → run → verify → commit — then hands a project over to them via
`/vibe_graduate` when it outgrows vibe coding.

---

## Shared architecture

All four packs are built the same way:

```
<pack>/
├── README.md             ← what the pack is, its invariant rules, phase/area model
├── ADOPTION.md           ← ~30-minute onboarding for a new project
├── COMMAND-FLOW.md       ← how the commands chain, and the refine loop
├── profile/
│   ├── <pack>.profile.yaml   ← template: the ONLY file you edit per project
│   ├── PROFILE-SCHEMA.md     ← field-by-field spec
│   └── examples/             ← worked profiles for typical project shapes
└── .claude/
    ├── CLAUDE.md         ← project-instruction template
    ├── settings.json
    ├── hooks/            ← guard hooks (Python 3)
    ├── rules/            ← invariant standards, loaded for every task
    ├── skills/           ← phase/area knowledge, loaded on demand
    ├── commands/         ← slash-command entry points
    └── agents/           ← delegated workers with narrow tool sets
```

Skills never hardcode project values. They write `{{profile.*}}` tokens that the spine skill
(`sdlc_project`, `mig_project`, `pm_project`) resolves from the profile at load time.

Principles common to all packs:

- **Traceability is explicit and machine-checkable** — every artifact cites its source ID
  (in `vibe-standard`, lightly: intent → slice → commit → check).
- **Baselines are change-controlled** — approved documents change only through a CR.
- **No invention** — nothing is specified without an anchor (legacy source, requirement,
  recorded decision, or approved change); otherwise it is an open question or a labelled
  assumption.
- **No deliverable templates shipped** — the client's own forms (Excel/Word/Markdown/CSV) are
  registered and outrank the pack's skeleton.
- **Agents run on `model: opus`** by default, because the failure modes are silent.

---

## Which pack do I want?

| Situation | Pack |
|---|---|
| Building something new | `sdlc-standard` |
| Building fast with AI — prototype, side project, MVP, internal tool | `vibe-standard` |
| A vibe-coded product that now has contracts, investors or a growing team | `vibe-standard` → `/vibe_graduate handoff` to `sdlc` / `pm` |
| Rewriting or replatforming an existing system | `migration-standard` |
| Migration that also adds significant new capability | `migration-standard` as base, plus `sdlc_requirements`, `sdlc_nfr_design`, `sdlc_test_st` for the new parts |
| Maintaining a system either pack delivered | `sdlc-standard`, phase P9 |
| Planning, costing, reporting and governing the project | `pm-standard`, alongside a technical pack |
| Managing a project whose engineering is done elsewhere | `pm-standard` standalone |

---

## Install as a Claude Code plugin

This repository is a Claude Code plugin marketplace named **`ai-pack`**, published at
<https://github.com/kaitondt/ai-pack>. It offers one plugin per pack:

| Plugin | Init command | Profile it creates |
|---|---|---|
| `sdlc-standard@ai-pack` | `/sdlc_init` | `.claude/sdlc.profile.yaml` |
| `migration-standard@ai-pack` | `/mig_init` | `.claude/migration.profile.yaml` |
| `pm-standard@ai-pack` | `/pm_init` | `.claude/pm.profile.yaml` |
| `vibe-standard@ai-pack` | `/vibe_init` | `.claude/vibe.profile.yaml` |

**Requirements:** Claude Code with plugin support, `git` (to fetch the marketplace), and
Python 3 on `PATH` as `python` (the guard hooks are Python; without it they fail silently).

### 1. Add the marketplace (once per machine)

Inside Claude Code:

```text
/plugin marketplace add kaitondt/ai-pack
```

or from a terminal — any of these forms works:

```bash
claude plugin marketplace add kaitondt/ai-pack                          # GitHub shorthand
claude plugin marketplace add https://github.com/kaitondt/ai-pack.git   # full git URL
claude plugin marketplace add F:/2.AI/ai-pack                           # local clone (for pack authors)
```

If the repository is private, the machine needs git credentials that can clone it.

### 2. Install the pack(s) you need

Run this from the root of the project that will use the pack:

```bash
claude plugin install sdlc-standard@ai-pack --scope project
```

or, inside Claude Code, `/plugin` → **Discover** → `ai-pack` → pick the pack → choose the
scope. Restart Claude Code (or open a new session) after installing.

| Scope | Where it is recorded | Use it when |
|---|---|---|
| `project` (recommended) | `<project>/.claude/settings.json` — commit it | the whole team uses the pack in this repository |
| `local` | `<project>/.claude/settings.local.json` — not committed | only you, only this repository |
| `user` (default) | `~/.claude/settings.json` | you want the pack in every repository |

Each pack adds roughly 4k–9k tokens of skill descriptions to every session, so enable only the
packs a project uses. `pm-standard` combines with `sdlc-standard` or `migration-standard`:
install both.

### 3. Initialise the project

In a new Claude Code session in the project, run the pack's init command (`/sdlc_init`,
`/mig_init`, `/pm_init`, `/vibe_init`; the namespaced form `/sdlc-standard:sdlc_init` also
works). It writes the profile, copies the pack's rules into `.claude/rules/`, and generates
`CLAUDE.md`. Commit what it creates. Then continue as the pack's `ADOPTION.md` describes.

In scripts and CI (`claude -p`), use the namespaced form — `claude -p "/vibe-standard:vibe_status"`
is expanded directly, while a bare `/vibe_status` is passed to the model as text and only works
if the model decides to run it. From Git Bash on Windows, also set `MSYS_NO_PATHCONV=1`, or
Bash rewrites `/vibe_status` into a Windows path before Claude Code sees it.

To check the install: `claude plugin list` shows the pack as enabled, and a new session
prints `[sdlc] plugin root: …` (or `[migration]`, `[pm]`, `[vibe]`) followed by the profile
status.

### Team setup: install automatically for everyone

Commit this to the project's `.claude/settings.json`. Teammates who trust the folder are
offered the marketplace and the pack on their first session:

```json
{
  "extraKnownMarketplaces": {
    "ai-pack": { "source": { "source": "github", "repo": "kaitondt/ai-pack" } }
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

### How the plugin install differs from the copy install

- **Hooks** come from the plugin and only act in projects that have the pack's profile
  (`.claude/<pack>.profile.yaml`). Elsewhere they are no-ops apart from a session-start hint.
- **Rules** cannot be loaded by a plugin, so `/<prefix>_init` copies them from the plugin's
  `templates/rules/` into the project's `.claude/rules/`, and generates `CLAUDE.md` from
  `templates/CLAUDE.md`.
- **Agents and skills are read-only** in the plugin cache. To change an agent's model, copy it
  into the project's `.claude/agents/`, where a project agent overrides the plugin one.
- **Do not mix both installs** in one project: a copied `.claude/settings.json` plus the plugin
  runs every hook twice.

### Troubleshooting

| Symptom | Cause / fix |
|---|---|
| `/sdlc_init` is not found | The session started before the install — restart Claude Code. Check `claude plugin list`. |
| No `plugin root:` line at session start | The plugin is disabled in this scope, or `python` is not on `PATH`. |
| Guards never block anything | The profile `.claude/<pack>.profile.yaml` does not exist yet — run the init command. |
| `marketplace add` fails | No git access to the repository, or a typo in `kaitondt/ai-pack`. |
| `its network source differs from the one declared for it in settings` | A marketplace named `ai-pack` is already declared with another source (e.g. a local path, or the shorthand instead of the full URL). Run `claude plugin marketplace remove ai-pack`, then add it again. |

### For pack maintainers

The `plugins/` folder and `.claude-plugin/marketplace.json` are **generated**. Edit the packs,
then rebuild, validate and commit:

```bash
python scripts/build_plugins.py
claude plugin validate .
```

Bump `VERSION` in `scripts/build_plugins.py` when releasing; installed copies only update when
the version changes. Users then run `claude plugin marketplace update ai-pack` and
`claude plugin update <pack>@ai-pack`.

---

## Quick start (copy install)

Copy a pack into your project, copy its profile template, then run the pack's init command
inside Claude Code:

```bash
# Development project
cp -r sdlc-standard/.claude                <your-project>/.claude
cp sdlc-standard/profile/sdlc.profile.yaml <your-project>/.claude/sdlc.profile.yaml
# in Claude Code:  /sdlc_init  then  /sdlc_template_register

# Migration project
cp -r migration-standard/.claude                     <your-project>/.claude
cp migration-standard/profile/migration.profile.yaml <your-project>/.claude/migration.profile.yaml
# in Claude Code:  /mig_init  then  /mig_template_register

# Vibe coding
cp -r vibe-standard/.claude                <your-project>/.claude
cp vibe-standard/profile/vibe.profile.yaml <your-project>/.claude/vibe.profile.yaml
# in Claude Code:  /vibe_init  then  /vibe_intent "..."  →  /vibe_plan  →  /vibe_build

# Project management (merge into an existing .claude/ if a technical pack is installed)
cp -r pm-standard/.claude              <your-project>/.claude
cp pm-standard/profile/pm.profile.yaml <your-project>/.claude/pm.profile.yaml
# in Claude Code:  /pm_init
```

When combining `pm-standard` with a technical pack, merge the `.claude/` folders rather than
overwriting — see [pm-standard/ADOPTION.md](pm-standard/ADOPTION.md). `/pm_init` detects the
installed technical pack automatically.

**Requirements:** Python 3 for the guard hooks (without it they fail silently and the
protections are off), plus `openpyxl` / `python-docx` if deliverables are Excel or Word. Each
pack's `ADOPTION.md` covers installation and troubleshooting.

---

## Other contents

| Path | What it is |
|---|---|
| [`MAPPING.md`](MAPPING.md) | Derivation record: how the original project-specific WMS pack was generalised into `migration-standard`. Kept outside the pack so it is not copied into projects. |
| `sample-project/` | Empty placeholder for trying a pack out. |
| `plugins/`, `.claude-plugin/` | Generated plugin builds and marketplace manifest — do not edit by hand. |
| `scripts/build_plugins.py` | Regenerates `plugins/` and the marketplace from the four packs. |
