const fs = require('node:fs');
const {chromium} = require('playwright');
(async()=>{
  const browser=await chromium.launch({headless:true,executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',args:['--no-sandbox']});
  const checks=[];
  for (const [name,width,height] of [['phone',390,844],['desktop',1280,800]]) {
    const page=await browser.newPage({viewport:{width,height}});
    await page.goto('http://127.0.0.1:8769/%E5%BD%92%E6%A1%A3%E9%98%85%E8%AF%BB%E4%B8%8E%E6%81%A2%E5%A4%8D.html');
    await page.waitForLoadState('load');
    await page.screenshot({path:`/private/tmp/gse-publication-20261027/persona-${name}-top.png`});
    for (const text of ['阅读入口','下载与恢复','证据边界']) {
      await page.getByRole('link',{name:text,exact:true}).click();
      await page.waitForTimeout(900);
      const result=await page.evaluate(()=>{
        const target=document.querySelector(location.hash);
        return {hash:location.hash,firstText:target?.innerText.slice(0,350),top:target?.getBoundingClientRect().top};
      });
      checks.push({width:name,link:text,...result});
    }
    await page.getByRole('heading',{name:'恢复 BaoCut',exact:true}).scrollIntoViewIfNeeded();
    await page.screenshot({path:`/private/tmp/gse-publication-20261027/persona-${name}-restore.png`});
    for (const [heading,label] of [['质量与范围','scope'],['取得源视频','media']]) {
      await page.getByRole('heading',{name:heading,exact:true}).scrollIntoViewIfNeeded();
      await page.screenshot({path:`/private/tmp/gse-publication-20261027/persona-${name}-${label}.png`});
    }
    const pres=await page.locator('pre').evaluateAll(es=>es.map(e=>({text:e.innerText,clientWidth:e.clientWidth,scrollWidth:e.scrollWidth,overflowX:getComputedStyle(e).overflowX})));
    checks.push({width:name,commandBlocks:pres});
    if(name==='phone'){
      const blocks=page.locator('pre');
      for(let i=0;i<await blocks.count();i++){
        const b=blocks.nth(i);await b.scrollIntoViewIfNeeded();
        const result=await b.evaluate(e=>{const before=e.scrollLeft;e.scrollLeft=e.scrollWidth;return {before,after:e.scrollLeft,width:e.clientWidth,content:e.scrollWidth};});
        checks.push({width:name,localHorizontalScroll:i,...result});
      }
      await page.screenshot({path:'/private/tmp/gse-publication-20261027/persona-phone-command-scroll.png'});
    }
    await page.close();
  }
  fs.writeFileSync('/private/tmp/gse-publication-20261027/persona-path-evidence.json',JSON.stringify(checks,null,2));
  console.log(JSON.stringify(checks,null,2));
  await browser.close();
})().catch(e=>{console.error(e);process.exit(1)});
