/* Deterministic 1920 × 1080 visual study. All time is relative to the 47–67 s audio clip. */
const canvas = document.getElementById('stage');
const c = canvas.getContext('2d', { alpha: false, desynchronized: false });
const W = 1920, H = 1080;
const INK = '#0A0A0B', PANEL = '#151517', GRAPH = '#5E5B57';
const ASH = '#9C978F', BONE = '#EEE9DF', ORANGE = '#FF4D12', EMBER = '#FF9B57';
const TAU = Math.PI * 2;
let data = { lines: [], beats: [], energy: [] };
let bounds = [0, 5, 10, 15, 20];
let worldOnly = false;
let shots = [];

const clamp = (v, lo = 0, hi = 1) => Math.max(lo, Math.min(hi, v));
const smooth = (v) => { v = clamp(v); return v * v * (3 - 2 * v); };
const expo = (v) => 1 - Math.pow(2, -10 * clamp(v));
const lerp = (a, b, p) => a + (b - a) * p;
const hash = (n) => { let x = Math.sin(n * 127.1 + 13.37) * 43758.5453; return x - Math.floor(x); };
const fmt = (n) => String(n).padStart(2, '0');
const plain = (s) => String(s ?? '').replace(/[‘’]/g, "'");

function pLine(points, color, width = 1, alpha = 1, close = false) {
  c.save(); c.globalAlpha = alpha; c.strokeStyle = color; c.lineWidth = width;
  c.beginPath(); points.forEach(([x,y], i) => i ? c.lineTo(x,y) : c.moveTo(x,y));
  if (close) c.closePath(); c.stroke(); c.restore();
}
function rect(x,y,w,h,color,alpha=1) { c.save(); c.globalAlpha=alpha; c.fillStyle=color; c.fillRect(x,y,w,h); c.restore(); }
function strokeRect(x,y,w,h,color,width=1,alpha=1) { c.save(); c.globalAlpha=alpha; c.strokeStyle=color; c.lineWidth=width; c.strokeRect(x,y,w,h); c.restore(); }
function circle(x,y,r,color,alpha=1) { c.save(); c.globalAlpha=alpha; c.fillStyle=color; c.beginPath(); c.arc(x,y,r,0,TAU); c.fill(); c.restore(); }
function ring(x,y,r,color,width=1,alpha=1) { c.save(); c.globalAlpha=alpha; c.strokeStyle=color; c.lineWidth=width; c.beginPath(); c.arc(x,y,r,0,TAU); c.stroke(); c.restore(); }
function ellipse(x,y,rx,ry,color,width=1,alpha=1) { c.save(); c.globalAlpha=alpha; c.strokeStyle=color; c.lineWidth=width; c.beginPath(); c.ellipse(x,y,rx,ry,0,0,TAU); c.stroke(); c.restore(); }
function mono(s,x,y,size=20,color=ASH,align='left',alpha=1) {
  c.save(); c.globalAlpha=alpha; c.font=`${size}px Plex, monospace`; c.textAlign=align;
  c.textBaseline='alphabetic'; c.fillStyle=color; c.fillText(s,x,y); c.restore();
}
function label(s,x,y,color=ASH,size=20) { mono(s.toUpperCase(),x,y,size,color); }
function hatch(x,y,w,h,spacing,color,alpha=.12) {
  c.save(); c.beginPath(); c.rect(x,y,w,h); c.clip(); c.globalAlpha=alpha; c.strokeStyle=color; c.lineWidth=1;
  for (let k=-h; k<w+h; k+=spacing) { c.beginPath(); c.moveTo(x+k,y+h); c.lineTo(x+k+h,y); c.stroke(); }
  c.restore();
}
function cross(x,y,r,col=ORANGE,alpha=.8) { pLine([[x-r,y],[x+r,y]],col,1.5,alpha); pLine([[x,y-r],[x,y+r]],col,1.5,alpha); }
function arrow(x1,y1,x2,y2,col=GRAPH,alpha=.6) {
  pLine([[x1,y1],[x2,y2]],col,1.4,alpha);
  const a=Math.atan2(y2-y1,x2-x1), d=11;
  pLine([[x2-Math.cos(a-.55)*d,y2-Math.sin(a-.55)*d],[x2,y2],[x2-Math.cos(a+.55)*d,y2-Math.sin(a+.55)*d]],col,1.4,alpha);
}
function spark(x,y,t,r=7,amount=1) {
  c.save(); c.shadowColor=ORANGE; c.shadowBlur=32*amount;
  circle(x,y,r*2.2,ORANGE,.18*amount); circle(x,y,r,ORANGE,.95*amount);
  circle(x,y,r*.35,BONE,amount); c.restore();
  for (let i=0;i<5;i++) {
    const a=hash(i*13+Math.floor(t*12))*TAU, d=8+hash(i*29+Math.floor(t*12))*28;
    circle(x+Math.cos(a)*d,y+Math.sin(a)*d,1.2,EMBER,.38*amount);
  }
}
function beatPulse(t) {
  let v=0; const bs=data.beats;
  for (let i=0;i<bs.length;i++) {
    const d=t-bs[i]; if (d>=0 && d<.48) v=Math.max(v,Math.exp(-d*11));
  }
  return v;
}
function wordPulse(t, a, b, expression) {
  let v=0;
  for (let i=a;i<=b;i++) for (const w of data.lines[i]?.words ?? []) {
    if (!expression.test(plain(w.text))) continue;
    const d=t-w.start;
    if (d>=0 && d<.42) v=Math.max(v,Math.exp(-d*9));
  }
  return v;
}
function phase(t,scene) { return clamp((t-bounds[scene])/(bounds[scene+1]-bounds[scene])); }
function currentLine(scene,t) {
  const a=scene*2, b=a+1;
  return t >= (data.lines[b]?.start ?? Infinity) ? b : a;
}
function drawLyric(t, scene, x=132, y=194, size=112) {
  if (worldOnly) return;
  const li=currentLine(scene,t), line=data.lines[li];
  if (!line?.words?.length) return;
  const light=scene===1, past=light?INK:BONE, future=light?'#5A554F':ASH;
  const maxW=W-x-125, gap=17;
  c.font=`900 ${size}px Archivo, sans-serif`;
  let widths=line.words.map(w=>c.measureText(plain(w.text)).width);
  const content=widths.reduce((a,b)=>a+b,0)+gap*(widths.length-1);
  if(content>maxW) { size*=maxW/content; c.font=`900 ${size}px Archivo, sans-serif`; widths=line.words.map(w=>c.measureText(plain(w.text)).width); }
  let xx=x;
  c.textBaseline='alphabetic'; c.textAlign='left';
  for(let k=0;k<line.words.length;k++) {
    const w=line.words[k], text=plain(w.text), ww=widths[k], prog=clamp((t-w.start)/Math.max(.05,w.end-w.start));
    c.fillStyle=t>=w.end?past:future;
    c.globalAlpha=t>=w.end?.98:.28;
    c.fillText(text,xx,y);
    if(t>=w.start && t<w.end) {
      c.save(); c.beginPath(); c.rect(xx-1,y-size,Math.max(4,ww*prog),size*1.3); c.clip();
      c.globalAlpha=1; c.fillStyle=ORANGE; c.fillText(text,xx,y); c.restore();
      rect(xx,y+14,Math.max(5,ww*prog),4,ORANGE);
    }
    xx+=ww+gap;
  }
  c.globalAlpha=1;
  pLine([[x,y+39],[Math.min(W-130,xx-gap),y+39]],light?INK:BONE,1,.22);
  mono(`${fmt(li+1)} / 08    ${scene===0?'TRANSPORT':scene===1?'FORMATION':scene===2?'RETURN':'INTERNAL'}`,x,y+77,19,light?GRAPH:ASH);
}
function drawBase(t,scene,light=false) {
  rect(0,0,W,H,light?BONE:INK);
  const grid=light?INK:BONE;
  c.save(); c.strokeStyle=grid; c.lineWidth=1; c.globalAlpha=light?.055:.045;
  for(let x=0;x<=W;x+=80){c.beginPath();c.moveTo(x,0);c.lineTo(x,H);c.stroke();}
  for(let y=0;y<=H;y+=80){c.beginPath();c.moveTo(0,y);c.lineTo(W,y);c.stroke();}
  c.restore();
  if (!worldOnly) drawHud(t,scene,light);
}
function drawHud(t,scene,light=false) {
  const grid=light?INK:BONE;
  // Film registration marks and one calm technical running line.
  for (const xx of [58,W-58]) for(const yy of [57,H-57]) {
    const sx=xx<W/2?1:-1, sy=yy<H/2?1:-1;
    pLine([[xx,yy+20*sy],[xx,yy],[xx+20*sx,yy]],grid,1.3,.38);
  }
  mono('ALH  /  PROCESS FILM  04',132,73,19,light?GRAPH:ASH);
  mono(`T + ${t.toFixed(2)} S`,W-132,73,19,light?GRAPH:ASH,'right');
  pLine([[132,88],[W-132,88]],grid,1,.22);
  pLine([[132,1000],[W-132,1000]],grid,1,.18);
  mono('SECTION  /  '+fmt(scene+1),132,1034,18,light?GRAPH:ASH);
  const bpm=data.beats.length>1?Math.round(60/(data.beats[1]-data.beats[0])):99;
  mono(`GRID ${bpm} BPM   •   ${String(Math.round(t/20*100)).padStart(3,'0')}%`,W-132,1034,18,light?GRAPH:ASH,'right');
}

// Plate 1 — repeated mechanical registration. The motor goes on; the one part cannot.
function conveyor(t) {
  const p=phase(t,0), beat=beatPulse(t), jam=wordPulse(t,0,1,/stuck|line/i);
  drawBase(t,0);
  rect(0,364,W,440,PANEL);
  hatch(0,364,W,48,28,BONE,.075); hatch(0,756,W,48,28,BONE,.07);
  for(const y of [412,444,725,755]) pLine([[0,y],[W,y]],ASH,y===412||y===755?2:1,.6);
  // Conveyor tread moves even when the workpiece stops.
  const shift=(t*146)%120;
  for(let i=-1;i<18;i++) {
    const x=i*120+shift;
    pLine([[x,447],[x-98,720]],BONE,1,.105);
    ring(x,766,28,ASH,2,.45); ring(x,766,8,ORANGE,1,.4);
    pLine([[x-14,766],[x+14,766]],GRAPH,1,.5);
  }
  // Station frames, dimension notation and clamps.
  for(let i=0;i<6;i++) {
    const x=210+i*300;
    pLine([[x,405],[x,723]],ASH,1,.28);
    pLine([[x-18,405],[x+18,405]],ASH,2,.7);
    pLine([[x-18,723],[x+18,723]],ASH,2,.7);
    mono('0'+(i+1),x,390,17,ASH,'center');
  }
  const stuckAt=(data.lines[0]?.words??[]).find(w=>/stuck/i.test(w.text))?.start ?? bounds[1]*.34;
  const echoAt=data.lines[1]?.start ?? bounds[1]*.65;
  const reset=t>=echoAt;
  const localStart=reset?echoAt:0;
  const moving=clamp((t-localStart)/Math.max(.3,stuckAt-localStart));
  const mx=reset?lerp(530,922,expo(clamp((t-echoAt)/.9))):lerp(430,922,expo(moving));
  const jitter=jam*7*Math.sin(t*75);
  const cy=584;
  // Workpiece: precise drawn metal housing, unfilled at this point.
  c.save(); c.translate(mx+jitter,cy);
  rect(-185,-88,370,176,INK,.9); strokeRect(-185,-88,370,176,BONE,2,.85);
  strokeRect(-166,-69,332,138,GRAPH,1.4,.85);
  for(const sx of [-134,134]) {ring(sx,0,22,ASH,2,.75); ring(sx,0,8,ORANGE,1,.8);}
  pLine([[-85,0],[85,0]],ORANGE,3,.86);
  for(let k=-3;k<=3;k++){pLine([[k*24,-44],[k*24,44]],ASH,1,.2);}
  mono('UNFINISHED / 001',0,122,17,ASH,'center');
  c.restore();
  // The orange lead travels with the part, then is trapped in the clamp.
  pLine([[160,cy],[mx-188,cy]],ORANGE,3,.95);
  spark(mx-185+jitter,cy,t,6,1);
  rect(906,399,32,100,INK); rect(906,671,32,100,INK);
  strokeRect(906,399,32,100,BONE,2,.85); strokeRect(906,671,32,100,BONE,2,.85);
  rect(918,495,9,178,ORANGE,.75+jam*.25);
  pLine([[906,499],[860,534]],BONE,2,.8); pLine([[938,499],[984,534]],BONE,2,.8);
  pLine([[906,671],[860,635]],BONE,2,.8); pLine([[938,671],[984,635]],BONE,2,.8);
  // Impact lettering belongs to the machine, behind the workpiece.
  c.save(); c.globalAlpha=.08+jam*.12; c.font='900 245px Archivo'; c.fillStyle=BONE;
  c.fillText('STUCK',1080,648); c.restore();
  pLine([[906,830],[906,901],[1280,901]],ORANGE,1.5,.65);
  circle(906,901,4,ORANGE);
  mono('MOTOR CONTINUES',1289,908,20,ASH);
  mono('REGISTRATION ERROR    Δx = 0',132,900,18,ASH);
  for(let i=0;i<12;i++){rect(132+i*31,924,20,6,i<Math.floor(12*p)?ORANGE:GRAPH,i<Math.floor(12*p)?.9:.4);}
  drawLyric(t,0,132,208,115);
  if (beat>.35) rect(0,0,W,H,ORANGE,.025*beat);
}

// Plate 2 — pressure gives a drawn part weight; the word REAL is minted in the tooling.
function press(t) {
  const p=phase(t,1), hit=wordPulse(t,2,3,/real/i), beat=beatPulse(t);
  drawBase(t,1,true);
  // Engineering sheet: small notes and ruled dimensions, deliberately distinct from the dark plates.
  label('FORMING DIE / SECTION A–A',132,306,GRAPH,21);
  label('TOLERANCE  ± 0.02',132,338,GRAPH,18);
  pLine([[176,412],[176,756]],INK,1,.55); pLine([[164,412],[188,412]],INK,1,.55); pLine([[164,756],[188,756]],INK,1,.55);
  mono('344 mm',147,592,17,GRAPH,'right');
  pLine([[690,822],[1450,822]],INK,1,.55); pLine([[690,810],[690,835]],INK,1,.55); pLine([[1450,810],[1450,835]],INK,1,.55);
  mono('760 mm',1070,852,17,GRAPH,'center');
  // Heavy platen and steel throat. The descending head follows sung REAL, rather than free-running.
  rect(532,280,1076,52,INK);
  for(let k=0;k<25;k++) rect(544+k*43,289,26,34,GRAPH,.28);
  const drop=180*hit + 15*beat;
  rect(630,334+drop,880,120,INK);
  strokeRect(630,334+drop,880,120,INK,3);
  hatch(630,334+drop,880,120,20,BONE,.1);
  rect(672,449+drop,795,16,INK);
  for(const x of [672,1468]) {rect(x-26,238,23,530,INK,.78); strokeRect(x-26,238,23,530,INK,1);}
  rect(600,777,965,45,INK);
  rect(676,731,810,39,GRAPH,.9);
  // Drawn laminae grow into a solid layered pump shell over the two invocations of the line.
  const layers=3+Math.round(p*6);
  for(let k=layers-1;k>=0;k--) {
    const off=k*7, y=576+off;
    c.save(); c.globalAlpha=.4+.55*(1-k/(layers+1));
    c.fillStyle=k===0?INK:GRAPH;
    c.beginPath(); c.moveTo(790,y-66); c.lineTo(1355,y-66); c.lineTo(1410,y);
    c.lineTo(1355,y+69); c.lineTo(790,y+69); c.lineTo(735,y); c.closePath(); c.fill();
    c.strokeStyle=k===0?INK:BONE; c.lineWidth=k===0?4:1; c.stroke(); c.restore();
  }
  // An orange inner cavity stays visible under the solid shell.
  c.save(); c.shadowColor=ORANGE; c.shadowBlur=14;
  ellipse(1072,575,178+12*beat,48+5*beat,ORANGE,3,.7); c.restore();
  pLine([[826,574],[1317,574]],ORANGE,4,.72);
  for(const x of [790,1355]) {ring(x,576,22,BONE,2,.7); circle(x,576,4,ORANGE);}
  // The REAL mark is engraved into the upper die.
  c.save(); c.font='900 84px Archivo'; c.fillStyle=BONE; c.textAlign='center';
  c.fillText('REAL',1070,419+drop); c.restore();
  label('DENSITY',1535,473,GRAPH,19); mono((0.12+p*.88).toFixed(3),1535,508,33,INK);
  label('REPEAT / PRESS',1535,591,GRAPH,18);
  pLine([[1535,607],[1740,607]],INK,1,.5);
  for(let i=0;i<8;i++){rect(1535+i*25,630,17,13,i<Math.floor(p*8)?ORANGE:INK,i<Math.floor(p*8)?1:.25);}
  // Contact flash only on the die impact, still readable on the paper plate.
  if(hit>.15) rect(630,450+drop,880,5,ORANGE,.55*hit);
  drawLyric(t,1,132,205,116);
}

// Plate 3 — the machine repeats into depth. One signal finally leaves its lane.
function corridor(t) {
  const p=phase(t,2), beat=beatPulse(t), jam=wordPulse(t,4,5,/stuck|line/i);
  drawBase(t,2);
  const vx=1000, vy=337;
  const floor=c.createLinearGradient(0,vy,0,H); floor.addColorStop(0,'#0D0D0E'); floor.addColorStop(1,'#23201E');
  c.fillStyle=floor; c.beginPath(); c.moveTo(vx,vy); c.lineTo(W,850); c.lineTo(W,H); c.lineTo(0,H); c.lineTo(0,850); c.closePath(); c.fill();
  // Perspective rail structure and depth marching, a little like an engraved tunnel.
  for(let i=0;i<20;i++) {
    const z=((i/20+(t*0.20))%1); const s=.055+Math.pow(z,1.9)*1.08;
    const xl=vx-790*s, xr=vx+790*s, top=vy-285*s, bot=vy+550*s;
    pLine([[xl,bot],[xl,top],[xr,top],[xr,bot]],BONE,1.2,.09+.30*s);
    pLine([[vx-260*s,bot],[vx+260*s,bot]],ASH,1,.11+.30*s);
    if(i%2===0) {mono(fmt(i+1),xr-8,top+23,14,ASH,'right',.15+.38*s);}
  }
  for(const q of [-1,-.55,.55,1]) {
    pLine([[vx+q*18,vy],[vx+q*910,H]],q===-.55?ORANGE:BONE,q===-.55?2:1.2,q===-.55?.68:.26);
  }
  // A repeating series of empty housings streaks by. The same empty center is the visual refrain.
  for(let i=0;i<12;i++) {
    const z=((i/12+t*.17)%1), s=.13+Math.pow(z,1.7)*1.2;
    const y=vy+s*455, x=vx+(i%2?-1:1)*190*s, w=140*s, h=70*s;
    strokeRect(x-w/2,y-h/2,w,h,BONE,Math.max(.7,s),.16+.3*s);
    ellipse(x,y,30*s,21*s,ORANGE,1,.2+.24*s);
  }
  // The trapped orange part remains at one screen coordinate as the entire factory flows around it.
  const mx=945+5*Math.sin(t*64)*jam, my=684;
  rect(mx-164,my-77,328,154,INK,.98); strokeRect(mx-164,my-77,328,154,BONE,2,.87);
  strokeRect(mx-146,my-60,292,120,ASH,1,.62);
  for(const sx of [-114,114]) ring(mx+sx,my,18,ASH,2,.7);
  pLine([[mx-82,my],[mx+82,my]],ORANGE,4,.85);
  hatch(mx-159,my-72,318,145,19,BONE,.07);
  // A signal escapes the mechanical routing at the end of the repeat.
  const leave=smooth((p-.59)/.36);
  const ex=mx+152+520*leave, ey=my-90-330*leave;
  pLine([[mx+150,my],[mx+150+75*leave,my-45*leave],[ex,ey]],ORANGE,3,.95);
  spark(ex,ey,t,6+2*beat,1);
  cross(ex+48,ey-26,14,BONE,.35);
  // Deep type recurs along the wall; main lyric remains crisply word-timed above.
  c.save(); c.font='900 195px Archivo'; c.globalAlpha=.055+.05*jam; c.fillStyle=BONE;
  c.translate(130,600); c.rotate(-.10); c.fillText('STUCK IN THE LINE',0,0); c.restore();
  mono('ERROR: PART UNABLE TO EXIT LINE',133,878,19,ASH);
  for(let k=0;k<7;k++) {
    const x=137+k*56; ring(x,910,14,k<Math.floor(p*7)?ORANGE:GRAPH,1.5,.6);
    if(k<6) pLine([[x+14,910],[x+42,910]],ASH,1,.32);
  }
  drawLyric(t,2,132,206,114);
  if(beat>.4) rect(0,0,W,H,BONE,.012*beat);
}

// Plate 4 — a technical section opens and reveals a self-powered two-chamber pump.
function heart(t) {
  const p=phase(t,3), b=beatPulse(t), reveal=smooth((p-.04)/.36);
  drawBase(t,3);
  const hx=1130, hy=571, spread=250*reveal;
  // Housing cross section: outside remains graphite, with bolts and engraved hatch.
  c.save(); c.globalAlpha=.2+.7*reveal; c.strokeStyle=BONE; c.lineWidth=3;
  c.beginPath(); c.ellipse(hx,hy,399,335,0,0,TAU); c.stroke(); c.restore();
  ellipse(hx,hy,380,315,GRAPH,2,.85); ellipse(hx,hy,326,263,ASH,1.5,.5);
  for(let i=0;i<24;i++) {
    const a=TAU*i/24, x=hx+391*Math.cos(a), y=hy+327*Math.sin(a);
    ring(x,y,8,ASH,1.2,.6); circle(x,y,2.1,ORANGE,.35);
  }
  // The two casing leaves pull away, exposing the chamber without implying a human face.
  const lx=hx-205-spread, rx=hx+205+spread;
  c.save(); c.globalAlpha=.88; c.fillStyle=PANEL; c.strokeStyle=BONE; c.lineWidth=3;
  c.beginPath(); c.moveTo(lx+44,hy-228); c.bezierCurveTo(lx-90,hy-196,lx-95,hy+198,lx+44,hy+238);
  c.lineTo(lx+44,hy-228); c.fill(); c.stroke();
  c.beginPath(); c.moveTo(rx-44,hy-228); c.bezierCurveTo(rx+90,hy-196,rx+95,hy+198,rx-44,hy+238);
  c.lineTo(rx-44,hy-228); c.fill(); c.stroke(); c.restore();
  // Inner cavity with two different-sized pressure bellows and interlocking valves.
  const core=clamp((p-.10)/.27), beatScale=1+.055*b;
  c.save(); c.globalAlpha=core; c.translate(hx,hy); c.scale(beatScale,beatScale);
  const glow=c.createRadialGradient(0,10,8,0,10,276);
  glow.addColorStop(0,'rgba(255,117,53,.42)'); glow.addColorStop(.5,'rgba(255,77,18,.11)'); glow.addColorStop(1,'rgba(255,77,18,0)');
  c.fillStyle=glow; c.fillRect(-300,-295,600,590);
  function chamber(cx,cy,rx,ry,flip) {
    c.save(); c.translate(cx,cy); c.rotate(flip*.17);
    c.fillStyle='#341B13'; c.strokeStyle=ORANGE; c.lineWidth=3;
    c.beginPath(); c.moveTo(0,-ry); c.bezierCurveTo(rx*.9,-ry*.90,rx*1.16,ry*.1,0,ry);
    c.bezierCurveTo(-rx*1.16,ry*.1,-rx*.90,-ry*.90,0,-ry); c.fill(); c.stroke();
    for(let k=1;k<8;k++) {
      const yy=-ry+k*2*ry/8, w=rx*Math.sqrt(Math.max(0,1-(yy/ry)**2));
      pLine([[-w*.96,yy],[w*.96,yy]],k%2?EMBER:ORANGE,1.5,.33+.08*k);
    }
    ellipse(0,0,rx*.42,ry*.57,EMBER,1.5,.5);
    c.restore();
  }
  chamber(-103,29,126,202,-1); chamber(117,34,113,176,1);
  // Manifold, screws and valves make this a machine with a heart, not an icon.
  for(const yy of [-143,171]) {rect(-164,yy,328,22,GRAPH,.95); pLine([[-164,yy], [164,yy]],BONE,1,.68);}
  for(const xx of [-148,-74,0,74,148]) {ring(xx,-132,7,BONE,1,.75);ring(xx,182,7,BONE,1,.75);}
  for(const xx of [-63,66]) {ring(xx,-180,30,ORANGE,2,.7); ring(xx,-180,13,BONE,1,.55);}
  pLine([[-63,-211],[-63,-255],[-232,-255]],ORANGE,3,.7);
  pLine([[66,-211],[66,-262],[221,-262]],ORANGE,3,.7);
  pLine([[0,195],[0,255],[-106,255]],ORANGE,3,.72);
  c.restore();
  // Beat-synchronous orange pulse travels from the pump to the ECG hairline.
  const lineY=910;
  pLine([[164,lineY],[600,lineY],[645,lineY-64],[677,lineY+68],[712,lineY-139],[754,lineY],[W-154,lineY]],ORANGE,2,.35+.55*reveal);
  const px=164+(W-318)*((t*0.15)%1);
  if(reveal>.25) spark(px,lineY,t,3,.45);
  mono('UNIT 01 / SELF-POWERED',160,624,23,ASH);
  mono('OUTPUT: PERSISTENT',160,659,20,ASH);
  const live=(.74+.26*b)*reveal;
  circle(170,697,7,ORANGE,live); mono('ACTIVE',192,705,24,ORANGE,'left',live);
  arrow(450,680,hx-360,680,ASH,.47);
  label('INTERIOR / X-RAY',hx+272,321,ASH,20);
  label('PULSE',hx+340,818,ASH,17);
  drawLyric(t,3,132,209,111);
  // The last answer lands as a typographic hold, not another cut.
  if(t>=(data.lines[7]?.start??19)) {
    const q=clamp((t-(data.lines[7]?.start??19))/.38);
    c.save(); c.globalAlpha=.16*q; c.font='900 212px Archivo'; c.fillStyle=BONE;
    c.fillText('HEART',145,478); c.restore();
  }
}

// Twenty shot cues. Each is attached to a sung word, so edits to the alignment remain safe.
function buildShots() {
  const specs = [
    // line, word, plate, camera center, scale, entrance, drift, hit, type treatment
    [0,0,0,550,575,1.95,'crash',-16,0,18,'top'],
    [0,2,0,920,575,1.82,'punch',8,4,20,'stuck'],
    [0,5,0,1260,580,1.58,'right',65,0,14,'rail'],
    [1,0,0,625,580,1.63,'left',-25,0,19,'stuck'],
    [1,3,0,922,566,2.04,'punch',0,7,17,'clamp'],
    [2,0,1,1060,540,1.07,'cut',0,-12,13,'top'],
    [2,2,1,1070,420,1.68,'down',0,25,24,'real'],
    [2,4,1,1430,450,2.02,'right',22,0,15,'gauge'],
    [3,0,1,1070,405,1.62,'down',0,18,22,'real'],
    [3,2,1,1070,470,1.92,'punch',-8,0,15,'emboss'],
    [4,0,2,1000,540,1.07,'cut',0,-13,15,'top'],
    [4,2,2,945,675,1.72,'punch',5,12,22,'stuck'],
    [4,5,2,1290,515,1.65,'right',45,-6,17,'rail'],
    [5,0,2,970,645,1.36,'left',-30,0,18,'stuck'],
    [5,3,2,1430,380,2.02,'up',30,-8,17,'rail'],
    [6,0,3,1100,555,1.10,'cut',0,0,15,'top'],
    [6,4,3,1130,570,1.66,'punch',0,8,24,'heart'],
    [6,5,3,800,750,1.50,'down',-20,14,16,'inside'],
    [7,0,3,1110,555,1.07,'pull',0,0,17,'heart'],
    [7,1,3,990,665,1.39,'down',0,-6,15,'inside'],
  ];
  shots=specs.map((a,i)=>({
    t:data.lines[a[0]]?.words?.[a[1]]?.start ?? i,
    line:a[0], word:a[1], scene:a[2], cx:a[3], cy:a[4], z:a[5],
    enter:a[6], dx:a[7], dy:a[8], hit:a[9], type:a[10], index:i,
  }));
}
function shotAt(t) {
  let active=shots[0];
  for (let i=1;i<shots.length;i++) { if(t>=shots[i].t) active=shots[i]; else break; }
  return active;
}
function cameraAt(t,shot) {
  const dt=Math.max(0,t-shot.t), next=shots[shot.index+1]?.t ?? 20;
  const travel=clamp(dt/Math.max(.2,next-shot.t));
  const enter=expo(clamp(dt/.19));
  let x=shot.cx+shot.dx*travel, y=shot.cy+shot.dy*travel;
  let z=shot.z*(1+.016*travel), rot=0;
  // Fast camera entries settle into a hold. Nothing uses persistent frame state.
  if(shot.enter==='right') {x+=240*(1-enter)/z; rot=-.018*(1-enter);}
  if(shot.enter==='left') {x-=240*(1-enter)/z; rot=.018*(1-enter);}
  if(shot.enter==='up') {y+=200*(1-enter)/z; rot=.012*(1-enter);}
  if(shot.enter==='down') {y-=190*(1-enter)/z; rot=-.011*(1-enter);}
  if(shot.enter==='punch'||shot.enter==='crash') z*=1+.13*(1-enter);
  if(shot.enter==='pull') z*=1+.17*(1-enter);
  // Bounds prevent the transformed 1920×1080 world from exposing empty edges.
  const safeX=W/(2*z)+18, safeY=H/(2*z)+18;
  x=clamp(x,safeX,W-safeX); y=clamp(y,safeY,H-safeY);
  let sx=0, sy=0;
  if(dt<.42) {
    const decay=Math.exp(-dt*13)*shot.hit;
    sx+=Math.sin(dt*88)*decay;
    sy+=Math.sin(dt*107+.6)*decay*.42;
    z*=1+.018*Math.exp(-dt*20);
  }
  // Small beat ticks keep long holds alive; strong motion is reserved for the word cuts.
  const tick=beatPulse(t)*2.0;
  sx+=tick*Math.sin(t*60); sy+=tick*Math.cos(t*73);
  return {x,y,z,rot,sx,sy};
}
function heroWord(t,shot) {
  const w=data.lines[shot.line]?.words?.[shot.word]; if(!w) return;
  const p=clamp((t-w.start)/Math.max(.05,w.end-w.start));
  const text=plain(w.text).replace(/[^A-Za-z]/g,'').toUpperCase();
  let x=0,y=0,size=0,align='left';
  switch(shot.type) {
    case 'stuck': x=shot.scene===0?1120:1120; y=shot.scene===0?690:680; size=215; break;
    case 'clamp': x=1145; y=640; size=190; break;
    case 'real': x=900; y=610; size=205; break;
    case 'heart': x=136; y=700; size=205; break;
    case 'inside': x=136; y=850; size=160; break;
    default: return;
  }
  c.save(); c.font=`900 ${size}px Archivo`; c.textAlign=align; c.textBaseline='alphabetic';
  const width=c.measureText(text).width;
  c.fillStyle=shot.scene===1?INK:BONE; c.globalAlpha=t>=w.end?.22:.12;
  c.fillText(text,x,y);
  if(t>=w.start&&t<w.end) {
    c.beginPath(); c.rect(x,y-size*1.1,Math.max(6,width*p),size*1.3); c.clip();
    c.fillStyle=ORANGE; c.globalAlpha=.88; c.fillText(text,x,y);
  }
  c.restore();
}
function shotTransition(t,shot) {
  if(shot.index===0) return;
  const d=t-shot.t; if(d<0||d>.12) return;
  const q=1-d/.12, light=shot.scene===1;
  // A sparse high-contrast cut flash and a directional mechanical swipe.
  rect(0,0,W,H,light?INK:BONE,.025*q);
  c.save(); c.strokeStyle=light?INK:BONE; c.lineWidth=2; c.globalAlpha=.13*q;
  const dir=shot.enter==='left'?-1:1;
  for(let i=0;i<5;i++) {
    const yy=290+i*136, offset=(1-q)*500*dir;
    c.beginPath(); c.moveTo(120+offset,yy); c.lineTo(650+offset,yy); c.stroke();
  }
  c.restore();
}
function render(t) {
  t=clamp(Number(t)||0,0,20);
  const shot=shotAt(t), s=shot.scene, light=s===1, cam=cameraAt(t,shot);
  c.save(); c.setTransform(1,0,0,1,0,0); c.clearRect(0,0,W,H);
  rect(0,0,W,H,light?BONE:INK);
  c.translate(W/2+cam.sx,H/2+cam.sy); c.rotate(cam.rot); c.scale(cam.z,cam.z); c.translate(-cam.x,-cam.y);
  worldOnly=true;
  if(s===0) conveyor(t); else if(s===1) press(t); else if(s===2) corridor(t); else heart(t);
  worldOnly=false;
  c.restore();
  c.save(); c.setTransform(1,0,0,1,0,0);
  // The forming-machine closeups push its platen through the frame. A fixed paper
  // header keeps every sung word and its line number readable above the tooling.
  if(light && cam.z>1.3) {
    rect(0,89,W,216,BONE,.975);
    for(let gx=80;gx<W;gx+=80) pLine([[gx,90],[gx,305]],INK,1,.045);
    pLine([[132,304],[W-132,304]],INK,1,.19);
  }
  shotTransition(t,shot);
  drawHud(t,s,light);
  // The full sung line is always present; selected words also become large machine typography.
  const hero=/^(stuck|clamp|real|heart|inside)$/.test(shot.type);
  const x=132+(hero?cam.sx*.22:0), y=hero?174:(s===0?208:s===1?205:s===2?206:209);
  const size=hero?78:(s===0?115:s===1?116:s===2?114:111);
  drawLyric(t,s,x,y,size);
  if(hero) heroWord(t,shot);
  // Fine fixed-seed grain prevents camera motion from feeling like flat UI.
  c.globalAlpha=light?.10:.15; c.fillStyle=grainPattern; c.fillRect(0,0,W,H);
  c.restore();
}

// One tiny repeatable texture. No random values change from frame to frame.
const grainTile=document.createElement('canvas'); grainTile.width=160; grainTile.height=160;
const g=grainTile.getContext('2d'); const im=g.createImageData(160,160);
for(let i=0;i<160*160;i++) { const n=hash(i+73); const off=i*4; im.data[off]=255; im.data[off+1]=250; im.data[off+2]=237; im.data[off+3]=Math.floor(n*23); }
g.putImageData(im,0,0); const grainPattern=c.createPattern(grainTile,'repeat');

window.drawAt=render;
Promise.all([
  fetch('./timing.json').then(r=>{ if(!r.ok) throw new Error('timing.json: '+r.status); return r.json(); }),
  document.fonts.load('900 112px Archivo'),
  document.fonts.load('18px Plex')
]).then(([timing])=>{
  data=timing;
  if(!Array.isArray(data.lines)||data.lines.length<8) throw new Error('Expected eight lyric lines');
  const raw=[0,data.lines[2].start,data.lines[4].start,data.lines[6].start,20];
  bounds=raw.map((x,i)=>i===0?0:i===4?20:clamp(Number(x)||0,.01,19.99));
  for(let i=1;i<5;i++) if(bounds[i]<=bounds[i-1]) bounds[i]=bounds[i-1]+.001;
  buildShots();
  window.ready=true; render(0);
}).catch(e=>{ window.renderError=String(e); console.error(e); });
