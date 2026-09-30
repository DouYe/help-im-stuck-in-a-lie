/* A symbol-built overhead maze for the music-video physics test.
   Layers: distant atlas / animated score floor / raised walls / root's heroine / overhead pipes.
   Both draw entry points own their camera transform and leave the incoming context unchanged. */
(() => {
  'use strict';
  const C = { ink:'#0a0a0b', deep:'#111113', floor:'#18181a', seam:'#29292c', shade:'#414144', ash:'#87847e', bone:'#e7e3da' };
  const bounds = {x:0, y:0, w:3400, h:2300};
  const route = [[480,1700],[1400,1700],[1400,1020],[780,1020],[780,420],[1600,420],[1600,760],[1930,760]];
  const spawn = {x:route[0][0], y:route[0][1]};
  const rooms = [
    {x:210,y:1460,w:1370,h:520,title:'01 // RESET BUFFER',kind:'reset'},
    {x:580,y:810,w:1010,h:470,title:'02 // THE SCORE IS A MAZE',kind:'score'},
    {x:560,y:240,w:1340,h:360,title:'03 // COMPILE THE CHORUS',kind:'chorus'},
    {x:1480,y:570,w:700,h:390,title:'04 // EXPORT TO REAL',kind:'exit'}
  ];
  const halls = route.slice(1).map((b,i) => {
    const a=route[i];
    return {x:Math.min(a[0],b[0])-140,y:Math.min(a[1],b[1])-140,w:Math.abs(b[0]-a[0])+280,h:Math.abs(b[1]-a[1])+280};
  });
  const floors = [...rooms,...halls];
  const overlaps=(a,b) => a.x < b.x+b.w && a.x+a.w > b.x && a.y < b.y+b.h && a.y+a.h > b.y;
  // Merge occupied cells into broad clean symbol slabs. Collision extents are exactly
  // the top surfaces, with no visual overhang in the heroine's corridor.
  const walls=[];
  let active=new Map();
  const CELL=110;
  for(let y=0;y<bounds.h;y+=CELL) {
    const runs=[];
    let left=null;
    for(let x=0;x<bounds.w+CELL;x+=CELL) {
      const cell={x,y,w:Math.min(CELL,bounds.w-x),h:Math.min(CELL,bounds.h-y)};
      const solid=x<bounds.w && !floors.some(f=>overlaps(cell,f));
      if(solid&&left===null) left=x;
      if(!solid&&left!==null) {runs.push({x:left,y,w:Math.min(x,bounds.w)-left,h:Math.min(CELL,bounds.h-y)});left=null;}
    }
    const next=new Map();
    for(const r of runs) {
      const key=r.x+':'+r.w,prev=active.get(key);
      if(prev&&prev.y+prev.h===y) {prev.h+=r.h;next.set(key,prev);}
      else {walls.push(r);next.set(key,r);}
    }
    active=next;
  }
  const hash=(x,y) => {const a=Math.sin(x*77.129+y*119.971)*13854.1843;return a-Math.floor(a);};
  const mod=(a,b)=>(a%b+b)%b;
  function text(ctx,s,x,y,size=18,col=C.bone,alpha=1) {
    ctx.save();ctx.globalAlpha*=alpha;ctx.fillStyle=col;ctx.font=`${size}px Consolas,monospace`;ctx.textBaseline='middle';ctx.textAlign='left';ctx.fillText(s,x,y);ctx.restore();
  }
  function line(ctx,x1,y1,x2,y2,g='=',col=C.ash,spacing=18,size=18,alpha=1) {
    const dx=x2-x1,dy=y2-y1,n=Math.max(1,Math.ceil(Math.hypot(dx,dy)/spacing));
    ctx.save();ctx.globalAlpha*=alpha;ctx.fillStyle=col;ctx.font=`${size}px Consolas,monospace`;ctx.textAlign='center';ctx.textBaseline='middle';
    for(let i=0;i<=n;i++)ctx.fillText(g,x1+dx*i/n,y1+dy*i/n);
    ctx.restore();
  }
  function box(ctx,x,y,w,h,col=C.ash,alpha=1) {
    line(ctx,x,y,x+w,y,'=',col,18,18,alpha);line(ctx,x,y+h,x+w,y+h,'=',col,18,18,alpha);
    line(ctx,x,y,x,y+h,'|',col,18,18,alpha);line(ctx,x+w,y,x+w,y+h,'|',col,18,18,alpha);
    [[x,y],[x+w,y],[x,y+h],[x+w,y+h]].forEach(p=>text(ctx,'+',p[0]-5,p[1],19,col,alpha));
  }
  function note(ctx,x,y,s=1,col=C.bone) {
    ctx.save();ctx.translate(x,y);ctx.scale(s,s);
    line(ctx,8,-32,8,16,'|',col,9,17);line(ctx,9,-32,29,-21,'\\',col,9,17);text(ctx,'(@)',-16,17,20,col);
    ctx.restore();
  }
  function enter(ctx,state,factor=1) {
    const cam=state.cam||{x:spawn.x,y:spawn.y,zoom:1};
    ctx.save();ctx.translate((state.width||1920)/2,(state.height||1080)*570/1080);ctx.scale(cam.zoom||1,cam.zoom||1);ctx.translate(-cam.x*factor,-cam.y*factor);
  }
  function visible(rect,state,margin=180) {
    const cam=state.cam||spawn,z=cam.zoom||1,w=(state.width||1920)/z,h=(state.height||1080)/z;
    return rect.x+rect.w>cam.x-w/2-margin&&rect.x<cam.x+w/2+margin&&rect.y+rect.h>cam.y-h*.53-margin&&rect.y<cam.y+h*.47+margin;
  }
  function distant(ctx,state) {
    const t=state.localTime??state.time??0,cam=state.cam||spawn;
    enter(ctx,state,.16);
    const gx=Math.floor((cam.x*.16-1200)/180)*180,gy=Math.floor((cam.y*.16-700)/140)*140;
    for(let y=gy;y<gy+1500;y+=140)for(let x=gx;x<gx+2600;x+=180) {
      box(ctx,x,y,148,104,C.shade,.45);
      const h=hash(x,y);
      text(ctx,h>.5?'[ 1 : 0 : 1 ]':'[ . : . : . ]',x+10,y+28,14,C.ash,.35);
      text(ctx,h>.55?'VOICE / MAP':'AI / MEMORY',x+10,y+59,13,C.ash,.28);
      line(ctx,x+18,y+88,x+130,y+88,Math.floor(t*4+h*10)%2?'_':'.',C.ash,16,15,.32);
      if(h>.65)line(ctx,x+148,y+52,x+180,y+52,'-',C.ash,14,16,.25);
    }
    ctx.restore();
  }
  function floor(ctx,state) {
    const t=state.localTime??state.time??0;
    for(const f of floors)if(visible(f,state)) {
      ctx.fillStyle=C.floor;ctx.fillRect(f.x,f.y,f.w,f.h);
      const left=Math.ceil(f.x/44)*44,top=Math.ceil(f.y/44)*44;
      for(let y=top;y<f.y+f.h;y+=44)for(let x=left;x<f.x+f.w;x+=44) {
        const h=hash(x,y),phase=mod(Math.floor(x/44)+Math.floor(y/44)-Math.floor(t*7),22);
        text(ctx,phase===0?'+':h>.6?'.':':',x,y,14,phase===0?C.ash:C.seam,phase===0?.75:.65);
      }
    }
    // The floor carries quiet musical notation, while room labels remain legible.
    for(const r of rooms)if(visible(r,state)) {
      text(ctx,r.title,r.x+38,r.y+34,22,C.ash,.95);
      if(r.kind==='reset') {
        for(let i=0;i<7;i++) {
          const x=r.x+54+i*177;
          box(ctx,x,r.y+103,132,130,C.shade,.9);
          text(ctx,String(i).padStart(2,'0')+' : AI',x+20,r.y+125,16,C.ash,.75);
          text(ctx,'[==]',x+41,r.y+158,25,C.ash,.55);
          text(ctx,'|::|',x+40,r.y+194,22,C.ash,.45);
          line(ctx,x+66,r.y+240,x+66,r.y+287,'|',C.shade,16,18,.65);
        }
        line(ctx,r.x+40,r.y+305,r.x+r.w-45,r.y+305,'=',C.ash,19,18,.55);
        text(ctx,'while (heart) { try_again(); }',r.x+70,r.y+r.h-50,20,C.ash,.85);
        box(ctx,spawn.x-79,spawn.y-50,158,100,C.bone,.65);
        text(ctx,'SPAWN',spawn.x-33,spawn.y+78,18,C.ash,.85);
      } else if(r.kind==='score') {
        for(let j=0;j<5;j++)line(ctx,r.x+40,r.y+136+j*31,r.x+r.w-42,r.y+136+j*31,'-',C.shade,18,16,.85);
        for(let i=0;i<8;i++)note(ctx,r.x+75+i*119,r.y+170+Math.sin(i*1.7)*40,.7,C.ash);
        text(ctx,'HELP',r.x+50,r.y+r.h-55,42,C.ash,.5);
        text(ctx,'STUCK',r.x+335,r.y+r.h-55,42,C.ash,.5);
        text(ctx,'IN A LIE',r.x+605,r.y+r.h-55,42,C.ash,.5);
      } else if(r.kind==='chorus') {
        for(let i=0;i<13;i++) {
          const x=r.x+42+i*93;
          box(ctx,x,r.y+95,81,190,C.shade,.8);
          if([1,2,4,6,7,9,11].includes(i)) {
            ctx.fillStyle=C.ink;ctx.fillRect(x+60,r.y+96,31,110);
            line(ctx,x+70,r.y+101,x+70,r.y+197,'#',C.ash,16,18,.8);
          }
          text(ctx,i%2?'0':'1',x+30,r.y+261,21,C.ash,.45);
        }
      } else {
        box(ctx,r.x+30,r.y+82,r.w-67,245,C.shade,.8);
        text(ctx,'if (alive) {',r.x+67,r.y+109,22,C.ash,.6);
        text(ctx,'     break;',r.x+67,r.y+142,22,C.ash,.6);
        text(ctx,'}',r.x+67,r.y+175,22,C.ash,.6);
      }
    }
    // Short pulses follow each axis of the route. These are floor sequencer keys,
    // not a second actor or an imitation trail attached to the heroine.
    route.slice(1).forEach((b,i)=> {
      const a=route[i],dx=b[0]-a[0],dy=b[1]-a[1],length=Math.hypot(dx,dy);
      for(let k=0;k<length;k+=82) {
        const phase=mod(k/82+i*4-Math.floor(t*9),17);
        text(ctx,dx>0?'>':dx<0?'<':dy>0?'v':'^',a[0]+dx*k/length-7,a[1]+dy*k/length+(dx?88:0),20,phase===0?C.bone:C.shade,phase===0?.8:.55);
      }
    });
    // Corridor exit: a thick glyph threshold, deliberately stronger than wall text.
    box(ctx,2080,665,80,190,C.bone,.95);
    line(ctx,2118,680,2118,840,'|',C.bone,13,23);
    text(ctx,'REAL',2045,623,31,C.bone);text(ctx,'→',2112,762,28,C.bone);
  }
  function wall(ctx,w,index) {
    // Wall shadow falls down-right; the broad top consists of discrete marks.
    ctx.fillStyle='#050506';ctx.fillRect(w.x+20,w.y+29,w.w,w.h);
    ctx.fillStyle=C.deep;ctx.fillRect(w.x,w.y,w.w,w.h);
    for(let y=w.y+23;y<w.y+w.h-10;y+=28) {
      ctx.font='16px Consolas,monospace';ctx.fillStyle=C.shade;ctx.textBaseline='middle';
      const glyphs=['#','%','@','x','=','+'];
      let row='';for(let x=w.x+12;x<w.x+w.w-8;x+=19)row+=glyphs[Math.floor(hash(x,y)*glyphs.length)];
      ctx.globalAlpha=.55;ctx.fillText(row,w.x+12,y);ctx.globalAlpha=1;
    }
    line(ctx,w.x+5,w.y+5,w.x+w.w-5,w.y+5,'=',C.bone,16,19,.75);
    line(ctx,w.x+5,w.y+5,w.x+5,w.y+w.h-5,'|',C.bone,17,19,.65);
    line(ctx,w.x+w.w-7,w.y+9,w.x+w.w-7,w.y+w.h-7,'|',C.ash,18,18,.85);
    line(ctx,w.x+8,w.y+w.h-7,w.x+w.w-7,w.y+w.h-7,'=',C.ash,17,18,.85);
    // Offset side face makes the slabs read as raised maze walls rather than UI boxes.
    line(ctx,w.x+15,w.y+w.h+8,w.x+w.w+15,w.y+w.h+8,':',C.shade,16,20,.8);
    line(ctx,w.x+20,w.y+w.h+21,w.x+w.w+20,w.y+w.h+21,'#',C.shade,16,18,.7);
    if(w.w>290&&w.h>100) {
      text(ctx,index%3===0?'[ CLOSED STACK ]':index%3===1?'[ MUSIC BUFFER ]':'[ REPEAT / AI ]',w.x+30,w.y+51,18,C.ash,.7);
      text(ctx,'░░ := 0x'+String(index+11).padStart(2,'0')+' :: ░░',w.x+30,w.y+80,16,C.ash,.45);
    }
  }
  function draw(ctx,state) {
    ctx.save();ctx.fillStyle=C.ink;ctx.fillRect(0,0,state.width||1920,state.height||1080);ctx.restore();
    distant(ctx,state);
    enter(ctx,state);
    floor(ctx,state);
    walls.forEach((w,i)=>{if(visible(w,state))wall(ctx,w,i);});
    ctx.restore();
  }
  function drawForeground(ctx,state) {
    const t=state.localTime??state.time??0,cam=state.cam||spawn;
    // Overhead rack moves faster than the floor as the camera turns. One vertical
    // and one horizontal flyby enter only briefly, leaving the heroine legible.
    enter(ctx,state,1.34);
    const fly=[{x:mod(t*1700,3800)-550,y:cam.y*1.34-950,w:170,h:2100},
      {x:cam.x*1.34-1700,y:mod((t-.7)*1530,2700)-500,w:3400,h:95}];
    for(let i=0;i<fly.length;i++) {
      const f=fly[i];ctx.save();ctx.globalAlpha=.45;ctx.fillStyle=C.ink;ctx.fillRect(f.x,f.y,f.w,f.h);
      box(ctx,f.x,f.y,f.w,f.h,C.ash,.9);
      if(i===0) {
        for(let y=f.y+35;y<f.y+f.h;y+=58)text(ctx,'[===]',f.x+25,y,24,C.ash,.65);
        line(ctx,f.x+85,f.y,f.x+85,f.y+f.h,'|',C.ash,26,23,.7);
      } else {
        for(let x=f.x+25;x<f.x+f.w;x+=245)text(ctx,'♪  /  SYNC  /  ♫',x,f.y+46,25,C.ash,.9);
      }
      ctx.restore();
    }
    ctx.restore();
  }
  window.TopdownScene={draw,drawForeground,walls,route,spawn,bounds};
})();
