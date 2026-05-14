# V5 — GitHub Pages public demo edition

This release adds a public-facing static site so reviewers can try the project without installing Python.

## Added

- `site/index.html`: GitHub Pages landing page and interactive browser demo.
- `site/styles.css`: responsive portfolio-style UI.
- `site/app.js`: browser-only synthetic scoring simulator and decision packet generator.
- `.github/workflows/pages.yml`: GitHub Pages deployment workflow.
- `docs/assets/github_pages_demo_preview.png`: README preview image for the public demo.
- `docs/github_pages_site_ko.md`: Korean setup guide for GitHub Pages.
- `tests/test_github_pages_site.py`: validation for site files and deployment workflow.

## Positioning

GitHub Pages cannot run the FastAPI backend. The site is intentionally a static demo simulator, while the real Python/FastAPI pipeline remains in `app/`, `src/`, and `run_demo.py`.
