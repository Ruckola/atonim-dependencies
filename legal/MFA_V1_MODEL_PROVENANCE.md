# MFA V1 multilingual model provenance and notices

This document records the model provenance and redistribution notices for the Atonim V1 Montreal Forced Aligner (MFA) language components. It is release evidence for the exact model files identified below; it does not grant an umbrella license over this repository.

## Attribution

Montreal Forced Aligner pretrained models are provided by the Montreal Corpus Tools project. Where indicated below, the upstream model license is Creative Commons Attribution 4.0 International (CC BY 4.0). Attribution for the MFA model line is to Michael McAuliffe and Morgan Sonderegger, together with any upstream corpora or resources identified by the corresponding MFA model metadata. Redistributors must preserve the applicable CC BY 4.0 attribution and notices.

The Dutch `dutch_cv` acoustic model and dictionary are recorded as CC0 in the MFA model metadata used for this release. Atonim's Dutch G2P archive is a Ruckola-produced portable MFA/Pynini model trained from the approved Dutch dictionary; its source dictionary digest is recorded below.

## Exact V1 assets

### English — `alignment.mfa.models.en`

Language: `en`

Upstream:
- acoustic model: `english_mfa` 3.1.0 — CC BY 4.0
- dictionary: `english_mfa` 3.1.0 — CC BY 4.0
- no G2P model is included in this component

Exact files:
- `models/acoustic.zip` SHA-256 `2c08bd4f82c3943dd57ac09aeac99dbce17a1e1bfe9fd932c8d95cd13d971068`
- `models/dictionary.dict` SHA-256 `975bf9c7791535c5aec57995e0bd2b77eb7ca364d1d974c2134e07bb0f16b079`

### Dutch — `alignment.mfa.models.nl`

Language: `nl`

Upstream:
- acoustic model: `dutch_cv` 2.0.0 — CC0
- dictionary: `dutch_cv` 2.0.0 — CC0
- G2P: Ruckola-produced portable MFA/Pynini model trained from the approved Dutch dictionary

Exact files:
- `models/acoustic.zip` SHA-256 `7ad2db98cd0ae9787a91a7ad0adc83b08a6dd5995a4c17bd61077d620d1b09ec`
- `models/dictionary.dict` SHA-256 `40a8230d5a9b317e17066b8574349ae1063175408d7439eaccaf40eaa7a618b6`
- `models/g2p.zip` SHA-256 `56e5b114eb9c9ef2ad53805e5723876c2ef15f62dd0ab22d92baada13601e77c`
- G2P source dictionary SHA-256 `40a8230d5a9b317e17066b8574349ae1063175408d7439eaccaf40eaa7a618b6`

### German — `alignment.mfa.models.de`

Language: `de`

Upstream:
- acoustic model: `german_mfa` 3.0.0 — CC BY 4.0
- dictionary: `german_mfa` 3.0.0 — CC BY 4.0
- G2P: `german_mfa` 3.0.0 — CC BY 4.0

Exact files:
- `models/acoustic.zip` SHA-256 `9a9e0f032f0e1ff2014ed42da60f2c88efb8a9a122c3da09adc2de30e4c48322`
- `models/dictionary.dict` SHA-256 `a73c24711fd29fa20e09ec133ff850a52a2759d1d79c362b4c20f12db2ff251c`
- `models/g2p.zip` SHA-256 `ab5340cb0ff19a5e383564b4adf5db301e8d8bf23218d6b0e4e37d38a8943f73`

### French — `alignment.mfa.models.fr`

Language: `fr`

Upstream:
- acoustic model: `french_mfa` 3.0.0 — CC BY 4.0
- dictionary: `french_mfa` 3.0.0 — CC BY 4.0
- G2P: `french_mfa` 3.0.0 — CC BY 4.0

Exact files:
- `models/acoustic.zip` SHA-256 `37163d109c89706d447ed582a0f8902a1212ea68e09004b876f5fc02a711226a`
- `models/dictionary.dict` SHA-256 `e28e20fceb4141221df9de6abb8fd96f26ed57f1a5a9429a9380905b0b4616d7`
- `models/g2p.zip` SHA-256 `d4ebbb146ca123e887d2f0c17d09dff6c4f4a7d51a5be49c5564fb7f4a80d3c4`

### Spanish (Latin America) — `alignment.mfa.models.es419`

Language: `es-419`

Upstream:
- acoustic model: `spanish_mfa` 3.3.0 — CC BY 4.0
- dictionary: `spanish_latin_america_mfa` 3.3.0 — CC BY 4.0
- G2P: `spanish_latin_america_mfa` 3.3.0 — CC BY 4.0

Exact files:
- `models/acoustic.zip` SHA-256 `287f0a6a0f0c38380e794ea92e1eb04d5d61a6c24c8cd795b832e00d7939f15f`
- `models/dictionary.dict` SHA-256 `c7f0dd55a9feed3420767c887ccb8ce033f9e7f8abdba54cb75f0519b2d68e74`
- `models/g2p.zip` SHA-256 `58e0743cf364d8aa2cc8b419e7c95dd9127908268af670f305722c601f726b2a`

### Portuguese (Brazil) — `alignment.mfa.models.ptbr`

Language: `pt-BR`

Upstream:
- acoustic model: `portuguese_mfa` 2.0.0 — CC BY 4.0
- dictionary: `portuguese_brazil_mfa` 2.0.0 — CC BY 4.0
- G2P: `portuguese_brazil_mfa` 2.0.0 — CC BY 4.0

Exact files:
- `models/acoustic.zip` SHA-256 `d5e5156d25f38b254add200ac3fa000e7e13c0993a32934ef28a1c1bb1a9e7ca`
- `models/dictionary.dict` SHA-256 `8a51a8a05682da6c9f93dc29334158cdbb93be96cd9e3742065f6ae8f64ecd8c`
- `models/g2p.zip` SHA-256 `11e7f72ecccbae7905fa064017ac1a1fead9b6ebfdde4e23e506c28edfbcbcc8`

## Redistribution checklist

Before any manifest for these components is published with `redistribution.cleared: true`:

1. Verify each file digest above against the canonical release artifact.
2. Preserve the applicable CC BY 4.0 attribution and license notice in the public distribution materials.
3. Preserve the CC0 identification for the Dutch upstream assets.
4. Record the canonical artifact digest and sizes in the signed component manifest.
5. Validate the component manifest against `schemas/component-v2.schema.json`.
6. Sign the final manifest with the production metadata signing key.
7. Do not treat this document as clearance for the MFA runtime; runtime compliance is reviewed separately.
