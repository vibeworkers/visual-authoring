# PPTX Native Runtime Receipt Contract

## Purpose

Use this contract after a structurally valid PPTX candidate has been built and
before anyone calls it release-ready. It records a PowerPoint observation for
the **exact candidate hash** without pretending that an OOXML check, preview,
or recovered session is native-runtime evidence.

This contract does not open PowerPoint, click a dialog, save a file, or repair
a package. Those are document-runtime actions. If an implementation ever
performs one, it must first use `generate-skill`'s native action-binding
contract and its static action audit. The normal portable path is a manual,
target-bound observation followed by a deterministic receipt validator.

## Native-runtime gate and receipt

The compiler writes a `*.powerpoint-native-gate.json` beside its candidate.
It declares the candidate path/hash, slide count, required criteria, and the
names of objects that must survive an edit round-trip. A tester writes a
separate observation JSON. The tester may describe what happened; only
`scripts/validate_pptx_native_runtime_receipt.py` computes the status.

```text
fresh authored source -> compile -> structural/read/render ledgers
  -> exact candidate hash -> fresh PowerPoint observation
  -> deterministic receipt -> release decision
```

Required baseline criteria:

| Criterion | Evidence | Meaning |
| --- | --- | --- |
| `fresh_process` | `opened_in_fresh_process: true` | PowerPoint had no presentation open before this candidate. |
| `exact_candidate` | candidate SHA-256 equals gate SHA-256 | The observation belongs to this build, not a previous one. |
| `no_recovery_dialog` | `recovery_dialog_visible: false` | No recovery dialog appeared before a save/export/action. |
| `all_slides_reviewed` | complete ordered slide list | Title, body, footer, and number received a visual review. |
| `*_edit_roundtrip` | named object, saved separate copy, clean reopen | Required native editing works after save and reopen. |

The gate can add named edit-roundtrip criteria, but it must not replace these
four baseline criteria. Each named object comes from the gate's observation
template; the observation cannot substitute a different name.

## Fixed, Flexible, Decisional ownership

- **Fixed**: candidate hash, baseline required criteria, status vocabulary,
  receipt schema, and all status computation stay in the validator.
- **Flexible**: the authored candidate path, slide count, named editable
  objects, and the recorder's factual observations vary by deck.
- **Decisional**: a person decides whether the requested release needs the
  partial first-open receipt or the complete review/edit receipt. The compiler
  may require more named round-trips, but it cannot relabel an incomplete
  receipt as release-ready.

## Status vocabulary

| Status | Exact interpretation | Next action |
| --- | --- | --- |
| `pass_native_runtime` | Every required criterion is true. | Release decision may use this native-runtime ledger only; review other ledgers separately. |
| `pass_native_first_open_pending_release` | Fresh process, exact hash, and no recovery dialog are true; required review/edit evidence is intentionally incomplete. | Complete the named review and edit-roundtrip observations. Do not call the deck released. |
| `pending_native_observation` | A required native observation has not happened yet. | Perform the exact manual observation or record a manual-action blocker. |
| `fail_native_runtime` | A recovery dialog, exact-hash mismatch, or failed recorded round-trip occurred. | Freeze this candidate as an incident artifact; correct authored source/compiler and start a fresh family. |
| `blocked_invalid_gate` | Gate or observation schema cannot bind the event to a candidate. | Fix the evidence contract; do not infer a result. |

`pass_native_first_open_pending_release` is deliberately not a release pass.
It makes partial evidence visible without relabeling it as a failure or a
completion.

## Observation boundary and incident isolation

- A recovery dialog on an exact candidate is a `fail_native_runtime` event for
  that hash. Keep the file only as a diagnostic artifact.
- Do not dismiss, accept, repair, resave, export, or normalize a recovery
  dialog as part of this receipt flow. A UI action requires exact target
  binding, explicit authorization, literal action events, and an independent
  postcondition; otherwise stop for a person.
- A rebuilt PPTX has a different hash. Its old native receipt is stale even if
  filenames match.
- Native-runtime proof does not prove visual quality, accessibility,
  instructional quality, learner comprehension, or distribution outcome.

## Run

```bash
scripts/visual-authoring-runtime run scripts/validate_pptx_native_runtime_receipt.py \
  --gate build/deck.powerpoint-native-gate.json \
  --observation build/deck.first-open.observation.json \
  --report build/deck.native-runtime-receipt.json
```

Run the deterministic fixtures first:

```bash
scripts/visual-authoring-runtime run scripts/validate_pptx_native_runtime_receipt.py --self-test
```

The validator writes a receipt only. It has no PowerPoint automation and no
package-mutation path.
