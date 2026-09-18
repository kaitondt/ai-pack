# AI Pack — Claude Code Skill Packs

A set of **project-agnostic Claude Code skill packs** for delivering and managing software
projects. Each pack is a drop-in `.claude/` folder plus one profile file: the methodology lives
in the pack, and everything project-specific (stack, IDs, paths, gates, templates) lives in
the profile.

| Pack | Use it for | Prefix | Skills | Commands | Agents |
|---|---|---|---|---|---|
| [`sdlc-standard`](sdlc-standard/README.md) | Building something new (greenfield or a new subsystem), P0 Inception → P9 Maintenance | `sdlc_` | 32 | 36 | 14 |
| [`migration-standard`](migration-standard/README.md) | Rewriting or replatforming a legacy system where behaviour must be preserved | `mig_` | 27 | 30 | 14 |
| [`pm-standard`](pm-standard/README.md) | Managing the project itself (PMBOK-aligned): charter, scope, cost, schedule, reporting, quality, risk, closing | `pm_` | 16 | 28 | 7 |

The two technical packs (`sdlc`, `migration`) manage the **product** — what is built and
whether it is correct. `pm-standard` manages the **project** — what was committed, at what
cost, by which date, approved by whom — and runs alongside either of them or standalone.

---

## Shared architecture

All three packs are built the same way:

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

- **Traceability is explicit and machine-checkable** — every artifact cites its source ID.
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
| Rewriting or replatforming an existing system | `migration-standard` |
| Migration that also adds significant new capability | `migration-standard` as base, plus `sdlc_requirements`, `sdlc_nfr_design`, `sdlc_test_st` for the new parts |
| Maintaining a system either pack delivered | `sdlc-standard`, phase P9 |
| Planning, costing, reporting and governing the project | `pm-standard`, alongside a technical pack |
| Managing a project whose engineering is done elsewhere | `pm-standard` standalone |

---

## Quick start

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
