---
name: microdots-generate
description: Generate MicroDots in resumable batches. Use for "generate these five dots", "build the dots in this brief", "resume the batch", "the batch failed halfway" — several MicroDots at once, with dependency order, isolated subagents, per-item verification and scoped local catalog registration. When a batch turns out to be blocked on a capability that does not exist, prepare one reviewed prerequisite through microdots-extend rather than extending the framework silently. One ordinary MicroDot, with no batch and no missing capability, belongs to bespoke-agentics:microdots-new-micro or the checkout's own new-micro skill. A request that names the extension up front starts at microdots-suite.
---

# Generate MicroDots

Read the suite [working contract](../microdots-suite/references/working-contract.md)
and [generation lanes](references/generation-lanes.md). For multiple items also
read the [batch protocol](../microdots-suite/references/batch-protocol.md).

## Check the request is yours

Before planning anything, confirm the request is a batch. It is yours when it
asks for several MicroDots, resumes or recovers a partial batch, or carries a
dependency between items.

A single ordinary MicroDot is not. Hand it to the checkout's `.claude/skills/new-micro/`
or to `bespoke-agentics:microdots-new-micro`, and say which. That skill may be
configured not to fire on its own — invoke it by name rather than assuming it
will pick the work up. Only when no such skill is available do you generate the
single dot here, and say that you did so for lack of a better provider.

A request that names a framework extension up front ("add a chart primitive, then
build three dots using it") is compound work: it starts at
[microdots-suite](../microdots-suite/SKILL.md), which orders the prerequisite
before its dependents. What belongs to you is the gap you *discover* mid-batch.

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
