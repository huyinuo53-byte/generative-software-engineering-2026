const {chromium}=require('playwright');
const fs=require('node:fs'), path=require('node:path');
const {pathToFileURL}=require('node:url');
(async()=>{
 const root=process.argv[2],out=path.join(root,'archive/qa/reader');fs.mkdirSync(out,{recursive:true});
 const review=JSON.parse(fs.readFileSync(path.join(root,'生成式软件工程/review.json')));
 const rows=[],errors=[],network=[];
 const browser=await chromium.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:true});
 try{
 const context=await browser.newContext();await context.route(/^https?:/,route=>{network.push(route.request().url());return route.abort();});
 const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
 const index=path.join(root,'生成式软件工程/课程索引.html');
 for(const width of [1280,390]){
  await page.setViewportSize({width,height:844});
  await page.goto(pathToFileURL(index).href,{waitUntil:'load'});
  const links=await page.locator('a[href]').evaluateAll(es=>es.map(e=>e.getAttribute('href')));
  const missing=review.items.filter(x=>!links.includes(x.html));if(missing.length)throw Error('index missing '+JSON.stringify(missing));
  await page.screenshot({path:path.join(out,`index-${width}.png`),fullPage:true});
  for(const item of review.items){
   await page.goto(pathToFileURL(index).href,{waitUntil:'load'});
   await page.locator(`a[href="${item.html}"]`).first().click();await page.waitForLoadState('load');
   await page.evaluate(()=>Promise.all([...document.images].filter(im=>im.getAttribute('src')).map(im=>im.decode().catch(()=>null))));
   const state=await page.evaluate(()=>({title:document.title,images:[...document.images].filter(i=>i.getAttribute('src')).length,broken:[...document.images].filter(i=>i.getAttribute('src')&&(!i.complete||!i.naturalWidth)).length,overflow:document.documentElement.scrollWidth>innerWidth,externalImages:[...document.images].filter(i=>i.getAttribute('src')&&!i.src.startsWith('data:')).length}));
   if(state.images!==item.images||state.broken||state.overflow||state.externalImages)throw Error(JSON.stringify({width,item:item.folder,state}));
   if(item.folder==='lecture-09')await page.screenshot({path:path.join(out,`lecture09-${width}.png`),fullPage:false});
   rows.push({width,item:item.folder,expectedImages:item.images,...state,click:'passed'});
  }
 }
 const result={status:errors.length||network.length?'FAIL':'PASS',scope:'copied current index click-through and offline image decode; no new semantic or native-project restoration claim',rows,errors,network,realPhone:'not_tested'};
 fs.writeFileSync(path.join(out,'journey.json'),JSON.stringify(result,null,2));console.log(JSON.stringify({status:result.status,paths:rows.length,images:rows.reduce((n,x)=>n+x.images,0),errors,network}));
 if(result.status!=='PASS')process.exitCode=1;
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1});
