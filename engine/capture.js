// Headless Chrome capture for devlog-recorder. node capture.js job.json
// job.mode = "shot"   {url, out, w, h, scroll, full, wait}
// job.mode = "record" {url, out_dir, w, h, dur, wait, keys:[{key,down,up}]}  -> fNNNNN.png + times.json (real timestamps)
const puppeteer = require('puppeteer-core');
const fs = require('fs'), path = require('path');
const CHROME = process.env.CHROME || (process.platform === 'darwin' ? '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
  : process.platform === 'win32' ? 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe' : '/usr/bin/google-chrome');
const job = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const sleep = ms => new Promise(r => setTimeout(r, ms));
(async () => {
  const browser = await puppeteer.launch({ executablePath: CHROME, headless: true, args: [`--window-size=${(job.w || 1280) + 40},${(job.h || 720) + 120}`, '--mute-audio', '--autoplay-policy=no-user-gesture-required'] });
  const page = await browser.newPage();
  await page.setViewport({ width: job.w || 1280, height: job.h || 720, deviceScaleFactor: 1 });
  await page.goto(job.url, { waitUntil: 'networkidle2', timeout: 60000 });
  await sleep((job.wait || 1) * 1000);
  await page.evaluate(() => { for (const b of document.querySelectorAll('button')) { const t = (b.textContent || '').toLowerCase(); if (/accept|agree|got it/.test(t)) { try { b.click(); } catch (e) {} } } });
  if (job.mode === 'shot') {
    if (job.scroll) { await page.evaluate(sel => { const el = document.querySelector(sel); if (el) { el.scrollIntoView(); window.scrollBy(0, -40); } }, job.scroll); await sleep(500); }
    fs.mkdirSync(path.dirname(job.out), { recursive: true });
    await page.screenshot({ path: job.out, fullPage: !!job.full });
    console.log('shot', job.out);
  } else {
    fs.mkdirSync(job.out_dir, { recursive: true });
    try { await page.mouse.click((job.w || 1280) / 2, (job.h || 720) / 2); } catch (e) {}   // focus the page so games get key events
    const t0 = Date.now(); const times = []; let i = 0;
    for (const k of (job.keys || [])) {
      setTimeout(() => page.keyboard.down(k.key).catch(() => {}), k.down);
      setTimeout(() => page.keyboard.up(k.key).catch(() => {}), k.up);
    }
    while (Date.now() - t0 < job.dur * 1000) {
      const shot = await page.screenshot({ type: 'png' });
      times.push((Date.now() - t0) / 1000);
      fs.writeFileSync(path.join(job.out_dir, `f${String(i++).padStart(5, '0')}.png`), shot);
    }
    fs.writeFileSync(path.join(job.out_dir, 'times.json'), JSON.stringify(times));
    console.log('recorded', i, 'frames in', ((Date.now() - t0) / 1000).toFixed(1), 's');
  }
  await browser.close();
})().catch(e => { console.error(e); process.exit(1); });
