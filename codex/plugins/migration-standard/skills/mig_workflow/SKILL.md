---
name: mig_workflow
description: "Route a mig pack task to the correct lifecycle workflow. Use when the user asks to start, plan, build, test, review, release, report, or assess work governed by this pack."
---

# mig workflow router

1. Read `.codex/migration.profile.yaml`. If it is missing, stop and ask the user to adopt the pack by copying the profile template from this plugin and its generated `AGENTS.md` into the repository root.
2. Load `mig_project` first, then the phase/area skill it routes to.
3. Treat legacy slash-command names as workflow aliases, not literal Codex commands. Their source procedures are in `references/commands/`.
4. Follow the profile, invariant rules, and evidence/reporting requirements; do not invent project values.

Legacy workflow aliases: `/mig_analyze_legacy` · `/mig_context_map` · `/mig_cr_analyze` · `/mig_cr_design` · `/mig_cr_implement` · `/mig_cr_report` · `/mig_generate_basic_design` · `/mig_generate_detail_design` · `/mig_generate_infra` · `/mig_generate_mockup` · `/mig_generate_requirements` · `/mig_generate_test` · `/mig_generate_testscript` · `/mig_implement_feature` · `/mig_init` · `/mig_profile_check` · `/mig_refine_skill` · `/mig_review_commit` · `/mig_review_design` · `/mig_review_testcase` · `/mig_scaffold_codebase` · `/mig_template_register` · `/mig_test_lifecycle` · `/mig_trace_bug` · `/mig_trace_check` · `/mig_translate` · `/mig_triage_failures` · `/mig_uat_fix` · `/mig_uat_investigate` · `/mig_uat_report` · `/mig_verify_build`
