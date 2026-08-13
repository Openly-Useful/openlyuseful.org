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
    required = ["index.html", "styles.css", "favicon.svg", "og.png", "robots.txt", "sitemap.xml", "vercel.json"]
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
    assert "https://openlyuseful.org/og.png" in html

    css = (ROOT / "styles.css").read_text(encoding="utf-8")
    assert "prefers-reduced-motion" in css
    assert "@media (max-width:520px)" in css
    print("Validated Openly Useful landing page")


if __name__ == "__main__":
    main()
