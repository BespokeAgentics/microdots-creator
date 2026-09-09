# Evidence guide

## Bind the claim

Record source revision and relevant dirty inputs, semantic selection/spec, compiler
and catalog-lock identity, generated receipt, emitted manifest/version, target,
URL and verification time. Keep evidence scoped to that identity. Rebuilding,
relocking or changing source invalidates affected proof; a summary file cannot
make old screenshots prove new bytes.

For batches, use per-item records and a coordinator-owned index. A useful record
contains criterion, observed action/result, verdict, identity, artifact paths and
known limitations. Hash receipts/logs/screenshots for resume integrity. Hashes
preserve evidence identity; they do not independently verify its claims.

## Meaningful checks

| Surface | Evidence |
| --- | --- |
| Application compiler | Public selection/schema/compile and structural verify succeed with matching pins/receipt |
| Code and bundles | Appropriate generated/repository checks, focused behavioral tests, final build; self-contained bundle and correct target imports |
| Visible primary journey | Open real UI in visible Chrome/browser, operate meaningful controls and correlate DOM with actual service/RPC results |
| Persistence, when present | Write a distinguishable record, reload and read it back; restart the owned service when durability is part of the promise |
| Refresh, when present | Observe an actual poll or brokered update; prove the fallback when broker independence is claimed |
| Attributes/events/composition | Set meaningful attributes, observe outbound events/host-mediated effects and independent mounts when applicable |
| Auth/errors/connectors | Missing/invalid credentials fail closed, errors are intelligible, fixture/live evidence is explicit; never claim a live connector based on fixtures |
| Compiler extension | Find/select the new entry and real parameter controls in Platform authoring, compile a fresh consumer and exercise its behavior |
| Runtime Catalog | Register exact manifest, read exact version back, select availability through owning path, find/select through Platform placeable surface and exercise actual mount |

Some checks are inapplicable: a stateless markdown transformation need not poll,
and a layout-only change need not invent a database. Document why a criterion is
not applicable; do not omit an explicit user requirement by changing the profile.

## Browser and resource handling

Use available browser tools and discover actual routes/listeners. Visible headed
Chrome is the suite default. A headless script or virtual display is labeled
accurately and cannot silently replace the requested visible session. Reuse the
repository's relevant browser proof scripts only after inspecting their side
effects, selected target, headless mode and fixture/live configuration.

Preview must both listen and render. Inspect the currently attached DOM, not a
detached mount node replaced by the runtime. Capture observable behavior and
request results along with screenshots. Blank output with a clean console can
be a swallowed startup defect: use the relevant blank-MicroDot skill and scoped
Foldkit diagnostics before adding arbitrary logging.

Shared developer services belong to their owner. A requested verification does
not authorize killing them, changing their configuration or wiping their data.
Use run-owned test records/hosts and resource leases where possible. Retain
uncertain or failed cleanup evidence; do not declare resources removed merely
because the original parent process exited.

## Closeout

Report passed, failed, blocked and not-applicable criteria for each item with
evidence and next action. Keep local build/browser/catalog proof distinct from
production deployment. If only skill syntax, helper behavior or dry-run decisions
were tested, describe precisely that scope rather than claiming end-to-end
MicroDot generation was exercised.
