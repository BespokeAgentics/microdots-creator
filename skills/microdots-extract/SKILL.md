---
name: microdots-extract
description: Scan a MicroDots checkout and selected external repositories for reusable fragments, rank evidence-backed candidates with provenance, dependencies and adaptation cost, then adapt only the candidates the user selects into tested MicroDots building blocks. Use for reuse discovery, "what in here is worth extracting", and deliberate fragment-level extraction with a selection step. Not for porting a whole foreign application or a whole feature end to end — those belong to the porting skills; this one ranks fragments and extracts a chosen subset.
---

# Discover and extract reusable fragments

Read the [working contract](../microdots-suite/references/working-contract.md) and
[candidate record](references/candidate-record.md).

## Scan the requested scope

Resolve selected repositories, revisions and feature areas. Record dirty-source
identity when it matters. Treat external source as read-only; fetch a requested
repository into a separate location when necessary. Exclude generated outputs,
dependency trees, credentials and unrelated private areas. Read relevant license
and provenance information before copying material.

Use Rig for indexed graph questions, then source reads to verify candidates; use
`rg` when a source is unindexed. Trace behavior through UI, state, contracts,
service/storage and dependencies rather than ranking files by superficial
similarity. Independent subagents may inspect disjoint repositories or features
and return candidate records without changing source.

Compare candidates with executable catalogs and reuse patterns. Identify existing
shared imports, configurable capabilities, copy-adapt patterns, new extensions,
and unsuitable coupled fragments. Rank by demonstrated reuse value, boundary
clarity, compatibility and adaptation effort. Explain uncertainty rather than
manufacturing precise effort scores.

## Select before extraction

Present a concise table with stable candidate IDs, source references, proposed
destination, consumers, dependencies, adaptation cost/risk and evidence gaps.
Ask the user to select candidates using a multiple-choice tool when available,
allowing a custom selection. Selection authorizes the described extraction; do
not repeatedly ask for the same authorization. If the user already selected an
exact fragment and destination, inspect scope without another election.

Scanning alone creates no framework/catalog entries. Freeze candidate provenance
at selection; later scans are explicit refreshes and do not silently overwrite
extracted copies or presets. If source changes before extraction, report the delta
and reassess affected decisions.

## Adapt and prove

Preserve selected behavior and deliberately translate boundaries into Effect
services, Foldkit state/update/view, attributes, brokered events and owned storage
as needed. Do not transliterate foreign components or preserve hidden global
state. Distinguish source behavior, adaptations, omissions and new requirements.

Use [microdots-extend](../microdots-extend/SKILL.md) for compiler/runtime catalog
work and [microdots-generate](../microdots-generate/SKILL.md) for whole MicroDots.
Independent selected candidates may run in a batch with one integration owner.
A selected proposal satisfies extension review if it already describes that
design; ask again only for a materially different extension.

Finish with a real consumer and agreed catalog/visible-browser evidence. Preserve
repository/revision/file/symbol lineage outside runtime Catalog's narrow wire
provenance schema. Report adopted, skipped and blocked candidates separately,
with resulting catalog identities and verification evidence.
