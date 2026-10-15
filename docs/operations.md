# Operations policy

## Environments and secrets

Development, staging and production are intended boundaries, not verified resources.
Each needs isolated databases, service accounts, callbacks and credentials. Never use
production credentials or unsanitized customer data in development or previews.
Use sandbox payment providers outside production.

Infrastructure validation requires no secrets. `.env.example` contains comments;
future approved variables must have empty values. Ignore/validation rules exclude
environment files, keys and state. Force-staging bypasses ignores: always scan.
Keep development secrets in an approved password manager and local ignored files.
Future deployment should use scoped GitHub environment secrets or short-lived OIDC
when supported. Production requires separately approved environments and reviewers.
Never expose secrets to fork PRs, echo credentials or use shell tracing around them.
`NEXT_PUBLIC_` variables are browser-visible and cannot hold secrets.

## CI/CD

Infrastructure CI runs on PRs, supported branch pushes and manual dispatch. It uses
read-only contents permission, no deployment secrets, pinned Actions, timeouts and
checkout without persisted authentication. Repository guardrails check forbidden
files, formatting, empty template values, local documentation links and selected
credential patterns. YAML lint validates configuration. Checksum-pinned Gitleaks
scans files and complete reachable Git history with redaction. No scan guarantees
absence of secrets. Dependabot proposes weekly Actions and Python updates.

No shell scripts or Terraform exist, so their checks are not applicable. App builds
belong in the private app repository. Never execute contributor code through
pull_request_target with elevated privileges. Review dependency updates before merge.
The downloaded Gitleaks version/checksums require manual reviewed updates; Dependabot
does not discover versions embedded in Python constants.

## Deployment readiness checklist

- Confirm host, owners, region, budget, data residency, runtime and pnpm versions.
- Establish reproducible Linux builds and repair standalone packaging in an app PR.
- Run independent type checking, security review and application tests.
- Inventory integrations privately; verify sandbox callbacks and payment idempotency.
- Verify PostgreSQL/PostGIS requirements and an audited migration process.
  Development db push/migrate dev commands are not production migration procedures.
- Prove database/storage restoration and schema compatibility before migrations.
- Verify uploads, TLS, networking, authorized cron scheduling and outbound mail.
- Add health checks, monitoring, alerts and named incident ownership.
- Agree recovery objectives and exercise staging deployment and rollback.
- Approve a concrete deployment change separately before production execution.

## Disaster recovery

Git preserves configuration, not databases, uploaded files or provider settings.
Agree RPO/RTO with business owners before setting backup frequency/retention. Assign
a backup owner; encrypt backups, restrict access and isolate copies where feasible.
Monitor backup failures and periodically restore into an isolated environment with
live payments/callbacks disabled. Record restoration duration and integrity evidence
without customer data.

Revert repository regressions through a PR and rerun CI. Future deployment must retain
a known-good artifact/configuration revision and tested traffic rollback procedure.
Database rollback may need forward repair; never blindly reverse migrations. An
authorized incident owner must verify health, auth, integrity, payments, cron jobs
and alerts before reopening traffic after recovery.
