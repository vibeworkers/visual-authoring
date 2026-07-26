# Universal Visual VLC Concept Map

## Scope Path Markers

- Core Path: `/Volumes/Extend/.codex-relocated/skills/universal-visual-vlc/SKILL.md`
- Support Path: `/Volumes/Extend/cogarch/tools/surface_vlc_gate.py`
- Scope: visual/storytelling review gate and delivery evidence routing.

## Nodes

- `universal-visual-vlc-skill`
  - path: `/Volumes/Extend/.codex-relocated/skills/universal-visual-vlc/SKILL.md`
  - role: ordinary skill review gate for visual/storytelling surfaces
- `surface-vlc-design`
  - path: `/Volumes/Extend/cogarch/docs/20260507_universal_vlp_surface_proxy_gate_design.md`
  - role: generic Surface VLC gate design SoT
- `visual-adapter-design`
  - path: `/Volumes/Extend/cogarch/docs/20260507_vlp_visual_quality_tool_design.md`
  - role: visual/storytelling adapter design
- `image-required-route-gate`
  - path: `/Volumes/Extend/.codex-relocated/skills/universal-visual-vlc/references/image-required-route-gate.md`
  - role: official route-status and close gate for visual surfaces requiring concrete image material
- `surface-vlc-tool`
  - path: `/Volumes/Extend/cogarch/tools/surface_vlc_gate.py`
  - role: executable language/context/goal proxy gate
- `delivery-gate-tool`
  - path: `/Volumes/Extend/cogarch/tools/run_surface_delivery_gate.py`
  - role: combined Surface VLC plus target-profile delivery gate
- `cogarch-skill`
  - path: `/Volumes/Extend/.codex-relocated/skills/cogarch/SKILL.md`
  - role: umbrella governor and visual review intake router
- `generate-skill-management`
  - path: `/Volumes/Extend/.codex-relocated/skills/generate-skill/references/global-skill-management.md`
  - role: cross-skill route and ordinary-skill portfolio registry
- `vector-language-cognition`
  - path: `/Volumes/Extend/.codex-relocated/skills/vector-language-cognition/SKILL.md`
  - role: owner for core VLP metric/schema/validator changes

## Edges

- `cogarch-skill -> universal-visual-vlc-skill`
  - reason: visual-related requests are first treated as review-gate candidates
- `universal-visual-vlc-skill -> surface-vlc-design`
  - reason: generic surface proxy contract remains the core abstraction
- `universal-visual-vlc-skill -> visual-adapter-design`
  - reason: visual/storytelling behavior is an adapter, not a separate core metric family
- `universal-visual-vlc-skill -> image-required-route-gate`
  - reason: visual surfaces that need concrete image recognition must not close as SVG-only proxy work
- `universal-visual-vlc-skill -> surface-vlc-tool`
  - reason: file-backed review should prefer executable proxy evidence
- `universal-visual-vlc-skill -> delivery-gate-tool`
  - reason: slide/PDF/HTML release claims need target-profile evidence
- `generate-skill-management -> universal-visual-vlc-skill`
  - reason: the proof package has been promoted to an ordinary skill surface
- `universal-visual-vlc-skill -> vector-language-cognition`
  - reason: core VLP metric/schema/validator changes remain specialist-owned

## Shared Constraints

- Review before production for visual-related requests.
- No human-outcome pass from proxy evidence alone.
- `ROUTED_IMAGE_REQUIRED` requires preserved image, ledger, integration, and verification evidence before close.
- `SVG_PROXY_ONLY` and `BLOCKED_IMAGEGEN` are failed close states for concrete-image routes.
- New contexts add adapters and target profiles, not domain-specific core scores.
- Audience-facing artifacts should not expose internal method labels unless requested.
