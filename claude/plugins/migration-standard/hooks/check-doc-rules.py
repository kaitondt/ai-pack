#!/usr/bin/env python3
"""PreToolUse reminder: surface the document rules that apply to the file being written.

Non-blocking. Prints a short, targeted reminder based on which deliverable directory the
path falls in, so the rules that matter arrive at the moment of writing rather than only
at review time.
"""
import sys, json, os, re

PROFILE = os.path.join(os.environ.get("CLAUDE_PROJECT_DIR", "."),
                       ".claude", "migration.profile.yaml")

# directory keyword -> reminder
RULES = [
    (("screen", "画面設計", "ui-design"),
     "[SD] Screen design: fixed section order; continuous No counter across item "
     "subsections; dialogs in the 'other items' subsection; controlled type vocabulary "
     "only; no physical column names, route paths or component names; attribute/length "
     "blank for read-only fields; MSG-IDs use the module base; message text verbatim."),
    (("function", "機能設計", "processing"),
     "[FD] Function design: server-side scope only; top-down flow diagram with every "
     "branch labelled and every error path terminating in its MSG-ID; every diagram "
     "branch has a rule or error row; parameter names must match the interface document; "
     "paging and sorting explicit; state rounding and precision for every calculation."),
    (("interface", "api", "インタフェース"),
     "[API] Interface design: contract only, no behaviour or rationale; version segment "
     "present; every field typed with explicit nullability; paging names and error "
     "envelope match the project-wide convention; error set must match the function "
     "design; no internals in error responses."),
    (("data", "db", "DB設計", "schema"),
     "[DT] Data design: the only place physical names appear freely; reconcile every "
     "column against the legacy definition; decide null vs empty string per column; map "
     "every date sentinel; state rounding and precision; check uniqueness constraints "
     "against existing data before enforcing them."),
    (("batch", "バッチ", "job"),
     "[BT] Batch design: no UI, no HTTP, no paging; state expected and peak volume and "
     "the runtime window; commit points explicit in the flow; restart and rerun "
     "behaviour specified and compared with the legacy; record failures separated from "
     "run failures; file layouts copied exactly including headers and trailers."),
    (("detail-design", "詳細設計", "dd"),
     "[DD] Detail design: name real repository paths, do not restate the basic design; "
     "when code exists, run the GAP analysis and decide every verdict against the LEGACY "
     "source, never by editing the document to match the code."),
    (("test", "テスト"),
     "[UT/IT] Test design: expected values come from the legacy system with anchors, "
     "never from the current implementation; viewpoint 9 (rounding, truncation, date "
     "sentinels, century window, time zone, collation) is mandatory wherever numbers or "
     "dates are involved; leave result columns empty."),
]

ALWAYS = ("[DS] Every deliverable: fixed revision-history columns, NO automatic version "
          "bump, footer once at the end, Open Items section present ('None.' when empty), "
          "every behavioural claim anchored to legacy source or raised as SPEC-GAP.")


def deliverable_root(path):
    """Return docs_root from the profile, or a sensible default."""
    if os.path.exists(PROFILE):
        with open(PROFILE, encoding="utf-8") as fh:
            for line in fh:
                m = re.match(r"^\s+docs_root:\s+[\"']?([^\"'#]+?)[\"']?\s*$", line)
                if m:
                    return m.group(1).strip()
    return "docs"


def main():
    try:
        data = json.loads(sys.stdin.buffer.read().decode("utf-8"))
    except Exception:
        return 0
    fp = str(data.get("tool_input", {}).get("file_path", "")).replace("\\", "/")
    if not fp.endswith(".md"):
        return 0
    root = deliverable_root(fp)
    if root not in fp and "/docs/" not in fp:
        return 0
    lower = fp.lower()
    out = [m for keys, m in RULES if any(k.lower() in lower for k in keys)]
    if not out:
        return 0
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    print(ALWAYS)
    for line in out:
        print(line)
    return 0


if __name__ == "__main__":
    sys.exit(main())
