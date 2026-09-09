# microdots-creator

Framework-owner workflows for a MicroDots checkout (Effect v4 + Foldkit custom
elements). Six coordinated skills covering batch generation, compiler and catalog
extension, reusable-fragment extraction, runtime Catalog lifecycle, and
completion evidence.

This plugin operates **on** a MicroDots repository resolved from the working
directory. It ships no framework code and never treats its own files as a target.

## Skills

| Skill | Owns |
| --- | --- |
| `microdots-suite` | Router. Read once per run, then load one worker skill. Owns the shared working contract, batch protocol and source map. |
| `microdots-generate` | Resumable batch generation through the compiler or reference-dot scaffolding, with dependency order and isolated subagents. |
| `microdots-extend` | Compiler shapes, capabilities, backend UI primitives, data connectors, reusable components, shared runtime primitives — through to Platform exposure. |
| `microdots-extract` | Reuse discovery across the checkout and selected external repos: ranked candidates, user selection, then adaptation. |
| `microdots-manage` | Existing artifacts and runtime Catalog lifecycle: identity, versions, compatibility, deprecation, retirement, reinstatement. |
| `microdots-verify-local` | Completion evidence bound to exact identity: builds, tests, invariant audit, visible browser, catalog usability. |

Start at `microdots-suite` for anything spanning more than one of these, or when
the right workflow is unclear.

## Scope boundary

This suite covers framework-owner work. Four adjacent jobs belong elsewhere, and
the router discovers whichever provider the workspace actually has:

| Job | Provider |
| --- | --- |
| Single ordinary MicroDot | checkout `.claude/skills/new-micro/`, or `bespoke-agentics:microdots-new-micro` |
| Blank / stale / unreachable dot | checkout `.claude/skills/debug-blank-microdot/`, or `bespoke-agentics:microdots-debug-blank` |
| Plain workspace verification | checkout `.claude/skills/verify/`, or `bespoke-agentics:microdots-verify` |
| Deployment | checkout `.claude/skills/deploy/`, or `bespoke-agentics:microdots-deploy` |
| Visual and design work | `impeccable-microdots` |
| Porting a whole app or feature | `bespoke-agentics:microdots-port-app` / `microdots-port-feature` |

Descriptions on both sides are written to keep these apart, so this plugin and
`bespoke-agentics` can be installed together. A missing neighbour degrades scope,
not correctness — this suite carries the compiler, boundary and browser rules it
needs.

## Prerequisites

| Requirement | Why |
| --- | --- |
| A MicroDots framework checkout | Every operation targets one; the plugin resolves it from the working directory. |
| `bun` | The repository's own generator, catalog and check scripts. |
| `python3` (stdlib only) | The bundled batch checker. No third-party packages. |
| A visible browser | Verification defaults to visible-browser evidence. Headless is supplemental, not sufficient. |
| Rig MCP tools | Optional. Speeds indexed graph queries during extraction; `rg` is the documented fallback. |

## Batch checker

`skills/microdots-suite/scripts/check_batch.py` validates a batch `plan.json`
against an optional `state.json`: schema, ID format, workspace overlap and
symlink aliasing, tag and port collisions, dependency cycles, attempt ceilings,
and SHA-256 identity of every declared input, output and evidence file.

```sh
python3 "${CLAUDE_PLUGIN_ROOT}"/skills/microdots-suite/scripts/check_batch.py /absolute/run/plan.json
python3 "${CLAUDE_PLUGIN_ROOT}"/skills/microdots-suite/scripts/check_batch.py /absolute/run/plan.json --state /absolute/run/state.json
```

Read-only — it prints a JSON report to stdout and writes nothing. Paths inside
the plan resolve against the plan file's own directory, so the ledger can live
anywhere.

| Exit | Meaning |
| --- | --- |
| 0 | Valid, and every declared identity is current |
| 1 | Invalid or unreadable plan/state |
| 2 | Structurally valid, but inputs/outputs/evidence changed or went missing |

Tests: `PYTHONDONTWRITEBYTECODE=1 python3 "${CLAUDE_PLUGIN_ROOT}"/skills/microdots-suite/scripts/test_check_batch.py`

## Source map staleness

`skills/microdots-suite/references/source-map.md` indexes the repository's
compiler, authoring, Workbench, Catalog and Platform interfaces by `file:line`.
It is a snapshot of one checkout, shipped in a plugin that versions independently
of the repository it describes. A miss is expected, not an error — the file's
"When an anchor misses" section defines the recovery order and requires that any
`file:line` in a report comes from the current run.

## Installation

```sh
claude --plugin-dir /path/to/microdots-creator
```

Or via the Bespoke Agentics marketplace, where it is registered as
`microdots-creator`.

## Provenance

Ported from `MicroDots/.agents/skills/` (authored 2026-09-08 against the OpenAI
Agents runtime; each skill retains its `agents/openai.yaml` for cross-runtime
parity, which Claude Code ignores). The port changed install-location claims,
script invocation paths, the neighbouring-skill routing, the invariant-auditor
dispatch, and all six skill descriptions. Skill bodies and reference content are
otherwise unchanged.
