# Contributing to AI Pack

This repository is the **hub**: it holds the pack sources and the build scripts. Each AI's
installable build is generated from here and published in its own repository (a git submodule).
Edit packs here; never edit the generated submodules.

## Shared architecture

All four packs live in [`packs/`](packs/README.md) and are built the same way. Their `.claude/`
folder is the **canonical source for every AI**, not a Claude-only copy: the build scripts
translate it into each AI's format.

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
├── docs/           ← INSTALL.md: install guide for users of the packs
├── scripts/
│   ├── build-claude-plugins.py      → claude/
│   ├── build-codex-plugins.py       → codex/
│   ├── build-gemini-extensions.py   → gemini/<pack>/
│   ├── build-antigravity-plugins.py → antigravity/
│   ├── build-copilot-plugins.py     → copilot/
│   ├── install-claude-project.py    ← copy a pack's .claude/ into a project (no plugin)
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

---

## Releasing

Never edit the generated submodules by hand. Edit the pack sources, then for each AI:

```bash
python scripts/build-<ai>-*.py                            # rebuild the submodule
git -C <submodule> add -A && git -C <submodule> commit -m "..." && git -C <submodule> push
git add <submodule> && git commit -m "Bump <ai> build"     # record the new pointer here
```

Bump the `VERSION` constant in the build script when a change must reach installed copies;
each AI's README describes how users then update.
