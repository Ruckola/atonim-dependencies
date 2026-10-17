"""Non-production reference checks for the published producer contract.

This is a contract-test helper, not a signing tool or an application verifier.
"""
import base64
from datetime import datetime
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
from urllib.parse import urlsplit

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
ID = r'[a-z][a-z0-9]*(?:\.[a-z][a-z0-9]*)+'
VERSION = r'[0-9]+\.[0-9]+\.[0-9]+'
KEY_ID = r'sha256-[a-f0-9]{64}'
DIGEST = r'[a-f0-9]{64}'


def _pairs(pairs):
    out = {}
    for key, value in pairs:
        if key in out:
            raise ValueError('duplicate JSON key')
        out[key] = value
    return out


def _constant(_):
    raise ValueError('non-JSON numeric constant')


def parse(raw):
    if not isinstance(raw, bytes) or len(raw) > 1024 * 1024:
        raise ValueError('invalid payload size/type')
    return json.loads(raw.decode('utf-8'), object_pairs_hook=_pairs, parse_constant=_constant)


def _full(pattern, value):
    if not isinstance(value, str) or not re.fullmatch(pattern, value, flags=re.ASCII):
        raise ValueError('invalid producer string')


def _integer(value):
    # JSON 1 is decoded to int; 1.0 and 1e0 decode to float; bool is not int here.
    if type(value) is not int:
        raise ValueError('integer must use a JSON integer token')


def _base64(value, length):
    raw = base64.b64decode(value, validate=True)
    if len(raw) != length or base64.b64encode(raw).decode('ascii') != value:
        raise ValueError('invalid canonical Base64')
    return raw


def _metadata_url(url):
    parsed = urlsplit(url)
    if (parsed.scheme != 'https' or parsed.netloc != 'raw.githubusercontent.com'
            or not re.fullmatch(r'/Ruckola/atonim-dependencies/[^/]+/(?:channels|components)/[^?#]+\.json', parsed.path)
            or parsed.query or parsed.fragment or '..' in parsed.path.split('/')):
        raise ValueError('invalid metadata URL')


def _artifact_url(url):
    parsed = urlsplit(url)
    if (parsed.scheme != 'https' or parsed.netloc != 'github.com'
            or not re.fullmatch(r'/Ruckola/atonim-dependencies/releases/download/[^/]+/[^/]+', parsed.path)
            or parsed.query or parsed.fragment):
        raise ValueError('invalid artifact URL')


def validate(kind, raw, *, now=None):
    """Validate exact JSON bytes as producer metadata; returns parsed object."""
    names = {'envelope': 'signature-envelope-v1.schema.json', 'root': 'root-policy-v1.schema.json',
             'channel': 'channel-v2.schema.json', 'component': 'component-v2.schema.json'}
    if kind == 'envelope' and len(raw) > 8192:
        raise ValueError('envelope too large')
    doc = parse(raw)
    schema = json.loads((ROOT / 'schemas' / names[kind]).read_text(encoding='utf-8'))
    errors = list(Draft202012Validator(schema).iter_errors(doc))
    if errors:
        raise ValueError('schema: ' + errors[0].message)
    _integer(doc['schema_version'])
    if kind == 'envelope':
        _integer(doc['sequence'])
        _full(KEY_ID, doc['key_id'])
        _full(r'(?:root|channel:(?:stable|beta)|component:' + ID + ':' + VERSION + ')', doc['role'])
        _full(DIGEST, doc['payload_sha256'])
        _base64(doc['signature'], 64)
        expires = datetime.fromisoformat(doc['expires'].replace('Z', '+00:00'))
        if expires.tzinfo is None or now is None or expires <= now:
            raise ValueError('invalid or expired timestamp')
    elif kind == 'root':
        for key_id, encoded in doc['keys'].items():
            _full(KEY_ID, key_id)
            key = _base64(encoded, 32)
            if key_id != 'sha256-' + hashlib.sha256(key).hexdigest():
                raise ValueError('key fingerprint mismatch')
        for key_id in doc['revoked']:
            _full(KEY_ID, key_id)
    elif kind == 'channel':
        for identifier, entry in doc['components'].items():
            _full(ID, identifier)
            _full(VERSION, entry['version'])
            _metadata_url(entry['manifest_url'])
    else:
        _full(ID, doc['id'])
        _full(VERSION, doc['version'])
        for item in doc['requires']:
            _full(ID, item['id']); _full(VERSION, item['version'])
        compat = doc['compatibility']
        for field in ('min_app_version', 'max_app_version'):
            _full(VERSION, compat[field])
        if tuple(map(int, compat['min_app_version'].split('.'))) > tuple(map(int, compat['max_app_version'].split('.'))):
            raise ValueError('reversed compatibility range')
        artifact = doc['artifact']
        _artifact_url(artifact['url']); _full(DIGEST, artifact['sha256'])
        for field in ('size_bytes', 'extracted_size_bytes'):
            _integer(artifact[field])
        for export in doc['exports'].values():
            value = export['path']; path = PurePosixPath(value)
            if '\\' in value or path.is_absolute() or '..' in path.parts or not path.parts:
                raise ValueError('invalid export path')
            if export['type'] != 'directory':
                _full(DIGEST, export['sha256'])
        for check in doc['health']:
            if check['export'] not in doc['exports'] or doc['exports'][check['export']]['type'] != 'executable':
                raise ValueError('invalid health cross-reference')
            if 'timeout_seconds' in check:
                _integer(check['timeout_seconds'])
            for field in ('success_exit_codes', 'empty_stderr_exit_codes'):
                for value in check.get(field, []):
                    _integer(value)
    return doc
