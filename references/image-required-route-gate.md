# Visual Authoring Image-Required Route Gate

This reference is the official additional close gate for visual production routes that need concrete image material. Every route first uses the all-route `scene_first_judgement_packet`; this file adds image-specific production and evidence requirements only.

## Decision Order

1. Fix the `visual_vlc_review_packet`.
2. Fix the `scene_first_judgement_packet`.
3. Classify `route_status`.
4. If routed to image, create or preserve an image base artifact.
5. Add deterministic semantic layers in SVG/HTML/PPTX/Carbon.
6. Verify proxy readability and record human-validation boundary.

## Route Status Values

| Status | Meaning | Can Close? |
|---|---|---|
| `CLASSIFICATION_PENDING` | Source, goal, or scene is not stable. | No |
| `SVG_ALLOWED` | The visual claim is structural, abstract, or diagram-first. | Yes, with proxy evidence |
| `ROUTED_IMAGE_REQUIRED` | Concrete image material is needed but not yet produced/integrated. | No |
| `IMAGE_ASSET_PRESENT` | A preserved image exists, but integration/validation is incomplete. | No |
| `INTEGRATED_HYBRID` | Image base and deterministic semantic layer are both present. | Candidate/usable with evidence |
| `SVG_PROXY_ONLY` | SVG is replacing a needed concrete image scene. | No |
| `BLOCKED_IMAGEGEN` | Image generation/source acquisition is blocked. | No |

## Required Manifest

```yaml
image_production_manifest:
  product_anchor:
  model_or_source:
  output_form_slug:
  prompt_or_source_ledger:
  image_output_path:
  integration_path:
  verification_path:
  deterministic_semantic_layer:
    owner:
    controls:
      - exact Korean labels
      - arrows and attention path
      - evidence callouts
      - accessibility/contrast/readability
  read_tests:
    three_second_read:
    five_second_proxy:
    label_hidden_thumbnail:
  human_outcome_validation:
```

## Ownership Split

- `visual-authoring`: route classification, all-route scene-first judgement, deterministic semantic-layer integration, proxy/human boundary, and close gate.
- `creator-agent`: optional upstream core-message or story brief when the request needs separate narrative development; it does not own the scene-first packet or release decision.
- `imagegen`: generated image base or blocked image-generation evidence.
- `vector-language-cognition`: cognitive proxy, readability, grouping, proximity, split-attention, transfer cues.
- Target-format owners such as slides, documents, sites, and Carbon keep native editability and medium-specific verification responsibility.
- `quality-gate`: Must evidence closure and release decision.

## Non-Negotiable Close Rules

- `SVG_PROXY_ONLY` is a failed close state when concrete image recognition is required.
- `BLOCKED_IMAGEGEN` is a blocker, not a workaround success.
- Exact Korean labels, evidence text, arrows, citations, and ordering belong to deterministic layers.
- Human understanding, persuasion, cinematic immersion, and learning transfer claims require actual human evidence.
