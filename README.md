# SAJI Infrastructure

Infrastructure and DevOps foundation for SAJI Solutions and MySaji. This repository
validates its configuration and documents safe operations. No live deployment or
resource provisioning is configured.

| Path | Purpose |
| --- | --- |
| `.github/` | CI, ownership, dependency updates and PR template |
| `scripts/` | Repository validation, YAML lint dependencies and secret scanning |
| `docs/architecture.md` | Verified stack and deployment uncertainties |
| `docs/operations.md` | Environments, secrets, readiness and recovery |
| `docs/github-governance.md` | Access audit and proposed safeguards |
| `docs/bootstrap-report.md` | Evidence, limitations and follow-up work |

Terraform, Ansible, Docker and environment directories await verified requirements.

## Local validation

Use Python 3.12+ and Git. No application or cloud credentials are needed.
From this repository in PowerShell:

```powershell
python -m venv .venv
.venv/Scripts/python -m pip install -r scripts/requirements.txt
.venv/Scripts/python scripts/validate.py
.venv/Scripts/python -m yamllint .
.venv/Scripts/python scripts/scan_secrets.py
git diff --check
```

On Linux/macOS use `.venv/bin/python`. Secret scanning downloads a checksum-pinned
Gitleaks binary; it supports Linux/Windows x64 and macOS arm64. It scans publishable
files and Git history, excluding ignored local credentials/dependencies from the file scan.

Read [CONTRIBUTING.md](CONTRIBUTING.md) and [SECURITY.md](SECURITY.md) before publishing changes.
