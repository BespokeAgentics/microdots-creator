---
name: microdots-suite
description: Route framework-owner work on a MicroDots checkout to the right suite skill, and coordinate work spanning several of them: batch generation, compiler and catalog extension, reusable-fragment extraction, catalog lifecycle, and completion evidence. Use when a request names more than one of those operations, when a batch needs a plan and a dependency order, or when it is unclear which MicroDots workflow applies. Not for a single ordinary MicroDot, a blank-dot diagnosis, a design change, or a deploy.
---

# MicroDots creator suite

Turn a framework-owner request into scoped work with independently verified results.
Read [working-contract.md](references/working-contract.md) once per run, then load
only the skill needed for the requested operation.

Resolve the target repository root from the working directory, never from this
skill's own location — these files ship in a plugin and sit outside the checkout
they operate on. Confirm the root is a MicroDots repository before acting, and
name it in the run record. The plugin's own bundled files are reachable at
`${CLAUDE_PLUGIN_ROOT}` and are never a target of the work.

| Request | Skill |
| --- | --- |
| Generate one or many MicroDots; resume a batch | [microdots-generate](../microdots-generate/SKILL.md) |
| Add a core primitive, shape, capability, component, or data connector | [microdots-extend](../microdots-extend/SKILL.md) |
| Find and extract reusable fragments from selected repositories | [microdots-extract](../microdots-extract/SKILL.md) |
| Inspect, update, version, replace, deprecate, retire, or reinstate | [microdots-manage](../microdots-manage/SKILL.md) |
| Prove behavior and local Platform catalog usability | [microdots-verify-local](../microdots-verify-local/SKILL.md) |

## Coordinate

Identify the artifacts and their consumers. Distinguish application outputs,
repository-owned reference MicroDots, compiler catalog entries, and runtime
Catalog records. They carry different write authority and completion criteria.
Use the [source map](references/source-map.md) to locate current interfaces.

For compound work, map dependencies before dispatch: a shared missing capability
is one extension prerequisite, followed by its dependent MicroDots. Present its
design and compatibility impact for the user's review before implementation.
Continue independent work while that decision is pending.

State scope, output locations, evidence, concurrency, attempt/time limits, and
any configured paid-resource ceiling in the batch plan. Respect existing task
authorization; announcing a plan does not require another approval for already
authorized work. Concrete missing-capability proposals and extraction candidate
selection retain the review boundaries the user requested.

Use subagents for independent bounded work in isolated worktrees or output
directories. One coordinator owns shared integration and the run record. Delegate
the relevant skill, exact scope, source identity, allowed paths, limits,
dependencies and evidence requirements. If delegation is unavailable, report that
limitation and use the same dependency order serially; do not claim parallel work.

The [batch protocol](references/batch-protocol.md) provides resumable state and a
read-only checker. Use it for multi-item work; simple single-item edits do not
need a batch ledger. Preserve successes and report failed/blocked items
individually. No batch-wide success while a required item remains incomplete.

## Neighbouring guidance

This suite owns framework-owner work. Four adjacent jobs belong elsewhere, and
the workspace decides where: single-dot authoring, blank-dot diagnosis, workspace
verification, and deployment.

Discover what is actually available before routing to any of them. List the
checkout's own `.claude/skills/` directory, and check the installed skills for
equivalents (the `bespoke-agentics` plugin ships `microdots-new-micro`,
`microdots-debug-blank`, `microdots-verify` and `microdots-deploy`). Prefer the
checkout's copy when both exist — it is versioned with the code it describes.
Name the one you chose in the run record. If none exists, say so and proceed
with this suite's own rules rather than citing a skill that is not installed.

This suite carries the compiler, boundary and browser rules it needs, so a
missing neighbour degrades scope, not correctness. Porting skills for foreign
applications supply deeper source analysis when installed and requested.
Deployment is always a separately requested operation, never implied by
generation or verification.
