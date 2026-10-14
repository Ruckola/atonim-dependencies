# MFA alignment distribution

This component family is **not published yet**.

Proposed independent component IDs:
- `alignment.mfa.runtime`: MFA CLI plus validated required runtime dependencies, with per-platform release artifacts.
- `alignment.mfa.models.en`: compatible English acoustic model + dictionary (and explicitly selected G2P if needed), versioned independently of runtime.

Source recipe and tests currently live in private `Ruckola/SpeechFactory`:
`packaging/mfa-runtime/`, `tools/mfa_cli_bridge.py`.
Relevant issues: [#216](https://github.com/Ruckola/SpeechFactory/issues/216), [#231](https://github.com/Ruckola/SpeechFactory/issues/231), [#234](https://github.com/Ruckola/SpeechFactory/issues/234).

Known macOS ARM64 experiment: MFA 3.4.3 on Python 3.11.17, English `english_mfa` acoustic and dictionary. **Not redistribution-cleared**; prior Conda closure included an FFmpeg dependency requiring legal review. No public binary/model distribution until documented clearance and physical validation.

The initial `stable` and `beta` channels intentionally advertise **zero installable components**. Never insert placeholder download URLs or synthetic checksums. The installer must handle unavailable components explicitly and safely.
