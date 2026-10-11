// Imprime tools/_build/*.html em pdf/*.pdf com o Chromium do Playwright.
// Uso: node tools/print.js   (NODE_PATH precisa enxergar o pacote playwright)
const path = require('path');
const fs = require('fs');
const { chromium } = require('playwright');

(async () => {
  const root = path.resolve(__dirname, '..');
  const build = path.join(root, 'tools', '_build');
  const out = path.join(root, 'pdf');
  fs.mkdirSync(out, { recursive: true });
  const browser = await chromium.launch();
  const page = await browser.newPage();
  for (const f of fs.readdirSync(build).filter((f) => f.endsWith('.html')).sort()) {
    await page.goto('file://' + path.join(build, f), { waitUntil: 'load' });
    const dest = path.join(out, f.replace(/\.html$/, '.pdf'));
    await page.pdf({
      path: dest, format: 'A4', printBackground: true, preferCSSPageSize: true,
      displayHeaderFooter: true, headerTemplate: '<span></span>',
      footerTemplate: '<div style="font-size:8px;color:#9ca3af;width:100%;text-align:center">Boxe — do zero à elite · <span class="pageNumber"></span>/<span class="totalPages"></span></div>',
    });
    console.log('pdf', dest);
  }
  await browser.close();
})();
