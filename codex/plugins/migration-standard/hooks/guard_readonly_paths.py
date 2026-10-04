#!/usr/bin/env python3
"""PreToolUse guard: deny writes to paths the migration profile marks read-only.

Enforces rules/migration/legacy-readonly.md LR-01 and LR-04 mechanically, so the
constraint does not depend on the model remembering it.

Exit 2 blocks the tool call and returns stderr to the model.
"""
import sys, json, os, fnmatch, re

PROFILE = os.path.join(os.environ.get("CODEX_PROJECT_DIR", "."),
                       ".codex", "migration.profile.yaml")

FALLBACK_GLOBS = ["**/legacy/**", "**/*.generated.*"]


def read_globs(path):
    """Minimal extraction of constraints.readonly_globs without a yaml dependency."""
    if not os.path.exists(path):
        return FALLBACK_GLOBS
    globs, in_block = [], False
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            if re.match(r"^\s*readonly_globs:", line):
                in_block = True
                continue
            if in_block:
                m = re.match(r"^\s+-\s+[\"']?([^\"'#]+?)[\"']?\s*$", line)
                if m:
                    globs.append(m.group(1).strip())
                    continue
                if line.strip() and not line.startswith((" ", "\t")):
                    break
                if line.strip() and not line.lstrip().startswith("-"):
                    break
    return globs or FALLBACK_GLOBS


def matches(path, pattern):
    p = path.replace("\\", "/")
    pat = pattern.replace("\\", "/")
    if fnmatch.fnmatch(p, pat):
        return True
    # treat "a/**" as also matching "a/b" and any deeper path
    if pat.endswith("/**") and (p == pat[:-3] or p.startswith(pat[:-2])):
        return True
    return fnmatch.fnmatch(p, "*/" + pat.lstrip("/"))


def main():
    try:
        data = json.loads(sys.stdin.buffer.read().decode("utf-8"))
    except Exception:
        return 0
    fp = str(data.get("tool_input", {}).get("file_path", ""))
    if not fp:
        return 0
    for pattern in read_globs(PROFILE):
        if matches(fp, pattern):
            sys.stderr.write(
                "[LR-01] BLOCKED: {} matches read-only glob '{}' from "
                "migration.profile.yaml.\n"
                "The source system and generated files are never modified. "
                "Write analysis output under the docs paths instead; if a generated "
                "file needs to change, change its generator input.\n".format(fp, pattern))
            return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
