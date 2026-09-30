/* Music-video worlds: all visible structure is composed of glyph marks.
 * Background parallax .12 / .35 / .65, traversable world 1.0, sparse foreground 1.4.
 * No bitmap assets, random runtime state, glow or orange paint. */
(function (global) {
  'use strict';
  const C = {ink:'#0a0a0b', deep:'#111113', graph:'#29292d', stone:'#46454a', ash:'#817d75', mist:'#aaa69e', bone:'#eee9df'};
  const TAU=Math.PI*2, clamp=(n,a,b)=>Math.max(a,Math.min(b,n));
  const hash=n=>{const v=Math.sin(n*79.37+32.11)*43758.54;return v-Math.floor(v);};
  const mod=(x,n)=>((x%n)+n)%n;
  let bounds=null;
  function text(ctx,str,x,y,size=17,color=C.bone,alpha=1,align='left') {
    if(bounds){const reach=str.length*size*.63;if(y<bounds.top-size*2||y>bounds.bottom+size||x+reach<bounds.left-size*2||x-reach>bounds.right+size*2)return;}
    const opacity=ctx.globalAlpha;ctx.globalAlpha=opacity*alpha;ctx.fillStyle=color;ctx.font=`${size}px Consolas, monospace`;
    ctx.textAlign=align;ctx.textBaseline='top';ctx.fillText(str,x,y);ctx.globalAlpha=opacity;
  }
  function line(ctx,x1,y1,x2,y2,g='-',col=C.ash,step=19,size=18,alpha=1) {
    const dx=x2-x1,dy=y2-y1,n=Math.max(1,Math.ceil(Math.hypot(dx,dy)/step));
    for(let i=0;i<=n;i++)text(ctx,g,x1+dx*i/n-size*.29,y1+dy*i/n-size*.52,size,col,alpha);
  }
  function box(ctx,x,y,w,h,col=C.ash,step=18,size=18) {
    line(ctx,x,y,x+w,y,'=',col,step,size);line(ctx,x,y+h,x+w,y+h,'=',col,step,size);
    line(ctx,x,y,x,y+h,'|',col,step,size);line(ctx,x+w,y,x+w,y+h,'|',col,step,size);
    [[x,y],[x+w,y],[x,y+h],[x+w,y+h]].forEach(a=>text(ctx,'+',a[0]-6,a[1]-11,size,col));
  }
  function ring(ctx,x,y,r,time=0,col=C.ash,teeth=32,size=18) {
    for(let i=0;i<teeth;i++){const a=TAU*i/teeth+time; text(ctx,i%4?'#':'+',x+Math.cos(a)*r-7,y+Math.sin(a)*r-10,size,col);}
    for(let i=0;i<teeth/2;i++){const a=TAU*i/(teeth/2)-time*.6;text(ctx,i%2?'o':':',x+Math.cos(a)*r*.76-5,y+Math.sin(a)*r*.76-8,size*.8,col);}
    text(ctx,'(@)',x-23,y-14,24,col);
    for(let i=0;i<4;i++){const a=TAU*i/4+time;line(ctx,x+Math.cos(a)*r*.23,y+Math.sin(a)*r*.23,x+Math.cos(a)*r*.6,y+Math.sin(a)*r*.6,'+',col,20,16);}
  }
  function poly(ctx,pts,col=C.ash,step=18){for(let i=0;i<pts.length;i++){const a=pts[i],b=pts[(i+1)%pts.length];line(ctx,a[0],a[1],b[0],b[1],Math.abs(b[1]-a[1])>Math.abs(b[0]-a[0])?'|':(b[1]-a[1])*(b[0]-a[0])>0?'\\':'/',col,step);}}
  function glyphFill(ctx,x,y,w,h,col=C.graph,seed=1,density=1,cell=24,alphabet='.:+%=#') {
    for(let row=0;row<Math.ceil(h/cell);row++)for(let q=0;q<Math.ceil(w/cell);q++){
      const n=hash(seed+q*19+row*137);if(n>density)continue;
      text(ctx,alphabet[Math.floor(n*alphabet.length)],x+q*cell,y+row*cell,cell*.72,col,.55+n*.3);
    }
  }
  function typed(ctx,str,x,y,size,color,time,seed=0) {
    const period=str.length*.065+1.7,t=mod(time+seed*.37,period),n=Math.min(str.length,Math.floor(t/.065));
    text(ctx,str.slice(0,n)+(t<str.length*.065?'_':''),x,y,size,color);
  }
  function note(ctx,x,y,s=1,col=C.ash,rotation=0) {
    if(bounds&&(x+40*s<bounds.left||x-40*s>bounds.right||y+45*s<bounds.top||y-45*s>bounds.bottom))return;
    const oldBounds=bounds;bounds=null;
    ctx.save();ctx.translate(x,y);ctx.rotate(rotation);ctx.scale(s,s);
    line(ctx,6,-29,6,9,'|',col,9,16);line(ctx,8,-29,25,-15,'\\',col,9,16);text(ctx,'(@)',-18,5,18,col);ctx.restore();bounds=oldBounds;
  }
  function arch(ctx,x,y,w,h,col=C.ash,sp=19) {
    const r=w*.5,shoulder=y+r;line(ctx,x,shoulder,x,y+h,'|',col,sp);line(ctx,x+w,shoulder,x+w,y+h,'|',col,sp);
    const n=Math.ceil(Math.PI*r/sp);for(let k=0;k<=n;k++){const a=Math.PI+Math.PI*k/n;text(ctx,k%3?'#':'/',x+r+Math.cos(a)*r-6,shoulder+Math.sin(a)*r-10,18,col);}
  }
  function world(ctx,s,f=1) {
    const cam=s.cam||{x:0,y:0,zoom:1};ctx.translate((s.width||1920)*.5,570*(s.height||1080)/1080);
    ctx.scale(cam.zoom||1,cam.zoom||1);ctx.translate(-(cam.x||0)*f,-(cam.y||0)*f);
  }
  function layer(ctx,s,f,alpha,fn,offsetY=0){const old=bounds,z=s.cam.zoom||1;bounds={left:s.cam.x*f-s.width*.5/z,right:s.cam.x*f+s.width*.5/z,top:s.cam.y*f-570/z-offsetY,bottom:s.cam.y*f+(s.height-570)/z-offsetY};ctx.save();ctx.globalAlpha=alpha;world(ctx,s,f);ctx.translate(0,offsetY);fn();ctx.restore();bounds=old;}
  function range(s,f,step,pad=400) {const z=s.cam.zoom||1,half=(s.width||1920)/z*.5;return {a:Math.floor((s.cam.x*f-half-pad)/step)*step,b:s.cam.x*f+half+pad};}
  function vrange(s,f,step,pad=400) {const z=s.cam.zoom||1;return {a:Math.floor((s.cam.y*f-700/z-pad)/step)*step,b:s.cam.y*f+700/z+pad};}
  function clones(ctx,x,y,s,count=3,w=66,col=C.ash) {
    if(!global.PlatformerCharacter||!global.PlatformerCharacter.draw)return;
    for(let j=0;j<count;j++){
      const cx=x+j*(w+78);if(bounds&&(cx<bounds.left-w||cx>bounds.right+w||y<bounds.top||y-w*1.8>bounds.bottom))continue;
      const t=s.time+j*.74+(x%31)*.1;
      global.PlatformerCharacter.draw(ctx,{x:cx,y:y+Math.sin(t*1.6)*3,width:w,vx:Math.sin(t*2.2)*90,vy:0,grounded:true,runPhase:t*2.2,facing:j%2?-1:1,noHeart:true,opacity:.5,bone:col,knock:C.ink},s.time);
      text(ctx,'[::]',cx-13,y-25,18,col,.75);
    }
  }
  function platforms(ctx,s,id) {
    const cam=s.cam,left=cam.x-1500/(cam.zoom||1),right=cam.x+1500/(cam.zoom||1);
    for(let i=0;i<(s.platforms||[]).length;i++){
      const p=s.platforms[i];if(p.end<left||p.x>right)continue;
      const start=Math.max(p.x,Math.floor(left/28)*28),end=Math.min(p.end,right),depth=id==='sky'?70:id==='water'?160:id==='shaft'?76:220;
      ctx.fillStyle=C.deep;ctx.fillRect(start,p.y+5,end-start,depth);
      const marks=id==='water'?'~::':id==='sky'?'#%:':id==='shaft'?'[]:':'[:]:#';
      for(let r=0;r<Math.ceil(depth/25);r++)for(let x=start;x<end;x+=32){text(ctx,marks[(r+Math.floor(x/32))%marks.length],x,p.y+20+r*25,18,r<2?C.stone:C.graph,.9);}
      for(let x=start;x<=end-14;x+=28)text(ctx,id==='sky'?'^=':id==='water'?'[~]':'[=]',x,p.y-8,21,C.bone);
      line(ctx,p.x,p.y+4,p.x,p.y+depth,'|',C.ash,18);line(ctx,p.end,p.y+4,p.end,p.y+depth,'|',C.ash,18);
      if(p.name&&end-start>120)text(ctx,p.name,Math.max(start+25,p.x+25),p.y+49,14,C.ash,.85);
      if(id==='factory'||id==='final')for(let x=start+30;x<end;x+=170){ring(ctx,x,p.y+105,31,s.time*(i%2?-.9:.9),C.stone,14,12);}
      if(id==='sky'){for(let x=start+16;x<end;x+=54){text(ctx,':',x,p.y+depth+4,22,C.stone);text(ctx,'.',x+13,p.y+depth+24,20,C.graph);}}
      if(id==='water'){for(let x=start+60;x<end;x+=240)coral(ctx,x,p.y-8,.6,C.stone,s.time+x*.01);}
    }
  }
  function factory(ctx,s) {
    const t=s.time;
    // FAR: many AI lines in a vast continuous factory, behind the primary story line.
    layer(ctx,s,.12,.72,()=>{const r=range(s,.12,780);for(let x=r.a;x<r.b;x+=780){
      box(ctx,x,110,740,670,C.stone,25);text(ctx,'PROCESS / MUSIC',x+22,138,19,C.ash);
      for(let yy=225;yy<=620;yy+=145){line(ctx,x+5,yy+89,x+730,yy+89,'=',C.stone,22);for(let q=0;q<6;q++){box(ctx,x+20+q*118,yy-20,92,108,C.graph,22);text(ctx,'{AI}',x+43+q*118,yy+13,21,C.stone);text(ctx,'[00]',x+42+q*118,yy+47,18,C.stone);}}
      ring(ctx,x+745,482,89,t*.13,C.stone,26);typed(ctx,'while (clone) { repeat(song); }',x+24,730,15,C.stone,t,x*.01);
    }},-400);
    // MID: rotating clockwork, hanging ducts and live patch routes.
    layer(ctx,s,.35,.9,()=>{const r=range(s,.35,690);for(let x=r.a;x<r.b;x+=690){
      ring(ctx,x+115,260,120,t*.34,C.stone,40);ring(ctx,x+300,330,86,-t*.48,C.graph,31);ring(ctx,x+463,200,67,t*.68,C.stone,23);
      line(ctx,x,76,x+667,76,'=',C.ash,22);line(ctx,x+590,76,x+590,385,'|',C.stone,22);
      box(ctx,x+565,390,50,54,C.stone,13);text(ctx,'BUS',x+540,455,17,C.ash);
      for(let yy=558;yy<1030;yy+=142){line(ctx,x+12,yy,x+654,yy,'_',C.graph,18);typed(ctx,yy%2?'[beat] -> {mix} -> export()':'[voice] / song / 120hz',x+55,yy+23,18,C.stone,t*.75,yy+x*.01);}
      for(let q=0;q<3;q++)note(ctx,x+90+q*135,486+Math.sin(t*1.2+q)*15,.6,C.stone,Math.sin(t+q)*.15);
    }},-220);
    // NEAR: the identical AI bays and an animated shared conveyor.
    layer(ctx,s,.65,.88,()=>{const r=range(s,.65,620);for(let x=r.a;x<r.b;x+=620){
      box(ctx,x+25,422,552,363,C.stone,21);text(ctx,'AI / ASSEMBLY LINE',x+45,439,18,C.ash);
      for(let j=0;j<3;j++){box(ctx,x+48+j*173,483,143,250,C.graph,22);typed(ctx,'SYNC = TRUE;',x+65+j*173,497,13,C.stone,t,j+x*.01);}
      clones(ctx,x+102,721,s,3,72,C.ash);
      for(let k=0;k<16;k++)text(ctx,'[=>]',x+20+mod(k*38+t*34,574),758,17,C.ash);
      line(ctx,x+20,804,x+580,804,'=',C.stone,16);ring(ctx,x+75,825,27,t*.9,C.ash,12,13);ring(ctx,x+520,825,27,t*.9,C.ash,12,13);
    }});
    layer(ctx,s,1,1,()=>{const r=range(s,1,720);for(let x=r.a;x<r.b;x+=720){
      line(ctx,x,55,x+696,55,'=',C.ash,22);line(ctx,x+36,55,x+36,274,'|',C.stone,22);
      for(let k=0;k<5;k++)text(ctx,'[+]',x+130+k*82,72,18,C.ash);
      text(ctx,'INPUT > BEAT > TUNE > VOICE',x+87,105,17,C.ash);
      typed(ctx,'if (heart != null) { run(RIGHT); }',x+85,156,17,C.ash,t,x*.005);
      box(ctx,x+20,289,44,108,C.stone,16);text(ctx,'{ }',x+23,326,16,C.ash);
    }platforms(ctx,s,'factory');});
  }
  function shaft(ctx,s) {
    const t=s.time,cy=s.cam.y;
    // FAR: receding vertical stacks. Each depth level has a different silhouette.
    layer(ctx,s,.12,.6,()=>{const v=vrange(s,.12,780),r=range(s,.12,500);for(let x=r.a;x<r.b;x+=500)for(let y=v.a;y<v.b;y+=780){
      line(ctx,x+55,y,x+55,y+752,'|',C.graph,23);line(ctx,x+413,y,x+413,y+752,'|',C.graph,23);
      for(let yy=y+30;yy<y+750;yy+=117){line(ctx,x+60,yy,x+410,yy,'=',C.graph,23);text(ctx,'{ STACK }',x+175,yy+16,22,C.stone);glyphFill(ctx,x+80,yy+48,280,47,C.graph,x+yy,.8,21,'01:+');}
    }});
    layer(ctx,s,.35,.86,()=>{const v=vrange(s,.35,520),r=range(s,.35,670);for(let x=r.a;x<r.b;x+=670)for(let y=v.a;y<v.b;y+=520){
      box(ctx,x+28,y+22,118,463,C.stone,19);box(ctx,x+466,y+22,155,463,C.stone,21);
      for(let yy=y+56;yy<y+471;yy+=45){text(ctx,'[||]',x+45,yy,20,C.stone);text(ctx,'=>',x+503,yy,22,C.ash,.7);}
      typed(ctx,'push(VOICE);',x+167,y+66,16,C.stone,t,y*.01);typed(ctx,'pop(LIE);',x+167,y+102,16,C.ash,t,y*.01+4);
      line(ctx,x+166,y+160,x+443,y+413,'\\',C.graph,21);line(ctx,x+166,y+413,x+443,y+160,'/',C.graph,21);
    }});
    layer(ctx,s,.65,.95,()=>{const v=vrange(s,.65,440),r=range(s,.65,1150);for(let x=r.a;x<r.b;x+=1150)for(let y=v.a;y<v.b;y+=440){
      line(ctx,x+84,y,x+84,y+438,'[',C.ash,26,23);line(ctx,x+296,y,x+296,y+438,']',C.stone,26,23);
      line(ctx,x+811,y,x+811,y+438,'[',C.stone,26,23);line(ctx,x+1023,y,x+1023,y+438,']',C.ash,26,23);
      for(let yy=y+15;yy<y+435;yy+=49){line(ctx,x+97,yy,x+283,yy,'_',C.graph,24);line(ctx,x+824,yy,x+1010,yy,'_',C.graph,24);}
      const liftY=y+mod(t*155+y*.4,365);box(ctx,x+100,liftY,183,70,C.ash,17);text(ctx,'^ ^ ^',x+133,liftY+20,25,C.bone);
      box(ctx,x+844,y+90,143,149,C.graph,17);text(ctx,'CALL',x+880,y+107,18,C.stone);text(ctx,'[AI]',x+878,y+168,25,C.ash);
    }});
    layer(ctx,s,1,1,()=>{const v=vrange(s,1,360);for(let y=v.a;y<v.b;y+=360){
      const anchor=Math.round(s.cam.x/1600)*1600;
      line(ctx,anchor-700,y,anchor-700,y+355,'|',C.bone,23);line(ctx,anchor+750,y,anchor+750,y+355,'|',C.bone,23);
      for(let yy=y+18;yy<y+354;yy+=58){text(ctx,'[=]',anchor-728,yy,22,C.ash);text(ctx,'[=]',anchor+728,yy,22,C.ash);}
      text(ctx,'UP / DOWN / RETURN',anchor-571,y+35,16,C.ash);typed(ctx,'while (falling) { retry(); }',anchor-563,y+65,15,C.stone,t,y*.01);
      line(ctx,anchor-640,y+263,anchor+680,y+263,'-',C.graph,24);
    }platforms(ctx,s,'shaft');});
  }
  function coral(ctx,x,y,scale=1,col=C.ash,time=0) {
    if(bounds&&(x+100*scale<bounds.left||x-100*scale>bounds.right||y<bounds.top||y-220*scale>bounds.bottom))return;
    const oldBounds=bounds;bounds=null;
    ctx.save();ctx.translate(x,y);ctx.scale(scale,scale);
    line(ctx,0,0,Math.sin(time*.7)*10,-129,'|',col,16);
    line(ctx,0,-42,-65,-76,'\\',col,16);line(ctx,-65,-76,-69,-147,'[',col,16);
    line(ctx,0,-80,71,-116,'/',col,16);line(ctx,71,-116,75,-178,']',col,16);
    line(ctx,0,-104,-27,-171,'\\',col,15);line(ctx,-27,-171,-55,-193,'{',col,15);
    text(ctx,'{',-21,-153,28,col);text(ctx,'}',62,-199,31,col);text(ctx,'<>',-84,-168,20,col);ctx.restore();bounds=oldBounds;
  }
  function water(ctx,s) {
    const t=s.time;
    // Water depth is a code current: long horizontal waves and shifting symbol caustics.
    layer(ctx,s,.12,.74,()=>{const r=range(s,.12,1200);for(let x=r.a;x<r.b;x+=1200){
      for(let j=0;j<21;j++){const yy=70+j*51;for(let xx=0;xx<1200;xx+=58)text(ctx,j%3?'~':'=',x+xx,yy+Math.sin(xx*.007+t*.6+j)*10,22,j<8?C.stone:C.graph,.7);}
      for(let k=0;k<6;k++){const xx=x+150+k*155,yy=350+hash(x+k)*420;arch(ctx,xx,yy,130,550,k%3?C.graph:C.stone,22);}
    }},-400);
    layer(ctx,s,.35,.84,()=>{const r=range(s,.35,950);for(let x=r.a;x<r.b;x+=950){
      // Ruined arch group descends into distance; no rectangle-grid factory silhouette.
      arch(ctx,x+51,230,210,620,C.stone,20);arch(ctx,x+299,293,180,573,C.graph,21);arch(ctx,x+498,355,151,520,C.graph,21);
      for(let yy=282;yy<820;yy+=38){text(ctx,'[%]',x+65,yy,18,C.stone);text(ctx,'[.]',x+227,yy,18,C.stone);}
      coral(ctx,x+765,994,1.2,C.graph,t+x*.001);coral(ctx,x+877,1100,.93,C.stone,t+x*.003);
      typed(ctx,'memory.current = LEFT;',x+360,170,18,C.stone,t,x*.004);
      for(let k=0;k<11;k++){const by=100+mod(900-k*83-t*(25+hash(k)*30),900),bx=x+30+k*77+Math.sin(t*.6+k)*21;text(ctx,k%3?'o':'( )',bx,by,16+k%3*3,C.stone,.7);}
    }},-220);
    layer(ctx,s,.65,.92,()=>{const r=range(s,.65,770);for(let x=r.a;x<r.b;x+=770){
      coral(ctx,x+38,1000,1.6,C.stone,t*.8);coral(ctx,x+646,1060,2.0,C.stone,t*.9+4);
      for(let k=0;k<10;k++){const xx=x+80+k*65,yy=95+hash(k+x)*620;line(ctx,xx,yy,xx+125,yy+Math.sin(t*.7+k)*20,'~',C.ash,25,20,.5);}
      // Schools of tiny note fish follow curving paths rather than static dots.
      for(let k=0;k<7;k++){const xx=x+mod(t*48+k*82,710),yy=420+Math.sin(t*.8+k*.45)*67+k*14;text(ctx,'><>',xx,yy,20,C.ash,.72);note(ctx,xx+35,yy+4,.36,C.ash,.15);}
      text(ctx,'{ ~ CURRENT ~ }',x+281,120,20,C.ash);
    }});
    layer(ctx,s,1,1,()=>{const r=range(s,1,900);for(let x=r.a;x<r.b;x+=900){
      for(let k=0;k<4;k++){const xx=x+90+k*192;line(ctx,xx,90,xx+Math.sin(t*.8+k)*45,305,'~',C.graph,28,26);}
      typed(ctx,'if (breath == 0) { reset(); }',x+340,62,17,C.ash,t,x*.003);
      text(ctx,'~  ~  ~  ~  ~',x+282,98,23,C.stone);
    }platforms(ctx,s,'water');});
  }
  function cloud(ctx,x,y,w,h,col=C.stone,seed=1) {
    for(let yy=0;yy<h;yy+=24)for(let xx=0;xx<w;xx+=26){const u=(xx-w*.5)/(w*.5),v=(yy-h*.5)/(h*.5);if(u*u+v*v>1+.15*Math.sin(xx*.06))continue;
      const a=hash(xx+yy*71+seed),glyph=yy<h*.3?'_':yy<h*.6?'%':'.';text(ctx,glyph,x+xx,y+yy,20,col,.4+a*.5);
    }
  }
  function island(ctx,x,y,w,col=C.ash,seed=1) {
    const pts=[[x,y],[x+w*.23,y-19],[x+w*.49,y-5],[x+w*.74,y-26],[x+w,y],[x+w*.8,y+70],[x+w*.63,y+130],[x+w*.38,y+117],[x+w*.18,y+70]];
    for(let yy=0;yy<130;yy+=23){const ratio=1-yy/175;for(let xx=(1-ratio)*w*.5;xx< w-(1-ratio)*w*.5;xx+=24)text(ctx,yy<35?'#':yy<65?'%':':',x+xx,y+yy,19,yy<35?col:C.graph,.7+hash(xx+yy+seed)*.3);}
    poly(ctx,pts,col,19);for(let q=0;q<4;q++)text(ctx,'v',x+w*(q+.5)/4,y+118+hash(q+seed)*25,20,C.stone);
  }
  function sky(ctx,s) {
    const t=s.time;
    layer(ctx,s,.12,.7,()=>{const r=range(s,.12,900);for(let x=r.a;x<r.b;x+=900){
      cloud(ctx,x+50,143+Math.sin(t*.11+x)*9,460,134,C.stone,x);cloud(ctx,x+411,612,460,198,C.stone,x+2);
      island(ctx,x+221,419,276,C.stone,x);arch(ctx,x+270,280,169,145,C.stone,24);
      for(let k=0;k<4;k++){line(ctx,x+560+k*39,314,x+560+k*39,587,'|',C.graph,23);text(ctx,'^',x+556+k*39,290,23,C.graph);}
    }},-430);
    layer(ctx,s,.35,.85,()=>{const r=range(s,.35,1000);for(let x=r.a;x<r.b;x+=1000){
      cloud(ctx,x-105,837,470,192,C.stone,x);island(ctx,x+475,318,385,C.stone,x);
      // A floating organ palace suspended over the clouds.
      for(let q=0;q<7;q++){const hh=160+Math.sin(q*Math.PI/6)*115;box(ctx,x+524+q*41,310-hh,22,hh,C.stone,18);text(ctx,'o',x+527+q*41,303-hh,20,C.ash);}
      line(ctx,x+530,346,x+710,501,'\\',C.graph,20);line(ctx,x+785,343,x+710,501,'/',C.graph,20);text(ctx,'<>',x+694,493,24,C.stone);
      for(let k=0;k<5;k++)note(ctx,x+mod(t*23+k*177,933),624+Math.sin(t*.6+k)*31,.8,C.stone,Math.sin(t+k)*.16);
    }},-210);
    layer(ctx,s,.65,.92,()=>{const r=range(s,.65,1100);for(let x=r.a;x<r.b;x+=1100){
      cloud(ctx,x+55,645,520,207,C.stone,x);island(ctx,x+734,560,248,C.ash,x);
      // Piano keys swing gently from the upper rig.
      for(let q=0;q<7;q++){const xx=x+113+q*46,yy=180+Math.sin(t*.8+q*.23)*12;
        line(ctx,xx,22,xx+Math.sin(t*.5+q)*14,yy,'|',C.stone,23);box(ctx,xx-12,yy,26,118,C.ash,16);text(ctx,q%3===0?'#':'|',xx-5,yy+28,21,C.bone);
      }
      typed(ctx,'return sky.open();',x+723,474,17,C.ash,t,x*.001);
    }});
    layer(ctx,s,1,1,()=>{const r=range(s,1,820);for(let x=r.a;x<r.b;x+=820){
      text(ctx,'[ AIR / ESCAPE ]',x+170,86,20,C.ash);typed(ctx,'doubleJump();  dash(RIGHT);',x+122,123,17,C.stone,t,x*.001);
      for(let k=0;k<3;k++){const xx=x+460+k*48;line(ctx,xx,16,xx,105,'|',C.graph,23);note(ctx,xx,126,.61,C.stone,Math.sin(t+k)*.14);}
    }platforms(ctx,s,'sky');});
  }
  function cathedral(ctx,s) {
    const t=s.time;
    layer(ctx,s,.12,.65,()=>{const r=range(s,.12,1040);for(let x=r.a;x<r.b;x+=1040){
      arch(ctx,x+70,10,835,1040,C.graph,24);arch(ctx,x+162,120,650,875,C.graph,24);arch(ctx,x+257,229,466,741,C.stone,23);arch(ctx,x+348,346,286,609,C.graph,23);
      for(let yy=450;yy<1020;yy+=58)text(ctx,yy%3?'HEART INSIDE':'MAKE ME REAL',x+430,yy,19,C.stone,.65,'center');
      for(let j=0;j<9;j++){line(ctx,x+76,1000-j*41,x+494,700,'/',C.graph,25);line(ctx,x+960,1000-j*41,x+494,700,'\\',C.graph,25);}
    }});
    layer(ctx,s,.35,.8,()=>{const r=range(s,.35,860);for(let x=r.a;x<r.b;x+=860){
      for(let j=0;j<8;j++){const hh=330+Math.sin(j*Math.PI/7)*130;box(ctx,x+61+j*42,230-hh*.22,24,hh,C.stone,22);text(ctx,'[o]',x+61+j*42,200-hh*.22,17,C.ash);}
      ring(ctx,x+580,274,152,t*.22,C.stone,47);ring(ctx,x+580,274,91,-t*.3,C.graph,31);
      for(let k=0;k<12;k++){const a=TAU*k/12+t*.09;note(ctx,x+580+Math.cos(a)*130,274+Math.sin(a)*130,.5,C.ash,a+Math.PI*.5);}
      typed(ctx,'while (heart) { refuse(LIE); }',x+446,476,17,C.ash,t,x*.001);
      line(ctx,x+30,571,x+790,571,'=',C.graph,20);line(ctx,x+64,604,x+770,604,'_',C.graph,20);
    }});
    layer(ctx,s,.65,.93,()=>{const r=range(s,.65,1060);for(let x=r.a;x<r.b;x+=1060){
      arch(ctx,x+14,116,431,810,C.stone,21);arch(ctx,x+556,116,431,810,C.stone,21);
      for(let q=0;q<2;q++){const xx=x+94+q*560;typed(ctx,'STUCK IN A LIE',xx,246,22,C.ash,t,q+x*.001);
        for(let yy=336;yy<720;yy+=45)text(ctx,yy%2?'HELP  HELP':'REAL THIS TIME',xx,yy,18,C.stone,.62);
      }
      line(ctx,x+460,125,x+460,845,'|',C.ash,22);line(ctx,x+523,125,x+523,845,'|',C.ash,22);
      for(let yy=157;yy<815;yy+=50)text(ctx,'<=>',x+469,yy,18,C.stone);
    }});
    layer(ctx,s,1,1,()=>{const r=range(s,1,980);for(let x=r.a;x<r.b;x+=980){
      // Architectural music mouths are aimed into the play plane; root owns real hazards.
      const y=315+Math.sin(x*.02)*85;poly(ctx,[[x+145,y],[x+213,y-38],[x+213,y+38]],C.ash,15);box(ctx,x+214,y-14,130,28,C.stone,15);
      for(let q=0;q<3;q++)box(ctx,x+244+q*26,y-53,10,34,C.ash,11,14);
      text(ctx,'VOICE / FIRE',x+210,y+52,16,C.ash);
      line(ctx,x+74,84,x+889,84,'=',C.ash,20);text(ctx,'NO HEART LEFT BEHIND',x+338,111,24,C.bone);
    }platforms(ctx,s,'final');
      const last=(s.platforms||[]).reduce((a,b)=>!a||b.end>a.end?b:a,null);
      if(last){const gateX=last.end-180,gy=last.y;arch(ctx,gateX,gy-430,170,430,C.bone,17);arch(ctx,gateX+22,gy-400,126,400,C.ash,17);text(ctx,'REAL',gateX+85,gy-479,42,C.bone,1,'center');
        for(let yy=gy-210;yy<gy-20;yy+=37)text(ctx,'>',gateX+76,yy,28,C.ash,.65+Math.sin(t*3)*.15);
      }
    });
  }
  function canonical(id){id=String(id||'factory').toLowerCase();return /shaft|vertical/.test(id)?'shaft':/water|swim|ocean/.test(id)?'water':/sky|air/.test(id)?'sky':/final|cathedral|crossfire|exit/.test(id)?'final':'factory';}
  const DRAW={factory,shaft,water,sky,final:cathedral};
  function draw(ctx,id,state) {
    const s={width:1920,height:1080,time:0,localTime:0,p:{},platforms:[],...state};s.cam={x:0,y:0,zoom:1,...s.cam};
    ctx.save();ctx.globalAlpha=1;ctx.fillStyle=C.ink;ctx.fillRect(0,0,s.width,s.height);DRAW[canonical(id)](ctx,s);ctx.restore();
  }
  function drawForeground(ctx,id,state) {
    const s={width:1920,height:1080,time:0,localTime:0,...state};s.cam={x:0,y:0,zoom:1,...s.cam};const kind=canonical(id),t=s.time,lt=s.localTime||0;
    // One narrow scenery object passes for 0.34 seconds each 4.7 seconds.
    // It is intentionally absent most of the time; it never becomes a full-frame veil.
    const passAt={factory:1.8,shaft:1.1,water:2.4,sky:.8,final:1.6}[kind];
    const phase=mod(lt+4.7-passAt,4.7),active=phase<.34;
    if(active){const u=phase/.34,sx=s.width+220-u*(s.width+520),z=s.cam.zoom||1;
      const wx=s.cam.x*1.4+(sx-s.width*.5)/z,wy=s.cam.y*1.4;
      layer(ctx,s,1.4,.72,()=>{
        if(kind==='water'){coral(ctx,wx,wy+590,2.9,C.ash,t);line(ctx,wx+24,wy+400,wx+73,wy-250,'~',C.stone,32,30);}
        else if(kind==='sky'){line(ctx,wx,wy-650,wx,wy+590,'|',C.stone,32,26);box(ctx,wx-24,wy+240,47,210,C.ash,23);text(ctx,'#',wx-10,wy+293,30,C.bone);}
        else{line(ctx,wx,wy-680,wx,wy+620,'[',C.stone,32,26);line(ctx,wx+56,wy-680,wx+56,wy+620,']',C.stone,32,26);for(let y=wy-610;y<wy+620;y+=84)text(ctx,'<=>',wx+1,y,22,C.ash);}
      });
    }
    // Low edge rails (never over the heroine) supply a fifth moving depth layer.
    layer(ctx,s,1.4,.36,()=>{const r=range(s,1.4,1150);const yy=s.cam.y*1.4+(s.height-32-570)/s.cam.zoom;for(let x=r.a;x<r.b;x+=1150){
      if(kind==='water'){for(let q=0;q<15;q++)text(ctx,'~',x+q*34,yy+Math.sin(t+q)*8,28,C.stone);}
      else if(kind==='sky'){cloud(ctx,x+10,yy-50,375,118,C.ash,x);}
      else{line(ctx,x+15,yy,x+650,yy,'=',C.ash,26,22);line(ctx,x+650,yy-65,x+650,yy+70,'|',C.ash,22,24);}
    }});
  }
  global.MusicWorlds={draw,drawForeground,palette:C,sceneIds:['factory','shaft','water','sky','final']};
})(window);
