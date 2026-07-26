#!/usr/bin/env node
"use strict";

const fs = require("fs");
const os = require("os");
const path = require("path");
const childProcess = require("child_process");

const SYSTEM_ID = "document-slide-authoring-representative-agent-system";
const REQUIRED_AGENTS = [
  "representative-agent",
  "evidence-intake-agent",
  "cognitive-authoring-agent",
  "writing-agent",
  "storyline-readability-agent",
  "session-feedback-agent",
  "visualization-agent",
  "pptx-build-agent",
  "artifact-surface-agent",
  "presentationml-compliance-agent",
  "repetition-gate-agent",
  "powerpoint-open-check-agent"
];

const REQUIRED_SKILLS = [
  { id: "evidence-freeze-skill", path: "agent-system/skills/evidence-freeze/SKILL.md" },
  { id: "working-source-clarification-skill", path: "agent-system/skills/working-source-clarification/SKILL.md" },
  { id: "ziphyun-particle-research-skill", path: "agent-system/skills/ziphyun-particle-research/SKILL.md" },
  { id: "cognitive-document-visual-authoring-skill", path: "agent-system/skills/cognitive-document-visual-authoring/SKILL.md" },
  { id: "writing-flow-skill", path: "agent-system/skills/writing-flow/SKILL.md" },
  { id: "storyline-readability-gate-skill", path: "agent-system/skills/storyline-readability-gate/SKILL.md" },
  { id: "session-feedback-pattern-gate-skill", path: "agent-system/skills/session-feedback-pattern-gate/SKILL.md" },
  { id: "semantic-staging-design-skill", path: "agent-system/skills/semantic-staging-design/SKILL.md" },
  { id: "visualization-flow-skill", path: "agent-system/skills/visualization-flow/SKILL.md" },
  { id: "pptx-native-build-skill", path: "agent-system/skills/pptx-native-build/SKILL.md" },
  { id: "drawingml-table-anchor-sanitizer-skill", path: "agent-system/skills/drawingml-table-anchor-sanitizer/SKILL.md" },
  { id: "artifact-surface-separation-skill", path: "agent-system/skills/artifact-surface-separation/SKILL.md" },
  { id: "presentationml-compliance-skill", path: "agent-system/skills/presentationml-compliance/SKILL.md" },
  { id: "repetition-release-gate-skill", path: "agent-system/skills/repetition-release-gate/SKILL.md" },
  { id: "powerpoint-human-open-check-skill", path: "agent-system/skills/powerpoint-human-open-check/SKILL.md" },
  { id: "routing-experiment-gate-skill", path: "agent-system/skills/routing-experiment-gate/SKILL.md" }
];

const REQUIRED_TOOLS = [
  "manual-check",
  "prompt-check",
  "pipeline-check",
  "tools-check",
  "system-init",
  "system-run",
  "research-build",
  "research-check",
  "working-source-clarification-check",
  "course-flow-map-check",
  "cognitive-authoring-packet-check",
  "outline-note-check",
  "slide-planning-map-check",
  "storyline-readability-check",
  "session-feedback-pattern-check",
  "symbol-inventory-check",
  "semantic-design-system-check",
  "semantic-staging-design-check",
  "image-first-visualization-check",
  "vlpp-expression-distance-check",
  "artifact-surface-separation-check",
  "pptx-standard-xml-build",
  "pptx-build",
  "presentationml-spec-check",
  "native-powerpoint-check",
  "recovery-compare-check",
  "repetition-gate-check",
  "release-check",
  "agent-system-check",
  "manual-powerpoint-open-check",
  "routing-experiment-check"
];

const REQUIRED_WORKFLOW_STAGES = [
  "evidence-freeze",
  "working-source-clarification",
  "course-flow-map",
  "cognitive-authoring-packet",
  "writing-flow",
  "outline-note-gate",
  "slide-planning-map",
  "storyline-readability-gate",
  "session-feedback-pattern-gate",
  "symbol-inventory",
  "semantic-design-system",
  "semantic-staging-design-gate",
  "image-first-visualization-gate",
  "open-visualization-planning",
  "new-pptx-native-build",
  "presentationml-compliance",
  "artifact-surface-separation",
  "repetition-release-gate",
  "powerpoint-open-check",
  "routing-experiment-gate",
  "representative-closeout"
];

const REQUIRED_RELEASE_GATES = [
  "agent-system-integrity",
  "working-source-clarification",
  "course-flow-map",
  "cognitive-authoring-packet",
  "outline-notes-before-pptx",
  "slide-planning-map",
  "storyline-readability-proxy",
  "session-feedback-patterns",
  "symbol-inventory",
  "semantic-design-system",
  "semantic-staging-design",
  "image-first-visualization-proof",
  "vlpp-expression-distance-boundary",
  "presentationml-source-coverage",
  "native-powerpoint-package",
  "artifact-surface-separation",
  "repetition-infrastructure",
  "release-readiness",
  "manual-powerpoint-open-success",
  "routing-experiment-coverage"
];

const REQUIRED_SKILL_HEADINGS = ["## Trigger", "## Inputs", "## Outputs", "## Tools", "## Exit Gate"];
const REQUIRED_AUTHORING_PACKET_FIELDS = [
  "process_lock",
  "reader_situation",
  "cognitive_task",
  "desired_action",
  "semantic_fit",
  "evidence_boundary",
  "output_route",
  "verification_surface",
  "folded_unit",
  "weakness_diagnosis",
  "cta_interview_log",
  "unfolding_trace",
  "seed_sentence",
  "title_sequence",
  "knowledge_split",
  "visual_rationale",
  "visual_value_spec",
  "cognitive_load_risks",
  "transfer_artifact",
  "stage_gate_log"
];
const REQUIRED_VISUAL_VALUE_FIELDS = [
  "design_intent",
  "reader_path_support",
  "readability_accessibility",
  "native_medium_constraints",
  "chosen_values",
  "intentionally_unconstrained"
];
const REQUIRED_READABILITY_FIT_FIELDS = [
  "readability_target",
  "audience_distance_or_device",
  "fit_rationale",
  "intentionally_unconstrained"
];
const REQUIRED_OUTLINE_NOTE_FIELDS = [
  "reader_situation",
  "deck_or_document_purpose",
  "section_flow",
  "slide_sequence",
  "title_story_draft",
  "visible_message",
  "spoken_or_facilitation_notes",
  "evidence_links",
  "visual_intent",
  "open_questions"
];
const REQUIRED_CLARIFICATION_FIELDS = [
  "goal",
  "scope",
  "excluded_surfaces",
  "working_source_of_truth",
  "success_condition",
  "evidence_target",
  "runtime_target",
  "provider_provenance",
  "output_brand"
];
const REQUIRED_THREE_LAYER_FIELDS = [
  "fixed",
  "flexible",
  "decisional",
  "drift_rule"
];
const REQUIRED_INTENTIONAL_IMPLEMENTATION_FIELDS = [
  "fixed",
  "flexible",
  "decisional",
  "calculated_values",
  "implementation_trace"
];
const REQUIRED_CALCULATED_VALUE_FIELDS = [
  "semantic_role",
  "reader_situation",
  "medium_constraint",
  "safe_area",
  "readable_size",
  "density",
  "scan_path",
  "action_exit",
  "element_tradeoff",
  "element_placement",
  "front_back_order"
];
const REQUIRED_LAYOUT_ELEMENT_CALCULATION_FIELDS = [
  "element_id",
  "semantic_role",
  "element_tradeoff",
  "attention_cost",
  "space_cost",
  "semantic_gain",
  "placement",
  "front_back_order",
  "reading_order",
  "native_object_order",
  "overlap_risk"
];
const REQUIRED_COURSE_FLOW_FIELDS = [
  "program_goal",
  "audience_context",
  "fixed_schedule",
  "module_sequence",
  "session_timing",
  "learning_arc",
  "output_chain",
  "constraints_and_non_goals"
];
const REQUIRED_SLIDE_PLANNING_FIELDS = [
  "source_module",
  "slide_goal",
  "visual_situation",
  "cognitive_operation",
  "learner_action",
  "output_artifact",
  "timing_budget",
  "evidence_boundary",
  "reuse_policy"
];
const REQUIRED_SYMBOL_INVENTORY_FIELDS = [
  "symbol_id",
  "semantic_role",
  "source_context",
  "target_expression_vector",
  "possible_confusions",
  "visual_candidates",
  "selection_reason",
  "learner_facing_boundary"
];
const REQUIRED_SEMANTIC_DESIGN_SYSTEM_FIELDS = [
  "design_principles",
  "symbol_mapping",
  "layout_families",
  "typography_rules",
  "color_logic",
  "image_style_rules",
  "pptx_element_use",
  "layout_element_calculations",
  "accessibility_and_density",
  "calculated_values",
  "implementation_trace"
];
const REQUIRED_SESSION_FEEDBACK_CHECKS = [
  "title_story_naturalness",
  "decorative_load",
  "internal_metadata_relevance",
  "legal_or_regulated_ai_boundary",
  "citation_link_integrity",
  "table_or_slide_body_fit",
  "prompt_structure_knowledge_split"
];
const REQUIRED_STAGING_DESIGN_FIELDS = [
  "scene_beat",
  "attention_entry",
  "curiosity_gap",
  "reading_path",
  "listening_cue",
  "evidence_reveal",
  "semantic_variables",
  "accessibility_and_load",
  "design_freedom_boundary",
  "open_expression_options",
  "selected_expression_rationale",
  "avoid_unnecessary_constraints"
];
const REQUIRED_IMAGE_FIRST_VISUALIZATION_FIELDS = [
  "image_first_visualization_surface",
  "visual_candidate_set",
  "candidate_semantic_role",
  "target_expression_vector",
  "expression_vector_dimensions",
  "candidate_expression_vectors",
  "distance_metric",
  "distance_to_target",
  "candidate_strength_formula",
  "selected_candidate",
  "monitoring_rules",
  "evidence_state",
  "claim_boundary",
  "learner_facing_boundary"
];
const REQUIRED_ARTIFACT_SURFACES = [
  "learner_facing",
  "instructor_facilitator",
  "production_source",
  "evidence_fact_table",
  "render_native_proof",
  "delivery_handoff"
];
const REQUIRED_ROUTING_EXPERIMENT_FIELDS = [
  "should_trigger",
  "should_not_trigger",
  "expected_behavior",
  "near_miss_rationale"
];
const COMPATIBLE_NPM_WORKSPACE = "/Volumes/Extend/lecture-works/AX-Groups/AX/Training/.work/agentic_paradigm_editable";
const COMPATIBLE_NPM_STATE_OUTPUTS = [
  "09-system-state.json",
  "10-system-runbook.md",
  "11-release-packet.md"
];
const COMPATIBLE_NPM_BUILD_OUTPUT = "Document_Slide_Authoring_System_new.pptx";
const COMPATIBLE_NPM_MANUAL_OPEN_CHECK = "manual-open-checks/latest-powerpoint-open-check.json";
const COMPATIBLE_NPM_ACCEPTED_RELEASE_STATUSES = [
  "pass",
  "pass_superseded_old_recovery_artifacts"
];
const RUNTIME_COMPATIBILITY_STATUSES = new Set([
  "shared-core only / no-delta",
  "runtime-delta implemented",
  "runtime target known, but manual fallback only"
]);

const SKILL_MODULE_DEFINITIONS = [
  {
    dir: "evidence-freeze",
    title: "Evidence Freeze Skill",
    skillId: "evidence-freeze-skill",
    owner: "evidence-intake-agent",
    trigger: "Use this skill before writing or visualization decisions when source inventory, uncertainty, or evidence boundaries must be fixed.",
    inputs: ["source material", "audience context", "uncertainty list", "project constraints"],
    outputs: ["source inventory", "evidence state labels", "claim boundary", "research handoff"],
    tools: ["project-specific inventory check", "research check"],
    exitGate: "Exit only when observed evidence, inferred proxies, human outcomes, and blocked external claims are separated."
  },
  {
    dir: "working-source-clarification",
    title: "Working Source Clarification Skill",
    skillId: "working-source-clarification-skill",
    owner: "evidence-intake-agent",
    trigger: "Use this skill when source materials, target audience, output surfaces, runtime, provider provenance, or success conditions must be fixed before authoring.",
    inputs: ["source inventory", "user request", "workspace constraints", "known exclusions", "target runtime"],
    outputs: ["working source of truth", "clarification packet", "conflict resolution log", "fixed/flexible/decisional classification"],
    tools: ["working-source-clarification check"],
    exitGate: "Exit only when the working source, clarification packet, conflict priority, and three-layer classification are explicit enough to prevent drift."
  },
  {
    dir: "ziphyun-particle-research",
    title: "Ziphyun Particle Research Skill",
    skillId: "ziphyun-particle-research-skill",
    owner: "evidence-intake-agent",
    trigger: "Use this skill when research must be normalized into corpus, particles, concept map, and a Ziphyun-ready handoff.",
    inputs: ["raw sources", "source inventory", "chapter or topic boundaries", "retrieval tags"],
    outputs: ["canonical corpus", "particles.v1", "concept map", "Ziphyun handoff"],
    tools: ["project-specific research build", "project-specific research check"],
    exitGate: "Exit only when the handoff is explicit and direct Ziphyun ingest is not implied unless a separate ingest tool is used."
  },
  {
    dir: "cognitive-document-visual-authoring",
    title: "Cognitive Document Visual Authoring Skill",
    skillId: "cognitive-document-visual-authoring-skill",
    owner: "cognitive-authoring-agent",
    trigger: "Use this skill before writing, slide design, report writing, visualization, or PPTX implementation when reader situation, semantic fit, unfolding, or visual values must be fixed.",
    inputs: ["evidence boundary", "reader situation", "folded or weak content unit", "output route", "verification surface"],
    outputs: ["cognitive authoring packet", "semantic fit", "CTA interview log", "unfolding trace", "knowledge split", "visual rationale", "visual value spec", "stage gate log"],
    tools: ["cognitive authoring packet check"],
    exitGate: "Exit only when reader situation, cognitive task, desired action, evidence boundary, unfolding trace, title sequence, knowledge split, and visual value spec are explicit."
  },
  {
    dir: "writing-flow",
    title: "Writing Flow Skill",
    skillId: "writing-flow-skill",
    owner: "writing-agent",
    trigger: "Use this skill when evidence must become whole-course flow, brief, seed, MCII, outline, outline notes, slide planning map, slide specs, and reader judgment.",
    inputs: ["source inventory", "research corpus", "audience", "reader situation", "fixed schedule", "module/session constraints"],
    outputs: ["course flow map", "brief", "seed", "MCII", "outline", "outline notes", "draft slide titles", "slide planning map", "slide specs", "visible/spoken message split"],
    tools: ["course flow map check", "manual check", "prompt check", "pipeline check", "outline note check", "slide planning map check"],
    exitGate: "Exit only when course-flow-map.md fixes the whole lecture flow before slide planning, slide-planning-map.json connects situation, cognitive operation, learner action, output artifact, timing, evidence, and reuse policy, and outline notes separate reader situation, section flow, visible message, spoken notes, evidence, visual intent, and open questions before PPTX work starts."
  },
  {
    dir: "storyline-readability-gate",
    title: "Storyline Readability Gate Skill",
    skillId: "storyline-readability-gate-skill",
    owner: "storyline-readability-agent",
    trigger: "Use this skill before visualization or PPTX build when slide titles, story flow, assertion-evidence fit, or cognitive load must be checked.",
    inputs: ["outline notes", "outline", "draft slide titles", "slide specs", "reader situation", "evidence and source IDs"],
    outputs: ["title-only storyline", "assertion-evidence map", "one-beat review", "5-second scan proxy", "cognitive load proxy", "evidence boundary notes", "revision queue"],
    tools: ["title-only story test", "assertion-evidence test", "cognitive readability proxy check"],
    exitGate: "Exit only when slide titles form a coherent learner-facing story, each slide body supports one claim or action, decorative load is reduced, and human learning outcomes are not claimed without separate human evidence."
  },
  {
    dir: "session-feedback-pattern-gate",
    title: "Session Feedback Pattern Gate Skill",
    skillId: "session-feedback-pattern-gate-skill",
    owner: "session-feedback-agent",
    trigger: "Use this skill when prior review comments reveal recurring weaknesses in title story, expression naturalness, decorative load, legal/regulated-domain AI boundaries, citation links, table/prose fit, or prompt structure.",
    inputs: ["storyline audit", "slide specs", "review comments", "reader situation", "evidence boundary"],
    outputs: ["session feedback pattern audit", "revision queue", "near-miss pattern notes", "blocked claim boundary"],
    tools: ["session feedback pattern check"],
    exitGate: "Exit only when recurring feedback patterns are turned into reusable checks instead of one-off copy edits."
  },
  {
    dir: "semantic-staging-design",
    title: "Semantic Staging Design Skill",
    skillId: "semantic-staging-design-skill",
    owner: "visualization-agent",
    trigger: "Use this skill when the artifact needs attention entry, curiosity, guided reading, spoken flow, evidence reveal, action exit, and explicit design freedom before visualization or PPTX build.",
    inputs: ["course flow map", "slide planning map", "symbol inventory", "outline notes", "storyline audit", "session feedback audit", "reader situation", "evidence boundary", "visual value spec"],
    outputs: ["semantic design system", "staging design brief", "scene beat", "attention entry", "curiosity gap", "reading path", "listening cue", "evidence reveal", "layout element calculations", "open expression options", "design freedom boundary"],
    tools: ["semantic design system check", "semantic staging design check"],
    exitGate: "Exit only when semantic-design-system.json is derived from course-flow-map.md, slide-planning-map.json, and symbol-inventory.json, layout elements record tradeoff, placement, front/back order, reading order, native object order, and overlap risk, and staging-design-brief.json makes scene beat, attention entry, curiosity gap, reading/listening path, evidence reveal, design-freedom boundary, open expression options, selected-expression rationale, and unnecessary constraints explicit before visualization or PPTX work."
  },
  {
    dir: "visualization-flow",
    title: "Visualization Flow Skill",
    skillId: "visualization-flow-skill",
    owner: "visualization-agent",
    trigger: "Use this skill when slides need image-first visual exploration, VLPP expression-distance monitoring, or open visual planning before PPTX implementation.",
    inputs: ["slide planning map", "symbol inventory", "semantic design system", "slide specs", "reader judgment", "staging design brief", "visual exploration candidates", "medium constraints", "target expression vector"],
    outputs: ["symbol inventory", "image-first visualization packet", "visual candidate contact sheet", "VLPP expression-distance monitor", "open visualization plan", "semantic variables", "layout element calculations", "chosen or intentionally unconstrained visual decisions", "staging-aware visual plan"],
    tools: ["symbol inventory check", "semantic design system check", "image-first visualization check", "VLPP expression-distance check", "semantic variable check", "visual cognition review"],
    exitGate: "Exit only when symbol-inventory.json exists before semantic-design-system.json, requested image-first surfaces exist, every important visual decision is named as a semantic variable before build, layout elements record tradeoff, placement, and front/back order, and VLPP results are stated as symbolic expression distance rather than learner psychology."
  },
  {
    dir: "pptx-native-build",
    title: "PPTX Native Build Skill",
    skillId: "pptx-native-build-skill",
    owner: "pptx-build-agent",
    trigger: "Use this skill when a new editable PowerPoint file must be generated through standard PresentationML/OPC-aware helpers or the compatible npm authoring flow instead of repairing an old recovered file.",
    inputs: ["outline notes", "slide planning map", "symbol inventory", "semantic design system", "staging design brief", "slide specs", "semantic variables", "layout element calculations", "visual value spec", "native PowerPoint feature requirements", "PresentationML constraints"],
    outputs: ["compatible npm state outputs when routed", "new PPTX", "native feature audit", "standard XML generation notes", "editable layouts, notes, tables, charts, hyperlinks, alt text, object names, reading order, and native object order"],
    tools: ["system init", "system run", "PPTX standard XML build", "project-specific PPTX build", "native PowerPoint package check"],
    exitGate: "Exit only when outline notes, slide-planning-map.json, symbol-inventory.json, semantic-design-system.json, and layout element calculations exist, compatible npm state/runbook/release-packet outputs exist when routed, a new PPTX exists, standard XML generation constraints were applied, and native PowerPoint feature checks pass structurally."
  },
  {
    dir: "drawingml-table-anchor-sanitizer",
    title: "DrawingML Table Anchor Sanitizer Skill",
    skillId: "drawingml-table-anchor-sanitizer-skill",
    owner: "pptx-build-agent",
    trigger: "Use this skill when DrawingML tables, anchors, or text body structure can cause PowerPoint recovery dialogs.",
    inputs: ["slide XML", "DrawingML table XML", "native feature audit"],
    outputs: ["sanitized table anchors", "invalid anchor count", "repair notes"],
    tools: ["PresentationML package check", "native feature audit"],
    exitGate: "Exit only when invalid table cell anchors and related DrawingML structure issues are zero or explicitly blocked."
  },
  {
    dir: "artifact-surface-separation",
    title: "Artifact Surface Separation Skill",
    skillId: "artifact-surface-separation-skill",
    owner: "artifact-surface-agent",
    trigger: "Use this skill before closeout when learner-facing artifacts, instructor/facilitator artifacts, production source, evidence tables, proof surfaces, and delivery packets could be collapsed into one status.",
    inputs: ["deck or document outputs", "source files", "evidence tables", "render proof", "native proof", "handoff target"],
    outputs: ["artifact surface map", "surface role audit", "missing surface queue", "closeout wording boundary"],
    tools: ["artifact surface separation check"],
    exitGate: "Exit only when each artifact surface has a role, evidence path, and closeout status without flattening source, proof, and learner-facing content."
  },
  {
    dir: "presentationml-compliance",
    title: "PresentationML Compliance Skill",
    skillId: "presentationml-compliance-skill",
    owner: "presentationml-compliance-agent",
    trigger: "Use this skill when ECMA-376, OPC, DrawingML, and MS-PPTX rules must be treated as normative.",
    inputs: ["PPTX package", "spec source bundle", "native feature audit", "relationship map"],
    outputs: ["PresentationML spec audit", "relationship integrity result", "schema coverage result"],
    tools: ["PresentationML spec check", "native package check"],
    exitGate: "Exit only when root relationships, content types, slide order, master/layout/theme/notes, and DrawingML checks are accounted for."
  },
  {
    dir: "repetition-release-gate",
    title: "Repetition Release Gate Skill",
    skillId: "repetition-release-gate-skill",
    owner: "repetition-gate-agent",
    trigger: "Use this skill when the same PowerPoint recovery or preview failure has repeated and must become a gate instead of another retry.",
    inputs: ["native audit", "spec audit", "recovered artifact evidence", "recent failure pattern"],
    outputs: ["repetition gate audit", "release blocker state", "next smallest action"],
    tools: ["recovery comparison check", "repetition gate check", "release check"],
    exitGate: "Exit only when structural pass, repeated-recovery comparison, accepted release status, and manual-open blocker state are reported separately."
  },
  {
    dir: "powerpoint-human-open-check",
    title: "PowerPoint Human Open Check Skill",
    skillId: "powerpoint-human-open-check-skill",
    owner: "powerpoint-open-check-agent",
    trigger: "Use this skill when release readiness depends on Microsoft PowerPoint opening the PPTX without a recovery dialog.",
    inputs: ["new PPTX", "manual or automation-backed PowerPoint open evidence", "latest PPTX build timestamp"],
    outputs: ["fresh open result", "recovery dialog state", "release unblock or blocker", "manual-open-checks/latest-powerpoint-open-check.json when the compatible npm route is used"],
    tools: ["manual Microsoft PowerPoint open check"],
    exitGate: "Exit only when a fresh open check newer than the PPTX build records no recovery dialog, or release remains blocked. If any command rebuilds the PPTX after the open check, repeat this gate."
  },
  {
    dir: "routing-experiment-gate",
    title: "Routing Experiment Gate Skill",
    skillId: "routing-experiment-gate-skill",
    owner: "representative-agent",
    trigger: "Use this skill when the reusable agent system changes and should-trigger, should-not-trigger, and near-miss behavior must be checked.",
    inputs: ["trigger contract", "skill descriptions", "recent feedback patterns", "near-miss examples"],
    outputs: ["routing experiment table", "should-trigger cases", "should-not-trigger cases", "expected behavior notes"],
    tools: ["routing experiment check"],
    exitGate: "Exit only when the routing contract includes positive, negative, and near-miss cases with expected behavior."
  }
];

function createArchitecture(projectName) {
  const name = projectName || "Document Slide Authoring";
  return {
    schema_version: "1.6-portable",
    system_id: SYSTEM_ID,
    goal: `Represent the ${name} cognitive document, visual, slide, and PowerPoint authoring workflow as a modular agent system whose skills and tools are verified against local evidence.`,
    claim_boundary: "The system may claim structural readiness when the agent-system audit passes. It may claim working-source readiness when source of truth, clarification, conflict, and fixed/flexible/decisional classification are explicit. It may claim cognitive authoring packet readiness when required reader-task, semantic-fit, unfolding, and visual-value fields are present. It may claim outline-note readiness when reader situation, purpose, section flow, slide sequence, visible message, spoken notes, evidence, visual intent, and open questions are explicit before PPTX work. It may claim cognitive readability proxy readiness when storyline, assertion-evidence, one-beat, scan, load, and session-feedback pattern checks pass. It may claim semantic-staging readiness when scene beat, attention entry, curiosity gap, reading path, listening cue, evidence reveal, semantic variables, accessibility/load, design-freedom boundary, open expression options, selected-expression rationale, and unnecessary-constraint removal are explicit before visualization or PPTX build. It may claim image-first visualization readiness when visual candidates or contact sheets are produced before build and their semantic roles are explicit. It may claim VLPP expression-distance readiness only as observed computation over symbolic expression vectors, not learner psychology. It may claim artifact handoff readiness only when learner-facing, instructor/facilitator, production source, evidence/fact table, render/native proof, and delivery/handoff surfaces are separated. It may claim compatible npm authoring readiness only when system state, runbook, release packet, new PPTX, PresentationML/native/repetition checks, and manual-open-checks/latest-powerpoint-open-check.json are present with result=no_recovery_dialog and the open check is newer than the PPTX build. It may claim release readiness only after project-specific native checks pass and a fresh Microsoft PowerPoint open check records no recovery dialog. Any rebuild after the open check invalidates that release claim. It may claim human comprehension, retention, or transfer only after separate human outcome evidence.",
    runtime_compatibility: {
      status: "shared-core only / no-delta",
      reason: "The agent system is encoded as local JSON, Markdown, and deterministic Node.js checks. It does not require a separate agent runtime."
    },
    adaptation_contract: {
      target_project_root: ".",
      customize: [
        "project-specific manual names",
        "project-specific prompt names",
        "project-specific PPTX builder",
        "project-specific PresentationML research bundle",
        "project-specific authoring packet evidence paths",
        "project-specific outline note content and evidence paths",
        "project-specific artifact surface paths",
        "project-specific session feedback examples",
        "project-specific staging examples and visual expression candidates",
        "project-specific image-first visual candidates, contact sheets, and VLPP expression vectors",
        "project-specific compatible npm authoring workspace, work id, title, and command aliases",
        "project-specific release evidence"
      ],
      keep_global: [
        "agent IDs",
        "skill IDs",
        "workflow order",
        "working source clarification fields",
        "three-layer classification fields",
        "cognitive authoring packet field requirements",
        "outline note field requirements before PPTX build",
        "session feedback pattern checks",
    "semantic-staging field requirements and design-freedom boundary",
    "image-first visualization and VLPP expression-distance claim boundaries",
    "workflow stage order and stage-order checks",
    "artifact surface separation requirements",
        "structural versus release readiness boundary",
        "manual PowerPoint open-check gate",
        "compatible npm process order when that route is available",
        "fresh open check newer than generated PPTX build",
        "rebuild invalidates the manual PowerPoint open check"
      ]
    },
    compatible_npm_authoring_process: {
      default_workspace: COMPATIBLE_NPM_WORKSPACE,
      init_command: "npm run system:init -- <work-id> --title \"<slide title>\"",
      run_command: "npm run system:run -- <work-id>",
      state_outputs: COMPATIBLE_NPM_STATE_OUTPUTS,
      build_command: "npm run build",
      build_output: COMPATIBLE_NPM_BUILD_OUTPUT,
      verification_commands: [
        "npm run verify:presentationml-spec",
        "npm run research:build",
        "npm run verify:research",
        "npm run verify:powerpoint"
      ],
      recovery_commands: [
        "npm run compare:recovery",
        "npm run verify:repetition-gate"
      ],
      manual_open_check: {
        path: COMPATIBLE_NPM_MANUAL_OPEN_CHECK,
        required_result: "no_recovery_dialog",
        freshness_rule: "The recorded manual open check must be newer than the PPTX build it validates."
      },
      release_commands: [
        "npm run verify:release",
        "npm run agent-system:check"
      ],
      accepted_release_statuses: COMPATIBLE_NPM_ACCEPTED_RELEASE_STATUSES,
      rebuild_warning: "npm test internally runs npm run build. After a fresh PowerPoint open check, do not run npm test again unless the PPTX is rebuilt and the PowerPoint open check is repeated."
    },
    working_source_contract: {
      source_distillation: "distilled from repeated deck-production feedback into a reusable intake contract; no project content is copied into the global skill",
      required_fields: REQUIRED_CLARIFICATION_FIELDS,
      clarification_rule: "Lock the current source of truth, success condition, runtime target, provider provenance, and output brand before authoring. Mark missing facts as TODO, question, or blocked instead of filling them with generic assumptions."
    },
    conflict_resolution: {
      priority_order: [
        "user's latest explicit requirement",
        "project AGENTS.md and workspace SoT",
        "target artifact role and audience",
        "source evidence and license boundary",
        "native tool/release constraints",
        "general style preferences"
      ],
      rule: "When two requirements conflict, keep the higher-priority constraint and record the lower-priority item as deferred, blocked, or target-specific."
    },
    three_layer_contract: {
      required_fields: REQUIRED_THREE_LAYER_FIELDS,
      fixed: ["workflow order", "course-flow to slide-planning to symbol-inventory to design-system dependency", "release gates", "artifact surface roles", "evidence boundary labels", "runtime compatibility status"],
      flexible: ["wording", "examples", "visual tone", "layout expression", "project-specific filenames"],
      decisional: ["audience action", "claim strength", "evidence sufficiency", "surface inclusion or exclusion", "manual release status"],
      drift_rule: "A flexible adaptation cannot change fixed workflow gates or decisional claim boundaries without an explicit version bump and routing experiment."
    },
    intentional_implementation_contract: {
      required_fields: REQUIRED_INTENTIONAL_IMPLEMENTATION_FIELDS,
      calculated_value_required_fields: REQUIRED_CALCULATED_VALUE_FIELDS,
      fixed_rule: "Workflow order, release gates, evidence labels, artifact-surface roles, and stage-order checks must be explicitly fixed before implementation.",
      flexible_rule: "Wording, examples, visual tone, layout expression, image style, and project-specific filenames may vary only inside the fixed gates and recorded constraints.",
      decisional_rule: "Audience action, candidate selection, claim strength, evidence sufficiency, and override decisions must be recorded with rationale.",
      implementation_rule: "Every important implementation value must be traceable to semantic role, reader situation, medium constraint, safe area, readable size, density, scan path, or action exit."
    },
    course_flow_to_design_system_contract: {
      sequence_lock: [
        "course-flow-map",
        "slide-planning-map",
        "symbol-inventory",
        "semantic-design-system"
      ],
      rule: "Do not start by fixing style, template, palette, motif, or design system. First map the whole lecture flow, then plan slides by learning situation and learner action, then collect symbols that carry the planned meaning, then create the design system from those symbols and constraints.",
      required_files: {
        course_flow_map: "course-flow-map.md",
        slide_planning_map: "slide-planning-map.json",
        symbol_inventory: "symbol-inventory.json",
        semantic_design_system: "semantic-design-system.json"
      },
      course_flow_required_fields: REQUIRED_COURSE_FLOW_FIELDS,
      slide_planning_required_fields: REQUIRED_SLIDE_PLANNING_FIELDS,
      symbol_inventory_required_fields: REQUIRED_SYMBOL_INVENTORY_FIELDS,
      semantic_design_system_required_fields: REQUIRED_SEMANTIC_DESIGN_SYSTEM_FIELDS,
      layout_element_calculation_required_fields: REQUIRED_LAYOUT_ELEMENT_CALCULATION_FIELDS,
      design_start_boundary: "A design system may only be selected or generated after course-flow-map.md, slide-planning-map.json, and symbol-inventory.json exist as production sources or are explicitly marked blocked with reasons.",
      learner_facing_boundary: "Internal file paths, generation process notes, review comments, and provider provenance stay out of learner-facing slides unless they are being taught as course content."
    },
    cognitive_authoring_packet: {
      process_lock: "cognitive-document-visual-authoring-v1",
      source_distillation: "distilled from project-local cognitive-document-visual-authoring into reusable packet fields and checks; no runtime dependency on the source project",
      required_fields: REQUIRED_AUTHORING_PACKET_FIELDS,
      visual_value_required_fields: REQUIRED_VISUAL_VALUE_FIELDS,
      readability_fit_required_fields: REQUIRED_READABILITY_FIT_FIELDS,
      stage_gates: [
        "R. Research / Evidence Freeze",
        "P. Person / Problem Model",
        "M. Message / Mental Model",
        "W. Writing / Visual Realization",
        "A. Audit / Artifact Release"
      ]
    },
    outline_note_contract: {
      required_fields: REQUIRED_OUTLINE_NOTE_FIELDS,
      rule: "Before storyline review, visualization, or PPTX build, write outline notes that connect the reader situation, deck or document purpose, section flow, slide sequence, title story draft, visible message, spoken or facilitation notes, evidence links, visual intent, and open questions."
    },
    session_feedback_pattern_gate: {
      source_distillation: "distilled from repeated slide-review comments into reusable checks; comments remain local evidence, not global deck content",
      required_checks: REQUIRED_SESSION_FEEDBACK_CHECKS,
      rule: "Recurring review feedback must become a named check before another rewrite. The gate checks story, expression, visual load, legal/regulated use boundaries, citation links, table/prose fit, and prompt knowledge structure."
    },
    semantic_staging_design_framework: {
      required_fields: REQUIRED_STAGING_DESIGN_FIELDS,
      rule: "Before visualization or PPTX build, decide the scene beat, attention entry, curiosity gap, reading path, listening cue, evidence reveal, semantic variables, accessibility/load, design-freedom boundary, open expression options, selected-expression rationale, and avoid-unnecessary-constraints list.",
      freedom_boundary: "No predefined style kit, layout family, motif, fixed image-generation method, animation plan, palette, icon style, or recurring visual language is mandatory. The framework fixes the cognitive job and evidence boundary; the expression remains open unless a target project supplies a real medium, accessibility, brand, or native-PPTX constraint."
    },
    image_first_visualization_framework: {
      required_fields: REQUIRED_IMAGE_FIRST_VISUALIZATION_FIELDS,
      rule: "When visual direction is unsettled or explicitly requested before HTML/PPTX, produce visual candidates or a contact sheet before implementation and record the semantic role, calculated values, selected-candidate rationale, and intentionally unconstrained areas.",
      vlpp_boundary: "VLPP monitoring observes computed distance between target symbolic expression and candidate rendered expression. It must not infer learner psychology, comprehension, persuasion, retention, or behavior change.",
      evidence_state_required: "observed_computation"
    },
    artifact_surface_separation: {
      required_surfaces: REQUIRED_ARTIFACT_SURFACES,
      rule: "Do not collapse learner-facing content, instructor/facilitator notes, production source, evidence tables, render/native proof, and handoff package into one 'slides done' status."
    },
    routing_experiments: {
      required_fields: REQUIRED_ROUTING_EXPERIMENT_FIELDS,
      should_trigger: [
        "Create or improve a reusable document/slide/PPTX authoring agent system.",
        "Separate student deck, instructor handoff, evidence table, source files, and native PPTX proof.",
        "Turn repeated slide review comments into reusable checks.",
        "Remove premature method or style assumptions and keep slide design expression open before visualization or PPTX work.",
        "Include a compatible npm authoring flow with system:init, system:run, build, PresentationML/native checks, recovery comparison, manual PowerPoint open check, release check, and agent-system check."
      ],
      should_not_trigger: [
        "Rewrite one sentence naturally.",
        "Recommend only Canva colors or a single template style.",
        "Export a simple image-only slide with no reusable workflow."
      ],
      expected_behavior: "Trigger for reusable authoring-system work and near-miss prevention; stay out of one-off copy edits or unrelated design advice."
    },
    code_llm_boundary: {
      deterministic_code_owns: [
        "required IDs",
        "file existence",
        "module headings",
        "workflow order",
        "audit JSON creation",
        "presence of working-source clarification fields",
        "presence of conflict-resolution and three-layer classification contracts",
        "presence and order of course-flow-map, slide-planning-map, symbol-inventory, and semantic-design-system before visual design or PPTX build",
        "presence of required cognitive authoring packet fields",
        "presence of semantic_fit, unfolding_trace, visual_value_spec, and readability-fit rationale fields",
        "presence of outline notes before storyline, visualization, and PPTX build",
        "presence of storyline/readability gate artifacts",
        "presence of session-feedback pattern checks",
        "presence of semantic-staging design fields before visualization or PPTX build",
        "presence of design-freedom boundary so predefined style kits, templates, images, motifs, palettes, and animations remain optional unless real target constraints require them",
        "presence of layout element calculation fields for element tradeoff, placement, front-back order, reading order, native object order, and overlap risk",
        "presence and order of image-first visualization before open visualization planning and PPTX build",
        "presence of VLPP expression-distance claim boundary when a target-expression vector is used",
        "presence of artifact-surface roles",
        "presence of compatible npm authoring process order, state outputs, build output, manual open-check path, accepted release statuses, and rebuild warning",
        "presence of routing experiment fields"
      ],
      llm_judgment_owns: [
        "audience-specific wording",
        "reader situation and cognitive task judgment",
        "semantic fit judgment",
        "CTA probe quality and unfolding interpretation",
        "narrative emphasis",
        "title-only story coherence",
        "assertion-evidence fit",
        "cognitive load proxy interpretation",
        "outline note concreteness for the target audience and session",
        "session feedback pattern interpretation",
        "whole-course flow quality and whether the module/session sequence fits the target learners",
        "slide-planning quality by visual situation, cognitive operation, learner action, and output artifact",
        "symbol selection quality and semantic design-system rationale",
        "element tradeoff interpretation: whether attention cost and space cost are worth the semantic gain",
        "semantic-staging choices such as scene beat, attention entry, curiosity gap, reading path, listening cue, evidence reveal, open expression options, selected-expression rationale, and unnecessary-constraint removal",
        "image-first candidate interpretation and selected-candidate rationale",
        "target-expression dimension rationale and whether a non-distance constraint should override distance ranking",
        "artifact surface fit by project situation",
        "visual semantics and visual value choices",
        "blocked evidence interpretation",
        "whether the compatible npm route is actually available in the target project and which work id/title should be used"
      ]
    },
    working_source_of_truth: [
      "cognitive-authoring-packet.json",
      "outline-notes.md",
      "cognitive-document-visual-authoring-process.md",
      "working-source-clarification-packet.json",
      "course-flow-map.md",
      "document-slide-authoring-manual.md",
      "flexible-judgment-action-prompts.md",
      "integrated-authoring-pipeline.md",
      "slide-planning-map.json",
      "symbol-inventory.json",
      "semantic-design-system.json",
      "session-feedback-pattern-audit.json",
      "staging-design-brief.json",
      "artifact-surface-map.json",
      "routing-experiment-table.md",
      "presentationml-compliance-process.md",
      "repeated-issue-playbook.md",
      "09-system-state.json",
      "10-system-runbook.md",
      "11-release-packet.md",
      "manual-open-checks/latest-powerpoint-open-check.json",
      "authoring_tools.js",
      "research_pipeline.js",
      "pptxgenjs_helpers/",
      "build_authoring_system_deck.js",
      "verify_native_pptx.js",
      "verify_presentationml_spec.js",
      "verify_repetition_gate.js"
    ],
    agents: [
      {
        id: "representative-agent",
        label: "Document Slide Authoring Representative",
        role: "Own the visible goal, rubric, routing, and closeout boundary for the whole authoring workflow.",
        owns: ["system_goal", "rubric", "agent_skill_routing", "release_claim_boundary"],
        uses_skills: [
          "evidence-freeze-skill",
          "working-source-clarification-skill",
          "cognitive-document-visual-authoring-skill",
          "writing-flow-skill",
          "storyline-readability-gate-skill",
          "session-feedback-pattern-gate-skill",
          "semantic-staging-design-skill",
          "visualization-flow-skill",
          "presentationml-compliance-skill",
          "pptx-native-build-skill",
          "artifact-surface-separation-skill",
          "repetition-release-gate-skill",
          "powerpoint-human-open-check-skill",
          "routing-experiment-gate-skill"
        ],
        outputs: ["authoring-agent-system-audit.json", "repetition-gate-audit.json"],
        handoff_to: [
          "evidence-intake-agent",
          "cognitive-authoring-agent",
          "writing-agent",
          "storyline-readability-agent",
          "session-feedback-agent",
          "visualization-agent",
          "pptx-build-agent",
          "artifact-surface-agent",
          "presentationml-compliance-agent",
          "repetition-gate-agent",
          "powerpoint-open-check-agent"
        ]
      },
      {
        id: "evidence-intake-agent",
        label: "Evidence Intake Agent",
        role: "Freeze source inventory, research bundle, particle outputs, Ziphyun handoff, and uncertainty boundaries before authoring decisions.",
        owns: ["source_inventory", "raw_archive_freeze", "canonical_corpus", "particleization", "ziphyun_handoff", "working_source_clarification"],
        uses_skills: ["evidence-freeze-skill", "working-source-clarification-skill", "ziphyun-particle-research-skill"],
        outputs: ["research/presentationml/reports/research-pipeline-audit.json"],
        handoff_to: ["cognitive-authoring-agent", "presentationml-compliance-agent"]
      },
      {
        id: "cognitive-authoring-agent",
        label: "Cognitive Authoring Agent",
        role: "Convert evidence and reader context into a cognitive authoring packet before writing, storyline, visualization, or PPTX implementation.",
        owns: [
          "reader_situation",
          "cognitive_task",
          "desired_action",
          "semantic_fit",
          "evidence_boundary",
          "folded_unit",
          "weakness_diagnosis",
          "cta_interview_log",
          "unfolding_trace",
          "knowledge_split",
          "visual_rationale",
          "visual_value_spec",
          "stage_gate_log"
        ],
        uses_skills: ["cognitive-document-visual-authoring-skill"],
        outputs: ["cognitive-authoring-packet.json"],
        handoff_to: ["writing-agent", "storyline-readability-agent", "visualization-agent"]
      },
      {
        id: "writing-agent",
        label: "Writing Agent",
        role: "Convert the cognitive authoring packet and evidence into brief, seed, outline, outline notes, section flow, draft slide titles, reader judgment, and slide-level visible/spoken message split.",
        owns: ["brief", "seed", "mcii", "outline", "outline_notes", "draft_slide_titles", "slide_spec", "visible_spoken_message_split"],
        uses_skills: ["writing-flow-skill"],
        outputs: ["outline-notes.md", "manual-tools-audit.json", "prompt-tools-audit.json", "pipeline-tools-audit.json"],
        handoff_to: ["storyline-readability-agent"]
      },
      {
        id: "storyline-readability-agent",
        label: "Storyline Readability Agent",
        role: "Evaluate the outline notes, packet-derived title sequence, title-only story flow, assertion-evidence fit, one-beat discipline, 5-second scan proxy, cognitive-load risk, and evidence boundary before visual production.",
        owns: [
          "outline_note_review",
          "title_only_storyline",
          "assertion_evidence_map",
          "one_beat_review",
          "five_second_scan_proxy",
          "cognitive_load_proxy",
          "human_outcome_claim_boundary"
        ],
        uses_skills: ["storyline-readability-gate-skill"],
        outputs: ["storyline-readability-audit.json"],
        handoff_to: ["session-feedback-agent", "visualization-agent", "writing-agent"]
      },
      {
        id: "session-feedback-agent",
        label: "Session Feedback Pattern Agent",
        role: "Convert recurring review comments into reusable gates for title story, natural expression, decorative load, legal/regulated AI boundaries, citation links, table/prose fit, and prompt knowledge structure.",
        owns: [
          "session_feedback_pattern_audit",
          "review_comment_taxonomy",
          "near_miss_feedback_cases",
          "revision_queue"
        ],
        uses_skills: ["session-feedback-pattern-gate-skill"],
        outputs: ["session-feedback-pattern-audit.json"],
        handoff_to: ["visualization-agent", "writing-agent"]
      },
      {
        id: "visualization-agent",
        label: "Visualization Agent",
        role: "Run semantic-staging design after storyline/readability and session-feedback checks, generate image-first visual candidates when needed, monitor VLPP expression distance as computed symbolic distance, then keep visual expression open while turning the staging brief into explicit semantic variables for PPTX implementation.",
        owns: ["staging_design_brief", "scene_beat", "attention_entry", "curiosity_gap", "reading_path", "listening_cue", "evidence_reveal", "design_freedom_boundary", "open_expression_options", "selected_expression_rationale", "avoid_unnecessary_constraints", "image_first_visualization_packet", "visual_candidate_contact_sheet", "target_expression_vector", "candidate_expression_vectors", "vlpp_expression_distance_monitor", "visual_exploration_candidates", "semantic_variables", "visual_value_spec", "readability_fit", "visual_cognition_words", "native_visualization_intent"],
        uses_skills: ["semantic-staging-design-skill", "visualization-flow-skill"],
        outputs: ["staging-design-brief.json", "image-first-visualization-packet.json", "visual-candidate-contact-sheet.png", "vlpp-expression-distance-monitor.json", "semantic-variables.json"],
        handoff_to: ["pptx-build-agent"]
      },
      {
        id: "pptx-build-agent",
        label: "PPTX Native Build Agent",
        role: "Create a new editable PowerPoint package from outline notes and slide specs through the compatible npm system run when available, PresentationML/OPC-aware standard XML generation, native layout, theme, notes, tables, charts, alt text, read order, and audit slide surfaces.",
        owns: ["compatible_npm_system_state", "new_pptx_generation", "standard_xml_generation", "native_powerpoint_features", "drawingml_sanitization", "editable_object_surface"],
        uses_skills: ["pptx-native-build-skill", "drawingml-table-anchor-sanitizer-skill"],
        outputs: ["09-system-state.json", "10-system-runbook.md", "11-release-packet.md", "Document_Slide_Authoring_System_new.pptx", "native-feature-audit.json"],
        handoff_to: ["presentationml-compliance-agent", "artifact-surface-agent", "repetition-gate-agent"]
      },
      {
        id: "presentationml-compliance-agent",
        label: "PresentationML Compliance Agent",
        role: "Treat ECMA-376, OPC, DrawingML, and MS-PPTX as the normative basis for package structure and PowerPoint workflow validation.",
        owns: ["presentationml_source_bundle", "opc_relationship_integrity", "drawingml_anchor_rules", "schema_coverage"],
        uses_skills: ["presentationml-compliance-skill"],
        outputs: ["spec_sources/presentationml/reports/presentationml-spec-audit.json", "native-feature-audit.json"],
        handoff_to: ["artifact-surface-agent", "repetition-gate-agent"]
      },
      {
        id: "artifact-surface-agent",
        label: "Artifact Surface Separation Agent",
        role: "Separate learner-facing artifacts, instructor/facilitator artifacts, production source, evidence tables, render/native proof, and delivery handoff before closeout.",
        owns: [
          "learner_facing_surface",
          "instructor_facilitator_surface",
          "production_source_surface",
          "evidence_fact_table_surface",
          "render_native_proof_surface",
          "delivery_handoff_surface"
        ],
        uses_skills: ["artifact-surface-separation-skill"],
        outputs: ["artifact-surface-map.json"],
        handoff_to: ["repetition-gate-agent", "representative-agent"]
      },
      {
        id: "repetition-gate-agent",
        label: "Repeated Issue Gate Agent",
        role: "Stop repeated PowerPoint recovery work from becoming another manual retry by recording a pattern, comparing recovery artifacts, and separating structural pass from release pass.",
        owns: ["repeated_issue_pattern", "release_gate", "recovery_artifact_scan", "recovery_comparison", "accepted_release_status", "next_action_boundary"],
        uses_skills: ["repetition-release-gate-skill"],
        outputs: ["repetition-gate-audit.json"],
        handoff_to: ["powerpoint-open-check-agent", "representative-agent"]
      },
      {
        id: "powerpoint-open-check-agent",
        label: "PowerPoint Open Check Agent",
        role: "Own the manual Microsoft PowerPoint open evidence that cannot be inferred from PNG, PDF, QuickLook, or ZIP validation.",
        owns: ["fresh_powerpoint_open_check", "no_recovery_dialog_evidence", "manual_open_check_json", "open_check_freshness_against_build", "manual_release_unblock"],
        uses_skills: ["powerpoint-human-open-check-skill"],
        outputs: ["manual_powerpoint_open_check", "manual-open-checks/latest-powerpoint-open-check.json"],
        handoff_to: ["representative-agent"]
      }
    ],
    skills: REQUIRED_SKILLS.map((skill) => ({
      id: skill.id,
      path: skill.path,
      type: skill.id === "ziphyun-particle-research-skill"
        ? "deterministic-preprocess"
        : (skill.id === "cognitive-document-visual-authoring-skill"
          ? "semantic-authoring-gate"
          : (skill.id === "semantic-staging-design-skill" ? "semantic-staging-gate" : "reusable-workflow")),
      tools: toolsForSkill(skill.id)
    })),
    tools: [
      { id: "manual-check", command: "npm run verify:manual", evidence: ["manual-tools-audit.json"] },
      { id: "prompt-check", command: "npm run verify:prompts", evidence: ["prompt-tools-audit.json"] },
      { id: "pipeline-check", command: "npm run verify:pipeline", evidence: ["pipeline-tools-audit.json"] },
      { id: "tools-check", command: "npm run tools:check", evidence: [] },
      {
        id: "system-init",
        command: "npm run system:init -- <work-id> --title \"<slide title>\"",
        evidence: ["work directory initialized for the compatible npm authoring route"]
      },
      {
        id: "system-run",
        command: "npm run system:run -- <work-id>",
        evidence: COMPATIBLE_NPM_STATE_OUTPUTS
      },
      {
        id: "research-build",
        command: "npm run research:build",
        evidence: [
          "research/presentationml/corpus/presentationml-research-corpus.md",
          "research/presentationml/particle/presentationml-research-particles.v1.json",
          "research/presentationml/ziphyun-handoff.md"
        ]
      },
      { id: "research-check", command: "npm run verify:research", evidence: ["research/presentationml/reports/research-pipeline-audit.json"] },
      {
        id: "working-source-clarification-check",
        command: "project-specific: verify working source, clarification packet, conflict priority, and fixed/flexible/decisional classification",
        evidence: ["working-source-clarification-packet.json"]
      },
      {
        id: "course-flow-map-check",
        command: "project-specific: verify course-flow-map.md fixes the whole lecture flow, fixed schedule, module sequence, session timing, learning arc, output chain, and non-goals before slide planning",
        evidence: ["course-flow-map.md"]
      },
      {
        id: "cognitive-authoring-packet-check",
        command: "project-specific: verify cognitive-authoring-packet.json contains required semantic-fit, unfolding, knowledge-split, visual-value, and readability-fit rationale fields",
        evidence: ["cognitive-authoring-packet.json"]
      },
      {
        id: "outline-note-check",
        command: "project-specific: verify outline-notes.md contains reader situation, purpose, section flow, slide sequence, visible/spoken message split, evidence links, visual intent, and open questions before PPTX work",
        evidence: ["outline-notes.md"]
      },
      {
        id: "slide-planning-map-check",
        command: "project-specific: verify slide-planning-map.json plans slides by source module, slide goal, visual situation, cognitive operation, learner action, output artifact, timing budget, evidence boundary, and reuse policy before symbol collection",
        evidence: ["slide-planning-map.json"]
      },
      {
        id: "storyline-readability-check",
        command: "project-specific: run title-only story, assertion-evidence, one-beat, 5-second scan, cognitive-load, and evidence-boundary checks",
        evidence: ["storyline-readability-audit.json"]
      },
      {
        id: "session-feedback-pattern-check",
        command: "project-specific: verify recurring review feedback patterns are covered before visual production",
        evidence: ["session-feedback-pattern-audit.json"]
      },
      {
        id: "symbol-inventory-check",
        command: "project-specific: verify symbol-inventory.json maps symbols to semantic role, source context, target expression vector, possible confusion, visual candidates, selection reason, and learner-facing boundary before design-system work",
        evidence: ["symbol-inventory.json"]
      },
      {
        id: "semantic-design-system-check",
        command: "project-specific: verify semantic-design-system.json is derived from course flow, slide planning, symbol inventory, medium/accessibility constraints, and calculated values rather than a predefined style kit",
        evidence: ["semantic-design-system.json"]
      },
      {
        id: "semantic-staging-design-check",
        command: "project-specific: verify staging-design-brief.json contains required semantic-staging fields and preserves design freedom by keeping predefined style kits, templates, images, motifs, palettes, animation plans, and recurring visual language optional unless target constraints require them",
        evidence: ["staging-design-brief.json"]
      },
      {
        id: "image-first-visualization-check",
        command: "project-specific: verify image-first visual candidates or contact sheet exist before HTML/PPTX implementation when visual direction is unsettled or requested",
        evidence: ["image-first-visualization-packet.json", "visual-candidate-contact-sheet.png"]
      },
      {
        id: "vlpp-expression-distance-check",
        command: "project-specific: verify target expression vector, candidate expression vectors, distance metric, distance-to-target, evidence_state=observed_computation, and non-psychological claim boundary",
        evidence: ["vlpp-expression-distance-monitor.json"]
      },
      {
        id: "artifact-surface-separation-check",
        command: "project-specific: verify learner-facing, instructor/facilitator, production source, evidence/fact table, render/native proof, and delivery/handoff surfaces are separated",
        evidence: ["artifact-surface-map.json"]
      },
      {
        id: "pptx-standard-xml-build",
        command: "project-specific: build a new PPTX with PresentationML/OPC-aware helpers such as pptxgenjs_helpers and project-specific XML sanitizers",
        evidence: ["Document_Slide_Authoring_System_new.pptx", "native-feature-audit.json"]
      },
      { id: "pptx-build", command: "npm run build", evidence: ["Document_Slide_Authoring_System_new.pptx"] },
      { id: "presentationml-spec-check", command: "npm run verify:presentationml-spec", evidence: ["spec_sources/presentationml/reports/presentationml-spec-audit.json"] },
      { id: "native-powerpoint-check", command: "npm run verify:powerpoint", evidence: ["native-feature-audit.json"] },
      { id: "recovery-compare-check", command: "npm run compare:recovery", evidence: ["recovery comparison result or explicit no-recovery-artifact note"] },
      { id: "repetition-gate-check", command: "npm run verify:repetition-gate", evidence: ["repetition-gate-audit.json"] },
      {
        id: "release-check",
        command: "npm run verify:release",
        evidence: ["repetition-gate-audit.json"],
        pass_when: "release_status is pass or pass_superseded_old_recovery_artifacts",
        expected_failure_when: "release_status is blocked_powerpoint_recovery_evidence or manual PowerPoint evidence is missing"
      },
      { id: "agent-system-check", command: "node authoring_agent_system.js", evidence: ["authoring-agent-system-audit.json"] },
      {
        id: "manual-powerpoint-open-check",
        command: "manual: open the generated PPTX in Microsoft PowerPoint and record whether a recovery dialog appears",
        evidence: ["manual_powerpoint_open_check", COMPATIBLE_NPM_MANUAL_OPEN_CHECK],
        manual: true
      },
      {
        id: "routing-experiment-check",
        command: "project-specific: verify should-trigger, should-not-trigger, expected behavior, and near-miss routing examples",
        evidence: ["routing-experiment-table.md"]
      }
    ],
    workflow: [
      {
        order: 1,
        stage: "evidence-freeze",
        agent: "evidence-intake-agent",
        primary_skill: "evidence-freeze-skill",
        exit_condition: "Research audit passes and uncertainty boundaries are explicit.",
        required_evidence: ["research/presentationml/reports/research-pipeline-audit.json"]
      },
      {
        order: 2,
        stage: "working-source-clarification",
        agent: "evidence-intake-agent",
        primary_skill: "working-source-clarification-skill",
        exit_condition: "Working source, clarification packet, conflict priority, and fixed/flexible/decisional classification are explicit.",
        required_evidence: ["working-source-clarification-packet.json"]
      },
      {
        order: 3,
        stage: "course-flow-map",
        agent: "writing-agent",
        primary_skill: "writing-flow-skill",
        exit_condition: "Whole lecture flow, fixed schedule, module sequence, session timing, learning arc, output chain, and non-goals are explicit before slide planning.",
        required_evidence: ["course-flow-map.md"]
      },
      {
        order: 4,
        stage: "cognitive-authoring-packet",
        agent: "cognitive-authoring-agent",
        primary_skill: "cognitive-document-visual-authoring-skill",
        exit_condition: "Reader situation, cognitive task, desired action, semantic fit, unfolding trace, knowledge split, and visual value spec are explicit.",
        required_evidence: ["cognitive-authoring-packet.json"]
      },
      {
        order: 5,
        stage: "writing-flow",
        agent: "writing-agent",
        primary_skill: "writing-flow-skill",
        exit_condition: "Manual, prompt, pipeline, and outline note checks pass.",
        required_evidence: ["course-flow-map.md", "manual-tools-audit.json", "prompt-tools-audit.json", "pipeline-tools-audit.json", "outline-notes.md"]
      },
      {
        order: 6,
        stage: "outline-note-gate",
        agent: "writing-agent",
        primary_skill: "writing-flow-skill",
        exit_condition: "Outline notes make reader situation, purpose, section flow, slide sequence, visible message, spoken notes, evidence links, visual intent, and open questions explicit before PPTX work.",
        required_evidence: ["outline-notes.md"]
      },
      {
        order: 7,
        stage: "slide-planning-map",
        agent: "writing-agent",
        primary_skill: "writing-flow-skill",
        exit_condition: "Each slide is planned by situation, cognitive operation, learner action, output artifact, timing budget, evidence boundary, and reuse policy before symbol collection.",
        required_evidence: ["slide-planning-map.json"]
      },
      {
        order: 8,
        stage: "storyline-readability-gate",
        agent: "storyline-readability-agent",
        primary_skill: "storyline-readability-gate-skill",
        exit_condition: "Title-only story, assertion-evidence fit, one-beat discipline, 5-second scan proxy, cognitive-load risk, and evidence boundary are explicit.",
        required_evidence: ["storyline-readability-audit.json"]
      },
      {
        order: 9,
        stage: "session-feedback-pattern-gate",
        agent: "session-feedback-agent",
        primary_skill: "session-feedback-pattern-gate-skill",
        exit_condition: "Recurring review feedback patterns are checked before visual production continues.",
        required_evidence: ["session-feedback-pattern-audit.json"]
      },
      {
        order: 10,
        stage: "symbol-inventory",
        agent: "visualization-agent",
        primary_skill: "visualization-flow-skill",
        exit_condition: "Symbols, semantic roles, source context, target expression vectors, possible confusion, visual candidates, selection reasons, and learner-facing boundaries are explicit before design-system work.",
        required_evidence: ["symbol-inventory.json"]
      },
      {
        order: 11,
        stage: "semantic-design-system",
        agent: "visualization-agent",
        primary_skill: "semantic-staging-design-skill",
        exit_condition: "Design principles, symbol mapping, layout families, typography rules, color logic, image style rules, PPTX element use, accessibility/density, calculated values, and implementation trace are derived from course flow, slide planning, and symbol inventory.",
        required_evidence: ["course-flow-map.md", "slide-planning-map.json", "symbol-inventory.json", "semantic-design-system.json"]
      },
      {
        order: 12,
        stage: "semantic-staging-design-gate",
        agent: "visualization-agent",
        primary_skill: "semantic-staging-design-skill",
        exit_condition: "Scene beat, attention entry, curiosity gap, reading path, listening cue, evidence reveal, design-freedom boundary, open expression options, selected-expression rationale, and unnecessary-constraint removal are explicit before visualization or PPTX build.",
        required_evidence: ["semantic-design-system.json", "staging-design-brief.json"]
      },
      {
        order: 13,
        stage: "image-first-visualization-gate",
        agent: "visualization-agent",
        primary_skill: "visualization-flow-skill",
        exit_condition: "Requested or unsettled visual direction has image-first candidates or a contact sheet, and VLPP monitoring is bounded to symbolic expression distance rather than learner psychology.",
        required_evidence: ["semantic-design-system.json", "image-first-visualization-packet.json", "visual-candidate-contact-sheet.png", "vlpp-expression-distance-monitor.json"]
      },
      {
        order: 14,
        stage: "open-visualization-planning",
        agent: "visualization-agent",
        primary_skill: "visualization-flow-skill",
        exit_condition: "Semantic variables, selected or intentionally unconstrained visual decisions, and real medium/accessibility constraints are explicit before PPTX build.",
        required_evidence: ["semantic-design-system.json", "staging-design-brief.json", "image-first-visualization-packet.json", "semantic-variables.json"]
      },
      {
        order: 15,
        stage: "new-pptx-native-build",
        agent: "pptx-build-agent",
        primary_skill: "pptx-native-build-skill",
        exit_condition: "Outline notes exist, compatible npm state/runbook/release-packet outputs exist when this route is used, a new PPTX exists, and native PowerPoint audit passes.",
        required_evidence: ["outline-notes.md", "slide-planning-map.json", "symbol-inventory.json", "semantic-design-system.json", "staging-design-brief.json", "image-first-visualization-packet.json", "09-system-state.json", "10-system-runbook.md", "11-release-packet.md", "Document_Slide_Authoring_System_new.pptx", "native-feature-audit.json"]
      },
      {
        order: 16,
        stage: "presentationml-compliance",
        agent: "presentationml-compliance-agent",
        primary_skill: "presentationml-compliance-skill",
        exit_condition: "Local ECMA-376, OPC, DrawingML, and MS-PPTX coverage audit passes.",
        required_evidence: ["spec_sources/presentationml/reports/presentationml-spec-audit.json"]
      },
      {
        order: 17,
        stage: "artifact-surface-separation",
        agent: "artifact-surface-agent",
        primary_skill: "artifact-surface-separation-skill",
        exit_condition: "Learner-facing, instructor/facilitator, production source, evidence/fact table, render/native proof, and handoff surfaces are separated.",
        required_evidence: ["artifact-surface-map.json"]
      },
      {
        order: 18,
        stage: "repetition-release-gate",
        agent: "repetition-gate-agent",
        primary_skill: "repetition-release-gate-skill",
        exit_condition: "Recovery comparison and repeated issue infrastructure pass, accepted release status is explicit, and release blocker state is explicit.",
        required_evidence: ["repetition-gate-audit.json"]
      },
      {
        order: 19,
        stage: "powerpoint-open-check",
        agent: "powerpoint-open-check-agent",
        primary_skill: "powerpoint-human-open-check-skill",
        exit_condition: "A fresh Microsoft PowerPoint open check newer than the PPTX build reports no recovery dialog.",
        required_evidence: ["manual_powerpoint_open_check", "manual-open-checks/latest-powerpoint-open-check.json"],
        manual_gate: true
      },
      {
        order: 20,
        stage: "routing-experiment-gate",
        agent: "representative-agent",
        primary_skill: "routing-experiment-gate-skill",
        exit_condition: "Should-trigger, should-not-trigger, expected behavior, and near-miss routing examples are recorded.",
        required_evidence: ["routing-experiment-table.md"]
      },
      {
        order: 21,
        stage: "representative-closeout",
        agent: "representative-agent",
        primary_skill: "repetition-release-gate-skill",
        exit_condition: "Closeout states structural readiness, release readiness, or blocked external boundary without mixing them.",
        required_evidence: ["authoring-agent-system-audit.json", "repetition-gate-audit.json"]
      }
    ],
    release_gates: [
      { id: "agent-system-integrity", source: "authoring-agent-system-audit.json", pass_when: "status=pass" },
      { id: "working-source-clarification", source: "working-source-clarification-packet.json", pass_when: "required clarification, conflict, and three-layer classification fields are present" },
      { id: "course-flow-map", source: "course-flow-map.md", pass_when: "whole lecture flow, fixed schedule, module sequence, session timing, learning arc, output chain, and non-goals are explicit before slide planning" },
      { id: "cognitive-authoring-packet", source: "cognitive-authoring-packet.json", pass_when: "required reader-task, semantic-fit, unfolding, visual-value, and readability-fit fields are present" },
      { id: "outline-notes-before-pptx", source: "outline-notes.md", pass_when: "required outline note fields are present before storyline, visualization, or PPTX build" },
      { id: "slide-planning-map", source: "slide-planning-map.json", pass_when: "each slide is connected to visual situation, cognitive operation, learner action, output artifact, timing budget, evidence boundary, and reuse policy before symbol collection" },
      { id: "storyline-readability-proxy", source: "storyline-readability-audit.json", pass_when: "status=pass and human_outcome_validation is not overstated" },
      { id: "session-feedback-patterns", source: "session-feedback-pattern-audit.json", pass_when: "required recurring feedback checks are present and unresolved patterns become revision queue items" },
      { id: "symbol-inventory", source: "symbol-inventory.json", pass_when: "symbols, semantic roles, target-expression vectors, possible confusion, visual candidates, selection reasons, and learner-facing boundaries are explicit before design-system work" },
      { id: "semantic-design-system", source: "semantic-design-system.json", pass_when: "design principles, symbol mapping, layout families, PPTX element use, layout element calculations, accessibility/density, calculated values, and implementation trace are derived from course flow, slide planning, and symbol inventory" },
      { id: "semantic-staging-design", source: "staging-design-brief.json", pass_when: "required semantic-staging fields are present before visualization or PPTX build and design expression remains open unless target constraints require a restriction" },
      { id: "image-first-visualization-proof", source: "image-first-visualization-packet.json", pass_when: "visual candidates or contact sheet exist before HTML/PPTX implementation when visual direction is unsettled or requested" },
      { id: "vlpp-expression-distance-boundary", source: "vlpp-expression-distance-monitor.json", pass_when: "distance metric, target vector, candidate vectors, distance-to-target, evidence_state=observed_computation, and non-psychological claim boundary are explicit" },
      { id: "presentationml-source-coverage", source: "spec_sources/presentationml/reports/presentationml-spec-audit.json", pass_when: "status=pass and coverage_counts.failed=0" },
      { id: "native-powerpoint-package", source: "native-feature-audit.json", pass_when: "status=pass and invalidTableCellAnchors=0 and slideWorkflowIssues=0" },
      { id: "artifact-surface-separation", source: "artifact-surface-map.json", pass_when: "required artifact surfaces are mapped to distinct roles, paths, and readiness states" },
      { id: "repetition-infrastructure", source: "repetition-gate-audit.json", pass_when: "status=pass and compare:recovery has no active repeated-recovery blocker" },
      { id: "release-readiness", source: "repetition-gate-audit.json", pass_when: "release_status=pass or release_status=pass_superseded_old_recovery_artifacts" },
      { id: "manual-powerpoint-open-success", source: "manual_powerpoint_open_check or manual-open-checks/latest-powerpoint-open-check.json", pass_when: "fresh PowerPoint open check newer than the PPTX build shows result=no_recovery_dialog" },
      { id: "routing-experiment-coverage", source: "routing-experiment-table.md", pass_when: "should-trigger, should-not-trigger, expected behavior, and near-miss rationale are present" }
    ]
  };
}

function toolsForSkill(skillId) {
  const map = {
    "evidence-freeze-skill": ["tools-check", "research-build", "research-check"],
    "working-source-clarification-skill": ["working-source-clarification-check"],
    "ziphyun-particle-research-skill": ["research-build", "research-check"],
    "cognitive-document-visual-authoring-skill": ["cognitive-authoring-packet-check"],
    "writing-flow-skill": ["course-flow-map-check", "manual-check", "prompt-check", "pipeline-check", "outline-note-check", "slide-planning-map-check"],
    "storyline-readability-gate-skill": ["storyline-readability-check"],
    "session-feedback-pattern-gate-skill": ["session-feedback-pattern-check"],
    "semantic-staging-design-skill": ["semantic-design-system-check", "semantic-staging-design-check"],
    "visualization-flow-skill": ["tools-check", "symbol-inventory-check", "semantic-design-system-check", "semantic-staging-design-check", "image-first-visualization-check", "vlpp-expression-distance-check"],
    "pptx-native-build-skill": ["system-init", "system-run", "pptx-standard-xml-build", "pptx-build", "native-powerpoint-check"],
    "drawingml-table-anchor-sanitizer-skill": ["native-powerpoint-check", "presentationml-spec-check"],
    "artifact-surface-separation-skill": ["artifact-surface-separation-check"],
    "presentationml-compliance-skill": ["presentationml-spec-check", "native-powerpoint-check"],
    "repetition-release-gate-skill": ["recovery-compare-check", "repetition-gate-check", "release-check"],
    "powerpoint-human-open-check-skill": ["manual-powerpoint-open-check"],
    "routing-experiment-gate-skill": ["routing-experiment-check"]
  };
  return map[skillId] || [];
}

function createSkillModule(def) {
  const bullets = (items) => items.map((item) => `- ${item}`).join("\n");
  return [
    `# ${def.title}`,
    "",
    `skill_id: ${def.skillId}  `,
    `agent_owner: ${def.owner}`,
    "",
    "## Trigger",
    "",
    def.trigger,
    "",
    "## Inputs",
    "",
    bullets(def.inputs),
    "",
    "## Outputs",
    "",
    bullets(def.outputs),
    "",
    "## Tools",
    "",
    bullets(def.tools),
    "",
    "## Exit Gate",
    "",
    def.exitGate,
    ""
  ].join("\n");
}

function createReadme() {
  return [
    "# Authoring Agent System",
    "",
    "This folder contains a local modular agent system for document, slide, and native PPTX authoring.",
    "",
    "## Check",
    "",
    "```bash",
    "node authoring_agent_system.js",
    "```",
    "",
    "The check proves structural readiness only. PowerPoint release readiness still needs a fresh Microsoft PowerPoint open check with no recovery dialog.",
    "",
    "## Compatible NPM Authoring Process",
    "",
    "Use this route when the target project exposes the compatible authoring scripts.",
    "",
    "```bash",
    "npm run system:init -- <work-id> --title \"<slide title>\"",
    "npm run system:run -- <work-id>",
    "npm run build",
    "npm run verify:presentationml-spec",
    "npm run research:build",
    "npm run verify:research",
    "npm run verify:powerpoint",
    "npm run compare:recovery",
    "npm run verify:repetition-gate",
    "# Open Document_Slide_Authoring_System_new.pptx in Microsoft PowerPoint",
    "# Record manual-open-checks/latest-powerpoint-open-check.json with result=no_recovery_dialog",
    "npm run verify:release",
    "npm run agent-system:check",
    "```",
    "",
    "Required run outputs: `09-system-state.json`, `10-system-runbook.md`, and `11-release-packet.md`.",
    "",
    "Accepted release statuses are `pass` and `pass_superseded_old_recovery_artifacts`. Running `npm test` after the manual PowerPoint open check can rebuild the PPTX, so repeat the open check if that happens.",
    "",
    "## Adaptation",
    "",
    "- Keep agent IDs, skill IDs, and workflow order stable unless the whole system is intentionally versioned.",
    "- Replace project-specific file names, commands, and evidence paths in `authoring-agent-system.json`.",
    "- Fix the working source of truth, clarification packet, conflict priority, and fixed/flexible/decisional classification before authoring.",
    "- Build `course-flow-map.md` before slide planning. Do not fix style, template, palette, motif, or design system first.",
    "- Build the cognitive authoring packet before writing, storyline/readability review, visualization, or PPTX build.",
    "- Write outline notes before storyline/readability review, visualization, or PPTX build.",
    "- Build `slide-planning-map.json` before symbol collection, and connect each slide to situation, cognitive operation, learner action, output artifact, timing, evidence, and reuse policy.",
    "- Build `symbol-inventory.json` before `semantic-design-system.json`; symbols must carry semantic roles, possible confusion, visual candidates, and selection reasons.",
    "- Build `semantic-design-system.json` from course flow, slide planning, and symbols, not from a predefined look.",
    "- Calculate element tradeoff, placement, front/back order, reading order, native object order, and overlap risk before PPTX object placement.",
    "- Keep writing and visualization as separate processes.",
    "- Keep storyline/readability checks between writing and visualization.",
    "- Turn recurring review comments into session feedback pattern gates before more visual work.",
    "- Create a semantic-staging design brief before visualization or PPTX build without forcing a predefined style kit, template, fixed image-generation method, motif, palette, icon style, animation plan, or recurring visual language.",
    "- Treat visual values as intentional semantic decisions when selected, and record what remains intentionally unconstrained.",
    "- Separate learner-facing artifacts, instructor/facilitator artifacts, production source, evidence tables, proof surfaces, and handoff packages.",
    "- Keep the manual PowerPoint open check as a release gate.",
    "- When the compatible npm route is available, keep `system:init`, `system:run`, build, PresentationML/native checks, recovery comparison, manual open check, release check, and agent-system check in that order.",
    ""
  ].join("\n");
}

function createGeneratedCheckerSource() {
  const lines = [
    "#!/usr/bin/env node",
    "\"use strict\";",
    "",
    "const fs = require(\"fs\");",
    "const path = require(\"path\");",
    "",
    `const SYSTEM_ID = ${JSON.stringify(SYSTEM_ID)};`,
    `const REQUIRED_AGENTS = ${JSON.stringify(REQUIRED_AGENTS, null, 2)};`,
    `const REQUIRED_SKILLS = ${JSON.stringify(REQUIRED_SKILLS, null, 2)};`,
    `const REQUIRED_TOOLS = ${JSON.stringify(REQUIRED_TOOLS, null, 2)};`,
    `const REQUIRED_WORKFLOW_STAGES = ${JSON.stringify(REQUIRED_WORKFLOW_STAGES, null, 2)};`,
    `const REQUIRED_RELEASE_GATES = ${JSON.stringify(REQUIRED_RELEASE_GATES, null, 2)};`,
    `const REQUIRED_SKILL_HEADINGS = ${JSON.stringify(REQUIRED_SKILL_HEADINGS, null, 2)};`,
    `const REQUIRED_AUTHORING_PACKET_FIELDS = ${JSON.stringify(REQUIRED_AUTHORING_PACKET_FIELDS, null, 2)};`,
    `const REQUIRED_VISUAL_VALUE_FIELDS = ${JSON.stringify(REQUIRED_VISUAL_VALUE_FIELDS, null, 2)};`,
    `const REQUIRED_READABILITY_FIT_FIELDS = ${JSON.stringify(REQUIRED_READABILITY_FIT_FIELDS, null, 2)};`,
    `const REQUIRED_OUTLINE_NOTE_FIELDS = ${JSON.stringify(REQUIRED_OUTLINE_NOTE_FIELDS, null, 2)};`,
    `const REQUIRED_CLARIFICATION_FIELDS = ${JSON.stringify(REQUIRED_CLARIFICATION_FIELDS, null, 2)};`,
    `const REQUIRED_THREE_LAYER_FIELDS = ${JSON.stringify(REQUIRED_THREE_LAYER_FIELDS, null, 2)};`,
    `const REQUIRED_INTENTIONAL_IMPLEMENTATION_FIELDS = ${JSON.stringify(REQUIRED_INTENTIONAL_IMPLEMENTATION_FIELDS, null, 2)};`,
    `const REQUIRED_CALCULATED_VALUE_FIELDS = ${JSON.stringify(REQUIRED_CALCULATED_VALUE_FIELDS, null, 2)};`,
    `const REQUIRED_LAYOUT_ELEMENT_CALCULATION_FIELDS = ${JSON.stringify(REQUIRED_LAYOUT_ELEMENT_CALCULATION_FIELDS, null, 2)};`,
    `const REQUIRED_SESSION_FEEDBACK_CHECKS = ${JSON.stringify(REQUIRED_SESSION_FEEDBACK_CHECKS, null, 2)};`,
    `const REQUIRED_COURSE_FLOW_FIELDS = ${JSON.stringify(REQUIRED_COURSE_FLOW_FIELDS, null, 2)};`,
    `const REQUIRED_SLIDE_PLANNING_FIELDS = ${JSON.stringify(REQUIRED_SLIDE_PLANNING_FIELDS, null, 2)};`,
    `const REQUIRED_SYMBOL_INVENTORY_FIELDS = ${JSON.stringify(REQUIRED_SYMBOL_INVENTORY_FIELDS, null, 2)};`,
    `const REQUIRED_SEMANTIC_DESIGN_SYSTEM_FIELDS = ${JSON.stringify(REQUIRED_SEMANTIC_DESIGN_SYSTEM_FIELDS, null, 2)};`,
    `const REQUIRED_STAGING_DESIGN_FIELDS = ${JSON.stringify(REQUIRED_STAGING_DESIGN_FIELDS, null, 2)};`,
    `const REQUIRED_IMAGE_FIRST_VISUALIZATION_FIELDS = ${JSON.stringify(REQUIRED_IMAGE_FIRST_VISUALIZATION_FIELDS, null, 2)};`,
    `const REQUIRED_ARTIFACT_SURFACES = ${JSON.stringify(REQUIRED_ARTIFACT_SURFACES, null, 2)};`,
    `const REQUIRED_ROUTING_EXPERIMENT_FIELDS = ${JSON.stringify(REQUIRED_ROUTING_EXPERIMENT_FIELDS, null, 2)};`,
    `const COMPATIBLE_NPM_STATE_OUTPUTS = ${JSON.stringify(COMPATIBLE_NPM_STATE_OUTPUTS, null, 2)};`,
    `const COMPATIBLE_NPM_BUILD_OUTPUT = ${JSON.stringify(COMPATIBLE_NPM_BUILD_OUTPUT)};`,
    `const COMPATIBLE_NPM_MANUAL_OPEN_CHECK = ${JSON.stringify(COMPATIBLE_NPM_MANUAL_OPEN_CHECK)};`,
    `const COMPATIBLE_NPM_ACCEPTED_RELEASE_STATUSES = ${JSON.stringify(COMPATIBLE_NPM_ACCEPTED_RELEASE_STATUSES, null, 2)};`,
    `const RUNTIME_COMPATIBILITY_STATUSES = new Set(${JSON.stringify(Array.from(RUNTIME_COMPATIBILITY_STATUSES), null, 2)});`,
    "",
    "function readJson(file) { return JSON.parse(fs.readFileSync(file, \"utf8\")); }",
    "function exists(root, rel) { return fs.existsSync(path.join(root, rel)); }",
    "function compatibleManualOpenCheck(root) {",
    "  const manualPath = path.join(root, COMPATIBLE_NPM_MANUAL_OPEN_CHECK);",
    "  const pptxPath = path.join(root, COMPATIBLE_NPM_BUILD_OUTPUT);",
    "  if (!fs.existsSync(manualPath)) return { pass: false, reason: \"missing_compatible_manual_open_check\", path: COMPATIBLE_NPM_MANUAL_OPEN_CHECK };",
    "  try {",
    "    const manual = readJson(manualPath);",
    "    const resultOk = manual.result === \"no_recovery_dialog\";",
    "    const pptxExists = fs.existsSync(pptxPath);",
    "    const manualMtime = fs.statSync(manualPath).mtimeMs;",
    "    const pptxMtime = pptxExists ? fs.statSync(pptxPath).mtimeMs : null;",
    "    const freshnessOk = pptxExists && manualMtime >= pptxMtime;",
    "    return { pass: resultOk && freshnessOk, path: COMPATIBLE_NPM_MANUAL_OPEN_CHECK, result: manual.result || null, pptx_path: COMPATIBLE_NPM_BUILD_OUTPUT, freshness: freshnessOk ? \"manual_check_newer_or_equal_to_pptx\" : \"manual_check_missing_or_older_than_pptx\" };",
    "  } catch (error) {",
    "    return { pass: false, reason: \"invalid_compatible_manual_open_check\", path: COMPATIBLE_NPM_MANUAL_OPEN_CHECK, message: error.message };",
    "  }",
    "}",
    "function ids(list) { return new Set(Array.isArray(list) ? list.map((item) => item && item.id).filter(Boolean) : []); }",
    "function stages(list) { return new Set(Array.isArray(list) ? list.map((item) => item && item.stage).filter(Boolean) : []); }",
    "function add(checks, name, pass, details) { checks.push({ name, status: pass ? \"pass\" : \"fail\", details }); }",
    "function checkRequiredSet(checks, name, required, actualSet) { const missing = required.filter((id) => !actualSet.has(id)); add(checks, name, missing.length === 0, { missing }); }",
    "function listSet(value) { return new Set(Array.isArray(value) ? value.filter(Boolean) : []); }",
    "function stageIndex(workflow, stage) { return workflow.findIndex((item) => item && item.stage === stage); }",
    "function checkStageOrder(checks, workflow, name, before, after) {",
    "  const beforeIndex = stageIndex(workflow, before);",
    "  const afterIndex = stageIndex(workflow, after);",
    "  add(checks, name, beforeIndex >= 0 && afterIndex >= 0 && beforeIndex < afterIndex, { before, after, beforeIndex, afterIndex });",
    "}",
    "function checkWorkflowOrderContract(checks, system) {",
    "  const workflow = Array.isArray(system.workflow) ? system.workflow : [];",
    "  const expected = REQUIRED_WORKFLOW_STAGES;",
    "  const actual = workflow.map((item) => item && item.stage).filter(Boolean);",
    "  const mismatch = [];",
    "  for (let index = 0; index < expected.length; index += 1) {",
    "    if (actual[index] !== expected[index]) mismatch.push({ index, expected: expected[index], actual: actual[index] || null });",
    "  }",
    "  add(checks, \"fixed workflow stage order\", mismatch.length === 0, { mismatch, actual });",
    "  checkStageOrder(checks, workflow, \"course flow precedes slide planning\", \"course-flow-map\", \"slide-planning-map\");",
    "  checkStageOrder(checks, workflow, \"slide planning precedes symbol inventory\", \"slide-planning-map\", \"symbol-inventory\");",
    "  checkStageOrder(checks, workflow, \"symbol inventory precedes semantic design system\", \"symbol-inventory\", \"semantic-design-system\");",
    "  checkStageOrder(checks, workflow, \"semantic design system precedes semantic staging\", \"semantic-design-system\", \"semantic-staging-design-gate\");",
    "  checkStageOrder(checks, workflow, \"semantic design system precedes image-first visualization\", \"semantic-design-system\", \"image-first-visualization-gate\");",
    "  checkStageOrder(checks, workflow, \"semantic design system precedes PPTX build\", \"semantic-design-system\", \"new-pptx-native-build\");",
    "  checkStageOrder(checks, workflow, \"semantic staging precedes image-first visualization\", \"semantic-staging-design-gate\", \"image-first-visualization-gate\");",
    "  checkStageOrder(checks, workflow, \"image-first visualization precedes open visualization planning\", \"image-first-visualization-gate\", \"open-visualization-planning\");",
    "  checkStageOrder(checks, workflow, \"image-first visualization precedes PPTX build\", \"image-first-visualization-gate\", \"new-pptx-native-build\");",
    "  checkStageOrder(checks, workflow, \"open visualization planning precedes PPTX build\", \"open-visualization-planning\", \"new-pptx-native-build\");",
    "}",
    "function checkCognitiveAuthoringContract(checks, system) {",
    "  const packet = system.cognitive_authoring_packet || {};",
    "  add(checks, \"cognitive authoring process lock\", packet.process_lock === \"cognitive-document-visual-authoring-v1\", { actual: packet.process_lock || null });",
    "  checkRequiredSet(checks, \"authoring packet required fields\", REQUIRED_AUTHORING_PACKET_FIELDS, listSet(packet.required_fields));",
    "  checkRequiredSet(checks, \"visual value required fields\", REQUIRED_VISUAL_VALUE_FIELDS, listSet(packet.visual_value_required_fields));",
    "  checkRequiredSet(checks, \"readability fit required fields\", REQUIRED_READABILITY_FIT_FIELDS, listSet(packet.readability_fit_required_fields));",
    "  const workflow = Array.isArray(system.workflow) ? system.workflow : [];",
    "  const cognitiveIndex = workflow.findIndex((item) => item && item.stage === \"cognitive-authoring-packet\");",
    "  const writingIndex = workflow.findIndex((item) => item && item.stage === \"writing-flow\");",
    "  const visualizationIndex = workflow.findIndex((item) => item && item.stage === \"open-visualization-planning\");",
    "  add(checks, \"cognitive authoring precedes writing\", cognitiveIndex >= 0 && writingIndex >= 0 && cognitiveIndex < writingIndex, { cognitiveIndex, writingIndex });",
    "  add(checks, \"cognitive authoring precedes visualization\", cognitiveIndex >= 0 && visualizationIndex >= 0 && cognitiveIndex < visualizationIndex, { cognitiveIndex, visualizationIndex });",
    "}",
    "",
    "function checkOutlineNoteContract(checks, system) {",
    "  const contract = system.outline_note_contract || {};",
    "  checkRequiredSet(checks, \"outline note required fields\", REQUIRED_OUTLINE_NOTE_FIELDS, listSet(contract.required_fields));",
    "  add(checks, \"outline note rule\", Boolean(contract.rule), { rule: contract.rule || null });",
    "  const workflow = Array.isArray(system.workflow) ? system.workflow : [];",
    "  const writingIndex = workflow.findIndex((item) => item && item.stage === \"writing-flow\");",
    "  const outlineIndex = workflow.findIndex((item) => item && item.stage === \"outline-note-gate\");",
    "  const storylineIndex = workflow.findIndex((item) => item && item.stage === \"storyline-readability-gate\");",
    "  const visualizationIndex = workflow.findIndex((item) => item && item.stage === \"open-visualization-planning\");",
    "  const pptxIndex = workflow.findIndex((item) => item && item.stage === \"new-pptx-native-build\");",
    "  add(checks, \"outline notes follow writing\", writingIndex >= 0 && outlineIndex >= 0 && writingIndex <= outlineIndex, { writingIndex, outlineIndex });",
    "  add(checks, \"outline notes precede storyline\", outlineIndex >= 0 && storylineIndex >= 0 && outlineIndex < storylineIndex, { outlineIndex, storylineIndex });",
    "  add(checks, \"outline notes precede visualization\", outlineIndex >= 0 && visualizationIndex >= 0 && outlineIndex < visualizationIndex, { outlineIndex, visualizationIndex });",
    "  add(checks, \"outline notes precede PPTX build\", outlineIndex >= 0 && pptxIndex >= 0 && outlineIndex < pptxIndex, { outlineIndex, pptxIndex });",
    "  const pptxStep = workflow.find((item) => item && item.stage === \"new-pptx-native-build\") || {};",
    "  const pptxEvidence = listSet(pptxStep.required_evidence);",
    "  add(checks, \"PPTX build requires outline notes\", pptxEvidence.has(\"outline-notes.md\"), { required_evidence: Array.from(pptxEvidence) });",
    "}",
    "",
    "function checkWorkingSourceContract(checks, system) {",
    "  const contract = system.working_source_contract || {};",
    "  checkRequiredSet(checks, \"working source clarification fields\", REQUIRED_CLARIFICATION_FIELDS, listSet(contract.required_fields));",
    "  const conflict = system.conflict_resolution || {};",
    "  add(checks, \"conflict resolution priority order\", Array.isArray(conflict.priority_order) && conflict.priority_order.length >= 4 && Boolean(conflict.rule), { priority_count: Array.isArray(conflict.priority_order) ? conflict.priority_order.length : 0, has_rule: Boolean(conflict.rule) });",
    "  const threeLayer = system.three_layer_contract || {};",
    "  checkRequiredSet(checks, \"three-layer classification fields\", REQUIRED_THREE_LAYER_FIELDS, listSet(threeLayer.required_fields));",
    "  add(checks, \"three-layer drift rule\", Boolean(threeLayer.drift_rule), { drift_rule: threeLayer.drift_rule || null });",
    "  add(checks, \"fixed decisions declared\", Array.isArray(threeLayer.fixed) && threeLayer.fixed.length >= 3, { fixed: threeLayer.fixed || [] });",
    "  add(checks, \"flexible decisions declared\", Array.isArray(threeLayer.flexible) && threeLayer.flexible.length >= 3, { flexible: threeLayer.flexible || [] });",
    "  add(checks, \"decisional decisions declared\", Array.isArray(threeLayer.decisional) && threeLayer.decisional.length >= 3, { decisional: threeLayer.decisional || [] });",
    "  const intentional = system.intentional_implementation_contract || {};",
    "  checkRequiredSet(checks, \"intentional implementation fields\", REQUIRED_INTENTIONAL_IMPLEMENTATION_FIELDS, listSet(intentional.required_fields));",
    "  checkRequiredSet(checks, \"calculated value fields\", REQUIRED_CALCULATED_VALUE_FIELDS, listSet(intentional.calculated_value_required_fields));",
    "  add(checks, \"intentional implementation rules\", Boolean(intentional.fixed_rule && intentional.flexible_rule && intentional.decisional_rule && intentional.implementation_rule), { has_fixed_rule: Boolean(intentional.fixed_rule), has_flexible_rule: Boolean(intentional.flexible_rule), has_decisional_rule: Boolean(intentional.decisional_rule), has_implementation_rule: Boolean(intentional.implementation_rule) });",
    "  const workflow = Array.isArray(system.workflow) ? system.workflow : [];",
    "  const sourceIndex = workflow.findIndex((item) => item && item.stage === \"working-source-clarification\");",
    "  const cognitiveIndex = workflow.findIndex((item) => item && item.stage === \"cognitive-authoring-packet\");",
    "  add(checks, \"working source precedes cognitive authoring\", sourceIndex >= 0 && cognitiveIndex >= 0 && sourceIndex < cognitiveIndex, { sourceIndex, cognitiveIndex });",
    "}",
    "",
    "function checkCourseFlowToDesignSystemContract(checks, system) {",
    "  const contract = system.course_flow_to_design_system_contract || {};",
    "  const sequence = Array.isArray(contract.sequence_lock) ? contract.sequence_lock : [];",
    "  const expectedSequence = [\"course-flow-map\", \"slide-planning-map\", \"symbol-inventory\", \"semantic-design-system\"];",
    "  const sequenceMismatch = expectedSequence.filter((stage, index) => sequence[index] !== stage);",
    "  add(checks, \"course flow to design system sequence lock\", sequenceMismatch.length === 0, { expected: expectedSequence, actual: sequence, mismatch: sequenceMismatch });",
    "  add(checks, \"course flow design-start rule\", Boolean(contract.rule) && /First map the whole lecture flow/i.test(contract.rule), { rule: contract.rule || null });",
    "  const files = contract.required_files || {};",
    "  add(checks, \"course flow required files declared\", files.course_flow_map === \"course-flow-map.md\" && files.slide_planning_map === \"slide-planning-map.json\" && files.symbol_inventory === \"symbol-inventory.json\" && files.semantic_design_system === \"semantic-design-system.json\", { required_files: files });",
    "  checkRequiredSet(checks, \"course flow required fields\", REQUIRED_COURSE_FLOW_FIELDS, listSet(contract.course_flow_required_fields));",
    "  checkRequiredSet(checks, \"slide planning required fields\", REQUIRED_SLIDE_PLANNING_FIELDS, listSet(contract.slide_planning_required_fields));",
    "  checkRequiredSet(checks, \"symbol inventory required fields\", REQUIRED_SYMBOL_INVENTORY_FIELDS, listSet(contract.symbol_inventory_required_fields));",
    "  checkRequiredSet(checks, \"semantic design system required fields\", REQUIRED_SEMANTIC_DESIGN_SYSTEM_FIELDS, listSet(contract.semantic_design_system_required_fields));",
    "  checkRequiredSet(checks, \"layout element calculation fields\", REQUIRED_LAYOUT_ELEMENT_CALCULATION_FIELDS, listSet(contract.layout_element_calculation_required_fields));",
    "  add(checks, \"design start boundary\", /course-flow-map\\.md/i.test(contract.design_start_boundary || \"\") && /slide-planning-map\\.json/i.test(contract.design_start_boundary || \"\") && /symbol-inventory\\.json/i.test(contract.design_start_boundary || \"\"), { design_start_boundary: contract.design_start_boundary || null });",
    "  add(checks, \"learner-facing boundary\", /Internal file paths/i.test(contract.learner_facing_boundary || \"\") && /learner-facing/i.test(contract.learner_facing_boundary || \"\"), { learner_facing_boundary: contract.learner_facing_boundary || null });",
    "  const workflow = Array.isArray(system.workflow) ? system.workflow : [];",
    "  const courseStep = workflow.find((item) => item && item.stage === \"course-flow-map\") || {};",
    "  const slideStep = workflow.find((item) => item && item.stage === \"slide-planning-map\") || {};",
    "  const symbolStep = workflow.find((item) => item && item.stage === \"symbol-inventory\") || {};",
    "  const designStep = workflow.find((item) => item && item.stage === \"semantic-design-system\") || {};",
    "  const pptxStep = workflow.find((item) => item && item.stage === \"new-pptx-native-build\") || {};",
    "  const courseEvidence = listSet(courseStep.required_evidence);",
    "  const slideEvidence = listSet(slideStep.required_evidence);",
    "  const symbolEvidence = listSet(symbolStep.required_evidence);",
    "  const designEvidence = listSet(designStep.required_evidence);",
    "  const pptxEvidence = listSet(pptxStep.required_evidence);",
    "  add(checks, \"course stage requires course-flow-map\", courseEvidence.has(\"course-flow-map.md\"), { required_evidence: Array.from(courseEvidence) });",
    "  add(checks, \"slide planning stage requires slide-planning-map\", slideEvidence.has(\"slide-planning-map.json\"), { required_evidence: Array.from(slideEvidence) });",
    "  add(checks, \"symbol stage requires symbol-inventory\", symbolEvidence.has(\"symbol-inventory.json\"), { required_evidence: Array.from(symbolEvidence) });",
    "  add(checks, \"semantic design stage requires upstream maps\", [\"course-flow-map.md\", \"slide-planning-map.json\", \"symbol-inventory.json\", \"semantic-design-system.json\"].every((item) => designEvidence.has(item)), { required_evidence: Array.from(designEvidence) });",
    "  add(checks, \"PPTX build requires planning and design maps\", [\"slide-planning-map.json\", \"symbol-inventory.json\", \"semantic-design-system.json\"].every((item) => pptxEvidence.has(item)), { required_evidence: Array.from(pptxEvidence) });",
    "}",
    "",
    "function checkSessionFeedbackContract(checks, system) {",
    "  const gate = system.session_feedback_pattern_gate || {};",
    "  checkRequiredSet(checks, \"session feedback checks\", REQUIRED_SESSION_FEEDBACK_CHECKS, listSet(gate.required_checks));",
    "  add(checks, \"session feedback rule\", Boolean(gate.rule), { rule: gate.rule || null });",
    "  const workflow = Array.isArray(system.workflow) ? system.workflow : [];",
    "  const storylineIndex = workflow.findIndex((item) => item && item.stage === \"storyline-readability-gate\");",
    "  const feedbackIndex = workflow.findIndex((item) => item && item.stage === \"session-feedback-pattern-gate\");",
    "  const visualizationIndex = workflow.findIndex((item) => item && item.stage === \"open-visualization-planning\");",
    "  add(checks, \"session feedback follows storyline\", storylineIndex >= 0 && feedbackIndex >= 0 && storylineIndex < feedbackIndex, { storylineIndex, feedbackIndex });",
    "  add(checks, \"session feedback precedes visualization\", feedbackIndex >= 0 && visualizationIndex >= 0 && feedbackIndex < visualizationIndex, { feedbackIndex, visualizationIndex });",
    "}",
    "",
    "function checkSemanticStagingContract(checks, system) {",
    "  const framework = system.semantic_staging_design_framework || {};",
    "  checkRequiredSet(checks, \"semantic staging design fields\", REQUIRED_STAGING_DESIGN_FIELDS, listSet(framework.required_fields));",
    "  add(checks, \"semantic staging rule\", Boolean(framework.rule), { rule: framework.rule || null });",
    "  add(checks, \"design freedom boundary\", /optional|unless|constraint|unconstrained/i.test(framework.freedom_boundary || \"\"), { freedom_boundary: framework.freedom_boundary || null });",
    "  const workflow = Array.isArray(system.workflow) ? system.workflow : [];",
    "  const feedbackIndex = workflow.findIndex((item) => item && item.stage === \"session-feedback-pattern-gate\");",
    "  const stagingIndex = workflow.findIndex((item) => item && item.stage === \"semantic-staging-design-gate\");",
    "  const visualizationIndex = workflow.findIndex((item) => item && item.stage === \"open-visualization-planning\");",
    "  const pptxIndex = workflow.findIndex((item) => item && item.stage === \"new-pptx-native-build\");",
    "  add(checks, \"semantic staging follows session feedback\", feedbackIndex >= 0 && stagingIndex >= 0 && feedbackIndex < stagingIndex, { feedbackIndex, stagingIndex });",
    "  add(checks, \"semantic staging precedes visualization\", stagingIndex >= 0 && visualizationIndex >= 0 && stagingIndex < visualizationIndex, { stagingIndex, visualizationIndex });",
    "  add(checks, \"semantic staging precedes PPTX build\", stagingIndex >= 0 && pptxIndex >= 0 && stagingIndex < pptxIndex, { stagingIndex, pptxIndex });",
    "  const visualizationStep = workflow.find((item) => item && item.stage === \"open-visualization-planning\") || {};",
    "  const pptxStep = workflow.find((item) => item && item.stage === \"new-pptx-native-build\") || {};",
    "  const visualizationEvidence = listSet(visualizationStep.required_evidence);",
    "  const pptxEvidence = listSet(pptxStep.required_evidence);",
    "  add(checks, \"visualization requires staging brief\", visualizationEvidence.has(\"staging-design-brief.json\"), { required_evidence: Array.from(visualizationEvidence) });",
    "  add(checks, \"PPTX build requires staging brief\", pptxEvidence.has(\"staging-design-brief.json\"), { required_evidence: Array.from(pptxEvidence) });",
    "}",
    "",
    "function checkImageFirstVisualizationContract(checks, system) {",
    "  const framework = system.image_first_visualization_framework || {};",
    "  checkRequiredSet(checks, \"image-first visualization fields\", REQUIRED_IMAGE_FIRST_VISUALIZATION_FIELDS, listSet(framework.required_fields));",
    "  add(checks, \"image-first visualization rule\", Boolean(framework.rule), { rule: framework.rule || null });",
    "  add(checks, \"VLPP expression-distance boundary\", /distance/i.test(framework.vlpp_boundary || \"\") && /psychology|comprehension|persuasion|retention|behavior/i.test(framework.vlpp_boundary || \"\"), { vlpp_boundary: framework.vlpp_boundary || null });",
    "  add(checks, \"VLPP observed computation evidence state\", framework.evidence_state_required === \"observed_computation\", { evidence_state_required: framework.evidence_state_required || null });",
    "  const workflow = Array.isArray(system.workflow) ? system.workflow : [];",
    "  checkStageOrder(checks, workflow, \"image-first follows semantic staging\", \"semantic-staging-design-gate\", \"image-first-visualization-gate\");",
    "  checkStageOrder(checks, workflow, \"image-first precedes open visualization\", \"image-first-visualization-gate\", \"open-visualization-planning\");",
    "  checkStageOrder(checks, workflow, \"image-first precedes native PPTX build\", \"image-first-visualization-gate\", \"new-pptx-native-build\");",
    "  const imageStep = workflow.find((item) => item && item.stage === \"image-first-visualization-gate\") || {};",
    "  const imageEvidence = listSet(imageStep.required_evidence);",
    "  const hasImageEvidence = (name) => Array.from(imageEvidence).some((item) => item === name || item.endsWith('/' + name));",
    "  add(checks, \"image-first gate requires packet\", hasImageEvidence(\"image-first-visualization-packet.json\"), { required_evidence: Array.from(imageEvidence) });",
    "  add(checks, \"image-first gate requires contact sheet\", hasImageEvidence(\"visual-candidate-contact-sheet.png\"), { required_evidence: Array.from(imageEvidence) });",
    "  add(checks, \"image-first gate requires VLPP monitor\", hasImageEvidence(\"vlpp-expression-distance-monitor.json\"), { required_evidence: Array.from(imageEvidence) });",
    "}",
    "",
    "function checkArtifactSurfaceContract(checks, system) {",
    "  const gate = system.artifact_surface_separation || {};",
    "  checkRequiredSet(checks, \"artifact surfaces\", REQUIRED_ARTIFACT_SURFACES, listSet(gate.required_surfaces));",
    "  add(checks, \"artifact surface rule\", Boolean(gate.rule), { rule: gate.rule || null });",
    "  const workflow = Array.isArray(system.workflow) ? system.workflow : [];",
    "  const pptxIndex = workflow.findIndex((item) => item && item.stage === \"new-pptx-native-build\");",
    "  const surfaceIndex = workflow.findIndex((item) => item && item.stage === \"artifact-surface-separation\");",
    "  const closeoutIndex = workflow.findIndex((item) => item && item.stage === \"representative-closeout\");",
    "  add(checks, \"artifact surface follows PPTX build\", pptxIndex >= 0 && surfaceIndex >= 0 && pptxIndex < surfaceIndex, { pptxIndex, surfaceIndex });",
    "  add(checks, \"artifact surface precedes closeout\", surfaceIndex >= 0 && closeoutIndex >= 0 && surfaceIndex < closeoutIndex, { surfaceIndex, closeoutIndex });",
    "}",
    "",
    "function checkRoutingExperimentContract(checks, system) {",
    "  const routing = system.routing_experiments || {};",
    "  checkRequiredSet(checks, \"routing experiment fields\", REQUIRED_ROUTING_EXPERIMENT_FIELDS, listSet(routing.required_fields));",
    "  add(checks, \"routing experiment positive and negative cases\", Array.isArray(routing.should_trigger) && routing.should_trigger.length >= 2 && Array.isArray(routing.should_not_trigger) && routing.should_not_trigger.length >= 2, { should_trigger: Array.isArray(routing.should_trigger) ? routing.should_trigger.length : 0, should_not_trigger: Array.isArray(routing.should_not_trigger) ? routing.should_not_trigger.length : 0 });",
    "  add(checks, \"routing experiment expected behavior\", Boolean(routing.expected_behavior), { expected_behavior: routing.expected_behavior || null });",
    "}",
    "",
    "function checkCompatibleNpmProcessContract(checks, system) {",
    "  const process = system.compatible_npm_authoring_process || {};",
    "  add(checks, \"compatible npm authoring process declared\", Boolean(process.init_command && process.run_command && process.build_command), { init_command: process.init_command || null, run_command: process.run_command || null, build_command: process.build_command || null });",
    "  const stateOutputs = listSet(process.state_outputs);",
    "  checkRequiredSet(checks, \"compatible npm state outputs declared\", COMPATIBLE_NPM_STATE_OUTPUTS, stateOutputs);",
    "  add(checks, \"compatible npm PPTX output declared\", process.build_output === COMPATIBLE_NPM_BUILD_OUTPUT, { expected: COMPATIBLE_NPM_BUILD_OUTPUT, actual: process.build_output || null });",
    "  const manual = process.manual_open_check || {};",
    "  add(checks, \"compatible npm manual open gate declared\", manual.path === COMPATIBLE_NPM_MANUAL_OPEN_CHECK && manual.required_result === \"no_recovery_dialog\" && /newer/i.test(manual.freshness_rule || \"\"), { manual_open_check: manual });",
    "  const statuses = listSet(process.accepted_release_statuses);",
    "  checkRequiredSet(checks, \"compatible npm accepted release statuses declared\", COMPATIBLE_NPM_ACCEPTED_RELEASE_STATUSES, statuses);",
    "  add(checks, \"compatible npm rebuild warning declared\", /npm test/i.test(process.rebuild_warning || \"\") && /build/i.test(process.rebuild_warning || \"\") && /open check|PowerPoint/i.test(process.rebuild_warning || \"\"), { rebuild_warning: process.rebuild_warning || null });",
    "  const toolSet = ids(system.tools);",
    "  checkRequiredSet(checks, \"compatible npm command tools declared\", [\"system-init\", \"system-run\", \"pptx-build\", \"presentationml-spec-check\", \"research-build\", \"research-check\", \"native-powerpoint-check\", \"recovery-compare-check\", \"repetition-gate-check\", \"release-check\", \"agent-system-check\", \"manual-powerpoint-open-check\"], toolSet);",
    "  const workflow = Array.isArray(system.workflow) ? system.workflow : [];",
    "  const pptxStep = workflow.find((item) => item && item.stage === \"new-pptx-native-build\") || {};",
    "  const pptxEvidence = listSet(pptxStep.required_evidence);",
    "  const missingPptxEvidence = COMPATIBLE_NPM_STATE_OUTPUTS.concat([COMPATIBLE_NPM_BUILD_OUTPUT]).filter((item) => !pptxEvidence.has(item));",
    "  add(checks, \"compatible npm build evidence routed\", missingPptxEvidence.length === 0, { missing: missingPptxEvidence, required_evidence: Array.from(pptxEvidence) });",
    "  const openStep = workflow.find((item) => item && item.stage === \"powerpoint-open-check\") || {};",
    "  const openEvidence = listSet(openStep.required_evidence);",
    "  add(checks, \"compatible npm manual open evidence routed\", openEvidence.has(COMPATIBLE_NPM_MANUAL_OPEN_CHECK), { required_evidence: Array.from(openEvidence), expected: COMPATIBLE_NPM_MANUAL_OPEN_CHECK });",
    "}",
    "",
    "function check(root) {",
    "  const targetRoot = path.resolve(root || process.cwd());",
    "  const checks = [];",
    "  const recommendations = [];",
    "  const systemPath = path.join(targetRoot, \"authoring-agent-system.json\");",
    "  if (!fs.existsSync(systemPath)) {",
    "    add(checks, \"system file exists\", false, { path: systemPath });",
    "    return writeAudit(targetRoot, checks, recommendations, [], []);",
    "  }",
    "  let system;",
    "  try { system = readJson(systemPath); add(checks, \"system JSON parses\", true, { path: systemPath }); }",
    "  catch (error) { add(checks, \"system JSON parses\", false, { message: error.message }); return writeAudit(targetRoot, checks, recommendations, [], []); }",
    "  add(checks, \"system id\", system.system_id === SYSTEM_ID, { expected: SYSTEM_ID, actual: system.system_id });",
    "  add(checks, \"claim boundary separates structural and release readiness\", /structural|local computational|agent-system/i.test(system.claim_boundary || \"\") && /release/i.test(system.claim_boundary || \"\"), { claim_boundary: system.claim_boundary || null });",
    "  const runtimeStatus = system.runtime_compatibility && system.runtime_compatibility.status;",
    "  add(checks, \"runtime compatibility status\", RUNTIME_COMPATIBILITY_STATUSES.has(runtimeStatus), { actual: runtimeStatus, allowed: Array.from(RUNTIME_COMPATIBILITY_STATUSES) });",
    "  checkRequiredSet(checks, \"required agents\", REQUIRED_AGENTS, ids(system.agents));",
    "  checkRequiredSet(checks, \"required skills\", REQUIRED_SKILLS.map((item) => item.id), ids(system.skills));",
    "  checkRequiredSet(checks, \"required tools\", REQUIRED_TOOLS, ids(system.tools));",
    "  checkRequiredSet(checks, \"required workflow stages\", REQUIRED_WORKFLOW_STAGES, stages(system.workflow));",
    "  checkRequiredSet(checks, \"required release gates\", REQUIRED_RELEASE_GATES, ids(system.release_gates));",
    "  checkWorkflowOrderContract(checks, system);",
    "  checkWorkingSourceContract(checks, system);",
    "  checkCourseFlowToDesignSystemContract(checks, system);",
    "  checkCognitiveAuthoringContract(checks, system);",
    "  checkOutlineNoteContract(checks, system);",
    "  checkSessionFeedbackContract(checks, system);",
    "  checkSemanticStagingContract(checks, system);",
    "  checkImageFirstVisualizationContract(checks, system);",
    "  checkArtifactSurfaceContract(checks, system);",
    "  checkRoutingExperimentContract(checks, system);",
    "  checkCompatibleNpmProcessContract(checks, system);",
    "  const manualGate = Array.isArray(system.workflow) && system.workflow.some((item) => item && item.stage === \"powerpoint-open-check\" && item.manual_gate === true);",
    "  add(checks, \"manual PowerPoint gate\", manualGate, { required_stage: \"powerpoint-open-check\" });",
    "  for (const skill of REQUIRED_SKILLS) {",
    "    const file = path.join(targetRoot, skill.path);",
    "    const present = fs.existsSync(file);",
    "    add(checks, `skill module exists: ${skill.id}`, present, { path: skill.path });",
    "    if (present) {",
    "      const content = fs.readFileSync(file, \"utf8\");",
    "      const missingHeadings = REQUIRED_SKILL_HEADINGS.filter((heading) => !content.includes(heading));",
    "      add(checks, `skill module headings: ${skill.id}`, missingHeadings.length === 0, { missingHeadings });",
    "    }",
    "  }",
    "  const missingEvidence = [];",
    "  const presentEvidence = [];",
    "  const compatibleManual = compatibleManualOpenCheck(targetRoot);",
    "  for (const step of Array.isArray(system.workflow) ? system.workflow : []) {",
    "    for (const evidence of Array.isArray(step.required_evidence) ? step.required_evidence : []) {",
    "      if (evidence === \"manual_powerpoint_open_check\") {",
    "        if (compatibleManual.pass) presentEvidence.push({ stage: step.stage, evidence: COMPATIBLE_NPM_MANUAL_OPEN_CHECK, satisfies: evidence, manual: true, result: compatibleManual.result, freshness: compatibleManual.freshness });",
    "        else missingEvidence.push({ stage: step.stage, evidence, manual: true, compatible_manual_open_check: compatibleManual });",
    "      }",
    "      else if (exists(targetRoot, evidence)) presentEvidence.push({ stage: step.stage, evidence });",
    "      else missingEvidence.push({ stage: step.stage, evidence, manual: Boolean(step.manual_gate) });",
    "    }",
    "  }",
    "  const packagePath = path.join(targetRoot, \"package.json\");",
    "  if (fs.existsSync(packagePath)) {",
    "    try {",
    "      const pkg = readJson(packagePath);",
    "      if (!pkg.scripts || !pkg.scripts[\"agent-system:check\"]) recommendations.push(\"Add package script: agent-system:check -> node authoring_agent_system.js\");",
    "    } catch (error) {",
    "      recommendations.push(`package.json exists but could not be parsed: ${error.message}`);",
    "    }",
    "  }",
    "  return writeAudit(targetRoot, checks, recommendations, presentEvidence, missingEvidence);",
    "}",
    "",
    "function writeAudit(targetRoot, checks, recommendations, presentEvidence, missingEvidence) {",
    "  const failed = checks.filter((check) => check.status === \"fail\");",
    "  const releaseReadiness = failed.length > 0 ? \"blocked_structure\" : (missingEvidence.length > 0 ? \"blocked_missing_project_or_manual_evidence\" : \"candidate_pending_native_release_review\");",
    "  const audit = {",
    "    schema_version: \"1.1-portable-audit\",",
    "    generated_at: new Date().toISOString(),",
    "    target_root: targetRoot,",
    "    status: failed.length === 0 ? \"pass\" : \"fail\",",
    "    passed: checks.length - failed.length,",
    "    failed: failed.length,",
    "    release_readiness: releaseReadiness,",
    "    checks,",
    "    evidence_summary: { present: presentEvidence, missing_or_manual: missingEvidence },",
    "    recommendations",
    "  };",
    "  try { fs.writeFileSync(path.join(targetRoot, \"authoring-agent-system-audit.json\"), JSON.stringify(audit, null, 2) + \"\\n\"); } catch (error) { audit.write_error = error.message; }",
    "  return audit;",
    "}",
    "",
    "const result = check(process.argv[2] || __dirname);",
    "console.log(`status=${result.status}`);",
    "console.log(`passed=${result.passed}`);",
    "console.log(`failed=${result.failed}`);",
    "console.log(`release_readiness=${result.release_readiness}`);",
    "console.log(`audit=${path.join(result.target_root, \"authoring-agent-system-audit.json\")}`);",
    "process.exit(result.status === \"pass\" ? 0 : 1);",
    ""
  ];
  return lines.join("\n");
}

function scaffoldTarget(targetRoot, options = {}) {
  const root = path.resolve(targetRoot);
  const force = Boolean(options.force);
  const projectName = options.name || path.basename(root);
  const writes = [];
  const skipped = [];
  fs.mkdirSync(root, { recursive: true });

  writeFile(root, "authoring-agent-system.json", JSON.stringify(createArchitecture(projectName), null, 2) + "\n", force, writes, skipped);
  writeFile(root, "authoring_agent_system.js", createGeneratedCheckerSource(), force, writes, skipped, 0o755);
  writeFile(root, "agent-system/README.md", createReadme(), force, writes, skipped);

  for (const def of SKILL_MODULE_DEFINITIONS) {
    writeFile(root, `agent-system/skills/${def.dir}/SKILL.md`, createSkillModule(def), force, writes, skipped);
  }

  return {
    target_root: root,
    written: writes,
    skipped,
    force
  };
}

function writeFile(root, relPath, content, force, writes, skipped, mode) {
  const file = path.join(root, relPath);
  fs.mkdirSync(path.dirname(file), { recursive: true });
  if (fs.existsSync(file) && !force) {
    skipped.push(relPath);
    return;
  }
  fs.writeFileSync(file, content);
  if (mode) {
    try {
      fs.chmodSync(file, mode);
    } catch (_error) {
      // chmod is best effort for copied workspaces.
    }
  }
  writes.push(relPath);
}

function readJson(file) {
  return JSON.parse(fs.readFileSync(file, "utf8"));
}

function exists(root, relPath) {
  return fs.existsSync(path.join(root, relPath));
}

function compatibleManualOpenCheck(root) {
  const manualPath = path.join(root, COMPATIBLE_NPM_MANUAL_OPEN_CHECK);
  const pptxPath = path.join(root, COMPATIBLE_NPM_BUILD_OUTPUT);
  if (!fs.existsSync(manualPath)) {
    return { pass: false, reason: "missing_compatible_manual_open_check", path: COMPATIBLE_NPM_MANUAL_OPEN_CHECK };
  }
  try {
    const manual = readJson(manualPath);
    const resultOk = manual.result === "no_recovery_dialog";
    const pptxExists = fs.existsSync(pptxPath);
    const manualMtime = fs.statSync(manualPath).mtimeMs;
    const pptxMtime = pptxExists ? fs.statSync(pptxPath).mtimeMs : null;
    const freshnessOk = pptxExists && manualMtime >= pptxMtime;
    return {
      pass: resultOk && freshnessOk,
      path: COMPATIBLE_NPM_MANUAL_OPEN_CHECK,
      result: manual.result || null,
      pptx_path: COMPATIBLE_NPM_BUILD_OUTPUT,
      freshness: freshnessOk ? "manual_check_newer_or_equal_to_pptx" : "manual_check_missing_or_older_than_pptx"
    };
  } catch (error) {
    return { pass: false, reason: "invalid_compatible_manual_open_check", path: COMPATIBLE_NPM_MANUAL_OPEN_CHECK, message: error.message };
  }
}

function ids(list) {
  return new Set(Array.isArray(list) ? list.map((item) => item && item.id).filter(Boolean) : []);
}

function stages(list) {
  return new Set(Array.isArray(list) ? list.map((item) => item && item.stage).filter(Boolean) : []);
}

function addCheck(checks, name, pass, details) {
  checks.push({ name, status: pass ? "pass" : "fail", details });
}

function checkRequiredSet(checks, name, required, actualSet) {
  const missing = required.filter((id) => !actualSet.has(id));
  addCheck(checks, name, missing.length === 0, { missing });
}

function listSet(value) {
  return new Set(Array.isArray(value) ? value.filter(Boolean) : []);
}

function stageIndex(workflow, stage) {
  return workflow.findIndex((item) => item && item.stage === stage);
}

function checkStageOrder(checks, workflow, name, before, after) {
  const beforeIndex = stageIndex(workflow, before);
  const afterIndex = stageIndex(workflow, after);
  addCheck(checks, name, beforeIndex >= 0 && afterIndex >= 0 && beforeIndex < afterIndex, {
    before,
    after,
    beforeIndex,
    afterIndex
  });
}

function checkWorkflowOrderContract(checks, system) {
  const workflow = Array.isArray(system.workflow) ? system.workflow : [];
  const expected = REQUIRED_WORKFLOW_STAGES;
  const actual = workflow.map((item) => item && item.stage).filter(Boolean);
  const mismatch = [];
  for (let index = 0; index < expected.length; index += 1) {
    if (actual[index] !== expected[index]) {
      mismatch.push({ index, expected: expected[index], actual: actual[index] || null });
    }
  }
  addCheck(checks, "fixed workflow stage order", mismatch.length === 0, { mismatch, actual });
  checkStageOrder(checks, workflow, "course flow precedes slide planning", "course-flow-map", "slide-planning-map");
  checkStageOrder(checks, workflow, "slide planning precedes symbol inventory", "slide-planning-map", "symbol-inventory");
  checkStageOrder(checks, workflow, "symbol inventory precedes semantic design system", "symbol-inventory", "semantic-design-system");
  checkStageOrder(checks, workflow, "semantic design system precedes semantic staging", "semantic-design-system", "semantic-staging-design-gate");
  checkStageOrder(checks, workflow, "semantic design system precedes image-first visualization", "semantic-design-system", "image-first-visualization-gate");
  checkStageOrder(checks, workflow, "semantic design system precedes PPTX build", "semantic-design-system", "new-pptx-native-build");
  checkStageOrder(checks, workflow, "semantic staging precedes image-first visualization", "semantic-staging-design-gate", "image-first-visualization-gate");
  checkStageOrder(checks, workflow, "image-first visualization precedes open visualization planning", "image-first-visualization-gate", "open-visualization-planning");
  checkStageOrder(checks, workflow, "image-first visualization precedes PPTX build", "image-first-visualization-gate", "new-pptx-native-build");
  checkStageOrder(checks, workflow, "open visualization planning precedes PPTX build", "open-visualization-planning", "new-pptx-native-build");
}

function checkCognitiveAuthoringContract(checks, system) {
  const packet = system.cognitive_authoring_packet || {};
  addCheck(checks, "cognitive authoring process lock", packet.process_lock === "cognitive-document-visual-authoring-v1", {
    actual: packet.process_lock || null
  });
  checkRequiredSet(checks, "authoring packet required fields", REQUIRED_AUTHORING_PACKET_FIELDS, listSet(packet.required_fields));
  checkRequiredSet(checks, "visual value required fields", REQUIRED_VISUAL_VALUE_FIELDS, listSet(packet.visual_value_required_fields));
  checkRequiredSet(checks, "readability fit required fields", REQUIRED_READABILITY_FIT_FIELDS, listSet(packet.readability_fit_required_fields));

  const workflow = Array.isArray(system.workflow) ? system.workflow : [];
  const cognitiveIndex = workflow.findIndex((item) => item && item.stage === "cognitive-authoring-packet");
  const writingIndex = workflow.findIndex((item) => item && item.stage === "writing-flow");
  const visualizationIndex = workflow.findIndex((item) => item && item.stage === "open-visualization-planning");
  addCheck(checks, "cognitive authoring precedes writing", cognitiveIndex >= 0 && writingIndex >= 0 && cognitiveIndex < writingIndex, {
    cognitiveIndex,
    writingIndex
  });
  addCheck(checks, "cognitive authoring precedes visualization", cognitiveIndex >= 0 && visualizationIndex >= 0 && cognitiveIndex < visualizationIndex, {
    cognitiveIndex,
    visualizationIndex
  });
}

function checkOutlineNoteContract(checks, system) {
  const contract = system.outline_note_contract || {};
  checkRequiredSet(checks, "outline note required fields", REQUIRED_OUTLINE_NOTE_FIELDS, listSet(contract.required_fields));
  addCheck(checks, "outline note rule", Boolean(contract.rule), {
    rule: contract.rule || null
  });

  const workflow = Array.isArray(system.workflow) ? system.workflow : [];
  const writingIndex = workflow.findIndex((item) => item && item.stage === "writing-flow");
  const outlineIndex = workflow.findIndex((item) => item && item.stage === "outline-note-gate");
  const storylineIndex = workflow.findIndex((item) => item && item.stage === "storyline-readability-gate");
  const visualizationIndex = workflow.findIndex((item) => item && item.stage === "open-visualization-planning");
  const pptxIndex = workflow.findIndex((item) => item && item.stage === "new-pptx-native-build");
  addCheck(checks, "outline notes follow writing", writingIndex >= 0 && outlineIndex >= 0 && writingIndex <= outlineIndex, {
    writingIndex,
    outlineIndex
  });
  addCheck(checks, "outline notes precede storyline", outlineIndex >= 0 && storylineIndex >= 0 && outlineIndex < storylineIndex, {
    outlineIndex,
    storylineIndex
  });
  addCheck(checks, "outline notes precede visualization", outlineIndex >= 0 && visualizationIndex >= 0 && outlineIndex < visualizationIndex, {
    outlineIndex,
    visualizationIndex
  });
  addCheck(checks, "outline notes precede PPTX build", outlineIndex >= 0 && pptxIndex >= 0 && outlineIndex < pptxIndex, {
    outlineIndex,
    pptxIndex
  });
  const pptxStep = workflow.find((item) => item && item.stage === "new-pptx-native-build") || {};
  const pptxEvidence = listSet(pptxStep.required_evidence);
  addCheck(checks, "PPTX build requires outline notes", pptxEvidence.has("outline-notes.md"), {
    required_evidence: Array.from(pptxEvidence)
  });
}

function checkWorkingSourceContract(checks, system) {
  const contract = system.working_source_contract || {};
  checkRequiredSet(checks, "working source clarification fields", REQUIRED_CLARIFICATION_FIELDS, listSet(contract.required_fields));

  const conflict = system.conflict_resolution || {};
  addCheck(checks, "conflict resolution priority order", Array.isArray(conflict.priority_order) && conflict.priority_order.length >= 4 && Boolean(conflict.rule), {
    priority_count: Array.isArray(conflict.priority_order) ? conflict.priority_order.length : 0,
    has_rule: Boolean(conflict.rule)
  });

  const threeLayer = system.three_layer_contract || {};
  checkRequiredSet(checks, "three-layer classification fields", REQUIRED_THREE_LAYER_FIELDS, listSet(threeLayer.required_fields));
  addCheck(checks, "three-layer drift rule", Boolean(threeLayer.drift_rule), {
    drift_rule: threeLayer.drift_rule || null
  });
  addCheck(checks, "fixed decisions declared", Array.isArray(threeLayer.fixed) && threeLayer.fixed.length >= 3, {
    fixed: threeLayer.fixed || []
  });
  addCheck(checks, "flexible decisions declared", Array.isArray(threeLayer.flexible) && threeLayer.flexible.length >= 3, {
    flexible: threeLayer.flexible || []
  });
  addCheck(checks, "decisional decisions declared", Array.isArray(threeLayer.decisional) && threeLayer.decisional.length >= 3, {
    decisional: threeLayer.decisional || []
  });
  const intentional = system.intentional_implementation_contract || {};
  checkRequiredSet(checks, "intentional implementation fields", REQUIRED_INTENTIONAL_IMPLEMENTATION_FIELDS, listSet(intentional.required_fields));
  checkRequiredSet(checks, "calculated value fields", REQUIRED_CALCULATED_VALUE_FIELDS, listSet(intentional.calculated_value_required_fields));
  addCheck(checks, "intentional implementation rules", Boolean(intentional.fixed_rule && intentional.flexible_rule && intentional.decisional_rule && intentional.implementation_rule), {
    has_fixed_rule: Boolean(intentional.fixed_rule),
    has_flexible_rule: Boolean(intentional.flexible_rule),
    has_decisional_rule: Boolean(intentional.decisional_rule),
    has_implementation_rule: Boolean(intentional.implementation_rule)
  });

  const workflow = Array.isArray(system.workflow) ? system.workflow : [];
  const sourceIndex = workflow.findIndex((item) => item && item.stage === "working-source-clarification");
  const cognitiveIndex = workflow.findIndex((item) => item && item.stage === "cognitive-authoring-packet");
  addCheck(checks, "working source precedes cognitive authoring", sourceIndex >= 0 && cognitiveIndex >= 0 && sourceIndex < cognitiveIndex, {
    sourceIndex,
    cognitiveIndex
  });
}

function checkCourseFlowToDesignSystemContract(checks, system) {
  const contract = system.course_flow_to_design_system_contract || {};
  const sequence = Array.isArray(contract.sequence_lock) ? contract.sequence_lock : [];
  const expectedSequence = ["course-flow-map", "slide-planning-map", "symbol-inventory", "semantic-design-system"];
  const sequenceMismatch = expectedSequence.filter((stage, index) => sequence[index] !== stage);
  addCheck(checks, "course flow to design system sequence lock", sequenceMismatch.length === 0, {
    expected: expectedSequence,
    actual: sequence,
    mismatch: sequenceMismatch
  });
  addCheck(checks, "course flow design-start rule", Boolean(contract.rule) && /First map the whole lecture flow/i.test(contract.rule), {
    rule: contract.rule || null
  });
  const files = contract.required_files || {};
  addCheck(
    checks,
    "course flow required files declared",
    files.course_flow_map === "course-flow-map.md" &&
      files.slide_planning_map === "slide-planning-map.json" &&
      files.symbol_inventory === "symbol-inventory.json" &&
      files.semantic_design_system === "semantic-design-system.json",
    { required_files: files }
  );
  checkRequiredSet(checks, "course flow required fields", REQUIRED_COURSE_FLOW_FIELDS, listSet(contract.course_flow_required_fields));
  checkRequiredSet(checks, "slide planning required fields", REQUIRED_SLIDE_PLANNING_FIELDS, listSet(contract.slide_planning_required_fields));
  checkRequiredSet(checks, "symbol inventory required fields", REQUIRED_SYMBOL_INVENTORY_FIELDS, listSet(contract.symbol_inventory_required_fields));
  checkRequiredSet(checks, "semantic design system required fields", REQUIRED_SEMANTIC_DESIGN_SYSTEM_FIELDS, listSet(contract.semantic_design_system_required_fields));
  checkRequiredSet(checks, "layout element calculation fields", REQUIRED_LAYOUT_ELEMENT_CALCULATION_FIELDS, listSet(contract.layout_element_calculation_required_fields));
  addCheck(
    checks,
    "design start boundary",
    /course-flow-map\.md/i.test(contract.design_start_boundary || "") &&
      /slide-planning-map\.json/i.test(contract.design_start_boundary || "") &&
      /symbol-inventory\.json/i.test(contract.design_start_boundary || ""),
    { design_start_boundary: contract.design_start_boundary || null }
  );
  addCheck(checks, "learner-facing boundary", /Internal file paths/i.test(contract.learner_facing_boundary || "") && /learner-facing/i.test(contract.learner_facing_boundary || ""), {
    learner_facing_boundary: contract.learner_facing_boundary || null
  });

  const workflow = Array.isArray(system.workflow) ? system.workflow : [];
  const courseStep = workflow.find((item) => item && item.stage === "course-flow-map") || {};
  const slideStep = workflow.find((item) => item && item.stage === "slide-planning-map") || {};
  const symbolStep = workflow.find((item) => item && item.stage === "symbol-inventory") || {};
  const designStep = workflow.find((item) => item && item.stage === "semantic-design-system") || {};
  const pptxStep = workflow.find((item) => item && item.stage === "new-pptx-native-build") || {};
  const courseEvidence = listSet(courseStep.required_evidence);
  const slideEvidence = listSet(slideStep.required_evidence);
  const symbolEvidence = listSet(symbolStep.required_evidence);
  const designEvidence = listSet(designStep.required_evidence);
  const pptxEvidence = listSet(pptxStep.required_evidence);
  addCheck(checks, "course stage requires course-flow-map", courseEvidence.has("course-flow-map.md"), {
    required_evidence: Array.from(courseEvidence)
  });
  addCheck(checks, "slide planning stage requires slide-planning-map", slideEvidence.has("slide-planning-map.json"), {
    required_evidence: Array.from(slideEvidence)
  });
  addCheck(checks, "symbol stage requires symbol-inventory", symbolEvidence.has("symbol-inventory.json"), {
    required_evidence: Array.from(symbolEvidence)
  });
  addCheck(
    checks,
    "semantic design stage requires upstream maps",
    ["course-flow-map.md", "slide-planning-map.json", "symbol-inventory.json", "semantic-design-system.json"].every((item) => designEvidence.has(item)),
    { required_evidence: Array.from(designEvidence) }
  );
  addCheck(
    checks,
    "PPTX build requires planning and design maps",
    ["slide-planning-map.json", "symbol-inventory.json", "semantic-design-system.json"].every((item) => pptxEvidence.has(item)),
    { required_evidence: Array.from(pptxEvidence) }
  );
}

function checkSessionFeedbackContract(checks, system) {
  const gate = system.session_feedback_pattern_gate || {};
  checkRequiredSet(checks, "session feedback checks", REQUIRED_SESSION_FEEDBACK_CHECKS, listSet(gate.required_checks));
  addCheck(checks, "session feedback rule", Boolean(gate.rule), {
    rule: gate.rule || null
  });

  const workflow = Array.isArray(system.workflow) ? system.workflow : [];
  const storylineIndex = workflow.findIndex((item) => item && item.stage === "storyline-readability-gate");
  const feedbackIndex = workflow.findIndex((item) => item && item.stage === "session-feedback-pattern-gate");
  const visualizationIndex = workflow.findIndex((item) => item && item.stage === "open-visualization-planning");
  addCheck(checks, "session feedback follows storyline", storylineIndex >= 0 && feedbackIndex >= 0 && storylineIndex < feedbackIndex, {
    storylineIndex,
    feedbackIndex
  });
  addCheck(checks, "session feedback precedes visualization", feedbackIndex >= 0 && visualizationIndex >= 0 && feedbackIndex < visualizationIndex, {
    feedbackIndex,
    visualizationIndex
  });
}

function checkSemanticStagingContract(checks, system) {
  const framework = system.semantic_staging_design_framework || {};
  checkRequiredSet(checks, "semantic staging design fields", REQUIRED_STAGING_DESIGN_FIELDS, listSet(framework.required_fields));
  addCheck(checks, "semantic staging rule", Boolean(framework.rule), {
    rule: framework.rule || null
  });
  addCheck(checks, "design freedom boundary", /optional|unless|constraint|unconstrained/i.test(framework.freedom_boundary || ""), {
    freedom_boundary: framework.freedom_boundary || null
  });

  const workflow = Array.isArray(system.workflow) ? system.workflow : [];
  const feedbackIndex = workflow.findIndex((item) => item && item.stage === "session-feedback-pattern-gate");
  const stagingIndex = workflow.findIndex((item) => item && item.stage === "semantic-staging-design-gate");
  const visualizationIndex = workflow.findIndex((item) => item && item.stage === "open-visualization-planning");
  const pptxIndex = workflow.findIndex((item) => item && item.stage === "new-pptx-native-build");
  addCheck(checks, "semantic staging follows session feedback", feedbackIndex >= 0 && stagingIndex >= 0 && feedbackIndex < stagingIndex, {
    feedbackIndex,
    stagingIndex
  });
  addCheck(checks, "semantic staging precedes visualization", stagingIndex >= 0 && visualizationIndex >= 0 && stagingIndex < visualizationIndex, {
    stagingIndex,
    visualizationIndex
  });
  addCheck(checks, "semantic staging precedes PPTX build", stagingIndex >= 0 && pptxIndex >= 0 && stagingIndex < pptxIndex, {
    stagingIndex,
    pptxIndex
  });

  const visualizationStep = workflow.find((item) => item && item.stage === "open-visualization-planning") || {};
  const pptxStep = workflow.find((item) => item && item.stage === "new-pptx-native-build") || {};
  const visualizationEvidence = listSet(visualizationStep.required_evidence);
  const pptxEvidence = listSet(pptxStep.required_evidence);
  addCheck(checks, "visualization requires staging brief", visualizationEvidence.has("staging-design-brief.json"), {
    required_evidence: Array.from(visualizationEvidence)
  });
  addCheck(checks, "PPTX build requires staging brief", pptxEvidence.has("staging-design-brief.json"), {
    required_evidence: Array.from(pptxEvidence)
  });
}

function checkImageFirstVisualizationContract(checks, system) {
  const framework = system.image_first_visualization_framework || {};
  checkRequiredSet(checks, "image-first visualization fields", REQUIRED_IMAGE_FIRST_VISUALIZATION_FIELDS, listSet(framework.required_fields));
  addCheck(checks, "image-first visualization rule", Boolean(framework.rule), {
    rule: framework.rule || null
  });
  addCheck(checks, "VLPP expression-distance boundary", /distance/i.test(framework.vlpp_boundary || "") && /psychology|comprehension|persuasion|retention|behavior/i.test(framework.vlpp_boundary || ""), {
    vlpp_boundary: framework.vlpp_boundary || null
  });
  addCheck(checks, "VLPP observed computation evidence state", framework.evidence_state_required === "observed_computation", {
    evidence_state_required: framework.evidence_state_required || null
  });

  const workflow = Array.isArray(system.workflow) ? system.workflow : [];
  checkStageOrder(checks, workflow, "image-first follows semantic staging", "semantic-staging-design-gate", "image-first-visualization-gate");
  checkStageOrder(checks, workflow, "image-first precedes open visualization", "image-first-visualization-gate", "open-visualization-planning");
  checkStageOrder(checks, workflow, "image-first precedes native PPTX build", "image-first-visualization-gate", "new-pptx-native-build");

  const imageStep = workflow.find((item) => item && item.stage === "image-first-visualization-gate") || {};
  const imageEvidence = listSet(imageStep.required_evidence);
  const hasImageEvidence = (name) => Array.from(imageEvidence).some((item) => item === name || item.endsWith("/" + name));
  addCheck(checks, "image-first gate requires packet", hasImageEvidence("image-first-visualization-packet.json"), {
    required_evidence: Array.from(imageEvidence)
  });
  addCheck(checks, "image-first gate requires contact sheet", hasImageEvidence("visual-candidate-contact-sheet.png"), {
    required_evidence: Array.from(imageEvidence)
  });
  addCheck(checks, "image-first gate requires VLPP monitor", hasImageEvidence("vlpp-expression-distance-monitor.json"), {
    required_evidence: Array.from(imageEvidence)
  });
}

function checkArtifactSurfaceContract(checks, system) {
  const gate = system.artifact_surface_separation || {};
  checkRequiredSet(checks, "artifact surfaces", REQUIRED_ARTIFACT_SURFACES, listSet(gate.required_surfaces));
  addCheck(checks, "artifact surface rule", Boolean(gate.rule), {
    rule: gate.rule || null
  });

  const workflow = Array.isArray(system.workflow) ? system.workflow : [];
  const pptxIndex = workflow.findIndex((item) => item && item.stage === "new-pptx-native-build");
  const surfaceIndex = workflow.findIndex((item) => item && item.stage === "artifact-surface-separation");
  const closeoutIndex = workflow.findIndex((item) => item && item.stage === "representative-closeout");
  addCheck(checks, "artifact surface follows PPTX build", pptxIndex >= 0 && surfaceIndex >= 0 && pptxIndex < surfaceIndex, {
    pptxIndex,
    surfaceIndex
  });
  addCheck(checks, "artifact surface precedes closeout", surfaceIndex >= 0 && closeoutIndex >= 0 && surfaceIndex < closeoutIndex, {
    surfaceIndex,
    closeoutIndex
  });
}

function checkRoutingExperimentContract(checks, system) {
  const routing = system.routing_experiments || {};
  checkRequiredSet(checks, "routing experiment fields", REQUIRED_ROUTING_EXPERIMENT_FIELDS, listSet(routing.required_fields));
  addCheck(checks, "routing experiment positive and negative cases", Array.isArray(routing.should_trigger) && routing.should_trigger.length >= 2 && Array.isArray(routing.should_not_trigger) && routing.should_not_trigger.length >= 2, {
    should_trigger: Array.isArray(routing.should_trigger) ? routing.should_trigger.length : 0,
    should_not_trigger: Array.isArray(routing.should_not_trigger) ? routing.should_not_trigger.length : 0
  });
  addCheck(checks, "routing experiment expected behavior", Boolean(routing.expected_behavior), {
    expected_behavior: routing.expected_behavior || null
  });
}

function checkCompatibleNpmProcessContract(checks, system) {
  const process = system.compatible_npm_authoring_process || {};
  addCheck(checks, "compatible npm authoring process declared", Boolean(process.init_command && process.run_command && process.build_command), {
    init_command: process.init_command || null,
    run_command: process.run_command || null,
    build_command: process.build_command || null
  });

  const stateOutputs = listSet(process.state_outputs);
  checkRequiredSet(checks, "compatible npm state outputs declared", COMPATIBLE_NPM_STATE_OUTPUTS, stateOutputs);
  addCheck(checks, "compatible npm PPTX output declared", process.build_output === COMPATIBLE_NPM_BUILD_OUTPUT, {
    expected: COMPATIBLE_NPM_BUILD_OUTPUT,
    actual: process.build_output || null
  });

  const manual = process.manual_open_check || {};
  addCheck(checks, "compatible npm manual open gate declared", manual.path === COMPATIBLE_NPM_MANUAL_OPEN_CHECK && manual.required_result === "no_recovery_dialog" && /newer/i.test(manual.freshness_rule || ""), {
    manual_open_check: manual
  });

  const statuses = listSet(process.accepted_release_statuses);
  checkRequiredSet(checks, "compatible npm accepted release statuses declared", COMPATIBLE_NPM_ACCEPTED_RELEASE_STATUSES, statuses);
  addCheck(checks, "compatible npm rebuild warning declared", /npm test/i.test(process.rebuild_warning || "") && /build/i.test(process.rebuild_warning || "") && /open check|PowerPoint/i.test(process.rebuild_warning || ""), {
    rebuild_warning: process.rebuild_warning || null
  });

  const toolSet = ids(system.tools);
  checkRequiredSet(checks, "compatible npm command tools declared", [
    "system-init",
    "system-run",
    "pptx-build",
    "presentationml-spec-check",
    "research-build",
    "research-check",
    "native-powerpoint-check",
    "recovery-compare-check",
    "repetition-gate-check",
    "release-check",
    "agent-system-check",
    "manual-powerpoint-open-check"
  ], toolSet);

  const workflow = Array.isArray(system.workflow) ? system.workflow : [];
  const pptxStep = workflow.find((item) => item && item.stage === "new-pptx-native-build") || {};
  const pptxEvidence = listSet(pptxStep.required_evidence);
  const missingPptxEvidence = COMPATIBLE_NPM_STATE_OUTPUTS.concat([COMPATIBLE_NPM_BUILD_OUTPUT]).filter((item) => !pptxEvidence.has(item));
  addCheck(checks, "compatible npm build evidence routed", missingPptxEvidence.length === 0, {
    missing: missingPptxEvidence,
    required_evidence: Array.from(pptxEvidence)
  });

  const openStep = workflow.find((item) => item && item.stage === "powerpoint-open-check") || {};
  const openEvidence = listSet(openStep.required_evidence);
  addCheck(checks, "compatible npm manual open evidence routed", openEvidence.has(COMPATIBLE_NPM_MANUAL_OPEN_CHECK), {
    required_evidence: Array.from(openEvidence),
    expected: COMPATIBLE_NPM_MANUAL_OPEN_CHECK
  });
}

function checkTarget(targetRoot, options = {}) {
  const root = path.resolve(targetRoot);
  const checks = [];
  const recommendations = [];
  const systemPath = path.join(root, "authoring-agent-system.json");

  if (!fs.existsSync(systemPath)) {
    addCheck(checks, "system file exists", false, { path: systemPath });
    return writeAudit(root, checks, recommendations, [], [], options.writeAudit !== false);
  }

  let system;
  try {
    system = readJson(systemPath);
    addCheck(checks, "system JSON parses", true, { path: systemPath });
  } catch (error) {
    addCheck(checks, "system JSON parses", false, { message: error.message });
    return writeAudit(root, checks, recommendations, [], [], options.writeAudit !== false);
  }

  addCheck(checks, "system id", system.system_id === SYSTEM_ID, { expected: SYSTEM_ID, actual: system.system_id });
  addCheck(
    checks,
    "claim boundary separates structural and release readiness",
    /structural|local computational|agent-system/i.test(system.claim_boundary || "") && /release/i.test(system.claim_boundary || ""),
    { claim_boundary: system.claim_boundary || null }
  );
  const runtimeStatus = system.runtime_compatibility && system.runtime_compatibility.status;
  addCheck(checks, "runtime compatibility status", RUNTIME_COMPATIBILITY_STATUSES.has(runtimeStatus), {
    actual: runtimeStatus,
    allowed: Array.from(RUNTIME_COMPATIBILITY_STATUSES)
  });

  checkRequiredSet(checks, "required agents", REQUIRED_AGENTS, ids(system.agents));
  checkRequiredSet(checks, "required skills", REQUIRED_SKILLS.map((item) => item.id), ids(system.skills));
  checkRequiredSet(checks, "required tools", REQUIRED_TOOLS, ids(system.tools));
  checkRequiredSet(checks, "required workflow stages", REQUIRED_WORKFLOW_STAGES, stages(system.workflow));
  checkRequiredSet(checks, "required release gates", REQUIRED_RELEASE_GATES, ids(system.release_gates));
  checkWorkflowOrderContract(checks, system);
  checkWorkingSourceContract(checks, system);
  checkCourseFlowToDesignSystemContract(checks, system);
  checkCognitiveAuthoringContract(checks, system);
  checkOutlineNoteContract(checks, system);
  checkSessionFeedbackContract(checks, system);
  checkSemanticStagingContract(checks, system);
  checkImageFirstVisualizationContract(checks, system);
  checkArtifactSurfaceContract(checks, system);
  checkRoutingExperimentContract(checks, system);
  checkCompatibleNpmProcessContract(checks, system);

  const manualGate = Array.isArray(system.workflow) && system.workflow.some((item) => item && item.stage === "powerpoint-open-check" && item.manual_gate === true);
  addCheck(checks, "manual PowerPoint gate", manualGate, { required_stage: "powerpoint-open-check" });

  for (const skill of REQUIRED_SKILLS) {
    const file = path.join(root, skill.path);
    const present = fs.existsSync(file);
    addCheck(checks, `skill module exists: ${skill.id}`, present, { path: skill.path });
    if (present) {
      const content = fs.readFileSync(file, "utf8");
      const missingHeadings = REQUIRED_SKILL_HEADINGS.filter((heading) => !content.includes(heading));
      addCheck(checks, `skill module headings: ${skill.id}`, missingHeadings.length === 0, { missingHeadings });
    }
  }

  const missingEvidence = [];
  const presentEvidence = [];
  const compatibleManual = compatibleManualOpenCheck(root);
  for (const step of Array.isArray(system.workflow) ? system.workflow : []) {
    for (const evidence of Array.isArray(step.required_evidence) ? step.required_evidence : []) {
      if (evidence === "manual_powerpoint_open_check") {
        if (compatibleManual.pass) {
          presentEvidence.push({
            stage: step.stage,
            evidence: COMPATIBLE_NPM_MANUAL_OPEN_CHECK,
            satisfies: evidence,
            manual: true,
            result: compatibleManual.result,
            freshness: compatibleManual.freshness
          });
        } else {
          missingEvidence.push({ stage: step.stage, evidence, manual: true, compatible_manual_open_check: compatibleManual });
        }
      } else if (exists(root, evidence)) {
        presentEvidence.push({ stage: step.stage, evidence });
      } else {
        missingEvidence.push({ stage: step.stage, evidence, manual: Boolean(step.manual_gate) });
      }
    }
  }

  const packagePath = path.join(root, "package.json");
  if (fs.existsSync(packagePath)) {
    try {
      const pkg = readJson(packagePath);
      if (!pkg.scripts || !pkg.scripts["agent-system:check"]) {
        recommendations.push("Add package script: agent-system:check -> node authoring_agent_system.js");
      }
    } catch (error) {
      recommendations.push(`package.json exists but could not be parsed: ${error.message}`);
    }
  }

  return writeAudit(root, checks, recommendations, presentEvidence, missingEvidence, options.writeAudit !== false);
}

function writeAudit(root, checks, recommendations, presentEvidence, missingEvidence, shouldWrite) {
  const failed = checks.filter((check) => check.status === "fail");
  const releaseReadiness = failed.length > 0
    ? "blocked_structure"
    : (missingEvidence.length > 0 ? "blocked_missing_project_or_manual_evidence" : "candidate_pending_native_release_review");
  const audit = {
    schema_version: "1.1-portable-audit",
    generated_at: new Date().toISOString(),
    target_root: root,
    status: failed.length === 0 ? "pass" : "fail",
    passed: checks.length - failed.length,
    failed: failed.length,
    release_readiness: releaseReadiness,
    checks,
    evidence_summary: {
      present: presentEvidence,
      missing_or_manual: missingEvidence
    },
    recommendations
  };
  if (shouldWrite) {
    try {
      fs.writeFileSync(path.join(root, "authoring-agent-system-audit.json"), JSON.stringify(audit, null, 2) + "\n");
    } catch (error) {
      audit.write_error = error.message;
    }
  }
  return audit;
}

function selfcheck() {
  const skillRoot = path.resolve(__dirname, "..");
  const checks = [];
  const references = [
    "references/glossary.md",
    "references/concept-map.md",
    "references/cognitive-authoring-process.md",
    "references/course-flow-to-design-system-sequence.md",
    "references/pptx-standard-xml-generation.md",
    "references/session-feedback-and-surface-gates.md",
    "references/semantic-staging-design-framework.md",
    "references/source-notes.md",
    "references/slide-authoring-methods.md"
  ];

  addCheck(checks, "SKILL.md exists", fs.existsSync(path.join(skillRoot, "SKILL.md")), { path: "SKILL.md" });
  addCheck(checks, "script exists", fs.existsSync(__filename), { path: "scripts/portable_agent_system.js" });
  for (const relPath of references) {
    addCheck(checks, `reference exists: ${relPath}`, fs.existsSync(path.join(skillRoot, relPath)), { path: relPath });
  }

  const tmpRoot = fs.mkdtempSync(path.join(os.tmpdir(), "document-slide-authoring-agent-system-"));
  const scaffold = scaffoldTarget(tmpRoot, { force: true, name: "Selfcheck" });
  const audit = checkTarget(tmpRoot);
  addCheck(checks, "selfcheck scaffold wrote files", scaffold.written.length >= 18, { written: scaffold.written.length, target: tmpRoot });
  addCheck(checks, "selfcheck target audit passes structurally", audit.status === "pass", {
    target: tmpRoot,
    failed: audit.failed,
    release_readiness: audit.release_readiness
  });
  let localCheckerResult = { status: "pass" };
  try {
    childProcess.execFileSync(process.execPath, [path.join(tmpRoot, "authoring_agent_system.js")], {
      cwd: path.dirname(tmpRoot),
      encoding: "utf8",
      stdio: "pipe"
    });
  } catch (error) {
    localCheckerResult = {
      status: "fail",
      message: error.message,
      stdout: error.stdout ? String(error.stdout) : "",
      stderr: error.stderr ? String(error.stderr) : ""
    };
  }
  addCheck(checks, "generated local checker runs from outside target root", localCheckerResult.status === "pass", {
    target: tmpRoot,
    error: localCheckerResult.status === "fail" ? localCheckerResult : null
  });

  const failed = checks.filter((check) => check.status === "fail");
  return {
    status: failed.length === 0 ? "pass" : "fail",
    passed: checks.length - failed.length,
    failed: failed.length,
    skill_root: skillRoot,
    scaffold_target: tmpRoot,
    target_audit: path.join(tmpRoot, "authoring-agent-system-audit.json"),
    checks
  };
}

function usage() {
  return [
    "Usage:",
    "  node portable_agent_system.js scaffold <targetRoot> [--force] [--name <projectName>]",
    "  node portable_agent_system.js check <targetRoot>",
    "  node portable_agent_system.js selfcheck",
    ""
  ].join("\n");
}

function parseCli(argv) {
  const [command, targetRoot, ...rest] = argv;
  const options = { force: rest.includes("--force") };
  const nameIndex = rest.indexOf("--name");
  if (nameIndex >= 0 && rest[nameIndex + 1]) {
    options.name = rest[nameIndex + 1];
  }
  return { command, targetRoot, options };
}

function main(argv) {
  const { command, targetRoot, options } = parseCli(argv);
  if (command === "scaffold") {
    if (!targetRoot) {
      console.error(usage());
      return 2;
    }
    const result = scaffoldTarget(targetRoot, options);
    console.log(`status=pass`);
    console.log(`target=${result.target_root}`);
    console.log(`written=${result.written.length}`);
    console.log(`skipped=${result.skipped.length}`);
    if (result.skipped.length) console.log(`skipped_files=${result.skipped.join(",")}`);
    return 0;
  }

  if (command === "check") {
    if (!targetRoot) {
      console.error(usage());
      return 2;
    }
    const result = checkTarget(targetRoot);
    console.log(`status=${result.status}`);
    console.log(`passed=${result.passed}`);
    console.log(`failed=${result.failed}`);
    console.log(`release_readiness=${result.release_readiness}`);
    console.log(`audit=${path.join(result.target_root, "authoring-agent-system-audit.json")}`);
    return result.status === "pass" ? 0 : 1;
  }

  if (command === "selfcheck") {
    const result = selfcheck();
    console.log(`status=${result.status}`);
    console.log(`passed=${result.passed}`);
    console.log(`failed=${result.failed}`);
    console.log(`skill_root=${result.skill_root}`);
    console.log(`scaffold_target=${result.scaffold_target}`);
    console.log(`target_audit=${result.target_audit}`);
    return result.status === "pass" ? 0 : 1;
  }

  console.error(usage());
  return 2;
}

if (require.main === module) {
  process.exit(main(process.argv.slice(2)));
}

module.exports = {
  createArchitecture,
  scaffoldTarget,
  checkTarget,
  selfcheck
};
