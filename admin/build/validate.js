#!/usr/bin/env node
// wardley-maps.sgit.ai pre-release gate. Run from anywhere: node admin/build/validate.js
//
// The first four checks are the house gate, inherited from pki.sgit.ai and
// graphs.sgit.ai unchanged in intent:
//   1. version agreement — admin/build/version.txt vs every page's version badge,
//      the versions table, llms.txt, llms-full.txt and index.md
//   2. internal links — every relative href/src in every .html file resolves to a
//      file in the tree (fragments stripped; external and mailto links skipped)
//   3. canonical host — every <link rel="canonical"> and og:url points at the host
//      in CNAME, and every page declares one
//   4. key-leak tripwire — nothing in the tree may look like an sgit vault key
//
// Three more are specific to this site, and each exists because this site makes a
// promise the others do not:
//   5. licence stamp — every raw markdown document under briefs/ carries the CC BY 4.0
//      stamp. The site sits inside a CC BY-SA ecosystem (see about/licensing.html);
//      an unstamped document is the first step towards a mixed, unlabelled licence.
//   6. maps ship their source — every maps/*.mmd has a maps/*.svg beside it, and no
//      rendered .svg contains Mermaid's `error-text`. A broken wardley-beta source
//      renders a byte-identical "Syntax error in text" SVG with no line number and no
//      non-zero exit, which in a batch render looks exactly like success. See
//      briefs/05__maps-and-rendering.md §3.
//   7. resource pages carry a verification date — every page under resources/ has a
//      `data-verified` stamp. It is the site's whole differentiator in that category
//      and the one rule 04__ says has no exceptions.
//
// Any failure exits 1: no tag, no publish.
'use strict';
const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..', '..');
const errors = [];

function walk(dir, out = []) {
  for (const name of fs.readdirSync(dir)) {
    if (name === '.git' || name === '.github' || name === 'node_modules' || name === '.sg_vault') continue;
    const p = path.join(dir, name);
    const st = fs.statSync(p);
    if (st.isDirectory()) walk(p, out);
    else out.push(p);
  }
  return out;
}
const rel = f => path.relative(ROOT, f);

const files = walk(ROOT);
const htmlFiles = files.filter(f => f.endsWith('.html'));

// --- 1. version agreement -------------------------------------------------
const VERSION = fs.readFileSync(path.join(ROOT, 'admin/build/version.txt'), 'utf8').trim();
if (!/^v\d+\.\d+\.\d+$/.test(VERSION)) {
  errors.push(`version.txt does not carry a vX.Y.Z version: "${VERSION}"`);
}
for (const f of htmlFiles) {
  const t = fs.readFileSync(f, 'utf8');
  const badges = [...t.matchAll(/class="ver"[^>]*>(v\d+\.\d+\.\d+)</g)].map(m => m[1]);
  for (const b of badges) if (b !== VERSION) {
    errors.push(`${rel(f)}: version badge ${b} != ${VERSION}`);
  }
}
for (const extra of ['llms.txt', 'llms-full.txt', 'index.md']) {
  const t = fs.readFileSync(path.join(ROOT, extra), 'utf8');
  if (!t.includes(VERSION)) errors.push(`${extra} does not mention ${VERSION}`);
}
const versTable = fs.readFileSync(path.join(ROOT, 'admin/versions.html'), 'utf8');
if (!versTable.includes(`class="vnum">${VERSION}<`)) {
  errors.push(`admin/versions.html has no row for ${VERSION}`);
}
// each release appears exactly once — a blanket version-bump sed that touches the
// history table produces duplicates, which shipped once on the NHI site
const rows = [...versTable.matchAll(/class="vnum">(v\d+\.\d+\.\d+)</g)].map(m => m[1]);
for (const v of rows) if (rows.filter(x => x === v).length > 1) {
  errors.push(`admin/versions.html lists ${v} more than once`);
  break;
}

// --- 2. internal links ----------------------------------------------------
for (const f of htmlFiles) {
  const t = fs.readFileSync(f, 'utf8');
  const dir = path.dirname(f);
  for (const m of t.matchAll(/(?:href|src)="([^"#]+)(?:#[^"]*)?"/g)) {
    const target = m[1];
    if (/^(https?:|mailto:|data:|\/\/)/.test(target) || target === '') continue;
    if (!fs.existsSync(path.resolve(dir, target))) {
      errors.push(`${rel(f)}: broken link -> ${target}`);
    }
  }
}

// --- 3. canonical host ----------------------------------------------------
const HOST = fs.readFileSync(path.join(ROOT, 'CNAME'), 'utf8').trim();
if (!/^[a-z0-9.-]+$/.test(HOST)) errors.push(`CNAME does not carry a hostname: "${HOST}"`);
for (const f of htmlFiles) {
  const t = fs.readFileSync(f, 'utf8');
  const claimed = [
    ...[...t.matchAll(/<link[^>]+rel="canonical"[^>]+href="([^"]+)"/g)].map(m => m[1]),
    ...[...t.matchAll(/<meta[^>]+property="og:url"[^>]+content="([^"]+)"/g)].map(m => m[1]),
  ];
  for (const url of claimed) if (!url.startsWith(`https://${HOST}/`)) {
    errors.push(`${rel(f)}: canonical/og:url is not on ${HOST} -> ${url}`);
  }
  if (!/rel="canonical"/.test(t)) errors.push(`${rel(f)}: no canonical link`);
}

// --- 4. key-leak tripwire -------------------------------------------------
const KEY_SHAPE = /[A-Za-z0-9_-]{20,}:[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}/;
for (const f of files) {
  if (/\.(png|jpg|jpeg|gif|webp|ico|svg|woff2?|zip|pdf)$/.test(f)) continue;
  if (KEY_SHAPE.test(fs.readFileSync(f, 'utf8'))) {
    errors.push(`${rel(f)}: contains a vault-key-shaped string`);
  }
}

// --- 5. licence stamp on the raw briefs -----------------------------------
const STAMP = 'Creative Commons Attribution 4.0 International licence (CC BY 4.0)';
for (const f of files.filter(f => f.startsWith(path.join(ROOT, 'briefs')) && f.endsWith('.md'))) {
  if (!fs.readFileSync(f, 'utf8').includes(STAMP)) {
    errors.push(`${rel(f)}: missing the CC BY 4.0 licence stamp`);
  }
}

// --- 6. every map ships its source, and renders ---------------------------
const MAPS = path.join(ROOT, 'maps');
for (const f of fs.readdirSync(MAPS).filter(n => n.endsWith('.mmd'))) {
  const svg = path.join(MAPS, f.replace(/\.mmd$/, '.svg'));
  if (!fs.existsSync(svg)) {
    errors.push(`maps/${f}: no rendered .svg beside it (run bin/render-maps.sh)`);
    continue;
  }
  if (fs.readFileSync(svg, 'utf8').includes('error-text')) {
    errors.push(`maps/${path.basename(svg)}: rendered a Mermaid syntax error, not a map`);
  }
}
for (const f of fs.readdirSync(MAPS).filter(n => n.endsWith('.svg'))) {
  if (!fs.existsSync(path.join(MAPS, f.replace(/\.svg$/, '.mmd')))) {
    errors.push(`maps/${f}: rendered without its source — every map ships its .mmd`);
  }
}

// --- 7. resource pages carry a verification date --------------------------
// verification.html is the exception, and for the right reason: its date comes from the
// live link-check report it renders, so a stamp baked into the HTML would be the one
// verification date on the site that could go stale without anyone noticing.
for (const f of htmlFiles.filter(f => f.startsWith(path.join(ROOT, 'resources'))
                                   && path.basename(f) !== 'verification.html')) {
  const t = fs.readFileSync(f, 'utf8');
  if (!/data-verified="\d{4}-\d{2}-\d{2}"/.test(t)) {
    errors.push(`${rel(f)}: no data-verified stamp (every resource page carries one)`);
  }
}

// --- report ---------------------------------------------------------------
if (errors.length) {
  console.error(`validate: ${errors.length} error(s)`);
  for (const e of errors) console.error('  ✗ ' + e);
  process.exit(1);
}
const mmd = fs.readdirSync(MAPS).filter(n => n.endsWith('.mmd')).length;
console.log(`validate: OK — ${VERSION} on ${HOST}, ${htmlFiles.length} pages, ${mmd} maps ` +
            `(source + render), links resolve, briefs stamped, no key-shaped strings`);
