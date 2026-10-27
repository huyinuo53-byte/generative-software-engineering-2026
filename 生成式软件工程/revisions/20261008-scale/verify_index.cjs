const fs=require('fs'),path=require('path'),assert=require('assert/strict');
const {chromium}=require('playwright'),{pathToFileURL}=require('url');
(async()=>{
const root=path.resolve(__dirname,'../..'),b=await chromium.launch({headless:true,executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',args:['--disable-background-networking']}),result=[];
try{for(const width of [1440,768,390,320]){
 const p=await b.newPage({viewport:{width,height:1000}}),errors=[];p.on('pageerror',e=>errors.push(String(e)));
 await p.goto(pathToFileURL(path.join(root,'课程索引.html')).href);
 const s=await p.evaluate(()=>({width:innerWidth,scrollWidth:document.documentElement.scrollWidth,links:[...document.querySelectorAll('a.card')].map(a=>a.getAttribute('href')),text:document.body.textContent}));
 assert.equal(s.width,s.scrollWidth);assert.equal(s.links.length,8);for(const link of s.links)assert(fs.existsSync(path.join(root,link)));assert(s.text.includes('311'));
 await p.screenshot({path:path.join(__dirname,`index-${width}.png`)});await p.locator('details summary').click();assert(await p.locator('details').evaluate(x=>x.open));
 await p.locator('a.card').first().click();assert(await p.locator('.section-takeaway').count());assert.deepEqual(errors,[]);result.push({width,scrollWidth:s.scrollWidth,links:s.links,errors});await p.close();
}fs.writeFileSync(path.join(__dirname,'index-browser.json'),JSON.stringify({status:'passed',viewports:result},null,2));console.log('Index four viewports, eight local links and navigation passed');}finally{await b.close()}
})().catch(e=>{console.error(e);process.exit(1)});
