# grantcurell.com site

Astro Starlight site that fronts the project notes in this repo. Pages are
generated at build time from the `<Project Name>/README.md` folders at the
repo root - nothing in `src/content/docs/` is hand-written or committed.

```bash
npm install
npm run dev      # sync content + dev server at http://localhost:4321
npm run build    # sync + astro build + old-URL redirect pages -> dist/
npm run preview  # serve dist/ exactly as production
```

| Path                          | Purpose                                                  |
|-------------------------------|----------------------------------------------------------|
| `scripts/sync-content.mjs`    | Folders -> Starlight pages, images, assets, sidebar, redirect map |
| `scripts/emit-redirects.mjs`  | Writes redirect HTML at old mkdocs URLs into `dist/`     |
| `.generated/sync-report.txt`  | Warnings from the last sync (broken/fixed links)         |
| `public/`                     | Static files: CNAME, robots.txt, verification files, OG image |

Deployment is automatic on push to `main` (see `.github/workflows/deploy.yml`
and `DEPLOYMENT.md`).
