# Generation lanes and collision handling

## Compiler-owned application

Run from the resolved repository root. Catalog query files contain `{}` or a
supported filter such as `{"kind":"capability","query":"repository"}`:

```sh
bun scripts/microdots-authoring.ts inspect-catalog --input catalog-query.json
bun scripts/microdots-authoring.ts schema-for-selection --input partial-selection.json
```

The schema command takes `{"partialSelection": ...}`. Re-query after shape,
target or capability changes. Fill the returned `AuthoringSelectionV1`, including
the correct caller provenance; inspect the current schema rather than inventing
fields or passing a complete wrapper to the wrong command. Degradation requires
the actual consequence acknowledgement, never a fabricated acceptance.

```sh
bun run new:microdot application --input selection.json --destination /absolute/empty-output
```

Here `selection.json` is the selection itself. In contrast, the public
`compile-composition` command takes `{"selection": ..., "destination": ...}`.
The destination must be empty with an existing parent, outside the target repository's
reference-dot directory. Check real paths, including symlinked parents.

Run `verify-workspace` with `{"workspace":"/absolute/output"}`. Keep the raw
selection, exact catalog snapshot/lock identity, compiler receipt and diagnostics.
Use `explain-issue` with `{"diagnostic": ...}` for a compiler refusal. Exit code 2
means a structured refusal/failed check, not successful generation with warnings.

Application generation does not acquire authority for repository aliases, registry,
topology, reference inventory or workspace dependency changes. Install/check/build
the generated workspace as needed in its own directory for runtime verification;
the fact that compilation itself does not install dependencies is not a ban on
the subsequent verification work.

## Repository-owned reference/proof MicroDot

Use this lane only for an explicitly requested repository artifact or reviewed
extension. Consult the workspace's single-dot authoring skill for relevant detail
when one is available — the checkout's own `.claude/skills/new-micro/` or an
installed equivalent such as `bespoke-agentics:microdots-new-micro`. Verify
whatever it says against the current generator's output and these actual paths:

1. The coordinator runs `bun run new:microdot repository name` serially when
   allocating identities. It chooses one past the highest claimed service port.
   Separate worktrees at the same baseline would choose the same port.
2. Complete the domain contract, service and Foldkit behavior. Confirm the bare
   manifest plugin, self-contained CSS, runtime target and any storage migration.
3. Integrate contract aliases in `tsconfig.json` and `vitest.config.ts`, and one
   registry row per element in the intended host. For the reference host that is
   `apps/pitch-deck-website/host/src/registry.ts`, not an assumed `apps/host` path.
4. Match host markup, route data and slot manifest in
   `apps/pitch-deck-website/host/host-topology.json`. Every mount and declared slot
   must have a real matching element. Host value imports of dot implementation
   are forbidden.
5. When deployable, update the expected discovery inventory in
   `microdots/deploy/service/discovery.test.ts`; do not weaken its assertion.
   Respect deliberately Worker-less dots.
6. Run workspace dependency/catalog generation and record wiki/reuse changes only
   through the shared integration owner and within the current task's scope.

A safe parallel reference workflow is serial scaffolding/integration allocation,
then disjoint implementation work with assigned paths. An alternative is isolated
workers returning source patches, with final scaffold identities assigned by the
coordinator before integrated verification. Do not assume a nonexistent CLI port
override. Recheck ports/tags/paths in the final combined workspace.

## Concurrent runtime proof

Compile-time IDs and live listener ports are different resources. Record actual
emitted IDs; do not hand-edit compiler output to invent a private runtime layout.
Use supported runtime configuration or isolated environments, or serialize browser
proof when safe isolation is unavailable. Existing developer processes are not
owned by the batch. Claim/reserve shared resources before launching, release only
after the run's worker and children have stopped, and retain uncertain leases
as blocked for operator reconciliation.
