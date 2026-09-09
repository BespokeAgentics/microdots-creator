# Batch plan and recovery protocol

The coordinator owns scheduling, approvals, integration and the durable run
record. The bundled `check_batch.py` is a read-only integrity/readiness check, not
a worker launcher, approval service, process supervisor or proof judge.

## Plan and isolation

Use a permitted run directory outside worker outputs. Normal framework plans
belong in `wiki/plans/active/`; the run's machine-readable state and evidence can
live in a scoped QA/run directory. Honor a narrower user-defined write scope.
Do not put credentials in plans or fingerprints. Capture selected sources and
dirty prerequisites deliberately; a fresh worktree from HEAD is not the dirty
checkout the user is looking at.

Write `plan.json` before dispatch. The following is a schema illustration, not a
copy-ready approved plan; substitute actual paths, hashes, limits and requirements:

```json
{
  "version": 1,
  "id": "inventory-batch",
  "limits": {"concurrency": 2, "max_attempts": 2, "task_timeout_seconds": 600},
  "items": [{
    "id": "inventory",
    "kind": "application",
    "workspace": "outputs/inventory",
    "depends_on": [],
    "ports": [],
    "tags": [],
    "inputs": {"inputs/inventory-selection.json": "actual-sha256"},
    "required_evidence": ["build", "tests", "browser", "catalog"]
  }]
}
```

Each item owns a disjoint workspace and stable lower-kebab ID. `kind` is
`application`, `reference`, `extension`, `extraction` or `management`. Dependencies
form an acyclic graph. Reserve known tags/ports; empty arrays mean unassigned,
not collision-free. Discover actual compiler/scaffold identities and reserve them
through the coordinator before concurrent runtime work. The checker does not
probe live ports. If runtimes cannot be isolated, serialize them.

`inputs` maps files to actual SHA-256 values. Include semantic brief/selection,
catalog snapshot/lock, compiler/source identity and prerequisite artifacts that
determine the output. A source manifest is useful for many files, but its own
hash alone does not verify the files it describes: reconcile that manifest too.
All paths, including state evidence/output paths, resolve relative to the plan
directory, regardless of the state file's location. Canonical workspace checks
detect overlapping/nested destinations and symlink aliases.

Additional plan fields can record task scope, baseline, acceptance narratives,
actual review references, allowed tools/write paths, costs, per-step time budgets
and coordination ownership. The checker ignores those fields; the coordinator
must enforce them. A review string in JSON is a record, never authorization by
itself. Keep a copy of the plan reviewed for a new shared extension.

## Dispatch and durable state

```sh
python3 "${CLAUDE_PLUGIN_ROOT}"/skills/microdots-suite/scripts/check_batch.py /absolute/run/plan.json
python3 "${CLAUDE_PLUGIN_ROOT}"/skills/microdots-suite/scripts/check_batch.py /absolute/run/plan.json --state /absolute/run/state.json
```

Exit 0: schema/recorded identities pass. Exit 1: invalid plan/state or unreadable
input JSON. Exit 2: structurally valid but listed inputs/evidence/outputs changed
or disappeared. Inspect structured results; independent `ready` items may still
proceed when a different branch is stale. No exit code proves browser behavior.

`state.json` has `version: 1`, the returned `plan_sha256`, and an `items` object
keyed by item ID. Each record has `status` (pending/running/succeeded/failed/blocked)
and `attempts` (total attempts started, never reset on resume). Successful records
also require:

```json
{
  "status": "succeeded",
  "attempts": 1,
  "outputs": {"outputs/inventory/receipt.json": "actual-sha256"},
  "evidence": {
    "build": {"path": "proof/inventory-build.json", "sha256": "actual-sha256"},
    "tests": {"path": "proof/inventory-tests.json", "sha256": "actual-sha256"},
    "browser": {"path": "proof/inventory-browser.json", "sha256": "actual-sha256"},
    "catalog": {"path": "proof/inventory-catalog.json", "sha256": "actual-sha256"}
  }
}
```

Include actual output files or a separately reconciled full output manifest;
hashing a receipt alone cannot detect arbitrary later edits to output files.
Retain phase results, exact catalog version and resource leases even for failed
items, so publication retries do not repeat compilation or browser work.

Only the coordinator changes canonical state. Write an atomic replacement in the
same directory after each transition, preserving prior attempts in a journal or
history field. Record running state/attempt and owned resources before starting a
worker. Workers return their own result files and do not edit shared state.
Bound actual execution with the announced timeout/call/cost limits; the checker
validates numeric limits but cannot enforce elapsed time or kill processes.

## Resume without losing successful work

1. Check live processes/leases and service identity. A stored running item is not
   an invitation to start a duplicate worker. Cancel/reap only owned resources or
   retain a blocker when ownership/cleanup is uncertain.
2. Reconcile current source, output, evidence and Catalog/Workbench identities.
   `reusable` means listed file hashes and dependency records match; the operator
   must still establish required live state and truth of the evidence.
3. Respect completed prerequisites and continue `ready` items within capacity.
   Failed items below the attempt limit are candidates for a justified retry;
   blocked items need the actual blocker resolved. Preserve valid successes.
4. Missing capabilities remain explicit reviewed extension prerequisites. When
   the extension lands or intended source changes, write a new plan revision and
   state bound to its hash. Revalidate per-item inputs, outputs and dependency
   closure before carrying forward successes. Preserve old plan/state lineage;
   do not overwrite an expected hash merely to turn a stale result green.
5. Read back catalog state before retrying a timed-out publication. Stop repeated
   auth/refusal loops. Exhausted limits require a revised authorized scope/limit,
   not resetting attempts. Report completed, failed, blocked and running items.

## Maintaining the checker

Run `PYTHONDONTWRITEBYTECODE=1 python3 "${CLAUDE_PLUGIN_ROOT}"/skills/microdots-suite/scripts/test_check_batch.py`
after changing the helper. These controls exercise the public CLI in temporary
directories, including stale inputs/output/evidence, partial failure, running
workers, collisions and plan identity. Their fixture reports are not real
MicroDot build or browser evidence.
