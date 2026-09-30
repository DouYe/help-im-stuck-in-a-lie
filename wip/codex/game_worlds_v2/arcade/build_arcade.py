"""Code-native bullet-hell arena: syntax is the stage and punctuation is the hazard."""
from pathlib import Path
import math
import sys

ROOT = Path(r"D:\Videos\Help! I'm stuck in a LIE")
sys.path.insert(0, str(ROOT / "wip/codex/visual_audit/lib"))
sys.path.insert(0, str(ROOT / "design/character/src"))
from PIL import Image, ImageDraw, ImageFont
from final_sheet import render, SS, INK, BONE, ASH, GR
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from ascii_paint import paint

W, H = 1920, 1080
ground = Image.new("L", (W, H), 9)
gd = ImageDraw.Draw(ground)
# Literal ASCII pixels form the arena substrate. Each wide value mass is
# rebuilt as characters below, so these grey polygons never appear as paint.
gd.polygon([(0,660),(260,625),(560,790),(830,700),(1110,765),(1450,625),(1920,685),(1920,1080),(0,1080)],fill=67)
gd.polygon([(0,803),(330,750),(610,862),(890,799),(1260,890),(1630,783),(1920,850),(1920,1080),(0,1080)],fill=94)
gd.rectangle((0,922,1920,1080),fill=123)
gd.polygon([(190,218),(420,225),(510,450),(390,650),(196,638)],fill=58)
gd.polygon([(1485,210),(1727,232),(1710,700),(1490,653),(1410,445)],fill=59)
gd.line([(385,315),(610,178),(970,235),(1310,174),(1530,322)],fill=76,width=43)
im = paint(ground,(W,H),cell=(11,16),supersample=SS)
d = ImageDraw.Draw(im)
font_dir = ROOT / "app/public/fonts/src"
mono_name = font_dir / "IBMPlexMono-Bold.ttf"
if not mono_name.exists(): mono_name = ROOT / "app/public/fonts/IBMPlexMono-Bold.ttf"
mono_regular = font_dir / "IBMPlexMono-Regular.ttf"
if not mono_regular.exists(): mono_regular = ROOT / "app/public/fonts/IBMPlexMono-Regular.ttf"
cache = {}
def f(size, bold=True):
    key = (size, bold)
    if key not in cache: cache[key] = ImageFont.truetype(str(mono_name if bold else mono_regular), size * SS)
    return cache[key]
def text(x, y, s, size=28, color=BONE, bold=True):
    d.text((int(x * SS), int(y * SS)), s, font=f(size, bold), fill=color)

# Several nested code frames recede toward the playfield. They are made of
# literal syntax tokens, with scale and contrast encoding camera depth.
for k, (x0, y0, x1, y1, tone, size) in enumerate([
    (72, 33, 1848, 1008, (32,32,32), 25),
    (158, 104, 1762, 955, (58,58,58), 25),
    (236, 166, 1684, 903, (86,86,86), 25),
]):
    text(x0, y0, "{" + "=" * int((x1-x0)/(size*0.65)) + "}", size, tone)
    for y in range(y0+size, y1-size, size*2):
        text(x0, y, "{", size, tone)
        text(x1, y, "}", size, tone)
    text(x0, y1-size, "}" + "_" * int((x1-x0)/(size*0.65)) + "{", size, tone)

# Actual code blocks create the arena's raised walls and gates. Readable code
# is visible at several scales, rather than a texture stamped onto masonry.
for j, line in enumerate([
    "if (lie == true) {",
    "    state = STUCK;",
    "    exit  = null;",
    "    while (heart) {",
    "        retry();",
    "    }",
    "} else { return REAL; }",
]):
    text(258, 245+j*78, line, 33 if j in (0,6) else 27, (61,61,61), True)
for j, line in enumerate([
    "for (let i = 0; i < 8; i++) {",
    "    spawn('x');",
    "    spawn('+');",
    "    spawn('o');",
    "    if (girl.alive) continue;",
    "}",
]):
    text(1160, 277+j*77, line, 25, (71,71,71), False)

# Boss emitters are conditional branches, drawn as code rather than monsters.
text(293, 355, "if(false)", 40, ASH)
text(1393, 340, "else{}", 40, ASH)
text(320, 442, "<<<", 53, BONE)
text(1514, 432, ">>>", 53, BONE)

# Three choreographed waves. Every mark is a symbol projectile on an exact
# orbit; one diagonal lane is deliberately open for a playable escape path.
CX, CY = 970, 555
for ring, radius in enumerate((235, 320, 405, 490)):
    count = 31 + ring*11
    for i in range(count):
        a = 2*math.pi*i/count + ring*0.16
        # The lane from lower-left to upper-right is the only safe gap.
        if min(abs((a-2.43+math.pi)%(2*math.pi)-math.pi), abs((a-5.57+math.pi)%(2*math.pi)-math.pi)) < 0.23:
            continue
        x = CX + radius*math.cos(a)*1.28
        y = CY + radius*math.sin(a)*0.66
        if not (248 < x < 1685 and 175 < y < 913): continue
        glyph = ("x", "+", "o", "{}")[(i+ring)%4]
        col = BONE if ring < 2 else ASH
        text(x, y, glyph, 28+ring*2, col)

# A closing instruction becomes a thick rhythmic wall on the bottom edge.
for x in range(306, 1620, 68):
    text(x, 813 + int(16*math.sin(x/140)), "}", 54, BONE)

# Last: the same approved symbol heroine, on top of terrain and gameplay
# projectiles. Her black knockout preserves legibility at this dense moment.
render(d, "help", 857, 407, 190, knock=INK)

# The sung HELP is the function call that begins this second chorus loop.
text(758, 66, "HELP()", 74, BONE)
text(284, 993, "WAVE 02 / LIE LOOP", 24, ASH)
text(1318, 993, "SAFE PATH: 01", 24, ASH)

out = im.resize((W,H), Image.Resampling.LANCZOS)
target = Path(__file__).parent / "KF11_HELP_code_bullet_hell.png"
out.save(target)
print(target)
