/* Music-video-first platformer revision: snap control, double jump, six direct-cut worlds. */
(() => {
'use strict';
const W=1920,H=1080,DT=1/120,G=5200,JUMP=1500,SPEED=1320,DASH=2850;
const C={ink:'#0a0a0b',bone:'#eee9df',ash:'#817d75',graph:'#353538'};
const canvas=document.getElementById('screen'),ctx=canvas.getContext('2d',{alpha:false});
const music=document.getElementById('music');let soundOn=false;
const renderMode=new URLSearchParams(location.search).has('render');if(renderMode)document.body.classList.add('render');
const definitions=[
 {id:'factory',name:'01 / MUSIC FACTORY',start:0,end:3.2,spawn:[360,850],speed:SPEED,platforms:[[0,850,850],[1180,1900,790],[2280,3000,680],[3000,3500,890],[3900,5500,760]]},
 {id:'shaft',name:'02 / VERTICAL MEMORY',start:3.2,end:6.4,spawn:[520,1700],speed:1150,platforms:[[150,850,1700],[1080,1710,1430],[250,850,1160],[1110,1800,900],[370,1040,620],[1080,2000,360]]},
 {id:'underwater',name:'03 / BUFFER SEA',start:6.4,end:9.6,spawn:[350,1100],speed:1120,platforms:[],route:[[350,1100],[1200,580],[2000,1130],[1680,1410],[3300,600]]},
 {id:'topdown',name:'04 / ROUTE GRID',start:9.6,end:13.6,spawn:[480,1700],speed:1220,platforms:[]},
 {id:'sky',name:'05 / SKY SCORE',start:13.6,end:16.8,spawn:[340,940],speed:1380,platforms:[[0,760,940],[1250,2070,810],[2350,3140,740],[3360,4210,900],[4380,5230,700],[5440,6650,860]]},
 {id:'final',name:'06 / LYRIC CATHEDRAL',start:16.8,end:20,spawn:[280,900],speed:1440,platforms:[[0,1150,900],[1470,2250,790],[2560,3300,860],[3630,4800,760]]}
];
const keys=new Set();let mode='auto',time=0,sceneIndex=0,localTime=0,p,cam,platforms=[],shots=[],effects=[],ghosts=[],events=[],fired=new Set(),routeIndex=1,shaftIndex=1,deadUntil=-1;
let accumulator=0,lastStamp=0,jumpWas=false,dashWas=false,rehearsing=false,attemptTime=0;
const rehearsals=new Map();
const clamp=(v,a,b)=>Math.min(b,Math.max(a,v));
const def=()=>definitions[sceneIndex];
const random=n=>{const a=Math.sin(n*127.71+37.1)*43758.5453;return a-Math.floor(a);};
function spawn(index,log=true){
 sceneIndex=index;const d=def();localTime=0;attemptTime=0;const xy=d.id==='topdown'?[TopdownScene.spawn.x,TopdownScene.spawn.y]:d.spawn;
 p={x:xy[0],y:xy[1],vx:0,vy:0,width:110,maxSpeed:d.speed,facing:1,grounded:!['underwater','topdown'].includes(d.id),duck:0,landing:0,runPhase:0,hair:PlatformerCharacter.createHair(),jumps:0,dashAvailable:1,dashing:0,dashTime:0,dashCooldown:0,grace:.08,jumpBuffer:0,airAge:0,z:0,zv:0,dead:false,lastGroundY:xy[1]};
 cam={x:p.x+60,y:p.y-(d.id==='topdown'?0:d.id==='underwater'?50:d.id==='shaft'?100:190),zoom:d.id==='topdown'?.9:1};
 platforms=d.platforms.map((a,i)=>({x:a[0],end:a[1],y:a[2],baseY:a[2],index:i}));shots=[];effects=[];ghosts=[];fired=new Set();routeIndex=1;shaftIndex=1;deadUntil=-1;jumpWas=false;dashWas=false;
 document.getElementById('scene').value=String(index);if(log)events.push({kind:'cut',t:time,scene:d.id});
}
function reset(nextMode='auto',index=0){mode=nextMode;time=0;events=[];accumulator=0;spawn(index);draw();if(music&&!rehearsing){music.pause();music.currentTime=0;if(mode==='auto'&&soundOn&&!renderMode)music.play().catch(()=>{});}}
function groundAt(x,y=p.y){return platforms.find(s=>x>=s.x-18&&x<=s.end+18&&Math.abs(y-s.y)<8);}
function effect(kind,x,y){effects.push({kind,x,y,born:time});}
function jump(){
 if(p.jumpBuffer<=0||p.dashTime>0||p.duck>.55)return false;
 const grounded=p.grounded||p.grace>0;
 if(!grounded&&p.jumps>=2)return false;
 p.jumpBuffer=0;p.jumps=grounded?1:p.jumps+1;p.grounded=false;p.grace=0;p.vy=-JUMP*(p.jumps===2?.92:1);p.airAge=0;
 events.push({kind:p.jumps===2?'double-jump':'jump',t:time,scene:def().id,x:p.x,y:p.y});effect(p.jumps===2?'double':'jump',p.x,p.y);return true;
}
function dash(mx,my){
 if(p.dashCooldown>0||p.dashAvailable<=0)return false;const l=Math.hypot(mx,my)||1;
 p.dashX=(mx||(!my?p.facing:0))/l;p.dashY=my/l;p.dashTime=.115;p.dashCooldown=.24;p.dashAvailable--;p.dashing=1;
 events.push({kind:'dash',t:time,scene:def().id,dx:p.dashX,dy:p.dashY});effect('dash',p.x,p.y-65);return true;
}
function die(cause){if(p.dead)return;p.dead=true;deadUntil=time+.22;events.push({kind:'death',t:time,scene:def().id,cause});effect('death',p.x,p.y-70);}
function routeControl(route){
 const target=route[Math.min(routeIndex,route.length-1)],dx=target[0]-p.x,dy=target[1]-p.y;
 const dist=Math.hypot(dx,dy);if(dist<24&&routeIndex<route.length-1){routeIndex++;return routeControl(route);}
 if(dist<12)return {mx:0,my:0,jump:false,dash:false,duck:false};
 return {mx:dx/dist,my:dy/dist,jump:false,dash:false,duck:false};
}
function control(){
 if(mode==='manual')return {mx:(keys.has('KeyD')||keys.has('ArrowRight')?1:0)-(keys.has('KeyA')||keys.has('ArrowLeft')?1:0),my:(keys.has('KeyS')||keys.has('ArrowDown')?1:0)-(keys.has('KeyW')||keys.has('ArrowUp')?1:0),jump:keys.has('Space')||(['factory','sky','final','shaft'].includes(def().id)&&(keys.has('KeyW')||keys.has('ArrowUp'))),dash:keys.has('KeyX')||keys.has('ShiftLeft')||keys.has('ShiftRight'),duck:keys.has('KeyS')||keys.has('ArrowDown')};
 const d=def();
 if(d.id==='topdown')return routeControl(TopdownScene.route);
 if(d.id==='underwater'){const c=routeControl(d.route);c.dash=attemptTime>1.7&&attemptTime<1.72;return c;}
 if(d.id==='shaft'){
  if(p.grounded&&shaftIndex<platforms.length&&p.y<=platforms[shaftIndex].y+6)shaftIndex++;
  const s=platforms[Math.min(shaftIndex,platforms.length-1)],target=(s.x+s.end)/2,dx=target-p.x;
  const mx=Math.abs(dx)<55?0:Math.sign(dx);
  return {mx,my:-1,jump:(p.grounded&&shaftIndex<platforms.length)||(p.jumps===1&&p.vy>-380&&p.airAge>.20),dash:false,duck:false};
 }
 const floor=groundAt(p.x),index=platforms.indexOf(floor),next=platforms[index+1];let mx=1,my=0,wantJump=false,wantDash=false,duck=false;
 if(floor&&next&&floor.end-p.x<210&&(next.x-floor.end>20||next.y<floor.y-20))wantJump=true;
 if(floor&&wantJump)p.wideGap=!!next&&next.x-floor.end>=300;
 const farGap=d.id==='sky'||p.wideGap;
 if(p.jumps===1&&p.vy>-260&&p.airAge>.22&&(farGap||d.id==='final'))wantJump=true;
 if(d.id==='sky'&&p.jumps===2&&p.airAge>.16&&p.dashAvailable&&p.vy>-450)wantDash=true;
 // Two brief lateral reversals expose snap responsiveness in the film.
 if(d.id==='factory'&&attemptTime>1.22&&attemptTime<1.36)mx=-1;
 if(d.id==='final'&&attemptTime>.78&&attemptTime<.86)mx=-1;
 // The film follows a rehearsed movement path; manual mode remains a real collision game.
 if(d.id==='final'&&attemptTime>2.25&&attemptTime<2.28)wantDash=true;
 return {mx,my,jump:wantJump,dash:wantDash,duck};
}
function collideMaze(prevX,prevY){
 const r=25;for(const w of TopdownScene.walls){const wx=Array.isArray(w)?w[0]:w.x,wy=Array.isArray(w)?w[1]:w.y,ww=Array.isArray(w)?w[2]:w.w,wh=Array.isArray(w)?w[3]:w.h;
  if(p.x+r<=wx||p.x-r>=wx+ww||p.y+r<=wy||p.y-r>=wy+wh)continue;
  if(prevX+r<=wx){p.x=wx-r;p.vx=0;}else if(prevX-r>=wx+ww){p.x=wx+ww+r;p.vx=0;}else if(prevY+r<=wy){p.y=wy-r;p.vy=0;}else if(prevY-r>=wy+wh){p.y=wy+wh+r;p.vy=0;}
 }
}
function fireHazards(){
 if(rehearsing)return;
 const d=def(),count=Math.min(mode==='auto'?Math.round((d.end-d.start)*10):Infinity,Math.floor((localTime+1e-6)*10)+1);
 for(let i=0;i<count;i++){
  if(fired.has(i))continue;fired.add(i);
  const type=i%3===0?'word':'note',label=['HELP','STUCK IN A LIE','MAKE ME REAL','HEART INSIDE'][Math.floor(i/3)%4];
  const flight=.38+(i%4)*.045,track=rehearsals.get(d.id),future=track?.[Math.min(track.length-1,Math.round((attemptTime+flight)*120))];
  const anchor=mode==='auto'&&future?future:{x:p.x,y:p.y-(d.id==='topdown'?0:78)};
  // Four attack directions and a changing open lane, calculated from the film's
  // actual physics rehearsal. No collision exemption is given to the film actor.
  const a=[Math.PI,-Math.PI*.5,0,Math.PI*.5,Math.PI*.78,Math.PI*1.22][i%6],speed=1800+(i%5)*100;
  const vx=Math.cos(a)*speed,vy=Math.sin(a)*speed;
  const lateral=(i%2?1:-1)*(type==='word'?160:125);
  let s={x:anchor.x-vx*flight-Math.sin(a)*lateral,y:anchor.y-vy*flight+Math.cos(a)*lateral,vx,vy,type,text:label,high:i%2===0,born:time,id:i,passed:false};
  // Film attacks graze the rehearsed route. Human input must find that narrow
  // moving opening; in manual mode the emitters aim directly at the live actor.
  if(mode==='auto'&&track){
   const half=type==='word'?label.length*8.3+43:47,high=d.id==='topdown'?50:97;
   // Select the closest safe crossing of the actual future trajectory. These
   // are stage directions for the music video, not an invincible player.
   outer:for(const margin of [0,65,135,230,340,470])for(const sign of [1,-1]){
    const lane=lateral*sign+(lateral<0?-margin:margin)*sign;
    const sx=anchor.x-vx*flight-Math.sin(a)*lane,sy=anchor.y-vy*flight+Math.cos(a)*lane;
    let safe=true;
    for(let k=12;k<336;k+=2){const age=k*DT,q=track[Math.round(attemptTime*120)+k];if(!q)break;
     if(Math.abs(sx+vx*age-q.x)<half+42&&Math.abs(sy+vy*age-q.y)<high+42){safe=false;break;}
    }
    if(safe){s.x=sx;s.y=sy;s.lane=lane;break outer;}
   }
  }else if(mode==='manual'){s.x=p.x-vx*flight;s.y=p.y-(d.id==='topdown'?0:78)-vy*flight;}
  shots.push(s);events.push({kind:'fire',t:time,scene:d.id,id:i,type});effect('fire',s.x,s.y);
 }
}
function step(dt){
 time+=dt;const expected=definitions.findIndex(d=>time>=d.start&&time<d.end);
 if(mode==='auto'&&expected>=0&&expected!==sceneIndex)spawn(expected);
 localTime+=dt;const d=def();
 if(p.dead){fireHazards();if(time>=deadUntil){const lt=localTime,done=fired;spawn(sceneIndex,false);localTime=lt;fired=done;
  if(d.id==='sky'){p.y=platforms[0].baseY+18*Math.sin(localTime*2.4);p.lastGroundY=p.y;}
  events.push({kind:'respawn',t:time,scene:d.id});}return;}
 attemptTime+=dt;p.topDown=d.id==='topdown';
 if(d.id==='sky')platforms.forEach(s=>s.y=s.baseY+18*Math.sin(localTime*2.4+s.index));
 const ctl=control(),prevX=p.x,prevY=p.y;p.airAge+=dt;p.dashCooldown=Math.max(0,p.dashCooldown-dt);p.grace=p.grounded?.085:Math.max(0,p.grace-dt);p.jumpBuffer=Math.max(0,p.jumpBuffer-dt);
 p.duck=clamp(p.duck+(ctl.duck?1:-1)*dt*20,0,1);if(ctl.mx)p.facing=Math.sign(ctl.mx);
 const jumpPress=ctl.jump&&(!jumpWas||mode==='auto');if(jumpPress)p.jumpBuffer=.10;
 if(ctl.dash&&(!dashWas||mode==='auto'))dash(ctl.mx,(['underwater','topdown','shaft'].includes(d.id)?ctl.my:0));
 if(d.id==='topdown'||d.id==='underwater'){
  const len=Math.hypot(ctl.mx,ctl.my),n=len>1?len:1;p.vx=d.speed*ctl.mx/n;p.vy=d.speed*ctl.my/n;
  if(p.dashTime>0){p.vx=p.dashX*DASH;p.vy=p.dashY*DASH;p.dashTime-=dt;}
  p.x+=p.vx*dt;p.y+=p.vy*dt;p.grounded=false;p.swim=d.id==='underwater';
  if(d.id==='underwater'){p.x=clamp(p.x,100,4600);p.y=clamp(p.y,300,1570);p.dashAvailable=1;}
  if(d.id==='topdown'){
   collideMaze(prevX,prevY);if(jumpPress&&p.jumps<2){p.zv=780;p.jumps++;events.push({kind:p.jumps===2?'double-jump':'jump',t:time,scene:d.id});}
   p.zv-=2600*dt;p.z=Math.max(0,p.z+p.zv*dt);if(p.z===0){p.zv=0;p.jumps=0;p.dashAvailable=1;}
  }
 }else{
  p.swim=false;jump();
  p.vx=ctl.mx*d.speed; // deliberate instant start/reversal/stop requested by Hon
  if(p.dashTime>0){p.vx=p.dashX*DASH;p.vy=p.dashY*DASH;p.dashTime-=dt;}
  else {if(mode==='manual'&&jumpWas&&!ctl.jump&&p.vy< -400)p.vy*=.55;p.vy=Math.min(2400,p.vy+G*dt);}
  p.x+=p.vx*dt;p.y+=p.vy*dt;p.grounded=false;
  for(const s of platforms){
   if(p.x+22<s.x||p.x-22>s.end)continue;
   if(prevY<=s.y+3&&p.y>=s.y&&p.vy>=0){const impact=p.vy;p.y=s.y;p.vy=0;p.grounded=true;p.lastGroundY=s.y;p.jumps=0;p.airAge=0;p.dashAvailable=1;p.wideGap=false;
    if(impact>480){p.landing=clamp(impact/1900,0,1);effect('land',p.x,p.y);events.push({kind:'land',t:time,scene:d.id,x:p.x,y:p.y});}
   }else if(p.y>s.y+8&&prevX+22<s.x&&p.x+22>=s.x){p.x=s.x-23;p.vx=0;}
  }
  if(p.y>2400||(d.id!=='shaft'&&p.y>1500))die('gap');p.x=clamp(p.x,70,6500);
 }
 p.dashing=p.dashTime>0?1:Math.max(0,p.dashing-dt*12);p.landing=Math.max(0,p.landing-dt*8);
 const distance=Math.hypot(p.x-prevX,p.y-prevY);p.runPhase+=Math.min(distance*Math.PI*2/140,dt*29);
 PlatformerCharacter.updateHair(p.hair,p,dt);jumpWas=ctl.jump;dashWas=ctl.dash;
 if(d.id==='final'&&p.x>platforms.at(-1).end-190&&!p.dead&&!p.escaped){p.escaped=true;events.push({kind:'exit',t:time,scene:d.id});}
 if(p.dashing&&Math.floor(time*120)%3===0)ghosts.push({p:{...p,hair:{...p.hair}},born:time});ghosts=ghosts.filter(g=>time-g.born<.12);
 fireHazards();
 for(const s of shots){s.x+=s.vx*dt;s.y+=s.vy*dt;const half=s.type==='word'?s.text.length*8.3+20:24,ph=d.id==='topdown'?35:p.width*(1.43-.30*p.duck);
  const cx=d.id==='topdown'?p.x:p.x,cy=d.id==='topdown'?p.y-p.z:p.y-ph*.5;
  const hit=Math.abs(s.x-cx)<half+23&&Math.abs(s.y-cy)<(d.id==='topdown'?32:ph*.5)+18;
  // Dash offers a short traversal grace; otherwise real collision resets the room.
  if(hit&&p.dashTime<=0&&time-s.born>.08)die(s.text||'note');
  if(!s.passed&&Math.hypot(s.x-p.x,s.y-p.y)>500&&((s.vx<0&&s.x<p.x-80)||(s.vy>0&&s.y>p.y+80))){s.passed=true;events.push({kind:'dodge',t:time,scene:d.id,type:s.type});}
 }
 shots=shots.filter(s=>time-s.born<2.8);effects=effects.filter(e=>time-e.born<.5);
 const tx=p.x+(d.id==='topdown'?0:60);let ty;
 if(d.id==='topdown')ty=p.y;else if(d.id==='underwater')ty=p.y-50;else if(d.id==='shaft')ty=p.y-100;else ty=p.lastGroundY-190+(p.y-p.lastGroundY)*.32;
 cam.x+=(tx-cam.x)*Math.min(1,dt*23);cam.y+=(ty-cam.y)*Math.min(1,dt*(d.id==='topdown'?23:14));
 const targetZoom=d.id==='topdown'?.92:d.id==='final'?1+localTime*.045:1;cam.zoom+=(targetZoom-cam.zoom)*Math.min(1,dt*4);
}
function text(s,x,y,size=20,col=C.bone,alpha=1){ctx.save();ctx.globalAlpha=alpha;ctx.font=`${size}px Consolas,monospace`;ctx.fillStyle=col;ctx.textBaseline='middle';ctx.fillText(s,x,y);ctx.restore();}
function note(x,y,r=1){ctx.save();ctx.translate(x,y);ctx.scale(r,r);ctx.strokeStyle=C.bone;ctx.lineWidth=3;ctx.beginPath();ctx.moveTo(5,12);ctx.lineTo(5,-25);ctx.lineTo(26,-13);ctx.stroke();text('(@)',-22,15,22);ctx.restore();}
function actor(){
 const isTop=def().id==='topdown';
 if(isTop){ctx.save();ctx.globalAlpha=.45;text(':: ::: ::',p.x-43,p.y+30,18,C.ash);ctx.restore();PlatformerCharacter.drawTop(ctx,{...p,y:p.y-p.z,width:102},time);}
 else PlatformerCharacter.draw(ctx,p,time);
}
function transform(){ctx.translate(960,570);ctx.scale(cam.zoom,cam.zoom);ctx.translate(-cam.x,-cam.y);}
function draw(){
 ctx.fillStyle=C.ink;ctx.fillRect(0,0,W,H);const s={time,localTime,p,cam,platforms,width:W,height:H};
 if(def().id==='topdown')TopdownScene.draw(ctx,s);else MusicWorlds.draw(ctx,def().id,s);
 ctx.save();transform();
 for(const g of ghosts){const q={...g.p,opacity:.28*(1-(time-g.born)/.12)};if(def().id==='topdown')PlatformerCharacter.drawTop(ctx,q,time);else PlatformerCharacter.draw(ctx,q,time);}
 for(const h of shots){if(h.type==='note')note(h.x,h.y,1.3);else {const ww=h.text.length*16.5+36;ctx.fillStyle=C.ink;ctx.fillRect(h.x-ww/2,h.y-23,ww,46);text('['+h.text+']',h.x-ww/2+2,h.y,27);}
  const speed=Math.hypot(h.vx,h.vy)||1;for(let k=0;k<4;k++)text(k%2?':':'.',h.x-h.vx/speed*(60+k*31),h.y-h.vy/speed*(60+k*31),19,C.ash,.45-k*.08);
 }
 for(const e of effects){const age=time-e.born;
  if(e.kind==='double'||e.kind==='jump'||e.kind==='land'){for(let k=0;k<10;k++){const a=k*Math.PI*2/10;text(k%2?'_':'+',e.x+Math.cos(a)*(20+age*210),e.y+Math.sin(a)*(8+age*70),18,C.bone,Math.max(0,.8-age*2.5));}}
  if(e.kind==='death'){for(let k=0;k<30;k++){const a=random(k+41)*6.283;text('|/\\-+'[k%5],e.x+Math.cos(a)*age*750,e.y+Math.sin(a)*age*600,25,C.bone,Math.max(0,1-age*3));}}
 }
 if(!p.dead)actor();ctx.restore();
 if(def().id==='topdown')TopdownScene.drawForeground(ctx,s);else MusicWorlds.drawForeground(ctx,def().id,s);
 // Film titles kept small; no explanatory game HUD covers the action.
 text(def().name,44,38,19,C.bone,.88);text('HEART / ESCAPE',W-232,38,18,C.ash,.8);
}
function renderAt(t){if(t<time-DT)reset('auto');while(time+DT<=t+1e-7)step(DT);draw();return {time,scene:def().id,localTime,p:{...p},cam:{...cam}};}
function raf(ts){if(renderMode)return;if(!lastStamp)lastStamp=ts;accumulator+=Math.min(.04,(ts-lastStamp)/1000);lastStamp=ts;while(accumulator>=DT){step(DT);accumulator-=DT;}draw();if(mode==='auto'&&time>20.35)reset('auto');requestAnimationFrame(raf);}
document.getElementById('auto').textContent='Replay film + music';document.getElementById('auto').onclick=()=>{soundOn=true;reset('auto');lastStamp=0;};document.getElementById('play').onclick=()=>{reset('manual',Number(document.getElementById('scene').value));lastStamp=0;};document.getElementById('scene').onchange=()=>reset('manual',Number(document.getElementById('scene').value));
addEventListener('keydown',e=>{if(['Space','ArrowUp','ArrowDown','ArrowLeft','ArrowRight'].includes(e.code))e.preventDefault();keys.add(e.code);if(e.code==='KeyR')reset(mode,mode==='manual'?sceneIndex:0);if(e.code==='KeyN')reset('manual',(sceneIndex+1)%6);});addEventListener('keyup',e=>keys.delete(e.code));
function rehearse(){
 rehearsing=true;
 for(let index=0;index<definitions.length;index++){
  reset('manual',index);mode='auto';time=definitions[index].start;const frames=[];
  const length=definitions[index].end-definitions[index].start;
  for(let n=0;n<Math.ceil(length/DT);n++){frames.push({x:p.x,y:p.y-(def().id==='topdown'?0:78)});step(DT);}
  rehearsals.set(definitions[index].id,frames);
 }
 rehearsing=false;
}
window.demo={ready:true,renderAt,reset,events:()=>events,state:()=>({time,scene:def().id,sceneIndex,localTime,p:{...p},cam:{...cam},shots:shots.map(s=>({...s})),mode}),duration:20,fps:60,physicsHz:120,scenes:definitions.map(d=>({id:d.id,start:d.start,end:d.end})),layerDepths:[.12,.35,.65,1,1.4],hazardsPerSecond:10};
rehearse();
reset('auto');if(!renderMode)requestAnimationFrame(raf);
})();
