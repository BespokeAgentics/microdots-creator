# Shared working contract

Read once per suite run. These defaults were selected by the framework creator
in the requirements interview on 2026-09-08; a later task can narrow or override
them. The suite ships as the `microdots-creator` plugin; its own files live under
`${CLAUDE_PLUGIN_ROOT}` and are never the target of the work it performs.

The suite targets a MicroDots framework checkout. Resolve that repository root
from the working directory, not from this plugin's location, and confirm it is a
MicroDots repository before acting. Every repository path, script and command
named in these references is an anchor to verify against the live checkout, not
a guarantee. When an anchor misses, discover the current one and say so; never
invent a path to make an instruction fit.

## Agreed behavior

- Generate multiple MicroDots with isolated subagents and one shared integration
  coordinator. Propose concurrency, total-attempt, time and resource limits in
  the batch plan; allow overrides, then operate within the announced limits.
- Default completion: built, tested, visibly verified, registered in the local
  Platform catalog and demonstrably usable through the appropriate Platform flow.
- Author compiler shapes, capabilities, backend UI primitives, data connectors,
  reusable UI components and shared runtime primitives. Cover inspect/update/test,
  version/compatibility/replacement, deprecation/retirement/reinstatement workflows.
  A requested workflow may reveal a missing platform operation; do not pretend
  the skill implements that operation merely by describing it.
- Propose a missing shared extension for review, implement it once after review,
  verify, and resume dependent items. Continue unrelated items while blocked.
- Preserve verified successes after partial failure; bounded retries and resume
  must not repeat valid completed work.
- Scan the target repository and selected external code repositories. Present ranked
  candidates with provenance, dependencies and adaptation costs; extract the
  candidates selected by the user.
- Reuse relevant existing guidance in the checkout and in other installed
  plugins rather than replacing it. This suite owns framework-owner work:
  batches, compiler and catalog vocabulary, extraction, lifecycle. Single-dot
  authoring, blank-dot debugging, deployment and design remain with whichever
  skills the workspace already provides.

## Establish current context

Read applicable `AGENTS.md`, `docs/reuse-catalog.md` and the relevant wiki pages;
start at `wiki/framework/_index.md` when framework context is missing. Code is
authoritative for behavior, wiki for decisions/rationale. Check current scripts,
contracts and exports; do not hardcode dependency versions from this suite.
Use Rig light tools for indexed graph questions and its required bootstrap. Heavy
Rig tools belong in a subagent; if unavailable or rejected, use ordinary source
reads without attempting to bypass the tool boundary.

Record the run's allowed writes and baseline dirty files. Protect another agent's
work; use a deliberate source snapshot/worktree for shared-source changes. A new
worktree from HEAD omits uncommitted prerequisites: make the chosen baseline
explicit and transfer only authorized prerequisites with verifiable identity.
Source fingerprints should name the compiler/catalog plus any dirty inputs that
affect the output. Never stash, reset, clean, or commit unrelated changes.

Documentation follows current scope. Normal framework implementation records
decisions/reuse changes in `wiki/` using its schema. A skills-only or read-only
request does not authorize wiki or application edits. Explain a proposed scope
change before doing that work; do not interpret this suite as overriding the user.

## Boundaries that change decisions

- **Application lane:** semantic selection and catalog-locked compiler own source
  output. Fix inputs/definitions through their owning lane; no hand repairs to
  generated source, unrequested host integration or hidden framework extensions.
- **Repository extension lane:** owns approved source/reference integration;
  one coordinator handles aliases, registry, host markup/topology, shared catalog
  outputs and workspace lockfile changes. Generated scaffolds alone are unfinished.
- **Compiler catalog versus runtime Catalog:** descriptors/snapshots make building
  blocks selectable by the compiler. Emitted manifests register built MicroDots
  and their lifecycle. One operation does not substitute for the other.
- **Runtime invariants:** each MicroDot owns its stack; only contract crosses its
  boundary. Hosts import no MicroDot implementation. Configuration is attributes,
  cross-dot communication is host-brokered, and each bundle includes its CSS.
  Use platform-appropriate runtime exports, `defineMicroDot`/mount identity,
  service-provided bindings, typed D1 failures and fail-closed secrets.
- **Approval and lineage:** preserve actual actor/selection provenance and immutable
  plan/spec/run/manifest identity. Workbench approval and readiness checks must use
  the owning service, including compare-and-set gates. Do not fake a human click,
  rewrite stored approval state, or reconstruct missing evidence from expectations.
- **Resources:** secrets remain server-side and out of prompts, evidence and source
  records. Reuse configured credentials without printing them. Bound paid calls
  by actual task authorization; never select a paid fallback silently. Cleanup
  only resources this run owns. Repeated auth/unsupported failures are not retryable.

## Completion reporting

Separate implementation, structural checks, visible runtime behavior and catalog
usability. State the identity each proof covers. Preserve per-item blocked/failed
states and make the next action concrete. A skill delivery or dry-run evaluation
does not establish that a real MicroDot was generated, published or deployed.
