import fs from 'node:fs';
import fsp from 'node:fs/promises';
import path from 'node:path';
import http from 'node:http';
import {spawn} from 'node:child_process';
import {createRequire} from 'node:module';
import {fileURLToPath} from 'node:url';
const require=createRequire(import.meta.url);
const {chromium}=require('C:/Users/honkw/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright-core');
const root=path.dirname(fileURLToPath(import.meta.url)),mode=process.argv[2]||'audit';
const output=path.join(root,process.argv[3]||(mode==='slow'?'platformer_hair_slow_v1.mp4':'platformer_motion_v2.mp4'));
const audio=path.resolve(root,'../../..','audio/final/song.mp3');
let encoder=null,stderr='',frameCount=0;
const server=http.createServer(async(req,res)=>{
 try {
  const url=new URL(req.url,'http://localhost');
  if(url.pathname==='/frame'&&req.method==='POST'){
   const chunks=[];for await(const chunk of req)chunks.push(chunk);
   const buf=Buffer.concat(chunks);
   if(buf.length!==1920*1080*4)throw new Error(`Wrong RGBA size ${buf.length}`);
   await new Promise((resolve,reject)=>encoder.stdin.write(buf,e=>e?reject(e):resolve()));
   frameCount++;res.end('ok');return;
  }
  if(url.pathname==='/progress'){console.log(`Rendered ${frameCount}/1200 frames`);res.end('ok');return;}
  const clean=decodeURIComponent(url.pathname==='/'?'/index.html':url.pathname);
  const target=path.resolve(root,'.'+clean);if(!target.startsWith(root+path.sep))throw new Error('Path outside renderer root');
  const data=await fsp.readFile(target);res.setHeader('Content-Type',target.endsWith('.js')?'text/javascript':target.endsWith('.html')?'text/html':'application/octet-stream');res.end(data);
 }catch(e){res.statusCode=500;res.end(String(e));}
});
await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
const browser=await chromium.launch({executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe',headless:true,args:['--disable-lcd-text','--disable-background-timer-throttling','--disable-renderer-backgrounding','--disable-backgrounding-occluded-windows']});
const page=await browser.newPage({viewport:{width:1920,height:1080},deviceScaleFactor:1});
page.on('pageerror',e=>console.error('PAGE ERROR',String(e)));
try{
 await page.goto(`http://127.0.0.1:${server.address().port}/?render=1`);
 await page.evaluate(()=>document.fonts.ready);await page.waitForFunction(()=>window.demo?.ready);
 const audit=await page.evaluate(()=>{demo.reset('auto');for(let f=0;f<=1200;f++)demo.renderAt(f/60);return{events:demo.events(),state:demo.state(),physicsHz:demo.physicsHz};});
 await fsp.writeFile(path.join(root,'motion_audit.json'),JSON.stringify(audit,null,2));
 console.log(JSON.stringify({deaths:audit.events.filter(e=>e.kind==='death'),respawns:audit.events.filter(e=>e.kind==='respawn'),dodges:audit.events.filter(e=>e.kind==='dodge'),exits:audit.events.filter(e=>e.kind==='exit'),endX:audit.state.p.x}));
 const previews=path.join(root,'qa');await fsp.mkdir(previews,{recursive:true});
 await page.evaluate(()=>demo.reset('auto'));
 for(const t of [0.8,2.4,3.5,5.5,7.5,9.5,11.5,13.5,15.5,17.5,19.5]){
  const result=await page.evaluate(t=>{const state=demo.renderAt(t);return{state,png:document.getElementById('screen').toDataURL('image/png').split(',')[1]};},t);
  await fsp.writeFile(path.join(previews,`frame_${t.toFixed(1)}.png`),Buffer.from(result.png,'base64'));
 }
 if(mode==='render'||mode==='slow'){
  if(fs.existsSync(output))throw new Error('Output already exists; use a new versioned name');
  const args=['-hide_banner','-loglevel','warning','-f','rawvideo','-pix_fmt','rgba','-s','1920x1080','-r','60','-i','pipe:0'];
  if(mode==='render')args.push('-ss','42.012','-t','20','-i',audio,'-map','0:v:0','-map','1:a:0');
  const filter=(mode==='slow'?'crop=1080:608:120:470,scale=1920:1080:flags=lanczos,':'')+'scale=out_color_matrix=bt709,setparams=color_primaries=bt709:color_trc=bt709';
  args.push('-vf',filter,'-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p');
  if(mode==='render')args.push('-c:a','aac','-b:a','320k','-t','20');else args.push('-an');
  args.push('-movflags','+faststart',output);
  encoder=spawn('ffmpeg',args,{windowsHide:true,stdio:['pipe','ignore','pipe']});encoder.stderr.on('data',b=>stderr=(stderr+b).slice(-6000));
  const done=new Promise((resolve,reject)=>{encoder.on('error',reject);encoder.on('exit',code=>code===0?resolve():reject(new Error(`ffmpeg ${code}: ${stderr}`)));});
  await page.evaluate(async(slow)=>{
   demo.reset('auto');const canvas=document.getElementById('screen'),c=canvas.getContext('2d');
   const total=slow?240:1200;
   for(let frame=0;frame<total;frame++){
    demo.renderAt(slow?9.2+frame/120:frame/60);const rgba=c.getImageData(0,0,1920,1080).data;
    const response=await fetch('/frame',{method:'POST',body:rgba});if(!response.ok)throw new Error(await response.text());
    if(frame%180===179)await fetch('/progress');
   }
  },mode==='slow');
  encoder.stdin.end();await done;console.log(`VIDEO: ${output}`);
 }
}finally{await browser.close();await new Promise(resolve=>server.close(resolve));}
