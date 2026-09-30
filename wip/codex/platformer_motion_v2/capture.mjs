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
const output=path.join(root,process.argv[3]||'six_worlds_motion_v1.mp4');
const projectAudio=path.resolve(root,'../../..','audio/final/song.mp3');
const audio=fs.existsSync(projectAudio)?projectAudio:path.join(root,'preview_audio.mp3'),audioStart=fs.existsSync(projectAudio)?'42.012':'0';
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
 const audit=await page.evaluate(()=>{demo.reset('auto');const samples=[];for(let f=0;f<=1200;f++){demo.renderAt(f/60);if(f%6===0){const s=demo.state();samples.push({t:s.time,scene:s.scene,x:s.p.x,y:s.p.y,shots:s.shots.length,dead:s.p.dead});}}return{events:demo.events(),samples,state:demo.state(),physicsHz:demo.physicsHz,layers:demo.layerDepths,hazardsPerSecond:demo.hazardsPerSecond};});
 await fsp.writeFile(path.join(root,'motion_audit.json'),JSON.stringify(audit,null,2));
 const counts={};for(const e of audit.events)counts[e.kind]=(counts[e.kind]||0)+1;
 console.log(JSON.stringify({counts,deaths:audit.events.filter(e=>e.kind==='death'),shotsPeak:Math.max(...audit.samples.map(s=>s.shots)),layers:audit.layers}));
 const previews=path.join(root,'qa');await fsp.mkdir(previews,{recursive:true});
 await page.evaluate(()=>demo.reset('auto'));
 for(const t of [1.5,2.8,4.8,5.9,8.0,9.1,11.5,13.1,15.2,16.1,18.5,19.5]){
  const result=await page.evaluate(t=>{const state=demo.renderAt(t);return{state,png:document.getElementById('screen').toDataURL('image/png').split(',')[1]};},t);
  await fsp.writeFile(path.join(previews,`frame_${t.toFixed(1)}.png`),Buffer.from(result.png,'base64'));
 }
 if(mode==='render'){
  if(fs.existsSync(output))throw new Error('Output already exists; use a new versioned name');
  const args=['-hide_banner','-loglevel','warning','-f','rawvideo','-pix_fmt','rgba','-s','1920x1080','-r','60','-i','pipe:0'];
  args.push('-ss',audioStart,'-t','20','-i',audio,'-map','0:v:0','-map','1:a:0');
  const filter='scale=out_color_matrix=bt709,setparams=color_primaries=bt709:color_trc=bt709';
  args.push('-vf',filter,'-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p');
  args.push('-c:a','aac','-b:a','320k','-t','20');
  args.push('-movflags','+faststart',output);
  encoder=spawn('ffmpeg',args,{windowsHide:true,stdio:['pipe','ignore','pipe']});encoder.stderr.on('data',b=>stderr=(stderr+b).slice(-6000));
  const done=new Promise((resolve,reject)=>{encoder.on('error',reject);encoder.on('exit',code=>code===0?resolve():reject(new Error(`ffmpeg ${code}: ${stderr}`)));});
  await page.evaluate(async()=>{
   demo.reset('auto');const canvas=document.getElementById('screen'),c=canvas.getContext('2d');
   const total=1200;
   for(let frame=0;frame<total;frame++){
    demo.renderAt(frame/60);const rgba=c.getImageData(0,0,1920,1080).data;
    const response=await fetch('/frame',{method:'POST',body:rgba});if(!response.ok)throw new Error(await response.text());
    if(frame%180===179)await fetch('/progress');
   }
  });
  encoder.stdin.end();await done;console.log(`VIDEO: ${output}`);
 }
}finally{await browser.close();await new Promise(resolve=>server.close(resolve));}
