# Candidate and extraction record

Use a compact record per behavioral fragment, not per matching file. Keep large
source inventories out of the main response. Plans and decisions normally belong
in the repository wiki; use a user-specified permitted location when scope limits
writing there. No required artifact may expand a read-only or skills-only task.

Each candidate carries:

- Stable ID, human name, behavior and demonstrated/current prospective consumers.
- Source repository, selected revision, dirty-input hashes if applicable, precise
  file:line/symbol references and relevant license/attribution facts.
- Inputs/outputs, state/persistence, UI states and error behavior; hidden session,
  environment, global store and platform dependencies that extraction must remove.
- Existing reuse/capability match and why configuration/import alone is insufficient.
- Proposed destination: shared import, copy-adapt fragment, capability, shape,
  backend primitive, connector or whole MicroDot; expected Platform exposure.
- Adaptations, omissions, compatibility concerns, estimated effort range with
  assumptions, and evidence still needed. Code-derived UI claims are labeled as
  such until an actual browser journey is observed.
- Disposition: proposed, selected, rejected, deferred, extracted, verified or
  blocked; record the user's actual selection and later design changes.

Rank a small actionable shortlist by likely reuse and cost to establish a clean
boundary. Include high-value candidates that need substantial work when relevant;
do not let ease of copying stand in for usefulness.

At extraction, bind the record to the exact source identity and resulting public
contract/catalog identity. Retain provenance without copying credentials, user
data or proprietary content outside the requested work. Runtime Catalog provenance
supports only its declared `repo` or `workbench-run` shapes; keep richer extraction
lineage in this record and supported descriptor provenance, never invented RPC keys.

Refreshing discovery creates a comparison and new candidate decisions. Existing
extracted fragments/presets are independent copies with provenance, not live
mirrors of an upstream repository.
