# AGENTS.md

## Cursor Cloud specific instructions

### What this repo is
A large collection of personal technical notes, where each top-level `<Project Name>/README.md` folder is content. The one deployable product is the documentation website in `site/` (Astro + Starlight), which generates its pages at build time from those folders. The Angular app under `OpenFlow on 4112F-ON/angular` and the Python `requirements.txt` files are isolated example artifacts tied to physical hardware, not part of the site.

### The site (`site/`) — the product
- Requires Node 22 + npm (already available in the environment). Commands and pipeline are documented in `site/README.md` and `site/DEPLOYMENT.md`; don't duplicate them.
- `npm run dev`/`npm run build` automatically run the content sync (`scripts/sync-content.mjs`) first, so there is no separate sync step needed before running.
- There are no `lint` or `test` scripts defined for the site — `site/package.json` only has `sync`/`dev`/`start`/`build`/`preview`/`astro`.
- Dev server (`npm run dev`) serves at `http://localhost:4321`. Cold start is slow (~40s) because the content sync transforms ~130 note folders and many images; wait for the `ready` line before hitting it.
- Non-obvious: **search is disabled in dev mode**. Pagefind search only works against a production build — run `npm run build` then `npm run preview` to test search locally.
- `astro-expressive-code` prints harmless `[WARN]` lines for unknown code-block languages (e.g. `dhcp`); these are not errors and the build still completes.
- Sync warnings (broken/fixed links and images) are written to `site/.generated/sync-report.txt`.
