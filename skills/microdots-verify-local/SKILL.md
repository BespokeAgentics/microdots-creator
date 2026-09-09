---
name: microdots-verify-local
description: Produce completion evidence for MicroDots framework-owner work: bind builds, tests, invariant audit, visible-browser behavior and exact local Platform catalog usability to a specific source, selection, lock and build identity, then report every acceptance criterion as passed, failed, blocked or not applicable. Use to close out a generation batch, a framework extension or an extraction, and whenever a catalog entry must be proven selectable and mountable rather than merely rendered. A plain "is this workspace change done" check, with no batch, extension or catalog claim, belongs to the workspace's own verification skill.
---

# Verify a local MicroDots result

Read the [working contract](../microdots-suite/references/working-contract.md) and
[evidence guide](references/evidence-guide.md). Scale checks to the changed surface
while retaining every acceptance criterion the user requested.

Bind verification to exact source, selection, compiler/catalog lock, output receipt
and build identity. Separate historical evidence from current runs. For source
diffs affecting silent-failure boundaries, run a bounded read-only invariant audit
before browser verification. Look for an invariant-auditor agent the checkout
owns — conventionally `.claude/agents/invariant-auditor.md` — and dispatch it as a
subagent. This plugin deliberately ships no copy: that agent encodes one
repository's `AGENTS.md` invariants, and a bundled duplicate would drift from
them silently. If no such agent exists or delegation is unavailable, perform the
scoped audit directly against the checkout's own invariant documentation and
state that limit in the evidence report. Include new/untracked files in scope.

Run appropriate compiler structural checks, tests, type/lint checks and builds.
For framework-wide changes run required repository checks; generated outputs use
their own workspace checks. Do not repair unrelated failures or relax assertions
to manufacture a pass. Identify baseline failures separately.

Use visible headed Chrome or an available visible browser interface. Verify each
MicroDot's primary behavior using DOM and service/RPC evidence, then relevant
reload/persistence, polling, attributes/events or host wiring. A screenshot,
listening port, green build or preview status alone does not prove the journey.
Do not impose polling on deliberately stateless or event-only components.

After primary behavior passes, register only requested builds through
[microdots-manage](../microdots-manage/references/catalog-lifecycle.md), then verify
the exact version and actual Platform selection/usability. Compiler extensions
must be selectable in authoring and consumed by a fresh build. Do not invent a
Platform `/catalog` page: discover the current surface from topology/UI.

Keep cleanup scoped to services, browser contexts and data owned by this run.
Never free a port by stopping an unknown process. If a canonical port is occupied,
reuse a compatible authorized service or use a configured isolated environment;
host origins/CORS and served bundle paths must also match.

Report each criterion as passed, failed, blocked or not applicable with a reason
and evidence pointer. A missing visible browser session or unreachable generated
bundle leaves completion open. Headless runs are useful supplemental evidence
but do not satisfy this suite's agreed visible-browser default.
