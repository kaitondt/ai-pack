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
| [`sdlc-standard`](packs/sdlc-standard/README.md) | Building something new (greenfield or a new subsystem), P0 Inception → P9 Maintenance | `sdlc-` | 33 | 39 | 14 |
| [`migration-standard`](packs/migration-standard/README.md) | Rewriting or replatforming a legacy system where behaviour must be preserved | `mig-` | 28 | 33 | 14 |
| [`pm-standard`](packs/pm-standard/README.md) | Managing the project itself (PMBOK-aligned): charter, scope, cost, schedule, reporting, quality, risk, closing | `pm-` | 16 | 29 | 7 |
| [`vibe-standard`](packs/vibe-standard/README.md) | Vibe coding — building fast with AI (spike → prototype → MVP → production), with intents, small slices, evidence and guard rails | `vibe-` | 13 | 22 | 6 |

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

## Install

All repositories are private: the machine needs `git` credentials with access to them (for
example `gh auth login`) and **Python 3** on `PATH` as `python` (the guard hooks are Python).

Example for Claude Code, installing `vibe-standard` — swap in the pack you chose:

```bash
claude plugin marketplace add kaitondt/ai-pack-claude
claude plugin install vibe-standard@ai-pack --scope project
```

Then open a new session and run `/vibe-init` (or `/sdlc-init`, `/mig-init`, `/pm-init`).

| AI | Repository |
|---|---|
| Claude Code | [ai-pack-claude](https://github.com/kaitondt/ai-pack-claude) |
| Codex | [ai-pack-codex](https://github.com/kaitondt/ai-pack-codex) |
| Gemini CLI | `ai-pack-gemini-<pack>` (one per pack) |
| Antigravity (CLI `agy`, IDE) | [ai-pack-antigravity](https://github.com/kaitondt/ai-pack-antigravity) |
| GitHub Copilot (CLI, VS Code) | [ai-pack-copilot](https://github.com/kaitondt/ai-pack-copilot) |

The full guide is in **[docs/INSTALL.md](docs/INSTALL.md)**: installing each AI's CLI, terminal
and in-chat install for every AI, Claude Code without the plugin, installing for one project
only, and where each AI keeps the project files.

## Contributing

This repository holds the pack sources and the build scripts; the per-AI builds are generated
from it. See [CONTRIBUTING.md](CONTRIBUTING.md) for the shared architecture, the repository
layout and how to release.

---

## License

Licensed under either of

- Apache License, Version 2.0 ([LICENSE-APACHE](LICENSE-APACHE))
- MIT license ([LICENSE-MIT](LICENSE-MIT))

at your option.
