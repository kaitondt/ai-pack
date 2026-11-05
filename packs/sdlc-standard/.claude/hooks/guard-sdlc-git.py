#!/usr/bin/env python3
"""PreToolUse guard (Bash|PowerShell): git commits follow rules/sdlc/git-commit.md.

Acts only on shell commands that run git, and only in a project that has the profile.
Blocks, with the rule id:
  GT-01  a commit whose subject does not match commit.format (when commit.enforce is true),
         or a commit that would open an editor (no -m / -F).
  GT-02  sweeping stages - git add -A / --all / -u / . / * and git commit -a - when
         commit.stage_explicit_paths is true.
  GT-03  a commit or add that changes a read-only path. Paths in commit.regenerated_globs
         are exempt (a generator rewrites them); see ADD_UNDER_READONLY for new files.
  GT-04  a commit changing a baselined document while no change request is active, or whose
         message does not carry the active CR id; and, where the pack names CR-governed
         paths, a commit touching them during an active CR without its id.
  GT-05  staging an env or key file, git add -f, or a staged line that looks like a credential.
  GT-06  hook bypass (--no-verify, commit -n, core.hooksPath) and commits on
         commit.protected_branches.
  GT-07  rewriting or destroying history: --amend (unless commit.allow_amend and not yet
         pushed), force push, push --delete, reset --hard, clean -f, checkout/restore of the
         whole tree, branch -D, stash drop/clear, filter-branch/filter-repo, reflog expire,
         update-ref -d.
  GT-08  git push, unless commit.allow_push is true.

The hook is the backstop; /sdlc-commit is the way to commit. Exit 2 blocks the tool call and
returns stderr to the model.
"""
import fnmatch
import json
import os
import re
import shlex
import subprocess
import sys

# --- pack constants ---------------------------------------------------------------------------
PACK = "sdlc"
PROFILE_NAME = "sdlc.profile.yaml"
RULE_FILE = "rules/sdlc/git-commit.md"
COMMIT_COMMAND = "/sdlc-commit"
READONLY_KEY = "readonly_globs"          # list key in the profile holding read-only globs
FALLBACK_READONLY = ["**/*.generated.*"]
BASELINE_BLOCK = "baselined"             # list of "- path:" entries; "" = the pack has none
ACTIVE_CR_FILE = ".claude/.active_cr"    # "" = the pack has no active-CR marker
CR_HINT = "/sdlc-cr-analyze, then /sdlc-cr-design (it writes .claude/.active_cr)"
ADD_UNDER_READONLY = True                # new files under a read-only glob (a baseline snapshot)
CHECK_DESTRUCTIVE = True                 # GT-07 destructive git commands
ENV_FILES_KEY = ""                       # profile list of env files; "" = the built-in list
CR_GOVERNED_KEY = ""                     # profile list of paths that carry the active CR id; "" = none
# ----------------------------------------------------------------------------------------------

ROOT = os.environ.get("CLAUDE_PROJECT_DIR", ".")
PROFILE = os.path.join(ROOT, ".claude", PROFILE_NAME)

DEFAULTS = {
    "format": "{ID} {ACTION} {SUMMARY}",
    "actions": ["ADD", "UPDATE", "DELETE", "FIX", "REVIEW", "CONFIRM", "REFACTOR", "REVERT"],
    "id_pattern": "",
    "id_separator": ",",
    "no_id": "",
    "summary_max": "72",
    "body": "optional",
    "enforce": "true",
    "stage_explicit_paths": "true",
    "regenerated_globs": ["**/*.generated.*"],
    "protected_branches": [],
    "allow_push": "false",
    "allow_amend": "false",
}
# Any upper-case id that contains a digit: REQ-012, CR-2024-001, INT-003.2, XX0000PG-SC-001.
# The digit keeps an action word (UPDATE) from passing as an id.
DEFAULT_ID = r"(?=[A-Z0-9_.-]*[0-9])[A-Z][A-Z0-9_]*(?:[-.][A-Z0-9_]+)*"

DEFAULT_ENV_FILES = [".env", ".env.local", ".env.development.local", ".env.test.local",
                     ".env.production", ".env.production.local", ".env.staging"]
KEY_FILES = ["*.pem", "*.key", "*.p12", "*.pfx", "*.kdbx", "id_rsa", "id_rsa.*", "id_dsa",
             "id_ecdsa", "id_ed25519", "id_ed25519.*", ".npmrc", ".pypirc", ".netrc"]
SECRETS = [
    ("AWS access key", r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b"),
    ("GitHub token", r"\b(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{36,}\b"),
    ("GitHub fine-grained token", r"\bgithub_pat_[A-Za-z0-9_]{50,}"),
    ("Anthropic API key", r"\bsk-ant-[A-Za-z0-9_\-]{20,}"),
    ("OpenAI-style API key", r"\bsk-(?:proj-|svcacct-)?[A-Za-z0-9_\-]{32,}"),
    ("Stripe live key", r"\b(?:sk|rk)_live_[A-Za-z0-9]{20,}"),
    ("Slack token", r"\bxox[abprs]-[A-Za-z0-9-]{10,}"),
    ("Google API key", r"\bAIza[0-9A-Za-z_\-]{35}\b"),
    ("private key", r"-----BEGIN (?:RSA |EC |DSA |OPENSSH |PGP |ENCRYPTED )?PRIVATE KEY-----"),
]
OBVIOUS_FAKE = re.compile(r"(?i)example|fake|dummy|xxxxx|00000000|placeholder")
SEPARATORS = set(";&|\n")


# --- minimal YAML reading (no yaml dependency) -----------------------------------------------
def strip_comment(s):
    out, quote = [], None
    for i, ch in enumerate(s):
        if quote:
            if ch == quote:
                quote = None
        elif ch in "\"'":
            quote = ch
        elif ch == "#" and (i == 0 or s[i - 1] in " \t"):
            break
        out.append(ch)
    return "".join(out).strip()


def unquote(v):
    v = v.strip()
    if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
        v = v[1:-1]
        if v and '\\"' in v:
            v = v.replace('\\"', '"')
    return v


def inline_list(raw):
    body = raw.strip()[1:-1] if raw.strip().endswith("]") else raw.strip()[1:]
    items = re.findall(r"\"(?:[^\"\\]|\\.)*\"|'[^']*'|[^,]+", body)
    return [unquote(i) for i in items if unquote(i)]


def value(raw):
    raw = strip_comment(raw)
    if raw.startswith("["):
        return inline_list(raw)
    return unquote(raw)


def profile_lines():
    try:
        with open(PROFILE, encoding="utf-8") as fh:
            return fh.read().splitlines()
    except OSError:
        return None


def read_section(lines, name):
    """Top-level `name:` mapping -> {key: str | list}."""
    out, inside, indent, key = {}, False, None, None
    for line in lines:
        if not inside:
            if re.match(r"^{}:\s*(#.*)?$".format(re.escape(name)), line):
                inside = True
            continue
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        lead = len(line) - len(line.lstrip())
        if lead == 0:
            break
        m = re.match(r"^(\s+)([A-Za-z_][\w-]*):\s*(.*)$", line)
        if m and (indent is None or len(m.group(1)) == indent):
            indent = len(m.group(1))
            key = m.group(2)
            rest = strip_comment(m.group(3))
            out[key] = value(rest) if rest else []
            continue
        item = re.match(r"^\s+-\s+(.*)$", line)
        if item and key is not None and isinstance(out.get(key), list):
            out[key].append(value(item.group(1)))
    return out


def read_list(lines, key):
    """First `key:` anywhere -> list (block or inline)."""
    out, inside, indent = [], False, 0
    for line in lines:
        m = re.match(r"^(\s*){}:\s*(.*)$".format(re.escape(key)), line)
        if m and not inside:
            rest = strip_comment(m.group(2))
            if rest:
                v = value(rest)
                return v if isinstance(v, list) else [v]
            inside, indent = True, len(m.group(1))
            continue
        if inside:
            if not line.strip() or line.strip().startswith("#"):
                continue
            item = re.match(r"^(\s*)-\s+(.+?)\s*$", line)
            if item and len(item.group(1)) >= indent:
                v = value(item.group(2))
                if isinstance(v, str) and v and not v.endswith(":"):
                    out.append(v)
                continue
            break
    return out


def read_scalar(lines, key):
    for line in lines:
        m = re.match(r"^\s*{}:\s*(.+)$".format(re.escape(key)), line)
        if m:
            v = value(m.group(1))
            return v if isinstance(v, str) else ""
    return ""


def read_baselined(lines):
    if not BASELINE_BLOCK:
        return []
    out, inside = [], False
    for line in lines:
        if re.match(r"^\s*{}:".format(re.escape(BASELINE_BLOCK)), line):
            inside = True
            continue
        if inside:
            m = re.match(r"^\s+-\s+path:\s*(.*)$", line)
            if m:
                p = value(m.group(1))
                if isinstance(p, str) and p:
                    out.append(p)
                continue
            if line.strip() and not line.startswith((" ", "\t")):
                break
    return out


def config(lines):
    cfg = dict(DEFAULTS)
    section = read_section(lines, "commit")
    cfg.update({k: v for k, v in section.items() if v != [] or k in (
        "protected_branches", "regenerated_globs", "actions")})
    # Tokens are case-insensitive: {summary} is {SUMMARY}.
    cfg["format"] = re.sub(r"\{(\w+)\}", lambda m: "{" + m.group(1).upper() + "}",
                           str(cfg.get("format") or DEFAULTS["format"]))
    return cfg


def truthy(v):
    return str(v).strip().lower() in ("true", "yes", "on", "1")


# --- matching ---------------------------------------------------------------------------------
def matches(path, pattern):
    p = path.replace("\\", "/").lstrip("./") if path.startswith("./") else path.replace("\\", "/")
    pat = pattern.replace("\\", "/")
    if fnmatch.fnmatch(p, pat) or fnmatch.fnmatch(p, "*/" + pat.lstrip("/")):
        return True
    if pat.startswith("**/") and (fnmatch.fnmatch(p, pat[3:])
                                  or fnmatch.fnmatch(os.path.basename(p), pat[3:])):
        return True
    if pat.endswith("/**"):
        base = pat[:-3].lstrip("./")
        return p == base or p.startswith(base + "/") or ("/" + base + "/") in ("/" + p)
    return False


def any_match(path, patterns):
    return next((pat for pat in patterns if pat and matches(path, pat)), None)


# --- git --------------------------------------------------------------------------------------
def git(args, cwd):
    try:
        r = subprocess.run(["git"] + args, cwd=cwd, stdout=subprocess.PIPE,
                           stderr=subprocess.DEVNULL, timeout=5)
    except (OSError, subprocess.SubprocessError):
        return None
    if r.returncode != 0:
        return None
    return r.stdout.decode("utf-8", errors="replace")


def name_status(args, cwd):
    """[(status, path, old_path)] from `git <args> --name-status -z`."""
    out = git(args + ["--name-status", "-z", "-M"], cwd)
    if not out:
        return []
    parts, res, i = out.split("\0"), [], 0
    while i < len(parts) and parts[i]:
        st = parts[i]
        if st[:1] in "RC" and i + 2 < len(parts):
            res.append((st[0], parts[i + 2], parts[i + 1]))
            i += 3
        elif i + 1 < len(parts):
            res.append((st[0], parts[i + 1], ""))
            i += 2
        else:
            break
    return res


def status_paths(paths, cwd):
    """Changed paths `git add <paths>` would stage: [(status, path, old)]."""
    out = git(["status", "--porcelain=v1", "-z", "--untracked-files=all", "--"] + paths, cwd)
    if not out:
        return []
    parts, res, i = out.split("\0"), [], 0
    while i < len(parts) and parts[i]:
        entry = parts[i]
        xy, path = entry[:2], entry[3:]
        st = "A" if xy == "??" else (xy[1] if xy[1] != " " else xy[0])
        if "R" in xy:
            res.append(("R", path, parts[i + 1] if i + 1 < len(parts) else ""))
            i += 2
            continue
        res.append((st, path, ""))
        i += 1
    return res


def to_project_rel(path, cwd):
    top = git(["rev-parse", "--show-toplevel"], cwd)
    if not top:
        return [path]
    absolute = os.path.normpath(os.path.join(top.strip(), path))
    try:
        rel = os.path.relpath(absolute, os.path.abspath(ROOT)).replace("\\", "/")
    except ValueError:
        rel = path
    return [rel, path] if rel != path and not rel.startswith("..") else [path]


# --- command parsing --------------------------------------------------------------------------
def segments(cmd):
    try:
        lex = shlex.shlex(cmd, posix=True, punctuation_chars=";&|\n")
        lex.whitespace = " \t\r"
        lex.whitespace_split = True
        lex.commenters = ""
        tokens = list(lex)
    except ValueError:
        return None
    segs, cur = [], []
    for t in tokens:
        if t and set(t) <= SEPARATORS:
            if cur:
                segs.append(cur)
            cur = []
        else:
            cur.append(t)
    if cur:
        segs.append(cur)
    return segs


GLOBAL_WITH_VALUE = {"-C", "-c", "--git-dir", "--work-tree", "--namespace", "--exec-path",
                     "--config-env"}


def git_invocation(seg, cwd):
    """Return (subcommand, args, cwd, global_config) when seg runs git, else None."""
    i = 0
    while i < len(seg) and re.match(r"^[A-Za-z_][A-Za-z0-9_]*=", seg[i]):
        i += 1                                       # VAR=value prefixes
    if i < len(seg) and seg[i] in ("&", "."):
        i += 1                                       # PowerShell call operator
    if i >= len(seg):
        return None
    exe = os.path.basename(seg[i].replace("\\", "/")).lower()
    if exe not in ("git", "git.exe"):
        return None
    i += 1
    configs = []
    while i < len(seg) and seg[i].startswith("-"):
        opt = seg[i]
        if opt in GLOBAL_WITH_VALUE and i + 1 < len(seg):
            if opt == "-C":
                cwd = os.path.join(cwd, seg[i + 1])
            if opt in ("-c", "--config-env"):
                configs.append(seg[i + 1])
            i += 2
            continue
        if opt.startswith("-c") and len(opt) > 2:
            configs.append(opt[2:])
        i += 1
    if i >= len(seg):
        return None
    return seg[i], [a for a in seg[i + 1:] if not re.match(r"^\d*[<>]", a)], cwd, configs


COMMIT_VALUE_SHORT = set("mFCct")
COMMIT_VALUE_LONG = {"--message", "--file", "--reuse-message", "--reedit-message", "--fixup",
                     "--squash", "--author", "--date", "--template", "--cleanup", "--trailer",
                     "--pathspec-from-file", "--gpg-sign"}


def parse_commit(args):
    o = {"messages": [], "file": None, "reuse": False, "no_edit": False, "amend": False,
         "all": False, "no_verify": False, "fixup": False, "paths": [], "dry_run": False}
    i, after_dd = 0, False
    while i < len(args):
        a = args[i]
        if after_dd or not a.startswith("-") or a == "-":
            o["paths"].append(a)
            i += 1
            continue
        if a == "--":
            after_dd = True
        elif a.startswith("--"):
            name, _, val = a.partition("=")
            if name in COMMIT_VALUE_LONG and not _ and name != "--gpg-sign":
                val = args[i + 1] if i + 1 < len(args) else ""
                i += 1
            if name == "--message":
                o["messages"].append(val)
            elif name == "--file":
                o["file"] = val
            elif name in ("--reuse-message", "--reedit-message"):
                o["reuse"] = True
            elif name in ("--fixup", "--squash"):
                o["fixup"] = True
            elif name == "--no-edit":
                o["no_edit"] = True
            elif name == "--amend":
                o["amend"] = True
            elif name == "--all":
                o["all"] = True
            elif name == "--no-verify":
                o["no_verify"] = True
            elif name == "--dry-run":
                o["dry_run"] = True
        else:
            cluster = a[1:]
            for j, ch in enumerate(cluster):
                if ch in COMMIT_VALUE_SHORT:
                    val = cluster[j + 1:]
                    if not val:
                        val = args[i + 1] if i + 1 < len(args) else ""
                        i += 1
                    if ch == "m":
                        o["messages"].append(val)
                    elif ch == "F":
                        o["file"] = val
                    elif ch in "Cc":
                        o["reuse"] = True
                    break
                if ch == "a":
                    o["all"] = True
                elif ch == "n":
                    o["no_verify"] = True
        i += 1
    return o


def heredoc_body(cmd):
    m = re.search(r"<<-?\s*(['\"]?)(\w+)\1[^\n]*\n(.*?)\n\s*\2\s*(?:\n|$)", cmd, re.S)
    if m:
        return m.group(3)
    m = re.search(r"@(['\"])\r?\n(.*?)\r?\n\1@", cmd, re.S)
    return m.group(2) if m else None


def commit_message(o, raw_cmd, cwd):
    """(message or None, known: bool)."""
    if o["messages"]:
        return "\n\n".join(o["messages"]), True
    if o["file"] is not None:
        if o["file"] in ("-", "/dev/stdin"):
            body = heredoc_body(raw_cmd)
            return body, body is not None
        path = o["file"] if os.path.isabs(o["file"]) else os.path.join(cwd, o["file"])
        try:
            with open(path, encoding="utf-8") as fh:
                return fh.read(), True
        except OSError:
            return None, False                     # written earlier in this same command
    return None, False


# --- checks -----------------------------------------------------------------------------------
def id_regex(cfg):
    one = cfg.get("id_pattern") or DEFAULT_ID
    sep = re.escape(cfg.get("id_separator") or ",")
    ids = r"(?:{0})(?:\s*{1}\s*(?:{0}))*".format(one, sep)
    if cfg.get("no_id"):
        ids = r"(?:{}|{})".format(ids, re.escape(cfg["no_id"]))
    return ids


def subject_regex(cfg):
    actions = cfg.get("actions") or DEFAULTS["actions"]
    if isinstance(actions, str):
        actions = [actions]
    out = "^"
    for part in re.split(r"(\{[A-Z_]+\})", cfg.get("format") or DEFAULTS["format"]):
        if part == "{ID}":
            out += id_regex(cfg)
        elif part == "{ACTION}":
            out += "(?:" + "|".join(re.escape(a) for a in actions) + ")"
        elif part == "{SUMMARY}":
            out += r"(?P<summary>\S.*?)"
        elif re.match(r"^\{[A-Z_]+\}$", part):
            out += r".+?"
        else:
            out += re.escape(part)
    return out + r"\s*$"


def check_message(msg, cfg, errors):
    lines = [ln for ln in msg.replace("\r\n", "\n").split("\n") if not ln.startswith("#")]
    while lines and not lines[0].strip():
        lines.pop(0)
    subject = lines[0].strip() if lines else ""
    try:
        m = re.match(subject_regex(cfg), subject)
    except re.error as exc:
        errors.append(("GT-01", "commit.format / commit.id_pattern does not compile ({}). Fix the "
                       "profile; /{}-profile-check reports it.".format(exc, PACK)))
        return
    if not m:
        errors.append(("GT-01", "subject '{}' does not match commit.format '{}' "
                       "(actions: {}).".format(subject, cfg.get("format"),
                                               ", ".join(cfg.get("actions") or []))))
        return
    limit = int(cfg.get("summary_max") or 0) if str(cfg.get("summary_max", "")).isdigit() else 0
    summary = m.groupdict().get("summary") or ""
    if limit and len(summary) > limit:
        errors.append(("GT-01", "summary is {} characters; commit.summary_max is {}."
                       .format(len(summary), limit)))
    if str(cfg.get("body")).lower() == "required" and not any(ln.strip() for ln in lines[1:]):
        errors.append(("GT-01", "commit.body is 'required' and the message has no body."))


def read_active_cr():
    if not ACTIVE_CR_FILE:
        return None
    try:
        with open(os.path.join(ROOT, ACTIVE_CR_FILE), encoding="utf-8") as fh:
            return fh.read().strip()
    except OSError:
        return ""


def check_changes(changes, lines, cfg, cwd, errors, msg=None, msg_known=False):
    readonly = read_list(lines, READONLY_KEY) or FALLBACK_READONLY
    regenerated = cfg.get("regenerated_globs") or []
    if isinstance(regenerated, str):
        regenerated = [regenerated]
    env_files = (read_list(lines, ENV_FILES_KEY) if ENV_FILES_KEY else []) or DEFAULT_ENV_FILES
    baselined = read_baselined(lines)
    governed = read_list(lines, CR_GOVERNED_KEY) if CR_GOVERNED_KEY else []
    touched_baseline, touched_governed = [], []
    for st, path, old in changes:
        for cand in [p for p in (path, old) if p]:
            for p in to_project_rel(cand, cwd):
                if governed and any_match(p, governed) and cand not in touched_governed:
                    touched_governed.append(cand)
                pat = any_match(p, readonly)
                if pat and not any_match(p, regenerated) and not (st == "A" and ADD_UNDER_READONLY):
                    errors.append(("GT-03", "{} ({}) matches read-only glob '{}'. Read-only paths "
                                   "never change in a commit; restore it with `git restore "
                                   "--staged --worktree -- {}` after asking the user, or change "
                                   "the generator input.".format(cand, st, pat, cand)))
                    break
                if baselined and st != "A" and any(p.endswith(d.replace("\\", "/")) or matches(p, d)
                                                   for d in baselined):
                    touched_baseline.append(cand)
                    break
        base = os.path.basename(path)
        if st in "AMRC" and ((base in env_files or (base.startswith(".env.") and not re.search(
                r"\.(example|sample|template|dist)$", base))) or any(
                fnmatch.fnmatch(base, k) for k in KEY_FILES)):
            errors.append(("GT-05", "{} is an env or key file. It never goes into git: unstage it "
                           "(`git restore --staged -- {}`) and make sure .gitignore covers it."
                           .format(path, path)))
    if touched_baseline:
        cr = read_active_cr()
        docs = ", ".join(sorted(set(touched_baseline)))
        if cr is not None and not cr:
            errors.append(("GT-04", "{} is baselined and no change request is active. Open one "
                           "with {}.".format(docs, CR_HINT)))
        elif cr and cr.upper() != "EDITORIAL" and msg_known and msg is not None and cr not in msg:
            errors.append(("GT-04", "{} is baselined; the commit message must carry the active "
                           "CR id '{}'.".format(docs, cr)))
    if touched_governed and msg_known and msg is not None:
        cr = read_active_cr()
        docs = ", ".join(sorted(set(touched_governed))[:5])
        if cr and cr.upper() == "PENDING":
            errors.append(("GT-04", "a change request is open but its id is not known yet "
                           "(.active_cr = PENDING), and {} is under its documents. Get the id "
                           "from the client's CR list and write it to the marker first."
                           .format(docs)))
        elif cr and cr.upper() != "EDITORIAL" and cr not in msg:
            errors.append(("GT-04", "change request {} is active and {} is under the paths it "
                           "governs; the commit message must carry '{}'. Unrelated work is "
                           "committed after the CR closes, or the user clears the marker."
                           .format(cr, docs, cr)))


def check_secrets(diff_args, cwd, errors):
    out = git(diff_args + ["-U0", "--no-color", "--no-ext-diff"], cwd)
    if not out:
        return
    current = ""
    for line in out[:2000000].splitlines():
        if line.startswith("+++ "):
            current = line[6:] if line.startswith("+++ b/") else line[4:]
            continue
        if not line.startswith("+") or line.startswith("+++"):
            continue
        for name, pat in SECRETS:
            m = re.search(pat, line)
            if m and not OBVIOUS_FAKE.search(m.group(0)):
                s = m.group(0)
                errors.append(("GT-05", "{} adds what looks like a credential: {} ({}...). Remove it from the "
                               "file, read it from the environment instead, and tell the user to "
                               "rotate it if it is real.".format(current, name, s[:6])))
                return


def on_protected_branch(cfg, cwd):
    branches = cfg.get("protected_branches") or []
    if isinstance(branches, str):
        branches = [branches]
    if not branches:
        return None
    head = (git(["rev-parse", "--abbrev-ref", "HEAD"], cwd) or "").strip()
    return head if head and any(fnmatch.fnmatch(head, b) for b in branches) else None


def check_git(sub, args, cwd, configs, raw_cmd, lines, cfg, errors):
    for c in configs:
        if c.lower().startswith("core.hookspath"):
            errors.append(("GT-06", "overriding core.hooksPath bypasses the repository's git "
                           "hooks."))
    if sub == "config" and any(a.lower() == "core.hookspath" for a in args) and not any(
            a in ("--get", "--list", "-l") for a in args):
        errors.append(("GT-06", "changing core.hooksPath bypasses the repository's git hooks."))

    if sub == "add":
        flags = [a for a in args if a.startswith("-") and a != "--"]
        paths = [a for a in args if not a.startswith("-")]
        sweeping = any(a in ("-A", "--all", "-u", "--update", "--no-ignore-removal") or (
            re.match(r"^-[a-zA-Z]+$", a) and ("A" in a or "u" in a)) for a in flags) or any(
            p in (".", "*", ":/", "./", ":") for p in paths)
        if sweeping and truthy(cfg.get("stage_explicit_paths")):
            errors.append(("GT-02", "stage explicit paths, not the whole tree: `git add -- "
                           "<file> <file>` with the files you reviewed."))
        if any(a in ("-f", "--force") or (re.match(r"^-[a-zA-Z]+$", a) and "f" in a)
               for a in flags):
            errors.append(("GT-05", "git add -f stages a gitignored file - that is how secrets "
                           "and build output reach the repository."))
        if paths or sweeping:
            check_changes(status_paths(paths or ["."], cwd), lines, cfg, cwd, errors)
        return

    if sub == "commit":
        o = parse_commit(args)
        if o["dry_run"]:
            return
        if o["no_verify"]:
            errors.append(("GT-06", "--no-verify / -n skips the repository's commit hooks. Fix "
                           "what the hook reports instead."))
        if o["all"] and truthy(cfg.get("stage_explicit_paths")):
            errors.append(("GT-02", "git commit -a stages every tracked change. Stage the "
                           "reviewed files with `git add -- <file>` and commit without -a."))
        if o["amend"]:
            if not truthy(cfg.get("allow_amend")):
                errors.append(("GT-07", "--amend rewrites the last commit. Make a new commit, or "
                               "ask the user (commit.allow_amend is false)."))
            elif (git(["branch", "-r", "--contains", "HEAD"], cwd) or "").strip():
                errors.append(("GT-07", "--amend on a commit that is already pushed rewrites "
                               "shared history."))
        branch = on_protected_branch(cfg, cwd)
        if branch:
            errors.append(("GT-06", "'{}' is in commit.protected_branches. Commit on a work "
                           "branch and merge through review.".format(branch)))
        msg, known = commit_message(o, raw_cmd, cwd)
        skip_format = o["reuse"] or o["fixup"] or (o["no_edit"] and not o["messages"])
        if not known and not skip_format and o["file"] is None:
            errors.append(("GT-01", "no message given, so git would open an editor. Pass the "
                           "message with -m, or write it to a file and use -F <file>."))
        elif known and msg is not None and not skip_format and truthy(cfg.get("enforce")):
            check_message(msg, cfg, errors)
        changes = name_status(["diff", "--cached"], cwd)
        diff_sets = [["diff", "--cached"]]
        if o["all"]:
            changes += name_status(["diff"], cwd)
            diff_sets.append(["diff"])
        if o["paths"]:
            changes += name_status(["diff", "HEAD", "--"] + o["paths"], cwd)
            diff_sets.append(["diff", "HEAD", "--"] + o["paths"])
        check_changes(changes, lines, cfg, cwd, errors, msg, known)
        for d in diff_sets:
            check_secrets(d, cwd, errors)
        return

    if sub == "push":
        if not truthy(cfg.get("allow_push")):
            errors.append(("GT-08", "pushing is the user's step (commit.allow_push is false). "
                           "Report the commits and the push command instead."))
        if "--no-verify" in args:
            errors.append(("GT-06", "--no-verify skips the repository's pre-push hook."))
        if CHECK_DESTRUCTIVE:
            if any(a in ("--force", "-f", "--force-with-lease", "--force-if-includes", "--mirror")
                   or a.startswith("--force-with-lease=")
                   or (re.match(r"^-[a-zA-Z]+$", a) and "f" in a) for a in args) or any(
                       a.startswith("+") for a in args if not a.startswith("-")):
                errors.append(("GT-07", "force push rewrites shared history."))
            if any(a in ("--delete", "-d", "--prune") for a in args) or any(
                    a.startswith(":") and len(a) > 1 for a in args):
                errors.append(("GT-07", "push --delete / :ref removes a remote branch or tag."))
        return

    if not CHECK_DESTRUCTIVE:
        return
    flags = [a for a in args if a.startswith("-")]
    rest = [a for a in args if not a.startswith("-")]
    short = "".join(a[1:] for a in flags if re.match(r"^-[a-zA-Z]+$", a))
    hit = None
    if sub == "reset" and "--hard" in flags:
        hit = "git reset --hard discards uncommitted work"
    elif sub == "clean" and ("f" in short or "--force" in flags):
        hit = "git clean -f deletes untracked files"
    elif sub == "checkout" and ("." in rest or ":/" in rest or "-f" in flags or "--force" in flags):
        hit = "git checkout of the whole tree discards local changes"
    elif sub == "restore" and ("." in rest or ":/" in rest) and (
            "--worktree" in flags or "W" in short or not ("--staged" in flags or "S" in short)):
        hit = "git restore of the whole tree discards local changes"
    elif sub == "branch" and ("D" in short or ("--delete" in flags and (
            "--force" in flags or "f" in short))):
        hit = "git branch -D deletes an unmerged branch"
    elif sub == "stash" and rest[:1] and rest[0] in ("drop", "clear"):
        hit = "dropping stashes deletes saved work"
    elif sub in ("filter-branch", "filter-repo"):
        hit = "rewriting the whole history"
    elif sub == "reflog" and rest[:1] and rest[0] in ("expire", "delete"):
        hit = "expiring the reflog removes the way back"
    elif sub == "update-ref" and "-d" in flags:
        hit = "deleting a ref"
    if hit:
        errors.append(("GT-07", hit + ". Irreversible git operations are run by the user: show "
                       "them the exact command and what it destroys."))


def main():
    try:
        data = json.loads(sys.stdin.buffer.read().decode("utf-8"))
    except Exception:
        return 0
    cmd = (data.get("tool_input") or {}).get("command", "")
    if isinstance(cmd, list):
        cmd = cmd[-1] if len(cmd) >= 3 and cmd[-2] in ("-lc", "-c", "-Command") else " ".join(cmd)
    cmd = str(cmd)
    if not re.search(r"\bgit\b", cmd):
        return 0
    lines = profile_lines()
    if lines is None:
        return 0                                    # the pack is not adopted here
    cfg = config(lines)
    cwd = data.get("cwd") or ROOT
    segs = segments(cmd)
    errors = []
    if segs is None:
        # Unparseable (unbalanced quotes, here-strings): check only what a regex can see.
        if re.search(r"\bgit\b[^\n;&|]*\s--no-verify\b", cmd):
            errors.append(("GT-06", "--no-verify skips the repository's git hooks."))
        if re.search(r"\bgit\b[^\n;&|]*\bpush\b", cmd) and not truthy(cfg.get("allow_push")):
            errors.append(("GT-08", "pushing is the user's step (commit.allow_push is false)."))
    else:
        for seg in segs:
            if seg and seg[0].lower() in ("cd", "set-location", "sl", "pushd", "chdir") and len(seg) > 1:
                cwd = os.path.join(cwd, seg[1])
                continue
            inv = git_invocation(seg, cwd)
            if inv:
                sub, args, gcwd, configs = inv
                check_git(sub, args, gcwd, configs, cmd, lines, cfg, errors)
    if not errors:
        return 0
    seen, out = set(), []
    for rule, text in errors:
        if (rule, text) not in seen:
            seen.add((rule, text))
            out.append("[{}] BLOCKED: {}".format(rule, text))
    text = "\n".join(out) + "\nSee {} - {} stages, checks and writes the message in the " \
        "agreed format.\n".format(RULE_FILE, COMMIT_COMMAND)
    sys.stderr.flush()
    sys.stderr.buffer.write(text.encode("utf-8"))   # paths may be non-ASCII on any console
    sys.stderr.flush()
    return 2


if __name__ == "__main__":
    sys.exit(main())
