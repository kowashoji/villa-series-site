# villa-series.jp

Static site deployed by Cloudflare Pages (project `villa-series`). Every push to `main` goes live.

- Pages: the `.html` files in `public/` (Cloudflare build output directory: `public`) (URLs without `.html`, e.g. `/bianca`).
- Photos, fonts and PDFs: separate Cloudflare Pages project `villa-series-assets` (https://villa-series-assets.pages.dev).
- Vacancies: edit `public/vacancies.json` only.
- Source: `_src/` (`gen2.py` + `data.py` regenerate the pages).
