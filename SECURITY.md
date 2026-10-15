# Security policy

Never put credentials, customer records or exploit details in public issues.
Use GitHub private vulnerability reporting if enabled; otherwise contact a verified
MySaji owner through an existing private channel. Private reporting availability
has not been established. Only current main receives infrastructure maintenance.
No security response-time SLA is established.

For exposed secrets: revoke/rotate immediately at the provider, audit use, notify an
owner privately and remove current exposure. Deleting files does not revoke secrets.
Coordinate history cleanup separately with explicit approval; never rewrite shared
history automatically. Inspect Actions logs/artifacts privately for further exposure.
Publish only sanitized incident details after remediation.

See [operations policy](docs/operations.md) for isolation and recovery.
