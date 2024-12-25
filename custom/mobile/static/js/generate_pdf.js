// generate_pdf.js
const puppeteer = require('puppeteer');

async function generatePDF(url, outputPath) {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  await page.goto(url, { waitUntil: 'networkidle0' });
  await page.pdf({
    path: outputPath,
    format: 'A4',
    printBackground: true,
  });
  await browser.close();
}

// 从命令行参数获取 URL 和输出路径
const args = process.argv.slice(2);
const url = args[0];
const outputPath = args[1];

generatePDF(url, outputPath).then(() => {
  console.log('PDF generated successfully!');
}).catch((error) => {
  console.error('Error generating PDF:', error);
});
