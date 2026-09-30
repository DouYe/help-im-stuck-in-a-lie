"""Build a review sheet for Codex's five proposed character-world keyframes."""
from pathlib import Path
import sys

BASE = Path(r"D:\Videos\Help! I'm stuck in a LIE")
sys.path.insert(0, str(BASE / "wip/codex/visual_audit/lib"))
from PIL import Image, ImageDraw, ImageFont

W, H = 2064, 2160
PW, PH, LH = 980, 551, 70
INK, INK2, BONE, ASH, GRAPHITE = '#0A0A0B', '#161618', '#EEE9DF', '#9C978F', '#5E5B57'
FONT = BASE / 'app/public/fonts/src/IBMPlexMono-Bold.ttf'
REG = BASE / 'app/public/fonts/src/IBMPlexMono-Regular.ttf'
TITLE = BASE / 'app/public/fonts/Archivo-w1250-900.ttf'
OUT = BASE / 'wip/codex/root/selection_sheet.png'

f_title = ImageFont.truetype(str(TITLE), 55)
f_sub = ImageFont.truetype(str(REG), 21)
f_head = ImageFont.truetype(str(FONT), 25)
f_note = ImageFont.truetype(str(REG), 19)
f_small = ImageFont.truetype(str(REG), 16)

frames = [
    ('A', 'THE PROMPT PRESS', '~21.5 s / verse 1', BASE/'wip/codex/visual_audit/KF_A_prompt_factory.png'),
    ('B', 'FALSE FLOOR', '46.78 s / lie', BASE/'wip/codex/tech_audit/01_stuck_side_chute.png'),
    ('C', 'VIEWPOINT RUPTURE', '47.50 s / make', BASE/'wip/codex/tech_audit/02_make_me_real_deep_maze.png'),
    ('D', 'THE REAL THRESHOLD', '50.53 s / real this time', BASE/'wip/codex/root/50_53_real_threshold.png'),
    ('E', 'HEART CROSS-SECTION', '58.66 s / heart inside', BASE/'wip/codex/visual_audit/KF_B_heart_interior.png'),
]

sheet = Image.new('RGB', (W, H), INK)
d = ImageDraw.Draw(sheet)
d.text((36, 26), 'HELP! I\'M STUCK IN A LIE', font=f_title, fill=BONE)
d.text((38, 94), 'CODEX  /  FIVE PROPOSED SCENES  /  THE SAME SYMBOL GIRL', font=f_sub, fill=ASH)
d.line((36, 138, W-36, 138), fill=GRAPHITE, width=2)

top = 170
for i, (letter, name, timing, path) in enumerate(frames):
    x = 36 + (i%2)*(PW+32)
    y = top + (i//2)*(PH+LH+32)
    im = Image.open(path).convert('RGB')
    if im.size != (1920,1080):
        raise ValueError(f'{path}: unexpected size {im.size}')
    sheet.paste(im.resize((PW, PH), Image.Resampling.LANCZOS), (x,y))
    d.rectangle((x,y,x+PW-1,y+PH-1), outline=GRAPHITE, width=2)
    d.text((x, y+PH+13), letter+'  '+name, font=f_head, fill=BONE)
    tb = d.textbbox((0,0), timing, font=f_note)
    d.text((x+PW-(tb[2]-tb[0]), y+PH+18), timing, font=f_note, fill=ASH)

# Sixth cell is the comparison key, not a rendered video frame.
x, y = 36+PW+32, top+2*(PH+LH+32)
d.rectangle((x,y,x+PW-1,y+PH-1), outline=GRAPHITE, width=2)
d.text((x+40, y+38), 'READ THE CUT', font=f_head, fill=BONE)
d.line((x+40,y+85,x+PW-40,y+85), fill=GRAPHITE, width=2)
notes = [
    'B --> C     One girl, same screen anchor.',
    '            The world changes dimension.',
    '',
    'C --> D     The camera closes in on REAL.',
    '            Her eyes and heart become legible.',
    '',
    'D ... E     Later, the heart becomes a world.',
    '            Density gives way to a held beat.',
    '',
    'Selected moments, not a finished sequence.',
    'A is a verse option; B-E are chorus options.',
    'Existing Claude keyframes remain separate.',
]
yy = y+119
for line in notes:
    if line: d.text((x+40, yy), line, font=f_note, fill=ASH)
    yy += 36
d.text((x, y+PH+13), 'F  SHOT RELATIONSHIP', font=f_head, fill=BONE)
d.text((x, y+PH+47), 'Visuals are proposals, not locked designs.', font=f_small, fill=ASH)

d.line((36, H-52, W-36, H-52), fill=GRAPHITE, width=2)
d.text((36, H-38), 'CHARACTER: STYLE 1 / 17 x 27     PALETTE: INK + BONE / ORANGE FOR THE SYMBOL HEART', font=f_small, fill=ASH)
OUT.parent.mkdir(parents=True, exist_ok=True)
sheet.save(OUT, optimize=True)
print(OUT)
