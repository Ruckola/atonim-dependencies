# Component release operations

## Purpose

This repository is the public, durable source of truth for Atonim optional-component metadata, provenance and release selection. GitHub Release assets referenced by immutable manifests are part of that boundary.

A developer workstation must not be the only location of an input needed to reproduce, verify or legally redistribute a component release.

## Immutability

A published component version identifies immutable bytes. Do not replace an artifact, manifest or source companion under an existing version when bytes change. Publish a new component version and a newly signed channel sequence.

The manifest's URL, compressed size, SHA-256, extracted-size bound and exports are release evidence, not advisory metadata.

## Safe publication order

When activating new component versions:

1. finish and independently verify runtime/model archives;
2. finish provenance, notices, redistribution review and required corresponding-source material;
3. create/sign immutable component manifests;
4. stage release assets;
5. publish the GitHub Releases while the active channel still selects the previous component set;
6. fetch every exact artifact URL from the manifests and verify availability, size and SHA-256;
7. update/sign the channel with a higher sequence;
8. merge/publish the channel and manifests to `main`;
9. fetch the public `main` channel and detached signature and independently verify exact bytes;
10. perform clean-machine installation through Atonim with no manual artifact staging.

This order prevents an active channel from pointing at unavailable draft assets.

## Signing operations

Private signing keys and passphrases never belong in GitHub.

The durable repository/release record must retain the public trust material and enough procedure to recover operation after loss of a development Mac. The production design uses an offline/pinned root role and an online metadata-signing role. Component signatures are bound to `component:<id>:<version>`; channel signatures are bound to `channel:<name>`.

Every release operation must deliberately choose a sequence and future expiry. Lower sequence replay and equal-sequence/different-payload are rejected by clients. Expiry therefore requires operational renewal before it becomes a user-facing outage.

Key rotation, revocation and compromise response must be tested/documented before they are needed. A private-key backup is an external protected secret-management responsibility; its existence must be verified without copying key material into this repository.

## Rollback

Never rollback by mutating or replacing published component bytes.

To return clients to a known-good component set, publish a newly signed **higher-sequence** channel payload that selects the already-published immutable known-good versions. Preserve the failed versions for forensic/reproducibility purposes unless a legal/security requirement mandates removal.

## Rebuild provenance

For every runtime/model component retain or reference:

- exact upstream source/revision;
- build/training recipe where applicable;
- patches;
- licenses/notices/attribution;
- redistribution decision;
- source-delivery material where required;
- exact artifact size/hash;
- export hashes and health contract;
- application compatibility bounds.

Large artifacts may live in GitHub Releases rather than Git blobs. A local build directory is never provenance.

## Current V1 MFA set

Shared runtime: `alignment.mfa.runtime 1.0.1`.

Language components:

- `alignment.mfa.models.en 1.0.0` — `en`
- `alignment.mfa.models.nl 1.0.0` — `nl`
- `alignment.mfa.models.de 1.0.0` — `de`
- `alignment.mfa.models.fr 1.0.0` — `fr`
- `alignment.mfa.models.es419 1.0.0` — `es-419`
- `alignment.mfa.models.ptbr 1.0.0` — `pt-BR`

The beta channel also retains the Whisper base model component. Supported-language claims require application-side physical acceptance; publication alone is not acceptance.

## Operational verification

After every publication, independently verify from public URLs rather than local files:

- release assets are downloadable;
- exact manifest URL is reachable;
- manifest/signature verifies;
- channel/signature verifies;
- selected versions are exactly intended;
- a clean Atonim installation can acquire, verify, activate and rediscover the component.

Release automation should eventually perform all deterministic checks and emit an auditable result. Manual physical acceptance remains separate.
