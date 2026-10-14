# Atonim Dependencies

Public distribution metadata and release index for **optional Atonim engine runtimes and language models**.

> **Status:** contract established; **no installable packages published yet**. The stable and beta channels currently have empty component catalogs. Do not mistake this repository for a working runtime download location until verified GitHub Release assets are available.

## Repository layout

| Path | Purpose |
| --- | --- |
| [`channels/stable.json`](channels/stable.json) | Stable component-version selection |
| [`channels/beta.json`](channels/beta.json) | Beta component-version selection |
| [`schemas/`](schemas/) | JSON Schema contracts for channels and components |
| [`components/alignment/mfa/`](components/alignment/mfa/) | MFA component family and planned independent runtime / language-model packs |
| [`docs/DISTRIBUTION_CONTRACT.md`](docs/DISTRIBUTION_CONTRACT.md) | Versioning, releases, integrity, trust, compatibility and publication protocol |
| [`legal/`](legal/) | License policy and third-party notices |

Binary packages will be hosted as **immutable GitHub Release assets** after reproducible builds, legal review and clean installation tests. Application code and integration logic remain in the private Atonim development repository, `Ruckola/SpeechFactory`.

## Public discovery entry points

- Stable: https://raw.githubusercontent.com/Ruckola/atonim-dependencies/main/channels/stable.json
- Beta: https://raw.githubusercontent.com/Ruckola/atonim-dependencies/main/channels/beta.json

The channel points to an exact component version manifest. A manifest then points to exact release assets, sizes and SHA-256 hashes. Production installation additionally requires an authenticated manifest trust design.

## Immediate delivery sequence

1. Audit current MFA runtime, models and their **full binary dependency/license closure** (the current Conda experiment is not redistribution-cleared).
2. Decide compliant packaging or direct-upstream provisioning and sign/secure the manifest trust chain.
3. Publish real versioned packages with third-party notices and provenance.
4. Verify publicly accessible assets, hashes, model health, macOS ARM64 alignment, and clean-install behavior.
5. Integrate Atonim provisioning, preflight before paid Combined rendering, and Retry Split from preserved masters.

Tracking: [SpeechFactory #216](https://github.com/Ruckola/SpeechFactory/issues/216), [#231](https://github.com/Ruckola/SpeechFactory/issues/231), [#234](https://github.com/Ruckola/SpeechFactory/issues/234).

**Do not place API keys, customer data, user Engine Profiles, private app builds, or generated media in this public repository.**
