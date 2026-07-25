# Author-Corpus Essay Grammar

## Purpose

This reference turns an author's existing essay corpus or an explicitly bounded
conversation-derived corpus into a reusable reading-flow packet for visual
authoring. It does not recreate a publishing platform, claim an official platform
style, infer an author's intent, diagnose a person, or treat theory-informed
interpretation as empirical validation.

## Packet contract

Use `visual-authoring.essay-grammar.v1`.

```json
{
  "schema_version": "visual-authoring.essay-grammar.v1",
  "corpus_id": "author-corpus-id",
  "source_role": "author_corpus_reference",
  "sample_sources": [
    {
      "id": "stable-source-id",
      "source_path": "relative/path/to/source.md",
      "title": "source title",
      "observed_roles": ["entry_tension", "context_bridge", "open_end"]
    }
  ],
  "observed_flow": [
    "entry_tension",
    "exploration_question",
    "context_bridge",
    "thought_shift",
    "open_end"
  ],
  "non_claims": [
    "not_official_brunch_platform_grammar",
    "not_a_human_outcome_claim"
  ],
  "provenance": {
    "source_kind": "conversation_and_local_artifacts",
    "accessible_surfaces": ["current_conversation", "codex_memory_summary", "local_project_artifacts"],
    "unavailable_surfaces": ["claude_raw_session_transcript"],
    "transformation": "paraphrase_and_observation_not_verbatim_transcript",
    "source_boundary": "Use only accessible material; do not infer unavailable speaker intent."
  },
  "theory_validation": [
    {
      "lens": "linguistics",
      "observation": "question and repair move",
      "bounded_interpretation": "supports a discourse-move observation",
      "not_claim": "not a universal grammar or author-intent proof"
    }
  ],
  "target_adaptation": {
    "target_surface": "web",
    "preserve": ["reader-facing movement"],
    "transfer": ["layout or interaction choice"],
    "discard": ["platform chrome"],
    "open_end_policy": "how the reader-facing ending remains open"
  }
}
```

`source_path` must remain relative to the project corpus root. The optional
`--root` validator check confirms that the listed files are present without
modifying them.

### Conversation-derived corpus and theory boundary

When the available material is a ChatGPT/Codex conversation, a local work log, or
another explicitly accessible artifact rather than an author-owned article
corpus, set `source_role` to `conversation_corpus_reference`. Record the
accessible and unavailable surfaces in `provenance`, and mark paraphrase versus
verbatim text. A Claude session may be listed only when its transcript is
actually accessible; a plan filename or memory mention is not a transcript.

`theory_validation` is a bounded interpretation ledger, not a research result.
For conversation-derived material, include one entry for each of these lenses:
`linguistics`, `counseling_psychology`, `coaching`, `behavior_change`,
`symbolic_systems`, and `cognitive_science`. Each entry separates the observable
cue, the useful interpretation, and the claim that remains prohibited. These
lenses can improve wording, question design, action specificity, symbol choice,
and reading load; they cannot prove diagnosis, motivation, comprehension,
behavior change, or author intent.

## Observation roles

The packet does not reproduce an official platform style; `official platform style`
is an excluded claim, not an output target.

| Role | What to look for | What not to claim |
|---|---|---|
| `entry_tension` | a scene, friction, surprise, or discomfort that starts the thought | that every text begins this way |
| `exploration_question` | a stated or implicit question that keeps inquiry open | that it is a universal rhetorical formula |
| `context_bridge` | an example, source, history, or lived context that changes the question | that the source proves the author’s intent |
| `thought_shift` | a reframing, correction, or broadened relation | that it resolves the subject once and for all |
| `open_end` | a question, invitation to notice, or intentionally unfinished thought | reader empathy, conversion, or comprehension |

## Worked example: Haegyung Brunch corpus

The project-local packet may cite the supplied corpus and its own analysis report.
For the initial study, three articles cover a reading/culture essay, an AI essay,
and a design essay. The corpus report records a broader proxy observation:
`question -> reframing -> correction -> relation/value/action`. That report is a
marker-based analysis, not proof of author intent.

The transferable candidate is therefore:

```
entry tension or scene
  -> question worth staying with
  -> context that complicates it
  -> thought shift or reframing
  -> open end for the reader's own situation
```

When authoring a web theme, this can become a quiet opening, a readable body
column, evidence or example breaks, and a final related question. It must not
be renamed "the Brunch UI" or used to promise that readers will feel understood.

## Prompt / reference / code boundary

- Prompt (`SKILL.md`): decides when the module applies and asks for source-based
  observation, transfer, and discard decisions.
- Reference (this file): defines the schema, roles, provenance, theory lenses,
  exclusions, and interpretation boundary.
- Code (`scripts/validate_essay_grammar_packet.py`): checks source shape, allowed
  roles, relative source paths, required corpus coverage, provenance, theory-lens
  coverage, and required non-claims.
- Eval: valid and invalid fixtures test both normal use and the platform-claim
  near miss.

## Source, license, and runtime notes

- Use only a corpus the requester supplied or has authority to inspect. Keep source
  material read-only and preserve source URLs or local provenance in project SoT.
- The packet stores observations and paths, not copied article bodies. Quotation
  follows the source license and the requester’s publishing rights.
- No credentials or network access are needed for validation. The portable module
  uses the shared skill core; no runtime-specific delta is required.
