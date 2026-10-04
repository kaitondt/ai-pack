---
name: pm_workflow
description: "Route a pm pack task to the correct lifecycle workflow. Use when the user asks to start, plan, build, test, review, release, report, or assess work governed by this pack."
---

# pm workflow router

1. Read `.codex/pm.profile.yaml`. If it is missing, stop and ask the user to adopt the pack by copying the profile template from this plugin and its generated `AGENTS.md` into the repository root.
2. Load `pm_project` first, then the phase/area skill it routes to.
3. Treat legacy slash-command names as workflow aliases, not literal Codex commands. Their source procedures are in `references/commands/`.
4. Follow the profile, invariant rules, and evidence/reporting requirements; do not invent project values.

Legacy workflow aliases: `/pm_audit` · `/pm_change_apply` · `/pm_change_assess` · `/pm_charter` · `/pm_closing` · `/pm_comm_plan` · `/pm_cost_baseline` · `/pm_estimate` · `/pm_evm` · `/pm_gate_review` · `/pm_health_check` · `/pm_init` · `/pm_lessons` · `/pm_plan` · `/pm_process_define` · `/pm_profile_check` · `/pm_quality_plan` · `/pm_refine_skill` · `/pm_report` · `/pm_resource_plan` · `/pm_risk_assess` · `/pm_risk_review` · `/pm_schedule_baseline` · `/pm_scope_baseline` · `/pm_status_collect` · `/pm_sync_technical` · `/pm_trace_check` · `/pm_wbs`
