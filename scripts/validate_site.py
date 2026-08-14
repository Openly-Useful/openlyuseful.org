from __future__ import annotations

import json
import zlib
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


def png_rgb_pixels(path: Path) -> tuple[int, int, list[bytes]]:
    data = path.read_bytes()
    assert data[:8] == b"\x89PNG\r\n\x1a\n"
    offset = 8
    width = height = 0
    compressed = bytearray()
    while offset < len(data):
        length = unpack(">I", data[offset : offset + 4])[0]
        chunk_type = data[offset + 4 : offset + 8]
        chunk = data[offset + 8 : offset + 8 + length]
        offset += 12 + length
        if chunk_type == b"IHDR":
            width, height, bit_depth, color_type = unpack(">IIBB", chunk[:10])
            assert bit_depth == 8 and color_type == 2, path
        elif chunk_type == b"IDAT":
            compressed.extend(chunk)
        elif chunk_type == b"IEND":
            break

    raw = zlib.decompress(bytes(compressed))
    stride = width * 3
    rows: list[bytes] = []
    previous = bytearray(stride)
    cursor = 0
    for _ in range(height):
        filter_type = raw[cursor]
        source = raw[cursor + 1 : cursor + 1 + stride]
        cursor += stride + 1
        row = bytearray(stride)
        for index, value in enumerate(source):
            left = row[index - 3] if index >= 3 else 0
            up = previous[index]
            upper_left = previous[index - 3] if index >= 3 else 0
            if filter_type == 0:
                predictor = 0
            elif filter_type == 1:
                predictor = left
            elif filter_type == 2:
                predictor = up
            elif filter_type == 3:
                predictor = (left + up) // 2
            elif filter_type == 4:
                estimate = left + up - upper_left
                distances = (abs(estimate - left), abs(estimate - up), abs(estimate - upper_left))
                predictor = (left, up, upper_left)[distances.index(min(distances))]
            else:
                raise AssertionError(f"Unsupported PNG filter {filter_type}: {path}")
            row[index] = (value + predictor) & 0xFF
        rows.append(bytes(row))
        previous = row
    return width, height, rows


def assert_profile_raster(path: Path, expected_size: int) -> None:
    width, height, rows = png_rgb_pixels(path)
    assert (width, height) == (expected_size, expected_size)

    def pixel(x_unit: int, y_unit: int) -> tuple[int, int, int]:
        x = min(width - 1, round(width * x_unit / 64))
        y = min(height - 1, round(height * y_unit / 64))
        start = x * 3
        return tuple(rows[y][start : start + 3])

    shell = (247, 243, 233)
    green = (36, 122, 75)
    assert pixel(0, 0) == shell, f"{path}: profile canvas must use Shell"
    assert pixel(32, 8) == green, f"{path}: top of institutional O missing"
    assert pixel(32, 18) == shell, f"{path}: institutional counter missing"
    assert pixel(24, 25) == green, f"{path}: left canonical eye missing"
    assert pixel(24, 38) == green, f"{path}: left canonical U stem missing"


def main() -> None:
    validate_brand_geometry()
    validate_brand_system()
    required = [
        "index.html",
        "styles.css",
        "favicon-v3.svg",
        "apple-touch-icon-v1.png",
        "icon-192-v1.png",
        "icon-512-v1.png",
        "site.webmanifest",
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
        "brand/ou-profile-mark-v1.svg",
        "brand/ou-profile-mark-v1.png",
        "brand/profile-mark-raster.html",
        "brand/ou-wordmark-v4.svg",
        "brand/ou-wordmark-reverse-v4.svg",
        "brand/ou-tagline-v4.svg",
        "brand/ou-tagline-reverse-v4.svg",
        "brand/ou-lockup-horizontal-v4.svg",
        "brand/ou-lockup-horizontal-reverse-v4.svg",
        "brand/ou-lockup-stacked-v4.svg",
        "brand/ou-lockup-stacked-reverse-v4.svg",
        "brand/brandkit-open-monitor-v5.png",
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
    assert "/brand/ou-profile-mark-v1.svg" in html
    assert "/apple-touch-icon-v1.png" in html
    assert "/site.webmanifest" in html
    assert "/brand/ou-monitor-bot-v3.svg" in html
    assert "open-shell" not in html

    system_html = (ROOT / "design-system/index.html").read_text(encoding="utf-8")
    system_parser = LandingPageParser()
    system_parser.feed(system_html)
    assert system_parser.title == "Design System — Openly Useful"
    assert "The Open Monitor" in system_html
    assert "/brand/brandkit-open-monitor-v5.png" in system_html
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

    board = ROOT / "brand/brandkit-open-monitor-v5.png"
    assert board.stat().st_size > 100_000
    assert png_dimensions(board) == (1536, 1024)
    assert png_dimensions(ROOT / "brand/monitorfolk-workshop.png") == (704, 1024)
    assert png_dimensions(ROOT / "og-v6.png") == (1200, 630)
    assert_profile_raster(ROOT / "brand/ou-profile-mark-v1.png", 1024)
    assert_profile_raster(ROOT / "apple-touch-icon-v1.png", 180)
    assert_profile_raster(ROOT / "icon-192-v1.png", 192)
    assert_profile_raster(ROOT / "icon-512-v1.png", 512)

    web_manifest = json.loads((ROOT / "site.webmanifest").read_text(encoding="utf-8"))
    assert web_manifest["name"] == "Openly Useful"
    assert web_manifest["background_color"] == "#f7f3e9"
    assert web_manifest["theme_color"] == "#f7f3e9"
    assert {(icon["src"], icon["sizes"]) for icon in web_manifest["icons"]} == {
        ("/icon-192-v1.png", "192x192"),
        ("/icon-512-v1.png", "512x512"),
    }

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
