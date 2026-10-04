#!/usr/bin/env python3
"""PreToolUse reminder: surface the document rules that apply to the file being written.

Non-blocking. Prints a short, targeted reminder based on which deliverable directory the
path falls in, so the rules that matter arrive at the moment of writing rather than only
at review time.
"""
import sys, json, os, re

PROFILE = os.path.join(os.environ.get("CODEX_PROJECT_DIR", "."),
                       ".codex", "sdlc.profile.yaml")

# directory keyword -> reminder
RULES = [
    (("inception", "scope", "glossary", "decision"),
     "[P0] Inception: every scope exclusion carries a reason; every BR has an owner and a "
     "priority; decisions are appended to the decision log with option, owner and date and "
     "are never rewritten (BL-05); a term enters the glossary once and is then used "
     "everywhere unchanged."),
    (("requirement", "srs", "要件"),
     "[RQ] Requirements: one testable statement per row, no conjunctions hiding two "
     "requirements; every REQ traces to a BR; every NFR states target, condition and "
     "measurement method (RS-07); TBD is written as TBD with an ASM id and a due date, "
     "never as a plausible value; no screen layout, no table names, no technology."),
    (("non-functional", "nfr", "architecture", "方式"),
     "[NF] NFR / architecture: each quality attribute gets target, condition, measurement "
     "method and the ST case that verifies it; every architecture decision records the "
     "options rejected and why (DEC-*); state which NFR each decision is serving - an "
     "architecture with no NFR behind it is a preference."),
    (("screen-design", "画面設計", "ui-design"),
     "[SD] Screen design: fixed section order; continuous No counter across item "
     "subsections; dialogs in the 'other items' subsection; controlled type vocabulary "
     "only; no physical column names, route paths or component names; attribute/length "
     "blank for read-only fields; MSG-IDs use the module base."),
    (("function-design", "機能設計", "処理設計"),
     "[FD] Function design: server-side scope only; top-down flow diagram with every "
     "branch labelled and every error path terminating in its MSG-ID; every diagram branch "
     "has a rule or error row; parameter names must match the interface document; paging "
     "and sorting explicit; state rounding and precision for every calculation."),
    (("interface-design", "api-design", "インタフェース"),
     "[API] Interface design: contract only, no behaviour or rationale; version segment "
     "present; every field typed with explicit nullability; paging names and error "
     "envelope match the project-wide convention; the error set must match the function "
     "design; no internals in error responses."),
    (("data-design", "db設計", "DB設計", "/db/"),
     "[DT] Data design: the only place physical names appear freely; every column traces "
     "to a requirement or is justified as technical; decide null vs empty per column; "
     "state precision, scale and time zone; name the index behind every query the design "
     "promises to be fast; retention and personal-data classification per table."),
    (("batch-design", "バッチ設計", "batch-job"),
     "[BT] Batch design: no UI, no HTTP, no paging; state expected and peak volume and the "
     "runtime window; commit points explicit in the flow; restart and rerun behaviour "
     "specified; record failures separated from run failures; file layouts exact, "
     "including headers and trailers."),
    (("detail-design", "詳細設計", "/dd"),
     "[DD] Detail design: name real repository paths; do not restate the basic design; "
     "describe the internals a UT case can be written against; when code exists, run the "
     "drift check and decide every verdict against the DESIGN, never by editing the "
     "document to match the code."),
    (("test", "テスト", "/uat"),
     "[TEST] Test design: expected values come from the baselined specification with an "
     "anchor, never from what the implementation currently returns; state the level the "
     "case belongs to and the document it verifies; viewpoint VP-10 (rounding, precision, "
     "dates, time zone, collation) is mandatory wherever numbers or dates appear; leave "
     "result columns empty."),
    (("maintenance", "incident", "保守"),
     "[MT] Maintenance: every incident gets a class, a severity, a root cause and an "
     "injection phase; a fix ships with the regression test that would have caught it; a "
     "hotfix still owes its documents inside the retro-documentation window (BL-06)."),
]

ALWAYS = ("[DS] Every deliverable: fixed revision-history columns, review record present, "
          "NO automatic version bump, footer once at the end, Open Items section present "
          "('None.' when empty) with an owner and a due date per item, and every "
          "behavioural claim anchored to a requirement, decision or elicitation record.")


def deliverable_root():
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
    root = deliverable_root()
    lower = fp.lower()
    # A deliverable lives under docs_root, or under one of the record trees. Match on
    # path segments so a repo-relative path like "test/cases/..." is recognised too.
    in_tree = bool(re.search(r"(^|/)(test|uat|maintenance|change-requests)/", lower)) \
        or re.search(r"(^|/){}/".format(re.escape(root.lower())), lower) is not None
    if not in_tree:
        return 0
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
