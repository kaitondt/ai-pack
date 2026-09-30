#!/usr/bin/env python3
"""PreToolUse guard: protect baselined management documents and archived snapshots.

Enforces rules/pm/baseline-integrity.md PB-03 mechanically, so the constraint does not depend
on the model remembering it.

Two protections:
  1. baselines.readonly_globs      -> always denied.
  2. baselines.registered[].path   -> denied unless a change request is active, i.e.
     .claude/.active_pm_cr exists and names a CR id. /pm_change_apply writes that file and
     clears it when the CR closes.

Exit 2 blocks the tool call and returns stderr to the model.
"""
import sys, json, os, fnmatch, re

ROOT = os.environ.get("CLAUDE_PROJECT_DIR", ".")
PROFILE = os.path.join(ROOT, ".claude", "pm.profile.yaml")
ACTIVE_CR = os.path.join(ROOT, ".claude", ".active_pm_cr")

FALLBACK_GLOBS = ["pm/closing/archive/**"]


def read_globs(path):
    """Minimal extraction of baselines.readonly_globs without a yaml dependency."""
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
                if line.strip():
                    break
    return globs or FALLBACK_GLOBS


def read_registered(path):
    """Extract baselines.registered[].path entries, with their artifact label."""
    if not os.path.exists(path):
        return []
    out, in_block, current = [], False, None
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            if re.match(r"^\s*registered:", line):
                in_block = True
                continue
            if in_block:
                m = re.match(r"^\s+-\s+path:\s*[\"']?([^\"'#]*?)[\"']?\s*$", line)
                if m:
                    current = m.group(1).strip()
                    if current:
                        out.append([current, ""])
                    continue
                m = re.match(r"^\s+version:\s*[\"']?([^\"'#]*?)[\"']?\s*$", line)
                if m and out and current:
                    out[-1][1] = m.group(1).strip()
                    continue
                if line.strip() and not line.startswith((" ", "\t")):
                    break
    return out


def active_cr():
    if not os.path.exists(ACTIVE_CR):
        return ""
    try:
        with open(ACTIVE_CR, encoding="utf-8") as fh:
            return fh.read().strip()
    except Exception:
        return ""


def matches(path, pattern):
    p = path.replace("\\", "/")
    pat = pattern.replace("\\", "/")
    if fnmatch.fnmatch(p, pat):
        return True
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
                "[PB-03] BLOCKED: {} matches read-only glob '{}' from pm.profile.yaml.\n"
                "Archived and snapshot baselines are never edited in place - the whole point "
                "of retaining them is that they show what was approved at the time. If a new "
                "version is needed, produce a new baseline through /pm_change_apply.\n"
                .format(fp, pattern))
            return 2

    cr = active_cr()
    if not cr:
        norm = fp.replace("\\", "/")
        for doc, ver in read_registered(PROFILE):
            d = doc.replace("\\", "/")
            if norm.endswith(d) or matches(norm, d):
                sys.stderr.write(
                    "[PB-03] BLOCKED: {}{} is baselined. A baselined document changes only "
                    "through approved change control.\n"
                    "Assess it with /pm_change_assess; once the authority in "
                    "change_control.authority has approved, /pm_change_apply writes the CR id "
                    "to .claude/.active_pm_cr, which unblocks these edits until the CR closes.\n"
                    "For an editorial correction that changes no commitment - a typo, a broken "
                    "link, formatting - ask the user to confirm, write EDITORIAL to "
                    ".claude/.active_pm_cr for the duration, and record it in the revision "
                    "history. Never use that path for a number, a date, a scope item or an "
                    "acceptance criterion.\n".format(doc, " v" + ver if ver else ""))
                return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
