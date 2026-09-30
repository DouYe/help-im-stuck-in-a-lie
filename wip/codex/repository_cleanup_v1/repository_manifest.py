"""Build/verify a portable tracked-file manifest, including original LFS media hashes."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys

root = Path(__file__).resolve().parents[3]
manifest_name = 'coordination/REPOSITORY_MANIFEST.json'

def git(*args):
    return subprocess.check_output(['git', *args], cwd=root)

def index():
    result = {}
    for item in git('ls-files', '--stage', '-z').split(b'\0'):
        if not item:
            continue
        meta, name = item.split(b'\t', 1)
        mode, blob, stage = meta.decode().split()
        assert stage == '0'
        result[name.decode('utf-8')] = {'mode': mode, 'git_blob': blob}
    return result

tracked = index()
if len(sys.argv) > 1 and sys.argv[1] == 'verify':
    data = json.loads((root / manifest_name).read_text(encoding='utf-8'))
    for entry in data['files']:
        name = entry['path']
        assert name in tracked and tracked[name]['git_blob'] == entry['git_blob'], name
        path = root / name
        assert path.is_file(), name
        if entry['storage'] == 'lfs':
            assert path.stat().st_size == entry['bytes'], name
            assert hashlib.sha256(path.read_bytes()).hexdigest() == entry['sha256'], name
    unexpected = sorted(set(tracked) - {r['path'] for r in data['files']} - {manifest_name})
    assert not unexpected, unexpected
    assert not git('diff', '--name-only').strip(), 'Working tree modifications found'
    print(json.dumps({'tracked_files_verified': len(data['files']) + 1,
                      'lfs_media_verified': sum(r['storage'] == 'lfs' for r in data['files']),
                      'result': 'passed'}))
else:
    lfs = {r['name']: r for r in json.loads(git('lfs', 'ls-files', '--json'))['files']}
    files = []
    for name, info in sorted(tracked.items()):
        if name == manifest_name:
            continue
        entry = {'path': name, **info, 'storage': 'git'}
        if name in lfs:
            entry.update(storage='lfs', sha256=lfs[name]['oid'], bytes=lfs[name]['size'])
        files.append(entry)
    data = {'date': '2026-09-30', 'repository': 'https://github.com/DouYe/help-im-stuck-in-a-lie',
            'scope': 'All tracked project paths except this manifest itself. Text/source Git object hashes allow line-ending normalization; LFS hashes verify actual full media bytes.',
            'files': files}
    (root / manifest_name).write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    print(json.dumps({'files_in_manifest': len(files), 'lfs_files': len(lfs),
                      'lfs_unique_objects': len({r['oid'] for r in lfs.values()}),
                      'lfs_bytes_in_tree': sum(r['size'] for r in lfs.values())}))
