from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import shutil, json, hashlib, zipfile

root = Path(__file__).resolve().parent
project = root.parents[2]
out = Path(r"C:\Users\honkw\Documents\Codex\2026-09-28\https-github-com-mexicat-pdoom-video\outputs\codex_six_worlds_motion_v1")
shared = project / 'design/keyframes/codex_six_worlds_motion_v1'
movie = root / 'six_worlds_motion_v1.mp4'
assert movie.is_file(), 'Render first'
assert not out.exists(), 'Delivery exists: use a new version'
assert not shared.exists(), 'Shared stills exist: use a new version'
out.mkdir(parents=True)
shared.mkdir(parents=True)
playable = out / 'playable'
playable.mkdir()
entries = [(1.5,'01_MUSIC_FACTORY'),(4.8,'02_VERTICAL_MEMORY'),(8.0,'03_BUFFER_SEA'),(11.5,'04_ROUTE_GRID'),(15.2,'05_SKY_SCORE'),(18.5,'06_LYRIC_CATHEDRAL')]
sheet = Image.new('RGB',(1920,804),'#0a0a0b')
draw = ImageDraw.Draw(sheet)
font = ImageFont.truetype(r'C:\Windows\Fonts\consola.ttf',20)
for i,(t,name) in enumerate(entries):
    source = root / 'qa' / f'frame_{t:.1f}.png'
    frame = Image.open(source).convert('RGB')
    frame.resize((640,360),Image.Resampling.LANCZOS).save(root / 'qa' / f'thumb_{i+1}.png')
    x,y=(i%3)*640,(i//3)*402
    sheet.paste(frame.resize((640,360),Image.Resampling.LANCZOS),(x,y))
    draw.text((x+16,y+370),f'{name.replace("_"," ")} / {t:.1f}s',font=font,fill='#eee9df')
    shutil.copy2(source,shared/f'{name}.png')
sheet.save(shared/'six_worlds_review_sheet.png')
shutil.copy2(shared/'six_worlds_review_sheet.png',out/'six_worlds_review_sheet.png')
shutil.copy2(movie,out/movie.name)
render = project / 'renders/2026-09-30_codex_six_worlds_motion_v1.mp4'
assert not render.exists(), 'Shared render exists'
shutil.copy2(movie,render)
source_names=['index.html','game.js','character.js','worlds.js','topdown.js','preview_audio.mp3','README.md','capture.mjs','control-qa-v2.mjs','control-qa-v2.json','motion_audit.json','worlds-notes.md','topdown-notes.md','character-notes-v2.md']
for name in source_names:
    source=root/name
    if source.exists(): shutil.copy2(source,playable/name)
with zipfile.ZipFile(out/'playable_engine.zip','w',zipfile.ZIP_DEFLATED) as z:
    for p in playable.iterdir(): z.write(p,p.name)
shutil.copy2(root/'README.md',out/'README.md')
shared.joinpath('README.md').write_text('Six captured frames from Codex T24 motion revision. Proposals for review, not selected final scenes. See docs/CODEX_SIX_WORLDS_MOTION_V1.md. All older stills and movies retained.\n',encoding='utf-8')
audit=json.loads(root.joinpath('motion_audit.json').read_text(encoding='utf-8'))
manifest={'status':'motion proposal for Hon review','duration':20,'fps':60,'resolution':[1920,1080],'master':'audio/final/song.mp3','audioRange':[42.012,62.012],'hazards':sum(e['kind']=='fire' for e in audit['events']),'events':{k:sum(e['kind']==k for e in audit['events']) for k in ['cut','jump','double-jump','dash','death','respawn','dodge','exit']},'files':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in shared.glob('*.png')}}
shared.joinpath('manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
out.joinpath('manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
print(json.dumps({'outputs':str(out),'sharedFrames':str(shared),'sharedRender':str(render),'manifest':manifest},indent=2))
