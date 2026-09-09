# Scoped local Catalog operations

Current source anchors are in the [source map](../../microdots-suite/references/source-map.md).
Re-read the public contracts before mutation. Compiler authoring catalog entries
and runtime built-MicroDot Catalog records have different owners and lifecycles.

## Register only the requested builds

There is currently no scoped registration CLI. `bun run catalog:scan` discovers
all top-level `microdots/*/dist/*.manifest.json`, registers them and makes every
non-retired result available. Do not use it to register a selected batch.

Use the public `CatalogRpcs` with the exact emitted `MicroDotManifest`, decoded
through its schema. Reuse the NDJSON HTTP transport in `scripts/catalog-scan.ts`
without invoking its broad `scanCatalog` loop. The operation shapes are:

```ts
const registered = yield* client.registerBuild({
  writeKey,
  manifest,
  provenance: { _tag: 'repo', manifestPath },
})
// Separately select this exact verified version when readiness is in scope:
yield* client.makeAvailable({
  writeKey,
  name: registered.microdot.name,
  versionId: registered.versionId,
})
const current = yield* client.get({ name: registered.microdot.name })
```

Use `RpcClient.make(CatalogRpcs)` with `RpcClient.layerProtocolHttp({url:
baseUrl + '/rpc'})`, `FetchHttpClient.layer`, `RpcSerialization.layerNdjson`,
and `Effect.scoped`, matching the current source. Plain JSON fetch calls are not
a substitute for this transport. The usual local endpoint is `localhost:3122`;
verify service configuration. Read `CATALOG_WRITE_KEY` from configured server-side
environment without putting its value in arguments, logs, artifacts or prompts.
Missing credentials block publication, not already completed generation.

`manifestPath` must truthfully identify the emitted file in the source repository
or generated workspace; prefer stable relative paths with the repository/workspace
recorded in run lineage. Do not invent `external`, `batch`, license or commit fields
on the wire. Provenance is only `{_tag:'repo',manifestPath}` or
`{_tag:'workbench-run',appId,runId}`. Preserve richer source/extraction lineage in
the run record. Never fabricate Workbench app/run identities.

Preserve the submitted manifest and returned `versionId`/revision. Registration
uses canonical full-manifest identity, not just bundle hash. Same manifest and
provenance is idempotent. A later deployed-URL annotation can change stored manifest
data without changing that ID; do not derive an identity by hashing later readback.

## Workbench-owned builds

Use the existing green-build publication outbox for real Workbench runs. It records
the exact manifest and app/run provenance, retries transient failures and preserves
publication identity. Inspect/reconcile that state before attempting registration
again. A publication failure is not a reason to repeat the completed build.

Readiness uses Workbench `markReady({appId,expectedVersion,author})`, which checks
the exact previewed green run, current spec version and active-build state. Do not
bypass it with direct Catalog `makeAvailable` for a Workbench-owned app. Current
`bun run catalog:proof ready <app-id>` invokes readiness; the bare `catalog:proof`
command creates a canned proof application and is not a generic registration tool.

## Lifecycle decisions

| Action | Current meaning and constraints |
| --- | --- |
| Register build | Adds history; a new record starts `registered`, with no available version. Appending a version does not change the current selection |
| Select available version | `makeAvailable` selects the exact registered ID; refuses retired records and versions that drop tags from the current selection |
| Inspect latest/in-flight | `get` exposes history; `list({view:'in-flight'})` shows newest unselected non-retired version. `list({view:'catalog'})` can still show an older available version |
| Inspect placeable | `list({view:'placeable'})` exposes available selections, not every registered build |
| Replace/rollback | Select an already registered target ID after compatibility checks. Dropped-tag rules can also forbid a rollback |
| Retire | `retire({writeKey,name})` retains history, selected version and permanent tag ownership; prevents new placements while existing ones may remain |
| Reinstate | `reinstate({writeKey,name})` restores the previously selected available version, not the newest version |
| Deprecate/delete/rename/reassign tags | No equivalent general runtime RPC currently exists; an advisory migration recommendation must not masquerade as a new lifecycle state |

Before retirement, check whether an available version was ever selected. Current
`reinstate` refuses a retired record with no available version, while `makeAvailable`
also refuses retired records. Do not offer retire-then-undo for that case. Explain
the concrete unsupported recovery before any such mutation; choose a supported
requested alternative or obtain a decision on the actual irreversible effect.

## Availability and Platform usability

The default generated-batch outcome includes local usability. Once primary runtime
proof passes, make the exact version available through its owning path when that
is part of the requested outcome. Registration alone is complete only for an
explicit registration-only request. Read back the exact result before a retry.

The Platform currently exposes placeable runtime entries through `/pages` Add;
its authoring building blocks use Workbench catalog/schema selection. There is no
Platform `/catalog` route in the inspected checkout. The reference host's
`http://localhost:5173/#/catalog` is useful for history, but is not itself Platform
placement proof. Discover actual current URLs and controls before interacting.

Registering a manifest does not serve its bundle or service. Local bundle
middleware normally reads `MICRODOT_BUNDLE_ROOT/<child>/dist/<file>`. External
generated workspaces require a real compatible serving/registry arrangement.
Configure an isolated authorized host/runtime or reuse a supported existing flow;
do not move compiler output into repository-reference source just to make a URL
work. If the serving/exposure path needs unapproved application changes, report
that specific blocker and prepare the extension proposal.
