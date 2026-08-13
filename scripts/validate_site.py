from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path

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


def main() -> None:
    required = [
        "index.html",
        "styles.css",
        "favicon.svg",
        "og.png",
        "og-v2.png",
        "robots.txt",
        "sitemap.xml",
        "vercel.json",
        "brand/README.md",
        "brand/open-shell-mark.svg",
        "brand/open-shell-reverse.svg",
        "brand/shellfolk-builder.svg",
        "brand/brandkit-overview.png",
        "design-system/README.md",
        "design-system/index.html",
        "design-system/tokens.css",
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
    assert "https://openlyuseful.org/og-v2.png" in html
    assert "/design-system" in parser.links
    assert "/brand/open-shell-mark.svg" in html

    system_html = (ROOT / "design-system/index.html").read_text(encoding="utf-8")
    system_parser = LandingPageParser()
    system_parser.feed(system_html)
    assert system_parser.title == "Design System — Openly Useful"
    assert "The Open Shell" in system_html
    assert "/brand/brandkit-overview.png" in system_html
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

    board = ROOT / "brand/brandkit-overview.png"
    assert board.stat().st_size > 500_000
    print("Validated Openly Useful landing page")


if __name__ == "__main__":
    main()
