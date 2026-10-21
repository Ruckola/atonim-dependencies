# Unsigned release candidates

These files are review inputs only. They are deliberately outside the active
component/channel paths, have no signatures, and must never be published or
installed as-is.

`alignment.mfa.runtime-1.0.2.json` is the proposed immutable manifest for the
already-published 1.0.1 runtime archive. It adds the authenticated bounded
health declarations required by the application readiness contract; it does
not change artifact bytes, export paths, or export digests. `beta-4.json` is
the proposed next beta payload selecting that manifest.

The release operator must copy the reviewed runtime manifest to
`components/alignment/mfa/runtime/1.0.2.json`, sign it as
`component:alignment.mfa.runtime:1.0.2`, then replace and sign the active beta
channel at sequence 4. See `docs/RELEASE_OPERATIONS.md` for publication order.
