import { createRequire } from 'node:module';
import { writeFileSync, readFileSync } from 'node:fs';
import { pathToFileURL } from 'node:url';
import { createHash } from 'node:crypto';
import path from 'node:path';

const require = createRequire(import.meta.url);
const { chromium } = require('C:/Users/honkw/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright-core');
const root = "D:/Videos/Help! I'm stuck in a LIE/wip/codex/platformer_motion_v1";
const sourceHash = createHash('sha256').update(readFileSync(path.join(root, 'game.js'))).digest('hex');
const report = { sourceHash, viewport: [1920,1080], physicsHz:120, checks:[], errors:[], observations:[] };
const browser = await chromium.launch({ executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe', headless:true });
const page = await browser.newPage({viewport:{width:1920,height:1080},deviceScaleFactor:1});
page.on('pageerror', error => report.errors.push(error.message));
page.on('console', message => { if(message.type()==='error') report.errors.push(message.text()); });
const state = () => page.evaluate(() => window.demo.state());
const reset = () => page.evaluate(() => window.demo.reset('manual'));
const at = t => page.evaluate(t => window.demo.renderAt(t), t);
const check = (name, pass, evidence) => { report.checks.push({name,pass:!!pass,evidence}); };
try {
 const url=pathToFileURL(path.join(root,'index.html'));url.search='render=1';
 await page.goto(url.href);await page.waitForFunction(() => window.demo?.ready===true);await page.evaluate(() => document.fonts.ready);
 const controls = [
  {code:'ArrowRight',direction:1}, {code:'KeyD',direction:1},
  {code:'ArrowLeft',direction:-1}, {code:'KeyA',direction:-1}
 ];
 for(const control of controls){
  await reset();await page.keyboard.down(control.code);await at(.5);const s=await state();await page.keyboard.up(control.code);
  check(`move ${control.code}`,control.direction===1?s.p.x>220&&s.p.vx>0:s.p.x<220&&s.p.vx<0,{x:s.p.x,vx:s.p.vx,facing:s.p.facing});
 }
 for(const code of ['Space','KeyW','ArrowUp']){
  await reset();await page.keyboard.down(code);await at(.05);const s=await state();await page.keyboard.up(code);
  check(`jump ${code}`,s.p.vy<0&&s.p.y<800&&!s.p.grounded,{y:s.p.y,vy:s.p.vy,events:s.time});
  await at(.9);const landed=await state();check(`land after ${code}`,landed.p.grounded&&landed.p.y===800,{y:landed.p.y,grounded:landed.p.grounded});
 }
 for(const code of ['KeyS','ArrowDown']){
  await reset();const standing=await state();await page.keyboard.down(code);await at(.15);const duck=await state();await page.keyboard.up(code);await at(.3);const recovered=await state();
  const standingHeight=standing.p.width*(1.38-.46*standing.p.duck),duckHeight=duck.p.width*(1.38-.46*duck.p.duck);
  check(`duck ${code}`,duck.p.duck>.99&&duckHeight<standingHeight&&recovered.p.duck<.01,{duck:duck.p.duck,standingHeight,duckHeight,recoveredDuck:recovered.p.duck});
 }
 await reset();await page.keyboard.down('KeyD');await page.keyboard.down('Space');await at(.5);await page.keyboard.up('KeyD');await page.keyboard.up('Space');
 const beforeR=await state();await page.keyboard.press('KeyR');const afterR=await state();
 check('R clears simulation state',afterR.time===0&&afterR.p.x===220&&afterR.p.y===800&&afterR.p.vx===0&&afterR.p.vy===0&&afterR.attempt===1&&afterR.finishAt===-1&&afterR.shots.length===0&&afterR.cam.x===0&&afterR.cam.y===0,{before:{time:beforeR.time,x:beforeR.p.x,y:beforeR.p.y},after:afterR});
 const events=await page.evaluate(() => window.demo.events());check('R clears event history',events.length===0,{events});
 await at(.2);const idle=await state();check('R retains manual idle mode',idle.p.x===220&&idle.p.vx===0,{x:idle.p.x,vx:idle.p.vx,time:idle.time});
 await page.keyboard.down('KeyD');await at(.4);const resumed=await state();await page.keyboard.up('KeyD');check('movement works after R',resumed.p.x>220&&resumed.p.vx>0,{x:resumed.p.x,vx:resumed.p.vx});
 check('no page or console errors',report.errors.length===0,{errors:report.errors});
 report.observations.push('render=1 freezes requestAnimationFrame; all movement in this audit used deterministic renderAt times after manual reset.');
 report.observations.push('Duck collision height uses width*(1.38-.46*duck), changing 144.9px standing to 96.6px fully ducked.');
 report.observations.push('Input keys intentionally persist while physically held across reset; all restart checks released movement keys before R.');
 report.passed=report.checks.every(c=>c.pass);
 writeFileSync(path.join(root,'qa','manual_controls_audit.json'),JSON.stringify(report,null,2));
 console.log(JSON.stringify({passed:report.passed,checks:report.checks.map(c=>({name:c.name,pass:c.pass})),errors:report.errors},null,2));
}finally{await browser.close();}
