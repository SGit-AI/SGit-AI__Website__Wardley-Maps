#!/usr/bin/env node
// The link-verification job. Run: node bin/verify-links.js [--out data/link-check.json]
//
// Why this exists, and why no sibling site has one. The Wardley ecosystem's own
// canonical indexes are wrong: as of August 2026 awesome-wardley-maps, Wikipedia and
// Simon Wardley's own resources page all still list MapKeep, MapScript, both doctrine
// assessment tools, the Map Camp Slack invite and the Leading Edge Forum course as
// live. All five are dead. A site that curates that ecosystem while making the same
// mistake has no standing to point it out.
//
// So: every external URL this site publishes gets fetched on a schedule, and the run
// date is published next to the result. A resource page's verification stamp is not
// decoration — it is the site's whole competitive position in that category
// (briefs/04__job-b__industry-resources.md §1).
//
// Method, stated because a verification you cannot audit is not one:
//   · Every https? href in every .html file in the tree, deduplicated, fragment stripped.
//   · HEAD first, GET on any non-2xx — a lot of hosts refuse HEAD but serve GET.
//   · Redirects followed; the final URL is recorded, so a link that now lands somewhere
//     else shows up as a redirect rather than silently passing.
//   · A UA string that identifies this job and links back here.
//   · SKIP_HOSTS are recorded as "skipped", never as "ok". LinkedIn, SlideShare and
//     YouTube block automated retrieval; claiming a 200 we did not get would be worse
//     than admitting we cannot check. These need a human, and the report says so.
//   · A 401/403/429/451/999 is recorded as "blocked", not "error". Medium serves 403 to
//     everything without a browser, and calling that a dead link would make this report
//     wrong in exactly the way it exists to complain about. "Blocked" means we could not
//     check; only a 404, a 5xx or a connection failure means the link is broken.
//   · Our own host is skipped entirely. Those links are checked properly by
//     admin/build/validate.js against the files on disk, which is a stronger check than
//     fetching a deployment that may not have happened yet.
//   · Failures are published exactly like successes. captured.json in screenshots/ does
//     the same thing for screenshots, for the same reason.
'use strict';
const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const OUT = process.argv.includes('--out')
  ? process.argv[process.argv.indexOf('--out') + 1]
  : path.join(ROOT, 'data/link-check.json');

const UA = 'wardley-maps.sgit.ai link-verification (+https://wardley-maps.sgit.ai/resources/verification.html)';
const CONCURRENCY = 8;
const TIMEOUT_MS = 20000;

const SELF_HOST = fs.readFileSync(path.join(ROOT, 'CNAME'), 'utf8').trim();

// A response that means "not to a robot", rather than "not here".
const BLOCKED_STATUS = new Set([401, 403, 429, 451, 999]);

// Hosts that refuse automated retrieval outright. Recorded as skipped, never as ok.
const SKIP_HOSTS = [
  'www.linkedin.com', 'linkedin.com',
  'www.slideshare.net', 'slideshare.net',
  'www.youtube.com', 'youtube.com', 'youtu.be', 'www.youtube-nocookie.com',
  'discord.com', 'discord.gg',
];

function walk(dir, out = []) {
  for (const name of fs.readdirSync(dir)) {
    if (['.git', '.github', 'node_modules', '.sg_vault'].includes(name)) continue;
    const p = path.join(dir, name);
    fs.statSync(p).isDirectory() ? walk(p, out) : out.push(p);
  }
  return out;
}

// --- collect ---------------------------------------------------------------
const urls = new Map();  // url -> Set(pages that link it)
for (const f of walk(ROOT).filter(f => f.endsWith('.html'))) {
  const rel = path.relative(ROOT, f);
  for (const m of fs.readFileSync(f, 'utf8').matchAll(/(?:href|src)="(https?:\/\/[^"]+)"/g)) {
    const u = m[1].split('#')[0].replace(/&amp;/g, '&');
    if (!urls.has(u)) urls.set(u, new Set());
    urls.get(u).add(rel);
  }
}

async function check(url) {
  let host;
  try { host = new URL(url).host; } catch { return { url, state: 'invalid' }; }
  if (host === SELF_HOST) {
    return { url, state: 'self', reason: 'our own host — checked against the files on disk by validate.js' };
  }
  if (SKIP_HOSTS.includes(host)) {
    return { url, state: 'skipped', reason: 'host blocks automated retrieval — needs a human' };
  }
  for (const method of ['HEAD', 'GET']) {
    const ac = new AbortController();
    const timer = setTimeout(() => ac.abort(), TIMEOUT_MS);
    try {
      const r = await fetch(url, {
        method, redirect: 'follow', signal: ac.signal,
        headers: { 'user-agent': UA, accept: '*/*' },
      });
      clearTimeout(timer);
      if (!r.ok && method === 'HEAD') continue;
      const final = r.url && r.url.split('#')[0];
      const state = r.ok ? 'ok' : BLOCKED_STATUS.has(r.status) ? 'blocked' : 'error';
      return {
        url, state, status: r.status, method,
        ...(state === 'blocked'
          ? { reason: 'the host refused an automated request — not evidence the link is dead' }
          : {}),
        ...(final && final !== url ? { final_url: final } : {}),
      };
    } catch (e) {
      clearTimeout(timer);
      if (method === 'GET') return { url, state: 'error', error: String(e.message || e) };
    }
  }
  return { url, state: 'error', error: 'unreachable' };
}

(async () => {
  const list = [...urls.keys()].sort();
  const results = new Array(list.length);
  let next = 0;
  await Promise.all(Array.from({ length: CONCURRENCY }, async () => {
    while (next < list.length) {
      const i = next++;
      results[i] = { ...await check(list[i]), linked_from: [...urls.get(list[i])].sort() };
      process.stderr.write(`${results[i].state === 'ok' ? '.' : results[i].state === 'skipped' ? 's' : 'X'}`);
    }
  }));
  process.stderr.write('\n');

  const tally = results.reduce((a, r) => (a[r.state] = (a[r.state] || 0) + 1, a), {});
  const report = {
    schema: 'wardley-maps-link-check/v1',
    run_at: new Date().toISOString().replace(/\.\d+Z$/, 'Z'),
    method: 'HEAD then GET, redirects followed, 20s timeout. A 401/403/429/451/999 is ' +
            'recorded as blocked (the host refused a robot), not as error (the link is ' +
            'broken). Hosts that block outright are skipped, never ok. Our own host is ' +
            'skipped: validate.js checks those against the files on disk.',
    user_agent: UA,
    skip_hosts: SKIP_HOSTS,
    count: results.length,
    tally,
    results,
  };
  fs.mkdirSync(path.dirname(OUT), { recursive: true });
  fs.writeFileSync(OUT, JSON.stringify(report, null, 1) + '\n');
  console.log(`link-check: ${results.length} URLs — ` +
    Object.entries(tally).map(([k, v]) => `${v} ${k}`).join(', ') + ` -> ${path.relative(ROOT, OUT)}`);
  // A dead link is a finding to publish, not a build failure: the whole point is that
  // the ecosystem's links rot, and a red pipeline would tempt somebody to delete the
  // evidence. Exit 0 always; the report carries the verdict.
})();
