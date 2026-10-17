# Public Engine Profile recipes for Atonim

**Status:** Accepted catalog-location decision, 2026-10-17. **Content status:** catalog structure defined; no profile is yet published or claimed tested.

This is the **canonical public location** for downloadable, user-owned Atonim **Engine Profile JSON recipes**. It is separate from `channels/stable.json`, `channels/beta.json` and binary runtime/model distribution.

## Public entry point

- Human-readable catalog: https://github.com/Ruckola/atonim-dependencies/tree/main/engine-profiles
- This README is the canonical landing page for Atonim's **Get Engine Profiles** help link and the Ruckola website's Engine Profiles download section.
- Profile files will be linked here **individually by tested version**, rather than treating an entire folder as an automatically trusted feed.

## Proposed layout

```text
engine-profiles/
  README.md
  catalog.json                 # proposed index; not yet implemented or published
  schemas/                     # public catalog metadata validation, when implemented
  recipes/
    <provider>/
      <stable-recipe-name>-v<recipe-semver>.json
  guides/
    <provider>-setup.md
```

Paths below this README are **reserved naming conventions**, not claims that these files exist.

## Publication contract

1. A recipe is a **user-importable Engine Profile JSON object**, conforming to the release-compatible schema implemented by `Ruckola/SpeechFactory/services/engine_profile_service.py`. Do **not** substitute an internal `profile_support/recipes` wrapper for an importable profile without an explicit conversion step.
2. The recipe contains **no credentials, API keys, user paths, account identifiers, personal voices, private endpoints or third-party binary weights**.
3. Give every recipe an explicit ID, version, intended operation (TTS, Voice Change, alignment), provider, compatible Atonim version/build, prerequisites and source/API contract. Keep its provider-specific beginner setup article adjacent in `guides/`.
4. No recipe is labeled **Tested** until import, credential configuration, discovery (if applicable), one actual permitted rendering request, take creation and safe failure paths have passed on a clean supported build.
5. Recipe versions are immutable after publication; issue a new filename for a change. Retain older compatible versions and document deprecations. Protect published JSON with review and recorded SHA-256 digest in a future catalog manifest.
6. **Manual downloads** use a visible GitHub source/file page with an explicit raw-file link and import instructions. Do not silently install, update or overwrite user profiles.
7. If Atonim gains a **built-in remote catalog browser**, require HTTPS, explicit user opt-in/confirmation, verified manifest integrity/authenticity and strict JSON schema validation before automatic import. A GitHub folder listing or unsigned JSON feed is not an authenticated software-update service.
8. Link to the same canonical catalog from the application's UI/Help and the public website; site may present a nicer facade but must not host conflicting copies.

## Separation from optional runtime catalog

A tiny JSON recipe is **not** the same as a runnable engine or downloadable AI model. The existing `components/`, `channels/` and signed-manifest trust architecture remains authoritative for external runtime/model packages. A recipe can point users toward a separately provisioned runtime but cannot claim to install it.

## First release milestone

Publish one complete, verified beginner profile for a hosted TTS provider and its step-by-step guide, with provider permissions and costs explained, plus a matching Voice Chain onboarding procedure in the Atonim manual. The exact provider/recipe stays **unassigned** until its real configuration and rights are verified.

**Current catalog:** no provider recipe or download is declared available by this document. Do not link to a hypothetical JSON file as if it exists.
