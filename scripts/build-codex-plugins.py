#!/usr/bin/env python3
"""Build Codex-native ai-pack plugins from the four canonical Claude packs.

The source methodology stays in each pack's .claude/ tree.  This builder produces
an installable Codex marketplace in codex/ without modifying the Claude release.
codex/ is the git submodule https://github.com/kaitondt/ai-pack-codex; commit and push
there after a rebuild, then commit the new submodule pointer in ai-pack.
"""
from __future__ import annotations

import json
import re
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
LICENSE = "MIT OR Apache-2.0"
LICENSE_FILES = ("LICENSE-MIT", "LICENSE-APACHE")
OUT = ROOT / "codex"
VERSION = "1.5.0"
OWNER = {"name": "ThucND", "url": "https://github.com/kaitondt"}
REPOSITORY = "https://github.com/kaitondt/ai-pack"

PACKS = (
    ("sdlc-standard", "sdlc", "sdlc.profile.yaml", "Build new software with requirements, design, traceability, testing, and gates.", ["sdlc", "requirements", "testing", "traceability"]),
    ("migration-standard", "mig", "migration.profile.yaml", "Replatform a legacy system while preserving evidenced behaviour.", ["migration", "legacy", "replatform", "traceability"]),
    ("pm-standard", "pm", "pm.profile.yaml", "Manage software project scope, estimates, schedule, risk, reporting, and change control.", ["project-management", "pmbok", "risk", "change-control"]),
    ("vibe-standard", "vibe", "vibe.profile.yaml", "Build AI-assisted products with intent, small slices, verification, debt, and stage gates.", ["vibe-coding", "mvp", "verification", "guardrails"]),
)


PRODUCT = "Codex"
# Pack sources wrap the Claude-only model/effort policy in these markers. Other builds replace
# the block with a note, after the product rename, so the note can still name Claude Code.
MODEL_POLICY = re.compile(r"<!-- model-policy:claude -->\n.*?<!-- /model-policy:claude -->\n?", re.S)
MODEL_NOTE = (
    "> **Model and effort on {product}:** the agents in this build run on the model and reasoning\n"
    "> effort selected in your session. The `model:` and `effort:` agent fields,\n"
    "> `execution.model_profile`, `agent_model_overrides` and `agent_effort_overrides` take effect\n"
    "> only in the Claude Code build of this pack, so any check comparing agent models with the\n"
    "> profile does not apply here: report it as N/A. Use your strongest model for analysis,\n"
    "> design, review and triage work, and a faster one for production work from an approved\n"
    "> document. How to set both: \"Choosing the model and effort\" in the AI Pack for\n"
    "> {product} README.\n")


def model_note(text):
    return MODEL_POLICY.sub(lambda m: MODEL_NOTE.format(product=PRODUCT), text)


# Codex has no slash commands; a pack command ships as a skill and is invoked as $<name>.
COMMAND_REF = re.compile(r"(?<![\w/.$-])/((?:sdlc|mig|pm|vibe)-[a-z][a-z-]*)")


def codex_text(text: str) -> str:
    """Make filesystem references portable to a Codex project installation."""
    text = COMMAND_REF.sub(r"$\1", text)
    return model_note(text.replace(".claude", ".codex")
                .replace("CLAUDE_PROJECT_DIR", "CODEX_PROJECT_DIR")
                .replace("CLAUDE_PLUGIN_ROOT", "PLUGIN_ROOT")
                .replace("Claude Code", "Codex")
                .replace("CLAUDE.md", "AGENTS.md"))


def copy_text_tree(source: Path, dest: Path) -> None:
    for item in source.rglob("*"):
        target = dest / item.relative_to(source)
        if item.is_dir():
            target.mkdir(parents=True, exist_ok=True)
        elif item.suffix in {".md", ".py", ".json", ".yaml", ".yml"}:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(codex_text(item.read_text(encoding="utf-8")), encoding="utf-8")
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(item, target)


def workflow_skill(prefix: str, profile: str, commands: list[str]) -> str:
    command_list = " · ".join(f"`${name}`" for name in commands)
    return f'''---
name: {prefix}-workflow
description: "Route a {prefix} pack task to the correct lifecycle workflow. Use when the user asks to start, plan, build, test, review, release, report, or assess work governed by this pack."
---

# {prefix} workflow router

1. Read `.codex/{profile}`. If it is missing, stop and tell the user to set the pack up with `${prefix}-init`.
2. Load `{prefix}-project` first, then the phase/area skill it routes to.
3. Every slash command of the Claude Code build is a skill of the same name here: `/{prefix}-init` is `${prefix}-init`. When the user names a command, with or without `/` or `$`, load that skill and follow it.
4. Follow the profile, invariant rules, and evidence/reporting requirements; do not invent project values.

Command skills: {command_list}
'''


PLUGIN_NOTE = """
> **Running as a Codex plugin:** the pack's files are not in this repository's `.codex/` —
> they live in the plugin directory (`~/.codex/plugins/cache/ai-pack/{name}/<version>/`).
> Map every "pack" path in this procedure as follows:
>
> | Pack path in this procedure | Plugin location |
> |---|---|
> | profile template `{profile}` | `<plugin>/templates/profile/{profile}` |
> | the pack's `AGENTS.md` template | `<plugin>/templates/AGENTS.md` |
> | `.codex/rules/` | `<plugin>/templates/rules/` — **copy into this project's `.codex/rules/`**. Never overwrite an existing file without asking. |
> | `.codex/hooks/*.py` | `<plugin>/hooks/` — already registered by the plugin's `hooks.json`; they act once `.codex/{profile}` exists |
> | `.codex/agents/{prefix}-*.md` | not shipped in the Codex build: where a step delegates to an agent, do that work in this session |
> | `.codex/skills/` | `<plugin>/skills/`, read-only |
> | `/{prefix}-<command>` | the skill `${prefix}-<command>` |
>
> The profile `.codex/{profile}` and everything the pack generates stay in this project.
"""

NOTE_TARGETS = ("-init.md", "-profile-check.md", "-refine-skill.md")


def split_frontmatter(text: str) -> tuple[dict, str]:
    m = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not m:
        return {}, text
    meta = {}
    for line in m.group(1).splitlines():
        key, sep, value = line.partition(":")
        if sep:
            meta[key.strip()] = value.strip()
    return meta, text[m.end():]


def command_skill(path: Path, name: str, prefix: str, profile: str) -> str:
    """A slash command becomes a skill of the same name, invoked as $<name>."""
    meta, body = split_frontmatter(path.read_text(encoding="utf-8"))
    body = codex_text(body).replace("$ARGUMENTS", "the text the user typed after the skill name")
    if path.name.endswith(NOTE_TARGETS):
        m = re.match(r"(?:\s*\n)*(#[^\n]*\n)?", body)
        note = PLUGIN_NOTE.format(name=name, prefix=prefix, profile=profile)
        body = body[:m.end()] + note + "\n" + body[m.end():]
    description = codex_text(meta.get("description", f'"{path.stem}"'))
    return f"---\nname: {path.stem}\ndescription: {description}\n---\n{body}"


def hook_launcher(profile: str) -> str:
    return f'''#!/usr/bin/env python3
"""Run a pack hook only after a Codex project has opted in with its profile.

Codex edits files through apply_patch, whose tool_input is {{"command": "<patch>"}} rather
than the file_path/content the pack hooks read. The patch is split per file and the hook runs
once per touched file with a Write-shaped tool_input, so path and secret guards still apply.
"""
import json
import os
import re
import subprocess
import sys

profile, script = sys.argv[1], sys.argv[2]
always = "--always" in sys.argv[3:]
here = os.path.dirname(os.path.abspath(__file__))
root = os.path.dirname(here)
project = os.environ.get("CODEX_PROJECT_DIR", os.getcwd())
stdin = sys.stdin.buffer.read() if not sys.stdin.isatty() else b""
if not os.path.exists(os.path.join(project, ".codex", profile)) and not always:
    raise SystemExit(0)
if always:
    print("[{{}}] plugin root: {{}}".format(profile.split(".")[0], root))
    sys.stdout.flush()
env = dict(os.environ, CODEX_PROJECT_DIR=project, PLUGIN_ROOT=root,
           CLAUDE_PROJECT_DIR=project, CLAUDE_PLUGIN_ROOT=root)
FILE_HEADER = re.compile(r"^[*]{{3}} (?:Add|Update|Delete) File: (.+)$|^[*]{{3}} Move to: (.+)$")


def patch_files(patch):
    """Return [(path, added_text)] for every file an apply_patch body touches."""
    files, current = [], None
    for line in patch.splitlines():
        m = FILE_HEADER.match(line)
        if m:
            current = [(m.group(1) or m.group(2)).strip(), []]
            files.append(current)
        elif current is not None and line.startswith("+"):
            current[1].append(line[1:])
    return [(path, "\\n".join(lines)) for path, lines in files]


def run(payload):
    return subprocess.run([sys.executable, os.path.join(here, script)], input=payload, env=env).returncode


try:
    data = json.loads(stdin.decode("utf-8")) if stdin else {{}}
except ValueError:
    data = {{}}
tool_input = data.get("tool_input") or {{}}
patch = str(tool_input.get("command", "")) if isinstance(tool_input, dict) else ""
if "file_path" not in tool_input and "*** Begin Patch" in patch:
    for path, added in patch_files(patch):
        item = dict(data, tool_input={{"file_path": path, "content": added}})
        code = run(json.dumps(item).encode("utf-8"))
        if code:
            raise SystemExit(code)
    raise SystemExit(0)
raise SystemExit(run(stdin))
'''


def build_pack(name: str, prefix: str, profile: str, description: str, keywords: list[str]) -> dict:
    source = ROOT / "packs" / name / ".claude"
    dest = OUT / "plugins" / name
    skills = dest / "skills"
    copy_text_tree(source / "skills", skills)
    # Rules are adopted into the project (.codex/rules/), as in the Claude install.
    for skill in skills.rglob("SKILL.md"):
        text = skill.read_text(encoding="utf-8")
        skill.write_text(re.sub(r"(?<![\w./-])rules/", ".codex/rules/", text), encoding="utf-8")
    copy_text_tree(source / "rules", dest / "templates" / "rules")
    # Codex plugins have no slash commands: each command ships as a skill of the same name.
    for cmd in sorted((source / "commands").glob("*.md")):
        target = skills / cmd.stem / "SKILL.md"
        target.parent.mkdir(parents=True, exist_ok=True)
        text = command_skill(cmd, name, prefix, profile)
        target.write_text(re.sub(r"(?<![\w./-])rules/", ".codex/rules/", text), encoding="utf-8")
    copy_text_tree(source / "hooks", dest / "hooks")
    (dest / "hooks" / "run-hook.py").write_text(hook_launcher(profile), encoding="utf-8")
    settings = json.loads((source / "settings.json").read_text(encoding="utf-8"))
    hooks = settings.get("hooks", {})
    for event, groups in hooks.items():
        for group in groups:
            for hook in group.get("hooks", []):
                command = hook.get("command", "")
                script = command.rsplit("/", 1)[-1].replace('"', "")
                hook["command"] = f'python "${{PLUGIN_ROOT}}/hooks/run-hook.py" {profile} {script}' + (" --always" if event == "SessionStart" else "")
    (dest / "hooks" / "hooks.json").write_text(json.dumps({"hooks": hooks}, indent=2) + "\n", encoding="utf-8")
    copy_text_tree(ROOT / "packs" / name / "profile", dest / "templates" / "profile")

    command_names = sorted(path.stem for path in (source / "commands").glob("*.md"))
    (skills / f"{prefix}-workflow" / "SKILL.md").parent.mkdir(parents=True, exist_ok=True)
    (skills / f"{prefix}-workflow" / "SKILL.md").write_text(
        workflow_skill(prefix, profile, command_names), encoding="utf-8")

    agents = codex_text((source / "CLAUDE.md").read_text(encoding="utf-8"))
    agents = agents.replace("Generated by", "Template generated by")
    (dest / "templates" / "AGENTS.md").write_text(agents, encoding="utf-8")
    (dest / "README.md").write_text(
        f"# {name} for Codex\n\nInstall this plugin, then run `${prefix}-init` in the target repository: it writes `.codex/{profile}`, copies `templates/rules/` to `.codex/rules/` and generates `AGENTS.md` from `templates/AGENTS.md`. Every slash command of the Claude Code build is a skill of the same name (`/{prefix}-init` is `${prefix}-init`); `${prefix}-workflow` routes a task described in plain words.\n",
        encoding="utf-8")

    copy_licenses(dest)

    manifest = {
        "name": name,
        "version": VERSION,
        "description": description,
        "author": OWNER,
        "homepage": f"{REPOSITORY}/tree/main/packs/{name}",
        "repository": REPOSITORY,
        "license": LICENSE,
        "keywords": keywords,
        "skills": "./skills/",
        "interface": {
            "displayName": f"AI Pack: {name}",
            "shortDescription": description,
            "longDescription": description,
            "developerName": OWNER["name"],
            "category": "Productivity",
            "capabilities": ["Read", "Write"],
            "defaultPrompt": [f"Use {name} to help me with this software-project task."],
        },
    }
    manifest_path = dest / ".codex-plugin" / "plugin.json"
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return {"name": name, "source": {"source": "local", "path": f"./plugins/{name}"}, "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"}, "category": "Productivity"}



def copy_licenses(dst):
    for name in LICENSE_FILES:
        shutil.copy2(ROOT / name, dst / name)


def clean_dir(path):
    """Empty a generated directory but keep .git: each output is its own git submodule."""
    path.mkdir(parents=True, exist_ok=True)
    for item in path.iterdir():
        if item.name == ".git":
            continue
        if item.is_dir():
            shutil.rmtree(item)
        else:
            item.unlink()


def main() -> None:
    clean_dir(OUT)
    copy_licenses(OUT)
    entries = [build_pack(*pack) for pack in PACKS]
    marketplace = {"name": "ai-pack", "interface": {"displayName": "AI Pack for Codex"}, "plugins": entries}
    # Codex looks for the manifest at <root>/.agents/plugins/marketplace.json; plugin source
    # paths stay relative to the marketplace root.
    manifest = OUT / ".agents" / "plugins" / "marketplace.json"
    manifest.parent.mkdir(parents=True)
    manifest.write_text(json.dumps(marketplace, indent=2) + "\n", encoding="utf-8")
    (OUT / "README.md").write_text("""# AI Pack for Codex

This marketplace publishes four separately installable Codex plugins:

- `sdlc-standard`: development lifecycle, traceability, design and test gates
- `migration-standard`: evidence-led legacy migration
- `pm-standard`: project governance and controls
- `vibe-standard`: fast AI-assisted delivery with safety rails

## Requirements

Install the Codex CLI and run `codex` once to sign in (**Sign in with ChatGPT**); the guard hooks
also need Python 3 on `PATH` as `python`.

```sh
curl -fsSL https://chatgpt.com/codex/install.sh | sh     # macOS, Linux
npm install -g @openai/codex                             # any platform, incl. Windows
brew install --cask codex                                # or Homebrew
codex --version
```

## Install

This marketplace is published as its own (private) repository,
https://github.com/kaitondt/ai-pack-codex, and appears in `ai-pack` as the `codex/` submodule.

```sh
codex plugin marketplace add kaitondt/ai-pack-codex
codex plugin add vibe-standard@ai-pack
codex plugin list
```

The marketplace manifest is `.agents/plugins/marketplace.json`. A local clone works too:
`codex plugin marketplace add <path>/ai-pack-codex` (the repository root, not `plugins/`). To
update later, see **Update** below.

Replace `vibe-standard` with the plugin you need. Start a new Codex thread after installation.

### From the chat

Adding the marketplace is a one-time terminal step (the first line above). After that,
plugins are installed from inside the Codex TUI: run `/plugins`, switch to the **ai-pack** tab,
select the plugin and install it (Space toggles an installed plugin on or off). Start a new
thread afterwards.

### Project-only install

Codex has no project-level plugin install: plugin state lives in `~/.codex/config.toml`, so an
installed plugin is available in every repository. Its guard hooks stay inactive in any
repository without `.codex/<profile>.yaml`, and `/plugins` → Space switches it off machine-wide
when needed. To keep a pack inside one repository instead, copy only its skills there — Codex
reads skills from `.agents/skills/`:

```powershell
mkdir .agents/skills
cp -r ./ai-pack-codex/plugins/vibe-standard/skills/* .agents/skills/
```

That vendored copy has no guard hooks and must be re-copied when the pack is updated.

## Update

```sh
codex plugin marketplace upgrade ai-pack     # fetch the latest catalogue
codex plugin add vibe-standard@ai-pack       # reinstall: upgrade does not update installed plugins
```

Then start a new thread. Copies vendored into `.agents/skills/` (project-only install) are not
updated — copy them again.

### After updating: bring the project in line

Updating the plugin replaces the pack's commands, skills, agents and hooks. It does **not** touch
what you copied into each project when adopting the plugin:

- `.codex/rules/` — compare it with the plugin's `templates/rules/` and copy the files that changed.
  Keep your own edits: a local rule change belongs in the pack's source, not only in one project.
- `AGENTS.md` — regenerate the pack's section only when the release notes say its template
  changed.
- `.codex/<profile>.yaml` — run `$<prefix>-profile-check` in a new thread. It reports fields a new release
  added or renamed; fill them in and run it again until it is clean.

## Adopt a plugin in a project

In the project, start a thread and run `$<prefix>-init` (e.g. `$vibe-init`). It writes the profile to
`.codex/<profile>.yaml`, copies the plugin's `templates/rules/` into `.codex/rules/`, and generates
`AGENTS.md` from `templates/AGENTS.md`. The guard hooks only act in a repository that has
`.codex/<profile>.yaml`.

Codex plugins have no slash commands, so every command of the Claude Code build ships as a skill
of the same name: `/sdlc-init` is `$sdlc-init`, `/pm-wbs` is `$pm-wbs`. Type `$` to pick one, or
describe the task and let `$<prefix>-workflow` route it.

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

### How to set it in Codex

```toml
# ~/.codex/config.toml — the default for every thread
model = "<model>"
model_reasoning_effort = "high"        # a level the model advertises: low, medium, high, xhigh, ...
plan_mode_reasoning_effort = "xhigh"   # optional: deeper reasoning while planning only
```

- **One session:** `codex -m <model> -c model_reasoning_effort="medium"` — `-c` overrides any
  config key for that run.
- **Mid-thread:** `/model` switches the model.
- **Named setups:** keep one config per kind of work (for example `design.config.toml` with
  `high`, `build.config.toml` with `medium` in `$CODEX_HOME`) and start with
  `codex --profile design` or `codex --profile build`.

The generated files in this directory are rebuilt with:

```powershell
python scripts/build-codex-plugins.py
```
""", encoding="utf-8")
    print(f"Built {len(entries)} Codex plugins in {OUT}")


if __name__ == "__main__":
    main()
