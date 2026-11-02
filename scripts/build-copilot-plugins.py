#!/usr/bin/env python3
"""Build GitHub Copilot agent plugins (Copilot CLI, VS Code) from the four canonical packs.

Source of truth stays in packs/<pack>/.claude/ and packs/<pack>/profile/. This script regenerates copilot/
as a Copilot plugin marketplace (.github/plugin/marketplace.json) whose plugins use the
Agent Plugins 1.0 layout:

    plugins/<pack>/plugin.json                 manifest ($schema 1.0.0)
    plugins/<pack>/skills/                     portable skills
    plugins/<pack>/com.github.copilot/         agents (*.agent.md), commands, hooks
    plugins/<pack>/templates/                  adoption files copied into a project

copilot/ is the git submodule https://github.com/kaitondt/ai-pack-copilot; commit and push
there after a rebuild, then commit the new submodule pointer in ai-pack.

    python scripts/build-copilot-plugins.py
"""
import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LICENSE = "MIT OR Apache-2.0"
LICENSE_FILES = ("LICENSE-MIT", "LICENSE-APACHE")
OUT = ROOT / "copilot"

MARKETPLACE = "ai-pack-copilot"
OWNER = {"name": "ThucND", "url": "https://github.com/kaitondt"}
REPOSITORY = "https://github.com/kaitondt/ai-pack-copilot"
VERSION = "1.5.0"
SCHEMA = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
NS = "com.github.copilot"

PACKS = [
    {
        "name": "sdlc-standard",
        "prefix": "sdlc",
        "profile": "sdlc.profile.yaml",
        "description": "Project-agnostic SDLC pack, P0 Inception to P9 Maintenance: requirements, "
                       "basic/detail design, implementation, test levels, UAT, change requests, "
                       "traceability.",
        "keywords": ["sdlc", "requirements", "design", "testing", "traceability"],
    },
    {
        "name": "migration-standard",
        "prefix": "mig",
        "profile": "migration.profile.yaml",
        "description": "Rewrite or replatform a legacy system while preserving behaviour: legacy "
                       "analysis, gap-driven design, no-invention rules, read-only legacy guards.",
        "keywords": ["migration", "legacy", "replatform", "traceability"],
    },
    {
        "name": "pm-standard",
        "prefix": "pm",
        "profile": "pm.profile.yaml",
        "description": "PMBOK-aligned project management: charter, scope/WBS, estimation, cost and "
                       "schedule baselines, EVM, reporting, quality, risk, change control, closing.",
        "keywords": ["project-management", "pmbok", "evm", "risk", "baseline"],
    },
    {
        "name": "vibe-standard",
        "prefix": "vibe",
        "profile": "vibe.profile.yaml",
        "description": "Vibe coding with guard rails: intent -> slice -> run -> verify -> commit, "
                       "stage model, debt ledger, and handoff to sdlc/pm when the project outgrows it.",
        "keywords": ["vibe-coding", "prototype", "mvp", "guardrails"],
    },
]

DOCS = ["README.md", "ADOPTION.md", "COMMAND-FLOW.md"]

# Claude Code tool -> GitHub custom-agent tool alias (understood by Copilot CLI and VS Code).
TOOL_MAP = {
    "Read": "read", "Write": "edit", "Edit": "edit", "MultiEdit": "edit",
    "Grep": "search", "Glob": "search", "Bash": "execute", "PowerShell": "execute",
    "WebFetch": "web", "WebSearch": "web",
}

# Claude matchers are kept (Copilot applies Claude matcher semantics to PascalCase events);
# the native Copilot tool names are added so the hook also fires if they are not aliased.
MATCHER_EXTRA = {"Write": ["create"], "Edit": ["edit", "apply_patch"],
                 "Bash": ["bash"], "PowerShell": ["powershell"]}

# Hooks that inject rules with exit 0 + text: moved to PostToolUse, where Copilot accepts
# additionalContext, so the model reads the rules right after the write.
CONTEXT_HOOKS = {"check-doc-rules.py", "check-pm-doc-rules.py"}

LAUNCHER = '''#!/usr/bin/env python3
"""Copilot hook launcher: python run-hook.py <event> <profile-file> <hook-script> [--always]

Runs a pack hook only when the project has opted in (.github/<profile-file> exists). The
Copilot payload is normalised to the Claude shape the pack hooks read: tool_name/toolName,
tool_input/toolArgs, path -> file_path, file_text -> content, new_str -> new_string, and an
apply_patch body is split into one call per touched file. Plain-text stdout is returned as
additionalContext; exit 2 (deny, reason on stderr) is passed through unchanged.
"""
import json
import os
import re
import subprocess
import sys

FILE_HEADER = re.compile(r"^[*]{3} (?:Add|Update|Delete) File: (.+)$|^[*]{3} Move to: (.+)$")


def patch_files(patch):
    files, current = [], None
    for line in patch.splitlines():
        m = FILE_HEADER.match(line)
        if m:
            current = [(m.group(1) or m.group(2)).strip(), []]
            files.append(current)
        elif current is not None and line.startswith("+"):
            current[1].append(line[1:])
    return [(path, "\\n".join(lines)) for path, lines in files]


def tool_inputs(data):
    """Yield Claude-shaped tool_input dicts for one Copilot tool call."""
    ti = data.get("tool_input", data.get("toolArgs", {}))
    if isinstance(ti, str):
        try:
            ti = json.loads(ti)
        except ValueError:
            ti = {"command": ti}
    if not isinstance(ti, dict):
        ti = {}
    patch = ti.get("patch") or ti.get("input") or ti.get("command") or ""
    if "file_path" not in ti and "path" not in ti and "*** Begin Patch" in str(patch):
        for path, added in patch_files(str(patch)):
            yield {"file_path": path, "content": added}
        return
    out = dict(ti)
    for src, dst in (("path", "file_path"), ("file_text", "content"), ("new_str", "new_string"),
                     ("old_str", "old_string")):
        if src in out and dst not in out:
            out[dst] = out[src]
    yield out


def main():
    event, profile, script = sys.argv[1], sys.argv[2], sys.argv[3]
    always = "--always" in sys.argv[4:]
    here = os.path.dirname(os.path.abspath(__file__))
    root = os.path.dirname(os.path.dirname(here))
    raw = sys.stdin.buffer.read() if not sys.stdin.isatty() else b""
    try:
        data = json.loads(raw.decode("utf-8")) if raw else {}
    except ValueError:
        data = {}
    project = os.environ.get("CLAUDE_PROJECT_DIR") or data.get("cwd") or os.getcwd()

    if not os.path.exists(os.path.join(project, ".github", profile)) and not always:
        return 0

    env = dict(os.environ, CLAUDE_PROJECT_DIR=project, PLUGIN_ROOT=root,
               CLAUDE_PLUGIN_ROOT=root, PYTHONIOENCODING="utf-8")
    data["tool_name"] = data.get("tool_name") or data.get("toolName", "")
    texts = []
    for ti in tool_inputs(data):
        payload = dict(data, tool_input=ti)
        proc = subprocess.run([sys.executable, os.path.join(here, script)],
                              input=json.dumps(payload).encode("utf-8"), env=env,
                              stdout=subprocess.PIPE)
        if proc.returncode != 0:
            return proc.returncode
        texts.append(proc.stdout.decode("utf-8", errors="replace").replace("\\r\\n", "\\n").strip())

    text = "\\n".join(t for t in texts if t)
    if always:
        text = "[{}] plugin root: {}\\n{}".format(profile.split(".")[0], root, text).strip()
    if not text:
        return 0
    try:
        out = json.loads(text)
        if not isinstance(out, dict):
            raise ValueError
        spec = out.get("hookSpecificOutput")
        if isinstance(spec, dict):
            spec["hookEventName"] = event
            if spec.get("additionalContext"):
                out.setdefault("additionalContext", spec["additionalContext"])
    except ValueError:
        out = {"additionalContext": text,
               "hookSpecificOutput": {"hookEventName": event, "additionalContext": text}}
    sys.stdout.write(json.dumps(out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
'''

PLUGIN_NOTE = """
> **Installed as a GitHub Copilot plugin?** The pack's files are not in this repository's
> `.github/` — they live in the plugin directory printed at session start as
> `[{stem}] plugin root: …`. Map every "pack" path in this command as follows:
>
> | Pack path in this command | Plugin location |
> |---|---|
> | profile template `profile/{profile}` | `<plugin root>/templates/profile/{profile}` |
> | `.github/copilot-instructions.md` template | `<plugin root>/templates/copilot-instructions.md` → write it as `.github/copilot-instructions.md` in this repository |
> | `.github/instructions/` | `<plugin root>/templates/instructions/` — **copy into this project's `.github/instructions/`** (plugins do not load project rules; Copilot applies `*.instructions.md` from the repository). Never overwrite an existing file without asking. |
> | `.github/hooks/*.py` | `<plugin root>/{ns}/hooks/` — already registered by the plugin; do **not** add them to the repository's hook config, they would run twice |
> | `.github/agents/{prefix}-*.md` | `<plugin root>/{ns}/agents/*.agent.md`, read-only (overwritten on update). To change an agent, copy it into this project's `.github/agents/` and edit the copy |
> | `.github/skills/` | `<plugin root>/skills/`, read-only. Override locally by copying the skill into this project's `.github/skills/` |
>
> The profile `.github/{profile}` and everything the pack generates stay in this project.
"""

NOTE_TARGETS = ("-init.md", "-profile-check.md", "-refine-skill.md")

RULE_REF = re.compile(r"(?<![\w./-])(?:\.claude/)?rules/([a-z0-9-]+)/([a-z0-9-]+)\.md")


PRODUCT = "GitHub Copilot"
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


def copilot_text(text):
    """Retarget filesystem and product references from Claude Code to GitHub Copilot."""
    text = text.replace(".claude/CLAUDE.md", ".github/copilot-instructions.md")
    text = RULE_REF.sub(r".github/instructions/\1/\2.instructions.md", text)
    text = text.replace(".claude/rules", ".github/instructions")
    text = re.sub(r"(?<![\w.-])CLAUDE\.md", ".github/copilot-instructions.md", text)
    return model_note(text.replace(".claude", ".github").replace("Claude Code", "GitHub Copilot"))



def copy_licenses(dst):
    for name in LICENSE_FILES:
        shutil.copy2(ROOT / name, dst / name)


def clean_dir(path):
    """Empty a generated directory but keep .git: the output is its own git submodule."""
    path.mkdir(parents=True, exist_ok=True)
    for item in path.iterdir():
        if item.name == ".git":
            continue
        if item.is_dir():
            shutil.rmtree(item)
        else:
            item.unlink()


def copy_tree(src, dst):
    for item in src.rglob("*"):
        if "__pycache__" in item.parts:
            continue
        target = dst / item.relative_to(src)
        if item.is_dir():
            target.mkdir(parents=True, exist_ok=True)
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        if item.suffix in {".md", ".py", ".json", ".yaml", ".yml"}:
            target.write_text(copilot_text(item.read_text(encoding="utf-8")), encoding="utf-8")
        else:
            shutil.copy2(item, target)


def split_frontmatter(text):
    m = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not m:
        return {}, text
    meta = {}
    for line in m.group(1).splitlines():
        key, sep, value = line.partition(":")
        if sep:
            meta[key.strip()] = value.strip()
    return meta, text[m.end():]


def convert_command(path, pack):
    meta, body = split_frontmatter(path.read_text(encoding="utf-8"))
    body = copilot_text(body)
    if path.name.endswith(NOTE_TARGETS):
        m = re.match(r"(?:\s*\n)*(#[^\n]*\n)?", body)
        note = PLUGIN_NOTE.format(prefix=pack["prefix"], profile=pack["profile"], ns=NS,
                                  stem=pack["profile"].split(".")[0])
        body = body[:m.end()] + note + "\n" + body[m.end():]
    # allowed-tools is dropped: it lists Claude tool names.
    return "---\ndescription: {}\n---\n{}".format(
        copilot_text(meta.get("description", '"{}"'.format(path.stem))), body)


def convert_agent(path):
    meta, body = split_frontmatter(path.read_text(encoding="utf-8"))
    lines = ["---", "name: " + meta.get("name", path.stem),
             "description: " + copilot_text(meta.get("description", ""))]
    if "tools" in meta:
        tools = []
        for tool in json.loads(meta["tools"]):
            alias = TOOL_MAP.get(tool)
            if alias and alias not in tools:
                tools.append(alias)
        lines.append("tools: " + json.dumps(tools))
    # model: is dropped — Claude aliases (opus/sonnet) are not Copilot model names; the agent
    # then uses the model picked in the session.
    lines.append("---")
    return "\n".join(lines) + "\n" + copilot_text(body)


def map_matcher(matcher):
    names = []
    for part in matcher.split("|"):
        for name in [part] + MATCHER_EXTRA.get(part, []):
            if name not in names:
                names.append(name)
    return "|".join(names)


def hook_entries(pack, settings):
    """Claude settings.json hooks -> Copilot hooks.json (PascalCase, Claude-compatible)."""
    pattern = re.compile(r'\$CLAUDE_PROJECT_DIR/\.claude/hooks/([A-Za-z0-9_-]+\.py)')
    out = {}
    for event, groups in settings.get("hooks", {}).items():
        for group in groups:
            for h in group["hooks"]:
                m = pattern.search(h["command"])
                if not m:
                    raise SystemExit("unrecognised hook command in {}: {}".format(
                        pack["name"], h["command"]))
                script = m.group(1)
                cevent = "PostToolUse" if script in CONTEXT_HOOKS else event
                entry = {
                    "type": "command",
                    "command": 'python "${{PLUGIN_ROOT}}/{}/hooks/run-hook.py" {} {} {}{}'.format(
                        NS, cevent, pack["profile"], script,
                        " --always" if event == "SessionStart" else ""),
                    "timeout": int(h.get("timeout", 10)),
                }
                matcher = map_matcher(group["matcher"]) if "matcher" in group else None
                bucket = out.setdefault(cevent, [])
                target = next((g for g in bucket if g.get("matcher") == matcher), None)
                if target is None:
                    target = {"matcher": matcher, "hooks": []} if matcher else {"hooks": []}
                    bucket.append(target)
                target["hooks"].append(entry)
    return {"version": 1, "hooks": out}


RULE_PATHS = re.compile(r"\A---\n(.*?)\n---\n+", re.S)


def rule_scope(text):
    """Split a rule's `paths:` front matter (stack rules) from its body: (globs, body)."""
    m = RULE_PATHS.match(text.replace("\r\n", "\n"))
    if not m:
        return [], text
    globs = re.findall(r'^\s*-\s*["\']?([^"\'\n]+?)["\']?\s*$', m.group(1), re.M)
    return globs, text.replace("\r\n", "\n")[m.end():]


def instructions(rules_dir, dst):
    """Rules -> .instructions.md files: repository-wide, or scoped by the rule's `paths:`."""
    for rule in sorted(rules_dir.rglob("*.md")):
        rel = rule.relative_to(rules_dir)
        target = dst / rel.parent / (rule.stem + ".instructions.md")
        target.parent.mkdir(parents=True, exist_ok=True)
        globs, body = rule_scope(rule.read_text(encoding="utf-8"))
        target.write_text('---\napplyTo: "{}"\n---\n\n'.format(",".join(globs) or "**") +
                          copilot_text(body), encoding="utf-8")


def build(pack):
    src = ROOT / "packs" / pack["name"]
    claude = src / ".claude"
    dst = OUT / "plugins" / pack["name"]
    ns = dst / NS
    dst.mkdir(parents=True)

    copy_tree(claude / "skills", dst / "skills")

    (ns / "commands").mkdir(parents=True)
    for cmd in sorted((claude / "commands").glob("*.md")):
        (ns / "commands" / cmd.name).write_text(convert_command(cmd, pack), encoding="utf-8")

    (ns / "agents").mkdir()
    for agent in sorted((claude / "agents").glob("*.md")):
        (ns / "agents" / (agent.stem + ".agent.md")).write_text(convert_agent(agent),
                                                                encoding="utf-8")

    copy_tree(claude / "hooks", ns / "hooks")
    (ns / "hooks" / "run-hook.py").write_text(LAUNCHER, encoding="utf-8")
    settings = json.loads((claude / "settings.json").read_text(encoding="utf-8"))
    (ns / "hooks" / "hooks.json").write_text(
        json.dumps(hook_entries(pack, settings), indent=2) + "\n", encoding="utf-8")

    tpl = dst / "templates"
    instructions(claude / "rules", tpl / "instructions")
    copy_tree(src / "profile", tpl / "profile")
    (tpl / "copilot-instructions.md").write_text(
        copilot_text((claude / "CLAUDE.md").read_text(encoding="utf-8")), encoding="utf-8")

    for doc in DOCS:
        if (src / doc).exists():
            (dst / doc).write_text(copilot_text((src / doc).read_text(encoding="utf-8")),
                                   encoding="utf-8")

    copy_licenses(dst)

    manifest = {
        "$schema": SCHEMA,
        "name": pack["name"],
        "version": VERSION,
        "description": pack["description"],
        "author": OWNER["name"],
        "homepage": "{}/tree/main/plugins/{}".format(REPOSITORY, pack["name"]),
        "repository": REPOSITORY,
        "license": LICENSE,
        "keywords": pack["keywords"],
    }
    (dst / "plugin.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    counts = {"commands": len(list((ns / "commands").glob("*.md"))),
              "agents": len(list((ns / "agents").glob("*.agent.md"))),
              "skills": len(list((dst / "skills").glob("*/SKILL.md")))}
    print("  {:<20} {commands:>3} commands  {agents:>3} agents  {skills:>3} skills".format(
        pack["name"], **counts))


README = """# AI Pack for GitHub Copilot

Four GitHub Copilot agent plugins (Copilot CLI and VS Code), generated from
[kaitondt/ai-pack](https://github.com/kaitondt/ai-pack). This repository is a Copilot plugin
marketplace named **`{marketplace}`**:

| Plugin | Commands | Profile it creates |
|---|---|---|
{rows}

Each plugin uses the Agent Plugins 1.0 layout: `plugin.json`, portable `skills/`, and
`com.github.copilot/` with custom agents (`*.agent.md`), slash commands and hooks.

## Requirements

A GitHub Copilot subscription, Python 3 on `PATH` as `python` (guard hooks), and either VS Code
with Copilot Chat or the Copilot CLI — run `copilot` once and `/login`:

```sh
curl -fsSL https://gh.io/copilot-install | bash    # macOS, Linux
winget install GitHub.Copilot                      # Windows
npm install -g @github/copilot                     # any platform (Node.js 22+)
brew install --cask copilot-cli                    # or Homebrew
copilot --version
```

## Install

Copilot CLI:

```sh
copilot plugin marketplace add kaitondt/ai-pack-copilot
copilot plugin install vibe-standard@{marketplace}
```

### From the chat

Copilot CLI session:

```text
/plugin marketplace add kaitondt/ai-pack-copilot
/plugin install vibe-standard@{marketplace}
/plugin marketplace browse {marketplace}
```

VS Code: open the Chat view → **gear icon** → **Plugins**, or run **Chat: Install Plugin From
Source** from the Command Palette with `https://github.com/kaitondt/ai-pack-copilot.git`. To
browse the marketplace in VS Code, add it to the `chat.plugins.marketplaces` setting
(`["https://github.com/kaitondt/ai-pack-copilot.git"]` — the `.git` URL form works for private
repositories) and install from the Plugins list or **Extensions → @agentPlugins**.

Start a new chat session after installing.

### Project-only install

VS Code reads workspace plugin settings: commit `.github/copilot/settings.json` and the
repository declares the marketplace and the plugin itself — VS Code recommends it the first time
a chat message is sent in the workspace, and no other workspace has it enabled:

```json
{{
  "extraKnownMarketplaces": {{
    "{marketplace}": {{ "source": {{ "source": "github", "repo": "kaitondt/ai-pack-copilot" }} }}
  }},
  "enabledPlugins": {{ "vibe-standard@{marketplace}": true }}
}}
```

Copilot CLI installs plugins per machine (`~/.copilot/installed-plugins/`). Its hooks stay
inactive in any repository without `.github/<profile>.yaml`.

The repository is private: installing needs `git` credentials with access to it.

## Update

Copilot CLI:

```sh
copilot plugin marketplace update {marketplace}    # refresh the catalogue
copilot plugin update vibe-standard                 # or: copilot plugin update --all
```

In chat: `/plugin marketplace update {marketplace}`, or press **R** in the Marketplace view of
`/plugin`; then start a new session.

VS Code checks agent plugins for updates every 24 hours; to update now, run **Extensions: Check
for Extension Updates** from the Command Palette. A workspace that enables the plugin through
`.github/copilot/settings.json` gets the update the same way.

### After updating: bring the project in line

Updating the plugin replaces the pack's commands, skills, agents and hooks. It does **not** touch
what `/<prefix>-init` copied into each project:

- `.github/instructions/` — compare it with the plugin's `templates/rules/` and copy the files that changed.
  Keep your own edits: a local rule change belongs in the pack's source, not only in one project.
- `.github/copilot-instructions.md` — regenerate the pack's section only when the release notes say its template
  changed.
- `.github/<profile>.yaml` — run `/<prefix>-profile-check` in a new session. It reports fields a new release
  added or renamed; fill them in and run it again until it is clean.

## Adopt in a project

Run `/<prefix>-init` (e.g. `/vibe-init`). It writes the profile to `.github/<profile>.yaml`,
copies the rules into `.github/instructions/` as `*.instructions.md` (`applyTo: "**"`), and
generates `.github/copilot-instructions.md`. The hooks only act in a repository that has
`.github/<profile>.yaml`; elsewhere they are no-ops apart from a session-start hint.

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

### How to set it in GitHub Copilot

- **Mid-session:** `/model` switches the model, and lets you set the reasoning effort on models
  that support it.
- **At start-up:** `copilot --model <model>`, or the `COPILOT_MODEL` environment variable.
- **Default:** `~/.copilot/settings.json` (or `$COPILOT_HOME/settings.json`):

  ```json
  {{ "model": "<model>", "effortLevel": "high" }}
  ```

  `effortLevel` applies only to models with adjustable reasoning effort.
- **Which model:** for example an Opus-class model for the first row, a Sonnet-class model for
  the second and `claude-haiku-4.5` for mechanical checks — or the equivalent GPT models.

## Differences from the Claude plugins

- Project files live under `.github/` instead of `.claude/`.
- Custom agents drop `model:` and use the tool aliases `read`, `edit`, `search`, `execute`, `web`.
- The document-rule hooks (`check-doc-rules`, `check-pm-doc-rules`) run on **PostToolUse**.
- The hook launcher maps Copilot tool arguments (`path`, `file_text`, `new_str`, apply_patch
  bodies) to the Claude shape the pack hooks read.

Generated by `python scripts/build-copilot-plugins.py` in ai-pack; do not edit by hand.
"""


def main():
    clean_dir(OUT)
    copy_licenses(OUT)
    print("Building Copilot plugins into {}".format(OUT.relative_to(ROOT)))
    for pack in PACKS:
        build(pack)

    marketplace = {
        "name": MARKETPLACE,
        "owner": OWNER,
        "metadata": {
            "description": "AI Pack for GitHub Copilot: sdlc, migration, pm and vibe plugins",
            "version": VERSION,
        },
        "plugins": [
            {
                "name": p["name"],
                "source": "./plugins/{}".format(p["name"]),
                "description": p["description"],
                "version": VERSION,
            }
            for p in PACKS
        ],
    }
    mp = OUT / ".github" / "plugin" / "marketplace.json"
    mp.parent.mkdir(parents=True)
    mp.write_text(json.dumps(marketplace, indent=2) + "\n", encoding="utf-8")

    rows = "\n".join("| `{}` | `/{}-*` | `.github/{}` |".format(p["name"], p["prefix"], p["profile"])
                     for p in PACKS)
    (OUT / "README.md").write_text(README.format(marketplace=MARKETPLACE, rows=rows),
                                   encoding="utf-8")


if __name__ == "__main__":
    main()
