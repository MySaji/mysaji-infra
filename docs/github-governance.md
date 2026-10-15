# GitHub access and governance

Initial read-only API audit, 15 October 2026, using existing Git HTTPS authentication.
All four repositories are accessible; OliverYoung-dev has admin permission on each.
The table records the initial state. Approved subsequent changes are recorded below.
No access grants or organization settings were changed.

| Repository | Visibility | Main/protection | Rulesets | Dependency alerts |
| --- | --- | --- | --- | --- |
| mysaji-infra | Public | Main exists, unprotected | None | Enabled (HTTP 204) |
| mysaji-docs | Public | Main lookup HTTP 404 | None | Enabled (HTTP 204) |
| mysaji-marketing | Public | Main lookup HTTP 404 | None | Enabled (HTTP 204) |
| MySaji | Private | Main exists, unprotected | HTTP 403 | HTTP 404; unavailable/unverified |

Docs/marketing may be empty; the 404 does not establish a protected branch. Private
ruleset/alert results need owner investigation; plan support is not established.
For all four, Actions is enabled, all actions are allowed, SHA enforcement is off,
default token permission is read and Actions cannot approve PRs. The public repos
report secret scanning, push protection and Dependabot security updates disabled.
Private security feature state is not exposed in the repository response.

## Applied safeguards after user approval

On 15 October 2026, the user approved continuing with the mysaji-infra-only settings.
After verifying both CI checks passed on the PR head, the repository API was used to
create [SAJI main protection](https://github.com/MySaji/mysaji-infra/rules/25195553),
ruleset ID `25195553`. Independent read-back confirmed active enforcement:

- Applies only to `refs/heads/main` in `MySaji/mysaji-infra`.
- Requires pull requests and successful `Repository validation` and `Secret scan`
  checks from the GitHub Actions integration (ID `15368`). The branch must be current
  with main before merging.
- Blocks force pushes and branch deletion, subject to administrator emergency bypass.
- Requires zero independent approvals until a second qualified reviewer is available.
- Repository administrators retain always-available bypass (repository role ID `5`).
  Use only for documented emergencies, record the reason and affected commit privately
  if sensitive, and follow with a reviewed corrective PR and incident review.

Read-back also confirmed native secret scanning and secret-scanning push protection
enabled, Dependabot security updates enabled and not paused, and dependency alerts
enabled. Actions token defaults remain read-only and Actions PR approval remains
disabled. No other repository or organization settings were changed.

These GitHub settings are live independently of merging PR #1. The CI configuration,
ownership and dependency update files still require PR merge to become main's defaults.
No test force push, branch deletion or real credential push was attempted.

## Follow-up governance recommendations

Inspect the live main ruleset under Settings > Rules > Rulesets. Enable one required
approval, stale-review dismissal and code-owner review only after reviewer coverage
is established and approved. Do not apply these rules organization-wide automatically.

Under Settings > Security (Code security / Secret protection), maintain the enabled
mysaji-infra secret scanning and push protection: protection can reject contributor
pushes containing supported secrets. Other public repositories retain their audited
settings. Consider private vulnerability reporting and dependency
review when available. Investigate private repository plan support with an owner;
do not infer feature availability from public repo behavior.

Under Settings > Actions > General retain read-only token permissions and disabled
PR approval. Consider an approved Actions allowlist/SHA enforcement only after
inventorying current workflows; organization-wide enforcement can break other repos.

Review organization membership privately: individual MFA, at least two accountable
owners for recovery, minimum base permission and scoped teams. Team grants, MFA
enforcement and owner changes require explicit approval. Replace interim individual
CODEOWNERS with a verified team only when membership and access are established.

Repository files become main's configuration after merge. Live rulesets and native
security controls are separately managed GitHub settings; review both when auditing.
