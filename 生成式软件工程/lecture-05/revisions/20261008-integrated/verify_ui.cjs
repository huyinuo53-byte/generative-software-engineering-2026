const fs = require('fs');
const path = require('path');
const assert = require('assert/strict');
const { pathToFileURL } = require('url');
const { chromium } = require('playwright');
const root = path.resolve(__dirname, '../..');
const notes = JSON.parse(fs.readFileSync(path.join(root, 'notes.json')));
const map = JSON.parse(fs.readFileSync(path.join(__dirname, 'integration-map.json')));

(async () => {
  const browser = await chromium.launch({headless:true, executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', args:['--disable-background-networking']});
  const result = {method:'isolated Chrome, local file, desktop 1440px and narrow 390px; no real phone',viewports:[]};
  try {
    for (const width of [1440,390]) {
      const page = await browser.newPage({viewport:{width,height:1000}});
      const errors=[];
      page.on('pageerror', e=>errors.push(String(e)));
      page.on('console', m=>{if(m.type()==='error')errors.push(m.text())});
      await page.goto(pathToFileURL(path.join(root,'课堂笔记.html')).href);
      await page.locator('main img').evaluateAll(xs=>Promise.all(xs.map(x=>x.decode())));
      const state=await page.evaluate(({notes,map})=>{
        const ids=[...document.querySelectorAll('[id]')].map(x=>x.id);
        const allText=document.body.textContent;
        const blocks=[...notes.summary];
        for(const s of notes.sections) blocks.push(...s.paragraphs,...(s.examples||[]),...(s.editor_notes||[]).map(x=>x.startsWith('讲义延伸｜')?x.split('）：')[1]:x));
        for(const q of notes.self_test)blocks.push(q.question,q.answer);
        return {
          width:innerWidth,scrollWidth:document.documentElement.scrollWidth,
          images:document.querySelectorAll('main figure img').length,
          broken:[...document.querySelectorAll('main img')].filter(x=>!x.naturalWidth).length,
          duplicateIds:ids.filter((x,i)=>ids.indexOf(x)!==i),
          badAnchors:[...document.querySelectorAll('a[href^="#"]')].filter(x=>!document.getElementById(x.hash.slice(1))).map(x=>x.hash),
          missingText:blocks.filter(x=>!allText.includes(x)),
          integrations:map.map(x=>({page:x.page,section:document.querySelector('#slide-'+x.page).closest('section').id,images:document.querySelectorAll('#slide-'+x.page+' figure').length,hasLabel:document.querySelector('#slide-'+x.page).textContent.includes('课堂未展开')})),
          quizCount:document.querySelectorAll('.quiz-card').length,
          answersInitiallyClosed:[...document.querySelectorAll('.quiz-answer')].every(x=>!x.open),
          oldAppendix:!!document.querySelector('#supplements')
        };
      },{notes,map});
      assert.equal(state.width,state.scrollWidth);assert.equal(state.images,40);assert.equal(state.broken,0);
      assert.deepEqual(state.missingText,[]);assert.deepEqual(state.badAnchors,[]);assert.deepEqual(state.duplicateIds,[]);
      assert.equal(state.quizCount,12);assert(state.answersInitiallyClosed);assert(!state.oldAppendix);
      state.integrations.forEach((x,i)=>{assert.equal(x.section,'s'+map[i].section);assert.equal(x.images,1);assert(x.hasLabel)});
      await page.screenshot({path:path.join(__dirname,`${width}-top.png`)});
      for(const p of (width===1440?map.map(x=>x.page):[33,36])){
        await page.locator('#slide-'+p).screenshot({path:path.join(__dirname,`${width}-slide-${p}.png`)});
      }
      await page.locator('.course-toc summary').click();
      await page.locator('nav a[href="#s14"]').click();
      assert.equal(new URL(page.url()).hash,'#s14');
      await page.locator('#slide-33 .zoom').click();
      assert(await page.locator('dialog').evaluate(x=>x.open));
      await page.locator('#actual-size').click();
      await page.keyboard.press('Escape');
      assert(!(await page.locator('dialog').evaluate(x=>x.open)));
      const card=page.locator('.quiz-card').first();
      await card.scrollIntoViewIfNeeded();
      await page.screenshot({path:path.join(__dirname,`${width}-quiz-closed.png`)});
      await card.locator('summary').focus();await page.keyboard.press('Enter');
      assert(await card.locator('details').evaluate(x=>x.open));
      await page.screenshot({path:path.join(__dirname,`${width}-quiz-open.png`)});
      const colors=await card.evaluate(x=>({question:getComputedStyle(x.querySelector('.quiz-question')).backgroundColor,answer:getComputedStyle(x.querySelector('.answer-body')).backgroundColor}));
      assert.notEqual(colors.question,colors.answer);
      await card.locator('.answer-body a').click();assert.equal(new URL(page.url()).hash,'#s3');
      await card.locator('summary').click();assert(!(await card.locator('details').evaluate(x=>x.open)));
      if(width===1440){
        await page.pdf({path:path.join(__dirname,'print-check.pdf'),format:'A4',printBackground:true,margin:{top:'14mm',bottom:'14mm',left:'10mm',right:'10mm'}});
        assert(await page.locator('.quiz-answer').evaluateAll(xs=>xs.every(x=>!x.open)));
      }
      assert.deepEqual(errors,[]);
      result.viewports.push({...state,colors,errors,toc:true,zoom:true,keyboardAnswerToggle:true,returnLink:true});
      await page.close();
    }
    result.status='passed';
    fs.writeFileSync(path.join(__dirname,'browser.json'),JSON.stringify(result,null,2));
    console.log(JSON.stringify(result,null,2));
  } finally {await browser.close()}
})().catch(e=>{console.error(e);process.exit(1)});
