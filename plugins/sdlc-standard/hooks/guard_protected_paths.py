#!/usr/bin/env python3
"""PreToolUse guard: protect generated files and baselined documents.

Enforces rules/sdlc/baseline-change-control.md BL-02 and BL-07 mechanically, so the
constraint does not depend on the model remembering it.

Two protections:
  1. constraints.readonly_globs  -> always denied.
  2. constraints.baselined[].path -> denied unless a change request is active, i.e.
     .claude/.active_cr exists and names a CR id. /sdlc_cr_design writes that file;
     /sdlc_cr_report removes it.

Exit 2 blocks the tool call and returns stderr to the model.
"""
import sys, json, os, fnmatch, re

ROOT = os.environ.get("CLAUDE_PROJECT_DIR", ".")
PROFILE = os.path.join(ROOT, ".claude", "sdlc.profile.yaml")
ACTIVE_CR = os.path.join(ROOT, ".claude", ".active_cr")

FALLBACK_GLOBS = ["**/*.generated.*"]


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
                if line.strip():
                    break
    return globs or FALLBACK_GLOBS


def read_baselined(path):
    """Extract constraints.baselined[].path entries."""
    if not os.path.exists(path):
        return []
    out, in_block = [], False
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            if re.match(r"^\s*baselined:", line):
                in_block = True
                continue
            if in_block:
                m = re.match(r"^\s+-\s+path:\s*[\"']?([^\"'#]*?)[\"']?\s*$", line)
                if m:
                    if m.group(1).strip():
                        out.append(m.group(1).strip())
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
                "[BL-07] BLOCKED: {} matches read-only glob '{}' from "
                "sdlc.profile.yaml.\n"
                "Generated files and baselined snapshots are not hand-edited. Change the "
                "generator input and regenerate; if no generator exists, correct "
                "constraints.generated_files_glob in the profile.\n".format(fp, pattern))
            return 2

    cr = active_cr()
    if not cr:
        norm = fp.replace("\\", "/")
        for doc in read_baselined(PROFILE):
            d = doc.replace("\\", "/")
            if norm.endswith(d) or matches(norm, d):
                sys.stderr.write(
                    "[BL-02] BLOCKED: {} is baselined. A baselined document changes only "
                    "through an approved change request.\n"
                    "Open one with /sdlc_cr_analyze - /sdlc_cr_design writes the CR id to "
                    ".claude/.active_cr, which unblocks these edits until "
                    "/sdlc_cr_report clears it.\n"
                    "For an editorial correction that changes no meaning (BL-02 "
                    "exception): ask the user to confirm, then write EDITORIAL to "
                    ".claude/.active_cr for the duration and note it in the revision "
                    "history.\n".format(doc))
                return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
