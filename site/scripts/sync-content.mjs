// Transforms the repo's `<Project Name>/README.md` folders into Starlight
// content under src/content/docs/. Source of truth stays at the repo root;
// everything this script writes is generated and gitignored.
//
// Outputs:
//   - src/content/docs/<slug>/index.md   (+ co-located images for Astro's pipeline)
//   - public/files/<slug>/...            (non-image assets referenced from pages)
//   - .generated/redirects.json          (old mkdocs URL -> new URL map)
//   - .generated/sidebar.json            (ordered sidebar for astro.config.mjs)
//   - .generated/sync-report.txt         (warnings: fixed/missing links and images)

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const SITE_DIR = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const ROOT = path.resolve(SITE_DIR, '..');
const DOCS_OUT = path.join(SITE_DIR, 'src/content/docs');
const FILES_OUT = path.join(SITE_DIR, 'public/files');
const GENERATED = path.join(SITE_DIR, '.generated');
const SITE_URL = 'https://grantcurell.com';
const GITHUB_REPO = 'https://github.com/grantcurell/projects';
const GITHUB_BRANCH = 'main';

const IMAGE_EXTS = new Set(['.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp', '.avif', '.bmp', '.ico']);
const MAX_ASSET_BYTES = 50 * 1024 * 1024;

// Directory names never traversed (anywhere in the tree).
const EXCLUDED_DIR_NAMES = new Set([
  '.git', '.github', '.idea', '.vscode', '.astro', '.cursor', 'node_modules',
  '__pycache__', 'dist', 'venv', '.venv', 'site',
]);

// Repo-relative paths excluded from page discovery and asset copying.
// Seeded from the old mkdocs file_transfer.py ignore list: vendored sources,
// datasets, and binaries that should never become site content.
const IGNORED_PATHS = [
  'Reverse Engineering OpenSHMEM/SOS-main',
  'Reverse Engineering OpenSHMEM/libfabric-main',
  'Custom NVMe Debug Driver/linux_source',
  'Swap Kernel on Rocky 9/source',
  'Aircraft Detection/data_set',
  'How Does SIFT Work/output_images',
  'Understand and Run LINPACK/binary',
  'Windows Workstation Deployer for Offline Environments/roles',
  'Build Preboot Environment with Ansible/pxe_kickstart_ansible/roles',
  'OpenFlow on 4112F-ON/angular',
];

const warnings = [];
const warn = (msg) => {
  warnings.push(msg);
  console.warn(`[sync] ${msg}`);
};

const isIgnored = (absPath) => {
  const rel = path.relative(ROOT, absPath);
  if (rel.startsWith('..')) return true;
  if (rel.split(path.sep).some((seg) => EXCLUDED_DIR_NAMES.has(seg) || seg.startsWith('.'))) return true;
  const relPosix = rel.split(path.sep).join('/');
  return IGNORED_PATHS.some((p) => relPosix === p || relPosix.startsWith(p + '/'));
};

const slugify = (name) =>
  name
    .toLowerCase()
    .replace(/['’]/g, '')
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '') || 'untitled';

// ---------------------------------------------------------------------------
// Page discovery
// ---------------------------------------------------------------------------

/** @typedef {{ dirRel: string[], slugParts: string[], sourceFile: string, oldPath: string[] }} Page */

/** @type {Page[]} */
const pages = [];

const discover = (absDir, relParts) => {
  const entries = fs.readdirSync(absDir, { withFileTypes: true });
  const dirs = entries
    .filter((e) => e.isDirectory() && !isIgnored(path.join(absDir, e.name)))
    .map((e) => e.name)
    .sort((a, b) => a.localeCompare(b, 'en', { sensitivity: 'base' }));
  for (const dir of dirs) {
    const childAbs = path.join(absDir, dir);
    const childRel = [...relParts, dir];
    if (fs.existsSync(path.join(childAbs, 'README.md'))) {
      pages.push({
        dirRel: childRel,
        slugParts: childRel.map(slugify),
        sourceFile: path.join(childAbs, 'README.md'),
        oldPath: childRel,
      });
    }
    discover(childAbs, childRel);
  }
};

// ---------------------------------------------------------------------------
// Markdown transformation
// ---------------------------------------------------------------------------

const tryDecode = (s) => {
  try {
    return decodeURIComponent(s);
  } catch {
    return s;
  }
};

const isExternal = (target) =>
  /^(https?:|mailto:|ftp:|data:|#|\/)/i.test(target);

const stripTitleSuffix = (target) => target.replace(/\s+"[^"]*"$/, '');

const extractTitle = (body, fallback) => {
  const m = body.match(/^#\s+(.+?)\s*$/m);
  return m ? m[1].replace(/[#*`]/g, '').trim() : fallback;
};

const stripFirstH1 = (body) => body.replace(/^\s*#\s+.+?\r?\n/, '');

const extractDescription = (body) => {
  const lines = body.split(/\r?\n/);
  let para = '';
  let inFence = false;
  for (const line of lines) {
    const t = line.trim();
    if (t.startsWith('```') || t.startsWith('~~~')) {
      inFence = !inFence;
      continue;
    }
    if (inFence) continue;
    if (!t || /^[#>|\-*\d<!\[]/.test(t) || t.startsWith('![')) {
      if (para) break;
      continue;
    }
    para += (para ? ' ' : '') + t;
    if (para.length > 220) break;
  }
  let text = para
    .replace(/!\[[^\]]*\]\([^)]*\)/g, '')
    .replace(/\[([^\]]*)\]\([^)]*\)/g, '$1')
    .replace(/[`*_]/g, '')
    .replace(/<[^>]+>/g, '')
    .replace(/\s+/g, ' ')
    .trim();
  if (text.length > 160) {
    text = text.slice(0, 157).replace(/\s+\S*$/, '') + '...';
  }
  return text;
};

/** Recursively search a project dir for a file matching basename (case-insensitive). */
const findByBasename = (rootDir, basename) => {
  const matches = [];
  const walk = (dir) => {
    let entries;
    try {
      entries = fs.readdirSync(dir, { withFileTypes: true });
    } catch {
      return;
    }
    for (const e of entries) {
      const abs = path.join(dir, e.name);
      if (isIgnored(abs)) continue;
      if (e.isDirectory()) walk(abs);
      else if (e.name.toLowerCase() === basename.toLowerCase()) matches.push(abs);
    }
  };
  walk(rootDir);
  return matches;
};

const yamlStr = (s) => JSON.stringify(s ?? '');

const escapeHtml = (s) =>
  s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');

/** Folder on GitHub that contains this page's source README or markdown file. */
const githubFolderUrl = (sourceFile) => {
  const rel = path.relative(ROOT, path.dirname(sourceFile));
  if (!rel || rel === '.') return `${GITHUB_REPO}/tree/${GITHUB_BRANCH}`;
  return `${GITHUB_REPO}/tree/${GITHUB_BRANCH}/${rel.split(path.sep).map(encodeURIComponent).join('/')}`;
};

const githubFolderLabel = (sourceFile) => {
  const rel = path.relative(ROOT, path.dirname(sourceFile));
  if (!rel || rel === '.') return 'projects';
  return rel.split(path.sep).join('/');
};

const githubSourceLinkHtml = (sourceFile) => {
  const url = githubFolderUrl(sourceFile);
  const label = githubFolderLabel(sourceFile);
  return `<p class="source-repo-link"><a href="${url}" target="_blank" rel="noopener noreferrer" aria-label="View ${escapeHtml(label)} on GitHub"><svg class="source-repo-link__icon" aria-hidden="true" viewBox="0 0 16 16" width="16" height="16"><path fill="currentColor" d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0 0 16 8c0-4.42-3.58-8-8-8z"/></svg><span class="source-repo-link__text">View on GitHub</span><code class="source-repo-link__path">${escapeHtml(label)}</code></a></p>`;
};

const pageUrl = (slugParts) => (slugParts.length ? `/${slugParts.join('/')}/` : '/');

/** Map from absolute README path -> page (for .md link rewriting). */
const pagesBySource = new Map();
/** Extra .md pages discovered via links, keyed by absolute source path. */
const extraPages = new Map();

const transformPage = (page) => {
  const srcDir = path.dirname(page.sourceFile);
  const outDir = path.join(DOCS_OUT, ...page.slugParts);
  const outFile = path.join(outDir, 'index.md');
  fs.mkdirSync(outDir, { recursive: true });

  let body = fs.readFileSync(page.sourceFile, 'utf8');
  // Normalize potential BOM
  body = body.replace(/^\uFEFF/, '');

  const folderName = page.dirRel[page.dirRel.length - 1] ?? "Grant Curell's Projects";
  const title = extractTitle(body, folderName);
  body = stripFirstH1(body);
  const description = extractDescription(body);

  const pageId = page.dirRel.join('/') || '(root)';

  // Mask fenced code blocks and inline code spans so link/image rewriting
  // never touches code samples (e.g. JSX `<img>` snippets in tutorials).
  const masked = [];
  const mask = (s) =>
    s.replace(/```[\s\S]*?```|~~~[\s\S]*?~~~|`[^`\n]+`/g, (m) => {
      masked.push(m);
      return `\u0000MASK${masked.length - 1}\u0000`;
    });
  const unmask = (s) => s.replace(/\u0000MASK(\d+)\u0000/g, (_, i) => masked[+i]);
  body = mask(body);

  const copyImage = (relTarget) => {
    const abs = path.resolve(srcDir, relTarget);
    const dest = path.join(outDir, relTarget);
    fs.mkdirSync(path.dirname(dest), { recursive: true });
    fs.copyFileSync(abs, dest);
  };

  const copyAsset = (absSource, relForUrl) => {
    const size = fs.statSync(absSource).size;
    if (size > MAX_ASSET_BYTES) {
      warn(`${pageId}: asset too large, skipped: ${relForUrl} (${(size / 1e6).toFixed(0)} MB)`);
      return null;
    }
    const dest = path.join(FILES_OUT, ...page.slugParts, relForUrl);
    fs.mkdirSync(path.dirname(dest), { recursive: true });
    fs.copyFileSync(absSource, dest);
    return encodeURI(`/files/${page.slugParts.join('/')}/${relForUrl.split(path.sep).join('/')}`);
  };

  // --- images: ![alt](target) --- (regex tolerates one level of parens in URLs)
  body = body.replace(/!\[([^\]]*)\]\(((?:[^()]|\([^()]*\))+)\)/g, (full, alt, rawTarget) => {
    let target = stripTitleSuffix(rawTarget.trim()).replace(/^<|>$/g, '');
    if (isExternal(target)) return full;
    const decoded = tryDecode(target).replace(/^\.\//, '');
    const ext = path.extname(decoded).toLowerCase();
    const abs = path.resolve(srcDir, decoded);

    if (fs.existsSync(abs) && IMAGE_EXTS.has(ext)) {
      copyImage(decoded);
      return `![${alt}](${encodeURI(decoded)})`;
    }

    // Image syntax pointing at a non-image file (mis-authored) -> regular link.
    if (fs.existsSync(abs) && !IMAGE_EXTS.has(ext)) {
      const url = copyAsset(abs, decoded);
      warn(`${pageId}: image syntax pointed at non-image, converted to link: ${decoded}`);
      return url ? `[${alt || path.basename(decoded)}](${url})` : alt;
    }

    // Missing image: try to locate it by basename within the project.
    const matches = findByBasename(srcDir, path.basename(decoded)).filter((m) =>
      IMAGE_EXTS.has(path.extname(m).toLowerCase())
    );
    if (matches.length === 1) {
      const fixedRel = path.relative(srcDir, matches[0]).split(path.sep).join('/');
      copyImage(fixedRel);
      warn(`${pageId}: fixed image path ${decoded} -> ${fixedRel}`);
      return `![${alt}](${encodeURI(fixedRel)})`;
    }

    warn(`${pageId}: MISSING image dropped: ${decoded}`);
    return alt ? `*${alt}*` : '';
  });

  // --- HTML <img src="..."> (rare; not handled by Astro's md pipeline) ---
  body = body.replace(/(<img\b[^>]*\bsrc=")([^"]+)(")/gi, (full, pre, src, post) => {
    if (isExternal(src)) return full;
    const decoded = tryDecode(src).replace(/^\.\//, '');
    const abs = path.resolve(srcDir, decoded);
    if (!fs.existsSync(abs)) {
      warn(`${pageId}: MISSING <img> src left as-is: ${decoded}`);
      return full;
    }
    const url = copyAsset(abs, decoded);
    return url ? `${pre}${url}${post}` : full;
  });

  // --- regular links: [text](target) ---
  body = body.replace(/(^|[^!])\[([^\]]+)\]\(((?:[^()]|\([^()]*\))+)\)/g, (full, prefix, text, rawTarget) => {
    let target = stripTitleSuffix(rawTarget.trim()).replace(/^<|>$/g, '');
    if (isExternal(target) || !target) return full;
    const [pathPart, anchor = ''] = target.split('#');
    if (!pathPart) return full;
    const decoded = tryDecode(pathPart).replace(/^\.\//, '');
    const abs = path.resolve(srcDir, decoded);
    const hash = anchor ? `#${anchor}` : '';

    if (!fs.existsSync(abs)) {
      warn(`${pageId}: broken relative link left as-is: ${decoded}`);
      return full;
    }

    // Directory link -> page link if that directory is a page.
    const stats = fs.statSync(abs);
    if (stats.isDirectory()) {
      const readme = path.join(abs, 'README.md');
      const known = pagesBySource.get(readme);
      if (known) return `${prefix}[${text}](${pageUrl(known.slugParts)}${hash})`;
      warn(`${pageId}: link to non-page directory left as-is: ${decoded}`);
      return full;
    }

    if (path.extname(decoded).toLowerCase() === '.md') {
      const known = pagesBySource.get(abs);
      if (known) return `${prefix}[${text}](${pageUrl(known.slugParts)}${hash})`;
      // Non-README markdown file: turn it into an extra page under this project.
      let extra = extraPages.get(abs);
      if (!extra) {
        const base = slugify(path.basename(decoded, '.md'));
        extra = {
          dirRel: [...page.dirRel, path.basename(decoded, '.md')],
          slugParts: [...page.slugParts, base],
          sourceFile: abs,
          // Old mkdocs URL for Foo/bar.md was /Foo/bar/
          oldPath: [...page.dirRel, path.basename(decoded, '.md')],
        };
        extraPages.set(abs, extra);
        pagesBySource.set(abs, extra);
      }
      return `${prefix}[${text}](${pageUrl(extra.slugParts)}${hash})`;
    }

    // Any other file: copy to public/files and rewrite.
    const url = copyAsset(abs, decoded);
    return url ? `${prefix}[${text}](${url})` : full;
  });

  const jsonLd = JSON.stringify({
    '@context': 'https://schema.org',
    '@type': 'TechArticle',
    headline: title,
    description: description || undefined,
    url: `${SITE_URL}${pageUrl(page.slugParts)}`,
    author: { '@type': 'Person', name: 'Grant Curell', url: SITE_URL },
    inLanguage: 'en',
  });

  const frontmatter = [
    '---',
    `title: ${yamlStr(title)}`,
    description ? `description: ${yamlStr(description)}` : null,
    'head:',
    '  - tag: script',
    '    attrs:',
    '      type: application/ld+json',
    `    content: ${yamlStr(jsonLd)}`,
    '---',
  ]
    .filter(Boolean)
    .join('\n');

  body = unmask(body);
  const sourceLink = githubSourceLinkHtml(page.sourceFile);
  fs.writeFileSync(outFile, `${frontmatter}\n\n${sourceLink}\n\n${body.trimStart()}`);
  return { title };
};

// ---------------------------------------------------------------------------
// Main
// ---------------------------------------------------------------------------

fs.rmSync(DOCS_OUT, { recursive: true, force: true });
fs.rmSync(FILES_OUT, { recursive: true, force: true });
fs.mkdirSync(DOCS_OUT, { recursive: true });
fs.mkdirSync(GENERATED, { recursive: true });

discover(ROOT, []);

// Slug collision guard
const seen = new Map();
for (const p of pages) {
  const key = p.slugParts.join('/');
  const n = seen.get(key) ?? 0;
  if (n > 0) p.slugParts[p.slugParts.length - 1] += `-${n + 1}`;
  seen.set(key, n + 1);
}

for (const p of pages) pagesBySource.set(p.sourceFile, p);

const titles = new Map();
for (const p of pages) {
  titles.set(p, transformPage(p).title);
}
// Extra pages can themselves reference more md files; drain the queue.
const processedExtra = new Set();
let pending = [...extraPages.values()];
while (pending.length) {
  const batch = pending.filter((p) => !processedExtra.has(p.sourceFile));
  pending = [];
  for (const p of batch) {
    processedExtra.add(p.sourceFile);
    titles.set(p, transformPage(p).title);
  }
  pending = [...extraPages.values()].filter((p) => !processedExtra.has(p.sourceFile));
}

// --- homepage from root README.md ---
{
  const rootReadme = path.join(ROOT, 'README.md');
  const homePage = {
    dirRel: [],
    slugParts: [],
    sourceFile: rootReadme,
    oldPath: [],
  };
  // transformPage writes to DOCS_OUT/index.md because slugParts is empty
  const { title } = transformPage(homePage);
  titles.set(homePage, title);
}

// --- redirects map (old mkdocs URLs used the raw folder names) ---
const redirects = [];
for (const p of [...pages, ...extraPages.values()]) {
  const oldPath = `/${p.oldPath.join('/')}/`;
  const newUrl = pageUrl(p.slugParts);
  if (oldPath.toLowerCase() !== newUrl.toLowerCase()) {
    redirects.push({ from: oldPath, to: `${SITE_URL}${newUrl}` });
  }
}
fs.writeFileSync(path.join(GENERATED, 'redirects.json'), JSON.stringify(redirects, null, 2));

// --- sidebar (mirrors old mkdocs nav: alphabetical, nested groups) ---
const topLevel = new Map(); // first dir component -> entries
const buildSidebar = () => {
  /** node: { label, page?, children: Map } */
  const rootNode = { children: new Map() };
  for (const p of [...pages, ...extraPages.values()]) {
    let node = rootNode;
    for (let i = 0; i < p.dirRel.length; i++) {
      const part = p.dirRel[i];
      if (!node.children.has(part)) node.children.set(part, { label: part, children: new Map() });
      node = node.children.get(part);
    }
    node.page = p;
  }
  const toEntries = (node) => {
    const entries = [];
    const keys = [...node.children.keys()].sort((a, b) =>
      a.localeCompare(b, 'en', { sensitivity: 'base' })
    );
    for (const key of keys) {
      const child = node.children.get(key);
      const label = child.page ? titles.get(child.page) ?? key : key;
      if (child.children.size === 0) {
        entries.push({ label, link: pageUrl(child.page.slugParts) });
      } else {
        const items = toEntries(child);
        if (child.page) items.unshift({ label: 'Overview', link: pageUrl(child.page.slugParts) });
        entries.push({ label, items, collapsed: true });
      }
    }
    return entries;
  };
  return toEntries(rootNode);
};
fs.writeFileSync(path.join(GENERATED, 'sidebar.json'), JSON.stringify(buildSidebar(), null, 2));

fs.writeFileSync(path.join(GENERATED, 'sync-report.txt'), warnings.join('\n') + '\n');

console.log(
  `[sync] ${pages.length} pages + ${extraPages.size} extra md pages, ` +
    `${redirects.length} redirects, ${warnings.length} warnings (see site/.generated/sync-report.txt)`
);
