const {chromium}=require('playwright');
const fs=require('fs');const path=require('path');const {pathToFileURL}=require('url');
(async()=>{
 const root=process.cwd();const dir=path.join(root,'research/research_notes/pstack-skills-20261022');
 const file=path.join(root,'research/reports/pstack Skills 写法与生成式软件工程启发.html');
 const browser=await chromium.launch({headless:true,executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'});
 const rows=[];
 try{
  const page=await browser.newPage();
  for(const width of [1280,390,320]){
   await page.setViewportSize({width,height:900});await page.goto(pathToFileURL(file).href);
   await page.locator('nav a[href="#walkthrough"]').click();
   const nav=await page.evaluate(()=>location.hash==='#walkthrough');
   const tables=[];
   for(const box of await page.locator('.table-wrap').all()){
    await box.scrollIntoViewIfNeeded();await box.focus();
    for(let i=0;i<16;i++)await page.keyboard.press('ArrowRight');
    await page.waitForTimeout(150);
    tables.push(await box.evaluate(e=>({client:e.clientWidth,scroll:e.scrollWidth,left:e.scrollLeft,end:e.scrollLeft>=e.scrollWidth-e.clientWidth-2})));
   }
   await page.locator('#selfcheck summary').click();
   const answer=await page.locator('#selfcheck').evaluate(e=>e.open);
   await page.locator('#selfcheck summary').click();
   const closed=await page.locator('#selfcheck').evaluate(e=>!e.open);
   await page.locator('#walkthrough').scrollIntoViewIfNeeded();
   await page.screenshot({path:path.join(dir,`reader-${width}-table.png`)});
   await page.locator('#new h3').nth(1).scrollIntoViewIfNeeded();
   await page.screenshot({path:path.join(dir,`reader-${width}-statechart.png`)});
   const overflow=await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth);
   rows.push({width,nav,answer,closed,overflow,tables});
  }
  await page.locator('a[href="../../生成式软件工程/lecture-05/课堂笔记.html#s11"]').click();
  const evidence=await page.locator('#s11').textContent();
  const source={url:page.url(),sectionText:evidence.slice(0,220),targetExists:!!evidence};
  await page.goBack();
  const restored=await page.title();
  const pass=rows.every(r=>r.nav&&r.answer&&r.closed&&!r.overflow&&r.tables.every(t=>t.end))&&source.targetExists&&restored.includes('pstack');
  fs.writeFileSync(path.join(dir,'reader-check.json'),JSON.stringify({status:pass?'PASS':'FAIL',rows,source,restored},null,2));
  console.log(JSON.stringify({status:pass?'PASS':'FAIL',rows,source,restored}));if(!pass)process.exitCode=1;
 }finally{await browser.close()}
})().catch(e=>{console.error(e);process.exitCode=1});
