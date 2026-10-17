"""Non-production synthetic contract fixtures; no keys here are trusted roots."""
import base64
import copy
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest

from jsonschema import Draft202012Validator, FormatChecker
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from producer_contract import validate as validate_producer


ROOT = Path(__file__).resolve().parents[1]
SPEECHFACTORY = os.environ.get('SPEECHFACTORY_SOURCE')
if SPEECHFACTORY:
    sys.path.insert(0, SPEECHFACTORY)


def schema(name):
    value = json.loads((ROOT / 'schemas' / name).read_text(encoding='utf-8'))
    Draft202012Validator.check_schema(value)
    return Draft202012Validator(value, format_checker=FormatChecker())


def compact(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=True).encode('utf-8')


def validate_expiry(value, now):
    """Mandatory producer check: schema format validation may be unavailable."""
    parsed = datetime.fromisoformat(value.replace('Z', '+00:00'))
    if parsed.tzinfo is None or parsed <= now:
        raise ValueError('Expiry must be a valid future timezone-aware timestamp')


def validate_envelope_contract(value, now):
    """Test producer contract with mandatory semantic expiry validation."""
    validate_producer('envelope', compact(value), now=now)


class TrustContractTests(unittest.TestCase):
    def setUp(self):
        self.key = Ed25519PrivateKey.from_private_bytes(bytes(range(32)))  # TEST ONLY
        self.public = self.key.public_key().public_bytes(serialization.Encoding.Raw, serialization.PublicFormat.Raw)
        self.key_id = 'sha256-' + hashlib.sha256(self.public).hexdigest()
        self.channel = {'schema_version': 2, 'channel': 'beta', 'components': {
            'alignment.fixture.runtime': {'version': '1.0.0', 'manifest_url':
                'https://raw.githubusercontent.com/Ruckola/atonim-dependencies/main/components/fixture.json'}}}
        self.component = {
            'schema_version': 2, 'id': 'alignment.fixture.runtime', 'version': '1.0.0',
            'name': 'Synthetic fixture', 'description': 'NON-PRODUCTION TEST DATA',
            'languages': [], 'requires': [],
            'compatibility': {'platform': 'macos', 'architecture': 'arm64', 'min_app_version': '1.0.0', 'max_app_version': '1.0.0'},
            'artifact': {'format': 'tar.gz', 'url': 'https://github.com/Ruckola/atonim-dependencies/releases/download/fixture/fixture.tar.gz',
                         'sha256': 'a' * 64, 'size_bytes': 1, 'extracted_size_bytes': 1},
            'exports': {'tool': {'path': 'runtime/bin/tool', 'type': 'executable', 'sha256': 'b' * 64}},
            'health': [{'export': 'tool', 'argv': ['--help']}],
            # A synthetic true value tests the installer shape; it is NOT approval.
            'redistribution': {'cleared': True},
        }
        self.policy = {'schema_version': 1, 'keys': {self.key_id: base64.b64encode(self.public).decode()}, 'revoked': []}
        self.raw = compact(self.channel)
        self.envelope = {'schema_version': 1, 'key_id': self.key_id, 'role': 'channel:beta', 'sequence': 1,
                         'expires': '2099-01-01T00:00:00Z', 'payload_sha256': hashlib.sha256(self.raw).hexdigest()}
        self.envelope['signature'] = base64.b64encode(self.key.sign(compact(self.envelope))).decode()

    def test_all_schemas_accept_representative_fixture(self):
        for name, data in [('channel-v2.schema.json', self.channel), ('component-v2.schema.json', self.component),
                           ('root-policy-v1.schema.json', self.policy), ('signature-envelope-v1.schema.json', self.envelope)]:
            with self.subTest(name=name):
                self.assertTrue(schema(name).is_valid(data))

    def test_health_timeout_producer_and_client_agree(self):
        validator = schema('component-v2.schema.json')
        for value in (1, 15, 75, 90):
            component = copy.deepcopy(self.component)
            component['health'][0]['timeout_seconds'] = value
            with self.subTest(value=value):
                self.assertTrue(validator.is_valid(component))
                validate_producer('component', compact(component))
                if SPEECHFACTORY:
                    from services.component_catalog import ComponentCatalog
                    ComponentCatalog(None, None).validate(component, component['id'], '1.0.0', None)
        for value in (0, -1, 91, True, '75', 1.5, 75.0, None):
            component = copy.deepcopy(self.component)
            component['health'][0]['timeout_seconds'] = value
            with self.subTest(value=value), self.assertRaises(ValueError):
                validate_producer('component', compact(component))
            if SPEECHFACTORY:
                from services.component_catalog import ComponentCatalog
                from services.component_installation import ComponentError
                with self.assertRaises(ComponentError):
                    ComponentCatalog(None, None).validate(component, component['id'], '1.0.0', None)

    def test_channel_rejects_v1_shape_and_untrusted_url(self):
        validator = schema('channel-v2.schema.json')
        bad = copy.deepcopy(self.channel)
        bad['schema_version'] = 1
        self.assertFalse(validator.is_valid(bad))
        bad = copy.deepcopy(self.channel)
        bad['components']['alignment.fixture.runtime']['manifest_url'] = 'https://example.org/fixture.json'
        self.assertFalse(validator.is_valid(bad))

    def test_channel_rejects_literal_traversal_segments(self):
        validator = schema('channel-v2.schema.json')
        urls = [
            'https://raw.githubusercontent.com/Ruckola/atonim-dependencies/main/components/../fixture.json',
            'https://raw.githubusercontent.com/Ruckola/atonim-dependencies/../components/fixture.json',
            'https://raw.githubusercontent.com/Ruckola/atonim-dependencies/main/components/nested/../fixture.json',
        ]
        for url in urls:
            with self.subTest(url=url):
                bad = copy.deepcopy(self.channel)
                bad['components']['alignment.fixture.runtime']['manifest_url'] = url
                self.assertFalse(validator.is_valid(bad))
                if SPEECHFACTORY:
                    from services.component_catalog import metadata_url
                    from services.component_installation import ComponentError
                    with self.assertRaises(ComponentError):
                        metadata_url(url)
        url = self.channel['components']['alignment.fixture.runtime']['manifest_url']
        self.assertTrue(validator.is_valid(self.channel))
        if SPEECHFACTORY:
            from services.component_catalog import metadata_url
            self.assertEqual(metadata_url(url), url)

    def test_expiry_semantics_do_not_depend_on_optional_format_checker(self):
        now = datetime(2026, 1, 1, tzinfo=timezone.utc)
        schema_only = Draft202012Validator(schema('signature-envelope-v1.schema.json').schema)
        for expires in ['2099-13-01T00:00:00Z', '2099-02-30T00:00:00Z',
                        '2099-01-01T24:00:00Z', '2099-01-01T00:60:00Z',
                        '2099-01-01T00:00:60Z']:
            with self.subTest(expires=expires):
                bad = dict(self.envelope, expires=expires)
                self.assertTrue(schema_only.is_valid(bad))  # Shape is not semantic validation.
                with self.assertRaises(ValueError):
                    validate_envelope_contract(bad, now)
                if SPEECHFACTORY:
                    from services.component_installation import ComponentError, verify_metadata
                    unsigned = {key: val for key, val in bad.items() if key != 'signature'}
                    bad['signature'] = base64.b64encode(self.key.sign(compact(unsigned))).decode()
                    with self.assertRaises(ComponentError):
                        verify_metadata(self.raw, compact(bad), {self.key_id: self.public}, role='channel:beta', now=now)
        validate_envelope_contract(self.envelope, now)
        with self.assertRaises(ValueError):
            validate_expiry('2025-01-01T00:00:00Z', now)

    def test_component_rejects_bad_artifact_and_unapproved(self):
        validator = schema('component-v2.schema.json')
        for mutate in (lambda d: d['artifact'].update(size_bytes=0),
                       lambda d: d['artifact'].update(sha256='bad'),
                       lambda d: d['redistribution'].update(cleared=False),
                       lambda d: d['exports']['tool'].update(path='../escape'),
                       lambda d: d['health'][0].update(argv=['--run'])):
            bad = copy.deepcopy(self.component)
            mutate(bad)
            self.assertFalse(validator.is_valid(bad))

    def test_envelope_and_policy_reject_invalid_fields(self):
        envelope_validator = schema('signature-envelope-v1.schema.json')
        for key, value in [('key_id', 'arbitrary'), ('signature', '!'), ('role', 'channel:other'), ('sequence', -1), ('expires', 'not-a-date')]:
            bad = dict(self.envelope, **{key: value})
            self.assertFalse(envelope_validator.is_valid(bad))
        bad_policy = copy.deepcopy(self.policy)
        bad_policy['keys'][self.key_id] = 'not-base64'
        self.assertFalse(schema('root-policy-v1.schema.json').is_valid(bad_policy))

    def test_strict_integer_tokens_envelope(self):
        now = datetime(2026, 1, 1, tzinfo=timezone.utc)
        for field in ('schema_version', 'sequence'):
            for token in ('1', '1.0', '1e0', '1E0', '"1"', 'true', 'null'):
                with self.subTest(field=field, token=token):
                    raw = compact(self.envelope).decode().replace('"' + field + '":1', '"' + field + '":' + token).encode()
                    if token == '1':
                        validate_producer('envelope', raw, now=now)
                    else:
                        with self.assertRaises(ValueError):
                            validate_producer('envelope', raw, now=now)
                        if SPEECHFACTORY and token in ('1.0', '1e0', '1E0', '"1"', 'true', 'null'):
                            from services.component_installation import ComponentError, verify_metadata
                            bad = json.loads(raw)
                            unsigned = {key: val for key, val in bad.items() if key != 'signature'}
                            bad['signature'] = base64.b64encode(self.key.sign(compact(unsigned))).decode()
                            with self.assertRaises(ComponentError):
                                verify_metadata(self.raw, compact(bad), {self.key_id: self.public}, role='channel:beta', now=now)

    def test_strict_integer_tokens_other_metadata(self):
        variants = [('root', self.policy, ('schema_version',)),
                    ('channel', self.channel, ('schema_version',)),
                    ('component', self.component, ('schema_version',))]
        for kind, doc, fields in variants:
            for field in fields:
                bad = copy.deepcopy(doc); bad[field] = float(bad[field])
                with self.subTest(kind=kind, field=field), self.assertRaises(ValueError):
                    validate_producer(kind, compact(bad))
        for field in ('size_bytes', 'extracted_size_bytes'):
            bad = copy.deepcopy(self.component); bad['artifact'][field] = 1.0
            with self.subTest(field=field), self.assertRaises(ValueError):
                validate_producer('component', compact(bad))
        bad = copy.deepcopy(self.component); bad['health'][0]['success_exit_codes'] = [0.0]
        with self.assertRaises(ValueError):
            validate_producer('component', compact(bad))

    def test_producer_cross_field_and_exact_parsing_boundaries(self):
        for kind, doc in [('root', self.policy), ('channel', self.channel), ('component', self.component)]:
            validate_producer(kind, compact(doc))
        for kind, doc in [('root', self.policy), ('channel', self.channel), ('component', self.component)]:
            raw = compact(doc)
            duplicate = raw[:-1] + b',"schema_version":1}'
            with self.subTest(kind=kind), self.assertRaises(ValueError):
                validate_producer(kind, duplicate)
        bad = copy.deepcopy(self.component); bad['health'][0]['export'] = 'absent'
        with self.assertRaises(ValueError):
            validate_producer('component', compact(bad))
        bad = copy.deepcopy(self.component); bad['compatibility']['min_app_version'] = '2.0.0'
        with self.assertRaises(ValueError):
            validate_producer('component', compact(bad))
        bad = copy.deepcopy(self.policy); bad['keys']['sha256-' + '0' * 64] = bad['keys'].pop(self.key_id)
        with self.assertRaises(ValueError):
            validate_producer('root', compact(bad))

    def test_component_producer_adversarial_field_matrix(self):
        def change(doc, group, key, value):
            (doc if group is None else doc[group])[key] = value
        cases = [
            (None, 'id', 'invalid'), (None, 'version', '1.0'), (None, 'name', ''),
            (None, 'description', ''), (None, 'languages', 'en'), (None, 'requires', [{}]),
            (None, 'extra', True), ('compatibility', 'platform', ''),
            ('compatibility', 'architecture', ''), ('compatibility', 'max_app_version', '1'),
            ('artifact', 'format', 'zip'), ('artifact', 'url', 'https://github.com/Ruckola/atonim-dependencies/releases/download/tag/file?x=1'),
            ('artifact', 'sha256', '0' * 63), ('artifact', 'size_bytes', True),
            ('artifact', 'size_bytes', 0), ('artifact', 'extracted_size_bytes', 1.0),
            ('redistribution', 'cleared', False),
        ]
        for group, key, value in cases:
            with self.subTest(group=group, key=key, value=value):
                bad = copy.deepcopy(self.component); change(bad, group, key, value)
                with self.assertRaises(ValueError):
                    validate_producer('component', compact(bad))
        for path in ('/absolute', '../outside', 'a/../outside', '.', 'a\\outside'):
            with self.subTest(path=path):
                bad = copy.deepcopy(self.component); bad['exports']['tool']['path'] = path
                with self.assertRaises(ValueError):
                    validate_producer('component', compact(bad))
        for change_health in ({'argv': ['--run']}, {'export': 'missing'},
                              {'success_exit_codes': [256]}, {'success_exit_codes': [True]},
                              {'empty_stderr_exit_codes': [0.0]}, {'extra': 1}):
            with self.subTest(health=change_health):
                bad = copy.deepcopy(self.component); bad['health'][0].update(change_health)
                with self.assertRaises(ValueError):
                    validate_producer('component', compact(bad))

    def test_root_and_channel_producer_adversarial_field_matrix(self):
        for mutation in ('missing_keys', 'bad_key', 'unknown_field', 'bad_revoked'):
            bad = copy.deepcopy(self.policy)
            if mutation == 'missing_keys': del bad['keys']
            if mutation == 'bad_key': bad['keys'][self.key_id] = '!' * 44
            if mutation == 'unknown_field': bad['extra'] = 1
            if mutation == 'bad_revoked': bad['revoked'] = [True]
            with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                validate_producer('root', compact(bad))
        for url in ('https://example.org/x.json',
                    'http://raw.githubusercontent.com/Ruckola/atonim-dependencies/main/components/x.json',
                    'https://raw.githubusercontent.com/Ruckola/atonim-dependencies/main/components/x.json?x=1',
                    'https://raw.githubusercontent.com/Ruckola/atonim-dependencies/main/components/x.json#x',
                    'https://raw.githubusercontent.com/Ruckola/atonim-dependencies/main/components/../x.json'):
            with self.subTest(url=url):
                bad = copy.deepcopy(self.channel)
                bad['components']['alignment.fixture.runtime']['manifest_url'] = url
                with self.assertRaises(ValueError):
                    validate_producer('channel', compact(bad))

    @unittest.skipUnless(SPEECHFACTORY, 'set SPEECHFACTORY_SOURCE for application integration')
    def test_four_metadata_types_producer_and_client_end_to_end(self):
        from services.component_catalog import ComponentCatalog, MetadataTrust
        now = datetime(2026, 1, 1, tzinfo=timezone.utc)
        def signed(doc, role):
            raw = compact(doc)
            env = {'schema_version': 1, 'key_id': self.key_id, 'role': role, 'sequence': 1,
                   'expires': '2099-01-01T00:00:00Z', 'payload_sha256': hashlib.sha256(raw).hexdigest()}
            env['signature'] = base64.b64encode(self.key.sign(compact(env))).decode()
            validate_producer('envelope', compact(env), now=now)
            return raw, compact(env)
        channel_url = 'https://raw.githubusercontent.com/Ruckola/atonim-dependencies/main/channels/beta.json'
        manifest_url = self.channel['components']['alignment.fixture.runtime']['manifest_url']
        root_raw, root_sig = signed(self.policy, 'root')
        channel_raw, channel_sig = signed(self.channel, 'channel:beta')
        component_raw, component_sig = signed(self.component, 'component:alignment.fixture.runtime:1.0.0')
        for kind, raw in [('root', root_raw), ('channel', channel_raw), ('component', component_raw)]:
            validate_producer(kind, raw)
        data = {channel_url: channel_raw, channel_url + '.sig.json': channel_sig,
                manifest_url: component_raw, manifest_url + '.sig.json': component_sig}
        with tempfile.TemporaryDirectory() as directory:
            trust = MetadataTrust(Path(directory) / 'trust.json', {self.key_id: self.public})
            trust.accept_policy(root_raw, root_sig, now=now)
            catalog = ComponentCatalog(trust, lambda url, limit: data[url])
            self.assertEqual(catalog.resolve(channel_url, 'beta', ['alignment.fixture.runtime'], language='en'), [self.component])

    @unittest.skipUnless(SPEECHFACTORY, 'set SPEECHFACTORY_SOURCE for application integration')
    def test_documented_serialization_agrees_with_existing_verifier(self):
        from services.component_installation import ComponentError, verify_metadata
        now = datetime(2026, 1, 1, tzinfo=timezone.utc)
        result = verify_metadata(self.raw, compact(self.envelope), {self.key_id: self.public}, role='channel:beta', now=now)
        self.assertEqual(result, self.channel)
        # Adding a payload newline changes exact bytes, even though JSON parses identically.
        with self.assertRaises(ComponentError):
            verify_metadata(self.raw + b'\n', compact(self.envelope), {self.key_id: self.public}, role='channel:beta', now=now)
        with self.assertRaises(ComponentError):
            verify_metadata(self.raw, compact(self.envelope), {self.key_id: self.public}, role='channel:stable', now=now)

    @unittest.skipUnless(SPEECHFACTORY, 'set SPEECHFACTORY_SOURCE for application integration')
    def test_component_fixture_matches_existing_catalog(self):
        from services.component_catalog import ComponentCatalog
        ComponentCatalog(None, None).validate(self.component, self.component['id'], self.component['version'], 'en')


if __name__ == '__main__':
    unittest.main()
