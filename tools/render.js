// node tools/render.js <ordner> <name>  -> <ordner>/<name>.png und .pdf
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const [dir, name] = process.argv.slice(2);
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1280, height: 900 }, deviceScaleFactor: 2 });
  await p.goto('file://' + path.resolve(dir, 'index.html'), { waitUntil: 'networkidle' });
  await p.evaluate(() => document.fonts.ready);
  await (await p.$('.page')).screenshot({ path: path.resolve(dir, name + '.png') });
  await p.emulateMedia({ media: 'print' });
  const h = await p.evaluate(() => document.querySelector('.page').offsetHeight);
  await p.pdf({ path: path.resolve(dir, name + '.pdf'), width: '1180px', height: (h + 2) + 'px', printBackground: true, pageRanges: '1' });
  console.log(dir, h);
  await b.close();
})();
