# Visual Semantic Encoding Gate

This gate prevents visual production from depending on labels after the image is
already weak. It is used before image generation, SVG overlay, Carbon token
integration, or final visual judgement.

## Purpose

The viewer should read the main meaning from visible cues first. Text labels,
arrows, numbers, and Carbon callouts may guide attention, but they must not be
the only reason a viewer understands the scene.

## Required Order

1. Fix the core message in one sentence.
2. Convert the message into visual semantic units.
3. Define the label-masked reading criterion for each unit.
4. Generate or draw the base scene from visible cues only.
5. Hide labels, titles, arrows, and numbered callouts; judge what remains.
6. Add SVG semantic layer only after the base scene passes the masked read.
7. Integrate with Carbon tokens and run contact sheet / PNG evidence checks.

## Visual Semantic Unit Sheet

Use this table before prompting an image model or drawing SVG.

| Field | Meaning |
| --- | --- |
| meaning_unit | The meaning that must be understood. |
| visible_cue | What the viewer can see without reading labels. |
| masked_read_criterion | What a viewer should say when labels are hidden. |
| risk | How the cue may become ambiguous or decorative. |
| recovery_action | What to change if the cue fails. |

Minimum units for identity-consumption style key visuals:

| meaning_unit | visible_cue | masked_read_criterion | risk | recovery_action |
| --- | --- | --- | --- | --- |
| chosen object | concrete product with recognizable form | viewer can name the object category | object becomes generic decor | enlarge, simplify, or replace with a more familiar object |
| post-purchase evidence | receipt, box, confirmation, tag, or package trace | viewer can say a purchase happened | receipt looks like random paper | add receipt shape, barcode, torn edge, price line, or register context |
| repeated-use evidence | app streak, calendar marks, logbook, wear marks, repeated marks | viewer can infer repetition or tracking | phone reads as generic device | add repeated dots, graph trend, calendar marks, or wear traces |
| self-confirmation anchor | mirror, profile, face reflection, hand pointing back, silhouette looking at evidence | viewer can infer "this returns to me" | self becomes icon-only abstraction | use mirror/reflection/profile endpoint before adding text |
| meaning flow | spatial order from object to evidence to record to self | viewer can roughly follow the path | arrows do all the work | arrange objects in reading order and use path only as signal |

## Pass / Fail

Must pass before claiming visual clarity:

- At least three of four key units are identifiable with labels hidden.
- The self-confirmation anchor is readable as a person/self endpoint, not only a
  circular icon or abstract target.
- The approximate movement is readable from layout and object placement before
  arrows explain it.
- SVG reinforces attention and sequence; it does not rescue an unreadable base
  scene.
- "Cinematic immersion PASS" is not declared before a human 5-second read test.

Fail if:

- The viewer needs labels to identify the main objects.
- The visual can be understood only after reading the caption.
- The generated image adds attractive texture but does not strengthen the
  semantic units.
- The fix is "add more labels" instead of improving visible cues.

## Prompt Implication

Image prompts should ask for concrete scene evidence: objects, surfaces, light,
hands, receipts, screens, mirrors, reflections, use traces, and spatial order.
They should not ask the model to draw abstract theory, condition gates, arrows,
or Korean explanatory labels. Those belong in editable SVG/HTML layers.
