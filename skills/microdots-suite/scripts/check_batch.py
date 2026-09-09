#!/usr/bin/env python3
"""Read-only batch-plan, identity and resume checks. No scheduling or mutations."""

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path


class Invalid(ValueError):
    pass


def need(condition, message):
    if not condition:
        raise Invalid(message)


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def object_value(value, label):
    need(isinstance(value, dict), f'{label} must be an object')
    return value


def positive(value, label):
    need(type(value) is int and value > 0, f'{label} must be a positive integer')
    return value


def strings(value, label, nonempty=False):
    need(isinstance(value, list), f'{label} must be a list')
    need(all(isinstance(x, str) and x.strip() for x in value),
         f'{label} must contain nonempty strings')
    need(len(value) == len(set(value)), f'{label} contains duplicates')
    need(not nonempty or len(value) > 0, f'{label} must not be empty')
    return value


def hashes(value, label):
    value = object_value(value, label)
    need(bool(value), f'{label} must not be empty')
    for path, sha in value.items():
        need(isinstance(path, str) and path.strip(), f'{label} has an empty path')
        need(isinstance(sha, str) and re.fullmatch(r'[0-9a-f]{64}', sha),
             f'{label}: invalid SHA-256 for {path}')
    return value


def mismatches(entries, base):
    result = []
    for name, expected in entries.items():
        path = (base / name).resolve()
        try:
            actual = digest(path)
        except (OSError, ValueError):
            result.append(f'missing or unreadable file: {name}')
            continue
        if actual != expected:
            result.append(f'changed file: {name}')
    return result


def validate_plan(plan, base):
    object_value(plan, 'plan')
    need(type(plan.get('version')) is int and plan['version'] == 1, 'plan version must be 1')
    need(isinstance(plan.get('id'), str) and plan['id'].strip(), 'plan id is required')
    limits = object_value(plan.get('limits'), 'limits')
    for key in ('concurrency', 'max_attempts', 'task_timeout_seconds'):
        positive(limits.get(key), f'limits.{key}')
    items = plan.get('items')
    need(isinstance(items, list) and items, 'items must be a nonempty list')
    by_id, roots, tags, ports = {}, [], set(), set()
    for item in items:
        object_value(item, 'item')
        ident = item.get('id')
        need(isinstance(ident, str) and re.fullmatch(r'[a-z][a-z0-9-]*', ident),
             'item id must be lower-kebab')
        need(ident not in by_id, f'duplicate item id: {ident}')
        need(item.get('kind') in ('application', 'reference', 'extension', 'extraction', 'management'),
             f'{ident}: unknown kind')
        workspace = item.get('workspace')
        need(isinstance(workspace, str) and workspace.strip(), f'{ident}: workspace required')
        root = (base / workspace).resolve()
        for other_id, other in roots:
            need(root != other and root not in other.parents and other not in root.parents,
                 f'overlapping workspaces: {ident} and {other_id}')
        roots.append((ident, root))
        strings(item.get('depends_on'), f'{ident}.depends_on')
        hashes(item.get('inputs'), f'{ident}.inputs')
        strings(item.get('required_evidence'), f'{ident}.required_evidence', nonempty=True)
        item_tags = strings(item.get('tags', []), f'{ident}.tags')
        need(not tags.intersection(item_tags), f'{ident}: tag collision')
        tags.update(item_tags)
        item_ports = item.get('ports', [])
        need(isinstance(item_ports, list) and
             all(type(p) is int and 1 <= p <= 65535 for p in item_ports),
             f'{ident}: invalid ports')
        need(len(item_ports) == len(set(item_ports)) and not ports.intersection(item_ports),
             f'{ident}: port collision')
        ports.update(item_ports)
        by_id[ident] = item
    for ident, item in by_id.items():
        need(all(d in by_id and d != ident for d in item['depends_on']),
             f'{ident}: unknown or self dependency')
    pending, ordered = set(by_id), []
    while pending:
        wave = [i for i in by_id if i in pending and
                all(d in ordered for d in by_id[i]['depends_on'])]
        need(bool(wave), 'dependency cycle')
        ordered.extend(wave)
        pending.difference_update(wave)
    return by_id, ordered


def check(plan_path, state_path=None):
    raw = plan_path.read_bytes()
    plan = json.loads(raw)
    base = plan_path.parent
    by_id, ordered = validate_plan(plan, base)
    plan_sha = hashlib.sha256(raw).hexdigest()
    state = {} if state_path is None else json.loads(state_path.read_bytes())
    object_value(state, 'state')
    if state_path is not None:
        need(type(state.get('version')) is int and state['version'] == 1, 'state version must be 1')
        need(state.get('plan_sha256') == plan_sha, 'state belongs to a different plan identity')
    records = object_value(state.get('items', {}), 'state.items')
    need(not set(records).difference(by_id), 'state contains unknown items')
    stale, statuses, attempts = {}, {}, {}
    for ident, item in by_id.items():
        record = object_value(records.get(ident, {}), f'{ident} state')
        status = record.get('status', 'pending')
        need(status in ('pending', 'running', 'succeeded', 'failed', 'blocked'),
             f'{ident}: unknown status')
        count = record.get('attempts', 0)
        need(type(count) is int and 0 <= count <= plan['limits']['max_attempts'],
             f'{ident}: invalid attempt count')
        need(status not in ('running', 'succeeded', 'failed') or count > 0,
             f'{ident}: executed state requires an attempt')
        statuses[ident], attempts[ident] = status, count
        problems = mismatches(item['inputs'], base)
        if status == 'succeeded':
            evidence = object_value(record.get('evidence'), f'{ident}.evidence')
            for criterion in item['required_evidence']:
                entry = object_value(evidence.get(criterion), f'{ident} evidence {criterion}')
                path, sha = entry.get('path'), entry.get('sha256')
                need(isinstance(path, str) and path.strip(), f'{ident}: evidence path required')
                problems.extend(mismatches(hashes({path: sha}, f'{ident} evidence'), base))
            problems.extend(mismatches(hashes(record.get('outputs'), f'{ident}.outputs'), base))
        if problems:
            stale[ident] = problems
    reusable, blocked, running, ready = [], {}, [], []
    for ident in ordered:
        dependencies = by_id[ident]['depends_on']
        unmet = [d for d in dependencies if d not in reusable]
        status = statuses[ident]
        if unmet:
            blocked[ident] = ['dependency not verified: ' + d for d in unmet]
        if ident in stale:
            blocked.setdefault(ident, []).extend(stale[ident])
        if status == 'running':
            running.append(ident)
            blocked.setdefault(ident, []).append('reconcile the owned worker before resume')
        if ident in blocked:
            continue
        if status == 'succeeded':
            reusable.append(ident)
        elif status == 'blocked':
            blocked[ident] = ['resolve recorded blocker before changing state']
        elif attempts[ident] >= plan['limits']['max_attempts']:
            blocked[ident] = ['attempt limit reached']
        else:
            ready.append(ident)
    need(len(running) <= plan['limits']['concurrency'], 'running items exceed concurrency limit')
    capacity = max(0, plan['limits']['concurrency'] - len(running))
    return {
        'valid': True, 'plan_sha256': plan_sha, 'identity_current': not stale,
        'ready': ready[:capacity], 'waiting_capacity': ready[capacity:],
        'running': running, 'reusable': reusable, 'blocked': blocked, 'stale': stale,
        'all_succeeded': len(reusable) == len(by_id),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('plan', type=Path)
    parser.add_argument('--state', type=Path)
    args = parser.parse_args()
    try:
        result = check(args.plan.resolve(), args.state.resolve() if args.state else None)
        code = 0 if result['identity_current'] else 2
    except (Invalid, OSError, ValueError, TypeError, RecursionError) as error:
        result, code = {'valid': False, 'error': str(error)}, 1
    print(json.dumps(result, indent=2, sort_keys=True))
    return code


if __name__ == '__main__':
    sys.exit(main())
