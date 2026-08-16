from __future__ import annotations

import json
import re
from pathlib import Path
from xml.etree import ElementTree

ROOT = Path(__file__).resolve().parents[1]

ACTIVE_SURFACES = [
    "open-source.html",
    "studio.html",
    "design-system/index.html",
    "brand/brandkit.html",
    "brand/og-card.html",
    "brand/media-kit.html",
]

DEPRECATED_PUBLIC_PATHS = [
    "/brand/ou-monitor-mark.svg",
    "/brand/ou-monitor-reverse.svg",
    "/brand/ou-monitor-character.svg",
    "/brand/ou-monitor-bot.svg",
    "/brand/open-shell-mark.svg",
    "/brand/open-shell-reverse.svg",
    "/brand/shellfolk-builder.svg",
    "/brand/brandkit-open-monitor.png",
    "/brand/brandkit-open-monitor-v3.png",
    "/brand/brandkit-open-monitor-v4.png",
    "/favicon.svg",
    "/favicon-v3.svg",
    "/og.png",
    "/og-v2.png",
    "/og-v3.png",
    "/og-v4.png",
    "/og-v5.png",
    "/og-v6.png",
]


def read(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8")


def lockup_count(html: str) -> int:
    return len(re.findall(r'class="[^"]*\bou-lockup\b[^"]*"', html))


def validate_outlined_svg(relative_path: str, expected_view_box: str) -> None:
    root = ElementTree.parse(ROOT / relative_path).getroot()
    assert root.get("viewBox") == expected_view_box, relative_path
    assert root.get("shape-rendering") == "geometricPrecision", relative_path
    assert not any(element.tag.rsplit("}", 1)[-1] == "text" for element in root.iter())
    assert any(element.tag.rsplit("}", 1)[-1] == "path" for element in root.iter())


def direct_path_data(element: ElementTree.Element) -> list[str]:
    return [
        child.get("d", "")
        for child in element
        if child.tag.rsplit("}", 1)[-1] == "path"
    ]


def validate_shared_outlines() -> None:
    wordmark = ElementTree.parse(ROOT / "brand/ou-wordmark-v4.svg").getroot()
    tagline = ElementTree.parse(ROOT / "brand/ou-tagline-v4.svg").getroot()
    wordmark_paths = direct_path_data(wordmark)
    tagline_paths = direct_path_data(tagline)
    assert len(wordmark_paths) == 13
    assert len(tagline_paths) == 27

    for relative_path in [
        "brand/ou-lockup-horizontal-v4.svg",
        "brand/ou-lockup-horizontal-reverse-v4.svg",
    ]:
        root = ElementTree.parse(ROOT / relative_path).getroot()
        groups = [direct_path_data(element) for element in root if element.tag.rsplit("}", 1)[-1] == "g"]
        assert wordmark_paths in groups, f"{relative_path}: wordmark outlines diverged"

    for relative_path in [
        "brand/ou-lockup-stacked-v4.svg",
        "brand/ou-lockup-stacked-reverse-v4.svg",
    ]:
        root = ElementTree.parse(ROOT / relative_path).getroot()
        groups = [direct_path_data(element) for element in root if element.tag.rsplit("}", 1)[-1] == "g"]
        assert wordmark_paths in groups, f"{relative_path}: wordmark outlines diverged"
        assert tagline_paths in groups, f"{relative_path}: tagline outlines diverged"


def validate_brand_system() -> None:
    manifest = json.loads(read("brand/manifest.json"))
    assert manifest["brandVersion"] == "3.1.0"
    assert manifest["canonicalName"] == "Openly Useful"
    assert manifest["canonicalTagline"] == "Useful things, openly made."

    assets = manifest["assets"]
    for public_path in assets.values():
        assert public_path.startswith("/")
        assert (ROOT / public_path.removeprefix("/")).is_file(), public_path

    active_text = "\n".join(read(path) for path in ACTIVE_SURFACES)
    for deprecated in DEPRECATED_PUBLIC_PATHS:
        assert deprecated not in active_text, f"Deprecated brand path remains active: {deprecated}"
    assert "ou-lockup__" not in active_text
    assert manifest["canonicalName"] in active_text
    assert manifest["canonicalTagline"] in active_text

    institutional = assets["institutional"]
    reverse = assets["reverse"]
    character = assets["character"]
    monitorfolk = assets["monitorfolk"]
    horizontal = assets["horizontalLockup"]
    horizontal_reverse = assets["horizontalLockupReverse"]
    stacked = assets["stackedLockup"]

    home = read("open-source.html")
    assert lockup_count(home) == 3
    assert home.count(horizontal) == 1
    assert home.count(horizontal_reverse) == 1
    assert home.count(stacked) == 1
    assert home.count(monitorfolk) == 1

    studio = read("studio.html")
    assert lockup_count(studio) == 2
    assert studio.count(horizontal_reverse) == 2
    assert horizontal not in studio

    specimen = read("design-system/index.html")
    assert lockup_count(specimen) == 4
    assert institutional in specimen
    assert horizontal_reverse in specimen
    assert character in specimen
    assert assets["brandBoard"] in specimen

    board = read("brand/brandkit.html")
    assert lockup_count(board) == 1
    assert board.count(stacked) == 1
    assert board.count(institutional) == 6
    assert board.count(character) == 1

    social = read("brand/og-card.html")
    assert lockup_count(social) == 1
    assert social.count(stacked) == 1

    brand_css = read("design-system/brand.css")
    tokens = read("design-system/tokens.css")
    for required in [
        "@font-face",
        ".ou-lockup--horizontal",
        ".ou-lockup--stacked",
        ".ou-visually-hidden",
    ]:
        assert required in brand_css
    for required in [
        "--ou-brand-horizontal-height: 2.125rem",
        "--ou-brand-stacked-width: 8.400113",
        "--ou-brand-display-unit:",
        "--ou-brand-board-unit: 5.25rem",
        "--ou-brand-social-unit: 3.625rem",
    ]:
        assert required in tokens

    other_css = read("styles.css") + read("studio.css") + board + social
    assert not re.search(r"\.ou-lockup(?:--horizontal|--stacked)?\s*\{", other_css)

    validate_outlined_svg("brand/ou-wordmark-v4.svg", "0 0 8018.29 880")
    validate_outlined_svg("brand/ou-wordmark-reverse-v4.svg", "0 0 8018.29 880")
    validate_outlined_svg("brand/ou-tagline-v4.svg", "0 0 15040 963")
    validate_outlined_svg("brand/ou-tagline-reverse-v4.svg", "0 0 15040 963")
    validate_outlined_svg("brand/ou-lockup-horizontal-v4.svg", "0 0 354.502 64")
    validate_outlined_svg("brand/ou-lockup-horizontal-reverse-v4.svg", "0 0 354.502 64")
    validate_outlined_svg("brand/ou-lockup-stacked-v4.svg", "0 0 8400.113 5733.643")
    validate_outlined_svg("brand/ou-lockup-stacked-reverse-v4.svg", "0 0 8400.113 5733.643")
    validate_outlined_svg("brand/ou-profile-mark-v1.svg", "0 0 64 64")
    validate_shared_outlines()

    assert manifest["lockups"]["profile"] == {
        "contexts": ["GitHub organization", "browser icon", "Apple touch icon", "installed web app"],
        "asset": "/brand/ou-profile-mark-v1.svg",
        "uploadAsset": "/brand/ou-profile-mark-v1.png",
        "viewBox": "0 0 64 64",
        "background": "#f7f3e9",
    }

    source_specs = manifest["sourceSpecifications"]
    assert source_specs["wordmark"] == {
        "font": "Atkinson Hyperlegible Next",
        "weight": 780,
        "tracking": "-0.062em",
        "scaleX": 1.34,
    }
    assert source_specs["tagline"] == {
        "font": "IBM Plex Mono",
        "weight": 700,
        "tracking": "-0.035em",
    }

    fonts = manifest["fonts"]
    for public_path in fonts.values():
        assert public_path.startswith("/")
        assert (ROOT / public_path.removeprefix("/")).is_file(), public_path
    for key in ["wordmark", "technical"]:
        assert (ROOT / fonts[key].removeprefix("/")).stat().st_size > 20_000

    vercel = read("vercel.json")
    for deprecated in DEPRECATED_PUBLIC_PATHS:
        assert f'"source": "{deprecated}"' in vercel, f"Missing compatibility redirect: {deprecated}"


def main() -> None:
    validate_brand_system()
    print("Validated Openly Useful brand system")


if __name__ == "__main__":
    main()
