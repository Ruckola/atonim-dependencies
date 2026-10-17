# MFA alignment distribution

The MFA component family is in **publication preparation**. It is not yet advertised by the stable or beta channels.

Independent component IDs:

- `alignment.mfa.runtime`: MFA CLI plus the validated required runtime dependency closure, packaged per platform.
- `alignment.mfa.models.en`: compatible English acoustic model + dictionary, versioned independently from the runtime.

Source recipe, compliance assembly and tests live in private `Ruckola/SpeechFactory`:

- `packaging/mfa-runtime/`
- `tools/mfa_cli_bridge.py`

Relevant tracking: [#216](https://github.com/Ruckola/SpeechFactory/issues/216), [#231](https://github.com/Ruckola/SpeechFactory/issues/231), [#248](https://github.com/Ruckola/SpeechFactory/issues/248).

## alignment.mfa.runtime 1.0.0 — frozen publication candidate

Platform: **macOS arm64**

Source authority:

- private repository: `Ruckola/SpeechFactory`
- source HEAD: `49bf4c9ecf98ff99b9d047a2616b65bbffa8f21b`
- package version: `1.0.0`
- intended immutable Release tag: `mfa-runtime-macos-arm64-v1.0.0`

Frozen runtime artifact:

- filename: `atonim-mfa-runtime-macos-arm64-1.0.0.tar.gz`
- size: `146679531` bytes
- SHA-256: `282eebf4f607d1f655183960a50510382eeaa12fd5acd1778afa1472d591fb5b`

Frozen source companion:

- filename: `atonim-mfa-runtime-macos-arm64-1.0.0-sources.tar.gz`
- size: `231113077` bytes
- SHA-256: `8b1aff243f7def93f117395703f7f97207b9420ed540d86352f27df1537466d8`

The final artifact-freeze gate passed with two independent byte-identical assemblies for both artifacts, runtime payload preservation, archive-safety checks and the focused 42-test compliance/publication suite.

This records the **frozen publication candidate**, not Publication GO, Production Acceptance or REDISTRIBUTION GO.

## Remaining publication gates

Before channel activation:

1. Publish the exact frozen bytes above as immutable GitHub Release assets in **this repository**.
2. Verify the public asset bytes still match the frozen sizes and SHA-256 values.
3. Create the exact versioned component manifest using the real immutable asset URLs.
4. Complete and test manifest authentication/trust and its client verification path.
5. Verify clean installation/provisioning and component health from the public distribution route.
6. Complete production acceptance, including applicable LGPL replacement-rights behavior.

The initial `stable` and `beta` channels continue to advertise **zero installable components** until those gates pass. Never insert placeholder URLs, synthetic checksums or a `latest` endpoint.

## Repository ownership

`Ruckola/atonim-dependencies` is the canonical distribution repository for this component. Do not publish MFA runtime/model assets to legacy `Ruckola/atonim-runtime-assets`; repository consolidation and Whisper migration are tracked in SpeechFactory #248.
