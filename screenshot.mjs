import puppeteer from 'puppeteer';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __dirname = dirname(fileURLToPath(import.meta.url));
const htmlPath = join(__dirname, 'index.html');

const browser = await puppeteer.launch({ headless: true });
const page = await browser.newPage();

// A4 at 96dpi: 794 x 1123
await page.setViewport({ width: 794, height: 1123, deviceScaleFactor: 2 });
await page.goto(`file://${htmlPath}`, { waitUntil: 'networkidle0' });

const outputPath = join(__dirname, 'flyer_A4.png');
await page.screenshot({
  path: outputPath,
  clip: { x: 0, y: 0, width: 794, height: 1123 }
});

await browser.close();
console.log(`Screenshot saved: ${outputPath}`);
