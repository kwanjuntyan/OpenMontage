# Production Unit Protocol — 30-minute benchmark evidence

Status: completed experimental evidence for one frozen course/profile. This is
not M6 qualification and does not establish a universal optimum for unit size.

## Scope

- Compared one 30-minute `mode=off` scene plan with `auto@180s` PUP output.
- Source duration: 1804.153 seconds; 44 script sections.
- PUP arm: 12 isolated units, merged deterministically.
- Generation and blind review model display name: Gemini Flash 3.8 high.
- Blind review: 12 matched spans across three fresh-context batches; arm labels
  hidden and A/B order randomized per span.
- No media was generated and unavailable provider telemetry was not invented.

## Mechanical result

Both arms passed the applicable schema, timeline, section-coverage, and CLP
checks. The PUP merge had zero boundary defects, zero duplicate scene IDs, and
exact CLP-binding coverage.

| Metric | off | PUP auto@180s |
|---|---:|---:|
| Scenes | 85 | 105 |
| Scenes per minute | 2.827 | 3.492 |
| Median description characters | 144 | 651 |
| Structured-detail retention | 0.462 | 0.957 |
| Scene-type diversity | 4 | 5 |
| Longest same-type run | 10 | 27 |

`longest_same_type_run` counts only the coarse canonical `scene.type` label.
It does not inspect setting, framing, movement, overlays, character action, or
the semantic content of the description. It is therefore an advisory
diagnostic, not a visual-quality gate.

## Blinded semantic result

- Verdict: `pup_superiority_passed` for this frozen comparison.
- Matched spans: PUP 12 wins, 0 losses, 0 ties.
- Mean composite: PUP 5.000, off 3.361; gain +1.639 on the frozen 1–5 scale.
- Critical semantic findings: 0.
- Critical boundary defects: 0.
- Visual variety and non-redundancy: PUP 5.000, off 3.167; delta +1.833.

The blind result contradicts interpreting the longer coarse-type run as actual
visual repetition. The supported statement is narrower: this PUP run reused
the `character_scene` schema label for longer stretches while reviewers judged
its visual variety and non-redundancy to be better.

## Limits

- One course and one 30-minute source were evaluated.
- The same model family generated and reviewed the material; blinding,
  randomized arm order, and fresh review contexts reduce but do not eliminate
  evaluator-family bias.
- The PUP arm reached a 5.000 ceiling, so later trials should use additional
  evaluators or a more discriminating rubric when calibrating defaults.
- This evidence does not compare 300- or 480-second units and cannot establish
  that 180 seconds is the best default.
- M6 still requires the separately approved 60-minute, cross-platform,
  recovery, resource, and media qualification work.

## Frozen local evidence digests

The raw reports remain in the gitignored benchmark project. These hashes bind
this summary to the reviewed local evidence without checking generated project
artifacts into the product branch.

| Evidence | SHA-256 |
|---|---|
| `30m_paired_evaluation_protocol.json` | `BF7F1F44A4C531761B0F2E9442BAF81A71AB46F3BCA172D553BD3A7F1A9577F3` |
| `30m_pup_assembly_comparison.json` | `AB81F6DE8E1002206C5A8C559AA37CC43B9F7A0AEF507D80A3B12D11E31D6EAB` |
| `30m_blind_semantic_result.json` | `3BDA7A8DDAD1F7166BD724364C6E944A5745D8ABCA78DDD9D9C08D660DD80B78` |

Future telemetry should supplement the coarse type run with consecutive
`type + setting + framing + movement` tuples, repeated visual-motif/template
rate, and description semantic similarity. Those additions are observability
work and are not a reason to change the current PUP segmentation algorithm.
