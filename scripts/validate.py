"""Offline repository guardrails; report filenames/rule names, never values."""
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def main():
    files = subprocess.check_output(
        ['git', 'ls-files', '-z', '--cached', '--others', '--exclude-standard'],
        cwd=ROOT,
    ).decode().split('\0')
    failures = []
    for name in sorted(set(filter(None, files))):
        path = ROOT / name
        if not path.is_file():
            continue
        if ((path.name.startswith('.env') and path.name != '.env.example')
                or path.suffix.lower() in {'.pem', '.key', '.p12', '.pfx', '.tfstate', '.tfplan', '.tfvars'}
                or '.tfstate.' in path.name
                or any(part in {'.aws', '.terraform', 'node_modules', '.venv'} for part in path.parts)):
            failures.append(f'{name}: forbidden sensitive/generated file')
        if path.suffix in {'.md', '.yml', '.yaml', '.py', '.txt'} or path.name.startswith('.'):
            try:
                content = path.read_text(encoding='utf-8')
            except UnicodeError:
                failures.append(f'{name}: expected UTF-8 text')
                continue
            if not content.endswith('\n') or any(line.rstrip() != line for line in content.splitlines()):
                failures.append(f'{name}: final newline or trailing whitespace')
            # Complement Gitleaks; this is not a comprehensive secret detector.
            patterns = [r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----',
                        r'\b(?:ghp|gho|ghu|ghs|github_pat)_[A-Za-z0-9_]{30,}\b',
                        r'\bAKIA[A-Z0-9]{16}\b']
            if any(re.search(pattern, content) for pattern in patterns):
                failures.append(f'{name}: possible credential; inspect privately')
        if path.name == '.env.example':
            for line in path.read_text().splitlines():
                if line.strip() and not line.lstrip().startswith('#'):
                    if '=' not in line or line.split('=', 1)[1].strip():
                        failures.append(f'{name}: template values must be empty')
    for name in filter(lambda n: n.endswith('.md'), files):
        path = ROOT / name
        if not path.exists():
            continue
        for target in re.findall(r'\]\(([^)]+)\)', path.read_text(encoding='utf-8')):
            if '://' not in target and not target.startswith('#'):
                if not (path.parent / target.split('#')[0]).exists():
                    failures.append(f'{name}: unresolved local documentation link')
    for failure in failures:
        print(failure)
    if failures:
        return 1
    print('Repository validation passed: file policy, formatting, template, credential patterns, links.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
