---
name: microdots-suite
description: Route and coordinate framework-owner work on a MicroDots checkout. Use for "generate these five dots", "add a capability then build the dots that need it", "scan these repos for what we can reuse", "close out the batch" — and for any request naming more than one of: batch generation, compiler/catalog extension, fragment extraction, catalog lifecycle, completion evidence. Not for a single ordinary MicroDot (bespoke-agentics:microdots-new-micro), a blank or stale dot (microdots-debug-blank), a plain done-check (microdots-verify), how a dot looks (microdots-design), porting a whole app or feature (microdots-port-app, microdots-port-feature), or a deploy (microdots-deploy).
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
| Generate several MicroDots; resume or recover a batch | [microdots-generate](../microdots-generate/SKILL.md) |
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

This suite owns framework-owner work: batches, compiler and catalog vocabulary,
extraction, lifecycle, evidence. Six adjacent jobs belong elsewhere.

| Adjacent job | Route to |
| --- | --- |
| One ordinary MicroDot, no batch, no missing capability | single-dot authoring |
| Blank, stale, or service-unreachable dot | blank-dot diagnosis |
| "Is this change done" with no batch or catalog claim | workspace verification |
| How a dot looks | design |
| Port a named app or a named feature whole | porting |
| Publish to a real environment | deployment |

Resolve each route at the moment you need it, not up front, and in this order.

1. List the checkout's own `.claude/skills/`. Prefer a match there — it is
   versioned alongside the code it describes.
2. Otherwise use an installed plugin skill. The `bespoke-agentics` plugin
   conventionally covers all six. Do not assume its inventory: name the skill you
   are routing to and let the model's own skill list confirm it exists.
3. If neither is available, say so plainly and continue under this suite's rules.
   Never cite a skill you did not confirm.

Record which provider you chose. This suite carries the compiler, boundary and
browser rules it needs, so a missing neighbour narrows scope rather than
threatening correctness. Deployment is always a separately requested operation,
never implied by generation or verification.
