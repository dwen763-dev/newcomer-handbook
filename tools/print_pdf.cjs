// 把 HTML 打印成 A4 PDF：node tools/print_pdf.cjs <in.html> <out.pdf>
// 需要 Playwright（require('playwright')）和环境变量 CHROME 指向 Chromium 可执行文件
const {chromium} = require('playwright'); const path = require('path'); const {pathToFileURL} = require('url');
const [, , input, output] = process.argv;
(async () => {
  const b = await chromium.launch({executablePath: process.env.CHROME});
  const p = await b.newPage();
  await p.goto(pathToFileURL(path.resolve(input)).href, {waitUntil: 'load'});
  await p.waitForTimeout(500);
  await p.pdf({path: output, format: 'A4', printBackground: true, preferCSSPageSize: true,
    displayHeaderFooter: true, headerTemplate: '<div></div>',
    footerTemplate: '<div style="width:100%;font-size:8px;color:#888;text-align:center;font-family:Microsoft YaHei">新人办事说明书 · 视频版 抖音 @牧林Mlin · <span class="pageNumber"></span> / <span class="totalPages"></span></div>',
    margin: {top: '18mm', bottom: '20mm', left: '16mm', right: '16mm'}});
  await b.close(); console.log('ok', output);
})();
