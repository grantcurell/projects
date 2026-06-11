# Deployment Guide

How the site gets from this repo to https://grantcurell.com, and the one-time
manual steps required to finish the cutover from the old mkdocs setup.

## How it works

- Content lives at the repo root as `<Project Name>/README.md` folders. Keep
  writing notes exactly as before.
- On every push to `main`, the `Deploy site` GitHub Action:
  1. runs `site/scripts/sync-content.mjs` (transforms the folders into
     Starlight pages, copies images and referenced files, generates the
     sidebar and a redirect map),
  2. runs `astro build`,
  3. runs `site/scripts/emit-redirects.mjs` (writes redirect pages at the old
     mkdocs URLs),
  4. force-pushes the built site to the `main` branch of
     `grantcurell/grantcurell.github.io`, which GitHub Pages serves.
- `site/public/CNAME` keeps the custom domain bound across deploys.

## Local preview

```bash
cd site
npm install        # first time only
npm run dev        # syncs content, serves at http://localhost:4321 with hot reload
```

For an exact replica of production output:

```bash
npm run build      # full pipeline including redirect pages
npm run preview    # serves dist/ at http://localhost:4321
```

After a sync, check `site/.generated/sync-report.txt` for warnings about
broken or fixed links and images.

## One-time setup steps

### 1. Deploy key so the Action can push to grantcurell.github.io

```bash
ssh-keygen -t ed25519 -C "deploy projects -> grantcurell.github.io" -f deploy_key -N ""
```

- In **grantcurell.github.io** repo: Settings > Deploy keys > Add deploy key.
  Paste `deploy_key.pub`, check **Allow write access**.
- In **projects** repo: Settings > Secrets and variables > Actions > New
  repository secret. Name: `PAGES_DEPLOY_KEY`, value: contents of `deploy_key`
  (the private key).
- Delete both files locally afterwards.

### 2. DNS for grantcurell.com

At your registrar, create:

| Type  | Host | Value                                          |
|-------|------|------------------------------------------------|
| A     | @    | 185.199.108.153                                |
| A     | @    | 185.199.109.153                                |
| A     | @    | 185.199.110.153                                |
| A     | @    | 185.199.111.153                                |
| CNAME | www  | grantcurell.github.io                          |

### 3. GitHub Pages custom domain

In the **grantcurell.github.io** repo: Settings > Pages:

- Custom domain: `grantcurell.com` (GitHub will verify DNS, may take a few
  minutes).
- Check **Enforce HTTPS** once the certificate is provisioned.

After this, `grantcurell.github.io` automatically 301-redirects to
`grantcurell.com`, so every existing inbound link keeps working and passes
its ranking signal to the new domain.

### 4. Search engine re-verification

The old verification files (`google3c20e65f49ac224c.html`, `BingSiteAuth.xml`)
are already carried over in `site/public/`, so the existing
`grantcurell.github.io` properties stay verified.

**Google Search Console** (https://search.google.com/search-console):

1. Add a new property for `grantcurell.com`. Prefer the **Domain** property
   type (requires one DNS TXT record at your registrar; covers www and http/https
   variants in one shot). If you'd rather not touch DNS again, use a URL-prefix
   property: Google will offer an HTML file - drop it into `site/public/` and
   redeploy.
2. Submit the sitemap: `https://grantcurell.com/sitemap-index.xml`.
3. In the old `grantcurell.github.io` property, run **Settings > Change of
   address** pointing at the new `grantcurell.com` property. This tells Google
   to transfer rankings explicitly.

**Bing Webmaster Tools** (https://www.bing.com/webmasters):

1. Add `grantcurell.com` as a new site. Easiest path: use the
   "Import from Google Search Console" option after the Google setup, or
   verify with the existing `BingSiteAuth.xml` (already deployed).
2. Submit `https://grantcurell.com/sitemap-index.xml`.

DuckDuckGo needs nothing: its results come from Bing's index, so the Bing
setup covers it. Brave, Ecosia, and others consume the same sitemap/robots
standards automatically.

### 5. Retire the old mkdocs source (optional)

The `dev` branch of `grantcurell.github.io` (mkdocs config, `deploy.sh`,
`file_transfer.py`, `scan_folders.py`) is now obsolete. Delete it whenever
you're comfortable; the `main` branch gets fully overwritten by each deploy.
