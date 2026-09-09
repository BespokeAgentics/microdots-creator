---
name: microdots-extract
description: Scan a MicroDots checkout and selected external repositories for reusable fragments, rank candidates with provenance, dependencies and adaptation cost, then adapt only the ones the user selects. Use for "what in here is worth extracting", "find reusable pieces across these repos", "scan for reuse", "is this worth pulling out" — discovery and ranking first, with a selection step before any code moves. Not for "port this app to MicroDots" or "carve feature X out of app Y" (bespoke-agentics:microdots-port-app, microdots-port-feature): those name their target up front and port it whole, while this one starts without a named target and produces a ranked shortlist.
---

# Discover and extract reusable fragments

Read the [working contract](../microdots-suite/references/working-contract.md) and
[candidate record](references/candidate-record.md).

## Check the request is yours

Apply one test: **did the user name the target?**

A request that names what to move — "port this app to MicroDots", "carve the
filter bar out of the admin app", "turn this feature into a micro" — is a port.
The decision of what to take is already made; the work is re-expressing it whole.
Route it to `bespoke-agentics:microdots-port-app` or `microdots-port-feature`.

A request that names only a *place to look* — "what in here is worth extracting",
"scan these repos for reuse", "is any of this reusable" — is yours. The decision
of what to take is the deliverable: you produce a ranked shortlist and the user
selects from it before any code moves.

The ambiguous middle is real. "Extract the filter bar so we can reuse it" names a
target but asks about reuse. Resolve it by asking whether the user wants a
shortlist or wants that one thing moved, rather than guessing. If the user has
already named an exact fragment and destination, skip the election and scope the
work directly.

## Scan the requested scope

Resolve selected repositories, revisions and feature areas. Record dirty-source
identity when it matters. Treat external source as read-only; fetch a requested
repository into a separate location when necessary. Exclude generated outputs,
dependency trees, credentials and unrelated private areas. Read relevant license
and provenance information before copying material.

Use Rig light tools for indexed graph questions when that MCP server is
available, then source reads to verify every candidate. When Rig is absent, or
the source is simply unindexed, use `rg` and ordinary reads — this changes how
long the scan takes, never what counts as evidence. State which route you used,
because an unindexed scan has weaker recall and the ranking inherits that. Trace behavior through UI, state, contracts,
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
