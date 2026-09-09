# Extension surfaces

Use the [source map](../../microdots-suite/references/source-map.md) to relocate
current definitions. Choose by executable role, not by the generic word component.

| Building block | Authoritative input | Required consumer proof |
| --- | --- | --- |
| Shared runtime primitive | Platform-appropriate implementation and `packages/microdots-runtime/package.json` export map | A real importing MicroDot; browser bundle cannot acquire server code; authoring adapter if Platform-selectable behavior is required |
| Frontend shape | Source reference dot, `template.json`, source enumeration in `scripts/generate-authoring-catalog.ts` | Regenerated source digest/pin, current shape vocabulary/generated-front mapping, fresh compiled and rendered consumer |
| Capability | `packages/microdots-capability-catalog/capabilities/<id>/definition.ts` and declared materialization source | Parameters/targets/contributions resolve and generated behavior actually executes |
| Backend UI primitive | `packages/microdots-backend-catalog/primitives/<ref>/definition.ts` plus real compiler support | Binding/operation kinds/layout constraints and actual emitted backend UI, not descriptor-only visibility |
| Data connector | Capability definition, connector schema, service factory, RPC and generated UI materialization | Declared request/response/error behavior, fixture and live modes distinguished, relevant target and secret handling |
| Copy-adapt fragment | Its owned source and feature-keyed entry in `docs/reuse-catalog.md` | Adapted consumer with documented changes; no false promise that it is a compiler-selectable entry |

The current public-API connector schema in
`packages/microdots-authoring/src/connector.ts` is deliberately narrow: public
unauthenticated HTTPS GET, zero-input operation objects, one attempt and a backend
record-reader surface. Credentialed operations, writes, pagination, arbitrary
inputs and domain-store substitution need explicit schema/compiler/runtime design
if still unsupported. Do not present fixture data as a live integration.

Use `connector.github-public-repository/definition.ts` as full-stack prior art,
but inspect current target/evidence rows. `scripts/proof-public-api-connector.ts`
currently defaults to a fixture and headless browser; running it does not satisfy
visible-browser or real-provider proof.

## Generate rather than patch outputs

`bun run catalog:generate` regenerates source-backed descriptors, digests, barrels,
snapshot and lock. `bun run catalog:check` verifies the same outputs without
rewriting them. Inspect the generated diff; this is a shared repository mutation,
not a per-worker command to run concurrently. Keep compiler version and snapshot/
lock identity coherent, including `authoringVersion.ts` when semantics/output change.

New shape vocabulary may need `ShapeKind`/`ShapeRef` and generated-front mapping.
New backend vocabulary may need materializer dispatch: current code explicitly
handles certain primitive refs. Current recipe compilation also limits distinct
pinned source shapes; inspect its diagnostic before promising arbitrary composition.

## Acceptance and migration

- Validate deterministic generation and check mode, supported parameter/target
  combinations, malformed inputs and meaningful unsupported combinations.
- Build a fresh consumer through the public authoring surface; test behavior and
  error handling, then visible Platform authoring/preview and relevant persistence.
- For an existing definition, compare old and new selected consumers and document
  compatibility, version changes, migration requirements and rollback constraints.
- Keep old lock refusal honest. An explicit migration can update pins; retrying a
  failed old selection is not permission to silently rebind it to new semantics.

The runtime Catalog accepts whole emitted MicroDot manifests. Adding a runtime
primitive, compiler capability or reuse document to that Catalog is not a valid
substitute for authoring exposure. If current Platform controls cannot expose the
entry, the extension remains incomplete until the reviewed exposure work passes.
