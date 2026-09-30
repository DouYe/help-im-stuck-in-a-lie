"""One-time archival cleanup: retain every non-MP3 ZIP member, verified by SHA-256."""
import hashlib
import json
from pathlib import Path
import zipfile

root = Path(__file__).resolve().parents[3]
source = root / 'lie-video-project.zip'
target = root / 'archive/lie-video-project_without_audio.zip'
report = root / 'archive/snapshot-sanitization.json'
target.parent.mkdir(parents=True, exist_ok=True)
if target.exists():
    raise SystemExit('Refusing to overwrite existing sanitized snapshot')
retained, removed = [], []
with zipfile.ZipFile(source) as old, zipfile.ZipFile(target, 'w', compression=zipfile.ZIP_DEFLATED) as new:
    for item in old.infolist():
        data = old.read(item.filename)
        record = {'name': item.filename, 'size': len(data), 'sha256': hashlib.sha256(data).hexdigest()}
        if item.filename.lower().endswith('.mp3'):
            removed.append(record)
        else:
            new.writestr(item, data)
            retained.append(record)
with zipfile.ZipFile(target) as check:
    assert check.testzip() is None
    assert check.namelist() == [r['name'] for r in retained]
    for record in retained:
        assert hashlib.sha256(check.read(record['name'])).hexdigest() == record['sha256']
report.write_text(json.dumps({'source': source.name, 'target': target.relative_to(root).as_posix(),
    'all_non_audio_members_verified': True, 'retained': retained, 'removed_mp3': removed}, indent=2), encoding='utf-8')
print(json.dumps({'retained': len(retained), 'removed_mp3': len(removed), 'verified': True}))
