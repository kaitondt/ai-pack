#!/usr/bin/env python3
"""PreToolUse reminder: surface the management-document rules for the file being written.

Non-blocking. Prints a short, targeted reminder based on which management directory the path
falls in, so the rules that matter arrive at the moment of writing rather than at review time.
"""
import sys, json, os, re

PROFILE = os.path.join(os.environ.get("CODEX_PROJECT_DIR", "."),
                       ".codex", "pm.profile.yaml")

# directory keyword -> reminder
RULES = [
    (("charter",),
     "[CH] Charter: every objective needs a metric, today's value, a target and a date; success "
     "criteria objective enough that two readers reach the same verdict; the PM's authority "
     "written, not assumed; the budget envelope carries its estimating stage and its exclusions; "
     "high-level risks seed the register with owners and initial responses."),
    (("scope", "requirement"),
     "[SM] Scope: the scope baseline is scope statement + WBS + WBS dictionary; every exclusion "
     "carries a reason; every deliverable has objective acceptance criteria and a named acceptor "
     "agreed BEFORE the work starts; every requirement is testable, atomic, sourced and owned; "
     "nothing enters scope without a change request."),
    (("wbs",),
     "[WB] WBS: decompose deliverables (nouns), not activities; children total exactly the "
     "parent; 8/80 and never longer than one reporting period; one named owner per work package; "
     "verifiable acceptance criteria; the dictionary states what is explicitly NOT included; keep "
     "the management, QA and handover branches with real effort in them."),
    (("schedule", "milestone"),
     "[SH] Schedule: durations are DERIVED from effort using real productive hours, allocation "
     "and waiting time - never declared; dependency type and category recorded; the critical path "
     "named; buffers visible and owned by the PM, never padding inside estimates; milestones have "
     "objective criteria and payment-linked ones are marked; baseline and working file stay "
     "separate files."),
    (("cost", "budget", "estimate"),
     "[CT/ES] Cost and estimates: never a bare number - method, basis, range, assumptions, "
     "exclusions, estimator and date; effort, duration and cost are three different numbers; "
     "contingency is inside the baseline and management reserve outside it; the cost baseline is "
     "time-phased from the schedule; every contingency drawdown is logged with its risk and "
     "approver."),
    (("report", "status", "weekly", "monthly", "quarterly", "daily"),
     "[RI] Reporting: every number carries its source and as-of date - nothing from memory or "
     "from the last report; progress by the profile's method only (no 90%); RAG computed from "
     "thresholds then explained in one sentence, never green over a red section; every variance "
     "has a specific cause, an impact and an action with an owner and a date; not collected is a "
     "legitimate status, invented is not."),
    (("quality", "test-plan", "testplan"),
     "[QP] Quality: every objective states target, condition, measurement method and verifying "
     "level; entry and exit criteria objective and enforced; severity model and the "
     "defect-versus-change-request rule agreed BEFORE testing starts; defects attributed to the "
     "phase that injected them; no severity adjusted to pass a gate."),
    (("risk", "issue"),
     "[RK] Risk: write cause -> event -> effect, never a single noun; probability and impact on "
     "the profile's anchored scales; 'monitor' is not a response - avoid, mitigate, transfer, "
     "accept or escalate, each with an action, an owner and a trigger; state the secondary and "
     "residual risk; a materialised risk becomes an issue and keeps the risk id as its ancestor."),
    (("change", "/cr"),
     "[IC] Change control: log every change including the trivial ones; determine defect vs "
     "clarification vs change by QUOTING the baselined document, before any fix; assess every "
     "impact dimension including documentation and test; schedule impact is not effort impact; "
     "present at least two options with a recommendation; baselines update before execution "
     "begins."),
    (("process", "audit", "capa"),
     "[PR] Process: entry and exit criteria objective enough that two people reach the same "
     "verdict; tailoring recorded with reason, risk accepted and approver; QA and QC separated, "
     "and QA never performed by the person being assured; audits sample artifacts, not opinions; "
     "every CAPA has a root cause and an effectiveness check date."),
    (("closing", "acceptance", "lesson", "handover"),
     "[CL] Closing: acceptance per deliverable against the criteria agreed at planning time, with "
     "evidence and a named acceptor; 'accepted with conditions' is a distinct state; every open "
     "defect, CR, risk, action and assumption gets a disposition; the final report measures "
     "against the CHARTER, not the last re-baselined plan; a lesson needs a destination and an "
     "owner or it is an anecdote."),
    (("resource", "raci", "staffing"),
     "[RM] Resource: derive the requirement from the schedule, not from available headcount; "
     "nobody planned above the profile's allocation limit; ramp-up and mentoring are work "
     "packages in the WBS; every single-holder role is a risk with a concrete response; exactly "
     "one Accountable per RACI row."),
    (("meeting", "minute"),
     "[RG] Minutes: circulate within one working day; decisions as DEC-* with owners, actions as "
     "ACT-* with owners and due dates; record disagreements as disagreements; state that silence "
     "by a named date is acceptance. Discussion narrative is not the point - in six months only "
     "the decisions and the actions matter."),
]

ALWAYS = ("[MD] Every management deliverable: title block with status, revision history, approval "
          "block, distribution list, Open Items section ('None.' when empty, each item with one "
          "named owner and a due date), references cited WITH versions, numbers carrying units "
          "and as-of dates, NO automatic version bump, and every commitment traceable to the "
          "charter, a baselined document, an approved CR or a recorded decision.")


def pm_root():
    if os.path.exists(PROFILE):
        with open(PROFILE, encoding="utf-8") as fh:
            for line in fh:
                m = re.match(r"^\s+pm_root:\s+[\"']?([^\"'#]+?)[\"']?\s*$", line)
                if m:
                    return m.group(1).strip()
    return "pm"


def main():
    try:
        data = json.loads(sys.stdin.buffer.read().decode("utf-8"))
    except Exception:
        return 0
    fp = str(data.get("tool_input", {}).get("file_path", "")).replace("\\", "/")
    if not fp.endswith(".md"):
        return 0
    root = pm_root().lower()
    lower = fp.lower()
    if re.search(r"(^|/){}/".format(re.escape(root)), lower) is None:
        return 0
    out = [m for keys, m in RULES if any(k in lower for k in keys)]
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
