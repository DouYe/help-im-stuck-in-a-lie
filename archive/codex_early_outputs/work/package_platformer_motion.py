import hashlib
import json
import shutil
import zipfile
from pathlib import Path

project = Path(r"D:\Videos\Help! I'm stuck in a LIE")
source = project / 'wip/codex/platformer_motion_v1'
outputs = Path(r"C:\Users\honkw\Documents\Codex\2026-09-28\https-github-com-mexicat-pdoom-video\outputs") / 'codex_platformer_motion_v1'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()

if outputs.exists(): raise FileExistsError(outputs)
outputs.mkdir(parents=True)
records=[]
for name, delivered in [('platformer_motion_v2.mp4','2026-09-30_codex_platformer_motion_v2.mp4'),('platformer_hair_slow_v1.mp4','2026-09-30_codex_platformer_hair_slow_v1.mp4')]:
    original=source/name
    target=project/'renders'/delivered
    if target.exists(): raise FileExistsError(target)
    shutil.copy2(original,target)
    shutil.copy2(original,outputs/name)
    if sha(original)!=sha(target) or sha(original)!=sha(outputs/name): raise IOError(name)
    records.append({'file':name,'shared_project_file':str(target.relative_to(project)),'sha256':sha(original)})
playable=outputs/'playable'
playable.mkdir()
for name in ['index.html','game.js','character.js','README.md','character-notes.md','capture.mjs','motion_audit.json']:
    shutil.copy2(source/name,playable/name)
shutil.copy2(source/'qa/manual_controls_audit.json',playable/'manual_controls_audit.json')
with zipfile.ZipFile(outputs/'playable_engine.zip','x',zipfile.ZIP_DEFLATED) as z:
    for p in sorted(playable.iterdir()): z.write(p,'playable/'+p.name)
with zipfile.ZipFile(outputs/'playable_engine.zip') as z:
    if z.testzip() is not None: raise IOError('ZIP failed')
(outputs/'README_zh.md').write_text('''# Platformer 运动测试

主视频：20 秒，1920×1080 / 60 fps。当前项目 Final 音频 42.012–62.012 秒。

女孩向右跑、跳过缺口、低头躲歌词、跨越音符攻击；一次死亡重置后重新出发，结尾加速并靠近出口。头发由速度与加速度驱动的弹簧计算，下落时向上扬，落地后继续摆动再回稳。

`platformer_hair_slow_v1.mp4` 是原样片 9.2–11.2 秒的近景、半速、无声检查片段。它从同一模拟以更密的时间点重新渲染，没有使用补帧生成模型。

解压 `playable_engine.zip`，用 Chrome / Edge 打开 `playable/index.html`。点击 Play yourself：A/D 或左右移动，Space/W/上跳跃，S/下低头，R 重启。引擎不依赖网络。

这是运动和玩法原型，便于继续调整动作、场景密度、镜头和歌曲节奏；完整的音乐视频与工厂之外的结局还需后续制作。之前的图片全部保留。
''',encoding='utf-8')
(outputs/'delivery_manifest.json').write_text(json.dumps({'main_duration':20,'main_frames':1200,'fps':60,'resolution':[1920,1080],'audio_excerpt':[42.012,62.012],'files':records},indent=2),encoding='utf-8')
print(f'Delivered two verified movies and playable engine: {outputs}')
