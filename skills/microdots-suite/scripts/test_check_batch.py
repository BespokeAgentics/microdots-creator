#!/usr/bin/env python3
"""Behavioral CLI controls using temporary fixture evidence, never live services."""

import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


CHECKER = Path(__file__).with_name('check_batch.py')


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


class BatchControls(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='microdots-skill-test-')
        self.root = Path(self.temp.name)
        self.addCleanup(self.temp.cleanup)
        self.plan = {'version': 1, 'id': 'test', 'limits': {
            'concurrency': 2, 'max_attempts': 2, 'task_timeout_seconds': 60}, 'items': []}
        for ident in ('first', 'second', 'third'):
            source = self.root / f'{ident}.json'
            source.write_text(json.dumps({'fixture': ident}))
            self.plan['items'].append({
                'id': ident, 'kind': 'application', 'workspace': f'outputs/{ident}',
                'depends_on': [], 'ports': [], 'tags': [],
                'inputs': {source.name: sha(source)},
                'required_evidence': ['build', 'tests', 'browser', 'catalog'],
            })
        self.state = {'version': 1, 'items': {}}

    def save(self):
        plan_file = self.root / 'plan.json'
        plan_file.write_text(json.dumps(self.plan))
        self.state['plan_sha256'] = sha(plan_file)
        state_file = self.root / 'state.json'
        state_file.write_text(json.dumps(self.state))
        return plan_file, state_file

    def invoke(self, with_state=True, save=True):
        if save:
            self.save()
        args = [sys.executable, str(CHECKER), str(self.root / 'plan.json')]
        if with_state:
            args += ['--state', str(self.root / 'state.json')]
        result = subprocess.run(args, capture_output=True, text=True, timeout=5)
        self.assertEqual(result.stderr, '')
        return result.returncode, json.loads(result.stdout)

    def succeed(self, ident):
        output = self.root / f'{ident}-output.json'
        output.write_text('fixture output, not a compiled MicroDot')
        evidence = {}
        for key in ('build', 'tests', 'browser', 'catalog'):
            path = self.root / f'{ident}-{key}.json'
            path.write_text(json.dumps({'fixture': True, 'criterion': key}))
            evidence[key] = {'path': path.name, 'sha256': sha(path)}
        self.state['items'][ident] = {'status': 'succeeded', 'attempts': 1,
                                     'outputs': {output.name: sha(output)}, 'evidence': evidence}

    def test_parallel_capacity_without_mutations(self):
        self.save()
        before = {str(p): p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
        code, report = self.invoke(save=False)
        self.assertEqual(code, 0)
        self.assertEqual(report['ready'], ['first', 'second'])
        self.assertEqual(report['waiting_capacity'], ['third'])
        self.assertEqual(before, {str(p): p.read_bytes() for p in self.root.rglob('*') if p.is_file()})

    def test_partial_failure_preserves_success_and_allows_independent_retry(self):
        self.succeed('first')
        self.state['items']['second'] = {'status': 'failed', 'attempts': 1}
        self.plan['items'][2]['depends_on'] = ['first']
        code, report = self.invoke()
        self.assertEqual(code, 0)
        self.assertEqual(report['reusable'], ['first'])
        self.assertEqual(report['ready'], ['second', 'third'])
        self.assertFalse(report['all_succeeded'])

    def test_changed_input_blocks_descendant_but_not_independent_item(self):
        self.succeed('first')
        self.plan['items'][2]['depends_on'] = ['first']
        (self.root / 'first.json').write_text('changed source')
        code, report = self.invoke()
        self.assertEqual(code, 2)
        self.assertEqual(report['ready'], ['second'])
        self.assertEqual(report['reusable'], [])
        self.assertIn('third', report['blocked'])

    def test_changed_output_or_missing_evidence_prevents_reuse(self):
        self.succeed('first')
        (self.root / 'first-output.json').write_text('later output edit')
        code, report = self.invoke()
        self.assertEqual(code, 2)
        self.assertIn('first', report['stale'])
        self.succeed('first')
        (self.root / 'first-browser.json').unlink()
        code, report = self.invoke()
        self.assertEqual(code, 2)
        self.assertNotIn('first', report['reusable'])

    def test_missing_required_proof_is_invalid(self):
        self.succeed('first')
        del self.state['items']['first']['evidence']['catalog']
        code, report = self.invoke()
        self.assertEqual(code, 1)
        self.assertFalse(report['valid'])

    def test_running_worker_occupies_capacity_and_requires_reconciliation(self):
        self.state['items']['first'] = {'status': 'running', 'attempts': 1}
        code, report = self.invoke()
        self.assertEqual(code, 0)
        self.assertEqual(report['running'], ['first'])
        self.assertIn('first', report['blocked'])
        self.assertEqual(report['ready'], ['second'])
        self.assertEqual(report['waiting_capacity'], ['third'])

    def test_attempt_ceiling_and_explicit_blockers(self):
        self.state['items']['first'] = {'status': 'failed', 'attempts': 2}
        self.state['items']['second'] = {'status': 'blocked', 'attempts': 0}
        code, report = self.invoke()
        self.assertEqual(code, 0)
        self.assertEqual(report['ready'], ['third'])
        self.assertEqual(set(report['blocked']), {'first', 'second'})

    def test_cycles_and_unknown_dependencies_are_rejected(self):
        self.plan['items'][0]['depends_on'] = ['second']
        self.plan['items'][1]['depends_on'] = ['first']
        self.assertEqual(self.invoke()[0], 1)
        self.plan['items'][1]['depends_on'] = ['absent']
        self.assertEqual(self.invoke()[0], 1)

    def test_nested_and_symlinked_workspace_collisions(self):
        self.plan['items'][1]['workspace'] = 'outputs/first/nested'
        self.assertEqual(self.invoke()[0], 1)
        destination = self.root / 'real'
        destination.mkdir()
        (self.root / 'alias').symlink_to(destination, target_is_directory=True)
        self.plan['items'][0]['workspace'] = 'real/first'
        self.plan['items'][1]['workspace'] = 'alias/first'
        self.assertEqual(self.invoke()[0], 1)

    def test_duplicate_ports_tags_ids_and_nonpositive_limits(self):
        for field, value in [('ports', [3100]), ('tags', ['demo-panel'])]:
            self.plan['items'][0][field] = value
            self.plan['items'][1][field] = value
            self.assertEqual(self.invoke()[0], 1)
            self.plan['items'][0][field] = []
            self.plan['items'][1][field] = []
        self.plan['limits']['concurrency'] = True
        self.assertEqual(self.invoke()[0], 1)
        self.plan['limits']['concurrency'] = 2
        self.plan['items'][1]['id'] = 'first'
        self.assertEqual(self.invoke()[0], 1)

    def test_plan_identity_cannot_be_rebound_by_formatting_or_edit(self):
        self.save()
        with (self.root / 'plan.json').open('a') as stream:
            stream.write('\n')
        code, report = self.invoke(save=False)
        self.assertEqual(code, 1)
        self.assertFalse(report['valid'])

    def test_all_verified_fixtures_are_reusable(self):
        for ident in ('first', 'second', 'third'):
            self.succeed(ident)
        code, report = self.invoke()
        self.assertEqual(code, 0)
        self.assertTrue(report['all_succeeded'])
        self.assertEqual(report['ready'], [])


if __name__ == '__main__':
    unittest.main()
