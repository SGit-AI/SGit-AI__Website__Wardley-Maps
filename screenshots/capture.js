#!/usr/bin/env node
/*
 * capture.js — screenshot every industry resource listed in targets.json
 *
 * WHY THIS IS A SCRIPT AND NOT A FOLDER OF PNGs:
 * the pack was assembled inside a sandbox whose egress proxy allows only
 * package registries. Every third-party host returned ERR_TUNNEL_CONNECTION_FAILED.
 * Rather than fake it, the capture is shipped as code for you to run where
 * the network is open.
 *
 *   npm i playwright && npx playwright install chromium
 *   node capture.js            # all targets
 *   node capture.js 04 07 12   # only these ids (prefix match)
 *
 * Writes <id>.png next to this file and updates captured.json with the
 * status, page title, final URL (after redirects) and capture timestamp of
 * every attempt — including failures. Publish that file; it is the evidence
 * that a screenshot is what the page looked like on the day claimed.
 */
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const DIR = __dirname;
const targets = JSON.parse(fs.readFileSync(path.join(DIR, 'targets.json'), 'utf8'));
const only = process.argv.slice(2);
const list = only.length ? targets.filter(t => only.some(p => t.id.startsWith(p))) : targets;

(async () => {
  // Launch a Chromium that exists. Playwright pins a build number and refuses to run
  // if that exact build is not installed, which is the common case on a machine that
  // already ships a browser (CI images, sandboxes, this repo's own build container).
  // CHROME_PATH, or a Playwright browsers directory, takes precedence over the pin.
  const chromePath = process.env.CHROME_PATH
    || ['/opt/pw-browsers/chromium', '/usr/bin/chromium', '/usr/bin/google-chrome']
       .find(p => fs.existsSync(p));
  const browser = await chromium.launch(chromePath ? { executablePath: chromePath } : {});
  if (chromePath) console.log(`chromium: ${chromePath}`);
  const ctx = await browser.newContext({
    viewport: { width: 1440, height: 900 },
    deviceScaleFactor: 2,              // retina; the PNGs are for a web page
    reducedMotion: 'reduce',
    colorScheme: 'light'               // keep the set visually consistent
  });
  // Where the browser has no egress but the process does — a sandbox with an egress
  // proxy, a CI runner with a network policy — set PROXY_FETCH=1 and every request the
  // page makes is performed by Node's fetch (which honours HTTPS_PROXY) and fulfilled
  // back into the page. Same requests, same responses, same policy: the only thing that
  // moves is which process opens the socket. Off by default; a real browser connection
  // is a truer capture when you can have one.
  if (process.env.PROXY_FETCH) {
    console.log('proxy-fetch: page requests are performed by Node');
    await ctx.route('**/*', async route => {
      const req = route.request();
      try {
        const r = await fetch(req.url(), {
          method: req.method(),
          headers: req.headers(),
          body: ['GET', 'HEAD'].includes(req.method()) ? undefined : req.postDataBuffer(),
          redirect: 'follow',
        });
        const headers = {};
        r.headers.forEach((v, k) => {
          // content-encoding/length describe the wire body Node already decoded.
          if (!['content-encoding', 'content-length'].includes(k.toLowerCase())) headers[k] = v;
        });
        await route.fulfill({
          status: r.status, headers,
          body: Buffer.from(await r.arrayBuffer()),
        });
      } catch (e) {
        await route.abort();
      }
    });
  }

  const results = [];

  for (const t of list) {
    const rec = { id: t.id, name: t.name, url: t.url, licence: t.licence, attribution: t.attribution };
    const page = await ctx.newPage();
    try {
      const resp = await page.goto(t.url, { waitUntil: 'networkidle', timeout: 60000 });
      rec.status = resp ? resp.status() : null;
      rec.finalUrl = page.url();
      rec.title = await page.title();
      if (t.dismiss) {                 // cookie banners etc.
        for (const sel of t.dismiss) {
          try { await page.click(sel, { timeout: 2500 }); } catch (_) {}
        }
      }
      await page.waitForTimeout(t.wait || 3000);
      const file = path.join(DIR, `${t.id}.png`);
      await page.screenshot({ path: file, fullPage: !!t.fullPage });
      rec.file = `${t.id}.png`;
      rec.bytes = fs.statSync(file).size;
      rec.capturedAt = new Date().toISOString();
      rec.ok = true;
    } catch (err) {
      rec.ok = false;
      rec.error = String(err).split('\n')[0].slice(0, 200);
    }
    results.push(rec);
    console.log(`${rec.ok ? 'ok  ' : 'FAIL'}  ${t.id}  ${rec.error || rec.title || ''}`);
    await page.close();
  }

  fs.writeFileSync(path.join(DIR, 'captured.json'), JSON.stringify(results, null, 2));
  const ok = results.filter(r => r.ok).length;
  console.log(`\n${ok}/${results.length} captured -> captured.json`);
  await browser.close();
})();
