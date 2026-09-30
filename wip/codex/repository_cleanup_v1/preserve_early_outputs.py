"""Copy audited unique early project work into the canonical tree, excluding old audio."""
from pathlib import Path
import hashlib
import json
import shutil
import zipfile

root = Path(__file__).resolve().parents[3]
audit = json.loads((Path(__file__).parent / 'codex_workspace_unique.json').read_text(encoding='utf-8-sig'))
audio = {'.mp3', '.flac', '.wav', '.ogg', '.m4a', '.aac'}
ledger = []
for record in audit['candidates']:
    source = Path(record['source_abs'])
    target = (root / record['target_relative']).resolve()
    assert root.resolve() in target.parents
    assert source.suffix.lower() not in audio
    assert hashlib.sha256(source.read_bytes()).hexdigest() == record['sha256'].lower()
    if record['disposition'] == 'sanitize_zip_before_preserving':
        target = target.with_name(target.stem + '_without_audio.zip')
    if target.exists():
        raise SystemExit(f'Refusing existing target: {target}')
    target.parent.mkdir(parents=True, exist_ok=True)
    item = {'source': source.relative_to(Path(audit['source_root'])).as_posix(),
            'target': target.relative_to(root).as_posix(), 'source_sha256': record['sha256']}
    if record['disposition'] == 'sanitize_zip_before_preserving':
        retained, removed = [], []
        with zipfile.ZipFile(source) as old, zipfile.ZipFile(target, 'w') as new:
            for entry in old.infolist():
                content = old.read(entry.filename)
                info = {'name': entry.filename, 'sha256': hashlib.sha256(content).hexdigest()}
                if Path(entry.filename).suffix.lower() in audio:
                    removed.append(info)
                else:
                    new.writestr(entry, content)
                    retained.append(info)
        with zipfile.ZipFile(target) as verify:
            assert verify.testzip() is None
            assert verify.namelist() == [entry['name'] for entry in retained]
            for entry in retained:
                assert hashlib.sha256(verify.read(entry['name'])).hexdigest() == entry['sha256']
        item.update(retained_verified=retained, old_audio_removed=removed)
    else:
        shutil.copy2(source, target)
        assert hashlib.sha256(target.read_bytes()).hexdigest() == record['sha256'].lower()
    item['target_sha256'] = hashlib.sha256(target.read_bytes()).hexdigest()
    item['bytes'] = target.stat().st_size
    ledger.append(item)
destination = root / 'archive/codex_early_outputs'
(destination / 'import-manifest.json').write_text(json.dumps(ledger, indent=2), encoding='utf-8')
print(json.dumps({'files_preserved': len(ledger), 'bytes': sum(r['bytes'] for r in ledger),
                  'sanitized_zips': sum('old_audio_removed' in r for r in ledger),
                  'all_hashes_verified': True}))
