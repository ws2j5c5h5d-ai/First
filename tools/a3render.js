// node tools/a3render.js <html> <out.png>
// Breite der Seite so wählen, dass das Seitenverhältnis A3 (1:1,414) entspricht, dann hochauflösend rendern.
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const [html, out] = process.argv.slice(2);
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 2400, height: 1200 } });
  await p.goto('file://' + path.resolve(html), { waitUntil: 'networkidle' });
  await p.evaluate(() => document.fonts.ready);
  await p.addStyleTag({ content: 'html,body{background:#fff!important;padding:0!important}.page{box-shadow:none!important;margin:0!important;background:#fff!important}' });
  const ratio = w => p.evaluate(w => { const e = document.querySelector('.page'); e.style.width = w + 'px'; return e.offsetHeight / w; }, w);
  let lo = 1180, hi = 2300;
  for (let i = 0; i < 14; i++) { const m = (lo + hi) / 2; (await ratio(m)) > Math.SQRT2 ? lo = m : hi = m; }
  const w = Math.round(hi); const r = await ratio(w);
  const dpr = 3400 / w;
  const p2 = await b.newPage({ viewport: { width: 2400, height: 1200 }, deviceScaleFactor: dpr });
  await p2.goto('file://' + path.resolve(html), { waitUntil: 'networkidle' });
  await p2.evaluate(() => document.fonts.ready);
  await p2.addStyleTag({ content: 'html,body{background:#fff!important;padding:0!important}.page{box-shadow:none!important;margin:0!important;background:#fff!important}' });
  await p2.evaluate(w => { document.querySelector('.page').style.width = w + 'px'; }, w);
  await (await p2.$('.page')).screenshot({ path: out });
  console.log(html, 'width', w, 'ratio', r.toFixed(3));
  await b.close();
})();
