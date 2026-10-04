# AI Pack — Skill Packs for Claude Code, Codex, Gemini CLI and GitHub Copilot

A set of **project-agnostic AI skill packs** for delivering and managing software projects.
The methodology lives in the pack; everything project-specific (stack, IDs, paths, gates,
templates) lives in one profile file per project.

This repository is the **hub**: it holds the pack sources and the build scripts. Each AI's
installable build is generated from here and published in its own repository, linked below as a
git submodule.

## The packs

| Pack | Use it for | Prefix | Skills | Commands | Agents |
|---|---|---|---|---|---|
| [`sdlc-standard`](sdlc-standard/README.md) | Building something new (greenfield or a new subsystem), P0 Inception → P9 Maintenance | `sdlc-` | 33 | 37 | 14 |
| [`migration-standard`](migration-standard/README.md) | Rewriting or replatforming a legacy system where behaviour must be preserved | `mig-` | 28 | 31 | 14 |
| [`pm-standard`](pm-standard/README.md) | Managing the project itself (PMBOK-aligned): charter, scope, cost, schedule, reporting, quality, risk, closing | `pm-` | 16 | 28 | 7 |
| [`vibe-standard`](vibe-standard/README.md) | Vibe coding — building fast with AI (spike → prototype → MVP → production), with intents, small slices, evidence and guard rails | `vibe-` | 13 | 20 | 6 |

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
| GitHub Copilot (CLI, VS Code) | [ai-pack-copilot](https://github.com/kaitondt/ai-pack-copilot) | [copilot/README.md](copilot/README.md) |

### Claude Code

```bash
claude plugin marketplace add kaitondt/ai-pack-claude
claude plugin install vibe-standard@ai-pack --scope project
```

Then, in a new session: `/vibe-init`.

### Codex

```bash
git clone https://github.com/kaitondt/ai-pack-codex <dir>/ai-pack-codex
codex plugin marketplace add <dir>/ai-pack-codex
codex plugin add vibe-standard@ai-pack
```

Then copy the adoption files from `<dir>/ai-pack-codex/plugins/vibe-standard/templates/`
(`profile/vibe.profile.yaml` → `.codex/`, `rules/` → `.codex/rules/`, `AGENTS.md` → repository
root) and ask Codex to run the `vibe-init` procedure through the `vibe-workflow` skill.

### Gemini CLI

```bash
gemini extensions install https://github.com/kaitondt/ai-pack-gemini-vibe
```

Then, in `gemini`: `/vibe-init`.

### GitHub Copilot

```bash
copilot plugin marketplace add kaitondt/ai-pack-copilot
copilot plugin install vibe-standard@ai-pack-copilot
```

In VS Code: Command Palette → **Chat: Install Plugin From Source** →
`https://github.com/kaitondt/ai-pack-copilot`. Then, in chat: `/vibe-init`.

### Where each AI keeps the project files

The init command writes the profile, the rules and a context file into the project:

| AI | Profile | Rules | Context file |
|---|---|---|---|
| Claude Code | `.claude/<pack>.profile.yaml` | `.claude/rules/` | `CLAUDE.md` |
| Codex | `.codex/<pack>.profile.yaml` | `.codex/rules/` | `AGENTS.md` |
| Gemini CLI | `.gemini/<pack>.profile.yaml` | `.gemini/rules/` (imported) | `GEMINI.md` |
| GitHub Copilot | `.github/<pack>.profile.yaml` | `.github/instructions/` | `.github/copilot-instructions.md` |

Several AIs can work on the same project: initialise once, copy the filled profile to the other
AIs' locations and keep the copies identical (each AI's guard hooks read only its own profile).
Deliverables (e.g. `vibe/`, `docs/`) are shared.

---

## Shared architecture

All four packs are built the same way. `.claude/` is the canonical source; the build scripts
translate it for each AI.

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
├── sdlc-standard/  migration-standard/  pm-standard/  vibe-standard/   ← pack sources
├── scripts/
│   ├── build-claude-plugins.py      → claude/
│   ├── build-codex-plugins.py       → codex/
│   ├── build-gemini-extensions.py   → gemini/<pack>/
│   ├── build-copilot-plugins.py     → copilot/
│   ├── migrate-project-names.py     ← upgrade a 1.x project to 2.0 names
│   └── readme/                      ← README sources for generated repositories
├── claude/            (submodule → ai-pack-claude)
├── codex/             (submodule → ai-pack-codex)
├── copilot/           (submodule → ai-pack-copilot)
├── gemini/<pack>/     (submodules → ai-pack-gemini-sdlc | -migration | -pm | -vibe)
└── ECC/               (submodule → ECC)
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
