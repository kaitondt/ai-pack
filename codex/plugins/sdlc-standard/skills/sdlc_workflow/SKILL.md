---
name: sdlc_workflow
description: "Route a sdlc pack task to the correct lifecycle workflow. Use when the user asks to start, plan, build, test, review, release, report, or assess work governed by this pack."
---

# sdlc workflow router

1. Read `.codex/sdlc.profile.yaml`. If it is missing, stop and ask the user to adopt the pack by copying the profile template from this plugin and its generated `AGENTS.md` into the repository root.
2. Load `sdlc_project` first, then the phase/area skill it routes to.
3. Treat legacy slash-command names as workflow aliases, not literal Codex commands. Their source procedures are in `references/commands/`.
4. Follow the profile, invariant rules, and evidence/reporting requirements; do not invent project values.

Legacy workflow aliases: `/sdlc_context_map` · `/sdlc_cr_analyze` · `/sdlc_cr_design` · `/sdlc_cr_implement` · `/sdlc_cr_report` · `/sdlc_discover` · `/sdlc_generate_basic_design` · `/sdlc_generate_detail_design` · `/sdlc_generate_infra` · `/sdlc_generate_mockup` · `/sdlc_generate_requirements` · `/sdlc_generate_test` · `/sdlc_generate_testscript` · `/sdlc_implement_feature` · `/sdlc_init` · `/sdlc_maintain_fix` · `/sdlc_maintain_intake` · `/sdlc_maintain_report` · `/sdlc_phase_gate` · `/sdlc_profile_check` · `/sdlc_quality_report` · `/sdlc_refine_skill` · `/sdlc_release_check` · `/sdlc_review_commit` · `/sdlc_review_design` · `/sdlc_review_testcase` · `/sdlc_scaffold_codebase` · `/sdlc_template_register` · `/sdlc_test_lifecycle` · `/sdlc_trace_bug` · `/sdlc_trace_check` · `/sdlc_translate` · `/sdlc_triage_defects` · `/sdlc_uat_prepare` · `/sdlc_uat_report` · `/sdlc_uat_triage` · `/sdlc_verify_build`
