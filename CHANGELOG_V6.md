# V6 Live Lab Upgrade

This release turns the GitHub Pages demo from a visual landing page into a hands-on browser lab.

## Added

- Direct interactive live lab on GitHub Pages.
- Scenario presets: Growth upside, Margin shock, Liquidity crunch, Market stress, Disclosure event.
- Slider-based company scoring with immediate risk packet generation.
- Batch scoring table with downloadable CSV results.
- Paste/upload CSV scoring inside the browser.
- Copyable decision packet JSON and cURL request preview.
- Feature-contribution preview for explanation storytelling.
- Root `index.html` fallback so branch-based Pages deployments do not accidentally render the README instead of the live lab.
- More robust Pages workflow that publishes the `site/` directory through GitHub Actions.

## Positioning

The Pages demo remains intentionally static. It does not claim to run the real model backend. The public page is a product-style reviewer experience, while the real Python/FastAPI pipeline lives in `app/`, `src/`, and `run_demo.py`.
