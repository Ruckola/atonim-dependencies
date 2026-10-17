# Atonim Dependencies

Public distribution metadata and release index for **optional Atonim engine runtimes and language models**.

> **Status:** distribution contract established. The first frozen MFA runtime package is in publication preparation, but **no installable component is advertised by the stable or beta channels yet**. Do not mistake this repository for an active production runtime catalog until immutable Release assets, trusted manifests, public-download verification and clean-install acceptance are complete.

## Repository layout

| Path | Purpose |
| --- | --- |
| [`channels/stable.json`](channels/stable.json) | Stable component-version selection |
| [`channels/beta.json`](channels/beta.json) | Beta component-version selection |
| [`schemas/`](schemas/) | JSON Schema contracts for channels and components |
| [`components/alignment/mfa/`](components/alignment/mfa/) | MFA component family and independent runtime / language-model packs |
| [`docs/DISTRIBUTION_CONTRACT.md`](docs/DISTRIBUTION_CONTRACT.md) | Versioning, releases, integrity, trust, compatibility and publication protocol |
| [`legal/`](legal/) | License policy and third-party notices |

Binary packages are hosted as **immutable GitHub Release assets** only after reproducible builds, redistribution/compliance preparation and release-gate verification. Application code and integration logic remain in the private Atonim development repository, `Ruckola/SpeechFactory`.

## Canonical distribution repository

This repository is the canonical public distribution/index repository for new Atonim optional runtimes and model packs.

The older `Ruckola/atonim-runtime-assets` repository is **legacy** and must not receive new dependency publications. Its existing Whisper release is tracked for controlled migration before that repository is retired. See `Ruckola/SpeechFactory#248`.

## Public discovery entry points

- Stable: https://raw.githubusercontent.com/Ruckola/atonim-dependencies/main/channels/stable.json
- Beta: https://raw.githubusercontent.com/Ruckola/atonim-dependencies/main/channels/beta.json

The channel points to an exact component version manifest. A manifest then points to exact release assets, sizes and SHA-256 hashes. Production installation additionally requires an authenticated manifest trust design.

Both channels intentionally remain empty during MFA 1.0.0 publication preparation.

## Immediate delivery sequence

1. Publish only already-frozen, redistribution-prepared component bytes as immutable version-specific GitHub Release assets.
2. Record the real public asset URLs, sizes, hashes, provenance and notices in the exact component-version manifest.
3. Complete and test manifest authentication/trust before a network-driven production installer relies on the catalog.
4. Verify public downloads, hashes, component health and clean-install behavior.
5. Perform production acceptance before moving a component into stable/beta.

Tracking: [SpeechFactory #216](https://github.com/Ruckola/SpeechFactory/issues/216), [#248](https://github.com/Ruckola/SpeechFactory/issues/248).

**Do not place API keys, customer data, user Engine Profiles, private app builds, generated media, build caches or release archives directly in Git history.**
