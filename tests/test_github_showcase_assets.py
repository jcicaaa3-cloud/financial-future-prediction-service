from pathlib import Path


def test_github_showcase_assets_exist() -> None:
    root = Path(__file__).resolve().parents[1]
    assets = root / "docs" / "assets"
    required = [
        assets / "github_hero.png",
        assets / "dashboard_preview.png",
        assets / "pipeline_flow.gif",
        assets / "architecture_diagram.png",
        assets / "github_social_preview.png",
    ]
    missing = [str(path) for path in required if not path.exists()]
    assert not missing
    assert all(path.stat().st_size > 1024 for path in required)


def test_readme_references_existing_visual_assets() -> None:
    root = Path(__file__).resolve().parents[1]
    readme = (root / "README.md").read_text(encoding="utf-8")
    for rel in [
        "docs/assets/github_hero.png",
        "docs/assets/dashboard_preview.png",
        "docs/assets/pipeline_flow.gif",
        "docs/assets/architecture_diagram.png",
    ]:
        assert rel in readme
        assert (root / rel).exists()
