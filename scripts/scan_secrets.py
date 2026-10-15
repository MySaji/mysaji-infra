"""Download checksum-pinned official Gitleaks; redact findings on every platform."""
import hashlib
import io
from pathlib import Path
import platform
import shutil
import subprocess
import tarfile
import tempfile
import urllib.request
import zipfile

VERSION = '8.30.0'
# Official release asset digests verified through GitHub API on 2026-10-15.
ASSETS = {
    'Linux': ('linux_x64.tar.gz', '79a3ab579b53f71efd634f3aaf7e04a0fa0cf206b7ed434638d1547a2470a66e'),
    'Windows': ('windows_x64.zip', '54fe94f644b832dd08e8c3a5915efb3bfa862386d59fb27ca0792cb687a83573'),
    'Darwin': ('darwin_arm64.tar.gz', 'b251ab2bcd4cd8ba9e56ff37698c033ebf38582b477d21ebd86586d927cf87e7'),
}


def main():
    system = platform.system()
    machine = platform.machine().lower()
    if (system in {'Linux', 'Windows'} and machine not in {'x86_64', 'amd64'}) or (
            system == 'Darwin' and machine != 'arm64') or system not in ASSETS:
        raise SystemExit('Unsupported platform; install the verified Gitleaks release manually.')
    suffix, expected = ASSETS[system]
    url = f'https://github.com/gitleaks/gitleaks/releases/download/v{VERSION}/gitleaks_{VERSION}_{suffix}'
    print(f'Downloading official Gitleaks {VERSION} for {system}...', flush=True)
    with urllib.request.urlopen(url, timeout=60) as response:
        archive = response.read()
    if hashlib.sha256(archive).hexdigest() != expected:
        raise SystemExit('Gitleaks checksum mismatch; refusing execution.')
    print('Gitleaks checksum verified; scanning publishable files and Git history.', flush=True)
    executable = 'gitleaks.exe' if system == 'Windows' else 'gitleaks'
    with tempfile.TemporaryDirectory(prefix='saji-gitleaks-') as directory:
        binary = Path(directory) / executable
        if system == 'Windows':
            with zipfile.ZipFile(io.BytesIO(archive)) as bundle:
                binary.write_bytes(bundle.read(executable))
        else:
            with tarfile.open(fileobj=io.BytesIO(archive), mode='r:gz') as bundle:
                member = bundle.extractfile(executable)
                if member is None:
                    raise SystemExit('Gitleaks binary missing.')
                binary.write_bytes(member.read())
            binary.chmod(0o700)
        root = Path(__file__).resolve().parents[1]
        # Scan publishable files, not ignored local credentials or dependencies.
        snapshot = Path(directory) / 'files'
        snapshot.mkdir()
        names = subprocess.check_output(
            ['git', 'ls-files', '-z', '--cached', '--others', '--exclude-standard'], cwd=root,
        ).decode().split('\0')
        for name in set(filter(None, names)):
            source = root / name
            if source.is_file():
                destination = snapshot / name
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(source, destination)
        result = subprocess.run([str(binary), 'dir', str(snapshot), '--redact', '--no-banner'], cwd=root)
        if result.returncode:
            return result.returncode
        return subprocess.run([str(binary), 'git', '.', '--redact', '--no-banner'], cwd=root).returncode


if __name__ == '__main__':
    raise SystemExit(main())
