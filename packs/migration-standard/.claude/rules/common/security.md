# Common Security

## Non-negotiables

- No secrets in source, in fixtures, in logs, in error messages, or in documents.
  `.env.example` documents required keys with placeholder values.
- All input crossing a trust boundary is validated server-side, whatever the client does.
- Parameterised queries only. String-built SQL is a defect regardless of the input source.
- Authorisation is checked on the server for every operation, including the ones the UI
  already hides.

## Migration-specific exposures

Legacy systems routinely embed practices that must not be carried over. These are the
exceptions to "reproduce, do not improve" — carrying them forward creates a live
vulnerability, so they are escalated rather than copied:

| Legacy practice | Action |
|---|---|
| Plaintext or reversibly-encrypted passwords | STOP, raise as a decision item, propose a hashing migration path |
| Connection strings / credentials in source or config in VCS | Do not carry over. Move to the target secret store, note in the TSD |
| Client-side-only authorisation (hidden menu = the only check) | Reimplement server-side; record in Open Items |
| Trusted-network assumption (no auth between tiers) | Raise explicitly; a web target usually invalidates the assumption |
| Unvalidated file paths from user input | Fix; note as a security-mandated deviation |

Record every such deviation in the deliverable's Open Items with kind `SECURITY-DEVIATION`
so the client sees exactly where the new system intentionally differs.

## Data handling during migration

- Production data pulled for analysis or test fixtures must be masked before it enters the
  repository or any AI context. Personal data, account numbers and addresses in particular.
- Legacy captures and screenshots frequently contain live customer data — mask before
  committing to `{{profile.legacy.screen_capture_dir}}`.

## Transport and headers

Enforce at the platform edge and verify in the target: HTTPS only with HSTS,
`nosniff`, a frame-ancestors policy, a referrer policy, and a content security policy
without `unsafe-inline` for scripts.

## Dependencies

- Pin versions. Review the lockfile diff on every dependency change.
- Run the ecosystem's audit tool in CI; a new Critical advisory blocks release.
