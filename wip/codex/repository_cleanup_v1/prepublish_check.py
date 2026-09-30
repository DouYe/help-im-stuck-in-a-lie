"""Check the public project tree, ZIP audio cleanup and source credential patterns."""
from pathlib import Path
import json
import re
import zipfile

root = Path(__file__).resolve().parents[3]
skipped = {'.git', 'node_modules', '__pycache__', '.venv', 'venv', '.tmp'}
audio = {'.mp3', '.flac', '.wav', '.ogg', '.m4a', '.aac'}
text = {'.py', '.ps1', '.ts', '.js', '.mjs', '.json', '.md', '.txt', '.html', '.css', '.yml', '.yaml', '.toml'}
pattern = re.compile(rb'(?:ghp_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|sk-[A-Za-z0-9_-]{30,}|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----)')
files, secret_paths, loose_audio, zip_audio = [], [], [], []
for path in root.rglob('*'):
    if not path.is_file() or any(part in skipped for part in path.relative_to(root).parts):
        continue
    relative = path.relative_to(root).as_posix()
    files.append((relative, path.stat().st_size))
    if path.suffix.lower() in audio:
        loose_audio.append(relative)
    if path.name.startswith('.env') and path.name != '.env.example':
        secret_paths.append(relative)
    if path.suffix.lower() in text and pattern.search(path.read_bytes()):
        secret_paths.append(relative)
    if path.suffix.lower() == '.zip':
        with zipfile.ZipFile(path) as archive:
            assert archive.testzip() is None, relative
            for name in archive.namelist():
                suffix = Path(name).suffix.lower()
                if suffix in audio:
                    zip_audio.append(f'{relative}!{name}')
                if suffix in text and pattern.search(archive.read(name)):
                    secret_paths.append(f'{relative}!{name}')
report = {'checked_files': len(files), 'bytes': sum(size for _, size in files),
          'loose_song_audio': loose_audio, 'audio_inside_zips': zip_audio,
          'credential_pattern_paths': sorted(set(secret_paths)), 'zip_integrity_passed': True,
          'scope': 'Project deliverables; excludes Git/dependencies/temporary caches. Pattern scan is a bounded check, not a guarantee about every possible secret format.'}
(Path(__file__).parent / 'prepublish-check.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
print(json.dumps(report))
assert not loose_audio and not zip_audio and not secret_paths
