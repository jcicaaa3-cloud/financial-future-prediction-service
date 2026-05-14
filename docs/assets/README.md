# README visual assets

These assets are intentionally committed because the repository is being used as a portfolio project.
They make the GitHub landing page reviewable without requiring a reviewer to run the app first.

- `github_hero.png`: README hero image.
- `pipeline_flow.gif`: animated service flow with highlighted arrows.
- `architecture_diagram.png`: full architecture overview.
- `dashboard_preview.png`: reviewer-facing dashboard mock preview.
- `api_contract_preview.png`: API request/response preview.
- `github_social_preview.png`: image to upload in GitHub repository settings as the social preview.

Regenerate them with:

```bash
python scripts/render_github_assets.py --force
```
