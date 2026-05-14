# Validation note

The V4 GitHub showcase package was validated in the build environment.

```bash
python -m compileall -q app src scripts tests
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python -m pytest -q
python run_demo.py --company-id C003 --artifact-dir /tmp/v4_verify
python scripts/build_portfolio_snapshot.py --company-id C003
```

Observed results:

```text
pytest: 12 passed
compileall: passed
run_demo: generated request-scoped decision packet, report, dashboard, metrics, model bundle, and monitoring files
portfolio snapshot: examples/portfolio_snapshot/portfolio_dashboard.html generated
```

Expected repository assets:

- `docs/assets/github_hero.png`
- `docs/assets/pipeline_flow.gif`
- `docs/assets/architecture_diagram.png`
- `docs/assets/dashboard_preview.png`
- `docs/assets/github_social_preview.png`

Caveat: sample data is synthetic and only demonstrates the engineering flow.
