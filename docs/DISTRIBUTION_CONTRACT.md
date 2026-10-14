# Atonim dependency distribution contract (draft v1)

This public repository is a **catalog and release-index**, not the application source, a user-profile store, or a dumping ground for binary assets.

## Boundaries
- **Source code / integration:** private `Ruckola/SpeechFactory` repository.
- **Public metadata:** versioned component manifests, channel pointers, schemas, provenance and notices in this repository.
- **Large binaries:** GitHub Releases assets, each at a version-specific immutable URL. Never commit archives, model weights, credentials, or build caches to Git.
- **User installation:** optional, user initiated, isolated from `Atonim.app` and user-owned Engine Profiles; no silently provisioned user profile.
- **Commercial licensing:** redistribution requires recorded clearance of the exact binary dependency closure, acoustic models, dictionaries and any transitive components. The current MFA Conda experiment is **not cleared** (possible GPL FFmpeg dependency). No runtime/model asset may be published until cleared. For uncleared assets, evaluate a lawful direct-from-upstream retrieval path; do not mirror them by default.

## Identity and versioning
- Component ID: e.g. `alignment.mfa.runtime`, `alignment.mfa.models.en`.
- Package release version is independent of upstream MFA/model versions and of Atonim app versions.
- Release tag convention: `<component-slug>-v<package-semver>` (e.g. `mfa-runtime-macos-arm64-v1.0.0`).
- A release is immutable: no overwriting published assets or repointing a version-specific manifest. Publish a new version instead.
- `channels/stable.json` and `channels/beta.json` are the only moving selection pointers. Unsupported components are absent, never represented by fake URLs.
- Client chooses channel -> pinned component manifest -> exact artifact and checks checksum/signature, verifies compatibility, and applies an atomic install. No `latest` download endpoints.

## Manifest trust
SHA-256 detects corruption **only if the manifest itself is trusted**. Before shipping a network-driven production installer, introduce signed manifests (and an embedded trusted verification key or equivalent pinned trust root), verified prior to trusting URLs/hashes. TLS alone and an unsigned JSON hash are not a complete supply-chain security model. Key rotation, revocation and rollback behavior require implementation/tests.

## Channels and atomic publication
1. Produce a reproducible runtime and SBOM/license inventory in the private source/build workflow.
2. Verify redistribution of each actual artifact, and document provenance/notices.
3. Publish immutable assets to GitHub Releases, obtain final sizes and SHA-256 values.
4. Add versioned manifest referencing **real** asset URLs, with tested hashes; validate against schema.
5. Publish signed manifest and update channel pointer only after all downloads are publicly accessible and clean-install tested.
6. Preserve old assets/manifests for installations pinned to earlier versions.

## Runtime preflight and recovery
Atonim must validate runtime, model and CLI execution *before* paid Combined rendering requiring auto-split. Failed splits preserve Combined masters and allow a no-TTS Retry Split. Details: `Ruckola/SpeechFactory` issues #216 and #234. Model packs are distinct from runtimes and may be updated separately.

## Operational policy
- Never store customer data, projects, API credentials or telemetric identifiers here.
- No automatic updates to already-installed user runtimes without informed action.
- Support macOS ARM64 first. Windows and Linux need their own proven builds and acceptance.
- The `main` branch metadata is public and non-secret; avoid pushing internal test data.
