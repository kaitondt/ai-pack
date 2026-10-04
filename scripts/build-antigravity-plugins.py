#!/usr/bin/env python3
"""Build Google Antigravity plugins (agy CLI and IDE) from the four canonical packs.

Source of truth stays in packs/<pack>/.claude/ and packs/<pack>/profile/. Antigravity does not
read Gemini CLI extensions (gemini-extension.json, TOML commands, Gemini hooks); it has its own
plugin format, which this script generates in antigravity/:

    plugins/<pack>/plugin.json     manifest (schema v1)
    plugins/<pack>/skills/         pack skills + one skill per slash command (/vibe-init, ...)
    plugins/<pack>/agents/         custom agents (Antigravity tool names)
    plugins/<pack>/hooks.json      PreToolUse guards -> hooks/run-hook.py
    plugins/<pack>/templates/      adoption files copied into a project (.agents/)

Plugin-level rules/ are deliberately not used: Antigravity activates them in every workspace,
while the pack's rules must only apply in adopted projects, so /<prefix>-init copies them into
the project's .agents/rules/.

antigravity/ is the git submodule https://github.com/kaitondt/ai-pack-antigravity; commit and
push there after a rebuild, then commit the new submodule pointer in ai-pack.

    python scripts/build-antigravity-plugins.py
"""
import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "antigravity"
VERSION = "1.1.0"
README_SOURCE = ROOT / "scripts" / "readme" / "antigravity.md"

PACKS = [
    {"name": "sdlc-standard", "prefix": "sdlc", "profile": "sdlc.profile.yaml",
     "description": "Project-agnostic SDLC pack, P0 Inception to P9 Maintenance: requirements, "
                    "design, implementation, test levels, UAT, change requests, traceability."},
    {"name": "migration-standard", "prefix": "mig", "profile": "migration.profile.yaml",
     "description": "Rewrite or replatform a legacy system while preserving behaviour: legacy "
                    "analysis, gap-driven design, no-invention rules, read-only legacy guards."},
    {"name": "pm-standard", "prefix": "pm", "profile": "pm.profile.yaml",
     "description": "PMBOK-aligned project management: charter, scope/WBS, estimation, baselines, "
                    "EVM, reporting, quality, risk, change control, closing."},
    {"name": "vibe-standard", "prefix": "vibe", "profile": "vibe.profile.yaml",
     "description": "Vibe coding with guard rails: intent -> slice -> run -> verify -> commit, "
                    "stage model, debt ledger, and handoff to sdlc/pm."},
]

DOCS = ["README.md", "ADOPTION.md", "COMMAND-FLOW.md"]

# Claude Code tool -> Antigravity tools. A custom agent with no tools gets none, so agents
# without a tools list receive the full set.
TOOL_MAP = {
    "Read": ["view_file", "list_dir"],
    "Write": ["write_to_file"],
    "Edit": ["replace_file_content", "multi_replace_file_content"],
    "MultiEdit": ["multi_replace_file_content"],
    "Grep": ["grep_search"],
    "Glob": ["find_by_name", "list_dir"],
    "Bash": ["run_command"],
    "PowerShell": ["run_command"],
    "WebFetch": ["read_url_content"],
    "WebSearch": ["search_web"],
}
ALL_TOOLS = ["Read", "Write", "Edit", "Grep", "Glob", "Bash"]

MATCHER_MAP = {"Write": "write_to_file", "Edit": "replace_file_content",
               "MultiEdit": "multi_replace_file_content", "Bash": "run_command",
               "PowerShell": "run_command"}

LAUNCHER = '''#!/usr/bin/env python3
"""Antigravity hook launcher: python run-hook.py <profile-file> <hook-script>

Runs a pack guard only when the workspace has opted in (.agents/<profile-file> exists).
Antigravity sends {"toolCall": {"name", "args"}, "workspacePaths": [...]} and expects
{"decision": "allow" | "deny", "reason": ...} on stdout. The call is mapped to the Claude
shape the pack hooks read (TargetFile -> file_path, CodeContent / ReplacementContent /
ReplacementChunks -> content, CommandLine -> command); a hook exit 2 becomes a deny with the
hook's stderr as the reason.
"""
import json
import os
import subprocess
import sys


def answer(decision, reason=None):
    out = {"decision": decision}
    if reason:
        out["reason"] = reason
    sys.stdout.write(json.dumps(out))
    return 0


def tool_input(args):
    ti = {}
    path = args.get("TargetFile") or args.get("AbsolutePath") or args.get("file_path")
    if path:
        ti["file_path"] = path
    chunks = [c.get("ReplacementContent", "") for c in args.get("ReplacementChunks") or []
              if isinstance(c, dict)]
    content = args.get("CodeContent") or args.get("ReplacementContent") or "\\n".join(chunks)
    if content:
        ti["content"] = content
        ti["new_string"] = content
    if args.get("CommandLine"):
        ti["command"] = args["CommandLine"]
    return ti


def main():
    profile, script = sys.argv[1], sys.argv[2]
    here = os.path.dirname(os.path.abspath(__file__))
    raw = sys.stdin.buffer.read() if not sys.stdin.isatty() else b""
    try:
        data = json.loads(raw.decode("utf-8")) if raw else {}
    except ValueError:
        data = {}
    paths = data.get("workspacePaths") or []
    project = os.environ.get("CLAUDE_PROJECT_DIR") or (paths[0] if paths else os.getcwd())
    if not os.path.exists(os.path.join(project, ".agents", profile)):
        return answer("allow")

    call = data.get("toolCall") or {}
    args = call.get("args") or {}
    if isinstance(args, str):
        try:
            args = json.loads(args)
        except ValueError:
            args = {}
    payload = {"tool_name": call.get("name", ""), "tool_input": tool_input(args), "cwd": project}
    env = dict(os.environ, CLAUDE_PROJECT_DIR=project,
               CLAUDE_PLUGIN_ROOT=os.path.dirname(here), PYTHONIOENCODING="utf-8")
    proc = subprocess.run([sys.executable, os.path.join(here, script)],
                          input=json.dumps(payload).encode("utf-8"), env=env,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if proc.returncode == 2:
        return answer("deny", proc.stderr.decode("utf-8", errors="replace").strip())
    return answer("allow")


if __name__ == "__main__":
    sys.exit(main())
'''

PLUGIN_NOTE = """
> **Installed as an Antigravity plugin?** The pack's files are not in this repository's
> `.agents/` — they live in the plugin directory (`~/.gemini/antigravity-cli/plugins/{name}/`,
> `~/.gemini/config/plugins/{name}/`, or `.agents/plugins/{name}/` for a workspace install).
> Map every "pack" path in this procedure as follows:
>
> | Pack path in this procedure | Plugin location |
> |---|---|
> | profile template `profile/{profile}` | `<plugin>/templates/profile/{profile}` |
> | `.agents/rules/{prefix}-context.md` template | `<plugin>/templates/rules/{prefix}-context.md` |
> | `.agents/rules/` | `<plugin>/templates/rules/` — **copy into this project's `.agents/rules/`** (plugin rules would apply in every workspace, so the pack ships them as templates). Never overwrite an existing file without asking. |
> | `.agents/hooks/*.py` | `<plugin>/hooks/` — already registered by the plugin's `hooks.json` |
> | `.agents/agents/{prefix}-*.md` | `<plugin>/agents/`, read-only. To change an agent, copy it into this project's `.agents/agents/` |
> | `.agents/skills/` | `<plugin>/skills/`, read-only. Override by copying a skill into this project's `.agents/skills/` |
>
> The profile `.agents/{profile}` and everything the pack generates stay in this project.
"""

NOTE_TARGETS = ("-init.md", "-profile-check.md", "-refine-skill.md")
RULE_REF = re.compile(r"(?<![\w./-])(?:\.claude/)?rules/([a-z0-9-]+)/([a-z0-9-]+)\.md")


PRODUCT = "Antigravity"
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


def agy_text(text, pack):
    """Retarget filesystem and product references from Claude Code to Antigravity."""
    context = ".agents/rules/{}-context.md".format(pack["prefix"])
    text = text.replace(".claude/CLAUDE.md", context)
    text = RULE_REF.sub(r".agents/rules/\1-\2.md", text)
    text = text.replace(".claude/rules", ".agents/rules")
    text = re.sub(r"(?<![\w.-])CLAUDE\.md", context, text)
    text = text.replace("$ARGUMENTS", "the text the user typed after the command")
    return model_note(text.replace(".claude", ".agents").replace("Claude Code", "Antigravity"))


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


def copy_tree(src, dst, pack):
    for item in src.rglob("*"):
        if "__pycache__" in item.parts:
            continue
        target = dst / item.relative_to(src)
        if item.is_dir():
            target.mkdir(parents=True, exist_ok=True)
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        if item.suffix in {".md", ".py", ".json", ".yaml", ".yml"}:
            target.write_text(agy_text(item.read_text(encoding="utf-8"), pack), encoding="utf-8")
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


def command_skill(path, pack):
    """A slash command becomes a skill of the same name, invoked as /<name>."""
    meta, body = split_frontmatter(path.read_text(encoding="utf-8"))
    body = agy_text(body, pack)
    if path.name.endswith(NOTE_TARGETS):
        m = re.match(r"(?:\s*\n)*(#[^\n]*\n)?", body)
        note = PLUGIN_NOTE.format(name=pack["name"], prefix=pack["prefix"],
                                  profile=pack["profile"])
        body = body[:m.end()] + note + "\n" + body[m.end():]
    description = agy_text(meta.get("description", '"{}"'.format(path.stem)), pack)
    return "---\nname: {}\ndescription: {}\n---\n{}".format(path.stem, description, body)


def convert_agent(path, pack):
    meta, body = split_frontmatter(path.read_text(encoding="utf-8"))
    tools = []
    for tool in (json.loads(meta["tools"]) if "tools" in meta else ALL_TOOLS):
        for mapped in TOOL_MAP.get(tool, []):
            if mapped not in tools:
                tools.append(mapped)
    lines = ["---", "name: " + meta.get("name", path.stem),
             "description: " + agy_text(meta.get("description", ""), pack),
             "tools: " + json.dumps(tools),
             "plugins: " + json.dumps([pack["name"]]),
             "---"]
    # model: is dropped — Claude aliases are not Antigravity tiers; the agent inherits the model.
    return "\n".join(lines) + "\n" + agy_text(body, pack)


def hook_entries(pack, settings):
    """Only PreToolUse guards are carried over: Antigravity has no SessionStart event, and its
    PostToolUse cannot return context, so the profile-status and doc-rule hooks are dropped
    (the rules themselves are always-on workspace rules)."""
    pattern = re.compile(r'\$CLAUDE_PROJECT_DIR/\.claude/hooks/([A-Za-z0-9_-]+\.py)')
    groups_out = []
    for group in settings.get("hooks", {}).get("PreToolUse", []):
        tools = []
        for part in group.get("matcher", "").split("|"):
            mapped = MATCHER_MAP.get(part)
            if mapped and mapped not in tools:
                tools.append(mapped)
                if mapped == "replace_file_content":
                    tools.append("multi_replace_file_content")
        hooks = []
        for h in group["hooks"]:
            script = pattern.search(h["command"]).group(1)
            if script.startswith("check-"):
                continue
            hooks.append({"type": "command",
                          "command": "python ./hooks/run-hook.py {} {}".format(
                              pack["profile"], script),
                          "timeout": int(h.get("timeout", 10))})
        if tools and hooks:
            groups_out.append({"matcher": "|".join(dict.fromkeys(tools)), "hooks": hooks})
    return {"{}-guards".format(pack["prefix"]): {"enabled": True, "PreToolUse": groups_out}}


def build(pack):
    src = ROOT / "packs" / pack["name"]
    claude = src / ".claude"
    dst = OUT / "plugins" / pack["name"]
    dst.mkdir(parents=True)

    copy_tree(claude / "skills", dst / "skills", pack)
    for cmd in sorted((claude / "commands").glob("*.md")):
        target = dst / "skills" / cmd.stem / "SKILL.md"
        target.parent.mkdir(parents=True)
        target.write_text(command_skill(cmd, pack), encoding="utf-8")

    (dst / "agents").mkdir()
    for agent in sorted((claude / "agents").glob("*.md")):
        (dst / "agents" / agent.name).write_text(convert_agent(agent, pack), encoding="utf-8")

    copy_tree(claude / "hooks", dst / "hooks", pack)
    (dst / "hooks" / "run-hook.py").write_text(LAUNCHER, encoding="utf-8")
    settings = json.loads((claude / "settings.json").read_text(encoding="utf-8"))
    (dst / "hooks.json").write_text(json.dumps(hook_entries(pack, settings), indent=2) + "\n",
                                    encoding="utf-8")

    rules = dst / "templates" / "rules"
    rules.mkdir(parents=True)
    for rule in sorted((claude / "rules").rglob("*.md")):
        name = "{}-{}.md".format(rule.parent.name, rule.stem)
        (rules / name).write_text("---\ntrigger: always_on\n---\n\n" +
                                  agy_text(rule.read_text(encoding="utf-8"), pack),
                                  encoding="utf-8")
    (rules / "{}-context.md".format(pack["prefix"])).write_text(
        "---\ntrigger: always_on\n---\n\n" +
        agy_text((claude / "CLAUDE.md").read_text(encoding="utf-8"), pack), encoding="utf-8")
    copy_tree(src / "profile", dst / "templates" / "profile", pack)

    for doc in DOCS:
        if (src / doc).exists():
            (dst / doc).write_text(agy_text((src / doc).read_text(encoding="utf-8"), pack),
                                   encoding="utf-8")

    # plugin.json accepts only name, description, logo, suggestedPrompts, displayName,
    # version and disabled; other fields are silently discarded by the loader.
    manifest = {"name": pack["name"], "displayName": "AI Pack: " + pack["name"],
                "version": VERSION, "description": pack["description"],
                "suggestedPrompts": ["/{}-init".format(pack["prefix"])]}
    (dst / "plugin.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    counts = (len(list((claude / "commands").glob("*.md"))),
              len(list((dst / "agents").glob("*.md"))),
              len(list((dst / "skills").glob("*/SKILL.md"))))
    print("  {:<20} {:>3} commands  {:>3} agents  {:>3} skills (incl. commands)".format(
        pack["name"], *counts))


def main():
    clean_dir(OUT)
    print("Building Antigravity plugins into {}".format(OUT.relative_to(ROOT)))
    for pack in PACKS:
        build(pack)
    shutil.copy2(README_SOURCE, OUT / "README.md")


if __name__ == "__main__":
    main()
