# Current source map

Verified against the working checkout on 2026-09-08. Line numbers are navigation
anchors, not frozen truths; confirm current definitions before acting, especially
when another agent is changing the compiler or Platform. This reference locates
interfaces; it does not certify their current runtime health.

| Concern | Source anchors and significance |
| --- | --- |
| Application/repository modes | `scripts/new-microdot.ts:80` usage; `:111` application destination guard; `:152` repository allocation. `packages/microdots-generate/src/index.ts` scaffold implementation |
| Public authoring CLI | `scripts/microdots-authoring.ts:63` operations; `:111` input decoding; `:191` usage. `--input` is a JSON file, otherwise stdin |
| Selection vocabulary | `packages/microdots-authoring/src/selection.ts:14`; catalog inspection/schema projection `packages/microdots-authoring/src/operations.ts:72` |
| Source-backed catalog generation | `scripts/generate-authoring-catalog.ts:63` shape sources, `:293` shape pins, `:321` capabilities, `:382` backend primitives, `:581` snapshot/lock, `:627` check mode |
| Lock and compiler compatibility | `packages/microdots-generate/src/resolve.ts:126`; output version policy `packages/microdots-generate/src/authoringVersion.ts:2` |
| Runtime export boundaries | `packages/microdots-runtime/package.json:15`; reuse classification `docs/reuse-catalog.md:9` |
| Connector limits/prior art | `packages/microdots-authoring/src/connector.ts:4`; `packages/microdots-capability-catalog/capabilities/connector.github-public-repository/definition.ts:33` |
| Real materializer consumption | `packages/microdots-generate/src/authoringCompile.ts:3611`; a backend descriptor alone does not prove generated UI |
| Platform authoring entries | `microdots/workbench/service/authoringCatalog.ts:6`; `microdots/workbench/src/contract.ts:2473`; `microdots/workbench/service/bootstrapWizard.ts:1236` |
| Runtime Catalog wire contract | `microdots/catalog/src/contract.ts:28` provenance, `:68` views, `:182` register/select, `:246` reads |
| Runtime version/lifecycle semantics | `microdots/catalog/service/store.ts:339` identity, `:536` registration, `:607` availability, `:849` retirement, `:871` reinstatement |
| Scoped RPC transport precedent | `scripts/catalog-scan.ts:162`; its `scanCatalog` operation at `:109` is broad and also makes entries available |
| Workbench publication/readiness | `microdots/workbench/service/catalogPublisher.ts:110`; `microdots/workbench/service/storeSqlite.ts:4626`; `microdots/workbench/service/handlers.ts:724` |
| Platform runtime catalog selection | `microdots/pages/service/handlers.ts:326`; `microdots/pages/src/inspector/app.ts:2259`; current routes `apps/platform/src/routes.test.ts:70` |
| Reference catalog browser | `apps/pitch-deck-website/host/host-topology.json:312`; this is a reference-host surface, not a Platform `/catalog` route |
| Local bundle serving | `scripts/serve-microdot-bundles.ts:25`; registration itself serves no bundle or service |

For focused tests, locate the current files before running: `scripts/microdots-authoring.test.ts`,
`scripts/generate-authoring-catalog.test.ts`, `packages/microdots-generate/src/connectorCatalog.test.ts`,
`scripts/catalog-lifecycle.e2e.bun.test.ts`, and the changed dot's tests. Use Vitest
for ordinary `.test.ts`, Bun for `.bun.test.ts`; check root `package.json` for
required repository checks. Do not invoke a lifecycle E2E against a shared service
without checking its fixture and mutation scope first.

## When an anchor misses

This map is a snapshot of one checkout, shipped inside a plugin that upgrades on
a different schedule than the repository it describes. Treat a miss as expected,
not as an error, and never as licence to guess.

A miss is any of: the file does not exist, the symbol is not at the cited line,
or the surrounding code no longer matches the "significance" column. Recover in
this order.

1. Confirm you resolved the right repository root. A wrong root produces a whole
   column of misses at once and is the most common cause.
2. Locate the current definition. Use Rig light tools when the checkout is
   indexed — `rig_search` for the symbol, then `rig_node` to confirm the file —
   and `rg` when it is not. Search the symbol name, not the line number.
3. Act on what you found, citing the anchor you actually verified. A `file:line`
   in a report must come from this run, never copied from the row above.
4. Say so in the run record: which row missed, what replaced it, and whether the
   surrounding contract changed or only moved.

Whole-section drift — several rows in one concern all pointing at renamed or
deleted files — means the interface was restructured, not relocated. Stop and
report it before continuing. Re-deriving one row is navigation; re-deriving a
section is a finding the framework owner needs.

Correcting this file is a normal outcome of a run. Update the rows you verified
and restate the verification date at the top. Do not edit rows you did not check
this run, and do not delete a row merely because you did not need it.
