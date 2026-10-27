import fs from 'node:fs/promises';
import path from 'node:path';
import os from 'node:os';
import {createHash,randomUUID} from 'node:crypto';
import {pathToFileURL,fileURLToPath} from 'node:url';
import {createRequire} from 'node:module';
const self=fileURLToPath(import.meta.url), widths=[1280,390];
const sha=async p=>createHash('sha256').update(await fs.readFile(p)).digest('hex');
const read=async p=>JSON.parse(await fs.readFile(p,'utf8'));
const save=async(p,v)=>{const tmp=`${p}.${process.pid}.tmp`;await fs.writeFile(tmp,JSON.stringify(v,null,2)+'\n');await fs.rename(tmp,p);};

export async function judgeViewport(row,profile) {
 const issues=[];
 if(!widths.includes(row.width)||row.width!==row.viewportWidth||!Number.isFinite(row.scrollWidth)||row.scrollWidth>row.width)issues.push('page overflow or viewport mismatch');
 for(const key of ['brokenImages','duplicateIds','brokenAnchors','errors'])
  if(!Array.isArray(row[key])||row[key].length)issues.push(key);
 for(const key of ['navigation','details','comparison','zoom']) {
  const verdict=row.interactions?.[key];
  if(verdict!=='PASS'&&!(profile==='generic'&&verdict==='NOT_APPLICABLE'))issues.push(`${key}: ${verdict??'missing'}`);
 }
 try{if(!row.screenshot||await sha(row.screenshot.path)!==row.screenshot.sha256)issues.push('screenshot changed');}
 catch{issues.push('screenshot unavailable');}
 return issues;
}

export async function judgeAudit(result,file,profile='generic') {
 if(!['generic','index'].includes(profile))return {status:'BLOCKED',issues:['unknown profile']};
 if(!result||result.schema_version!==2)return {status:'STALE',issues:['no current audit; run --resume']};
 try {
  if(result.file!==path.resolve(file)||result.html_sha256!==await sha(file)||result.auditor_sha256!==await sha(self)||result.profile!==profile)
   return {status:'STALE',issues:['HTML, auditor or profile changed']};
  if(!result.dependencies||typeof result.dependencies!=='object'||Array.isArray(result.dependencies))return {status:'STALE',issues:['dependency record missing']};
  for(const [resource,digest] of Object.entries(result.dependencies))
   if(await sha(resource)!==digest)return {status:'STALE',issues:[`dependency changed: ${resource}`]};
 }catch(error){return {status:'STALE',issues:[`input unavailable: ${error.message}`]};}
 const issues=[];
 for(const width of widths) {
  const row=result.viewports?.find(v=>v.width===width);
  if(!row){issues.push(`${width}: pending`);continue;}
  issues.push(...(await judgeViewport(row,profile)).map(v=>`${width}: ${v}`));
 }
 return {status:issues.length?'FAIL':'PASS',issues};
}

async function viewport(page,width,output,profile) {
 const errors=[],interactions={};
 const onError=e=>errors.push(e.message),onConsole=m=>{if(m.type()==='error')errors.push(m.text());};
 page.on('pageerror',onError);page.on('console',onConsole);
 async function journey(name,selector,action) {
  try {
   const candidates=page.locator(selector.endsWith(':visible')?selector:`${selector}:visible`);
   let target;
   for(const candidate of await candidates.all()) {
    if(name==='details'&&await candidate.evaluate(e=>getComputedStyle(e).pointerEvents==='none'))continue;
    target=candidate;break;
   }
   if(!target){interactions[name]=profile==='index'?'FAIL':'NOT_APPLICABLE';return;}
   interactions[name]=await action(target)?'PASS':'FAIL';
  }catch(error){interactions[name]='FAIL';errors.push(`${name}: ${error.message}`);}
 }
 try {
  await page.setViewportSize({width,height:900});
  await page.goto(pathToFileURL(page.auditFile).href,{waitUntil:'load'});
  await page.locator('details').evaluateAll(items=>items.forEach(e=>{e.open=true;}));
  // Reveal visible lazy images before decode; container overflow is allowed, page overflow is not.
  for(const image of await page.locator('img[src]').all())if(await image.isVisible())await image.scrollIntoViewIfNeeded();
  await page.evaluate(()=>Promise.all([...document.images].map(i=>Promise.race([i.decode().catch(()=>null),new Promise(resolve=>setTimeout(resolve,5000))]))));
  await journey('navigation','nav a[href^="#"]:visible',async link=>{
   const href=await link.getAttribute('href');
   await link.evaluate(el=>{for(let p=el.parentElement;p;p=p.parentElement)if(p.tagName==='DETAILS')p.open=true;});
   await link.click();await page.waitForFunction(hash=>location.hash===hash,href);
   return page.evaluate(hash=>!!document.getElementById(hash.slice(1)),href);
  });
  await journey('details','details summary',async summary=>{
   const before=await summary.evaluate(e=>e.parentElement.open);await summary.click();
   const changed=await summary.evaluate((e,value)=>e.parentElement.open!==value,before);await summary.click();return changed;
  });
  await journey('comparison','[data-view="after"]',async target=>{
   await target.click();return await page.locator('#after').isVisible()&&!await page.locator('#before').isVisible();
  });
  await journey('zoom','[data-zoom]:visible, button.zoom:visible',async target=>{
   await target.click();const dialog=page.locator('dialog').first();await dialog.waitFor({state:'visible'});
   await dialog.locator('img').evaluateAll(items=>Promise.all(items.map(i=>i.decode().catch(()=>null))));
   const images=await dialog.locator('img').evaluateAll(items=>items.length>0&&items.every(i=>i.complete&&i.naturalWidth>0));
   await page.locator('[data-close], dialog #close').first().click();await dialog.waitFor({state:'hidden'});
   await target.click();await dialog.waitFor({state:'visible'});await page.keyboard.press('Escape');await dialog.waitFor({state:'hidden'});return images;
  });
  const row=await page.evaluate(()=>{
   const ids=[...document.querySelectorAll('[id]')].map(e=>e.id);
   return {width:innerWidth,viewportWidth:innerWidth,scrollWidth:document.documentElement.scrollWidth,title:document.title,
    images:document.images.length,
    brokenImages:[...document.images].filter(i=>i.hasAttribute('src')&&(!i.complete||!i.naturalWidth)).map(i=>i.getAttribute('src').slice(0,200)),
    duplicateIds:ids.filter((id,i)=>ids.indexOf(id)!==i),
    brokenAnchors:[...document.querySelectorAll('a[href^="#"]')].filter(a=>!document.getElementById(a.getAttribute('href').slice(1))).map(a=>a.getAttribute('href'))};
  });
  await page.evaluate(()=>scrollTo(0,0));
  const proof=path.join(output,`${width}-top.png`);await page.screenshot({path:proof});
  return {...row,interactions,errors,screenshot:{path:proof,sha256:await sha(proof)}};
 }finally{page.off('pageerror',onError);page.off('console',onConsole);}
}

export async function main(args=process.argv.slice(2)) {
 const [requestedFile,requestedOutput,...options]=args;let profile='generic';
 for(let i=0;i<options.length;i++) {
  if(options[i]==='--profile')profile=options[++i];
  else if(!['--resume','--check'].includes(options[i]))throw new Error(`Unknown option: ${options[i]}`);
 }
 if(!requestedFile||!requestedOutput||!['generic','index'].includes(profile))throw new Error('Usage: node scripts/audit-report.mjs HTML OUTPUT_DIR [--profile generic|index] [--resume|--check]');
 const file=path.resolve(requestedFile),output=path.resolve(requestedOutput),auditFile=path.join(output,'audit.json'),lockFile=path.join(output,'.audit.lock');
 let previous,lock;
 try{previous=await read(auditFile);}catch(error){if(error.code!=='ENOENT'&&!(error instanceof SyntaxError))throw error;}
 try{lock=await read(lockFile);}catch(error){if(error.code!=='ENOENT')throw error;}
 if(lock){console.log(JSON.stringify({status:'BLOCKED',owner:lock,next_action:'Check owner process/session; do not remove a live lock or start a second writer.'}));return 2;}
 const verdict=await judgeAudit(previous,file,profile);
 if(options.includes('--check')){console.log(JSON.stringify(verdict));return verdict.status==='PASS'?0:verdict.status==='FAIL'?1:2;}
 if(options.includes('--resume')&&verdict.status==='PASS'){console.log(JSON.stringify({status:'PASS',reused_viewports:widths,audit:auditFile}));return 0;}
 const result={schema_version:2,file,html_sha256:await sha(file),auditor_sha256:await sha(self),profile,dependencies:{},viewports:[],reused_viewports:[],status:'IN_PROGRESS',scope:'mechanical browser checks; no semantic, source, video, real-device or native-print certification'};
 await fs.mkdir(output,{recursive:true});
 const token=randomUUID(),owner={pid:process.pid,host:os.hostname(),token,file,started_at:new Date().toISOString()};
 try{await fs.writeFile(lockFile,JSON.stringify(owner),{flag:'wx'});}catch(error){if(error.code!=='EEXIST')throw error;console.log(JSON.stringify({status:'BLOCKED',reason:'another writer acquired lock'}));return 2;}
 let browser,interrupted=false;
 const stop=()=>{interrupted=true;if(browser)browser.close().catch(()=>{});};
 process.once('SIGINT',stop);process.once('SIGTERM',stop);
 try {
  if(options.includes('--resume')&&verdict.status==='FAIL') {
   for(const row of previous.viewports??[])if(!(await judgeViewport(row,profile)).length){result.viewports.push(row);result.reused_viewports.push(row.width);}
   result.dependencies={...previous.dependencies};
  }
  await save(auditFile,result);
  const {chromium}=createRequire(import.meta.url)('playwright');
  browser=await chromium.launch({headless:true,handleSIGINT:false,handleSIGTERM:false,executablePath:process.env.AUDIT_BROWSER_PATH||'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'});
  const page=await browser.newPage();page.auditFile=file;page.setDefaultTimeout(5000);
  const resources=new Map(Object.entries(result.dependencies).map(([p,digest])=>[p,Promise.resolve(digest)]));
  page.on('request',r=>{if(r.url().startsWith('file:')){const p=fileURLToPath(r.url());if(!resources.has(p))resources.set(p,sha(p).catch(()=>null));}});
  for(const width of widths) {
   if(result.reused_viewports.includes(width))continue;
   if(interrupted)throw new Error('Audit interrupted; current checkpoints retained for --resume.');
   const row=await viewport(page,width,output,profile);
   if(interrupted)throw new Error('Audit interrupted; current checkpoints retained for --resume.');
   result.viewports=result.viewports.filter(v=>v.width!==width);result.viewports.push(row);
   for(const [resource,pending] of resources){const digest=await pending;if(digest)result.dependencies[resource]=digest;}
   result.status=(await judgeAudit(result,file,profile)).status;await save(auditFile,result);
  }
  Object.assign(result,await judgeAudit(result,file,profile));await save(auditFile,result);
  console.log(JSON.stringify({status:result.status,issues:result.issues,reused_viewports:result.reused_viewports,audit:auditFile}));
  return result.status==='PASS'?0:result.status==='FAIL'?1:2;
 }catch(error){result.status='BLOCKED';result.error=error.message;await save(auditFile,result);console.log(JSON.stringify({status:'BLOCKED',reason:error.message,audit:auditFile}));return 2;}
 finally{process.removeListener('SIGINT',stop);process.removeListener('SIGTERM',stop);try{if(browser)await browser.close();}finally{if((await read(lockFile)).token===token)await fs.unlink(lockFile);}}
}
if(process.argv[1]&&path.resolve(process.argv[1])===self)main().then(c=>{process.exitCode=c;}).catch(e=>{console.error(e.message);process.exitCode=2;});
