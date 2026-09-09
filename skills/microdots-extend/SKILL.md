---
name: microdots-extend
description: Add or evolve MicroDots framework vocabulary. Use for "we need a data connector for X", "add a chart primitive", "make this capability selectable in authoring", "add a new shape", "change what this capability accepts" — compiler shapes, capabilities, backend UI primitives, data connectors, reusable components and shared runtime primitives, carried through catalog generation to Platform exposure, including versioning, pinned consumers, migration and rollback. Not for building an application out of vocabulary that already exists, and not for how a dot looks (bespoke-agentics:microdots-design).
---

# Extend the framework and catalogs

Read the [working contract](../microdots-suite/references/working-contract.md),
then relevant rows of [extension surfaces](references/extension-surfaces.md).

## Define the extension

Inspect executable catalogs, `docs/reuse-catalog.md`, related source and a working
consumer. Choose the smallest reusable abstraction serving the actual use cases.
Distinguish runtime exports, copy-adapt patterns, compiler descriptors/materializers,
and complete MicroDots. A data connector is not a backend layout primitive.

Describe the public contract, supported targets, parameters, errors, storage or
credential boundary, behavior, consumers, and compatibility impact. For a gap
discovered during generation, present this concrete proposal for user review before
implementation; batch creation does not accept a new framework design. An already
reviewed extension proceeds without repeated approval.

Record unsupported operations accurately. Inspect the current connector schema
before promising authenticated writes, pagination or arbitrary inputs; those may
require a larger extension. Missing Platform exposure belongs in the proposal if
catalog usability is required.

## Implement once, expose, consume

Edit authoritative definitions/materialized source, then run the repository catalog
generator. Descriptors, digests, barrels, snapshots and locks are outputs; do not
hand-edit them to suppress drift. Give shared-source changes one integration owner,
even when distinct extension implementations run in parallel.

Carry the addition through decoding, semantic validation, resolution,
materialization, target support and Platform parameter/selection surfaces as
applicable. Keep browser/service/Worker imports separated. A package export or
descriptor alone does not make a usable Platform capability.

Version changed public semantics and compiler output identities according to current
contracts. Preserve old pinned consumers or provide explicit migration and rollback
analysis; do not silently relock them. Test supported and rejected combinations,
including unset credentials for secret-dependent work.

Compile a fresh consumer selecting the new entry, check/build it, and use
[microdots-verify-local](../microdots-verify-local/SKILL.md) to prove visible
Platform selection, primary behavior and relevant persistence/refresh. UI pieces
need a rendered consumer; a headless connector fixture is not live-service or
visible-browser proof. Register the resulting MicroDot through the separate
runtime Catalog path only when that artifact is in scope.

Release dependent items only after the shared extension is integrated and verified
against the exact inputs they will consume. Report vocabulary, identity, targets,
consumer and evidence. Unmet exposure or compatibility requirements stay incomplete.
