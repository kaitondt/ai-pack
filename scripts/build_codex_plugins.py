#!/usr/bin/env python3
"""Build Codex-native ai-pack plugins from the four canonical Claude packs.

The source methodology stays in each pack's .claude/ tree.  This builder produces
an installable Codex marketplace in codex/ without modifying the Claude release.
"""
from __future__ import annotations

import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "codex"
VERSION = "0.1.0"
OWNER = {"name": "ThucND", "url": "https://github.com/kaitondt"}
REPOSITORY = "https://github.com/kaitondt/ai-pack"

PACKS = (
    ("sdlc-standard", "sdlc", "sdlc.profile.yaml", "Build new software with requirements, design, traceability, testing, and gates.", ["sdlc", "requirements", "testing", "traceability"]),
    ("migration-standard", "mig", "migration.profile.yaml", "Replatform a legacy system while preserving evidenced behaviour.", ["migration", "legacy", "replatform", "traceability"]),
    ("pm-standard", "pm", "pm.profile.yaml", "Manage software project scope, estimates, schedule, risk, reporting, and change control.", ["project-management", "pmbok", "risk", "change-control"]),
    ("vibe-standard", "vibe", "vibe.profile.yaml", "Build AI-assisted products with intent, small slices, verification, debt, and stage gates.", ["vibe-coding", "mvp", "verification", "guardrails"]),
)


def codex_text(text: str) -> str:
    """Make filesystem references portable to a Codex project installation."""
    return (text.replace(".claude", ".codex")
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
    command_list = " · ".join(f"`/{name}`" for name in commands)
    return f'''---
name: {prefix}_workflow
description: "Route a {prefix} pack task to the correct lifecycle workflow. Use when the user asks to start, plan, build, test, review, release, report, or assess work governed by this pack."
---

# {prefix} workflow router

1. Read `.codex/{profile}`. If it is missing, stop and ask the user to adopt the pack by copying the profile template from this plugin and its generated `AGENTS.md` into the repository root.
2. Load `{prefix}_project` first, then the phase/area skill it routes to.
3. Treat legacy slash-command names as workflow aliases, not literal Codex commands. Their source procedures are in `references/commands/`.
4. Follow the profile, invariant rules, and evidence/reporting requirements; do not invent project values.

Legacy workflow aliases: {command_list}
'''


def hook_launcher(profile: str) -> str:
    return f'''#!/usr/bin/env python3
"""Run a pack guard only after a Codex project has opted in with its profile."""
import os
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
env = dict(os.environ, CODEX_PROJECT_DIR=project, PLUGIN_ROOT=root,
           CLAUDE_PROJECT_DIR=project, CLAUDE_PLUGIN_ROOT=root)
raise SystemExit(subprocess.run([sys.executable, os.path.join(here, script)], input=stdin, env=env).returncode)
'''


def build_pack(name: str, prefix: str, profile: str, description: str, keywords: list[str]) -> dict:
    source = ROOT / name / ".claude"
    dest = OUT / "plugins" / name
    skills = dest / "skills"
    copy_text_tree(source / "skills", skills)
    for skill in skills.rglob("SKILL.md"):
        skill.write_text(skill.read_text(encoding="utf-8").replace("rules/", "references/rules/"), encoding="utf-8")
    copy_text_tree(source / "rules", dest / "references" / "rules")
    copy_text_tree(source / "rules", dest / "templates" / "rules")
    copy_text_tree(source / "commands", dest / "references" / "commands")
    copy_text_tree(source / "hooks", dest / "hooks")
    (dest / "hooks" / "_run_hook.py").write_text(hook_launcher(profile), encoding="utf-8")
    settings = json.loads((source / "settings.json").read_text(encoding="utf-8"))
    hooks = settings.get("hooks", {})
    for event, groups in hooks.items():
        for group in groups:
            for hook in group.get("hooks", []):
                command = hook.get("command", "")
                script = command.rsplit("/", 1)[-1].replace('"', "")
                hook["command"] = f'python "${{PLUGIN_ROOT}}/hooks/_run_hook.py" {profile} {script}' + (" --always" if event == "SessionStart" else "")
    (dest / "hooks" / "hooks.json").write_text(json.dumps({"hooks": hooks}, indent=2) + "\n", encoding="utf-8")
    copy_text_tree(ROOT / name / "profile", dest / "templates" / "profile")

    command_names = sorted(path.stem for path in (source / "commands").glob("*.md"))
    (skills / f"{prefix}_workflow" / "SKILL.md").parent.mkdir(parents=True, exist_ok=True)
    (skills / f"{prefix}_workflow" / "SKILL.md").write_text(
        workflow_skill(prefix, profile, command_names), encoding="utf-8")

    agents = codex_text((source / "CLAUDE.md").read_text(encoding="utf-8"))
    agents = agents.replace("Generated by", "Template generated by")
    (dest / "templates" / "AGENTS.md").write_text(agents, encoding="utf-8")
    (dest / "README.md").write_text(
        f"# {name} for Codex\n\nInstall this plugin, copy `templates/profile/{profile}` to `.codex/{profile}` in the target repository, copy `templates/rules/` to `.codex/rules/`, then copy `templates/AGENTS.md` to `AGENTS.md`. Use `${prefix}_workflow` or describe the lifecycle task naturally. The former Claude slash-command procedures remain in `references/commands/` as compatibility documentation.\n",
        encoding="utf-8")

    manifest = {
        "name": name,
        "version": VERSION,
        "description": description,
        "author": OWNER,
        "homepage": f"{REPOSITORY}/tree/main/{name}",
        "repository": REPOSITORY,
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


def main() -> None:
    if OUT.exists():
        shutil.rmtree(OUT)
    entries = [build_pack(*pack) for pack in PACKS]
    marketplace = {"name": "ai-pack", "interface": {"displayName": "AI Pack for Codex"}, "plugins": entries}
    (OUT / "marketplace.json").write_text(json.dumps(marketplace, indent=2) + "\n", encoding="utf-8")
    (OUT / "README.md").write_text("""# AI Pack for Codex

This marketplace publishes four separately installable Codex plugins:

- `sdlc-standard`: development lifecycle, traceability, design and test gates
- `migration-standard`: evidence-led legacy migration
- `pm-standard`: project governance and controls
- `vibe-standard`: fast AI-assisted delivery with safety rails

## Local development install

```powershell
codex plugin marketplace add F:/2.AI/ai-pack/codex
codex plugin add vibe-standard@ai-pack
```

Replace `vibe-standard` with the plugin you need. Start a new Codex thread after installation.

## Adopt a plugin in a project

Copy the selected plugin's `templates/profile/<profile>.yaml` to `.codex/`, copy `templates/rules/` to `.codex/rules/`, and copy `templates/AGENTS.md` to the repository's `AGENTS.md`. Then invoke the `<prefix>_workflow` skill (or describe the task normally).

The generated files in this directory are rebuilt with:

```powershell
python scripts/build_codex_plugins.py
```
""", encoding="utf-8")
    print(f"Built {len(entries)} Codex plugins in {OUT}")


if __name__ == "__main__":
    main()
