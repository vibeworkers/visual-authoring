# Publication Surfaces

## Purpose

Use this reference when a visual artifact becomes something a reader receives:
a textbook, workbook, ebook, public HTML, EPUB, or distribution PDF. It turns
the project decision into a surface contract instead of preserving accidental
cover copy or an old implementation.

This reference does not certify a file format. It records which standard
features matter, who verifies them, and what remains unclaimed.

## Three Surfaces

| Surface | Owns | Must not leak into it |
|---|---|---|
| `reader_public` | title, cover, TOC, body, reader actions, accessibility copy | prompt IDs, generation layers, validator IDs, release state, internal evidence labels |
| `facilitator_editor` | teaching notes, editorial notes, activity facilitation, operational handoff | production-only secrets or unverified outcome claims |
| `production_evidence` | source inventory, prompts, tests, scores, logs, format proof | reader-facing claims that exceed the proof |

`reader_public` is not an edited version of production evidence. It is a
separate composition whose words answer what the reader is learning, why it
matters, and what to do next.

## Vocabulary Mapping

Before writing a public cover, hero, TOC, status panel, or action card, create a
mapping like this in the project SoT:

| Internal item | Public treatment |
|---|---|
| scene or layer name | omit; describe the subject or learning relationship instead |
| prompt/model/output identifier | production evidence only |
| validator key, score, pass state | production evidence only unless the score itself is the reader's subject |
| release/draft/fix status | editor workflow only; omit from the reader copy |
| claim-evidence boundary | teach in the body only when it is a real course concept, with a reader-facing definition, example, and decision use |

Do not apply this table mechanically to real domain concepts. A technical term
can be taught in the body when it is the lesson itself. The prohibition is
against presenting authoring machinery or internal uncertainty labels as the
reader's first-facing message.

## Textbook and Workbook Roles

Choose the artifact profile explicitly.

| Profile | Required role contract |
|---|---|
| `single_publication` | one reader artifact; its internal sections still distinguish explanation from application |
| `textbook_with_workbook` | a main textbook plus a companion workbook, with distinct paths, TOCs, metadata, and cross-references |

For `textbook_with_workbook`:

- Main textbook: context, concepts, principles, mechanisms, misconceptions,
  judgment criteria, examples, and a first action. It cannot be only a set of
  forms, prompts, or checklists.
- Companion workbook: reusable worksheets, activity records, observation
  sheets, decision logs, and prompts that identify the relevant main-textbook
  concept. It cannot silently replace the explanation layer.
- A combined file must preserve these roles through clear parts and navigation;
  a cover or page count is not proof of the separation.

The intended reader response (understands the topic, trusts the author, can try
the method) is a design hypothesis. Use readability, explanation coverage,
traceable sources, and first-action clarity as proxies. Keep human reader
testing as a separate evidence surface.

## Standard-Informed Delivery Profile

For every requested delivery format, inventory relevant standard capabilities.
Mark each one `used`, `not_applicable`, or `blocked`. A `used` feature needs an
evidence path; `not_applicable` and `blocked` need a reason. A `blocked`
feature prevents release. The feature inventory is mandatory when the format is
in scope; the exact list is chosen by the format and audience.

### PDF

For a distribution PDF, inspect as applicable:

- target page size and stable page geometry;
- document title, author, subject, keywords, creator, and document language;
- embedded fonts and Unicode mapping;
- outline/bookmarks and working internal links when navigation is promised;
- static output with no encryption or JavaScript unless the delivery contract
  specifically allows them;
- tagging, reading order, alt text, and other accessibility structure when the
  audience and source format make them applicable.

PDF/A and PDF/UA are conformance profiles, not style names. Set
`conformance_claim: not_claimed` until the chosen profile has passed its
appropriate validator and the evidence path is recorded.

### HTML

When the document is a navigable public HTML artifact, use and verify:

- semantic headings and `nav` for the table of contents;
- stable anchors and hash navigation for location links;
- current-location indication and keyboard focus after navigation;
- document language, image alternatives, and reading order appropriate to the
  content;
- print styles only if printing or PDF conversion is part of the delivery
  profile.

### EPUB

When EPUB is in scope, verify cover, package metadata, reading order, TOC,
document language, navigation, and CSS fallback behavior. Do not infer EPUB
quality from a PDF or HTML render alone.

## Contract Shape

Keep the project contract in JSON so the deterministic validator can inspect
the declared boundary. Project validators may add more precise PDF, DOM, or
render checks.

```json
{
  "schema_version": 1,
  "artifact_profile": "textbook_with_workbook",
  "reader_public": {
    "files": ["proof/cover-public.txt", "proof/toc-public.txt"],
    "forbidden_terms": ["internal layer name", "draft status"]
  },
  "artifact_roles": {
    "textbook_main": {
      "path": "deliverables/textbook.md",
      "required_markers": ["핵심 개념", "사례", "판단 기준"]
    },
    "workbook_companion": {
      "path": "deliverables/workbook.md",
      "required_markers": ["실습", "기록", "본권"]
    }
  },
  "format_standard_profile": {
    "pdf": {
      "profile": "standard_informed_distribution_pdf",
      "features": [
        {
          "id": "metadata",
          "status": "used",
          "evidence_path": "proof/pdf-metadata.txt"
        },
        {
          "id": "pdfua_conformance",
          "status": "not_applicable",
          "reason": "No PDF/UA conformance profile was requested."
        }
      ],
      "conformance_claim": "not_claimed"
    }
  }
}
```

`reader_public.files` are focused text extracts or dedicated public-surface
files, not a shortcut for scanning an entire mixed-purpose source document.
For a single HTML file that contains both cover and body, a project validator
must inspect the relevant DOM selectors. The generic validator intentionally
does not guess those selectors.

Run:

```bash
scripts/visual-authoring-runtime run scripts/validate_publication_surface_contract.py \
  publication_surface_contract.json --root <project-root>
```

## Proof Surfaces

Report at least these separately:

1. Source proof: role map, required markers, public vocabulary map.
2. Render proof: cover, TOC navigation, pages, reader-visible labels.
3. Format proof: PDF/HTML/EPUB profile features and validator output.
4. Human proof: reader reaction or usability test, when collected.

A render that looks finished is not conformance proof. A format validator pass
is not evidence that readers understood or trusted the material.
