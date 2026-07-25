# Glossary — visual-authoring (통합)

## Authoring 계열 (원형: document-slide-authoring-agent-system)

# Glossary

## Representative Agent

The owner of the whole document/slide authoring workflow. It routes work to subagents, owns the visible goal and rubric, and closes with a clear readiness boundary.

## Structural Readiness

The local project has the expected agent, skill, tool, workflow, release-gate, and module files. This is a code and configuration claim.

## Working Source Of Truth

The current source set the workflow is allowed to use. It includes the goal,
scope, excluded surfaces, success condition, evidence target, runtime target,
provider provenance, and output brand. It prevents the agent from filling gaps
with convenient assumptions.

## Original Source Inventory

The explicit list of original artifacts used as the baseline for regeneration
or transfer. It names file paths or handles, version/date, artifact type, scene
or slide ids, assets, text units, native features, and read-only boundary.

## Source Decomposition

The analysis of an original artifact before implementation. It separates scene
intent, information units, visual hierarchy, reading order, text units, assets,
native features, and risks so the target artifact is not rebuilt from memory.

## Preserve / Transfer / Discard / Regenerate

The decision labels used when moving from source to target. Preserve keeps a
source element; transfer recreates it in the target medium; discard removes it
with a reason; regenerate rebuilds the intent because the original execution is
weak or out of date.

## Source Parity Evidence

The comparison record between original and regenerated artifact. It separates
matched, changed, missing, and intentional_gap rows and prevents render proof
from being mistaken for source fidelity proof. It is required for a fidelity
baseline, not for a reference benchmark.

## Reference Benchmark

A source used to observe useful visual principles, native-medium choices, or
quality signals without promising a faithful recreation. Similarity to the
benchmark is diagnostic evidence, not an improved-variant gate.

## Content-Fit Quality Hierarchy

The evaluation order that puts content, reader task, and desired action first;
then semantic relations and reading flow; then medium implementation; then
computable geometry; then render/native proof; and finally human outcome
evidence. A lower layer cannot substitute for a higher one.

## Editability Value

The judgment of whether an object is worth making native/editable. It depends
on meaning density, fit to the slide or screen job, expected future edits,
native tool support, and visual fidelity risk.

## Clarification Packet

The compact intake record created before authoring. It names what is known,
unknown, out of scope, blocked, or target-specific.

## Conflict Resolution

The priority rule used when user requests, project rules, evidence boundaries,
native tool constraints, and style preferences disagree.

## 3-Layer Classification

The split between executable fixed rules and calculations, flexible
project-specific visual generation and thresholds, and decisional judgments
that combine fixed observations with context and human evidence. A prose-only
claim that something is calculated is not Fixed.

## Visual Strategy

The content-facing choice of how to expose a relationship or task, such as a
comparison, process, timeline, data story, scene, workshop board, editorial
course sequence, or product simulation.

## Cognitive Visual Encoding

The decision record that maps a content relationship and reader task to an
inference goal, candidate visual grammars, selected grammar, visible and
suppressed cues, reading path, and explicit evidence and human-validation
boundaries. It does not itself prove comprehension or learning.

## Inference Goal

The specific relationship or conclusion the reader should be able to derive
from a visual unit, distinct from the topic it mentions.

## Visual Grammar

A spatial and directional rule for exposing a relationship, such as aligned
contrast, path, feedback loop, hierarchy, branch, matrix, or layered
decomposition. A visual grammar is not a color palette or expression system.

## Validation Boundary

The explicit separation between technical editability, semantic structure,
cognitive-readability proxies, and actual human-outcome validation. A proxy
pass cannot be promoted to a human-outcome claim.

## Expression System

An optional style tool used to make a chosen visual strategy consistent.
Carbon, Vivid, a brand system, Editorial, or Custom are expression systems;
none of them is visualization itself.

## Medium Implementation Plan

The orthogonal plan for realizing a visual strategy in PowerPoint native
objects, SVG/HTML, image, chart/table, or a hybrid. Native PowerPoint is a
medium capability, not an expression-system candidate or token namespace.

## Native Object Intent Plan

The pre-build mapping from semantic units to named PowerPoint object types,
edit boundaries, groups, z-order, reading order, geometry relations,
presentation behavior, and raster exceptions.

## Native Semantic Coverage

The proportion of eligible semantic units whose declared objects exist, match
the expected native type, and satisfy required relations. Object count alone
does not establish coverage.

## Geometry Constraint Audit

A deterministic comparison of actual object bounds and connections against
declared safe-area, separation, containment, alignment, spacing, and connector
relations. It proves geometric conformance, not good design or comprehension.

## Visual Support Convergence

The repeated process of raising the weakest content-support scene by comparing
it with a strongly supported scene, extracting the transferable meaning-support
principle, applying that principle to the weak scene and a second different
scene, and verifying implementation and judgment evidence separately. It does
not mean making every scene look alike.

## Support Floor

The weakest current state across relationship, priority, inference/action,
evidence/completion, and medium support in an artifact. Raising the support
floor reduces the low-support tail while preserving relationship-driven
silhouette differences.

## Principle Transfer

The move from `source relation -> visible cue -> reader inference or action ->
transfer condition`. Copying colors, cards, or object positions is surface
reuse, not principle transfer. A valid transfer is adapted once to the weak
scene and once to a second scene with a different relationship.

## Pattern Guard

The reusable check created from an accepted repair. A recurrence strengthens
the written gate; a recurrence after that strengthened gate promotes the check
to an executable stop condition or validator fixture.

## Observed Computation

An evidence state for values produced reproducibly from explicit inputs by
code, such as bounding boxes, overlap ratios, alignment error, spacing
deviation, object density, connector attachment, and semantic coverage.

## Cognitive Authoring Packet

A structured packet created before drafting or visual production. It fixes reader situation, cognitive task, desired action, semantic fit, evidence boundary, output route, verification surface, unfolding trace, title sequence, knowledge split, visual rationale, visual value spec, and stage-gate log.

## Outline Notes

The production note written before storyline review, visualization, or PPTX
build. It connects reader situation, deck or document purpose, section flow,
slide sequence, title story draft, visible message, spoken or facilitation
notes, evidence links, visual intent, and open questions. It is not just speaker
notes; it is the inspectable bridge between the writing plan and native artifact
production.

## Semantic Fit

The check that context, topic, purpose, reader need, evidence boundary, and intended action fit each other before the artifact chooses wording, layout, or visual style.

## Folded Unit

A compressed or weak sentence, title, slide, table, chart, section, or deck move whose hidden judgment, sequence, or action is not yet visible enough for the reader.

## Weakness Diagnosis

The named reason a folded unit is not yet usable, such as missing situation, missing distinction, missing evidence boundary, missing action, missing sequence, or overloaded visual surface.

## CTA Interview Log

The cognitive-task-analysis question log used to reveal what the author, speaker, or reader was already implying. In this skill, CTA always means Cognitive Task Analysis, not a marketing call to action.

## Unfolding Trace

The record of how hidden content inside a folded unit became visible as a sentence, title, diagram, table, visual hierarchy, or action step.

## Release Readiness

The final presentation can be released. For PPTX work, this requires a fresh Microsoft PowerPoint open check with no recovery dialog, not only zip/XML validation.

## Open Visualization Planning

The visual planning stage explores any suitable expression path, such as
diagram, table, layout, sketch, image, native PPTX object, chart, or text-first
composition. PPTX implementation follows only after semantic variables, chosen
values, intentionally unconstrained areas, and real medium constraints are
explicit.

## Title-Only Story

The slide-title sequence read by itself. In this skill, it is a proxy for whether the deck's problem, development, practice reason, judgment standard, response, and close are visible before visual design.

## Assertion-Evidence Fit

The relationship between a slide title and its body. The title states one claim or action, and the body directly supports it with evidence, comparison, procedure, example, or action.

## One Beat

The rule that one slide should perform one main learner-facing job. Definitions, examples, warnings, source inventories, and practice instructions should not compete on the same slide unless the exception is explicit.

## Cognitive Readability Proxy

A non-human-outcome review of grouping, proximity, signaling, redundancy, split attention, scan path, and decorative load. It can support a candidate judgment, not a claim that learners understood or retained the material.

## Session Feedback Pattern Gate

The gate that turns repeated review comments into reusable checks. It covers
title story naturalness, decorative load, internal metadata relevance,
legal/regulated-domain AI boundaries, citation links, table/body fit, and
prompt knowledge structure.

## Semantic Staging Design Framework

The visual direction framework used when an artifact needs attention, curiosity,
guided reading, spoken flow, evidence reveal, action exit, and explicit design
freedom. It defines the scene beat, attention entry, curiosity gap, reading
path, listening cue, evidence reveal, semantic variables, accessibility and load
control, design-freedom boundary, open expression options, selected-expression
rationale, and unnecessary constraints to remove before open visualization
planning or PPTX build.

## Design Freedom Boundary

The record of which visual choices are fixed, flexible, or intentionally open.
It prevents a predefined style kit, template, layout family, palette, fixed
image-generation method, icon style, motif, animation plan, or typography scale
from becoming a hidden default unless a real audience, evidence, medium,
accessibility, brand, native-PPTX, license, or production constraint requires it.

## Artifact-Level Design System Lock

The stable style grammar for one active artifact: token/style namespace,
typography hierarchy, spacing and density, component grammar, status semantics,
and accessibility/contrast. Its values are project-specific, but changing them
after production starts requires a new lock id and fresh proof. It does not lock
every scene to one layout, camera, silhouette, or material.

## Open Visual Materiality

An open candidate space that treats every visual form an LLM can currently or
later render as eligible until a real source, brand, license, safety,
accessibility, medium, or production constraint closes it. It is not a finite
style whitelist and does not force image generation when SVG/native structure
better serves the meaning.

## Scene-Centered Meaning

The requirement that every major semantic unit has one scene and one reader
inference or action, whether the scene is a concrete world, an operational state,
or an abstract relationship. It records recognizable entities or anchors,
action/state change, visible cues, semantic boundaries, deterministic meaning
items, materiality choice, and route without equating a scene with a repeated
layout.

## Localization Materialization / Reflow

The visual-authoring work that follows translation, naturalization, or
concretization: preserve facts and claim boundaries, update visible and
accessible copy, invalidate affected text-fit/geometry/render/native-open proof,
recompute layout, rerender the target medium, and close with fresh evidence.
The `korean` skill owns language judgment; visual-authoring owns this
materialization and proof-freshness boundary.

## Internal Metadata Relevance

The check that process labels, version labels, model/provider labels, or source
workflow names appear in learner-facing output only when the reader needs them.

## Artifact Surface Separation

The closeout rule that learner-facing artifacts, instructor/facilitator
artifacts, production source, evidence/fact tables, render/native proof, and
delivery handoff are tracked as distinct surfaces.

## Near-Miss Trigger

A case that resembles this skill but should not trigger it, such as a single
sentence rewrite, one-off color advice, or simple image export with no reusable
authoring workflow.

## Human Outcome Validation

Evidence from actual people or learner artifacts, such as comprehension answers, transfer tasks, collaborator edit sessions, or performance outputs. Proxy checks do not replace this evidence.

## Semantic Variables

Named visual decisions that actually carry meaning, such as contrast, position,
grouping, object type, label, scale, reveal timing, relationship encoding,
native object type, alt text, or reading order.

## PPTX Standard XML Generation

The build surface that creates a new editable PPTX through PresentationML/OPC-aware helpers or builders. It supports a structural generation claim, not final PowerPoint release readiness.

## PresentationML Compliance

The validation surface that checks ECMA-376, OPC, DrawingML, and MS-PPTX rule families against package structure, relationships, slide order, drawing IDs, table anchors, native features, and source coverage.

## Visual Value Spec

The intentional visual-value record for design intent, reader-path support,
readability/accessibility, native medium constraints, chosen values, and
intentionally unconstrained areas.

## Readability Fit

The check that reading effort, audience distance or device, delivery mode, and
cognitive load are considered when text decisions matter. It does not force a
specific type measurement, type scale, or layout unless the target medium
requires it.

## Ziphyun Handoff

A prepared research or particle output that can be handed to Ziphyun or another knowledge system. The scaffold does not ingest directly into Ziphyun.

---

## Visual Semantic 계열 (원형: geo-carbon-visual-integrator)

# Glossary

- `의도된 시각 시스템`: 페이지 목적을 기준으로 색/간격/계층/행동을 사전에 고정한 규칙 집합.
- `Carbon 의미론 토큰`: 값 자체가 아니라 역할(배경/텍스트/상태) 중심으로 이름 붙인 선택형 변수 체계. Carbon 적용 자체가 시각화는 아니다.
- `Token Alias`: 레거시 변수명을 Carbon 토큰으로 연결해 하위 호환을 유지하는 매핑.
- `Evidence-first 판정`: 스크린샷/DOM/CSS 근거가 없는 시각 평가는 무효 처리하는 방식.
- `PASS/CONDITIONAL/FAIL`: Must 충족 여부를 단계적으로 판정하는 결과 체계.
- `Section Job`: 각 섹션이 수행하는 단일 핵심 목적(설명/신뢰/전환 중 하나).
