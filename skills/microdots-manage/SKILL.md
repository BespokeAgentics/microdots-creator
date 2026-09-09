---
name: microdots-manage
description: Inspect and manage MicroDots that already exist, and their runtime Catalog lifecycle. Use for "what version is selected", "what is the latest version of X", "register this build", "retire this dot", "reinstate it", "what consumers break if I change this", "the publication failed halfway" — identity, selected versus latest version, compatibility impact, replacement, deprecation, retirement, reinstatement, and reconciling a partially completed batch. Not for proving a change works (bespoke-agentics:microdots-verify) or for deploying (microdots-deploy).
---

# Manage MicroDots

Read the [working contract](../microdots-suite/references/working-contract.md).
For Catalog mutations or recovery, read [catalog lifecycle](references/catalog-lifecycle.md).

## Identify the managed object

Resolve human names to actual artifacts. Determine whether the request concerns
compiler vocabulary, a generated workspace, a repository-owned MicroDot, a runtime
Catalog version, or a host placement. Read current source/catalog state and affected
consumers before changing it. A catalog version change is not automatically a
live-host update.

Inspect/status requests stay read-only. Report current identity, selected versus
latest version, lifecycle, provenance, compatibility and evidence limits. Use
`get` for exact version history; a list can show the older selected version while
a new version remains in flight.

## Choose the operation

| Operation | Route |
| --- | --- |
| Change generated application behavior | Change semantic selection/spec, compile fresh output through `microdots-generate`; preserve original until replacement is verified |
| Evolve runtime/compiler definitions or add a reusable component | `microdots-extend`; assess pinned consumers and migrations |
| Update a repository-owned reference MicroDot | Scoped source edit, integration checks and `microdots-verify-local` |
| Register, select a version, retire or reinstate | Current public Catalog/Workbench operations in the lifecycle reference |
| Resume a partial batch or failed publication | Batch ledger plus live identity/state reconciliation; do not rebuild valid successes |
| Deprecate, rename, delete, transfer tags, migrate storage, or roll back | Inspect support and consumers; distinguish advisory recommendations from implemented lifecycle operations |

Before changing compatibility, enumerate attribute/event/RPC/schema/tag/target
effects and affected consumers. Give a concrete migration and rollback path where
possible. Do not promise reversibility an operation does not support. For an
unsupported lifecycle request, prepare an extension proposal; never fabricate an
RPC or directly edit the database to approximate it.

## Apply and reconcile

Operate only on requested identities through the owning service or appropriate
source lane. Preserve immutable build/approval identities and publication lineage.
Reuse authorization for the named operation; ask only when an unresolved destructive
effect or materially different extension needs a new decision.

For batch lifecycle work, apply independent operations within announced limits;
serialize operations touching the same record or shared catalog. On timeouts,
read current state before retrying: an operation may have succeeded despite a
lost response. Keep successes while reporting refusals/blockers for other items.

Verify exact readback and relevant Platform behavior. Use
[microdots-verify-local](../microdots-verify-local/SKILL.md) when behavior, selection,
placement or availability changed. Return before/after identities, affected
consumers, evidence and unresolved items. Publishing, deployment and production
changes remain separately scoped requests.
