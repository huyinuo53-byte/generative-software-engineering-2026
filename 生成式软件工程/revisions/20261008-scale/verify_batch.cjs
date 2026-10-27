const fs=require('fs'),path=require('path'),assert=require('assert/strict');
const {pathToFileURL}=require('url');
const {chromium}=require('playwright');
const root=path.resolve(__dirname,'../..');
(async()=>{
 const browser=await chromium.launch({headless:true,executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',args:['--disable-background-networking']});
 try{
  for(const name of fs.readdirSync(root).filter(n=>fs.existsSync(path.join(root,n,'reading-layout.json')) && (!process.argv[2] || process.argv.slice(2).includes(n)))){
   const dir=path.join(root,name),out=path.join(dir,'revisions/20261008-scale');
   const notes=JSON.parse(fs.readFileSync(path.join(dir,'notes.json'))),layout=JSON.parse(fs.readFileSync(path.join(dir,'reading-layout.json')));
   const report={scope:'Local isolated Chrome; four viewport widths, not physical phone; no new source reading',viewports:[]};
   for(const width of [1440,768,390,320]){
    const page=await browser.newPage({viewport:{width,height:1000}}),errors=[];
    page.on('pageerror',e=>errors.push(String(e)));page.on('console',m=>{if(m.type()==='error')errors.push(m.text())});
    await page.goto(pathToFileURL(path.join(dir,'课堂笔记.html')).href);
    await page.locator('main img').evaluateAll(xs=>Promise.all(xs.map(x=>x.decode())));
    const state=await page.evaluate(({notes,layout})=>{
     const text=document.body.textContent,ids=[...document.querySelectorAll('[id]')].map(x=>x.id);
     const blocks=[...(notes.summary||[]),...notes.limitations];
     for(const s of notes.sections)blocks.push(...s.paragraphs,...(s.examples||[]),...(s.editor_notes||[]));
     for(const x of (notes.supplements||notes.official_slide_supplements||[]))blocks.push(x.title,x.text);
     for(const q of (notes.self_test||[]))blocks.push(q.question,q.answer);
     const positions=[];
     layout.sections.forEach((s,i)=>s.flow.split(/\s+/).forEach(t=>{
      let selector;if(t[0]==='x')selector='#supplement-'+t.slice(1);
      if(t[0]==='f')selector='[data-frame="'+(t.includes(':')?t.slice(1):(i+1)+':'+t.slice(1))+'"]';
      if(selector)positions.push({token:t,expected:'s'+(i+1),actual:document.querySelector(selector)?.closest('section')?.id});
     }));
     return {width:innerWidth,scrollWidth:document.documentElement.scrollWidth,missingText:blocks.filter(t=>!text.includes(t)),textBlocks:blocks.length,
      images:document.querySelectorAll('main figure img').length,broken:[...document.querySelectorAll('main img')].filter(x=>!x.naturalWidth).length,
      duplicateIds:ids.filter((x,i)=>ids.indexOf(x)!==i),badAnchors:[...document.querySelectorAll('a[href^="#"]')].filter(x=>!document.getElementById(x.hash.slice(1))).map(x=>x.hash),
      positions,quizCount:document.querySelectorAll('.quiz-card').length,answersClosed:[...document.querySelectorAll('.quiz-answer')].every(x=>!x.open),oldAppendix:!!document.querySelector('#supplements'),
      takeaways:document.querySelectorAll('.section-takeaway').length,strongCount:document.querySelectorAll('main strong').length,emphasisRatio:[...document.querySelectorAll('main strong')].reduce((n,x)=>n+x.textContent.length,0)/document.querySelector('main').textContent.length,
      externalImages:document.querySelectorAll('img[src^=http]').length,externalStyles:document.querySelectorAll('link[rel=stylesheet]').length};
    },{notes,layout});
    assert.equal(state.width,state.scrollWidth,`${name} overflow ${width}`);assert.deepEqual(state.missingText,[]);assert.deepEqual(state.duplicateIds,[]);assert.deepEqual(state.badAnchors,[]);
    assert.equal(state.images,notes.sections.reduce((n,s)=>n+(s.frames||[]).length,0));assert.equal(state.broken,0);assert(state.answersClosed);assert(!state.oldAppendix);assert(state.emphasisRatio<0.12);
    assert.equal(state.takeaways,notes.sections.length);assert.equal(state.quizCount,(notes.self_test||[]).length);assert.equal(state.externalImages,0);assert.equal(state.externalStyles,0);state.positions.forEach(x=>assert.equal(x.actual,x.expected));
    await page.screenshot({path:path.join(out,`${width}-top.png`)});
    if(width===1440||width===390){await page.locator('#s3').evaluate(x=>x.scrollIntoView());await page.screenshot({path:path.join(out,`${width}-reading.png`)});
     if(await page.locator('.inline-reading').count())await page.locator('.inline-reading').first().screenshot({path:path.join(out,`${width}-supplement.png`)});
    }
    if(width<1100)await page.locator('.course-toc summary').click();
    await page.locator('nav a[href="#s2"]').click();assert.equal(new URL(page.url()).hash,'#s2');
    await page.locator('main .zoom').first().click();assert(await page.locator('dialog').evaluate(x=>x.open));await page.locator('#actual-size').click();await page.keyboard.press('Escape');assert(!(await page.locator('dialog').evaluate(x=>x.open)));
    const card=page.locator('.quiz-card').first();if(await card.count()){
     await card.locator('summary').focus();await page.keyboard.press('Enter');assert(await card.locator('details').evaluate(x=>x.open));
     await card.scrollIntoViewIfNeeded();await page.screenshot({path:path.join(out,`${width}-quiz.png`)});
     state.colors=await card.evaluate(x=>({question:getComputedStyle(x.querySelector('.quiz-question')).backgroundColor,answer:getComputedStyle(x.querySelector('.answer-body')).backgroundColor}));assert.notEqual(state.colors.question,state.colors.answer);
     const link=card.locator('.answer-body a');if(await link.count()){const target=await link.getAttribute('href');await link.click();assert.equal(new URL(page.url()).hash,target)}
     await card.locator('summary').click();assert(!(await card.locator('details').evaluate(x=>x.open)));
    }
    if(width===1440){
     await page.evaluate(()=>window.dispatchEvent(new Event('beforeprint')));assert(await page.locator('.quiz-answer').evaluateAll(xs=>xs.every(x=>x.open)));await page.evaluate(()=>window.dispatchEvent(new Event('afterprint')));
     await page.pdf({path:path.join(out,'print-check.pdf'),format:'A4',printBackground:true,margin:{top:'14mm',bottom:'14mm',left:'10mm',right:'10mm'}});assert(await page.locator('.quiz-answer').evaluateAll(xs=>xs.every(x=>!x.open)));
    }
    assert.deepEqual(errors,[]);report.viewports.push({...state,errors,toc:true,zoom:true,keyboardAnswerToggle:true});await page.close();
   }
   report.status='passed';fs.writeFileSync(path.join(out,'browser.json'),JSON.stringify(report,null,2));console.log(JSON.stringify({lesson:name,status:report.status,viewports:report.viewports.map(x=>({width:x.width,images:x.images,emphasisRatio:x.emphasisRatio,textBlocks:x.textBlocks}))}));
  }
 }finally{await browser.close()}
})().catch(e=>{console.error(e);process.exit(1)});
