#!/usr/bin/env python3
"""PostToolUse: run the repository's formatter and linter on the file just written.

Reads target.build.on_edit from .claude/migration.profile.yaml - a list of entries:

    on_edit:
      - glob: "apps/web/src/**/*.{ts,tsx}"   # repo-relative; ** and {a,b} supported
        cwd: "apps/web"                      # repo-relative working directory
        run: "pnpm exec prettier --write {file}"
        blocking: false                      # true: a non-zero exit is returned to the model
        timeout: 20                          # seconds, per entry

Placeholders in `run`: {file} absolute path, {rel} path relative to cwd, {root} project root.
Every matching entry runs, in profile order (formatter before linter). No entries, no match,
or a missing tool -> no-op. Never fetches or installs anything (rules/common/hooks.md).
Exit 2 with the tool output on stderr only for a failing `blocking: true` entry.
"""
import sys, json, os, re, subprocess

ROOT = os.environ.get("CLAUDE_PROJECT_DIR", ".")
PROFILE = os.path.join(ROOT, ".claude", "migration.profile.yaml")
SECTION = "target"
DEFAULT_TIMEOUT = 20
MAX_OUTPUT_LINES = 60


def scalar(value):
    value = value.strip()
    if value[:1] == "'":
        out, i = "", 1
        while i < len(value):
            if value[i] == "'":
                if value[i + 1:i + 2] != "'":
                    break
                i += 1
            out, i = out + value[i], i + 1
        return out
    if value[:1] == "\"":
        out, i = "", 1
        while i < len(value) and value[i] != "\"":
            if value[i] == "\\" and i + 1 < len(value):
                i += 1
            out, i = out + value[i], i + 1
        return out
    value = value.split(" #", 1)[0].strip()
    if value.lower() in ("true", "yes"):
        return True
    if value.lower() in ("false", "no"):
        return False
    if re.fullmatch(r"\d+", value):
        return int(value)
    return value


def read_entries(path):
    """Extract <SECTION>.build.on_edit[] without a yaml dependency."""
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8") as fh:
        lines = fh.read().splitlines()
    stack, entries, block_indent, current = [], [], None, None
    for line in lines:
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        indent = len(line) - len(line.lstrip())
        if block_indent is not None:
            if indent <= block_indent:
                break
            m = re.match(r"^\s*-\s+([a-z_]+):\s*(.*)$", line)
            if m:
                current = {m.group(1): scalar(m.group(2))}
                entries.append(current)
                continue
            m = re.match(r"^\s*([a-z_]+):\s*(.*)$", line)
            if m and current is not None:
                current[m.group(1)] = scalar(m.group(2))
            continue
        m = re.match(r"^(\s*)([a-z_]+):", line)
        if not m:
            continue
        while stack and stack[-1][0] >= indent:
            stack.pop()
        stack.append((indent, m.group(2)))
        if [k for _, k in stack] == [SECTION, "build", "on_edit"]:
            if re.search(r":\s*\[\s*\]", line):
                return []
            block_indent = indent
    return [e for e in entries if e.get("glob") and e.get("run")]


def glob_regex(pattern):
    """Glob -> regex: ** crosses directories, * and ? do not, {a,b} alternates."""
    out, i = "", 0
    while i < len(pattern):
        c = pattern[i]
        if pattern.startswith("**/", i):
            out, i = out + "(?:.*/)?", i + 3
        elif pattern.startswith("**", i):
            out, i = out + ".*", i + 2
        elif c == "*":
            out, i = out + "[^/]*", i + 1
        elif c == "?":
            out, i = out + "[^/]", i + 1
        elif c == "{":
            end = pattern.find("}", i)
            if end < 0:
                out, i = out + re.escape(c), i + 1
            else:
                alts = pattern[i + 1:end].split(",")
                out, i = out + "(?:" + "|".join(re.escape(a) for a in alts) + ")", end + 1
        else:
            out, i = out + re.escape(c), i + 1
    return re.compile("^" + out + "$")


def main():
    try:
        data = json.loads(sys.stdin.buffer.read().decode("utf-8"))
    except Exception:
        return 0
    tool_input = data.get("tool_input", {}) or {}
    fp = str(tool_input.get("file_path", "") or tool_input.get("path", ""))
    if not fp:
        return 0

    root = os.path.abspath(ROOT)
    absolute = os.path.abspath(fp if os.path.isabs(fp) else os.path.join(root, fp))
    if not os.path.isfile(absolute):
        return 0
    rel_root = os.path.relpath(absolute, root).replace("\\", "/")
    if rel_root.startswith("../"):
        return 0

    failures = []
    for entry in read_entries(PROFILE):
        if not glob_regex(str(entry["glob"]).replace("\\", "/")).match(rel_root):
            continue
        cwd = os.path.join(root, str(entry.get("cwd") or "."))
        if not os.path.isdir(cwd):
            continue
        command = (str(entry["run"])
                   .replace("{file}", '"{}"'.format(absolute))
                   .replace("{rel}", '"{}"'.format(
                       os.path.relpath(absolute, cwd).replace("\\", "/")))
                   .replace("{root}", '"{}"'.format(root)))
        timeout = entry.get("timeout") if isinstance(entry.get("timeout"), int) else DEFAULT_TIMEOUT
        try:
            proc = subprocess.run(command, shell=True, cwd=cwd, timeout=timeout,
                                  stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        except subprocess.TimeoutExpired:
            if entry.get("blocking") is True:
                failures.append((command, "timed out after {}s".format(timeout)))
            continue
        except Exception:
            continue
        if proc.returncode != 0 and entry.get("blocking") is True:
            output = proc.stdout.decode("utf-8", "replace").strip().splitlines()
            failures.append((command, "\n".join(output[-MAX_OUTPUT_LINES:])))

    if failures:
        sys.stderr.write("[on_edit] {} failed a blocking check after this edit. Fix the "
                         "file; do not weaken the tool's configuration.\n".format(rel_root))
        for command, output in failures:
            sys.stderr.write("$ {}\n{}\n".format(command, output))
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
