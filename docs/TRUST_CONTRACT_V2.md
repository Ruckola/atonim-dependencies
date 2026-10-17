# Atonim optional-component trust contract: v2 producer specification

Status: **proposed; not production activation**. This specification describes
the v2 application implementation and a narrower producer profile. The public
v1 channels remain unsigned, empty and unchanged; they are not v2 catalogs.
No key, signature, model, component manifest or channel entry is published by
this document. Schema validation alone does not authenticate metadata.

## Ownership and trust chain

SpeechFactory owns the verifier, resolver, installer and application-pinned
public roots. This repository owns public schemas, metadata and release assets.
An app-pinned Ed25519 root verifies a root policy, whose non-revoked online
public keys verify channels and versioned component manifests. A manifest binds
the release URL, byte size and SHA-256 of an immutable artifact. HTTPS alone,
immutable releases alone and an unsigned hash do not authenticate metadata.
Unknown, missing, malformed, expired or invalid signatures fail closed.

## Detached envelope and signed bytes

For each payload at `URL`, the current client fetches the detached envelope at
`URL + ".sig.json"`. The v1 envelope has exactly the seven members in
`schemas/signature-envelope-v1.schema.json`. Roles are `root`,
`channel:stable`, `channel:beta` and `component:<component-id>:<version>`.
The client requires the expected role rather than trusting the supplied role.

`payload_sha256` is lowercase hex SHA-256 of the **exact received payload
bytes**; whitespace, UTF-8 encoding and trailing newlines matter. It is not a
hash of reserialized JSON. The Ed25519 signature is over exactly:

```python
json.dumps({k: v for k, v in envelope.items() if k != "signature"},
           sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")
```

There is no trailing newline in this signed message. Envelope member names and
producer values are ASCII, sequence is a JSON integer, and strings are escaped
as in that Python expression. Publish payloads as UTF-8 JSON; producers should
use sorted keys and compact separators with no trailing newline, but the
current verifier authenticates the exact bytes rather than requiring that
payload serialization. Use standard padded Base64 for a 64-byte Ed25519
signature and for each raw 32-byte Ed25519 public key. Duplicate object keys in
payload or envelope are rejected. The client limits payloads to 1 MiB and
envelopes to 8192 bytes and checks signature, role, digest, expiry and sequence
before trusting a payload.

## Key IDs, rotation and expiry

**Required producer convention:** `sha256-` followed by the 64 lowercase hex
digits of SHA-256 over the raw 32-byte public key. Schema pattern matching does
not prove the relationship: a producer must independently derive/check it.
The existing verifier accepts arbitrary string key IDs and does **not** enforce
that relationship. Changing that verifier is not part of this contract gate.

The `root` payload has schema version 1, `keys` (ID to Base64 public key), and
`revoked` (key IDs). Only an app-pinned root signs it. A higher-sequence policy
can add or revoke online keys; root replacement requires an application update.
Private keys must never be committed or bundled. `expires` is a timezone-aware
timestamp strictly later than verification time; producers use RFC 3339. The
schema's timestamp pattern checks representation, not calendar/time validity:
JSON Schema `format` checking can be disabled or unavailable. Producer
contract validation MUST additionally parse the timestamp as a real date and
time with an explicit timezone, and reject invalid or non-future values. The
mandatory contract tests perform this semantic check without depending on
optional format checkers; the client independently uses `datetime.fromisoformat`
and enforces expiry. Each
role has its own nonnegative integer sequence. After a client sees a role,
lower sequences and equal-sequence/different-payload metadata are rejected;
once seen, a component ID/version's payload bytes cannot change even with a
higher sequence. Identical payloads may be re-signed at a higher sequence.

High-water state is local. A fresh installation or deleted/rolled-back state has
no earlier counter; clocks and offline clients limit freshness. Existing
authenticated installations may operate offline past metadata expiry and honor
the latest cached revocation; they cannot learn new revocations while offline.

## Channel and component payloads

`schemas/channel-v2.schema.json` specifies the producer shape: channel, schema
version, and entries `{version, manifest_url}`. URLs are HTTPS raw GitHub URLs
in this repository with exact host `raw.githubusercontent.com`, followed by
`/Ruckola/atonim-dependencies/<nonempty-ref>/channels/` or `/components/`,
a nonempty path ending in `.json`, and no query or fragment. A literal `..`
path segment anywhere is rejected, including in the ref. Producers must check
these URL semantics, not merely rely on schema matching. The client uses
`urlsplit` and does not percent-decode path segments for this comparison;
this contract does not claim broader URL normalization. Dependency selections reference exact
IDs and versions. No channel entry is added by this specification.

`schemas/component-v2.schema.json` specifies the producer shape for one exact
component/version. It includes inclusive application version bounds; platform
and architecture; `tar.gz` asset URL, compressed/extracted byte bounds and
digest; exports; bounded `--help`/`--version` health checks; dependencies;
and a `redistribution.cleared` assertion. Such an assertion may be published
only after actual approval: this document does not grant approval. Empty
`languages` means language-independent. Each file/executable export has a
digest. Required executable exports need corresponding health checks; the client
also checks their cross-references, compatibility, archive safety and actual
file properties. JSON Schema cannot enforce all of those runtime conditions.
An optional per-check `timeout_seconds` is an integer from 1 through 90;
absence retains the client's 15-second per-check default. The client enforces
the timeout and a bounded aggregate health budget.

## Validation responsibilities

**JSON Schema** checks the documented producer structure, required fields,
enums, bounded lists, basic URL/path patterns and numerical bounds. It is not a
complete validity test: ordinary JSON Schema considers `1.0` and `1e0`
integers, and optional `format` checking is not a reliable date validator.

**Mandatory producer validation** operates on the actual UTF-8 JSON bytes and
rejects duplicate keys and non-JSON numeric constants. Every integer field
must use an integer JSON token (for example `1`, never `1.0`, `1e0`, `"1"`,
`true`, or `null`). This applies to every schema version, envelope sequence,
artifact byte size, health exit code and health timeout. It must additionally verify semantic
expiry, exact URL parsing and traversal rules, canonical Base64/length, key
fingerprints, full-match IDs/versions/digests/roles, safe export paths, ordered
app-version bounds and health-to-executable cross-references. The deterministic
`tests/producer_contract.py` is test/reference code for these requirements, not
a production signing CLI. `tests/test_v2_contract.py` exercises it using
synthetic fixtures; install `jsonschema` and `cryptography` in a test
environment and run `python -m unittest discover -s tests -p test_v2_contract.py`.
Set `SPEECHFACTORY_SOURCE` to a SpeechFactory checkout to include direct client
agreement checks. Schema and reference validation do not establish authenticity:
signature, expected role, exact payload digest, keys and trust state must still
be checked independently.

**Client runtime validation** independently enforces authenticated roles,
signature, exact payload hash, timestamps, URL policy, local sequence/replay
state, manifest identity and supported app version/platform/language, plus
installation/extraction and health constraints. Some client checks depend on
external state, not metadata shape. Schemas and producer rules are intentionally
stricter in places (including fingerprint IDs); they do not alter the client.
Example/fixture metadata is explicitly non-production.

The current v2 catalog selects one manifest per component ID/version and each
manifest describes one platform. The signature format is platform-neutral, but
multi-platform selection and Windows locking are not solved by this document.
Runtime and model component versions are independent.

## Legal/source companion

The source companion is legal/release discovery material, not an artifact for
normal runtime installation. The frozen macOS arm64 MFA 1.0.0 source companion is
`atonim-mfa-runtime-macos-arm64-1.0.0-sources.tar.gz`, 231113077 bytes, SHA-256
`8b1aff243f7def93f117395703f7f97207b9420ed540d86352f27df1537466d8`.
Its [immutable release asset](https://github.com/Ruckola/atonim-dependencies/releases/download/mfa-runtime-macos-arm64-v1.0.0/atonim-mfa-runtime-macos-arm64-1.0.0-sources.tar.gz)
is the source-discovery location. Release/legal metadata
is not authenticated by the application's component signature under this
contract. Source availability does not itself constitute redistribution GO.
