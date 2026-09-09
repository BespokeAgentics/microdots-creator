---
name: microdots-generate
description: Generate MicroDots in resumable batches through the repository compiler or explicit reference-dot scaffolding, coordinating isolated subagents, dependency order, per-item verification and scoped local catalog registration. Use for several MicroDots at once, for resuming or recovering a partial batch, or when generation is blocked on a framework capability that does not exist yet. A single ordinary MicroDot with no batch, no dependency and no missing capability belongs to the workspace's own single-dot authoring skill. Never silently extends the framework to close a gap.
---

# Generate MicroDots

Read the suite [working contract](../microdots-suite/references/working-contract.md)
and [generation lanes](references/generation-lanes.md). For multiple items also
read the [batch protocol](../microdots-suite/references/batch-protocol.md).

## Plan the batch

Translate each brief into domain behavior and observable acceptance criteria.
Inspect the live authoring catalog and selection schema; match reuse patterns
before proposing new source. Use stable item IDs and distinct destinations.
Ask only for missing domain decisions that materially change behavior.

Classify each item as a compiler-owned application or an explicitly requested
repository extension. Framework ownership by the user does not turn every
application request into permission to modify the compiler.

Deduplicate shared requirements. If the catalog cannot represent a capability,
record the actual diagnostic and prepare one reviewed prerequisite through
[microdots-extend](../microdots-extend/SKILL.md). Stop only its dependent items.
Do not substitute a weaker capability or patch compiler output by hand.

Propose limits scaled to the batch and available worker slots, allowing user
overrides. Count the coordinator against agent capacity. A small-batch starting
proposal is up to three workers and two total attempts per item; choose time
limits from expected build and browser costs. Limits are ceilings, not a reason
to consume all retries or spawn idle workers.

## Execute and integrate

Give each ready item to a bounded subagent with its lane, pinned inputs, private
paths, acceptance checks and limits. Workers return changed paths/output location,
receipts, diagnostics and evidence. They do not edit common registry, lockfile,
catalog, topology or wiki files concurrently.

The coordinator integrates verified source changes and shared prerequisites,
regenerates shared catalog outputs once per compatible wave, then supplies the
resulting exact source/catalog identity to dependents. Run serial scaffold/port
allocation where the generator derives identities from repository state;
independent worktrees alone do not prevent duplicate allocated ports.

Use [microdots-verify-local](../microdots-verify-local/SKILL.md) for every final
item. Prove build, tests and visible primary behavior, then use
[scoped registration](../microdots-manage/references/catalog-lifecycle.md), followed
by readback and the actual Platform selection/mount journey. A catalog row is
insufficient when its bundle or service cannot be reached.

## Recovery and result

Preserve successes and continue independent items after a failure. Retry only
after a concrete diagnosis/change or an identified transient failure, within
announced attempt/time/resource limits. Authentication, authorization and
unsupported-operation failures require resolution, not repeated requests.

On resume, inspect task-owned processes before replacing a running worker,
recheck source/catalog/evidence identities, and skip still-valid successes. Retry
catalog publication separately from a completed build. Report each item's status,
identity, destination, proof and remaining action, plus batch progress and resource
use. Completion means all requested evidence and local catalog usability passed.
