# Architecture and evidence

Inspected 15 October 2026. The local private application checkout is clean at
`98da6d5`. These findings establish source configuration, not live deployment.
No private source or connection values are reproduced here.

| Component | Verified source evidence |
| --- | --- |
| Application | One Next.js App Router app with server actions and HTTP handlers |
| Framework | package.json declares Next.js 16.0.10 and React/React DOM 19.2.0 |
| Language/UI | TypeScript, Tailwind and React components |
| Package manager | pnpm lockfile and workspace file; no packageManager/engines declaration |
| Data | Prisma 6.19.3, PostgreSQL schema; comments reference Supabase |
| Authentication | NextAuth/Auth.js dependency and Prisma adapter |
| Integrations | Payments, mail/SMS, AI, push, maps and monitoring code/dependencies |
| Packaging | Linux standalone output; Windows skips it unless explicitly enabled |
| Scheduling | Vercel configuration retains three cron jobs |

Local tools report Node 24.13.1 and Python 3.14.3; production runtime versions remain
unknown. An existing private architecture audit references Supabase/PostGIS and
cPanel/Passenger self-hosting. Vercel config also exists. Active hosting, databases,
storage, network and service availability were not tested. Dependencies alone do
not establish running external services.

The app's postbuild packaging script is empty. Next configuration ignores TypeScript
build errors. Packaging and independent type checking need authorized application
work before release. No app source was modified by this bootstrap.

No cloud account, DNS zone, server, Terraform state, Ansible inventory or container
platform was verified. No IaC/deployment configuration is introduced without those
decisions. Public docs must contain only approved, sanitized architecture metadata.

Neither requested MobKazi SAJI Developer/DevOps runbook PDF was found in the project
tree or user Downloads. Historical `/home/izach/Downloads` paths refer to another
machine. Existing private architecture documentation informed the review and was
checked against current files; obtain the runbooks before approving deployment.
