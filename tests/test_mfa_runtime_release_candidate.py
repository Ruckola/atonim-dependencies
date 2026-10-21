"""Source-level release gate for the reviewed MFA runtime metadata candidate."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import unittest

from jsonschema import Draft202012Validator, FormatChecker

from producer_contract import validate as validate_producer


ROOT = Path(__file__).resolve().parents[1]
CANDIDATE = ROOT / 'release-candidates' / 'alignment.mfa.runtime-1.0.2.json'
CHANNEL = ROOT / 'release-candidates' / 'beta-4.json'
LANGUAGES = (
    ('en', 'alignment.mfa.models.en'),
    ('nl', 'alignment.mfa.models.nl'),
    ('de', 'alignment.mfa.models.de'),
    ('fr', 'alignment.mfa.models.fr'),
    ('es-419', 'alignment.mfa.models.es419'),
    ('pt-BR', 'alignment.mfa.models.ptbr'),
)
RUNTIME_REQUIRED_EXPORTS = (
    'python', 'mfa', 'sqlite3', 'fstcompile', 'compute-mfcc-feats',
    'compute-and-process-kaldi-pitch-feats', 'gmm-align-compiled',
    'gmm-est-fmllr', 'gmm-est-fmllr-gpost', 'lattice-oracle',
    'gmm-latgen-faster', 'fstdeterminizestar', 'fsttablecompose',
    'gmm-rescore-lattice',
)


def load(path):
    return json.loads(path.read_text(encoding='utf-8'))


class MfaRuntimeReleaseCandidateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.candidate = load(CANDIDATE)
        cls.channel = load(CHANNEL)

    def test_candidate_is_schema_and_producer_valid(self):
        schema = load(ROOT / 'schemas' / 'component-v2.schema.json')
        validator = Draft202012Validator(schema, format_checker=FormatChecker())
        self.assertTrue(validator.is_valid(self.candidate))
        validate_producer('component', CANDIDATE.read_bytes())

    def test_every_required_runtime_executable_has_integrity_and_authenticated_health(self):
        exports = self.candidate['exports']
        health = {item['export']: item for item in self.candidate['health']}
        self.assertEqual(tuple(name for name in exports if name != 'bin'), RUNTIME_REQUIRED_EXPORTS)
        for name in RUNTIME_REQUIRED_EXPORTS:
            with self.subTest(export_name=name):
                self.assertEqual(exports[name]['type'], 'executable')
                self.assertRegex(exports[name]['sha256'], r'^[0-9a-f]{64}$')
                self.assertIn(name, health)
                self.assertIn(health[name]['argv'], (['--version'], ['--help']))
        self.assertEqual(health['python']['argv'], ['--version'])
        self.assertEqual(health['fstcompile']['success_exit_codes'], [1])

    def test_channel_candidate_selects_runtime_1_0_2_and_all_six_existing_model_manifests(self):
        schema = load(ROOT / 'schemas' / 'channel-v2.schema.json')
        self.assertTrue(Draft202012Validator(schema, format_checker=FormatChecker()).is_valid(self.channel))
        validate_producer('channel', CHANNEL.read_bytes())
        components = self.channel['components']
        self.assertEqual(components['alignment.mfa.runtime']['version'], '1.0.2')
        self.assertTrue(components['alignment.mfa.runtime']['manifest_url'].endswith('/runtime/1.0.2.json'))
        for language, identifier in LANGUAGES:
            with self.subTest(language=language):
                item = components[identifier]
                manifest = ROOT / item['manifest_url'].split('/main/', 1)[1]
                document = load(manifest)
                self.assertEqual((document['id'], document['version'], document['languages']),
                                 (identifier, item['version'], [language]))
                for export in document['exports'].values():
                    self.assertRegex(export.get('sha256', ''), r'^[0-9a-f]{64}$')

    @unittest.skipUnless(os.environ.get('SPEECHFACTORY_SOURCE'), 'set SPEECHFACTORY_SOURCE for recipe integration')
    def test_all_shipped_mfa_recipes_resolve_against_candidate_component_contract(self):
        source = Path(os.environ['SPEECHFACTORY_SOURCE']).resolve()
        recipes = [load(path) for path in (source / 'profile_support' / 'recipes').glob('mfa-*-alignment.json')]
        for language, model_id in LANGUAGES:
            with self.subTest(language=language):
                recipe = next(item for item in recipes
                              if item['profile']['runtime']['readiness']['languages'] == [language])
                requirements = recipe['profile']['runtime']['readiness']['components']
                runtime, model = requirements
                self.assertEqual(runtime['id'], 'alignment.mfa.runtime')
                self.assertEqual(runtime['required_exports'], list(RUNTIME_REQUIRED_EXPORTS))
                self.assertEqual(model['id'], model_id)
                for parameter, export in runtime['parameters'].items():
                    self.assertIn(export, self.candidate['exports'], parameter)
                model_manifest = load(ROOT / self.channel['components'][model_id]['manifest_url'].split('/main/', 1)[1])
                for parameter, export in model['parameters'].items():
                    self.assertIn(export, model_manifest['exports'], parameter)

    def test_candidate_keeps_the_immutable_1_0_1_payload_identity(self):
        published = load(ROOT / 'components/alignment/mfa/runtime/1.0.1.json')
        self.assertEqual(self.candidate['artifact'], published['artifact'])
        self.assertEqual(self.candidate['exports'], published['exports'])
        self.assertNotEqual(hashlib.sha256(CANDIDATE.read_bytes()).hexdigest(),
                            hashlib.sha256((ROOT / 'components/alignment/mfa/runtime/1.0.1.json').read_bytes()).hexdigest())

