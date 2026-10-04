# Common Security

## Non-negotiables

- No secrets in source, in fixtures, in logs, in error messages, or in documents.
  `.env.example` documents required keys with placeholder values.
- All input crossing a trust boundary is validated server-side, whatever the client does.
- Parameterised queries only. String-built SQL is a defect regardless of the input source.
- Authorisation is checked on the server for every operation, including the ones the UI
  already hides. Hiding a button is presentation, not a permission check.
- Authentication state is verified per request, not per session start.

## Security is a requirement family, not a review at the end

Every security property the system must have is an `NFR-SEC-*` with a target and a
measurement method (RS-07), verified at P7 by a named ST case. "We will do a security
review before release" is not a requirement and cannot be gated.

Minimum set to define at P1, per project:

| Area | What must be decided at P1 |
|---|---|
| Identity | who authenticates, how, session lifetime, MFA scope |
| Authorisation | the role model, and where it is enforced |
| Data classification | which fields are personal, financial or regulated |
| Retention | how long each class is kept, and how it is deleted |
| Audit | which operations are logged, with what, kept how long |
| Transport | TLS policy, internal-hop policy |
| Secrets | where they live, who rotates them, how often |

An undecided item here is an `ASM-*` with an owner, not a detail to settle later. Settling
it later means settling it in code, by whoever is writing it, without a decision.

## Data handling

- Production data pulled for analysis or test fixtures must be masked before it enters the
  repository, a test environment, or any AI context. Personal data, account numbers and
  addresses in particular.
- Screenshots attached as test evidence frequently contain live customer data — mask
  before committing.
- Non-production environments get non-production credentials. A staging system with
  production API keys is a production system with a weaker password policy.

## Application-level

- Escape on output, per context (HTML, attribute, URL, SQL, shell, log).
- Never build a file path from user input without normalising and confining it.
- Uploads: verify type by content, cap size, store outside the web root, and never execute.
- Errors returned to the user say what to do, not what broke internally. Stack traces,
  SQL text, internal hostnames and library versions stay server-side.
- Rate-limit authentication, password reset, and anything that sends a message or costs
  money.

## Transport and headers

Enforce at the platform edge and verify in the application: HTTPS only with HSTS,
`nosniff`, a frame-ancestors policy, a referrer policy, and a content security policy
without `unsafe-inline` for scripts.

## Dependencies

- Pin versions. Review the lockfile diff on every dependency change.
- Run the ecosystem's audit tool in CI; a new Critical advisory blocks release.
- Know which dependencies are in the runtime image versus the build image. Build-time
  tooling shipped to production is attack surface nobody inventories.
