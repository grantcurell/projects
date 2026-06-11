// Writes static redirect pages into dist/ at the old mkdocs URLs
// (e.g. "/Adding Hashing to OpenSwitch/") pointing at the new slugged URLs.
// GitHub Pages can't issue server-side 301s for these, so we use instant
// meta-refresh + rel=canonical, which Google and Bing treat as a permanent
// redirect signal. Runs after `astro build` (see package.json).

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const SITE_DIR = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const DIST = path.join(SITE_DIR, 'dist');
const redirects = JSON.parse(
  fs.readFileSync(path.join(SITE_DIR, '.generated/redirects.json'), 'utf8')
);

const esc = (s) =>
  s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');

let written = 0;
for (const { from, to } of redirects) {
  // "from" is a raw old path like "/Folder Name/Sub Name/"
  const outDir = path.join(DIST, ...from.split('/').filter(Boolean));
  const outFile = path.join(outDir, 'index.html');
  if (fs.existsSync(outFile)) {
    console.warn(`[redirects] skipping ${from}: would overwrite an existing page`);
    continue;
  }
  fs.mkdirSync(outDir, { recursive: true });
  fs.writeFileSync(
    outFile,
    `<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Redirecting\u2026</title>
<link rel="canonical" href="${esc(to)}">
<meta http-equiv="refresh" content="0; url=${esc(to)}">
<script>location.replace(${JSON.stringify(to)});</script>
</head>
<body>
<p>This page has moved to <a href="${esc(to)}">${esc(to)}</a>.</p>
</body>
</html>
`
  );
  written++;
}

console.log(`[redirects] wrote ${written}/${redirects.length} redirect pages into dist/`);
