// 在既有 Puppeteer Docker 映像中驗證靜態網站；不安裝外部套件。
const puppeteer = require('/home/pptruser/node_modules/puppeteer');
const http = require('node:http');
const fs = require('node:fs');
const path = require('node:path');
const assert = require('node:assert/strict');
const prefix = '/ai-software-archaeology-handbook/';
const output = '/out';
const remote = process.env.SITE_URL;

(async () => {
  assert.equal(fs.statSync(output).uid, process.getuid(), '輸出目錄擁有權不符');
  for (const name of fs.readdirSync(output)) assert.equal(fs.statSync(path.join(output,name)).uid,process.getuid());
  let server;
  if (!remote) {
    server=http.createServer((req,res)=>{
      const pathname=decodeURIComponent(new URL(req.url,'http://localhost').pathname);
      if (!pathname.startsWith(prefix)) {res.writeHead(404);res.end();return;}
      const relative=pathname.slice(prefix.length) || 'index.html';
      const file=path.resolve('/work/docs',relative);
      if (!file.startsWith('/work/docs/') || !fs.existsSync(file) || !fs.statSync(file).isFile()) {res.writeHead(404);res.end('Not found');return;}
      const types={'.html':'text/html; charset=utf-8','.css':'text/css','.js':'text/javascript','.svg':'image/svg+xml','.png':'image/png','.xml':'application/xml','.txt':'text/plain'};
      res.setHeader('Content-Type',types[path.extname(file)]||'application/octet-stream');res.end(fs.readFileSync(file));
    });
    await new Promise(resolve=>server.listen(4173,'127.0.0.1',resolve));
  }
  const base=remote || 'http://127.0.0.1:4173'+prefix;
  let browser;
  try {
    browser=await puppeteer.launch({headless:true,args:['--no-sandbox','--disable-dev-shm-usage'],userDataDir:'/tmp/osa-site-browser'});
    const reports=[];
    const manifest=JSON.parse(fs.readFileSync('/work/docs/site-manifest.json')).pages;
    for (const record of manifest) {
      const page=await browser.newPage();await page.setViewport({width:390,height:900});
      const response=await page.goto(base+record.page,{waitUntil:'load'});assert.equal(response.status(),200,record.page);
      assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth+1),false,record.page);
      assert.ok(await page.$eval('article',e=>e.textContent.length)>100,record.page);
      if(record.page.endsWith('00-principles.html')||record.page.endsWith('worked-example.html')) await page.screenshot({path:path.join(output,record.page.replaceAll('/','-')+'.png'),fullPage:true});
      await page.close();
    }
    console.log(`${manifest.length} 份文件內頁：手機寬度、完整文章容器與 HTTP 狀態通過。`);
    for(const width of [1440,768,390,320]) {
      const page=await browser.newPage();const errors=[];const requests=[];
      page.on('pageerror',e=>errors.push(e.message));
      page.on('requestfailed',r=>errors.push(r.url()+': '+r.failure().errorText));
      page.on('request',r=>requests.push(r.url()));
      await page.setViewport({width,height:900,deviceScaleFactor:1});
      const response=await page.goto(base,{waitUntil:'networkidle0',timeout:45000});
      assert.equal(response.status(),200);
      await page.evaluate(()=>document.fonts.ready);
      const structure=await page.evaluate(()=>({
        title:document.title, lang:document.documentElement.lang,
        horizontalOverflow:document.documentElement.scrollWidth>innerWidth+1,
        h1:document.querySelectorAll('h1').length,
        cases:document.querySelectorAll('.case-list article').length,
        editions:document.querySelectorAll('.editions article').length,
        pdfs:[...document.querySelectorAll('.editions a.download')].map(a=>a.href),
        missingAnchors:[...document.querySelectorAll('a[href^="#"]')].filter(a=>!document.getElementById(a.hash.slice(1))).map(a=>a.hash),
        externalScripts:[...document.scripts].filter(s=>s.src && new URL(s.src).origin!==location.origin).map(s=>s.src),
        tinyText:[...document.querySelectorAll('p,a,button,summary')].filter(e=>e.getBoundingClientRect().width>0 && parseFloat(getComputedStyle(e).fontSize)<11).map(e=>e.textContent.slice(0,30))
      }));
      assert.equal(structure.lang,'zh-Hant');assert.equal(structure.h1,1);assert.equal(structure.cases,7);assert.equal(structure.editions,3);assert.equal(structure.pdfs.length,3);
      assert.equal(structure.horizontalOverflow,false,`${width}px 橫向溢出`);assert.deepEqual(structure.missingAnchors,[]);assert.deepEqual(structure.externalScripts,[]);assert.deepEqual(structure.tinyText,[]);
      assert.ok(requests.every(url=>new URL(url).origin===new URL(base).origin),'載入了第三方資源');
      await page.screenshot({path:path.join(output,`site-${width}.png`),fullPage:true});
      await page.screenshot({path:path.join(output,`hero-${width}.png`)});
      await page.click('nav a[href="#handbook"]');
      await page.waitForFunction(()=>Math.abs(document.querySelector('#handbook').getBoundingClientRect().top-24)<3);
      await page.click('summary');assert.equal(await page.$eval('details',e=>e.open),true);
      await page.emulateMediaFeatures([{name:'prefers-reduced-motion',value:'reduce'}]);
      assert.equal(await page.evaluate(()=>getComputedStyle(document.documentElement).scrollBehavior),'auto');
      if (width===1440) {
        await page.goto(base,{waitUntil:'networkidle0'});await page.keyboard.press('Tab');
        assert.equal(await page.evaluate(()=>document.activeElement.className),'skip');
        await browser.defaultBrowserContext().overridePermissions(new URL(base).origin,['clipboard-read','clipboard-write','clipboard-sanitized-write']);
        await page.bringToFront();
        await page.click('#share');await page.waitForFunction(()=>document.querySelector('#share-status').textContent.length>0);
        assert.match(await page.$eval('#share-status',e=>e.textContent),/已複製/);
        assert.equal(await page.evaluate(()=>navigator.clipboard.readText()),'https://wicanr2.github.io/ai-software-archaeology-handbook/');
      }
      assert.deepEqual(errors,[]);reports.push({width,...structure,requestCount:requests.length,errors});await page.close();
    }
    const nojs=await browser.newPage();await nojs.setJavaScriptEnabled(false);await nojs.goto(base,{waitUntil:'networkidle0'});
    assert.equal(await nojs.$$eval('.editions a.download',els=>els.length),3);assert.equal(await nojs.$eval('#share',e=>e.hidden),true);await nojs.close();
    fs.writeFileSync(path.join(output,'report.json'),JSON.stringify({base,browser:await browser.version(),noJavaScript:true,reports},null,2)+'\n');
    console.log('四種寬度、頁內錨點、案例／PDF 數量、鍵盤入口、複製連結、減少動態效果、無 JavaScript 閱讀：通過。');
  } finally { if(browser)await browser.close();if(server)server.close(); }
})().catch(error=>{console.error(error);process.exitCode=1;});
