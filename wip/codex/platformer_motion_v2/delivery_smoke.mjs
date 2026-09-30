import {createRequire} from 'node:module';
import fs from 'node:fs';
const require=createRequire(import.meta.url);
const {chromium}=require('C:/Users/honkw/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright-core');
const browser=await chromium.launch({executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe',headless:true});
try{
 const page=await browser.newPage();const errors=[];page.on('pageerror',e=>errors.push(String(e)));
 await page.goto('http://127.0.0.1:5189/playable/?render=1');await page.waitForFunction(()=>demo.ready);
 const result=await page.evaluate(()=>{
  demo.reset('manual',0);demo.renderAt(1.6);
  return{scene:demo.state().scene,mode:demo.state().mode,deaths:demo.events().filter(e=>e.kind==='death').length,respawns:demo.events().filter(e=>e.kind==='respawn').length,musicUrl:document.getElementById('music').src,ready:demo.ready};
 });
 const response=await page.request.get(result.musicUrl);result.audioHttp=response.status();result.errors=errors;
 if(!result.ready||result.audioHttp!==200||errors.length||result.deaths<1||result.respawns<1)throw Error(JSON.stringify(result));
 fs.writeFileSync('delivery_smoke.json',JSON.stringify(result,null,2));console.log(JSON.stringify(result));
}finally{await browser.close();}
