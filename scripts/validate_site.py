from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
from struct import unpack

from validate_brand_geometry import validate_brand_geometry
from validate_brand_system import validate_brand_system

ROOT = Path(__file__).resolve().parents[1]


class LandingPageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.title = ""
        self.in_title = False
        self.ids: set[str] = set()
        self.links: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if tag == "title":
            self.in_title = True
        if values.get("id"):
            self.ids.add(values["id"] or "")
        if tag == "a" and values.get("href"):
            self.links.append(values["href"] or "")

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self.in_title = False

    def handle_data(self, data: str) -> None:
        if self.in_title:
            self.title += data


def png_dimensions(path: Path) -> tuple[int, int]:
    with path.open("rb") as image:
        assert image.read(8) == b"\x89PNG\r\n\x1a\n"
        assert image.read(4) == b"\x00\x00\x00\r"
        assert image.read(4) == b"IHDR"
        return unpack(">II", image.read(8))


def main() -> None:
    validate_brand_geometry()
    validate_brand_system()
    required = [
        "index.html",
        "styles.css",
        "favicon-v3.svg",
        "og-v6.png",
        "robots.txt",
        "sitemap.xml",
        "vercel.json",
        "brand/README.md",
        "brand/manifest.json",
        "brand/ou-monitor-mark-v3.svg",
        "brand/ou-monitor-reverse-v3.svg",
        "brand/ou-monitor-character-v3.svg",
        "brand/ou-monitor-bot-v3.svg",
        "brand/ou-wordmark-v4.svg",
        "brand/ou-wordmark-reverse-v4.svg",
        "brand/ou-tagline-v4.svg",
        "brand/ou-tagline-reverse-v4.svg",
        "brand/ou-lockup-horizontal-v4.svg",
        "brand/ou-lockup-horizontal-reverse-v4.svg",
        "brand/ou-lockup-stacked-v4.svg",
        "brand/ou-lockup-stacked-reverse-v4.svg",
        "brand/brandkit-open-monitor-v4.png",
        "brand/monitorfolk-workshop.png",
        "brand/brandkit.html",
        "brand/og-card.html",
        "design-system/README.md",
        "design-system/ARCHITECTURE.md",
        "design-system/index.html",
        "design-system/brand.css",
        "design-system/tokens.css",
        "scripts/build_brand_vectors.py",
        "scripts/requirements-vector.txt",
    ]
    missing = [name for name in required if not (ROOT / name).is_file()]
    if missing:
        raise AssertionError(f"Missing required site files: {', '.join(missing)}")

    html = (ROOT / "index.html").read_text(encoding="utf-8")
    parser = LandingPageParser()
    parser.feed(html)
    assert parser.title == "Openly Useful — Useful things, openly made."
    assert {"top", "projects", "principles"}.issubset(parser.ids)
    assert "https://github.com/openly-useful" in [link.lower() for link in parser.links]
    assert "mailto:hello@openlyuseful.org" in parser.links
    assert "https://openlyuseful.org/og-v6.png" in html
    assert "/design-system" in parser.links
    assert "/brand/ou-lockup-horizontal-v4.svg" in html
    assert "/brand/ou-lockup-stacked-v4.svg" in html
    assert "/brand/ou-monitor-bot-v3.svg" in html
    assert "open-shell" not in html

    system_html = (ROOT / "design-system/index.html").read_text(encoding="utf-8")
    system_parser = LandingPageParser()
    system_parser.feed(system_html)
    assert system_parser.title == "Design System — Openly Useful"
    assert "The Open Monitor" in system_html
    assert "/brand/brandkit-open-monitor-v4.png" in system_html
    assert "/brand/ou-monitor-character-v3.svg" in system_html
    assert "Comfortable sharing" in system_html

    css = (ROOT / "styles.css").read_text(encoding="utf-8")
    assert "prefers-reduced-motion" in css
    assert "forced-colors" in css
    assert "@media (max-width:520px)" in css

    tokens = (ROOT / "design-system/tokens.css").read_text(encoding="utf-8")
    for token in [
        "--ou-color-shell-50",
        "--ou-color-ink-900",
        "--ou-color-terminal-600",
        "--ou-color-process-600",
        "--ou-font-sans",
        "--ou-space-4",
        "--ou-focus-ring",
    ]:
        assert token in tokens

    board = ROOT / "brand/brandkit-open-monitor-v4.png"
    assert board.stat().st_size > 100_000
    assert png_dimensions(board) == (1536, 1024)
    assert png_dimensions(ROOT / "brand/monitorfolk-workshop.png") == (704, 1024)
    assert png_dimensions(ROOT / "og-v6.png") == (1200, 630)

    board_source = (ROOT / "brand/brandkit.html").read_text(encoding="utf-8")
    assert board_source.count("/brand/ou-monitor-mark-v3.svg") == 6
    assert board_source.count("/brand/ou-lockup-stacked-v4.svg") == 1
    assert board_source.count("/brand/ou-monitor-character-v3.svg") == 1
    assert "brandkit-open-monitor-source-tmp" not in board_source

    social_source = (ROOT / "brand/og-card.html").read_text(encoding="utf-8")
    assert social_source.count("/brand/ou-lockup-stacked-v4.svg") == 1
    print("Validated Openly Useful landing page")


if __name__ == "__main__":
    main()
