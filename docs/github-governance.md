# GitHub access and governance

Read-only API audit, 15 October 2026, using existing Git HTTPS authentication.
All four repositories are accessible; OliverYoung-dev has admin permission on each.
No access grants, organization settings or blocking rules were changed.

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

## Proposed settings requiring approval

For mysaji-infra, after this PR's CI passes, create a main branch ruleset under
Settings > Rules > Rulesets. Require PRs and checks `Repository validation` and
`Secret scan`; block force pushes and branch deletion. Preserve an administrator
emergency bypass with documented incident review. Begin without mandatory independent
approval until a second reviewer exists. Adding one required approval now could block
the sole maintainer. Enable stale-review dismissal/code-owner review after reviewer
coverage is established. Do not apply these rules organization-wide automatically.

Under Settings > Security (Code security / Secret protection), enable secret scanning
and push protection after approval: push protection can reject existing contributor
pushes. Enable Dependabot security updates; dependency alerts are already enabled on
the public repositories. Consider private vulnerability reporting and dependency
review when available. Investigate private repository plan support with an owner;
do not infer feature availability from public repo behavior.

Under Settings > Actions > General retain read-only token permissions and disabled
PR approval. Consider an approved Actions allowlist/SHA enforcement only after
inventorying current workflows; organization-wide enforcement can break other repos.

Review organization membership privately: individual MFA, at least two accountable
owners for recovery, minimum base permission and scoped teams. Team grants, MFA
enforcement and owner changes require explicit approval. Replace interim individual
CODEOWNERS with a verified team only when membership and access are established.

Configuration in this PR becomes effective after merge; it does not activate branch
protection, GitHub native secret scanning or security settings by itself.
