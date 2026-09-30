/* Deterministic character-built platformer. 120 Hz physics; canvas is the movie frame. */
(() => {
'use strict';
const C={ink:'#0a0a0b',ink2:'#161618',graph:'#353538',ash:'#817d75',bone:'#eee9df',orange:'#ff5314'};
const W=1920,H=1080,DT=1/120,G=2350,JUMP=990;
const canvas=document.getElementById('screen'),ctx=canvas.getContext('2d',{alpha:false});
const renderMode=new URLSearchParams(location.search).has('render');
if(renderMode) document.body.classList.add('render');
const terrain=[
 {x:0,end:1200,y:800,name:'INPUT LINE'}, {x:1420,end:2500,y:800,name:'BRASS / 01'},
 {x:2500,end:3050,y:710,name:'VOICE BUS'}, {x:3050,end:3650,y:900,name:'STACK BELOW'},
 {x:3870,end:4650,y:900,name:'MIX / BUFFER'}, {x:4650,end:5200,y:810,name:'CHORUS'},
 {x:5400,end:6050,y:810,name:'CROSS FIRE'}, {x:6250,end:7000,y:740,name:'LAST CONDITIONAL'},
 {x:7000,end:7800,y:820,name:'EXPORT / REAL'}
];
const emitters=[
 {x:2150,y:650,trigger:1200,type:'word',text:'LIE',speed:570,high:true},
 {x:4100,y:859,trigger:3350,type:'note',speed:520,high:false},
 {x:4650,y:750,trigger:3940,type:'word',text:'STUCK',speed:580,high:true},
 {x:6200,y:772,trigger:5500,type:'note',speed:570,high:false},
 {x:7250,y:590,trigger:6500,type:'word',text:'HELP',speed:640,high:true},
 {x:7680,y:775,trigger:7050,type:'note',speed:660,high:false}
];
const keys=new Set();let mode='auto',time=0,accumulator=0,p,cam,shots=[],effects=[],events=[],fired=new Set(),attempt=1,deadAt=-1,finishAt=-1;
let lastTimestamp=0,jumpWas=false,deathPos=null;
const clamp=(x,a,b)=>Math.min(b,Math.max(a,x));
const approach=(v,target,n)=>v<target?Math.min(target,v+n):Math.max(target,v-n);
function seed(n){let x=Math.sin(n*127.17+77.3)*43758.5453;return x-Math.floor(x);}
function spawn(){
 p={x:220,y:800,vx:0,vy:0,width:105,grounded:true,duck:0,landing:0,runPhase:0,facing:1,hair:PlatformerCharacter.createHair(),dead:false};
 cam={x:0,y:0,vx:0,vy:0,zoom:1};shots=[];effects=[];fired=new Set();jumpWas=false;deadAt=-1;finishAt=-1;
}
function reset(newMode='auto'){mode=newMode;time=0;accumulator=0;attempt=1;events=[];deathPos=null;spawn();draw();}
function closestGround(x){return terrain.find(s=>x>=s.x&&x<=s.end);}
function jump(){if(!p.grounded||p.duck>.55)return false;p.vy=-JUMP;p.grounded=false;events.push({kind:'jump',t:time,x:p.x});effect('takeoff',p.x,p.y);return true;}
function effect(kind,x,y){effects.push({kind,x,y,born:time});}
function die(cause){if(p.dead||finishAt>=0)return;p.dead=true;p.vx*=.3;deadAt=time;deathPos={x:p.x,y:p.y};events.push({kind:'death',t:time,x:p.x,cause});effect('death',p.x,p.y-80);}
function input(){
 if(mode==='manual')return {move:(keys.has('ArrowRight')||keys.has('KeyD')?1:0)-(keys.has('ArrowLeft')||keys.has('KeyA')?1:0),duck:keys.has('ArrowDown')||keys.has('KeyS'),jump:keys.has('Space')||keys.has('KeyW')||keys.has('ArrowUp')};
 let duck=false,wantJump=false;
 const floor=closestGround(p.x),idx=terrain.indexOf(floor),next=terrain[idx+1];
 if(floor&&next&&p.grounded&&floor.end-p.x<125&&(next.x-floor.end>20||next.y<floor.y-15))wantJump=true;
 for(const s of shots){
  const dx=s.x-p.x;if(dx< -90||dx>450)continue;
  if(s.high&&dx<350&&p.grounded&&attempt>1)duck=true;
  if(!s.high&&dx<420&&dx>110&&p.grounded)wantJump=true;
 }
 // One failure demonstrates the reset; the second attempt changes the same dodge.
 if(attempt===1&&p.x>1470&&p.x<2100){duck=false;wantJump=false;}
 if(p.x>7190&&p.x<7250&&p.grounded)wantJump=true;
 return {move:1,duck,jump:wantJump};
}
function step(dt){
 time+=dt;
 if(p.dead){
  if(time-deadAt>.64){attempt++;spawn();events.push({kind:'respawn',t:time,x:p.x});}
  return;
 }
 const control=input(),prevX=p.x,prevY=p.y,prevVy=p.vy;
 const targetSpeed=(finishAt>=0?0:(p.x>6000?550:480))*control.move;
 p.vx=approach(p.vx,targetSpeed,(p.grounded?1900:920)*dt);if(p.vx) p.facing=Math.sign(p.vx);
 p.duck=approach(p.duck,control.duck?1:0,9*dt);
 if(control.jump&&(!jumpWas||mode==='auto'))jump();jumpWas=control.jump;
 p.x+=p.vx*dt;p.vy=Math.min(1500,p.vy+G*dt);p.y+=p.vy*dt;p.grounded=false;
 for(const s of terrain){
  if(p.x+19<s.x||p.x-19>s.end)continue;
  if(prevY<=s.y+2&&p.y>=s.y&&p.vy>=0){
   const impact=p.vy;p.y=s.y;p.vy=0;p.grounded=true;
   if(impact>350){p.landing=clamp(impact/1300,0,1);effect('land',p.x,p.y);events.push({kind:'land',t:time,x:p.x,impact});}
  } else if(p.y>s.y+7&&prevX+22<s.x&&p.x+22>=s.x){p.x=s.x-23;p.vx=0;}
 }
 p.x=clamp(p.x,60,7700);p.landing=Math.max(0,p.landing-dt*5.6);
 if(p.grounded)p.runPhase+=Math.abs(p.x-prevX)*Math.PI*2/130;
 PlatformerCharacter.updateHair(p.hair,p,dt);
 emitters.forEach((e,i)=>{
  if(!fired.has(i)&&p.x>=e.trigger){
   fired.add(i);shots.push({...e,id:i,x:e.x,born:time});effect('fire',e.x,e.y);
   if(i===5){for(let k=1;k<=2;k++)shots.push({...e,id:i,x:e.x+k*140,born:time});}
  }
 });
 const h=p.width*(1.38-.46*p.duck),half=23;
 for(const s of shots){
  s.x-=s.speed*dt;const sw=s.type==='word'?s.text.length*16+25:30,sh=s.type==='word'?31:44;
  if(s.x+sw/2>p.x-half&&s.x-sw/2<p.x+half&&s.y+sh/2>p.y-h&&s.y-sh/2<p.y-10)die(s.type==='word'?s.text:'note');
  if(!s.passed&&s.x<p.x-half-sw){s.passed=true;events.push({kind:'dodge',t:time,x:p.x,type:s.type,duck:p.duck,airborne:!p.grounded});}
 }
 shots=shots.filter(s=>s.x>p.x-1500);effects=effects.filter(e=>time-e.born<1.3);
 if(p.y>1250)die('gap');
 if(p.x>7460&&finishAt<0){finishAt=time;events.push({kind:'exit',t:time,x:p.x});effect('door',7480,730);}
 // Damped look-ahead. The world scrolls smoothly; y follows drops more than jumps.
 const tx=Math.max(0,p.x-650+clamp(p.vx*.18,-80,120));
 cam.vx+=(tx-cam.x)*65*dt-cam.vx*16*dt;cam.x+=cam.vx*dt;
 const ty=clamp((p.y-800)*.32,-20,70);
 cam.vy+=(ty-cam.y)*30*dt-cam.vy*11*dt;cam.y+=cam.vy*dt;
 const targetZoom=p.x>6200?1.16:1;cam.zoom+= (targetZoom-cam.zoom)*dt*2;
}
// Every architectural edge below is built from discrete glyph marks.
function glyphText(text,x,y,size=17,color=C.bone,alpha=1){ctx.save();ctx.globalAlpha=alpha;ctx.fillStyle=color;ctx.font=`${size}px Consolas,monospace`;ctx.textAlign='left';ctx.textBaseline='top';ctx.fillText(text,x,y);ctx.restore();}
function symbolLine(x1,y1,x2,y2,char='-',color=C.ash,spacing=18,size=18){const dx=x2-x1,dy=y2-y1,len=Math.hypot(dx,dy),n=Math.max(1,Math.ceil(len/spacing));for(let i=0;i<=n;i++)glyphText(char,x1+dx*i/n-size*.28,y1+dy*i/n-size*.55,size,color);}
function box(x,y,w,h,color=C.ash,sp=18){symbolLine(x,y,x+w,y,'-',color,sp);symbolLine(x,y+h,x+w,y+h,'-',color,sp);symbolLine(x,y,x,y+h,'|',color,sp);symbolLine(x+w,y,x+w,y+h,'|',color,sp);for(const a of [[x,y],[x+w,y],[x,y+h],[x+w,y+h]])glyphText('+',a[0]-5,a[1]-10,18,color);}
function note(x,y,scale=1,col=C.bone,rotation=0){ctx.save();ctx.translate(x,y);ctx.rotate(rotation);ctx.scale(scale,scale);symbolLine(5,-28,5,9,'|',col,9,17);symbolLine(7,-27,24,-16,'\\',col,8,16);glyphText('(@)',-21,4,18,col);ctx.restore();}
function trumpet(e){const x=e.x,y=e.y;box(x+25,y-15,190,34,C.ash,14);symbolLine(x+27,y-13,x-40,y-43,'\\',C.bone,13);symbolLine(x-40,y-43,x-40,y+45,'|',C.bone,13);symbolLine(x-40,y+45,x+27,y+15,'/',C.bone,13);for(let k=0;k<3;k++){box(x+60+k*40,y-60,14,46,C.bone,12);}glyphText('TRUMPET.EXE',x+40,y+34,16,C.ash);}
function layerBackground(parallax,opacity){
 ctx.save();ctx.globalAlpha=opacity;ctx.translate(-cam.x*parallax,-cam.y*parallax);
 const start=Math.floor(cam.x*parallax/340)*340;
 for(let x=start-340;x<cam.x*parallax+W+340;x+=340){
  const idx=Math.floor(x/340);box(x+28,210,240,500,C.graph,20);
  glyphText(`AI / ${String(Math.abs(idx)%99).padStart(2,'0')}`,x+48,232,17,C.ash);
  for(let r=0;r<8;r++)glyphText((r%3===0?'if (clone) { repeat(); }':r%3===1?'[..] === [..] === [..]':'// queue : voice : sync'),x+44,278+r*22,13,C.ash,.7);
  PlatformerCharacter.draw(ctx,{x:x+145,y:682,width:65,vx:0,vy:0,grounded:true,facing:1,noHeart:true,opacity:.32,bone:C.ash,knock:C.ink2},time);
 }
 symbolLine(start-400,738,cam.x*parallax+W+400,738,'=',C.graph,20);
 ctx.restore();
}
function drawWorld(){
 const left=cam.x-400,right=cam.x+W+500;
 // Overhead code gantry: readable machinery rather than random full-screen noise.
 for(let x=Math.floor(left/600)*600;x<right;x+=600){
  symbolLine(x,120,x+570,120,'=',C.graph,16);symbolLine(x+30,120,x+30,410,'|',C.graph,20);
  glyphText(x<3000?'for (AI of line) { sing(); }':'while (alive) { run(RIGHT); }',x+55,138,16,C.ash,.65);
 }
 for(const s of terrain){if(s.end<left||s.x>right)continue;
  ctx.fillStyle=C.ink2;ctx.fillRect(s.x,s.y, s.end-s.x,260);
  const x0=Math.max(s.x,Math.floor(left/36)*36),x1=Math.min(s.end,right);
  for(let x=x0;x<x1;x+=36){glyphText('[=]',x,s.y-8,20,C.bone);glyphText('[:]',x,s.y+25,17,C.ash);}
  for(let r=1;r<8;r++)for(let x=x0;x<x1;x+=35)glyphText((r%3===0?'@@':r%3===1?'%#':'::'),x,s.y+25+r*24,16,r<3?C.graph:'#252527');
  symbolLine(s.x,s.y,s.x,s.y+160,'|',C.ash,18);symbolLine(s.end,s.y,s.end,s.y+160,'|',C.ash,18);
  glyphText(s.name,s.x+35,s.y+59,16,C.ash);
 }
 for(let i=0;i<terrain.length-1;i++){const a=terrain[i],b=terrain[i+1];if(b.x-a.end<20)continue;const pitY=Math.max(a.y,b.y)+150;for(let x=a.end+15;x<b.x;x+=29)glyphText('/\\',x,pitY,25,C.ash);}
 emitters.forEach((e,i)=>{if(e.x>left-200&&e.x<right)trumpet(e);});
 // A factory entrance recurs exactly at the reset.
 box(80,560,115,238,C.ash);glyphText('SPAWN',93,576,18,C.bone);glyphText('00',124,606,23,C.ash);
 // Large, clear end gate.
 box(7420,570,140,250,C.bone,14);box(7440,589,100,226,C.ash,14);glyphText('REAL',7440,530,35,C.bone);
 if(finishAt>=0){const close=clamp((time-finishAt)/.45,0,1);ctx.fillStyle=C.ink2;ctx.fillRect(7442,595,96*close,213);for(let y=604;y<810;y+=23)glyphText('|||',7445,y,18,C.graph,close);}
 for(const s of shots){if(s.type==='note')note(s.x,s.y,1.4,C.bone,Math.sin((time-s.born)*10)*.12);else {const w=s.text.length*16+28;ctx.fillStyle=C.ink;ctx.fillRect(s.x-w/2-5,s.y-22,w+10,44);box(s.x-w/2,s.y-20,w,40,C.bone,12);glyphText(s.text,s.x-w/2+12,s.y-12,25,C.bone);}
  for(let k=1;k<=3;k++)glyphText('<',s.x+55+k*24,s.y-8,17,C.ash,.5-k*.1);
 }
 for(const e of effects){const age=time-e.born;
  if(e.kind==='land'||e.kind==='takeoff'){for(let k=0;k<6;k++){const side=k%2?1:-1;glyphText(k%2?'_':'-',e.x+side*(17+age*120+(k>>1)*11),e.y-8-age*22+age*age*100,17,C.bone,Math.max(0,.8-age*3));}}
  if(e.kind==='death'){for(let k=0;k<30;k++){const a=seed(k+37)*Math.PI*2,v=100+seed(k+85)*330;glyphText('|-/\\+_'[k%6],e.x+Math.cos(a)*v*age,e.y+Math.sin(a)*v*age+600*age*age,25,C.bone,Math.max(0,1-age));}}
  if(e.kind==='fire'){glyphText('> <',e.x-55-age*80,e.y-11,21,C.bone,Math.max(0,1-age*4));}
 }
 if(!p.dead)PlatformerCharacter.draw(ctx,p,time);
 // Sparse foreground machinery moves faster than the background, emphasizing speed.
}
function draw(){
 ctx.fillStyle=C.ink;ctx.fillRect(0,0,W,H);layerBackground(.31,.72);
 ctx.save();ctx.translate(W*.36,H*.62);ctx.scale(cam.zoom,cam.zoom);ctx.translate(-W*.36,-H*.62);ctx.translate(-cam.x,-cam.y);
 if(p.dead&&time-deadAt<.18){const q=(.18-(time-deadAt))/.18;ctx.translate(Math.sin(time*100)*q*7,Math.cos(time*120)*q*4);}
 drawWorld();ctx.restore();
 // Foreground character rails are kept low so they do not cover the heroine.
 ctx.save();ctx.globalAlpha=.48;for(let x=-cam.x*1.1%900;x<W;x+=900){symbolLine(x,1020,x+600,1020,'=',C.ash,24);symbolLine(x+600,950,x+600,1080,'|',C.ash,22);}ctx.restore();
 ctx.fillStyle=C.ink;ctx.fillRect(0,0,W,90);glyphText('MUSIC FACTORY  //  EXIT THE LOOP',56,29,23,C.bone);
 glyphText(`ATTEMPT ${String(attempt).padStart(2,'0')}`,W-240,32,22,C.bone);
 if(p.dead){ctx.fillStyle=C.ink;ctx.fillRect(665,410,600,124);glyphText('return spawn(0);',698,444,44,C.bone);}
 if(finishAt>=0&&time-finishAt>.5){glyphText('HEART != NULL',W-425,94,24,C.bone);}
}
function renderAt(t){if(t<time-DT)reset('auto');while(time+DT<=t+1e-7)step(DT);draw();return {time,x:p.x,y:p.y,vy:p.vy,grounded:p.grounded,attempt,dead:p.dead,hair:p.hair,finishAt};}
function raf(stamp){if(renderMode)return;if(!lastTimestamp)lastTimestamp=stamp;const delta=Math.min(.04,(stamp-lastTimestamp)/1000);lastTimestamp=stamp;accumulator+=delta;while(accumulator>=DT){step(DT);accumulator-=DT;}draw();if(mode==='auto'&&time>20.5)reset('auto');requestAnimationFrame(raf);}
document.getElementById('auto').onclick=()=>{reset('auto');lastTimestamp=0;};document.getElementById('play').onclick=()=>{reset('manual');lastTimestamp=0;};
addEventListener('keydown',e=>{if(['Space','ArrowUp','ArrowDown','ArrowLeft','ArrowRight'].includes(e.code))e.preventDefault();keys.add(e.code);if(e.code==='KeyR')reset(mode);});addEventListener('keyup',e=>keys.delete(e.code));
window.demo={ready:true,renderAt,reset,events:()=>events,state:()=>({time,p:{...p},cam:{...cam},attempt,finishAt,shots:shots.map(s=>({...s}))}),duration:20,fps:60,physicsHz:120};
reset('auto');if(!renderMode)requestAnimationFrame(raf);
})();
