import puppeteer from 'puppeteer';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __dirname = dirname(fileURLToPath(import.meta.url));
const htmlPath = join(__dirname, 'index.html');

const browser = await puppeteer.launch({ headless: true });
const page = await browser.newPage();
await page.setViewport({ width: 794, height: 2000, deviceScaleFactor: 1 });
await page.goto(`file://${htmlPath}`, { waitUntil: 'networkidle0' });

const data = await page.evaluate(() => {
  const flyer = document.querySelector('.flyer');
  const children = flyer.children;
  const results = [];
  for (const child of children) {
    const rect = child.getBoundingClientRect();
    results.push({ class: child.className, height: Math.round(rect.height) });
  }
  return results;
});

const total = data.reduce((s, d) => s + d.height, 0);
console.log('A4 target: 1123px');
console.log('Total:', total, 'Overflow:', total - 1123);
console.log('---');
data.forEach(d => console.log(`${d.class}: ${d.height}px`));
await browser.close();
