# GitHub Pages Live Lab

This directory is the static public demo deployed to GitHub Pages.

It is intentionally browser-only:

- no backend call;
- no API key;
- no real financial data;
- synthetic sample companies only;
- explainable heuristic scoring for product-demo purposes.

Interactive features:

- metric sliders;
- shock scenario buttons;
- decision packet JSON generation;
- batch scoring;
- CSV paste/upload scoring;
- JSON/cURL/CSV copy-download actions.

The real service pipeline is implemented in `app/`, `src/financial_risk_scoring/`, and `run_demo.py`.
